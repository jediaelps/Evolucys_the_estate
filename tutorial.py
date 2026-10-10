"""Mundos descartáveis de teste, separados da campanha e de qualquer save."""
from game_state import GameState
from world import Room, GameObject
from confrontation import Enemy
from items import WeaponState


SCENARIOS = {1: 'Exploração', 2: 'Inventário e sobrevivência',
             3: 'Puzzle', 4: 'Confronto'}


def supplies():
    descriptions = {
        'lanterna': 'Uma lanterna funcional.', 'bandagem': 'Bandagem para ferimentos leves.',
        'spray de cura': 'Spray medicinal.', 'kit médico': 'Um kit completo.',
        'chá': 'Um chá familiar.', 'energético': 'Uma lata lacrada.',
        'pé de cabra': 'Uma ferramenta resistente.',
    }
    result = [GameObject(name, desc, portable=True) for name, desc in descriptions.items()]
    result += [GameObject('pistola', 'Uma pistola para testes.', portable=True, weapon=WeaponState()),
               GameObject('munição de pistola', 'Cartuchos para testes.', portable=True, ammo_count=12)]
    return result


class TutorialState(GameState):
    def __init__(self, scenario):
        if scenario not in SCENARIOS:
            raise ValueError('Cenário inexistente')
        super().__init__()
        # O equipamento inicial da campanha não pertence aos cenários isolados.
        self.inventory.clear()
        self.item_objects.clear()
        self.scenario = scenario
        self.safety_notice = ''
        self.rooms = {}
        start = Room('test_start', SCENARIOS[scenario], 'Uma sala fechada de testes. O corredor à frente leva a outro ambiente.')
        end = Room('test_end', 'Sala adjacente', 'O mesmo espaço visto pelos olhos de Joseph. A saída está atrás de você.')
        self.rooms = {start.room_id: start, end.room_id: end}
        self.current_location = start.room_id
        door = GameObject('porta de teste', 'Uma porta simples. Pode ser aberta.', openable=True)
        if scenario == 1:
            start.add_object(GameObject('mesa de teste', 'A mesa está presa ao piso. Há marcas de uso.'))
            start.add_object(GameObject('lanterna', 'Uma lanterna deixada sobre a mesa.', portable=True))
            start.add_object(GameObject('caixa', 'Uma caixa com tampa.', contents=[
                GameObject('bilhete de teste', 'Um papel dobrado com linhas escritas à mão.', portable=True,
                           text='Este espaço serve para observar, experimentar e voltar quando quiser. Nada aqui altera a mansão.')]))
        elif scenario in (2, 4):
            for obj in supplies():
                start.add_object(obj)
            door.opened = True
            if scenario == 4:
                end.name = 'Sala do vigia — teste'
                end.description = 'O vigia ronda o ambiente. Você pode entrar em silêncio ou recuar ao sul.'
                end.enemy = Enemy('vigia', health=120)
            else:
                end.description = 'Uma sala vazia para testar deslocamento e descarte de itens.'
        elif scenario == 3:
            door.locked = True
            door.required_item = 'chave de teste'
            door.lock_id = 'tutorial.exit'
            start.add_object(GameObject('quadro de teste', 'A moldura está solta. Algo aparece atrás dela.', hidden_objects=[
                GameObject('anotação', 'Quatro algarismos escritos à mão: 2468.', portable=True)]))
            start.add_object(GameObject('cofre de teste', 'Um pequeno cofre com teclado.', locked=True, code='2468', contents=[
                GameObject('chave de teste', 'Uma chave de treino permanente.', portable=True,
                           key_lock_ids={'tutorial.exit'}, permanent_key=True)]))
            end.add_object(GameObject('registro', 'A passagem foi aberta. O puzzle de teste está concluído.'))
        start.add_exit('norte', end.room_id, door)
        end.add_exit('sul', start.room_id, door)
        self.supply_room = start.room_id
        if scenario == 1:
            start.add_object(GameObject('aviso fixo', 'Um papel envelhecido preso à parede.',
                object_id='tutorial.notice', document_type='bilhete',
                text='Área de observação. Este aviso permanece na parede.',
                pages=['As páginas podem ser consultadas sem alterar os recursos da campanha.']))
            start.add_object(GameObject('retrato antigo', 'Um retrato em moldura de madeira.',
                object_id='tutorial.portrait', inspection_faces={
                    'front': 'Um homem observa a entrada da mansão. A moldura está solta.',
                    'back': 'À luz da lanterna, uma inscrição: «Não confie no relógio da entrada.»'}))
            start.objects['caixa'].inspection_faces = {'interior': 'O forro está gasto. Há marcas no fundo.'}
        if scenario == 2:
            start.add_object(GameObject('carta antiga', 'Uma carta dobrada.', portable=True,
                object_id='tutorial.letter', document_type='carta', text='Joseph, guarde suas anotações.',
                pages=['A chuva continua. Este é apenas um documento da área de testes.']))
        if scenario == 3:
            start.add_object(GameObject('chave de arquivo', 'Uma chave com duas marcações.', portable=True,
                key_lock_ids={'tutorial.archive.a', 'tutorial.archive.b'}))
            for suffix in ('a', 'b'):
                start.add_object(GameObject('armário ' + suffix, 'Um armário de arquivos.',
                    locked=True, lock_id='tutorial.archive.' + suffix, required_item='chave de arquivo'))
        for obj in list(start.objects.values()) + list(end.objects.values()):
            for document in [obj] + obj.hidden_objects:
                if document.name in ('anotação', 'registro'):
                    document.text = document.description

    def damage(self, amount):
        super().damage(amount)
        if self.scenario == 4 and self.health <= 0:
            self.health = 25
            self.game_over = False
            self.safety_notice = 'MODO DE TESTE: morte impedida; vida restaurada para 25.'

    def install_targets(self):
        """Demonstração opcional; mantém os quatro cenários anteriores intactos."""
        from visual_assets import SpriteSpec
        room = self.rooms['test_end']
        room.name = 'Sala das duas criaturas'
        room.description = 'Duas criaturas ocupam o corredor. A saída ao sul continua livre.'
        left = Enemy('zumbi', health=120, distance='próximo', trait='casaco rasgado')
        right = Enemy('zumbi', health=120, distance='distante', trait='camisa clara')
        left.sprite.position = (.32, .56)
        right.sprite.position = (.72, .32)
        room.enemies = [left, right]

    def debug(self, action):
        """Comandos não disponíveis em GameState nem no parser da campanha."""
        if action == 'dano':
            self.damage(25)
        elif action == 'curar':
            self.game_over = False
            self.health = self.max_health
        elif action == 'medo+':
            self.increase_fear(25)
        elif action == 'medo-':
            self.reduce_fear(25)
        elif action == 'recursos':
            if self.scenario not in (2, 4):
                return 'Recursos disponíveis nos cenários 2 e 4.'
            # Repor os consumidos, sem duplicar instâncias já carregadas/largadas.
            names = set(self.inventory)
            for room in self.rooms.values():
                names.update(room.objects)
            for obj in supplies():
                if obj.name not in names:
                    self.rooms[self.supply_room].add_object(obj)
        elif action == 'munição':
            if self.scenario not in (2, 4):
                return 'Munição disponível nos cenários 2 e 4.'
            ammo = self.item_objects.get('munição de pistola')
            if ammo:
                ammo.ammo_count = 12
            else:
                for room in self.rooms.values():
                    room.objects.pop('munição de pistola', None)
                self.get_current_room().add_object(GameObject('munição de pistola',
                    'Cartuchos de teste.', portable=True, ammo_count=12))
        elif action == 'esvaziar':
            obj = self.item_objects.get(self.equipped_item)
            if not obj or not obj.weapon:
                return 'Equipe uma arma para esvaziá-la neste teste.'
            obj.weapon.ammo = 0
        else:
            return 'Controle de teste desconhecido.'
        notice = self.safety_notice
        self.safety_notice = ''
        return notice or 'MODO DE TESTE: estado ajustado sem consumir turno.'
