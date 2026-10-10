# Fase 4.5.4 — diálogos e memória contextual

## Comportamento

As falas existentes de Joseph são identificadas no histórico como `Joseph: “frase”`. Descrições autorais de salas, objetos e documentos, acontecimentos em terceira pessoa, comandos e dicas permanecem separados. `narrative.dialogue(emissor, texto, vocalization=False)` permite novos eventos com emissor explícito; vocalizações usam `Nome: *ação*`. Não foram acrescentados personagens ou falas de campanha.

`narrative.history_text` adapta os pensamentos legados por uma lista delimitada de aberturas já usadas no protótipo, protegendo conteúdo narrativo autoral. Novas falas devem usar o emissor explícito, sem depender desse adaptador. A formatação ocorre no histórico; não muda o resultado das ações.

`ThreatMemory`, associado a `ExplorationSystems`, registra contextos de percepção sonora, escuta de uma passagem e observação direta. Cada contexto guarda sinais identificados por criatura, localização e som, conhecimento interno e visitas já comentadas. Há estados desconhecido, suspeito, confirmado, conhecido e alterado. Eles não aparecem na interface.

A primeira percepção produz descoberta; a volta pode gerar um lembrete e voltas seguintes sem novidade podem ficar em silêncio. Escutar uma porta confirma o contexto. Cada observação compara a memória aos inimigos vivos e aos sinais reais naquele momento. Movimento, derrota, silêncio ou substituição invalidam a afirmação anterior. A memória não move inimigos, não prolonga sons nem congela o mundo. Mudanças remotas só geram comentários quando Joseph volta a observar aquele contexto.

Não há filtro global de frases nem sorteio aleatório: outro local ou uma mudança real podem justificar uma reação semelhante. A entrada e o processamento posterior do mesmo turno compartilham a observação para não duplicar a descoberta.

A memória acompanha a exportação/restauração adicional de exploração; estados antigos sem esse campo são aceitos. Continua não existindo save/load completo.

## Correções anteriores solicitadas

- Removida a enumeração automática “Você percebe: ...” das descrições de salas, inclusive ao entrar/olhar. Objetos continuam no cenário, disponíveis para investigação e interação conforme as regras anteriores.
- Abrir o inventário registra apenas “Inventário aberto.” no histórico. O terminal mantém a consulta dos itens com o título neutro “Inventário:”, sem “Joseph está carregando...”.
- Histórico mantém ordem cronológica, conteúdo ancorado embaixo, dicas e narração. Ajustado o momento de alinhamento para evitar callbacks pendentes ao destruir painéis.
- Layout, barra de comando, objetivo, HUD, dois raios, inventário e mecânicas preservados.

## Arquivos

Criados: `narrative.py`, `threat_memory.py`, `test_phase454.py` e este relatório.

Modificados: `exploration_systems.py`, `visual_session.py`, `world.py`, `command_parser.py`, `visual.py`, `test_look_around.py`, `test_phase452.py`, `README.md` e `GUI_README.md`.

Os testes antigos de olhar foram ajustados à remoção explicitamente solicitada das listas automáticas; a visibilidade dos itens revelados/coletados continua verificada no estado do mundo. A identificação da versão passou para 4.5.4.

## Testes executados

Na pasta do projeto:

```sh
python -B -m unittest test_phase454 test_phase452.SystemsTests -q
python -B -m unittest test_phase454 test_look_around test_command_history test_visual_session test_phase45.InspectionTests test_phase452.SystemsInterfaceTests -q
python -B -m unittest test_phase454 test_phase452.SystemsInterfaceTests test_command_history -q
```

As seleções aprovaram respectivamente **44**, **58** e **25** testes. Há sobreposição entre elas: foram **93 testes distintos**, incluindo **13 novos**. A última execução confirmou as correções finais do histórico e os dois casos adicionais de retorno real e mudança da ameaça. Nenhuma suíte completa foi executada.

Cobertura: identificação de emissores, vocalizações, preservação da narração/dicas, descoberta e retorno, confirmação de portas, mudança/morte/silêncio/substituição, ausência de repetição no mesmo evento, silêncio sem novidade, persistência adicional e histórico em 1100×760. As verificações existentes de exploração abrangem foco, sustos, percepção, rondas, esconderijos e iluminação.

Para validar manualmente, use `python visual.py` e o Tutorial: aproxime-se de uma ameaça audível, escute uma porta, recue e retorne. Compare descoberta e lembrança; avance uma ronda e escute novamente. Confira as falas identificadas e o inventário sem enumeração no histórico.

Nenhuma mecânica fora do escopo foi intencionalmente alterada. Esta versão é a **Fase 4.5.4**. A **Fase 5 não foi iniciada**.
