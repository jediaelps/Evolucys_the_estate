import unittest
from command_parser import CommandParser
from game_state import GameState
from world import Room, GameObject
from confrontation import Enemy
from items import WeaponState
from visual_session import VisualSession
from narrative import dialogue, history_text
import test_visual_commands as ui


def passage_game(two=False):
    game = GameState()
    start = Room('start', 'Entrada', 'A luz atravessa as frestas da madeira.')
    cellar = Room('cellar', 'Porão', 'O ar frio cheira a papel envelhecido.')
    laundry = Room('laundry', 'Lavanderia', 'Canos escuros cobrem a parede.')
    door = GameObject('porta do porão', 'Madeira gasta.', openable=True); door.opened = True
    start.add_exit('norte', 'cellar', door)
    cellar.add_exit('sul', 'start', door)
    if two:
        other = GameObject('porta da lavanderia', 'Uma porta estreita.', openable=True); other.opened = True
        start.add_exit('leste', 'laundry', other)
    game.rooms = {r.room_id: r for r in (start, cellar, laundry)}
    game.current_location = 'start'
    return game


class PassageTests(unittest.TestCase):
    def test_equivalent_destination_phrases(self):
        for phrase in ('passar pela porta do porão', 'seguir pela porta do porão', 'entrar pela porta do porão',
                       'ir pela porta do porão', 'atravessar a porta do porão', 'passar pelo porão', 'norte'):
            with self.subTest(phrase=phrase):
                game = passage_game(); parser = CommandParser(game)
                parser.execute(phrase)
                self.assertEqual(game.current_location, 'cellar')
                self.assertEqual(game.turn_count, 1)

    def test_caution_modifiers_preserve_rules(self):
        for phrase in ('esgueirar pela porta do porão', 'entrar devagar pela porta', 'passar com cuidado',
                       'atravessar sem fazer barulho', 'entrar furtivamente', 'passar silenciosamente'):
            with self.subTest(phrase=phrase):
                game = passage_game(); game.rooms['cellar'].enemy = Enemy('vigia')
                CommandParser(game).execute(phrase)
                self.assertTrue(game.hidden)
                self.assertFalse(game.rooms['cellar'].enemy.alert)
                self.assertEqual(game.current_location, 'cellar')

    def test_unique_door_and_ambiguous_continuation(self):
        for cautious in (False, True):
            game = passage_game(True); parser = CommandParser(game)
            self.assertIn('Qual', parser.execute('esgueirar pela porta' if cautious else 'passar pela porta'))
            self.assertEqual(game.current_location, 'start'); self.assertEqual(game.turn_count, 0)
            parser.execute('a do porão')
            self.assertEqual(game.current_location, 'cellar'); self.assertEqual(game.hidden, cautious)
            self.assertEqual(game.turn_count, 1)
        game = passage_game(); CommandParser(game).execute('passar pela porta')
        self.assertEqual(game.current_location, 'cellar')

    def test_pending_cannot_be_reused_after_other_action(self):
        game = passage_game(True); parser = CommandParser(game)
        parser.execute('passar pela porta'); parser.execute('esperar'); parser.execute('a do porão')
        self.assertEqual(game.current_location, 'start')

    def test_direction_answer_keeps_caution_and_help_keeps_pending(self):
        game = passage_game(True); parser = CommandParser(game)
        parser.execute('esgueirar pela porta'); parser.execute('ajuda'); parser.execute('norte')
        self.assertEqual(game.current_location, 'cellar'); self.assertTrue(game.hidden)

    def test_closed_door_still_blocks_and_consumes_attempt(self):
        game = passage_game(); game.get_current_room().exit_doors['norte'].opened = False
        self.assertIn('fechada', CommandParser(game).execute('seguir pela porta do porão'))
        self.assertEqual(game.current_location, 'start'); self.assertEqual(game.turn_count, 1)

    def test_named_open_passage_without_door(self):
        game = passage_game(); game.get_current_room().add_exit('leste', 'laundry', name='passagem para o corredor')
        CommandParser(game).execute('seguir pela passagem para o corredor')
        self.assertEqual(game.current_location, 'laundry')

    def test_key_missing_target_can_be_completed(self):
        game = passage_game(True); parser = CommandParser(game)
        key = GameObject('chave', 'Uma chave.', portable=True)
        game.add_item('chave'); game.item_objects['chave'] = key
        before = game.turn_count
        self.assertIn('Em quê?', parser.execute('usar chave'))
        self.assertEqual(game.turn_count, before)
        response = parser.execute('a do porão')
        self.assertNotIn('entender', response)
        self.assertEqual(game.turn_count, before+1)


class HelpTests(unittest.TestCase):
    def setUp(self):
        self.game = passage_game(); self.parser = CommandParser(self.game)
        self.safe = GameObject('cofre', 'Um cofre com teclado.', locked=True, code='1947')
        self.note = GameObject('bilhete', 'Um papel.', text='Cofre: 1947.')
        self.game.get_current_room().add_object(self.safe)
        self.game.get_current_room().add_object(self.note)

    def test_natural_requests_are_contextual_free_and_short(self):
        for phrase in ('ajuda', 'me ajuda', 'estou perdido', 'o que eu faço?', 'o que posso fazer?',
                       'o que posso fazer agora?', 'o que eu posso fazer agora?', 'o que devo fazer?', 'alguma ideia?', 'e agora?'):
            response = self.parser.execute(phrase)
            self.assertTrue(response.startswith('Joseph: “'))
            self.assertLess(len(response), 250)
            self.assertNotIn('1947', response)
        self.assertEqual(self.game.turn_count, 0)

    def test_progress_follows_reading_and_investigation_not_help_count(self):
        first = self.parser.execute('ajuda')
        for _ in range(6): self.assertEqual(self.parser.execute('ajuda'), first)
        self.parser.execute('ler bilhete')
        self.assertIn('Aquele número', self.parser.execute('ajuda'))
        self.parser.execute('examinar cofre')
        response = self.parser.execute('ajuda')
        self.assertIn('DIGITAR', response)
        self.assertNotIn('Digite o comando', response)
        self.assertTrue(self.safe.locked)
        self.parser.execute('digitar 1947 no cofre'); self.assertFalse(self.safe.locked)

    def test_hidden_or_unread_clues_and_dark_details_do_not_leak(self):
        self.game.get_current_room().objects.pop('bilhete')
        self.safe.contents.append(self.note)
        self.assertNotIn('1947', self.parser.execute('ajuda'))
        hidden = GameObject('marca secreta', 'O código é 7777.', requires_uv=True)
        self.game.get_current_room().add_object(hidden)
        self.assertNotIn('7777', self.parser.execute('ajuda marca secreta'))
        self.assertNotIn('1947', self.parser.execute('ajuda bilhete'))

    def test_failure_is_neutral_not_joseph_or_help_advertisement(self):
        response = self.parser.execute('blablabla impossível')
        self.assertEqual(response, 'Não foi possível entender essa ação.')
        self.assertEqual(history_text(response, self.game), response)

    def test_other_help_verbs_and_current_threat(self):
        self.assertIn('LER', self.parser.execute('ajuda bilhete'))
        self.game.get_current_room().enemies.append(Enemy('vigia'))
        self.assertIn('ESCONDER', self.parser.execute('ajuda'))
        self.game.get_current_room().enemy.alert = True
        self.assertIn('FUGIR', self.parser.execute('ajuda'))

    def test_help_remembers_evidence_without_remote_knowledge(self):
        self.game.get_current_room().objects.pop('cofre')
        enemy = Enemy('vigia', sound='passos'); self.game.rooms['cellar'].enemy = enemy
        self.assertNotIn('Lembro dos sinais', self.parser.execute('ajuda'))
        self.game.exploration.perception()
        remembered = self.parser.execute('ajuda')
        self.assertIn('Lembro dos sinais', remembered)
        enemy.sound = None
        self.assertEqual(remembered, self.parser.execute('ajuda'))
        self.assertNotIn('ainda ouço', remembered)
        self.game.exploration.listen('porta')
        self.assertIn('Lembro dos sinais', self.parser.execute('ajuda'))

    def test_examined_carried_note_can_support_reasonable_inference(self):
        note = GameObject('anotação', 'Quatro algarismos escritos à mão: 2468.', portable=True)
        self.game.add_item(note.name); self.game.item_objects[note.name] = note
        self.parser.execute('examinar cofre')
        self.assertNotIn('DIGITAR', self.parser.execute('ajuda'))
        self.parser.execute('examinar anotação')
        self.assertIn('DIGITAR', self.parser.execute('ajuda'))
        self.assertNotIn('2468', self.parser.execute('ajuda'))


class NarrationTests(unittest.TestCase):
    def test_damage_ammo_defeat_and_history(self):
        game = passage_game(); game.current_location = 'cellar'; enemy = Enemy('vigia', health=60)
        game.get_current_room().enemy = enemy
        gun = GameObject('pistola', '', portable=True, weapon=WeaponState())
        game.add_item('pistola'); game.item_objects['pistola'] = gun; game.equip_item('pistola')
        session = VisualSession(); session._attach(game, 'campaign')
        session.execute('atacar vigia')
        self.assertEqual(enemy.health, 25); self.assertEqual(gun.weapon.ammo, 1)
        self.assertIn('ferido', session.history[-1][1])
        self.assertNotRegex(session.history[-1][1], r'\d+ de dano|Resistência:|Vida:')
        session.execute('atacar vigia')
        self.assertEqual(enemy.health, 0); self.assertEqual(gun.weapon.ammo, 0)
        self.assertIn('cair imóvel', session.history[-1][1])
        self.assertNotIn('deixa de ser uma ameaça', session.history[-1][1])
        self.assertEqual(game.health, 100)

    def test_incoming_damage_still_exact(self):
        game = passage_game(); game.current_location = 'cellar'
        enemy = Enemy('vigia'); enemy.alert = enemy.preparing = True; game.get_current_room().enemy = enemy
        response = CommandParser(game).execute('esperar')
        self.assertEqual(game.health, 84); self.assertNotIn('16', response)

    def test_room_and_stealth_are_narrative_without_fields_or_menu(self):
        game = passage_game(); game.rooms['cellar'].enemy = Enemy('vigia')
        response = CommandParser(game).execute('esgueirar pela porta')
        self.assertIn(game.get_current_room().description, response)
        self.assertNotIn('\nPorão\n', '\n'+response+'\n')
        for phrase in ('Saídas:', 'Resistência:', 'É possível', 'esconder-se antes', 'continua sua ronda'):
            self.assertNotIn(phrase, response)
        self.assertTrue(game.hidden)
        self.assertEqual(dialogue('Criatura', 'grunhe', True), 'Criatura: *grunhe*')


class HelpInterfaceTests(unittest.TestCase):
    setUp = ui.VisualCommandTests.setUp
    tearDown = ui.VisualCommandTests.tearDown
    enter = ui.VisualCommandTests.enter

    def test_digitar_highlights_only_verb_after_discovery(self):
        game = self.app.session.game
        room = game.get_current_room()
        room.enemies.clear()
        safe = GameObject('cofre', 'Um cofre com teclado.', locked=True, code='1947')
        note = GameObject('bilhete do cofre', 'Um papel.', text='Cofre: 1947.')
        room.add_object(safe); room.add_object(note)
        self.enter('ler bilhete do cofre'); self.enter('fechar leitura'); self.enter('examinar cofre')
        self.app.reader_panel.back.invoke()
        self.enter('ajuda')
        view = self.app.history_view
        ranges = view.tag_ranges('action_verb')
        self.assertEqual([view.get(a,b) for a,b in zip(ranges[::2], ranges[1::2])], ['DIGITAR', 'NORTE'])
        text = view.get('1.0','end')
        self.assertIn('Joseph: “Talvez eu possa DIGITAR', text)
        self.assertNotIn('1947', text)
        self.assertNotIn('Joseph: “DICA:', text)
        last = view.dlineinfo('end-1c')
        self.assertLessEqual(abs(view.winfo_height()-last[1]-last[3]), 5)

    def test_only_action_verb_is_highlighted_and_layout_kept(self):
        self.app.root.geometry('1100x760'); self.app.root.update()
        before = [(w.winfo_x(), w.winfo_y(), w.winfo_width(), w.winfo_height()) for w in
                  (self.app.canvas, self.app.history_frame, self.app.command_entry, self.app.indicators)]
        self.enter('o que eu faço?')
        view = self.app.history_view
        ranges = view.tag_ranges('action_verb')
        self.assertTrue(ranges)
        for start,end in zip(ranges[::2],ranges[1::2]):
            self.assertIn(view.get(start,end), ('EXAMINAR','LER','OUVIR','ESCONDER','FUGIR','INVENTÁRIO','NORTE','SUL','LESTE','OESTE','SUBIR','DESCER'))
        self.assertIsNone(self.app.reader_window)
        self.assertEqual(before, [(w.winfo_x(), w.winfo_y(), w.winfo_width(), w.winfo_height()) for w in
                         (self.app.canvas, self.app.history_frame, self.app.command_entry, self.app.indicators)])
        self.assertIn('4.5.5', self.app.root.title())


if __name__ == '__main__': unittest.main()

