# Evolucys: The Estate — Fase 4.5

Extraia o projeto e execute `python visual.py`. Requer Python 3.8+ com Tkinter/Tk 8.6. O terminal continua disponível por `python main.py`. Nenhum acesso à internet é necessário.

## Como validar

1. Tutorial 1: `ler aviso fixo`. O papel aparece na janela principal com o texto completo. Avance pelas páginas e feche com ESC ou Voltar. O histórico conserva uma reação breve, sem copiar o documento.
2. Ainda no Tutorial 1: `examinar retrato`. Na entrada de comandos do painel, escreva `olhar atrás do retrato` e pressione Enter. A imagem muda para o verso e a inscrição aparece na área de leitura. `examinar retrato` retorna à frente. ESC fecha. Cada inspeção efetiva segue as mesmas regras de ação do jogo.
3. `olhar dentro da caixa` antes de abri-la é recusado. Depois de `abrir caixa`, o interior fica disponível. Objetos sem verso não podem ser virados. O retrato e a gaveta da campanha também têm faces configuradas.
4. Tutorial 2: `pegar carta antiga`, `inventário`, selecione a carta. Imagem, descrição e páginas ficam no painel integrado. `ler carta antiga` na entrada do inventário seleciona o documento, sem janela adicional nem cópia no histórico.
5. Observe a lanterna, use `pegar lanterna`: seu PNG desaparece da cena e ela aparece no inventário. `largar lanterna` devolve a mesma instância e sua imagem à sala.
6. Tutorial 4: entre ao norte e espere. O vigia muda de estado visual conforme alerta e preparação do golpe. Fugir e evitar confronto continuam disponíveis.

## Testes e compatibilidade

Execute na pasta extraída:

```text
python -B -m unittest discover -v
python -B visual_smoke.py
```

A suíte contém 163 testes: os 144 anteriores foram mantidos e 19 foram acrescentados. O smoke gráfico reúne 39 testes com widgets reais. A validação cobre conteúdo no painel, histórico resumido, frente/verso, inscrições, interior bloqueado, estados, coleta, inimigos, PNG/transparência, fallback, linguagem da interface e funcionamento offline. As regras de chaves, munição, itens e confronto permanecem.

## Arquivos criados e modificados

Criados: `visual_assets.py`, `test_phase45.py`, `FASE4_5.md`, `assets/README.md`, 47 PNGs em `assets/objects/` e `assets/enemies/`, documentos de reserva das demais pastas. Os 12 WAVs anteriores foram copiados para `assets/audio/`.

Modificados: `world.py`, `confrontation.py`, `command_language.py`, `command_parser.py`, `visual_session.py`, `visual.py`, `document_view.py`, `inventory_view.py`, `context_help.py`, `audio_events.py`, `tutorial.py`, `visual_smoke.py`, `README.md`, `GUI_README.md`.

## Organização e limites

Leia `assets/README.md` para configurar posição, escala, visibilidade, estado, ID e camada. Os caminhos são relativos ao projeto; não é necessário instalar Pillow ou baixar recursos. PNGs faltantes ou inválidos usam formas provisórias. O inventário e todos os leitores permanecem dentro da única janela principal.

As referências a parser e regras de implementação foram removidas das descrições e da ajuda do jogador. Conteúdo técnico permanece apenas no código, documentação e ferramentas de desenvolvimento. A área de tutorial conserva seus controles de treino existentes.

Os sprites e papéis são provisórios, não pixel art definitivo. Apenas objetos com faces configuradas recebem inspeção aproximada. Algumas pistas antigas continuam sendo reveladas ao examinar a frente para preservar os puzzles anteriores. A apresentação do ambiente tem área própria; `olhar em volta` conserva também seu registro histórico por compatibilidade. Ainda não há campanha completa, outras espécies de inimigos, animações, cutscenes, save em disco, mixagem ou instalador. Janela mínima: 1100×760. Validado em Windows; outras plataformas não foram verificadas.
