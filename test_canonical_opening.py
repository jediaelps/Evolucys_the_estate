import unittest
from unittest.mock import patch, Mock
from game_state import GameState
from command_parser import CommandParser
from world import GameObject
from visual_session import VisualSession
import test_visual_commands as ui

class CanonicalOpeningTests(unittest.TestCase):
    def setUp(self):
        self.game=GameState();self.parser=CommandParser(self.game)

    def walk(self, command, destination):
        turn=self.game.turn_count
        response=self.parser.execute(command)
        self.assertEqual(self.game.current_location,destination,(command,response))
        self.assertEqual(self.game.turn_count,turn+1)
        return response

    def light(self,on=True,mode='normal'):
        lamp=GameObject('lanterna','Lanterna.',portable=True)
        self.game.add_item('lanterna');self.game.item_objects['lanterna']=lamp
        self.game.equipped_item='lanterna';lamp.light_on=on;lamp.light_mode=mode
        return lamp

    def test_start_car_gate_front_with_cardinal_and_relative_names(self):
        self.assertEqual(self.game.current_location,'E01')
        self.assertEqual(self.game.visited_rooms,{'E01'})
        text=self.parser.execute('olhar em volta')
        self.assertIn('pneu estragado',text);self.assertIn('silhueta',text)
        self.walk('seguir em frente','E02')
        self.walk('atravessar o portão','E03')
        self.assertTrue(self.game.get_room('E02').objects['portão'].opened)
        self.walk('ir sul','E02');self.walk('ir sul','E01')
        self.walk('ir norte','E02');self.walk('ir norte','E03')

    def test_canonical_route_jack_fall_and_underground_continuation(self):
        for command,room in (('norte','E02'),('atravessar portão','E03'),('ir para a lateral da casa','E05'),
            ('ir aos fundos','E11'),('ir para o pátio da casinha','E12'),('entrar na casinha','E07')):
            self.walk(command,room)
        self.assertNotIn('manivela',self.game.get_current_room().objects)
        self.assertIn('Falta a manivela',self.parser.execute('examinar macaco'))
        self.parser.execute('pegar macaco')
        self.assertIn('macaco',self.game.inventory)
        self.assertIn('Falta a manivela',self.parser.execute('usar macaco'))
        for command,room in (('ir para o pátio da casinha','E12'),('ir aos fundos','E06'),
            ('ir para o jardim do poço','E13'),('entrar na estufa','E08')):
            self.walk(command,room)
        text=self.walk('pegar manivela','B01')
        self.assertIn('tábuas cedem',text);self.assertNotIn('manivela',self.game.inventory)
        self.assertEqual(self.game.health,100);self.assertIn('macaco',self.game.inventory)
        self.assertEqual(self.game.world_events,{'greenhouse_fall'})
        self.walk('ir para o túnel antigo','B02')
        self.walk('ir para o corredor de serviço','B03')
        self.walk('entrar na oficina','B09')
        self.parser.execute('pegar pé de cabra')
        self.walk('ir para o corredor de serviço','B03')
        self.parser.execute('usar pé de cabra na porta de manutenção')
        self.walk('subir escada','T12')
        self.walk('ir para o salão principal','main_hall')
        self.walk('sul','entrance')
        self.parser.execute('pegar lanterna')
        self.assertIn('lanterna',self.game.inventory)

    def test_fall_aliases_and_full_inventory_do_not_give_handle(self):
        for command in ('pegar barra de aço','pegar barra de aço do macaco','apanhar manivela do macaco','recolher barra do macaco','pegar barra de ferro'):
            self.setUp();self.game.current_location='E08'
            for i in range(6):self.game.add_item('item '+str(i))
            before=list(self.game.inventory)
            self.walk(command,'B01')
            self.assertEqual(self.game.inventory,before)
            self.assertEqual(len(self.game.rooms),58)
            self.game.current_location='E08'
            self.parser.execute(command)
            self.assertEqual(self.game.current_location,'E08')
            self.assertIn('manivela',self.game.get_current_room().objects)
            self.assertFalse(self.game.get_current_room().objects['manivela'].accessible)

    def test_no_fall_on_inspect_wait_or_traversing_script_exit(self):
        self.game.current_location='E08'
        for command in ('examinar manivela','olhar em volta','esperar','ir queda','fugir queda','ir baixo'):
            self.parser.execute(command)
            self.assertEqual(self.game.current_location,'E08')
            self.assertFalse(self.game.world_events)
        self.game.current_location='B01'
        self.assertNotIn('E08',self.game.get_current_room().exits.values())

    def test_doorbell_two_parts_wait_free_completion_and_door_stays_locked(self):
        self.game.current_location='E04';door=self.game.get_current_room().objects['porta principal']
        self.assertIn('TOCAR',self.parser.execute('ajuda'))
        text=self.parser.execute('tocar a campainha')
        self.assertIn('espera por uma resposta',text);self.assertEqual(self.game.turn_count,1)
        self.assertTrue(door.locked);self.assertTrue(door.blocked)
        self.parser.execute('ir para a mansão')
        self.assertEqual(self.game.turn_count,1)
        text=self.parser.finish_delayed_response()
        self.assertIn('Ninguém responde',text);self.assertIn('Joseph:',text)
        self.assertEqual(self.parser.finish_delayed_response(),'')
        self.assertIn('arredores',self.parser.execute('ajuda'))
        self.assertEqual(self.game.turn_count,1)
        self.parser.execute('passar pela porta principal')
        self.assertEqual(self.game.current_location,'E04')

    def test_well_requires_light_even_if_name_or_direction_guessed(self):
        self.game.current_location='E13';state=self.game.get_current_room().exit_states['baixo']
        self.assertIn('escuro',self.parser.execute('olhar poço'))
        self.assertFalse(state.known)
        for command in ('descer pelo poço','ir baixo','fugir baixo','esgueirar baixo','ir para túnel antigo'):
            self.parser.execute(command)
            self.assertEqual(self.game.current_location,'E13')
        lamp=self.light(on=False)
        self.parser.execute('usar lanterna no poço');self.assertFalse(state.known)
        lamp.light_on=True;lamp.light_mode='uv'
        self.parser.execute('olhar poço');self.assertFalse(state.known)
        lamp.light_mode='normal';self.game.equipped_item=None
        self.parser.execute('olhar poço');self.assertFalse(state.known)
        self.game.equipped_item='lanterna'
        text=self.parser.execute('usar lanterna no poço')
        self.assertIn('escada',text);self.assertIn('fechado',text)
        self.assertTrue(state.known);self.assertFalse(state.enabled)
        for command in ('descer pelo poço','abrir acesso do poço','forçar acesso do poço','usar lanterna no acesso do poço'):
            self.parser.execute(command)
            self.assertFalse(state.enabled);self.assertEqual(self.game.current_location,'E13')

    def test_well_internal_unlock_and_return_with_light_gate(self):
        self.game.current_location='B02'
        self.game.world_events.add('containment_disabled')
        self.parser.execute('abrir acesso do poço')
        state=self.game.get_current_room().exit_states['cima']
        self.assertTrue(state.enabled)
        self.walk('subir escada','E13')
        self.parser.execute('descer pelo poço');self.assertEqual(self.game.current_location,'E13')
        lamp=self.light()
        text=self.parser.execute('olhar poço');self.assertIn('aberto',text)
        self.walk('descer pelo poço','B02')
        self.walk('subir escada','E13')
        lamp.light_on=False
        self.assertNotIn('DESCER',self.parser.execute('ajuda'))
        for command in ('ir baixo','atravessar acesso do poço','fugir baixo','esgueirar baixo'):
            self.parser.execute(command);self.assertEqual(self.game.current_location,'E13')

    def test_back_window_does_not_reveal_inside_or_allow_entry(self):
        self.game.current_location='E06'
        self.assertIn('não consigo distinguir',self.parser.execute('olhar pela janela'))
        self.parser.execute('entrar pela janela')
        self.assertEqual(self.game.current_location,'E06')

    def test_events_and_items_are_separate_between_games_and_prototype(self):
        self.game.current_location='E08';self.parser.execute('pegar manivela')
        other=GameState()
        self.assertFalse(other.world_events)
        self.assertTrue(other.get_room('E08').objects['manivela'].accessible)
        prototype=GameState(configuration='prototype')
        self.assertEqual(len(prototype.rooms),6)
        self.assertEqual(prototype.current_location,'entrance')
        self.assertFalse(any(o.interaction for o in prototype.all_objects()))

class CanonicalInterfaceTests(unittest.TestCase):
    setUp=ui.VisualCommandTests.setUp
    tearDown=ui.VisualCommandTests.tearDown
    enter=ui.VisualCommandTests.enter

    def test_bell_delay_callback_no_extra_turn_and_restores_input(self):
        self.app.start_campaign();self.app.session.game.current_location='E04';self.app.build_game()
        with patch.object(self.app.root,'after') as after:
            self.enter('tocar campainha')
            after.assert_called_once()
            milliseconds, callback=after.call_args.args
            self.assertEqual(milliseconds,800)
            self.assertEqual(self.app.command_entry.cget('state'),'disabled')
            self.assertNotIn('Ninguém responde',self.app.history_view.get('1.0','end'))
            callback();self.app.root.update()
        self.assertIn('Ninguém responde',self.app.history_view.get('1.0','end'))
        self.assertEqual(self.app.session.game.turn_count,1)
        self.assertEqual(self.app.command_entry.cget('state'),'normal')
        self.assertIs(self.app.root.focus_get(),self.app.command_entry)

    def test_old_bell_callback_cannot_change_new_game(self):
        self.app.start_campaign();self.app.session.game.current_location='E04';self.app.build_game()
        with patch.object(self.app.root,'after') as after:
            self.enter('tocar campainha');callback=after.call_args.args[1]
            self.app.start_campaign();before=self.app.session.game.snapshot()
            callback()
            self.assertEqual(self.app.session.game.snapshot(),before)
            self.assertFalse(self.app.session.history)

    def test_fall_updates_scene_once_and_inspection_must_close_before_pickup(self):
        self.app.start_campaign();self.app.session.game.current_location='E08';self.app.build_game()
        self.enter('examinar manivela')
        self.enter('pegar manivela')
        self.assertEqual(self.app.session.game.current_location,'E08')
        self.app.reader_panel.back.invoke()
        parser=self.app.session.parser
        with patch.object(parser,'execute',wraps=parser.execute) as execute:
            self.enter('pegar manivela');execute.assert_called_once()
        self.assertEqual(self.app.session.game.current_location,'B01')
        self.assertIsNone(self.app.reader_window)
        self.assertNotIn('manivela',self.app.session.game.inventory)
        self.assertIs(self.app.root.focus_get(),self.app.command_entry)

class PrologueNarrativeTests(unittest.TestCase):
    def test_initial_inspection_and_local_approach(self):
        game = GameState(); parser = CommandParser(game)
        intro = parser.execute('olhar em volta')
        for text in ('2000', 'empresário adulto', 'fim de tarde', 'tempestade', 'pneu estragado', 'silhueta'):
            self.assertIn(text, intro)
        for command, text in (('examinar pneu', 'ferramentas adequadas'),
                              ('examinar carro', 'rasgado'), ('olhar mansão', 'Joseph:')):
            self.assertIn(text, parser.execute(command))
            self.assertEqual(game.current_location, 'E01')
        parser.execute('caminhar até o portão'); self.assertEqual(game.current_location, 'E02')
        parser.execute('atravessar o portão'); self.assertEqual(game.current_location, 'E03')
        self.assertIn('Trepadeiras', parser.execute('examinar fachada'))
        parser.execute('caminhar até o portão'); self.assertEqual(game.current_location, 'E02')
        game.current_location = 'B01'
        parser.execute('caminhar até o portão'); self.assertEqual(game.current_location, 'B01')

    def test_bell_first_and_repeat_preserve_delay_and_lock(self):
        game = GameState(); game.current_location = 'E04'; parser = CommandParser(game)
        first = parser.execute('tocar campainha')
        self.assertIn('Tem alguém aí?', first)
        self.assertIsNotNone(parser.delayed_response)
        self.assertIn('Joseph:', parser.finish_delayed_response())
        second = parser.execute('tocar campainha')
        self.assertNotIn('Tem alguém aí?', second)
        self.assertIn('espera', second)
        self.assertEqual(parser.finish_delayed_response(), 'Ninguém responde desta vez também.')
        self.assertEqual(game.turn_count, 2)
        self.assertTrue(game.get_room('E04').exit_doors['via_t01'].locked)
        self.assertIn('Ninguém respondeu', parser.execute('ajuda'))

    def test_handle_knowledge_and_help_depend_on_inspection(self):
        game = GameState(); parser = CommandParser(game); game.current_location = 'E08'
        for command in ('olhar em volta', 'examinar estufa', 'olhar mesa', 'examinar manivela', 'ajuda'):
            text = parser.execute(command)
            self.assertNotIn('macaco', text)
            self.assertNotIn('laboratório', text)
            self.assertEqual(game.current_location, 'E08')
            self.assertFalse(game.world_events)
        self.assertIn('alcançá-la', parser.execute('ajuda'))
        game.current_location = 'E07'
        self.assertIn('incompleto', parser.execute('examinar macaco') + parser.execute('ajuda'))
        parser.execute('pegar macaco')
        game.current_location = 'E08'
        self.assertIn('macaco que examinei', parser.execute('examinar manivela'))
        self.assertIn('Joseph:', parser.inspection_text)
        self.assertEqual(game.world_events, set())

    def test_all_handle_pickup_aliases_share_single_fall(self):
        for command in ('pegar manivela', 'apanhar manivela', 'coletar manivela',
                        'recolher barra de aço', 'alcançar manivela', 'alcançar a barra do macaco'):
            with self.subTest(command=command):
                game = GameState(); game.current_location = 'E08'; parser = CommandParser(game)
                text = parser.execute(command)
                self.assertEqual(game.current_location, 'B01', text)
                self.assertIn('recupera a orientação', text)
                self.assertIn('Joseph:', text)
                self.assertNotIn('manivela', game.inventory)
                self.assertEqual(game.health, 100)
                self.assertEqual(game.world_events, {'greenhouse_fall'})
                self.assertIn('outra saída', parser.execute('ajuda'))
                self.assertNotIn('laboratório', parser.execute('ajuda'))
                self.assertNotIn('dor', parser.execute('olhar em volta'))
                game.current_location = 'E08'
                self.assertIn('Não alcanço', parser.execute(command))
                self.assertEqual(game.current_location, 'E08')

class InitialFlashlightTests(unittest.TestCase):
    def test_campaign_lamp_is_unique_functional_and_prototype_unchanged(self):
        game = GameState(); parser = CommandParser(game)
        self.assertEqual(game.current_location, 'E01')
        self.assertEqual(game.inventory, ['lanterna'])
        self.assertEqual(game.inventory_limit, 6)
        lamp = game.item_objects['lanterna']
        self.assertFalse(any('lanterna' in room.objects for room in game.rooms.values()))
        self.assertIsNot(lamp, GameState().item_objects['lanterna'])
        parser.execute('equipar lanterna'); parser.execute('ligar lanterna')
        self.assertTrue(game.well_lit)
        parser.execute('desligar lanterna'); self.assertFalse(game.well_lit)
        prototype = GameState(configuration='prototype')
        self.assertEqual(prototype.inventory, [])
        self.assertIn('lanterna', prototype.get_room('T01').objects)

    def test_actual_initial_lamp_well_unlock_only_inside(self):
        game = GameState(); parser = CommandParser(game); game.current_location = 'E13'
        parser.execute('largar lanterna')
        self.assertIn('escuro', parser.execute('olhar poço'))
        parser.execute('pegar lanterna'); parser.execute('equipar lanterna'); parser.execute('ligar lanterna')
        self.assertIn('escada', parser.execute('usar lanterna no poço'))
        state = game.get_current_room().exit_states['baixo']
        for item in ('chave', 'pé de cabra'):
            game.add_item(item); game.item_objects[item] = GameObject(item, '', portable=True)
            parser.execute('usar ' + item + ' no acesso do poço')
            self.assertFalse(state.enabled)
        for command in ('abrir acesso do poço', 'forçar acesso do poço', 'descer pelo poço'):
            parser.execute(command)
            self.assertFalse(state.enabled); self.assertEqual(game.current_location, 'E13')
        game.current_location = 'B02'; game.world_events.add('containment_disabled'); parser.execute('abrir acesso do poço')
        self.assertTrue(state.enabled)
        parser.execute('subir escada'); self.assertEqual(game.current_location, 'E13')
        parser.execute('desligar lanterna'); parser.execute('descer pelo poço')
        self.assertEqual(game.current_location, 'E13')
        parser.execute('ligar lanterna'); parser.execute('descer pelo poço')
        self.assertEqual(game.current_location, 'B02')
