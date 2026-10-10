import unittest

from action_context import ActionContext
from command_parser import CommandParser
from confrontation import Enemy
from game_state import GameState
from visual_session import VisualSession
from world import Room, GameObject, PassageState, ROOM_ALIASES, OFFICIAL_ROOM_IDS


def small_world(*rooms):
    game = GameState()
    game.rooms = {r.room_id: r for r in rooms}
    game.current_location = rooms[0].room_id
    game.visited_rooms = {game.current_location}
    return game


class MapInfrastructureTests(unittest.TestCase):
    def test_aliases_do_not_duplicate_or_move_rooms(self):
        game = GameState(configuration='prototype')
        self.assertEqual(len(OFFICIAL_ROOM_IDS), 58)
        self.assertEqual(set(game.rooms), set(ROOM_ALIASES))
        self.assertEqual(len({id(r) for r in game.rooms.values()}), 6)
        for old, official in ROOM_ALIASES.items():
            self.assertIs(game.get_room(old), game.get_room(official))
            self.assertEqual(game.resolve_room_id(official), old)
        self.assertEqual(game.current_location, 'entrance')
        with self.assertRaises(KeyError):
            game.get_room('L12')
        with self.assertRaises(KeyError):
            game.current_location = 'E01'
        self.assertEqual(game.current_location, 'entrance')

    def test_official_rooms_accept_legacy_references(self):
        game = small_world(Room('T01', 'Vestíbulo', ''), Room('U01', 'Galeria', ''))
        self.assertIs(game.get_room('entrance'), game.rooms['T01'])
        game.current_location = 'upper_hall'
        self.assertEqual(game.current_location, 'U01')
        game.rooms['entrance'] = Room('entrance', 'Duplicata', '')
        with self.assertRaises(ValueError):
            game.get_room('T01')

    def test_official_destinations_normalize_visits_and_memory(self):
        game = GameState()
        game.current_location = 'T01'
        game.rooms['entrance'].exits['norte'] = 'T02'
        enemy = Enemy('vigia', sound='passos')
        game.get_room('T02').enemies = [enemy]
        game.exploration.perception()
        signals = game.exploration.memory.contexts['sound:entrance']['signals']
        self.assertEqual(signals[0][1], 'main_hall')
        CommandParser(game).execute('norte')
        self.assertEqual(game.current_location, 'main_hall')
        self.assertIn('main_hall', game.visited_rooms)
        self.assertNotIn('T02', game.visited_rooms)

    def test_nine_named_destinations_without_extra_rooms_in_campaign(self):
        center = Room('T02', 'Salão', 'Um salão silencioso.')
        names = [('T01', 'vestíbulo'), ('T03', 'sala de estar'), ('T04', 'sala de jantar'),
                 ('T08', 'escritório'), ('T09', 'biblioteca'), ('T11', 'banheiro social'),
                 ('T12', 'sala de manutenção'), ('U01', 'galeria superior'), ('B07', 'arquivo do porão')]
        destinations = [Room(key, name, 'Um espaço de teste.') for key, name in names]
        for room in destinations:
            center.connect(room, 'via_' + room.room_id.lower(), name='passagem para ' + room.name)
        game = small_world(center, *destinations)
        parser = CommandParser(game)
        for key, name in names:
            game.current_location = 'T02'
            parser.execute('ir para a ' + name)
            self.assertEqual(game.current_location, key)
        self.assertEqual(len(center.exits), 9)
        self.assertEqual(len(GameState().rooms), 58)

    def test_ambiguity_continuation_keeps_caution_and_turns(self):
        start, office, cellar = [Room(n, n, '') for n in ('start', 'office', 'cellar')]
        for destination, name in [(office, 'escritório'), (cellar, 'porão')]:
            door = GameObject('porta do ' + name, '', openable=True)
            door.opened = True
            start.connect(destination, 'via_' + destination.room_id, door=door)
        for command in ('passar pela porta', 'esgueirar pela porta'):
            game = small_world(start, office, cellar)
            parser = CommandParser(game)
            self.assertIn('Joseph:', parser.execute(command))
            self.assertEqual(game.turn_count, 0)
            parser.execute('a do escritório')
            self.assertEqual(game.current_location, 'office')
            self.assertEqual(game.turn_count, 1)
            self.assertEqual(game.hidden, command.startswith('esgueirar'))

    def test_display_name_and_physical_name_both_resolve_and_listen(self):
        start, end = Room('start', 'A', ''), Room('end', 'B', '')
        door = GameObject('porta do porão', '', openable=True)
        door.opened = True
        start.connect(end, 'via_b', door=door, name='corredor de serviço')
        game = small_world(start, end)
        for name in ('porta do porão', 'corredor de serviço'):
            game.current_location = 'start'
            self.assertEqual(game.exploration.door_direction(name), 'via_b')
            CommandParser(game).execute('passar pela ' + name)
            self.assertEqual(game.current_location, 'end')

    def test_shared_lock_open_close_and_block_both_sides(self):
        a, b = Room('T02', 'Salão', ''), Room('T09', 'Biblioteca', '')
        door = GameObject('porta da biblioteca', '', locked=True, lock_id='test.lock')
        a.connect(b, 'biblioteca', reverse='salao', door=door)
        game = small_world(a, b)
        key = GameObject('chave de teste', '', portable=True, key_lock_ids={'test.lock'})
        game.add_item(key.name); game.item_objects[key.name] = key
        game.current_location = 'T09'
        parser = CommandParser(game)
        parser.execute('usar chave de teste na porta da biblioteca')
        self.assertFalse(a.exit_doors['biblioteca'].locked)
        self.assertTrue(a.exit_doors['biblioteca'].opened)
        parser.execute('fechar porta da biblioteca')
        self.assertFalse(a.exit_doors['biblioteca'].opened)
        door.blocked = True
        for location, direction in [('T02', 'biblioteca'), ('T09', 'salao')]:
            game.current_location = location
            parser.execute('ir ' + direction)
            self.assertEqual(game.current_location, location)
        self.assertIs(a.exit_doors['biblioteca'], b.exit_doors['salao'])

    def test_shortcut_release_shared_without_puzzle(self):
        a, b = Room('a', 'A', ''), Room('b', 'B', '')
        state = PassageState('test.shortcut', enabled=False)
        a.connect(b, 'norte', reverse='sul', state=state)
        game = small_world(a, b); parser = CommandParser(game)
        for location, command in [('a', 'norte'), ('b', 'sul')]:
            game.current_location = location
            parser.execute(command)
            self.assertEqual(game.current_location, location)
        state.enabled = True
        parser.execute('sul')
        self.assertEqual(game.current_location, 'a')
        parser.execute('norte')
        self.assertEqual(game.current_location, 'b')

    def test_fall_is_not_walkable_or_a_patrol_route(self):
        a, b = Room('E07', 'Casinha', ''), Room('B01', 'Câmara', '')
        state = PassageState('C_B01_E07', kind='fall')
        a.connect(b, 'queda', state=state)
        game = small_world(a, b)
        CommandParser(game).execute('ir queda')
        self.assertEqual(game.current_location, 'E07')
        enemy = Enemy('vigia'); a.enemies.append(enemy)
        self.assertFalse(game.exploration._step(a, enemy, 'B01'))
        self.assertEqual(b.exits, {})
        with self.assertRaises(ValueError):
            a.connect(b, 'baixo', reverse='cima', state=state)
        self.assertNotIn('baixo', a.exits)

    def test_secret_guessing_never_discovers_or_unlocks(self):
        a, b = Room('B10', 'Câmara fria', ''), Room('L01', 'Acesso oculto', '')
        state = PassageState('C_B10_L01', known=False, enabled=False)
        door = GameObject('porta secreta', 'MARCADOR_SECRETO', openable=True)
        door.opened = True
        a.connect(b, 'norte', reverse='sul', door=door, name='entrada oculta', state=state)
        game = small_world(a, b); parser = CommandParser(game)
        b.enemies.append(Enemy('vigia secreto', sound='passos'))
        for command in ('norte', 'ir L01', 'ir acesso oculto', 'passar pela entrada oculta',
                        'atravessar porta secreta', 'abrir porta secreta', 'examinar porta secreta',
                        'esgueirar norte', 'ouvir porta secreta', 'ajuda', 'olhar em volta'):
            response = parser.execute(command)
            self.assertNotIn('MARCADOR_SECRETO', response)
            self.assertNotIn('passos', response)
            self.assertEqual(game.current_location, 'B10')
            self.assertFalse(state.known)
            self.assertFalse(state.enabled)
            self.assertNotIn(door.name, game.visible_objects())
        self.assertEqual(ActionContext().passages(game, 'entrada oculta'), [])
        state.reveal()
        self.assertIn(door.name, a.objects)
        self.assertIn(door.name, b.objects)
        parser.execute('norte')
        self.assertEqual(game.current_location, 'B10')
        state.enabled = True
        b.enemies.clear()
        parser.execute('norte'); parser.execute('sul')
        self.assertEqual(game.current_location, 'B10')

    def test_visual_session_keeps_prototype_and_history(self):
        session = VisualSession(); session.start_campaign(configuration='prototype')
        game = session.game
        self.assertEqual(game.current_location, 'entrance')
        for command, destination in [('norte', 'main_hall'), ('oeste', 'kitchen'),
                                     ('leste', 'main_hall'), ('leste', 'office'),
                                     ('oeste', 'main_hall'), ('subir a escadaria', 'upper_hall'),
                                     ('voltar ao salão', 'main_hall')]:
            session.execute(command)
            self.assertEqual(game.current_location, destination)
            self.assertNotIn('Saídas:', session.last_message)
            self.assertNotIn('DICA:', session.history[-1][1])
        door = game.get_room('B07').exit_doors['sul']
        self.assertIs(door, game.get_room('T02').exit_doors['norte'])
        self.assertTrue(door.locked)
        self.assertEqual(len(game.rooms), 6)


if __name__ == '__main__':
    unittest.main()
