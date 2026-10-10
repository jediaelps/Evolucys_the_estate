import unittest

from action_context import ActionContext
from command_parser import CommandParser
from game_state import GameState
from system_demo import create_system_demo
from tutorial import TutorialState
from visual_session import VisualSession
from world import ROOM_ALIASES, create_world


IMPLEMENTED = {'T01', 'T02', 'T03', 'T04', 'T05', 'T06', 'T07', 'T08', 'T09', 'T10', 'T11', 'T12', 'B07', 'U01', 'U02', 'U03', 'U04', 'U05', 'U06', 'U07', 'U08', 'U09'}
IMPLEMENTED |= {f'E{n:02}' for n in range(1, 15)}
IMPLEMENTED |= {f'B{n:02}' for n in range(1, 11)}
IMPLEMENTED |= {f'L{n:02}' for n in range(1, 13)}
IMPLEMENTED.add('G01')
EDGES = {frozenset(pair.split()) for pair in (
    'T01 T02', 'T02 T03', 'T02 T04', 'T02 T08', 'T02 T09', 'T02 T11',
    'T03 T04', 'T04 T05', 'T05 T06', 'T08 T09', 'T02 U01', 'T02 B07',
    'T05 T07', 'T09 T10', 'T02 T12', 'T05 T12',
    'U01 U02', 'U01 U03', 'U01 U04', 'U01 U08', 'U02 U06', 'U03 U05', 'U06 U07', 'U07 U09',
    'E01 E02', 'E02 E03', 'E03 E04', 'E03 E05', 'E05 E11', 'E11 E10', 'E11 E12', 'E12 E07', 'E12 E06', 'E06 E13', 'E13 E08',
    'B03 B04', 'B03 B05', 'B03 B09', 'B05 B06', 'B06 B07', 'B07 B08', 'B09 B10', 'B04 B09', 'B08 B10',
    'E03 E14', 'E14 G01', 'T03 G01', 'B10 L01', 'L01 L02', 'L02 L03', 'L03 L04', 'L04 L05', 'L05 L06', 'L06 L09', 'L09 L11',
    'L05 L07', 'L07 L08', 'L08 L11', 'L03 L10', 'L10 L05', 'L11 L12',
    'E06 E09', 'B01 B02', 'B02 B03', 'B03 T12', 'E13 B02', 'E08 B01', 'E04 T01', 'E06 T07')}


def official(room_id):
    return ROOM_ALIASES.get(room_id, room_id)


class CampaignMapTests(unittest.TestCase):
    def setUp(self):
        self.game = GameState()
        self.game.current_location = 'T01'  # Fixture de regressão do interior.
        self.parser = CommandParser(self.game)

    def walk(self, command, expected):
        before = self.game.turn_count
        self.parser.execute(command)
        self.assertEqual(official(self.game.current_location), expected, command)
        self.assertEqual(self.game.turn_count, before + 1)

    def test_exact_rooms_aliases_and_start(self):
        self.game = GameState()
        self.assertEqual({official(r) for r in self.game.rooms}, IMPLEMENTED)
        self.assertEqual(len({id(r) for r in self.game.rooms.values()}), 58)
        self.assertEqual(self.game.current_location, 'E01')
        self.assertEqual(self.game.visited_rooms, {'E01'})
        for old, new in ROOM_ALIASES.items():
            self.assertIs(self.game.get_room(old), self.game.get_room(new))
        for missing in ('L13', 'B11'):
            with self.assertRaises(KeyError):
                self.game.get_room(missing)

    def test_exact_edges_bidirectional_and_shared_states(self):
        arcs = {(official(room.room_id), official(destination))
                for room in self.game.rooms.values() for destination in room.exits.values()}
        self.assertEqual({frozenset(arc) for arc in arcs}, EDGES)
        self.assertEqual(len(arcs), 137)
        for a, b in arcs:
            if (a, b) == ('E08', 'B01'):
                self.assertNotIn((b, a), arcs)
                self.assertEqual(self.game.get_room(a).exit_states['queda'].kind, 'fall')
                continue
            self.assertIn((b, a), arcs)
            room, other = self.game.get_room(a), self.game.get_room(b)
            direction = next(d for d, dest in room.exits.items() if official(dest) == b)
            reverse = next(d for d, dest in other.exits.items() if official(dest) == a)
            self.assertIs(room.exit_states[direction], other.exit_states[reverse])
            self.assertIs(room.exit_doors.get(direction), other.exit_doors.get(reverse))

    def test_both_kitchen_routes_and_returns(self):
        self.walk('ir para o salão principal', 'T02')
        self.walk('entrar na sala de estar', 'T03')
        self.walk('ir para a sala de jantar', 'T04')
        self.walk('ir para a cozinha', 'T05')
        self.walk('ir para a despensa', 'T06')
        self.walk('ir para a cozinha', 'T05')
        self.walk('ir para a sala de jantar', 'T04')
        self.walk('voltar ao salão principal', 'T02')

        self.walk('ir para a sala de jantar', 'T04')
        self.walk('ir para a cozinha', 'T05')
        self.walk('ir para a sala de jantar', 'T04')
        self.walk('entrar na sala de estar', 'T03')
        self.walk('voltar ao salão principal', 'T02')

    def test_ground_floor_complete_and_new_routes_both_ways(self):
        self.assertTrue({f'T{n:02}' for n in range(1, 13)} <= IMPLEMENTED)
        for origin, target, outward, back in (
            ('T05', 'T07', 'entrar na lavanderia', 'ir para a cozinha'),
            ('T09', 'T10', 'entrar na sala de música', 'ir para a biblioteca'),
            ('T02', 'T12', 'ir para a sala de manutenção', 'voltar ao salão principal'),
        ):
            self.game.current_location = origin
            self.walk(outward, target)
            self.walk(back, origin)

    def test_nine_real_hall_connections_resolve_individually(self):
        self.game.current_location = 'T02'
        hall = self.game.get_current_room()
        expected = {'T01', 'T03', 'T04', 'T08', 'T09', 'T11', 'T12', 'U01', 'B07'}
        self.assertEqual({official(d) for d in hall.exits.values()}, expected)
        self.assertEqual(len(hall.exits), 9)
        for direction, name in hall.exit_names.items():
            self.assertEqual(ActionContext().passages(self.game, name), [direction])
        self.parser.execute('esgueirar pela passagem')
        self.assertEqual(self.game.turn_count, 0)
        self.parser.execute('a da sala de manutenção')
        self.assertEqual(self.game.current_location, 'T12')
        self.assertTrue(self.game.hidden)
        self.assertEqual(self.game.turn_count, 1)

    def test_visiting_new_rooms_does_not_release_shortcuts(self):
        for room_id in ('T07', 'T10', 'T12', 'U02', 'U03', 'U04', 'U05', 'U06', 'U07', 'U08', 'U09'):
            self.game.current_location = room_id
            self.parser.execute('olhar em volta')
        for room_id, direction in (('T02', 'via_t09'), ('T02', 'norte'), ('T05', 'via_t12')):
            room = self.game.get_room(room_id)
            self.assertFalse(room.exit_states[direction].enabled)
            self.assertTrue(room.exit_doors[direction].blocked)

    def test_removed_shortcut_has_no_old_command_or_remote_autowalk(self):
        for location, commands in (
            ('T02', ('oeste', 'ir oeste', 'ir para a cozinha', 'entrar na cozinha', 'ir T05', 'ir kitchen')),
            ('T05', ('leste', 'ir leste', 'voltar ao salão principal', 'ir para o salão principal')),
        ):
            self.game.current_location = location
            origin = self.game.current_location
            for command in commands:
                self.parser.execute(command)
                self.assertEqual(self.game.current_location, origin, command)
        self.game.current_location = 'T02'
        response = self.parser.execute('ir para a cozinha')
        self.assertIn('Joseph:', response)
        self.assertIn('passagem direta', response)

    def test_upper_connections_bidirectional_by_name(self):
        for a, b in (('U01', 'U02'), ('U01', 'U03'), ('U01', 'U04'), ('U01', 'U08'),
                     ('U02', 'U06'), ('U03', 'U05'), ('U06', 'U07'), ('U07', 'U09')):
            with self.subTest(connection=(a, b)):
                self.game.current_location = a
                self.walk('ir para ' + self.game.get_room(b).name.lower(), b)
                self.walk('ir para ' + self.game.get_room(a).name.lower(), a)
        self.assertEqual(self.game.player_name, 'Joseph')

    def test_gallery_door_is_one_real_shared_connection(self):
        gallery = self.game.get_room('U01')
        bedroom = self.game.get_room('U02')
        door = gallery.objects['porta de quarto']
        self.assertIs(gallery.exit_doors['via_u02'], door)
        self.assertIs(bedroom.exit_doors['via_u01'], door)
        self.assertFalse(door.locked)
        self.assertTrue(door.opened)
        self.assertNotIn('trancada', gallery.description)
        self.game.current_location = 'U01'
        self.assertIn('Joseph:', self.parser.execute('passar pela porta de quarto'))
        self.assertEqual(self.game.current_location, 'upper_hall')
        self.assertEqual(self.game.turn_count, 0)
        self.walk('a do quarto principal', 'U02')
        self.parser.execute('fechar porta de quarto')
        self.parser.execute('ir para a galeria superior')
        self.assertEqual(self.game.current_location, 'U02')
        self.parser.execute('abrir porta de quarto')
        self.walk('ir para a galeria superior', 'U01')
        demo = GameState(configuration='prototype')
        demo.current_location = 'upper_hall'
        self.assertTrue(demo.get_current_room().objects['porta de quarto'].locked)
        self.assertEqual(set(demo.get_current_room().exits), {'baixo'})
        self.assertIn('trancada', CommandParser(demo).execute('passar pela porta de quarto'))
        self.assertEqual(demo.current_location, 'upper_hall')

    def test_upper_route_from_start_preserves_caution_and_has_no_save_event(self):
        for command, destination in (
            ('norte', 'T02'), ('subir', 'U01'), ('entrar no quarto principal', 'U02'),
            ('ir para o estudo privado', 'U06'), ('ir para o depósito superior', 'U07'),
            ('ir para o sótão', 'U09'), ('ir para o depósito superior', 'U07'),
            ('ir para o estudo privado', 'U06'), ('ir para o quarto principal', 'U02'),
            ('ir para a galeria superior', 'U01'), ('esgueirar pela passagem', 'U01'),
        ):
            if command == 'esgueirar pela passagem':
                before = self.game.turn_count
                self.assertIn('Joseph:', self.parser.execute(command))
                self.assertEqual(self.game.turn_count, before)
            else:
                self.walk(command, destination)
        self.walk('a da varanda superior', 'U08')
        self.assertTrue(self.game.hidden)
        self.assertFalse(self.game.phone_signal)
        self.assertFalse(any('save' in event['name'] for event in self.game.events))

    def test_office_library_bathroom_and_stairs(self):
        self.walk('norte', 'T02')
        self.walk('entrar no escritório', 'T08')
        self.walk('ir para a biblioteca', 'T09')
        self.walk('entrar no escritório', 'T08')
        self.walk('voltar ao salão principal', 'T02')
        self.walk('ir para o banheiro social', 'T11')
        self.walk('voltar ao salão principal', 'T02')
        self.walk('subir a escadaria', 'U01')
        self.walk('voltar ao salão principal', 'T02')
        self.walk('subir', 'U01')
        self.walk('descer', 'T02')

    def test_both_shortcuts_cannot_be_opened_or_bypassed_from_either_side(self):
        for a, b, command, door_name in (
            ('T02', 'T09', 'passar pela porta da biblioteca', 'porta da biblioteca'),
            ('T02', 'B07', 'passar pela porta do porão', 'porta do porão'),
            ('T05', 'T12', 'passar pela porta de serviço', 'porta de serviço'),
        ):
            for origin, destination in ((a, b), (b, a)):
                self.game = GameState()
                self.parser = CommandParser(self.game)
                self.game.current_location = origin
                # Evita que o vigia legado interfira no teste isolado do bloqueio.
                self.game.get_room('B07').enemies.clear()
                room = self.game.get_current_room()
                direction = next(d for d, dest in room.exits.items() if official(dest) == destination)
                state = room.exit_states[direction]
                door = room.exit_doors[direction]
                self.assertFalse(state.enabled)
                self.assertTrue(door.blocked)
                for action in ('abrir ' + door_name, 'forçar ' + door_name, command,
                               'ir ' + direction, 'esgueirar ' + direction,
                               'ir para ' + self.game.get_room(destination).name.lower()):
                    self.parser.execute(action)
                    self.assertEqual(official(self.game.current_location), origin)
                    self.assertFalse(state.enabled)
                    self.assertFalse(door.opened)
                # Nem a abertura física interna de teste pode contornar a condição.
                door.opened = True
                self.parser.execute('ir ' + direction)
                self.assertEqual(official(self.game.current_location), origin)
                door.opened = False

    def test_contextual_choice_and_caution_are_preserved(self):
        self.game.current_location = 'T02'
        response = self.parser.execute('esgueirar pela passagem')
        self.assertIn('Joseph:', response)
        self.assertEqual(self.game.turn_count, 0)
        self.parser.execute('a da sala de estar')
        self.assertEqual(official(self.game.current_location), 'T03')
        self.assertTrue(self.game.hidden)
        self.assertEqual(self.game.turn_count, 1)
        self.assertEqual(ActionContext().passages(self.game, 'cozinha'), [])

    def test_unimplemented_destinations_do_not_appear_or_move_player(self):
        for room in self.game.rooms.values():
            self.game.current_location = room.room_id
            for destination in ('L13', 'B11', 'sala inexistente'):
                self.assertEqual(ActionContext().passages(self.game, destination), [])
                self.parser.execute('ir para ' + destination)
                self.assertEqual(self.game.current_location, room.room_id)

    def test_new_rooms_only_have_provisional_environment_and_connection(self):
        for room_id in ('T03', 'T04', 'T06', 'T07', 'T09', 'T10', 'T11', 'T12',
                        'U02', 'U03', 'U04', 'U05', 'U06', 'U07', 'U08', 'U09'):
            room = self.game.get_room(room_id)
            self.assertFalse(room.enemies)
            self.assertTrue(room.description)
            expected_content = {'T09': {'nota de pesquisa'}, 'T11': {'bandagem'}, 'T12': {'bandagem'}, 'U05': {'spray de cura'}, 'U06': {'armário de armas', 'correspondência'}, 'U07': {'fusíveis', 'munição de pistola', 'registro de fusíveis'}}.get(room_id, set())
            self.assertTrue({o.name for o in room.objects.values() if o not in room.exit_doors.values()} <= expected_content)
            self.assertNotIn('Saídas:', room.describe(self.game))

    def test_configurations_do_not_share_mutable_state_or_relocate_items(self):
        prototype = GameState(configuration='prototype')
        self.assertEqual(set(prototype.rooms), set(ROOM_ALIASES))
        self.assertEqual(prototype.get_room('T02').exits['oeste'], 'kitchen')
        self.assertFalse(prototype.get_room('T02').exit_doors['norte'].blocked)
        for legacy in ROOM_ALIASES:
            demo, campaign = prototype.rooms[legacy], self.game.rooms[legacy]
            self.assertIsNot(demo, campaign)
            campaign_objects = dict(campaign.objects)
            if legacy == 'entrance':
                campaign_objects['lanterna'] = self.game.item_objects['lanterna']
            self.assertTrue(set(demo.objects) <= set(campaign_objects))
            self.assertEqual([e.name for e in demo.enemies], [e.name for e in campaign.enemies])
            for name, obj in demo.objects.items():
                self.assertIsNot(obj, campaign_objects[name])
                expected_contents = [o.name for o in obj.contents if not (legacy == 'office' and name == 'cofre' and o.name == 'pistola')]
                self.assertEqual(expected_contents, [o.name for o in campaign_objects[name].contents])
                self.assertEqual([o.name for o in obj.hidden_objects], [o.name for o in campaign_objects[name].hidden_objects])
        self.game.get_room('B07').exit_doors['sul'].locked = False
        self.assertTrue(prototype.get_room('B07').exit_doors['sul'].locked)
        with self.assertRaises(ValueError):
            create_world('invalid')

    def test_visual_session_campaign_and_isolated_demonstrations(self):
        session = VisualSession(); session.start_campaign()
        self.assertEqual(len(session.game.rooms), 58)
        session.game.current_location = 'T01'
        session.execute('norte'); session.execute('entrar na sala de estar')
        self.assertEqual(session.game.current_location, 'T03')
        campaign = session.game
        session.start_campaign(configuration='prototype')
        self.assertEqual(len(session.game.rooms), 6)
        session.execute('norte'); session.execute('oeste')
        self.assertEqual(session.game.current_location, 'kitchen')
        self.assertEqual(campaign.current_location, 'T03')
        for scenario in (1, 2, 3, 4):
            self.assertEqual(set(TutorialState(scenario).rooms), {'test_start', 'test_end'})
        for kind in ('surprise', 'patrol', 'light'):
            self.assertEqual(set(create_system_demo(kind).rooms), {'demo_foyer', 'demo_hall', 'demo_end'})

    def test_exterior_natural_paths_bidirectional_without_parser_changes(self):
        for a, b, outward, back in (
            ('E01', 'E02', 'ir até o portão', 'seguir pela estrada'),
            ('E02', 'E03', 'seguir pelo caminho frontal', 'ir até o portão'),
            ('E03', 'E04', 'ir até a varanda da mansão', 'seguir pelo caminho frontal'),
            ('E03', 'E05', 'ir para a lateral da mansão', 'seguir pelo caminho frontal'),
            ('E13', 'E08', 'entrar na estufa', 'ir para o jardim do poço'),
            ('E05', 'E11', 'ir aos fundos', 'ir para a lateral da casa'),
            ('E12', 'E07', 'entrar na casinha', 'ir para o pátio da casinha'),
            ('E06', 'E09', 'ir até o gerador externo', 'ir aos fundos'),
        ):
            with self.subTest(connection=(a,b)):
                self.game.current_location=a
                self.walk(outward,b);self.walk(back,a)
        self.game.current_location='E03'
        turn=self.game.turn_count
        self.assertIn('Joseph:',self.parser.execute('seguir pelo caminho'))
        self.assertEqual(self.game.current_location,'E03')
        self.assertEqual(self.game.turn_count,turn)

    def test_exterior_contains_only_authorized_initial_resources(self):
        found = {}
        for rid in sorted(r for r in IMPLEMENTED if r.startswith('E')):
            room=self.game.get_room(rid)
            self.assertFalse(room.enemies)
            self.assertTrue(room.description)
            for obj in room.objects.values():
                self.assertFalse(obj.contents);self.assertFalse(obj.hidden_objects)
                self.assertIsNone(obj.text)
                if obj.portable:found[obj.name]=rid
        self.assertEqual(found,{'macaco':'E07','manivela':'E08'})
        self.assertEqual(set(self.game.get_room('E07').exits.values()),{'E12'})
        self.assertEqual(self.game.get_room('E08').exits['queda'],'B01')
        self.assertEqual(self.game.get_room('B01').name,'Câmara sob a Estufa')

    def test_exterior_boundaries_shared_and_blocked_in_both_directions(self):
        for a,b in (('E04','T01'),('E06','T07')):
            for origin,destination in ((a,b),(b,a)):
                with self.subTest(origin=origin):
                    self.game.current_location=origin;room=self.game.get_current_room()
                    side=next(d for d,r in room.exits.items() if official(r)==destination)
                    door=room.exit_doors[side];state=room.exit_states[side]
                    other=self.game.get_room(destination)
                    reverse=next(d for d,r in other.exits.items() if official(r)==origin)
                    self.assertIs(other.exit_doors[reverse],door)
                    self.assertIs(other.exit_states[reverse],state)
                    self.assertFalse(state.enabled);self.assertTrue(door.blocked)
                    if a=='E04':self.assertTrue(door.locked)
                    for command in ('abrir '+door.name,'forçar '+door.name,'passar pela '+door.name,
                                    'ir '+side,'esgueirar '+side,'fugir '+side,
                                    'ir para '+other.name.lower()):
                        self.parser.execute(command)
                        self.assertEqual(official(self.game.current_location),origin,command)
                        self.assertFalse(state.enabled);self.assertFalse(door.opened)
                    door.opened=True;door.locked=False
                    self.parser.execute('fugir '+side)
                    self.assertEqual(official(self.game.current_location),origin)
                    door.opened=False;door.locked=(a=='E04')

    def test_existing_main_door_reused_and_prototype_untouched(self):
        self.assertIs(self.game.get_room('T01').objects['porta principal'],
                      self.game.get_room('E04').exit_doors['via_t01'])
        demo=GameState(configuration='prototype')
        self.assertEqual(len(demo.rooms),6)
        self.assertEqual(demo.get_room('T01').exits,{'norte':'main_hall'})
        self.assertFalse(demo.get_room('T01').objects['porta principal'].locked)
        self.assertTrue(demo.get_room('T01').objects['porta principal'].blocked)
        self.assertEqual(self.game.current_location,'entrance')
        self.assertEqual(self.game.player_name,'Joseph')

    def test_exterior_help_inspection_and_perception_reuse_existing_systems(self):
        self.game.current_location='E03'
        before=self.game.snapshot()
        text=self.parser.execute('ajuda')
        for path in ('SUL','varanda','lateral'):self.assertIn(path,text)
        self.assertEqual(self.game.snapshot(),before)
        self.game.current_location='E04'
        self.assertEqual(self.game.exploration.audible_signals(),[])
        session=VisualSession();session._attach(self.game,'campaign')
        session.execute('examinar porta principal')
        self.assertIs(session.inspection_object,self.game.get_current_room().objects['porta principal'])
        self.assertIn('bloqueando',session.reading_text)
        before=self.game.snapshot();session.execute('fechar leitura')
        self.assertEqual(self.game.snapshot(),before)
        self.assertIsNone(session.reading_text)



class CampaignDisplayTests(unittest.TestCase):
    def test_existing_view_renders_recorte_and_prototype_launcher(self):
        import tkinter as tk
        from unittest.mock import patch
        from visual import VisualApp
        import prototype_demo

        try:
            root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(str(error))
        root.withdraw()
        app = VisualApp(root)
        try:
            root.geometry('1100x760')
            app.start_campaign()
            for room_id in IMPLEMENTED:
                app.session.game.current_location = room_id
                app.build_game()
                root.update()
                self.assertTrue(app.command_entry.winfo_exists())
                self.assertNotIn('DICA:', app.history_view.get('1.0', 'end'))
            with patch('prototype_demo.VisualApp', return_value=app), patch.object(app, 'run') as run:
                prototype_demo.main()
                self.assertEqual(app.session.game.configuration, 'prototype')
                self.assertEqual(len(app.session.game.rooms), 6)
                run.assert_called_once()
        finally:
            root.destroy()


if __name__ == '__main__':
    unittest.main()

class GarageTests(unittest.TestCase):
    def test_shared_open_door_cardinal_and_natural_navigation(self):
        game = GameState(); parser = CommandParser(game)
        room, garage = game.get_room('T03'), game.get_room('G01')
        self.assertEqual(garage.name, 'Garagem')
        self.assertEqual(room.exits['oeste'], 'G01')
        self.assertEqual(garage.exits, {'leste': 'T03', 'via_e14': 'E14'})
        self.assertIs(room.exit_states['oeste'], garage.exit_states['leste'])
        self.assertIs(room.exit_doors['oeste'], garage.exit_doors['leste'])
        self.assertTrue(room.exit_doors['oeste'].opened)
        self.assertFalse(room.exit_doors['oeste'].locked)
        for command in ('entrar na garagem', 'ir para a garagem', 'passar pela porta da garagem', 'ir oeste', 'ir esquerda'):
            game.current_location = 'T03'
            response = parser.execute(command)
            self.assertEqual(game.current_location, 'G01', response)
            parser.execute('voltar para a sala de estar')
            self.assertEqual(game.current_location, 'T03')
        game.current_location = 'E01'; parser.execute('entrar na garagem')
        self.assertEqual(game.current_location, 'E01')
        self.assertIn('lanterna', game.inventory)
        self.assertNotIn('G01', GameState(configuration='prototype').rooms)

    def test_inspection_environment_and_no_wheel_collection(self):
        game = GameState(); game.current_location = 'G01'; parser = CommandParser(game)
        before = list(game.inventory)
        for target in ('carro antigo 1', 'carro antigo 2', 'compartimento', 'bancada', 'ferramentas', 'portões externos'):
            with self.subTest(target=target):
                response = parser.execute('examinar ' + target)
                self.assertEqual(parser.presentation, 'inspection', response)
                self.assertNotIn('Daniel', response)
                self.assertNotIn('roda compatível', response)
                parser.execute('pegar ' + target)
                self.assertEqual(game.inventory, before)
        parser.execute('pegar roda'); self.assertEqual(game.inventory, before)
        self.assertFalse(game.game_over)
        self.assertFalse(game.get_current_room().enemies)

    def test_external_gates_blocked_without_any_exit(self):
        game = GameState(); game.current_location = 'G01'; parser = CommandParser(game)
        garage = game.get_current_room(); gates = garage.objects['portões externos']
        for alias in ('portões externos', 'portão externo', 'portão da garagem', 'portas externas'):
            for verb in ('abrir', 'forçar', 'atravessar', 'passar pela', 'ir para'):
                parser.execute(verb + ' ' + alias)
                self.assertEqual(game.current_location, 'G01')
                self.assertTrue(gates.blocked)
                self.assertTrue(gates.locked)
                self.assertFalse(gates.opened)
        # Abrir apenas o objeto não habilita o estado compartilhado da passagem.
        gates.blocked = gates.locked = False; gates.opened = True
        parser.execute('atravessar portões externos')
        self.assertEqual(game.current_location, 'G01')
        self.assertEqual(garage.exits, {'leste': 'T03', 'via_e14': 'E14'})
        self.assertFalse(game.game_over)
        self.assertTrue(GameState().get_room('G01').objects['portões externos'].blocked)

class GarageFacadeTests(unittest.TestCase):
    def test_approach_aliases_and_exterior_inspection(self):
        game = GameState(); parser = CommandParser(game)
        for command, target in (('norte','E02'), ('atravessar portão','E03'), ('ir para a garagem','E14')):
            parser.execute(command); self.assertEqual(game.current_location,target)
        for command in ('ir para a garagem', 'ir até a frente da garagem', 'seguir para os portões', 'examinar a garagem'):
            parser.execute('voltar ao caminho frontal')
            self.assertEqual(game.current_location,'E03')
            parser.execute(command); self.assertEqual(game.current_location,'E14')
        for command in ('examinar garagem','examinar portões','observar fachada'):
            text=parser.execute(command)
            self.assertEqual(game.current_location,'E14')
            self.assertEqual(parser.presentation,'inspection')
            self.assertNotIn('contenção',text)
            self.assertNotIn('Evolucys',text)
        self.assertNotIn('E14',GameState(configuration='prototype').rooms)

    def test_shared_gates_block_both_sides_after_actual_power_restore(self):
        game=GameState(); parser=CommandParser(game)
        outside,inside=game.get_room('E14'),game.get_room('G01')
        self.assertIs(outside.exit_doors['via_g01'],inside.objects['portões externos'])
        self.assertIs(outside.exit_states['via_g01'],inside.exit_states['via_e14'])
        game.current_location='U07';parser.execute('pegar fusíveis')
        game.current_location='B06';parser.execute('instalar fusíveis');parser.execute('ligar gerador')
        self.assertIn('power_restored',game.world_events)
        for origin,direction,target in (('E14','via_g01','interior da garagem'),('G01','via_e14','frente da garagem')):
            for command in ('abrir portões','atravessar portões','passar pelas portas externas',
                            'ir '+direction,'fugir '+direction,'esgueirar '+direction,'ir para '+target):
                game.current_location=origin
                parser.execute(command)
                self.assertEqual(game.current_location,origin,command)
                self.assertTrue(inside.objects['portões externos'].blocked)
                self.assertFalse(outside.exit_states['via_g01'].enabled)
        self.assertTrue(game.get_room('T03').exit_doors['oeste'].opened)
        self.assertFalse(game.game_over)
