# -*- coding: utf-8 -*-
"""Funcoes utilitarias compartilhadas pelas regras."""

import re


def parse_numero(texto):
    """Converte numero em formato brasileiro ('1.234,56', ' - ') para float.

    Retorna None quando o campo esta vazio ou nao representa um numero.
    O traco ' - ' usado no arquivo representa zero.
    """
    if texto is None:
        return None
    t = texto.strip()
    if t == "":
        return None
    if t == "-":
        return 0.0
    # Remove separador de milhar (.) e troca a virgula decimal por ponto.
    t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def normalizar_chave(texto):
    """Normaliza nome (maiusculas, espacos colapsados) para comparacao."""
    return re.sub(r"\s+", " ", (texto or "").strip()).upper()
