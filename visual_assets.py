"""Projeções visuais do mundo e PNGs opcionais; sem dependências externas."""
from dataclasses import dataclass, field
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / 'assets'


@dataclass
class SpriteSpec:
    object_id: str = ''
    position: tuple = None  # coordenadas normalizadas, ou distribuição automática
    scale: float = 1.0
    visible: bool = True
    state: str = 'front'
    layer: int = 20
    images: dict = field(default_factory=dict)  # estado -> caminho relativo a assets


def default_object_images(obj):
    name = obj.name
    kind = ('document' if obj.text is not None else 'portrait' if 'retrato' in name else
            'key' if 'chave' in name else 'pistol' if obj.weapon else 'ammo' if obj.ammo_count else
            'flashlight' if name == 'lanterna' else 'item')
    return {state: f'objects/{kind}_{state}.png' for state in ('front', 'back', 'open', 'closed', 'interior', 'damaged')}


def object_state(obj):
    if obj.damaged:
        return 'damaged'
    return ('open' if obj.opened else 'closed') if obj.openable else obj.sprite.state


def enemy_state(enemy):
    return ('fallen' if not enemy.alive else 'distracted' if enemy.distracted else
            'preparing' if enemy.preparing else 'alert' if enemy.alert else 'idle')


def scene_sprites(room, game=None):
    from target_selection import arrange
    arrange(room)
    entries = []
    for obj in (game.visible_objects(room) if game else room.objects).values():
        if obj.sprite.visible:
            entries.append((obj.sprite.layer, obj, object_state(obj)))
    for enemy in room.enemies:
        if enemy.sprite.visible:
            entries.append((enemy.sprite.layer, enemy, enemy_state(enemy)))
    return sorted(entries, key=lambda entry: entry[0])


class AssetStore:
    def __init__(self, root, directory=ASSETS):
        self.root, self.directory = root, Path(directory).resolve()
        self.cache = {}

    def image(self, relative, scale=1.0, limit=(400, 240)):
        import tkinter as tk
        if not relative:
            return None
        path = (self.directory / relative).resolve()
        if self.directory not in path.parents or not path.is_file():
            return None
        key = (str(path), scale, limit)
        if key in self.cache:
            return self.cache[key]
        try:
            original = tk.PhotoImage(master=self.root, file=str(path))
            # Zoom inteiro e amostragem pontual preservam bordas de pixels.
            zoom = max(1, min(8, round(scale)))
            shrink = max(1, round(1 / max(.125, scale)),
                         -(-original.width()*zoom // limit[0]),
                         -(-original.height()*zoom // limit[1]))
            result = original.zoom(zoom).subsample(shrink)
        except (tk.TclError, OSError, ValueError):
            return None
        if len(self.cache) >= 128:
            self.cache.clear()
        self.cache[key] = result
        return result

    def draw(self, canvas, obj, state, x, y, size=1.0, limit=(400, 240)):
        spec = obj.sprite
        tags = ('sprite', 'object:' + spec.object_id, 'state:' + state)
        picture = self.image(spec.images.get(state), spec.scale * size, limit)
        if picture is not None:
            canvas._sprite_images.append(picture)
            canvas.create_image(x, y, image=picture, tags=tags)
            return
        s = max(.25, min(4, spec.scale * size))
        if hasattr(obj, 'alive'):
            color = '#ad7362' if state == 'preparing' else '#778276'
            if state == 'fallen':
                canvas.create_rectangle(x-30*s, y, x+30*s, y+12*s, fill=color, tags=tags)
            else:
                canvas.create_rectangle(x-9*s, y-35*s, x+9*s, y-17*s, fill=color, tags=tags)
                canvas.create_polygon(x-15*s,y-14*s,x+15*s,y-14*s,x+24*s,y+35*s,x-24*s,y+35*s, fill=color, tags=tags)
        else:
            paper = obj.text is not None or state == 'back'
            color = '#c5b88f' if paper else '#725f47'
            canvas.create_rectangle(x-26*s,y-30*s,x+26*s,y+30*s,fill=color,outline='#b19b70',width=3,tags=tags)
            if state == 'open' or state == 'interior':
                canvas.create_rectangle(x-20*s,y-20*s,x+20*s,y+20*s,fill='#242622',tags=tags)
            elif state == 'damaged':
                canvas.create_line(x-15*s,y-25*s,x+5*s,y,x-5*s,y+25*s,fill='#211d1c',width=3,tags=tags)
            elif obj.inspection_faces and state == 'front':
                canvas.create_rectangle(x-7*s,y-17*s,x+7*s,y-3*s,fill='#ab9374',tags=tags)
                canvas.create_rectangle(x-13*s,y,x+13*s,y+20*s,fill='#373c37',tags=tags)
            elif paper:
                for row in range(4):
                    canvas.create_line(x-17*s,y+(-14+row*8)*s,x+17*s,y+(-14+row*8)*s,fill='#6e6550',tags=tags)


def clear_canvas(canvas):
    canvas.delete('all')
    canvas._sprite_images = []
