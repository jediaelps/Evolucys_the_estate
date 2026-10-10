import unittest
from unittest.mock import patch
from pathlib import Path

from visual_session import VisualSession
from world import GameObject
from command_language import normalize
from visual_assets import SpriteSpec, scene_sprites, enemy_state, object_state, ASSETS
from inventory_view import item_details
from context_help import help_text
import test_visual_commands as ui


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.session = VisualSession()
        self.session.start_tutorial(1)
        self.game = self.session.game
        self.portrait = self.game.get_current_room().objects['retrato antigo']

    def test_document_content_separated_from_history(self):
        self.session.execute('ler aviso fixo')
        doc = self.session.reading_document
        self.assertEqual(self.session.reading_text, doc.pages[0])
        self.assertNotIn(doc.pages[0], self.session.history[-1][1])
        self.assertLess(len(self.session.history[-1][1]), 80)

    def test_examine_document_also_keeps_content_out_of_history(self):
        self.session.execute('examinar aviso fixo')
        self.assertIsNotNone(self.session.reading_document)
        self.assertNotIn(self.session.reading_text, self.session.history[-1][1])

    def test_front_back_and_hidden_inscription(self):
        self.session.execute('examinar retrato antigo')
        self.assertEqual(self.session.inspection_face, 'front')
        self.assertNotIn('relógio', self.session.reading_text)
        turn = self.game.turn_count
        self.session.execute('olhar atrás do retrato')
        self.assertEqual(self.session.inspection_face, 'back')
        self.assertIn('relógio', self.session.reading_text)
        self.assertNotIn('relógio', self.session.history[-1][1])
        self.assertEqual(self.game.turn_count, turn + 1)
        self.assertEqual(self.portrait.inspected_faces, {'front', 'back'})

    def test_face_aliases_resolve_only_visible_objects(self):
        for command in ('virar o retrato', 'inspecionar o verso do retrato', 'olhar atras do retrato'):
            self.assertEqual(normalize(self.game, command), 'inspecionar back retrato antigo')
        self.assertNotEqual(normalize(self.game, 'virar bilhete'), 'inspecionar back bilhete de teste')

    def test_unsupported_face_does_not_turn_or_open_object(self):
        self.session.execute('virar mesa de teste')
        self.assertIsNone(self.session.inspection_object)
        self.assertIn('Não consigo', self.session.last_message)
        self.assertFalse(self.game.get_current_room().objects['mesa de teste'].opened)

    def test_interior_requires_open_unlocked_container(self):
        box = self.game.get_current_room().objects['caixa']
        self.session.execute('olhar dentro da caixa')
        self.assertIn('Preciso abrir', self.session.last_message)
        self.assertFalse(box.inspected_faces)
        self.session.execute('abrir caixa')
        self.session.execute('olhar dentro da caixa')
        self.assertEqual(self.session.inspection_face, 'interior')
        self.assertIn('forro', self.session.reading_text)

    def test_inaccessible_inspection(self):
        self.portrait.accessible = False
        self.session.execute('virar retrato')
        self.assertIsNone(self.session.inspection_object)
        self.assertFalse(self.portrait.inspected_faces)

    def test_object_states_follow_actual_state(self):
        box = self.game.get_current_room().objects['caixa']
        self.assertEqual(object_state(box), 'closed')
        self.session.execute('abrir caixa')
        self.assertEqual(object_state(box), 'open')
        box.damaged = True
        self.assertEqual(object_state(box), 'damaged')

    def test_sprite_identity_visibility_and_layers(self):
        self.portrait.sprite.layer = -2
        self.portrait.sprite.position = (.25, .5)
        entries = scene_sprites(self.game.get_current_room())
        self.assertIs(entries[0][1], self.portrait)
        self.assertEqual(self.portrait.sprite.object_id, self.portrait.object_id)
        self.portrait.sprite.visible = False
        self.assertNotIn(self.portrait, [entry[1] for entry in scene_sprites(self.game.get_current_room())])

    def test_sprite_removed_on_pickup_and_returned_on_drop(self):
        obj = self.game.get_current_room().objects['lanterna']
        self.session.execute('pegar lanterna')
        self.assertNotIn(obj, [entry[1] for entry in scene_sprites(self.game.get_current_room())])
        self.assertIs(self.game.item_objects['lanterna'], obj)
        self.session.execute('largar lanterna')
        self.assertIn(obj, [entry[1] for entry in scene_sprites(self.game.get_current_room())])

    def test_enemy_states_derive_from_combat(self):
        self.session.start_tutorial(4)
        enemy = self.session.game.rooms['test_end'].enemy
        self.assertEqual(enemy_state(enemy), 'idle')
        self.session.execute('ir norte')
        self.assertEqual(enemy_state(enemy), 'alert')
        self.session.execute('esperar')
        self.assertEqual(enemy_state(enemy), 'preparing')
        enemy.health = 0
        self.assertEqual(enemy_state(enemy), 'fallen')

    def test_player_help_and_item_descriptions_have_no_technical_terms(self):
        self.session.execute('pegar lanterna')
        texts = [help_text(self.game, topic) for topic in ('', 'inventário', 'comandos', 'confronto')]
        texts.append(item_details(self.game, 'lanterna')[0])
        for text in texts:
            self.assertNotRegex(text.lower(), r'parser|gamestate|debug|implementação|arquitetura|testes automatizados')

    def test_combat_read_preserves_reaction_but_not_document_body(self):
        self.session.start_tutorial(4)
        self.session.execute('ir norte')
        self.session.execute('esperar')
        self.session.game.get_current_room().objects['nota'] = GameObject('nota', '', text='Conteúdo reservado da nota.')
        self.session.execute('ler nota')
        self.assertIn('golpeia', self.session.history[-1][1])
        self.assertNotIn('Conteúdo reservado', self.session.history[-1][1])
        self.assertNotIn('golpeia', self.session.reading_text)


class VisualInvestigationTests(unittest.TestCase):
    setUp = ui.VisualCommandTests.setUp
    tearDown = ui.VisualCommandTests.tearDown
    enter = ui.VisualCommandTests.enter

    def test_document_full_text_only_in_reader(self):
        self.enter('ler carta antiga')
        text = self.app.session.reading_document.pages[0]
        self.assertIn(text, self.app.reader_text.get('1.0', 'end'))
        self.assertNotIn(text, self.app.history_view.get('1.0', 'end'))
        self.app.reader_panel.next.invoke()
        self.assertIn(self.app.session.reading_document.pages[1], self.app.reader_text.get('1.0', 'end'))

    def test_inspect_entry_turns_portrait_inside_same_frame(self):
        app = self.app
        app.start_tutorial(1)
        self.enter('examinar retrato')
        frame = app.reader_window
        entry = app.reader_panel.inspect_entry
        entry.insert(0, 'olhar atrás do retrato')
        entry.focus_force()
        app.root.update()
        entry.event_generate('<Return>')
        app.root.update()
        self.assertIs(app.reader_window, frame)
        self.assertIn('relógio', app.reader_text.get('1.0', 'end'))
        self.assertEqual(app.session.inspection_face, 'back')
        before = app.session.game.snapshot()
        self.enter('pegar lanterna')
        self.assertEqual(app.session.game.snapshot(), before)
        app.close_reader()
        app.root.update()
        self.assertIs(app.root.focus_get(), app.command_entry)

    def test_inventory_preview_and_document_command(self):
        self.enter('pegar carta antiga')
        self.enter('inventário')
        app = self.app
        entry = app.inventory_view.entry
        entry.insert(0, 'ler carta antiga')
        entry.event_generate('<Return>')
        app.root.update()
        self.assertIsNone(app.reader_window)
        self.assertEqual(app.session.selected_item, 'carta antiga')
        self.assertTrue(app.inventory_view.preview.find_withtag('sprite'))
        self.assertIn('Joseph, guarde', app.inventory_view.description.get('1.0', 'end'))
        self.assertNotIn('Joseph, guarde', app.history_view.get('1.0', 'end'))
        self.assertNotIn('Joseph, guarde', app.inventory_view.result.get())

    def test_png_transparency_nearest_scaling_and_missing_fallback(self):
        assets = self.app.assets
        image = assets.image('objects/key_front.png', 2)
        self.assertIsNotNone(image)
        self.assertEqual((image.width(), image.height()), (64, 80))
        self.assertTrue(image.transparency_get(0, 0))
        self.assertEqual(image.get(14, 8), image.get(15, 9))
        self.assertIsNone(assets.image('objects/not_present.png'))
        self.assertIsNone(assets.image('../visual.py'))
        with patch('tkinter.PhotoImage', side_effect=ui.tk.TclError('corrupt PNG')):
            self.assertIsNone(assets.image('objects/key_back.png', 3))
        obj = self.app.session.game.get_current_room().objects['lanterna']
        obj.sprite.images = {'front': 'objects/absent.png'}
        self.app.draw_scene()
        self.assertTrue(self.app.canvas.find_withtag('object:' + obj.object_id))

    def test_scene_png_pickup_and_enemy_change(self):
        app = self.app
        obj = app.session.game.get_current_room().objects['lanterna']
        self.assertTrue(app.canvas.find_withtag('object:' + obj.object_id))
        self.enter('pegar lanterna')
        self.assertFalse(app.canvas.find_withtag('object:' + obj.object_id))
        app.start_tutorial(4)
        self.enter('ir norte')
        self.assertTrue(app.canvas.find_withtag('state:alert'))
        self.enter('esperar')
        self.assertTrue(app.canvas.find_withtag('state:preparing'))

    def test_offline_resources_and_player_widgets(self):
        with patch('socket.socket', side_effect=AssertionError('network must not be used')):
            self.enter('pegar pistola')
            self.enter('inventário')
            self.app.inventory_view.select(0)
            self.app.root.update()
        for widget in ui.all_widgets(self.app.root):
            if widget.winfo_class() in ('Label', 'Button'):
                self.assertNotRegex(widget.cget('text').lower(), r'parser|gamestate|debug|implementação|arquitetura|testes automatizados')


if __name__ == '__main__':
    unittest.main()
