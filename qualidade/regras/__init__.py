# -*- coding: utf-8 -*-
"""Registro central das regras de qualidade.

Para adicionar uma nova regra: crie um modulo neste pacote com uma funcao
`verificar(linhas, colunas)` que retorna uma lista de Ocorrencia e registre-a
na lista REGRAS abaixo.
"""

from . import (
    consistencia_valor,
    marcadores_erro,
    unicidade_empreendimento,
    booleanos,
    dados_faltantes,
)

# Ordem em que as regras sao executadas.
REGRAS = [
    consistencia_valor.verificar,
    marcadores_erro.verificar,
    unicidade_empreendimento.verificar,
    booleanos.verificar,
    dados_faltantes.verificar,
]
