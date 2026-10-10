# Fase 4.5.2 — refinamento dos sistemas

Esta versão amplia a base da Fase 4.5.1. Não inicia a campanha da Fase 5. O confronto continua dentro do cenário, por ações: abrir/fechar inventário e consultar ajuda não provocam reação; ações efetivas sobre itens continuam respeitando turnos. Fuga, investigação, documentos, inspeção e seleção de alvos permanecem disponíveis.

## Arquitetura e comportamento

- `confidence.py` calcula confiança a partir de capacidades do equipamento, munição, quantidade/tipo de ameaças, desconhecimento, ferimentos e surpresa. Os parâmetros são configuráveis; o resultado aparece em pensamentos, sem percentual no HUD e sem multiplicar dano.
- `items.py` define `ItemCapabilities`: uso pessoal, equipamento, ferramenta, dano corpo a corpo e confiança. Interpretar “atacar com” não transforma qualquer objeto em arma.
- `exploration_systems.py` mantém percepção, escuta, surpresa, esconderijos e rondas no mesmo `GameState`. Cada ação efetiva avança os eventos; não existem perseguição em tempo real ou temporizadores de combate.
- Consumíveis pessoais exigem inventário. A tentativa fora dele recebe “Melhor eu olhar isso no inventário.”, sem consumir item ou turno. Chaves e ferramentas contextuais continuam utilizáveis no cenário sem equipar.
- Energético concede duas cargas persistentes de foco. Uma carga só é gasta ao impedir uma perda de ação por surpresa; ouvir/perceber não gasta cargas. Não há armadura, bônus de dano ou expiração por turnos. Uma nova lata é preservada enquanto houver cargas.
- Sem proteção suficiente, o susto aumenta medo e pode fazer Joseph perder a próxima ação física. Cautela e confiança influenciam a condição. Medo, confiança e foco permanecem distintos.
- Inimigos podem ter sentidos de luz, som e proximidade, som próprio, surpresa, ameaça, rota e intervalo configurados. Esconderijos têm eficácia interna. A sequência chegada → procura → espera → saída ocorre em ações sucessivas, com variações narrativas; falha inicia confronto.
- Cômodos escuros preservam elementos grandes; detalhes marcados exigem luz. O modo UV revela pistas marcadas, sem resolver puzzles. O módulo só está habilitado na demonstração.
- O HUD mostra objetivo, vida, celular, mão e cargas ⚡ ⚡ → ⚡ → nenhuma. O Canvas se ajusta ao espaço disponível; validado também em 1100×760 para manter o rodapé visível.

## Arquivos criados

`confidence.py`, `exploration_systems.py`, `system_demo.py`, `test_phase452.py` e este relatório (`FASE4_5_2.md`).

## Arquivos modificados

Lógica: `items.py`, `world.py`, `game_state.py`, `confrontation.py`, `survival.py`, `command_parser.py`, `command_language.py`.

Interface e orientação: `visual.py`, `visual_assets.py`, `visual_session.py`, `inventory_view.py`, `hud_state.py`, `context_help.py`, `contextual_tutorial.py`.

Validação e documentação: `visual_smoke.py`, `test_survival.py`, `test_game.py`, `test_confrontation.py`, `test_phase451.py`, `test_visual_session.py`, `README.md`, `GUI_README.md`.

Os recursos visuais e sonoros provisórios existentes foram reutilizados.

## Testes

Na pasta do projeto:

```sh
python -B -m unittest discover -q
python -B visual_smoke.py
```

Resultado: **242 testes aprovados**, incluindo **36 novos**. A execução gráfica dedicada aprova **45 testes com widgets e eventos Tk reais**, já incluídos no total; não são 45 testes adicionais.

Os novos testes cobrem restrição de consumíveis, uso contextual sem equipamento, capacidades de armas, confiança independente, foco persistente, perda/prevenção de ação, percepção antecipada, silêncio, sinônimos, cautela/pressa, esconderijos, rondas, sentidos, luz/UV, restauração do estado adicional, HUD, integração do inventário e dimensões da janela.

As alterações em testes antigos acompanham duas mudanças explicitamente solicitadas: abrir o inventário antes de usar consumíveis e substituir a antiga duração/redução de dano do energético por cargas persistentes. Os cenários anteriores continuam executados; as expectativas antigas incompatíveis foram substituídas por verificações das novas regras, incluindo ausência de redução de dano.

## Como validar a interface

Execute `python visual.py` e abra o menu **Tutorial**. As três demonstrações usam estado descartável e não modificam a distribuição de itens da campanha. Para reiniciar uma demonstração, selecione-a novamente no menu.

### Sustos e foco

1. Selecione **Sustos e foco**.
2. Digite `pegar energético`, depois `usar energético`: o item deve ser preservado e Joseph recomenda o inventário.
3. Abra `inventário`, selecione o energético e clique **Usar**. Verifique ⚡ ⚡; feche com ESC ou Fechar.
4. Digite `ir norte`. O susto gasta uma carga para evitar a perda de ação; o medo ainda pode aumentar.
5. Reinicie a demonstração e entre sem consumir energético para comparar a perda da próxima ação física.

### Esconderijos e ronda

1. Selecione **Esconderijos e ronda**.
2. Digite `ir norte`, `esconder no armário pesado` e repita `esperar` para acompanhar a aproximação, procura, espera e saída.
3. Reinicie e escolha `esconder atrás das caixas baixas` para comparar a descoberta.
4. Abra/feche o inventário enquanto aguarda: isso não deve avançar a ronda. A passagem do tempo real também não avança os eventos.

### Luz e silêncio

1. Selecione **Luz e silêncio**; digite `pegar lanterna` e `equipar lanterna`.
2. Experimente `ouvir atrás da porta` e `entrar devagar`. O silêncio não garante ausência de ameaça.
3. Use `olhar em volta` no cômodo escuro e compare após `acender lanterna`: a anotação pequena passa a ser visível.
4. Digite `mudar para uv` e observe a marca oculta; lê-la não desbloqueia automaticamente puzzles. `apagar lanterna` desliga a luz.
5. Redimensione a janela até 1100×760 e confira objetivo, campo de comandos e rodapé. Abra o inventário, selecione itens com o mouse e feche com ESC para verificar o retorno ao cenário.

## Limitações e preparação futura

- Não há save/load completo nem interface de salvamento. `export_state()`/`restore_state()` serializam apenas o estado adicional de exploração, foco, iluminação e rondas, sobre um mundo base já restaurado com as mesmas identidades. Vida, inventário, localização do jogador e o restante do mundo exigirão o sistema de save futuro.
- Condições e valores são determinísticos e configuráveis, ainda sem balanceamento definitivo. A ronda segue conexões e portas válidas; ao entrar em confronto, não implementa perseguição completa nem retomada automática após fuga.
- UV habilitado apenas no ambiente de demonstração. Não foram adicionados módulo, armas, mapa, puzzles ou posicionamento definitivo da Fase 5.
- Arte e áudio continuam provisórios. Os ícones de foco atualizam sem a piscada opcional. Validação gráfica realizada no Windows/Tk 8.6; outras plataformas não foram verificadas.
