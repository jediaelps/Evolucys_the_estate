"""Cômodos descartáveis de validação; não fazem parte do mapa da campanha."""
from tutorial import TutorialState
from world import Room, GameObject
from confrontation import Enemy
from items import ItemCapabilities


def create_system_demo(kind='surprise'):
    game = TutorialState(4)
    foyer = Room('demo_foyer', 'Sala de preparação', 'Uma sala de treino. A passagem ao norte leva a um corredor escuro.')
    hall = Room('demo_hall', 'Corredor de treino', 'Móveis grandes ocupam a penumbra. Há uma passagem ao norte e uma ao sul.')
    end = Room('demo_end', 'Sala distante', 'Um espaço reservado aos ruídos e à ronda.')
    front = GameObject('porta norte', 'Uma porta de madeira.', openable=True)
    front.opened = True
    back = GameObject('porta interna', 'Uma porta aberta para o próximo espaço.', openable=True)
    back.opened = True
    foyer.add_exit('norte', hall.room_id, front)
    hall.add_exit('sul', foyer.room_id, front)
    hall.add_exit('norte', end.room_id, back)
    end.add_exit('sul', hall.room_id, back)
    game.rooms = {r.room_id: r for r in (foyer, hall, end)}
    game.current_location = foyer.room_id
    game.supply_room = foyer.room_id
    game.objective = 'Experimente escutar, observar e atravessar com cuidado.'
    for name in ('lanterna', 'energético', 'bandagem', 'pé de cabra'):
        obj = GameObject(name, 'Um recurso disponível para esta prática.', portable=True)
        if name == 'lanterna':
            obj.uv_enabled = True  # Bancada de teste, não upgrade da campanha.
        foyer.add_object(obj)
    foyer.add_object(GameObject('barra do macaco', 'Uma ferramenta específica, curta e pouco manejável.', portable=True,
                                capabilities=ItemCapabilities(tool=True)))
    hall.dark = True
    hall.add_object(GameObject('armário pesado', 'Cabe uma pessoa entre as roupas grossas.', hiding_effectiveness=85))
    hall.add_object(GameObject('caixas baixas', 'As caixas deixam boa parte do corpo exposta.', hiding_effectiveness=15))
    hall.add_object(GameObject('anotação pequena', 'Há letras muito pequenas.', text='Uma lembrança esquecida.', requires_light=True))
    hall.add_object(GameObject('marca oculta', 'Uma escrita surge sob ultravioleta.', text='Observe antes de avançar.', requires_uv=True))
    if kind == 'surprise':
        hall.enemy = Enemy('criatura', surprise=85, unknown=True)
    elif kind == 'patrol':
        end.enemy = Enemy('criatura', patrol_route=[end.room_id, hall.room_id], patrol_interval=4)
    else:
        end.enemy = Enemy('criatura silenciosa', sound=None, hears=False, sensitive_to_light=False)
    return game
