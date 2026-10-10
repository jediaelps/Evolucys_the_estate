import unittest
from unittest.mock import patch
from visual_session import VisualSession


class CommandHistoryTests(unittest.TestCase):
    def setUp(self):
        self.session = VisualSession()
        self.session.start_tutorial(2)

    def test_command_is_forwarded_to_existing_parser_once(self):
        with patch.object(self.session.parser, 'execute', wraps=self.session.parser.execute) as execute:
            self.session.execute('pegar bandagem')
            execute.assert_called_once_with('pegar bandagem')
        self.assertIn('bandagem', self.session.game.inventory)
        self.assertEqual(self.session.game.turn_count, 1)

    def test_history_discards_oldest_pair(self):
        commands = ['olhar', 'status', 'inventário', 'ajuda', 'examinar pistola']
        for command in commands:
            self.session.execute(command)
        self.assertEqual(len(self.session.history), 4)
        self.assertEqual([entry[0] for entry in self.session.history], commands[1:])
        self.assertTrue(all(response for _, response in self.session.history))

    def test_blank_command_keeps_history_and_turns(self):
        self.session.execute('status')
        before = list(self.session.history)
        self.session.execute('   ')
        self.assertEqual(list(self.session.history), before)
        self.assertEqual(self.session.game.turn_count, 0)

    def test_reset_and_tutorial_switch_clear_history(self):
        self.session.execute('pegar pistola')
        self.session.reset()
        self.assertFalse(self.session.history)
        self.assertFalse(self.session.game.inventory)
        self.session.execute('status')
        self.session.start_tutorial(3)
        self.assertFalse(self.session.history)

    def test_contextual_responses_preserved(self):
        self.assertIn('pegar lanterna primeiro', self.session.execute('usar lanterna'))
        self.session.execute('pegar lanterna')
        self.assertIn('lanterna na mão primeiro', self.session.execute('usar lanterna'))
        self.assertIn('lanterna na mão primeiro', self.session.history[-1][1])

    def test_history_contains_enemy_reaction_and_protection(self):
        self.session.start_tutorial(4)
        self.session.execute('ir norte')
        self.session.execute('esperar')
        self.session.game.health = 1
        self.session.execute('esperar')
        command, response = self.session.history[-1]
        self.assertEqual(command, 'esperar')
        self.assertIn('golpeia', response)
        self.assertIn('morte impedida', response)

    def test_admin_history_is_distinct_and_free(self):
        self.session.debug('dano')
        self.assertEqual(self.session.history[-1][0], '[TESTE] dano')
        self.assertEqual(self.session.game.turn_count, 0)


if __name__ == '__main__':
    unittest.main()
