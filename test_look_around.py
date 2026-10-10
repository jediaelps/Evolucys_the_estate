import unittest

from command_parser import CommandParser
from game_state import GameState
from tutorial import TutorialState
from visual_session import VisualSession


class LookAroundTests(unittest.TestCase):
    def test_all_campaign_and_tutorial_rooms(self):
        games = [GameState()] + [TutorialState(number) for number in range(1, 5)]
        for game in games:
            parser = CommandParser(game)
            for room_id, room in game.rooms.items():
                with self.subTest(world=getattr(game, 'scenario', 'campaign'), room=room_id):
                    game.current_location = room_id
                    expected = room.describe()
                    response = parser.execute('  OLHAR   EM VOLTA  ')
                    self.assertTrue(response.startswith(expected))
                    self.assertNotIn(room.name, response.splitlines())
                    self.assertIn(room.description, response)
                    self.assertNotIn('Você percebe:', response)
                    self.assertNotIn('Saídas:', response)
                    if room.enemy:
                        self.assertIn(room.enemy.name, response.lower())

    def test_visible_contents_follow_reveal_pickup_and_drop(self):
        game = TutorialState(1)
        parser = CommandParser(game)
        self.assertNotIn('bilhete de teste', parser.execute('olhar em volta'))
        parser.execute('abrir caixa')
        self.assertIn('bilhete de teste', game.visible_objects())
        parser.execute('pegar bilhete')
        self.assertNotIn('bilhete de teste', game.visible_objects())
        parser.execute('largar bilhete')
        self.assertIn('bilhete de teste', game.visible_objects())

    def test_hidden_objects_are_not_revealed_by_looking(self):
        game = TutorialState(3)
        parser = CommandParser(game)
        response = parser.execute('olhar em volta')
        self.assertNotIn('anotação', response)
        self.assertNotIn('2468', response)
        self.assertNotIn('chave de teste', response)
        self.assertNotIn('anotação', game.get_current_room().objects)

    def test_visual_session_history_and_single_combat_reaction(self):
        session = VisualSession()
        session.start_tutorial(4)
        session.execute('ir norte')
        session.execute('esperar')
        before = session.game.turn_count
        response = session.execute('olhar em volta')
        self.assertIn(session.game.get_current_room().description, response)
        self.assertIn('golpeia', response)
        self.assertEqual(session.game.health, 84)
        self.assertEqual(session.game.turn_count, before + 1)
        self.assertEqual(session.history[-1], ('olhar em volta', response))


if __name__ == '__main__':
    unittest.main()
