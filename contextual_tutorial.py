"""Dicas de sessão, serializáveis e sem acesso a conteúdos ocultos."""
class TutorialGuide:
    def __init__(self, presented=()):
        self.presented = set(presented)
        self.current = ''

    def to_dict(self):
        return {'presented': sorted(self.presented)}

    @classmethod
    def from_dict(cls, data):
        return cls(data.get('presented', []))

    def update(self, game, presentation=None):
        room = game.get_current_room()
        enemies = [e for e in room.enemies if e.alive and e.sprite.visible]
        options = [
            ('danger', bool(enemies), 'Há perigo por perto. Você pode recuar por uma saída aberta.'),
            ('combat', bool(enemies), 'Você pode dizer atacar seguido do nome da criatura, ou tentar fugir.'),
            ('targets', len(enemies)>1, 'Há mais de uma criatura. Indique a posição ou a distância do alvo.'),
            ('inspection', presentation == 'inspection', 'Descreva o que deseja observar neste objeto. Use ESC para voltar.'),
            ('reading', presentation == 'reading', 'Você pode ler com calma, virar as páginas e voltar com ESC.'),
            ('inventory', presentation == 'inventory', 'Selecione um pertence para vê-lo melhor e escolher uma ação.'),
            ('observe', True, 'Você pode observar melhor o ambiente. Experimente “olhar em volta”.'),
            ('collect', any(o.portable and o.accessible for o in game.visible_objects().values()), 'Para guardar algo ao alcance, diga pegar seguido do nome.'),
            ('move', bool(room.exits), 'Siga por uma saída usando ir e a direção.'),
            ('use', bool(game.inventory), 'Para usar consumíveis, abra o inventário. Ferramentas também podem ser usadas no cenário.'),
            ('interaction', bool(game.inventory) and bool(room.objects), 'Indique o alvo de uma interação: usar item no objeto.'),
        ]
        self.current = ''
        for topic, available, text in options:
            if available and topic not in self.presented:
                self.presented.add(topic)
                self.current = text
                break
        return self.current
