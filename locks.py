"""Utilidade das chaves por IDs de fechaduras; IDs futuros não consomem chaves."""
from narrative import dialogue


def matches(key, lock):
    if key.key_lock_ids:
        return lock.lock_id is not None and lock.lock_id in key.key_lock_ids
    return key.name == lock.required_item


def find_key(game, lock):
    return next((obj for obj in game.item_objects.values() if obj.name in game.inventory and matches(obj, lock)), None)


def unlock(game, key, lock, opening=False):
    if not lock.locked or lock.blocked or not lock.accessible or not matches(key, lock):
        return ''
    lock.locked = False
    is_key = bool(key.key_lock_ids or key.name.startswith('chave'))
    if is_key:
        game.emit('key_use', object_id=key.object_id, lock_id=lock.lock_id)
    game.emit('lock_unlock', lock_id=lock.lock_id)
    message = dialogue('Joseph', 'A chave encaixou perfeitamente... pronto.') if is_key else ''
    if not opening:
        message = '\n'.join(t for t in (message, 'O mecanismo destrava, mas a abertura ainda precisa ser feita.' if not lock.opened
                                       else 'O mecanismo destrava.') if t)
    if key.permanent_key or not key.key_lock_ids:
        return message
    # Qualquer ID ausente ou ainda trancado representa utilidade futura.
    locks = {}
    for obj in game.all_objects():
        if obj.lock_id:
            locks.setdefault(obj.lock_id, []).append(obj)
    spent = all(lock_id in locks and all(not obj.locked for obj in locks[lock_id])
                for lock_id in key.key_lock_ids)
    if spent and key.name in game.inventory:
        game.remove_item(key.name)
        message = '\n'.join(t for t in (message, dialogue('Joseph', 'Não vou precisar mais dessa chave.')) if t)
    return message
