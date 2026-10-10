# Evolucys: The Estate — Fase 4.4

Execute `python visual.py` na pasta extraída. Requer Python 3.8+ com Tkinter e sessão gráfica. O terminal continua disponível por `python main.py`.

## Validação manual

- **Documento fixo:** Tutorial 1, `ler aviso fixo`. Use Próxima página e Página anterior; feche com Voltar ou ESC. O aviso permanece na sala e não ocupa slot. `pegar aviso fixo` é recusado.
- **Documento portátil:** Tutorial 2, `pegar carta antiga`, `inventário`. Clique na carta: todas as páginas aparecem na descrição com rolagem. Feche e digite `ler carta antiga` para usar o leitor de páginas. O mesmo objeto e seu estado de leitura são preservados.
- **Chave reutilizável/consumo:** Tutorial 3, `pegar chave de arquivo`, `usar chave de arquivo no armário a`. Confira que a chave continua no inventário. `usar chave de arquivo no armário b` abre a segunda fechadura e remove a chave com mensagem. Examinar e reabrir não a consomem. A chave de teste original é permanente. IDs futuros sem fechadura carregada mantêm a chave por segurança.
- **Pistola:** Tutorial 2, `pegar pistola`, `pegar munição de pistola`, `equipar pistola`, `recarregar`. Vai de 2/12 a 12/12, restando 2 dos 12 cartuchos de reserva do tutorial. Na campanha a reserva segue em 3. Dano base 35, sem mudança. O botão de teste Esvaziar arma permite repetir a recarga; não existe na campanha.
- **Modal e confronto:** Tutorial 4 continua validando ações e reações. Abrir inventário, consultar seleção, virar páginas e fechar painéis não gastam turnos. O comando `ler` mantém o custo anterior de uma ação e uma reação; depois disso o leitor bloqueia comandos físicos. Ações efetivas de itens no inventário continuam pelo parser e custam turnos.
- **Interface:** redimensione entre 1100×760 e tamanhos maiores. Os documentos e o inventário são Frames da única janela, com fundo escurecido, foco e rolagem. Joseph tem uma representação frontal de corpo inteiro com rosto, roupa, botas e marca de ferimento.

## Testes

`python -B -m unittest discover -v`: 144 testes, incluindo os 127 anteriores e 17 novos. As expectativas antigas de capacidade foram atualizadas de 6 para 12, preservando a verificação de sobras e recarga cheia.

`python -B visual_smoke.py`: 33 testes com widgets/eventos reais do Tk. A suíte gráfica acusa indisponibilidade do display em vez de alegar validação.

## Arquivos

Criados: `document_view.py`, `locks.py`, `audio_events.py`, `test_phase44.py`, este relatório, `audio/README.md` e 12 WAVs provisórios.

Modificados: `world.py`, `game_state.py`, `command_parser.py`, `command_language.py`, `context_help.py`, `items.py`, `tutorial.py`, `visual_session.py`, `visual.py`, `inventory_view.py`, `visual_smoke.py`, `test_survival.py`, `test_visual_commands.py`, `test_visual_session.py`, `README.md`, `GUI_README.md`.

## Áudio e limites

Eventos implementados: pegar/usar/chave incorreta; destrancar fechadura; abrir/fechar porta; abrir/virar página/fechar/coletar documento; abrir/fechar inventário. Todos os 12 sons são placeholders sintéticos locais. Arquivos ausentes não impedem jogar. Reprodução padrão no Windows, sem mixagem: efeitos simultâneos podem interromper uns aos outros. Veja `audio/README.md`.

A direção visual segue survival horror em primeira pessoa, mansão antiga escura, madeira envelhecida, umidade, luz quente e contraste cinematográfico. Pixel art detalhado permanece a referência para os sprites definitivos. Nesta fase, Joseph e os papéis usam formas, cores e fontes provisórias; bilhete, carta, relatório EVOLUCYS, pasta, diário e fotografia têm estilos configuráveis. Ainda não há arte final, animações, save em disco ou mixagem de áudio. Janela mínima de 1100×760; validado em Windows/Tk 8.6. Documentos e fechaduras usam o GameState existente, sem cópias paralelas. IDs automáticos de objetos são únicos na sessão; ao criar conteúdo persistente, forneça `object_id` explícito.
