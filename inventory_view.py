"""Inventário sobreposto na janela principal; sem janela nativa adicional."""
import tkinter as tk
from items import HEALING
from command_language import normalize
from visual_assets import clear_canvas, object_state

BG, PANEL, TEXT, ACCENT = '#101518', '#1b2429', '#e3e5df', '#c8b58a'


def inventory_command_allowed(game, command):
    """Filtro de interface; não interpreta nem executa regras de itens."""
    try:
        command = normalize(game, command)
    except ValueError:
        return False
    if command in ('inventário', 'fechar inventário', 'fechar leitura', 'status', 'ajuda') or command.startswith('ajuda '):
        return True
    action, _, target = command.partition(' ')
    if action == 'usar' and ' no ' in target:
        item, other = target.split(' no ', 1)
        return item in game.inventory and other in game.inventory
    if action == 'recarregar' and not target:
        target = game.equipped_item
    return action in {'examinar', 'observar', 'olhar', 'ler', 'equipar', 'segurar',
                      'usar', 'tomar', 'largar', 'soltar', 'ligar', 'desligar', 'recarregar'} and target in game.inventory


def item_details(game, name):
    """Projeção de leitura; não executa examine(), efeitos ou turnos."""
    obj = game.item_objects.get(name)
    if name not in game.inventory or obj is None:
        return 'Selecione um item para consultar suas informações.', {}
    text = f'{name.upper()}\n\n{obj.description}'
    if name == 'lanterna':
        text += '\nEstado: ' + ('ligada' if obj.light_on else 'desligada') + '.'
    if obj.weapon:
        text += f'\nMunição: {obj.weapon.ammo}/{obj.weapon.spec.capacity}. Dano: {obj.weapon.spec.damage}.\nUse atacar durante confronto e recarregar para repor cartuchos.'
    if obj.ammo_count:
        text += f'\nQuantidade: {obj.ammo_count} cartuchos. Use recarregar com uma arma equipada.'
    if obj.text is not None:
        text += '\n\n' + '\n\n'.join(f'Página {i+1}\n{page}' for i, page in enumerate(obj.pages))
    reasons = {'examinar': '', 'equipar': '', 'usar': '', 'largar': ''}
    if game.equipped_item == name:
        text += '\nEquipado na mão.'
        reasons['equipar'] = 'Já está na mão.'
    if name in HEALING:
        if game.health == game.max_health:
            reasons['usar'] = 'Não preciso de cura agora.'
    elif name == 'energético':
        if game.focus_charges:
            reasons['usar'] = 'O energético ainda está fazendo efeito.'
    elif name == 'lanterna':
        if game.equipped_item != name:
            reasons['usar'] = 'Preciso colocar a lanterna na mão primeiro.'
    elif name != 'chá':
        reasons['usar'] = 'Este item precisa de um alvo ou comando específico no cenário.'
    if name in game.get_current_room().objects:
        reasons['largar'] = 'Já há um item igual neste local; não posso sobrescrevê-lo.'
    if not obj.capabilities.equipable:
        reasons['equipar'] = 'É melhor manter este item guardado.'
    if game.game_over:
        reasons = {action: 'A partida terminou.' for action in reasons}
    unavailable = [f'{action.capitalize()}: {reason}' for action, reason in reasons.items() if reason]
    if obj.openable:
        text += '\n' + ('Aberto.' if obj.opened else 'Trancado.' if obj.locked else 'Fechado.')
    if unavailable:
        text += '\n\n' + '\n'.join(unavailable)
    return text, reasons


class InventoryWindow:
    def __init__(self, app):
        self.app = app
        # O atributo window permanece compatível com os testes anteriores,
        # mas agora identifica um Frame filho da única janela do jogo.
        self.window = tk.Frame(app.root, bg=BG, highlightbackground=ACCENT, highlightthickness=1)
        self.window.bind('<Escape>', lambda event: self.close())
        self.window.bind('<Configure>', self.resize)
        self.active = False
        self.close_button = app.button(self.window, 'Fechar', self.close)
        self.close_button.pack(side='bottom', pady=6)
        self.entry = tk.Entry(self.window, bg=PANEL, fg=TEXT, insertbackground=ACCENT,
                              font=('Segoe UI', 11))
        self.entry.pack(side='bottom', fill='x', padx=20, pady=4, ipady=5)
        self.entry.bind('<Return>', app.submit_command)
        self.guide = tk.Label(self.window, bg=BG, fg=ACCENT, font=('Segoe UI', 9), wraplength=900)
        self.guide.pack(side='bottom', fill='x', padx=20)
        tk.Label(self.window, text='Comandos de itens ou fechar inventário • ESC fecha',
                 bg=BG, fg=TEXT, font=('Segoe UI', 9)).pack(side='bottom')
        self.result = tk.StringVar()
        result_frame = tk.Frame(self.window, bg=BG)
        result_frame.pack(side='bottom', fill='x', padx=20, pady=4)
        self.result_text = tk.Text(result_frame, height=3, bg=BG, fg=ACCENT,
                                   wrap='word', relief='flat', font=('Segoe UI', 10), state='disabled')
        result_scroll = tk.Scrollbar(result_frame, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=result_scroll.set)
        result_scroll.pack(side='right', fill='y')
        self.result_text.pack(fill='x', expand=True)
        self.result.trace_add('write', self.show_result)
        self.frame = tk.Frame(self.window, bg=BG)
        self.frame.pack(fill='both', expand=True, padx=15, pady=15)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=2)
        self.frame.columnconfigure(2, weight=2)
        self.frame.rowconfigure(0, weight=1)
        left = tk.Frame(self.frame, bg=BG)
        left.grid(row=0, column=0, sticky='nsew', padx=8)
        self.body = tk.Canvas(left, width=150, height=300, bg=BG, highlightthickness=0)
        self.body.pack()
        self.body.create_text(75, 18, text='JOSEPH', fill=TEXT, font=('Segoe UI', 12))
        self.body.create_oval(58, 40, 92, 77, fill='#67736e', outline='')
        self.body.create_polygon(51, 88, 99, 88, 110, 177, 42, 177, fill='#58655e')
        self.body.create_line(51, 96, 29, 189, fill='#58655e', width=15)
        self.body.create_line(99, 96, 121, 189, fill='#58655e', width=15)
        self.body.create_line(58, 173, 49, 273, fill='#58655e', width=20)
        self.body.create_line(92, 173, 101, 273, fill='#58655e', width=20)
        # Camadas frontais provisórias: rosto, camisa, casaco e botas.
        self.body.create_rectangle(61, 48, 89, 73, fill='#b1977c', outline='')
        self.body.create_rectangle(58, 40, 92, 49, fill='#352d28', outline='')
        for x in (67, 81):
            self.body.create_rectangle(x, 56, x+3, 59, fill='#211f20', outline='')
        self.body.create_rectangle(67, 89, 83, 175, fill='#8a8070', outline='')
        self.body.create_line(75, 90, 75, 175, fill='#b4aa92', width=2)
        self.body.create_rectangle(34, 264, 61, 280, fill='#302c29', outline='')
        self.body.create_rectangle(89, 264, 116, 280, fill='#302c29', outline='')
        self.body.create_line(49, 124, 60, 135, fill='#a76a59', width=3, tags='injury')
        self.condition = tk.Label(left, bg=BG, fg=TEXT, font=('Segoe UI', 12), justify='left')
        self.condition.pack(pady=12)
        center = tk.Frame(self.frame, bg=BG)
        center.grid(row=0, column=1, sticky='nsew', padx=8)
        self.slots = []
        for index in range(6):
            center.columnconfigure(index % 2, weight=1)
            button = tk.Button(center, bg=PANEL, fg=TEXT, activebackground='#4b4d3d',
                               activeforeground=TEXT, wraplength=125, width=16, height=6,
                               font=('Segoe UI', 10), relief='flat',
                               command=lambda i=index: self.select(i))
            button.grid(row=index // 2, column=index % 2, sticky='nsew', padx=3, pady=4)
            self.slots.append(button)
        right = tk.Frame(self.frame, bg=BG)
        right.grid(row=0, column=2, sticky='nsew', padx=8)
        self.preview = tk.Canvas(right, height=85, bg=BG, highlightthickness=0)
        self.preview.pack(fill='x')
        self.preview.bind('<Configure>', lambda event: self.draw_preview())
        self.description = tk.Text(right, width=30, height=18, bg=BG, fg=TEXT,
                                   wrap='word', relief='flat', font=('Segoe UI', 10))
        actions = tk.Frame(right, bg=BG)
        actions.pack(side='bottom', fill='x', pady=4)
        scroll = tk.Scrollbar(right, command=self.description.yview)
        self.description.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        self.description.pack(fill='both', expand=True)
        self.actions = {}
        for index, action in enumerate(('examinar', 'equipar', 'usar', 'largar')):
            button = app.button(actions, action.capitalize() + ' item', lambda a=action: self.act(a))
            button.grid(row=index // 2, column=index % 2, padx=2, pady=2)
            self.actions[action] = button

    def resize(self, event=None):
        for slot in self.slots:
            slot.configure(wraplength=max(80, slot.winfo_width()-16))

    def draw_preview(self):
        clear_canvas(self.preview)
        game = self.app.session.game
        if game:
            obj = game.item_objects.get(self.app.session.selected_item)
            if obj:
                self.app.assets.draw(self.preview, obj, object_state(obj), max(80, self.preview.winfo_width())/2, 42, limit=(200, 75))

    def show_result(self, *args):
        self.result_text.configure(state='normal')
        self.result_text.delete('1.0', 'end')
        self.result_text.insert('end', self.result.get())
        self.result_text.configure(state='disabled')

    def hide(self):
        if self.window.grab_current() == self.window:
            self.window.grab_release()
        self.window.place_forget()
        self.active = False

    def close(self):
        if self.app.session.inventory_open:
            self.app.session.game.emit('inventory_close')
        self.app.session.inventory_open = False
        self.app.session.parser.inventory_context = False
        self.hide()
        self.entry.delete(0, 'end')
        self.app.draw_scene()
        self.app.flush_audio()
        self.app.command_entry.focus_set()
        return 'break'

    def select(self, index):
        if not self.app.session.inventory_open:
            return
        self.app.session.selected_item = self.app.session.slots()[index]
        obj = self.app.session.game.item_objects.get(self.app.session.selected_item)
        if obj and obj.text is not None:
            obj.was_read = True
            obj.read_pages.update(range(len(obj.pages)))
            self.app.session.game.emit('document_open', object_id=obj.object_id)
            self.app.flush_audio()
        self.result.set('')
        self.refresh()
        self.draw_preview()

    def act(self, action):
        session = self.app.session
        if not session.inventory_open:
            return
        _, reasons = item_details(session.game, session.selected_item)
        if action not in reasons or reasons[action]:
            return
        self.result.set(session.inventory_action(action))
        self.app.refresh()

    def refresh(self):
        session = self.app.session
        game = session.game
        self.guide.configure(text=game.guide.current if session.inventory_open else '')
        if session.inventory_open:
            if not self.active:
                self.window.place(relx=.5, rely=.5, anchor='center', relwidth=.94, relheight=.90)
                self.window.lift()
                self.window.grab_set()
                self.active = True
                self.entry.focus_set()
        else:
            self.hide()
        condition = 'crítico' if game.health <= 25 else 'ferido' if game.health < 100 else 'saudável'
        self.condition.configure(text=f'♥ {condition.capitalize()}\nVida {game.health}/100\nMedo {game.fear}/100')
        self.body.itemconfigure('injury', state='normal' if game.health < 100 else 'hidden')
        for index, name in enumerate(session.slots()):
            obj = game.item_objects.get(name)
            icon = '▣' if name else '□'
            text = f'{icon}  {index+1}\n{name or "Vazio"}'
            if obj and obj.weapon:
                text += f'\n{obj.weapon.ammo}/{obj.weapon.spec.capacity} tiros'
            elif obj and obj.ammo_count:
                text += f'\n{obj.ammo_count} cartuchos'
            if name and name == game.equipped_item:
                text += '\n[NA MÃO]'
            selected = bool(name and name == session.selected_item)
            self.slots[index].configure(text=text, bg='#4b4d3d' if selected else PANEL,
                highlightthickness=2, highlightbackground=ACCENT if name and name == game.equipped_item else PANEL)
        text, reasons = item_details(game, session.selected_item)
        self.description.configure(state='normal')
        self.description.delete('1.0', 'end')
        self.description.insert('end', text)
        self.description.configure(state='disabled')
        for action, button in self.actions.items():
            button.configure(state='normal' if action in reasons and not reasons[action] else 'disabled')
        self.draw_preview()
