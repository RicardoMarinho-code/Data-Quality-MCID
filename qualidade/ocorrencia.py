# -*- coding: utf-8 -*-
"""Representacao de uma ocorrencia (achado) de qualidade de dados."""

from dataclasses import dataclass


@dataclass
class Ocorrencia:
    """Um problema de qualidade encontrado em uma celula/linha.

    Attributes:
        regra: nome da regra que gerou o achado.
        linha: numero da linha no arquivo (1 = cabecalho).
        coluna: nome da coluna avaliada.
        valor: valor encontrado.
        detalhe: explicacao legivel do problema.
    """

    regra: str
    linha: int
    coluna: str
    valor: str
    detalhe: str
