# -*- coding: utf-8 -*-
"""Leitura da planilha e gravacao do relatorio de qualidade."""

import csv
import io
import os

from . import config
from .utils import normalizar_numero_br


def carregar(arquivo):
    """Le o CSV ou Excel e retorna (colunas, linhas).

    'linhas' e uma lista de tuplas (numero_da_linha_no_arquivo, dict),
    com os cabecalhos ja sem espacos em branco nas pontas.
    """
    is_excel = False
    try:
        with open(arquivo, "rb") as f:
            header = f.read(8)
            is_excel = header.startswith(b"PK\x03\x04") or header.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1")
    except Exception:
        pass

    if is_excel or os.path.splitext(arquivo)[1].lower() in (".xlsx", ".xls"):
        import pandas as pd
        df = pd.read_excel(arquivo, dtype=str, keep_default_na=False)
        colunas = [c.strip() for c in df.columns]
        linhas = []
        for i, row in enumerate(df.iterrows(), start=2):  # linha 1 = cabecalho
            # row e uma tupla (index, Series). O Excel entrega numeros como texto
            # americano ('25029745.59'); normalizamos para o formato brasileiro
            # para a limpeza numerica das regras funcionar.
            limpo = {
                k.strip(): normalizar_numero_br(v)
                for k, v in row[1].items()
                if k is not None
            }
            linhas.append((i, limpo))
        return colunas, linhas
    else:
        # CSV canonico: UTF-8 com BOM. Fallback para latin-1 (cp1252), comum em
        # arquivos brasileiros legados. Decodifica os bytes de uma vez (o erro
        # de UTF-8 pode ocorrer no meio do arquivo, nao so no inicio); latin-1
        # decodifica qualquer byte, servindo de fallback garantido.
        with open(arquivo, "rb") as fb:
            bruto = fb.read()
        try:
            texto = bruto.decode("utf-8-sig")
        except UnicodeDecodeError:
            texto = bruto.decode("latin-1")
        leitor = csv.DictReader(io.StringIO(texto), delimiter=config.DELIMITADOR)
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
