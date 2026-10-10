import unittest
from unittest.mock import patch
import test_visual_commands as base


class InventoryWindowTests(unittest.TestCase):
    setUp = base.VisualCommandTests.setUp
    tearDown = base.VisualCommandTests.tearDown
    enter = base.VisualCommandTests.enter
    scene_text = base.VisualCommandTests.scene_text

    def test_window_grid_and_selection_are_read_only(self):
        self.enter('pegar bandagem')
        self.enter('inventário')
        view = self.app.inventory_view
        self.assertTrue(view.window.winfo_ismapped())
        self.assertEqual([(int(b.grid_info()['row']), int(b.grid_info()['column'])) for b in view.slots],
                         [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)])
        before = self.app.session.game.snapshot()
        view.slots[0].invoke()
        self.assertIn('BANDAGEM', view.description.get('1.0', 'end'))
        self.assertEqual(self.app.session.game.snapshot(), before)
        self.assertEqual(view.actions['usar'].cget('state'), 'disabled')
        view.actions['usar'].invoke()
        self.assertIn('bandagem', self.app.session.game.inventory)

    def test_use_button_matches_parser_and_updates_slots(self):
        self.enter('pegar bandagem')
        self.app.debug('dano')
        self.enter('inventário')
        view = self.app.inventory_view
        view.slots[0].invoke()
        parser = self.app.session.parser
        with patch.object(parser, 'execute', wraps=parser.execute) as execute:
            view.actions['usar'].invoke()
            execute.assert_called_once_with('usar bandagem')
        self.assertEqual(self.app.session.game.health, 95)
        self.assertNotIn('bandagem', self.app.session.game.inventory)
        self.assertIn('Vazio', view.slots[0].cget('text'))
        self.assertIn('recupero', view.result.get())

    def test_mouse_equip_and_drop_cost_turn_in_combat(self):
        self.app.start_tutorial(4)
        for command in ('pegar pistola', 'ir norte', 'esperar', 'inventário'):
            self.enter(command)
        view = self.app.inventory_view
        view.slots[0].invoke()
        before = self.app.session.game.turn_count
        view.actions['equipar'].invoke()
        self.assertEqual(self.app.session.game.turn_count, before + 1)
        self.assertEqual(self.app.session.game.health, 84)
        self.assertIn('pistola', self.app.hand.get())
        self.app.session.game.get_current_room().enemy.preparing = True
        view.actions['largar'].invoke()
        self.assertEqual(self.app.session.game.health, 68)
        self.assertIn('nada', self.app.hand.get())
        self.assertIn('pistola', self.app.session.game.get_current_room().objects)

    def test_examine_uses_current_parser_turn_rules(self):
        self.enter('pegar lanterna')
        self.enter('inventário')
        view = self.app.inventory_view
        view.slots[0].invoke()
        before = self.app.session.game.turn_count
        view.actions['examinar'].invoke()
        self.assertEqual(self.app.session.game.turn_count, before + 1)
        self.assertIn('lanterna', view.result.get())

    def test_close_button_escape_and_command_preserve_state(self):
        self.enter('pegar pistola')
        self.enter('inventário')
        before = self.app.session.game.snapshot()
        self.app.inventory_view.close()
        self.app.root.update()
        self.assertFalse(self.app.inventory_frame.winfo_ismapped())
        self.enter('inventário')
        self.app.inventory_view.window.event_generate('<Escape>')
        self.app.root.update()
        self.assertEqual(self.app.screen, 'game')
        self.assertFalse(self.app.session.inventory_open)
        self.enter('abrir inventário')
        self.enter('fechar inventário')
        self.assertEqual(self.app.session.game.snapshot(), before)

    def test_mouse_healing_allows_exactly_one_reaction(self):
        self.app.start_tutorial(4)
        for command in ('pegar bandagem', 'ir norte', 'esperar', 'inventário'):
            self.enter(command)
        self.app.session.game.health = 50
        view = self.app.inventory_view
        view.slots[0].invoke()
        before = self.app.session.game.turn_count
        view.actions['usar'].invoke()
        self.assertEqual(self.app.session.game.health, 54)
        self.assertEqual(self.app.session.game.turn_count, before+1)

    def test_stairs_full_visual_flow(self):
        self.app.start_campaign()
        self.app.session.game.current_location = 'T01'
        for command in ('ir norte', 'subir as escadas', 'olhar', 'examinar quadro'):
            self.enter(command)
        self.assertIn('Galeria Superior', self.scene_text())
        self.assertIs(self.app.session.game.get_current_room(), self.app.session.game.get_room('U01'))
        self.app.reader_panel.back.invoke()
        self.enter('descer escada')
        self.assertIn('Salão Principal', self.scene_text())
        self.assertEqual(self.app.session.game.current_location, 'main_hall')

    def test_keyboard_actions_sync_open_inventory(self):
        self.enter('pegar pistola')
        self.enter('inventário')
        self.enter('equipar pistola')
        self.assertIn('NA MÃO', self.app.inventory_view.slots[0].cget('text'))
        self.enter('largar pistola')
        self.assertIn('Vazio', self.app.inventory_view.slots[0].cget('text'))


if __name__ == '__main__':
    unittest.main()
