import tkinter as tk
import unittest
from unittest.mock import patch
import test_visual_commands as base


class InventoryOverlayTests(unittest.TestCase):
    setUp = base.VisualCommandTests.setUp
    tearDown = base.VisualCommandTests.tearDown
    enter = base.VisualCommandTests.enter

    def test_inventory_is_embedded_frame_without_new_native_window(self):
        with patch('tkinter.Toplevel', side_effect=AssertionError('Inventário não deve abrir janela nativa')):
            self.enter('inventário')
        view = self.app.inventory_view
        self.assertIsInstance(view.window, tk.Frame)
        self.assertIs(view.window.master, self.app.root)
        self.assertIs(view.window.winfo_toplevel(), self.app.root)
        self.assertTrue(self.app.canvas.find_withtag('inventory_shade'))

    def test_open_close_are_free_and_return_focus_and_scene(self):
        game = self.app.session.game
        original = game.snapshot()
        self.enter('inventário')
        self.assertIs(self.app.root.focus_get(), self.app.inventory_view.entry)
        self.assertIs(self.app.root.grab_current(), self.app.inventory_view.window)
        self.app.inventory_view.close_button.invoke()
        self.app.root.update()
        self.assertIs(self.app.root.focus_get(), self.app.command_entry)
        self.assertIsNone(self.app.root.grab_current())
        self.assertEqual(game.snapshot(), original)
        self.assertFalse(self.app.canvas.find_withtag('inventory_shade'))

    def test_exploration_commands_are_blocked_before_parser_and_turn(self):
        self.enter('inventário')
        game = self.app.session.game
        original = game.snapshot()
        with patch.object(self.app.session.parser, 'execute', wraps=self.app.session.parser.execute) as execute:
            for command in ('ir norte', 'olhar em volta', 'pegar pistola', 'atacar', 'fugir norte'):
                self.enter(command)
            execute.assert_not_called()
        self.assertEqual(game.snapshot(), original)
        self.assertIn('Feche o inventário', self.app.inventory_view.result.get())

    def test_panel_entry_item_action_and_combat_reaction(self):
        self.app.start_tutorial(4)
        for command in ('pegar pistola', 'ir norte', 'esperar', 'inventário'):
            self.enter(command)
        view = self.app.inventory_view
        before = self.app.session.game.turn_count
        view.entry.insert(0, 'equipar pistola')
        view.entry.focus_force()
        self.app.root.update()
        view.entry.event_generate('<Return>')
        self.app.root.update()
        self.assertEqual(self.app.session.game.health, 84)
        self.assertEqual(self.app.session.game.turn_count, before+1)
        self.assertIn('pistola', self.app.hand.get())

    def test_escape_closes_panel_before_pause(self):
        self.enter('inventário')
        view = self.app.inventory_view
        view.entry.event_generate('<Escape>')
        self.app.root.update()
        self.assertFalse(self.app.session.inventory_open)
        self.assertEqual(self.app.screen, 'game')
        self.app.command_entry.event_generate('<Escape>')
        self.app.root.update()
        self.assertEqual(self.app.screen, 'pause')

    def test_resize_keeps_panel_centered_and_controls_inside(self):
        self.enter('inventário')
        view = self.app.inventory_view
        sizes = []
        for geometry in ('1100x760', '1400x900', '1200x800'):
            self.app.root.geometry(geometry)
            self.app.root.update()
            panel = view.window
            width, height = panel.winfo_width(), panel.winfo_height()
            sizes.append((width, height))
            self.assertAlmostEqual(panel.winfo_x()+width/2, self.app.root.winfo_width()/2, delta=2)
            self.assertAlmostEqual(panel.winfo_y()+height/2, self.app.root.winfo_height()/2, delta=2)
            for widget in [view.close_button, view.entry, view.description, *view.slots, *view.actions.values()]:
                self.assertTrue(widget.winfo_ismapped())
                x = widget.winfo_rootx()-panel.winfo_rootx()
                y = widget.winfo_rooty()-panel.winfo_rooty()
                self.assertGreaterEqual(x, 0)
                self.assertGreaterEqual(y, 0)
                self.assertLessEqual(x+widget.winfo_width(), width)
                self.assertLessEqual(y+widget.winfo_height(), height)
        self.assertNotEqual(sizes[0], sizes[1])

    def test_long_text_is_scrollable_without_moving_close_button(self):
        self.enter('pegar bandagem')
        self.app.session.game.item_objects['bandagem'].description = 'Descrição longa. ' * 500
        self.enter('inventário')
        view = self.app.inventory_view
        view.select(0)
        view.result.set('Resultado extenso. ' * 500)
        self.app.root.update()
        self.assertLess(view.description.yview()[1], 1)
        self.assertLess(view.result_text.yview()[1], 1)
        self.assertTrue(view.close_button.winfo_ismapped())

    def test_selection_and_blocked_commands_do_not_spend_buff(self):
        self.enter('pegar energético')
        self.enter('pegar bandagem')
        self.enter('usar energético')
        self.enter('inventário')
        original = self.app.session.game.snapshot()
        self.app.inventory_view.select(0)
        self.enter('ir norte')
        self.app.inventory_view.close()
        self.assertEqual(self.app.session.game.snapshot(), original)


if __name__ == '__main__':
    unittest.main()
