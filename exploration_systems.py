"""Exploração por eventos: percepção, surpresa e rondas sem relógio em tempo real."""
from threat_memory import ThreatMemory

class ExplorationSystems:
    def __init__(self, game):
        self.game = game
        self.noise = 0
        self.listening_direction = None
        self.hiding = None
        self.surprised_by = set()
        self.visited_empty = set()
        self.last_perception = ''
        self.narrative_counts = {}
        self.memory = ThreatMemory()

    def say(self, key, choices):
        index = self.narrative_counts.get(key, 0)
        self.narrative_counts[key] = index + 1
        return choices[index % len(choices)]

    def door_direction(self, target):
        from action_context import ActionContext
        choices = ActionContext().passages(self.game, target)
        return choices[0] if len(choices) == 1 else None

    def local_sound(self, enemy, room):
        distance = {'próximo': 0, 'médio': 1, 'distante': 2}.get(enemy.distance, 2)
        return enemy.alive and enemy.sound and enemy.sound_intensity - distance - max(0, room.ambient_noise) >= 1

    def visible_threats(self, room=None):
        room = room or self.game.get_current_room()
        lit = not room.dark or self.game.light_visible or any(o.light_on for o in room.objects.values())
        return [e for e in room.enemies if e.alive and e.sprite.visible and e.in_sight and lit]

    def sensory_passage(self, room, direction):
        if direction not in room.known_exits():
            return None
        state = room.exit_states.get(direction)
        door = room.exit_doors.get(direction)
        if state and not state.enabled or door and (door.blocked or not door.accessible):
            return None
        try:
            return self.game.get_room(room.exits[direction])
        except KeyError:
            return None

    def audible_signals(self, direction=None, explicit=False):
        # No máximo uma sala, ou duas com foco; cada obstáculo atenua o sinal.
        origin = self.game.get_current_room()
        frontier = [(origin, 0, 0, {origin.room_id})]
        found = {}
        max_depth = 1 if direction is not None else 2 if self.game.focus_charges else 1
        while frontier:
            room, depth, loss, seen = frontier.pop()
            if depth >= max_depth:
                continue
            for side in room.known_exits():
                if depth == 0 and direction is not None and side != direction:
                    continue
                other = self.sensory_passage(room, side)
                door = room.exit_doors.get(side)
                if other is None or other.room_id in seen or door and door.soundproof:
                    continue
                attenuation = loss + 1 + (door.sound_attenuation if door and not door.opened else 0)
                attenuation += max(0, other.ambient_noise)
                for enemy in other.enemies:
                    distance = {'próximo': 0, 'médio': 1, 'distante': 2}.get(enemy.distance, 2)
                    volume = enemy.sound_intensity - attenuation - distance - max(0, origin.ambient_noise)
                    volume += 1 if explicit else .5 if self.game.focus_charges else 0
                    if enemy.alive and enemy.sound and volume >= 1:
                        found[enemy.enemy_id] = (enemy.enemy_id, other.room_id, enemy.sound)
                frontier.append((other, depth + 1, attenuation, seen | {other.room_id}))
        return list(found.values())

    def sound_words(self, signals):
        sounds = list(dict.fromkeys(signal[2] for signal in signals))
        return ' e '.join(sounds)

    def observe_passage(self, target, explicit=True):
        direction = self.door_direction(target)
        if direction is None:
            return 'Em qual passagem quero olhar?' if explicit else ''
        room = self.game.get_current_room()
        other = self.sensory_passage(room, direction)
        door = room.exit_doors.get(direction)
        if other is None or door and not (door.opened or door.sight_gap):
            return 'Não consigo ver o outro lado por aqui.' if explicit else ''
        visible = self.visible_threats(other)
        signals = [(e.enemy_id, other.room_id, 'silhouette') for e in visible]
        from narrative import dialogue
        result = self.memory.observe('gap:' + room.room_id + ':' + other.room_id, signals,
            'suspected', 'Espera... vejo um vulto do outro lado. Preciso ter cuidado.',
            'Ainda vejo aquele vulto pela abertura.',
            changed='Agora não vejo aquele vulto. Isso não significa que o caminho esteja seguro.',
            explicit=explicit, changed_present='Há um vulto diferente naquela abertura.')
        return dialogue('Joseph', result) if result else ('Não consigo distinguir movimento do outro lado.' if explicit else '')

    def listen(self, target):
        direction = self.door_direction(target)
        if direction is None:
            return 'Em qual passagem quero escutar?'
        room = self.game.get_current_room()
        other = self.sensory_passage(room, direction)
        if other is None:
            return 'Não estou ouvindo nada por essa passagem. Ainda assim, é melhor ter cuidado.'
        self.listening_direction = direction
        signals = self.audible_signals(direction, explicit=True)
        sounds = self.sound_words(signals)
        remembered = self.memory.observe(
            'door:' + room.room_id + ':' + other.room_id, signals, 'confirmed',
            'Tem alguma coisa do outro lado dessa porta. Ouço ' + sounds + '.',
            'Ainda ouço ' + sounds + ' atrás dessa porta... melhor tomar cuidado.',
            changed='Estranho... não tô ouvindo mais nada. Ainda assim, é melhor ter cuidado.',
            explicit=True, changed_present='O som atrás dessa porta mudou... agora ouço ' + sounds + '.')
        if signals:
            self.perception()
        return remembered or 'Não estou ouvindo nada. Ainda assim, é melhor ter cuidado.'

    def perception(self):
        game = self.game
        room = game.get_current_room()
        door_messages = []
        for direction, destination in room.known_exits().items():
            try:
                destination = game.resolve_room_id(destination)
            except KeyError:
                continue
            context = 'door:' + game.current_location + ':' + destination
            if context not in self.memory.contexts:
                continue
            signals = self.audible_signals(direction, explicit=direction == self.listening_direction)
            sounds = self.sound_words(signals)
            notice = self.memory.observe(context, signals,
                'suspected', 'Ouço ' + sounds + ' atrás daquela porta.',
                'Ainda ouço ' + sounds + ' atrás dessa porta. Melhor tomar cuidado.',
                changed='Estranho... não tô ouvindo mais nada atrás daquela porta.',
                changed_present='O som atrás daquela porta mudou... ouço ' + sounds + '.')
            if notice:
                door_messages.append(notice)
        signals = self.audible_signals()
        steps = any(signal[2] == 'passos' for signal in signals)
        adjacent = {game.resolve_room_id(d) for d in room.known_exits().values() if d in game.rooms}
        distant = bool(signals) and all(signal[1] not in adjacent for signal in signals)
        sounds = self.sound_words(signals)
        notice = self.memory.observe('sound:' + game.current_location, signals, 'suspected',
            ('Peraí... acho que tô ouvindo passos.' if steps else 'Ouço ' + sounds + ' por perto.') if not distant else 'Estou mais atento... há um ruído muito fraco adiante: ' + sounds + '.',
            'Ainda tô ouvindo aqueles passos... melhor tomar cuidado.' if steps else 'Ainda ouço ' + sounds + '... melhor tomar cuidado.',
            changed_present='O som mudou de lugar ou de intensidade... ouço ' + sounds + '.',
            changed='Antes ouvi alguma coisa por aqui... agora está tudo quieto.')
        return '\n'.join(door_messages) if door_messages else notice

    def surprise(self, enemy, cautious=False):
        game = self.game
        if enemy.enemy_id in self.surprised_by:
            return ''
        self.surprised_by.add(enemy.enemy_id)
        game.increase_fear(12)
        from narrative import dialogue
        shock = dialogue('Joseph', self.say('shock', ('Meu Deus! Que coisa é essa?!', 'Droga! Preciso reagir!'))) + ' '
        severity = enemy.surprise or 60
        consequence = severity - (25 if cautious else 0) - game.confidence['value'] > 25
        if not consequence:
            return shock + 'Levo um susto, mas consigo manter a calma. ' + game.confidence['thought']
        if game.focus_charges:
            game.focus_charges -= 1
            game.emit('focus_spent')
            return shock + 'Quase paralisei de susto, mas consegui reagir a tempo.'
        game.pending_startle = 1
        return shock + 'Meu corpo trava por um instante. Preciso recuperar o controle.'

    def enter(self, old_room, cautious=False):
        game = self.game
        self.memory.visit += 1
        self.hiding = None
        old = game.rooms[old_room]
        if not any(e.alive for e in old.enemies):
            self.visited_empty.add(old_room)
        room = game.get_current_room()
        active = [e for e in room.enemies if e.alive]
        sight = self.memory.observe('sight:' + room.room_id,
            [(e.enemy_id, room.room_id, 'visible') for e in self.visible_threats(room)],
            'confirmed', game.confidence['thought'], 'Eu já vi essa ameaça aqui. Preciso ter cuidado.',
            changed='Não vejo mais aquela ameaça aqui. Melhor continuar atento.',
            changed_present='Tem algo diferente aqui... preciso ter cuidado.')
        for enemy in active:
            if enemy.patrol_route and enemy.patrol_phase == 'travel':
                enemy.patrol_phase = 'arrived'
        if not active:
            self.visited_empty.add(game.current_location)
            return '\n'.join(t for t in (sight, self.perception()) if t)
        surprise = next((e for e in active if e.surprise or game.current_location in self.visited_empty), None)
        return self.surprise(surprise, cautious) if surprise else sight

    def hide(self, target):
        game = self.game
        room = game.get_current_room()
        spots = [o for o in game.visible_objects().values() if o.hiding_effectiveness is not None and o.accessible]
        spot = next((o for o in spots if o.name == target), spots[0] if not target and len(spots)==1 else None)
        if not spot:
            return 'Não encontro um lugar adequado para me esconder aí.'
        if any(e.alive and e.alert for e in room.enemies):
            return 'Ele está olhando para mim. Não posso me esconder assim.'
        self.hiding = spot.object_id
        game.hidden = True
        return 'Fico imóvel, protegido por ' + spot.name + '. Preciso fazer silêncio.'

    def _step(self, room, enemy, destination):
        destination = self.game.resolve_room_id(destination)
        exits = {d: self.game.resolve_room_id(r) for d, r in room.known_exits().items()}
        if destination not in exits.values():
            return False
        direction = next(d for d, name in exits.items() if name == destination)
        state = room.exit_states.get(direction)
        if state is not None and not state.enabled:
            return False
        door = room.exit_doors.get(direction)
        if door and (door.blocked or door.locked or not door.opened or not door.accessible):
            return False
        room.enemies.remove(enemy)
        self.game.get_room(destination).enemies.append(enemy)
        return True

    def advance(self):
        game = self.game
        messages = []
        roster = [(room, enemy) for room in game.rooms.values() for enemy in list(room.enemies)
                  if enemy.alive and enemy.patrol_route]
        for room, enemy in roster:
            if enemy not in room.enemies or enemy.patrol_phase == 'combat':
                continue
            with_player = room.room_id == game.current_location
            if with_player and enemy.patrol_phase == 'arrived':
                enemy.patrol_phase = 'search'
                if enemy in self.visible_threats(room):
                    messages.append('Ele está aqui... parece estar procurando por mim.')
                elif self.local_sound(enemy, room):
                    messages.append('Ouço ' + enemy.sound + ' por perto.')
                continue
            if with_player and enemy.patrol_phase == 'search':
                spot = next((o for o in room.objects.values() if o.object_id == self.hiding), None)
                score = (enemy.detection if enemy.proximity else 0) + (30 if enemy.sensitive_to_light and game.light_visible else 0) + (20*self.noise if enemy.hears else 0)
                concealed = game.hidden and spot and spot.accessible and spot.hiding_effectiveness >= score
                if concealed:
                    enemy.patrol_phase = 'waiting'
                    if enemy in self.visible_threats(room) or self.local_sound(enemy, room):
                        messages.append(self.say('wait', ('Prendo a respiração. Tomara que ele siga adiante...', 'Não posso me mexer agora. Só mais um instante...')))
                else:
                    enemy.patrol_phase = 'combat'
                    enemy.alert = True
                    game.hidden = False
                    self.hiding = None
                    messages.append('Ele me encontrou! Preciso sair daqui.')
                continue
            enemy.patrol_clock += 1
            if enemy.patrol_phase != 'waiting' and enemy.patrol_clock < enemy.patrol_interval:
                continue
            enemy.patrol_clock = 0
            route = [game.resolve_room_id(r) for r in enemy.patrol_route]
            current = route.index(room.room_id) if room.room_id in route else -1
            destination = route[(current+1) % len(route)]
            # Som e luz só desviam criaturas que possuem esses sentidos.
            attracted = (enemy.hears and self.noise >= 2) or (enemy.sensitive_to_light and game.light_visible)
            if not with_player and attracted and game.current_location in {game.resolve_room_id(r) for r in room.known_exits().values()}:
                destination = game.current_location
            if self._step(room, enemy, destination):
                if with_player and (enemy in self.visible_threats(room) or self.local_sound(enemy, room)):
                    messages.append(self.say('relief', ('Os passos se afastam. Graças a Deus... ele não me viu.', 'O silêncio voltou. Parece que ele desistiu de procurar.')) if game.hidden else 'A criatura segue pelo corredor.')
                enemy.patrol_phase = 'arrived' if destination == game.current_location else 'travel'
                if destination == game.current_location:
                    if enemy in self.visible_threats():
                        messages.append('Uma criatura acaba de entrar pela passagem.')
                    elif self.local_sound(enemy, game.get_current_room()):
                        messages.append('Ouço ' + enemy.sound + ' na passagem.')
                    if not game.hidden and enemy in self.visible_threats() and (enemy.surprise or destination in self.visited_empty):
                        messages.append(self.surprise(enemy))
        perception = self.perception()
        room = game.get_current_room()
        context = 'sight:' + room.room_id
        if context in self.memory.contexts:
            change = self.memory.observe(context,
                [(e.enemy_id, room.room_id, 'visible') for e in self.visible_threats(room)],
                'confirmed', '', '', changed='Não vejo mais aquela ameaça aqui. Melhor continuar atento.',
                changed_present='Tem algo diferente aqui... preciso ter cuidado.')
            if change:
                messages.append(change)
        if perception:
            messages.append(perception)
        self.listening_direction = None
        self.last_perception = perception
        return '\n'.join(messages)

    def export_state(self):
        """Estado adicional para um futuro save; não substitui o mundo base."""
        game = self.game
        return {'version': 1, 'focus_charges': game.focus_charges, 'pending_startle': game.pending_startle,
                'threat_memory': self.memory.export_state(),
                'hiding': self.hiding, 'hidden': game.hidden, 'surprised_by': sorted(self.surprised_by),
                'visited_empty': sorted(self.visited_empty), 'last_perception': self.last_perception,
                'narrative_counts': dict(self.narrative_counts),
                'lights': [{'id': o.object_id, 'on': o.light_on, 'mode': o.light_mode}
                           for o in game.all_objects() if o.name == 'lanterna'],
                'patrols': [{'id': e.enemy_id, 'room': r.room_id, 'phase': e.patrol_phase, 'clock': e.patrol_clock}
                            for r in game.rooms.values() for e in r.enemies if e.patrol_route]}

    def restore_state(self, state):
        if state.get('version') != 1:
            raise ValueError('Unsupported exploration state version')
        game = self.game
        actors = {e.enemy_id: e for r in game.rooms.values() for e in r.enemies}
        for saved in state.get('patrols', []):
            if saved['id'] not in actors or saved['room'] not in game.rooms:
                raise ValueError('Restore the base world and entity identities first')
        game.focus_charges = max(0, min(2, int(state['focus_charges'])))
        game.pending_startle = max(0, min(1, int(state['pending_startle'])))
        self.hiding, game.hidden = state['hiding'], bool(state['hidden'])
        self.surprised_by = set(state['surprised_by'])
        self.visited_empty = set(state['visited_empty'])
        self.last_perception = state.get('last_perception', '')
        self.narrative_counts = dict(state.get('narrative_counts', {}))
        self.memory.restore_state(state.get('threat_memory', {}))
        objects = {o.object_id: o for o in game.all_objects()}
        for light in state.get('lights', []):
            if light['id'] in objects:
                obj = objects[light['id']]
                obj.light_on, obj.light_mode = bool(light['on']), light['mode']
        for saved in state.get('patrols', []):
            actor = actors[saved['id']]
            for room in game.rooms.values():
                if actor in room.enemies:
                    room.enemies.remove(actor)
            game.rooms[saved['room']].enemies.append(actor)
            actor.patrol_phase, actor.patrol_clock = saved['phase'], saved['clock']
