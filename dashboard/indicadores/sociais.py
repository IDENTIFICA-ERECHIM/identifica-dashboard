"""
Gráficos dos indicadores 29-48 (sociais)

Autor: Gabriel
Data de criação: 23/11/2026
"""

import pandas as pd
import streamlit as st

import dashboard.componentes as cmp
import dashboard.dados as dados
import dashboard.formatacao as fmt
import dashboard.graficos.grafs as graficos

CONDICOES_PRINCIPAIS = ["73554", "1055", "73553", "1058"]  # Próprio, Alugado, Cedido, Outra condição


def indicador_029(df: pd.DataFrame):
    # classificações: 1 sexo, 2 cor ou raça, 3 idade
    cmp.exibir_total_destaque(df, "Taxa de alfabetização (15+)", unidade="%", casas=1)

    dimensoes = {
        "Idade": "categoria_3",
        "Cor ou raça": "categoria_2",
        "Sexo": "categoria_1",
    }
    cmp.explorar_por_classificacao(df, dimensoes, key="ind029_dim", unidade="%")


def indicador_030(df: pd.DataFrame):
    # classificações: 1 sexo, 2 cor ou raça, 3 grupo de idade, 4 deficiência
    cmp.exibir_total_destaque(df, "Taxa de analfabetismo (15+)", unidade="%", casas=1)

    dimensoes = {
        "Grupo de idade": "categoria_3",
        "Deficiência": "categoria_4",
        "Cor ou raça": "categoria_2",
        "Sexo": "categoria_1",
    }
    cmp.explorar_por_classificacao(df, dimensoes, key="ind030_dim", unidade="%")


def indicador_031(df: pd.DataFrame):
    # classificações: 1 sexo, 2 cor ou raça, 3 grupo de idade
    dimensoes = {
        "Grupo de idade": "categoria_3",
        "Cor ou raça": "categoria_2",
        "Sexo": "categoria_1",
    }
    cmp.explorar_por_classificacao(df, dimensoes, key="ind031_dim", unidade="%")


def indicador_032(df: pd.DataFrame):
    # classificações: 1 sexo, 2 cor ou raça, 3 grupo de idade, 4 nível de instrução
    dimensoes = {
        "Grupo de idade": "categoria_3",
        "Sexo": "categoria_1",
        "Cor ou raça": "categoria_2",
    }
    d = dados.sem_indeterminados(df, "categoria_4")
    cmp.comparar_composicao(d, partes="categoria_4", dimensoes=dimensoes, key="ind032_dim")


def indicador_034(df: pd.DataFrame):
    cmp.exibir_valor_mais_recente_destaque(df, "Domicílios ocupados")


def indicador_035(df: pd.DataFrame):
    # classificações do responsável: 1 sexo, 2 cor ou raça, 3 grupo de idade
    cmp.exibir_total_destaque(df, "Média de moradores", unidade="pessoas", casas=2)

    dimensoes = {
        "Idade do responsável": "categoria_3",
        "Sexo do responsável": "categoria_1",
        "Cor ou raça do responsável": "categoria_2",
    }
    cmp.explorar_por_classificacao(df, dimensoes, key="ind035_dim", unidade="moradores", casas=2)


def indicador_036(df: pd.DataFrame):
    total = dados.filtrar(df, cod_variavel="381", categoria_1="Total")
    partes = dados.filtrar(df, nome_variavel="participacao_condicao_ocupacao",
                           cod_categoria_1=CONDICOES_PRINCIPAIS)

    # número total de domicílios no furo da rosca
    if total.empty:
        texto_central = ""
    else:
        texto_central = fmt.numero(total["valor"].sum()) + "<br>domicílios"

    cmp.renderizar_grafico(
        graficos.grafico_rosca(partes, rotulo="categoria_1", texto_central=texto_central)
    )


def indicador_037(df: pd.DataFrame):
    agua = dados.filtrar(df, nome_variavel="percentual_domicilios_rede_geral")
    cmp.exibir_barra_percentual(agua, "Domicílios ligados à rede geral de água")


def indicador_038(df: pd.DataFrame):
    esgoto = dados.filtrar(df, nome_variavel="percentual_domicilios_esgoto_rede_geral")
    cmp.exibir_barra_percentual(esgoto, "Domicílios com esgoto na rede geral ou pluvial")


def indicador_039(df: pd.DataFrame):
    lixo = dados.filtrar(df, nome_variavel="percentual_domicilios_coleta_adequada")
    cmp.exibir_barra_percentual(lixo, "Domicílios com coleta de lixo")


def indicador_040(df: pd.DataFrame):
    # classificações: 1 tempo de deslocamento, 2 nível de instrução, 3 grupo de idade, 4 cor ou raça
    dimensoes = {
        "Nível de instrução": "categoria_2",
        "Grupo de idade": "categoria_3",
        "Cor ou raça": "categoria_4",
    }
    cmp.comparar_composicao(df, partes="categoria_1", dimensoes=dimensoes, key="ind040_dim")


def indicador_041(df: pd.DataFrame):
    # classificações: 1 tempo de deslocamento, 2 sexo, 3 cor ou raça, 4 classe de rendimento
    dimensoes = {
        "Rendimento domiciliar per capita": "categoria_4",
        "Sexo": "categoria_2",
        "Cor ou raça": "categoria_3",
    }
    cmp.comparar_composicao(df, partes="categoria_1", dimensoes=dimensoes, key="ind041_dim")


def indicador_042(df: pd.DataFrame):
    # classificações: 1 meio de transporte, 2 nível de instrução, 3 cor ou raça
    d = dados.filtrar_totais(df, exceto=("categoria_1",))
    total = dados.filtrar(d, categoria_1="Total")["valor"].sum()

    # cada meio de transporte como % de quem trabalha fora de casa
    d = dados.sem_total(d, "categoria_1")
    d = d.assign(valor=d["valor"] / total * 100)

    cmp.renderizar_grafico(
        graficos.grafico_barras_horizontal(d, y="categoria_1", unidade="% de quem trabalha fora de casa", casas=1)
    )


def indicador_043(df: pd.DataFrame):
    # classificações: 1 sexo, 2 grupo de idade
    percentual = dados.filtrar(df, cod_variavel="13403")
    pessoas = dados.filtrar(df, cod_variavel="12785")

    col1, col2 = st.columns(2)
    with col1:
        cmp.exibir_total_destaque(percentual, "Com deficiência (2+ anos)", unidade="%", casas=1)
    with col2:
        cmp.exibir_total_destaque(pessoas, "Em número de pessoas")

    dimensoes = {
        "Grupo de idade": "categoria_2",
        "Sexo": "categoria_1",
    }
    cmp.explorar_por_classificacao(percentual, dimensoes, key="ind043_dim", unidade="%")


def indicador_046(df: pd.DataFrame):
    cmp.renderizar_grafico(
        graficos.grafico_barras_com_media_movel(df, unidade="por 100 mil hab.")
    )


def indicador_047(df: pd.DataFrame):
    cmp.renderizar_grafico(
        graficos.grafico_barras_com_media_movel(df, unidade="por 100 mil hab.")
    )


def indicador_048(df: pd.DataFrame):
    # classificações: 1 sexo, 2 cor ou raça, 3 grupo de idade
    cmp.exibir_total_destaque(df, "Rendimento domiciliar per capita", unidade="R$ cheio")

    dimensoes = {
        "Cor ou raça": "categoria_2",
        "Grupo de idade": "categoria_3",
        "Sexo": "categoria_1",
    }
    cmp.explorar_por_classificacao(df, dimensoes, key="ind048_dim", unidade="R$", casas=2)
