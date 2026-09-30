import pytest

from validators import validar_campo


@pytest.mark.parametrize(
    "chain",
    [
        "A",  # caso-limite: um único símbolo
        "FIFA 23",
        "God of War: Ragnarök",
        "Pokémon: Let's Go, Pikachu!",
        "Mario & Luigi: Brothership",
        "NieR:Automata",
        "Plants vs. Zombies",
        "WarioWare: Move It!",
    ],
)
def test_er01_accept(chain):
    assert validar_campo(chain, "TITULO")


@pytest.mark.parametrize(
    "chain",
    [
        "",  # caso-limite: cadeia vazia
        " Game",
        "Game ",
        "@GameTitle",
        "#Doom",
        "Game|PC",
        "   ",
    ],
)
def test_er01_reject(chain):
    assert not validar_campo(chain, "TITULO")


@pytest.mark.parametrize(
    "chain",
    ["PC", "PS1", "PS5", "Xbox One", "Xbox Series X/S", "Nintendo Switch", "Android", "iOS"],
)
def test_er02_accept(chain):
    assert validar_campo(chain, "PLATAFORMA")


@pytest.mark.parametrize(
    "chain",
    ["", "pc", "PS0", "PS6", "PS 5", "PlayStation 5", "Xbox 360", "Atari 2600"],
)
def test_er02_reject(chain):
    assert not validar_campo(chain, "PLATAFORMA")


@pytest.mark.parametrize(
    "chain",
    ["1950", "1959", "1999", "2000", "2015", "2026", "2029"],
)
def test_er03_accept(chain):
    assert validar_campo(chain, "ANO")


@pytest.mark.parametrize(
    "chain",
    ["", "1949", "2030", "202", "20200", "20A6", "2015.0", "202٩"],
)
def test_er03_reject(chain):
    assert not validar_campo(chain, "ANO")


@pytest.mark.parametrize(
    "chain",
    [
        "RPG",
        "Ação",
        "FPS",
        "Roguelike",
        "Metroidvania",
        "Sobrevivência",
        "Ação/Aventura",
        "RPG/Ação",
    ],
)
def test_er04_accept(chain):
    assert validar_campo(chain, "GENERO")


@pytest.mark.parametrize(
    "chain",
    ["", "rpg", "Acao", "Hack and Slash", "Ação/", "/Aventura", "RPG/Ação/Aventura", "Esporte"],
)
def test_er04_reject(chain):
    assert not validar_campo(chain, "GENERO")


@pytest.mark.parametrize(
    "chain",
    ["0/10", "0.0/10", "4/10", "7.5/10", "9.9/10", "10/10", "10.0/10"],
)
def test_er05_accept(chain):
    assert validar_campo(chain, "NOTA")


@pytest.mark.parametrize(
    "chain",
    ["", "-1/10", "10.1/10", "11/10", "9,5/10", "9.55/10", "8.5", "010/10"],
)
def test_er05_reject(chain):
    assert not validar_campo(chain, "NOTA")
