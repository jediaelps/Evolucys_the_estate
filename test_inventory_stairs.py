import unittest
from command_parser import CommandParser
from game_state import GameState
from tutorial import TutorialState
from inventory_view import item_details


class InventoryStairsTests(unittest.TestCase):
    def test_all_up_aliases(self):
        for command in ('subir', 'subir escada', 'subir escadaria', 'subir as escadas',
                        'ir para o andar de cima', 'ir andar superior'):
            with self.subTest(command=command):
                game = GameState()
                game.current_location = 'main_hall'
                parser = CommandParser(game)
                parser.execute(command)
                self.assertEqual(game.current_location, 'upper_hall')
                self.assertEqual(game.turn_count, 1)

    def test_all_down_aliases(self):
        for command in ('descer', 'descer escada', 'descer escadaria', 'descer as escadas', 'voltar ao salão'):
            with self.subTest(command=command):
                game = GameState()
                game.current_location = 'upper_hall'
                CommandParser(game).execute(command)
                self.assertEqual(game.current_location, 'main_hall')

    def test_vertical_movement_requires_local_connection(self):
        for game in (GameState(), TutorialState(1)):
            parser = CommandParser(game)
            origin = game.current_location
            for command in ('subir', 'descer', 'ir andar superior', 'voltar ao salão'):
                response = parser.execute(command)
                if command == 'voltar ao salão' and origin == 'entrance':
                    self.assertEqual(game.current_location, 'main_hall')
                else:
                    self.assertEqual(game.current_location, origin)
                    self.assertTrue('Não há' in response)

    def test_blocked_stairs_explain_cause_both_directions(self):
        game = GameState()
        stairs = game.rooms['main_hall'].objects['escadaria']
        stairs.blocked = True
        parser = CommandParser(game)
        for location, command in [('main_hall', 'subir'), ('upper_hall', 'descer')]:
            game.current_location = location
            self.assertIn('bloqueando', parser.execute(command))
            self.assertEqual(game.current_location, location)

    def test_upper_room_objects_and_unfinished_door_have_explanations(self):
        game = GameState(configuration='prototype')
        game.current_location = 'upper_hall'
        parser = CommandParser(game)
        room = game.get_current_room()
        observation = parser.execute('olhar em volta')
        self.assertTrue(room.description.strip())
        self.assertIn(room.description, observation)
        self.assertNotIn('Saídas:', observation)
        for name in ('janela', 'quadro antigo', 'porta de quarto', 'escadaria'):
            obj = game.visible_objects()[name]
            self.assertTrue(obj.accessible)
            self.assertIn(obj.description, parser.execute('examinar ' + name))
            self.assertIn(obj.object_id, game.investigated)
        self.assertIn('trancada', parser.execute('passar pela porta de quarto'))
        self.assertEqual(game.current_location, 'upper_hall')
        self.assertTrue(room.objects['porta de quarto'].locked)

    def test_help_recognizes_stairs_and_inventory_mouse_exception(self):
        game = GameState()
        game.current_location = 'main_hall'
        parser = CommandParser(game)
        room = game.get_current_room()
        before = game.snapshot()
        guidance = parser.execute('ajuda')
        self.assertTrue(guidance.startswith('Joseph:'))
        # Aceita ações sobre objetos conhecidos ou caminhos realmente livres.
        object_guidance = any(verb in guidance for verb in ('EXAMINAR', 'OBSERVAR', 'OUVIR')) and any(
            name in guidance for name in game.visible_objects())
        path_guidance = any(direction.upper() in guidance for direction in room.known_exits()
                            if direction in ('norte', 'sul', 'leste', 'oeste')
                            and not room.passage_failure(direction))
        stair_guidance = 'SUBIR' in guidance and not room.passage_failure('cima')
        self.assertTrue(object_guidance or path_guidance or stair_guidance, guidance)
        inventory_help = parser.execute('ajuda inventário')
        self.assertTrue(inventory_help.startswith('Joseph:'))
        self.assertIn('INVENTÁRIO', inventory_help)
        for secret in ('inscrição', 'chave do armário', 'chave do porão', '0417'):
            self.assertNotIn(secret, guidance + inventory_help)
        self.assertEqual(game.snapshot(), before)
        self.assertEqual(game.turn_count, 0)
        parser.execute('subir a escadaria')
        self.assertEqual(game.current_location, 'upper_hall')
        parser.execute('descer')
        self.assertEqual(game.current_location, 'main_hall')
        self.assertEqual(game.turn_count, 2)
        # Seleção por mouse é exercitada pelos testes de widgets do inventário.

    def test_item_description_query_does_not_consume_or_modify(self):
        game = TutorialState(2)
        parser = CommandParser(game)
        parser.execute('pegar bandagem')
        before = game.snapshot()
        text, reasons = item_details(game, 'bandagem')
        self.assertIn('BANDAGEM', text)
        self.assertTrue(reasons['usar'])
        self.assertEqual(game.snapshot(), before)
        self.assertIn('bandagem', game.inventory)

    def test_contextual_action_availability(self):
        game = TutorialState(2)
        parser = CommandParser(game)
        parser.execute('pegar lanterna')
        text, reasons = item_details(game, 'lanterna')
        self.assertIn('desligada', text)
        self.assertTrue(reasons['usar'])
        parser.execute('equipar lanterna')
        self.assertFalse(item_details(game, 'lanterna')[1]['usar'])
        parser.execute('usar lanterna')
        self.assertIn('ligada', item_details(game, 'lanterna')[0])


if __name__ == '__main__':
    unittest.main()
