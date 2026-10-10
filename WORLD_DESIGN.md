# Evolucys: The Estate — WORLD DESIGN — Fase 5.0

**Estado atual: Fase 5.3B — fachada externa da garagem integrada.** Campanha com 58 ambientes e 137 arcos; protótipo com seis. E03/E14 acessível, E14/G01 bloqueado com portões compartilhados. Conteúdo e progressão anteriores preservados. Registro vigente ao final.

## 1. Fonte, autoridade e escopo

Fonte: texto do usuário “EVOLUCYS: THE ESTATE — FASE 5.0 — CONCLUSÃO DO WORLD DESIGN — MAPA OFICIAL”, recebido em 08/10/2026, anexo `fb9eaad4-cebd-45cc-b87f-a5f6fdc68183/Texto colado.txt`. Substitui a pendência de fonte da versão preliminar deste documento.

Os IDs **E01–E09, T01–T12, U01–U09, B01–B10 e L01–L12** são os identificadores estáveis de planejamento fornecidos pelo usuário. A revisão 5.1H acrescenta E10–E13, conforme autorização para usar os próximos IDs livres, e atualiza a topologia externa pelo esboço. Não são renomeações dos IDs do código. Os identificadores `C_...` abaixo referenciam ligações e são reutilizados pelos estados de passagem implementados.

O mapa original tinha 52 ambientes; após a revisão 5.1H, o mundo planejado passou a 56 ambientes em cinco setores; a Fase 5.3A acrescenta G01, garagem da mansão, totalizando 57 ambientes; a Fase 5.3B acrescenta E14, chegando a **58 ambientes**, com backtracking, bloqueios e rotas alternativas. Referência de duração: aproximadamente até três horas na primeira experiência; jogadores experientes poderão concluir em cerca de 60–80 minutos, conforme domínio e dificuldade. São metas de experiência, não resultados medidos. Não criar barreiras artificiais para prolongar a campanha.

A documentação distingue: **confirmado** pela fonte; **recomendação técnica** para implementação futura; **pendência** não especificada. “Nenhum bloqueio especificado” não significa “aberta desde o início”. A lista de ligações é a autoridade topológica; não acrescentar adjacências por proximidade de nomes ou pisos.

## 2. Catálogo oficial dos ambientes

A coluna de ligações reproduz somente a topologia oficial: `↔` permite os dois sentidos quando as condições do mundo permitirem; `→` permite apenas o sentido indicado; `←` indica entrada, sem saída equivalente. “Previsto” não significa salvamento implementado. Um traço significa ausência de ponto previsto, não sinal garantidamente inexistente.

| Setor | Nome | Ambientes |
|---|---|---:|
| E | Exterior | 14 |
| T | Térreo | 12 |
| U | Andar superior | 9 |
| B | Porão principal | 10 |
| L | Complexo Evolucys | 12 |
| G | Garagem da mansão | 1 |
| **Total** | | **58** |


### E — Exterior

| ID de planejamento | Ambiente oficial | Ligações incidentes | Salvamento |
|---|---|---|---|
| E01 | Estrada / carro | ↔ E02 | — |
| E02 | Portão da propriedade | ↔ E01; ↔ E03 | — |
| E03 | Caminho frontal | ↔ E02; ↔ E04; ↔ E05; ↔ E14 | Previsto |
| E04 | Varanda da mansão | ↔ E03; ↔ T01 | — |
| E05 | Lateral da casa | ↔ E03; ↔ E11 | — |
| E06 | Fundos da propriedade | ↔ E12; ↔ E13; ↔ E09; ↔ T07 | — |
| E07 | Casinha de ferramentas | ↔ E12 | — |
| E08 | Estufa abandonada | ↔ E13; → B01 | — |
| E09 | Área do gerador externo | ↔ E06 | — |
| E10 | Jardim da Fonte | ↔ E11 | — |
| E11 | Corredor do Jardim | ↔ E05; ↔ E10; ↔ E12 | — |
| E12 | Pátio da Casinha | ↔ E11; ↔ E07; ↔ E06 | — |
| E13 | Jardim da Estufa e do Poço | ↔ E06; ↔ E08; ↔ B02 (condicionada) | — |

| E14 | Frente da Garagem | ↔ E03; ↔ G01 (bloqueada) | — |

### T — Térreo

| ID de planejamento | Ambiente oficial | Ligações incidentes | Salvamento |
|---|---|---|---|
| T01 | Vestíbulo | ↔ E04; ↔ T02 | — |
| T02 | Salão principal | ↔ T01; ↔ T03; ↔ T08; ↔ T11; ↔ T12; ↔ T04; ↔ T09; ↔ U01; ↔ B07 | Previsto |
| T03 | Sala de estar | ↔ T02; ↔ T04; ↔ G01 (oeste) | — |
| T04 | Sala de jantar | ↔ T03; ↔ T05; ↔ T02 | — |
| T05 | Cozinha | ↔ T04; ↔ T06; ↔ T07; ↔ T12 | — |
| T06 | Despensa | ↔ T05 | — |
| T07 | Lavanderia | ↔ E06; ↔ T05 | — |
| T08 | Escritório | ↔ T02; ↔ T09 | — |
| T09 | Biblioteca | ↔ T08; ↔ T10; ↔ T02 | — |
| T10 | Sala de música | ↔ T09 | — |
| T11 | Banheiro social | ↔ T02 | — |
| T12 | Sala de manutenção | ↔ T02; ↔ T05; ↔ B03 | — |

### U — Andar superior

| ID de planejamento | Ambiente oficial | Ligações incidentes | Salvamento |
|---|---|---|---|
| U01 | Galeria superior | ↔ T02; ↔ U02; ↔ U03; ↔ U04; ↔ U08 | — |
| U02 | Quarto principal | ↔ U01; ↔ U06 | — |
| U03 | Quarto de hóspedes | ↔ U01; ↔ U05 | — |
| U04 | Quarto infantil | ↔ U01 | — |
| U05 | Banheiro superior | ↔ U03 | — |
| U06 | Estudo privado | ↔ U02; ↔ U07 | — |
| U07 | Depósito superior | ↔ U06; ↔ U09 | — |
| U08 | Varanda superior | ↔ U01 | Previsto |
| U09 | Sótão | ↔ U07 | — |

### B — Porão principal

| ID de planejamento | Ambiente oficial | Ligações incidentes | Salvamento |
|---|---|---|---|
| B01 | Câmara sob a Estufa | ← E08; ↔ B02 | — |
| B02 | Túnel antigo | ↔ B01; ↔ B03; ↔ E13 (condicionada) | — |
| B03 | Corredor de serviço | ↔ T12; ↔ B02; ↔ B04; ↔ B05; ↔ B09 | Previsto |
| B04 | Depósito subterrâneo | ↔ B03; ↔ B09 | — |
| B05 | Sala da caldeira | ↔ B03; ↔ B06 | — |
| B06 | Sala elétrica | ↔ B05; ↔ B07 | — |
| B07 | Arquivo do porão | ↔ T02; ↔ B06; ↔ B08 | — |
| B08 | Adega | ↔ B07; ↔ B10 | — |
| B09 | Oficina | ↔ B03; ↔ B10; ↔ B04 | — |
| B10 | Câmara fria | ↔ B09; ↔ B08; ↔ L01 | — |

### L — Complexo Evolucys

| ID de planejamento | Ambiente oficial | Ligações incidentes | Salvamento |
|---|---|---|---|
| L01 | Acesso oculto | ↔ B10; ↔ L02 | — |
| L02 | Corredor do Laboratório | ↔ L01; ↔ L03 | — |
| L03 | Recepção técnica | ↔ L02; ↔ L04; ↔ L10 | Previsto |
| L04 | Sala de observação | ↔ L03; ↔ L05 | — |
| L05 | Laboratório principal | ↔ L04; ↔ L06; ↔ L07; ↔ L10 | — |
| L06 | Laboratório biológico | ↔ L05; ↔ L09 | — |
| L07 | Enfermaria e Cirurgia | ↔ L05; ↔ L08 | — |
| L08 | Câmara de Contenção | ↔ L07; ↔ L11 | — |
| L09 | Biotério | ↔ L06; ↔ L11 | — |
| L10 | Controle de energia | ↔ L03; ↔ L05 | — |
| L11 | Arquivo Científico | ↔ L09; ↔ L08; ↔ L12 | Previsto |
| L12 | Rota de fuga | ↔ L11 | — |

### G — Garagem da mansão

| ID | Ambiente | Ligações | Salvamento |
|---|---|---|---|
| G01 | Garagem | ↔ T03 (leste); ↔ E14 (bloqueada) | — |

## 3. Registro completo das conexões

**69 ligações: 68 bidirecionais e uma queda unidirecional; 137 arcos.** Fase 5.3B acrescenta C_E03_E14 (caminho livre) e C_E14_G01 (portões bloqueados). Nenhum arco anterior removido.

A revisão 5.1H define norte na aproximação E01 → E02 → E03 e sul no retorno. As demais passagens usam nomes locais; comprimentos não foram definidos. O sentido das setas representa navegabilidade, não orientação geográfica. Uma ligação sem tipo definido não será automaticamente convertida em porta.


### Internas — Exterior

| ID de conexão documental | Ligação oficial | Classificação física | Estado/observação |
|---|---|---|---|
| C_E01_E02 | E01 ↔ E02 | Ligação exterior; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_E02_E03 | E02 ↔ E03 | Ligação exterior; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_E03_E04 | E03 ↔ E04 | Ligação exterior; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_E03_E05 | E03 ↔ E05 | Ligação exterior; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_E06_E09 | E06 ↔ E09 | Ligação exterior; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |

| C_E05_E11 | E05 ↔ E11 | Caminho exterior | Disponível na 5.1H; esboço revisado do usuário. |
| C_E10_E11 | E10 ↔ E11 | Caminho exterior | Disponível na 5.1H; esboço revisado do usuário. |
| C_E11_E12 | E11 ↔ E12 | Caminho exterior | Disponível na 5.1H; esboço revisado do usuário. |
| C_E07_E12 | E07 ↔ E12 | Caminho exterior | Disponível na 5.1H; esboço revisado do usuário. |
| C_E06_E12 | E06 ↔ E12 | Caminho exterior | Disponível na 5.1H; esboço revisado do usuário. |
| C_E06_E13 | E06 ↔ E13 | Caminho exterior | Disponível na 5.1H; esboço revisado do usuário. |
| C_E08_E13 | E08 ↔ E13 | Caminho exterior | Disponível na 5.1H; esboço revisado do usuário. |

### Internas — Térreo

| ID de conexão documental | Ligação oficial | Classificação física | Estado/observação |
|---|---|---|---|
| C_T01_T02 | T01 ↔ T02 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_T02_T03 | T02 ↔ T03 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_T03_T04 | T03 ↔ T04 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_T04_T05 | T04 ↔ T05 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_T05_T06 | T05 ↔ T06 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_T05_T07 | T05 ↔ T07 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_T02_T08 | T02 ↔ T08 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_T08_T09 | T08 ↔ T09 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_T09_T10 | T09 ↔ T10 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_T02_T11 | T02 ↔ T11 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_T02_T12 | T02 ↔ T12 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_T02_T04 | T04 ↔ T02 | Passagem entre jantar e salão | Conexão secundária. Nenhum bloqueio especificado na fonte. |
| C_T02_T09 | T09 ↔ T02 | Atalho entre biblioteca e salão | Inicialmente fechado; tipo físico e condição exata de liberação a definir. |
| C_T05_T12 | T05 ↔ T12 | Porta secundária de serviço | Atalho sujeito a desbloqueio; condição e estado físico detalhado a definir. |

### Internas — Andar superior

| ID de conexão documental | Ligação oficial | Classificação física | Estado/observação |
|---|---|---|---|
| C_U01_U02 | U01 ↔ U02 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_U01_U03 | U01 ↔ U03 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_U01_U04 | U01 ↔ U04 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_U01_U08 | U01 ↔ U08 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_U02_U06 | U02 ↔ U06 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_U06_U07 | U06 ↔ U07 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_U07_U09 | U07 ↔ U09 | Acesso ao sótão pelo depósito | Conexão bidirecional confirmada; solução vertical (escada, alçapão etc.) não especificada. |
| C_U03_U05 | U03 ↔ U05 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |

### Internas — Porão principal

| ID de conexão documental | Ligação oficial | Classificação física | Estado/observação |
|---|---|---|---|
| C_B01_B02 | B01 ↔ B02 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_B02_B03 | B02 ↔ B03 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_B03_B04 | B03 ↔ B04 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_B03_B05 | B03 ↔ B05 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_B03_B09 | B03 ↔ B09 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_B05_B06 | B05 ↔ B06 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_B06_B07 | B06 ↔ B07 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_B07_B08 | B07 ↔ B08 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_B09_B10 | B09 ↔ B10 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_B04_B09 | B04 ↔ B09 | Porta de serviço | Inicialmente bloqueada por definição expressa da Fase 5.1I; desbloqueio futuro. |
| C_B08_B10 | B08 ↔ B10 | Corredor de armazenamento | Atalho inicialmente fechado; natureza do fechamento/desbloqueio a definir. |

### Internas — Complexo Evolucys

| ID de conexão documental | Ligação oficial | Classificação física | Estado/observação |
|---|---|---|---|
| C_L01_L02 | L01 ↔ L02 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_L02_L03 | L02 ↔ L03 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_L03_L04 | L03 ↔ L04 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_L03_L10 | L03 ↔ L10 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_L04_L05 | L04 ↔ L05 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_L05_L06 | L05 ↔ L06 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_L05_L07 | L05 ↔ L07 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_L05_L10 | L05 ↔ L10 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_L06_L09 | L06 ↔ L09 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_L07_L08 | L07 ↔ L08 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_L09_L11 | L09 ↔ L11 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_L08_L11 | L08 ↔ L11 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |
| C_L11_L12 | L11 ↔ L12 | Ligação interna; forma a definir | Topologia confirmada; tipo físico e estado inicial não especificados. |

### Entre setores

Garagem integrada à mansão: **C_G01_T03 — T03 oeste ↔ G01 leste**, porta interna compartilhada inicialmente aberta, sem chave ou energia. Na Fase 5.3B, os portões externos passam a compartilhar a conexão bloqueada E14/G01.

| ID de conexão documental | Ligação oficial | Classificação física | Estado/observação |
|---|---|---|---|
| C_E04_T01 | E04 ↔ T01 | Porta principal da mansão | Inicialmente trancada pelo lado externo; comportamento do lado interno e desbloqueio a definir. |
| C_E06_T07 | E06 ↔ T07 | Porta externa de serviço da lavanderia | Atalho; inicialmente inacessível. Condição de acesso/desbloqueio a definir. |
| C_B01_E08 | E08 → B01 | Queda pelo assoalho deteriorado | Evento unidirecional. Sem subida imediata pelo buraco; eventual retorno não está definido como ligação. |
| C_T02_U01 | T02 ↔ U01 | Escadaria principal | Ligação vertical bidirecional. Nenhum bloqueio especificado na fonte. |
| C_B03_T12 | T12 ↔ B03 | Escada de manutenção | Rota inicial de saída do subterrâneo. Sua disponibilidade nesse momento é requisito; condições exatas a definir. |
| C_B07_T02 | T02 ↔ B07 | Antiga escadaria do porão | Atalho; inicialmente bloqueada. Desbloqueio a definir, sem contorno indevido pelo retorno. |
| C_B10_L01 | B10 ↔ L01 | Entrada oculta do complexo | Condicionada a evento/mecanismo futuro; saber a localização não autoriza acesso. Sem liberar pelo lado reverso antecipadamente. |

| C_B02_E13 | E13 ↔ B02 | Escada interna do poço | Secreta; lanterna normal equipada e acesa para descer; trinco aberto somente por dentro em B02. |

## 4. Entradas, saídas e relações entre setores

| Setor | Pontos de fronteira oficiais | Função |
|---|---|---|
| E | E04 com T01; E06 com T07; E08 somente para B01; E13 com B02 | Acesso principal, serviço/atalho e queda |
| T | T01 com E04; T07 com E06; T02 com U01 e B07; T12 com B03 | Distribuição central, acesso superior e duas ligações ao porão |
| U | U01 com T02 | Única fronteira de setor informada |
| B | B01 recebe E08; B02 com E13; B03 com T12; B07 com T02; B10 com L01 | Entrada pela queda, primeira saída, atalho antigo e acesso secreto |
| L | L01 com B10 | Única fronteira de setor informada; L12 ainda não possui destino externo definido |

### Queda e primeira saída do subterrâneo

Sequência obrigatória de coerência: **E08 → B01 ↔ B02 ↔ B03 ↔ T12**. Após cair, Joseph deve poder explorar B01, B02 e B03 e alcançar T12 por uma rota fisicamente plausível. Essa primeira saída não pode exigir entrada em L01 ou em qualquer outro ambiente do complexo.

A queda acontece **antes** de Joseph pegar a barra de ferro procurada para usar no macaco do carro. Não colocar a barra no inventário antes da queda. A câmara B01 fica sob o piso da estufa, conforme revisão 5.1H; não inventar aqui túneis ou salas adicionais. A ligação E08 → B01 não recebe arco inverso. “Não consegue subir imediatamente” não autoriza criar um retorno posterior não listado.

A topologia já oferece B01 → B02 → B03 → T12. Essa rota está implementada e validada na revisão 5.1H, com passagens provisoriamente livres.

### Atalhos confirmados

| Ligação | Papel | Restrição registrada |
|---|---|---|
| T07 ↔ E06 | Lavanderia/fundos | Inicialmente inacessível |
| T09 ↔ T02 | Biblioteca/salão | Inicialmente fechado |
| T05 ↔ T12 | Cozinha/manutenção | Sujeito a desbloqueio |
| B04 ↔ B09 | Depósito/oficina | Circuito alternativo; bloqueio inicial não informado |
| B07 ↔ T02 | Escadaria antiga | Inicialmente bloqueada |
| B08 ↔ B10 | Corredor de armazenamento | Inicialmente fechado |

As condições exatas permanecem pendentes. Não inventar chaves, requisitos de inventário ou puzzles. Uma porta ou bloqueio deve controlar o estado navegável da ligação, e não apenas sua descrição. Atalhos não podem fornecer, pelo lado de retorno, acesso antecipado que contrarie uma condição importante.

### Complexo secreto

B10 ↔ L01 é uma entrada oculta **condicionada**, não uma saída livre. A descoberta do lugar e a autorização de passagem são estados distintos: conhecer antecipadamente o nome ou destino não satisfaz o evento/mecanismo necessário. A ligação só deve se tornar navegável conforme seu estado real. Permitir revisitas depois do desbloqueio, conforme o progresso autorizar. A justificativa física e narrativa permanece pendente, sem dispositivo implementado.

## 5. Salvamento previsto

Celular antigo compatível com o **ano 2000**. O salvamento completo ainda não existe; nenhum ponto abaixo foi implementado.

| Ambiente | Local previsto | Fundamentação/pendência |
|---|---|---|
| E03 | Caminho frontal | Ainda existe sinal de celular |
| T02 | Salão principal | Próximo a janela alta; sinal fraco |
| U08 | Varanda superior | Recepção de sinal |
| B03 | Corredor de serviço | Abertura/estrutura para recepção localizada; solução física a definir |
| L03 | Recepção técnica | Sem sinal normal nessa profundidade; instalação de retransmissão/equipamento equivalente a justificar |
| L11 | Arquivo central | Mesma exigência de justificativa física; dispositivo não definido |

Regras oficiais: seis pontos previstos; **cinco slots de save**; na dificuldade normal os pontos podem ser reutilizados; na dificuldade difícil desbloqueável, cada ponto poderá ser usado apenas uma vez. Não confundir quantidade de pontos com quantidade de slots. Critério de desbloqueio da dificuldade e detalhes da restrição por partida/carregamento ainda precisam de definição.

Dependências futuras: persistência completa e versionada de mundo, jogador, portas, inventário, inimigos, memória, conhecimento e progresso; identidade dos pontos; dificuldade/desbloqueio; uso de pontos na dificuldade difícil; seleção e armazenamento dos cinco slots; comportamento após carregar. O sinal atual do celular e o exportador parcial de exploração não implementam essas regras. Não criar aparelhos ou interfaces nesta etapa.

## 6. Arquitetura compatível com a base atual

`world.py` fornece `Room`, `GameObject` e `create_world()`; não há classe `World` paralela. `GameState.rooms` é o dicionário único de ambientes e `current_location` seu ID corrente. Preservar esse contrato.

`Room.exits` representa origem/direção/destino; `exit_doors` aponta para objetos físicos e `exit_names` oferece nomes naturais. `add_exit(direction, room_id, door=None, name=None)` já permite ligações sem porta e não cria retorno automaticamente. `CommandParser.move()` e a exploração devem continuar responsáveis pelas verificações e efeitos existentes.

Recomendação futura: definições por setor, montadas primeiro como ambientes e objetos compartilhados e depois como ligações orientadas. Não criar um segundo GameState nem mudar o motor de exploração. Criar somente o recorte autorizado numa etapa futura, sem saídas navegáveis para ambientes ainda ausentes.

Os estados `opened`, `locked`, `blocked` e `accessible` já sustentam passagens físicas. Os dois lados de uma mesma porta devem compartilhar uma instância quando seu estado for comum. A porta principal, trancada inicialmente do lado externo, exige validar o comportamento assimétrico antes de assumir que o estado compartilhado atual basta. A queda é evento unidirecional; sua forma de disparo pertence ao planejamento/implementação do prólogo.

Os IDs oficiais continuam documentais nesta fase. A futura tabela de correspondência com IDs de execução deve preservar referências existentes até uma migração explicitamente autorizada. Objetos persistentes precisarão de `object_id` e fechaduras de `lock_id` estáveis; UUIDs gerados novamente não substituem identidades persistentes. Atribuir IDs técnicos novos apenas no recorte autorizado.

## 7. Migração pendente dos seis ambientes atuais

| ID atual (inalterado) | Ambiente atual | Equivalente de planejamento | Pendência de migração |
|---|---|---|---|
| `entrance` | Entrada da Mansão | T01 — Vestíbulo (confirmada funcionalmente na 5.1A) | Equivalência funcional confirmada; descrição e geometria finais pendentes. Porta principal hoje é objeto bloqueado sem destino externo; falta E04 ↔ T01. Início atual aqui difere do prólogo E01. |
| `main_hall` | Salão Principal | T02 — Salão principal (clara) | Preservar referência; rever adjacências e aliases. Cozinha direta conflita com mapa oficial. |
| `kitchen` | Cozinha | T05 — Cozinha (clara) | Conexão atual direta com `main_hall` não consta do mapa; futura navegação deverá seguir somente ligações oficiais. |
| `office` | Escritório | T08 — Escritório (clara) | Ligação com T02 compatível; falta T08 ↔ T09. Distribuição do protótipo não é conteúdo definitivo. |
| `cellar` | Arquivo do Porão | B07 — Arquivo do porão (clara) | Atual acesso T02 corresponde à escadaria antiga, mas seu estado e liberação precisam seguir o mapa. Não corresponde a B01 nem representa todo o porão. Faltam B06/B08. |
| `upper_hall` | Corredor Superior | U01 — Galeria superior (confirmada funcionalmente na 5.1A) | A escada T02 ↔ U01 é compatível; revisar apresentação, geometria e novas adjacências na migração. |

O protótipo mantém `entrance → main_hall`, `main_hall ↔ kitchen`, `main_hall ↔ office`, `main_hall ↔ cellar` e `main_hall ↔ upper_hall`, com os retornos existentes. Nenhum ID, ligação, objeto ou estado foi alterado agora. Não transportar automaticamente pistas, itens ou inimigos do protótipo para o mapa oficial.

Referências que exigirão revisão em uma migração autorizada: entrada inicial e `visited_rooms` em GameState; aliases de salão/andar superior; destinos das rotas; memória contextual e identidades; referências de portas/chaves. A tabela é um plano de correspondência, não um script de renomeação.

## 8. Coerência espacial e decisões abertas

| Pendência | Registro e limite desta etapa |
|---|---|
| Orientação e geometria | A fonte é topológica, sem planta cardinal, distâncias, dimensões ou orientação das portas. Não atribuir direções por adivinhação. |
| Várias conexões por sala | T02 possui nove vizinhos oficiais, acima das seis direções cardinais/verticais usuais. `exits` admite apenas um destino por chave: estratégia de identificação definida na seção 10, com orientação e integração ainda pendentes. Nenhuma nova direção foi criada. |
| Tipo das ligações comuns | Muitas conexões não especificam porta, arco ou passagem aberta. Classificação detalhada e estados iniciais continuam pendentes, sem converter tudo em porta. |
| Porta principal | Trancada pelo exterior: validar abertura por dentro, compartilhamento do estado e liberação do retorno. |
| Atalhos e bloqueios | Falta definir condições exatas e lados de acionamento; conferir que não há contorno antecipado pelo retorno. |
| Estufa e subterrâneo | Implantação E08/B01 definida na 5.1H e deterioração do assoalho; queda antes da coleta da barra é obrigatória. |
| Primeira saída | Reservar disponibilidade B01–B02–B03–T12 sem exigir laboratório; restrições futuras não podem cortar essa rota no momento necessário. |
| Escadas e sótão | Escadarias entre setores estão identificadas. A solução vertical U07/U09, níveis relativos e percurso físico exigem validação. |
| Porão grande | Escala e apresentação devem tornar seu tamanho surpreendente em relação à mansão; planta ainda não define dimensões. |
| Entrada secreta | Definir justificativa e condição real de B10/L01; antecipar conhecimento não pode liberar acesso. |
| Final em L12 | “Rota de fuga” não traz destino externo/conexão de saída na fonte. L12 permanece terminal na topologia documentada; não acrescentar ambiente ou ligação para resolver isso agora. |
| Salvamento profundo | Justificar B03, L03 e L11 fisicamente, sem assumir cobertura normal de celular no complexo. |
| Migração | Equivalências funcionais confirmadas na seção 10; resolver principalmente a ligação direta salão/cozinha e o início da campanha. |

Não foi encontrada contradição entre os pares de conexões oficiais nem ambiente desconectado na topologia completa. Há lacunas de geometria/desbloqueio e o conflito com o protótipo registrado acima. Isso não prova que a campanha estará navegável com bloqueios iniciais: essa avaliação dependerá dos estados e eventos ainda não definidos.

## 9. Conferência documental

Conferência histórica da transcrição original da Fase 5.0 (antes da revisão 5.1H): **52 IDs únicos**, nomes e contagens por setor iguais à fonte; **61 ligações únicas**, das quais **sete intersetoriais**; **seis pontos de salvamento**; originalmente apenas **E07 → B01** unidirecional; rota **B01 → B02 → B03 → T12** presente; **B10 ↔ L01** marcada como condicionada. Menções repetidas dos mesmos vínculos na fonte contam uma única vez.

Sem ambientes ou conexões adicionais. Todas as referências de destino pertencem ao catálogo. A conectividade foi conferida documentalmente, sem tratar portas bloqueadas como abertas em gameplay. Nenhum teste do jogo foi executado na conclusão da Fase 5.0; verificações da 5.1A constam em CAMPAIGN_PROGRESS.md.

Somente `WORLD_DESIGN.md` e `CAMPAIGN_PROGRESS.md` foram atualizados. Nenhum código, ID de execução, interface, mecânica, item, puzzle, inimigo, arte ou áudio foi alterado. A **Fase 5.0 documental está concluída**; a preparação **5.1A** está registrada abaixo; sua implementação posterior **5.1B** consta da seção 11.


## 10. Fase 5.1A — contrato de compatibilidade e preparação

Registro do plano técnico da 5.1A; a implementação autorizada depois está na seção 11. Esta seção não implica migração de topologia, novos ambientes ou conteúdo. Foram examinados `world.py`, `game_state.py`, `command_parser.py`, `action_context.py` e `exploration_systems.py`, além dos aliases de escadas em `command_language.py`. A base executável e o início em `entrance` continuam na Fase 4.5.5.

### Identidade dos ambientes e referências antigas

A tabela da seção 7 é o mapeamento de migração. Confirmam-se **entrance → T01** pela descrição de um ambiente já dentro da mansão, com porta principal atrás de Joseph e acesso ao salão, e **upper_hall → U01** pela chegada da escadaria principal e retorno ao salão. Trata-se de equivalência funcional, sem afirmar que a decoração, o nome atual ou a geometria do protótipo sejam definitivos. As demais correspondências são **main_hall → T02, kitchen → T05, office → T08, cellar → B07**; B07 nunca deve ser convertido em B01.

Estratégia em etapas, dentro da mesma fábrica e do mesmo dicionário:

1. Enquanto o protótipo não for migrado, manter seus seis IDs como chaves reais. Uma futura tabela de aliases externa ao dicionário poderá resolver IDs oficiais para os IDs reais existentes; novos ambientes autorizados poderão usar seus IDs oficiais. Um ID planejado sem ambiente implementado deve ser rejeitado, nunca materializado implicitamente.
2. Centralizar a resolução de identidade nos pontos de consulta, atribuição e importação antes de trocar as chaves. Na migração autorizada, tornar os IDs oficiais canônicos e aceitar os seis nomes antigos como aliases de entrada. A saída do resolvedor será sempre a chave real, idempotente, sem cadeias/ciclos. Manter **uma entrada por Room** em `rooms`; não inserir simultaneamente `entrance` e `T01` apontando para o mesmo objeto. Isso duplicaria iterações de salas, rondas e exportações.
3. Atualizar em conjunto as chaves, `Room.room_id`, destinos de `exits`, `current_location`, `visited_rooms`, `visited_empty`, rotas de patrulha e referências espaciais da memória. Converter contextos estruturados como `door:<origem>:<destino>`, `sound:<sala>` e `sight:<sala>`, incluindo salas nos sinais; não fazer substituição global de texto nem apagar memória. Preservar entidades e seu estado, sem recriar inventário ou GameState.
4. Auditar acessos diretos `rooms[...]` e comparações literais: criar apenas um resolvedor não torna esses acessos automaticamente compatíveis. `command_language.py` compara `upper_hall` e `main_hall` em “voltar ao salão”; esses pontos e consumidores externos/testes devem passar pela resolução antes da troca. IDs exclusivos dos tutoriais permanecem válidos e não são renomeados como campanha.
5. O exportador de exploração é parcial e versionado, não um save completo. Sua futura importação deve normalizar os IDs antes de validar destinos e restaurar memória/rondas. Identidades de entidades precisam continuar reconhecíveis; não prometer compatibilidade de saves completos inexistentes nem recriar UUIDs como solução.

Aliases preservam **identidade**, não autorizam deslocamento remoto, descoberta ou passagem por bloqueios. O início permanecerá no mesmo ambiente funcional T01 quando houver somente migração de IDs; mudar para E01 pertence ao prólogo, em outra entrega.

### Nove conexões locais do Salão Principal

`Room.exits` aceita chaves de texto além de direções. Usar uma única chave local por ligação, `exit_names` para identificação e o ID documental `C_...` como identidade física estável. A tabela abaixo é um contrato proposto de resolução, não novas saídas já implementadas nem texto narrativo final. “Passagem” não determina a existência de uma porta onde a fonte não a especificou.

| Destino | Identificação local proposta | Chave local proposta em T02 | Observação |
|---|---|---|---|
| T01 | Passagem para o vestíbulo | `sul` | Preserva comando do protótipo |
| T03 | Passagem para a sala de estar | `via_t03` | Orientação não fornecida |
| T04 | Passagem para a sala de jantar | `via_t04` | Ligação oficial direta com salão |
| T08 | Passagem para o escritório | `leste` | Preserva comando do protótipo |
| T09 | Passagem para a biblioteca | `via_t09` | Atalho inicialmente fechado |
| T11 | Passagem para o banheiro social | `via_t11` | Orientação não fornecida |
| T12 | Passagem para a sala de manutenção | `via_t12` | Não confundir com a escada B03/T12 |
| U01 | Escadaria principal | `cima` | Preserva subir e aliases existentes |
| B07 | Antiga escadaria do porão | `norte` | Chave herdada; bloqueio oficial deve ser tratado na migração |

As chaves herdadas preservam comandos, **não confirmam orientação cardinal oficial**. Novos nomes devem ser apresentados somente conforme conhecimento/visibilidade autorizados; não revelar destinos secretos pela tabela de aliases. Nomes locais de portas podem ser usados sem visitar o destino, enquanto o nome remoto do ambiente só é resolvido quando visitado, conforme `ActionContext.passages()`.

O parser deve resolver a expressão para uma passagem local e então usar `move()` com suas verificações existentes. Não criar entradas duplicadas no grafo para sinônimos ou direções alternativas: elas gerariam falsas opções na desambiguação e ambiguidades nas rondas. Pedidos genéricos como “a passagem” mantêm a escolha contextual quando há múltiplas opções. As chaves `via_...` são técnicas, não comandos que o jogador precisará decorar.

Limites a resolver antes de implementar: `ActionContext` usa `exit_names` no lugar do nome da porta quando informado; alinhar os nomes ou resolver aliases explicitamente sem perder o nome físico. `ExplorationSystems.door_direction()` aceita chave/nome exato da porta, mas não consulta `exit_names`. Integrar a mesma resolução local nos consumidores necessários, preservando efeitos e turnos; não alterar ajuda, narrativa ou exploração nesta etapa. Os nomes propostos e comandos devem passar por validação direcionada de ambiguidade. Manter `cima`/`baixo` para escadas existentes e validar futuras salas com mais de uma escada, sem inventar orientação.

### Conflito salão–cozinha e ordem da expansão

Hoje `main_hall.oeste → kitchen` e `kitchen.leste → main_hall` existem. O mapa oficial não possui T02 ↔ T05. Na troca de topologia, remover **os dois sentidos** dessa ligação; aliases de IDs não podem mantê-la como atalho invisível nem fazer “oeste” atravessar várias salas em uma ação.

As alternativas oficiais incluem T02 → T04 → T05 (também T02 → T03 → T04 → T05); T02 → T12 → T05 depende do desbloqueio do acesso de serviço. Implementar primeiro os ambientes intermediários do recorte autorizado e validar uma rota disponível antes de remover a ligação do protótipo. Até essa entrega, manter a topologia atual intacta. Não redirecionar “oeste” para T04 por adivinhação: seu significado no mapa migrado depende da orientação futura. Compatibilidade de nomes antigos não pode garantir uma conexão que o mapa oficial proíbe.

### Estado físico, bloqueios e sentidos

Para uma porta de estado comum, criar **um único GameObject** e passar a mesma instância aos dois `add_exit()`; `exit_doors` dos dois lados compartilha `opened`, `locked`, `blocked` e `accessible`. O protótipo já faz isso com a porta do porão e a escadaria. Associar identidade persistente à conexão documental; não renomear agora `lock_id`, `object_id` ou chaves existentes. Não copiar dois objetos com estados independentes nem duplicar a lógica de abrir/destrancar.

Ligações abertas não precisam de porta artificial. Onde houver bloqueio físico, usar o mecanismo de passagem existente e distinguir fechado, trancado, bloqueado e inacessível; a fonte não autoriza transformar todo atalho fechado em fechadura com chave. Os seis atalhos permanecem os da seção 4, com os estados fornecidos ali. Eventos futuros deverão alterar o estado compartilhado uma única vez; lados de acionamento e requisitos ainda não definidos permanecem pendentes.

A porta E04/T01 exige decisão sobre restrição somente externa: o estado global atual pode ser insuficiente para regras diferentes por lado. Validar essa semântica antes de qualquer extensão mínima ao contrato da passagem, mantendo uma identidade/estado físico único. Não inventar uma solução de destranca interna nesta etapa.

A queda **E07 → B01** é transição de evento, sem arco inverso. Não cadastrá-la como saída livre bidirecional nem como caminhada comum: `_step()` das rondas só conhece adjacência e bloqueios, portanto uma saída livre poderia ser percorrida por atores sem a semântica da queda. Seu disparo e integração com o deslocamento existente pertencem ao prólogo autorizado; nenhum gatilho ou regra para inimigos foi criado. A rota **E07 → B01 → B02 → B03 → T12** e a disponibilidade da escada de manutenção na saída inicial continuam obrigatórias.

**B10 ↔ L01** deve compartilhar uma condição real de passagem nos dois sentidos. Separar descoberta de autorização: nomes conhecidos, IDs digitados, aliases, “ir”, “atravessar” ou comandos cautelosos nunca alteram o estado de liberação. Enquanto não satisfeita a condição futura, um bloqueio efetivo deve barrar ambos os lados; apenas texto ou ocultação na lista de sugestões não basta. Não definir chave, puzzle, evento narrativo ou dispositivo. `accessible=False` exclui candidatas no contexto, mas sozinho não garante ocultação de objetos em todos os consumidores; `visible_objects()` filtra iluminação, e a percepção sonora percorre adjacências. Validar também o conhecimento exposto por esses consumidores antes de registrar a passagem secreta jogável, sem modificar esses sistemas agora.

### Critérios para a próxima implementação autorizada

Validar separadamente: resolução de IDs antigos/oficiais sem duplicação de salas; continuidade de visitas/memória; nove ligações locais distintas; direções e aliases de escadas preservados; estados de porta refletidos dos dois lados; nenhum contorno dos bloqueios por nome ou retorno; ausência da ligação T02/T05 após a troca; preservação da rota inicial e ausência de B01 → E07. Topologia planejada não prova navegabilidade com estados ainda indefinidos.

A próxima etapa recomendada é **5.1B, somente após autorização**, com recorte explícito para infraestrutura de compatibilidade e testes locais antes da expansão de salas. Pendências narrativas e espaciais não devem ser preenchidas pelo código. As duas expectativas antigas de testes e o resultado da verificação desta preparação estão registrados em CAMPAIGN_PROGRESS.md.


## 11. Fase 5.1B — infraestrutura implementada

Implementação limitada à identidade e às passagens, sobre as seis salas existentes. `Room`, `GameState`, `create_world()` e o parser continuam responsáveis pelo mesmo mundo. A fábrica, os objetos, os inimigos, os documentos, o início em `entrance` e a ligação temporária salão/cozinha não foram modificados. Os 52 ambientes continuam sendo o mapa documental; não há campanha nova jogável.

### Contrato de IDs em execução

`world.ROOM_ALIASES` contém as seis correspondências da seção 7; `OFFICIAL_ROOM_IDS` contém os 52 identificadores oficiais, sem instanciar salas. `GameState.resolve_room_id(id)` retorna a chave realmente existente e `get_room(id)` retorna sua Room. Ambos aceitam os aliases antigos/oficiais; IDs sem ambiente implementado geram `KeyError`. Se as duas identidades forem registradas como entradas concorrentes, a resolução acusa `ValueError` em vez de escolher silenciosamente.

Exemplo atual: `game.get_room('entrance') is game.get_room('T01')`. `game.current_location = 'T02'` normaliza para `main_hall`; o setter é uma atribuição interna, não um comando de teleporte acessível ao jogador. Visitas e sinais da exploração continuam usando IDs reais. Destinos e rotas informados por alias são normalizados na navegação/percepção/ronda.

**`game.rooms` permanece um dicionário comum de chaves reais**, com exatamente seis entradas na campanha. Portanto, novos consumidores que aceitem aliases devem usar `get_room()`; `rooms['T01']` não é a API de compatibilidade enquanto a chave real for `entrance`. IDs próprios das demonstrações continuam funcionando. Não houve renomeação em massa, duplicação de salas ou alteração do formato parcial de exportação. Importar dados arbitrariamente renomeados, migrar as chaves canônicas e implementar save completo continuam fora desta entrega.

### Nomes e resolução local

`ActionContext.passages()` resolve apenas ligações conhecidas da sala corrente. Considera a chave local, `exit_names` e o nome físico da porta conjuntamente; um nome de apresentação não elimina mais o nome da porta. O nome do destino visitado permanece uma opção adicional. O normalizador mantém seus aliases locais e direcionais existentes, agora respeitando o filtro de conexões conhecidas.

O parser aceita chaves além dos pontos cardinais, permitindo nove ou mais conexões sem duplicar arcos para cada sinônimo. Pedidos ambíguos mantêm a intenção, inclusive cautela, para complemento como “a do escritório”. A pergunta não consome turno; a ação completada usa o fluxo de turnos/reação já existente. `door_direction()` utiliza a mesma resolução de nomes para a escuta e os consumidores existentes. Nenhuma lista técnica de saídas foi acrescentada à narração.

A tabela de nove conexões da seção 10 continua sendo planejamento de conteúdo. O suporte foi validado em salas mínimas de teste; T02 ainda possui somente as ligações do protótipo.

### Portas e conexões especiais

`Room.connect(other, direction, reverse=None, door=None, name=None, reverse_name=None, state=None)` monta conexões entre Rooms já existentes. O retorno só é criado quando `reverse` é fornecido. Quando há porta, a mesma instância é registrada nos dois lados, preservando integralmente abertura, fechamento, fechadura, chaves e bloqueio existentes. Os nomes locais podem diferir. Não foi criado outro gerenciador de mundo.

`Room.add_exit()` continua compatível com suas chamadas antigas e aceita `state` opcional. `PassageState` acrescenta apenas dados da ligação: `connection_id`, `kind`, descoberta (`known`, leitura) e autorização (`enabled`, mutável pelo mundo). `Room.connect()` gera identidade estável a partir dos endpoints quando nenhum estado é fornecido; identidades explícitas são aceitas. Para acessos bidirecionais montados manualmente com `add_exit()`, passar a mesma porta e o mesmo estado em ambos os lados. Não criar objetos de porta concorrentes para representar uma única porta física.

- **Atalho:** um estado compartilhado com `enabled=False` barra movimento nos dois lados e rondas. Uma futura alteração autorizada de `enabled` permite a passagem, ainda sujeita ao estado físico da porta. Nenhum evento, puzzle ou requisito foi inventado.
- **Segredo:** `known=False` mantém a conexão interna fora de `known_exits()`, resolução, ajuda e propagação sonora. Uma porta registrada por essa conexão não é adicionada aos objetos visíveis/interativos antes da descoberta. `state.reveal()` registra a porta nos lados e torna a conexão conhecida, sem mudar `enabled` ou abrir/destrancar a porta. Para B10/L01 condicionado, construir com `known=False, enabled=False`; nome, ID, direção, escuta ou comando antecipado não alteram esses estados. O evento de descoberta/liberação não foi implementado. Portas secretas devem ser cadastradas pelo contrato da conexão, não adicionadas manualmente aos objetos visíveis antes da descoberta.
- **Queda:** `kind='fall'` representa o arco de evento E07 → B01. `connect()` rejeita retorno para esse tipo; a ligação não entra nas saídas caminháveis, na ajuda ou nas rondas. O comando de movimento não a trata como escada. O disparo da queda e a integração do evento do prólogo permanecem futuros; a infraestrutura não inventa um comando de queda nem um arco de volta.

`Room.passage_failure()` aplica a descoberta/autorização antes das regras físicas existentes da porta. Assim, abrir uma porta não libera automaticamente uma condição independente da conexão. A pequena adaptação em `context_help.py` apenas impede recomendar ligações desconhecidas ou ainda não liberadas; conteúdo, formato e regras narrativas da ajuda foram preservados.

### Validação e limites

`test_map_infrastructure.py` cobre aliases, unicidade, IDs ausentes, normalização de visitas/memória, nove passagens, desambiguação/cautela, nomes físicos e de apresentação, estado compartilhado, bloqueio/liberação de atalho, queda, segredo e integração com VisualSession. Os testes de compatibilidade existentes executados estão registrados em CAMPAIGN_PROGRESS.md.

Continuam pendentes: recorte oficial a implementar, orientação, condições reais de desbloqueio, regra assimétrica da porta principal, migração persistente das chaves de salas, evento da queda e conteúdo da campanha. Preservados o planejamento E07 → B01 → B02 → B03 → T12 e o acesso condicionado B10 ↔ L01. Não remover T02/T05 antes de construir e validar sua rota substituta. **Fase 5.1C não iniciada.**


## 12. Fase 5.1C — recorte inicial do mapa oficial

### IMPLEMENTADO — ambientes e configuração

A mesma `create_world(configuration='campaign')` cria o conteúdo existente e aplica o recorte oficial usando `Room.connect()` e `PassageState` da 5.1B. `GameState()` e a opção de iniciar campanha de VisualSession selecionam essa configuração por padrão. A aplicação continua iniciando em **entrance / T01**, sem prólogo externo ou teleporte para outra sala.

| ID oficial | Chave real | Ambiente | Situação neste recorte |
|---|---|---|---|
| T01 | `entrance` | Vestíbulo | Existente, nome alinhado; início preservado |
| T02 | `main_hall` | Salão Principal | Existente; oito conexões locais, contando dois atalhos bloqueados |
| T03 | `T03` | Sala de Estar | Novo ambiente, descrição ambiental provisória |
| T04 | `T04` | Sala de Jantar | Novo ambiente, descrição ambiental provisória |
| T05 | `kitchen` | Cozinha | Existente; acesso oficial pela sala de jantar |
| T06 | `T06` | Despensa | Novo ambiente, descrição ambiental provisória |
| T08 | `office` | Escritório | Existente; acesso à biblioteca |
| T09 | `T09` | Biblioteca | Novo ambiente; acessível pelo escritório |
| T11 | `T11` | Banheiro Social | Novo ambiente, descrição ambiental provisória |
| U01 | `upper_hall` | Galeria Superior | Existente, nome alinhado; escadaria preservada |
| B07 | `cellar` | Arquivo do Porão | Instanciado e preservado, mas inacessível desde o início enquanto o atalho estiver bloqueado |

Há **11 Rooms únicas** no dicionário. A API `get_room()` aceita os seis IDs antigos e seus equivalentes oficiais sem duplicação. As seis chaves antigas não foram renomeadas; não há migração de memória ou salvamento nesta etapa.

Os cinco ambientes novos têm somente descrições ambientais, sem objetos de recompensa, documentos, inimigos ou puzzles adicionados. A porta do atalho da biblioteca é um objeto de conexão, não um puzzle com chave nova. As descrições não enumeram automaticamente objetos nem revelam mecanismos.

### IMPLEMENTADO — topologia e bloqueios

São **12 ligações bidirecionais / 24 arcos** neste recorte:

| Ligação | Estado inicial da campanha |
|---|---|
| T01 ↔ T02 | Disponível |
| T02 ↔ T03 | Disponível |
| T02 ↔ T04 | Disponível |
| T02 ↔ T08 | Disponível |
| T02 ↔ T09 | Atalho fechado e bloqueado, não utilizável |
| T02 ↔ T11 | Disponível |
| T03 ↔ T04 | Disponível |
| T04 ↔ T05 | Disponível |
| T05 ↔ T06 | Disponível |
| T08 ↔ T09 | Disponível |
| T02 ↔ U01 | Escadaria principal disponível nos dois sentidos |
| T02 ↔ B07 | Escadaria antiga bloqueada nos dois sentidos |

Os dois atalhos possuem `enabled=False` compartilhado e porta física bloqueada. Abrir, forçar, usar comandos nomeados, caminhar cautelosamente ou tentar pelo lado oposto não os libera. Não foram definidos eventos, chaves ou condições para seu desbloqueio. A chave antiga do porão não substitui a autorização do atalho oficial. O estado de uma porta é o mesmo nos dois lados.

A ligação direta **T02 ↔ T05 foi removida somente da configuração de campanha**, depois da inclusão das rotas T02 → T04 → T05 e T02 → T03 → T04 → T05, ambas verificadas também no retorno. “Oeste” no salão e “leste” na cozinha não preservam nem redirecionam o atalho antigo. Pedir uma sala remota não executa uma sequência automática de movimentos.

Os novos vínculos usam nomes de passagens e chaves `via_<id>`, sem inventar orientação cardinal. Permanecem as direções das ligações antigas compatíveis: vestíbulo/salão, salão/escritório, escadaria principal e a referência norte/sul do acesso bloqueado ao porão. Nomes locais permitem “entrar na sala de estar”, “ir para a cozinha” a partir do jantar, “entrar no escritório”, “passar pela porta da biblioteca” e “subir a escadaria”. “Voltar ao salão principal” resolve somente uma ligação local. O complemento de intenção e a cautela continuam passando pelo fluxo existente de turnos. Tentativas de ir a destino sem passagem direta recebem uma resposta de Joseph, sem lista técnica de saídas.

### IMPLEMENTADO — demonstração e conteúdo preservado

`create_world(configuration='prototype')` / `GameState(configuration='prototype')` selecionam a configuração de seis salas preservada, dentro da mesma fábrica e das mesmas classes. Cada sessão possui apenas seu próprio dicionário de Rooms; não há salas alternativas duplicadas dentro do mundo ativo ou segundo gerenciador.

Na demonstração permanecem a ligação salão/cozinha, a sequência de ferramentas/chaves/documentos, o vigia, a escada e a abertura antiga do porão. Para abri-la visualmente, executar **`python prototype_demo.py` a partir de outputs**. O lançador usa VisualApp e `VisualSession.start_campaign(configuration='prototype')`, sem modificar o layout nem acrescentar opções ao menu. Ao sair e iniciar uma nova campanha pelo menu normal, vale a configuração oficial. Tutoriais e demonstrações de sistemas já existentes permanecem isolados e inalterados.

Não houve redistribuição de objetos. O conteúdo legado continua nos mesmos locais também no recorte de campanha, **provisoriamente**, sem transformar essa distribuição em decisão definitiva. Somente as condições de acesso previstas pelo recorte mudaram; conteúdo definitivo e reorganização de recursos permanecem pendentes. A descrição do acesso ao porão na campanha não recomenda atravessar um atalho que agora está bloqueado. O texto original permanece na demonstração.

### PLANEJADO / PENDENTE

- Os outros **41 ambientes não foram instanciados**. Não há saídas para destinos ausentes. T02 terá nove conexões no mapa completo; a nona, T12, não pertence a este recorte.
- Permanecem planejadas a rota E07 → B01 → B02 → B03 → T12, a queda e a entrada condicionada B10 ↔ L01. Sua ausência do recorte não remove o planejamento nem autoriza criar rotas substitutas.
- Condições de liberação de T02/T09 e T02/B07, geometria cardinal definitiva, conteúdo da campanha, migração de chaves persistentes e salvamento seguem pendentes.
- **Fase 5.1F:** uniformizar a possibilidade de inserir comandos em todos os objetos inspecionáveis, tenham ou não segredos. Não implementado: `document_view.py`, a interface de inspeção e os comandos de manipulação não foram modificados.
- Próximo passo recomendado: definir o recorte e critérios da **Fase 5.1D** a partir desta topologia validada. **5.1D não iniciada.** Não avançar automaticamente para outra etapa.

### VALIDAÇÃO

71 testes distintos direcionados aprovados (seleção e contagem em CAMPAIGN_PROGRESS.md). Cobrem o grafo exato, aliases, navegação e retornos, bloqueios, contexto/cautela, salas ausentes, isolamento, objetos preservados, cadeia original da demonstração e integração com a interface existente. O teste de widgets construiu as 11 salas e o lançador do protótipo sem erro em Tkinter, com janela configurada para 1100×760; não foi um redesenho nem uma aprovação de arte definitiva. Nenhuma suíte completa foi executada.


## 13. Fase 5.1D — expansão e conclusão estrutural do térreo

### IMPLEMENTADO

Adicionados **T07 — Lavanderia**, **T10 — Sala de Música** e **T12 — Sala de Manutenção**, com IDs reais oficiais e descrições ambientais provisórias. A configuração padrão possui **14 Rooms únicas**, incluindo os 12 ambientes do térreo, B07 e U01. O início continua em entrance/T01; os seis aliases antigos continuam resolvendo as mesmas salas.

| Conexão adicionada | Estado inicial utilizado |
|---|---|
| T05 ↔ T07 (`C_T05_T07`) | Disponível, provisoriamente |
| T09 ↔ T10 (`C_T09_T10`) | Disponível, provisoriamente |
| T02 ↔ T12 (`C_T02_T12`) | Disponível, provisoriamente |
| T05 ↔ T12 (`C_T05_T12`) | Porta secundária de serviço fechada e bloqueada; estado compartilhado `enabled=False` |

A fonte não fixa o estado inicial das três passagens comuns. Foram deixadas disponíveis **para exploração e testes deste recorte**, sem transformar essa decisão em regra definitiva da campanha. São passagens nomeadas, sem direções cardinais novas ou portas artificiais nos vínculos comuns. A porta de serviço é somente um objeto físico da conexão oficial; não contém itens, chave, código ou condição de puzzle.

O recorte total possui **16 ligações bidirecionais / 32 arcos**. T02 tem exatamente seus nove vizinhos oficiais: T01, T03, T04, T08, T09, T11, T12, U01 e B07. Seus nomes são distinguíveis pelo resolvedor existente, inclusive ao esclarecer movimento cauteloso. A ligação direta T02/T05 continua ausente.

Bloqueios preservados em ambos os sentidos: **T02/T09, T02/B07 e T05/T12**. Os três usam estado compartilhado e porta bloqueada. Nenhum comando alternativo, direção local ou movimento cauteloso libera o acesso. Visitar os novos ambientes não altera os bloqueios. Não há evento de liberação implementado.

A configuração `prototype` mantém exatamente as seis salas originais, seus objetos, puzzles, inimigos e progressão. A expansão é aplicada somente à campanha, reutilizando a mesma fábrica e os sistemas existentes. Nenhum item foi redistribuído; nenhuma arma, documento, inimigo ou puzzle foi adicionado. A interface existente renderiza os 14 ambientes sem alteração de layout, menu ou arte.

### PLANEJADO

**E06 ↔ T07** permanece acesso de serviço inicialmente inacessível. **B03 ↔ T12** permanece a escada prevista para a futura saída do subterrâneo. E06 e B03 não existem em execução; não foram registrados arcos para esses destinos, salas fictícias ou teletransportes. Implementar essas ligações somente junto aos ambientes correspondentes. A rota E07 → B01 → B02 → B03 → T12 e a conexão secreta B10/L01 continuam no planejamento oficial.

Os demais **38 ambientes** seguem não implementados. Concluir a estrutura do térreo não significa concluir seu conteúdo ou a campanha.

### PENDENTE — somente etapas futuras

- Reorganização definitiva dos itens.
- Entrada de comandos uniforme em todos os objetos inspecionáveis, reservada à 5.1F.
- Desenvolvimento dos puzzles e condições de liberação.
- Organização de pastas/arquivos e eventuais renomeações, sem duplicar código.
- Remoção futura da opção Tutorial do menu do jogador, preservando os recursos técnicos de teste.
- Prólogo e queda para o subterrâneo.
- Validação dos estados provisórios das passagens comuns e definição do próximo recorte autorizado.

Não foram iniciadas essas atividades nem outra fase. Resultados de validação desta entrega registrados em CAMPAIGN_PROGRESS.md.


## 14. Fase 5.1E — conclusão estrutural do andar superior

### IMPLEMENTADO

Adicionados U02 — Quarto Principal; U03 — Quarto de Hóspedes; U04 — Quarto Infantil; U05 — Banheiro Superior; U06 — Estudo Privado; U07 — Depósito Superior; U08 — Varanda Superior; U09 — Sótão. São Rooms da fábrica existente, somente com descrições ambientais provisórias. Não receberam itens, inimigos, documentos, puzzles ou eventos. Joseph permanece o protagonista.

Implementadas exclusivamente as oito ligações oficiais: **U01 ↔ U02, U01 ↔ U03, U01 ↔ U04, U01 ↔ U08, U02 ↔ U06, U03 ↔ U05, U06 ↔ U07 e U07 ↔ U09**. Preservada T02 ↔ U01. O grafo parcial passa a **22 salas únicas e 24 ligações bidirecionais (48 arcos)**, sem saídas para ambientes ausentes ou novas conexões entre setores.

### Estados provisórios e integração de U01

As oito ligações estão disponíveis provisoriamente para exploração e validação, porque a fonte não fixa seus estados iniciais. Não são condições definitivas nem eventos de desbloqueio. Usam nomes locais e chaves `via_uXX`, sem orientações cardinais inventadas. U07/U09 é uma passagem nomeada ao sótão; a solução física definitiva desse acesso permanece pendente, sem criar alçapão ou mecanismo.

A instância existente de **porta de quarto** foi integrada a **U01/U02**, aberta e destrancada inicialmente apenas na configuração de campanha. É a mesma porta nas duas salas, com fechamento/abertura compartilhados e descrição coerente com o destino. A descrição de U01 deixou de afirmar que essa porta está trancada. Não foi criado quarto adicional nem chave. Seu nome físico antigo foi preservado; pedidos genéricos como “passar pela porta de quarto” podem exigir esclarecimento entre os quartos. “A do quarto principal” completa a intenção; o parser não foi alterado para escolher arbitrariamente.

Na configuração **prototype**, a porta conserva o texto, o bloqueio por fechadura e a ausência de destino originais; a demonstração continua com seis salas e progressão intacta. O teste antigo da porta de quarto trancada agora seleciona explicitamente essa configuração. Testes novos cobrem a representação oficial da campanha, fechamento e retorno.

Os bloqueios **T02/T09, T02/B07 e T05/T12** permanecem ativos nos dois sentidos, sem liberação por visita ou comando alternativo. Nenhum item legado foi redistribuído. U08 não recebeu salvamento, sinal de celular ou evento: o ponto de save permanece apenas planejado. A interface existente renderiza as 22 salas; não foi modificada.

### PLANEJADO / PENDENTE

Restam **30 ambientes** do mapa oficial. Mantêm-se E06/T07, B03/T12, prólogo/queda e entrada secreta como planejamento, sem novos arcos de execução. Pendentes: organização dos arquivos; renomeação sem duplicação de código; remoção futura do Tutorial do menu preservando testes técnicos; padronização da inspeção; distribuição definitiva dos itens; puzzles; desenvolvimento completo da narrativa; prólogo e queda para o subterrâneo; estados definitivos das passagens e solução física do acesso ao sótão.

Resultados reais de testes em CAMPAIGN_PROGRESS.md. **Nenhuma etapa posterior foi iniciada; Fase 5.1F não implementada.**


## 16. Fase 5.1F — apresentação de inspeção (IMPLEMENTADO)

A inspeção de um GameObject sem faces adicionais agora fornece sua descrição ao mesmo painel de leitura/inspeção existente, via metadado transitório `CommandParser.inspection_text` e `VisualSession`. Não exige alteração de Room, GameState, create_world ou cadastro de faces artificiais. Objetos especiais mantêm suas faces, acessibilidade, compartimentos e documentos. O contexto modal é validado no parser antes da execução física; não cria rota alternativa para acessar conteúdo bloqueado.

O mapa permanece com 22 salas na campanha e seis no protótipo. IDs, ligações, bloqueios, objetos e progressão não foram alterados. Esta seção atualiza apenas a decisão de apresentação; os registros anteriores da inspeção como pendente são históricos. Testes e pendências da 5.1F constam em CAMPAIGN_PROGRESS.md. Nenhuma fase seguinte foi iniciada.


## 17. Fase 5.1G — percepção e ações no mundo existente

**IMPLEMENTADO:** `ExplorationSystems` avalia sinais pelas conexões conhecidas existentes. Metadados opcionais: `GameObject.sight_gap`, `soundproof`, `sound_attenuation`; `Room.ambient_noise`; `Enemy.sound_intensity`, `in_sight`. Porta aberta ou fresta só permite observação com luz e linha de visão. Bloqueios oficiais, passagens desabilitadas/secretas e destinos ausentes interrompem a percepção e não viram atalhos. A única fresta explicitada na fábrica já constava da descrição da porta do porão do protótipo; bloqueio da campanha prevalece.

Ajuda oferece todos os caminhos reais disponíveis; orientação relativa exige referência local inequívoca. Fuga reutiliza movimento e respeita os mesmos bloqueios. Defesa e esquiva permanecem dentro de Confrontation, sem tela ou sistema paralelo.

**Preservado:** 22 ambientes da campanha, seis do protótipo, todas as conexões/IDs/objetos e bloqueios T02/T09, T02/B07, T05/T12. O catálogo oficial continua com 52 ambientes. Nenhuma distribuição ou narrativa de campanha foi acrescentada. Percentuais provisórios, regras sensoriais e validação detalhados em CAMPAIGN_PROGRESS.md.

A apresentação geral das criaturas e as mensagens de preparação de combate respeitam visibilidade e sinais atuais. Essa verificação não modifica textos de cenários nem enumera objetos; impede identificar ameaças no escuro ou por meio de pistas inexistentes. Um golpe efetivo continua sendo resolvido e comunicado mesmo sem identificar quem atacou.


## 18. Fase 5.1H — exterior da propriedade

### IMPLEMENTADO

Nove Rooms adicionadas exclusivamente à campanha: E01 — Estrada / Carro; E02 — Portão da Propriedade; E03 — Caminho Frontal; E04 — Varanda da Mansão; E05 — Lateral da Casa; E06 — Fundos da Propriedade; E07 — Casinha de Ferramentas; E08 — Estufa Abandonada; E09 — Área do Gerador Externo. Descrições provisórias situam o ano 2000, chuva, céu escurecendo, vegetação, abandono e isolamento, sem eventos ou recursos gráficos/sonoros novos.

Oito ligações internas bidirecionais, provisoriamente disponíveis: **E01/E02, E02/E03, E03/E04, E03/E05, E03/E08, E05/E06, E06/E07, E06/E09**. Usam chaves locais `via_eXX`, nomes naturais e os estados compartilhados já existentes. Não são atribuídas direções cardinais inventadas. O portão é descrito aberto e seu trajeto não possui chave, puzzle ou bloqueio. A fábrica continua única e o protótipo não recebe o exterior.

Adicionadas duas ligações intersetoriais, **ambas bloqueadas nos dois sentidos**:

- **E04/T01:** reutiliza exatamente a porta principal existente em T01. Na campanha, a porta permanece bloqueada e também é marcada trancada; o estado compartilhado C_E04_T01 fica desabilitado. A arquitetura atual compartilha o estado físico e não diferencia travamento por lado. Por segurança, o acesso interno também fica bloqueado até definição da campanha. Nenhum desbloqueio foi inventado. O objeto e o comportamento antigo do protótipo não foram modificados.
- **E06/T07:** porta da lavanderia como objeto de passagem não portátil, bloqueado, com estado C_E06_T07 desabilitado e compartilhado. É a estrutura de um atalho futuro; nenhum comando alternativo, fuga, cautela, abertura forçada ou acesso pelo lado oposto o libera.

Total do grafo executável: **31 salas, 34 ligações bidirecionais, 68 arcos**. Não há conexões adicionais por proximidade. Mantidos os bloqueios T02/T09, T02/B07 e T05/T12 e todos os IDs/conexões anteriores. O início continua em **entrance/T01**. Testes posicionam Joseph no exterior de forma controlada; não foi criado seletor de salas ou modificado o Tutorial.

### PLANEJADO / PENDENTE

- **E07 → B01:** nenhuma queda, arco de saída, sala B01 fictícia ou retorno foi criado. A implementação depende do porão inicial e da futura etapa narrativa. E07 tem apenas ligação com E06, sem dano, alteração de inventário, entrega da barra ou cutscene.
- **E03:** ponto de salvamento e sinal de celular apenas previstos. Não ativa sinal, eventos de save, slots ou interface.
- Definir o comportamento do lado interno da porta principal antes de liberar E04/T01; definir futuramente a condição do atalho da lavanderia. Validar os estados provisórios das oito passagens internas.
- **21 ambientes oficiais restantes**, prólogo, queda, distribuição de itens, puzzles, narrativa, arte/áudio finais e demais produções continuam pendentes. Catálogo oficial de 52 ambientes preservado.

A Fase 5.1H não conclui o prólogo. Sistemas da 5.1G, inspeção da 5.1F e interface foram reutilizados sem alterar seus módulos. Resultados reais de validação em CAMPAIGN_PROGRESS.md.


## 19. Fase 5.1H — revisão canônica vigente

Autoridade: pedido mais recente do usuário e `mapa externo - evolucys.png`. Substitui a entrega estrutural da seção 18 e a origem antiga E07 da queda, sem iniciar outra fase.

- Reaproveitados E01–E09. Novos IDs livres: E10 Jardim da Fonte, E11 Corredor do Jardim, E12 Pátio da Casinha, E13 Jardim da Estufa e do Poço. B01, B02 e B03, antes apenas planejados, são agora salas reais. B01 passa a Câmara sob a Estufa, preservando seu ID. Total: 38 salas implementadas de 56 planejadas.
- Início E01 (carro/pneu estragado) → norte E02 (caminho e portão aberto) → norte E03 (frente). E04 contém a porta principal trancada e a campainha. A resposta chega após 800 ms na interface, sem congelar o Tkinter; CLI aguarda o mesmo intervalo. Uma ação/turno, conclusão da espera sem turno adicional. Nenhuma resposta à campainha e orientação natural para os arredores.
- Lateral E03/E05/E11; fonte E11/E10; pátio E11/E12; casinha E12/E07; fundos E12/E06; gerador E06/E09; jardim E06/E13; estufa E13/E08. Doze ligações externas bidirecionais. Removidas E03/E08, E05/E06 e E06/E07 em favor dos percursos do esboço.
- Macaco coletável em E07, incompleto e inutilizável sem manivela; nenhum puzzle de conserto criado. Manivela sobre a mesa em E08, com aliases de barra de aço/ferro. Tentar pegá-la dispara uma única queda E08 → B01, mesmo com inventário cheio. Joseph cai antes da coleta; o item permanece estruturalmente em E08, inacessível após o desabamento. Recuperação futura pendente. Não se inventou dano de queda.
- B01 situa-se sob a estufa, com fragmentos do piso acima. B01/B02/B03/T12 permite continuar até o interior sem depender do complexo. Esses três vínculos estão provisoriamente livres. O arco de queda não é caminhada, fuga ou escada e não tem retorno.
- Poço em E13 ligado ao Túnel Antigo B02 por C_B02_E13. Sem luz adequada não revela o fundo. Lanterna possuída, equipada, acesa em modo normal revela escada e abertura (UV não basta). Porta/estado compartilhados: começa trancada, desconhecida e desabilitada; o trinco de B02 permite abrir por dentro, habilita e revela a rota. Conhecer nomes ou usar itens do lado externo não destranca. Para descer, a luz continua obrigatória mesmo após desbloquear. A lanterna existente em T01 permanece no mesmo local, alcançável pela rota subterrânea; não se acrescentou outra.
- E04/T01 e E06/T07 continuam bloqueados nos dois sentidos, aguardando condições definitivas. T02/T09, T02/B07, T05/T12 e o planejamento condicionado B10/L01 permanecem preservados. Protótipo, objetos e progressão de demonstração continuam isolados.
- Nenhum redesenho da interface: somente agendamento da resposta da campainha e bloqueio temporário da entrada durante a espera. Ajuda contextual e aliases acompanham os elementos locais, sem antecipar a solução.

Pendências: garagem/possível fuga aparecem no esboço como potencial, sem ambiente oficial anterior; ficam documentais, sem saída funcional inventada. Susto com animal é apenas possibilidade. Recuperação da manivela, uso completo do macaco, condições definitivas de portas, save/load completo dos estados/eventos, narrativa e recursos definitivos ficam para autorização futura. Flags desta etapa são de sessão, não novo sistema de salvamento. Organização de arquivos, renomeação, retirada do Tutorial, itens/puzzles definitivos e demais salas permanecem pendentes. Resultados reais em CAMPAIGN_PROGRESS.md.


## 20. Fase 5.1I — conclusão estrutural do porão principal

Acrescentados somente B04 Depósito Subterrâneo, B05 Sala da Caldeira, B06 Sala Elétrica, B08 Adega, B09 Oficina e B10 Câmara Fria. B07 Arquivo do Porão já existia como `cellar`: mesma instância por alias, conteúdo e descrição preservados. B01–B03 não foram recriados. Descrições novas ambientais, sem itens, inimigos, documentos ou puzzles novos.

**Contagem corrigida:** a meta textual de 45 pressupunha sete salas novas, mas B07 já estava entre as 38. Portanto 38 + 6 = **44 ambientes únicos**, sem inventar uma sala para completar a meta. São E13 + T12 + U9 + B10; restam L01–L12, total planejado de 56.

Sete conexões comuns bidirecionais adicionadas, provisoriamente disponíveis: B03/B04, B03/B05, B03/B09, B05/B06, B06/B07, B07/B08, B09/B10. Duas secundárias com porta e estado compartilhados, bloqueadas em ambos os sentidos: B04/B09 (porta de serviço) e B08/B10 (corredor de armazenamento). Nenhuma chave ou mecanismo de liberação criado. A definição mais recente torna B04/B09 inicialmente bloqueada, substituindo a ausência de condição explícita na fonte original.

Mantidos a queda E08 → B01 sem retorno/coleta, B01/B02/B03/T12, o poço condicionado E13/B02, a escadaria bloqueada B07/T02 e os demais bloqueios. Acesso alternativo a B07 pelo porão não libera sua escadaria para T02. Seu conteúdo legado continua presente; não houve redistribuição. Nomes das passagens resolvidos pelo parser existente, sem alteração desse sistema.

B10/L01 permanece exclusivamente documental e condicionado: nenhum destino fictício, saída executável ou mecanismo de abertura. Protótipo segue com seis salas e início original; campanha começa em E01. Nenhuma alteração de UI/HUD, arte, áudio ou mecânica. Validação e arquivos em CAMPAIGN_PROGRESS.md. Fase 5.1J não iniciada.


## 21. Fase 5.1J — laboratório e auditoria estrutural dos acessos

### Etapa A — implementado

L01 Acesso Oculto; L02 Corredor do Laboratório; L03 Recepção Técnica; L04 Sala de Observação; L05 Laboratório Principal; L06 Laboratório Biológico; L07 Enfermaria e Cirurgia; L08 Câmara de Contenção; L09 Biotério; L10 Controle de Energia; L11 Arquivo Científico; L12 Rota de Fuga. Os nomes atuais seguem o pedido 5.1J, preservando IDs e topologia original. Descrições somente ambientais; sem itens, inimigos, documentos, puzzles, sistemas científicos ou finais novos.

Treze conexões internas bidirecionais: L01/L02, L02/L03, L03/L04, L04/L05, L05/L06, L06/L09, L09/L11, L05/L07, L07/L08, L08/L11, L03/L10, L10/L05, L11/L12. Estados compartilhados; passagens comuns provisoriamente livres, pois o planejamento não define bloqueios internos específicos.

B10/L01 existe nos dois sentidos, com uma porta compartilhada trancada/bloqueada e estado desconhecido/desabilitado. Saber o nome, usar sinônimo ou revelar a ligação não a habilita. Nenhum mecanismo de liberação inventado. L12 só retorna a L11; não há saída externa, vitória ou fuga funcional. L03 e L11 continuam apenas pontos previstos de salvamento.

### Etapa B — validado

- 56 instâncias/IDs únicos: E13, T12, U9, B10, L12. Aliases legados continuam apontando para as mesmas salas. Grafo exato: 66 ligações, sendo 65 bidirecionais e a queda E08 → B01; 131 arcos, destinos existentes e nenhuma adjacência duplicada. Todos os setores conectados estruturalmente; não há sala isolada por erro.
- Estado inicial separado do grafo estrutural: a caminhada a partir de E01 alcança os 13 ambientes externos. A queda é evento, não saída caminhável. B01/B02/B03/T12 continua livre; o laboratório tem suas 12 salas conectadas internamente, mas não pode ser alcançado do exterior/porão sem liberação futura. Liberação da entrada testada somente em uma instância controlada; fábrica permanece bloqueada.
- Portas/estados compartilhados conferidos nos dois sentidos. Mantidos E04/T01, E06/T07, E13/B02, B07/T02, B04/B09, B08/B10, T02/T09, T05/T12 e B10/L01. Queda sem retorno; poço exige luz e destravamento interno; L11/L12 não encerra o jogo. Testes anteriores do prólogo, protótipo e renderização dos ambientes reaproveitados.
- Navegação local aceita nomes atuais e “sala de contenção” sem mudar o parser. Corrigida pontuação do nome local que impedia esse alias. Testes antigos de destinos inexistentes passam a usar L13/B11, pois L01–L12 agora existem. Nenhum bloqueio oficial relaxado.
- Limitação preexistente registrada: “sair pelo corredor” não é um comando de movimento suportado neste contexto; não move Joseph. “ir para o corredor do laboratório” funciona. Não foi ampliado o parser. “Voltar” sem destino só resolve quando a passagem local é inequívoca; ambiguidades permanecem sujeitas a esclarecimento.

Pendências: condições narrativas e mecanismos de desbloqueio, pontos de save/load, distribuição de conteúdo, puzzles, campanha completa e destino externo de L12. Nenhuma dessas funções foi implementada. Resultados reais e arquivos em CAMPAIGN_PROGRESS.md. Fase 5.2 e qualquer próxima etapa não iniciadas.


## 22. Fase 5.2 — prólogo e narrativa inicial

Refinamento da abertura existente, sem reconstrução de eventos/mapa. E01 apresenta Joseph como empresário adulto no ano 2000, pneu danificado, estrada deserta e tempestade se aproximando. E02/E03 tornam progressiva a aproximação da mansão abandonada. Descrições próprias de varanda, laterais, fundos, jardim/fonte, gerador, casinha e poço foram preservadas quando já adequadas. E08 recebeu vidro quebrado, ferrugem, vegetação sem controle, utensílios e piso deteriorado. B01 descreve pouca luz, poeira, silêncio e umidade sem repetir a reação física da queda em revisitas.

Interações locais: pneu/roda e mansão em E01; fachada/mansão em E03/E04; estufa em E08/E13. São alvos ambientais não coletáveis, sem novos recursos de inventário. Carro não revela objetos inexistentes. Macaco continua em E07, incompleto, coletável e inutilizável sem manivela. Comentários usam identificação Joseph e narração separada.

Manivela em E08 tem descrição neutra. Somente após examinar o macaco (`campaign.jack` no conjunto `investigated` existente), a inspeção acrescenta a suspeita de encaixe. Nem a descrição geral da estufa nem a ajuda antecipam sua função. Examinar mesa, estufa, manivela ou entrar não dispara queda. Ajuda considera inspeção, campainha e queda sem DICA automática ou revelação do laboratório.

Campainha: primeira tentativa mantém som, chamado de Joseph e espera de 800 ms; conclusão informa ausência de resposta e intenção de procurar ajuda. Tentativas seguintes usam texto curto e a mesma espera, sem repetir o diálogo inteiro. Reutilizado `doorbell_rung`, sem desbloquear a porta ou criar eventos paralelos.

Queda: mesma condição/evento `greenhouse_fall`, apenas ao tentar pegar a manivela, inclusive com inventário cheio. Aproximação, rangido, ruptura, queda antes da coleta, dor/desorientação e decisão de buscar saída são narrados uma vez. Destino B01; sem dano numérico novo, sem retorno pelo buraco, sem item no inventário. Peça segue inacessível sobre a mesa para desenvolvimento futuro. Rota B01/B02/B03/T12 e regras do poço preservadas integralmente.

Aliases pontuais: `caminhar até o portão` resolve somente uma passagem local conhecida com esse nome; `coletar` e `alcançar` (também sem acento) só são normalizados para pegar quando o alvo local é a manivela/evento. `pegar`, `apanhar`, `recolher` e nomes da barra reutilizam a mesma lógica existente. Nenhuma ampliação genérica do parser.

Pendências: conserto do carro, recuperação futura da peça, salvamento completo, narrativa posterior, puzzles, arte/áudio e fuga permanecem fora do escopo. Nenhum requisito novo de ordem de visita, campainha ou coleta do macaco foi imposto para chegar à estufa. Fase 5.3 não iniciada.


## Correção pontual — lanterna inicial e poço (referência Fase 5.3)

A campanha começa em E01 com a lanterna funcional no inventário, ocupando um dos seis espaços. A mesma instância antes disponível em T01 é transferida na inicialização; não existe outra lanterna para coletar na mansão. Começa guardada e apagada; os comandos existentes de equipar e ligar fornecem a iluminação adequada. Protótipo preserva sua lanterna original na sala; cenários do Tutorial não herdam o equipamento da campanha.

Poço E13/B02 sem alteração de mecânica: luz normal, acesa e equipada revela escada e acesso; a passagem começa trancada e só é destrancada em B02. Usar itens ou tentar abrir/forçar do exterior não libera o acesso. Depois da abertura interna, a descida continua exigindo iluminação. A referência anterior à obtenção posterior da lanterna em T01 está substituída por esta correção.

Escopo limitado à correção expressa do usuário. Distribuição de equipamentos, documentos, inimigos e demais progressões do anexo amplo da Fase 5.3 não foram implementadas nesta correção.


## 23. Fase 5.3A — garagem e correções estruturais

G01 Garagem acrescentada sem renumerar salas: 57 ambientes únicos. T03/oeste ↔ G01/leste, porta da garagem aberta, livre de chave/energia, mesmo estado e objeto nos dois lados. Nomes locais permitem entrar/ir para garagem, passar pela porta da garagem, ir esquerda/oeste e voltar à sala de estar. Nenhuma conexão antiga removida; protótipo não recebe G01.

Dois carros antigos não funcionais, compartimento traseiro do primeiro carro, bancada/armários e ferramentas/peças ambientais usam a inspeção uniforme. Nada coletável adicionado. A roda compatível fica **planejada no compartimento do carro antigo 1**, sem objeto portátil, concessão, retirada/transporte/instalação ou revelação de segredo na interface. O compartimento é examinável, sem puzzle.

As duas grandes portas externas são representadas conjuntamente pelo objeto interativo `portões externos` (G01.external_gates), inicialmente trancado e bloqueado por contenção. Não há saída externa cadastrada, pois seu destino ainda precisa ser definido. Nem sinônimos nem abertura hipotética do objeto criam rota de fuga. Uma futura liberação requer evento narrativo autorizado e definição de destino. A restauração de energia principal ainda não existe nesta base: não foi implementada nem ligada aos portões; quando existir, não deverá desbloqueá-los automaticamente. Porta interna independe dela.

Funções futuras preservadas: **Sobrevivente** — após os eventos finais, Joseph obtém a roda compatível e posteriormente conserta o carro na estrada; **A Última Vítima** — tentativa de fuga pela garagem é interceptada por Daniel. Somente planejamento, sem perseguição, combate, vitória, morte ou final novo.

Pendências: destino externo, liberação narrativa da contenção, integração futura com energia, obtenção da roda e recuperação da manivela, conserto e finais. Resultados em CAMPAIGN_PROGRESS.md. Nenhuma fase posterior iniciada.


## Correção oficial Fase 5.3 — gerador principal e contenção do poço

Gerador principal e quadro elétrico em **B06**, acessível pelo percurso interno T12 → B03 → B05 → B06. Fusíveis únicos coletáveis em **U07**, respeitando os seis espaços (inventário cheio preserva o item no depósito). E09 permanece equipamento auxiliar abandonado, sem função na progressão elétrica. Nenhuma sala ou conexão nova; 57 ambientes e 133 arcos preservados.

Sequência jogável: examinar quadro elétrico em B06; coletar fusíveis em U07; retornar e `instalar fusíveis` (também `usar fusíveis no quadro elétrico`); `ligar gerador`/`usar gerador principal`/`restaurar energia`. Instalação consome os fusíveis do inventário uma única vez e registra `fuses_installed`; acionamento registra `power_restored`. Aliases de instalação/acionamento limitados a B06. Registros usam `world_events` existente, sem subsistema novo. Energia não desativa contenção nem altera portas indiscriminadamente.

Poço: `abrir acesso do poço` em B02 exige agora `containment_disabled`. Estado inicial mantém contenção ativa (evento ausente), inclusive após restauração elétrica. Somente depois desse evento a abertura interna habilita a passagem compartilhada. Exterior continua incapaz de destrancar, mesmo após a contenção desativada. Iluminação normal equipada/acesa e demais regras anteriores preservadas; lanterna inicial mantida.

**Limitação real da base:** antes desta correção não existiam implementação de energia nem evento jogável de desativação da contenção. A sequência elétrica mínima foi acrescentada com os estados existentes. A lista de acessos internos a liberar e a ação narrativa que desativa contenção não foram definidas: permanecem pendentes, sem liberação inventada. Portanto o poço não pode ser desbloqueado numa sessão normal até essa integração futura. Testes simulam `containment_disabled` exclusivamente em instâncias isoladas. Portões de G01 e saídas externas permanecem bloqueados. Esta seção substitui a liberação incondicional anterior por B02 e a antiga indicação do gerador principal em E09.


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


## Fase 5.3B — frente externa da garagem

E14 Frente da Garagem acrescentado sem renumeração: duas grandes portas, paredes deterioradas, calçamento invadido pelo mato, ferrugem e ausência de atividade. Relação física à esquerda da fachada principal. E03/oeste ↔ E14/leste é caminho livre; E14/via_g01 ↔ G01/via_e14 usa o **mesmo objeto G01.external_gates** e o mesmo PassageState C_E14_G01, inicialmente desabilitado, trancado e bloqueado.

A conexão estrutural entre os portões e o exterior, antes pendente na 5.3A, está resolvida. Sua liberação narrativa continua pendente: energia não habilita o estado nem abre os portões; não há desativação de contenção ou fuga nova. Abrir hipoteticamente só o objeto não habilita o estado de passagem. T03/G01 continua aberto. Nenhum conteúdo interno duplicado; o texto compartilhado dos portões passa a mencionar travas pesadas, sem antecipar contenção biológica.

Comandos em E03: `ir para a garagem`, `ir até a frente da garagem`, `seguir para os portões` levam a E14. Conforme pedido, o alias estritamente local `examinar a garagem` também aproxima Joseph em E03; em E14 é inspeção normal. Inspeções de garagem/fachada e portões usam o sistema existente. `voltar ao caminho frontal` retorna a E03. Nomes de passagens continuam resolvidos localmente, sem teletransporte para G01.

58 salas únicas, seis no protótipo, 69 ligações/137 arcos. Preservados lanterna, queda, poço condicionado, gerador/fusíveis, itens e bloqueios anteriores. Pendentes somente os eventos futuros de liberação, roda, recuperação da manivela, conserto e finais. Fase 5.4 não iniciada. Resultados em CAMPAIGN_PROGRESS.md.
