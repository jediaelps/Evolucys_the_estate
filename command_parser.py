from narrative import dialogue
from confrontation import Confrontation
from survival import Survival
import feedback
from command_language import normalize
from context_help import help_text
import locks
from combat_language import CombatContext
from target_selection import candidates
from action_context import ActionContext


class CommandParser:
    def __init__(self, game_state):
        self.game = game_state
        self.confrontation = Confrontation(game_state)
        self.survival = Survival(game_state)
        self.presentation = None
        self.read_document = None
        self.inspection_object = None
        self.inspection_face = None
        self.inspection_text = None
        self.reaction = ''
        self.combat_context = CombatContext()
        self.inventory_context = False
        self.inspection_context = None
        self.action_context = ActionContext()
        self.delayed_response = None

    def execute(self, command):
        if self.delayed_response is not None:
            return 'Joseph ainda aguarda uma resposta à campainha.'
        self.presentation = None
        self.read_document = None
        self.inspection_object = None
        self.inspection_face = None
        self.inspection_text = None
        self.reaction = ''
        self.confrontation.selected = None
        self.confrontation.attack_weapon = None
        self.confrontation.attack_mode = None
        try:
            raw = ' '.join(command.lower().split())
            expanded, clarification = self.action_context.interpret(self.game, raw)
            if clarification:
                return clarification
            if expanded:
                command = raw = expanded
            intent, enemy, question = self.combat_context.interpret(self.game, raw) if raw else (None, None, None)
            if question:
                return question
            if intent:
                self.confrontation.selected = enemy
                self.confrontation.attack_weapon = intent['weapon']
                self.confrontation.attack_mode = intent['mode']
                command = 'atacar ' + (enemy.name if enemy else intent['target'])
            command = normalize(self.game, command)
        except ValueError as error:
            return str(error)
        if self.game.game_over:
            return "Joseph não pode agir. A partida terminou."
        action, _, target = command.partition(' ')
        held = self.game.item_objects.get(target)
        if action in ('usar', 'tomar') and held and held.capabilities.personal and not self.inventory_context:
            return 'Melhor eu olhar isso no inventário.'
        # Consultas de interface não alteram o mundo. Tentativas de ações
        # reconhecidas custam um turno, mesmo quando falham.
        free = {"ajuda", "inventário", "inventario", "status", "fechar inventário", "fechar leitura"}
        actions = {"olhar", "observar", "examinar", "checar", "ver", "pegar", "apanhar",
                   "largar", "soltar", "segurar", "equipar", "abrir", "forçar", "forcar",
                   "ir", "andar", "usar", "digitar", "atacar", "defender", "esquivar", "distrair",
                   "esconder", "esperar", "fugir", "esgueirar", "recarregar",
                   "ligar", "desligar", "tomar", "ler", "atravessar", "fechar", "inspecionar",
                   "ouvir", "espiar", "tocar", "esgueirar_porta", "correr", "uv", "normal"}
        if self.inspection_context is not None and command:
            name = self.inspection_context
            allowed = command == 'fechar leitura' or (name and (
                command in tuple(verb + ' ' + name for verb in ('examinar', 'observar', 'olhar', 'ler'))
                or (command.startswith('inspecionar ') and command.split(' ', 2)[-1] == name)))
            if not allowed:
                if command.split()[0] not in actions | {value.split()[0] for value in free}:
                    return feedback.UNKNOWN
                return 'Volte à exploração para executar essa ação. Nenhuma ação foi executada.'
        if not command or command in free or command.split()[0] not in actions:
            return self.dispatch(command)
        self.confrontation.begin_action(command.split()[0])
        previous_enemy = self.confrontation.enemy()
        action = command.split()[0]
        self.game.exploration.noise = 2 if action in ('atacar', 'correr', 'forçar', 'forcar') else 0 if action in ('esgueirar', 'esgueirar_porta', 'esconder', 'esperar', 'ouvir', 'ler', 'olhar', 'examinar', 'observar') else 1
        if self.game.pending_startle:
            self.game.pending_startle -= 1
            response = 'Ainda estou paralisado pelo susto. Preciso recuperar o controle.'
        else:
            if action not in {"esgueirar", "esgueirar_porta", "esconder", "examinar", "observar", "olhar", "esperar", "ler", "ouvir"}:
                self.game.hidden = False
            response = self.dispatch(command)
        self.game.turn_count += 1
        exploration = self.game.exploration.advance()
        reaction = self.confrontation.react(previous_enemy)
        expiry = self.game.end_turn()
        self.reaction = '\n'.join(text for text in (exploration, reaction, expiry) if text)
        return "\n".join(text for text in (response, exploration, reaction, expiry) if text)

    def dispatch(self, command):
        if not command:
            return ""
        if command == 'ajuda' or command.startswith('ajuda '):
            topic = command[5:].strip()
            if topic == 'comandos':
                self.presentation = 'reading'
            return help_text(self.game, topic)
        if command in ('fechar inventário', 'fechar leitura'):
            if command == 'fechar inventário':
                self.inventory_context = False
            self.presentation = 'close_inventory' if command == 'fechar inventário' else 'close_reading'
            return 'Painel fechado.'

        if command in ["olhar", "olhar sala", "observar ambiente"]:
            return self.look_room()

        if command in ["checar celular", "ver celular", "olhar celular"]:
            return self.check_phone()

        if command in ["inventário", "inventario"]:
            self.inventory_context = True
            self.presentation = 'inventory'
            return self.show_inventory()

        if command == "status":
            state = self.game.snapshot()
            weapons = "; ".join(f"{name}: {value['ammo']}/{value['capacity']}" for name, value in state['weapons'].items())
            return (f"Vida: {self.game.health}/{self.game.max_health}. Medo: {self.game.fear}. "
                    f"Equipado: {self.game.equipped_item or 'nada'}. Turnos: {self.game.turn_count}. "
                    f"Confronto: {'sim' if state['in_confrontation'] else 'não'}. "
                    f"{'Estou mais atento. ' if self.game.focus_charges else ''}"
                    f"Respiração: {state['fear_profile']['breathing']}. "
                    f"Luz visível: {'sim' if state['light_visible'] else 'não'}. "
                    + (f"Munição — {weapons}." if weapons else ""))

        words = command.split()
        action = words[0]
        target = " ".join(words[1:])
        if action == 'tocar':
            return self.ring_bell(target)
        if action == 'espiar':
            return self.game.exploration.observe_passage(target)
        if action == 'ouvir':
            return self.game.exploration.listen(target)
        if action in ('uv', 'normal'):
            return self.survival.light_mode(action)
        if action == 'esgueirar_porta':
            direction = self.game.exploration.door_direction(target)
            return self.move(direction or '', stealth=True)
        if action == 'correr':
            return self.move(target)
        if action == 'esconder' and (target or any(o.hiding_effectiveness is not None for o in self.game.visible_objects().values())):
            return self.game.exploration.hide(target)
        if action == 'inspecionar':
            face, _, name = target.partition(' ')
            return self.inspect_face(name, face)
        if action == 'ler':
            return self.read(target)
        if action == 'atravessar':
            return self.cross(target)
        if action == 'fechar':
            return self.close_object(target)

        if action == "recarregar":
            return self.survival.reload(target)
        if action in {"ligar", "desligar"}:
            if target != "lanterna":
                return "O que quero acionar? Use ligar lanterna ou desligar lanterna."
            return self.survival.light(action == "ligar")

        if action in {"atacar", "defender", "esquivar", "distrair", "esconder", "esperar"}:
            return self.confrontation.act(action, target)
        if action == "fugir":
            return self.confrontation.flee(target, self.move)
        if action == "esgueirar":
            return self.move(target, stealth=True)

        if action in ["examinar", "observar", "olhar"]:
            return self.examine(target)
        if action in ["pegar", "apanhar"]:
            return self.take(target)
        if action in ["largar", "soltar"]:
            return self.drop(target)
        if action in ["segurar", "equipar"]:
            return self.equip(target)
        if action in ["abrir", "forçar", "forcar"]:
            return self.open_object(target)
        if action in ["ir", "andar"]:
            return self.move(target)
        if action in {"usar", "tomar"}:
            return self.use_command(target)
        if action == "digitar":
            if " no " not in target:
                return "Use: digitar CÓDIGO no OBJETO."
            code, obj = target.split(" no ", 1)
            return self.enter_code(code, obj)

        return feedback.UNKNOWN

    def look_room(self):
        self.presentation = 'environment'
        return self.game.get_current_room().describe(self.game)

    def examine(self, target):
        if not target:
            return "Examinar o quê?"

        room = self.game.get_current_room()

        visible_enemies = candidates(room, target) if target else []
        if len(visible_enemies) == 1:
            return visible_enemies[0].describe()
        fallen = [e for e in room.enemies if not e.alive and e.name == target]
        if len(fallen) == 1:
            return fallen[0].describe()
        if target in room.objects:
            obj = room.objects[target]
            if not obj.accessible:
                return obj.inaccessible_reason
            self.game.investigated.add(obj.object_id)
            if obj.interaction == 'greenhouse_fall':
                text = obj.examine()
                if 'campaign.jack' in self.game.investigated:
                    text += '\n' + dialogue('Joseph', 'Essa ponta parece encaixar no macaco que examinei.')
                return self.inspect_description(obj, text)
            if obj.interaction == 'well':
                return self.inspect_description(obj, self.examine_well())
            if 'front' in obj.inspection_faces:
                return self.inspect_face(target, 'front') + self.reveal_message(obj.reveal_hidden(room))
            if obj.text is not None:
                self.read(target)
                return obj.examine()
            notice = self.game.exploration.observe_passage(target, explicit=False) if obj in room.exit_doors.values() else ''
            return self.inspect_description(obj, '\n'.join(t for t in (obj.examine() + self.reveal_message(obj.reveal_hidden(room)), notice) if t))
        if target in self.game.inventory:
            if target in self.game.item_objects:
                self.game.investigated.add(self.game.item_objects[target].object_id)
                if 'front' in self.game.item_objects[target].inspection_faces:
                    return self.inspect_face(target, 'front')
                if self.game.item_objects[target].text is not None:
                    self.read(target)
                    return self.game.item_objects[target].examine()
                obj = self.game.item_objects[target]
                return self.inspect_description(obj, obj.examine())
            return f"Joseph examina {target}."

        return f"Joseph não vê {target} por aqui."

    def inspect_description(self, obj, text):
        self.inspection_object, self.inspection_face = obj, None
        self.inspection_text = text
        self.presentation = 'inspection'
        return text

    def inspect_face(self, target, face):
        obj = self.game.get_current_room().objects.get(target) or self.game.item_objects.get(target)
        if obj is None:
            return 'Não vejo esse objeto aqui.'
        if not obj.accessible:
            return obj.inaccessible_reason
        if face == 'interior' and (obj.locked or not obj.opened):
            return 'Preciso abrir antes de olhar dentro.'
        if face == 'open' and not obj.opened or face == 'closed' and obj.opened or face == 'damaged' and not obj.damaged:
            return 'Não é assim que ele está agora.'
        if face not in obj.inspection_faces:
            return 'Não consigo examinar esse lado desse objeto.'
        obj.inspected_faces.add(face)
        self.game.investigated.add(obj.object_id)
        self.inspection_object, self.inspection_face = obj, face
        self.presentation = 'inspection'
        return obj.inspection_faces[face]

    def read(self, target):
        if not target:
            return 'Ler o quê?'
        obj = self.game.get_current_room().objects.get(target) or self.game.item_objects.get(target)
        if obj is None:
            return f'Não vejo {target} aqui nem no meu inventário.'
        if not obj.accessible:
            return obj.inaccessible_reason
        if obj.text is None:
            return 'Não há texto legível nesse objeto.'
        self.presentation = 'reading'
        self.read_document = obj
        self.game.emit('document_open', object_id=obj.object_id)
        return obj.read_page(0)

    def cross(self, target):
        room = self.game.get_current_room()
        for direction, door in room.exit_doors.items():
            if direction in room.known_exits() and door.name == target:
                return self.move(direction)
        if target in room.objects:
            obj = room.objects[target]
            if obj.blocked or obj.locked:
                return obj.passage_failure()
            return 'Esse objeto não dá acesso a uma passagem disponível.'
        return f'Não vejo {target or "essa passagem"} aqui.'

    def take(self, target):
        if not target:
            return "Pegar o quê?"

        room = self.game.get_current_room()

        if target not in room.objects:
            return f"Não há {target} aqui."

        obj = room.objects[target]

        if not obj.accessible:
            return obj.inaccessible_reason
        if obj.interaction == 'greenhouse_fall' and 'greenhouse_fall' not in self.game.world_events:
            destination = room.exits.get('queda')
            if destination is None or room.exit_states['queda'].kind != 'fall':
                return 'Não consigo alcançar a manivela daqui.'
            self.game.get_room(destination)  # valida o destino antes de aplicar o evento.
            self.game.world_events.add('greenhouse_fall')
            obj.accessible = False
            obj.inaccessible_reason = 'A manivela ficou sobre a mesa, além do piso que cedeu. Não alcanço daqui.'
            room.description = ('O piso da estufa cedeu junto à mesa. A manivela continua lá, '
                                'fora de alcance. Vasos quebrados cercam a abertura escura.')
            old_room = self.game.current_location
            self.game.current_location = destination
            self.game.visited_rooms.add(self.game.current_location)
            self.game.exploration.enter(old_room)
            self.presentation = 'environment'
            return ('Joseph se aproxima da mesa. A madeira range; quando ele estende a mão, '
                    'uma tábua se rompe e as tábuas cedem sob seus pés. Ele cai na escuridão, '
                    'sem alcançar a manivela.\n'
                    'Por alguns instantes, a dor o deixa sem ar. Aos poucos, ele recupera a orientação.\n'
                    + self.game.get_current_room().description + '\n'
                    + dialogue('Joseph', 'Por ali não consigo subir. Preciso encontrar outra saída.'))

        if not obj.portable:
            return f"{target.capitalize()} não é algo que eu consiga carregar."

        if len(self.game.inventory) >= self.game.inventory_limit:
            return feedback.FULL

        if not self.game.add_item(target):
            return "Já tenho um desses comigo. Melhor guardar espaço para outras coisas."
        self.game.item_objects[target] = obj
        del room.objects[target]
        if obj.text is not None:
            self.game.emit('document_collect', object_id=obj.object_id)
        if obj.key_lock_ids or obj.name.startswith('chave'):
            self.game.emit('key_pickup', object_id=obj.object_id)
        return f"Joseph pega {target}."

    def drop(self, target):
        if target not in self.game.inventory:
            return feedback.missing_item(self.game, target)
        obj = self.game.item_objects.get(target)
        if obj is None:
            return "Esse item não pode ser largado aqui."
        if target in self.game.get_current_room().objects:
            return "Já há um desses aqui. Melhor deixar o meu em outro lugar."
        self.game.remove_item(target)
        self.game.get_current_room().add_object(obj)
        return f"Joseph largou {target}."

    def equip(self, target):
        if not target:
            return "Segurar o quê?"

        obj = self.game.item_objects.get(target)
        if obj and not obj.capabilities.equipable:
            return 'É melhor deixar isso guardado para quando eu precisar.'
        if self.game.equip_item(target):
            return f"Joseph segura {target}."

        return feedback.missing_item(self.game, target)

    def move(self, target, stealth=False):
        if not target:
            return "Ir para onde?"

        room = self.game.get_current_room()

        if target not in room.exits:
            if target in ('cima', 'baixo'):
                return 'Não há escadaria acessível para ' + ('subir' if target == 'cima' else 'descer') + ' daqui.'
            from narrative import dialogue
            return dialogue('Joseph', 'Não há uma passagem direta para lá daqui.')

        if room.room_id == 'E13' and target == 'baixo':
            if not self.well_light():
                return 'Não consigo ver onde apoiar os pés. Preciso de uma lanterna acesa na mão.'
            self.examine_well()
            door = room.exit_doors[target]
            if door.locked or not room.exit_states[target].enabled:
                return 'Vejo a escada, mas o acesso no fundo está fechado. Não há como abri-lo daqui.'
        reason = room.passage_failure(target)
        if reason:
            return reason

        old_room = self.game.current_location
        self.inventory_context = False
        self.game.current_location = room.exits[target]
        self.game.visited_rooms.add(self.game.current_location)
        self.game.hidden = stealth
        notice = self.game.exploration.enter(old_room, stealth)
        self.presentation = 'environment'
        description = self.game.get_current_room().describe(self.game)
        if not description.startswith('Joseph '):
            description = 'Joseph atravessa a passagem. ' + description
        return '\n'.join(t for t in (description, notice) if t)

    def open_object(self, target):
        if not target:
            return "Abrir o quê?"

        room = self.game.get_current_room()

        if target not in room.objects:
            return f"Joseph não encontra {target} aqui."

        obj = room.objects[target]

        if obj.interaction == 'well_access':
            if room.room_id != 'B02':
                return 'O acesso do poço não pode ser aberto deste lado.'
            if 'containment_disabled' not in self.game.world_events:
                return 'A trava permanece presa pelo sistema de contenção. Não consigo soltá-la.'
            if obj.opened:
                return 'O acesso do poço já está aberto.'
            obj.locked = False
            obj.opened = True
            state = room.exit_states['cima']
            state.enabled = True
            # Conhecer o acesso por dentro revela a rota, mas não dispensa iluminação para descer.
            state.reveal()
            return 'Joseph solta a trava por dentro e abre o acesso. Uma escada sobe pela parede do poço.'

        if not obj.accessible:
            return obj.inaccessible_reason
        if obj.blocked:
            return obj.passage_failure()
        if obj.opened:
            return f"{target.capitalize()} já está aberto."

        key_message = ''
        was_locked = obj.locked
        if obj.locked:
            obj.known_state = 'trancada'
            if obj.code is not None:
                return f"{target.capitalize()} está trancado. Digite o código no teclado."
            key = locks.find_key(self.game, obj)
            if key is not None:
                key_message = locks.unlock(self.game, key, obj, opening=obj.openable)
            elif obj.required_item not in self.game.inventory:
                return feedback.LOCKED
            else:
                obj.locked = False

        if not obj.openable:
            return '\n'.join(t for t in (key_message, f"Joseph não pode abrir {target}.") if t)
        return '\n'.join(t for t in (key_message, self.finish_open(obj, unlocked=was_locked)) if t)

    def close_object(self, target):
        obj = self.game.get_current_room().objects.get(target)
        if obj is None:
            return f'Não vejo {target} aqui.'
        if not obj.accessible or obj.blocked:
            return obj.passage_failure()
        if not obj.openable:
            return 'Não há como fechar esse objeto.'
        if not obj.opened:
            return 'Já está fechado.'
        obj.opened = False
        obj.known_state = 'fechada'
        if obj in self.game.get_current_room().exit_doors.values():
            self.game.emit('door_close', object_id=obj.object_id)
        return f'Fecho {target}.'

    @staticmethod
    def reveal_message(names):
        return "\nJoseph encontra: " + ", ".join(names) + "." if names else ""

    def finish_open(self, obj, unlocked=False, tool=None):
        if not obj.accessible or obj.blocked:
            return obj.passage_failure()
        unlocked = unlocked or obj.locked
        if obj.locked:
            self.game.emit('lock_unlock', lock_id=obj.lock_id)
        obj.locked = False
        obj.opened = True
        obj.known_state = 'aberta'
        if obj in self.game.get_current_room().exit_doors.values():
            self.game.emit('door_open', object_id=obj.object_id)
        if tool:
            text = f"Com {tool}, Joseph solta o mecanismo e abre {obj.name}."
        elif unlocked:
            text = f"A fechadura cede com um estalo e {obj.name} se abre."
        else:
            text = f"{obj.name.capitalize()} se abre."
        return text + self.reveal_message(obj.reveal_contents(self.game.get_current_room()))

    def enter_code(self, code, target):
        obj = self.game.get_current_room().objects.get(target)
        if obj is None:
            return f"Não há {target} aqui."
        if not obj.accessible or obj.blocked:
            return obj.passage_failure()
        if obj.code is None:
            return f"{target.capitalize()} não tem teclado."
        if obj.opened:
            return f"{target.capitalize()} já está aberto."
        if code != obj.code:
            return "Código incorreto. O cofre permanece trancado."
        return self.finish_open(obj)

    def use_command(self, target):
        if not target:
            return "Usar o quê?"

        if " na " in target:
            item, obj = target.split(" na ", 1)
            return self.use_item_on_object(item, obj)

        if " no " in target:
            item, obj = target.split(" no ", 1)
            return self.use_item_on_object(item, obj)

        return self.use_item(target)

    def use_item_on_object(self, item, target):
        if item not in self.game.inventory:
            return feedback.missing_item(self.game, item)

        room = self.game.get_current_room()
        obj = room.objects.get(target)
        if obj and obj.interaction == 'main_power_panel' and item == 'fusíveis':
            if 'fuses_installed' in self.game.world_events:
                return 'Os fusíveis já estão instalados.'
            self.game.remove_item(item)
            self.game.world_events.add('fuses_installed')
            obj.description = 'Os fusíveis estão firmes no quadro do gerador principal.'
            return 'Joseph encaixa os fusíveis no quadro. O gerador principal pode ser acionado.'
        if obj and obj.interaction == 'well' and item == 'lanterna':
            return self.examine_well()
        if obj and obj.interaction == 'well_access':
            return 'A trava do poço só pode ser solta por dentro.'
        held = self.game.item_objects.get(item)
        if held and item == 'pé de cabra' and obj and obj.interaction == 'jammed_maintenance':
            if obj.opened:
                return 'A passagem já está aberta.'
            obj.blocked = False
            for direction, door in room.exit_doors.items():
                if door is obj:
                    room.exit_states[direction].enabled = True
            return self.finish_open(obj, tool=item)
        if held and held.interaction == 'jack':
            return dialogue('Joseph', 'O macaco está incompleto. Sem a manivela, não consigo levantar o carro.')
        threats = candidates(room, target)
        held_target = self.game.item_objects.get(target)
        held_item = self.game.item_objects.get(item)
        if held_target and held_target.weapon and held_item and held_item.ammo_count:
            return self.survival.reload(target)
        if threats and item in ('bandagem', 'spray de cura', 'kit médico', 'chá', 'energético'):
            return 'Isso não vai me ajudar contra ele. É algo para cuidar de mim.'

        if item == "lanterna" and room.enemy and target == room.enemy.name:
            if self.game.equipped_item != item:
                return "Preciso colocar a lanterna na mão primeiro."
            return self.confrontation.act("distrair", target)

        if target not in room.objects:
            return f"Não há {target} aqui."

        obj = room.objects[target]

        if not obj.accessible or obj.blocked:
            return obj.passage_failure()
        key = self.game.item_objects.get(item)
        if (locks.matches(key, obj) if key else obj.required_item == item) and obj.code is None:
            if obj.opened:
                return f"{target.capitalize()} já está aberto."
            was_locked = obj.locked
            message = locks.unlock(self.game, key, obj, opening=True) if key and obj.locked else ''
            is_key = bool(key and (key.key_lock_ids or key.name.startswith('chave')))
            return '\n'.join(t for t in (message, self.finish_open(obj, unlocked=was_locked,
                              tool=item if was_locked and not is_key else None)) if t)

        if key and (key.key_lock_ids or key.name.startswith('chave')):
            self.game.emit('key_wrong', object_id=key.object_id)
            return 'Essa chave não serve aqui.'

        if item == 'pé de cabra':
            return 'Talvez eu consiga forçar alguma estrutura com isso, mas aqui não encontro onde apoiar.'
        return "Isso não encaixa aqui. Talvez exista outra maneira."

    def use_item(self, target):
        generator = self.game.get_current_room().objects.get(target)
        if generator and generator.interaction == 'main_generator':
            if 'power_restored' in self.game.world_events:
                return 'O gerador principal já está funcionando.'
            if 'fuses_installed' not in self.game.world_events:
                return 'O gerador não responde. Faltam fusíveis no quadro elétrico.'
            self.game.world_events.add('power_restored')
            generator.description = 'O gerador principal funciona com um ronco constante.'
            return 'O gerador ganha força. A energia volta às instalações da mansão; as travas de contenção permanecem fechadas.'
        obj = self.game.item_objects.get(target)
        if obj and obj.interaction == 'jack':
            return dialogue('Joseph', 'Falta a manivela do macaco. Não consigo utilizá-lo assim.')
        return self.survival.use(target, from_inventory=self.inventory_context)

    def well_light(self):
        return self.game.well_lit

    def examine_well(self):
        if not self.well_light():
            return 'O poço é escuro e fundo demais. Não consigo distinguir o fundo direito.'
        room = self.game.get_current_room()
        state = room.exit_states['baixo']
        state.reveal()
        door = room.exit_doors['baixo']
        return ('A luz revela uma escada presa à parede interna e uma abertura no fundo. ' +
                ('O acesso está fechado, sem maneira de abri-lo daqui.' if door.locked or not state.enabled or not door.opened
                 else 'O acesso no fundo está aberto. Posso descer com cuidado.'))

    def ring_bell(self, target):
        obj = self.game.get_current_room().objects.get(target)
        if obj is None or obj.interaction != 'doorbell':
            return 'Não vejo uma campainha aqui.'
        from narrative import dialogue
        if 'doorbell_rung' in self.game.world_events:
            self.delayed_response = 'Ninguém responde desta vez também.'
            return 'A campainha soa outra vez. Joseph espera por uma resposta...'
        self.game.world_events.add('doorbell_rung')
        self.delayed_response = ('Ninguém responde.\n' + dialogue('Joseph',
            'Parece que não tem ninguém em casa. Vou olhar os arredores e procurar outra forma de achar ajuda.'))
        return ('Joseph toca a campainha. O som se perde atrás da porta.\n'
                + dialogue('Joseph', 'Tem alguém aí?') + '\nEle espera por uma resposta...')

    def finish_delayed_response(self):
        response, self.delayed_response = self.delayed_response, None
        return response or ''

    def show_inventory(self):
        if not self.game.inventory:
            return "Inventário vazio."
        descriptions = []
        for name in self.game.inventory:
            obj = self.game.item_objects.get(name)
            detail = name
            if obj and obj.weapon:
                detail += f" ({obj.weapon.ammo}/{obj.weapon.spec.capacity})"
            elif obj and obj.ammo_count:
                detail += f" ({obj.ammo_count} cartuchos)"
            descriptions.append(detail)
        return "Inventário: " + ", ".join(descriptions) + "."

    def check_phone(self):
        if self.game.phone_signal:
            return "O celular encontrou sinal."
        return "Sem sinal."

