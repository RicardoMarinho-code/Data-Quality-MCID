# Qualidados-MCID

Sistema simples de **qualidade de dados** para a planilha do CDV / MCMV-OGU.
Cada regra de qualidade fica em seu proprio arquivo e o nome da planilha do
governo e configurado via `.env`.

## Instalacao

```bash
pip install -r requirements.txt
```

## Configuracao

Copie o modelo e ajuste o nome da planilha:

```bash
cp .env.example .env
```

`.env`:

```
ARQUIVO_DADOS=Amostra de Dados.csv
ARQUIVO_RELATORIO=relatorio_qualidade.csv
TOLERANCIA_VALOR=1.0
```

> O `.env` esta no `.gitignore` (contem o nome da planilha do governo).

## Uso

```bash
python main.py                       # usa ARQUIVO_DADOS do .env
python main.py "outra planilha.csv"  # sobrescreve o arquivo
```

Saida: resumo no console + `relatorio_qualidade.csv` detalhado
(colunas: `regra; linha; coluna; valor; detalhe`).

## Estrutura

```
.
├── main.py                  # ponto de entrada (CLI + resumo)
├── .env / .env.example      # nome da planilha e parametros
├── requirements.txt
└── qualidade/
    ├── config.py            # le o .env e nomes de colunas
    ├── io_dados.py          # leitura do CSV / gravacao do relatorio
    ├── ocorrencia.py        # dataclass Ocorrencia
    ├── utils.py             # parse de numero BR, normalizacao de nome
    ├── executor.py          # orquestra as regras
    └── regras/
        ├── __init__.py                 # registro das regras (REGRAS)
        ├── consistencia_valor.py       # total = original + aporte
        ├── marcadores_erro.py          # #N/D, #NOME?, #VALOR! ...
        ├── unicidade_empreendimento.py # nomes duplicados
        ├── booleanos.py                # col 36/37: Sim/Nao e nao-vazio
        └── dados_faltantes.py          # col 38 obrigatoria
```

## Regras

| Regra | Descricao |
|---|---|
| Consistencia valor total | `val_contratado_total` = `original` + `aporte_adicional` (tolerancia `TOLERANCIA_VALOR`) |
| Marcador de erro | Procura `#N/D`, `#NOME?`, `#VALOR!`, `#REF!`, `#DIV/0!` etc. em qualquer celula |
| Unicidade empreendimento | Empreendimentos com o mesmo nome (normalizado) |
| Booleano vazio/invalido | Colunas 36 e 37 devem ser `Sim`/`Nao` e nao-vazias |
| Dado faltante | Coluna 38 (`qtd_entregues_2023`) obrigatoria |

## Resultado da amostra

Execucao sobre `Amostra de Dados.csv` (5.859 registros, 43 colunas):

| Regra | Ocorrencias |
|---|---|
| Consistencia valor total | 0 |
| Marcador de erro (#ND/#NOME) | 0 |
| Unicidade empreendimento | 296 |
| Booleano vazio (col 36/37) | 18 |
| Dado faltante (col 38) | 45 |
| **TOTAL** | **359** |

## Como adicionar uma nova regra

1. Crie `qualidade/regras/minha_regra.py` com uma funcao
   `verificar(linhas, colunas)` que retorna uma lista de `Ocorrencia`.
2. Registre-a em `qualidade/regras/__init__.py` (lista `REGRAS`).

> **Nota sobre o valor total:** a especificacao original mencionava subtracao,
> mas os dados seguem a soma (`aporte ADICIONAL` acrescenta ao total). A regra
> usa soma; por isso a amostra retorna 0 inconsistencias.
