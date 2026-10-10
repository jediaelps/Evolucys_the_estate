# Evolucys: The Estate — CAMPAIGN PROGRESS

## Estado atual

**Fase 5.0: documentação do mapa concluída em 08/10/2026.** Fonte oficial recebida no anexo `fb9eaad4-cebd-45cc-b87f-a5f6fdc68183/Texto colado.txt` e transcrita em [WORLD_DESIGN.md](WORLD_DESIGN.md).

**Estado atual: Fase 5.3B concluída estruturalmente.** E14 adicionado; 58 salas na campanha, seis no protótipo. Caminho E03/E14 livre e portões E14/G01 compartilhados/bloqueados. Validação ao final.

**Fase 5.1A: preparação de compatibilidade concluída em 08/10/2026**, somente documental. Estratégia detalhada na seção 10 de WORLD_DESIGN.md. **Fase 5.1B concluída**, conforme registro histórico abaixo. **Fase 5.1C validada; expansão 5.1D registrada abaixo.**

## Etapas planejadas e executadas

| Etapa | Estado | Entrega/limite |
|---|---|---|
| Fase 5.0 — análise da arquitetura atual | Concluída | Room, fábrica, GameState e seis ambientes inventariados; reutilização recomendada |
| Fase 5.0 — documentação do mapa oficial | Concluída | 52 ambientes, cinco setores, 61 ligações, sete ligações intersetoriais |
| Fase 5.0 — progressão e salvamento previstos | Documentados | Seis atalhos, queda, saída inicial, acesso secreto e seis pontos de save |
| Fase 5.0 — compatibilidade/migração | Documentada, execução pendente | Correspondências dos seis ambientes e conflitos listados |
| Fase 5.1A — compatibilidade e preparação | Concluída | Mapeamento funcional, aliases, nove conexões de T02, estados compartilhados e riscos documentados |
| Fase 5.1B — infraestrutura | Concluída | Resolução de IDs, passagens locais, estado compartilhado e conexões especiais, sem expansão da campanha |
| Fase 5.1C — recorte inicial | IMPLEMENTADO e validado | T01, T02, T03, T04, T05, T06, T08, T09, T11; B07/U01 preservados; dois atalhos bloqueados |
| Fase 5.1D — conclusão estrutural do térreo | IMPLEMENTADO | T07, T10 e T12; quatro conexões; nenhum novo setor |
| Fase 5.1E — andar superior | IMPLEMENTADO | Oito novas salas e oito ligações; porta de U01 integrada; protótipo preservado |
| Fase 5.1F — inspeção uniforme | IMPLEMENTADO | Painel compartilhado, descrição simples, entrada com foco e respostas contextuais |
| Fase 5.1G — ajuda, percepção e combate | IMPLEMENTADO | Etapas A/B/C validadas em ordem; sem expansão do mapa |
| Fase 5.1H — exterior e início canônico | IMPLEMENTADO | Treze salas externas, B01–B03, campainha, macaco, queda e poço condicionado |
| Fase 5.1I — porão principal | IMPLEMENTADO | B04–B10 completos, B07 reutilizado; sete ligações comuns e dois atalhos bloqueados |
| Fase 5.1J — laboratório e acessos | IMPLEMENTADO / VALIDADO | L01–L12; 13 conexões internas e entrada bloqueada; auditoria dos 56 ambientes |
| Fase 5.2 — prólogo e narrativa inicial | IMPLEMENTADO | Inspeções locais, conhecimento da manivela, campainha sem repetição e transição da queda |
| Fase 5.3A — garagem | IMPLEMENTADO | G01, porta interna aberta, portões externos bloqueados e roda apenas planejada |
| Fase seguinte | Não iniciada | Escopo futuro depende de autorização; abertura jogável antecipada por pedido explícito na 5.1H |
| Campanha e puzzles posteriores | Pendentes | Condições de desbloqueio, sequência, conteúdo e balanceamento a planejar |
| Save/load completo | Pendente | Cinco slots; normal reutilizável; difícil desbloqueável com uso único por ponto |
| Arte e áudio definitivos | Pendentes | Recursos existentes continuam provisórios |

Não foi construída a campanha completa. Somente os itens e eventos expressamente autorizados para a abertura foram acrescentados. As fases posteriores não foram automaticamente abertas.

## Registro da conclusão da Fase 5.0

- Atualizados somente `WORLD_DESIGN.md` e `CAMPAIGN_PROGRESS.md`.
- Registrados os catálogos oficiais E (9), T (12), U (9), B (10), L (12).
- Conexões repetidas entre seções da fonte consolidadas numa relação física única, preservando sentidos.
- Registrados tipos conhecidos e tipos ainda indefinidos, bloqueios, atalhos, fronteiras e pontos de salvamento.
- Conferidos IDs, nomes, adjacências, unicidade, destinos, sentidos, pontos de save e rota inicial contra a fonte.
- Nenhum código do jogo alterado. Nenhuma suíte ou teste de gameplay executado nesta atualização.

## Decisões técnicas mantidas

1. Reutilizar `Room`, `GameObject`, `create_world()` e o dicionário único de `GameState`; sem arquitetura paralela.
2. Separar planejamento (E01–L12 nos intervalos oficiais) e IDs de execução. Não renomear `entrance`, `main_hall`, `kitchen`, `office`, `cellar` ou `upper_hall` agora.
3. Montar ambientes e objetos antes das conexões. A 5.1C aplica isso ao recorte autorizado dentro de create_world(), com configuração isolada do protótipo.
4. Compartilhar estado físico de portas quando aplicável; validar casos por lado, especialmente a entrada principal.
5. Não criar retorno da queda, ligação externa de L12 ou outros caminhos ausentes para preencher lacunas.
6. Manter bloqueios e atalhos como estados do mundo na futura implementação. Saber o nome da entrada secreta não satisfaz sua condição de acesso.
7. Garantir a primeira saída B01 → B02 → B03 → T12 antes de exigir acesso ao complexo.
8. Preservar a queda antes de obter a barra procurada para o macaco do carro. O evento foi autorizado nesta revisão 5.1H e ocorre em E08.
9. Atribuir identidades persistentes para portas, pontos de salvamento e futuras entidades quando sua implementação for autorizada; não confundir UUID gerado em cada sessão com identidade durável.

## Pendências anteriores e resolução

| ID anterior | Situação após receber o mapa |
|---|---|
| P01 — fonte oficial | Resolvida: texto do usuário recebido e referenciado |
| P02 — setores e ambientes | Resolvida: cinco setores e 52 IDs/nomes de planejamento registrados |
| P03 — correspondência com protótipo | Seis equivalências funcionais confirmadas na 5.1A; execução da migração e revisão espacial pendentes |
| P04 — sentidos e retornos | Topologia oficial transcrita; queda é unidirecional. Geometria e destino final de L12 permanecem abertos |
| P05 — portas/bloqueios/atalhos | Estados fornecidos e seis atalhos registrados; condições exatas futuras |
| P06 — salvamento | Seis locais e regras registrados; justificativas profundas e implementação pendentes |
| P07 — fronteiras e início | Fronteiras registradas; prólogo parte do exterior, enquanto a base inicia na mansão. Migração para E01 concluída na revisão 5.1H |
| P08 — direções e estados por lado | Continua pendente; T02 possui nove conexões, e a porta principal tem restrição externa |

## Preparação da migração — Fase 5.1A

Mapeamento confirmado funcionalmente: `entrance → T01`, `main_hall → T02`, `kitchen → T05`, `office → T08`, `cellar → B07`, `upper_hall → U01`. Fundamentação, riscos e contrato detalhados nas seções 7 e 10 de WORLD_DESIGN.md; IDs do executável continuam antigos.

Decisões desta preparação:

- Uma Room por chave real; aliases separados de `rooms`. Primeiro preservar as chaves existentes; depois normalizar referências e migrar para IDs oficiais em conjunto, quando autorizado. Não criar segundo mundo nem duplicar salas para aceitar nomes antigos.
- Uma chave local por conexão; nomes em `exit_names` e desambiguação contextual para as nove ligações de T02. Direções herdadas mantidas nas conexões compatíveis, sem tratá-las como planta cardinal oficial.
- Remover os dois sentidos da ligação salão/cozinha somente junto da implantação de uma rota oficial disponível. Alias não substitui caminhos nem cria teleporte. Início atual preservado.
- Uma instância de porta por ligação de estado comum. Assimetria da porta externa depende de definição. Atalhos, queda e acesso B10/L01 seguem a fonte, sem condições inventadas.
- Revisar, na implementação, consumidores de IDs e nomes: comparações em `command_language.py`, resolução de escuta, visitas, rondas e memória/exportação parcial. A condição secreta precisa bloquear todos os caminhos de execução; descoberta e liberação são distintas.

## Expectativas antigas de testes — histórico da 5.1A, resolvidas na validação final da 5.1C

Arquivo `test_inventory_stairs.py`, classe `InventoryStairsTests`:

| Teste | Resultado observado na 5.1A | Atualização necessária |
|---|---|---|
| `test_upper_room_objects_and_unfinished_door_have_explanations` | Falha ao exigir `quadro antigo` no resultado de “olhar em volta” | Retirar a exigência de listar automaticamente cada objeto. Validar a descrição imersiva; conferir objetos visíveis e exame individual separadamente, mantendo a verificação da porta trancada. Não alterar `Room.describe()` para satisfazer a expectativa antiga. |
| `test_help_recognizes_stairs_and_inventory_mouse_exception` | Falha ao exigir a frase fixa `tentar subir`; a ajuda atual sugere EXAMINAR retrato e seguir ao SUL, identificada como Joseph | Validar ajuda contextual coerente com o estado e sem consumo de turno, sem obrigar uma sugestão de escadas em todo contexto. Revisar também a exigência antiga de `clique` na ajuda de inventário, cuja asserção não foi alcançada nesta execução, conforme a ajuda imersiva da 4.5.5. Testar comandos de escadas e seleção por mouse nos componentes próprios. |

As falhas são expectativas antigas reproduzidas **antes de qualquer alteração documental**; não são regressões introduzidas pela 5.1A. Nenhum teste foi reescrito para ocultá-las e nenhuma decisão narrativa da 4.5.5 foi revertida. A atualização ficou pendente naquela etapa e foi aplicada na validação final da 5.1C, registrada ao fim deste documento.

## Verificações direcionadas da Fase 5.1A

Executados uma vez com `python -B -m unittest`, somente seis métodos de `test_inventory_stairs.InventoryStairsTests`:

- Os dois métodos da tabela acima: **2 falhas de expectativa conhecidas**, registradas para atualização.
- `test_all_up_aliases`, `test_all_down_aliases`, `test_vertical_movement_requires_local_connection`, `test_blocked_stairs_explain_cause_both_directions`: **4 aprovados**. Confirmam aliases de subir/descer/retorno, exigência de conexão local e bloqueio de escadas nos dois sentidos.

Conferência documental direcionada: catálogo de 52 IDs e 61 ligações preservado; nove vizinhos de T02 iguais à proposta; rota E07 → B01 → B02 → B03 → T12 mantida, sem arco inverso da queda; B10/L01 continua condicionado. Comparação de hashes dos arquivos confirma alterações apenas nos dois documentos. Nenhum código, teste, interface ou mecânica alterado. A suíte completa não foi executada.

## Decisões ainda abertas

- Direções cardinais, geometria, comprimentos, pisos relativos e classificação física das ligações comuns.
- Nove conexões de T02 implementadas na 5.1D; condições definitivas de liberação dos atalhos ainda pendentes.
- Condições de desbloqueio, lados de acionamento e proteção contra contorno prematuro pelo retorno.
- Justificativa física casinha/subterrâneo; disponibilidade inicial da escada B03/T12; acesso vertical depósito/sótão.
- Evento/mecanismo e justificativa da entrada B10/L01, sem inventar puzzle nesta etapa.
- Destino final após L12: a fonte não especifica ligação externa. Registrar antes de qualquer expansão do grafo.
- Justificativas para sinal localizado em B03 e comunicação em L03/L11; nenhum dispositivo foi criado.
- Desbloqueio da dificuldade difícil, escopo da marca de uso único e comportamento ao carregar saves; formato versionado e interface de cinco slots ainda futuros.
- Recorte seguinte depende de nova autorização. A troca de topologia salão/cozinha foi concluída na campanha em 5.1C, com protótipo isolado. Resolver aliases em execução está implementado; migração persistente de dados/chaves continua pendente; as expectativas antigas dos testes foram corrigidas na validação final da 5.1C.

## Resultado da conferência documental da Fase 5.0

**52 IDs únicos: E=9, T=12, U=9, B=10, L=12.** Nomes e conjunto de ligações iguais à fonte; 61 ligações únicas (60 bidirecionais e a queda unidirecional), sete entre setores e seis pontos previstos de salvamento: E03, T02, U08, B03, L03 e L11.

Rota B01 → B02 → B03 → T12 presente sem passar pelo complexo. Entrada B10 ↔ L01 documentada como condicionada. Nenhum ambiente adicional, nenhum destino inexistente e nenhuma ligação de retorno inventada. Topologia completa conectada; disponibilidade com os futuros bloqueios exige validação posterior.

Não há contradição de adjacências na fonte oficial. O conflito concreto com a base é salão/cozinha diretamente conectados; lacunas de geometria, saída de L12 e condições de progresso estão registradas sem soluções inventadas.

## Próximas tarefas — somente após autorização

1. Definir e autorizar o recorte posterior à 5.1D. Não expandir automaticamente o mapa.
2. Definir orientação e futuras condições de desbloqueio sem inventar puzzles. A rota substituta salão/cozinha já está validada. As duas expectativas narrativas antigas foram corrigidas na validação final da 5.1C.
3. Na futura implementação autorizada, validar o grafo e os estados desse recorte com verificações direcionadas.
4. Planejar a Fase 5.2 separadamente, preservando a queda e a rota de saída inicial.
5. Manter puzzles, save/load completo, arte e áudio definitivos como entregas posteriores.

**Parada atual:** Fase 5.1E, sem iniciar a 5.1F. Os registros de fases anteriores abaixo são históricos.


## Registro da implementação — Fase 5.1B

- Contrato e exemplos de uso na seção 11 de WORLD_DESIGN.md; ela complementa o plano histórico da 5.1A.
- IDs antigos/oficiais resolvem a mesma Room por `get_room()`/`resolve_room_id()`. O dicionário único conserva suas chaves reais; nenhum ambiente foi duplicado ou criado na campanha.
- Resolução consistente de passagens nomeadas e escuta, com nove conexões validadas em cenário mínimo e preservação da intenção pendente.
- `Room.connect()` compartilha porta/estado e só cria retorno explícito. `PassageState` separa descoberta, liberação e tipo de conexão.
- Segredos não são descobertos por nomes antecipados; atalhos dependem do estado do mundo; quedas ficam fora da caminhada/ronda. Nenhum evento de campanha foi criado.
- Seis salas e suas ligações originais mantidas, inclusive salão/cozinha; início em `entrance`. VisualSession foi examinado e testado, sem alteração de código.

Arquivos alterados: `world.py`, `game_state.py`, `action_context.py`, `command_parser.py`, `command_language.py`, `exploration_systems.py`, `context_help.py`, `WORLD_DESIGN.md`, `CAMPAIGN_PROGRESS.md`. Criado `test_map_infrastructure.py`. Nenhuma alteração de layout, HUD, inventário, combate, regras de medo/confiança/foco, arte, áudio ou conteúdo das demonstrações.

### Testes direcionados e resultados

**64 testes distintos aprovados**, sem suíte completa:

- 11 novos testes de `test_map_infrastructure.MapInfrastructureTests`.
- `test_game.ExplorationTests.test_complete_puzzle_and_return`: cadeia original de objetos/chaves, acesso ao porão, documento e retorno.
- `test_phase455`: classes `PassageTests`, `HelpTests` e `NarrationTests`.
- `test_phase454.NarrativeTests`, `test_help_cleanup` e `test_action_narration`.
- Quatro métodos de escadas de `test_inventory_stairs`: aliases de subida/descida, exigência de conexão local e bloqueio nos dois sentidos.
- Quatro métodos de `test_phase452.SystemsTests`: sinônimos de escuta, ciclo de ronda/esconderijo, portas fechadas e consultas gratuitas nas rondas, percepção somente com som.
- Dois métodos de `test_visual_session.VisualSessionTests`: isolamento das quatro demonstrações e possibilidade de evitar combate.

Na primeira execução dos testes novos, duas asserções de teste precisaram de correção: restaurar a sala de origem antes da segunda consulta e conferir ausência de DICA no histórico apresentado, em vez de exigir vazio no buffer interno legado de dicas. Após a correção, os 11 testes novos passaram; não houve mudança de ajuda ou histórico para satisfazer essas asserções. As duas expectativas antigas registradas na 5.1A continuam pendentes e não foram incluídas nesta seleção; não se afirma que a suíte completa passa.

Não foram encontradas incompatibilidades nos componentes verificados. Limites explícitos: consumidores de IDs alternativos devem usar a API de resolução; exportação/importação parcial não migra saves arbitrariamente renomeados; gatilho da queda, assimetria externa da porta principal e condições narrativas ainda precisam de implementação autorizada. Os **52 ambientes não foram implementados**. **Fase 5.1C não iniciada.**


## Registro da implementação — Fase 5.1C

**IMPLEMENTADO:** onze ambientes e doze ligações bidirecionais. Lista completa de salas, estados e procedimentos na seção 12 de WORLD_DESIGN.md. T03, T04, T06, T09 e T11 são as cinco salas acrescentadas; T01/T02/T05/T08/B07/U01 reutilizam as instâncias e conteúdo existentes. Não houve renomeação das seis chaves antigas nem duplicação de salas.

**IMPLEMENTADO:** rotas salão → jantar → cozinha e salão → estar → jantar → cozinha, com retornos. Removidos os dois sentidos da ligação direta salão/cozinha na campanha. Atalhos salão/biblioteca e salão/porão bloqueados em ambos os lados; biblioteca acessível pelo escritório. B07 está instanciado, mas sua exploração desde o início depende de etapa futura: não declarar o acesso livre como concluído.

**IMPLEMENTADO:** configuração `prototype` preserva a demonstração de seis salas, a topologia antiga e o conteúdo. Lançador visual: `python prototype_demo.py` dentro de outputs. A campanha padrão usa `configuration='campaign'`. Objetos herdados permanecem nos mesmos lugares, sem assumir distribuição definitiva da campanha. Tutoriais e demonstrações de sistemas continuam com seus próprios cenários existentes.

**PLANEJADO:** demais 41 ambientes, conexões ausentes do recorte, conteúdo definitivo, prólogo, queda e acesso ao complexo. **PENDENTE:** condições de liberação dos atalhos, planta cardinal e escopo da 5.1D. **Fase 5.1F reservada:** comandos uniformes em todos os objetos inspecionáveis; nenhuma mudança em document_view.py, inspeção ou manipulação foi feita.

### Arquivos desta entrega

- Alterados: `world.py`, `game_state.py`, `visual_session.py`, `action_context.py`, `command_parser.py`, `test_map_infrastructure.py`, `test_game.py`, `WORLD_DESIGN.md`, `CAMPAIGN_PROGRESS.md`.
- Criados: `prototype_demo.py`, `test_campaign_map.py`.
- `test_game.py` passou a selecionar explicitamente o protótipo em sua preparação. Em `test_map_infrastructure.py`, as verificações de seis salas/demonstração selecionam `prototype`; a contagem da campanha passa a onze. Não foram relaxadas verificações de mecânicas nem alteradas as duas expectativas antigas sobre narrativa.
- `Room`, `PassageState`, resolvedor de IDs e exploração foram reutilizados. O corpo original que constrói salas, objetos, documentos e inimigos foi conferido por AST e preservado; a configuração oficial é aplicada ao final. Não houve alteração de layout/HUD, inventário, combate, medo, confiança, foco, memória, save, arte, áudio ou comportamento de inimigos.

### Testes executados

**71 testes distintos aprovados, nenhuma falha e nenhuma suíte completa executada.** Duas execuções direcionadas: 35 e 37 testes; o teste da cadeia original de puzzles/retorno está presente nas duas, portanto não é contado duas vezes.

Primeira seleção (35 aprovados):

- `test_campaign_map.CampaignMapTests`: 11 testes do recorte, aliases, grafo exato, rotas/retornos, bloqueios, ausência de destinos não implementados, contexto, isolamento e preservação de objetos.
- `test_map_infrastructure`: 11 testes de infraestrutura, incluindo segredos e queda em cenários mínimos.
- `test_phase455.PassageTests`: 8 testes de linguagem/contexto e cautela.
- `test_game.ExplorationTests.test_complete_puzzle_and_return`: demonstração antiga até o porão e retorno.
- Quatro testes de `test_inventory_stairs`: aliases de subir/descer, conexão local obrigatória e bloqueio nos dois sentidos.

Segunda seleção (37 aprovados):

- `test_campaign_map.CampaignDisplayTests`: integração dos onze ambientes e lançador do protótipo na interface existente, usando widgets Tkinter reais.
- `test_game`: módulo da demonstração e terminal, incluindo recursos, independência de partidas, saída e reinício.
- `test_phase455.HelpTests`, `test_phase455.NarrationTests`, `test_help_cleanup` e `test_action_narration`.
- Quatro métodos de `test_phase452.SystemsTests`: sinônimos de cautela, ciclo de esconderijo/ronda, respeito a portas fechadas/consultas gratuitas e roundtrip do estado parcial.
- Dois métodos de `test_visual_session.VisualSessionTests`: isolamento dos quatro tutoriais e possibilidade de evitar combate.

### Problemas identificados e limites

O estado real antes da alteração ainda era o protótipo de seis salas: nenhuma parte do recorte estava implementada. Os conflitos eram a ligação direta salão/cozinha e o acesso antigo ao porão mediante chave. Foram resolvidos na configuração de campanha, preservando o protótipo separadamente. O retorno natural “voltar ao salão principal” precisava passar pelo resolvedor local; foi acrescentado sem busca de caminhos intermediários. As suítes direcionadas passaram na primeira execução.

Testes antigos que pressupõem a topologia da demonstração devem escolher a configuração `prototype`; os arquivos exercitados nesta entrega foram ajustados onde necessário. As duas expectativas antigas de texto já registradas na 5.1A continuam pendentes e não foram executadas; não se declara a suíte completa aprovada. O catálogo oficial de 52 ambientes permanece documental e não foi expandido além do recorte autorizado.

**Encerramento:** Fase 5.1C concluída. Próximo passo recomendado: definir o recorte autorizado da 5.1D e seus critérios de desbloqueio/integração antes de implementar. **Fase 5.1D não iniciada; Fase 5.1F apenas registrada.**


## Fase 5.1C — correção final dos testes e validação

Esta atualização encerra as pendências de expectativas de testes registradas anteriormente. Não altera o jogo, o mapa oficial, o início padrão da campanha ou o planejamento dos 52 ambientes. Registros de falhas/pendências nas seções históricas acima descrevem as execuções anteriores.

### Correções e causas

- `test_confrontation.py`: todas as três instâncias de `GameState`, incluindo reinicialização e partida auxiliar, agora usam `configuration='prototype'`. Esses cenários pressupõem encontros e acessos do protótipo, incompatíveis com o bloqueio oficial T02/B07. As verificações de dano, turnos, fuga, cautela e reação foram preservadas.
- `test_survival.py`: configuração `prototype` na preparação e na instância auxiliar de independência da arma. Preservadas as verificações de recursos, consumo, munição e reações.
- `test_inventory_stairs.py`: observação geral exige descrição narrativa; exame individual verifica descrição, acessibilidade e registro de investigação dos quatro objetos. Porta trancada continua impedindo deslocamento. A ajuda verifica orientação sobre objetos conhecidos ou caminhos livres, identificação de Joseph, ausência de segredos, snapshot/turnos preservados e subida/descida funcional. Não exige enumeração automática, frase fixa de escadas ou instrução textual de clique; seleção e ações por mouse continuam cobertas pelos testes de widgets existentes.
- `test_ux.py`: expectativa de caminho inexistente aceita a fala aprovada de Joseph e verifica localização inalterada e consumo do turno de tentativa; comando desconhecido mantém sua resposta distinta e não avança turno.
- `test_inventory_window.py`: falha adicional descoberta na execução gráfica. O teste de escadas esperava o nome antigo “Corredor Superior”; agora valida “Galeria Superior”, identidade U01 e retorno ao salão. Não altera texto nem interface de produção.

Arquivos modificados nesta correção: os cinco testes acima e `CAMPAIGN_PROGRESS.md`. Nenhum teste foi removido, ignorado ou convertido em verificação sem efeito. O número de testes permaneceu 312. `WORLD_DESIGN.md` e todos os arquivos de produção permaneceram intactos, conferidos por hashes antes/depois.

### Execuções e resultados reais

1. Direcionados: `python -B -m unittest test_confrontation test_survival test_inventory_stairs test_ux` — **61 aprovados, 0 falhas, 0 ignorados**.
2. Suíte geral executada **uma única vez**, como solicitado: `python -B -m unittest discover -s . -p "test_*.py" -q` — **312 executados, 311 aprovados, 1 falha, 0 ignorados**, em 24,493 s. A única falha foi a expectativa visual do nome antigo de U01, descrita acima. Os testes de campanha oficial, demonstrações e interação por mouse passaram nessa execução.
3. Após corrigir exclusivamente esse teste visual: `python -B -m unittest test_inventory_window.InventoryWindowTests.test_stairs_full_visual_flow` — **1 aprovado, 0 falhas, 0 ignorados**. A suíte geral não foi repetida.

**Resultado consolidado:** os 312 testes tiveram resultado aprovado nas execuções acima; nenhuma falha permanece pendente e nenhum teste foi ignorado. Isso não significa que a execução única da suíte geral terminou verde: ela registrou uma falha, corrigida e confirmada no reteste isolado. O levantamento externo informado pelo usuário ignorava 54 testes; aqui Tkinter estava disponível e os testes gráficos também foram executados, revelando a expectativa adicional de nome.

### Preservação e pendências

`GameState()` continua selecionando a campanha oficial de 11 ambientes, com os atalhos bloqueados e sem ligação direta salão/cozinha. A demonstração `prototype` continua funcional. Nenhuma mecânica, item, inimigo, conteúdo narrativo, layout, HUD, inspeção, arte ou áudio foi alterado.

Não há pendência de falha de teste identificada nesta validação. Permanecem somente as pendências de desenvolvimento já documentadas: demais ambientes/conteúdo, condições futuras de liberação, persistência e inspeção uniforme reservada à 5.1F. **A versão continua na Fase 5.1C; Fase 5.1D não iniciada.**


## Registro da Fase 5.1D — térreo completo em estrutura

**IMPLEMENTADO:** T07, T10 e T12, totalizando 14 salas únicas. Adicionadas T05/T07, T09/T10, T02/T12 e T05/T12; nove conexões reais em T02. As três ligações comuns estão disponíveis provisoriamente porque a fonte não define seu estado inicial. T05/T12 permanece bloqueada, sem condição de desbloqueio inventada. T02/T09 e T02/B07 seguem bloqueadas. Os três estados físicos são compartilhados nos dois lados.

**PLANEJADO:** E06/T07, inicialmente inacessível, e B03/T12, importante para a saída subterrânea. Não há arcos nem salas fictícias para esses destinos. Os outros 38 ambientes permanecem fora da execução.

**PENDENTE:** distribuição definitiva de itens; inspeção uniforme (5.1F); puzzles; organização de pastas e renomeações sem duplicação; remoção futura de Tutorial do menu do jogador preservando os testes técnicos; prólogo/queda; validação definitiva dos estados provisórios. Nenhuma dessas atividades foi implementada nesta entrega.

Arquivos alterados: `world.py`, `test_campaign_map.py`, `test_map_infrastructure.py`, `WORLD_DESIGN.md` e `CAMPAIGN_PROGRESS.md`. Nenhum arquivo novo. Somente a configuração de campanha da fábrica foi expandida; GameState, parser, exploração, interface, inspeção, menu, recursos e mecânicas ficaram intactos.

Os testes do mapa foram atualizados para o conjunto exato de 14 salas/16 ligações, ampliando navegação, bloqueios, ausência de destinos futuros e renderização. Acrescentados três testes: novas rotas nos dois sentidos, identificação das nove conexões reais do salão e preservação dos bloqueios após visita. O teste de bloqueios usa uma partida nova por sentido e remove o vigia somente da fixture para impedir que combate/morte mascare uma falha de deslocamento.

Problemas encontrados durante a validação direcionada: cinco passos do teste anterior de retorno ficaram inicialmente no método novo durante a edição; foram recolocados no teste original, sem alteração do jogo. Uma tentativa de reteste foi lançada fora de outputs e não importou os módulos; foi corrigido apenas o diretório de execução. Não foi necessário modificar mecânicas.


### Resultados da validação 5.1D

- Seleção direcionada: `python -B -m unittest test_campaign_map test_map_infrastructure test_phase455.PassageTests test_game.ExplorationTests.test_complete_puzzle_and_return` — 35 testes, inicialmente 34 aprovados e uma falha de montagem de teste. Após a correção, os dois métodos afetados foram reexecutados e aprovados. Resultado direcionado consolidado: **35 aprovados**, sem falhas pendentes ou ignorados.
- Suíte geral, executada **uma vez**: `python -B -m unittest discover -s . -p "test_*.py" -q` — **315 aprovados, 0 falhas, 0 erros, 0 ignorados**, em 26,012 segundos. Inclui os testes gráficos com Tkinter e os três testes novos; a base anterior tinha 312.
- Verificação de escopo por hashes: somente os cinco arquivos listados acima foram modificados. Catálogo oficial de 52 ambientes e 61 ligações documentais preservado.

Nenhuma incompatibilidade remanescente identificada. Protótipo de seis salas e sua progressão aprovados, assim como aliases, contexto, cautela, estados de portas, inventário e testes gráficos. Próximo passo recomendado: definir o próximo recorte e suas condições de integração, mantendo as pendências separadas. **Fase 5.1D concluída; nenhuma fase seguinte iniciada.**


## Registro da Fase 5.1E — andar superior

**IMPLEMENTADO:** U02, U03, U04, U05, U06, U07, U08 e U09. Oito conexões oficiais bidirecionais disponíveis provisoriamente: U01/U02, U01/U03, U01/U04, U01/U08, U02/U06, U03/U05, U06/U07, U07/U09. Total: 22 ambientes e 24 ligações / 48 arcos. T02/U01 e os três atalhos bloqueados foram preservados. Nenhuma sala duplicada, saída extra ou mecanismo novo.

A porta de quarto já existente em U01 representa agora U01/U02 na campanha, compartilhada e inicialmente aberta/destrancada. Seu nome foi preservado; a descrição da galeria foi alinhada ao novo estado. Pedidos genéricos de quarto podem exigir esclarecimento. `prototype` mantém a porta trancada e sem destino, os seis ambientes e toda a progressão. Estados novos são provisórios, não regras definitivas. Não foi ativado o salvamento previsto em U08.

**Arquivos modificados:** `world.py`, `test_campaign_map.py`, `test_map_infrastructure.py`, `test_inventory_stairs.py`, `WORLD_DESIGN.md` e `CAMPAIGN_PROGRESS.md`. Nenhum arquivo novo. Não houve alteração de GameState, parser, exploração, mecânicas, interface, HUD, inspeção, áudio ou menu. Joseph continua sendo o protagonista. A única porta reaproveitada é um objeto de conexão, não um item ou puzzle novo.

Testes atualizados para o grafo exato de 22 ambientes/48 arcos e renderização das novas salas. Acrescentados três testes: navegação nominal nos oito pares, porta compartilhada U01/U02 com preservação do protótipo, e rota desde o início ao sótão/varanda com cautela e ausência de evento de save. O teste da porta de quarto inacabada passou a escolher `prototype`, mantendo suas verificações originais.

**Problema encontrado:** o novo teste inicialmente esperava que “porta de quarto” selecionasse U02 automaticamente; com vários quartos, o resolvedor aprovado pede esclarecimento. Corrigida a expectativa para exigir a pergunta sem turno e completar com “a do quarto principal”. Não foi alterado o parser nem simplificada a ambiguidade.

**PLANEJADO/PENDENTE:** 30 ambientes restantes, organização de arquivos, renomeações sem duplicação, remoção futura do Tutorial do menu, padronização da inspeção, distribuição definitiva de itens, puzzles, narrativa completa e prólogo/queda. Solução física do acesso ao sótão e estados definitivos das ligações ainda precisam de validação. Não implementados nesta fase.


### Validação 5.1E

- Direcionados: `python -B -m unittest test_campaign_map test_map_infrastructure test_inventory_stairs test_game.ExplorationTests.test_complete_puzzle_and_return` — 38 executados, inicialmente 37 aprovados e uma falha de expectativa de desambiguação, descrita acima. Após a correção, `test_campaign_map.CampaignMapTests.test_gallery_door_is_one_real_shared_connection` passou isoladamente. Resultado consolidado: **38 testes direcionados aprovados**, nenhum ignorado ou falha pendente.
- Suíte geral executada uma vez: `python -B -m unittest discover -s . -p "test_*.py" -q` — **318 aprovados, 0 falhas, 0 erros, 0 ignorados**, em 24,747 segundos. Inclui os testes gráficos e três novos testes sobre a base de 315.
- Hashes antes/depois confirmam somente os seis arquivos declarados alterados. Catálogo documental de 52 ambientes e 61 ligações preservado.

Não há incompatibilidade remanescente identificada nos testes. Protótipo, progressão, recursos e sistemas aprovados foram preservados. Próximo passo: revisar e autorizar o escopo da próxima entrega. **Fase 5.1E concluída. Fase 5.1F não iniciada.**


## Registro da Fase 5.1F — padronização da inspeção

**IMPLEMENTADO:** objetos comuns agora usam o mesmo DocumentPanel das inspeções especiais, com descrição real e campo de comandos, sem exigir `inspection_faces` artificiais. O campo também permanece disponível para documentos. ENTER executa uma única vez, permite edição normal e devolve o foco ao campo. Respostas ficam visíveis no painel; ESC/Voltar restauram a exploração. A entrada principal fica desabilitada enquanto o painel está ativo. No inventário, permanece apenas a entrada já existente, sem sobrepor outro leitor.

Componentes reutilizados: `CommandParser.examine/inspect_face/read`, `VisualSession`, `DocumentPanel` e a integração de leitura do inventário. `inspection_text` transporta a descrição simples; não há segunda instância de mundo, objetos ou inventário. A restrição do leitor passou da pré-validação da interface para o parser existente, após normalização e antes da execução física. Assim, erros de identificação e comandos desconhecidos recebem as respostas existentes; comandos autorizados continuam usando o mesmo caminho de execução.

**Limite de contexto preservado:** dentro do painel são permitidos examinar/observar/ler o objeto atual, consultar faces já suportadas e fechar a leitura. Pegar, equipar, abrir, mover e demais ações externas exigem voltar à exploração (ou ao inventário quando aplicável). Não há novas funcionalidades em objetos comuns. Faces inexistentes, interior trancado e inacessibilidade mantêm as validações existentes. Conhecer o nome de um conteúdo não o libera. A revelação de objetos ocultos continua somente nas ações já previstas; olhar em volta não ganha listagem automática.

**Turnos:** examinar/ler/inspecionar continuam com o custo original, inclusive falhas reconhecidas e reação inimiga quando aplicável. Exibir o painel não repete a ação. Fechar, redimensionar e paginar não consomem turnos. Comandos proibidos no contexto e desconhecidos não executam ações físicas.

**Arquivos modificados:** `command_parser.py`, `visual_session.py`, `document_view.py`, `visual.py`, `test_phase44.py`, `test_visual_commands.py`, `test_visual_ux.py`, `test_inventory_window.py`, `test_phase455.py`, `test_help_cleanup.py`, `CAMPAIGN_PROGRESS.md` e `WORLD_DESIGN.md`. **Arquivo criado:** `test_phase51f.py`, com dez testes novos. A expectativa antiga do leitor em `test_phase44.py` foi atualizada de foco no botão Voltar para foco no campo de comandos, exigência desta fase. Não foram alterados textos do mundo, topologia, itens, inimigos, puzzles, menu, HUD, salvamento ou áudio. Joseph permanece o protagonista.

### PLANEJADO — produção visual futura do menu (não implementada)

- Menu original: pixel art animada, opções à esquerda, Joseph completamente de costas olhando para a mansão, carro com pneu furado ao lado, chuva/tempestade, mansão em silhueta revelada por relâmpagos e título EVOLUCYS: THE ESTATE em pixel art.
- Após concluir a campanha: desbloquear atmosfera relacionada ao vírus Evolucys e mansão afetada, preservando as funcionalidades do menu.
- Remover futuramente Tutorial do menu do jogador, preservando recursos técnicos de teste.

### PENDENTE — sem implementação nesta entrega

Organização definitiva dos arquivos; renomeações sem duplicação de código e atualização de importações/referências em etapa própria; remoção de Tutorial; distribuição definitiva dos itens; puzzles completos; narrativa completa; prólogo de Joseph; queda para o subterrâneo; 30 ambientes restantes; pixel art definitiva; cutscenes; salvamento completo; finalização do jogo. As decisões de estados provisórios e conexões futuras do mapa continuam como documentadas nas fases anteriores.


### Validação 5.1F

- Testes direcionados finais: `python -B -m unittest test_phase51f test_phase44 test_phase45 test_visual_commands test_visual_ux test_inventory_window test_phase455 -q` — **87 aprovados, 0 falhas, 0 erros, 0 ignorados**, em 16,274 segundos. Incluem widgets e eventos reais de Tkinter, inspeção simples/oculta/especial, documentos, inventário, bloqueio contextual, ENTER único, foco, ESC/Voltar, redimensionamento em 1100×760 e 980×680 e uma reação por ação em confronto.
- Problemas encontrados e resolvidos: expectativa antiga de foco em Voltar; testes de exploração que precisavam fechar a nova inspeção antes de continuar; auxiliar de teclado que usava a entrada principal desabilitada. Os testes agora usam a entrada do leitor quando aberto e Voltar antes de explorar. Mantidas as verificações originais de progressão e estado.
- Encontrada e corrigida também duplicação do texto longo de ajuda na área de respostas, que ocultava o campo de comandos. Resultados de leitura/inspeção são mostrados no corpo do painel, e somente suas reações adicionais vão à área de resposta; erros continuam visíveis ali.
- Registro das tentativas: primeira rodada de 36 testes teve uma falha de expectativa de foco; uma chamada a partir da pasta errada produziu três erros de importação, corrigidos usando outputs como diretório de trabalho; duas rodadas de 46 passaram. Primeira suíte geral: 328 executados, quatro falhas nos fluxos gráficos citados. Rodada ampliada: 87 executados, uma falha no leitor de ajuda, corrigida antes da rodada final aprovada acima. Nenhum teste foi removido ou ignorado.

- Segunda suíte geral: 328 executados, uma falha remanescente no fluxo de ajuda sem dicas automáticas, que também precisava usar Voltar após examinar a mesa. Corrigido somente esse fluxo em `test_help_cleanup.py`; seus seis testes passaram em 1,404 segundos, sem ignorados. Cobertura direcionada consolidada: **93 testes aprovados** (87 + 6).

- Suíte geral final: `python -B -m unittest discover -s . -p "test_*.py" -q` — **328 aprovados, 0 falhas, 0 erros, 0 ignorados**, em 26,591 segundos. Foram necessárias três execuções gerais para resolver as incompatibilidades descritas; a base tinha 318 testes e recebeu dez novos. A suíte inclui campanha com 22 salas, protótipo com seis, progressão, bloqueios, turnos, combate, inventário, documentos e interface Tkinter.
- Conferência final por hashes: somente os 13 arquivos declarados desta fase foram criados/alterados. `world.py`, `game_state.py`, `command_language.py`, `inventory_view.py`, recursos, mapa e demais sistemas permanecem byte a byte iguais à base 5.1E.

**Fase 5.1F concluída.** Nenhuma falha pendente identificada nos testes. Não foram adicionadas salas, puzzles ou itens, nem alterados menu ou organização de pastas. A próxima fase não foi iniciada.


## Registro da Fase 5.1G — ajuda contextual, percepção e combate

### IMPLEMENTADO — Etapa A

`context_help` agora combina todos os caminhos locais conhecidos, implementados e transitáveis em uma fala de Joseph. Conserva sugestões sobre objetos, sobrevivência, comandos e escadarias; não mostra IDs internos, soluções ou passagens bloqueadas/secretas como saídas disponíveis. Consultar ajuda permanece gratuito e não modifica portas. Destinos ausentes são descartados com segurança. `ActionContext` pede esclarecimento para esquerda/direita/frente/trás sem referência; somente nomes locais explícitos permitem resolver esses pedidos. Não foi criado sistema de orientação cardinal fictício.

**Validação antes de B:** `python -B -m unittest test_phase51g test_help_cleanup test_phase455 test_inventory_stairs test_campaign_map -q`: **58 aprovados, zero erros/falhas/ignorados**, em 4,027 s. A primeira rodada teve uma expectativa antiga de destaque: a ajuda sobre DIGITAR agora também apresenta NORTE, caminho real; o teste passou a exigir ambos. Texto e comportamento de olhar em volta permanecem intactos.

### IMPLEMENTADO — Etapa B

Reutilizados `ExplorationSystems` e `ThreatMemory`, sem outra rede de percepção. Escuta e percepção passiva usam a mesma avaliação física: sinal produzido (`Enemy.sound`), intensidade, distância da criatura, portas fechadas, isolamento, bloqueio, ruído ambiente e conexões reais. Silêncio ou intensidade zero não geram presença inferida. Passagens desconhecidas, desabilitadas, inacessíveis, bloqueadas ou isoladas não transmitem sons. Sons cadastrados são narrados por seu próprio conteúdo: passos, rosnados, grunhidos, arranhões, respiração pesada, objetos sendo movimentados, impactos ou outros textos cadastrados. Não se deduz espécie/nome de um ruído.

Parâmetros provisórios em unidades abstratas: intensidade padrão 3; perda de 1 por ligação; porta fechada acrescenta 2 por padrão (`sound_attenuation`); distância médio/distante acrescenta 1/2; ruído ambiente é subtraído; limiar audível 1. Escuta ativa ganha 1; foco ganha 0,5 na escuta passiva e permite examinar até duas ligações em vez de uma, sem atravessar obstáculos nem consumir cargas. Portas `soundproof` interrompem propagação. Não há simulação acústica contínua ou áudio novo. `sound` representa o sinal atualmente produzido, não a identidade da criatura; cadastrá-lo como None representa silêncio.

Observação (`olhar pela fresta`, `espiar pela abertura`, `verificar se há movimento do outro lado`, além de examinar/observar a porta) exige passagem conhecida e habilitada, porta aberta ou `sight_gap`, iluminação e criatura com sprite visível/`in_sight`. Só comunica vulto, sem revelar descrição do cômodo remoto ou identidade. O atributo `sight_gap` da porta antiga do porão representa a fresta já descrita no protótipo; na campanha seu bloqueio continua impedindo observação. Nenhuma abertura foi criada no mapa. A inspeção usa seu painel existente e não muda suas regras modais.

Memórias registram observações, não localização absoluta: a ajuda pode lembrar de sinais e sugerir nova escuta, mas não consulta silenciosamente criaturas remotas. Mudança ou perda de sinais percebidos produz dúvida, sem garantir segurança. Rondas invisíveis e silenciosas não anunciam chegada. Sustos mantêm medo, confiança, foco e paralisação já existentes, acrescentando variação de fala sem ação automática nem turno extra.

**Validação antes de C:** `python -B -m unittest test_phase51g test_phase452 test_phase454 test_help_cleanup -q`: **75 aprovados, zero erros/falhas/ignorados**, em 4,358 s. Ajustados testes que esperavam afirmação absoluta de presença ou nenhuma lembrança após silêncio; a fixture de visão/ronda agora acende o ambiente em vez de exigir visão no escuro. O teste de aliases de observação isola a memória entre comandos para verificar primeira descoberta sem exigir repetição automática. Corrigida também a contradição entre escuta ativa de som abafado e percepção passiva na mesma ação.

### IMPLEMENTADO — Etapa C

Reutilizada `Confrontation`, com uma reação por ação. `esquivar` e aliases (`me esquivar`, `desviar`, `desviar do golpe`, `esquivar do ataque`) foram integrados ao parser e à referência de comandos; não movem Joseph entre salas. Sucesso evita o golpe; falha recebe dano integral, sem desconto defensivo. Fuga usa o mesmo método de movimento e valida saída/porta/bloqueio antes do sorteio. Somente uma ameaça viva, alerta e próxima ativa a probabilidade. Fuga bem-sucedida não recebe ataque da criatura deixada para trás; falha mantém Joseph no cômodo e resolve uma reação normal. Movimentação comum permanece sem probabilidade.

Valores **provisórios**, centralizados em `items.py`:

| Perfil/ação | Redução normal | Chance de sucesso/perfeita |
|---|---:|---:|
| Bastão de beisebol | 50% | 25% perfeita |
| Pé de cabra | 30% | 15% perfeita |
| Desarmado | 15% | 5% perfeita |
| Arma de fogo/equipamento sem perfil | 15% | 5% perfeita |
| Esquiva | Nenhuma quando falha | 30% |
| Fuga sob ameaça próxima e alerta | — | 75% |

Armas de fogo não são usadas para aparar: aplica-se o perfil corporal, sem gastar munição. Bastão é somente um perfil preparado e uma fixture isolada, não item adicionado ao mundo. Dano parcial é arredondado para cima; dano 16 resulta em 8 com bastão, 12 com pé de cabra e 14 desarmado. Bloqueio perfeito causa zero. Nenhum ataque especial foi criado: não existe caso real definido que justifique infraestrutura adicional.

Medo multiplica chances por `1 - 0,20 × medo/100`, com limites de 0 a 100 tanto no medo considerado quanto no resultado percentual. No medo máximo, chances-base conservam 80% do valor (esquiva 24%, fuga 60%); nunca vira falha automática. Outros efeitos de medo, confiança e foco não foram alterados. `Confrontation` aceita fonte aleatória injetável; testes controlam `roll` para verificar sucesso/falha, limites e aplicação única.

Defesa/esquiva são mutuamente exclusivas. Postura vale para o primeiro ataque elegível, até **três reações físicas contando a ação de preparação**, cobrindo alerta → preparação → golpe. Esperar mantém a postura dentro desse limite; consultas gratuitas não a desgastam. Outras ações físicas cancelam a postura. Repetir a preparação substitui o prazo e nunca acumula redução/probabilidade; após golpe, expiração, ausência de ameaça ou morte, a postura é limpa. Falas variam por resultado real e não afirmam bloqueio/esquiva quando houve dano integral.

**Validação C:** inicialmente **128 aprovados**, sem ignorados, com `python -B -m unittest test_phase51g test_confrontation test_survival test_visual_session test_phase451 -q` (2,197 s na rodada após os últimos ajustes de fixtures). Um teste novo revelou destino ausente não tratado pelo resolvedor de passagens, agora ignorado sem teletransporte. Fixtures antigas marcavam porta aberta mas ainda trancada; as rotas de sucesso foram preparadas abertas/destrancadas, e a nova cobertura exige bloqueio mesmo no estado inconsistente. Expectativas antigas de defesa fixa em 50% foram atualizadas para 15% desarmado, preservando as verificações de dano, foco e duração. Fuga/defesa antigas agora têm sorteio explícito nos testes.

**Reteste ampliado após revisão:** `python -B -m unittest test_phase51g test_confrontation test_survival test_visual_session test_phase451 test_phase455 -q` — **150 aprovados, 0 falhas, 0 erros, 0 ignorados**, em 2,998 s. Acrescentados casos para influência efetiva do medo sobre os resultados e ausência de revelação de porta secreta durante fuga. Os testes gráficos usam ENTER real, verificam execução única, foco, falas e fuga na interface existente.

### Arquivos e preservação

Produção: `context_help.py`, `action_context.py`, `command_language.py`, `command_parser.py`, `exploration_systems.py`, `confrontation.py`, `items.py` e `world.py` (metadados sensoriais e respeito à visibilidade na descrição de criaturas, sem alteração de salas/conexões/conteúdo). Teste novo: `test_phase51g.py`. Testes ajustados: `test_phase455.py`, `test_phase452.py`, `test_phase454.py`, `test_confrontation.py`, `test_survival.py` e `test_visual_session.py`. Documentos: `CAMPAIGN_PROGRESS.md` e `WORLD_DESIGN.md`.

GameState, Survival, ThreatMemory, CombatContext e os componentes de interface/inventário/documentos foram reutilizados sem modificar seus arquivos. Nenhum recurso gráfico ou sonoro foi alterado. Joseph permanece o protagonista.

### PLANEJADO / PENDENTE — não implementado

Balanceamento definitivo dos percentuais e calibração autoral de intensidade/isolamento/visibilidade; eventuais ataques especiais apenas quando houver definição real. Permanecem as 30 salas restantes, puzzles, itens/criaturas futuros, organização/renomeação de arquivos, remoção de Tutorial, distribuição definitiva de itens, narrativa completa, prólogo/queda, cutscenes, pixel art definitiva, cenários dinâmicos, menu principal/alternativo e salvamento completo. Nenhuma dessas produções foi iniciada.


### Revisão final de percepção e validação geral

A revisão de mensagens ampliou a cobertura da ronda silenciosa para chegada, busca, espera e saída. Falas que pressupunham presença conhecida foram condicionadas a sinais perceptíveis. A descrição geral e a reação do confronto também deixam de identificar uma criatura ou antecipar seu golpe no escuro/fora da linha de visão; um ataque efetivo continua causando seu dano e é narrado como algo fora de vista. Não foram alterados o ciclo de ataque, textos autorais das salas ou suas listagens. Este ajuste é necessário para manter o princípio sensorial também nas saídas narrativas existentes.

Histórico real das execuções gerais:
- Primeira suíte: **359 executados, uma falha**, em 27,382 s, num teste antigo que exigia ajuda atualizada automaticamente a partir do estado remoto da criatura. Corrigida a expectativa para memória incerta; o reteste com `test_phase51g test_phase455` teve **51 aprovados**.
- Segunda suíte (com mais dois casos de probabilidade/segredo): **361 aprovados, zero falhas/erros/ignorados**, em 28,756 s.
- Revisão final: **39 direcionados aprovados** em 2,346 s para o ciclo da ronda; depois **121 aprovados**, zero falhas/erros/ignorados, em 3,189 s com `test_phase51g test_phase452 test_phase454 test_confrontation test_survival`, incluindo o novo caso de criatura silenciosa no escuro e ataque efetivo sem revelação de identidade.

- **Suíte geral final:** `python -B -m unittest discover -s . -p "test_*.py" -q` — **362 aprovados, 0 falhas, 0 erros, 0 ignorados**, em **27,807 s**. Base anterior: 328; acréscimo: **34 testes**. Todos os testes gráficos foram executados com Tkinter disponível. Nenhuma limitação gráfica impediu a validação e nenhum teste foi ignorado para obter aprovação.
- Conferência por hashes: exatamente os **17 arquivos declarados** foram criados/modificados. Arquivos de UI/HUD, inventário, documentos, recursos gráficos/áudio, GameState e demais arquivos fora do escopo permaneceram iguais à base 5.1F. Testes do mapa/protótipo passaram na suíte geral: **22 salas da campanha e seis do protótipo**, bloqueios e progressão preservados.

**Fase 5.1G concluída e validada.** Nenhuma falha pendente identificada. Percentuais e parâmetros sensoriais continuam provisórios. Nenhuma próxima fase foi iniciada.


## Registro da Fase 5.1H — exterior da propriedade

**IMPLEMENTADO:** E01 — Estrada / Carro; E02 — Portão da Propriedade; E03 — Caminho Frontal; E04 — Varanda da Mansão; E05 — Lateral da Casa; E06 — Fundos da Propriedade; E07 — Casinha de Ferramentas; E08 — Estufa Abandonada; E09 — Área do Gerador Externo. Descrições ambientais provisórias, sem objetos coletáveis, inimigos, documentos, pistas, puzzles ou acontecimentos especiais.

Oito ligações internas bidirecionais: E01/E02, E02/E03, E03/E04, E03/E05, E03/E08, E05/E06, E06/E07, E06/E09. Disponíveis provisoriamente; portão aberto, sem chave. Nomes locais permitem os exemplos naturais “ir até o portão”, “seguir pela estrada”, “ir para a lateral da mansão”, “ir aos fundos”, “seguir até a casinha de ferramentas” e “entrar na estufa”, usando o parser inalterado. “Seguir pelo caminho” pede esclarecimento quando há mais de um caminho, sem escolher arbitrariamente.

E04/T01 reutiliza a porta principal e adiciona estado compartilhado desabilitado; E06/T07 recebe a porta de passagem da lavanderia, bloqueada e com estado compartilhado desabilitado. **Limitação técnica:** não existe travamento por lado na representação atual. Conforme autorizado, a porta principal fica inacessível nos dois sentidos até a definição do comportamento interno, sem improvisar desbloqueio. Detalhes e dependências na seção 18 de WORLD_DESIGN.md.

**Preservado:** 31 salas únicas, 34 ligações/68 arcos, nenhum destino ausente. Início em entrance/T01, sem acesso livre ao exterior a partir dele. Protótipo com exatamente seis salas, mesmos itens, inimigos, puzzles e progressão. Bloqueios anteriores mantidos. E07 não provoca queda, dano, ganho de itens ou cutscene; B01 continua ausente. E03 continua apenas previsão documental de save e sinal, sem ativação. Nenhuma mudança no Tutorial, menu, HUD, interface, áudio/arte, inspeção, inventário, parser ou sistemas da 5.1G.

**Arquivos modificados:** `world.py`, `test_campaign_map.py`, `test_map_infrastructure.py`, `test_phase51g.py`, `WORLD_DESIGN.md`, `CAMPAIGN_PROGRESS.md`. Nenhum arquivo novo em outputs. Somente a configuração de campanha da fábrica foi expandida. Testes do mapa atualizados para IDs/grafo completos; duas expectativas de contagem em testes anteriores passaram de 22 para 31, preservando as demais verificações. Acrescentados cinco testes para rotas naturais bidirecionais, ausência de conteúdo/queda, fronteiras bloqueadas nos dois lados, reutilização da porta/protótipo e integração da ajuda/inspeção/percepção. A renderização já existente agora percorre as 31 salas em 1100×760.

### Validação

- Direcionados: `python -B -m unittest test_campaign_map test_map_infrastructure test_phase51g test_phase51f -q` — **78 aprovados, 0 falhas, 0 erros, 0 ignorados**, em **4,298 s**. Incluem testes gráficos reais com Tkinter, as oito novas rotas e os bloqueios antigos/novos. Nenhuma correção de falha foi necessária nessa execução.

### PLANEJADO / PENDENTE

Comportamento interno da porta principal e eventual restrição por lado; liberação futura do atalho da lavanderia; validação definitiva das passagens provisórias; E07 → B01 e porão inicial; salvamento previsto em E03; prólogo/queda e introdução cinematográfica. Permanecem 21 ambientes oficiais, distribuição definitiva de itens, puzzles, narrativa completa, inimigos futuros, cutscenes, arte/áudio definitivos, organização de arquivos, remoção de Tutorial e menus futuros. Nada disso foi iniciado nesta entrega.


### Resultado final 5.1H

- Suíte geral executada **uma vez**: `python -B -m unittest discover -s . -p "test_*.py" -q` — **367 aprovados, 0 falhas, 0 erros, 0 ignorados**, em **31,414 s**. Base 5.1G: 362; cinco testes novos. Inclui validações gráficas com Tkinter e regressões de inspeção, percepção, combate, inventário e progressão do protótipo.
- Conferência por hashes: apenas os seis arquivos declarados foram alterados. Não há falhas pendentes identificadas. A restrição por lado da porta principal continua pendência explícita, tratada pelo bloqueio seguro em ambos os sentidos.

**Fase 5.1H concluída: 31 ambientes na campanha, seis no protótipo, início preservado em T01. Prólogo não implementado. Fase 5.2 não iniciada.** Nenhuma próxima etapa foi iniciada automaticamente.


## Revisão canônica da Fase 5.1H — entrega vigente

A definição mais recente e o esboço externo substituem a malha anterior e a queda da casinha. Detalhes e decisões na seção 19 de WORLD_DESIGN.md.

**Implementado:** E01–E09 adaptados; E10–E13 novos; B01–B03 construídos com IDs já planejados. Campanha: 38 salas únicas, 42 conexões bidirecionais e uma queda (85 arcos). Catálogo: 56 IDs; 18 ambientes ainda pendentes. Joseph começa junto ao carro, atravessa o portão aberto e encontra a porta da mansão fechada. Campainha com espera de 800 ms e resposta sem reação/turno adicional. Macaco incompleto em E07; tentativa de pegar manivela em E08 leva a B01, sem recebê-la. B01/B02/B03/T12 permite prosseguir no interior. Poço E13/B02 requer luz normal equipada/acesa e abertura por dentro; não há desbloqueio por nome ou item externo.

**Preservado:** protótipo de seis salas e sua progressão, bloqueios antigos, inventário, combate, inspeção, layout/HUD e arte/áudio. Pequenas integrações na linguagem, ajuda e apresentação da campainha, sem sistema de mundo paralelo. Testes antigos do interior usam T01 explicitamente quando dependem daquele cenário; o início de campanha real passa a E01.

**Pendências:** recuperação posterior da manivela e conserto do carro; desbloqueio definitivo das fronteiras da mansão; save/load completo dos eventos; 18 salas planejadas; garagem/fuga e susto animal apenas potenciais documentais. Organização de arquivos, renomeação sem duplicação, retirada do Tutorial, distribuição final de itens, puzzles, narrativa e prólogo cinematográfico continuam pendentes. Nenhuma próxima fase iniciada.

### Validação desta revisão

- Primeira execução direcionada: 170 testes, três falhas em expectativas/aliases de caminhos externos. Corrigidos nome do retorno ao portão e expectativa da direção sul, preservando esclarecimento quando o caminho é ambíguo.
- Direcionados ampliados: `python -B -m unittest test_canonical_opening test_campaign_map test_map_infrastructure test_phase51g test_phase51f test_game test_inventory_stairs test_visual_session test_inventory_window test_phase452 test_help_cleanup test_phase455 -q`: **196 aprovados**, zero falhas/erros/ignorados, em 13,760 s. Tkinter disponível; renderização dos 38 ambientes em 1100×760, espera/foco da campainha e integração da inspeção/queda incluídas.

- Suíte geral final executada **uma vez**: `python -B -m unittest discover -s . -p "test_*.py" -q` — **379 aprovados, zero falhas, erros ou ignorados**, em **28,253 s**. Inclui o alias completo “barra de aço do macaco”, acrescentado após os direcionados. Base: 367 testes; 12 novos casos (com subcenários). Nenhuma regressão identificada.
- Conferência documental: 66 conexões planejadas únicas; execução validada com 85 arcos e sem destinos ausentes. Conferência por SHA-256: somente os 19 arquivos abaixo diferem da base; nenhum removido. Arte, áudio e demais arquivos permaneceram iguais. Bytecode temporário gerado pela verificação de sintaxe foi removido.

### Arquivos desta revisão

- Mundo/ações: `world.py`, `game_state.py`, `command_parser.py`, `command_language.py`, `action_context.py`, `context_help.py`.
- Resposta temporizada da campainha: `visual.py`, `visual_session.py`, `main.py` (sem alteração de layout).
- Novo teste: `test_canonical_opening.py`.
- Testes adaptados ao novo início/mapa: `test_campaign_map.py`, `test_map_infrastructure.py`, `test_phase51g.py`, `test_game.py`, `test_inventory_window.py`, `test_phase452.py`, `test_visual_session.py`.
- Documentação: `WORLD_DESIGN.md`, `CAMPAIGN_PROGRESS.md`.

**Fase 5.1H concluída neste escopo. Nenhuma fase seguinte iniciada.**


## Fase 5.1I — conclusão estrutural do porão principal

**Implementação:** B04, B05, B06, B08, B09 e B10 adicionados; B07/cellar reaproveitado sem duplicação ou remoção do conteúdo legado. B01–B03 mantidos. Contagem real: **44 salas únicas** (38 + 6); o pedido de 45 conflita com a reutilização obrigatória de B07. Não foi inventado outro ambiente.

**Conexões:** sete comuns bidirecionais B03/B04, B03/B05, B03/B09, B05/B06, B06/B07, B07/B08, B09/B10. Atalhos B04/B09 e B08/B10 começam bloqueados com portas e estados compartilhados, sem mecanismo de desbloqueio. Total em execução: 51 ligações bidirecionais + queda unidirecional, **103 arcos**. A definição atual explicita o bloqueio de B04/B09, antes indefinido no documento original.

**Preservado:** começo E01, protótipo de seis salas, queda/manivela, rota inicial até T12, poço condicionado e escadaria B07/T02 bloqueada. Parser e GameState não alterados. Nenhum sistema, interface, recurso ou conteúdo fora do escopo modificado. B10/L01 continua só no planejamento; laboratório não criado.

**Arquivos:** `world.py`; novo `test_basement_map.py`; expectativas de mapa/contagem em `test_campaign_map.py`, `test_map_infrastructure.py`, `test_phase51g.py`, `test_canonical_opening.py`; `WORLD_DESIGN.md` e `CAMPAIGN_PROGRESS.md`.

**Validação:** execução direcionada com `test_basement_map test_campaign_map test_canonical_opening test_map_infrastructure test_phase51g`: 80 testes existentes passaram, mas o novo módulo não carregou por erro de caminho ao gravá-lo (81 entradas, um erro de importação; 4,500 s). Corrigido apenas o caminho; executado somente `test_basement_map`: **4 aprovados**, 0,020 s. Cobertura: identidade de B07, conteúdo/protótipo, nomes de navegação nos dois sentidos, bloqueios contra comandos alternativos, destinos não adjacentes e laboratório inacessível. Testes existentes validam queda, poço, rota inicial, grafo exato e renderização dos 44 ambientes em 1100×760.

Suíte geral final justificada pela ampliação do grafo compartilhado com exploração, ajuda e circulação do inimigo legado de B07; executada uma única vez nesta fase.

**Pendências:** 12 salas do complexo e condição futura B10/L01; condições definitivas de desbloqueio dos atalhos. Demais pendências anteriores permanecem sem implementação. Fase 5.1J não iniciada.


**Resultado final 5.1I:** `python -B -m unittest discover -s . -p "test_*.py" -q` executado uma vez: **383 aprovados, zero falhas, erros ou ignorados**, em **28,530 s**. Base 379; quatro testes novos com subcenários. Nenhuma regressão identificada. Tkinter disponível, sem testes gráficos ignorados. Conferência SHA-256: exatamente os oito arquivos declarados alterados/criados, nenhum removido; demais arquivos iguais à base 5.1H.

**Fase 5.1I concluída. Fase 5.1J não iniciada. Nenhuma mecânica fora do escopo alterada.**


## Fase 5.1J — relatório consolidado das etapas A e B

**IMPLEMENTADO:** L01–L12, com os nomes atualizados do pedido e descrições ambientais. Treze ligações internas bidirecionais e B10/L01 estrutural com porta/estado compartilhados, inicialmente oculta, trancada e bloqueada. Sem solução de abertura. L12 sem fuga/vitória; L03/L11 com save apenas previsto. Total real **56 salas únicas**, seis no protótipo; início E01. Nenhum novo item, inimigo, puzzle ou alteração de sistema/interface.

**VALIDADO:** grafo completo de 66 ligações/131 arcos; destinos existentes, ausência de duplicações, conectividade estrutural de todos os setores e compartilhamento de portas/estados. Alcance inicial da caminhada restrito aos 13 ambientes externos; laboratório internamente conectado mas inacessível do porão. Queda/poço, escadarias, atalhos antigos, prólogo e protótipo preservados. A liberação hipotética do laboratório só acontece em fixture de teste. Renderização já existente percorre os 56 ambientes.

**Correções/limitações:** o alias “sala de contenção” precisou de ajuste na pontuação do nome da passagem; parser não alterado. Duas expectativas antigas tratavam destinos do laboratório como inexistentes e foram atualizadas para destinos realmente ausentes. “Sair pelo corredor” é limitação anterior do parser; não movimenta, enquanto “ir para o corredor do laboratório” funciona. Nenhuma inconsistência de topologia/bloqueio exigiu alteração dos sistemas.

**Testes executados, na ordem solicitada:**
1. `python -B -m unittest test_laboratory_map.LaboratoryTests -q`: 4 testes, uma falha no alias de contenção, em 0,037 s; corrigido no nome da passagem.
2. `python -B -m unittest test_laboratory_map.WorldAccessAuditTests test_campaign_map test_canonical_opening test_basement_map test_map_infrastructure test_phase51g -q`: 86 testes, duas falhas nas expectativas antigas de destinos ausentes, em 5,556 s; corrigidas somente as fixtures/expectativas afetadas.
3. Reexecutados somente os três testes afetados: `test_laboratory_map.LaboratoryTests.test_local_language_and_no_remote_movement`, `test_campaign_map.CampaignMapTests.test_unimplemented_destinations_do_not_appear_or_move_player`, `test_phase51g.HelpPathsTests.test_secret_and_missing_destinations_do_not_leak_or_mutate`: **3 aprovados**, em 0,033 s.

**Arquivos:** `world.py`; novo `test_laboratory_map.py`; ajustes em `test_campaign_map.py`, `test_basement_map.py`, `test_canonical_opening.py`, `test_map_infrastructure.py`, `test_phase51g.py`; `WORLD_DESIGN.md` e `CAMPAIGN_PROGRESS.md`.

**PENDENTE:** solução de acesso B10/L01 e demais atalhos, salvamento, conteúdo científico/narrativo, puzzles, distribuição definitiva, destino de L12 e conclusão da campanha. Nenhuma fase seguinte foi iniciada.


4. **Suíte geral final, uma única execução após as alterações:** `python -B -m unittest discover -s . -p "test_*.py" -q` — **389 aprovados, zero falhas, erros ou ignorados**, em **30,826 s**. Base 383; seis testes parametrizados novos. Tkinter disponível, incluindo renderização dos 56 ambientes em 1100×760; nenhuma limitação de dependência impediu os testes gráficos.
5. Conferência SHA-256: somente os nove arquivos declarados foram alterados/criados; nenhum removido. Parser, GameState, UI/HUD, arte/áudio e demais arquivos iguais à base 5.1I. Nenhuma regressão pendente identificada.

**Fase 5.1J concluída, etapas A e B executadas. Fase 5.2 não iniciada.**


## Fase 5.2 — prólogo e narrativa inicial

**Implementado:** textos de E01–E03, estufa E08 e chegada B01 refinados; demais exteriores mantidos onde já atendiam à identidade ambiental pedida. Pneu/roda, mansão/fachada e estufa recebem alvos ambientais de inspeção. Macaco existente continua incompleto; função provável da manivela só é reconhecida após examinar o macaco, usando o estado `investigated`. Ajuda local acompanha campainha, inspeções e queda sem soluções futuras.

Campainha distingue primeira chamada e repetições pelo evento existente; mantém espera de 800 ms, sem liberar porta. Queda única mantém gatilho de coleta, destino B01 e ausência da manivela no inventário; reação física e fala de Joseph aparecem na transição, sem repetição nas revisitas. Aliases `coletar/alcançar` limitados ao objeto do evento e `caminhar até o portão` limitado à passagem local. Detalhes na seção 22 de WORLD_DESIGN.md.

**Preservado:** mapa de 56 salas/131 arcos, protótipo de seis salas, inventário, turnos, saúde, combate, poço condicionado, campainha temporizada, interface e demais sistemas. Nenhuma ordem obrigatória nova de exploração. Sem novos coletáveis, puzzles, inimigos ou mudanças no laboratório.

**Validação:** tentativa inicial de invocar os testes no diretório raiz falhou na importação dos cinco módulos, sem executar testes de jogo; corrigido o diretório para outputs. Execução direcionada `python -B -m unittest test_canonical_opening test_campaign_map test_laboratory_map test_help_cleanup test_phase51f -q`: **61 aprovados, zero falhas/erros/ignorados**, em **9,225 s**. Quatro casos novos em test_canonical_opening cobrem introdução/inspeções, repetição da campainha, conhecimento/ajuda e aliases da queda; testes anteriores cobrem poço, inventário cheio, integração visual, topologia e protótipo. Após essa execução, as duas respostas de uso do macaco receberam identificação explícita Joseph; incluídas na suíte geral final.

**Arquivos:** `world.py`, `command_parser.py`, `command_language.py`, `context_help.py`, `test_canonical_opening.py`, `WORLD_DESIGN.md`, `CAMPAIGN_PROGRESS.md`. GameState e narrative consultados/reutilizados sem alteração; nenhum arquivo novo de produção ou teste.

**Pendências:** conserto do carro, recuperação da manivela, desenvolvimento narrativo posterior, puzzles e salvamento. Fase 5.3 não iniciada.


**Resultado final:** suíte geral executada uma vez: `python -B -m unittest discover -s . -p "test_*.py" -q` — **393 aprovados, zero falhas, erros ou ignorados**, em **31,125 s**. Inclui testes gráficos com Tkinter disponível. Base 389; quatro casos novos. Conferência SHA-256: somente os sete arquivos declarados alterados; nenhum removido ou criado em outputs. Nenhuma regressão identificada.

**Fase 5.2 concluída neste escopo. Fase 5.3 não iniciada.**


## Correção pontual — lanterna inicial e poço (referência Fase 5.3)

A campanha começa em E01 com a lanterna funcional no inventário, ocupando um dos seis espaços. A mesma instância antes disponível em T01 é transferida na inicialização; não existe outra lanterna para coletar na mansão. Começa guardada e apagada; os comandos existentes de equipar e ligar fornecem a iluminação adequada. Protótipo preserva sua lanterna original na sala; cenários do Tutorial não herdam o equipamento da campanha.

Poço E13/B02 sem alteração de mecânica: luz normal, acesa e equipada revela escada e acesso; a passagem começa trancada e só é destrancada em B02. Usar itens ou tentar abrir/forçar do exterior não libera o acesso. Depois da abertura interna, a descida continua exigindo iluminação. A referência anterior à obtenção posterior da lanterna em T01 está substituída por esta correção.

Escopo limitado à correção expressa do usuário. Distribuição de equipamentos, documentos, inimigos e demais progressões do anexo amplo da Fase 5.3 não foram implementadas nesta correção.


Validação da correção: `test_canonical_opening test_campaign_map test_visual_session test_inventory_window test_phase452` — **105 aprovados**, em 12,770 s. Suíte geral executada uma vez: `python -B -m unittest discover -s . -p "test_*.py" -q` — **395 aprovados, zero falhas, erros ou ignorados**, em 31,790 s. Dois testes novos verificam equipamento inicial único/funcional, ausência em T01, protótipo, iluminação real e desbloqueio exclusivo em B02 com tentativas externas usando itens.

Arquivos alterados: `game_state.py`, `tutorial.py` (isolamento dos cenários), `test_campaign_map.py` (localização da lanterna), `test_canonical_opening.py`, `WORLD_DESIGN.md`, `CAMPAIGN_PROGRESS.md`. Parser e mecanismo do poço permaneceram inalterados. Nenhuma outra mecânica da Fase 5.3 foi modificada.


## Fase 5.3A — garagem e correções estruturais

**IMPLEMENTADO:** G01 Garagem, oeste de T03, retorno a leste por porta compartilhada inicialmente aberta. 57 salas únicas, 67 ligações/133 arcos. Dois carros antigos, compartimento do primeiro carro, bancada/armários, ferramentas/peças e conjunto de dois portões externos inspecionáveis. Portões trancados/bloqueados por contenção, sem destino externo; nenhum veículo, roda coletável ou fuga funcional. Parser e demais sistemas preservados.

**VALIDADO:** 34 testes direcionados aprovados, zero falhas/erros/ignorados, em 5,169 s: `python -B -m unittest test_campaign_map test_laboratory_map test_canonical_opening.InitialFlashlightTests -q`. Três casos parametrizados novos em test_campaign_map cobrem porta nos dois sentidos/direções/nomes, inspeção sem coleta/spoilers e ausência de saída por portões/sinônimos, inclusive objeto hipoteticamente aberto em fixture. Testes existentes validam grafo completo, bloqueios, lanterna, poço e renderização dos 57 ambientes. Não há restauração elétrica implementada para simular legitimamente: portões não possuem dependência de energia e a proibição de liberação automática foi registrada para futura integração.

**Arquivos:** `world.py`, `test_campaign_map.py`; expectativas de contagem em `test_map_infrastructure.py`, `test_phase51g.py`, `test_canonical_opening.py`, `test_basement_map.py`, `test_laboratory_map.py`; `WORLD_DESIGN.md`, `CAMPAIGN_PROGRESS.md`. Sem arquivo novo.

**PENDENTE:** roda compatível no compartimento do carro antigo 1, obtenção após progressão final, destino externo da garagem, evento narrativo de liberação, recuperação da manivela e conserto. Planejamento dos dois finais preservado na seção 23 de WORLD_DESIGN.md: retorno para obter roda no Sobrevivente; interceptação por Daniel na tentativa de fuga em A Última Vítima. Nenhum desses eventos implementado. Fase 5.4 ou qualquer etapa posterior não iniciada.


**Resultado final:** suíte geral executada uma única vez: `python -B -m unittest discover -s . -p "test_*.py" -q` — **398 aprovados, zero falhas, erros ou ignorados**, em **31,716 s**. Base 395, três casos novos. Tkinter disponível; testes gráficos executados. Nenhuma regressão identificada; limitação de integração com energia futura registrada acima.

**Fase 5.3A concluída. Nenhuma etapa posterior iniciada.**


## Correção oficial Fase 5.3 — gerador principal e contenção do poço

Gerador principal e quadro elétrico em **B06**, acessível pelo percurso interno T12 → B03 → B05 → B06. Fusíveis únicos coletáveis em **U07**, respeitando os seis espaços (inventário cheio preserva o item no depósito). E09 permanece equipamento auxiliar abandonado, sem função na progressão elétrica. Nenhuma sala ou conexão nova; 57 ambientes e 133 arcos preservados.

Sequência jogável: examinar quadro elétrico em B06; coletar fusíveis em U07; retornar e `instalar fusíveis` (também `usar fusíveis no quadro elétrico`); `ligar gerador`/`usar gerador principal`/`restaurar energia`. Instalação consome os fusíveis do inventário uma única vez e registra `fuses_installed`; acionamento registra `power_restored`. Aliases de instalação/acionamento limitados a B06. Registros usam `world_events` existente, sem subsistema novo. Energia não desativa contenção nem altera portas indiscriminadamente.

Poço: `abrir acesso do poço` em B02 exige agora `containment_disabled`. Estado inicial mantém contenção ativa (evento ausente), inclusive após restauração elétrica. Somente depois desse evento a abertura interna habilita a passagem compartilhada. Exterior continua incapaz de destrancar, mesmo após a contenção desativada. Iluminação normal equipada/acesa e demais regras anteriores preservadas; lanterna inicial mantida.

**Limitação real da base:** antes desta correção não existiam implementação de energia nem evento jogável de desativação da contenção. A sequência elétrica mínima foi acrescentada com os estados existentes. A lista de acessos internos a liberar e a ação narrativa que desativa contenção não foram definidas: permanecem pendentes, sem liberação inventada. Portanto o poço não pode ser desbloqueado numa sessão normal até essa integração futura. Testes simulam `containment_disabled` exclusivamente em instâncias isoladas. Portões de G01 e saídas externas permanecem bloqueados. Esta seção substitui a liberação incondicional anterior por B02 e a antiga indicação do gerador principal em E09.


Arquivos alterados: `world.py`, `command_parser.py`, `command_language.py`, `test_basement_map.py`, `test_canonical_opening.py`, `test_campaign_map.py`, `WORLD_DESIGN.md`, `CAMPAIGN_PROGRESS.md`. Expectativas antigas de salas vazias e abertura incondicional do poço ajustadas; protótipo e mecanismos fora do escopo preservados.

Testes direcionados: `python -B -m unittest test_basement_map test_canonical_opening test_campaign_map test_laboratory_map -q` — **57 aprovados**, zero falhas/erros/ignorados, em **6,506 s**. Três casos novos verificam sequência elétrica, isolamento dos bloqueios, contenção versus energia, abertura exclusivamente interna, luz, rota interna de acesso e inventário cheio.


Suíte geral final executada **uma vez**: `python -B -m unittest discover -s . -p "test_*.py" -q` — **401 aprovados, zero falhas, erros ou ignorados**, em **31,551 s**. Nenhuma regressão identificada. Bloqueios internos dependentes de energia e evento de desativação da contenção continuam pendências explícitas, não apresentados como funcionais. Nenhuma fase posterior iniciada.


## Continuação Fase 5.3 — itens e progressão essencial

### IMPLEMENTADO

| Item/conteúdo | Local | Obtenção e função |
|---|---|---|
| Pé de cabra único | B09 | Coleta normal; ferramenta reutilizável e arma improvisada já suportada (25 de dano nominal) |
| Porta de manutenção | B03/T12 | Inicialmente emperrada e bloqueada dos dois lados; `usar pé de cabra na porta de manutenção` habilita e abre permanentemente o estado compartilhado; ferramenta não consumida |
| Pistola existente | T08, armário de segurança | Transferida do cofre, sem duplicação; abrir armário destrancado, coletar/equipar; dois cartuchos iniciais |
| Espingarda | U06, armário de armas | Representada atrás do vidro e inspecionável pela descrição do armário; bloqueada, sem coleta ou solução de abertura. Estado de arma existente, sem munição inicial |
| Bandagens (uma por local) | T11, T12, B04, G01 | Primeiros socorros/manutenção/emergência automotiva; opcionais |
| Spray de cura | U05 | Uma unidade opcional |
| Kit médico (um por local) | B09, L07 | Oficina/enfermaria; opcionais |
| Munição de pistola | U07 | Dois cartuchos adicionais; preservada a caixa anterior de três em T08 |
| Fusíveis | U07 | Sem mudança: instalação em B06 e acionamento do gerador principal |

Recursos legados permanecem; não foram duplicados pistola, ferramentas essenciais ou eventos. Inventário de seis espaços preservado; itens permanecem no cenário quando a coleta falha. Conteúdo do protótipo inalterado. Os novos itens usam GameObject/WeaponState e capacidades existentes; sem crafting ou novo sistema de combate.

Doze registros curtos, usando leitura existente: T08 (circular administrativa, reaproveita documento), T09 (regeneração/longevidade), U06 (divergência Daniel/Adrian), U07 (transferência de fusíveis), B07 (incidentes com funcionários, reaproveita o objeto legado da pasta), L03 (equipe/procedimentos), L04 (comportamento), L05 (EV-7), L06 (espécies), L07 (consequências clínicas), L08 (falhas de contenção), L11 (evidência decisiva da agressão de Adrian e transformação de Daniel). Documentos não abrem portas nem são exigidos para progressão; revelações finais restritas a L11. O identificador legado da pasta em B07 permanece por compatibilidade, com texto substituído pelo registro de funcionários.

Referência consultada: `C:/Users/jedia/Downloads/Evolucys_The_Estate.pdf`, 37 páginas, romance com dois finais; o nome exato solicitado “Evolucys_The_Estate_História.pdf” não foi encontrado. O conteúdo localizado corresponde aos marcos fornecidos. Textos novos são paráfrases breves, sem reprodução do livro. A correção oficial de fusíveis em U07 e gerador B06 prevalece sobre a localização mais genérica no romance.

Progressão validada: B01/B02/B03 → B09 (pé de cabra) → B03/T12 (forçar) → T02/U01 → U02/U06/U07 (fusíveis) → retorno a B06 → energia. Sem visita externa obrigatória. Pé de cabra não libera portas eletrônicas, armário de armas, laboratório ou outros bloqueios. Restauração elétrica mantém saídas, garagem, laboratório e contenção bloqueados; poço continua exigindo desativação futura da contenção e abertura exclusivamente por B02.

### PLANEJADO / PENDENTE

**Empregada transformada em T02**, com uniforme de serviço e chave única destinada à escadaria T02/U01: registrada, ainda não inserida como encontro jogável. Não existe suporte atual a recuperação de itens de inimigos; aplicada a alternativa expressamente autorizada, sem inventar sistema de loot/IA. Porta já possui `lock_id=campaign.upper_stairs` e referência à futura `chave da empregada`, mas continua aberta e destrancada. Não existe chave coletável ou bloqueio ativo atrás de si mesmo. Implementar presença perceptível e recuperação legítima antes de ativar esse bloqueio.

Solução do armário da espingarda, evento de desativação de contenção, acessos internos dependentes de energia e liberação do laboratório permanecem pendentes. Roda em G01, recuperação da manivela, conserto e finais continuam somente planejados. Não implementados chefes, perseguições, garagem dirigível ou fuga. Nenhuma sala/conexão nova; 57 ambientes e 133 arcos. Fase 5.4 não iniciada.


Validação direcionada: `python -B -m unittest test_basement_map test_campaign_map test_canonical_opening test_laboratory_map test_inventory_window test_visual_session -q` — **86 aprovados**, zero falhas/erros/ignorados, em **10,338 s**. Três testes novos parametrizados validam percurso real até energia, armas/ferramenta única, coleta com inventário cheio e documentos fragmentados. Expectativas anteriores de salas vazias e escada de manutenção livre foram atualizadas para a progressão autorizada. Após os direcionados, acrescentada somente a referência inativa da chave da escadaria; coberta na suíte final.

Arquivos alterados: `world.py`, `command_parser.py`, `test_basement_map.py`, `test_campaign_map.py`, `test_canonical_opening.py`, `test_laboratory_map.py`, `WORLD_DESIGN.md`, `CAMPAIGN_PROGRESS.md`. Sem módulos novos, sem alteração do protótipo ou UI. Evidência extraída do PDF somente em work/story_reference.txt para consulta.


Suíte geral final executada **uma vez**: `python -B -m unittest discover -s . -p "test_*.py" -q` — **404 aprovados, zero falhas, erros ou ignorados**, em **32,131 s**. Base 401, três testes novos. Testes gráficos executados com Tkinter disponível. Nenhuma regressão identificada. Continuação encerrada com a alternativa autorizada para empregada/chave e demais pendências descritas, sem iniciar Fase 5.4.


## Fase 5.3B — fachada externa da garagem

**IMPLEMENTADO:** E14 Frente da Garagem; caminho E03/oeste ↔ E14/leste; conexão E14/G01 com o mesmo objeto dos portões de G01 e estado compartilhado desabilitado. Duas novas ligações, nenhum arco anterior removido. Total 58 salas, 137 arcos. Porta interna T03/G01 preservada aberta. Inspeção de fachada e portões sem spoilers; nenhuma arma/item/inimigo/puzzle novo. Exceção pontual autorizada: `examinar a garagem` em E03 aproxima até E14; em E14 permanece inspeção. Parser não refatorado.

**VALIDADO:** `python -B -m unittest test_campaign_map test_laboratory_map test_basement_map.PowerAndContainmentTests -q` — **37 aprovados, zero falhas/erros/ignorados**, em **5,368 s**. Dois casos novos parametrizados cobrem percurso completo E01/E02/E03/E14, aliases/retorno, inspeção, identidade de objeto/estado, bloqueios nos dois sentidos e energia realmente restaurada via fusíveis. Reutilizados grafo exato, compartilhamento global, renderização dos 58 ambientes e regressão da garagem interna. Nenhuma correção de falha necessária.

**Arquivos alterados:** `world.py`, `command_language.py`; novos casos e expectativas de mapa em `test_campaign_map.py`; contagens atualizadas em `test_laboratory_map.py`, `test_basement_map.py`, `test_canonical_opening.py`, `test_map_infrastructure.py`, `test_phase51g.py`; `WORLD_DESIGN.md`, `CAMPAIGN_PROGRESS.md`. Nenhum arquivo novo.

**PENDENTE:** desbloqueio narrativo dos portões/contenção, roda, conserto, manivela e finais. A lacuna de destino externo da garagem está resolvida estruturalmente por E14, sem ativar fuga. Fase 5.4 não iniciada.


**Suíte geral final:** executada uma vez, `python -B -m unittest discover -s . -p "test_*.py" -q` — **406 aprovados, zero falhas, erros ou ignorados**, em **33,331 s**. Base 404, dois casos novos. Tkinter disponível; validação gráfica executada. Nenhuma regressão identificada. **Fase 5.3B concluída; Fase 5.4 não iniciada.**
