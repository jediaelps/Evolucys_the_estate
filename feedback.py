"""Pensamentos reutilizáveis no terminal e em uma futura interface."""
NOT_OWNED = "Não tenho isso comigo."
NO_HEAL_NEEDED = "Não preciso disso agora."
EQUIP_FIRST = "Preciso colocar isso na mão primeiro."
EMPTY_WEAPON = "Droga... está vazia."
LOCKED = "Está trancada. Preciso encontrar outra maneira."
FULL = "Meus bolsos estão cheios. Não consigo carregar mais nada."
UNKNOWN = "Não foi possível entender essa ação."


def missing_item(game, name):
    obj = game.get_current_room().objects.get(name)
    if obj and obj.portable:
        return f"Melhor eu pegar {name} primeiro."
    return NOT_OWNED
