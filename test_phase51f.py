"""Fase 5.1F: inspeção compartilhada, eventos reais e limites do contexto."""
import unittest
from unittest.mock import patch
from world import GameObject
from visual_session import VisualSession
import test_visual_commands as ui
import feedback


class InspectionSessionTests(unittest.TestCase):
    def setUp(self):
        self.session = VisualSession()
        self.session.start_tutorial(2)
        self.game = self.session.game
        self.obj = GameObject('mesa', 'Madeira gasta pelo tempo.')
        self.game.get_current_room().add_object(self.obj)

    def test_simple_object_needs_no_faces_or_secrets(self):
        turn = self.game.turn_count
        self.session.execute('examinar mesa')
        self.assertIs(self.session.inspection_object, self.obj)
        self.assertIsNone(self.session.inspection_face)
        self.assertEqual(self.session.reading_text, self.obj.description)
        self.assertEqual(self.obj.inspection_faces, {})
        self.assertFalse(self.obj.inspected_faces)
        self.assertEqual(self.game.turn_count, turn + 1)

    def test_inaccessible_object_does_not_open_panel(self):
        self.obj.accessible = False
        self.session.execute('examinar mesa')
        self.assertIsNone(self.session.reading_text)
        self.assertIn(self.obj.inaccessible_reason, self.session.last_message)

    def test_locked_contents_stay_hidden_without_artificial_faces(self):
        self.obj.locked = True
        self.obj.contents = [GameObject('segredo', 'oculto', portable=True)]
        self.session.execute('examinar mesa')
        self.assertNotIn('segredo', self.session.reading_text)
        self.session.execute('olhar dentro da mesa')
        self.assertTrue(self.obj.locked)
        self.assertNotIn('segredo', self.game.get_current_room().objects)
        self.assertEqual(len(self.obj.contents), 1)

    def test_context_unknown_and_physical_commands_are_free_and_safe(self):
        self.session.parser.inspection_context = 'mesa'
        before = self.game.snapshot()
        self.assertEqual(self.session.execute('abracadabra'), feedback.UNKNOWN)
        self.assertIn('Volte à exploração', self.session.execute('pegar pistola'))
        self.assertEqual(before, self.game.snapshot())

    def test_hidden_objects_only_reveal_on_existing_examine_rule(self):
        hidden = GameObject('marca', 'Uma marca discreta.')
        self.obj.hidden_objects = [hidden]
        self.session.execute('olhar em volta')
        self.assertNotIn('marca', self.game.get_current_room().objects)
        self.assertNotIn('marca', self.session.last_message)
        self.session.execute('examinar mesa')
        self.assertIs(self.game.get_current_room().objects['marca'], hidden)
        self.assertEqual(self.obj.inspection_faces, {})


class InspectionPanelTests(unittest.TestCase):
    setUp = ui.VisualCommandTests.setUp
    tearDown = ui.VisualCommandTests.tearDown
    enter = ui.VisualCommandTests.enter

    def panel_enter(self, command):
        entry = self.app.reader_panel.inspect_entry
        entry.delete(0, 'end')
        entry.insert(0, command)
        entry.event_generate('<Return>')
        self.app.root.update()

    def simple_panel(self):
        obj = GameObject('mesa', 'Madeira gasta pelo tempo.')
        self.app.session.game.get_current_room().add_object(obj)
        self.enter('examinar mesa')
        return obj

    def test_edit_enter_once_focus_and_missing_face_response(self):
        obj = self.simple_panel()
        panel = self.app.reader_panel
        entry = panel.inspect_entry
        self.assertTrue(entry.winfo_ismapped())
        self.assertEqual(self.app.command_entry.cget('state'), 'disabled')
        self.assertIs(self.app.root.focus_get(), entry)
        entry.insert(0, 'texto errado')
        entry.delete(0, 'end')
        parser = self.app.session.parser
        turn = self.app.session.game.turn_count
        with patch.object(parser, 'execute', wraps=parser.execute) as execute:
            self.panel_enter('observar a mesa')
            execute.assert_called_once_with('observar a mesa')
        self.assertEqual(self.app.session.game.turn_count, turn + 1)
        self.assertIs(self.app.reader_panel, panel)
        self.assertIs(self.app.root.focus_get(), entry)
        self.assertEqual(entry.get(), '')
        self.panel_enter('olhar atrás da mesa')
        self.assertTrue(panel.response.get())
        self.assertEqual(obj.inspection_faces, {})
        self.assertIn(obj.description, panel.text.get('1.0', 'end'))
        self.panel_enter('abracadabra')
        self.assertEqual(panel.response.get(), feedback.UNKNOWN)

    def test_portable_requires_return_and_close_navigation_is_free(self):
        self.enter('examinar bandagem')
        before = self.app.session.game.snapshot()
        self.panel_enter('pegar bandagem')
        self.assertEqual(before, self.app.session.game.snapshot())
        self.app.reader_panel.back.invoke()
        self.app.root.update()
        self.assertIsNone(self.app.reader_window)
        self.assertEqual(self.app.command_entry.cget('state'), 'normal')
        self.assertEqual(before, self.app.session.game.snapshot())
        self.assertIs(self.app.root.focus_get(), self.app.command_entry)
        self.enter('pegar bandagem')
        self.assertIn('bandagem', self.app.session.game.inventory)

    def test_escape_and_resize_keep_one_panel_and_restore_exploration(self):
        self.simple_panel()
        before = self.app.session.game.snapshot()
        for size in ('1100x760', '980x680'):
            self.app.root.geometry(size)
            self.app.root.update()
            panel = self.app.reader_panel
            for widget in (panel.inspect_entry, panel.back, panel.text):
                self.assertTrue(widget.winfo_ismapped())
                self.assertGreater(widget.winfo_height(), 1)
                self.assertLessEqual(widget.winfo_rooty() + widget.winfo_height(), panel.frame.winfo_rooty() + panel.frame.winfo_height())
            self.assertEqual(len([w for w in ui.all_widgets(panel.frame) if isinstance(w, ui.tk.Entry)]), 1)
        self.app.reader_panel.inspect_entry.event_generate('<Escape>')
        self.app.root.update()
        self.assertIsNone(self.app.reader_window)
        self.assertEqual(self.app.command_entry.cget('state'), 'normal')
        self.assertEqual(before, self.app.session.game.snapshot())
        self.assertIs(self.app.root.focus_get(), self.app.command_entry)

    def test_inventory_inspection_reuses_inventory_entry(self):
        self.enter('pegar bandagem')
        self.enter('inventário')
        entry = self.app.inventory_view.entry
        entry.insert(0, 'examinar bandagem')
        entry.event_generate('<Return>')
        self.app.root.update()
        self.assertIsNone(self.app.reader_window)
        self.assertIs(self.app.root.focus_get(), entry)
        self.assertTrue(self.app.inventory_view.result.get())
        self.assertEqual(len(self.app.inventory_view.slots), 6)

    def test_combat_inspection_reacts_once_and_close_never_reacts(self):
        self.app.start_tutorial(4)
        self.enter('ir norte')
        self.enter('esperar')
        game = self.app.session.game
        game.get_current_room().add_object(GameObject('mesa', 'Madeira gasta.'))
        turn = game.turn_count
        confrontation = self.app.session.parser.confrontation
        with patch.object(confrontation, 'react', wraps=confrontation.react) as react:
            self.enter('examinar mesa')
            react.assert_called_once()
        self.assertEqual(game.turn_count, turn + 1)
        self.assertIn('golpeia', self.app.session.history[-1][1])
        before = game.snapshot()
        self.app.reader_panel.back.invoke()
        self.app.root.update()
        self.assertEqual(before, game.snapshot())


if __name__ == '__main__':
    unittest.main()
