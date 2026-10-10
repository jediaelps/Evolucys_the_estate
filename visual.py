"""Protótipo de cenas em primeira pessoa com Tkinter (sem motor 3D)."""
import tkinter as tk

from visual_session import VisualSession
from tutorial import SCENARIOS
from hud_state import indicators, focus_icons
from inventory_view import InventoryWindow, inventory_command_allowed
from document_view import DocumentPanel
from audio_events import AudioPlayer
from visual_assets import AssetStore, clear_canvas, scene_sprites
from target_selection import label as enemy_label, pose


BG = '#101518'
PANEL = '#1b2429'
TEXT = '#e3e5df'
ACCENT = '#c8b58a'


class VisualApp:
    def __init__(self, root=None):
        self.root = root or tk.Tk()
        self.root.title('Evolucys: The Estate — Fase 4.5.5')
        self.root.geometry('1200x800')
        self.root.minsize(1100, 760)
        self.root.configure(bg=BG)
        self.session = VisualSession()
        self.screen = 'menu'
        self.hud = tk.StringVar()
        self.hand = tk.StringVar()
        self.details = tk.StringVar()
        self.reader_window = None
        self.previous_health = None
        self.audio = AudioPlayer()
        self.assets = AssetStore(self.root)
        self.root.bind('<KeyPress>', self.key)
        self.menu()

    def clear(self, screen):
        self.screen = screen
        for child in self.root.winfo_children():
            child.destroy()
        self.reader_window = None

    def label(self, parent, text='', **kwargs):
        return tk.Label(parent, text=text, bg=BG, fg=TEXT, font=('Segoe UI', 11), **kwargs)

    def button(self, parent, text, command, **kwargs):
        return tk.Button(parent, text=text, command=command, bg=PANEL, fg=TEXT,
                         activebackground='#39434a', activeforeground='white',
                         disabledforeground='#626a6d', relief='flat', padx=9, pady=7,
                         font=('Segoe UI', 10), cursor='hand2', **kwargs)

    def menu(self):
        self.clear('menu')
        self.label(self.root, 'EVOLUCYS: THE ESTATE').pack(pady=(110, 12))
        self.label(self.root, 'A mansão espera.\nPrimeira pessoa comandada por texto • Fase 4.5.5').pack(pady=20)
        frame = tk.Frame(self.root, bg=BG)
        frame.pack()
        self.button(frame, 'Iniciar Jogo', self.start_campaign, width=32).pack(pady=7)
        self.button(frame, 'Continuar — sem save válido', lambda: None, width=32,
                    state='normal' if self.session.can_continue else 'disabled').pack(pady=7)
        self.button(frame, 'Tutorial / Área de Testes', self.tutorial_menu, width=32).pack(pady=7)
        self.button(frame, 'Opções', self.options, width=32).pack(pady=7)
        self.button(frame, 'Sair', self.root.destroy, width=32).pack(pady=7)
        self.label(self.root, 'O progresso desta versão fica apenas na sessão.').pack(pady=32)

    def options(self):
        self.clear('options')
        self.label(self.root, 'OPÇÕES').pack(pady=(100, 25))
        self.label(self.root, 'Janela redimensionável • Áudio offline provisório\n'
                   'Espaço reservado para configurações futuras.').pack(pady=25)
        self.button(self.root, 'Voltar ao menu', self.menu).pack()

    def tutorial_menu(self):
        self.clear('tutorial_menu')
        self.label(self.root, 'ÁREA DE TESTES — independente da campanha').pack(pady=(65, 18))
        self.label(self.root, 'Cada cenário começa do zero. Recursos e progresso são descartados ao sair.').pack(pady=15)
        descriptions = {1: 'Objetos, portas e inspeção', 2: 'Seis espaços, cura, medo, luz e munição',
                        3: 'Esconderijo, cofre, chave e passagem', 4: 'Vigia, turnos, fuga e proteção contra morte'}
        for number, name in SCENARIOS.items():
            self.button(self.root, f'{number} — {name}\n{descriptions[number]}',
                        lambda n=number: self.start_tutorial(n), width=52).pack(pady=9)
        self.button(self.root, 'Seleção de alvos — duas criaturas', self.start_target_demo).pack(pady=4)
        demo_row = tk.Frame(self.root, bg=BG)
        demo_row.pack(pady=4)
        for title, kind in (('Sustos e foco', 'surprise'), ('Esconderijos e ronda', 'patrol'), ('Luz e silêncio', 'light')):
            self.button(demo_row, title, lambda k=kind: self.start_system_demo(k)).pack(side='left', padx=3)
        self.button(self.root, 'Voltar ao menu', self.menu).pack(pady=20)

    def start_campaign(self):
        self.session.start_campaign()
        self.build_game()

    def start_tutorial(self, number):
        self.session.start_tutorial(number)
        self.build_game()

    def start_target_demo(self):
        self.session.start_tutorial(4)
        self.session.game.install_targets()
        self.build_game()

    def start_system_demo(self, kind):
        from system_demo import create_system_demo
        self.session._attach(create_system_demo(kind), 'tutorial')
        self.build_game()

    def pause(self):
        self.clear('pause')
        self.label(self.root, 'PAUSA — o tempo só avança com ações').pack(pady=(110, 35))
        self.button(self.root, 'Retomar sessão', self.build_game, width=32).pack(pady=10)
        if self.session.mode == 'tutorial':
            self.button(self.root, 'Reiniciar cenário', self.reset, width=32).pack(pady=10)
            self.button(self.root, 'Escolher outro cenário', self.leave_tutorial, width=32).pack(pady=10)
        self.button(self.root, 'Menu principal — encerrar sessão', self.leave, width=32).pack(pady=10)

    def leave(self):
        self.session.leave()
        self.menu()

    def leave_tutorial(self):
        self.session.leave()
        self.tutorial_menu()

    def reset(self):
        self.session.reset()
        self.build_game()

    def build_game(self):
        self.clear('game')
        top = tk.Frame(self.root, bg=BG)
        top.pack(fill='x', padx=16, pady=2)
        self.button(top, 'Pausa / ESC', self.pause).pack(side='right')

        # A cena é somente apresentação; não há bindings de ações por clique.
        self.canvas = tk.Canvas(self.root, bg='#121416', highlightthickness=0, height=240)
        self.canvas.pack(fill='both', expand=True, padx=16)
        self.canvas.bind('<Configure>', lambda event: self.draw_scene())

        self.inventory_view = InventoryWindow(self)
        self.inventory_frame = self.inventory_view.frame
        self.slot_labels = self.inventory_view.slots
        lower = tk.Frame(self.root, bg=BG)
        lower.pack(fill='x', padx=16, pady=(4, 0))
        lower.columnconfigure(0, weight=3, uniform='lower')
        lower.columnconfigure(1, weight=1, uniform='lower')
        self.objective_frame = tk.Frame(lower, bg=PANEL, padx=12, pady=6)
        self.objective_frame.grid(row=0, column=1, sticky='nsew', padx=(12, 0))
        tk.Label(self.objective_frame, text='OBJETIVO', bg=PANEL, fg=ACCENT,
                 font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        self.objective_label = tk.Label(self.objective_frame, bg=PANEL, fg=TEXT,
                                       font=('Segoe UI', 10), justify='left', anchor='nw')
        self.objective_label.pack(fill='both', expand=True, pady=(5, 0))
        self.objective_frame.bind('<Configure>', lambda e: self.objective_label.configure(wraplength=max(80, e.width-24)))
        history_frame = tk.Frame(lower, bg=BG)
        self.history_frame = history_frame
        history_frame.grid(row=0, column=0, sticky='nsew')
        self.history_view = tk.Text(history_frame, height=10, bg=BG, fg=TEXT,
                                    relief='flat', font=('Segoe UI', 10), wrap='word',
                                    state='disabled', takefocus=False)
        scroll = tk.Scrollbar(history_frame, command=self.history_view.yview, width=10, relief='flat', bd=0)
        self.history_view.configure(yscrollcommand=scroll.set)
        self.history_view.pack(side='left', fill='x', expand=True)
        scroll.pack(side='right', fill='y')
        self.history_view.tag_configure('command', foreground=ACCENT)
        self.history_view.tag_configure('hint', foreground='#91b6bf')
        self.history_view.tag_configure('action_verb', foreground=ACCENT, font=('Segoe UI', 10, 'bold'))
        self.history_view.bind('<Configure>', lambda event: self.anchor_history())

        command_space = tk.Frame(self.root, bg=BG)
        command_space.pack(fill='x', padx=16, pady=2)
        command_area = tk.Frame(self.root, bg=BG)
        command_area.place(in_=command_space, x=0, y=48, relwidth=.5)
        command_area.columnconfigure(0, weight=1, uniform='command')
        command_row = tk.Frame(command_area, bg=BG)
        command_row.grid(row=0, column=0, sticky='ew')
        self.label(command_row, '>').pack(side='left', padx=(0, 8))
        self.command_entry = tk.Entry(command_row, bg=PANEL, fg=TEXT,
                                      insertbackground=ACCENT, relief='flat',
                                      font=('Segoe UI', 12))
        self.command_entry.pack(side='left', fill='x', expand=True, ipady=3)
        self.command_entry.bind('<Return>', self.submit_command)
        self.command_caption = self.label(command_area, 'Digite uma ação e pressione Enter.')
        self.command_caption.grid(row=1, column=0, sticky='w', pady=(3, 0))
        command_area.update_idletasks()
        command_space.configure(height=command_area.winfo_reqheight() - 3)

        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill='x', padx=16, pady=4)
        self.indicators = tk.Canvas(footer, width=320, height=86, bg=BG, highlightthickness=0)
        self.indicators.pack(side='right')
        if self.session.mode == 'tutorial':
            debug = tk.Frame(self.root, bg=PANEL)
            debug.pack(fill='x', padx=16, pady=4)
            self.label(debug, 'TESTE:').pack(side='left')
            for title, action in [('-25 vida', 'dano'), ('Restaurar vida', 'curar'),
                                  ('+25 medo', 'medo+'), ('-25 medo', 'medo-'),
                                  ('Repor itens', 'recursos'), ('Repor munição', 'munição'),
                                  ('Esvaziar arma', 'esvaziar')]:
                self.button(debug, title, lambda a=action: self.debug(a)).pack(side='left', padx=1)
            self.button(debug, 'Reset', self.reset).pack(side='right')
        command_area.lift()
        self.refresh()
        (self.inventory_view.entry if self.session.inventory_open else self.command_entry).focus_set()

    def refresh(self):
        game = self.session.game
        state = game.snapshot()
        equipped = state['equipped_item'] or 'nada'
        weapon = state['weapons'].get(equipped)
        ammo = f" • Munição {weapon['ammo']}/{weapon['capacity']}" if weapon else ''
        mode = f'TESTE {game.scenario}' if self.session.mode == 'tutorial' else 'CAMPANHA'
        self.hud.set(f"{mode} • Mão: {equipped}{ammo} {focus_icons(state['focus_charges'])}"
                     f" • Luz: {'acesa' if state['light_visible'] else 'apagada'} • Turno {state['turn_count']}")
        self.hand.set(f'MÃO: {equipped}{ammo}')
        self.details.set(f"{mode}"
                         f" • Luz {'acesa' if state['light_visible'] else 'apagada'}")
        self.objective_label.configure(text=state['objective'] or 'Procurar uma saída.')
        self.inventory_view.refresh()
        self.history_view.configure(state='normal')
        self.history_view.delete('1.0', 'end')
        if not self.session.history:
            self.history_view.insert('end', self.session.initial_environment + '\n')
        for (command, response), hint in zip(self.session.history, self.session.history_hints):
            self.history_view.insert('end', f'> {command}\n', 'command')
            preview = response[:220] + '… [consulte o painel de leitura]' if len(response) > 500 and command.strip().lower().startswith('ajuda') else response
            self.history_view.insert('end', preview + '\n')
        self.history_view.delete('end-2c', 'end-1c')
        import re
        content = self.history_view.get('1.0', 'end-1c')
        for line in re.finditer(r'^Joseph: “[^\n]+”$', content, re.MULTILINE):
            for verb in re.finditer(r'\b(?:DIGITAR|EXAMINAR|OUVIR|ESCONDER|FUGIR|DEFENDER|USAR|LER|OBSERVAR|CHECAR|INVENTÁRIO|NORTE|SUL|LESTE|OESTE|SUBIR|DESCER)\b', line.group()):
                start, end = line.start()+verb.start(), line.start()+verb.end()
                self.history_view.tag_add('action_verb', f'1.0+{start}c', f'1.0+{end}c')
        self.history_view.configure(state='disabled')
        self.anchor_history()
        self.draw_indicators(state)
        self.draw_scene()
        self.update_reader()
        self.flush_audio()

    def anchor_history(self):
        view = self.history_view
        if not view.winfo_exists():
            return
        view.tag_configure('bottom_anchor', spacing1=0)
        view.tag_add('bottom_anchor', '1.0', '1.1')
        text_height = int(view.tk.call(view._w, 'count', '-update', '-ypixels', '1.0', 'end'))
        inset = sum(int(view.cget(option)) for option in ('pady', 'borderwidth', 'highlightthickness'))
        view.tag_configure('bottom_anchor', spacing1=max(0, view.winfo_height() - 2*inset - text_height))
        view.see('end')

    def flush_audio(self):
        if self.session.game:
            self.audio.handle(self.session.game.drain_events())

    def draw_indicators(self, state):
        view = indicators(state, self.previous_health)
        self.previous_health = state['health']
        c = self.indicators
        c.delete('all')
        equipped = state['equipped_item']
        weapon = state['weapons'].get(equipped)
        slot_text = equipped or 'Vazia'
        if weapon:
            slot_text += f" • {weapon['ammo']}/{weapon['capacity']}"
        c.create_rectangle(4, 3, 178, 41, fill=PANEL, outline='#46514f', tags='hand_slot')
        c.create_text(12, 12, text='MÃO', fill=ACCENT, anchor='w', font=('Segoe UI', 8), tags='hand_slot')
        c.create_text(12, 29, text=slot_text, fill=TEXT, anchor='w', font=('Segoe UI', 10), tags=('hand_slot', 'equipped'))
        for index in range(2):
            c.create_text(216 + index*30, 20, text='⚡',
                          fill=ACCENT if index < state['focus_charges'] else '#626a6d',
                          font=('Segoe UI Symbol', 17), tags=('focus', f'focus:{index}'))
        signal = state['phone_signal']
        phone_color = '#84b89a' if signal else '#88908e'
        c.create_rectangle(12, 51, 28, 78, outline=phone_color, width=2, tags='phone')
        c.create_line(17, 74, 23, 74, fill=phone_color, tags='phone')
        phone_text = 'vibrando' if view['phone']['vibrating'] else 'sinal' if signal else 'sem sinal'
        c.create_text(36, 64, text=phone_text, fill=phone_color, anchor='w', font=('Segoe UI', 10), tags='phone')
        heart = view['heart']['color']
        c.create_text(188, 53, text='♥', fill=heart, font=('Segoe UI', 17))
        c.create_text(204, 52, text=f"Vida {state['health']}", fill=TEXT, anchor='w', font=('Segoe UI', 11), tags='vitals')
        c.create_text(204, 74, text=f"Medo {state['fear']}", fill=TEXT, anchor='w', font=('Segoe UI', 11), tags='vitals')
        pulse = '#cf746a' if state['in_confrontation'] or state['fear'] >= 70 else '#839b91'
        c.create_line(288, 65, 294, 65, 298, 52, 303, 73, 308, 65, 318, 65, fill=pulse, width=2)

    def draw_scene(self):
        if self.screen != 'game':
            return
        c = self.canvas
        clear_canvas(c)
        w, h = max(c.winfo_width(), 600), max(c.winfo_height(), 300)
        game = self.session.game
        room = game.get_current_room()
        lit = game.light_visible
        c.create_rectangle(0, 0, w, h, fill='#161a1c', outline='')
        c.create_polygon(0, 0, w, 0, .78*w, .20*h, .22*w, .20*h, fill='#202628')
        c.create_polygon(0, h, w, h, .78*w, .66*h, .22*w, .66*h, fill='#353531' if lit else '#252724')
        c.create_polygon(0, 0, .22*w, .20*h, .22*w, .66*h, 0, h, fill='#353b3b' if lit else '#252b2c')
        c.create_polygon(w, 0, .78*w, .20*h, .78*w, .66*h, w, h, fill='#303536' if lit else '#222728')
        c.create_rectangle(.22*w, .20*h, .78*w, .66*h, fill='#4c5149' if lit else '#313735', outline='#555a52')
        for fraction in (.30, .45, .60, .75):
            c.create_line(fraction*w, h, (.22 + fraction*.56)*w, .66*h, fill='#41423c')
        c.create_text(16, 18, text=room.name, fill=TEXT, anchor='w', font=('Segoe UI', 14, 'bold'))
        c.create_text(16, 42, text='PRIMEIRA PESSOA • deslocamento entre cômodos', fill='#adb6b3', anchor='w', font=('Segoe UI', 9))
        entries = scene_sprites(room, game)
        columns = min(5, max(1, len(room.objects)))
        for index, (_, obj, state) in enumerate(entries):
            row, col = divmod(index, columns)
            position = obj.sprite.position or (.12 + .76*(col+.5)/columns, .40 + row*.19)
            size = 1
            title = obj.name
            if hasattr(obj, 'alive'):
                position, size = pose(obj)
                title = enemy_label(room, obj) + ' • ' + obj.distance
                if obj.trait:
                    title += '\n' + obj.trait
            x, y = w*position[0], h*position[1]
            self.assets.draw(c, obj, state, x, y, size=size, limit=(int(w*.2), int(h*.4)))
            c.create_text(x, y+43, text=title, fill='#b0b5aa', font=('Segoe UI', 9), width=w*.18)
        if game.game_over:
            c.create_rectangle(0, h*.35, w, h*.60, fill=BG)
            c.create_text(w/2, h*.47, text='JOSEPH NÃO RESISTIU — ESC para sair ou reinicie o teste', fill=TEXT, font=('Segoe UI', 13))
        if self.session.inventory_open or self.session.reading_text is not None:
            c.create_rectangle(0, 0, w, h, fill='black', stipple='gray50', outline='', tags='inventory_shade')

    def submit_command(self, event=None):
        source = event.widget if event is not None and isinstance(event.widget, tk.Entry) else self.command_entry
        command = source.get().strip()
        if command:
            if self.session.inventory_open and not inventory_command_allowed(self.session.game, command):
                message = 'Feche o inventário antes de explorar ou enfrentar a ameaça. Nenhuma ação foi executada.'
                self.session.last_message = message
                self.session.history.append((command, message))
                self.session.history_hints.append('')
                self.inventory_view.result.set(message)
                source.delete(0, 'end')
                self.refresh()
                self.inventory_view.entry.focus_set()
                return 'break'
            obj = self.session.inspection_object or self.session.reading_document
            self.session.parser.inspection_context = (obj.name if obj else '') if self.reader_window is not None else None
            try:
                self.session.execute(command)
            finally:
                self.session.parser.inspection_context = None
            source.delete(0, 'end')
            self.refresh()
            if self.reader_window is not None:
                self.reader_panel.response.set(self.session.parser.reaction
                    if self.session.parser.presentation in ('reading', 'inspection') else self.session.last_message)
            if self.session.inventory_open:
                self.inventory_view.result.set(self.session.last_message)
        (self.reader_panel.inspect_entry if self.reader_window is not None else
         self.inventory_view.entry if self.session.inventory_open else self.command_entry).focus_set()
        if self.session.parser.delayed_response is not None:
            game = self.session.game
            self.command_entry.configure(state='disabled')
            def finish_bell():
                if self.session.game is not game:
                    return
                self.session.finish_delayed_response()
                if self.screen == 'game':
                    self.refresh()
                    self.command_entry.configure(state='normal')
                    self.command_entry.focus_set()
            self.root.after(800, finish_bell)
        return 'break'

    def close_reader(self):
        if self.session.reading_text is not None:
            self.session.game.emit('document_close')
        self.session.reading_text = None
        self.session.reading_document = None
        self.session.inspection_object = None
        self.session.inspection_face = None
        if self.reader_window is not None:
            if self.root.grab_current() == self.reader_window:
                self.reader_window.grab_release()
            self.reader_window.destroy()
            self.reader_window = None
        if self.screen == 'game':
            self.command_entry.configure(state='normal')
            (self.inventory_view.entry if self.session.inventory_open else self.command_entry).focus_set()
            self.draw_scene()
        self.flush_audio()
        return 'break'

    def update_reader(self):
        self.command_entry.configure(state='disabled' if self.session.reading_text is not None
                                     and not self.session.inventory_open else 'normal')
        if self.session.inventory_open:
            if self.session.reading_text:
                if self.session.reading_document:
                    self.session.selected_item = self.session.reading_document.name
                    self.inventory_view.refresh()
                    self.inventory_view.result.set(self.session.last_message)
                else:
                    self.inventory_view.result.set(self.session.reading_text)
                self.session.reading_text = None
                self.session.reading_document = None
                self.session.inspection_object = None
            if self.reader_window is not None:
                self.reader_window.destroy()
                self.reader_window = None
            return
        if self.session.reading_text is None:
            if self.reader_window is not None:
                self.reader_window.destroy()
                self.reader_window = None
            return
        if self.reader_window is None:
            self.reader_panel = DocumentPanel(self)
            self.reader_window = self.reader_panel.frame
            self.reader_text = self.reader_panel.text
        self.reader_panel.refresh()

    def debug(self, action):
        self.session.debug(action)
        self.refresh()
        (self.inventory_view.entry if self.session.inventory_open else self.command_entry).focus_set()

    def key(self, event):
        # ESC navega pela interface; letras nunca executam ações de Joseph.
        if event.keysym == 'Escape':
            if self.screen == 'game':
                if self.reader_window is not None:
                    self.close_reader()
                elif self.session.inventory_open:
                    self.inventory_view.close()
                else:
                    self.pause()
            elif self.screen == 'pause':
                self.build_game()
            elif self.screen in ('options', 'tutorial_menu'):
                self.menu()
            return 'break'

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    VisualApp().run()





