# -*- coding: utf-8 -*-
"""Regra: colunas booleanas (vigente / novo MCMV).

As colunas mcmv_ogu_36_bln_vigente e mcmv_ogu_37_bln_novo_mcmv devem conter
apenas Sim/Nao e nao podem ficar vazias.
"""

from .. import config
from ..ocorrencia import Ocorrencia

NOME = "Booleano"

COLUNAS_BOOLEANAS = (config.COL_BLN_VIGENTE, config.COL_BLN_NOVO_MCMV)


def verificar(linhas, colunas):
    ocorrencias = []
    for col in COLUNAS_BOOLEANAS:
        for n, row in linhas:
            valor = (row.get(col) or "").strip()
            if valor == "":
                ocorrencias.append(Ocorrencia(
                    "Booleano vazio", n, col, "(vazio)",
                    "campo booleano sem preenchimento"))
            elif valor.lower() not in config.VALORES_BOOLEANOS:
                ocorrencias.append(Ocorrencia(
                    "Booleano invalido", n, col, valor,
                    "valor fora do dominio {Sim, Nao}"))
    return ocorrencias
