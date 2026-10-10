import unittest
from unittest.mock import Mock, patch

from world import GameObject
from visual_session import VisualSession
from items import WeaponState, WeaponSpec
from audio_events import AudioPlayer, SOUND_EVENTS
import locks
import test_visual_commands as ui


class DocumentsAndKeysTests(unittest.TestCase):
    def setUp(self):
        self.session = VisualSession()
        self.session.start_tutorial(3)
        self.game = self.session.game
        self.room = self.game.get_current_room()
        self.session.execute('pegar chave de arquivo')
        self.key = self.game.item_objects['chave de arquivo']
        self.a = self.room.objects['armário a']
        self.b = self.room.objects['armário b']
        self.game.drain_events()

    def test_reusable_key_consumed_only_after_last_actual_lock(self):
        first = self.session.execute('usar chave de arquivo no armário a')
        self.assertIn('encaixou', first)
        self.assertIn(self.key.name, self.game.inventory)
        self.assertFalse(self.a.locked)
        last = self.session.execute('usar chave de arquivo no armário b')
        self.assertIn('Não vou precisar', last)
        self.assertNotIn(self.key.name, self.game.inventory)
        self.assertFalse(self.b.locked)
        self.assertNotIn('Não vou precisar', self.session.execute('abrir armário b'))

    def test_reopen_and_examine_do_not_consume(self):
        self.session.execute('abrir armário a')
        self.session.execute('examinar armário b')
        self.session.execute('abrir armário a')
        self.assertIn(self.key.name, self.game.inventory)
        self.assertTrue(self.b.locked)

    def test_future_missing_lock_retains_key(self):
        self.key.key_lock_ids.add('future.lock')
        self.session.execute('abrir armário a')
        self.session.execute('abrir armário b')
        self.assertIn(self.key.name, self.game.inventory)

    def test_permanent_key_retained(self):
        self.key.permanent_key = True
        self.session.execute('abrir armário a')
        self.session.execute('abrir armário b')
        self.assertIn(self.key.name, self.game.inventory)

    def test_wrong_lock_id_overrides_matching_name(self):
        self.a.lock_id = 'wrong.id'
        response = self.session.execute('usar chave de arquivo no armário a')
        self.assertIn('não serve', response)
        self.assertTrue(self.a.locked)
        self.assertIn(self.key.name, self.game.inventory)
        self.assertEqual([e['name'] for e in self.game.drain_events()], ['key_wrong'])

    def test_inaccessible_and_blocked_lock_never_consumes(self):
        for attribute in ('blocked', 'accessible'):
            setattr(self.a, attribute, attribute == 'blocked')
            self.assertEqual(locks.unlock(self.game, self.key, self.a), '')
            self.assertTrue(self.a.locked)
            self.assertIn(self.key.name, self.game.inventory)
            setattr(self.a, attribute, attribute == 'accessible')

    def test_key_events_once_per_unlock(self):
        self.session.execute('abrir armário a')
        self.session.execute('abrir armário a')
        self.assertEqual([e['name'] for e in self.game.drain_events()], ['key_use', 'lock_unlock'])

    def test_fixed_document_pages_read_state_and_free_paging(self):
        self.session.start_tutorial(1)
        doc = self.session.game.get_current_room().objects['aviso fixo']
        self.assertFalse(doc.was_read)
        self.session.execute('ler aviso fixo')
        before = self.session.game.snapshot()
        self.session.turn_page(1)
        self.session.turn_page(1)
        self.assertEqual(self.session.reading_page, 1)
        self.assertEqual(doc.read_pages, {0, 1})
        self.assertTrue(doc.was_read)
        self.assertEqual(self.session.game.snapshot(), before)
        self.session.execute('fechar leitura')
        self.assertIsNone(self.session.reading_text)
        self.assertIn(doc.name, self.session.game.get_current_room().objects)
        self.assertNotIn(doc.name, self.session.game.inventory)

    def test_portable_document_preserves_identity_and_pages(self):
        self.session.start_tutorial(2)
        doc = self.session.game.get_current_room().objects['carta antiga']
        self.session.execute('pegar carta antiga')
        self.session.execute('ler carta antiga')
        self.assertIs(self.session.reading_document, doc)
        self.assertIs(self.session.game.item_objects[doc.name], doc)
        self.assertEqual(len(doc.pages), 2)
        events = [e['name'] for e in self.session.game.drain_events()]
        self.assertIn('document_collect', events)
        self.assertIn('document_open', events)

    def test_document_ids_unique_and_inaccessible_read_fails(self):
        a, b = GameObject('a', '', text='a'), GameObject('b', '', text='b', accessible=False)
        self.assertNotEqual(a.object_id, b.object_id)
        self.room.objects['b'] = b
        self.session.execute('ler b')
        self.assertFalse(b.was_read)
        self.assertIsNone(self.session.reading_document)

    def test_pistol_capacity_initial_and_partial_reload(self):
        gun = WeaponState()
        self.assertEqual((gun.spec.capacity, gun.ammo, gun.spec.damage), (12, 2, 35))
        self.assertEqual(gun.reload(3), 3)
        self.assertEqual(gun.ammo, 5)
        self.assertEqual(gun.reload(20), 7)
        self.assertEqual(gun.ammo, 12)
        self.assertEqual(gun.reload(20), 0)
        self.assertEqual(WeaponState(spec=WeaponSpec(initial_ammo=4)).ammo, 4)

    def test_audio_missing_files_and_invalid_backend_safe(self):
        backend = Mock()
        player = AudioPlayer(backend=backend)
        with patch('pathlib.Path.is_file', return_value=False):
            player.handle([{'name': name} for name in SOUND_EVENTS])
        backend.assert_not_called()
        with patch('pathlib.Path.is_file', return_value=True):
            player.handle([{'name': name} for name in SOUND_EVENTS])
        self.assertEqual(backend.call_count, 12)
        backend.side_effect = RuntimeError('audio unavailable')
        with patch('pathlib.Path.is_file', return_value=True):
            player.handle([{'name': 'document_open'}])

    def test_door_open_close_events(self):
        self.session.start_tutorial(1)
        self.session.execute('abrir porta de teste')
        self.session.execute('fechar porta de teste')
        names = [e['name'] for e in self.session.game.drain_events()]
        self.assertEqual(names, ['door_open', 'door_close'])


class DocumentPanelTests(unittest.TestCase):
    setUp = ui.VisualCommandTests.setUp
    tearDown = ui.VisualCommandTests.tearDown
    enter = ui.VisualCommandTests.enter

    def test_embedded_reader_blocks_physical_actions_and_returns_focus(self):
        self.enter('ler carta antiga')
        app = self.app
        self.assertEqual(app.reader_window.winfo_class(), 'Frame')
        self.assertIs(app.root.grab_current(), app.reader_window)
        self.assertIs(app.root.focus_get(), app.reader_panel.inspect_entry)
        before = app.session.game.snapshot()
        self.enter('pegar pistola')
        self.assertEqual(app.session.game.snapshot(), before)
        app.reader_panel.next.invoke()
        self.assertEqual(app.session.reading_page, 1)
        self.assertEqual(app.session.game.snapshot(), before)
        app.reader_panel.back.invoke()
        app.root.update()
        self.assertIsNone(app.reader_window)
        self.assertIs(app.root.focus_get(), app.command_entry)

    def test_reader_resize_scroll_and_escape(self):
        self.enter('ler carta antiga')
        app = self.app
        for size in ('1400x900', '1100x760'):
            app.root.geometry(size)
            app.root.update()
            back = app.reader_panel.back
            self.assertLessEqual(back.winfo_rootx()+back.winfo_width(), app.root.winfo_rootx()+app.root.winfo_width())
            self.assertLessEqual(back.winfo_rooty()+back.winfo_height(), app.root.winfo_rooty()+app.root.winfo_height())
        app.reader_panel.back.event_generate('<Escape>')
        app.root.update()
        self.assertIsNone(app.reader_window)
        self.assertIsNone(app.root.grab_current())

    def test_inventory_document_content_without_second_panel(self):
        self.enter('pegar carta antiga')
        self.enter('inventário')
        app = self.app
        before = app.session.game.snapshot()
        app.inventory_view.select(app.session.game.inventory.index('carta antiga'))
        doc = app.session.game.item_objects['carta antiga']
        self.assertTrue(doc.was_read)
        self.assertEqual(doc.read_pages, {0, 1})
        self.assertIsNone(app.reader_window)
        self.assertEqual(app.session.game.snapshot(), before)
        self.assertFalse(any(w.winfo_class() == 'Toplevel' for w in ui.all_widgets(app.root)))

    def test_reading_in_combat_costs_one_action_then_pages_are_free(self):
        app = self.app
        app.start_tutorial(4)
        self.enter('ir norte')
        self.enter('esperar')
        app.session.game.get_current_room().objects['nota'] = GameObject('nota', '', text='Primeira', pages=['Segunda'])
        turn = app.session.game.turn_count
        self.enter('ler nota')
        self.assertEqual(app.session.game.turn_count, turn+1)
        self.assertEqual(app.session.game.health, 84)
        before = app.session.game.snapshot()
        app.reader_panel.next.invoke()
        self.enter('atacar')
        self.assertEqual(app.session.game.snapshot(), before)


if __name__ == '__main__':
    unittest.main()
