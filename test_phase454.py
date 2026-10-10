import json
import unittest
from unittest.mock import patch

from narrative import dialogue, history_text
from system_demo import create_system_demo
from confrontation import Enemy
from command_parser import CommandParser
from visual_session import VisualSession
import test_visual_commands as ui


class NarrativeTests(unittest.TestCase):
    def setUp(self):
        self.game = create_system_demo('light')
        self.enemy = Enemy('criatura', sound='passos')
        self.game.rooms['demo_hall'].enemies = [self.enemy]
        self.exploration = self.game.exploration
        self.parser = CommandParser(self.game)

    def test_identified_speakers_and_narrative_separation(self):
        text = 'Joseph entra no salão.\nPreciso manter a calma.\nDICA: Use ajuda.'
        rendered = history_text(text, self.game)
        self.assertEqual(rendered, 'Joseph entra no salão.\nJoseph: “Preciso manter a calma.”\nDICA: Use ajuda.')
        self.assertEqual(dialogue('Cientista', 'Quem está aí?'), 'Cientista: “Quem está aí?”')
        self.assertEqual(dialogue('Criatura', 'rosna', True), 'Criatura: *rosna*')
        self.assertEqual(history_text(dialogue('Zumbi', 'Grrr...'), self.game), 'Zumbi: “Grrr...”')
        self.game.get_current_room().description = 'Ouço o vento: palavras gravadas na parede.'
        self.assertEqual(history_text(self.game.get_current_room().description, self.game), self.game.get_current_room().description)

    def test_first_steps_return_and_silence(self):
        self.assertIn('Peraí', self.exploration.perception())
        self.assertEqual(self.exploration.perception(), '')
        self.exploration.enter('demo_foyer')
        record = self.exploration.memory.contexts['sound:demo_foyer']
        self.assertEqual(record['state'], 'known')
        self.exploration.memory.visit += 1
        self.assertEqual(self.exploration.perception(), '')

    def test_return_reaction_is_not_first_discovery(self):
        self.exploration.perception()
        response = self.exploration.enter('demo_foyer')
        self.assertIn('Ainda tô ouvindo', response)
        self.assertNotIn('Peraí', response)

    def test_real_movement_does_not_duplicate_discovery_in_same_turn(self):
        self.game.rooms['demo_hall'].enemies = []
        self.game.rooms['demo_end'].enemies = [self.enemy]
        first = self.parser.execute('ir norte')
        self.assertEqual(first.count('Peraí'), 1)
        self.parser.execute('ir sul')
        again = self.parser.execute('ir norte')
        self.assertNotIn('Peraí', again)
        self.assertEqual(again.count('Ainda tô ouvindo'), 1)
        self.parser.execute('ir sul')
        self.assertNotIn('Ainda tô ouvindo', self.parser.execute('ir norte'))

    def test_door_return_after_change_does_not_assert_old_presence(self):
        self.exploration.listen('porta')
        self.enemy.sound = None
        response = self.exploration.enter('demo_foyer')
        self.assertNotIn('Eu sei que', response)
        self.assertIn('não tô ouvindo mais nada', response)

    def test_confirmed_door_remembered_without_duplicate_event(self):
        response = self.parser.execute('ouvir atrás da porta')
        self.assertIn('do outro lado dessa porta', response)
        self.assertNotIn('Peraí', response)
        context = 'door:demo_foyer:demo_hall'
        self.assertEqual(self.exploration.memory.contexts[context]['state'], 'confirmed')
        returned = self.exploration.enter('demo_foyer')
        self.assertIn('Ainda ouço passos', returned)
        self.assertEqual(self.exploration.perception(), '')

    def test_world_changes_override_door_memory(self):
        for change in ('move', 'dead', 'silent'):
            with self.subTest(change=change):
                self.setUp()
                self.exploration.listen('porta')
                if change == 'move':
                    self.game.rooms['demo_hall'].enemies.remove(self.enemy)
                    self.game.rooms['demo_end'].enemies.append(self.enemy)
                elif change == 'dead':
                    self.enemy.health = 0
                else:
                    self.enemy.sound = None
                response = self.exploration.listen('porta')
                self.assertIn('não tô ouvindo mais nada', response)
                self.assertNotIn('Eu sei que', response)
                self.assertEqual(self.exploration.memory.contexts['door:demo_foyer:demo_hall']['state'], 'altered')

    def test_replacement_and_new_context_are_distinct_events(self):
        self.exploration.perception()
        self.game.rooms['demo_hall'].enemies = [Enemy('outra', sound='passos')]
        self.assertIn('mudou', self.exploration.perception())
        self.game.current_location = 'demo_end'
        self.assertIn('Peraí', self.exploration.perception())

    def test_sight_and_defeat_update_memory(self):
        self.game.rooms['demo_hall'].dark = False
        self.game.current_location = 'demo_hall'
        self.exploration.enter('demo_foyer')
        self.assertEqual(self.exploration.memory.contexts['sight:demo_hall']['state'], 'confirmed')
        self.enemy.health = 0
        self.exploration.advance()
        self.assertEqual(self.exploration.memory.contexts['sight:demo_hall']['state'], 'altered')

    def test_memory_roundtrip_and_old_state(self):
        self.exploration.listen('porta')
        state = json.loads(json.dumps(self.exploration.export_state()))
        self.exploration.memory.contexts.clear()
        self.exploration.restore_state(state)
        self.assertNotIn('Peraí', self.exploration.perception())
        self.assertEqual(self.exploration.export_state(), state)
        del state['threat_memory']
        self.exploration.restore_state(state)
        self.assertFalse(self.exploration.memory.contexts)

    def test_no_automatic_object_lists_or_inventory_narration(self):
        self.assertNotIn('Você percebe:', self.game.get_current_room().describe(self.game))
        self.assertNotIn('bandagem', self.game.get_current_room().describe(self.game))
        self.parser.execute('pegar bandagem')
        self.assertNotIn('Joseph está carregando', self.parser.execute('inventário'))
        session = VisualSession(); session._attach(self.game, 'tutorial')
        session.execute('inventário')
        self.assertEqual(session.history[-1][1], 'Inventário aberto.')

    def test_session_formats_speech_without_changing_parser_result(self):
        session = VisualSession(); session._attach(self.game, 'tutorial')
        result = session.execute('usar bandagem')
        self.assertTrue(session.history[-1][1].startswith('Joseph: “'))
        self.assertFalse(result.startswith('Joseph:'))
        with patch.object(session.parser, 'execute', return_value=dialogue('Criatura', 'rosna', True)):
            session.execute('evento')
        self.assertEqual(session.history[-1][1], 'Criatura: *rosna*')


class NarrativeInterfaceTests(unittest.TestCase):
    setUp = ui.VisualCommandTests.setUp
    tearDown = ui.VisualCommandTests.tearDown
    enter = ui.VisualCommandTests.enter

    def test_history_order_bottom_anchor_dialogue_and_hints(self):
        self.app.root.geometry('1100x760'); self.app.root.update()
        self.enter('usar bandagem')
        self.enter('usar energético')
        view = self.app.history_view
        text = view.get('1.0', 'end-1c')
        self.assertLess(text.index('> usar bandagem'), text.index('> usar energético'))
        self.assertIn('Joseph: “Melhor eu pegar', text)
        self.assertNotIn('DICA:', text)
        self.assertNotIn('Joseph: “DICA:', text)
        last = view.dlineinfo('end-1c')
        self.assertLessEqual(abs(view.winfo_height()-last[1]-last[3]), 5)
        self.assertIn('4.5.5', self.app.root.title())


if __name__ == '__main__':
    unittest.main()
