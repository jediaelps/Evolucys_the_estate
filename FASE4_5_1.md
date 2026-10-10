# Evolucys: The Estate — Fase 4.5.1

Execute `python visual.py` após extrair o ZIP. Python 3.8+ com Tkinter, sem instalação de pacotes e sem acesso à internet. A campanha, os quatro cenários anteriores, o inventário, documentos e inspeção continuam disponíveis.

## Validação automatizada

- `python -B -m unittest discover -v`: **206 testes**, sendo os **163 anteriores preservados** e **43 novos**.
- `python -B visual_smoke.py`: **42 testes gráficos**, incluindo os 39 anteriores e três novos. Esses testes também fazem parte do total de 206.

A cobertura nova verifica variações de observação, artigos, preposições, coleta, movimento, uso, ataques, dicas, serialização, proteção de segredos, identidade de inimigos, posição/distância, ambiguidade e continuação, arma específica, alcance, pé de cabra preservado e integração da interface.

## Tutorial contextual

Uma orientação curta aparece quando a situação permite ensinar algo. Não existe uma nova tela longa de instruções. Observação, coleta e movimento são ensinados com oportunidades visíveis; inventário, leitura e inspeção têm orientações dentro dos painéis correspondentes. Perigo, ataque e escolha de alvo só aparecem quando há criaturas presentes; múltiplos alvos só são ensinados quando existem pelo menos dois.

Cada tópico entra no conjunto `game.guide.presented` ao ser apresentado. Redimensionar ou atualizar a tela não reapresenta orientações. A próxima interação atualiza a dica, sem repetir tópicos apresentados. `TutorialGuide.to_dict()` e `from_dict()` permitem integrar esse conjunto a um futuro save. Não foi criado save definitivo. Uma nova campanha ou um cenário reiniciado começa com um novo conjunto.

A inspeção não sugere olhar atrás, virar um objeto específico ou procurar inscrições. Dicas não consultam conteúdos ocultos, códigos nem itens necessários para fechaduras. A ajuda completa permanece acessível.

## Exemplos de linguagem

- Observação: `ver gaveta`, `ver a gaveta`, `olhar para a gaveta`, `observar gaveta`, `examinar a gaveta`, `inspecionar gaveta`, `dar uma olhada na gaveta`.
- Coleta: `pegar a chave`, `apanhar chave`, `recolher a chave`.
- Uso: `usar` e `utilizar`, com artigos e alvo quando pertinente.
- Movimento: `ir`, `seguir`, `andar`, `entrar`, direções com preposições e nomes exatos dos cômodos adjacentes; subir/descer continuam disponíveis.
- Combate: `atacar`, `bater`, `golpear`, `acertar`, `atirar`, `disparar`, além de `usar pistola no alvo` e `usar pé de cabra no alvo`.

Na campanha, vá ao norte e diga **`ver gaveta`**: Joseph abre a inspeção frontal da gaveta. Feche com ESC para continuar. Isso não abre nem destranca o móvel.

Intenção óbvia: com o pé de cabra equipado, `usar pé de cabra no zumbi da esquerda` executa um ataque de 25 pontos; a ferramenta permanece no inventário. Usar munição na pistola equipada recarrega sem exigir outro verbo.

Reformulação: com a pistola equipada, `bater no zumbi da esquerda com a pistola` recebe **“Melhor atirar com essa arma. Não é uma boa escolha para bater.”** Não dispara nem causa dano. `usar bandagem no zumbi` explica que ela serve para cuidar de Joseph e preserva a bandagem. Tentativas físicas continuam permitindo a reação prevista; uma pergunta de esclarecimento não executa a ação.

## Duas criaturas iguais

No menu Tutorial / Área de Testes, escolha **Seleção de alvos — duas criaturas**. Essa demonstração é separada da campanha e não substitui o confronto anterior. Antes de ir ao norte:

```text
recolher pistola
recolher munição de pistola
recolher pé de cabra
equipar pistola
recarregar
seguir norte
```

Há dois zumbis provisórios: o da esquerda está próximo e o da direita está distante. As legendas apresentam posição, distância e característica visível. As coordenadas horizontais usadas para resolver os comandos são as mesmas usadas para desenhá-los. Distância controla a altura e a escala da apresentação.

Experimente em sessões reiniciadas quando necessário:

```text
atirar no zumbi da esquerda
usar pistola no zumbi da direita
atacar o mais próximo
atirar no mais distante
atacar o segundo
atirar no de camisa clara
```

Para ambiguidade:

```text
atacar zumbi
o da direita
```

Joseph pergunta qual deles antes de agir. Também aceita `o da esquerda`, `o mais próximo`, `o mais distante` e `o segundo`. A intenção e a arma são preservadas apenas para essa escolha. Uma nova ação, mudança de sala, turno, inimigos ou posições invalida a continuação. Ela permanece limitada aos candidatos da pergunta original.

Para alcance:

```text
equipar pé de cabra
bater no zumbi distante com o pé de cabra
```

Joseph responde que está longe demais, sem atingir o inimigo. Armas de fogo alcançam as três faixas. Indicar uma arma que ainda não está equipada solicita colocá-la na mão primeiro, preservando o custo já existente de trocar equipamento. Armas não são equipadas silenciosamente e duas ações não são combinadas gratuitamente.

## Arquivos

Criados: `combat_language.py`, `target_selection.py`, `contextual_tutorial.py`, `test_phase451.py`, `FASE4_5_1.md`.

Modificados: `command_language.py`, `command_parser.py`, `confrontation.py`, `game_state.py`, `world.py`, `visual_assets.py`, `visual_session.py`, `visual.py`, `document_view.py`, `inventory_view.py`, `context_help.py`, `tutorial.py`, `visual_smoke.py`, `README.md`, `GUI_README.md`, `assets/README.md`.

## Limitações e compatibilidade

O vocabulário é extensível por tabelas e regras locais; não é um modelo de linguagem e ainda não compreende qualquer frase portuguesa. Granadas não foram acrescentadas: o exemplo do pedido orientou a interpretação contextual dos itens existentes. A memória curta de esclarecimento cobre ataques. Não foram adicionadas soluções automáticas para puzzles, campanha definitiva, mapa, arte final, novas espécies definitivas, cutscenes ou save.

O confronto mantém uma reação inimiga por ação. Com vários inimigos, os inimigos vivos alternam essa oportunidade de modo determinístico. Inimigos médios/distantes ainda observam de longe e não avançam automaticamente; a aproximação e o balanceamento definitivo ficam para uma fase posterior. O encontro único anterior mantém seu comportamento. Pode-se fugir pela saída aberta ao sul.

Os estados e identificadores internos não aparecem nas respostas. O nome repetido “Vigia vigia” foi removido. Posições, distâncias e características exibidas são informações perceptíveis ao jogador. Os controles de treino anteriores continuam limitados à área de testes. O botão Reiniciar cenário dessa demonstração retorna ao confronto individual original; para repetir a dupla, escolha novamente a demonstração no menu.
