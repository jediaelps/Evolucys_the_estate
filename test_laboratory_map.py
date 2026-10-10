import unittest
from command_parser import CommandParser
from game_state import GameState
from world import OFFICIAL_ROOM_IDS, ROOM_ALIASES

NAMES = ('Acesso Oculto', 'Corredor do Laboratório', 'Recepção Técnica', 'Sala de Observação',
         'Laboratório Principal', 'Laboratório Biológico', 'Enfermaria e Cirurgia',
         'Câmara de Contenção', 'Biotério', 'Controle de Energia', 'Arquivo Científico', 'Rota de Fuga')
PAIRS = [('L01','L02'), ('L02','L03'), ('L03','L04'), ('L04','L05'), ('L05','L06'),
         ('L06','L09'), ('L09','L11'), ('L05','L07'), ('L07','L08'), ('L08','L11'),
         ('L03','L10'), ('L10','L05'), ('L11','L12')]


def official(rid):
    return ROOM_ALIASES.get(rid, rid)


def reachable(game, start, initial=False):
    seen, todo = set(), [start]
    while todo:
        rid = todo.pop()
        if rid in seen:
            continue
        seen.add(rid)
        room = game.get_room(rid)
        todo.extend(official(dest) for direction, dest in room.exits.items()
                    if not initial or not room.passage_failure(direction))
    return seen


class LaboratoryTests(unittest.TestCase):
    def test_names_environment_and_exact_internal_edges(self):
        game = GameState()
        actual = set()
        for n, name in enumerate(NAMES, 1):
            rid = f'L{n:02}'
            room = game.get_room(rid)
            self.assertEqual(room.name, name)
            self.assertTrue(room.description)
            self.assertFalse(room.enemies)
            self.assertTrue(all(o in room.exit_doors.values() or o.text is not None or (rid == 'L07' and o.name == 'kit médico') for o in room.objects.values()))
            actual.update(frozenset((rid, dest)) for dest in room.exits.values() if dest.startswith('L'))
        self.assertEqual(actual, {frozenset(pair) for pair in PAIRS})

    def test_every_internal_connection_by_name_both_ways(self):
        for a, b in PAIRS:
            for origin, target in ((a,b),(b,a)):
                with self.subTest(origin=origin, target=target):
                    game = GameState()
                    game.current_location = origin
                    response = CommandParser(game).execute('ir para ' + game.get_room(target).name)
                    self.assertEqual(game.current_location, target, response)
                    self.assertFalse(game.game_over)
        self.assertEqual(set(GameState().get_room('L12').exits.values()), {'L11'})

    def test_secret_remains_blocked_even_if_revealed_and_can_be_released_in_fixture(self):
        game = GameState()
        state = game.get_room('B10').exit_states['via_l01']
        door = game.get_room('B10').exit_doors['via_l01']
        self.assertFalse(state.known)
        self.assertFalse(state.enabled)
        self.assertTrue(door.locked)
        for reveal in (False, True):
            if reveal:
                state.reveal()
            for origin, commands in (
                ('B10', ('ir para o laboratório', 'atravessar a porta', 'ir via_l01', 'fugir via_l01', 'esgueirar via_l01', 'abrir porta do laboratório')),
                ('L01', ('ir para a câmara fria', 'atravessar a porta', 'ir via_b10')),
            ):
                for command in commands:
                    game.current_location = origin
                    CommandParser(game).execute(command)
                    self.assertEqual(game.current_location, origin, command)
                    self.assertFalse(state.enabled)
        # Liberação somente nesta instância de teste; nenhum mecanismo novo no jogo.
        state.enabled = True
        door.blocked = door.locked = False
        door.opened = True
        game.current_location = 'B10'
        CommandParser(game).execute('ir para o laboratório')
        self.assertEqual(game.current_location, 'L01')
        self.assertTrue({f'L{n:02}' for n in range(1,13)} <= reachable(game, 'B10', initial=True))
        self.assertFalse(GameState().get_room('B10').exit_states['via_l01'].enabled)

    def test_local_language_and_no_remote_movement(self):
        for origin, command, target in (
            ('E01', 'ir ao norte', 'E02'), ('E01', 'seguir em frente', 'E02'),
            ('L03', 'entrar na sala', 'L04'), ('L12', 'voltar', 'L11'),
            ('L07', 'entrar na sala de contenção', 'L08'),
            ('L07', 'entrar na câmara de contenção', 'L08'),
            ('B07', 'entrar na adega', 'B08'),
            ('E01', 'ir para o laboratório', 'E01'),
            ('L12', 'entrar na adega', 'L12'),
        ):
            with self.subTest(command=command, origin=origin):
                game = GameState()
                game.get_room('B07').enemies.clear()
                game.current_location = origin
                response = CommandParser(game).execute(command)
                self.assertEqual(official(game.current_location), target, response)
        # A forma antiga "sair pelo corredor" não autoriza movimento remoto.
        game = GameState(); game.current_location = 'L03'
        CommandParser(game).execute('sair pelo corredor')
        self.assertEqual(game.current_location, 'L03')
        CommandParser(game).execute('ir para o corredor do laboratório')
        self.assertEqual(game.current_location, 'L02')


class WorldAccessAuditTests(unittest.TestCase):
    def test_entire_structural_graph_and_initial_reachability(self):
        game = GameState()
        self.assertEqual({official(r) for r in game.rooms}, OFFICIAL_ROOM_IDS)
        self.assertEqual(len({id(r) for r in game.rooms.values()}), 58)
        for room in game.rooms.values():
            self.assertEqual(len(room.exits.values()), len(set(room.exits.values())))
            for direction, dest in room.exits.items():
                other = game.get_room(dest)
                state = room.exit_states[direction]
                if state.kind == 'fall':
                    self.assertEqual((room.room_id, dest), ('E08', 'B01'))
                    self.assertNotIn('E08', other.exits.values())
                    continue
                reverse = next(d for d,r in other.exits.items() if r == room.room_id)
                self.assertIs(state, other.exit_states[reverse])
                self.assertIs(room.exit_doors.get(direction), other.exit_doors.get(reverse))
        self.assertEqual(reachable(game, 'E01'), OFFICIAL_ROOM_IDS)
        self.assertEqual(reachable(game, 'E01', initial=True), {f'E{n:02}' for n in range(1,15)})
        self.assertEqual(reachable(game, 'L01', initial=True), {f'L{n:02}' for n in range(1,13)})
        self.assertNotIn('T12', reachable(game, 'B01', initial=True))
        self.assertIn('B09', reachable(game, 'B01', initial=True))
        self.assertFalse(any(r.startswith('L') for r in reachable(game, 'B01', initial=True)))

    def test_all_initial_blocks_both_sides(self):
        for a,b in (('E04','T01'), ('E06','T07'), ('E13','B02'), ('B07','T02'),
                    ('B04','B09'), ('B08','B10'), ('B10','L01'), ('T02','T09'), ('T05','T12'), ('B03','T12')):
            for origin,target in ((a,b),(b,a)):
                game = GameState(); game.get_room('B07').enemies.clear()
                room = game.get_room(origin)
                direction = next(d for d,r in room.exits.items() if official(r)==target)
                self.assertTrue(room.passage_failure(direction))
                for command in ('ir '+direction, 'fugir '+direction, 'esgueirar '+direction,
                                'atravessar '+room.exit_names[direction], 'ir para '+game.get_room(target).name):
                    game.current_location = origin
                    CommandParser(game).execute(command)
                    self.assertEqual(official(game.current_location), origin, (origin,command))
        game = GameState()
        self.assertTrue(game.get_room('E04').exit_doors['via_t01'].locked)
        self.assertTrue(game.get_room('B03').passage_failure('cima'))
        self.assertTrue(game.get_room('T12').passage_failure('baixo'))
        prototype = GameState(configuration='prototype')
        self.assertEqual(len(prototype.rooms), 6)
        self.assertFalse(any(r.startswith('L') for r in prototype.rooms))
