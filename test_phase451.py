import unittest
from unittest.mock import patch
from command_language import normalize
from command_parser import CommandParser
from contextual_tutorial import TutorialGuide
from tutorial import TutorialState
from visual_session import VisualSession
from target_selection import candidates, pose
from world import GameObject
import test_visual_commands as ui


class NaturalLanguageTests(unittest.TestCase):
    def setUp(self):
        self.game = TutorialState(4)
        self.game.install_targets()
        self.parser = CommandParser(self.game)
        for name in ('pistola', 'pé de cabra', 'bandagem', 'munição de pistola'):
            self.parser.execute('pegar ' + name)
        self.parser.execute('equipar pistola')
        self.parser.execute('ir norte')
        self.left, self.right = self.game.get_current_room().enemies

    def test_observation_variants(self):
        self.game.get_current_room().add_object(GameObject('gaveta', 'Madeira antiga.'))
        for command in ('ver gaveta', 'ver a gaveta', 'olhar gaveta', 'olhar a gaveta', 'olhar para a gaveta', 'observar gaveta', 'examinar gaveta', 'examinar a gaveta', 'inspecionar gaveta', 'dar uma olhada na gaveta'):
            with self.subTest(command=command):
                self.assertIn('Madeira antiga', self.parser.execute(command))

    def test_collection_synonyms_articles(self):
        for command in ('pegar a lanterna', 'apanhar lanterna', 'recolher a lanterna'):
            game = TutorialState(1)
            CommandParser(game).execute(command)
            self.assertIn('lanterna', game.inventory)

    def test_movement_prepositions_and_room_name(self):
        for command in ('ir para o sul', 'seguir para sul', 'andar ao sul'):
            self.assertEqual(normalize(self.game, command), 'ir sul')
        name = self.game.rooms['test_start'].name
        self.assertEqual(normalize(self.game, 'seguir para ' + name.lower()), 'ir sul')

    def test_usage_synonym(self):
        self.game.health = 50
        self.parser.execute('inventário')
        self.parser.execute('utilizar a bandagem')
        self.assertNotIn('bandagem', self.game.inventory)

    def test_single_enemy_no_ambiguity(self):
        self.game.get_current_room().enemies = [self.left]
        self.assertIn('atinge zumbi', self.parser.execute('atirar no zumbi'))
        self.assertEqual(self.left.health, 85)

    def test_two_same_names_have_distinct_identity(self):
        self.assertEqual(self.left.name, self.right.name)
        self.assertNotEqual(self.left.enemy_id, self.right.enemy_id)
        self.assertEqual(self.left.enemy_id, self.left.sprite.object_id)
        self.assertNotEqual(self.left.sprite.object_id, self.right.sprite.object_id)

    def test_left_target(self):
        self.parser.execute('atirar no zumbi da esquerda')
        self.assertEqual((self.left.health, self.right.health), (85, 120))

    def test_right_target(self):
        self.parser.execute('usar pistola no zumbi da direita')
        self.assertEqual((self.left.health, self.right.health), (120, 85))

    def test_nearest_target(self):
        self.parser.execute('atacar o mais próximo')
        self.assertEqual((self.left.health, self.right.health), (85, 120))

    def test_farthest_target(self):
        self.parser.execute('atirar no mais distante')
        self.assertEqual((self.left.health, self.right.health), (120, 85))

    def test_ordinal_and_visible_trait(self):
        room = self.game.get_current_room()
        self.assertEqual(candidates(room, 'o segundo'), [self.right])
        self.assertEqual(candidates(room, 'o primeiro'), [self.left])
        self.assertEqual(candidates(room, 'o de casaco rasgado'), [self.left])

    def test_ambiguity_does_not_spend_ammo_turn_or_buff(self):
        self.game.buffs['energia'] = 3
        before = self.game.snapshot()
        text = self.parser.execute('atacar zumbi')
        self.assertIn('Qual deles?', text)
        self.assertIn('esquerda', text)
        self.assertEqual(self.game.snapshot(), before)

    def test_continuation_left(self):
        self.parser.execute('atacar zumbi')
        self.parser.execute('o da esquerda')
        self.assertEqual((self.left.health, self.right.health), (85, 120))

    def test_continuation_right_preserves_weapon(self):
        self.parser.execute('atacar zumbi com a pistola')
        self.parser.execute('o da direita')
        self.assertEqual((self.left.health, self.right.health), (120, 85))

    def test_continuation_nearest(self):
        self.parser.execute('atirar no zumbi')
        self.parser.execute('o mais próximo')
        self.assertEqual(self.left.health, 85)

    def test_continuation_farthest(self):
        self.parser.execute('atirar no zumbi')
        self.parser.execute('o mais distante')
        self.assertEqual(self.right.health, 85)

    def test_continuation_second(self):
        self.parser.execute('atirar no zumbi')
        self.parser.execute('o segundo')
        self.assertEqual(self.right.health, 85)

    def test_pending_cancelled_by_unrelated_command(self):
        self.parser.execute('atacar zumbi')
        self.parser.execute('status')
        self.parser.execute('o da esquerda')
        self.assertEqual(self.left.health, 120)

    def test_pending_invalidated_by_world_change(self):
        self.parser.execute('atacar zumbi')
        self.right.health = 0
        self.parser.execute('o da esquerda')
        self.assertEqual(self.left.health, 120)

    def test_crowbar_explicit_weapon_is_preserved(self):
        self.parser.execute('equipar pé de cabra')
        self.parser.execute('bater no zumbi da esquerda com o pé de cabra')
        self.assertEqual(self.left.health, 95)
        self.assertIn('pé de cabra', self.game.inventory)

    def test_using_crowbar_executes_obvious_attack(self):
        self.parser.execute('equipar pé de cabra')
        self.assertIn('atinge', self.parser.execute('usar pé de cabra no zumbi da esquerda'))
        self.assertEqual(self.left.health, 95)

    def test_melee_far_fails_without_damage(self):
        self.parser.execute('equipar pé de cabra')
        self.assertIn('longe demais', self.parser.execute('bater no zumbi distante com o pé de cabra'))
        self.assertEqual(self.right.health, 120)

    def test_explicit_weapon_requires_equipment(self):
        self.assertIn('mão primeiro', self.parser.execute('atacar o zumbi da esquerda com o pé de cabra'))
        self.assertEqual(self.left.health, 120)

    def test_shoot_requires_firearm(self):
        self.parser.execute('equipar pé de cabra')
        self.assertIn('arma de fogo', self.parser.execute('disparar contra o zumbi da esquerda'))
        self.assertEqual(self.left.health, 120)

    def test_joseph_reformulates_inappropriate_melee(self):
        self.assertIn('Melhor atirar', self.parser.execute('bater no zumbi da esquerda com a pistola'))
        self.assertEqual(self.left.health, 120)

    def test_healing_enemy_has_specific_response(self):
        self.assertIn('cuidar de mim', self.parser.execute('usar bandagem no zumbi da esquerda'))
        self.assertIn('bandagem', self.game.inventory)

    def test_using_ammo_on_held_pistol_reloads(self):
        self.parser.execute('usar munição de pistola na pistola')
        self.assertEqual(self.game.item_objects['pistola'].weapon.ammo, 12)

    def test_puzzle_wrong_item_never_reveals_required_key(self):
        self.game.get_current_room().add_object(GameObject('mecanismo', '', locked=True, required_item='fusível vermelho'))
        text = self.parser.execute('usar bandagem no mecanismo')
        self.assertIn('não encaixa', text)
        self.assertNotIn('fusível', text)

    def test_names_and_identifiers_not_leaked(self):
        text = self.game.get_current_room().describe() + self.parser.execute('atacar zumbi')
        for value in (self.left.enemy_id, self.right.enemy_id, 'vigia vigia', 'parser', 'GameState', 'enemy_b'):
            self.assertNotIn(value, text)

    def test_pose_and_distance_match(self):
        left, left_scale = pose(self.left)
        right, right_scale = pose(self.right)
        self.assertLess(left[0], right[0])
        self.assertGreater(left[1], right[1])
        self.assertGreater(left_scale, right_scale)

    def test_nonweapon_does_not_become_an_attack(self):
        self.parser.execute('equipar bandagem')
        text = self.parser.execute('atacar zumbi da esquerda com bandagem')
        self.assertIn('não é uma arma', text)
        self.assertEqual(self.left.health, 120)

    def test_default_positions_arranged_before_pending_memory(self):
        self.right.sprite.position = self.left.sprite.position
        self.parser.execute('atacar zumbi')
        self.parser.execute('o da direita')
        self.assertEqual(self.right.health, 85)
        self.assertLess(self.left.sprite.position[0], self.right.sprite.position[0])

    def test_pending_scope_does_not_include_other_creature_type(self):
        from confrontation import Enemy
        other = Enemy('criatura')
        other.sprite.position = (.95, .5)
        self.game.get_current_room().enemies.append(other)
        self.parser.execute('atacar zumbi')
        self.parser.execute('o da direita')
        self.assertEqual(self.right.health, 85)
        self.assertEqual(other.health, 60)

    def test_attack_synonyms_keep_damage_rules(self):
        self.parser.execute('equipar pé de cabra')
        for verb in ('atacar', 'bater', 'golpear', 'acertar'):
            self.left.health = 120
            self.parser.execute(verb + ' no zumbi da esquerda')
            self.assertEqual(self.left.health, 95)

    def test_center_reference(self):
        from confrontation import Enemy
        center = Enemy('zumbi')
        center.sprite.position = (.5, .44)
        self.game.get_current_room().enemies.append(center)
        self.assertEqual(candidates(self.game.get_current_room(), 'o do centro'), [center])


class GuideTests(unittest.TestCase):
    def setUp(self):
        self.session = VisualSession()
        self.session.start_tutorial(1)

    def test_first_opportunity_is_marked_presented(self):
        guide = self.session.game.guide
        self.assertIn('observe', guide.presented)
        self.assertIn('olhar em volta', guide.current)

    def test_hint_does_not_repeat(self):
        initial = self.session.game.guide.current
        for _ in range(15):
            self.session.execute('status')
            self.assertNotEqual(self.session.game.guide.current, initial)

    def test_inspection_hint_does_not_reveal_back(self):
        self.session.execute('examinar retrato')
        hint = self.session.game.guide.current
        self.assertIn('objeto', hint)
        for secret in ('atrás', 'verso', 'relógio', 'inscrição'):
            self.assertNotIn(secret, hint)
        self.session.execute('fechar leitura')
        self.session.execute('examinar retrato')
        self.assertNotEqual(self.session.game.guide.current, hint)

    def test_multi_target_lesson_only_when_multiple_present(self):
        for _ in range(20):
            self.session.execute('status')
        self.assertNotIn('targets', self.session.game.guide.presented)
        self.session.start_tutorial(4)
        self.session.game.install_targets()
        self.session.execute('ir norte')
        self.session.execute('status')
        self.session.execute('status')
        self.assertIn('targets', self.session.game.guide.presented)

    def test_guide_serialization_is_independent(self):
        guide = self.session.game.guide
        restored = TutorialGuide.from_dict(guide.to_dict())
        self.assertEqual(restored.presented, guide.presented)
        restored.presented.add('other')
        self.assertNotIn('other', guide.presented)


class NaturalInterfaceTests(unittest.TestCase):
    setUp = ui.VisualCommandTests.setUp
    tearDown = ui.VisualCommandTests.tearDown
    enter = ui.VisualCommandTests.enter

    def test_two_enemies_visual_and_continuation(self):
        self.app.start_target_demo()
        self.enter('recolher pistola')
        self.enter('equipar pistola')
        self.enter('seguir norte')
        left, right = self.app.session.game.get_current_room().enemies
        self.assertTrue(self.app.canvas.find_withtag('object:' + left.sprite.object_id))
        self.assertTrue(self.app.canvas.find_withtag('object:' + right.sprite.object_id))
        self.enter('atirar no zumbi')
        self.assertIn('Qual deles', self.app.session.last_message)
        self.enter('o da direita')
        self.assertEqual((left.health, right.health), (120, 85))

    def test_inspection_has_no_secret_hint_and_does_not_repeat(self):
        self.app.start_tutorial(1)
        self.enter('dar uma olhada no retrato')
        self.assertNotIn('atrás', self.app.reader_panel.inspect_hint.cget('text'))
        self.app.close_reader()
        self.enter('examinar retrato')
        self.assertNotIn('ESC me faz voltar', self.app.reader_panel.inspect_hint.cget('text'))

    def test_natural_inventory_commands_keep_world_blocked(self):
        self.enter('recolher bandagem')
        self.enter('inventário')
        before = self.app.session.game.snapshot()
        self.enter('seguir norte')
        self.assertEqual(self.app.session.game.snapshot(), before)
        self.enter('fechar inventário')
        self.enter('ver carta antiga')
        self.assertIn('Joseph, guarde', self.app.reader_text.get('1.0', 'end'))


if __name__ == '__main__':
    unittest.main()
