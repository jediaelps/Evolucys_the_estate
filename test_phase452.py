import json
import unittest
from dataclasses import replace

from command_parser import CommandParser
from command_language import normalize
from game_state import GameState
from system_demo import create_system_demo
from tutorial import TutorialState
from confrontation import Enemy
from items import ItemCapabilities, WeaponState
from world import Room, GameObject
from hud_state import focus_icons
import test_visual_commands as ui


class SystemsTests(unittest.TestCase):
    def setUp(self):
        self.game = create_system_demo('light')
        self.parser = CommandParser(self.game)

    def take(self, name):
        self.parser.execute('pegar ' + name)
        return self.game.item_objects[name]

    def focus(self):
        self.take('energético')
        self.parser.execute('inventário')
        self.parser.execute('usar energético')
        self.parser.execute('fechar inventário')

    def test_consumable_requires_inventory_without_consumption_or_reaction(self):
        self.take('bandagem')
        self.game.health = 50
        before = self.game.snapshot()
        self.assertIn('inventário', self.parser.execute('usar bandagem'))
        self.assertEqual(self.game.snapshot(), before)
        self.parser.execute('inventário')
        self.parser.execute('usar bandagem')
        self.assertEqual(self.game.health, 70)
        self.assertNotIn('bandagem', self.game.inventory)

    def test_closing_inventory_revokes_personal_use(self):
        self.take('energético')
        self.parser.execute('inventário')
        self.parser.execute('fechar inventário')
        self.parser.execute('usar energético')
        self.assertEqual(self.game.focus_charges, 0)

    def test_key_works_in_scene_without_equipping(self):
        game = TutorialState(3)
        parser = CommandParser(game)
        parser.execute('pegar chave de arquivo')
        parser.execute('usar chave de arquivo no armário a')
        self.assertFalse(game.get_current_room().objects['armário a'].locked)
        self.assertIsNone(game.equipped_item)

    def test_wrong_tool_not_a_weapon(self):
        self.take('barra do macaco')
        self.parser.execute('equipar barra do macaco')
        enemy = Enemy('criatura')
        self.game.get_current_room().enemy = enemy
        self.assertIn('não é uma arma', self.parser.execute('atacar criatura com barra do macaco'))
        self.assertEqual(enemy.health, 60)

    def test_capabilities_support_future_melee_tools(self):
        item = GameObject('taco', '', portable=True, capabilities=ItemCapabilities(melee_damage=20, confidence=23))
        self.game.get_current_room().add_object(item)
        self.take('taco')
        self.parser.execute('equipar taco')
        enemy = Enemy('criatura')
        self.game.get_current_room().enemy = enemy
        self.parser.execute('golpear criatura com taco')
        self.assertEqual(enemy.health, 40)
        self.assertIn('taco', self.game.inventory)

    def test_confidence_independent_of_damage_fear_and_focus(self):
        gun = GameObject('arma', '', portable=True, weapon=WeaponState(), capabilities=ItemCapabilities(confidence=70))
        self.game.add_item('arma')
        self.game.item_objects['arma'] = gun
        self.game.equip_item('arma')
        value = self.game.confidence['value']
        self.game.fear = 100
        self.game.focus_charges = 2
        gun.weapon.spec = replace(gun.weapon.spec, damage=999)
        self.assertEqual(self.game.confidence['value'], value)
        self.assertEqual(self.game.focus_charges, 2)

    def test_confidence_equipment_context_and_empty_ammo(self):
        base = self.game.confidence['value']
        self.take('pé de cabra')
        self.game.equip_item('pé de cabra')
        armed = self.game.confidence['value']
        self.assertGreater(armed, base)
        self.game.get_current_room().enemies = [Enemy('desconhecido', unknown=True, threat=10), Enemy('outro')]
        self.game.health = 20
        self.assertLess(self.game.confidence['value'], armed)
        gun = GameObject('arma', '', weapon=WeaponState(), portable=True)
        self.game.add_item('arma'); self.game.item_objects['arma'] = gun; self.game.equip_item('arma')
        loaded = self.game.confidence['value']
        gun.weapon.ammo = 0
        self.assertLess(self.game.confidence['value'], loaded)

    def test_energy_gives_two_persistent_charges(self):
        self.focus()
        for _ in range(10):
            self.parser.execute('esperar')
        self.assertEqual(self.game.focus_charges, 2)
        self.assertEqual(self.game.incoming_damage(16), 16)

    def test_perception_does_not_consume_charge(self):
        self.focus()
        self.game.rooms['demo_end'].enemy.sound = 'passos'
        self.assertTrue(self.game.exploration.perception())
        self.parser.execute('ouvir atrás da porta')
        self.assertEqual(self.game.focus_charges, 2)

    def test_focus_consumed_only_to_prevent_loss(self):
        self.focus()
        self.game.exploration.surprise(Enemy('surpresa', surprise=100))
        self.assertEqual(self.game.focus_charges, 1)
        self.assertEqual(self.game.pending_startle, 0)
        self.assertGreater(self.game.fear, 0)
        self.game.exploration.surprise(Enemy('outra', surprise=100))
        self.assertEqual(self.game.focus_charges, 0)

    def test_mild_surprise_does_not_spend_focus(self):
        self.focus()
        self.game.exploration.surprise(Enemy('leve', surprise=10))
        self.assertEqual(self.game.focus_charges, 2)

    def test_surprise_without_focus_loses_next_physical_action_once(self):
        self.game.exploration.surprise(Enemy('susto', surprise=100))
        turn = self.game.turn_count
        self.parser.execute('status')
        self.assertEqual(self.game.pending_startle, 1)
        self.parser.execute('pegar lanterna')
        self.assertNotIn('lanterna', self.game.inventory)
        self.assertEqual(self.game.turn_count, turn+1)
        self.parser.execute('pegar lanterna')
        self.assertIn('lanterna', self.game.inventory)

    def test_same_surprise_not_repeated(self):
        self.focus()
        enemy = Enemy('susto', surprise=100)
        self.game.exploration.surprise(enemy)
        self.game.exploration.surprise(enemy)
        self.assertEqual(self.game.focus_charges, 1)

    def test_focus_hud_two_one_empty(self):
        self.assertEqual([focus_icons(n) for n in (2,1,0)], ['⚡ ⚡', '⚡', ''])

    def test_early_perception_only_when_sound_exists(self):
        self.game.rooms['demo_end'].enemy.sound = 'passos'
        self.assertFalse(self.game.exploration.perception())
        self.game.focus_charges = 2
        self.assertIn('ruído', self.game.exploration.perception())
        self.game.rooms['demo_end'].enemy.sound = None
        self.assertIn('agora está tudo quieto', self.game.exploration.perception())
        self.assertFalse(self.game.exploration.perception())

    def test_listening_synonyms_and_real_other_side(self):
        self.game.rooms['demo_hall'].enemy = Enemy('criatura')
        for command in ('ouvir atrás da porta', 'escutar a porta', 'ouvir atrás da porta norte', 'encostar o ouvido na porta', 'ver se tem alguém do outro lado'):
            with self.subTest(command=command):
                self.assertIn('passos', self.parser.execute(command))

    def test_silent_enemy_does_not_mean_safe(self):
        self.game.rooms['demo_hall'].enemy = Enemy('silencioso', sound=None)
        text = self.parser.execute('escutar porta')
        self.assertIn('Não estou ouvindo nada', text)
        self.assertNotIn('seguro', text)
        self.assertTrue(self.game.rooms['demo_hall'].enemy.alive)

    def test_cautious_movement_synonyms(self):
        for command in ('entrar devagar', 'passar pela porta furtivamente', 'entrar com cuidado', 'me esgueirar pela porta', 'entrar sem fazer barulho', 'avançar silenciosamente'):
            with self.subTest(command=command):
                self.assertTrue(normalize(self.game, command).startswith('esgueirar'))

    def test_caution_reduces_surprise_not_guaranteed_immunity(self):
        self.game.rooms['demo_hall'].enemy = Enemy('criatura', surprise=60)
        self.parser.execute('entrar devagar')
        self.assertEqual(self.game.pending_startle, 0)
        game = create_system_demo('surprise')
        CommandParser(game).execute('entrar devagar')
        self.assertEqual(game.pending_startle, 1)

    def test_hiding_successful_patrol_enters_searches_waits_leaves(self):
        game = create_system_demo('patrol')
        game.rooms['demo_hall'].dark = False  # A ronda precisa estar visível nesta validação.
        game.current_location = 'demo_hall'
        enemy = game.rooms['demo_end'].enemy
        enemy.patrol_interval = 1
        parser = CommandParser(game)
        texts = [parser.execute('esconder no armário pesado')]
        texts += [parser.execute('esperar') for _ in range(3)]
        self.assertIn('acaba de entrar', texts[0])
        self.assertIn('procurando', texts[1])
        self.assertIn('respiração', texts[2])
        self.assertIn('se afastam', texts[3])
        self.assertIn(enemy, game.rooms['demo_end'].enemies)
        self.assertTrue(game.hidden)
        self.assertEqual(game.health, 100)

    def test_poor_hiding_is_discovered(self):
        game = create_system_demo('patrol'); game.current_location = 'demo_hall'
        enemy = game.rooms['demo_end'].enemy; enemy.patrol_interval = 1
        parser = CommandParser(game)
        parser.execute('esconder atrás das caixas baixas')
        parser.execute('esperar')
        text = parser.execute('esperar')
        self.assertTrue(enemy.alert)
        self.assertFalse(game.hidden)

    def test_patrol_respects_closed_door_and_modal_queries(self):
        game = create_system_demo('patrol')
        enemy = game.rooms['demo_end'].enemy; enemy.patrol_interval = 1
        game.rooms['demo_hall'].objects['porta interna'].opened = False
        parser = CommandParser(game)
        before = game.exploration.export_state()
        parser.execute('inventário'); parser.execute('status'); parser.execute('ajuda')
        self.assertEqual(game.exploration.export_state(), before)
        parser.execute('esperar')
        self.assertIn(enemy, game.rooms['demo_end'].enemies)

    def test_light_sensitive_search_differs_from_insensitive(self):
        results = []
        for sensitive in (True, False):
            game = create_system_demo('patrol'); game.current_location = 'demo_hall'
            enemy = game.rooms['demo_end'].enemy; enemy.patrol_interval = 1; enemy.sensitive_to_light = sensitive
            lantern = GameObject('lanterna', '', portable=True); lantern.light_on = True
            game.add_item('lanterna'); game.item_objects['lanterna'] = lantern
            parser = CommandParser(game)
            parser.execute('esconder armário pesado'); parser.execute('esperar'); parser.execute('esperar')
            results.append(enemy.alert)
        self.assertEqual(results, [True, False])

    def test_flashlight_aliases_and_small_details(self):
        self.take('lanterna'); self.parser.execute('equipar lanterna'); self.parser.execute('ir norte')
        self.assertNotIn('anotação pequena', self.game.visible_objects())
        self.assertIn('armário pesado', self.game.visible_objects())
        self.parser.execute('acender lanterna')
        self.assertIn('anotação pequena', self.game.visible_objects())
        self.parser.execute('apagar lanterna')
        self.assertNotIn('anotação pequena', self.game.visible_objects())

    def test_uv_reveals_only_information(self):
        self.take('lanterna'); self.parser.execute('equipar lanterna'); self.parser.execute('ir norte')
        self.parser.execute('ligar lanterna')
        mechanism = GameObject('painel', '', locked=True, code='9999')
        self.game.get_current_room().add_object(mechanism)
        self.assertNotIn('marca oculta', self.game.visible_objects())
        self.parser.execute('mudar para uv')
        self.assertIn('marca oculta', self.game.visible_objects())
        self.assertIn('Observe antes', self.parser.execute('ler marca oculta'))
        self.assertTrue(mechanism.locked)

    def test_uv_unavailable_in_campaign(self):
        game = GameState(); game.current_location = 'T01'; parser = CommandParser(game)
        parser.execute('pegar lanterna'); parser.execute('equipar lanterna')
        self.assertIn('ainda não tem', parser.execute('ligar uv'))

    def test_runtime_state_roundtrip_focus_patrol_light(self):
        game = create_system_demo('patrol')
        game.focus_charges = 1; game.pending_startle = 1
        lantern = game.get_current_room().objects['lanterna']; lantern.light_on = True; lantern.light_mode = 'uv'
        saved = json.loads(json.dumps(game.exploration.export_state()))
        game.focus_charges = 0; game.pending_startle = 0; lantern.light_on = False
        game.exploration.advance()
        game.exploration.restore_state(saved)
        self.assertEqual(game.exploration.export_state(), saved)

    def test_invalid_runtime_version_rejected(self):
        before = self.game.snapshot()
        with self.assertRaises(ValueError):
            self.game.exploration.restore_state({'version': 99})
        self.assertEqual(self.game.snapshot(), before)

    def test_sound_sense_controls_patrol_diversion(self):
        destinations = []
        for hears in (True, False):
            game = create_system_demo('light')
            a, b, c = [game.rooms[name] for name in ('demo_foyer', 'demo_hall', 'demo_end')]
            for room in game.rooms.values():
                room.enemies.clear()
            a.add_exit('leste', c.room_id)
            game.current_location = c.room_id
            enemy = Enemy('criatura', hears=hears, patrol_route=[a.room_id,b.room_id], patrol_interval=1)
            a.enemy = enemy
            game.exploration.noise = 2
            game.exploration.advance()
            destinations.append(next(r.room_id for r in game.rooms.values() if enemy in r.enemies))
        self.assertEqual(destinations, ['demo_end', 'demo_hall'])

    def test_cautious_entry_preserves_stealth_without_light(self):
        self.game.rooms['demo_hall'].enemy = Enemy('criatura', surprise=0)
        self.parser.execute('passar pela porta furtivamente')
        self.assertTrue(self.game.hidden)
        self.assertFalse(self.game.get_current_room().enemy.alert)

    def test_hurried_entry_produces_more_noise(self):
        self.parser.execute('entrar apressado')
        self.assertEqual(self.game.current_location, 'demo_hall')
        self.assertEqual(self.game.exploration.noise, 2)

    def test_contextual_installation_needs_no_equipment(self):
        fuse = GameObject('fusível', '', portable=True, capabilities=ItemCapabilities(tool=True))
        panel = GameObject('painel', '', locked=True, required_item='fusível')
        self.game.get_current_room().add_object(fuse); self.game.get_current_room().add_object(panel)
        self.take('fusível')
        self.parser.execute('colocar fusível no painel')
        self.assertFalse(panel.locked)
        self.assertIsNone(self.game.equipped_item)

    def test_invalid_actor_identity_does_not_partially_restore(self):
        before = self.game.exploration.export_state()
        invalid = dict(before, focus_charges=2, patrols=[{'id':'missing','room':'demo_hall'}])
        with self.assertRaises(ValueError):
            self.game.exploration.restore_state(invalid)
        self.assertEqual(self.game.exploration.export_state(), before)


class SystemsInterfaceTests(unittest.TestCase):
    setUp = ui.VisualCommandTests.setUp
    tearDown = ui.VisualCommandTests.tearDown
    enter = ui.VisualCommandTests.enter

    def test_consumable_redirect_then_click_inventory_use(self):
        self.enter('pegar energético'); self.enter('usar energético')
        self.assertEqual(self.app.session.game.focus_charges, 0)
        self.enter('inventário')
        self.app.inventory_view.select(0)
        self.app.inventory_view.actions['usar'].invoke()
        self.app.root.update()
        self.assertEqual(self.app.session.game.focus_charges, 2)
        self.assertEqual(len(self.app.indicators.find_withtag('focus')), 2)
        self.app.inventory_view.close()
        self.assertFalse(self.app.session.parser.inventory_context)

    def test_focus_hud_loss_and_objective_no_confidence_percentage(self):
        self.app.start_system_demo('light')
        self.app.root.geometry('1100x760')
        self.app.root.update()
        footer = self.app.indicators
        self.assertLessEqual(footer.winfo_rooty()+footer.winfo_height(), self.app.root.winfo_rooty()+self.app.root.winfo_height())
        game = self.app.session.game
        for charges, expected in ((2,'⚡ ⚡'),(1,'⚡'),(0,'')):
            game.focus_charges = charges
            self.app.refresh()
            icons = self.app.indicators.find_withtag('focus')
            self.assertEqual(len(icons), 2)
            self.assertEqual([self.app.indicators.itemcget(i, 'fill') for i in icons],
                             ['#c8b58a'] * charges + ['#626a6d'] * (2-charges))
        self.assertTrue(self.app.objective_label.cget('text'))
        self.assertNotIn('Confiança', self.app.hud.get())

    def test_compact_layout_and_contextual_history(self):
        from test_visual_commands import all_widgets, tk
        self.app.root.geometry('1100x760')
        self.app.root.update()
        self.assertFalse(hasattr(self.app, 'environment'))
        self.assertFalse(hasattr(self.app, 'guide_label'))
        text = self.app.history_view.get('1.0', 'end')
        self.assertIn(self.app.session.game.get_current_room().description, text)
        self.assertNotIn('DICA:', text)
        self.assertFalse(self.app.history_view.tag_ranges('hint'))
        self.assertEqual(self.app.command_caption.cget('text'), 'Digite uma ação e pressione Enter.')
        self.assertNotIn('EVOLUCYS: THE ESTATE', [w.cget('text') for w in all_widgets(self.app.root) if isinstance(w, tk.Label)])
        self.assertGreater(self.app.objective_frame.winfo_rootx(), self.app.history_frame.winfo_rootx()+self.app.history_frame.winfo_width())
        self.assertTrue(self.app.objective_label.cget('text'))
        self.assertGreater(self.app.history_view.winfo_height(), 160)
        self.assertLess(self.app.history_view.winfo_height(), 210)
        self.assertLess(self.app.command_entry.winfo_height(), 40)
        self.assertLess(self.app.indicators.winfo_height(), 90)
        self.assertGreater(self.app.canvas.winfo_height(), 300)
        self.assertLess(self.app.canvas.winfo_height(), 420)
        self.assertGreater(self.app.command_entry.winfo_width()/self.app.root.winfo_width(), .43)
        self.assertLess(self.app.command_entry.winfo_width()/self.app.root.winfo_width(), .51)
        self.assertIn('4.5.5', self.app.root.title())
        canvas = self.app.indicators
        self.assertLess(canvas.bbox('hand_slot')[3], canvas.bbox('phone')[1])
        self.assertLess(canvas.bbox('focus')[3], canvas.bbox('vitals')[1])
        self.assertGreater(canvas.winfo_rootx()-self.app.root.winfo_rootx(), 700)
        from tkinter.font import Font
        for item in canvas.find_withtag('vitals'):
            self.assertGreaterEqual(Font(font=canvas.itemcget(item, 'font')).actual('size'), 11)
        labels = [w.cget('text') for w in all_widgets(self.app.root) if isinstance(w, tk.Label)]
        self.assertFalse(any('Luz apagada' in t or 'CAMPANHA' in t or 'MÃO: nada' in t for t in labels))
        before = self.app.session.game.turn_count
        self.app.refresh(); self.app.refresh()
        self.assertEqual(text, self.app.history_view.get('1.0', 'end'))
        self.assertEqual(before, self.app.session.game.turn_count)
        self.enter('ir norte')
        self.assertIn(self.app.session.game.get_current_room().description, self.app.history_view.get('1.0', 'end'))
        self.assertEqual(self.app.history_view.get('1.0', 'end').count('DICA:'), 0)
        self.app.pause(); self.app.build_game(); self.app.root.update()
        self.assertEqual(self.app.history_view.get('1.0', 'end').count('DICA:'), 0)

    def test_equipped_slot_updates_in_right_hud(self):
        self.enter('pegar pistola'); self.enter('equipar pistola')
        canvas = self.app.indicators
        self.assertEqual(canvas.itemcget(canvas.find_withtag('equipped')[0], 'text'), 'pistola • 2/12')
        self.enter('largar pistola')
        self.assertEqual(canvas.itemcget(canvas.find_withtag('equipped')[0], 'text'), 'Vazia')

    def test_light_filters_sprites_and_inventory_modal_stops_patrol(self):
        self.app.start_system_demo('light')
        self.enter('pegar lanterna'); self.enter('equipar lanterna'); self.enter('ir norte')
        game = self.app.session.game
        detail = game.get_current_room().objects['anotação pequena']
        self.assertFalse(self.app.canvas.find_withtag('object:' + detail.object_id))
        self.enter('acender lanterna')
        self.assertTrue(self.app.canvas.find_withtag('object:' + detail.object_id))
        self.enter('inventário')
        before = game.exploration.export_state()
        self.app.root.update()
        self.enter('esperar')
        self.assertEqual(game.exploration.export_state(), before)


if __name__ == '__main__':
    unittest.main()
