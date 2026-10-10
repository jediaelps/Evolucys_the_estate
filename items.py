"""Definições ajustáveis e estado individual dos itens, sem dependência de UI."""
from dataclasses import dataclass
from typing import Optional


HEALING = {"bandagem": 20, "spray de cura": 50, "kit médico": 100}
TEA_RELIEF = 30
FOCUS_CHARGES = 2


@dataclass(frozen=True)
class ItemCapabilities:
    personal: bool = False
    melee_damage: int = 0
    confidence: int = 0
    equipable: bool = True
    tool: bool = False


def capabilities_for(name, weapon=None):
    if name in HEALING or name in ('chá', 'energético'):
        return ItemCapabilities(personal=True)
    if name == 'pé de cabra':
        return ItemCapabilities(melee_damage=25, confidence=25, tool=True)
    return ItemCapabilities(confidence=58 if weapon else 0)
HIGH_FEAR = 70
FEAR_GUN_PENALTY = 5


@dataclass(frozen=True)
class WeaponSpec:
    capacity: int = 12
    damage: int = 35
    ammo_item: str = "munição de pistola"
    initial_ammo: int = 2


PISTOL = WeaponSpec()


@dataclass
class WeaponState:
    spec: WeaponSpec = PISTOL
    ammo: Optional[int] = None

    def __post_init__(self):
        if self.ammo is None:
            self.ammo = self.spec.initial_ammo

    def reload(self, available):
        loaded = min(max(0, available), self.spec.capacity - self.ammo)
        self.ammo += loaded
        return loaded


def fear_profile(value):
    """Sinais para futuros HUD, áudio e animações; nenhum efeito gráfico aqui."""
    level = "alto" if value >= HIGH_FEAR else "moderado" if value >= 30 else "baixo"
    return {"level": level, "intensity": value / 100,
            "breathing": "ofegante" if level == "alto" else "regular",
            "heartbeat": "acelerado" if level != "baixo" else "regular",
            "perception": "tensa" if level == "alto" else "atenta",
            "ranged_damage_penalty": FEAR_GUN_PENALTY if value >= HIGH_FEAR else 0}


# Fase 5.1G: valores provisórios; não adicionam itens ao mundo.
@dataclass(frozen=True)
class DefenseProfile:
    reduction: float
    perfect: float

DEFENSE_PROFILES = {
    'bastão de beisebol': DefenseProfile(.50, .25),
    'pé de cabra': DefenseProfile(.30, .15),
}
UNARMED_DEFENSE = DefenseProfile(.15, .05)
DODGE_CHANCE = .30
FLEE_CHANCE = .75
FEAR_AVOIDANCE_PENALTY = .20
STANCE_REACTIONS = 3


def avoidance_chance(base, fear):
    return max(0., min(1., base * (1 - FEAR_AVOIDANCE_PENALTY * max(0, min(100, fear)) / 100)))


def defense_profile(item):
    # Armas de fogo/ferramentas sem perfil deixam Joseph aparar com o corpo.
    if item is None or item.weapon:
        return UNARMED_DEFENSE
    return DEFENSE_PROFILES.get(item.name, UNARMED_DEFENSE)
