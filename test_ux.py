import unittest
from command_parser import CommandParser
from game_state import GameState
from tutorial import TutorialState
from world import GameObject
from hud_state import indicators


class ContextUXTests(unittest.TestCase):
    def setUp(self):
        self.game = TutorialState(1)
        self.parser = CommandParser(self.game)

    def test_read_aliases_before_and_after_pickup(self):
        self.parser.execute('abrir a caixa')
        expected = self.game.get_current_room().objects['bilhete de teste'].text
        for command in ('ler bilhete', 'ler o bilhete', 'ler um bilhete de teste'):
            self.assertEqual(self.parser.execute(command), expected)
        self.parser.execute('pegar o bilhete')
        self.assertEqual(self.parser.execute('ler bilhete'), expected)
        self.assertIn('Há algo escrito', self.parser.execute('examinar o bilhete'))

    def test_read_non_text_missing_and_inaccessible_differ(self):
        self.assertIn('Não há texto', self.parser.execute('ler lanterna'))
        self.assertIn('Não vejo', self.parser.execute('ler carta'))
        self.game.get_current_room().add_object(GameObject('placa', 'Uma placa alta.', text='Texto da placa', accessible=False))
        for command in ('ler placa', 'examinar placa', 'pegar placa'):
            self.assertIn('não alcanço', self.parser.execute(command))

    def test_document_text_is_generic_metadata(self):
        for name in ('carta', 'diário', 'relatório', 'fotografia com texto'):
            self.game.get_current_room().add_object(GameObject(name, 'Descrição física.', text='Conteúdo próprio.'))
            self.assertEqual(self.parser.execute(f'ler {name}'), 'Conteúdo próprio.')

    def test_articles_on_actions(self):
        self.parser.execute('pegar uma lanterna')
        self.parser.execute('equipar a lanterna')
        self.assertEqual(self.game.equipped_item, 'lanterna')
        self.assertIn('mesa', self.parser.execute('olhar a mesa'))

    def test_closed_door_cause_and_open_passage(self):
        for command in ('passar porta', 'passar pela porta', 'entrar pela porta', 'ir norte'):
            self.assertIn('fechada', self.parser.execute(command))
        self.parser.execute('abrir uma porta')
        self.parser.execute('atravessar porta')
        self.assertEqual(self.game.current_location, 'test_end')
        self.parser.execute('passar pela porta de teste')
        self.assertEqual(self.game.current_location, 'test_start')

    def test_locked_door_and_item_condition(self):
        door = self.game.get_current_room().objects['porta de teste']
        door.locked = True
        door.required_item = 'chave'
        self.assertIn('trancada', self.parser.execute('passar pela porta'))
        self.assertIn('trancada', self.parser.execute('abrir porta'))
        self.game.get_current_room().add_object(GameObject('chave', 'Uma chave.', portable=True))
        self.parser.execute('pegar a chave')
        self.parser.execute('usar a chave em uma porta')
        self.parser.execute('entrar pela porta')
        self.assertEqual(self.game.current_location, 'test_end')

    def test_blocked_door_cannot_be_bypassed_with_key_or_code(self):
        door = self.game.get_current_room().objects['porta de teste']
        door.blocked = True
        door.required_item = 'chave'
        self.game.add_item('chave')
        for command in ('abrir porta', 'usar chave na porta', 'atravessar porta'):
            self.assertIn('bloqueando', self.parser.execute(command))
        door.code = '12'
        self.assertIn('bloqueando', self.parser.execute('digitar 12 na porta'))
        self.assertFalse(door.opened)
        door.blocked = False
        self.parser.execute('digitar 12 na porta')
        self.parser.execute('passar porta')
        self.assertEqual(self.game.current_location, 'test_end')

    def test_no_path_is_not_unknown_command(self):
        origin, turns = self.game.current_location, self.game.turn_count
        response = self.parser.execute('ir oeste')
        self.assertTrue(response.startswith('Joseph:'))
        self.assertIn('Não há uma passagem direta para lá daqui.', response)
        self.assertEqual(self.game.current_location, origin)
        self.assertEqual(self.game.turn_count, turns + 1)
        self.assertEqual('Não foi possível entender essa ação.', self.parser.execute('teletransportar'))
        self.assertEqual(self.game.current_location, origin)
        self.assertEqual(self.game.turn_count, turns + 1)

    def test_help_context_does_not_expose_contents_or_codes(self):
        help_before = self.parser.execute('ajuda')
        self.assertTrue(help_before.startswith('Joseph: “'))
        self.assertLess(len(help_before), 250)
        self.assertNotIn('bilhete', help_before)
        self.parser.execute('abrir caixa')
        self.assertIn('LER bilhete de teste', self.parser.execute('ajuda'))
        self.game = TutorialState(3)
        self.parser = CommandParser(self.game)
        for command in ('ajuda', 'ajuda cofre', 'ajuda porta', 'ajuda chave'):
            text = self.parser.execute(command)
            self.assertNotIn('2468', text)
            self.assertNotIn('chave de teste', text)
            self.assertNotIn('anotação', text)

    def test_help_knows_lock_only_after_observation(self):
        door = self.game.get_current_room().objects['porta de teste']
        door.locked = True
        self.assertNotIn('trancada', self.parser.execute('ajuda porta'))
        self.parser.execute('examinar porta')
        self.assertIn('Já percebi que está trancada', self.parser.execute('ajuda porta'))
        door.locked = False
        self.parser.execute('abrir porta')
        self.assertNotIn('trancada', self.parser.execute('ajuda porta'))

    def test_help_topics_are_free_and_reference_organized(self):
        for topic in ('comandos', 'inventário', 'combate', 'celular', 'porta'):
            self.assertTrue(self.parser.execute('ajuda ' + topic))
        self.assertEqual(self.game.turn_count, 0)
        text = self.parser.execute('ajuda comandos')
        for heading in ('EXPLORAÇÃO', 'OBJETOS', 'EQUIPAMENTO', 'SOBREVIVÊNCIA', 'CONFRONTO', 'INFORMAÇÕES'):
            self.assertIn(heading, text)

    def test_help_considers_health_fear_inventory_equipment(self):
        self.game.health = 40
        self.game.fear = 70
        self.game.add_item('bandagem')
        self.game.add_item('chá')
        self.game.equip_item('chá')
        text = self.parser.execute('ajuda')
        for phrase in ('ferido', 'INVENTÁRIO'):
            self.assertIn(phrase, text)
        self.game.health = self.game.max_health
        self.assertIn('chá', self.parser.execute('ajuda'))

    def test_ambiguous_names_require_disambiguation(self):
        self.game.get_current_room().add_object(GameObject('porta lateral', 'Outra porta.'))
        self.assertIn('mais específico', self.parser.execute('abrir porta'))
        self.assertFalse(self.game.get_current_room().objects['porta de teste'].opened)

    def test_inventory_aliases_and_close_are_free(self):
        for command, expected in [('inventário', 'inventory'), ('abrir o inventário', 'inventory'),
                                  ('fechar inventário', 'close_inventory')]:
            self.parser.execute(command)
            self.assertEqual(self.parser.presentation, expected)
        self.assertEqual(self.game.turn_count, 0)

    def test_complete_exploration_flow_and_reset(self):
        commands = ['olhar', 'examinar a mesa', 'pegar lanterna', 'examinar caixa',
                    'abrir caixa', 'ler o bilhete', 'passar pela porta', 'examinar porta',
                    'abrir porta', 'passar pela porta', 'entrar pela porta']
        for command in commands:
            self.parser.execute(command)
        self.assertEqual(self.game.current_location, 'test_start')
        self.assertIn('lanterna', self.game.inventory)
        fresh = TutorialState(1)
        self.assertFalse(fresh.get_current_room().objects['porta de teste'].opened)
        self.assertNotIn('bilhete de teste', fresh.get_current_room().objects)

    def test_reading_in_confrontation_reacts_help_does_not(self):
        game = TutorialState(4)
        parser = CommandParser(game)
        parser.execute('ir norte')
        enemy = game.get_current_room().enemy
        enemy.preparing = True
        game.get_current_room().add_object(GameObject('carta', 'Papel.', text='Conteúdo.'))
        parser.execute('ajuda combate')
        self.assertEqual(game.health, 100)
        self.assertIn('golpeia', parser.execute('ler carta'))
        self.assertEqual(game.health, 84)

    def test_hud_projection_encodes_damage_and_phone(self):
        game = GameState()
        game.health = 20
        game.phone_vibrating = True
        view = indicators(game.snapshot(), previous_health=100)
        self.assertTrue(view['heart']['critical'])
        self.assertTrue(view['heart']['damaged'])
        self.assertTrue(view['phone']['vibrating'])
        self.assertFalse(view['phone']['save_available'])


if __name__ == '__main__':
    unittest.main()
