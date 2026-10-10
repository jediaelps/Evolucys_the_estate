# Sons provisórios offline

Os 12 WAVs desta pasta são tons sintéticos curtos e discretos, criados para testar o fluxo de eventos. Todos são placeholders, sem gravações externas.

Substitua cada WAV pelo efeito definitivo mantendo seu nome:
key_pickup, key_use, key_wrong, lock_unlock, door_open, door_close,
document_open, document_page, document_close, document_collect,
inventory_open, inventory_close.

O parser apenas emite eventos. A interface drena a fila e AudioPlayer faz a reprodução assíncrona via winsound no Windows. Um som novo pode interromper o anterior; ainda não existe mixagem. Sem arquivos ou backend de áudio, o jogo continua silenciosamente. Outros sistemas podem fornecer um backend a AudioPlayer. Não há serviços online ou dependências pip.
