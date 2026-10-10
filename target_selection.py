"""Referências humanas sobre a mesma geometria usada pelos sprites."""
import re
import unicodedata

def plain(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text.lower()) if unicodedata.category(c) != 'Mn')

def ordered(room):
    arrange(room)
    return sorted((e for e in room.enemies if e.alive and e.sprite.visible), key=lambda e: e.sprite.position[0])

def arrange(room):
    enemies = room.enemies
    if len(enemies)>1 and len({e.sprite.position[0] for e in enemies}) < len(enemies):
        for index, enemy in enumerate(enemies):
            enemy.sprite.position = ((index+1)/(len(enemies)+1), enemy.sprite.position[1])

def pose(enemy):
    y, scale = {'próximo': (.56, 3), 'médio': (.44, 2), 'distante': (.32, 1)}[enemy.distance]
    return (enemy.sprite.position[0], y), scale

def label(room, enemy):
    peers = [e for e in ordered(room) if e.name == enemy.name]
    if len(peers) < 2 or enemy not in peers:
        return enemy.name
    index = peers.index(enemy)
    position = 'da esquerda' if index == 0 else 'da direita' if index == len(peers)-1 else 'do centro' if len(peers) == 3 else f'na posição {index+1}'
    return enemy.name + ' ' + position

def candidates(room, reference, scope=None):
    text = plain(reference)
    pool = ordered(room)
    if scope is not None:
        pool = [e for e in pool if e.enemy_id in scope]
    names = [e for e in pool if plain(e.name) in text]
    if names:
        pool = names
    elif text and not re.search(r'esquerda|direita|centro|proximo|distante|primeiro|segundo', text):
        traits = [e for e in pool if e.trait and plain(e.trait) in text]
        return traits
    if not pool:
        return []
    if 'esquerda' in text or 'primeiro' in text:
        return pool[:1]
    if 'direita' in text:
        return pool[-1:]
    if 'segundo' in text:
        return pool[1:2]
    if 'centro' in text:
        center = min(abs(e.sprite.position[0]-.5) for e in pool)
        return [e for e in pool if abs(e.sprite.position[0]-.5) == center]
    if 'proximo' in text or 'distante' in text:
        ranks = {'próximo': 0, 'médio': 1, 'distante': 2}
        rank = (min if 'proximo' in text else max)(ranks[e.distance] for e in pool)
        return [e for e in pool if ranks[e.distance] == rank]
    traits = [e for e in pool if e.trait and plain(e.trait) in text]
    return traits or pool

def clarification(room, pool):
    return 'Qual deles? ' + ' ou '.join('O ' + label(room, e) for e in pool) + '?'
