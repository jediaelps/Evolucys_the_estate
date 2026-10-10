import unittest

from command_parser import CommandParser
from game_state import GameState


class ConfrontationTests(unittest.TestCase):
    def setUp(self):
        self.game = GameState(configuration='prototype')
        self.parser = CommandParser(self.game)
        self.game.current_location = 'main_hall'
        self.game.rooms['main_hall'].objects['porta do porão'].opened = True
        self.game.rooms['main_hall'].objects['porta do porão'].locked = False
        self.enemy = self.game.rooms['cellar'].enemy

    def equip_from(self, room, name):
        obj = self.game.rooms[room].objects.pop(name)
        self.game.add_item(name)
        self.game.item_objects[name] = obj
        self.game.equip_item(name)

    def test_entry_telegraph_and_one_reaction_per_action(self):
        self.parser.execute('ir norte')
        self.assertTrue(self.enemy.alert)
        self.assertEqual(self.game.health, 100)
        self.parser.execute('examinar pasta de joseph')
        self.assertTrue(self.enemy.preparing)
        self.assertEqual(self.game.health, 100)
        self.parser.execute('olhar')
        self.assertEqual(self.game.health, 84)
        self.assertEqual(self.game.turn_count, 3)
        self.assertFalse(self.enemy.preparing)

    def test_entire_existing_puzzle_without_combat(self):
        self.game = GameState(configuration='prototype')
        self.parser = CommandParser(self.game)
        for command in ['ir norte', 'examinar retrato', 'examinar inscrição',
                        'ir oeste', 'pegar pé de cabra', 'ir leste', 'abrir gaveta',
                        'pegar chave do armário', 'ir leste', 'abrir armário',
                        'examinar bilhete', 'digitar 0417 no cofre', 'pegar chave do porão',
                        'ir oeste', 'abrir porta do porão', 'esgueirar norte',
                        'examinar pasta de joseph', 'esgueirar sul']:
            self.parser.execute(command)
        self.assertEqual(self.game.current_location, 'main_hall')
        self.assertEqual(self.game.health, 100)
        self.assertFalse(self.game.rooms['cellar'].enemy.alert)
        self.assertEqual(self.game.rooms['cellar'].enemy.health, 60)

    def test_flee_and_normal_movement_avoid_pending_attack(self):
        self.parser.confrontation.roll = lambda: 0.0
        for command in ('fugir sul', 'ir sul', 'esgueirar sul'):
            with self.subTest(command=command):
                self.game.current_location = 'cellar'
                self.enemy.alert = True
                self.enemy.preparing = True
                self.parser.execute(command)
                self.assertEqual(self.game.current_location, 'main_hall')
                self.assertEqual(self.game.health, 100)
                self.assertFalse(self.enemy.preparing)
        self.parser.execute('esperar')
        self.assertEqual(self.game.health, 100)

    def test_failed_escape_still_allows_reaction(self):
        self.parser.execute('ir norte')
        self.enemy.preparing = True
        self.game.get_current_room().objects['porta do porão'].opened = False
        self.parser.execute('fugir sul')
        self.assertEqual(self.game.current_location, 'cellar')
        self.assertEqual(self.game.health, 84)
        self.enemy.preparing = True
        self.parser.execute('fugir oeste')
        self.assertEqual(self.game.health, 68)

    def test_defense_is_consumed_by_first_attack(self):
        self.parser.confrontation.roll = lambda: 1.0
        self.parser.execute('ir norte')
        self.enemy.preparing = True
        self.parser.execute('defender')
        self.assertEqual(self.game.health, 86)
        self.parser.execute('esperar')
        self.parser.execute('esperar')
        self.assertEqual(self.game.health, 70)

    def test_weapon_and_defeat_persist_without_final_retaliation(self):
        self.equip_from('kitchen', 'pé de cabra')
        self.parser.execute('ir norte')
        self.parser.execute('atacar vigia')
        self.assertEqual(self.enemy.health, 35)
        self.parser.execute('atacar')
        self.assertEqual(self.enemy.health, 10)
        health = self.game.health
        self.enemy.preparing = True
        self.parser.execute('atacar')
        self.assertEqual(self.enemy.health, 0)
        self.assertEqual(self.game.health, health)
        for command in ('ir sul', 'ir norte', 'esperar', 'atacar'):
            self.parser.execute(command)
        self.assertEqual(self.game.health, health)
        self.assertTrue(GameState(configuration='prototype').rooms['cellar'].enemy.alive)

    def test_unarmed_attack_and_wrong_target(self):
        self.parser.execute('ir norte')
        self.parser.execute('atacar')
        self.assertEqual(self.enemy.health, 50)
        self.parser.execute('atacar fantasma')
        self.assertEqual(self.enemy.health, 50)
        self.assertEqual(self.game.health, 84)

    def test_flash_interrupts_once_and_requires_equipment(self):
        self.equip_from('entrance', 'lanterna')
        self.parser.execute('ir norte')
        self.enemy.preparing = True
        self.parser.execute('distrair vigia')
        self.assertEqual(self.game.health, 100)
        self.assertFalse(self.enemy.preparing)
        self.enemy.preparing = True
        self.parser.execute('distrair')
        self.assertEqual(self.game.health, 84)
        self.enemy.flash_used = False
        self.game.equipped_item = None
        self.enemy.preparing = True
        self.parser.execute('distrair')
        self.assertFalse(self.enemy.flash_used)
        self.assertEqual(self.game.health, 68)

    def test_tea_is_consumed_before_enemy_reacts(self):
        self.equip_from('kitchen', 'chá')
        self.parser.execute('ir norte')
        self.game.fear = 50
        self.enemy.preparing = True
        self.parser.execute('inventário')
        self.parser.execute('usar chá')
        self.assertEqual(self.game.fear, 25)  # -30 do chá, +5 do golpe.
        self.assertEqual(self.game.health, 84)
        self.assertIsNone(self.game.equipped_item)
        self.assertNotIn('chá', self.game.inventory)

    def test_free_queries_and_unknown_commands_do_not_advance(self):
        self.parser.execute('ir norte')
        self.enemy.preparing = True
        for command in ('ajuda', 'status', 'inventário', '', 'xyz'):
            self.parser.execute(command)
        self.assertEqual(self.game.turn_count, 1)
        self.assertEqual(self.game.health, 100)
        self.parser.execute('pegar item inexistente')
        self.assertEqual(self.game.turn_count, 2)
        self.assertEqual(self.game.health, 84)

    def test_noisy_action_breaks_stealth_and_cannot_hide_when_seen(self):
        self.parser.execute('esgueirar norte')
        self.parser.execute('esconder')
        self.assertFalse(self.enemy.alert)
        self.parser.execute('pegar item inexistente')
        self.assertTrue(self.enemy.alert)
        self.assertFalse(self.game.hidden)
        self.parser.execute('esconder')
        self.assertFalse(self.game.hidden)
        self.assertTrue(self.enemy.preparing)

    def test_death_blocks_further_actions(self):
        self.parser.execute('ir norte')
        self.game.health = 1
        self.enemy.preparing = True
        self.parser.execute('esperar')
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.health, 0)
        turns = self.game.turn_count
        self.parser.execute('fugir sul')
        self.parser.execute('atacar')
        self.assertEqual(self.game.current_location, 'cellar')
        self.assertEqual(self.enemy.health, 60)
        self.assertEqual(self.game.turn_count, turns)


if __name__ == '__main__':
    unittest.main()
