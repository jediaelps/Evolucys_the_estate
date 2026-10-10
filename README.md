Versão atual: **Fase 4.5.5** — [narração, linguagem natural e ajuda contextual](FASE4_5_5.md).

Base anterior: **Fase 4.5.4** — [diálogos e memória contextual](FASE4_5_4.md).

Layout preservado da **Fase 4.5.3**. Consulte [FASE4_5_3.md](FASE4_5_3.md) para o ajuste visual final e sua validação.

Base de sistemas: [Fase 4.5.2](FASE4_5_2.md) — foco, confiança, exploração cautelosa, esconderijos, rondas e iluminação.

Consulte [FASE4_5.md](FASE4_5.md) para inspeção visual, documentos sem duplicação no histórico e recursos PNG offline.

# EVOLUCYS: THE ESTATE

**Fase 4.5.5:** execute `python visual.py` para jogar por comandos + Enter. O inventário é um painel integrado sobre o cenário escurecido, sem janela externa: Joseph frontal provisório, seis slots e descrição com ações pelo mouse. Abra com `inventário` e feche com ESC, Fechar ou `fechar inventário`. Enquanto aberto, a exploração fica bloqueada; ações de itens continuam pelo mesmo parser e respeitam turnos. A escadaria e o terminal permanecem disponíveis. Consulte `GUI_README.md`.

Jogo de exploração textual em português, sem dependências externas. Requer Python 3.8 ou superior.

## Executar

Abra um terminal nesta pasta e execute:

```sh
python main.py
```

Digite `ajuda` para consultar os comandos e `sair` para encerrar. O progresso existe apenas durante a sessão; ainda não há salvamento. O menu de continuar após morrer reinicia a partida.

## Organização

- `world.py`: cômodos, objetos, conteúdos escondidos e portas compartilhadas entre passagens.
- `game_state.py`: Joseph, vida, medo, celular, inventário de seis espaços e item equipado.
- `command_parser.py`: comandos e regras de interação.
- `confrontation.py`: inimigos, ações de confronto e resolução de uma reação por turno.
- `main.py`: interface de terminal e reinício.
- `test_game.py`: testes de integração e regressão.
- `test_confrontation.py`: turnos, combate, furtividade, fuga e regressão do percurso pacífico.
- `items.py`: balanceamento, estado de armas e perfil de medo.
- `survival.py`: cura, chá, energético, lanterna e recarga.
- `feedback.py`: pensamentos contextuais reutilizáveis.
- `test_survival.py`: regressões da Fase 3.

## Fase 3 — sobrevivência

Vida e medo permanecem entre 0 e 100. A bandagem cura 20, o spray de cura 50 e o kit médico até 100; curas não ultrapassam a vida máxima. Com vida cheia, Joseph preserva o item e pensa “Não preciso disso agora.” A tentativa ainda custa uma ação. Há duas bandagens acessíveis, um spray guardado no armário e um kit protegido em uma caixa no porão. Estes recursos são finitos.

Consumíveis pessoais são usados dentro do inventário. Fora dele, Joseph recomenda abrir o inventário, sem consumir o item ou um turno. O chá reduz o medo em 30. O energético concede duas cargas persistentes de foco: cada carga impede uma perda de ação provocada por surpresa. Perceber sons e passar turnos não gastam cargas. O foco não reduz dano, não aumenta ataque e não elimina o medo. Não acumula nem renova cargas enquanto houver alguma ativa. A defesa reduz o golpe normal de 16 para 8, independentemente do foco.

A pistola fica no cofre e tem capacidade para 12 tiros, começa com dois e causa 35 de dano. Uma caixa de três cartuchos está no armário. `equipar pistola`, `atacar` e `recarregar` são ações distintas. A recarga transfere apenas o necessário; sobras permanecem na caixa e a caixa vazia sai do inventário. Arma vazia não dispara nem vira automaticamente um ataque corpo a corpo, mas a tentativa permite reação inimiga. Largar e recuperar a arma preserva a munição. Não existem munição infinita ou reaparecimento de recursos.

Com medo a partir de 70, o dano da pistola cai em 5: uma penalidade determinística de controle, sem chance aleatória de perder um cartucho. Respiração, batimentos e percepção são expostos como dados para a futura interface; esses efeitos ainda não têm áudio próprio. Os valores estão centralizados em `items.py`.

Use `ligar lanterna`, `desligar lanterna` ou `usar lanterna` para alternar seu estado, com ela equipada. `usar lanterna no vigia` permite a distração da Fase 2. Uma lanterna acesa, mesmo carregada sem estar equipada ou largada no cômodo, pode denunciar Joseph a um inimigo sensível à luz. Desligue-a antes de uma entrada furtiva. A fuga continua garantida por uma saída aberta, e o puzzle continua solucionável sem combate.

O inventário mantém seis espaços: arma e caixa de munição ocupam um espaço cada. Nesta fase, não há pilhas de itens com o mesmo nome; uma segunda bandagem pode ser coletada após consumir ou largar a primeira em outro cômodo. O jogo impede largar um item sobre outro homônimo para não apagar recursos do cenário.

`GameState.snapshot()` fornece cópias do estado para HUD, inventário, munição, celular, luz, medo e confronto, sem depender da interface. Os pensamentos são textos reutilizáveis; a interface Tkinter atual é iniciada por `visual.py`.

## Teste manual da Fase 3

Inicie com `python main.py`. Na entrada, experimente:

```text
usar lanterna
pegar lanterna
usar lanterna
equipar lanterna
ligar lanterna
desligar lanterna
pegar bandagem
usar bandagem
status
```

As primeiras tentativas mostram que é necessário pegar/equipar a lanterna. A bandagem é preservada enquanto a vida está cheia. Para observar o energético, vá à cozinha (`ir norte`, `ir oeste`), pegue `energético`, abra o inventário, use-o e consulte `status`; as duas cargas persistem ao esperar ou explorar. Consulte FASE4_5_2.md para testar sustos nas demonstrações.

Para testar cura e arma em confronto, resolva o percurso abaixo, recolha a pistola do cofre e a munição do armário e libere espaços com `largar ITEM` quando necessário. Entre normalmente no porão; `esperar` anuncia um golpe e o próximo `esperar` causa dano. Abra o inventário para `usar bandagem`, feche-o e experimente `equipar pistola`, `recarregar` e `atacar`, consultando `status` entre ações. Para sair, `fugir sul`. Você também pode pegar spray no armário e abrir a caixa médica no porão para testar as outras curas. Faça testes diferentes em partidas novas para não esgotar os recursos.

Os quatro cômodos originais foram preservados. O novo bloco acrescenta o Arquivo do Porão. Examinar objetos pode revelar pistas; abrir recipientes disponibiliza seu conteúdo no cômodo, sem colocá-lo automaticamente no inventário. Portas precisam ser abertas antes de atravessar. Itens podem ser largados e recuperados para administrar os seis espaços. As descrições continuam disponíveis após coletar documentos. Beber chá reduz o medo em 30, até o mínimo de zero, e remove o item equipado quando necessário.

## Validar

```sh
python -B -m unittest -v
```

## Confronto por ações

O vigia ronda o porão dentro do ambiente de exploração, sem tela de batalha. Nada acontece enquanto você pensa ou digita. Cada comando de ação reconhecido (inclusive uma tentativa sem sucesso) consome um turno, resolve Joseph primeiro e depois uma reação da ameaça presente. `ajuda`, `status` e `inventário` são gratuitos; comandos desconhecidos e linhas vazias também não avançam o tempo. `olhar` e `examinar` consomem turno.

- `atacar` ou `atacar vigia`: causa 10 de dano, ou 25 com o pé de cabra equipado. O vigia tem 60 de resistência. Um golpe que o derruba impede sua reação.
- `defender`: reduz de 16 para 8 o dano de um golpe neste turno. A defesa não fica acumulada para turnos posteriores.
- `distrair`: com a lanterna equipada, ofusca o vigia e cancela sua reação e o golpe preparado. Funciona uma vez por inimigo; depois ele protege os olhos.
- `fugir sul`: sai do porão sem sofrer o golpe pendente. Precisa de uma saída existente e aberta. `ir sul` também permite abandonar o encontro. O vigia permanece no cômodo, com a resistência e o alerta preservados; não persegue Joseph.
- `esgueirar norte`: entra silenciosamente. Um inimigo que ainda não percebeu Joseph continua desatento. Examinar, olhar, esperar e esconder-se preservam a furtividade; manipular objetos ou atacar revela Joseph. Não é possível despistar um vigia já alertado simplesmente entrando novamente em silêncio.
- `esconder`: mantém Joseph fora de vista antes de ser percebido. Não funciona quando o vigia já está acompanhando seus movimentos.
- `esperar`: passa um turno. `status` mostra vida, medo, equipamento e turnos.

Ao perceber Joseph, o vigia gasta a primeira reação se virando e aumenta o medo em 5. Nas reações seguintes, alterna entre anunciar e executar um golpe. Cada golpe aumenta o medo em 5. Beber chá ainda reduz o medo em 30 antes da reação inimiga; receber um golpe em seguida pode aumentar o medo novamente. Equipar ou largar itens durante o confronto também custa um turno.

É possível completar todo o puzzle, ler a pasta e voltar sem atacar ou sofrer dano: examine a porta para descobrir a ronda, entre com `esgueirar norte`, examine a pasta e saia com `esgueirar sul`. O confronto não bloqueia documentos nem exige derrotar o vigia.

## Solução do novo bloco (spoilers)

```text
ir norte
examinar retrato
examinar inscrição
ir oeste
pegar pé de cabra
ir leste
usar pé de cabra na gaveta
pegar chave do armário
ir leste
usar chave do armário no armário
examinar bilhete
digitar 0417 no cofre
pegar chave do porão
ir oeste
usar chave do porão na porta do porão
examinar porta do porão
esgueirar norte
examinar pasta de joseph
esgueirar sul
```

A pasta encerra este bloco narrativo e aponta para a ala superior. Na Fase 4.3, o Corredor Superior é acessível pela escadaria; a porta do quarto permanece trancada. O código do cofre pode ser inserido quando conhecido; não há bloqueio artificial exigindo a leitura prévia do bilhete.


Consulte FASE4_4.md para documentos visuais, chaves por IDs, áudio offline e roteiro de validação.



