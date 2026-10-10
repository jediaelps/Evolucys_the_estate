# Fase 4.5.5 — correção pontual da ajuda

O histórico normal deixou de exibir as dicas automáticas, inclusive na entrada inicial, após ações, no inventário e após pedidos incompletos. O sistema contextual foi preservado: a orientação aparece quando o jogador pede ajuda, por uma fala identificada de Joseph. `ajuda comandos` mantém a referência explícita.

A ajuda pode combinar uma observação com uma única alternativa de movimento. Essa alternativa é obtida das conexões reais e exclui portas fechadas, trancadas, bloqueadas, inacessíveis ou não visíveis. Direções e ações sugeridas mantêm destaque discreto, sem destacar a frase inteira. Uma ameaça alertada sem passagem livre gera orientação de defesa, sem afirmar que há uma saída aberta.

Arquivos modificados: `visual.py`, `context_help.py`, `test_phase452.py`, `test_phase454.py`, `test_phase455.py`. Acrescentados: `test_help_cleanup.py` e este relatório. As expectativas anteriores de dicas automáticas foram atualizadas para verificar sua ausência.

Validação executada:

```sh
python -B -m unittest test_help_cleanup test_phase455.HelpTests test_phase455.HelpInterfaceTests -q
```

**15 testes direcionados aprovados**, incluindo seis novos. Cobrem histórico limpo, ações, deslocamento, inventário, perguntas contextuais, falha neutra, ajuda solicitada, caminhos reais/bloqueados, proteção de pistas, destaque, referência explícita e ancoragem inferior. Não foi executada a suíte completa.

Nenhuma mecânica ou layout foi intencionalmente alterado. Continua sendo **Fase 4.5.5**. A **Fase 5 não foi iniciada**.
