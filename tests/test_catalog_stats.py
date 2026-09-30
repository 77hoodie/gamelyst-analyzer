from catalog_stats import calcular_resumo


def test_resumo_vazio():
    resumo = calcular_resumo([])
    assert resumo["quantidade"] == 0
    assert resumo["media_notas"] is None


def test_resumo_calcula_metricas():
    registros = [
        {"Título": "A", "Plataforma": "PC", "Ano": 2000, "Gênero": "RPG", "Nota numérica": 8.0},
        {"Título": "B", "Plataforma": "PC", "Ano": 2020, "Gênero": "Ação", "Nota numérica": 10.0},
        {"Título": "C", "Plataforma": "PS5", "Ano": 2020, "Gênero": "Ação", "Nota numérica": 9.0},
    ]
    resumo = calcular_resumo(registros)
    assert resumo["quantidade"] == 3
    assert resumo["media_notas"] == 9.0
    assert resumo["ano_minimo"] == 2000
    assert resumo["ano_maximo"] == 2020
    assert resumo["mais_antigos"] == ["A"]
    assert resumo["mais_recentes"] == ["B", "C"]
    assert resumo["por_plataforma"] == {"PC": 2, "PS5": 1}
