import unittest

from game_state import GameState
from tutorial import TutorialState
from visual_session import VisualSession


class VisualSessionTests(unittest.TestCase):
    def setUp(self):
        self.session = VisualSession()

    def select(self, name, action):
        self.session.selected_object = name
        return self.session.object_action(action)

    def inventory(self, name, action):
        self.session.selected_item = name
        return self.session.inventory_action(action)

    def test_continue_disabled_without_valid_save(self):
        self.assertFalse(self.session.can_continue)
        self.session.start_campaign()
        self.assertFalse(self.session.can_continue)  # Uma sessão em RAM não é um save.

    def test_tutorial_cannot_change_campaign(self):
        self.session.start_campaign()
        campaign = self.session.game
        campaign.current_location = 'T01'
        self.session.execute('pegar lanterna')
        before = campaign.snapshot()
        self.session.start_tutorial(2)
        self.session.debug('dano')
        self.session.debug('medo+')
        self.select('pistola', 'pegar')
        self.session.leave()
        self.assertIs(self.session.campaign, campaign)
        self.assertEqual(campaign.snapshot(), before)
        self.assertIn('lanterna', campaign.inventory)
        self.assertIsNone(self.session.game)

    def test_campaign_has_no_debug_controls_or_death_protection(self):
        self.session.start_campaign()
        before = self.session.game.snapshot()
        self.session.debug('curar')
        self.session.debug('munição')
        self.assertEqual(self.session.game.snapshot(), before)
        self.assertFalse(hasattr(self.session.game, 'debug'))
        self.session.game.damage(1000)
        self.assertTrue(self.session.game.game_over)
        self.assertFalse(self.session.reset())

    def test_four_worlds_have_no_campaign_rooms(self):
        for number in range(1, 5):
            with self.subTest(number=number):
                self.session.start_tutorial(number)
                self.assertEqual(set(self.session.game.rooms), {'test_start', 'test_end'})
                self.assertNotIn('entrance', self.session.game.rooms)
        with self.assertRaises(ValueError):
            TutorialState(5)

    def test_reset_restores_initial_state(self):
        self.session.start_tutorial(4)
        old_game = self.session.game
        self.select('pistola', 'pegar')
        self.session.debug('medo+')
        self.session.execute('ir norte')
        self.session.execute('atacar')
        self.assertTrue(self.session.reset())
        self.assertIsNot(self.session.game, old_game)
        self.assertEqual(self.session.game.health, 100)
        self.assertEqual(self.session.game.fear, 0)
        self.assertEqual(self.session.game.turn_count, 0)
        self.assertEqual(self.session.game.inventory, [])
        self.assertFalse(self.session.game.rooms['test_end'].enemy.alert)
        self.assertEqual(self.session.game.rooms['test_end'].enemy.health, 120)

    def test_scenario_switch_does_not_keep_items(self):
        self.session.start_tutorial(2)
        self.select('pistola', 'pegar')
        self.session.start_tutorial(1)
        self.assertNotIn('pistola', self.session.game.inventory)
        self.assertNotIn('pistola', self.session.game.get_current_room().objects)

    def test_exploration_container_and_nonportable(self):
        self.session.start_tutorial(1)
        self.select('mesa de teste', 'pegar')
        self.assertNotIn('mesa de teste', self.session.game.inventory)
        self.select('caixa', 'abrir')
        self.assertIn('bilhete de teste', self.session.game.get_current_room().objects)
        self.session.execute('ir norte')
        self.assertEqual(self.session.game.current_location, 'test_start')
        self.select('porta de teste', 'abrir')
        self.session.execute('ir norte')
        self.assertEqual(self.session.game.current_location, 'test_end')

    def test_six_slots_and_full_inventory(self):
        self.session.start_tutorial(2)
        self.assertEqual(self.session.slots(), [None] * 6)
        for name in ['lanterna', 'bandagem', 'spray de cura', 'kit médico', 'chá', 'energético']:
            self.select(name, 'pegar')
        self.assertEqual(len(self.session.slots()), 6)
        self.assertNotIn(None, self.session.slots())
        self.assertIn('cheios', self.select('pistola', 'pegar'))
        self.assertIn('pistola', self.session.game.get_current_room().objects)

    def test_visual_inventory_use_equip_drop(self):
        self.session.start_tutorial(2)
        self.select('bandagem', 'pegar')
        self.inventory('bandagem', 'equipar')
        self.session.debug('dano')
        self.session.execute('inventário')
        self.inventory('bandagem', 'usar')
        self.assertEqual(self.session.game.health, 95)
        self.assertIsNone(self.session.game.equipped_item)
        self.assertIsNone(self.session.selected_item)
        self.session.debug('recursos')
        self.select('bandagem', 'pegar')
        self.inventory('bandagem', 'largar')
        self.assertNotIn('bandagem', self.session.game.inventory)

    def test_debug_changes_fear_health_without_turn(self):
        self.session.start_tutorial(2)
        self.session.debug('dano')
        self.session.debug('medo+')
        self.assertEqual(self.session.game.health, 75)
        self.assertEqual(self.session.game.fear, 25)
        self.session.debug('curar')
        self.session.debug('medo-')
        self.assertEqual(self.session.game.health, 100)
        self.assertEqual(self.session.game.fear, 0)
        self.assertEqual(self.session.game.turn_count, 0)

    def test_tutorial_gun_empty_reload_and_ammo_refill(self):
        self.session.start_tutorial(2)
        self.select('pistola', 'pegar')
        self.select('munição de pistola', 'pegar')
        self.inventory('pistola', 'equipar')
        self.session.debug('esvaziar')
        self.assertEqual(self.session.game.item_objects['pistola'].weapon.ammo, 0)
        self.session.execute('recarregar')
        self.assertEqual(self.session.game.item_objects['pistola'].weapon.ammo, 12)
        self.assertNotIn('munição de pistola', self.session.game.inventory)
        self.session.debug('munição')
        self.session.execute('pegar munição de pistola')
        self.assertEqual(self.session.game.item_objects['munição de pistola'].ammo_count, 12)

    def test_puzzle_visual_actions(self):
        self.session.start_tutorial(3)
        self.select('porta de teste', 'abrir')
        self.session.execute('ir norte')
        self.assertEqual(self.session.game.current_location, 'test_start')
        self.assertNotIn('anotação', self.session.game.get_current_room().objects)
        self.select('quadro de teste', 'examinar')
        self.assertIn('2468', self.select('anotação', 'examinar'))
        self.session.selected_object = 'cofre de teste'
        self.session.object_action('código', '0000')
        self.assertNotIn('chave de teste', self.session.game.get_current_room().objects)
        self.session.object_action('código', '2468')
        self.select('chave de teste', 'pegar')
        self.inventory('chave de teste', 'equipar')
        self.select('porta de teste', 'usar equipado')
        self.session.execute('ir norte')
        self.assertEqual(self.session.game.current_location, 'test_end')
        self.assertIn('concluído', self.select('registro', 'examinar'))

    def test_tutorial_combat_safety_on_enemy_hit(self):
        self.session.start_tutorial(4)
        self.session.execute('ir norte')
        self.session.execute('esperar')
        self.session.game.health = 1
        response = self.session.execute('esperar')
        self.assertIn('MODO DE TESTE: morte impedida', response)
        self.assertFalse(self.session.game.game_over)
        self.assertEqual(self.session.game.health, 25)
        self.session.parser.confrontation.roll = lambda: 0.0
        self.session.execute('fugir sul')
        self.assertEqual(self.session.game.current_location, 'test_start')

    def test_safety_only_in_confrontation_scenario(self):
        for number in (1, 2, 3):
            game = TutorialState(number)
            game.damage(1000)
            self.assertTrue(game.game_over)
        game = TutorialState(4)
        game.damage(1000)
        self.assertFalse(game.game_over)

    def test_switching_equipment_in_visual_session_allows_reaction(self):
        self.session.start_tutorial(4)
        self.select('pistola', 'pegar')
        self.select('lanterna', 'pegar')
        self.session.execute('ir norte')
        self.session.execute('esperar')
        before = self.session.game.turn_count
        self.inventory('pistola', 'equipar')
        self.assertEqual(self.session.game.health, 84)
        self.assertEqual(self.session.game.turn_count, before + 1)

    def test_free_selection_and_queries_keep_enemy_waiting(self):
        self.session.start_tutorial(4)
        self.session.execute('ir norte')
        self.session.execute('esperar')
        before = self.session.game.snapshot()
        self.session.selected_object = 'vigia'
        self.session.slots()
        self.session.execute('status')
        self.session.execute('ajuda')
        self.assertEqual(self.session.game.snapshot(), before)

    def test_resource_refill_does_not_overwrite_carried_weapon(self):
        self.session.start_tutorial(4)
        self.select('pistola', 'pegar')
        self.inventory('pistola', 'equipar')
        self.session.debug('esvaziar')
        self.session.debug('recursos')
        self.assertEqual(self.session.game.item_objects['pistola'].weapon.ammo, 0)
        self.assertNotIn('pistola', self.session.game.rooms['test_start'].objects)

    def test_tutorial_can_avoid_combat(self):
        self.session.start_tutorial(4)
        self.session.execute('esgueirar norte')
        self.session.execute('examinar vigia')
        self.session.execute('esgueirar sul')
        self.assertEqual(self.session.game.health, 100)
        self.assertFalse(self.session.game.rooms['test_end'].enemy.alert)


if __name__ == '__main__':
    unittest.main()

