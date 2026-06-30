# -*- coding: utf-8 -*-
"""Regra: unicidade de empreendimentos.

Aponta empreendimentos com o mesmo nome (possivel duplicidade).
"""

from collections import defaultdict

from .. import config
from ..ocorrencia import Ocorrencia
from ..utils import normalizar_chave

NOME = "Unicidade empreendimento"


def verificar(linhas, colunas):
    ocorrencias = []
    indice = defaultdict(list)
    for n, row in linhas:
        chave = normalizar_chave(row.get(config.COL_NOME_EMPREENDIMENTO))
        if chave:
            indice[chave].append((n, (row.get(config.COL_NOME_EMPREENDIMENTO) or "").strip()))

    for chave, duplicados in indice.items():
        if len(duplicados) > 1:
            numeros = [str(n) for n, _ in duplicados]
            nome = duplicados[0][1]
            for n, _ in duplicados:
                ocorrencias.append(Ocorrencia(
                    NOME, n, config.COL_NOME_EMPREENDIMENTO, nome,
                    f"{len(duplicados)} ocorrencias do mesmo nome "
                    f"(linhas {', '.join(numeros)})"))
    return ocorrencias
