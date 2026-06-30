# -*- coding: utf-8 -*-
"""Leitura da planilha e gravacao do relatorio de qualidade."""

import csv

from . import config


def carregar(arquivo):
    """Le o CSV (UTF-8 com BOM, delimitador ';') e retorna (colunas, linhas).

    'linhas' e uma lista de tuplas (numero_da_linha_no_arquivo, dict),
    com os cabecalhos ja sem espacos em branco nas pontas.
    """
    with open(arquivo, "r", encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f, delimiter=config.DELIMITADOR)
        colunas = [c.strip() for c in leitor.fieldnames]
        linhas = []
        for i, row in enumerate(leitor, start=2):  # linha 1 = cabecalho
            limpo = {k.strip(): v for k, v in row.items() if k is not None}
            linhas.append((i, limpo))
    return colunas, linhas


def gravar_relatorio(ocorrencias, caminho):
    """Grava as ocorrencias em um CSV (delimitador ';', UTF-8 com BOM)."""
    with open(caminho, "w", encoding="utf-8-sig", newline="") as f:
        escritor = csv.writer(f, delimiter=config.DELIMITADOR)
        escritor.writerow(["regra", "linha", "coluna", "valor", "detalhe"])
        for o in ocorrencias:
            escritor.writerow([o.regra, o.linha, o.coluna, o.valor, o.detalhe])
