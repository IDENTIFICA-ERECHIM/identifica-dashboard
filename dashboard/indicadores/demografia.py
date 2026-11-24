"""
Gráficos dos indicadores 1-14 (demografia)

Autor: Gabriel
Data de criação: 22/11/2026
"""

import pandas as pd
import streamlit as st

import dashboard.componentes as cmp
import dashboard.dados as dados
import dashboard.formatacao as fmt
import dashboard.graficos.grafs as graficos
import dashboard.cores as tema

FAIXAS_IPEA = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-39", "40-49", "50-59", "60-69", "70+"]
FAIXAS_CENSO = [f"{i} a {i + 4} anos" for i in range(0, 100, 5)] + ["100 anos ou mais"]
REGIOES = ["Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"]


def indicador_001(df: pd.DataFrame):
    pop_estimada = dados.filtrar(df, nome_variavel="populacao")
    cmp.exibir_valor_mais_recente_destaque(pop_estimada, "População Estimada")

    pop_estimada = cmp.slider_anos(pop_estimada, key="ind001_anos")
    cmp.renderizar_grafico(
        graficos.grafico_linhas(pop_estimada, unidade="habitantes")
    )

def indicador_002(df: pd.DataFrame):
    taxa = dados.filtrar(df, nome_variavel="taxa_crescimento_populacao")
    taxa = cmp.slider_anos(taxa, key="ind002_anos")

    cmp.renderizar_grafico(
        graficos.grafico_barras_com_sinal(taxa, unidade="% ao ano", casas=2)
    )

def indicador_003(df: pd.DataFrame):
    nomes = {"populacao_urbana": "Urbana", "populacao_rural": "Rural"}
    pop = dados.filtrar(df, nome_variavel=list(nomes))
    pop["situacao"] = pop["nome_variavel"].map(nomes)

    cmp.renderizar_grafico(
        graficos.grafico_barras_empilhadas(
            pop,
            serie="situacao",
            cores=[tema.AZUL, tema.VERDE],
            unidade="habitantes",
            tipo_empilhamento="stack"
        )
    )

def indicador_004(df: pd.DataFrame):
    taxa = dados.filtrar(df, nome_variavel="taxa_urbanizacao")
    cmp.exibir_valor_mais_recente_destaque(taxa, "Taxa de urbanização", unidade="%", casas=1)

    cmp.renderizar_grafico(
        graficos.grafico_linhas(taxa, unidade="%", casas=1, area=True, faixa_y=[0, 100])
    )

def indicador_005(historico: pd.DataFrame, censo: pd.DataFrame):
    fonte = cmp.botoes_escolha(
        "Fonte",
        ["IBGE, Censo 2022", "Série histórica (Ipea)"],
        key="ind005_fonte"
    )

    if fonte == "Série histórica (Ipea)":
        historico = dados.filtrar(historico, sexo=["Homens", "Mulheres"])
        ano = cmp.dropdown_anos(historico, key="ind005_ano")

        piramide = dados.filtrar(historico, ano=ano)
        piramide = piramide.rename(columns={"faixa_etaria": "faixa"})
        ordem = FAIXAS_IPEA
    else:
        piramide = dados.filtrar(
            censo,
            cod_variavel="93",
            categoria_1=["Homens", "Mulheres"],
            categoria_2=FAIXAS_CENSO
        )
        piramide = piramide.rename(columns={"categoria_1": "sexo", "categoria_2": "faixa"})
        ordem = FAIXAS_CENSO

    cmp.renderizar_grafico(
        graficos.grafico_piramide_etaria(piramide, ordem=ordem)
    )

def indicador_006(df: pd.DataFrame):
    localizacao_total = dados.filtrar(df, categoria_1="Total")
    cmp.exibir_total_destaque(localizacao_total, "Idosos (60+) para cada 100 jovens (0-14)", casas=1)

    por_situacao = dados.sem_total(localizacao_total, "categoria_2")
    cmp.renderizar_grafico(
        graficos.grafico_barras_horizontal(
            por_situacao,
            y="categoria_2",
            unidade="idosos por 100 jovens",
            casas=1,
            linha_ref=100
        )
    )

def indicador_007(df: pd.DataFrame):
    cmp.exibir_valor_mais_recente_destaque(df, "Idade mediana", unidade="anos", casas=1)


def indicador_008(df: pd.DataFrame):
    # formato largo:
    tabela = df.pivot_table(
        index="ano",
        columns="nome_variavel",
        values="valor"
        )
    ativa = tabela["pop_ativa_15-59"]

    partes = pd.DataFrame({
        "Jovens (0-14)": tabela["pop_criancas_0-14"] / ativa * 100,
        "Idosos (60+)":  tabela["pop_idosa_60mais"] / ativa * 100,
    })


    # voltando p/ formato longo
    partes = partes.reset_index()
    partes = partes.melt(id_vars="ano", var_name="grupo", value_name="valor")
    partes = partes.dropna()

    razao = dados.filtrar(df, nome_variavel="razao_dependencia")
    cmp.exibir_valor_mais_recente_destaque(razao, "Razão de dependência", unidade="a cada 100 pessoas de 15-59", casas=1)

    cmp.renderizar_grafico(
        graficos.grafico_barras_empilhadas(
            partes,
            serie="grupo",
            unidade="dependentes por 100 pessoas de 15-59",
            casas=1,
            tipo_empilhamento="stack"
        )
    )

def indicador_009(df: pd.DataFrame):
    razao = dados.filtrar(df, nome_variavel="razao_sexo")
    cmp.exibir_valor_mais_recente_destaque(razao, "Homens para cada 100 mulheres", casas=1)

    cmp.renderizar_grafico(
        graficos.grafico_linhas(razao, unidade="homens por 100 mulheres", casas=1, linha_ref=100)
    )

def indicador_010(df: pd.DataFrame):
    densidade = dados.filtrar(df, nome_variavel="densidade_demografica")
    cmp.exibir_valor_mais_recente_destaque(densidade, "Densidade", unidade="hab./km²", casas=1)

    cmp.renderizar_grafico(
        graficos.grafico_barras(densidade, unidade="hab./km²", casas=1)
    )

def indicador_011(municipio: pd.DataFrame, uf: pd.DataFrame, internacional: pd.DataFrame):
    col1, col2, col3 = st.columns(3)
    with col1:
        cmp.exibir_total_destaque(municipio, "Vieram de outro município")
    with col2:
        cmp.exibir_total_destaque(uf, "Vieram de outra UF")
    with col3:
        cmp.exibir_total_destaque(internacional, "Vieram de outro país")

    visao = cmp.botoes_escolha(
        "Detalhar",
        ["Idade e sexo", "UF de origem", "País de origem"],
        key="ind011_visao"
    )

    if visao == "Idade e sexo":
        dtf = dados.filtrar(municipio, categoria_1=["Homens", "Mulheres"])
        dtf = dados.sem_total(dtf, "categoria_2")
        dtf = dtf.rename(columns={"categoria_1": "sexo", "categoria_2": "faixa"})

        cmp.renderizar_grafico(
            graficos.grafico_piramide_etaria(dtf)
        )

    elif visao == "UF de origem":
        dtf = uf[~uf["categoria_1"].isin(["Total"] + REGIOES)]  # só UFs: tira o total e as regiões

        cmp.renderizar_grafico(
            graficos.grafico_barras_horizontal(dtf.nlargest(10, "valor"), y="categoria_1", unidade="pessoas")
        )

    else:
        dtf = dados.filtrar_totais(internacional, exceto=("categoria_2",))
        dtf = dados.sem_total(dtf, "categoria_2")

        cmp.renderizar_grafico(
            graficos.grafico_barras_horizontal(dtf.nlargest(10, "valor"), y="categoria_2", unidade="pessoas")
        )

def indicador_012(df: pd.DataFrame):
    total = dados.filtrar(df, categoria_1="Total")
    cmp.exibir_valor_mais_recente_destaque(total, "Nascidos vivos")

    visao = cmp.botoes_escolha("Visão", ["Total por ano", "Idade da mãe"], key="ind012_visao")

    if visao == "Total por ano":
        cmp.renderizar_grafico(
            graficos.grafico_barras(total, unidade="nascimentos")
        )
    else:
        por_idade = dados.sem_total(df, "categoria_1")
        por_idade = dados.sem_indeterminados(por_idade, "categoria_1")

        # a tabela traz faixas ("15 a 19 anos") e idades simples ("15 anos"). 
        eh_faixa = por_idade["categoria_1"].str.contains(" a |Menos de|ou mais")
        por_idade = por_idade[eh_faixa]

        cores = tema.rampa(por_idade["categoria_1"].nunique())

        cmp.renderizar_grafico(
            graficos.grafico_areas_empilhadas(por_idade, serie="categoria_1", cores=cores, percentual=True)
        )


def indicador_013(df: pd.DataFrame):
    pass

def indicador_014(df: pd.DataFrame):
    pass
