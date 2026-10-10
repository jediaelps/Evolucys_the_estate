import unittest
import locks
from visual_session import VisualSession
from world import GameObject


class ActionNarrationTests(unittest.TestCase):
    def setUp(self):
        self.session = VisualSession(); self.session.start_tutorial(3)
        self.game = self.session.game
        self.room = self.game.get_current_room()
        self.session.execute('pegar chave de arquivo')
        self.key = self.game.item_objects['chave de arquivo']
        self.a, self.b = self.room.objects['armário a'], self.room.objects['armário b']

    def test_key_use_has_separate_speech_and_single_opening(self):
        self.session.execute('usar chave de arquivo no armário a')
        text = self.session.history[-1][1]
        self.assertIn('Joseph: “A chave encaixou perfeitamente... pronto.”\n', text)
        self.assertEqual(text.count('se abre.'), 1)
        self.assertNotIn('Joseph usa', text)
        self.assertNotIn('Joseph abriu', text)
        self.assertFalse(self.a.locked); self.assertTrue(self.a.opened)
        self.assertIn(self.key.name, self.game.inventory)

    def test_last_lock_consumes_key_and_reports_consequence(self):
        self.session.execute('abrir armário a')
        self.session.execute('usar chave de arquivo no armário b')
        text = self.session.history[-1][1]
        self.assertEqual(text.count('se abre.'), 1)
        self.assertIn('Joseph: “Não vou precisar mais dessa chave.”', text)
        self.assertNotIn(self.key.name, self.game.inventory)
        self.assertTrue(self.b.opened)

    def test_permanent_key_and_reopening_keep_state_and_no_false_unlock(self):
        self.key.permanent_key = True
        self.session.execute('abrir armário a'); self.session.execute('abrir armário b')
        self.assertIn(self.key.name, self.game.inventory)
        self.session.execute('fechar armário a')
        self.session.execute('abrir armário a')
        text = self.session.history[-1][1]
        self.assertEqual(text, 'Armário a se abre.')
        self.assertNotIn('encaixou', text)

    def test_unlock_alone_does_not_claim_opening(self):
        text = locks.unlock(self.game, self.key, self.a)
        self.assertFalse(self.a.locked); self.assertFalse(self.a.opened)
        self.assertIn('a abertura ainda precisa ser feita', text)
        self.assertNotIn('se abre', text)

    def test_tool_opening_and_revealed_contents_are_not_lost(self):
        tool = GameObject('pé de cabra', 'Ferro.', portable=True)
        drawer = GameObject('gaveta', 'Madeira.', locked=True, required_item=tool.name,
                            contents=[GameObject('bilhete novo', 'Uma anotação.', portable=True)])
        self.room.add_object(tool); self.room.add_object(drawer)
        self.session.execute('pegar pé de cabra')
        self.session.execute('usar pé de cabra na gaveta')
        text = self.session.history[-1][1]
        self.assertEqual(text.count('abre gaveta'), 1)
        self.assertNotIn('Joseph usa', text)
        self.assertNotIn('A ferramenta libera', text)
        self.assertIn('bilhete novo', text)
        self.assertIn('bilhete novo', self.room.objects)
        self.assertTrue(drawer.opened); self.assertFalse(drawer.locked)
        self.assertIn(tool.name, self.game.inventory)

    def test_pickup_equipment_and_code_have_one_result_each(self):
        tool = GameObject('lanterna extra', 'Uma lanterna.', portable=True)
        self.room.add_object(tool)
        self.session.execute('pegar lanterna extra')
        self.assertEqual(self.session.history[-1][1], 'Joseph pega lanterna extra.')
        self.session.execute('equipar lanterna extra')
        self.assertEqual(self.session.history[-1][1], 'Joseph segura lanterna extra.')
        self.assertEqual(self.game.equipped_item, tool.name)
        safe = GameObject('cofre extra', '', locked=True, code='1234')
        self.room.add_object(safe)
        self.session.execute('digitar 1234 no cofre extra')
        self.assertEqual(self.session.history[-1][1].count('se abre.'), 1)
        self.assertTrue(safe.opened); self.assertFalse(safe.locked)


if __name__ == '__main__': unittest.main()
