"""
Componentes reutilizáveis para a interface

Alguns links:
- Emojis: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

Autor: Gabriel
Data de criação: 22/11/2026
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import dashboard.dados as dados
import dashboard.formatacao as fmt
import dashboard.graficos.grafs as graficos

import dashboard.graficos.configs_grafs as cfg


CONFIG_PLOTLY = {"displayModeBar": False}


def renderizar_grafico(fig: go.Figure):
    altura = fig.to_dict().get("layout", {}).get("height")
    if altura is None:
        fig.update_layout(height=cfg.ALTURA_GRAFICO)

    st.plotly_chart(fig, theme=None, config=CONFIG_PLOTLY)


def exibir_mensagem_sem_dados():
    st.caption(f":material/warning: Sem dados para exibir")


def exibir_valor_mais_recente_destaque(df: pd.DataFrame, rotulo: str, unidade: str = "", casas: int = 0):
    df = df.dropna(subset=["valor"]).sort_values("ano")

    if df.empty:
        exibir_mensagem_sem_dados()
        return

    ano = int(df["ano"].iloc[-1])
    valor = df["valor"].iloc[-1]

    st.metric(
        label=f"{rotulo} - {ano}",
        value=fmt.com_unidade(valor, unidade, casas)
    )

def exibir_total_destaque(df: pd.DataFrame, rotulo: str, unidade: str = "", casas: int = 0):
    totais = dados.filtrar_totais(df)
    exibir_valor_mais_recente_destaque(totais, rotulo, unidade, casas)


def exibir_barra_percentual(df: pd.DataFrame, rotulo: str):
    df = df.dropna(subset=["valor"]).sort_values("ano")

    if df.empty:
        exibir_mensagem_sem_dados()
        return

    ano = int(df["ano"].iloc[-1])
    valor = df["valor"].iloc[-1]

    st.metric(
        label=f"{rotulo} - {ano}",
        value=fmt.percentual(valor)
    )

    st.progress(min(valor / 100, 1.0))

# ANOS
def slider_anos(df: pd.DataFrame, key: str) -> pd.DataFrame:
    anos = sorted(df["ano"].dropna().unique())

    if not anos:
        return df

    inicio, fim = st.select_slider(
        "Período",
        options=anos,
        value=(anos[0], anos[-1]),
        key=key,
        label_visibility="collapsed"
    )

    return df[df["ano"].between(inicio, fim)]

def dropdown_anos(df: pd.DataFrame, key: str) -> int:
    anos = sorted(df["ano"].dropna().unique())

    return int(st.selectbox(
        "Ano",
        options=anos,
        index=len(anos) - 1,
        key=key,
        label_visibility="collapsed"
    ))

def botoes_escolha(rotulo: str, opcoes: list[str], key: str) -> str:
    return st.segmented_control(
        rotulo,
        opcoes,
        default=opcoes[0],
        required=True,
        key=key,
        label_visibility="collapsed"
    )



def explorar_por_classificacao(df: pd.DataFrame, dimensoes: dict[str, str], key: str, unidade: str = "", casas: int = 1):
    escolha = botoes_escolha("Detalhar por", list(dimensoes), key=key)

    coluna = dimensoes[escolha]

    dtf = dados.filtrar_totais(df, exceto=(coluna,))
    dtf = dados.sem_total(dtf, coluna)
    dtf = dtf.dropna(subset=["valor"])

    if dtf.empty:
        exibir_mensagem_sem_dados()
        return

    renderizar_grafico(
        graficos.grafico_barras_horizontal(dtf, y=coluna, unidade=unidade, casas=casas, ordenar=False)
    )

def comparar_composicao(df: pd.DataFrame, partes: str, dimensoes: dict[str, str], key: str):
    escolha = botoes_escolha("Comparar por", list(dimensoes), key=key)
    coluna = dimensoes[escolha]

    dtf = dados.filtrar_totais(df, exceto=(coluna, partes))  # mantém o 'Total' da coluna escolhida (1ª barra)
    dtf = dados.sem_total(dtf, partes)
    dtf = dtf.dropna(subset=["valor"])

    if dtf.empty:
        exibir_mensagem_sem_dados()
        return

    renderizar_grafico(
        graficos.grafico_barras_horizontais_composicao(dtf, linhas=coluna, partes=partes)
    )
