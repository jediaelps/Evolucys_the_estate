import unittest
import test_visual_commands as base


class VisualUXTests(unittest.TestCase):
    setUp = base.VisualCommandTests.setUp
    tearDown = base.VisualCommandTests.tearDown
    enter = base.VisualCommandTests.enter
    scene_text = base.VisualCommandTests.scene_text

    def test_inventory_hidden_until_command_and_closed_again(self):
        self.assertFalse(self.app.inventory_frame.winfo_ismapped())
        self.enter('inventário')
        self.assertTrue(self.app.inventory_frame.winfo_ismapped())
        self.assertEqual(len(self.app.slot_labels), 6)
        self.enter('fechar inventário')
        self.assertFalse(self.app.inventory_frame.winfo_ismapped())
        self.enter('abrir inventário')
        self.assertTrue(self.app.inventory_frame.winfo_ismapped())
        self.assertEqual(self.app.session.game.turn_count, 0)

    def test_hand_updates_without_opening_inventory(self):
        self.enter('pegar pistola')
        self.enter('equipar pistola')
        self.assertIn('pistola', self.app.hand.get())
        self.assertFalse(self.app.inventory_frame.winfo_ismapped())
        self.enter('largar pistola')
        self.assertIn('nada', self.app.hand.get())

    def test_long_help_reader_and_close_command(self):
        self.enter('ajuda comandos')
        self.assertIsNotNone(self.app.reader_window)
        self.assertIn('EXPLORAÇÃO', self.app.reader_text.get('1.0', 'end'))
        self.assertLess(len(self.app.history_view.get('1.0', 'end')), 500)
        self.enter('fechar leitura')
        self.assertIsNone(self.app.reader_window)
        self.assertEqual(self.app.session.game.turn_count, 0)

    def test_full_exploration_by_enter_with_reading_return_reset(self):
        self.app.start_tutorial(1)
        for command in ('olhar', 'examinar mesa', 'usar lanterna', 'pegar lanterna',
                        'examinar caixa', 'abrir caixa', 'ler o bilhete'):
            self.enter(command)
            if command.startswith('examinar '):
                self.app.reader_panel.back.invoke()
        self.assertIn('Nada aqui altera a mansão', self.app.reader_text.get('1.0', 'end'))
        self.enter('fechar leitura')
        self.enter('passar pela porta')
        self.assertIn('fechada', self.app.session.last_message)
        self.enter('abrir porta')
        self.enter('entrar pela porta')
        self.assertIn('Sala adjacente', self.scene_text())
        self.enter('atravessar porta')
        self.assertEqual(self.app.session.game.current_location, 'test_start')
        self.app.reset()
        self.app.root.update()
        self.assertFalse(self.app.session.history)
        self.assertFalse(self.app.session.game.inventory)
        self.assertFalse(self.app.inventory_frame.winfo_ismapped())


if __name__ == '__main__':
    unittest.main()
