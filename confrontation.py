"""Encontros no próprio cômodo; uma reação por ação, sem laço de batalha."""
import feedback
import random
from math import ceil
from narrative import dialogue
from items import defense_profile, avoidance_chance, DODGE_CHANCE, FLEE_CHANCE, STANCE_REACTIONS
from items import fear_profile
from visual_assets import SpriteSpec
from uuid import uuid4
from target_selection import label


class Enemy:
    def __init__(self, name, health=60, damage=16, sensitive_to_light=True, sprite=None, distance='próximo', trait='',
                 hears=True, proximity=True, sound='passos', surprise=0, unknown=False, threat=0,
                 patrol_route=None, patrol_interval=2, detection=60, sound_intensity=3, in_sight=True):
        self.name = name
        self.enemy_id = uuid4().hex
        self.distance = distance
        self.trait = trait
        self.hears = hears
        self.proximity = proximity
        self.sound = sound
        self.sound_intensity = max(0, sound_intensity)
        self.in_sight = in_sight
        self.surprise = surprise
        self.unknown = unknown
        self.threat = threat
        self.patrol_route = list(patrol_route or [])
        self.patrol_interval = max(1, patrol_interval)
        self.patrol_clock = 0
        self.patrol_phase = 'travel'
        self.detection = detection
        self.health = health
        self.initial_health = health
        self.reported_condition = None
        self.damage = damage
        self.alert = False
        self.preparing = False
        self.distracted = False
        self.flash_used = False
        self.sensitive_to_light = sensitive_to_light
        self.sprite = sprite or SpriteSpec(object_id=uuid4().hex, position=(.64, .44), layer=30)
        self.sprite.object_id = self.enemy_id
        if sprite is None:
            self.sprite.images = {state: f'enemies/vigia_{state}.png' for state in ('idle', 'alert', 'preparing', 'distracted', 'fallen')}

    @property
    def alive(self):
        return self.health > 0

    def describe(self, display_name=None):
        name = display_name or self.name
        if not self.alive:
            return f"{name.capitalize()} está caído, sem reagir."
        if not self.alert:
            return f"{name.capitalize()} está de costas, caminhando lentamente. Até agora, não parece ter percebido Joseph."
        intent = "prepara um golpe" if self.preparing else "observa Joseph, pronto para avançar"
        return f"{name.capitalize()} {intent}. {self.condition()}"

    def condition(self):
        ratio = self.health / max(1, self.initial_health)
        return ('Parece ileso.' if ratio >= 1 else 'Está abalado.' if ratio > .7 else
                'Parece ferido.' if ratio > .4 else 'Cambaleia, gravemente ferido.' if ratio > .15 else
                'Mal consegue se manter em pé.')


class Confrontation:
    def __init__(self, game, rng=None):
        self.roll = rng or random.random
        self.dodging = False
        self.stance_expires = 0
        self.game = game
        self.guarding = False
        self.selected = None
        self.attack_weapon = None
        self.attack_mode = None
        self.reaction_index = 0

    def enemy(self):
        enemy = self.game.get_current_room().enemy
        return enemy if enemy and enemy.alive else None

    def act(self, action, target):
        enemy = self.selected if self.selected and self.selected.alive else self.enemy()
        if action == "esperar":
            return "Joseph espera, atento aos ruídos."
        if enemy is None:
            return "Não há ameaça ativa neste cômodo."
        if target and target != enemy.name and self.selected is None:
            return f"Joseph não encontra {target} como ameaça aqui."
        creature = label(self.game.get_current_room(), enemy)
        if action == "esconder":
            if enemy.alert:
                return f"O {creature} já acompanha cada movimento de Joseph."
            self.game.hidden = True
            return f"Joseph se oculta atrás das estantes, fora da vista do {creature}."
        if action in ('defender', 'esquivar'):
            self.guarding = action == 'defender'
            self.dodging = action == 'esquivar'
            self.stance_expires = self.game.turn_count + STANCE_REACTIONS
            return ('Joseph protege o corpo, preparando-se para amortecer o próximo golpe.' if self.guarding
                    else 'Joseph se prepara para desviar do próximo golpe.')
        if action == "distrair":
            if self.game.equipped_item != "lanterna" or "lanterna" not in self.game.inventory:
                return f"Equipe a lanterna para tentar ofuscar o {creature}."
            if enemy.flash_used:
                return f"O {creature} protege os olhos: a mesma distração não funciona novamente."
            enemy.flash_used = True
            lantern = self.game.item_objects.get("lanterna")
            if lantern:
                lantern.light_on = True
            enemy.distracted = True
            enemy.alert = True
            return f"Joseph ofusca o {creature} com a lanterna, interrompendo seu ataque."
        if action == "atacar":
            weapon_name = self.attack_weapon or self.game.equipped_item
            if self.attack_weapon and self.attack_weapon not in self.game.inventory:
                return 'Não tenho isso comigo.'
            if self.attack_weapon and self.game.equipped_item != self.attack_weapon:
                return f'Preciso colocar {self.attack_weapon} na mão primeiro.'
            item = self.game.item_objects.get(weapon_name)
            if self.attack_weapon and not (item and (item.weapon or item.capabilities.melee_damage)):
                return 'Isso não é uma arma. Não vai me ajudar a atingir essa criatura.'
            if self.attack_mode == 'melee' and item and item.weapon:
                return 'Melhor atirar com essa arma. Não é uma boa escolha para bater.'
            if self.attack_mode == 'shoot' and not (item and item.weapon):
                return 'Preciso ter uma arma de fogo na mão para atirar.'
            if not (item and item.weapon) and enemy.distance != 'próximo':
                return 'Está longe demais para eu alcançar com isso.'
            damage = item.capabilities.melee_damage if item and item.capabilities.melee_damage else 10
            item = self.game.item_objects.get(self.game.equipped_item)
            if item and item.weapon:
                if item.weapon.ammo <= 0:
                    return feedback.EMPTY_WEAPON
                item.weapon.ammo -= 1
                damage = max(1, item.weapon.spec.damage - fear_profile(self.game.fear)["ranged_damage_penalty"])
            enemy.health = max(0, enemy.health - damage)
            enemy.alert = True
            text = f"Joseph atinge {label(self.game.get_current_room(), enemy)} em cheio."
            if not enemy.alive:
                text += f" {enemy.name.capitalize()} cambaleia antes de cair imóvel."
            elif enemy.condition() != enemy.reported_condition:
                text += ' ' + enemy.condition()
                enemy.reported_condition = enemy.condition()
            return text
        raise ValueError(f"Ação de confronto desconhecida: {action}")

    def clear_stance(self):
        self.guarding = self.dodging = False
        self.stance_expires = 0

    def begin_action(self, action):
        if action not in ('defender', 'esquivar', 'esperar'):
            self.clear_stance()

    def flee(self, direction, move):
        room = self.game.get_current_room()
        if direction not in room.known_exits() or room.passage_failure(direction):
            return move(direction)
        door = room.exit_doors.get(direction)
        if door and door.locked:
            return dialogue('Joseph', 'Está trancada. Preciso encontrar outra maneira.')
        try:
            self.game.get_room(room.exits[direction])
        except KeyError:
            return dialogue('Joseph', 'Não há uma saída acessível por aí.')
        threatened = any(e.alive and e.alert and e.distance == 'próximo' for e in room.enemies)
        if threatened and self.roll() >= avoidance_chance(FLEE_CHANCE, self.game.fear):
            return dialogue('Joseph', self.game.exploration.say('flee_fail', (
                'Não consegui passar! Preciso reagir!', 'A saída está perto, mas não consegui escapar!')))
        result = move(direction)
        if self.game.get_current_room() is not room:
            self.clear_stance()
            if threatened:
                result += '\n' + dialogue('Joseph', self.game.exploration.say('flee_success', (
                    'Consegui escapar!', 'Passei! Preciso continuar atento.')))
        return result

    def resolve_defense(self, damage):
        if self.dodging:
            avoided = self.roll() < avoidance_chance(DODGE_CHANCE, self.game.fear)
            text = self.game.exploration.say('dodge_success' if avoided else 'dodge_fail',
                ('Foi por pouco! Aquilo quase me acertou!', 'Consegui sair da trajetória do golpe!') if avoided else
                ('Droga! Não consegui sair da frente!', 'Fui lento demais... o golpe me alcançou!'))
            result = 0 if avoided else damage
        elif self.guarding:
            item = self.game.item_objects.get(self.game.equipped_item)
            profile = defense_profile(item)
            perfect = self.roll() < avoidance_chance(profile.perfect, self.game.fear)
            result = 0 if perfect else ceil(damage * (1 - profile.reduction))
            text = (self.game.exploration.say('perfect_guard', ('Consegui bloquear o ataque!', 'Segurei o golpe! Por pouco!')) if perfect else
                    self.game.exploration.say('normal_guard', ('Consegui amortecer parte do golpe!', 'Ainda doeu, mas consegui aparar parte do impacto!'))
                    if result < damage else 'O golpe passou pela minha defesa!')
        else:
            return damage, ''
        self.clear_stance()
        return result, dialogue('Joseph', text)

    def react(self, previous_enemy):
        """Resolve a ameaça anterior OU a encontrada, nunca duas reações."""
        active = [e for e in self.game.get_current_room().enemies if e.alive and
                  (not e.patrol_route or e.patrol_phase == 'combat')]
        enemy = active[self.reaction_index % len(active)] if active else None
        self.reaction_index += 1
        article = 'A ' if enemy and enemy.name.startswith(('criatura', 'aranha')) else 'O '
        title = article + label(self.game.get_current_room(), enemy) if enemy else 'A criatura'
        visible = enemy in self.game.exploration.visible_threats() if enemy else False
        def perceived(text):
            if visible:
                return text
            if enemy and self.game.exploration.local_sound(enemy, self.game.get_current_room()):
                return dialogue('Joseph', 'Ouço ' + enemy.sound + ' por perto.')
            return ''
        try:
            if previous_enemy and previous_enemy.alive and previous_enemy not in self.game.get_current_room().enemies:
                previous_enemy.preparing = False
                previous_enemy.distracted = False
                return "A ameaça fica para trás. Joseph alcança a saída sem ser atingido."
            if enemy is None:
                return ""
            if enemy.distance != 'próximo':
                enemy.alert = True
                return perceived(title + ' observa Joseph à distância.')
            if self.game.hidden and not enemy.alert and not (enemy.sensitive_to_light and self.game.light_visible):
                return perceived(title + " continua caminhando lentamente, sem olhar na direção de Joseph.")
            if not enemy.alert and not enemy.proximity and not (enemy.sensitive_to_light and self.game.light_visible) and not (enemy.hears and self.game.exploration.noise >= 2):
                return perceived(title + ' não parece ter percebido minha presença.')
            self.game.hidden = False
            if enemy.distracted:
                enemy.distracted = False
                enemy.preparing = False
                return perceived(title + " recua ofuscado e não consegue reagir.")
            if not enemy.alert:
                self.game.hidden = False
                enemy.alert = True
                self.game.increase_fear(5)
                return perceived(title + " percebe Joseph e se vira bruscamente.")
            if not enemy.preparing:
                enemy.preparing = True
                return perceived(title + " ergue o braço e inclina o corpo na direção de Joseph.")
            damage, defense = self.resolve_defense(enemy.damage)
            damage = self.game.incoming_damage(damage)
            enemy.preparing = False
            self.game.damage(damage)
            self.game.increase_fear(5)
            attacker = title if visible else "Algo fora de vista"
            text = f"{attacker} golpeia Joseph, que recua com o impacto." if damage else ""
            text = "\n".join(t for t in (text, defense) if t)
            if self.game.game_over:
                text += " Joseph não resiste."
            return text
        finally:
            if enemy is None or self.game.game_over or self.game.turn_count >= self.stance_expires:
                self.clear_stance()
