<div align="center">

# EVOLUCYS: THE ESTATE

### A sobrevivência começa quando a estrada termina.

**Survival Horror • Mistério • Ficção Científica • Exploração narrativa**

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Interface](https://img.shields.io/badge/interface-Tkinter-informational)
![Idioma](https://img.shields.io/badge/idioma-PT--BR-success)

*Um jogo independente de terror em primeira pessoa no qual o jogador explora cenários e toma decisões por meio de comandos escritos.*

</div>

---

## Sobre o jogo

**Evolucys: The Estate** é um survival horror narrativo de exploração, investigação e resolução de enigmas. Inspirado pela tensão dos jogos clássicos de terror, combina cenários visuais estáticos, descrições atmosféricas e interação por linguagem natural.

Em vez de controlar o protagonista com WASD ou clicar nos cenários para realizar ações, você **escreve o que deseja fazer**. Observe detalhes, investigue objetos, procure caminhos, interprete pistas e decida como reagir às ameaças.

O objetivo não é derrotar tudo que aparece no caminho: **sobreviver exige atenção, cautela e improvisação**.

## Sinopse

Joseph, um empresário de 30 anos, está viajando por uma estrada isolada quando uma tempestade e um problema no pneu interrompem sua jornada. Em busca de ferramentas, ele se aproxima de uma antiga propriedade, onde uma imponente mansão se ergue em meio ao abandono.

A princípio, tudo o que Joseph deseja é encontrar uma maneira de consertar o carro e seguir viagem. Mas uma série de acontecimentos o leva para dentro de um lugar que esconde muito mais do que quartos vazios e portas trancadas.

Documentos esquecidos, instalações ocultas e sinais de experiências científicas revelam fragmentos de um projeto conhecido como **EVOLUCYS**. Algo aconteceu naquela propriedade — e talvez nem tudo o que vive ali seja humano.

**Encontre uma saída. Descubra a verdade. Sobreviva à noite.**

## Como funciona

### Exploração por comandos

A interação é feita principalmente digitando ações em português. O sistema interpreta comandos e variações de linguagem natural dentro das possibilidades do cenário.

Exemplos de ações:

```text
olhar
examinar a porta
investigar a estante
pegar lanterna
equipar lanterna
ligar lanterna
abrir inventário
passar pela porta com cuidado
esconder
```

As ações disponíveis dependem do ambiente, dos objetos presentes e do estado atual da partida. O jogo oferece ajuda contextual sem entregar automaticamente as soluções.

### Sobrevivência e recursos

- **Inventário de seis espaços:** escolha o que carregar e o que deixar para trás.
- **Vida e medo:** ferimentos e tensão afetam a sobrevivência.
- **Recursos limitados:** itens de cura, iluminação e munição exigem planejamento.
- **Ameaças no próprio cenário:** situações de perigo acontecem durante a exploração, sem uma tela de combate separada.
- **Furtividade, fuga e improvisação:** enfrentar um inimigo nem sempre é necessário ou aconselhável.
- **Investigação ambiental:** anotações, documentos, objetos e mecanismos ajudam a compreender a propriedade.

### Um mundo interligado

O projeto contempla áreas externas, térreo, andar superior, porão, garagem e instalações de pesquisa. Portas, atalhos, bloqueios e caminhos alternativos fazem parte do planejamento da exploração.

O mapa e a infraestrutura de navegação estão sendo implementados por etapas. **A existência de uma área no mapa não significa que todo o seu conteúdo narrativo e todos os seus enigmas estejam concluídos.**

## Estado do desenvolvimento

> **Protótipo jogável em desenvolvimento ativo.** Este repositório contém sistemas funcionais de exploração, interface, inventário, confronto e navegação, mas ainda não representa um jogo completo.

| Sistema | Situação |
| --- | --- |
| Interpretação de comandos e ajuda contextual | Implementado, em evolução |
| Interface visual em Tkinter | Protótipo funcional |
| Inventário com seis espaços | Implementado |
| Vida, medo, itens e recursos | Implementado no protótipo |
| Confronto, fuga e furtividade | Implementados no protótipo |
| Prólogo e começo canônico de Joseph | Implementados estruturalmente |
| Mapa ampliado da propriedade | Estrutura de navegação implementada por fases |
| Campanha, enigmas e eventos completos | Em desenvolvimento |
| Salvamento e carregamento completos | Planejados, ainda não implementados |
| Arte, animações e áudio definitivos | Em desenvolvimento |
| Localização para outros idiomas | Planejada |
| Empacotamento para Windows | Planejado |

O detalhamento técnico e o histórico das etapas estão disponíveis em [CAMPAIGN_PROGRESS.md](CAMPAIGN_PROGRESS.md) e [WORLD_DESIGN.md](WORLD_DESIGN.md).

## Executar o projeto

### Requisitos

- Python **3.8 ou superior**.
- Um ambiente desktop com suporte a **Tkinter** (incluído na maioria das instalações padrão de Python para Windows).
- Não são necessárias bibliotecas externas para o protótipo atual.

Clone o repositório:

```bash
git clone https://github.com/jediaelps/Evolucys_the_estate.git
cd Evolucys_the_estate
```

**Versão visual (recomendada):**

```bash
python visual.py
```

**Versão de terminal:**

```bash
python main.py
```

Na versão de terminal, digite `ajuda` para consultar os comandos e `sair` para encerrar.

> **Atenção:** o projeto ainda não possui um sistema completo de salvar/carregar. O progresso da sessão não é persistido entre execuções.

## Estrutura do projeto

```text
Evolucys_the_estate/
├── main.py                 # Execução em terminal
├── visual.py               # Interface gráfica em Tkinter
├── visual_session.py       # Sessão da interface visual
├── game_state.py           # Estado do jogador e do mundo
├── world.py                # Ambientes, objetos e conexões
├── command_parser.py       # Interpretação e execução de comandos
├── command_language.py     # Vocabulário e linguagem de interação
├── confrontation.py       # Encontros e reações de ameaças
├── exploration_systems.py  # Sistemas de exploração
├── items.py                # Definição e comportamento dos itens
├── survival.py             # Recursos e sobrevivência
├── inventory_view.py       # Interface do inventário
├── assets/                 # Recursos visuais e de interface
├── audio/                  # Recursos e documentação de áudio
├── test_*.py               # Testes automatizados
├── WORLD_DESIGN.md         # Mapa e decisões de design
├── CAMPAIGN_PROGRESS.md    # Histórico de desenvolvimento
└── GUI_README.md           # Detalhes da interface visual
```

A estrutura acima mostra os componentes principais, não todos os arquivos existentes.

## Testes

A base inclui testes automatizados de sistemas de jogo, navegação, narrativa, interface e regressão.

Para executar os testes disponíveis:

```bash
python -B -m unittest -v
```

## Direção do projeto

A proposta de **Evolucys: The Estate** é fazer da interpretação do ambiente a principal ferramenta do jogador. Uma descrição, um objeto aparentemente irrelevante ou um ruído distante podem influenciar a próxima decisão.

O jogo busca construir tensão por meio de descoberta gradual, vulnerabilidade, exploração coerente e consequências narrativas, e não pela quantidade de confrontos.

A história foi concebida com **desfechos alternativos**, que permanecem fora deste README para preservar a experiência.

## Documentação adicional

- [Interface e comandos visuais](GUI_README.md)
- [Projeto do mundo e mapa](WORLD_DESIGN.md)
- [Progresso da campanha](CAMPAIGN_PROGRESS.md)
- [Narração e linguagem natural — Fase 4.5.5](FASE4_5_5.md)

---

<div align="center">

**EVOLUCYS: THE ESTATE**

*Nem todo lugar abandonado está vazio.*

**Projeto independente — em desenvolvimento**

</div>
