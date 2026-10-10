"""Apresentação de falas; não altera respostas do parser ou regras do mundo."""
import re


def dialogue(speaker, text, vocalization=False):
    """Emissor explícito para eventos atuais/futuros, sem criar personagens."""
    return f'{speaker}: *{text}*' if vocalization else f'{speaker}: “{text}”'


# Compatibilidade com os pensamentos em primeira pessoa já escritos no protótipo.
# Novos eventos podem usar dialogue() diretamente. Não é um filtro de repetição.
JOSEPH_OPENINGS = (
    'Não tenho ', 'Não preciso ', 'Preciso ', 'Droga...', 'Está trancada. Preciso ',
    'Meus bolsos ', 'Não sei ', 'Melhor ', 'Assim está melhor.', 'Esse chá...',
    'Ainda sinto ', 'Bebo ', 'Não vejo ', 'Não consigo ', 'Ligo ', 'Desligo ',
    'Minha lanterna ', 'Acendo ', 'Volto ', 'Já está carregada.', 'Recarrego ',
    'Não tenho ', 'Isso não é uma arma.', 'Está longe demais para eu ',
    'Ainda estou ', 'O que quero ', 'É melhor ', 'Já tenho ', 'Já há um desses aqui.',
    'Isso não vai me ajudar ', 'Essa chave não serve ', 'Talvez eu ',
    'Isso não encaixa ', 'Tem alguma coisa escrita ', 'Vou olhar ',
    'Em qual passagem quero ', 'Não estou ouvindo ', 'Acho que ouvi ',
    'Tem alguma coisa se mexendo ', 'Espera...', 'Estou mais atento...',
    'Levo um susto', 'Quase paralisei ', 'Meu corpo ', 'Não encontro ',
    'Ele está olhando para mim.', 'Fico imóvel,', 'Ele está aqui...',
    'Ouço ', 'Prendo a respiração.', 'Não posso me mexer ', 'Ele me encontrou!',
    'Os passos se afastam. Graças a Deus', 'O silêncio voltou.', 'Estou preparado,',
    'Ainda tô ouvindo ', 'Eu sei que ', 'Estranho...', 'Peraí...',
    'Ainda ouço ', 'Tem alguma coisa do outro lado ', 'O som ', 'Eu já vi ',
    'Tem algo diferente ',
    'Qual deles?', 'Está fechada. Preciso ', 'Não é assim que ',
)


def history_text(text, game):
    # Conteúdo autoral de cenários/objetos/documentos nunca é reclassificado
    # só por começar com palavras também usadas por Joseph.
    narrative = set()
    for room in game.rooms.values():
        narrative.update(room.description.splitlines())
        narrative.add(room.name)
    for obj in game.all_objects():
        narrative.update(obj.description.splitlines())
        for page in obj.pages:
            narrative.update(page.splitlines())
        for face in obj.inspection_faces.values():
            narrative.update(face.splitlines())
    lines = []
    for line in text.splitlines():
        if line not in narrative and line.startswith(JOSEPH_OPENINGS):
            # Instruções anexadas a respostas antigas continuam sendo instruções.
            parts = re.split(r' (?=(?:Digite|Use) )', line, maxsplit=1)
            lines.append(dialogue('Joseph', parts[0]))
            lines.extend(parts[1:])
        else:
            lines.append(line)
    return '\n'.join(lines)
