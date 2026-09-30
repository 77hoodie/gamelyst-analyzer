from parser import processar_linhas, processar_texto


def test_registro_completo_valido():
    validos, invalidos = processar_texto("Hades | PC | 2020 | Roguelike | 9.5/10")
    assert len(validos) == 1
    assert invalidos == []
    assert validos[0]["Título"] == "Hades"
    assert validos[0]["Nota numérica"] == 9.5


def test_espacos_externos_sao_normalizados():
    validos, invalidos = processar_texto("  Hades   |   PC | 2020 | Roguelike | 9.5/10  ")
    assert len(validos) == 1
    assert invalidos == []
    assert validos[0]["Título"] == "Hades"


def test_registro_com_quatro_campos():
    validos, invalidos = processar_texto("Hades | PC | 2020 | Roguelike")
    assert validos == []
    assert invalidos[0]["Campos inválidos"] == "Estrutura"


def test_registro_com_seis_campos():
    validos, invalidos = processar_texto("Hades | PC | 2020 | Roguelike | 9.5/10 | extra")
    assert validos == []
    assert invalidos[0]["Campos inválidos"] == "Estrutura"


def test_multiplos_erros_sao_reportados():
    validos, invalidos = processar_texto("@Hades | PS6 | 1949 | desconhecido | 11/10")
    assert validos == []
    assert "Título" in invalidos[0]["Campos inválidos"]
    assert "Plataforma" in invalidos[0]["Campos inválidos"]
    assert "Ano" in invalidos[0]["Campos inválidos"]
    assert "Gênero" in invalidos[0]["Campos inválidos"]
    assert "Nota" in invalidos[0]["Campos inválidos"]


def test_linhas_vazias_sao_ignoradas_mantendo_numero_fisico():
    validos, invalidos = processar_linhas(["", "Hades | PC | 2020 | Roguelike | 9.5/10"])
    assert len(validos) == 1
    assert invalidos == []
    assert validos[0]["Linha"] == 2


def test_texto_vazio():
    assert processar_texto("") == ([], [])
    assert processar_texto("   \n\n") == ([], [])


def test_catalogo_misto():
    texto = "\n".join(
        [
            "Hades | PC | 2020 | Roguelike | 9.5/10",
            "Portal 2 | PlayStation 3 | 2011 | Puzzle | 9.5/10",
            "Celeste | Nintendo Switch | 2018 | Plataforma | 9.2/10",
        ]
    )
    validos, invalidos = processar_texto(texto)
    assert len(validos) == 1
    assert len(invalidos) == 2
