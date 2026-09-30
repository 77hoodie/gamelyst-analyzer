"""Interface Streamlit do Gamelyst Analyzer."""

from pathlib import Path

import pandas as pd
import streamlit as st

from automata import AUTOMATA_BUILDERS, get_automaton
from catalog_stats import calcular_resumo
from parser import processar_texto
from patterns import PATTERNS, PATTERN_IDS, PATTERN_NAMES

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DOCS_FILE = BASE_DIR / "docs" / "expressoes_regulares.md"

st.set_page_config(page_title="Gamelyst Analyzer", layout="wide")

st.title("Gamelyst Analyzer")
st.caption("Análise léxica e estruturação de catálogos de jogos com Expressões Regulares e AFNε.")


def carregar_exemplo(nome: str) -> str:
    path = DATA_DIR / nome
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def dataframe_validos(registros: list[dict]) -> pd.DataFrame:
    if not registros:
        return pd.DataFrame(columns=["Linha", "Título", "Plataforma", "Ano", "Gênero", "Nota", "Nota numérica"])
    return pd.DataFrame(registros)


def dataframe_invalidos(registros: list[dict]) -> pd.DataFrame:
    if not registros:
        return pd.DataFrame(columns=["Linha", "Conteúdo", "Campos inválidos", "Detalhes"])
    return pd.DataFrame(registros)


tab_app, tab_afn, tab_docs = st.tabs(["Analisador", "AFNε", "Expressões Regulares"])

with tab_app:
    st.subheader("Entrada")
    col_origem, col_formato = st.columns([1, 2])

    with col_origem:
        origem = st.radio(
            "Fonte dos dados",
            ["Exemplo", "Arquivo .txt", "Digitação manual"],
            horizontal=False,
        )

    with col_formato:
        st.markdown("**Formato de cada linha**")
        st.code("Título | Plataforma | Ano | Gênero | Nota", language="text")
        st.caption("Exemplo: Hades | PC | 2020 | Roguelike | 9.5/10")

    dados_entrada = ""

    if origem == "Exemplo":
        exemplo = st.selectbox(
            "Conjunto de exemplo",
            [
                "catalogo_demo.txt",
                "jogos_validos.txt",
                "jogos_invalidos.txt",
            ],
        )
        dados_entrada = carregar_exemplo(exemplo)
        st.text_area("Conteúdo carregado", value=dados_entrada, height=220, disabled=True)

    elif origem == "Arquivo .txt":
        uploaded_file = st.file_uploader("Arquivo de texto", type=["txt"])
        if uploaded_file is not None:
            try:
                dados_entrada = uploaded_file.getvalue().decode("utf-8")
                st.text_area("Pré-visualização", value=dados_entrada, height=220, disabled=True)
            except UnicodeDecodeError:
                st.error("O arquivo não pôde ser lido como UTF-8.")

    else:
        dados_entrada = st.text_area(
            "Catálogo",
            placeholder="Hades | PC | 2020 | Roguelike | 9.5/10",
            height=220,
        )

    st.divider()

    if not dados_entrada or not dados_entrada.strip():
        st.info("Nenhum registro disponível para análise.")
    else:
        validos, invalidos = processar_texto(dados_entrada)
        df_validos = dataframe_validos(validos)
        df_invalidos = dataframe_invalidos(invalidos)
        resumo = calcular_resumo(validos)

        total = len(validos) + len(invalidos)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Linhas analisadas", total)
        m2.metric("Registros válidos", len(validos))
        m3.metric("Registros inválidos", len(invalidos))
        m4.metric(
            "Média das notas",
            "—" if resumo["media_notas"] is None else f"{resumo['media_notas']:.2f}/10",
        )

        if validos:
            st.subheader("Resumo")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(
                    f"**Mais antigo(s):** {', '.join(resumo['mais_antigos'])} ({resumo['ano_minimo']})"
                )
                st.markdown(
                    f"**Mais recente(s):** {', '.join(resumo['mais_recentes'])} ({resumo['ano_maximo']})"
                )
            with c2:
                contagem_plataforma = pd.DataFrame(
                    list(resumo["por_plataforma"].items()),
                    columns=["Plataforma", "Quantidade"],
                )
                st.dataframe(contagem_plataforma, use_container_width=True, hide_index=True)

            st.subheader("Filtros")
            plataformas = sorted(df_validos["Plataforma"].unique().tolist())
            generos = sorted(df_validos["Gênero"].unique().tolist())
            ano_min = int(df_validos["Ano"].min())
            ano_max = int(df_validos["Ano"].max())

            f1, f2, f3, f4 = st.columns(4)
            plataforma_filtro = f1.selectbox("Plataforma", ["Todas"] + plataformas)
            genero_filtro = f2.selectbox("Gênero", ["Todos"] + generos)
            intervalo_ano = f3.slider("Ano", 1950, 2029, (ano_min, ano_max))
            nota_minima = f4.slider("Nota mínima", 0.0, 10.0, 0.0, 0.1)

            filtrado = df_validos.copy()
            if plataforma_filtro != "Todas":
                filtrado = filtrado[filtrado["Plataforma"] == plataforma_filtro]
            if genero_filtro != "Todos":
                filtrado = filtrado[filtrado["Gênero"] == genero_filtro]
            filtrado = filtrado[
                (filtrado["Ano"] >= intervalo_ano[0])
                & (filtrado["Ano"] <= intervalo_ano[1])
                & (filtrado["Nota numérica"] >= nota_minima)
            ]

            st.subheader("Registros reconhecidos")
            st.dataframe(
                filtrado.drop(columns=["Nota numérica"]),
                use_container_width=True,
                hide_index=True,
            )

            csv_validos = filtrado.drop(columns=["Nota numérica"]).to_csv(index=False).encode("utf-8")
            st.download_button(
                "Baixar registros filtrados em CSV",
                data=csv_validos,
                file_name="gamelyst_registros.csv",
                mime="text/csv",
            )

        if invalidos:
            st.subheader("Registros rejeitados")
            st.dataframe(df_invalidos, use_container_width=True, hide_index=True)
            csv_invalidos = df_invalidos.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Baixar relatório de rejeições em CSV",
                data=csv_invalidos,
                file_name="gamelyst_rejeicoes.csv",
                mime="text/csv",
            )

with tab_afn:
    st.subheader("AFNε das expressões")
    st.caption(
        "Nos diagramas, rótulos com vários símbolos separados por vírgula representam transições unitárias alternativas. "
        "Na ER-01, B, A e X são abreviações de conjuntos finitos descritos na legenda do próprio diagrama."
    )
    automato_nome = st.selectbox("Expressão", list(AUTOMATA_BUILDERS.keys()))
    st.graphviz_chart(get_automaton(automato_nome), use_container_width=True)

with tab_docs:
    st.subheader("Padrões implementados")
    tabela = pd.DataFrame(
        [
            {
                "ID": PATTERN_IDS[chave],
                "Nome": PATTERN_NAMES[chave],
                "Sintaxe usada no código": PATTERNS[chave],
            }
            for chave in PATTERNS
        ]
    )
    st.dataframe(tabela, use_container_width=True, hide_index=True)

    if DOCS_FILE.exists():
        st.markdown(DOCS_FILE.read_text(encoding="utf-8"))
    else:
        st.warning("A documentação detalhada das expressões não foi encontrada.")
