# Diagramas AFNε

Esta pasta contém as representações em DOT e SVG das cinco Expressões Regulares usadas pelo Gamelyst Analyzer.

| Arquivo | Expressão |
|---|---|
| `er01_titulo.*` | ER-01 — Título |
| `er02_plataforma.*` | ER-02 — Plataforma |
| `er03_ano.*` | ER-03 — Ano |
| `er04_genero.*` | ER-04 — Gênero |
| `er05_nota.*` | ER-05 — Nota |

Convenções gráficas:

- a seta sem origem visível aponta para o estado inicial;
- estados com círculo duplo são estados finais;
- `ε` representa movimento vazio;
- rótulos separados por vírgula representam alternativas de um único símbolo;
- na ER-01, `B`, `A` e `X` são abreviações de conjuntos finitos definidos em `docs/expressoes_regulares.md`;
- nomes de plataformas e gêneros são percorridos caractere por caractere, nunca como uma única transição.
