"""Testes de widgets e eventos reais, sem comparar posições fixas ou pixels.

Em ambiente sem display/Tk, a suíte é explicitamente ignorada.
"""
import unittest
from unittest.mock import patch

try:
    import tkinter as tk
    from visual import VisualApp
except ImportError:
    tk = None


def all_widgets(widget):
    for child in widget.winfo_children():
        yield child
        yield from all_widgets(child)


class VisualCommandTests(unittest.TestCase):
    def setUp(self):
        if tk is None:
            self.skipTest('Tkinter indisponível')
        try:
            self.app = VisualApp()
        except tk.TclError as error:
            self.skipTest(f'Sessão gráfica indisponível: {error}')
        self.app.start_tutorial(2)
        self.app.root.update()
        self.app.command_entry.focus_force()
        self.app.root.update()

    def tearDown(self):
        if hasattr(self, 'app'):
            self.app.root.destroy()

    def enter(self, command):
        entry = (self.app.reader_panel.inspect_entry if self.app.reader_window is not None
                 else self.app.command_entry)
        entry.delete(0, 'end')
        entry.insert(0, command)
        entry.focus_force()
        self.app.root.update()
        entry.event_generate('<Return>')
        self.app.root.update()

    def scene_text(self):
        c = self.app.canvas
        return [c.itemcget(item, 'text') for item in c.find_all() if c.type(item) == 'text']

    def test_enter_executes_parser_once_and_keeps_focus(self):
        parser = self.app.session.parser
        with patch.object(parser, 'execute', wraps=parser.execute) as execute:
            self.enter('pegar bandagem')
            execute.assert_called_once_with('pegar bandagem')
        self.assertIn('bandagem', self.app.session.game.inventory)
        self.assertEqual(self.app.command_entry.get(), '')
        self.assertIs(self.app.root.focus_get(), self.app.command_entry)

    def test_scene_updates_after_pickup_and_move(self):
        self.assertIn('bandagem', self.scene_text())
        self.enter('pegar bandagem')
        self.assertNotIn('bandagem', self.scene_text())
        self.enter('ir norte')
        self.assertIn('Sala adjacente', self.scene_text())

    def test_inventory_and_hud_share_game_state(self):
        self.enter('pegar pistola')
        self.enter('equipar pistola')
        self.assertIn('pistola', self.app.hud.get())
        self.assertIn('Munição 2/12', self.app.hud.get())
        self.assertTrue(any('pistola' in label.cget('text') for label in self.app.slot_labels))
        self.app.debug('dano')
        canvas = self.app.indicators
        values = [canvas.itemcget(item, 'text') for item in canvas.find_all() if canvas.type(item) == 'text']
        self.assertIn('Vida 75', values)
        self.assertIn('sem sinal', values)

    def test_history_widget_contains_only_last_four_pairs(self):
        for command in ('status', 'inventário', 'usar lanterna', 'pegar lanterna', 'equipar lanterna'):
            self.enter(command)
        text = self.app.history_view.get('1.0', 'end')
        self.assertNotIn('> status', text)
        self.assertEqual(text.count('> '), 4)
        self.assertIn('> equipar lanterna', text)

    def test_old_keys_only_type_text_without_actions(self):
        before = self.app.session.game.snapshot()
        for key in 'wasdefr':
            self.app.command_entry.event_generate(f'<KeyPress-{key}>')
            self.app.command_entry.event_generate(f'<KeyRelease-{key}>')
        self.app.root.update()
        self.assertEqual(self.app.command_entry.get(), 'wasdefr')
        self.assertEqual(self.app.session.game.snapshot(), before)
        self.app.canvas.focus_set()
        for key in 'wasdefr':
            self.app.canvas.event_generate(f'<KeyPress-{key}>')
        self.app.root.update()
        self.assertEqual(self.app.session.game.snapshot(), before)

    def test_scene_and_inventory_clicks_do_not_execute_actions(self):
        before = self.app.session.game.snapshot()
        self.app.canvas.event_generate('<Button-1>', x=150, y=150)
        self.app.slot_labels[0].event_generate('<Button-1>')
        self.app.root.update()
        self.assertEqual(self.app.session.game.snapshot(), before)
        buttons = [w.cget('text') for w in all_widgets(self.app.root) if isinstance(w, tk.Button)]
        for forbidden in ('Pegar', 'Abrir', 'Usar', 'Equipar', 'Atacar', 'Defender', 'Recarregar [R]'):
            self.assertNotIn(forbidden, buttons)

    def test_combat_by_enter_includes_reaction_in_history(self):
        self.app.start_tutorial(4)
        self.enter('pegar pistola')
        self.enter('ir norte')
        self.enter('esperar')
        self.enter('equipar pistola')
        self.assertEqual(self.app.session.game.health, 84)
        self.assertIn('golpeia', self.app.history_view.get('1.0', 'end'))

    def test_pause_preserves_history_and_focus(self):
        self.enter('olhar')
        before = list(self.app.session.history)
        self.app.command_entry.event_generate('<Escape>')
        self.app.root.update()
        self.assertEqual(self.app.screen, 'pause')
        self.app.root.event_generate('<Escape>')
        self.app.root.update()
        self.assertEqual(self.app.screen, 'game')
        self.assertEqual(list(self.app.session.history), before)
        self.assertIs(self.app.root.focus_get(), self.app.command_entry)

    def test_menu_and_all_tutorials_keep_campaign_isolated(self):
        self.app.start_campaign()
        campaign = self.app.session.game
        before = campaign.snapshot()
        self.app.leave()
        for number in range(1, 5):
            self.app.start_tutorial(number)
            self.enter('olhar')
            self.app.debug('dano')
            self.app.reset()
            self.assertFalse(self.app.session.history)
        self.assertEqual(campaign.snapshot(), before)
        self.app.leave()
        continuing = next(w for w in all_widgets(self.app.root)
                          if isinstance(w, tk.Button) and w.cget('text').startswith('Continuar'))
        self.assertEqual(continuing.cget('state'), 'disabled')


if __name__ == '__main__':
    unittest.main()

