"""Validação léxica dos campos do catálogo."""

import re
from patterns import PATTERNS

ERROR_MESSAGES = {
    "TITULO": "Título inválido.",
    "PLATAFORMA": "Plataforma não reconhecida.",
    "ANO": "Ano fora do intervalo aceito (1950 a 2029).",
    "GENERO": "Gênero não reconhecido.",
    "NOTA": "Nota inválida. Use valores de 0/10 a 10/10, com no máximo uma casa decimal.",
}


def validar_campo(valor: str, chave: str) -> bool:
    """Retorna True quando ``valor`` pertence à linguagem da ER indicada.

    Nenhuma normalização é feita aqui. A função valida exatamente a cadeia
    recebida, preservando a equivalência entre o padrão, os testes e a
    descrição formal.
    """
    if chave not in PATTERNS:
        raise KeyError(f"Expressão desconhecida: {chave}")
    if not isinstance(valor, str) or valor == "":
        return False
    return re.fullmatch(PATTERNS[chave], valor) is not None


def erros_do_registro(titulo: str, plataforma: str, ano: str, genero: str, nota: str) -> dict[str, str]:
    """Retorna os campos inválidos e suas mensagens."""
    valores = {
        "TITULO": titulo,
        "PLATAFORMA": plataforma,
        "ANO": ano,
        "GENERO": genero,
        "NOTA": nota,
    }
    return {
        chave: ERROR_MESSAGES[chave]
        for chave, valor in valores.items()
        if not validar_campo(valor, chave)
    }
