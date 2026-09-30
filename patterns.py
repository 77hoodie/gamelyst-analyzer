"""Expressões regulares avaliadas pelo Gamelyst Analyzer.

As expressões deste módulo são a fonte única usada pela aplicação e pelos testes.
A validação completa é feita com ``re.fullmatch``; por isso, os padrões não
precisam de ``^`` e ``$``.
"""

PATTERNS = {
    "TITULO": r"[A-Za-z0-9À-ÖØ-öø-ÿ]([A-Za-z0-9À-ÖØ-öø-ÿ :'\-!?.,&()]*[A-Za-z0-9À-ÖØ-öø-ÿ:'\-!?.,&()])?",
    "PLATAFORMA": r"(PC|PS[1-5]|Xbox (One|Series X/S)|Nintendo Switch|Android|iOS)",
    "ANO": r"(19[5-9][0-9]|20[0-2][0-9])",
    "GENERO": r"(RPG|Ação|Aventura|Estratégia|Esportes|Simulação|Terror|Puzzle|Luta|FPS|Corrida|Sandbox|Roguelike|Metroidvania|Sobrevivência)(/(RPG|Ação|Aventura|Estratégia|Esportes|Simulação|Terror|Puzzle|Luta|FPS|Corrida|Sandbox|Roguelike|Metroidvania|Sobrevivência))?",
    "NOTA": r"(10(\.0)?|[0-9](\.[0-9])?)/10",
}

PATTERN_IDS = {
    "TITULO": "ER-01",
    "PLATAFORMA": "ER-02",
    "ANO": "ER-03",
    "GENERO": "ER-04",
    "NOTA": "ER-05",
}

PATTERN_NAMES = {
    "TITULO": "Título",
    "PLATAFORMA": "Plataforma",
    "ANO": "Ano",
    "GENERO": "Gênero",
    "NOTA": "Nota",
}

PLATFORMS = (
    "PC",
    "PS1",
    "PS2",
    "PS3",
    "PS4",
    "PS5",
    "Xbox One",
    "Xbox Series X/S",
    "Nintendo Switch",
    "Android",
    "iOS",
)

GENRES = (
    "RPG",
    "Ação",
    "Aventura",
    "Estratégia",
    "Esportes",
    "Simulação",
    "Terror",
    "Puzzle",
    "Luta",
    "FPS",
    "Corrida",
    "Sandbox",
    "Roguelike",
    "Metroidvania",
    "Sobrevivência",
)

FIELD_TO_PATTERN = {
    "Título": "TITULO",
    "Plataforma": "PLATAFORMA",
    "Ano": "ANO",
    "Gênero": "GENERO",
    "Nota": "NOTA",
}
