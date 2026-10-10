# Recursos visuais — Fase 4.5

Todos os caminhos são relativos a esta pasta, localizada junto ao código do jogo. Não há downloads nem dependências externas. PNGs ausentes ou inválidos acionam formas provisórias; WAVs ausentes resultam em silêncio.

- `objects/`: 42 PNGs provisórios de 32×40 pixels, RGBA, cobrindo itens, papéis, retrato, chave, pistola, munição e lanterna. Cada família oferece `front`, `back`, `interior`, `open`, `closed`, `damaged`. Imagens não autorizam ações: estas dependem das propriedades do objeto.
- `enemies/`: cinco estados provisórios do vigia: `idle`, `alert`, `preparing`, `distracted`, `fallen`. Não foram adicionadas novas espécies ou novas regras de confronto.
- `documents/`: reservado para ilustrações definitivas de cartas, relatórios, diários e pastas. O papel e o conteúdo selecionável são apresentados pelo leitor integrado.
- `backgrounds/`, `characters/`, `ui/`: reservados para cenários, Joseph e elementos da interface; a apresentação atual conserva formas provisórias.
- `audio/`: os mesmos 12 sons provisórios offline da Fase 4.4.

## Configurar um objeto

`GameObject` aceita `sprite=SpriteSpec(...)` e `inspection_faces={...}`. O identificador visual é vinculado a `object_id` do próprio objeto. Exemplo:

```python
SpriteSpec(position=(0.4, 0.5), scale=2, visible=True, layer=20,
           images={'front': 'objects/portrait_front.png',
                   'back': 'objects/portrait_back.png'})
```

A posição usa frações da largura/altura da cena. Sem posição explícita, os objetos são distribuídos automaticamente. Camadas maiores são desenhadas por cima. `visible=False` oculta apenas a apresentação; acessibilidade e possibilidade de interação continuam sendo propriedades do mundo.

`inspection_faces` associa a face ao texto visível: `front`, `back`, `interior`, `open`, `closed`, `damaged`. Só faces configuradas são examináveis. Interior exige recipiente aberto e destrancado; estados aberto, fechado e danificado são verificados antes da inspeção. O estado desenhado na cena acompanha abertura e dano reais. O inimigo acompanha os estados reais do confronto. Coletar um objeto remove a mesma instância da sala e a coloca no inventário.

O carregamento usa `PhotoImage` do Tk, mantendo transparência. Ampliação inteira e amostragem pontual evitam borrões; escalas intermediárias são aproximadas por fatores inteiros. O cache é limitado e as imagens permanecem referenciadas enquanto visíveis. Não há interpolação suave, animação ou iluminação dinâmica nesta fase. Os PNGs incluídos são formas geométricas de validação, não arte definitiva.

Fase 4.5.1: inimigos possuem identidade individual. A seleção usa a posição horizontal do mesmo sprite; a distância próximo/médio/distante determina altura e escala da apresentação. A demonstração usa os PNGs provisórios existentes, sem nova arte definitiva.
