# -*- coding: utf-8 -*-
"""Orquestra a execucao das regras e a geracao do relatorio."""

from collections import defaultdict

from . import config, io_dados
from .regras import REGRAS


def executar(arquivo=None, relatorio=None):
    """Roda todas as regras sobre o arquivo e grava o relatorio.

    Retorna a lista de ocorrencias e um resumo {regra: quantidade}.
    """
    arquivo = arquivo or config.ARQUIVO_DADOS
    relatorio = relatorio or config.ARQUIVO_RELATORIO

    colunas, linhas = io_dados.carregar(arquivo)

    ocorrencias = []
    for regra in REGRAS:
        ocorrencias += regra(linhas, colunas)

    resumo = defaultdict(int)
    for o in ocorrencias:
        resumo[o.regra] += 1

    io_dados.gravar_relatorio(ocorrencias, relatorio)
    return ocorrencias, resumo, len(linhas), len(colunas)
