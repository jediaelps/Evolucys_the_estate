import unittest
from command_parser import CommandParser
from world import GameObject
from test_phase455 import passage_game
import test_visual_commands as ui


class ContextHelpCleanupTests(unittest.TestCase):
    def test_help_combines_known_object_and_real_open_direction(self):
        game = passage_game()
        game.get_current_room().add_object(GameObject('mesa', 'Uma mesa antiga.'))
        text = CommandParser(game).execute('ajuda')
        self.assertIn('Joseph:', text)
        self.assertIn('EXAMINAR mesa', text)
        self.assertIn('NORTE', text)
        self.assertNotIn('DICA:', text)
        self.assertLess(len(text), 250)

    def test_unavailable_routes_are_not_offered_as_free_paths(self):
        for state in ('blocked', 'locked', 'closed', 'hidden', 'inaccessible'):
            with self.subTest(state=state):
                game = passage_game(); room = game.get_current_room()
                door = room.exit_doors['norte']
                if state == 'closed': door.opened = False
                elif state == 'hidden': door.requires_uv = True
                elif state == 'inaccessible': door.accessible = False
                else: setattr(door, state, True)
                room.add_object(GameObject('mesa', 'Uma mesa antiga.'))
                text = CommandParser(game).execute('ajuda')
                self.assertNotIn('NORTE', text)
                self.assertNotIn('seguir', text)

    def test_known_blockage_is_contextual_and_free(self):
        game = passage_game(); parser = CommandParser(game)
        door = game.get_current_room().exit_doors['norte']
        door.blocked = True
        parser.execute('examinar porta do porão')
        before = game.turn_count
        text = parser.execute('ajuda porta do porão')
        self.assertIn('bloqueada', text)
        self.assertIn('EXAMINAR', text)
        self.assertEqual(game.turn_count, before)


class CleanHistoryTests(unittest.TestCase):
    setUp = ui.VisualCommandTests.setUp
    tearDown = ui.VisualCommandTests.tearDown
    enter = ui.VisualCommandTests.enter

    def test_normal_actions_and_errors_never_append_automatic_tips(self):
        self.app.start_tutorial(1); self.app.root.update()
        self.assertNotIn('DICA:', self.app.history_view.get('1.0','end'))
        for command in ('examinar mesa', 'pegar lanterna', 'inventário', 'fechar inventário',
                        'abrir porta', 'ir norte', 'ir sul', 'xyz impossível', 'ajuda'):
            self.enter(command)
            if command == 'examinar mesa':
                self.app.reader_panel.back.invoke()
            self.assertNotIn('DICA:', self.app.history_view.get('1.0','end'))
        self.assertIn('Joseph:', self.app.history_view.get('1.0','end'))

    def test_incomplete_command_is_only_a_question(self):
        self.app.session._attach(passage_game(True), 'campaign'); self.app.build_game()
        self.enter('passar pela porta')
        text = self.app.history_view.get('1.0','end')
        self.assertIn('Joseph: “Qual', text)
        self.assertNotIn('DICA:', text)
        self.assertEqual(self.app.session.game.turn_count, 0)
        self.enter('a do porão')
        self.assertEqual(self.app.session.game.current_location, 'cellar')

    def test_requested_help_highlight_reference_and_bottom_anchor(self):
        game = passage_game(); game.get_current_room().add_object(GameObject('mesa', 'Madeira.'))
        self.app.session._attach(game, 'campaign'); self.app.build_game(); self.app.root.update()
        self.enter('me ajuda')
        view = self.app.history_view
        ranges = view.tag_ranges('action_verb')
        self.assertEqual([view.get(a,b) for a,b in zip(ranges[::2], ranges[1::2])], ['EXAMINAR','NORTE'])
        self.assertIsNone(self.app.reader_window)
        self.assertNotIn('DICA:', view.get('1.0','end'))
        line = view.dlineinfo('end-1c')
        self.assertLessEqual(abs(view.winfo_height()-line[1]-line[3]), 5)
        self.enter('ajuda comandos')
        self.assertIsNotNone(self.app.reader_window)
        self.assertIn('EXPLORAÇÃO', self.app.reader_text.get('1.0','end'))


if __name__ == '__main__': unittest.main()
