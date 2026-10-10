"""Uso de recursos e efeitos temporários; resolução de turnos fica no parser."""
import feedback
from items import HEALING, TEA_RELIEF, FOCUS_CHARGES


class Survival:
    def __init__(self, game):
        self.game = game

    def use(self, name, from_inventory=False):
        game = self.game
        if name not in game.inventory:
            return feedback.missing_item(game, name)
        obj = game.item_objects.get(name)
        if obj and obj.capabilities.personal and not from_inventory:
            return 'Melhor eu olhar isso no inventário.'
        if name in HEALING:
            if game.health >= game.max_health:
                return feedback.NO_HEAL_NEEDED
            before = game.health
            game.heal(HEALING[name])
            game.remove_item(name)
            return f"Assim está melhor. Uso {name} e recupero {game.health - before} de vida."
        if name == "chá":
            game.reduce_fear(TEA_RELIEF)
            game.remove_item(name)
            return "Esse chá... conheço esse cheiro. Consigo me acalmar um pouco."
        if name == "energético":
            if game.focus_charges:
                return "Ainda sinto o efeito. Melhor guardar isso para depois."
            game.focus_charges = FOCUS_CHARGES
            game.remove_item(name)
            return "Bebo o energético. Consigo prestar mais atenção ao que acontece ao redor."
        if name == "lanterna":
            return self.light()
        obj = game.item_objects.get(name)
        if obj and obj.weapon:
            if game.equipped_item != name:
                return feedback.EQUIP_FIRST
            if obj.weapon.ammo == 0:
                return feedback.EMPTY_WEAPON
            return "Melhor escolher um alvo. Use atacar durante um confronto."
        if obj and obj.ammo_count:
            return "Preciso de uma arma na mão. Use recarregar para aproveitar esses cartuchos."
        return "Não vejo como isso pode me ajudar agora."

    def light(self, on=None):
        game = self.game
        if "lanterna" not in game.inventory:
            return feedback.missing_item(game, "lanterna")
        if game.equipped_item != "lanterna":
            return "Preciso colocar a lanterna na mão primeiro."
        obj = game.item_objects.get("lanterna")
        if obj is None:
            return "Não consigo ligar esta lanterna."
        obj.light_on = not obj.light_on if on is None else on
        return "Ligo a lanterna. Essa luz também pode me denunciar." if obj.light_on else "Desligo a lanterna."

    def light_mode(self, mode):
        obj = self.game.item_objects.get('lanterna')
        if not obj or self.game.equipped_item != 'lanterna':
            return 'Preciso ter a lanterna na mão primeiro.'
        if mode == 'uv' and not obj.uv_enabled:
            return 'Minha lanterna ainda não tem esse recurso.'
        obj.light_mode = mode
        obj.light_on = True
        return 'Acendo a luz ultravioleta.' if mode == 'uv' else 'Volto à luz normal.'

    def reload(self, name=""):
        game = self.game
        name = name or game.equipped_item
        if name not in game.inventory:
            return feedback.missing_item(game, name)
        if name != game.equipped_item:
            return feedback.EQUIP_FIRST
        obj = game.item_objects.get(name)
        if obj is None or obj.weapon is None:
            return "Preciso ter uma arma na mão para recarregar."
        weapon = obj.weapon
        if weapon.ammo >= weapon.spec.capacity:
            return "Já está carregada. Vou guardar os cartuchos."
        ammo = game.item_objects.get(weapon.spec.ammo_item)
        if ammo is None or ammo.ammo_count <= 0:
            return "Não tenho cartuchos de reserva."
        loaded = weapon.reload(ammo.ammo_count)
        ammo.ammo_count -= loaded
        if ammo.ammo_count == 0:
            game.remove_item(ammo.name)
        return f"Recarrego {loaded} cartuchos. Agora tenho {weapon.ammo}/{weapon.spec.capacity}."
