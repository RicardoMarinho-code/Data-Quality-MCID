# -*- coding: utf-8 -*-
"""Registra as regras R01-R12 em REGRAS_R.

Os arquivos das regras tem espaco/hifen no nome (ex: "R01 - soma_...py"), o que
impede o import normal. Por isso cada modulo e carregado via importlib e a sua
funcao regra_N e exposta na lista ordenada REGRAS_R = [(rotulo, funcao), ...].
"""

import importlib.util
from pathlib import Path

_PASTA = Path(__file__).parent

# (rotulo, arquivo, funcao) - na ordem R01..R12
_DEFINICOES = [
    ("R01", "R01 - soma_val_contratado_total.py", "regra_1"),
    ("R02", "R02 - distrato_exige_quantidade.py", "regra_2"),
    ("R03", "R03 - quantidade_distratadas.py", "regra_3"),
    ("R04", "R04 - data_termino_ate_referencia.py", "regra_4"),
    ("R05", "R05 - colunas_da_ficha_presentes.py", "regra_5"),
    ("R06", "R06 - marcadores_de_erro.py", "regra_6"),
    ("R07", "R07 - preenchimento_obrigatorio.py", "regra_7"),
    ("R08", "R08 - desembolso_ano_ate_total.py", "regra_8"),
    ("R09", "R09 - desembolso_e_numerico.py", "regra_9"),
    ("R10", "R10 - datas_dentro_do_intervalo.py", "regra_10"),
    ("R11", "R11 - entregues_ate_unidades.py", "regra_11"),
    ("R12", "R12 - quantidade_de_vigentes.py", "regra_12"),
]


def _carregar(arquivo, funcao):
    """Carrega dinamicamente `funcao` do arquivo (com nome nao-importavel)."""
    spec = importlib.util.spec_from_file_location(arquivo, _PASTA / arquivo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return getattr(modulo, funcao)


REGRAS_R = [(rotulo, _carregar(arq, fn)) for rotulo, arq, fn in _DEFINICOES]
