# Gamelyst Analyzer

Aplicação em Python para análise léxica, validação e estruturação de catálogos textuais de jogos. Cada registro é dividido em cinco campos e validado por Expressões Regulares antes de ser convertido para uma estrutura tabular. A interface também apresenta estatísticas, filtros, registros rejeitados e os AFNε correspondentes às cinco linguagens reconhecidas.

---

## Visão geral

Formato de entrada:

```text
Título | Plataforma | Ano | Gênero | Nota
```

Exemplo:

```text
Hades | PC | 2020 | Roguelike | 9.5/10
God of War: Ragnarök | PS5 | 2022 | Ação/Aventura | 10/10
Pokémon: Let's Go, Pikachu! | Nintendo Switch | 2018 | RPG/Aventura | 8.3/10
```

O processamento realiza as seguintes etapas:

1. leitura do texto digitado, de um arquivo `.txt` ou dos arquivos de exemplo;
2. remoção de espaços existentes apenas nas extremidades de cada campo;
3. separação da linha pelos caracteres `|`;
4. validação de título, plataforma, ano, gênero e nota;
5. classificação de cada registro como reconhecido ou rejeitado;
6. cálculo de estatísticas para os registros reconhecidos;
7. aplicação opcional de filtros e exportação dos resultados em CSV.

---

## Tecnologias

| Componente | Tecnologia |
|---|---|
| Linguagem | Python 3.11+ |
| Expressões Regulares | módulo nativo `re` |
| Interface | Streamlit |
| Tabelas | Pandas |
| Testes | pytest |
| AFNε | Graphviz |
| Entrada | texto ou arquivo `.txt` em UTF-8 |

---

## Expressões Regulares

As expressões ficam centralizadas em `patterns.py`. A aplicação e os testes importam os mesmos padrões, evitando versões divergentes.

| ID | Campo | Linguagem resumida |
|---|---|---|
| ER-01 | Título | letras latinas, dígitos, espaços internos e pontuação delimitada |
| ER-02 | Plataforma | conjunto fechado de plataformas aceitas |
| ER-03 | Ano | anos entre 1950 e 2029 |
| ER-04 | Gênero | um gênero cadastrado ou dois separados por `/` |
| ER-05 | Nota | valores entre `0/10` e `10/10`, com até uma casa decimal |

A descrição formal completa, os alfabetos, as cadeias aceitas e rejeitadas, os operadores e as limitações estão em [`docs/expressoes_regulares.md`](docs/expressoes_regulares.md).

---

## Estrutura de arquivos

```text
gamelyst-analyzer/
├── app.py
├── automata.py
├── catalog_stats.py
├── parser.py
├── patterns.py
├── validators.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
├── automatos/
│   ├── er01_titulo.dot
│   ├── er01_titulo.svg
│   ├── ...
│   └── er05_nota.svg
├── data/
│   ├── catalogo_demo.txt
│   ├── jogos_validos.txt
│   └── jogos_invalidos.txt
├── docs/
│   └── expressoes_regulares.md
└── tests/
    ├── test_catalog_stats.py
    ├── test_parser.py
    └── test_patterns.py
```

---

## Pré-requisitos

- Python 3.11 ou superior;
- `pip` disponível no ambiente;
- Graphviz instalado no sistema operacional para renderização dos arquivos SVG.

A presença do executável Graphviz pode ser verificada com:

```bash
dot -V
```

Instalação do Graphviz em ambientes comuns:

### Windows

```powershell
winget install Graphviz.Graphviz
```

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install graphviz
```

### macOS com Homebrew

```bash
brew install graphviz
```

---

## Ambiente Python

### Windows — PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Execução da interface

Com o ambiente virtual ativo:

```bash
python -m streamlit run app.py
```

O Streamlit informa no terminal o endereço local, normalmente:

```text
http://localhost:8501
```

A interface possui três áreas:

- **Analisador:** entrada, validação, estatísticas, filtros e exportação CSV;
- **AFNε:** visualização dos cinco autômatos;
- **Expressões Regulares:** padrões exatamente como usados no código e documentação formal.

---

## Formato dos dados

Cada linha não vazia precisa conter exatamente cinco campos:

```text
Título | Plataforma | Ano | Gênero | Nota
```

Exemplos reconhecidos:

```text
The Witcher 3: Wild Hunt | PC | 2015 | RPG | 9.8/10
Forza Horizon 5 | Xbox Series X/S | 2021 | Corrida | 9.1/10
God of War: Ragnarök | PS5 | 2022 | Ação/Aventura | 10/10
```

Exemplos rejeitados:

```text
GTA VI | PS5 | 2035 | Ação | 10.0/10
Portal 2 | PlayStation 3 | 2011 | Puzzle | 9.5/10
@Doom Eternal | PS4 | 2020 | Ação | 9.5
```

Os motivos de rejeição são mostrados por campo na interface.

---

## Testes automatizados

A suíte cobre:

- pelo menos seis cadeias aceitas e seis rejeitadas para cada ER;
- casos-limite das linguagens;
- rejeição de dígitos Unicode na ER de ano;
- normalização de espaços ao redor dos campos;
- linhas com quantidade incorreta de campos;
- múltiplos erros na mesma linha;
- cálculo das estatísticas.

Execução:

```bash
python -m pytest -q
```

---

## AFNε

Os diagramas são gerados por `automata.py` e ficam disponíveis na interface. Cópias em DOT e SVG podem ser recriadas com:

```bash
python automata.py --export automatos
```

Nos diagramas:

- `ε` indica movimento vazio;
- palavras como `PC`, `PS5` ou `Android` são percorridas caractere por caractere;
- rótulos separados por vírgula indicam alternativas de um único símbolo;
- na ER-01, os rótulos `B`, `A` e `X` são abreviações de conjuntos finitos definidos na documentação formal.

---

## Integrantes

| Integrante | Nome completo |
|---|---|
| 1 | João Pedro Almeida Follmann |
| 2 | Samuel Paula Nunes Salheb |
| 3 | Yuri Antonio Santos Fernandes |
| 4 | Arthur José Aviz Lima |

---

## Uso de Inteligência Artificial

Foi utilizado ChatGPT, da OpenAI, como ferramenta de apoio na revisão e refatoração do código, organização da documentação, elaboração e ampliação de casos de teste e revisão da correspondência entre as Expressões Regulares e os AFNε. O conteúdo resultante foi mantido de forma legível e modular para permitir conferência, explicação e modificação pelos integrantes.

---

## Licença e referências

As dependências externas utilizadas estão listadas em `requirements.txt`. A sintaxe de Expressões Regulares segue o motor `re` do Python; a renderização dos autômatos utiliza Graphviz.
