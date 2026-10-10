"""Aliases locais: só resolve nomes presentes, nunca procura itens escondidos."""
import re
import unicodedata

VERBS = {'recolher': 'pegar', 'utilizar': 'usar', 'seguir': 'ir', 'colocar': 'usar', 'acender': 'ligar', 'apagar': 'desligar'}


def fold(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')


def strip_article(text):
    return re.sub(r'^(?:a|o|as|os|um|uma)\s+', '', text.strip())


def resolve(game, target):
    target = strip_article(target)
    names = list(dict.fromkeys([*game.visible_objects(), *game.inventory]))
    if target in game.get_current_room().objects and target not in game.visible_objects():
        raise ValueError('Não consigo distinguir isso sob esta luz.')
    enemy = game.get_current_room().enemy
    if enemy:
        names.append(enemy.name)
    if target in names:
        return target
    normalized = fold(target)
    for name, obj in {**game.visible_objects(), **game.item_objects}.items():
        if normalized in {fold(alias) for alias in obj.aliases}:
            return name
    exact = [name for name in names if fold(name) == normalized]
    matches = exact or [name for name in names if normalized and
                       fold(name).startswith(normalized + ' ')]
    if len(matches) > 1:
        raise ValueError('Preciso ser mais específico: ' + ', '.join(matches) + '.')
    return matches[0] if matches else target


def normalize(game, command):
    command = ' '.join(command.lower().split())
    if not command:
        return command
    if game.get_current_room().room_id == 'E03' and command in ('examinar garagem', 'examinar a garagem'):
        return 'ir oeste'
    if game.get_current_room().room_id == 'B06':
        if command in ('ligar gerador', 'ligar gerador principal', 'restaurar energia'):
            return 'usar gerador principal'
        if command in ('instalar fusíveis', 'instalar fusíveis no quadro', 'instalar fusíveis no quadro elétrico'):
            return 'usar fusíveis no quadro elétrico'
    if command == 'caminhar até o portão':
        room = game.get_current_room()
        directions = [d for d in room.known_exits() if 'portão' in room.exit_names.get(d, '')]
        if len(directions) == 1:
            return 'ir ' + directions[0]
    attempt = re.fullmatch(r'(?:coletar|alcançar|alcancar)\s+(.+)', command)
    if attempt:
        target = resolve(game, attempt[1])
        obj = game.get_current_room().objects.get(target)
        if obj and obj.interaction == 'greenhouse_fall':
            return 'pegar ' + target
    if command in ('descer pelo poço', 'descer no poço', 'descer poço') and 'poço' in game.get_current_room().objects:
        return 'ir baixo'
    if command == 'olhar pela janela':
        return 'examinar ' + resolve(game, 'janela')
    if command in ('tocar a campainha', 'apertar campainha', 'apertar a campainha'):
        return 'tocar campainha'
    if command in ('me esquivar', 'desviar', 'desviar do golpe', 'esquivar do ataque'):
        return 'esquivar'
    if command in ('ligar uv', 'usar ultravioleta', 'mudar para uv', 'acender luz uv'):
        return 'uv'
    if command in ('mudar para luz normal', 'acender luz normal'):
        return 'normal'
    peek = re.fullmatch(r'(?:olhar pela fresta|espiar pela abertura|verificar se há movimento do outro lado)(?:\s+(?:da|do|de)\s+(.+))?', command)
    if peek:
        return 'espiar ' + resolve(game, peek[1] or 'porta')
    if command.startswith(('ouvir', 'escutar', 'encostar o ouvido', 'ver se tem alguém do outro lado')):
        target = re.sub(r'^(?:ouvir|escutar|encostar o ouvido|ver se tem alguém do outro lado)\s*', '', command)
        target = re.sub(r'^(?:atrás da|atras da|atrás de|atras de|na|no)\s+', '', target)
        return ('ouvir ' + resolve(game, target)).strip()
    cautious = re.search(r'\b(devagar|furtivamente|com cuidado|sem fazer barulho|silenciosamente)\b', command)
    if cautious or command.startswith('me esgueirar'):
        target = re.sub(r'\b(devagar|furtivamente|com cuidado|sem fazer barulho|silenciosamente)\b', '', command).strip()
        target = re.sub(r'^(?:me )?(?:entrar|passar|avançar|ir|seguir|esgueirar)\s*', '', target)
        target = re.sub(r'^(?:pela|pelo|por|na|no|para)\s+', '', target).strip()
        if target in game.get_current_room().known_exits():
            return 'esgueirar ' + target
        if not target and len(game.get_current_room().known_exits()) == 1:
            return 'esgueirar ' + next(iter(game.get_current_room().known_exits()))
        return ('esgueirar_porta ' + resolve(game, target)).strip()
    if command.startswith(('esconder ', 'me esconder ')):
        target = re.sub(r'^(?:me )?esconder\s+(?:(?:atrás de|atrás das|atrás dos|atrás da|atrás do|embaixo de|embaixo da|embaixo do|no|na|em)\s+)?', '', command)
        return 'esconder ' + resolve(game, target)
    if command.startswith(('entrar apressado', 'avançar depressa', 'correr')):
        target = re.sub(r'^(?:entrar apressado|avançar depressa|correr)\s*', '', command)
        target = re.sub(r'^(?:para|pela|pelo)\s+', '', target)
        direction = game.exploration.door_direction(resolve(game, target))
        return 'correr ' + (direction or target)
    if command == 'olhar em volta':
        return 'olhar'
    if command in ('inventario', 'abrir inventário', 'abrir inventario', 'abrir o inventário', 'abrir o inventario'):
        return 'inventário'
    if command in ('fechar inventario', 'fechar o inventário', 'fechar o inventario'):
        return 'fechar inventário'
    action, _, target = command.partition(' ')
    if command.startswith('dar uma olhada '):
        action, target = 'olhar', command[len('dar uma olhada '):]
    action = VERBS.get(action, action)
    target = re.sub(r'^(?:para|contra|em)\s+', '', target)
    target = re.sub(r'^(?:na|no|ao|à)\s+', '', target)
    if action == 'ver' and strip_article(target) != 'celular':
        action = 'examinar'
    if action in ('ir', 'andar', 'entrar'):
        direction = strip_article(target)
        if direction in ('norte', 'sul', 'leste', 'oeste', 'cima', 'baixo'):
            return 'ir ' + direction
        exits = [d for d, destination in game.get_current_room().known_exits().items()
                 if fold(game.get_room(destination).name.lower()) == fold(direction)]
        if len(exits) == 1:
            return 'ir ' + exits[0]
    if action in ('olhar', 'observar', 'examinar', 'inspecionar'):
        match = re.match(r'(?:atrás|atras|verso|o verso|dentro|interior|o interior)\s+(?:do|da|de)\s+(.+)', target)
        if match:
            face = 'interior' if target.startswith(('dentro', 'interior', 'o interior')) else 'back'
            return 'inspecionar ' + face + ' ' + resolve(game, match.group(1))
    if action == 'virar':
        return 'inspecionar back ' + resolve(game, target)
    if action == 'inspecionar':
        face, _, name = target.partition(' ')
        face = {'frente': 'front', 'verso': 'back', 'aberto': 'open', 'fechado': 'closed', 'danificado': 'damaged'}.get(face, face)
        if face in ('front', 'back', 'interior', 'open', 'closed', 'damaged'):
            name = re.sub(r'^(?:do|da|de)\s+', '', name)
            return 'inspecionar ' + face + ' ' + resolve(game, name)
        return 'examinar ' + resolve(game, target)
    if action in ('subir', 'descer') and strip_article(target) in ('', 'escada', 'escadas', 'escadaria'):
        return 'ir cima' if action == 'subir' else 'ir baixo'
    if command in ('ir para o andar de cima', 'ir andar superior', 'ir para o andar superior', 'ir andar de cima'):
        return 'ir cima'
    if command in ('voltar ao salão', 'voltar ao salao'):
        if game.get_current_room().room_id in ('upper_hall', 'U01'):
            return 'ir baixo'
        room = game.get_current_room()
        direction = next((d for d, destination in room.known_exits().items() if game.get_room(destination).room_id in ('main_hall', 'T02')), None)
        return 'ir ' + (direction or 'salão')
    if action in ('passar', 'atravessar', 'entrar'):
        target = re.sub(r'^(?:pela|pelo|por|na|no)\s+', '', target)
        return 'atravessar ' + resolve(game, target)
    if action == 'ajuda':
        return command
    if action in ('usar', 'tomar'):
        parts = re.split(r'\s+(?:em|no|na)\s+', target, maxsplit=1)
        return action + ' ' + ' no '.join(resolve(game, part) for part in parts)
    if action == 'digitar':
        parts = re.split(r'\s+(?:em|no|na)\s+', target, maxsplit=1)
        return action + ' ' + (parts[0] + ' no ' + resolve(game, parts[1]) if len(parts) == 2 else target)
    if action in {'examinar', 'observar', 'olhar', 'ler', 'pegar', 'apanhar', 'largar', 'soltar',
                  'equipar', 'segurar', 'abrir', 'fechar', 'forçar', 'forcar', 'recarregar', 'ligar',
                  'desligar', 'atacar', 'distrair'}:
        return (action + ' ' + resolve(game, target)).strip()
    return command
