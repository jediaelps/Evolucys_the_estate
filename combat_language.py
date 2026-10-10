"""Intenções de combate e continuação curta, sem executar ações."""
import re
from command_language import fold, resolve, strip_article
from target_selection import candidates, clarification, arrange

ATTACKS = {'atacar': 'attack', 'bater': 'melee', 'golpear': 'melee', 'acertar': 'attack', 'atirar': 'shoot', 'disparar': 'shoot'}

def parse(game, command):
    words = command.split(' ', 1)
    verb, rest = words[0], words[1] if len(words)>1 else ''
    weapon = None
    if verb in ATTACKS:
        target, *specified = re.split(r'\s+com\s+', rest, maxsplit=1)
        if specified:
            weapon = resolve(game, specified[0])
        return {'mode': ATTACKS[verb], 'target': target, 'weapon': weapon}
    if verb in ('usar', 'utilizar'):
        parts = re.split(r'\s+(?:no|na|em|contra)\s+', rest, maxsplit=1)
        if len(parts)==2:
            weapon = resolve(game, parts[0])
            obj = game.item_objects.get(weapon)
            if (weapon in ('pistola', 'pé de cabra') or obj and obj.weapon) and candidates(game.get_current_room(), parts[1]):
                return {'mode': 'attack', 'target': parts[1], 'weapon': weapon}
    return None

class CombatContext:
    def __init__(self):
        self.pending = None

    def signature(self, game):
        arrange(game.get_current_room())
        return (game.current_location, game.turn_count, tuple((e.enemy_id, e.alive, e.distance, e.sprite.position) for e in game.get_current_room().enemies))

    def interpret(self, game, command):
        signature = self.signature(game)
        pending = self.pending
        self.pending = None
        continuation = re.match(r'^(?:o |a |da |do |mais |esquerda|direita|primeiro|segundo)', command)
        scope = None
        if pending and pending['signature'] == signature and continuation:
            intent = dict(pending['intent'], target=command)
            scope = pending['scope']
        else:
            intent = parse(game, command)
        if intent is None:
            return None, None, None
        pool = candidates(game.get_current_room(), intent['target'], scope)
        if len(pool)>1:
            self.pending = {'signature': signature, 'intent': intent, 'scope': [e.enemy_id for e in pool]}
            return intent, None, clarification(game.get_current_room(), pool)
        return intent, pool[0] if pool else None, None
