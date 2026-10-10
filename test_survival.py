import unittest

from command_parser import CommandParser
from game_state import GameState
from items import HEALING, WeaponState, fear_profile
from world import GameObject


class SurvivalTests(unittest.TestCase):
    def setUp(self):
        self.game = GameState(configuration='prototype')
        self.parser = CommandParser(self.game)
        # 4.5.2: estes testes exercitam uso pessoal dentro do inventário.
        self.parser.execute('inventário')

    def give(self, name, **kwargs):
        obj = GameObject(name, 'Recurso de teste.', portable=True, **kwargs)
        self.assertTrue(self.game.add_item(name))
        self.game.item_objects[name] = obj
        return obj

    def encounter(self):
        self.game.current_location = 'cellar'
        enemy = self.game.get_current_room().enemy
        enemy.alert = True
        enemy.preparing = True
        return enemy

    def test_each_healing_item_outside_combat(self):
        for name, amount in HEALING.items():
            with self.subTest(item=name):
                self.game.health = 5
                self.give(name)
                self.game.equip_item(name)
                self.parser.execute(f'usar {name}')
                self.assertEqual(self.game.health, min(100, 5 + amount))
                self.assertNotIn(name, self.game.inventory)
                self.assertIsNone(self.game.equipped_item)
        self.assertEqual(self.game.turn_count, 3)

    def test_healing_cap_and_full_health_does_not_consume(self):
        for name in HEALING:
            with self.subTest(item=name):
                self.game.health = 100
                self.give(name)
                self.assertIn('Não preciso disso agora', self.parser.execute(f'usar {name}'))
                self.assertIn(name, self.game.inventory)
                self.game.health = 99
                self.parser.execute(f'usar {name}')
                self.assertEqual(self.game.health, 100)

    def test_consumables_resolve_before_exactly_one_enemy_reaction(self):
        for name, healed in [('bandagem', 20), ('spray de cura', 50), ('kit médico', 100),
                             ('chá', 0), ('energético', 0)]:
            with self.subTest(item=name):
                self.setUp()
                enemy = self.encounter()
                self.game.health = 40
                self.give(name)
                self.parser.execute(f'usar {name}')
                damage = 16  # Foco não reduz dano.
                self.assertEqual(self.game.health, min(100, 40 + healed) - damage)
                self.assertFalse(enemy.preparing)
                self.assertEqual(self.game.turn_count, 1)
                self.assertNotIn(name, self.game.inventory)

    def test_full_health_attempt_in_combat_costs_action_but_preserves_item(self):
        self.encounter()
        self.give('bandagem')
        self.parser.execute('usar bandagem')
        self.assertEqual(self.game.health, 84)
        self.assertIn('bandagem', self.game.inventory)

    def test_tea_floor_without_enemy_reaction(self):
        self.game.fear = 10
        self.give('chá')
        self.parser.execute('tomar chá')
        self.assertEqual(self.game.fear, 0)
        self.assertEqual(self.game.health, 100)

    def test_energy_focus_persists_across_actions_without_damage_bonus(self):
        self.give('energético')
        self.parser.execute('usar energético')
        self.assertEqual(self.game.focus_charges, 2)
        self.assertEqual(self.game.incoming_damage(16), 16)
        for _ in range(8):
            self.parser.execute('esperar')
        self.assertEqual(self.game.focus_charges, 2)
        self.assertNotIn('energia', self.game.buffs)
        self.assertEqual(self.game.incoming_damage(16), 16)

    def test_energy_no_stacking_free_queries_no_expiry(self):
        self.give('energético')
        self.parser.execute('usar energético')
        for command in ('status', 'inventário', 'ajuda', '', 'xyz'):
            self.parser.execute(command)
        self.assertEqual(self.game.focus_charges, 2)
        self.give('energético')
        self.parser.execute('usar energético')
        self.assertIn('energético', self.game.inventory)
        self.assertEqual(self.game.focus_charges, 2)

    def test_focus_does_not_increase_guard_damage_reduction(self):
        self.parser.confrontation.roll = lambda: 1.0
        self.encounter()
        self.game.focus_charges = 2
        self.parser.execute('defender')
        self.assertEqual(self.game.health, 86)
        self.assertEqual(self.game.incoming_damage(1), 1)
        self.assertEqual(self.game.focus_charges, 2)

    def test_weapon_ammo_damage_and_no_final_retaliation(self):
        enemy = self.encounter()
        gun = self.give('pistola', weapon=WeaponState())
        self.game.equip_item('pistola')
        self.parser.execute('atacar')
        self.assertEqual(enemy.health, 25)
        self.assertEqual(gun.weapon.ammo, 1)
        self.assertEqual(self.game.health, 84)
        enemy.preparing = True
        self.parser.execute('atacar')
        self.assertEqual(enemy.health, 0)
        self.assertEqual(gun.weapon.ammo, 0)
        self.assertEqual(self.game.health, 84)

    def test_empty_weapon_still_costs_turn_and_does_not_melee(self):
        enemy = self.encounter()
        gun = self.give('pistola', weapon=WeaponState(ammo=0))
        self.game.equip_item('pistola')
        self.assertIn('Droga... está vazia', self.parser.execute('atacar'))
        self.assertEqual(enemy.health, 60)
        self.assertEqual(gun.weapon.ammo, 0)
        self.assertEqual(self.game.health, 84)
        self.assertEqual(self.game.turn_count, 1)

    def test_reload_consumes_reserve_and_reaction(self):
        self.encounter()
        gun = self.give('pistola', weapon=WeaponState())
        self.give('munição de pistola', ammo_count=3)
        self.game.equip_item('pistola')
        self.parser.execute('recarregar')
        self.assertEqual(gun.weapon.ammo, 5)
        self.assertNotIn('munição de pistola', self.game.inventory)
        self.assertEqual(self.game.health, 84)
        self.assertEqual(self.game.turn_count, 1)

    def test_reload_capacity_leftover_and_full_feedback(self):
        gun = self.give('pistola', weapon=WeaponState(ammo=11))
        ammo = self.give('munição de pistola', ammo_count=3)
        self.game.equip_item('pistola')
        self.parser.execute('recarregar pistola')
        self.assertEqual(gun.weapon.ammo, 12)
        self.assertEqual(ammo.ammo_count, 2)
        self.assertIn('Já está carregada', self.parser.execute('recarregar'))
        self.assertEqual(ammo.ammo_count, 2)

    def test_reload_requires_equipment_and_reserve(self):
        gun = self.give('pistola', weapon=WeaponState())
        self.assertIn('na mão primeiro', self.parser.execute('recarregar pistola'))
        self.game.equip_item('pistola')
        self.assertIn('Não tenho cartuchos', self.parser.execute('recarregar'))
        self.assertEqual(gun.weapon.ammo, 2)

    def test_drop_and_recover_preserve_weapon_ammo(self):
        gun = self.give('pistola', weapon=WeaponState(ammo=1))
        self.game.equip_item('pistola')
        self.parser.execute('largar pistola')
        self.assertIsNone(self.game.equipped_item)
        self.parser.execute('pegar pistola')
        self.assertIs(self.game.item_objects['pistola'], gun)
        self.assertEqual(gun.weapon.ammo, 1)

    def test_equip_and_switch_both_allow_reaction(self):
        enemy = self.encounter()
        self.give('pistola', weapon=WeaponState())
        self.give('lanterna')
        self.parser.execute('equipar pistola')
        self.assertEqual(self.game.health, 84)
        enemy.preparing = True
        self.parser.execute('equipar lanterna')
        self.assertEqual(self.game.health, 68)
        self.assertEqual(self.game.turn_count, 2)

    def test_flashlight_before_pickup_equipment_and_toggle(self):
        self.assertIn('pegar lanterna primeiro', self.parser.execute('usar lanterna'))
        self.parser.execute('pegar lanterna')
        self.assertIn('lanterna na mão primeiro', self.parser.execute('usar lanterna'))
        self.parser.execute('equipar lanterna')
        self.parser.execute('ligar lanterna')
        self.assertTrue(self.game.light_visible)
        self.parser.execute('desligar lanterna')
        self.assertFalse(self.game.light_visible)
        self.parser.execute('usar lanterna')
        self.assertTrue(self.game.light_visible)

    def test_visible_flashlight_exposes_stealth(self):
        self.parser.execute('pegar lanterna')
        self.parser.execute('equipar lanterna')
        self.parser.execute('ligar lanterna')
        self.game.current_location = 'main_hall'
        self.game.get_current_room().objects['porta do porão'].opened = True
        self.parser.execute('esgueirar norte')
        self.assertTrue(self.game.in_confrontation)
        self.assertFalse(self.game.hidden)

    def test_flashlight_on_enemy_uses_one_turn(self):
        enemy = self.encounter()
        self.give('lanterna')
        self.game.equip_item('lanterna')
        self.parser.execute('usar lanterna no vigia')
        self.assertEqual(self.game.turn_count, 1)
        self.assertEqual(self.game.health, 100)
        self.assertTrue(enemy.flash_used)

    def test_fear_bounds_profile_and_weapon_penalty(self):
        self.game.increase_fear(200)
        self.assertEqual(self.game.fear, 100)
        self.assertEqual(fear_profile(100)['breathing'], 'ofegante')
        enemy = self.encounter()
        self.give('pistola', weapon=WeaponState())
        self.game.equip_item('pistola')
        self.parser.execute('atacar')
        self.assertEqual(enemy.health, 30)
        self.game.reduce_fear(200)
        self.assertEqual(self.game.fear, 0)
        self.assertEqual(fear_profile(0)['ranged_damage_penalty'], 0)

    def test_context_missing_unknown_and_locked_without_spoilers(self):
        self.assertIn('Não tenho isso comigo', self.parser.execute('usar kit médico'))
        self.assertEqual('Não foi possível entender essa ação.', self.parser.execute('asdfg'))
        self.game.current_location = 'main_hall'
        text = self.parser.execute('abrir gaveta')
        self.assertIn('outra maneira', text)
        for secret in ('pé de cabra', 'cozinha', '0417', 'escritório'):
            self.assertNotIn(secret, text)

    def test_duplicate_item_does_not_destroy_second_copy(self):
        self.parser.execute('pegar bandagem')
        self.game.current_location = 'kitchen'
        self.parser.execute('pegar bandagem')
        self.assertEqual(self.game.inventory.count('bandagem'), 1)
        self.assertIn('bandagem', self.game.get_current_room().objects)
        self.game.health = 50
        self.parser.execute('usar bandagem')
        self.parser.execute('pegar bandagem')
        self.assertIn('bandagem', self.game.inventory)

    def test_world_supply_distribution_and_independent_weapon_state(self):
        def collect(room):
            pending = list(room.objects.values())
            while pending:
                obj = pending.pop()
                yield obj
                pending.extend(obj.contents + obj.hidden_objects)
        objects = [obj for room in self.game.rooms.values() for obj in collect(room)]
        names = [obj.name for obj in objects]
        self.assertEqual(names.count('bandagem'), 2)
        for name in ('spray de cura', 'kit médico', 'pistola', 'energético'):
            self.assertEqual(names.count(name), 1)
        gun = next(obj for obj in objects if obj.name == 'pistola')
        gun.weapon.ammo = 0
        other = GameState(configuration='prototype').rooms['office'].objects['cofre'].contents
        self.assertEqual(next(obj for obj in other if obj.name == 'pistola').weapon.ammo, 2)

    def test_dropping_duplicate_cannot_overwrite_world_supply(self):
        self.parser.execute('pegar bandagem')
        carried = self.game.item_objects['bandagem']
        self.game.current_location = 'kitchen'
        original = self.game.get_current_room().objects['bandagem']
        self.parser.execute('largar bandagem')
        self.assertIs(self.game.get_current_room().objects['bandagem'], original)
        self.assertIs(self.game.item_objects['bandagem'], carried)

    def test_snapshot_is_read_only_copy_and_has_hud_data(self):
        self.give('pistola', weapon=WeaponState())
        state = self.game.snapshot()
        self.assertEqual(state['weapons']['pistola']['capacity'], 12)
        state['weapons']['pistola']['ammo'] = 99
        state['inventory'].clear()
        state['buffs']['energia'] = 99
        self.assertEqual(self.game.item_objects['pistola'].weapon.ammo, 2)
        self.assertIn('pistola', self.game.inventory)
        self.assertFalse(self.game.buffs)


if __name__ == '__main__':
    unittest.main()

