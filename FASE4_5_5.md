# Fase 4.5.5 — narração, linguagem natural e ajuda contextual

## Antes → depois

- “Joseph atinge vigia, causando 35 de dano.” → “Joseph atinge vigia em cheio. Parece ferido.” A condição deriva da proporção de vida real; só é acrescentada ao ataque quando muda.
- “Vigia cai e deixa de ser uma ameaça.” → “Vigia cambaleia antes de cair imóvel.”
- Nome da sala + descrição + “Saídas: ...” → descrição narrativa, com transição ao atravessar. O nome continua no cenário visual.
- Inimigo de costas seguido de instruções de furtividade → descrição de seus movimentos e atenção, sem menu de ações.
- Erro com anúncio de ajuda → “Não foi possível entender essa ação.”, sem atribuir a falha do parser a Joseph.
- Ajuda geral em lista → pensamento curto, por exemplo: `Joseph: “Talvez eu possa DIGITAR a combinação no cofre.”`

## Parser

`action_context.py` interpreta movimento, destino e cautela antes dos aliases existentes. “Passar”, “seguir”, “entrar”, “ir” e “atravessar” aceitam nomes das passagens locais; “devagar”, “com cuidado”, “sem fazer barulho” e demais modificadores mantêm a intenção de esgueirar. Não há nova regra de movimento: o resultado segue para `move`, incluindo as verificações de porta, turno e reação existentes.

Uma única passagem compatível pode ser inferida. Havendo ambiguidade, a pergunta não gasta turno e retém a intenção: “a do porão” ou uma direção completa a resposta, preservando cautela. Outro comando de ação ou uma alteração relevante de contexto invalida a intenção pendente. Consultar ajuda pode preservá-la. O contexto de combate já existente permanece separado e seus testes de alvos continuam aprovados.

`usar chave` sem alvo também pode pedir “Em quê?” e aceitar o complemento. A escolha não consulta a chave correta nem revela a solução da fechadura. `Room.add_exit(..., name=...)` permite nomear passagens que não são portas, sem modificar mapas ou introduzir conexões de campanha.

## Ajuda e conhecimento

Pedidos como “me ajuda”, “estou perdido”, “o que eu faço?”, “alguma ideia?” e “e agora?” consultam a mesma ajuda gratuita.

A orientação usa elementos visíveis/acessíveis, pertences, ferimentos, tensão, ameaças visíveis, objetivo conhecido, memória sonora ainda compatível com o mundo, páginas efetivamente lidas e faces/objetos examinados. Não lê códigos privados de fechaduras como fonte de solução. Documentos guardados mas não lidos não oferecem pistas à ajuda.

Para um cofre: sem pista, Joseph sugere investigação; após ler um número relacionado, considera a conexão; após investigar o teclado, pode sugerir DIGITAR. Uma anotação examinada com algarismos também permite inferência cautelosa se existe um único teclado visível já investigado. Repetir ajuda, por si só, não libera informação. Não há dedução automática de código nem desbloqueio de puzzle.

Pedidos explícitos de `ajuda comandos` ainda abrem a referência existente. A ajuda padrão não abre um manual. Dicas de interface permanecem identificadas como DICA e mantêm seu controle de repetição.

## Apresentação

Uma tag `action_verb` no Text existente aplica cor discreta e negrito apenas ao verbo destacado dentro de uma fala identificada de Joseph. DIGITAR, EXAMINAR, OUVIR, ESCONDER e as demais ações sugeridas usam a mesma apresentação. O restante da frase, narração e dicas não recebe esse destaque.

Nenhuma dimensão ou posição do layout foi alterada. Histórico continua cronológico e ancorado embaixo. HUD e inventário permanecem como estavam.

## Arquivos

Criados: `action_context.py`, `test_phase455.py` e este relatório.

Modificados: `command_parser.py`, `context_help.py`, `feedback.py`, `game_state.py`, `confrontation.py`, `world.py`, `visual.py`; testes `test_look_around.py`, `test_ux.py`, `test_survival.py`, `test_phase452.py`, `test_phase454.py`; `README.md` e `GUI_README.md`.

As expectativas antigas de nomes isolados, listas de saídas e anúncio de ajuda foram atualizadas por corresponderem justamente à apresentação removida neste pedido. O estado de investigação adicional é de sessão; o projeto continua sem save/load completo.

## Validação direcionada

Execuções na pasta do projeto:

```sh
python -B -m unittest test_phase455 test_phase454.NarrativeTests test_confrontation -q
python -B -m unittest test_phase455 -q
python -B -m unittest test_look_around test_ux test_phase451.NaturalLanguageTests test_phase455 -q
python -B -m unittest test_phase455.HelpTests test_phase455.HelpInterfaceTests -q
```

Resultados em cada etapa: **40**, **18**, **74** e **9** testes aprovados, com sobreposição. Ao todo foram **100 testes distintos**, incluindo **20 novos**. Não foi executada a suíte completa.

Cobertura inclui dano de arma, munição e vida calculados sem números na narração; derrota; condições do inimigo; ambiente; cautela; portas fechadas; ambiguidade; continuação com direção ou nome; chave sem alvo; falha neutra; ajuda gratuita/progressiva/sem spoilers; memória de ameaças; interação com pistas; destaque de DIGITAR e outros verbos; ancoragem e geometria preservadas em 1100×760.

Dano, HP, munição e os demais cálculos continuam internos. Nenhuma mecânica fora do escopo foi intencionalmente alterada. A versão é **Fase 4.5.5**; a **Fase 5 não foi iniciada**.
