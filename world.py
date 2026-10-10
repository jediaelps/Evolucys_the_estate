from confrontation import Enemy
from items import WeaponState, capabilities_for
from uuid import uuid4
from visual_assets import SpriteSpec, default_object_images


ROOM_ALIASES = {'entrance': 'T01', 'main_hall': 'T02', 'kitchen': 'T05',
                'office': 'T08', 'cellar': 'B07', 'upper_hall': 'U01'}
OFFICIAL_ROOM_IDS = frozenset(f'{sector}{n:02}' for sector, count in
                            [('E', 14), ('T', 12), ('U', 9), ('B', 10), ('L', 12), ('G', 1)]
                            for n in range(1, count + 1))


class PassageState:
    """Estado de uma ligação, compartilhado pelos lados registrados em Room."""
    def __init__(self, connection_id, *, kind='passage', known=True, enabled=True):
        if kind not in ('passage', 'fall'):
            raise ValueError('Unknown passage kind')
        self.connection_id = connection_id
        self.kind = kind
        self._known = known
        self.enabled = enabled
        self._sides = []

    def reveal(self):
        self._known = True
        for room, door in self._sides:
            if door is not None:
                room.add_object(door)

    @property
    def known(self):
        return self._known




class GameObject:
    def __init__(self, name, description, portable=False, locked=False, required_item=None,
                 contents=None, hidden_objects=None, code=None, openable=False,
                 weapon=None, ammo_count=0, text=None, blocked=False, accessible=True,
                 inaccessible_reason='Consigo ver, mas não alcanço daqui.',
                 object_id=None, document_type='bilhete', pages=None, lock_id=None,
                 key_lock_ids=None, permanent_key=False, inspection_faces=None, sprite=None,
                 capabilities=None, hiding_effectiveness=None, requires_light=False, requires_uv=False,
                 sight_gap=False, soundproof=False, sound_attenuation=2, interaction=None, aliases=()):
        self.interaction = interaction
        self.aliases = tuple(aliases)
        self.sight_gap = sight_gap
        self.soundproof = soundproof
        self.sound_attenuation = max(0, sound_attenuation)
        self.name = name
        self.description = description
        self.portable = portable
        self.locked = locked
        self.required_item = required_item
        self.opened = False
        self.contents = list(contents or [])
        self.hidden_objects = list(hidden_objects or [])
        self.code = code
        self.openable = openable or locked or bool(self.contents)
        self.weapon = weapon
        self.capabilities = capabilities or capabilities_for(name, weapon)
        self.hiding_effectiveness = hiding_effectiveness
        self.requires_light = requires_light
        self.requires_uv = requires_uv
        self.uv_enabled = False
        self.light_mode = 'normal'
        self.ammo_count = ammo_count
        self.light_on = False
        self.text = text
        self.blocked = blocked
        self.accessible = accessible
        self.inaccessible_reason = inaccessible_reason
        self.known_state = None
        self.object_id = object_id or uuid4().hex
        self.document_type = document_type
        self.additional_pages = list(pages or [])
        self.was_read = False
        self.read_pages = set()
        self.lock_id = lock_id
        self.key_lock_ids = set(key_lock_ids or [])
        self.permanent_key = permanent_key
        self.inspection_faces = dict(inspection_faces or {})
        self.inspected_faces = set()
        self.damaged = False
        self.sprite = sprite or SpriteSpec()
        self.sprite.object_id = self.object_id
        if sprite is None:
            self.sprite.images = default_object_images(self)

    @property
    def pages(self):
        return ([self.text] + self.additional_pages) if self.text is not None else []

    def read_page(self, index=0):
        page = self.pages[index]
        self.was_read = True
        self.read_pages.add(index)
        return page

    def passage_failure(self):
        self.known_state = 'bloqueada' if self.blocked else 'aberta' if self.opened else 'trancada' if self.locked else 'fechada'
        if not self.accessible:
            return self.inaccessible_reason
        if self.blocked:
            return 'Não vai abrir. Tem alguma coisa bloqueando do outro lado.'
        if self.opened:
            return ''
        if self.locked:
            return 'Está trancada. Preciso encontrar outra maneira.'
        if not self.opened:
            return ('Está fechada. Preciso abrir a porta antes de passar.' if self.name.startswith('porta')
                    else 'Está fechado. Preciso abrir antes de acessar o interior.')
        return ''

    def reveal_hidden(self, room):
        return self._reveal(self.hidden_objects, room)

    def reveal_contents(self, room):
        return self._reveal(self.contents, room)

    @staticmethod
    def _reveal(objects, room):
        names = [obj.name for obj in objects]
        for obj in objects:
            room.add_object(obj)
        objects.clear()
        return names

    def examine(self):
        text = self.description
        if self.text is not None and self.text != self.description:
            text += ' Há algo escrito; posso ler.'
        if self.openable:
            reason = self.passage_failure()
            text += ' ' + (reason or 'Está aberta; o acesso está livre.')
        if self.weapon:
            text += f" Munição: {self.weapon.ammo}/{self.weapon.spec.capacity}."
        if self.ammo_count:
            text += f" Cartuchos: {self.ammo_count}."
        return text


class Room:
    def __init__(self, room_id, name, description):
        self.room_id = room_id
        self.name = name
        self.description = description
        self.objects = {}
        self.exits = {}
        self.exit_doors = {}
        self.exit_names = {}
        self.exit_states = {}
        self.enemies = []
        self.dark = False
        self.ambient_noise = 0

    @property
    def enemy(self):
        return next((e for e in self.enemies if e.alive), self.enemies[0] if self.enemies else None)

    @enemy.setter
    def enemy(self, value):
        self.enemies = [value] if value else []

    def add_object(self, obj):
        self.objects[obj.name] = obj

    def add_exit(self, direction, room_id, door=None, name=None, *, state=None):
        self.exits[direction] = room_id
        if state is not None:
            self.exit_states[direction] = state
            state._sides.append((self, door))
        if name:
            self.exit_names[direction] = name
        if door is not None:
            self.exit_doors[direction] = door
            if state is None or state.known:
                self.add_object(door)

    def connect(self, other, direction, *, reverse=None, door=None, name=None,
                reverse_name=None, state=None):
        """Liga Rooms existentes; só cria retorno quando explicitamente pedido."""
        if state is None:
            ids = sorted(ROOM_ALIASES.get(r.room_id, r.room_id) for r in (self, other))
            state = PassageState('C_' + '_'.join(ids))
        if state.kind == 'fall' and reverse is not None:
            raise ValueError('A fall cannot create a return passage')
        self.add_exit(direction, other.room_id, door, name, state=state)
        if reverse is not None:
            other.add_exit(reverse, self.room_id, door, reverse_name, state=state)
        return state

    def known_exits(self):
        return {key: destination for key, destination in self.exits.items()
                if key not in self.exit_states or
                (self.exit_states[key].known and self.exit_states[key].kind != 'fall')}

    def passage_failure(self, direction):
        if direction not in self.known_exits():
            return 'Não há caminho por aí.'
        state = self.exit_states.get(direction)
        if state is not None and not state.enabled:
            return 'Não consigo passar por aqui ainda.'
        door = self.exit_doors.get(direction)
        return door.passage_failure() if door else ''

    def describe(self, game=None):
        text = self.description
        from target_selection import label
        for enemy in self.enemies:
            if enemy.sprite.visible and enemy.in_sight and (game is None or not self.dark
                    or game.light_visible or any(o.light_on for o in self.objects.values())):
                description = enemy.describe(label(self, enemy))
                if len(self.enemies)>1:
                    description += ' Está ' + enemy.distance + '.'
                text += '\n' + description
        return text


def create_world(configuration='campaign'):
    if configuration not in ('campaign', 'prototype'):
        raise ValueError('Unknown world configuration')
    rooms = {}

    entrance = Room(
        "entrance",
        "Entrada da Mansão",
        "A chuva bate violentamente nas janelas. "
        "O ar dentro da mansão é frio e cheira a madeira úmida. "
        "A porta atrás de Joseph parece ter travado."
    )
    entrance.add_object(GameObject(
        "porta principal",
        "Uma pesada porta de madeira. A fechadura parece ter sido danificada.",
        openable=True, blocked=True
    ))
    entrance.add_object(GameObject(
        "mesa",
        "Uma pequena mesa coberta de poeira. Há marcas recentes sobre sua superfície."
    ))
    entrance.add_object(GameObject(
        "lanterna",
        "Uma lanterna pequena. Ainda parece funcionar.",
        portable=True
    ))
    entrance.add_exit("norte", "main_hall")
    rooms["entrance"] = entrance

    main_hall = Room(
        "main_hall",
        "Salão Principal",
        "Um enorme salão ocupa o centro da mansão. "
        "Uma escadaria leva ao andar superior. Retratos antigos cobrem as paredes."
    )
    main_hall.add_object(GameObject(
        "retrato",
        "O retrato mostra uma família diante da mansão. "
        "O rosto de uma das pessoas foi riscado violentamente."
    ))
    main_hall.add_object(GameObject(
        "gaveta",
        "Uma pequena gaveta embutida em um móvel antigo. Ela parece estar emperrada.",
        locked=True,
        required_item="pé de cabra"
    ))
    main_hall.add_exit("sul", "entrance")
    main_hall.add_exit("oeste", "kitchen")
    main_hall.add_exit("leste", "office")
    rooms["main_hall"] = main_hall

    kitchen = Room(
        "kitchen",
        "Cozinha",
        "Pratos quebrados estão espalhados pelo chão. "
        "Há comida apodrecida sobre a bancada."
    )
    kitchen.add_object(GameObject(
        "pé de cabra",
        "Um pé de cabra enferrujado, mas resistente. Pode ser útil para forçar alguma coisa.",
        portable=True
    ))
    kitchen.add_object(GameObject(
        "chá",
        "Um pequeno recipiente de chá. O cheiro lembra alguma coisa familiar para Joseph.",
        portable=True
    ))
    kitchen.add_exit("leste", "main_hall")
    rooms["kitchen"] = kitchen

    office = Room(
        "office",
        "Escritório",
        "Livros e documentos estão espalhados pelo chão. "
        "Um computador antigo permanece desligado sobre uma mesa."
    )
    office.add_object(GameObject(
        "documento",
        "O documento menciona testes clínicos e utiliza repetidamente a palavra 'EVOLUCYS'.",
        portable=True
    ))
    office.add_exit("oeste", "main_hall")
    rooms["office"] = office

    # Cada etapa libera a pista ou ferramenta necessária à próxima.
    main_hall.objects["retrato"].hidden_objects.append(GameObject(
        "inscrição", "Atrás do retrato: 'O arquivo repousa sob a casa. "
        "A gaveta guarda a chave do armário do escritório.'"
    ))
    main_hall.objects["retrato"].description += " Há marcas sob a moldura solta."
    main_hall.objects["gaveta"].contents.append(GameObject(
        "chave do armário", "Uma chave de latão marcada ESCRITÓRIO.", portable=True
    ))
    office.add_object(GameObject(
        "armário", "Um armário de documentos com fechadura de latão.",
        locked=True, required_item="chave do armário", contents=[GameObject(
            "bilhete", "O bilhete diz: 'Cofre: lote 0417. Digite os quatro algarismos.'",
            portable=True
        )]
    ))
    office.add_object(GameObject(
        "cofre", "Um cofre com teclado de quatro algarismos.",
        locked=True, code="0417", contents=[GameObject(
            "chave do porão", "Uma chave de ferro marcada PORÃO.", portable=True
        )]
    ))
    cellar_door = GameObject(
        "porta do porão", "Uma porta de ferro ao norte do salão. A placa diz ARQUIVO.",
        locked=True, required_item="chave do porão"
    )
    cellar_door.sight_gap = True  # Fresta já descrita no protótipo.
    cellar_door.description += " Pela fresta, um vigia ronda de costas. Use esgueirar norte para entrar sem ser visto."
    main_hall.add_exit("norte", "cellar", cellar_door)
    cellar = Room("cellar", "Arquivo do Porão",
                  "Joseph desce os degraus. Pastas de pacientes cobrem as estantes. "
                  "Uma delas traz seu nome.")
    cellar.add_object(GameObject(
        "pasta de joseph", "A pasta revela: 'Joseph — sujeito do programa EVOLUCYS. "
        "Transferência autorizada para a ala superior.' O próximo destino está definido."
    ))
    # A mesma porta controla os dois sentidos da passagem.
    cellar.add_exit("sul", "main_hall", cellar_door)
    cellar.enemy = Enemy("vigia")
    rooms["cellar"] = cellar

    # A escadaria descrita no salão é uma conexão real e bidirecional.
    stairs = GameObject('escadaria', 'Uma escadaria firme liga o salão ao corredor superior.', openable=True)
    stairs.opened = True
    main_hall.add_exit('cima', 'upper_hall', stairs)
    upper = Room('upper_hall', 'Corredor Superior',
                 'Tábuas rangem sob os passos. A chuva bate nas janelas. '
                 'Uma porta de quarto está trancada; a escadaria permite retornar ao salão.')
    upper.add_object(GameObject('janela', 'Gotas escorrem pelo vidro. A janela está selada e não serve de passagem.'))
    upper.add_object(GameObject('quadro antigo', 'Uma paisagem desbotada em uma moldura rachada.'))
    upper.add_object(GameObject('porta de quarto', 'Uma porta trancada. Esta ala ainda está inacessível.', locked=True))
    upper.add_exit('baixo', 'main_hall', stairs)
    rooms['upper_hall'] = upper

    # Recursos finitos; nenhum reaparece ao revisitar os cômodos.
    for room in (entrance, kitchen):
        room.add_object(GameObject("bandagem", "Uma bandagem limpa para ferimentos leves.", portable=True))
    kitchen.add_object(GameObject("energético", "Uma lata de energético ainda lacrada.", portable=True))
    office.objects["armário"].contents.extend([
        GameObject("spray de cura", "Um spray medicinal com poucas aplicações.", portable=True),
        GameObject("munição de pistola", "Uma pequena caixa de cartuchos.", portable=True, ammo_count=3),
    ])
    office.objects["cofre"].contents.append(GameObject(
        "pistola", "Uma pistola antiga. Cada cartucho precisa valer a pena.",
        portable=True, weapon=WeaponState()))
    cellar.add_object(GameObject("caixa médica", "Uma caixa de emergência esquecida entre as estantes.",
        contents=[GameObject("kit médico", "Um kit completo, difícil de encontrar.", portable=True)]))

    # Mantém as descrições anteriores e dá conteúdo legível aos documentos existentes.
    def mark_documents(obj):
        if obj.name in {'documento', 'bilhete', 'inscrição', 'pasta de joseph'}:
            obj.text = obj.description
        for child in obj.contents + obj.hidden_objects:
            mark_documents(child)
    for room in rooms.values():
        for obj in room.objects.values():
            mark_documents(obj)
    office.objects['armário'].lock_id = 'office.cabinet'
    cellar_door.lock_id = 'cellar.door'
    for obj in main_hall.objects['gaveta'].contents:
        if obj.name == 'chave do armário':
            obj.key_lock_ids = {'office.cabinet'}
    for obj in office.objects['cofre'].contents:
        if obj.name == 'chave do porão':
            obj.key_lock_ids = {'cellar.door'}
    office.objects['documento'].document_type = 'relatório'
    office.objects['documento'].text += '\n\nPROJETO EVOLUCYS\nObservação clínica: registro incompleto.\nResponsável: assinatura ilegível.'
    cellar.objects['pasta de joseph'].document_type = 'pasta'
    portrait = main_hall.objects['retrato']
    portrait.inspection_faces = {'front': portrait.description,
                                'back': portrait.hidden_objects[0].text}
    main_hall.objects['gaveta'].inspection_faces = {
        'front': 'A madeira da gaveta está marcada pelo tempo.',
        'interior': 'O fundo de madeira tem riscos antigos.',
        'open': 'A gaveta está aberta.', 'closed': 'A gaveta permanece fechada.'}
    if configuration == 'campaign':
        _configure_campaign(rooms)
    return rooms


def _configure_campaign(rooms):
    """Térreo e andar superior 5.1E; conteúdo legado ainda provisório."""
    rooms['entrance'].name = 'Vestíbulo'
    rooms['upper_hall'].name = 'Galeria Superior'
    for room_id, name, description in (
        ('T03', 'Sala de Estar',
         'O cheiro de tecido úmido paira no ar. A luz cinzenta das janelas '
         'alcança apenas parte da sala; o assoalho range a cada passo.'),
        ('T04', 'Sala de Jantar',
         'Uma mesa comprida ocupa o centro da sala. Sob a poeira, o brilho '
         'da madeira quase desapareceu. O silêncio amplia o som dos passos.'),
        ('T06', 'Despensa',
         'O espaço é estreito e o ar, abafado. Prateleiras gastas acompanham '
         'as paredes; o cheiro antigo de mantimentos se mistura à umidade.'),
        ('T07', 'Lavanderia',
         'O ar frio tem um leve cheiro de sabão antigo. Manchas de umidade '
         'escurecem as paredes, e a luz esbranquiçada deixa o piso sem brilho.'),
        ('T09', 'Biblioteca',
         'O cheiro de papel envelhecido impregna o ambiente. Estantes altas '
         'limitam a luz, deixando sombras compridas sobre o piso.'),
        ('T10', 'Sala de Música',
         'A madeira do piso está gasta. Cortinas pesadas abafam a chuva, '
         'e o silêncio parece mais denso neste cômodo de teto alto.'),
        ('T11', 'Banheiro Social',
         'Azulejos opacos revestem as paredes. A louça perdeu o brilho e '
         'o ar frio retém um cheiro persistente de umidade.'),
        ('T12', 'Sala de Manutenção',
         'A pintura descascada expõe a aspereza das paredes. O cheiro de '
         'metal velho se mistura à poeira neste espaço de serviço pouco iluminado.'),
        ('U02', 'Quarto Principal',
         'A luz atravessa o tecido gasto das cortinas. O quarto amplo cheira '
         'a madeira antiga, e uma camada de poeira suaviza os contornos do piso.'),
        ('U03', 'Quarto de Hóspedes',
         'O papel de parede se desprende nos cantos. O ar está parado, '
         'com um cheiro tênue de tecido guardado por muito tempo.'),
        ('U04', 'Quarto Infantil',
         'Restos de tinta clara cobrem as paredes. A chuva soa distante '
         'neste quarto pequeno, onde a luz deixa o assoalho pálido.'),
        ('U05', 'Banheiro Superior',
         'O esmalte da louça está opaco. A umidade escureceu as juntas '
         'dos azulejos e o frio parece preso entre as paredes.'),
        ('U06', 'Estudo Privado',
         'A madeira escura absorve a pouca luz. O cheiro seco de poeira '
         'se concentra neste cômodo silencioso, afastado do salão.'),
        ('U07', 'Depósito Superior',
         'O espaço é apertado, com paredes ásperas e marcas de desgaste. '
         'O ar abafado traz o cheiro da madeira envelhecida.'),
        ('U08', 'Varanda Superior',
         'O vento frio leva gotas de chuva para o piso. A umidade escurece '
         'a pedra, e a luz de fora contrasta com a penumbra da galeria.'),
        ('U09', 'Sótão',
         'O teto inclinado aproxima as vigas do chão. O cheiro de madeira '
         'seca domina o ar, enquanto a chuva ressoa acima de Joseph.'),
    ):
        rooms[room_id] = Room(room_id, name, description)

    hall, cellar, upper = (rooms[key] for key in ('main_hall', 'cellar', 'upper_hall'))
    cellar_door = hall.exit_doors['norte']
    stairs = hall.exit_doors['cima']
    # Reconecta as mesmas instâncias; nenhum inventário/objeto é redistribuído.
    for room in rooms.values():
        room.exits.clear()
        room.exit_names.clear()
        room.exit_doors.clear()
        room.exit_states.clear()

    rooms['entrance'].connect(hall, 'norte', reverse='sul',
                             name='passagem para o salão principal',
                             reverse_name='passagem para o vestíbulo')
    hall.connect(rooms['office'], 'leste', reverse='oeste',
                 name='passagem para o escritório', reverse_name='passagem para o salão principal')
    hall.connect(upper, 'cima', reverse='baixo', door=stairs,
                 name='escadaria principal', reverse_name='escadaria para o salão principal')
    # A porta provisória ganha destino real somente na campanha.
    bedroom_door = upper.objects['porta de quarto']
    bedroom_door.description = 'Uma porta de madeira liga a galeria ao quarto principal.'
    bedroom_door.locked = False
    bedroom_door.opened = True
    upper.description = ('Tábuas rangem sob os passos. A chuva bate nas janelas. '
                         'A galeria acompanha os quartos; a escadaria permite retornar ao salão.')
    upper.connect(rooms['U02'], 'via_u02', reverse='via_u01', door=bedroom_door,
                  name='porta para o quarto principal', reverse_name='porta para a galeria superior')

    for origin, destination in (
        ('main_hall', 'T03'), ('main_hall', 'T04'), ('main_hall', 'T11'),
        ('T03', 'T04'), ('T04', 'kitchen'), ('kitchen', 'T06'), ('office', 'T09'),
        # Passagens comuns provisoriamente disponíveis para exploração.
        ('kitchen', 'T07'), ('T09', 'T10'), ('main_hall', 'T12'),
        ('upper_hall', 'U03'), ('upper_hall', 'U04'), ('upper_hall', 'U08'),
        ('U02', 'U06'), ('U03', 'U05'), ('U06', 'U07'), ('U07', 'U09'),
    ):
        a, b = rooms[origin], rooms[destination]
        a.connect(b, 'via_' + ROOM_ALIASES.get(destination, destination).lower(),
                  reverse='via_' + ROOM_ALIASES.get(origin, origin).lower(),
                  name='passagem para ' + b.name.lower(),
                  reverse_name='passagem para ' + a.name.lower())

    library_door = GameObject('porta da biblioteca',
                             'A porta entre o salão e a biblioteca permanece fechada.',
                             openable=True, blocked=True, object_id='C_T02_T09.door')
    hall.connect(rooms['T09'], 'via_t09', reverse='via_t02', door=library_door,
                 name='porta da biblioteca', reverse_name='porta para o salão principal',
                 state=PassageState('C_T02_T09', enabled=False))
    cellar_door.blocked = True
    cellar_door.description = 'Uma porta de ferro fecha a antiga escadaria do porão. A placa diz ARQUIVO.'
    hall.connect(cellar, 'norte', reverse='sul', door=cellar_door,
                 name='antiga escadaria do porão', reverse_name='antiga escadaria para o salão principal',
                 state=PassageState('C_B07_T02', enabled=False))
    service_door = GameObject('porta de serviço',
                             'Uma porta fechada separa a cozinha da sala de manutenção.',
                             openable=True, blocked=True, object_id='C_T05_T12.door')
    rooms['kitchen'].connect(rooms['T12'], 'via_t12', reverse='via_t05', door=service_door,
                            name='porta de serviço para a sala de manutenção',
                            reverse_name='porta de serviço para a cozinha',
                            state=PassageState('C_T05_T12', enabled=False))

    # Exterior 5.1H: início canônico e continuidade subterrânea autorizada.
    for room_id, name, description in (
        ('E01', 'Estrada / Carro',
         'O carro está parado junto à estrada estreita. Neste fim de tarde do ano 2000, '
         'a chuva embaça os vidros e o céu perde a cor. O mato alto encobre as margens; '
         'além do ruído das gotas na lataria, não se ouve trânsito.'),
        ('E02', 'Portão da Propriedade',
         'O portão de ferro permanece aberto entre pilares antigos, manchados de umidade. '
         'Trepadeiras se enroscam nas grades. A estrada fica para trás, enquanto a chuva '
         'faz as folhas roçarem umas nas outras do lado de dentro.'),
        ('E03', 'Caminho Frontal',
         'O cascalho molhado cede sob os passos. A vegetação avança sobre o caminho '
         'e a mansão surge ao fundo, sob o céu que escurece. O vento traz o cheiro de '
         'terra encharcada; o som distante da estrada quase desapareceu.'),
        ('E04', 'Varanda da Mansão',
         'A cobertura antiga abriga apenas parte da varanda. Água escorre pelas colunas '
         'e se acumula nas pedras gastas. A porta principal está fechada; junto à parede, '
         'o cheiro de madeira úmida se mistura ao ar frio da chuva.'),
        ('E05', 'Lateral da Casa',
         'O caminho se estreita junto à parede da mansão. Galhos pesados de água '
         'se inclinam sobre a passagem, e a pintura descascada deixa a alvenaria exposta. '
         'Aqui, o vento se reduz a um sopro entre a casa e a vegetação.'),
        ('E06', 'Fundos da Propriedade',
         'O terreno nos fundos está tomado por capim alto e poças escuras. As paredes '
         'antigas protegem parte do pátio do vento, mas a chuva continua batendo nos '
         'telhados. A entrada de serviço permanece fechada, e a estrada já não é visível.'),
        ('E07', 'Casinha de Ferramentas',
         'A pequena construção tem cheiro de madeira envelhecida e terra molhada. '
         'A luz cinzenta alcança o assoalho gasto e as paredes manchadas. Gotas ressoam '
         'no telhado; entre uma rajada de vento e outra, o espaço fica quieto.'),
        ('E08', 'Estufa Abandonada',
         'A armação antiga da estufa se perde entre folhas crescidas sem cuidado. '
         'A chuva marca os vidros opacos, e a umidade deixa o ar pesado. Sob o céu '
         'escuro, sombras de galhos cobrem o piso irregular.'),
        ('E09', 'Área do Gerador Externo',
         'Uma cobertura baixa protege a antiga instalação do gerador. O metal está '
         'marcado pela ferrugem e não há vibração de motor. A água pinga nas bordas '
         'do abrigo; além dele, o mato alto encobre o restante do terreno.'),
    ):
        rooms[room_id] = Room(room_id, name, description)

    rooms['E01'].description = ('Ano 2000. Joseph, um empresário adulto, interrompeu a viagem com o pneu estragado. '
        'É fim de tarde; nuvens carregadas anunciam uma tempestade e as primeiras gotas batem na lataria. '
        'Ao norte, em frente, um caminho entre o mato conduz a um portão; a silhueta de uma mansão '
        'se destaca ao longe contra o céu escurecendo. A estrada está deserta. Talvez haja alguém lá que possa ajudar.')
    rooms['E02'].description = ('O mato alto acompanha o caminho à esquerda e à direita. '
        'O chão irregular dificulta os passos, e o vento agita os galhos. À frente, ao norte, '
        'o portão antigo está aberto; a mansão aparece mais nítida entre as grades molhadas.')
    rooms['E03'].description = ('Do lado de dentro do portão, Joseph vê a fachada deteriorada da mansão. '
        'Duas estátuas antigas de cães guardam os degraus da varanda. Uma cerca viva acompanha '
        'a lateral leste; a chuva escorre pelo cascalho do caminho frontal.')
    rooms['E04'].description += ' Ao lado da porta há uma campainha.'
    rooms['E06'].description = ('As janelas traseiras estão opacas de sujeira. A porta de serviço permanece '
        'fechada. A chuva corre pelos beirais; de um lado fica o pátio da casinha e, do outro, '
        'um trecho de jardim onde se veem a estufa e o poço.')
    rooms['E07'].description += ' Um macaco de carro repousa num canto, sem a manivela.'
    rooms['E08'].description = ('Plantas crescem entre vasos rachados e utensílios de jardinagem. Vidros sujos, alguns quebrados, '
        'cobrem a armação enferrujada. Sobre uma mesa repousa uma barra de aço dobrada, como uma manivela. '
        'O piso de madeira está escurecido e deteriorado; o ar cheira a terra úmida.')
    for rid, name, description in (
        ('E10', 'Jardim da Fonte', 'A água da chuva escorre pela fonte antiga. Folhas cobrem a borda '
         'de pedra; a cerca viva separa o jardim do corredor lateral. O caminho retorna ao acesso dos fundos.'),
        ('E11', 'Corredor do Jardim', 'Uma passagem estreita contorna a cerca viva. De um lado fica '
         'o jardim com a fonte; adiante, o caminho alcança o pátio da casinha de ferramentas.'),
        ('E12', 'Pátio da Casinha', 'A casinha de ferramentas aparece junto ao limite do jardim. '
         'Seu acesso está livre. A trilha molhada segue até as janelas dos fundos da mansão.'),
        ('E13', 'Jardim da Estufa e do Poço', 'A estufa abandonada fica ao lado de um poço de pedra. '
         'Hera cobre parte da borda, e o vento move o mato entre os dois. O caminho de volta '
         'acompanha as janelas dos fundos da mansão.'),
        ('B01', 'Câmara sob a Estufa', 'Uma luz fraca atravessa a abertura alta no teto. Poeira e lascas de madeira cobrem '
         'o chão da câmara úmida; o silêncio pesa entre as paredes. O buraco está fora de alcance. '
         'Um túnel antigo se afasta na penumbra.'),
        ('B02', 'Túnel Antigo', 'Raízes atravessam as juntas do túnel. Uma passagem lateral termina '
         'num acesso fechado junto à base do poço; deste lado há uma trava simples. '
         'Adiante, a alvenaria continua até o corredor de serviço da mansão.'),
        ('B03', 'Corredor de Serviço', 'A umidade marca as paredes do corredor subterrâneo. '
         'O túnel retorna sob o jardim, enquanto uma escadaria sobe até a sala de manutenção.'),
    ):
        rooms[rid] = Room(rid, name, description)
    gate = GameObject('portão', 'O portão está aberto; o caminho continua até a frente da mansão.', openable=True)
    gate.opened = True
    rooms['E01'].connect(rooms['E02'], 'norte', reverse='sul',
        name='caminho em frente até o portão', reverse_name='estrada junto ao carro')
    rooms['E02'].connect(rooms['E03'], 'norte', reverse='sul', door=gate,
        name='portão em frente para o caminho frontal', reverse_name='caminho até o portão para a estrada')
    for a, b, outward, back in (
        ('E03', 'E04', 'passagem até a varanda da mansão', 'caminho frontal'),
        ('E03', 'E05', 'caminho para a lateral leste da casa junto à mansão', 'caminho frontal'),
        ('E05', 'E11', 'corredor de acesso aos fundos e ao jardim', 'caminho para a lateral da casa'),
        ('E11', 'E10', 'caminho para o jardim da fonte', 'corredor de acesso aos fundos'),
        ('E11', 'E12', 'caminho até o pátio da casinha', 'corredor do jardim'),
        ('E12', 'E07', 'entrada da casinha de ferramentas', 'pátio da casinha'),
        ('E12', 'E06', 'caminho aos fundos da propriedade', 'pátio da casinha'),
        ('E06', 'E13', 'jardim da estufa e do poço', 'caminho aos fundos da propriedade'),
        ('E13', 'E08', 'entrada da estufa', 'jardim do poço'),
        ('E06', 'E09', 'caminho até a área do gerador externo', 'caminho aos fundos da propriedade'),
        ('B01', 'B02', 'túnel antigo', 'câmara sob a estufa'),
        ('B02', 'B03', 'corredor de serviço', 'túnel antigo'),
    ):
        rooms[a].connect(rooms[b], 'via_' + b.lower(), reverse='via_' + a.lower(),
                         name=outward, reverse_name=back)
    rooms['B03'].connect(rooms['T12'], 'cima', reverse='baixo',
        name='escadaria para a sala de manutenção', reverse_name='escadaria para o corredor de serviço')
    rooms['E08'].connect(rooms['B01'], 'queda', state=PassageState('C_B01_E08', kind='fall'))
    well_door = GameObject('acesso do poço', 'Uma abertura fechada na base do poço.',
        locked=True, openable=True, interaction='well_access', object_id='C_B02_E13.door')
    rooms['E13'].connect(rooms['B02'], 'baixo', reverse='cima', door=well_door,
        name='escada pelo poço', reverse_name='escada para o poço',
        state=PassageState('C_B02_E13', known=False, enabled=False))
    # O lado interno vê a trava, sem revelar a rota para quem está no jardim.
    rooms['B02'].add_object(well_door)
    rooms['E04'].add_object(GameObject('campainha', 'Uma campainha antiga junto à porta.', interaction='doorbell'))
    rooms['E01'].add_object(GameObject('carro', 'O carro ficou parado na margem. Um dos pneus está rasgado e a roda se apoia torta no cascalho.'))
    rooms['E01'].add_object(GameObject('pneu', 'A borracha está rasgada.\nJoseph: “Vou precisar de ferramentas adequadas para trocar essa roda.”', aliases=('roda',)))
    rooms['E01'].add_object(GameObject('mansão', 'Uma construção grande recorta o horizonte além do mato.\nJoseph: “Talvez tenha alguém lá. Vale tentar pedir ajuda.”'))
    for rid in ('E03', 'E04'):
        rooms[rid].add_object(GameObject('fachada', 'A pintura se desprende das paredes antigas. Trepadeiras alcançam as janelas escuras; a casa parece abandonada há muito tempo.', aliases=('mansão',)))
    for rid in ('E08', 'E13'):
        rooms[rid].add_object(GameObject('estufa', 'A armação enferrujada sustenta vidros sujos e quebrados. Folhas crescem sem controle no interior.'))
    rooms['E06'].add_object(GameObject('janela', 'Pelo vidro sujo, não consigo distinguir o interior. A janela está fechada.'))
    rooms['E07'].add_object(GameObject('macaco', 'Um macaco de carro, com o encaixe vazio.\nJoseph: “Falta a manivela. Poderia servir para trocar o pneu, se eu encontrasse a peça certa.”',
        portable=True, interaction='jack', object_id='campaign.jack'))
    rooms['E08'].add_object(GameObject('mesa', 'Uma mesa de jardinagem sustenta a manivela. As tábuas do piso ao redor estão apodrecidas.'))
    rooms['E08'].add_object(GameObject('vasos', 'Vasos de jardinagem rachados, cheios de terra endurecida.'))
    rooms['E08'].add_object(GameObject('manivela', 'Uma barra de aço dobrada, com uma extremidade gasta. Parece uma manivela, mas não está presa a nada.',
        portable=True, interaction='greenhouse_fall', object_id='campaign.jack_handle',
        aliases=('barra de aço', 'barra de aço do macaco', 'barra do macaco', 'manivela do macaco', 'barra de ferro')))
    rooms['E13'].add_object(GameObject('poço', 'Um poço fundo, cercado por pedras molhadas.', interaction='well'))

    # Sem estado por lado: mantém ambos bloqueados até a definição interna.
    main_door = rooms['entrance'].objects['porta principal']
    main_door.locked = True
    rooms['E04'].connect(rooms['entrance'], 'via_t01', reverse='via_e04', door=main_door,
                         name='porta principal da mansão', reverse_name='porta principal para a varanda',
                         state=PassageState('C_E04_T01', enabled=False))
    laundry_door = GameObject('porta da lavanderia',
                             'Uma porta de serviço fechada liga os fundos à lavanderia.',
                             openable=True, blocked=True, object_id='C_E06_T07.door')
    rooms['E06'].connect(rooms['T07'], 'via_t07', reverse='via_e06', door=laundry_door,
                         name='porta de serviço da lavanderia', reverse_name='porta para os fundos da propriedade',
                         state=PassageState('C_E06_T07', enabled=False))

    # Porão 5.1I: B07 continua sendo a mesma sala legada, com seu conteúdo.
    for room_id, name, description in (
        ('B04', 'Depósito Subterrâneo',
         'A umidade escureceu o reboco do depósito. Marcas retangulares no chão '
         'empoeirado contrastam com as manchas que descem pelas paredes.'),
        ('B05', 'Sala da Caldeira',
         'A caldeira antiga ocupa boa parte da sala. Tubos enferrujados sobem '
         'até o teto baixo; o ar frio guarda um cheiro de metal úmido.'),
        ('B06', 'Sala Elétrica',
         'Painéis antigos cobrem uma parede, com a pintura rachada pela umidade. '
         'Conduítes percorrem o teto e desaparecem na alvenaria deteriorada.'),
        ('B08', 'Adega',
         'Fileiras de nichos vazios se perdem na penumbra. O piso irregular '
         'retém a umidade, e o cheiro de madeira envelhecida pesa no ar.'),
        ('B09', 'Oficina',
         'Bancadas gastas acompanham as paredes da oficina. A ferrugem mancha '
         'os suportes de metal, sob tubulações que atravessam o teto.'),
        ('B10', 'Câmara Fria',
         'O revestimento claro está amarelado e rachado. O ar permanece frio '
         'entre as paredes espessas; gotas se acumulam junto ao rodapé.'),
    ):
        rooms[room_id] = Room(room_id, name, description)
    for origin, destination in (
        ('B03', 'B04'), ('B03', 'B05'), ('B03', 'B09'), ('B05', 'B06'),
        ('B06', 'cellar'), ('cellar', 'B08'), ('B09', 'B10'),
    ):
        a, b = rooms[origin], rooms[destination]
        a.connect(b, 'via_' + ROOM_ALIASES.get(destination, destination).lower(),
                  reverse='via_' + ROOM_ALIASES.get(origin, origin).lower(),
                  name='passagem para ' + b.name.lower(),
                  reverse_name='passagem para ' + a.name.lower())
    for origin, destination, name in (
        ('B04', 'B09', 'porta de serviço'),
        ('B08', 'B10', 'corredor de armazenamento'),
    ):
        a, b = rooms[origin], rooms[destination]
        connection_id = 'C_' + origin + '_' + destination
        door = GameObject(name, 'O acesso permanece bloqueado.', openable=True,
                          blocked=True, object_id=connection_id + '.door')
        a.connect(b, 'via_' + destination.lower(), reverse='via_' + origin.lower(), door=door,
                  name=name + ' para ' + b.name.lower(),
                  reverse_name=name + ' para ' + a.name.lower(),
                  state=PassageState(connection_id, enabled=False))

    # Laboratório 5.1J: estrutura ambiental, sem liberação da entrada secreta.
    for room_id, name, description in (
        ('L01', 'Acesso Oculto',
         'O concreto estreita a passagem. Além da alvenaria antiga, um revestimento '
         'descascado revela instalações de outra época sob a propriedade.'),
        ('L02', 'Corredor do Laboratório',
         'Faixas desbotadas acompanham o corredor. Tubulações expostas e luminárias '
         'opacas se repetem sob o teto, entre manchas de infiltração.'),
        ('L03', 'Recepção Técnica',
         'Um balcão revestido de fórmica ocupa a recepção. Atrás dele, marcas na '
         'parede indicam placas removidas; o ar tem um odor tênue de desinfetante velho.'),
        ('L04', 'Sala de Observação',
         'Um vidro espesso toma parte da parede. A superfície turva devolve apenas '
         'reflexos imprecisos; suportes vazios permanecem fixados diante dele.'),
        ('L05', 'Laboratório Principal',
         'Bancadas compridas dividem o salão. Cuba após cuba, o metal está manchado '
         'e os encaixes de antigos aparelhos acumulam poeira.'),
        ('L06', 'Laboratório Biológico',
         'Recipientes vazios repousam atrás de vidro opaco. Crostas secas marcam '
         'as cubas, sob antigos dutos de ventilação cobertos de ferrugem.'),
        ('L07', 'Enfermaria e Cirurgia',
         'Uma luminária articulada pende sobre uma mesa de metal. Cortinas rígidas '
         'de sujeira separam espaços estreitos, entre azulejos rachados.'),
        ('L08', 'Câmara de Contenção',
         'Paredes reforçadas cercam o espaço. Marcas profundas interrompem a '
         'pintura junto ao piso; pequenas aberturas são protegidas por vidro espesso.'),
        ('L09', 'Biotério',
         'Fileiras de compartimentos vazios ocupam as paredes. Grades corroídas '
         'e canaletas ressecadas conservam um cheiro acre, difícil de identificar.'),
        ('L10', 'Controle de Energia',
         'Painéis fechados cobrem a parede, com inscrições quase apagadas. '
         'Cabos grossos desaparecem em canaletas sob uma camada de pó.'),
        ('L11', 'Arquivo Científico',
         'Estantes metálicas vazias deixam corredores apertados. Etiquetas '
         'ilegíveis se soltam das bordas, e a umidade ondulou o revestimento das paredes.'),
        ('L12', 'Rota de Fuga',
         'O corredor termina num fechamento pesado de concreto e metal. '
         'A ventilação sopra fracamente por uma grelha alta; não há saída transitável adiante.'),
    ):
        rooms[room_id] = Room(room_id, name, description)
    for origin, destination in (
        ('L01', 'L02'), ('L02', 'L03'), ('L03', 'L04'), ('L04', 'L05'),
        ('L05', 'L06'), ('L06', 'L09'), ('L09', 'L11'), ('L05', 'L07'),
        ('L07', 'L08'), ('L08', 'L11'), ('L03', 'L10'), ('L10', 'L05'), ('L11', 'L12'),
    ):
        a, b = rooms[origin], rooms[destination]
        # Nome local preserva também a expressão natural "sala de contenção".
        outward = b.name.lower() + (' / sala de contenção' if destination == 'L08' else '')
        back = a.name.lower() + (' / sala de contenção' if origin == 'L08' else '')
        a.connect(b, 'via_' + destination.lower(), reverse='via_' + origin.lower(),
                  name='passagem para ' + outward, reverse_name='passagem para ' + back)
    laboratory_door = GameObject('porta do laboratório',
        'Uma porta reforçada mantém o acesso fechado.', openable=True, locked=True,
        blocked=True, object_id='C_B10_L01.door')
    rooms['B10'].connect(rooms['L01'], 'via_l01', reverse='via_b10', door=laboratory_door,
        name='porta para o acesso oculto do laboratório', reverse_name='porta para a câmara fria',
        state=PassageState('C_B10_L01', known=False, enabled=False))

    garage = Room('G01', 'Garagem',
        'Dois carros antigos repousam sob uma camada espessa de poeira. Bancadas e armários '
        'acompanham as paredes, entre ferramentas enferrujadas e peças automotivas. '
        'Duas grandes portas externas fecham a frente da garagem. O ar parado cheira a óleo velho.')
    rooms['G01'] = garage
    rooms['B06'].add_object(GameObject('quadro elétrico',
        'O quadro do gerador principal tem encaixes vazios. Faltam os fusíveis.',
        interaction='main_power_panel', object_id='B06.power_panel'))
    rooms['B06'].add_object(GameObject('gerador principal',
        'O gerador principal da mansão está silencioso, ligado ao quadro elétrico.',
        interaction='main_generator', object_id='B06.generator', aliases=('gerador',)))
    rooms['B06'].description += ' O gerador principal está ligado a um quadro elétrico na parede.'
    rooms['U07'].add_object(GameObject('fusíveis',
        'Fusíveis de reposição guardados para a instalação elétrica da mansão.',
        portable=True, object_id='U07.fuses', aliases=('fusiveis',)))
    rooms['E09'].description = ('Sob uma cobertura baixa, um equipamento auxiliar abandonado '
        'enferruja entre folhas e poças. Cabos cortados pendem da carcaça; '
        'essa instalação externa não alimenta a mansão.')
    garage_door = GameObject('porta da garagem',
        'Uma porta na parede oeste da sala de estar liga a casa à garagem.',
        openable=True, object_id='C_G01_T03.door')
    garage_door.opened = True
    rooms['T03'].connect(garage, 'oeste', reverse='leste', door=garage_door,
        name='porta da garagem à esquerda', reverse_name='porta para a sala de estar',
        state=PassageState('C_G01_T03'))
    for name, description, aliases in (
        ('carro antigo 1', 'A pintura perdeu o brilho e os pneus estão baixos. '
         'O primeiro carro parece parado há anos; não está em condições de circular.', ('primeiro carro',)),
        ('carro antigo 2', 'A ferrugem avançou pelas bordas da carroceria do segundo carro. '
         'O interior está coberto de poeira; não há sinal de uso recente.', ('segundo carro',)),
        ('compartimento do carro antigo 1', 'O compartimento traseiro conserva um revestimento '
         'gasto sobre o fundo. A poeira se acumulou nas bordas e nas dobradiças.', ('compartimento', 'porta-malas')),
        ('bancada', 'Óleo ressecado mancha a bancada. Armários de manutenção antigos '
         'ocupam o espaço abaixo dela.', ('armário', 'armários')),
        ('ferramentas', 'Ferramentas corroídas e peças automotivas gastas estão espalhadas '
         'pela bancada. Parecem abandonadas há muito tempo.', ('objetos automotivos', 'peças automotivas')),
    ):
        garage.add_object(GameObject(name, description, aliases=aliases))
    garage.add_object(GameObject('portões externos',
        'Duas grandes portas de metal estão presas por travas pesadas. '
        'Cabos antigos chegam aos mecanismos, mas não há comando acessível deste lado.',
        locked=True, openable=True, blocked=True, object_id='G01.external_gates',
        aliases=('portões', 'portão externo', 'portão da garagem', 'portões da garagem', 'portas externas')))
    garage_front = Room('E14', 'Frente da Garagem',
        'À esquerda da fachada principal, duas grandes portas de garagem se erguem entre '
        'paredes deterioradas. O mato invade as juntas do calçamento gasto. A ferrugem '
        'escorre das ferragens; não há sinais de atividade.')
    rooms['E14'] = garage_front
    rooms['E03'].connect(garage_front, 'oeste', reverse='leste',
        name='caminho à esquerda até a frente da garagem e os portões',
        reverse_name='caminho frontal da propriedade')
    garage_front.add_object(GameObject('garagem',
        'A fachada antiga está manchada de umidade. Vegetação cresce junto às paredes '
        'e às duas portas travadas. Não há movimento do outro lado.', aliases=('fachada',)))
    garage_front.connect(garage, 'via_g01', reverse='via_e14',
        door=garage.objects['portões externos'],
        name='portões para o interior da garagem', reverse_name='portões para a frente da garagem',
        state=PassageState('C_E14_G01', enabled=False))
    # Continuação 5.3: conteúdo de campanha, sem alterar o protótipo.
    # Chave/encontro pendentes de recuperação funcional; bloqueio preparado, inativo.
    stairs.lock_id = 'campaign.upper_stairs'
    stairs.required_item = 'chave da empregada'
    maintenance_door = GameObject('porta de manutenção',
        'A porta entre o corredor de serviço e a sala de manutenção está emperrada no batente.',
        openable=True, blocked=True, interaction='jammed_maintenance',
        object_id='C_B03_T12.door', aliases=('passagem emperrada', 'porta emperrada'))
    rooms['B03'].connect(rooms['T12'], 'cima', reverse='baixo', door=maintenance_door,
        name='escadaria com porta de manutenção', reverse_name='escadaria com porta para o corredor de serviço',
        state=PassageState('C_B03_T12', enabled=False))
    rooms['B09'].add_object(GameObject('pé de cabra',
        'Uma barra robusta com a ponta curva, própria para fazer alavanca.',
        portable=True, object_id='B09.crowbar'))

    safe = rooms['office'].objects['cofre']
    pistol = next(o for o in safe.contents if o.name == 'pistola')
    safe.contents.remove(pistol)
    rooms['office'].add_object(GameObject('armário de segurança',
        'Um armário metálico destinado à segurança da propriedade. A porta está apenas encostada.',
        openable=True, contents=[pistol], object_id='T08.security_cabinet'))
    from items import WeaponSpec
    shotgun = GameObject('espingarda', 'Uma espingarda antiga conservada atrás do vidro.',
        portable=True, weapon=WeaponState(WeaponSpec(capacity=2, damage=60, ammo_item='munição de espingarda', initial_ammo=0)),
        object_id='U06.shotgun')
    rooms['U06'].add_object(GameObject('armário de armas',
        'Uma espingarda é visível através do vidro espesso. O armário permanece trancado.',
        locked=True, blocked=True, openable=True, contents=[shotgun], object_id='U06.weapon_cabinet'))
    # Representação inspecionável, sem tornar a arma alcançável ou duplicá-la.
    shotgun.accessible = False
    shotgun.inaccessible_reason = 'A espingarda está atrás do vidro do armário trancado. Não consigo alcançá-la.'
    for rid, name, description, ammo in (
        ('T11', 'bandagem', 'Uma bandagem lacrada no nicho de primeiros socorros.', 0),
        ('T12', 'bandagem', 'Uma bandagem guardada com os materiais de manutenção.', 0),
        ('U05', 'spray de cura', 'Um frasco medicinal lacrado no banheiro.', 0),
        ('U07', 'munição de pistola', 'Dois cartuchos guardados com os suprimentos antigos.', 2),
        ('B04', 'bandagem', 'Uma bandagem protegida num invólucro de manutenção.', 0),
        ('B09', 'kit médico', 'Um kit de primeiros socorros da oficina.', 0),
        ('L07', 'kit médico', 'Um kit médico lacrado da enfermaria.', 0),
        ('G01', 'bandagem', 'Uma bandagem do material automotivo de emergência.', 0),
    ):
        rooms[rid].add_object(GameObject(name, description, portable=True, ammo_count=ammo,
            object_id=rid + '.' + name))
    documents = (
        ('T08', 'documento', 'Circular administrativa',
         'Projeto Evolucys: manter separados os registros clínicos e os pedidos de manutenção. A direção científica responde por Daniel e Adrian Voss.'),
        ('T09', 'nota de pesquisa', 'Nota sobre regeneração',
         'A recomposição dos tecidos não demonstra, por si só, recuperação das funções cognitivas. Os estudos de longevidade exigem acompanhamento prolongado.'),
        ('U06', 'correspondência', 'Correspondência interna',
         'Daniel solicita a suspensão dos ensaios por risco à equipe. Adrian Voss discorda da interrupção e pede continuidade da avaliação. A decisão permanece contestada.'),
        ('U07', 'registro de fusíveis', 'Registro de manutenção',
         'Fusíveis de reposição transferidos para o Depósito Superior. Destino de instalação: quadro do gerador principal, Sala Elétrica do subsolo.'),
        ('B07', 'pasta de joseph', 'Registro de funcionários',
         'Plantão interrompido após agressão nos corredores. Funcionários ausentes não devem ser procurados individualmente. A equipe aguarda instruções de segurança.'),
        ('L03', 'registro de equipe', 'Procedimentos da equipe',
         'Acesso reservado ao pessoal autorizado. Registrar entrada e saída por turno. Divergências entre registros devem ser comunicadas à recepção técnica.'),
        ('L04', 'folha de observação', 'Observação comportamental',
         'Os sujeitos alternam imobilidade e respostas agressivas a estímulos. A ausência de reação não deve ser interpretada como recuperação.'),
        ('L05', 'relatório EV-7', 'Resultados do EV-7',
         'O EV-7 acelera a regeneração, mas as alterações não se limitam ao tecido lesionado. A estabilidade dos resultados permanece sem comprovação.'),
        ('L06', 'registro biológico', 'Comparação entre espécies',
         'Ensaios em espécies distintas apresentam crescimento e adaptação irregulares. Resultados em organismos não humanos não autorizam extrapolação clínica.'),
        ('L07', 'registro clínico', 'Acompanhamento clínico',
         'Alterações musculares e perda de coordenação persistem após os procedimentos. A equipe relata deterioração cognitiva e dificuldade de contenção.'),
        ('L08', 'registro de incidente', 'Falha de contenção',
         'Barreiras internas sofreram danos durante o incidente. A contenção externa deve permanecer ativa; o retorno da alimentação principal não autoriza evacuação.'),
        ('L11', 'evidência do incidente', 'Transcrição do incidente',
         'Registro de câmera: Daniel anuncia que comunicará os experimentos às autoridades. Adrian Voss o agride e injeta o composto. A transformação começa logo depois; o registro termina com danos ao equipamento.'),
    )
    for rid, name, title, text in documents:
        room = rooms[next((old for old, official in ROOM_ALIASES.items() if official == rid), rid)]
        obj = room.objects.get(name)
        if obj is None:
            obj = GameObject(name, title + '.', portable=True, object_id=rid + '.record')
            room.add_object(obj)
        obj.description = title + '.'
        obj.text = text
        obj.document_type = 'relatório'
