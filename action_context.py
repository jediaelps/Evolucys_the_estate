"""Complementos de intenção locais; não executa ações nem avança turnos."""
import re
from command_language import fold
from narrative import dialogue


HELP_REQUESTS = {'ajuda', 'me ajuda', 'estou perdido', 'o que eu faco', 'o que posso fazer',
                 'o que posso fazer agora', 'o que eu posso fazer agora', 'o que devo fazer',
                 'alguma ideia', 'e agora'}


def words(text):
    return [w for w in fold(text.lower()).split() if w not in
            {'a', 'o', 'as', 'os', 'ao', 'do', 'da', 'dos', 'das', 'de', 'para', 'pelo', 'pela', 'em', 'no', 'na', 'por'}]


class ActionContext:
    def __init__(self):
        self.pending = None

    def signature(self, game):
        room = game.get_current_room()
        return (room.room_id, game.turn_count, tuple(room.exits.items()),
                tuple((d, o.object_id, o.accessible) for d, o in room.exit_doors.items()),
                tuple((d, s.known, s.enabled, s.kind) for d, s in room.exit_states.items()), tuple(game.inventory))

    def passages(self, game, target):
        room = game.get_current_room()
        wanted = words(target)
        candidates = []
        for direction, destination in room.known_exits().items():
            try:
                game.get_room(destination)
            except KeyError:
                continue
            door = room.exit_doors.get(direction)
            if door and not door.accessible:
                continue
            # Um destino remoto só é resolvido por seu nome se já visitado;
            # nomes explícitos de portas locais são sempre utilizáveis.
            names = [direction, room.exit_names.get(direction, 'passagem')]
            if door:
                names.append(door.name)
            if game.resolve_room_id(destination) in game.visited_rooms:
                names.append(game.get_room(destination).name)
            available = words(' '.join(names))
            generic = not wanted or wanted in (['porta'], ['passagem'])
            if generic:
                matches = wanted != ['porta'] or ('porta' in words(' '.join(names)))
            else:
                significant = [w for w in wanted if w not in ('porta', 'passagem')]
                matches = bool(significant) and all(w in available for w in significant)
            if matches:
                candidates.append(direction)
        return candidates

    def interpret(self, game, raw):
        text = ' '.join(raw.lower().strip().rstrip('?! .').split())
        if fold(text) in HELP_REQUESTS:
            return 'ajuda', None
        relative = re.fullmatch(r'(?:(?:ir|andar|seguir|fugir|entrar)\s+)?(?:(?:para|à|a|pela|em)\s+)?(?:a\s+)?(esquerda|direita|frente|trás|tras)', text)
        if relative:
            choices = self.passages(game, relative[1])
            if choices:
                return self.complete(game, 'fugir' if text.startswith('fugir') else 'ir', choices, relative[1])
            return None, dialogue('Joseph', 'Em qual direção ou por qual passagem? Não tenho uma referência clara para esse lado.')
        if text in game.get_current_room().known_exits():
            action = (self.pending['action'] if self.pending and self.pending['action'] != 'usar'
                      and self.pending['signature'] == self.signature(game) else 'ir')
            self.pending = None
            return action + ' ' + text, None
        if self.pending and self.pending['signature'] != self.signature(game):
            self.pending = None
        movement = re.match(r'^(?:me )?(ir|andar|seguir|entrar|passar|atravessar|fugir|esgueirar|avançar|subir|descer|voltar)\b\s*(.*)', text)
        if movement:
            self.pending = None
            verb, target = movement.groups()
            cautious = verb == 'esgueirar' or bool(re.search(r'devagar|furtivamente|com cuidado|sem fazer barulho|silenciosamente', target))
            target = re.sub(r'devagar|furtivamente|com cuidado|sem fazer barulho|silenciosamente', '', target).strip()
            choices = self.passages(game, target)
            if verb in ('subir', 'descer'):
                expected = 'cima' if verb == 'subir' else 'baixo'
                choices = [d for d in choices if d == expected]
            # Preserve os aliases anteriores (escadas, destinos etc.) se não
            # houver passagem local compatível.
            if not choices:
                if verb == 'voltar' and fold(text) != 'voltar ao salao':
                    return 'ir ' + target, None
                return None, None
            return self.complete(game, 'fugir' if verb == 'fugir' else 'esgueirar' if cautious else 'ir', choices, target)
        if self.pending and text.startswith(('a ', 'o ', 'porta ', 'passagem ', 'no ', 'na ')):
            pending = self.pending
            if pending['action'] == 'usar':
                targets = [name for name in pending['choices'] if all(w in words(name) for w in words(text))]
                if len(targets) == 1:
                    self.pending = None
                    return f"usar {pending['item']} no {targets[0]}", None
                return None, dialogue('Joseph', 'Em quê?')
            choices = [d for d in self.passages(game, text) if d in pending['choices']]
            if len(choices) == 1:
                self.pending = None
                return pending['action'] + ' ' + choices[0], None
            return None, dialogue('Joseph', 'Qual passagem?')
        use = re.fullmatch(r'(?:usar|utilizar)\s+(?:a\s+)?(.+)', text)
        if use and not re.search(r'\s(?:no|na|em)\s', use[1]):
            items = [name for name in game.inventory if all(w in words(name) for w in words(use[1]))]
            if len(items) == 1 and 'chave' in items[0]:
                targets = [o.name for o in game.visible_objects().values() if o.openable and o.accessible]
                if len(targets) == 1:
                    return f'usar {items[0]} no {targets[0]}', None
                self.pending = dict(action='usar', item=items[0], choices=targets, signature=self.signature(game))
                return None, dialogue('Joseph', 'Em quê?')
        if text and not text.startswith('ajuda'):
            self.pending = None
        return None, None

    def complete(self, game, action, choices, target):
        if len(choices) == 1:
            return action + ' ' + choices[0], None
        self.pending = dict(action=action, choices=choices, signature=self.signature(game))
        question = ('Qual porta?' if action == 'esgueirar' else
                    'Qual delas? Tem mais de uma porta aqui.' if words(target) == ['porta'] else
                    'Qual delas? Há mais de uma passagem aqui.')
        return None, dialogue('Joseph', question)
