# -*- coding: utf-8 -*-
"""Ponto de entrada do sistema de qualidade de dados - CDV / MCMV-OGU.

O nome da planilha vem do arquivo .env (ARQUIVO_DADOS). E possivel sobrescrever
passando o caminho como argumento:

    python main.py
    python main.py "outra planilha.csv"
"""

import sys

from qualidade import config
from qualidade.executor import executar


def main():
    arquivo = sys.argv[1] if len(sys.argv) > 1 else config.ARQUIVO_DADOS

    print(f"Lendo: {arquivo}")
    ocorrencias, resumo, n_linhas, n_colunas = executar(arquivo)
    print(f"Registros: {n_linhas} | Colunas: {n_colunas}\n")

    print("=" * 60)
    print("RESUMO DE QUALIDADE DE DADOS")
    print("=" * 60)
    if not resumo:
        print("Nenhuma ocorrencia encontrada. :)")
    else:
        for regra in sorted(resumo):
            print(f"  {regra:.<40} {resumo[regra]:>6}")
    print("-" * 60)
    print(f"  {'TOTAL DE OCORRENCIAS':.<40} {len(ocorrencias):>6}")
    print("=" * 60)
    print(f"\nRelatorio detalhado gravado em: {config.ARQUIVO_RELATORIO}")


if __name__ == "__main__":
    main()
