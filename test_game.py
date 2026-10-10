import contextlib
import io
import unittest
from unittest.mock import patch

from command_parser import CommandParser
from game_state import GameState
from world import GameObject
import main


class ExplorationTests(unittest.TestCase):
    def setUp(self):
        self.game = GameState(configuration='prototype')
        self.parser = CommandParser(self.game)

    def run_commands(self, *commands):
        return [self.parser.execute(command) for command in commands]

    def test_complete_puzzle_and_return(self):
        self.run_commands('pegar lanterna', 'equipar lanterna', 'ir norte')
        self.assertNotIn('inscrição', self.game.get_current_room().objects)
        self.run_commands('examinar retrato')
        self.assertIn('gaveta', self.parser.execute('examinar inscrição'))
        self.run_commands('ir oeste', 'pegar pé de cabra', 'ir leste',
                          'usar pé de cabra na gaveta', 'pegar chave do armário',
                          'ir leste', 'abrir armário', 'pegar bilhete')
        self.assertIn('0417', self.parser.execute('examinar bilhete'))
        self.run_commands('digitar 0417 no cofre', 'pegar chave do porão',
                          'ir oeste', 'usar chave do porão na porta do porão', 'ir norte')
        self.assertEqual(self.game.current_location, 'cellar')
        self.assertIn('EVOLUCYS', self.parser.execute('examinar pasta de Joseph'))
        self.run_commands('ir sul', 'ir norte')
        self.assertEqual(self.game.current_location, 'cellar')

    def test_locks_and_hidden_items_cannot_be_bypassed(self):
        self.run_commands('pegar lanterna', 'ir norte', 'ir norte', 'abrir porta do porão',
                          'pegar chave do armário', 'abrir gaveta',
                          'usar lanterna na gaveta')
        self.assertEqual(self.game.current_location, 'main_hall')
        self.assertTrue(self.game.get_current_room().objects['gaveta'].locked)
        self.assertNotIn('chave do armário', self.game.inventory)
        self.run_commands('ir leste', 'abrir armário', 'pegar bilhete',
                          'abrir cofre', 'digitar 417 no cofre', 'digitar 0000 no cofre')
        self.assertTrue(self.game.get_current_room().objects['cofre'].locked)
        self.assertTrue(self.game.get_current_room().objects['armário'].locked)
        self.assertNotIn('bilhete', self.game.inventory)

    def test_repeated_open_does_not_duplicate_contents(self):
        self.run_commands('ir norte', 'ir oeste', 'pegar pé de cabra', 'ir leste',
                          'abrir gaveta', 'pegar chave do armário', 'abrir gaveta',
                          'usar pé de cabra na gaveta', 'examinar retrato', 'examinar retrato')
        self.assertNotIn('chave do armário', self.game.get_current_room().objects)
        self.assertEqual(self.game.inventory.count('chave do armário'), 1)
        self.assertEqual(list(self.game.get_current_room().objects).count('inscrição'), 1)

    def test_inventory_full_drop_and_recover(self):
        room = self.game.get_current_room()
        for i in range(6):
            name = f'item {i}'
            room.add_object(GameObject(name, 'Teste', portable=True))
            self.parser.execute(f'pegar {name}')
        self.assertIn('cheios', self.parser.execute('pegar lanterna'))
        self.assertIn('lanterna', room.objects)
        self.run_commands('equipar item 0', 'largar item 0', 'pegar lanterna')
        self.assertIsNone(self.game.equipped_item)
        self.assertEqual(len(self.game.inventory), 6)
        self.assertIn('item 0', room.objects)
        self.run_commands('largar lanterna', 'pegar item 0')
        self.assertEqual(self.parser.execute('examinar item 0'), 'Teste')

    def test_tea_consumption_and_fear_bounds(self):
        self.run_commands('ir norte', 'ir oeste', 'pegar chá', 'equipar chá')
        self.game.fear = 50
        self.run_commands('inventário', 'usar chá')
        self.assertEqual(self.game.fear, 20)
        self.assertIsNone(self.game.equipped_item)
        self.assertNotIn('chá', self.game.inventory)
        self.run_commands('usar chá')
        self.assertEqual(self.game.fear, 20)
        self.game.reduce_fear(30)
        self.assertEqual(self.game.fear, 0)
        self.game.increase_fear(200)
        self.assertEqual(self.game.fear, 100)

    def test_original_features_and_independent_games(self):
        self.assertIn('Sem sinal', self.parser.execute('checar celular'))
        self.game.phone_signal = True
        self.assertIn('encontrou sinal', self.parser.execute('ver celular'))
        self.run_commands('  PEGAR   lanterna  ', 'segurar lanterna')
        self.assertEqual(self.game.equipped_item, 'lanterna')
        self.assertIn('lanterna', self.parser.execute('inventario'))
        self.assertIn('lanterna', GameState(configuration='prototype').get_current_room().objects)
        self.game.damage(25)
        self.game.heal(10)
        self.assertEqual(self.game.health, 85)
        self.game.damage(100)
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.health, 0)

    def test_cli_exit_and_end_of_input(self):
        for response in ('sair', EOFError, KeyboardInterrupt):
            with self.subTest(response=response), contextlib.redirect_stdout(io.StringIO()):
                kwargs = {'side_effect': response} if isinstance(response, type) else {'return_value': response}
                with patch('builtins.input', **kwargs):
                    main.main()

    def test_cli_restart(self):
        dead = GameState()
        dead.damage(100)
        with patch('main.GameState', side_effect=[dead, GameState()]) as factory:
            with patch('builtins.input', side_effect=['1', 'sair']):
                with contextlib.redirect_stdout(io.StringIO()):
                    main.main()
            self.assertEqual(factory.call_count, 2)


if __name__ == '__main__':
    unittest.main()
