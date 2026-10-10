"""Adaptador sem renderização: a interface usa o mesmo parser do terminal."""
from game_state import GameState
from command_parser import CommandParser
from tutorial import TutorialState
from collections import deque
from narrative import history_text


class VisualSession:
    def __init__(self):
        self.campaign = None
        self.game = None
        self.parser = None
        self.selected_object = None
        self.selected_item = None
        self.mode = 'menu'
        self.last_message = ''
        self.history = deque(maxlen=4)
        self.history_hints = deque(maxlen=4)
        self.initial_environment = ''
        self.initial_hint = ''
        self.inventory_open = False
        self.reading_text = None
        self.reading_document = None
        self.reading_page = 0
        self.inspection_object = None
        self.inspection_face = None
        self.environment_text = ''

    @property
    def can_continue(self):
        # Não há formato validado/carregador de save nesta fase.
        return False

    def start_campaign(self, configuration='campaign'):
        self.campaign = GameState(configuration=configuration)
        self._attach(self.campaign, 'campaign')

    def start_tutorial(self, scenario):
        self._attach(TutorialState(scenario), 'tutorial')

    def _attach(self, game, mode):
        self.game, self.mode = game, mode
        self.parser = CommandParser(game)
        self.selected_object = self.selected_item = None
        self.last_message = game.get_current_room().description
        self.history.clear()
        self.history_hints.clear()
        self.environment_text = game.get_current_room().describe(game)
        self.inspection_object = None
        self.inspection_face = None
        self.inventory_open = False
        self.reading_text = None
        self.reading_document = None
        self.reading_page = 0
        self.initial_environment = self.environment_text
        self.initial_hint = game.guide.update(game)

    def leave(self):
        self.game = self.parser = None
        self.selected_object = self.selected_item = None
        self.mode = 'menu'
        self.last_message = ''
        self.history.clear()
        self.history_hints.clear()
        self.inventory_open = False
        self.reading_text = None
        self.reading_document = None
        self.inspection_object = None
        self.inspection_face = None

    def reset(self):
        if self.mode == 'tutorial':
            self.start_tutorial(self.game.scenario)
            return True
        return False

    def execute(self, command):
        if self.parser is None or not command.strip():
            return ''
        self.parser.inventory_context = self.inventory_open
        self.last_message = self.parser.execute(command)
        response = self.last_message
        if isinstance(self.game, TutorialState) and self.game.safety_notice:
            self.last_message += '\n' + self.game.safety_notice
            self.game.safety_notice = ''
        if self.selected_object not in self.game.get_current_room().objects:
            enemy = self.game.get_current_room().enemy
            if not enemy or self.selected_object != enemy.name:
                self.selected_object = None
        if self.selected_item not in self.game.inventory:
            self.selected_item = None
        presentation = self.parser.presentation
        if self.parser.read_document is not None:
            brief = 'Tem alguma coisa escrita aqui.'
            self.last_message = '\n'.join(t for t in (brief, self.parser.reaction) if t)
        elif presentation == 'inspection':
            self.last_message = '\n'.join(t for t in ('Vou olhar mais de perto.', self.parser.reaction) if t)
        elif presentation == 'inventory':
            self.last_message = 'Inventário aberto.'
        self.history.append((command.strip(), history_text(self.last_message, self.game)))
        self.environment_text = self.game.get_current_room().describe(self.game)
        if presentation in ('inventory', 'close_inventory'):
            previous = self.inventory_open
            self.inventory_open = presentation == 'inventory'
            if previous != self.inventory_open:
                self.game.emit('inventory_open' if self.inventory_open else 'inventory_close')
        if presentation == 'inspection':
            self.inspection_object = self.parser.inspection_object
            self.inspection_face = self.parser.inspection_face
            self.reading_document = None
            self.reading_page = 0
            self.reading_text = (self.inspection_object.inspection_faces[self.inspection_face]
                                 if self.inspection_face is not None else self.parser.inspection_text)
        elif presentation == 'reading' or (presentation != 'environment' and len(self.last_message) > 500):
            self.inspection_object = None
            self.inspection_face = None
            self.reading_text = (self.parser.read_document.pages[0] if self.parser.read_document else self.last_message)
            self.reading_document = self.parser.read_document
            self.reading_page = 0
        elif presentation == 'close_reading':
            if self.reading_text is not None:
                self.game.emit('document_close')
            self.reading_text = None
            self.reading_document = None
            self.inspection_object = None
            self.inspection_face = None
        self.history_hints.append(self.game.guide.update(self.game, presentation))
        return response if self.parser.read_document or presentation == 'inspection' else self.last_message

    def finish_delayed_response(self):
        response = self.parser.finish_delayed_response()
        if response:
            self.last_message += '\n' + response
            if self.history:
                command, _ = self.history[-1]
                self.history[-1] = (command, history_text(self.last_message, self.game))
        return response

    def turn_page(self, step):
        document = self.reading_document
        if document is None:
            return
        page = self.reading_page + step
        if 0 <= page < len(document.pages):
            self.reading_page = page
            self.reading_text = document.read_page(page)
            self.game.emit('document_page', object_id=document.object_id, page=page)

    def object_action(self, action, code=''):
        target = self.selected_object
        if not target:
            return 'Selecione um objeto no ambiente.'
        if action == 'usar equipado':
            item = self.game.equipped_item
            if not item:
                return 'Preciso ter um item na mão primeiro.'
            return self.execute(f'usar {item} no {target}')
        if action == 'código':
            return self.execute(f'digitar {code} no {target}')
        return self.execute(f'{action} {target}')

    def inventory_action(self, action):
        if not self.selected_item:
            return 'Selecione um dos seis espaços do inventário.'
        return self.execute(f'{action} {self.selected_item}')

    def debug(self, action):
        if self.mode != 'tutorial' or not isinstance(self.game, TutorialState):
            return 'Controles de teste indisponíveis na campanha.'
        self.last_message = self.game.debug(action)
        self.history.append((f'[TESTE] {action}', self.last_message))
        self.history_hints.append('')
        return self.last_message

    def slots(self):
        if not self.game:
            return [None] * 6
        return list(self.game.inventory) + [None] * (self.game.inventory_limit - len(self.game.inventory))
