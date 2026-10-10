"""Áudio offline na camada de apresentação. Arquivos ausentes = silêncio seguro."""
from pathlib import Path

SOUND_EVENTS = ('key_pickup', 'key_use', 'key_wrong', 'lock_unlock', 'door_open',
                'door_close', 'document_open', 'document_page', 'document_close',
                'document_collect', 'inventory_open', 'inventory_close')


class AudioPlayer:
    def __init__(self, directory=None, backend=None):
        self.directory = Path(directory) if directory else Path(__file__).parent / 'assets' / 'audio'
        self.backend = backend
        if backend is None:
            try:
                import winsound
                self.backend = lambda path: winsound.PlaySound(str(path), winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
            except ImportError:
                pass

    def handle(self, events):
        for event in events:
            name = event['name']
            if name not in SOUND_EVENTS:
                continue
            path = self.directory / (name + '.wav')
            if path.is_file() and self.backend:
                try:
                    self.backend(path)
                except (OSError, RuntimeError):
                    pass
