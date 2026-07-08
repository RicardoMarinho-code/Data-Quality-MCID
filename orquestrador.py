# -*- coding: utf-8 -*-
"""Ponte que roda as regras de qualidade/ e regras_R/ juntas.

Produz uma tabela larga consolidada: as colunas originais do arquivo mais uma
coluna de resultado por regra (Sucesso/Insucesso, linha a linha).

Uso (a partir da raiz do repositorio):
    python orquestrador.py
    python orquestrador.py "outra planilha.csv"
"""

import os
import sys

import pandas as pd

from qualidade import config
from qualidade.regras import REGRAS as REGRAS_QUALIDADE
from qualidade.utils import normalizar_data_br, normalizar_numero_br
from regras_R import REGRAS_R

SAIDA = "relatorio_consolidado.csv"


def carregar_df(arquivo):
    """Le a base de dados como texto (as regras fazem a propria conversao).

    Aceita CSV (formato canonico: ';' + UTF-8 com BOM) ou Excel (.xlsx/.xls),
    conforme a extensao ou assinatura do arquivo. Le tudo como string para
    as regras aplicarem sua limpeza numerica no formato brasileiro.
    """
    is_excel = False
    try:
        with open(arquivo, "rb") as f:
            header = f.read(8)
            is_excel = header.startswith(b"PK\x03\x04") or header.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1")
    except Exception:
        pass

    ext = os.path.splitext(arquivo)[1].lower()
    if is_excel or ext in (".xlsx", ".xls"):

        df = pd.read_excel(arquivo, dtype=str, keep_default_na=False)
        for c in df.columns:
            df[c] = df[c].map(normalizar_numero_br).map(normalizar_data_br)
    else:

        leitura = dict(
            sep=config.DELIMITADOR,
            dtype=str,
            keep_default_na=False,
        )
        try:
            df = pd.read_csv(arquivo, encoding="utf-8-sig", **leitura)
        except UnicodeDecodeError:
            df = pd.read_csv(arquivo, encoding="latin-1", **leitura)

    df.columns = df.columns.str.strip()

    if not any(str(c).startswith("mcmv_ogu_") for c in df.columns):
        raise ValueError(
            f"O arquivo '{arquivo}' nao parece ser a base MCMV-OGU: nenhuma "
            f"coluna 'mcmv_ogu_*' encontrada. Confira ARQUIVO_DADOS no .env - "
            f"ele deve apontar para os DADOS de contratacao, nao para o "
            f"dicionario de metadados."
        )
    return df


def _linhas_colunas(df):
    """Constroi (colunas, linhas) no formato esperado pelas regras de qualidade.

    Deriva do PROPRIO df para garantir o alinhamento de linhas: a posicao i no
    df corresponde a linha i + 2 no arquivo (linha 1 = cabecalho).
    """
    colunas = list(df.columns)
    linhas = [
        (i + 2, {c: (v if v != "" else None) for c, v in row.items()})
        for i, (_, row) in enumerate(df.iterrows())
    ]
    return colunas, linhas


def aplicar_qualidade(df):
    """Roda as regras de qualidade/ e vira cada uma numa coluna Sucesso/Insucesso."""
    colunas, linhas = _linhas_colunas(df)
    for verificar in REGRAS_QUALIDADE:
        nome = getattr(
            sys.modules[verificar.__module__],
            "NOME",
            verificar.__module__.split(".")[-1],
        )
        ocorrencias = verificar(linhas, colunas)

        posicoes_ruins = {o.linha - 2 for o in ocorrencias}
        df[f"Resultado_{nome}"] = [
            "Insucesso" if i in posicoes_ruins else "Sucesso"
            for i in range(len(df))
        ]
    return df


def executar(arquivo=None):
    """Roda todas as regras e grava a tabela larga consolidada. Retorna o df."""
    arquivo = arquivo or config.ARQUIVO_DADOS

    df = carregar_df(arquivo)

    for _rotulo, regra in REGRAS_R:
        df = regra(df)

    df = aplicar_qualidade(df)

    df.to_csv(SAIDA, sep=config.DELIMITADOR, index=False, encoding="utf-8-sig")
    return df


def main():
    arquivo = sys.argv[1] if len(sys.argv) > 1 else config.ARQUIVO_DADOS
    print(f"Lendo: {arquivo}")

    try:
        df = executar(arquivo)
    except ImportError as e:
        print(f"\nERRO: dependencia faltando ({e}).")
        print("Instale as dependencias no Python que voce esta usando:")
        print("    python -m pip install -r requirements.txt")
        sys.exit(1)
    except (ValueError, FileNotFoundError) as e:
        print(f"\nERRO: {e}")
        sys.exit(1)

    print(f"\nConsolidado gravado em: {SAIDA} ({len(df)} registros)")
    print("=" * 60)
    print("RESUMO DE INSUCESSOS POR REGRA")
    print("=" * 60)
    colunas_resultado = [c for c in df.columns if c.startswith("Resultado")]
    for col in colunas_resultado:
        n = int((df[col] == "Insucesso").sum())
        print(f"  {col:.<50} {n:>6}")
    print("=" * 60)


if __name__ == "__main__":
    main()
