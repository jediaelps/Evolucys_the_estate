import unittest
from command_parser import CommandParser
from game_state import GameState
from world import Room, GameObject, PassageState


class HelpPathsTests(unittest.TestCase):
    def setUp(self):
        self.game = GameState()
        self.game.current_location = 'T01'
        self.parser = CommandParser(self.game)

    def test_all_hall_routes_without_blocked_or_future_destinations(self):
        self.game.current_location = 'main_hall'
        before = self.game.snapshot()
        text = self.parser.execute('ajuda')
        for route in ('SUL', 'LESTE', 'SUBIR', 'sala de estar', 'sala de jantar', 'banheiro social', 'sala de manutenção'):
            self.assertIn(route, text)
        for secret in ('biblioteca', 'porão', 'NORTE', 'via_t', 'L01'):
            self.assertNotIn(secret, text)
        self.assertIn('Joseph:', text)
        self.assertIn('EXAMINAR', text)
        self.assertEqual(before, self.game.snapshot())

    def test_relative_directions_require_reference_and_no_turn(self):
        for command in ('ir esquerda', 'seguir para a direita', 'frente', 'ir para trás', 'fugir esquerda'):
            before = self.game.snapshot()
            self.assertIn('referência', self.parser.execute(command))
            self.assertEqual(before, self.game.snapshot())

    def test_explicit_local_relative_name_can_be_resolved(self):
        room = self.game.get_current_room()
        room.exit_names['norte'] = 'passagem da esquerda'
        self.parser.execute('ir esquerda')
        self.assertEqual(self.game.current_location, 'main_hall')

    def test_secret_and_missing_destinations_do_not_leak_or_mutate(self):
        room = self.game.get_current_room()
        room.add_exit('segredo', 'office', name='atalho secreto', state=PassageState('secret',known=False))
        room.add_exit('ausente', 'L13', name='laboratório futuro')
        text = self.parser.execute('ajuda')
        self.assertIn('NORTE', text)
        self.assertNotIn('secreto', text)
        self.assertNotIn('laboratório', text)
        self.assertFalse(room.exit_states['segredo'].known)

    def test_prototype_and_look_and_reference_preserved(self):
        game = GameState(configuration='prototype'); parser=CommandParser(game)
        self.assertEqual(len(game.rooms), 6)
        self.assertIn('EXPLORAÇÃO', parser.execute('ajuda comandos'))
        self.assertEqual(game.turn_count, 0)
        self.assertNotIn('lanterna', parser.execute('olhar em volta'))
        game.current_location='upper_hall'
        self.assertIn('DESCER', parser.execute('ajuda'))

    def test_survival_still_offers_all_paths(self):
        self.game.current_location='main_hall'; self.game.fear=70
        text=self.parser.execute('ajuda')
        self.assertIn('tenso', text)
        self.assertIn('SUL',text); self.assertIn('LESTE',text)

from confrontation import Enemy
from system_demo import create_system_demo

class PerceptionTests(unittest.TestCase):
    def setUp(self):
        self.game=create_system_demo('light'); self.parser=CommandParser(self.game)
        self.room=self.game.get_current_room(); self.other=self.game.rooms['demo_hall']
        self.enemy=Enemy('nome secreto', sound='rosnados')
        self.other.enemy=self.enemy
        self.door=self.room.exit_doors['norte']

    def test_specific_sounds_never_identify_creature(self):
        for sound in ('passos','rosnados','grunhidos','arranhões','respiração pesada','objetos sendo movimentados','impactos','batidas metálicas'):
            self.enemy.sound=sound
            text=self.game.exploration.listen('porta')
            self.assertIn(sound,text);self.assertNotIn('nome secreto',text)

    def test_silent_enemy_and_zero_intensity_have_no_evidence(self):
        for sound,intensity in ((None,3),('rosnados',0)):
            self.enemy.sound=sound; self.enemy.sound_intensity=intensity
            text=self.game.exploration.listen('porta')
            self.assertIn('nada',text);self.assertNotIn('seguro',text)
            self.assertNotIn('criatura',self.parser.execute('ajuda'))

    def test_closed_door_distance_and_noise_attenuate(self):
        self.enemy.sound_intensity=2
        self.assertTrue(self.game.exploration.audible_signals())
        self.door.opened=False
        self.assertFalse(self.game.exploration.audible_signals())
        self.door.opened=True;self.enemy.distance='distante'
        self.assertFalse(self.game.exploration.audible_signals())
        self.enemy.distance='próximo';self.room.ambient_noise=4
        self.assertFalse(self.game.exploration.audible_signals())

    def test_blocked_soundproof_and_disabled_edges_stop_sound(self):
        for attr in ('blocked','soundproof'):
            setattr(self.door,attr,True)
            self.assertFalse(self.game.exploration.audible_signals(explicit=True))
            setattr(self.door,attr,False)
        self.room.exit_states['norte']=PassageState('closed',enabled=False)
        self.assertFalse(self.game.exploration.audible_signals(explicit=True))

    def test_focus_does_not_hear_through_sealed_route(self):
        self.other.enemies=[]; self.game.rooms['demo_end'].enemy=self.enemy
        self.game.focus_charges=2
        self.assertTrue(self.game.exploration.audible_signals())
        self.door.soundproof=True
        self.assertFalse(self.game.exploration.audible_signals())
        self.assertEqual(self.game.focus_charges,2)

    def test_gap_requires_actual_opening_light_and_line_of_sight(self):
        self.door.opened=False;self.other.dark=False
        self.assertNotIn('vulto',self.game.exploration.observe_passage('porta'))
        self.door.sight_gap=True
        text=self.game.exploration.observe_passage('porta')
        self.assertIn('vulto',text);self.assertNotIn('nome secreto',text)
        for attr in ('dark',):
            setattr(self.other,attr,True)
            self.assertFalse(self.game.exploration.visible_threats(self.other))
        self.other.dark=False;self.enemy.in_sight=False
        self.assertFalse(self.game.exploration.visible_threats(self.other))

    def test_peek_aliases_and_examine_use_real_passage_without_moving(self):
        self.other.dark=False
        for cmd in ('olhar pela fresta', 'espiar pela abertura', 'verificar se há movimento do outro lado','olhar para a porta','examinar porta','observar a porta'):
            self.game.exploration.memory.contexts.clear()
            text=self.parser.execute(cmd)
            self.assertIn('vulto',text)
            self.assertNotIn('nome secreto',text)
            self.assertEqual(self.game.current_location,'demo_foyer')
        self.assertEqual(self.game.turn_count,6)

    def test_memory_is_uncertain_after_enemy_moves(self):
        self.game.exploration.listen('porta')
        self.other.enemies=[];self.game.rooms['demo_end'].enemy=self.enemy
        text=self.game.exploration.listen('porta')
        self.assertIn('não tô ouvindo mais nada',text)
        helptext=self.parser.execute('ajuda')
        self.assertIn('Lembro',helptext);self.assertNotIn('desapareceu',helptext)

    def test_hidden_or_unlit_local_threat_not_revealed_by_help(self):
        self.room.enemy=Enemy('oculto',sound=None)
        self.room.enemy.sprite.visible=False
        self.assertNotIn('DEFENDER',self.parser.execute('ajuda'))
        self.room.enemy.sprite.visible=True;self.room.dark=True
        self.assertNotIn('DEFENDER',self.parser.execute('ajuda'))

    def test_dark_silent_creature_does_not_disclose_identity_or_preparation(self):
        self.room.dark=True;self.room.enemy=self.enemy;self.other.enemies=[]
        self.enemy.sound=None;self.enemy.alert=True;self.enemy.preparing=False
        text=self.parser.execute('olhar em volta')
        self.assertNotIn('nome secreto',text)
        self.assertNotIn('ergue o braço',text)
        self.assertNotIn('prepara',text)
        self.assertTrue(self.enemy.preparing)
        text=self.parser.execute('esperar')
        self.assertIn('Algo fora de vista golpeia',text)
        self.assertNotIn('nome secreto',text)

    def test_surprise_once_without_automatic_defense_or_extra_turn(self):
        self.enemy.sound=None;self.enemy.surprise=85
        text=self.parser.execute('ir norte')
        self.assertIn('Meu Deus',text)
        self.assertEqual(self.game.turn_count,1)
        self.assertEqual(self.game.health,100)
        self.assertFalse(self.parser.confrontation.guarding)
        self.assertEqual(self.game.exploration.surprise(self.enemy),'')

    def test_silent_hidden_patrol_arrival_does_not_announce_creature(self):
        self.game=create_system_demo('patrol');self.game.current_location='demo_hall'
        enemy=self.game.rooms['demo_end'].enemy
        enemy.sound=None;enemy.sprite.visible=False;enemy.patrol_interval=1
        self.game.hidden=True
        text=self.game.exploration.advance()
        self.assertNotIn('criatura',text);self.assertNotIn('Ouço',text)
        self.assertIn(enemy,self.game.get_current_room().enemies)
        self.game.exploration.hiding = self.game.get_current_room().objects['armário pesado'].object_id
        for _ in range(3):
            text=self.game.exploration.advance()
            self.assertNotIn('criatura',text);self.assertNotIn('Ouço',text)
            self.assertNotIn('ele',text)

    def test_listening_through_closed_door_does_not_contradict_itself(self):
        self.door.opened=False
        text=self.parser.execute('ouvir porta')
        self.assertIn('rosnados',text)
        self.assertNotIn('não tô ouvindo',text)

from items import defense_profile, avoidance_chance, WeaponState
from unittest.mock import Mock, patch
import test_visual_commands as ui

class DefenseAndEscapeTests(unittest.TestCase):
    def setUp(self):
        self.game=GameState(configuration='prototype');self.parser=CommandParser(self.game)
        self.game.current_location='cellar';self.enemy=self.game.get_current_room().enemy
        self.enemy.alert=True;self.enemy.preparing=True
        self.game.get_current_room().exit_doors['sul'].opened=True
        self.game.get_current_room().exit_doors['sul'].locked=False
        self.combat=self.parser.confrontation
        self.combat.roll=Mock(return_value=.99)

    def equip(self,name,gun=False):
        obj=GameObject(name,'',portable=True,weapon=WeaponState() if gun else None)
        self.game.add_item(name);self.game.item_objects[name]=obj;self.game.equipped_item=name
        return obj

    def test_normal_defense_profiles_damage_and_no_ammo_consumption(self):
        for name,gun,damage in ((None,False,14),('pé de cabra',False,12),('bastão de beisebol',False,8),('pistola',True,14),('lanterna',False,14)):
            with self.subTest(name=name):
                self.setUp()
                obj=self.equip(name,gun) if name else None
                text=self.parser.execute('defender')
                self.assertEqual(self.game.health,100-damage)
                self.assertIn('amortecer',text);self.assertEqual(self.game.turn_count,1)
                self.assertFalse(self.combat.guarding)
                self.combat.roll.assert_called_once()
                if gun:self.assertEqual(obj.weapon.ammo,2)

    def test_perfect_defense_each_profile_is_zero_damage(self):
        for name in (None,'pé de cabra','bastão de beisebol','lanterna'):
            self.setUp()
            if name:self.equip(name)
            self.combat.roll=Mock(return_value=0)
            text=self.parser.execute('defender')
            self.assertEqual(self.game.health,100);self.assertIn('bloquear',text)
            self.assertNotIn('golpeia Joseph',text)

    def test_exact_profiles_and_moderate_bounded_fear(self):
        for name,reduction,perfect in (('bastão de beisebol',.5,.25),('pé de cabra',.3,.15),('lanterna',.15,.05)):
            profile=defense_profile(GameObject(name,''))
            self.assertEqual((profile.reduction,profile.perfect),(reduction,perfect))
        for base in (.05,.15,.25,.30,.75):
            self.assertEqual(avoidance_chance(base,0),base)
            self.assertAlmostEqual(avoidance_chance(base,100),base*.8)
            for fear in (-100,0,50,100,900):
                self.assertGreater(avoidance_chance(base,fear),0)
                self.assertLessEqual(avoidance_chance(base,fear),1)

    def test_dodge_success_and_failure_no_partial_reduction(self):
        for roll,damage in ((0,0),(.99,16)):
            self.setUp();self.combat.roll=Mock(return_value=roll)
            self.equip('bastão de beisebol')
            text=self.parser.execute('esquivar')
            self.assertEqual(self.game.health,100-damage)
            self.assertEqual(self.game.current_location,'cellar')
            self.assertEqual(self.game.turn_count,1);self.combat.roll.assert_called_once()
            self.assertIn('quase me acertou' if damage==0 else 'Não consegui sair',text)

    def test_guard_survives_preparation_and_free_queries(self):
        self.enemy.alert=False;self.enemy.preparing=False
        self.parser.execute('defender')
        self.assertTrue(self.combat.guarding)
        self.parser.execute('ajuda');self.parser.execute('status')
        self.assertTrue(self.combat.guarding);self.assertEqual(self.game.turn_count,1)
        self.parser.execute('esperar');self.assertTrue(self.combat.guarding)
        self.parser.execute('esperar')
        self.assertEqual(self.game.health,86);self.assertFalse(self.combat.guarding)

    def test_stance_expires_without_attack_and_other_action_cancels(self):
        self.enemy.distance='distante'
        self.parser.execute('defender');self.parser.execute('esperar');self.parser.execute('esperar')
        self.assertFalse(self.combat.guarding)
        self.parser.execute('defender');self.parser.execute('examinar nada')
        self.assertFalse(self.combat.guarding)
        self.combat.roll.assert_not_called()

    def test_defense_and_dodge_never_stack(self):
        self.enemy.preparing=False
        self.parser.execute('defender')
        self.parser.execute('esquivar')
        self.assertEqual(self.game.health,84)
        self.assertFalse(self.combat.guarding);self.assertFalse(self.combat.dodging)

    def test_flee_success_and_failure_one_reaction(self):
        for roll,room,health in ((0,'main_hall',100),(.99,'cellar',84)):
            self.setUp();self.combat.roll=Mock(return_value=roll)
            with patch.object(self.combat,'react',wraps=self.combat.react) as react:
                text=self.parser.execute('fugir sul');react.assert_called_once()
            self.assertEqual(self.game.current_location,room);self.assertEqual(self.game.health,health)
            self.assertEqual(self.game.turn_count,1);self.combat.roll.assert_called_once()
            self.assertIn('Consegui escapar' if roll==0 else 'Não consegui passar',text)

    def test_flee_obstacles_no_roll_or_bypass(self):
        for condition in ('locked','blocked','closed','disabled','absent'):
            self.setUp();door=self.game.get_current_room().exit_doors['sul']
            if condition=='closed':door.opened=False
            elif condition=='disabled':self.game.get_current_room().exit_states['sul']=PassageState('blocked',enabled=False)
            elif condition=='absent':self.game.get_current_room().exits['sul']='nonexistent'
            else:setattr(door,condition,True)
            self.parser.execute('fugir sul')
            self.assertEqual(self.game.current_location,'cellar');self.combat.roll.assert_not_called()
            self.assertEqual(self.game.health,84)

    def test_normal_move_and_unalert_escape_have_no_probability(self):
        for command in ('ir sul','esgueirar sul','fugir sul'):
            self.setUp()
            if command=='fugir sul':self.enemy.alert=False
            self.parser.execute(command)
            self.assertEqual(self.game.current_location,'main_hall')
            self.assertEqual(self.game.health,100);self.combat.roll.assert_not_called()

    def test_aliases_execute_once_and_preserve_focus_confidence(self):
        for command in ('me esquivar','desviar','desviar do golpe','esquivar do ataque'):
            self.setUp();self.game.focus_charges=2
            confidence=self.game.confidence
            self.parser.execute(command)
            self.assertEqual(self.game.turn_count,1);self.combat.roll.assert_called_once()
            self.assertEqual(self.game.focus_charges,2)
            self.assertEqual(self.game.confidence['value'],confidence['value'])

    def test_campaign_blocks_unchanged(self):
        game=GameState();parser=CommandParser(game);parser.confrontation.roll=Mock(return_value=0)
        for origin,side in (('main_hall','norte'),('main_hall','via_t09'),('kitchen','via_t12')):
            game.current_location=origin;enemy=Enemy('ameaça');enemy.alert=True
            game.get_current_room().enemies=[enemy]
            parser.execute('fugir '+side)
            self.assertEqual(game.current_location,origin)
        parser.confrontation.roll.assert_not_called()
        self.assertEqual(len(game.rooms),58)

    def test_probabilities_change_actual_outcomes_under_fear(self):
        for action,roll in (('defender',.24),('esquivar',.28),('fugir sul',.70)):
            for fear,success in ((0,True),(100,False)):
                with self.subTest(action=action,fear=fear):
                    self.setUp();self.equip('bastão de beisebol');self.game.fear=fear
                    self.combat.roll=Mock(return_value=roll)
                    self.parser.execute(action)
                    self.assertEqual(self.game.health==100,success)
                    self.combat.roll.assert_called_once()

    def test_unknown_secret_exit_does_not_reveal_locked_door(self):
        room=self.game.get_current_room()
        room.exit_states['sul']=PassageState('secret',known=False)
        room.exit_doors['sul'].locked=True
        response=self.parser.execute('fugir sul')
        self.assertNotIn('trancada',response)
        self.assertEqual(self.game.current_location,'cellar')
        self.combat.roll.assert_not_called()

class CombatInterfaceTests(unittest.TestCase):
    setUp=ui.VisualCommandTests.setUp
    tearDown=ui.VisualCommandTests.tearDown
    enter=ui.VisualCommandTests.enter

    def test_enter_dodge_and_flee_once_in_existing_interface(self):
        self.app.start_tutorial(4);self.enter('ir norte');self.enter('esperar')
        parser=self.app.session.parser;parser.confrontation.roll=Mock(return_value=0)
        before=self.app.session.game.turn_count
        with patch.object(parser,'execute',wraps=parser.execute) as execute:
            self.enter('esquivar');execute.assert_called_once_with('esquivar')
        self.assertEqual(self.app.session.game.turn_count,before+1)
        self.assertEqual(self.app.session.game.health,100)
        self.assertIs(self.app.root.focus_get(),self.app.command_entry)
        self.assertIn('Joseph:',self.app.history_view.get('1.0','end'))
        self.enter('fugir sul')
        self.assertEqual(self.app.session.game.current_location,'test_start')
        self.assertEqual(self.app.session.game.health,100)
