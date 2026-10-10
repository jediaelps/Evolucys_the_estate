Versão atual: **Fase 4.5.5** — [ajuda contextual e narração](FASE4_5_5.md). Layout preservado; destaque discreto dos verbos de ajuda.

Base anterior: **Fase 4.5.4** — [falas identificadas e memória contextual](FASE4_5_4.md). Layout preservado.

Base visual: **Fase 4.5.3** — [proporções, HUD e testes](FASE4_5_3.md).

Ajuste visual anterior: consulte [AJUSTE_INTERFACE_4_5_2.md](AJUSTE_INTERFACE_4_5_2.md). Histórico compacto à esquerda, objetivo à direita e dicas no histórico.

# Fase 4.5.5 — exploração e investigação visual integrada

O visual mostra o que Joseph vê. Você observa, pensa e escreve o que ele fará.

## Iniciar

Extraia os arquivos na mesma pasta e execute:

```sh
python visual.py
```

Requer Python 3.8+ com Tkinter/Tk 8.6 e uma sessão gráfica. Não há dependências de pip. No Python para Windows, mantenha **tcl/tk and IDLE** no instalador. Verifique com `python -m tkinter`. Algumas distribuições Linux fornecem o pacote separado `python3-tk`.

O terminal permanece disponível: `python main.py`.

## Como jogar

Digite na caixa abaixo do histórico e pressione **Enter**. A entrada é limpa, o foco permanece nela e o cenário/HUD/inventário são atualizados após a execução.

Exemplos:

```text
olhar
olhar em volta
examinar lanterna
pegar lanterna
equipar lanterna
usar lanterna
ir norte
inventário
status
ajuda
```

`olhar em volta` descreve o cômodo atual e lista todos os objetos atualmente visíveis, saídas e inimigos presentes, em toda a campanha e nos quatro cenários do Tutorial. A lista acompanha itens coletados, largados e revelados. Não revela conteúdos ainda escondidos ou dentro de recipientes fechados. Tem o mesmo custo de ação de `olhar`, inclusive a reação inimiga durante confronto.

WASD, E, F e R não são atalhos de gameplay: são letras comuns durante a digitação. Clicar no cenário não executa ações. A exceção da Fase 4.3 é o inventário: clique num slot para consultar e depois em Examinar item, Equipar item, Usar item ou Largar item para agir pelo parser. Os comandos escritos continuam disponíveis.

O mouse funciona em menus, inventário, Opções, pausa, leitura, histórico, entrada e controles administrativos. **ESC** fecha primeiro a janela auxiliar ativa; na cena, abre/fecha a pausa. Não consome ação. Para encerrar a sessão, use a pausa e o botão de menu principal.

## Histórico e HUD

O histórico guarda no máximo **quatro pares de comando/resposta**. Uma quinta interação remove a mais antiga. As mensagens não somem por cronômetro. Respostas longas podem ser lidas pela barra de rolagem dentro dessa região curta. Linhas vazias não consomem ação nem substituem o histórico. Reset, troca de cenário e nova sessão limpam o histórico; pausa o preserva.

Ações administrativas aparecem como `[TESTE]`, separadas semanticamente das ações de Joseph, e não consomem turno.

O HUD mostra o objetivo atual, um único slot MÃO, munição quando aplicável e luz. Os dois raios de foco permanecem visíveis: cargas disponíveis em dourado e espaços vazios em cinza. O pequeno celular indica sinal/vibração; o coração indica vida e muda de cor com dano ou estado crítico. O traço de pulso muda de cor com confronto ou medo alto. São indicadores visuais de estado, sem animação ou áudio. Consultar o HUD não executa `checar celular`: escreva o comando quando quiser essa interação.

O cenário permanece em primeira pessoa. Joseph só é desenhado no inventário, nunca no cenário. Os nomes discretos identificam objetos provisórios sem revelar itens escondidos. Ao pegar um objeto, sua forma desaparece; ao mover, muda o cômodo; a luz altera a claridade; o vigia mostra preparação de golpe ou queda.

## Tutorial: quatro cenários independentes

No menu, clique em **Tutorial / Área de Testes** e no cenário desejado. As ações de Joseph também são escritas aqui.

### 1 — Exploração

```text
olhar
examinar mesa de teste
pegar mesa de teste
usar lanterna
pegar lanterna
equipar lanterna
usar lanterna
abrir caixa
examinar bilhete de teste
abrir porta de teste
ir norte
ir sul
```

A mesa permanece no ambiente; a lanterna sai do cenário quando coletada. O conteúdo da caixa aparece só depois de aberta.

### 2 — Inventário e sobrevivência

Digite `pegar bandagem` e `usar bandagem` com vida cheia: o item é preservado. Clique no controle administrativo **−25 vida** e escreva `usar bandagem`: a vida sobe de 75 para 95.

Pegue spray de cura, kit médico, chá e energético e use-os pelo inventário. Ajuste medo com os botões +25/-25 medo. Para a arma:

```text
pegar pistola
pegar munição de pistola
equipar pistola
recarregar pistola
```

**Esvaziar arma** e **Repor munição** são controles exclusivos de teste. Depois de esvaziar, escreva `recarregar pistola` para validar a recarga real. Pegue mais recursos para testar o limite de seis espaços e escreva `largar ITEM` para liberar espaço.

### 3 — Puzzle

Escreva `olhar`, examine o quadro e os objetos que forem revelados. Selecione suas próprias ações por texto; não há menu de soluções. O código usa a sintaxe `digitar CÓDIGO no cofre de teste`. Depois de encontrar uma chave, use `usar chave de teste na porta de teste`. A sala seguinte possui um registro que confirma a conclusão.

### 4 — Confronto

Na sala inicial:

```text
pegar pistola
pegar bandagem
ir norte
esperar
equipar pistola
atacar vigia
usar bandagem
fugir sul
```

Observe a postura do inimigo, vida e histórico. Equipar e curar consomem ações e permitem reação. O vigia tem 120 de resistência para prolongar o teste. Somente neste cenário, dano fatal restaura a vida para 25, impede Game Over e registra o aviso de proteção.

Para evitar combate, entre com `esgueirar norte`, mantendo a lanterna apagada; examine e retorne com `esgueirar sul`. A campanha mantém morte e recursos limitados normalmente.

## Controles administrativos

Os botões TESTE ajustam vida/medo, repõem recursos e munição ou esvaziam a arma. Eles não são ações de gameplay e nunca aparecem na campanha.

**Reset** restaura o cenário inteiro: objetos, inventário, munição, inimigo, vida, medo, histórico e progresso. Também está disponível em ESC → Reiniciar cenário. ESC → Escolher outro cenário descarta o teste atual.

## Arquitetura e preservação

`visual.py` mantém as cenas Tkinter da Fase 4, agora sem callbacks de ações por clique ou atalhos de letras.

**Entry + Enter → VisualSession.execute → CommandParser → GameState → refresh visual.**

`visual_session.py` mantém o adaptador e o histórico. `inventory_view.py` usa inventory_action para encaminhar os botões ao parser. item_details produz informações e disponibilidade dos botões, sem aplicar efeitos. Não existe segunda lógica de dano, cura ou consumo. O Tutorial continua isolado.

Não há save/load. **Continuar** permanece desabilitado; **Retomar sessão** na pausa preserva a partida em memória.

## Testes

```sh
python -B -m unittest
python -B visual_smoke.py
```

São **242 testes**, com os 206 cenários anteriores e 36 novos. As expectativas antigas de consumo direto e energético temporário foram adaptadas às novas regras explícitas; consulte FASE4_5_2.md. Quarenta e cinco usam eventos e widgets Tk reais, incluindo painel integrado, foco, bloqueio de comandos, redimensionamento e escadaria. Sem Tk/display, os testes gráficos são explicitamente ignorados; `visual_smoke.py` termina com aviso/erro nessa condição para não alegar validação gráfica.

## Inventário da Fase 4.3

Abra com `inventário`, `inventario` ou `abrir inventário`. A janela possui Joseph e sua condição física à esquerda, seis slots em duas colunas e três linhas no centro, e descrição/ações à direita. Ícones e silhueta são provisórios. O destaque indica seleção e a marca NA MÃO identifica equipamento.

Selecionar e consultar é gratuito: clicar numa bandagem não a consome. Os botões usam exatamente os comandos do parser. Examinar mantém o custo atual de `examinar ITEM` (um turno); equipar, usar e largar também permitem a reação inimiga. Ações indisponíveis ficam desabilitadas com uma explicação: cura com vida cheia, lanterna fora da mão ou descarte sobre um item homônimo, por exemplo. Armas são disparadas por `atacar`; munição é utilizada por `recarregar`, não pelo botão Usar item.

Feche pelo botão Fechar, ESC ou `fechar inventário` na entrada do painel. Não há X nem janela nativa separada para o inventário. Fechar não altera cômodo, itens nem vida. Durante a exploração, só o slot MÃO e os indicadores permanecem visíveis.

### Integração da Fase 4.3.1

O inventário usa um Frame filho da janela principal, centralizado por dimensões relativas. O cenário ao fundo é escurecido. Não é criado Tk ou Toplevel para o inventário; o painel reaproveita a sessão e o GameState atuais.

Ao abrir, o foco vai para a entrada de comandos do próprio painel e os cliques ficam restritos a ele. Comandos de exploração como `ir norte`, `olhar em volta`, `pegar ITEM`, `atacar` ou `fugir sul` são bloqueados antes do parser, sem turno, reação inimiga ou desgaste de buff. O aviso aparece no painel e no histórico.

Continuam disponíveis comandos para itens carregados, como `equipar pistola`, `usar bandagem`, `examinar lanterna`, `largar ITEM` e `recarregar`, além de ajuda, status e fechamento. Os botões usam as mesmas regras. Textos longos consultados no inventário ficam na sua área rolável. Abrir, fechar e selecionar são gratuitos; executar uma ação efetiva mantém o custo já existente.

ESC fecha o painel antes de abrir a pausa. O foco retorna à entrada principal. O cenário é reapresentado a partir do mesmo estado, sem restaurar objetos ou reiniciar o cômodo.

O painel acompanha o redimensionamento da janela principal. Descrição e resultados possuem rolagem para não empurrar os botões para fora. Validado no mínimo suportado de 1100 × 760 e em tamanhos maiores; mantém-se esse mínimo da aplicação.

Para validar manualmente: entre no Tutorial 2, pegue uma bandagem e uma lanterna, digite `inventário`, selecione a lanterna e equipe. Redimensione a janela e confirme que Fechar, os seis slots e ações continuam acessíveis. Tente `ir norte` na entrada do painel: deve ser bloqueado sem turno. Pressione ESC e confirme a volta ao mesmo cômodo e ao comando principal. No Tutorial 4, abra com um golpe preparado e equipe/use um item para observar exatamente a reação prevista pelo parser.

Teste no cenário 2: `pegar bandagem`, use o controle -25 vida, abra o inventário, selecione a bandagem e clique Usar item. Deve recuperar 20, remover a bandagem e atualizar a condição física. Em confronto, a reação inimiga pode causar dano logo após a cura. Selecione um item, observe que o turno não muda, depois use Equipar item para verificar que o turno avança.

## Escadaria e primeiro andar superior

Na campanha, partindo da entrada:

```text
ir norte
ajuda
subir as escadas
olhar em volta
examinar janela
examinar quadro
examinar porta de quarto
descer escada
```

Também funcionam `subir`, `subir escada`, `subir escadaria`, `ir para o andar de cima`, `ir andar superior`, `descer`, `descer escadaria` e `voltar ao salão`. Os comandos dependem das conexões locais, sem teletransporte. Bloqueios usam a mesma lógica das outras passagens.

O Corredor Superior possui janela, quadro, porta de quarto e escadaria de retorno. A porta do quarto está explicitamente trancada: o quarto ainda não foi construído. Essa fase adiciona somente o corredor, não o andar inteiro.

O fluxo completo de subir, examinar e descer foi validado na janela real, assim como seleção, cura, equipamento, descarte e fechamento do inventário. Os gráficos permanecem provisórios, com áudio provisório, sem save ou novos inimigos.

## Novidades da Fase 4.2

### Leitura e aliases

Objetos possuem conteúdo textual separado da descrição física. Use `ler bilhete`, `ler o bilhete de teste`, `examinar um bilhete` ou `olhar bilhete`. A leitura funciona no ambiente e no inventário. Objetos sem texto, ausentes ou visíveis mas inacessíveis dão respostas distintas.

Artigos a/o/uma/um são opcionais. Nomes abreviados são aceitos quando identificam um único objeto percebido: `porta` pode identificar `porta de teste`. Havendo duas correspondências, Joseph pede um nome mais específico. A resolução não consulta conteúdos escondidos e não usa rede ou IA externa.

Também são equivalentes `passar porta`, `passar pela porta`, `atravessar porta` e `entrar pela porta`. Usar itens aceita em/no/na: `usar a chave em uma porta`.

### Portas e ajuda

Passagens distinguem fechada, trancada, bloqueada e inacessível. Uma direção inexistente informa que não há caminho. Bloqueios físicos não são ignorados por uma chave ou código correto.

`ajuda` mostra possibilidades percebidas no local, considerando vida, medo, inventário, equipamento e confronto. Não revela conteúdos escondidos, códigos ou localização de soluções. O estado de uma fechadura só é tratado como conhecido após exame ou tentativa de interação.

Use `ajuda comandos` para a referência por categorias; `ajuda inventário`, `ajuda combate` e `ajuda celular` para assuntos; `ajuda porta`, `ajuda caixa` ou `ajuda bilhete` para objetos percebidos. Toda ajuda é gratuita e não avança reações ou buffs.

### Painel de leitura e HUD

`ler DOCUMENTO` e `ajuda comandos` abrem uma janela rolável não modal. Respostas acima de 500 caracteres também abrem esse painel; o histórico mostra uma prévia curta e conserva as quatro últimas interações. Feche com o botão Fechar leitura, X, ESC na janela auxiliar ou `fechar leitura` na entrada principal. Fechar é gratuito. Ler durante confronto consome uma ação e inclui a reação inimiga no resultado.

`hud_state.py` separa os dados de celular e coração da renderização: sinal, vibração, dano recente, estado crítico, perigo e frequência sugerida para uma futura animação. Não há save ou mensagens externas; os indicadores ainda não têm áudio próprio.

### Fluxo completo validado — Tutorial 1

Entre em Tutorial → 1 — Exploração e execute:

```text
olhar
examinar a mesa
pegar a lanterna
examinar caixa
abrir caixa
ler o bilhete
fechar leitura
passar pela porta
examinar porta
abrir porta
passar pela porta
entrar pela porta
```

O bilhete aparece ao abrir a caixa. A primeira tentativa de passagem informa que a porta está fechada. Abrir é a condição simples para liberá-la: não é preciso encontrar uma chave. Atravessar leva à sala adjacente e atravessar de novo retorna. Reset restaura objetos, porta, inventário, histórico e painéis. Esse fluxo foi testado por Enter na janela real, além dos testes do parser.

Aliases são regras locais, não compreensão irrestrita de linguagem natural. O estado bloqueada está preparado para condições futuras; não existe um comando universal para remover obstáculos. A arte permanece provisória.

## Limitações conhecidas

- Cenas fixas por cômodo, sem câmera livre ou movimento 3D.
- Formas e nomes provisórios para os objetos; sem arte final ou animação completa; áudio provisório disponível.
- Histórico mantém apenas quatro interações e não é salvo.
- Janela mínima de 1100 × 760 unidades Tk; escalas de sistema elevadas podem exigir ajuste.
- Sem save, instalador ou opções avançadas.
- Testado em Windows/Tk 8.6. Outras plataformas não foram verificadas.


## Novidades e validação da Fase 4.4

Consulte FASE4_4.md: documentos fixos e portáteis, páginas, chaves reutilizáveis, pistola de 12 tiros e eventos sonoros. Todos os painéis permanecem na janela principal.



## Fase 4.5

Consulte FASE4_5.md para inspeção de frente, verso e interior, leitura visual, PNGs e roteiro de validação. A organização dos recursos e exemplos de configuração estão em assets/README.md. O conteúdo integral dos documentos aparece no leitor ou inventário; o histórico conserva apenas a reação de Joseph.



## Fase 4.5.1

Leia FASE4_5_1.md para os novos sinônimos, dicas sem segredos e a demonstração Seleção de alvos — duas criaturas, no menu de tutorial.


## Fase 4.5.2

Consulte [FASE4_5_2.md](FASE4_5_2.md) para arquitetura, arquivos, testes e instruções das demonstrações Sustos e foco, Esconderijos e ronda e Luz e silêncio, disponíveis no menu Tutorial.
