# -*- coding: utf-8 -*-
"""Funcoes utilitarias compartilhadas pelas regras."""

import re

# Decimal em formato americano/Excel: um numero com PONTO decimal, ex '25029745.59'.
_RE_DECIMAL_US = re.compile(r"^-?\d+\.\d+$")

# Data ISO vinda de celula datetime do Excel: '2026-04-30' ou, com a hora de
# meia-noite grudada, '2026-04-30 00:00:00'.
_RE_DATA_ISO = re.compile(r"^(\d{4})-(\d{2})-(\d{2})(?: 00:00:00(?:\.0+)?)?$")


def normalizar_data_br(valor):
    """Converte data ISO do Excel ('2026-04-30 00:00:00') para o formato
    brasileiro sem hora ('30/04/2026').

    O Excel guarda datas como celulas datetime; lidas com dtype=str elas viram
    '2026-04-30 00:00:00', com a hora de meia-noite grudada, e ao abrir o CSV
    final o Excel exibe '30/04/2026 00:00'. So converte quando o valor e uma
    data ISO pura (com ou sem a hora 00:00:00); qualquer outro texto (nomes,
    numeros, datas ja em formato BR) passa intacto.
    """
    if isinstance(valor, str):
        m = _RE_DATA_ISO.match(valor)
        if m:
            ano, mes, dia = m.groups()
            return f"{dia}/{mes}/{ano}"
    return valor


def normalizar_numero_br(valor):
    """Converte um decimal americano ('25029745.59') para brasileiro ('25029745,59').

    O Excel guarda numeros como float; lidos como texto (dtype=str) eles viram
    string com PONTO decimal. A limpeza das regras assume formato brasileiro e
    REMOVE os pontos (tratando-os como separador de milhar), o que corromperia
    esses valores (25029745.59 viraria 2502974559, 100x maior). Trocando o ponto
    decimal por virgula ANTES, a limpeza das regras passa a funcionar.

    So altera celulas que sao um decimal americano puro; texto (nomes, datas,
    CNPJ) e inteiros passam intactos.
    """
    if isinstance(valor, str) and _RE_DECIMAL_US.match(valor):
        return valor.replace(".", ",")
    return valor


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
