"""Ajuda baseada apenas em objetos percebidos e estados já observados."""
from command_language import resolve, fold
from items import HEALING


REFERENCE = '''EXPLORAÇÃO
  olhar / olhar em volta; examinar [objeto]; ler [documento]; ir [direção]
  passar pela [porta]; atravessar [porta]; esgueirar [direção]
  subir escada; descer escadaria; voltar ao salão
OBJETOS
  pegar [item]; abrir [objeto]; usar [item]; usar [item] em/no/na [objeto]
  digitar [código] no [objeto]
LINGUAGEM
  ver, olhar para, observar, examinar, inspecionar, dar uma olhada
  pegar, apanhar, recolher; usar, utilizar; ir, seguir, andar
  atacar, bater, golpear, acertar; atirar, disparar
  Posso indicar quem está à esquerda, à direita, perto ou longe.
EQUIPAMENTO
  equipar [item]; largar [item]; ligar lanterna; desligar lanterna; recarregar pistola
SOBREVIVÊNCIA
  No inventário: usar bandagem; usar spray de cura; usar kit médico; usar chá; usar energético
EXPLORAÇÃO CAUTELOSA
  ouvir atrás da porta; escutar porta; entrar devagar; passar pela porta furtivamente
  esconder no [esconderijo]; acender lanterna; apagar lanterna
CONFRONTO
  atacar [inimigo]; defender; esquivar; distrair; esconder; esperar; fugir [direção]
INFORMAÇÕES
  inventário; abrir inventário; fechar inventário; status; checar celular
  ajuda; ajuda [assunto]; fechar leitura
Posso consultar meus pertences com calma. Se houver perigo, preciso tomar cuidado ao agir.
Na interface visual, ESC pausa. No terminal, sair encerra a sessão.'''


def help_text(game, topic=''):
    from narrative import dialogue
    import re
    topic = fold(topic.strip())
    if topic == 'comandos':
        return REFERENCE
    room = game.get_current_room()
    visible = {name: obj for name, obj in game.visible_objects().items() if obj.accessible}
    known = dict(visible, **game.item_objects)
    paths = []
    for direction, destination in room.known_exits().items():
        state = room.exit_states.get(direction)
        if state is not None and not state.enabled:
            continue
        door = room.exit_doors.get(direction)
        if room.room_id == 'E13' and direction == 'baixo' and not game.well_lit:
            continue
        try:
            game.get_room(destination)
        except KeyError:
            continue
        if door and (door.name not in visible or not door.opened or door.locked or door.blocked):
            continue
        if direction in ('norte', 'sul', 'leste', 'oeste'):
            paths.append('seguir para o ' + direction.upper())
        elif direction in ('cima', 'baixo'):
            paths.append(('SUBIR' if direction == 'cima' else 'DESCER') + ' pela escadaria')
        elif door:
            paths.append(('passar pelo ' if door.name.startswith(('portão', 'acesso')) else 'passar pela ') + door.name)
        elif direction in room.exit_names:
            name = room.exit_names[direction]
            article = 'pelo ' if name.startswith(('caminho', 'corredor', 'jardim', 'pátio', 'túnel', 'acesso')) else 'pela '
            paths.append('seguir ' + article + name)
    routes = ' ou '.join(paths)
    def thought(text):
        if not topic and paths:
            text = text.rstrip('.') + '. Também posso ' + routes + '.'
        return dialogue('Joseph', text)
    if not topic and room.room_id == 'B01' and 'greenhouse_fall' in game.world_events:
        return thought('O buraco ficou alto demais. Preciso me orientar e procurar outra saída.')
    if not topic and room.room_id == 'E08' and 'greenhouse_fall' not in game.world_events:
        if 'campaign.jack_handle' in game.investigated:
            return thought('A peça está sobre a mesa. Posso tentar alcançá-la.')
        return thought('Há uma peça de metal sobre a mesa. Posso EXAMINAR a manivela com mais atenção.')
    if not topic and room.room_id == 'E07' and 'campaign.jack' in game.investigated:
        return thought('O macaco está incompleto. Preciso prestar atenção na peça que falta.')
    if not topic and room.room_id == 'E03':
        return thought('Ninguém respondeu à campainha. Posso explorar o terreno.'
                       if 'doorbell_rung' in game.world_events else
                       'Talvez alguém na mansão possa ajudar. Preciso OBSERVAR os arredores.')
    if not topic and 'campainha' in visible:
        return thought('Ninguém respondeu. Posso investigar os arredores em busca de ajuda.'
                       if 'doorbell_rung' in game.world_events else 'A porta está trancada. Posso TOCAR a campainha e esperar por alguém.')
    if not topic and 'carro' in visible:
        return thought('O pneu está estragado. Talvez eu encontre ajuda na mansão adiante.')
    if topic == 'inventario':
        return thought('Posso abrir o INVENTÁRIO e olhar meus pertences com calma.')
    if topic == 'celular':
        return thought('Talvez eu devesse CHECAR o celular para ver se há sinal.')
    obj = None
    if topic and topic not in ('combate', 'confronto'):
        try:
            name = resolve(game, topic)
        except ValueError:
            return thought('Em que preciso prestar mais atenção?')
        obj = known.get(name)
        if obj is None:
            return thought('Não percebo isso aqui. Melhor OBSERVAR o ambiente.')
    threats = game.exploration.visible_threats()
    if obj is None and threats:
        return thought('Ele ainda não me viu. Talvez seja melhor me ESCONDER.' if not any(e.alert for e in threats)
                       else 'Ele está perto demais. Posso me DEFENDER, ESQUIVAR ou tentar FUGIR.')
    if obj is None and game.health < game.max_health and any(n in HEALING for n in game.inventory):
        return thought('Estou ferido. Melhor abrir o INVENTÁRIO e cuidar disso.')
    if obj is None and game.fear >= 30:
        return thought('Estou tenso. Talvez o chá no INVENTÁRIO me ajude a recuperar a calma.' if 'chá' in game.inventory
                       else 'Estou tenso. Preciso OBSERVAR os arredores antes de me expor.')
    if obj is None:
        obj = next((o for o in visible.values() if o.locked and 'teclado' in o.description.lower()), None)
    if obj and obj.locked and 'teclado' in obj.description.lower():
        # Só páginas efetivamente lidas e faces examinadas fornecem pistas.
        evidence = []
        for source in game.all_objects():
            evidence.extend(source.pages[i] for i in source.read_pages if i < len(source.pages))
            evidence.extend(source.inspection_faces[f] for f in source.inspected_faces if f in source.inspection_faces)
            if source.object_id in game.investigated and source.text is None:
                evidence.append(source.description)
        related = [t for t in evidence if re.search(r'\b\d{3,}\b', t) and
                   (obj.name.lower() in t.lower() or ('cofre' in obj.name.lower() and 'cofre' in t.lower()) or
                    (obj.object_id in game.investigated and 'algarismos' in t.lower() and
                     sum('teclado' in o.description.lower() for o in visible.values()) == 1))]
        if related:
            if obj.object_id in game.investigated:
                return thought(f'Talvez eu possa DIGITAR a combinação no {obj.name}.')
            return thought(f'Aquele número que encontrei pode ter relação com {obj.name}. Preciso EXAMINAR melhor.')
        return thought(f'Esse {obj.name} precisa de uma combinação... talvez exista alguma pista por aqui para EXAMINAR.')
    if obj:
        if obj.text is not None and not obj.was_read:
            return thought(f'Talvez eu devesse LER {obj.name} com atenção.')
        if obj.known_state in ('trancada', 'bloqueada'):
            return thought(f'Já percebi que está {obj.known_state}. Preciso EXAMINAR melhor os arredores.')
        if obj.locked and any('chave' in n for n in game.inventory):
            return thought('Talvez eu consiga USAR uma das minhas chaves nessa fechadura.')
        return thought(f'Talvez eu devesse EXAMINAR {obj.name} com mais atenção.')
    for context, memory in game.exploration.memory.contexts.items():
        if not (context == 'sound:' + room.room_id or context.startswith('door:' + room.room_id + ':')):
            continue
        if memory['signals'] or memory['state'] == 'altered':
            return thought('Lembro dos sinais que percebi por aqui. Melhor OUVIR de novo antes de atravessar.')
    unread = next((o for o in reversed(list(visible.values())) if o.text is not None and not o.was_read), None)
    if unread:
        return thought(f'Talvez eu devesse LER {unread.name}. Pode haver algo importante ali.')
    unexplored = next((o for o in visible.values() if o.object_id not in game.investigated and o not in room.exit_doors.values()), None)
    if unexplored:
        return thought(f'Talvez eu devesse EXAMINAR {unexplored.name} com mais atenção.')
    if any(o.accessible for o in room.exit_doors.values()):
        return thought('Posso tentar OUVIR atrás dessa porta antes de entrar.')
    objective = (game.objective.rstrip('.') + '. ') if game.objective else ''
    return thought(objective + 'Melhor OBSERVAR os arredores antes de seguir.')
