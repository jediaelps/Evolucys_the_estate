# Fase 4.5.3 — ajuste visual final

Esta versão continua sendo a **Fase 4.5.3**. Nenhuma mecânica foi alterada e a Fase 5 não foi iniciada.

## Alterações

- Histórico ampliado de cinco para dez linhas, devolvendo espaço ao texto e reduzindo moderadamente a altura do cenário.
- Histórico à esquerda e objetivo à direita preservados, com descrições e dicas no histórico.
- Entrada limitada a aproximadamente metade da largura disponível, alinhada à esquerda; abaixo permanece somente “Digite uma ação e pressione Enter.”
- Removidas da tela as informações de modo/luz e a antiga indicação isolada da mão à esquerda.
- HUD agrupado no canto inferior direito: slot equipado acima do celular, raios acima de Vida/Medo. Vida e Medo passam de fonte 9 para 11.
- Dois raios sempre presentes, dourados ou cinza conforme as cargas. O slot reflete o equipamento e a munição quando aplicável.
- Pausa/ESC permanece no canto superior direito; não há título redundante dentro da tela de jogo.

## Arquivos

Modificados: `visual.py`, `test_phase452.py`, `README.md` e `GUI_README.md`. Acrescentado este relatório.

## Validação

Executado na pasta do projeto:

```sh
python -B -m unittest test_phase452.SystemsInterfaceTests test_visual_commands.VisualCommandTests.test_inventory_and_hud_share_game_state test_visual_commands.VisualCommandTests.test_pause_preserves_history_and_focus test_inventory_overlay.InventoryOverlayTests.test_resize_keeps_panel_centered_and_controls_inside -q
```

**8 testes aprovados**, sem testes ignorados. Cobrem proporções, entrada, posição e legibilidade dos indicadores, equipamento, estados dos raios, objetivo, histórico/dicas, pausa e redimensionamento do inventário. Não foi executada a suíte completa. Conferência visual adicional em 1100×760.

Para conferir, execute `python visual.py`, inicie o jogo e observe a divisão entre cenário e histórico. No Tutorial, equipe/largue a pistola e confira o slot; na demonstração de foco, confira os dois raios antes/depois do consumo e de um susto.
