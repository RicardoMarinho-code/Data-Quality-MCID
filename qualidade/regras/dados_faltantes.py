# -*- coding: utf-8 -*-
"""Regra: dados faltantes.

A coluna mcmv_ogu_38_qtd_entregues_2023 nao pode ficar vazia.
"""

from .. import config
from ..ocorrencia import Ocorrencia

NOME = "Dado faltante"

# Colunas obrigatorias (sem preenchimento = ocorrencia).
COLUNAS_OBRIGATORIAS = (config.COL_QTD_ENTREGUES_2023,)


def verificar(linhas, colunas):
    ocorrencias = []
    for col in COLUNAS_OBRIGATORIAS:
        for n, row in linhas:
            valor = (row.get(col) or "").strip()
            if valor == "":
                ocorrencias.append(Ocorrencia(
                    NOME, n, col, "(vazio)",
                    "campo obrigatorio sem preenchimento"))
    return ocorrencias
