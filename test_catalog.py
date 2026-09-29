import re
import pytest

PATTERNS = {
    "ER-01": r"^[a-zA-Z0-9\u00C0-\u00FF][a-zA-Z0-9\u00C0-\u00FF\ \:\-\'\!]*$",
    "ER-02": r"^(PC|PS1|PS2|PS3|PS4|PS5|Xbox One|Xbox Series X/S|Nintendo Switch|Android|iOS)$",
    "ER-03": r"^(19[5-9]\d|20[0-2]\d)$",
    "ER-04": r"^(RPG|Ação|Aventura|Estratégia|Esportes|Simulação|Terror|Puzzle|Luta)$",
    "ER-05": r"^(10(\.0)?|[0-9](\.[0-9])?)\/10$"
}

# --- ER-01: Título ---
@pytest.mark.parametrize("chain", ["God of War: Ragnarök", "FIFA 23", "A", "Half-Life 2: Episode Two", "Cyberpunk 2077!", "Devil May Cry 5"])
def test_er01_accept(chain): assert re.fullmatch(PATTERNS["ER-01"], chain) is not None

@pytest.mark.parametrize("chain", ["", " Space Invaders", "@GameTitle", "<script>", "#Doom", "   "])
def test_er01_reject(chain): assert re.fullmatch(PATTERNS["ER-01"], chain) is None

# --- ER-02: Plataforma ---
@pytest.mark.parametrize("chain", ["PC", "PS5", "Xbox Series X/S", "Nintendo Switch", "Android", "iOS"])
def test_er02_accept(chain): assert re.fullmatch(PATTERNS["ER-02"], chain) is not None

@pytest.mark.parametrize("chain", ["pc", "PlayStation 5", "Xbox 360", "", "PS 5", "Atari 2600"])
def test_er02_reject(chain): assert re.fullmatch(PATTERNS["ER-02"], chain) is None

# --- ER-03: Ano ---
@pytest.mark.parametrize("chain", ["1950", "1998", "2000", "2015", "2026", "2029"])
def test_er03_accept(chain): assert re.fullmatch(PATTERNS["ER-03"], chain) is not None

@pytest.mark.parametrize("chain", ["1949", "2030", "98", "2015.0", "ano2020", ""])
def test_er03_reject(chain): assert re.fullmatch(PATTERNS["ER-03"], chain) is None

# --- ER-04: Gênero ---
@pytest.mark.parametrize("chain", ["RPG", "Ação", "Aventura", "Estratégia", "Terror", "Puzzle"])
def test_er04_accept(chain): assert re.fullmatch(PATTERNS["ER-04"], chain) is not None

@pytest.mark.parametrize("chain", ["rpg", "Acao", "FPS", "Ação/Aventura", "", "Esporte"])
def test_er04_reject(chain): assert re.fullmatch(PATTERNS["ER-04"], chain) is None

# --- ER-05: Nota ---
@pytest.mark.parametrize("chain", ["0.0/10", "0/10", "8.5/10", "9/10", "10/10", "10.0/10"])
def test_er05_accept(chain): assert re.fullmatch(PATTERNS["ER-05"], chain) is not None

@pytest.mark.parametrize("chain", ["10.1/10", "-1/10", "9,5/10", "8.5", "9.85/10", ""])
def test_er05_reject(chain): assert re.fullmatch(PATTERNS["ER-05"], chain) is None