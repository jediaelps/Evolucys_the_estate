from world import create_world, ROOM_ALIASES
from items import fear_profile
from contextual_tutorial import TutorialGuide
from confidence import confidence


class GameState:
    def __init__(self, configuration='campaign'):
        self.player_name = "Joseph"
        self.health = 100
        self.max_health = 100
        self.fear = 0
        self.max_fear = 100

        self.inventory_limit = 6
        self.inventory = []
        self.item_objects = {}
        self.equipped_item = None

        self.phone_signal = False
        self.phone_vibrating = False

        self.configuration = configuration
        self.rooms = create_world(configuration)
        if configuration == 'campaign':
            lamp = self.rooms['entrance'].objects.pop('lanterna')
            self.add_item(lamp.name)
            self.item_objects[lamp.name] = lamp
        self.current_location = "E01" if configuration == "campaign" else "entrance"
        self.visited_rooms = {self.current_location}
        self.world_events = set()
        self.investigated = set()
        self.game_over = False
        self.turn_count = 0
        self.hidden = False
        self.buffs = {}
        self.events = []
        self.guide = TutorialGuide()
        self.focus_charges = 0
        self.pending_startle = 0
        self.confidence_settings = {}
        self.objective = ''
        from exploration_systems import ExplorationSystems
        self.exploration = ExplorationSystems(self)

    @property
    def well_lit(self):
        obj = self.item_objects.get('lanterna')
        return bool(obj and 'lanterna' in self.inventory and self.equipped_item == 'lanterna'
                    and obj.light_on and obj.light_mode == 'normal')

    @property
    def confidence(self):
        return confidence(self)

    def visible_objects(self, room=None):
        room = room or self.get_current_room()
        uv = any(o.light_on and o.light_mode == 'uv' for o in self.item_objects.values())
        return {name: obj for name, obj in room.objects.items()
                if not (obj.requires_light and room.dark and not self.light_visible)
                and not (obj.requires_uv and not uv)}

    def emit(self, name, **data):
        self.events.append({'name': name, **data})

    def drain_events(self):
        events, self.events = self.events, []
        return events

    def all_objects(self):
        pending = list(self.item_objects.values())
        for room in self.rooms.values():
            pending.extend(room.objects.values())
        seen = set()
        while pending:
            obj = pending.pop()
            if id(obj) in seen:
                continue
            seen.add(id(obj))
            yield obj
            pending.extend(obj.contents + obj.hidden_objects)

    @property
    def in_confrontation(self):
        return any(e.alive and e.alert for e in self.get_current_room().enemies)

    @property
    def light_visible(self):
        return any(obj.light_on for obj in self.item_objects.values()) or any(
            obj.light_on for obj in self.get_current_room().objects.values())

    def incoming_damage(self, amount):
        return max(0, amount)

    def end_turn(self):
        expired = []
        for name in list(self.buffs):
            self.buffs[name] -= 1
            if self.buffs[name] <= 0:
                del self.buffs[name]
                expired.append(name)
        return ''

    def snapshot(self):
        """Estado de leitura para HUDs, sem imprimir ou exigir uma câmera."""
        return {"health": self.health, "max_health": self.max_health,
                "fear": self.fear, "max_fear": self.max_fear,
                "fear_profile": fear_profile(self.fear), "inventory": list(self.inventory),
                "inventory_limit": self.inventory_limit, "equipped_item": self.equipped_item,
                "phone_signal": self.phone_signal, "phone_vibrating": self.phone_vibrating,
                "in_confrontation": self.in_confrontation, "hidden": self.hidden,
                "light_visible": self.light_visible, "buffs": dict(self.buffs),
                "turn_count": self.turn_count,
                "focus_charges": self.focus_charges, "objective": self.objective,
                "confidence": dict(self.confidence),
                "ammo_reserves": {name: obj.ammo_count for name, obj in self.item_objects.items()
                                  if obj.ammo_count > 0},
                "weapons": {name: {"ammo": obj.weapon.ammo, "capacity": obj.weapon.spec.capacity,
                                    "damage": obj.weapon.spec.damage, "ammo_item": obj.weapon.spec.ammo_item}
                            for name, obj in self.item_objects.items() if obj.weapon}}

    def resolve_room_id(self, room_id):
        """Resolve identidade, sem criar ambientes ou autorizar deslocamento."""
        official = ROOM_ALIASES.get(room_id, room_id.upper())
        legacy = next((old for old, new in ROOM_ALIASES.items() if new == official), None)
        matches = [key for key in dict.fromkeys((room_id, official, legacy)) if key in self.rooms]
        if len(matches) > 1:
            raise ValueError('Duplicate room identity: ' + room_id)
        if not matches:
            raise KeyError(room_id)
        return matches[0]

    def get_room(self, room_id):
        return self.rooms[self.resolve_room_id(room_id)]

    @property
    def current_location(self):
        return self._current_location

    @current_location.setter
    def current_location(self, room_id):
        self._current_location = self.resolve_room_id(room_id)

    def get_current_room(self):
        return self.get_room(self.current_location)

    def damage(self, amount):
        self.health -= max(0, amount)
        if self.health <= 0:
            self.health = 0
            self.game_over = True

    def heal(self, amount):
        if not self.game_over:
            self.health = min(self.health + max(0, amount), self.max_health)

    def increase_fear(self, amount):
        self.fear = min(self.fear + max(0, amount), self.max_fear)

    def reduce_fear(self, amount):
        self.fear = max(self.fear - max(0, amount), 0)

    def add_item(self, item):
        if item in self.inventory or len(self.inventory) >= self.inventory_limit:
            return False
        self.inventory.append(item)
        return True

    def equip_item(self, item):
        if item in self.inventory:
            self.equipped_item = item
            return True
        return False

    def remove_item(self, item):
        self.inventory.remove(item)
        if self.equipped_item == item:
            self.equipped_item = None
        return self.item_objects.pop(item, None)
