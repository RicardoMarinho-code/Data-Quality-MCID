# -*- coding: utf-8 -*-
"""Regra: consistencia do valor contratado total.

[valor contratado total] deve ser igual a [original] + [aporte adicional].

Observacao: a especificacao mencionava subtracao, mas os dados do arquivo
seguem a soma (o aporte ADICIONAL acrescenta ao total).
"""

from .. import config
from ..ocorrencia import Ocorrencia
from ..utils import parse_numero

NOME = "Consistencia valor total"


def verificar(linhas, colunas):
    ocorrencias = []
    for n, row in linhas:
        original = parse_numero(row.get(config.COL_VAL_ORIGINAL))
        aporte = parse_numero(row.get(config.COL_VAL_APORTE))
        total = parse_numero(row.get(config.COL_VAL_TOTAL))
        if original is None or total is None:
            continue
        esperado = original + (aporte or 0.0)
        if abs(esperado - total) > config.TOLERANCIA_VALOR:
            ocorrencias.append(Ocorrencia(
                NOME, n, config.COL_VAL_TOTAL, f"{total:.2f}",
                f"esperado {esperado:.2f} (orig {original:.2f} + aporte "
                f"{(aporte or 0.0):.2f}); diferenca {esperado - total:.2f}"))
    return ocorrencias
