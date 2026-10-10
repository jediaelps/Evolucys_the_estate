import unittest
from command_parser import CommandParser
from game_state import GameState
from world import ROOM_ALIASES


def official(rid):
    return ROOM_ALIASES.get(rid, rid)


class BasementMapTests(unittest.TestCase):
    def test_rooms_and_legacy_content(self):
        game = GameState()
        self.assertEqual(len(game.rooms), 58)
        self.assertEqual(len({id(r) for r in game.rooms.values()}), 58)
        self.assertIs(game.get_room('B07'), game.rooms['cellar'])
        self.assertNotIn('B07', game.rooms)
        self.assertEqual(game.current_location, 'E01')
        for rid in ('B04', 'B05', 'B06', 'B08', 'B09', 'B10'):
            room = game.get_room(rid)
            self.assertTrue(room.description)
            self.assertFalse(room.enemies)
            expected_content = {'B06': {'quadro elétrico', 'gerador principal'}, 'B04': {'bandagem'}, 'B09': {'pé de cabra', 'kit médico'}}.get(rid, set())
            self.assertTrue({o.name for o in room.objects.values() if o not in room.exit_doors.values()} <= expected_content)
        prototype = GameState(configuration='prototype')
        self.assertEqual(len(prototype.rooms), 6)
        old, reused = prototype.get_room('B07'), game.get_room('B07')
        self.assertEqual(old.description, reused.description)
        self.assertEqual(set(old.objects), set(reused.objects))
        self.assertEqual(len(old.enemies), len(reused.enemies))

    def test_common_connections_both_ways(self):
        for a, b, outward, back in (
            ('B03', 'B04', 'seguir para o depósito', 'atravessar o corredor'),
            ('B03', 'B05', 'ir para a sala da caldeira', 'voltar ao corredor'),
            ('B03', 'B09', 'entrar na oficina', 'atravessar o corredor'),
            ('B05', 'B06', 'ir para a sala elétrica', 'voltar à sala da caldeira'),
            ('B06', 'B07', 'voltar ao arquivo', 'ir para a sala elétrica'),
            ('B07', 'B08', 'ir para a adega', 'voltar ao arquivo'),
            ('B09', 'B10', 'entrar na câmara fria', 'entrar na oficina'),
        ):
            with self.subTest(edge=(a, b)):
                game = GameState()
                # Fixture de navegação isola a reação do inimigo legado.
                game.get_room('B07').enemies.clear()
                game.current_location = a
                parser = CommandParser(game)
                for command, target in ((outward, b), (back, a)):
                    response = parser.execute(command)
                    self.assertEqual(official(game.current_location), target, response)

    def test_blocked_shortcuts_and_old_stairs(self):
        for a, b in (('B04', 'B09'), ('B08', 'B10'), ('B07', 'T02')):
            game = GameState()
            game.get_room('B07').enemies.clear()
            for origin, target in ((a, b), (b, a)):
                room, other = game.get_room(origin), game.get_room(target)
                direction = next(d for d, dest in room.exits.items() if official(dest) == target)
                reverse = next(d for d, dest in other.exits.items() if official(dest) == origin)
                state, door = room.exit_states[direction], room.exit_doors[direction]
                self.assertIs(state, other.exit_states[reverse])
                self.assertIs(door, other.exit_doors[reverse])
                for command in ('ir ' + direction, 'ir para ' + other.name,
                                'atravessar ' + room.exit_names[direction],
                                'esgueirar ' + direction, 'fugir ' + direction,
                                'abrir ' + door.name):
                    game.current_location = origin
                    CommandParser(game).execute(command)
                    self.assertEqual(official(game.current_location), origin, command)
                    self.assertFalse(state.enabled)
                    self.assertTrue(door.blocked)

    def test_no_teleport_or_laboratory(self):
        game = GameState()
        for origin, command in (('B01', 'entrar na oficina'),
                                ('B04', 'ir para a sala elétrica'),
                                ('B10', 'entrar no laboratório'), ('B10', 'ir L01')):
            game.current_location = origin
            CommandParser(game).execute(command)
            self.assertEqual(game.current_location, origin)
        self.assertFalse(game.get_room('B10').exit_states['via_l01'].enabled)
        self.assertEqual({official(r) for r in game.get_room('B10').exits.values()}, {'B08', 'B09', 'L01'})

class PowerAndContainmentTests(unittest.TestCase):
    def test_fuses_generator_sequence_without_releasing_doors(self):
        game = GameState(); parser = CommandParser(game)
        before = {s.connection_id: (s.known, s.enabled) for r in game.rooms.values() for s in r.exit_states.values()}
        gates = game.get_room('G01').objects['portões externos']
        game.current_location = 'B06'
        self.assertIn('Faltam', parser.execute('examinar quadro elétrico'))
        parser.execute('ligar gerador'); self.assertNotIn('power_restored', game.world_events)
        parser.execute('instalar fusíveis'); self.assertNotIn('fuses_installed', game.world_events)
        game.current_location = 'U07'; parser.execute('pegar fusíveis')
        self.assertIn('fusíveis', game.inventory)
        game.current_location = 'E09'; parser.execute('restaurar energia')
        self.assertNotIn('power_restored', game.world_events)
        game.current_location = 'B06'; parser.execute('instalar fusíveis')
        self.assertNotIn('fusíveis', game.inventory)
        self.assertNotIn('fusíveis', game.item_objects)
        self.assertNotIn('power_restored', game.world_events)
        parser.execute('ligar gerador')
        self.assertIn('power_restored', game.world_events)
        self.assertNotIn('containment_disabled', game.world_events)
        self.assertIn('já está', parser.execute('ligar gerador'))
        self.assertEqual(before, {s.connection_id: (s.known, s.enabled) for r in game.rooms.values() for s in r.exit_states.values()})
        self.assertTrue(gates.blocked); self.assertTrue(gates.locked)
        game.current_location = 'U07'; parser.execute('pegar fusíveis')
        self.assertNotIn('fusíveis', game.inventory)

    def test_well_requires_containment_release_even_with_power(self):
        game = GameState(); parser = CommandParser(game)
        parser.execute('equipar lanterna'); parser.execute('ligar lanterna')
        state = game.get_room('B02').exit_states['cima']
        for powered in (False, True):
            if powered: game.world_events.add('power_restored')
            game.current_location = 'B02'
            self.assertIn('contenção', parser.execute('abrir acesso do poço'))
            self.assertFalse(state.enabled)
        game.world_events.add('containment_disabled')
        game.current_location = 'E13'; parser.execute('olhar poço')
        parser.execute('abrir acesso do poço'); self.assertFalse(state.enabled)
        game.current_location = 'B02'; parser.execute('abrir acesso do poço')
        self.assertTrue(state.enabled)
        parser.execute('subir escada'); self.assertEqual(game.current_location, 'E13')
        parser.execute('desligar lanterna'); parser.execute('descer pelo poço')
        self.assertEqual(game.current_location, 'E13')
        parser.execute('ligar lanterna'); parser.execute('descer pelo poço')
        self.assertEqual(game.current_location, 'B02')

    def test_internal_route_and_full_inventory_preserve_fuses(self):
        game = GameState(); parser = CommandParser(game); game.current_location = 'B09'
        parser.execute('pegar pé de cabra'); game.current_location = 'T12'
        parser.execute('usar pé de cabra na porta de manutenção')
        for command, target in (('descer escada','B03'), ('ir para a sala da caldeira','B05'), ('ir para a sala elétrica','B06')):
            parser.execute(command); self.assertEqual(game.current_location, target)
        game.current_location = 'U07'
        for n in range(5): game.add_item('item '+str(n))
        parser.execute('pegar fusíveis')
        self.assertIn('fusíveis', game.get_current_room().objects)
        self.assertNotIn('fusíveis', game.inventory)
        self.assertEqual(len(game.rooms), 58)
        prototype = GameState(configuration='prototype')
        self.assertEqual(len(prototype.rooms), 6)
        self.assertFalse(any(o.interaction == 'main_generator' for o in prototype.all_objects()))

class CampaignProgressionTests(unittest.TestCase):
    def test_end_to_end_crowbar_fuses_power_without_external_release(self):
        game = GameState(); parser = CommandParser(game); game.current_location = 'B01'
        def walk(command, target):
            response = parser.execute(command)
            self.assertEqual(official(game.current_location), target, response)
        walk('ir para o túnel antigo', 'B02'); walk('ir para o corredor de serviço', 'B03')
        for command in ('subir escada', 'ir cima', 'atravessar porta de manutenção', 'forçar porta de manutenção'):
            parser.execute(command); self.assertEqual(game.current_location, 'B03')
        walk('entrar na oficina', 'B09'); parser.execute('pegar pé de cabra')
        self.assertEqual(game.item_objects['pé de cabra'].capabilities.melee_damage, 25)
        walk('ir para o corredor de serviço', 'B03')
        parser.execute('usar pé de cabra na porta de manutenção')
        self.assertIn('pé de cabra', game.inventory)
        self.assertIn('já está', parser.execute('usar pé de cabra na porta de manutenção'))
        walk('subir escada', 'T12'); walk('descer escada', 'B03'); walk('subir escada', 'T12')
        walk('ir para o salão principal', 'T02'); walk('subir escada', 'U01')
        walk('entrar no quarto principal', 'U02'); walk('ir para o estudo privado', 'U06')
        walk('ir para o depósito superior', 'U07'); parser.execute('pegar fusíveis')
        walk('ir para o estudo privado', 'U06'); walk('ir para o quarto principal', 'U02')
        walk('ir para a galeria superior', 'U01'); walk('descer escada', 'T02')
        walk('ir para a sala de manutenção', 'T12'); walk('descer escada', 'B03')
        walk('ir para a sala da caldeira', 'B05'); walk('ir para a sala elétrica', 'B06')
        parser.execute('instalar fusíveis'); parser.execute('ligar gerador')
        self.assertIn('power_restored', game.world_events)
        self.assertNotIn('containment_disabled', game.world_events)
        self.assertFalse(game.get_room('B02').exit_states['cima'].enabled)
        self.assertFalse(game.get_room('B10').exit_states['via_l01'].enabled)
        self.assertTrue(game.get_room('G01').objects['portões externos'].blocked)

    def test_weapons_tool_boundaries_and_unique_items(self):
        game = GameState(); parser = CommandParser(game); game.current_location = 'B09'
        parser.execute('pegar pé de cabra'); game.current_location = 'B10'
        parser.execute('usar pé de cabra na porta do laboratório')
        self.assertFalse(game.get_current_room().exit_states['via_l01'].enabled)
        game.current_location = 'T08'; parser.execute('abrir armário de segurança')
        parser.execute('pegar pistola'); parser.execute('equipar pistola')
        self.assertEqual(game.equipped_item, 'pistola')
        self.assertEqual(game.item_objects['pistola'].weapon.ammo, 2)
        parser.execute('abrir armário de segurança')
        self.assertEqual(sum(o.name=='pistola' for o in game.all_objects()), 1)
        game.current_location = 'U06'
        self.assertIn('espingarda', parser.execute('examinar armário de armas'))
        for command in ('abrir armário de armas', 'usar pé de cabra no armário de armas', 'pegar espingarda'):
            parser.execute(command)
            self.assertNotIn('espingarda', game.inventory)
        self.assertTrue(game.get_current_room().objects['armário de armas'].blocked)

    def test_resources_full_inventory_and_fragmented_documents(self):
        for rid, name in (('T11','bandagem'),('U05','spray de cura'),('U07','munição de pistola'),
                          ('B09','pé de cabra'),('B09','kit médico'),('L07','kit médico'),('G01','bandagem')):
            game=GameState();game.current_location=rid;parser=CommandParser(game)
            for n in range(5):game.add_item('enchimento '+str(n))
            item=game.get_current_room().objects[name]
            parser.execute('pegar '+name)
            self.assertIs(game.get_current_room().objects[name],item)
            self.assertNotIn(name,game.inventory)
        game=GameState()
        for rid in ('T08','T09','U06','U07','B07','L03','L04','L05','L06','L07','L08','L11'):
            docs=[o for o in game.get_room(rid).objects.values() if o.text]
            self.assertTrue(docs,rid)
            for doc in docs:
                self.assertLess(len(doc.text),500)
                if rid!='L11':self.assertNotIn('injeta',doc.text)
        self.assertEqual(len(GameState(configuration='prototype').rooms),6)
