## Definições formais

As cinco expressões abaixo são validadas por correspondência completa com `re.fullmatch`. A remoção de espaços nas extremidades dos campos acontece antes da validação e não faz parte das linguagens reconhecidas pelas ERs.

- `D = {0,1,2,3,4,5,6,7,8,9}`.
- `L = {A,...,Z,a,...,z} ∪ {c | U+00C0 ≤ c ≤ U+00D6} ∪ {c | U+00D8 ≤ c ≤ U+00F6} ∪ {c | U+00F8 ≤ c ≤ U+00FF}`.
- `B = L ∪ D`.
- `P = { :, -, ', !, ?, ., ,, &, (, ) }`.
- `E = { espaço }`.
- `X = B ∪ P`.
- `A = B ∪ P ∪ E`.
- `G = {RPG, Ação, Aventura, Estratégia, Esportes, Simulação, Terror, Puzzle, Luta, FPS, Corrida, Sandbox, Roguelike, Metroidvania, Sobrevivência}`.

Classes como `[0-9]` são abreviações computacionais de uniões finitas. Nos AFNε, um rótulo com símbolos separados por vírgula representa várias transições unitárias entre o mesmo par de estados.

---

## ER-01 — Título

**Finalidade.** Reconhecer títulos formados por letras latinas, dígitos e um conjunto delimitado de sinais de pontuação. O primeiro símbolo precisa pertencer a `B` e a cadeia não pode terminar em espaço.

**Alfabeto.** `Σ₁ = L ∪ D ∪ P ∪ E`.

**Linguagem reconhecida.** Cadeias não vazias cujo primeiro símbolo pertence a `B`, cujos demais símbolos pertencem a `A` e cujo último símbolo, quando houver mais de um símbolo, pertence a `X`.

**ER formal.** `B(A*X | ε)`.

**Sintaxe no código.**

```python
r"[A-Za-z0-9À-ÖØ-öø-ÿ]([A-Za-z0-9À-ÖØ-öø-ÿ :'\-!?.,&()]*[A-Za-z0-9À-ÖØ-öø-ÿ:'\-!?.,&()])?"
```

**Operadores.** Concatenação; união implícita nas classes finitas; fecho de Kleene `*`; opcionalidade `?`; agrupamento `()`.

**Cadeias aceitas.** `A` (caso-limite), `FIFA 23`, `God of War: Ragnarök`, `Pokémon: Let's Go, Pikachu!`, `Mario & Luigi: Brothership`, `NieR:Automata`, `Plants vs. Zombies`.

**Cadeias rejeitadas.** `ε` (caso-limite), ` Game`, `Game `, `@GameTitle`, `#Doom`, `Game|PC`, três espaços.

**Limite conhecido.** O alfabeto foi delimitado para manter a linguagem formal finita e documentável; títulos que usem símbolos fora desse conjunto são rejeitados.

---

## ER-02 — Plataforma

**Finalidade.** Reconhecer uma das plataformas cadastradas, com grafia exata.

**Alfabeto.** Letras usadas nos nomes, dígitos de `1` a `5`, espaço e `/`.

**Linguagem reconhecida.** `{PC, PS1, PS2, PS3, PS4, PS5, Xbox One, Xbox Series X/S, Nintendo Switch, Android, iOS}`.

**ER formal.** `PC | PS(1|2|3|4|5) | Xbox espaço (One | Series espaço X/S) | Nintendo espaço Switch | Android | iOS`.

**Sintaxe no código.**

```python
r"(PC|PS[1-5]|Xbox (One|Series X/S)|Nintendo Switch|Android|iOS)"
```

**Operadores.** União `|`; concatenação; agrupamento `()`; classe finita `[1-5]`.

**Cadeias aceitas.** `PC`, `PS1` (caso-limite inferior da classe), `PS5` (caso-limite superior), `Xbox One`, `Xbox Series X/S`, `Nintendo Switch`, `Android`, `iOS`.

**Cadeias rejeitadas.** `ε`, `pc`, `PS0`, `PS6`, `PS 5`, `PlayStation 5`, `Xbox 360`, `Atari 2600`.

**Limite conhecido.** A lista de plataformas é fechada; nomes não cadastrados são rejeitados mesmo que correspondam a plataformas reais.

---

## ER-03 — Ano

**Finalidade.** Reconhecer anos de lançamento ou previsão entre 1950 e 2029.

**Alfabeto.** `Σ₃ = D`.

**Linguagem reconhecida.** Todos os anos de quatro dígitos no intervalo fechado `[1950, 2029]`.

**ER formal.** `19(5|6|7|8|9)D | 20(0|1|2)D`.

**Sintaxe no código.**

```python
r"(19[5-9][0-9]|20[0-2][0-9])"
```

**Operadores.** União `|`; concatenação; agrupamento; classes finitas `[5-9]`, `[0-2]` e `[0-9]`.

**Cadeias aceitas.** `1950` (caso-limite inferior), `1959`, `1999`, `2000`, `2015`, `2026`, `2029` (caso-limite superior).

**Cadeias rejeitadas.** `1949`, `2030`, `202`, `20200`, `20A6`, `2015.0`, `202٩`, `ε`.

**Limite conhecido.** O intervalo máximo é 2029 por definição da linguagem, independentemente da data atual.

---

## ER-04 — Gênero

**Finalidade.** Reconhecer um gênero cadastrado ou dois gêneros cadastrados separados por `/`.

**Alfabeto.** Letras presentes em `G`, caracteres acentuados e `/`.

**Linguagem reconhecida.** `G` ou `G/G`.

**ER formal.** `G(/G | ε)`.

**Sintaxe no código.**

```python
r"(RPG|Ação|Aventura|Estratégia|Esportes|Simulação|Terror|Puzzle|Luta|FPS|Corrida|Sandbox|Roguelike|Metroidvania|Sobrevivência)(/(RPG|Ação|Aventura|Estratégia|Esportes|Simulação|Terror|Puzzle|Luta|FPS|Corrida|Sandbox|Roguelike|Metroidvania|Sobrevivência))?"
```

**Operadores.** União `|`; concatenação; agrupamento; opcionalidade `?`.

**Cadeias aceitas.** `RPG`, `Ação`, `FPS`, `Roguelike`, `Metroidvania`, `Sobrevivência`, `Ação/Aventura`, `RPG/Ação`.

**Cadeias rejeitadas.** `ε`, `rpg`, `Acao`, `Hack and Slash`, `Ação/`, `/Aventura`, `RPG/Ação/Aventura`, `Esporte`.

**Limite conhecido.** Combinações sintaticamente válidas como `RPG/RPG` pertencem à linguagem. A ER não impõe diferença entre o primeiro e o segundo gênero.

---

## ER-05 — Nota

**Finalidade.** Reconhecer notas de 0 a 10 seguidas de `/10`, com zero ou uma casa decimal.

**Alfabeto.** `Σ₅ = D ∪ {., /}`.

**Linguagem reconhecida.** O valor `10` ou `10.0`, ou um dígito de `0` a `9` opcionalmente seguido de ponto e outro dígito, sempre seguido por `/10`.

**ER formal.** `(10(.0 | ε) | D(.D | ε))/10`.

**Sintaxe no código.**

```python
r"(10(\.0)?|[0-9](\.[0-9])?)/10"
```

**Operadores.** União `|`; concatenação; agrupamento; opcionalidade `?`; classes finitas `[0-9]`; `\.` para ponto literal na sintaxe Python.

**Cadeias aceitas.** `0/10` (caso-limite inferior), `0.0/10`, `4/10`, `7.5/10`, `9.9/10`, `10/10` (caso-limite superior), `10.0/10`.

**Cadeias rejeitadas.** `ε`, `-1/10`, `10.1/10`, `11/10`, `9,5/10`, `9.55/10`, `8.5`, `010/10`.

**Limite conhecido.** Não há arredondamento nem conversão automática de vírgula decimal; a cadeia precisa usar ponto quando houver casa decimal.
