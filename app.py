import os
import re
import pandas as pd
import streamlit as st
import graphviz

# Dicionário de Expressões Regulares com suporte completo a acentos Unicode (\u00C0-\u00FF)
PATTERNS = {
    "TITULO": r"^[a-zA-Z0-9\u00C0-\u00FF][a-zA-Z0-9\u00C0-\u00FF\ \:\-\'\!]*$",
    "PLATAFORMA": r"^(PC|PS1|PS2|PS3|PS4|PS5|Xbox One|Xbox Series X/S|Nintendo Switch|Android|iOS)$",
    "ANO": r"^(19[5-9]\d|20[0-2]\d)$",
    "GENERO": r"^(RPG|Ação|Aventura|Estratégia|Esportes|Simulação|Terror|Puzzle|Luta)$",
    "NOTA": r"^(10(\.0)?|[0-9](\.[0-9])?)\/10$"
}

st.set_page_config(page_title="GameCatalog Parser", page_icon="🎮", layout="wide")

st.title("🎮 GameCatalog Lexer & Parser")
st.markdown("Validação léxica de catálogo de jogos via Expressões Regulares.")

tab_app, tab_afn, tab_docs = st.tabs(["🚀 Processador de Dados", "🕸️ Diagramas AFN-ε (Graphviz)", "📜 Fichas das Expressões"])

def validar_campo(valor: str, chave: str) -> bool:
    if not valor:
        return False
    return bool(re.fullmatch(PATTERNS[chave], valor.strip()))

def processar_linhas(linhas):
    validos = []
    invalidos = []

    for idx, linha in enumerate(linhas, start=1):
        linha_limpa = linha.strip()
        if not linha_limpa:
            continue

        partes = [p.strip() for p in linha_limpa.split("|")]
        if len(partes) != 5:
            invalidos.append({
                "Linha": idx, 
                "Conteúdo": linha_limpa, 
                "Motivo": f"Esperados 5 campos separados por '|', encontrados {len(partes)}"
            })
            continue

        titulo, plataforma, ano, genero, nota = partes
        erros = []

        if not validar_campo(titulo, "TITULO"): erros.append("Título Inválido")
        if not validar_campo(plataforma, "PLATAFORMA"): erros.append("Plataforma Inválida")
        if not validar_campo(ano, "ANO"): erros.append("Ano Out-of-Range (1950-2029)")
        if not validar_campo(genero, "GENERO"): erros.append("Gênero Não Cadastrado")
        if not validar_campo(nota, "NOTA"): erros.append("Nota Inválida (esperado 0-10/10)")

        if erros:
            invalidos.append({
                "Linha": idx,
                "Conteúdo": linha_limpa,
                "Motivo": ", ".join(erros)
            })
        else:
            validos.append({
                "Linha": idx,
                "Título": titulo,
                "Plataforma": plataforma,
                "Ano": int(ano),
                "Gênero": genero,
                "Nota": nota
            })

    return pd.DataFrame(validos), pd.DataFrame(invalidos)

with tab_app:
    st.sidebar.header("Entrada de Dados")
    opcao_entrada = st.sidebar.radio(
        "Selecione a fonte de dados:", 
        ["Carregar de data/ (Arquivos de Exemplo)", "Upload de Arquivo .txt", "Digitação Manual"]
    )

    dados_entrada = ""

    if opcao_entrada == "Carregar de data/ (Arquivos de Exemplo)":
        arquivo_sel = st.sidebar.selectbox("Escolha o arquivo:", ["data/jogos_validos.txt", "data/jogos_invalidos.txt", "Ambos (Todos os 7 Jogos)"],index=2)
        
        conteudos = []
        if arquivo_sel in ["data/jogos_validos.txt", "Ambos (Todos os 7 Jogos)"] and os.path.exists("data/jogos_validos.txt"):
            with open("data/jogos_validos.txt", "r", encoding="utf-8") as f:
                conteudos.append(f.read())
                
        if arquivo_sel in ["data/jogos_invalidos.txt", "Ambos (Todos os 7 Jogos)"] and os.path.exists("data/jogos_invalidos.txt"):
            with open("data/jogos_invalidos.txt", "r", encoding="utf-8") as f:
                conteudos.append(f.read())

        dados_entrada = "\n".join(conteudos)

    elif opcao_entrada == "Upload de Arquivo .txt":
        uploaded_file = st.sidebar.file_uploader("Envie seu arquivo .txt", type=["txt"])
        if uploaded_file:
            dados_entrada = uploaded_file.getvalue().decode("utf-8")
    else:
        dados_entrada = st.sidebar.text_area("Cole os dados no formato:\nTítulo | Plataforma | Ano | Gênero | Nota/10", height=200)

    if dados_entrada:
        linhas = dados_entrada.split("\n")
        df_validos, df_invalidos = processar_linhas(linhas)

        col1, col2, col3 = st.columns(3)
        total = len(df_validos) + len(df_invalidos)
        col1.metric("Total de Linhas Analisadas", total)
        col2.metric("Registros Válidos ✅", len(df_validos))
        col3.metric("Registros Inválidos ❌", len(df_invalidos))

        st.divider()

        if not df_validos.empty:
            st.subheader("✅ Catálogo de Jogos Reconhecidos")
            st.dataframe(df_validos, use_container_width=True)

        if not df_invalidos.empty:
            st.subheader("❌ Registros Corrompidos / Rejeitados")
            st.dataframe(df_invalidos, use_container_width=True)

with tab_afn:
    st.subheader("Visualizador dos AFN-ε com Graphviz")
    dot = graphviz.Digraph(comment="AFNe Plataforma")
    dot.attr(rankdir="LR")
    dot.node("q0", "q0 (Inicial)", shape="circle")
    dot.node("qf", "qf (Final)", shape="doublecircle")
    
    for idx, plat in enumerate(["PC", "PS5", "iOS"], start=1):
        dot.edge("q0", f"q_{idx}_1", label="ε")
        dot.edge(f"q_{idx}_1", f"q_{idx}_2", label=plat)
        dot.edge(f"q_{idx}_2", "qf", label="ε")
        
    st.graphviz_chart(dot)

with tab_docs:
    st.subheader("Fichas de Notação Formal")
    st.markdown("""
    | ID | Nome | Notação Formal | Sintaxe Python |
    |---|---|---|---|
    | **ER-01** | Título | $(L \cup D)(L \cup D \cup S)^*$ | `^[a-zA-Z0-9\u00C0-\u00FF][a-zA-Z0-9\u00C0-\u00FF\ \:\-\'\!]*$` |
    | **ER-02** | Plataforma | $(\text{PC} \cup \text{PS5} \cup \dots)$ | `^(PC\|PS1\|PS2\|...)$` |
    | **ER-03** | Ano | $(19 D_5 D \cup 20 D_2 D)$ | `^(19[5-9]\d\|20[0-2]\d)$` |
    | **ER-04** | Gênero | $(\text{RPG} \cup \text{Ação} \cup \dots)$ | `^(RPG\|Ação\|Aventura\|...)$` |
    | **ER-05** | Nota | $((10(.0 \cup \epsilon) \cup D(.D \cup \epsilon))/10)$ | `^(10(\.0)?\|[0-9](\.[0-9])?)\/10$` |
    """)