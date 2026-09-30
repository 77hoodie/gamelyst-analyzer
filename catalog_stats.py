"""Estatísticas derivadas dos registros reconhecidos."""

from collections import Counter
from statistics import mean


def calcular_resumo(registros: list[dict]) -> dict:
    if not registros:
        return {
            "quantidade": 0,
            "media_notas": None,
            "ano_minimo": None,
            "ano_maximo": None,
            "mais_antigos": [],
            "mais_recentes": [],
            "por_plataforma": {},
            "por_genero": {},
        }

    ano_minimo = min(registro["Ano"] for registro in registros)
    ano_maximo = max(registro["Ano"] for registro in registros)

    return {
        "quantidade": len(registros),
        "media_notas": mean(registro["Nota numérica"] for registro in registros),
        "ano_minimo": ano_minimo,
        "ano_maximo": ano_maximo,
        "mais_antigos": [registro["Título"] for registro in registros if registro["Ano"] == ano_minimo],
        "mais_recentes": [registro["Título"] for registro in registros if registro["Ano"] == ano_maximo],
        "por_plataforma": dict(Counter(registro["Plataforma"] for registro in registros).most_common()),
        "por_genero": dict(Counter(registro["Gênero"] for registro in registros).most_common()),
    }
