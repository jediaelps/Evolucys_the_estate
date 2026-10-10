"""Preparação percebida, independente do dano da arma e da pressão psicológica."""
DEFAULTS = {'unarmed': 12, 'unknown_penalty': 18, 'extra_enemy_penalty': 10,
            'injury_penalty': 15, 'empty_penalty': 35, 'surprise_penalty': 15}

def confidence(game):
    settings = dict(DEFAULTS, **game.confidence_settings)
    item = game.item_objects.get(game.equipped_item)
    value = item.capabilities.confidence if item and (item.weapon or item.capabilities.melee_damage) else settings['unarmed']
    if item and item.weapon and item.weapon.ammo == 0:
        value -= settings['empty_penalty']
    enemies = [e for e in game.get_current_room().enemies if e.alive]
    value -= max(0, len(enemies)-1) * settings['extra_enemy_penalty']
    if any(e.unknown for e in enemies):
        value -= settings['unknown_penalty']
    value -= max((e.threat for e in enemies), default=0)
    if game.health < 40:
        value -= settings['injury_penalty']
    if game.pending_startle:
        value -= settings['surprise_penalty']
    value = max(0, min(100, value))
    return {'value': value, 'thought': ('Preciso manter a calma e procurar uma saída.' if value < 25 else
                                     'Talvez eu consiga lidar com isso, se tomar cuidado.' if value < 60 else
                                     'Estou preparado, mas não posso baixar a guarda.')}
