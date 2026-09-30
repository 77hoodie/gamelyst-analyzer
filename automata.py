"""Construção e exportação dos AFNε documentados no Gamelyst Analyzer."""

from __future__ import annotations

import argparse
from pathlib import Path

import graphviz

from patterns import GENRES, PLATFORMS

EPSILON = "ε"


def _base(nome: str) -> graphviz.Digraph:
    dot = graphviz.Digraph(name=nome, format="svg")
    dot.attr(rankdir="LR", labelloc="t", label=nome, fontsize="18")
    dot.attr("node", fontname="Arial")
    dot.attr("edge", fontname="Arial")
    dot.node("inicio", "", shape="point")
    return dot


def _mark_start(dot: graphviz.Digraph, state: str = "q0") -> None:
    dot.edge("inicio", state)


def _add_literal_branch(
    dot: graphviz.Digraph,
    start: str,
    final: str,
    word: str,
    prefix: str,
    branch_number: int,
    epsilon_start: bool = True,
    epsilon_end: bool = True,
) -> None:
    first = f"{prefix}_{branch_number}_0"
    if epsilon_start:
        dot.edge(start, first, label=EPSILON)
    else:
        first = start

    current = first
    for index, char in enumerate(word, start=1):
        nxt = f"{prefix}_{branch_number}_{index}"
        dot.edge(current, nxt, label=char)
        current = nxt

    if epsilon_end:
        dot.edge(current, final, label=EPSILON)
    elif current != final:
        dot.edge(current, final)


def afne_titulo() -> graphviz.Digraph:
    dot = _base("ER-01 — Título")
    dot.node("q0", "q0")
    dot.node("q1", "q1", shape="doublecircle")
    dot.node("q2", "q2")
    dot.node("qf", "qf", shape="doublecircle")
    _mark_start(dot)

    # B = L ∪ D; P = pontuação permitida; E = espaço;
    # A = B ∪ P ∪ E; X = B ∪ P.
    dot.edge("q0", "q1", label="B")
    dot.edge("q1", "q2", label=EPSILON)
    dot.edge("q2", "q2", label="A")
    dot.edge("q2", "qf", label="X")

    dot.attr("node", shape="note")
    dot.node(
        "legenda",
        "B = L ∪ D\\nP = { :, -, ', !, ?, ., ,, &, (, ) }\\nE = { espaço }\\nA = B ∪ P ∪ E\\nX = B ∪ P\\nCada rótulo de conjunto abrevia transições unitárias, uma por símbolo.",
    )
    return dot


def afne_plataforma() -> graphviz.Digraph:
    dot = _base("ER-02 — Plataforma")
    dot.node("q0", "q0")
    dot.node("qf", "qf", shape="doublecircle")
    _mark_start(dot)

    for index, word in enumerate(PLATFORMS, start=1):
        _add_literal_branch(dot, "q0", "qf", word, "p", index)
    return dot


def afne_ano() -> graphviz.Digraph:
    dot = _base("ER-03 — Ano")
    dot.node("q0", "q0")
    dot.node("qf", "qf", shape="doublecircle")
    _mark_start(dot)

    # 19[5-9][0-9]
    dot.edge("q0", "a0", label=EPSILON)
    dot.edge("a0", "a1", label="1")
    dot.edge("a1", "a2", label="9")
    dot.edge("a2", "a3", label="5,6,7,8,9")
    dot.edge("a3", "a4", label="0,1,2,3,4,5,6,7,8,9")
    dot.edge("a4", "qf", label=EPSILON)

    # 20[0-2][0-9]
    dot.edge("q0", "b0", label=EPSILON)
    dot.edge("b0", "b1", label="2")
    dot.edge("b1", "b2", label="0")
    dot.edge("b2", "b3", label="0,1,2")
    dot.edge("b3", "b4", label="0,1,2,3,4,5,6,7,8,9")
    dot.edge("b4", "qf", label=EPSILON)

    dot.attr("node", shape="note")
    dot.node("legenda", "Rótulos separados por vírgula representam transições unitárias alternativas.")
    return dot


def _add_genre_union(dot: graphviz.Digraph, start: str, end: str, prefix: str) -> None:
    for index, genre in enumerate(GENRES, start=1):
        _add_literal_branch(dot, start, end, genre, prefix, index)


def afne_genero() -> graphviz.Digraph:
    dot = _base("ER-04 — Gênero")
    dot.node("q0", "q0")
    dot.node("q1", "q1")
    dot.node("q2", "q2")
    dot.node("qf", "qf", shape="doublecircle")
    _mark_start(dot)

    _add_genre_union(dot, "q0", "q1", "g1")
    dot.edge("q1", "qf", label=EPSILON)
    dot.edge("q1", "q2", label="/")
    _add_genre_union(dot, "q2", "qf", "g2")
    return dot


def afne_nota() -> graphviz.Digraph:
    dot = _base("ER-05 — Nota")
    dot.node("q0", "q0")
    dot.node("n", "n")
    dot.node("qf", "qf", shape="doublecircle")
    _mark_start(dot)

    # Alternativa 10(.0)?
    dot.edge("q0", "a0", label=EPSILON)
    dot.edge("a0", "a1", label="1")
    dot.edge("a1", "a2", label="0")
    dot.edge("a2", "n", label=EPSILON)
    dot.edge("a2", "a3", label=".")
    dot.edge("a3", "n", label="0")

    # Alternativa D(.D)?
    dot.edge("q0", "b0", label=EPSILON)
    dot.edge("b0", "b1", label="0,1,2,3,4,5,6,7,8,9")
    dot.edge("b1", "n", label=EPSILON)
    dot.edge("b1", "b2", label=".")
    dot.edge("b2", "n", label="0,1,2,3,4,5,6,7,8,9")

    # Sufixo /10
    dot.edge("n", "s1", label="/")
    dot.edge("s1", "s2", label="1")
    dot.edge("s2", "qf", label="0")

    dot.attr("node", shape="note")
    dot.node("legenda", "Rótulos separados por vírgula representam transições unitárias alternativas.")
    return dot


AUTOMATA_BUILDERS = {
    "ER-01 — Título": afne_titulo,
    "ER-02 — Plataforma": afne_plataforma,
    "ER-03 — Ano": afne_ano,
    "ER-04 — Gênero": afne_genero,
    "ER-05 — Nota": afne_nota,
}


def get_automaton(name: str) -> graphviz.Digraph:
    return AUTOMATA_BUILDERS[name]()


def exportar_automatos(diretorio: str | Path = "automatos") -> list[Path]:
    output = Path(diretorio)
    output.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []

    slugs = ("titulo", "plataforma", "ano", "genero", "nota")
    for index, ((_, builder), slug) in enumerate(zip(AUTOMATA_BUILDERS.items(), slugs), start=1):
        base = output / f"er{index:02d}_{slug}"
        dot = builder()
        dot_path = base.with_suffix(".dot")
        svg_path = base.with_suffix(".svg")
        dot_path.write_text(dot.source, encoding="utf-8")
        svg_path.write_bytes(dot.pipe(format="svg"))
        generated.extend([dot_path, svg_path])

    return generated


def main() -> None:
    parser = argparse.ArgumentParser(description="Exporta os AFNε do Gamelyst Analyzer em DOT e SVG.")
    parser.add_argument("--export", default="automatos", help="Diretório de saída.")
    args = parser.parse_args()
    paths = exportar_automatos(args.export)
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
