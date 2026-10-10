"""Papéis e pastas provisórios, sempre dentro da janela principal."""
import tkinter as tk
from visual_assets import clear_canvas

STYLES = {
    'bilhete': ('#c7b68c', '#302b23', 'PAPEL ENVELHECIDO', 'Georgia'),
    'carta': ('#d1c5a7', '#3e352f', 'CARTA DOBRADA', 'Georgia'),
    'relatório': ('#c8c9bc', '#252a27', 'EVOLUCYS — RELATÓRIO', 'Consolas'),
    'pasta': ('#ae9468', '#2c2923', 'EVOLUCYS — ARQUIVO', 'Consolas'),
    'diário': ('#bdb08d', '#322d28', 'PÁGINA DE DIÁRIO', 'Georgia'),
    'fotografia': ('#b5b1a5', '#282828', 'ANOTAÇÕES DA FOTOGRAFIA', 'Segoe UI'),
}


class DocumentPanel:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg='#242923', highlightthickness=2, highlightbackground='#8f8061')
        self.frame.place(relx=.5, rely=.5, anchor='center', relwidth=.78, relheight=.83)
        self.frame.lift()
        self.frame.grab_set()
        self.frame.bind('<Escape>', lambda event: app.close_reader())
        self.heading = tk.Label(self.frame, font=('Segoe UI', 13, 'bold'), pady=12)
        self.heading.pack(fill='x')
        self.art = tk.Canvas(self.frame, height=150, bg='#242923', highlightthickness=0)
        self.art.pack(fill='x')
        self.art.bind('<Configure>', lambda event: self.draw_art())
        controls = tk.Frame(self.frame, bg='#242923')
        controls.pack(side='bottom', fill='x')
        self.previous = app.button(controls, 'Página anterior', lambda: self.page(-1))
        self.previous.pack(side='left', padx=8, pady=8)
        self.counter = tk.Label(controls, bg='#242923', fg='#ddd9c9')
        self.counter.pack(side='left', expand=True)
        self.next = app.button(controls, 'Próxima página', lambda: self.page(1))
        self.next.pack(side='left', padx=8)
        self.back = app.button(controls, 'Voltar', app.close_reader)
        self.back.pack(side='right', padx=8)
        self.inspect_entry = tk.Entry(self.frame, bg='#242923', fg='#ddd9c9', insertbackground='#ddd9c9')
        self.inspect_entry.bind('<Return>', app.submit_command)
        self.inspect_hint = tk.Label(self.frame, bg='#242923', fg='#ddd9c9', font=('Segoe UI', 9), wraplength=750)
        self.response = tk.StringVar()
        self.response_label = tk.Label(self.frame, textvariable=self.response, bg='#242923',
                                       fg='#ddd9c9', wraplength=700)
        self.response_label.pack(side='bottom', fill='x', padx=12)
        self.text = tk.Text(self.frame, wrap='word', relief='flat', padx=24, pady=20)
        scroll = tk.Scrollbar(self.frame, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        self.text.pack(fill='both', expand=True)
        self.inspect_entry.focus_set()

    def page(self, step):
        self.app.session.turn_page(step)
        self.refresh()
        self.app.flush_audio()

    def refresh(self):
        session = self.app.session
        document = session.reading_document
        obj = session.inspection_object
        style = document.document_type if document else 'relatório'
        paper, ink, title, font = STYLES.get(style, STYLES['bilhete'])
        self.heading.configure(text=title + (f' • {document.name}' if document else ''), bg=paper, fg=ink)
        if obj:
            paper, ink, font = '#c7b68c', '#302b23', 'Georgia'
            face = {None: 'Inspeção', 'front': 'Frente', 'back': 'Verso', 'interior': 'Interior', 'open': 'Aberto', 'closed': 'Fechado', 'damaged': 'Danificado'}[session.inspection_face]
            self.heading.configure(text=obj.name.capitalize() + ' — ' + face, bg=paper)
            self.inspect_entry.pack(side='bottom', fill='x', padx=12, pady=5, before=self.text)
            hint = session.game.guide.current
            self.inspect_hint.configure(text=hint)
            if hint:
                self.inspect_hint.pack(side='bottom', fill='x', before=self.text)
            else:
                self.inspect_hint.pack_forget()
        else:
            self.inspect_entry.pack(side='bottom', fill='x', padx=12, pady=5, before=self.text)
            if session.game.guide.current:
                self.inspect_hint.configure(text=session.game.guide.current)
                self.inspect_hint.pack(side='bottom', fill='x', before=self.text)
            else:
                self.inspect_hint.pack_forget()
        self.text.configure(state='normal', bg=paper, fg=ink, font=(font, 12))
        self.text.delete('1.0', 'end')
        self.text.insert('end', session.reading_text or '')
        self.text.configure(state='disabled')
        count = len(document.pages) if document else 1
        self.counter.configure(text=f'{session.reading_page+1} / {count}')
        self.previous.configure(state='normal' if session.reading_page > 0 else 'disabled')
        self.next.configure(state='normal' if session.reading_page+1 < count else 'disabled')
        self.draw_art()

    def draw_art(self):
        clear_canvas(self.art)
        session = self.app.session
        obj = session.inspection_object
        x = max(200, self.art.winfo_width())/2
        if obj:
            self.art.configure(bg='#242923')
            self.app.assets.draw(self.art, obj, session.inspection_face or 'front', x, 75, size=3, limit=(500, 140))
        else:
            # Cabeçalho material do papel; o texto abaixo continua selecionável e rolável.
            doc = session.reading_document
            style = doc.document_type if doc else 'relatório'
            paper = STYLES.get(style, STYLES['bilhete'])[0]
            self.art.configure(bg=paper)
            self.art.create_line(24, 135, 2*x-24, 135, fill='#796c51')
            if style == 'carta':
                self.art.create_line(24, 20, x, 85, 2*x-24, 20, fill='#a29375', width=2)
            elif style == 'pasta':
                self.art.create_rectangle(24, 30, 180, 55, fill='#90764f', outline='')
                self.art.create_text(100, 43, text='ARQUIVO', fill='#ece1cb')
            elif style == 'relatório':
                self.art.create_text(30, 35, text='EVOLUCYS\nREGISTRO DE PESQUISA • ACESSO RESTRITO', anchor='nw', fill='#363a30', font=('Consolas', 12))
            else:
                self.art.create_line(25, 10, 35, 120, fill='#9a8561', width=2)
            if doc and doc.sprite.images:
                self.app.assets.draw(self.art, doc, 'front', x, 70, limit=(300, 120))
