"""
Leitura dos dados no Banco de Dados e metadados dos indicadores (arquivo toml)

Autor: Gabriel
Data de criação: 22/11/2026
"""

import tomllib
from pathlib import Path

import pandas as pd
import sqlalchemy
import streamlit as st

import db.db as db

ARQUIVO_METADADOS = Path(__file__).parent.parent / "indicadores.toml"
TEMPO_CACHE = "2h"

def carregar_metadados() -> list[dict]:
    with open(ARQUIVO_METADADOS, "rb") as f:
        return tomllib.load(f)["indicador"]


@st.cache_data(ttl=TEMPO_CACHE, show_spinner=False)
def get_tabelas_existentes() -> set[str]:
    return set(sqlalchemy.inspect(db.get_engine()).get_table_names())


@st.cache_data(ttl=TEMPO_CACHE, show_spinner="Carregando dados...")
def carregar_tabela(nome_tabela: str) -> pd.DataFrame:
    return pd.read_sql_table(nome_tabela, db.get_engine())


def filtrar(df: pd.DataFrame, **condicoes) -> pd.DataFrame:
    for coluna, valor in condicoes.items():
        # se for uma lista, precisamos usar .isin
        if isinstance(valor, list):
            df = df[df[coluna].isin(valor)]
        else:
            # se for so um num, podemos usar == mesmo
            df = df[df[coluna] == valor]

    return df.copy()


def filtrar_totais(df: pd.DataFrame, exceto: tuple[str, ...] = ()) -> pd.DataFrame:
    # As tabelas estao no formato longo, e algumas ja incluem uma categoria 'Total'. Tem q cuidar com isso, pois pode alterar resultados de somas.
    for coluna in df.columns:
        if coluna.startswith("categoria_") and coluna not in exceto:
            df = df[df[coluna] == "Total"]

    return df

def sem_total(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    return df[df[coluna] != "Total"]


def sem_indeterminados(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    # Remove categorias do tipo 'Não determinado', 'Idade ignorada', ...
    indeterm = df[coluna].str.contains("determinad|ignorad", case=False, na=False)

    return df[~indeterm]


def so_secoes_cnae(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    # A CNAE vem em vários níveis: seção ("A ..."), divisão ("01 ..."), grupo ("01.1 ...") e classe ("01.11-3 ...").
    # Somar níveis diferentes conta a mesma atividade várias vezes.
    eh_secao = df[coluna].str.match(r"^[A-Z] ")
    return df[eh_secao]
