# -*- coding: utf-8 -*-
"""Regra: marcadores de erro de planilha (#N/D, #NOME?, etc.).

Varre todas as celulas procurando marcadores tipicos de erro do Excel pt-BR/en.
"""

import re

from ..ocorrencia import Ocorrencia

NOME = "Marcador de erro"

# Marcadores tipicos: #N/D, #ND, #NOME?, #VALOR!, #REF!, #DIV/0!, #NULO!, #NUM!, #N/A
PADRAO_ERRO = re.compile(
    r"#N/D|#ND|#NOME\??|#VALOR!?|#REF!?|#DIV/0!?|#NULO!?|#NUM!?|#N/A",
    re.IGNORECASE,
)


def verificar(linhas, colunas):
    ocorrencias = []
    for n, row in linhas:
        for col in colunas:
            valor = row.get(col) or ""
            achado = PADRAO_ERRO.search(valor)
            if achado:
                ocorrencias.append(Ocorrencia(
                    NOME, n, col, valor.strip(),
                    f"contem '{achado.group(0)}'"))
    return ocorrencias
