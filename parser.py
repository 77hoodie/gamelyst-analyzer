"""Leitura e estruturação das linhas do catálogo."""

from validators import erros_do_registro

FIELD_LABELS = {
    "TITULO": "Título",
    "PLATAFORMA": "Plataforma",
    "ANO": "Ano",
    "GENERO": "Gênero",
    "NOTA": "Nota",
}


def _nota_numerica(nota: str) -> float:
    return float(nota.removesuffix("/10"))


def processar_linhas(linhas: list[str]) -> tuple[list[dict], list[dict]]:
    """Processa uma sequência de linhas.

    Espaços presentes apenas nas extremidades da linha e de cada campo são
    removidos antes da validação. Essa normalização é externa às ERs.
    Linhas totalmente vazias são ignoradas.
    """
    validos: list[dict] = []
    invalidos: list[dict] = []

    for numero_linha, linha in enumerate(linhas, start=1):
        linha_limpa = linha.strip()
        if not linha_limpa:
            continue

        partes = [parte.strip() for parte in linha_limpa.split("|")]
        if len(partes) != 5:
            invalidos.append(
                {
                    "Linha": numero_linha,
                    "Conteúdo": linha_limpa,
                    "Campos inválidos": "Estrutura",
                    "Detalhes": (
                        "A linha deve conter exatamente 5 campos separados por '|'. "
                        f"Foram encontrados {len(partes)} campo(s)."
                    ),
                }
            )
            continue

        titulo, plataforma, ano, genero, nota = partes
        erros = erros_do_registro(titulo, plataforma, ano, genero, nota)

        if erros:
            invalidos.append(
                {
                    "Linha": numero_linha,
                    "Conteúdo": linha_limpa,
                    "Campos inválidos": ", ".join(FIELD_LABELS[chave] for chave in erros),
                    "Detalhes": " ".join(erros.values()),
                }
            )
            continue

        validos.append(
            {
                "Linha": numero_linha,
                "Título": titulo,
                "Plataforma": plataforma,
                "Ano": int(ano),
                "Gênero": genero,
                "Nota": nota,
                "Nota numérica": _nota_numerica(nota),
            }
        )

    return validos, invalidos


def processar_texto(texto: str) -> tuple[list[dict], list[dict]]:
    """Processa um catálogo em texto."""
    if not isinstance(texto, str) or not texto.strip():
        return [], []
    return processar_linhas(texto.splitlines())
