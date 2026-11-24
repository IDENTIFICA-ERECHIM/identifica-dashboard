"""
Gráficos dos indicadores 49-70 (sociais)

Autor: Gabriel
Data de criação: 23/11/2026
"""

import pandas as pd
import streamlit as st

import dashboard.componentes as cmp
import dashboard.dados as dados
import dashboard.graficos.grafs as graficos

REBANHOS = {
    "quant_bovinos": "Bovinos",
    "quant_suinos": "Suínos",
    "quant_ovinos": "Ovinos",
    "quant_caprinos": "Caprinos",
    "quant_equinos": "Equinos",
}


def _mil_reais(df: pd.DataFrame, cod_variavel: str) -> pd.DataFrame:
    """Variável do SIDRA em Mil Reais -> R$."""
    d = dados.filtrar(df, cod_variavel=cod_variavel)
    d["valor"] = d["valor"] * 1000
    return d


def _escala(df: pd.DataFrame, divisor: float) -> pd.DataFrame:
    """Divide os valores (ex.: divisor=1e6 passa de R$ para R$ milhões)."""
    return df.assign(valor=df["valor"] / divisor)


def indicador_049(df: pd.DataFrame):
    pib = _mil_reais(df, "37")
    cmp.exibir_valor_mais_recente_destaque(pib, "PIB", unidade="R$")

    pib_bilhoes = _escala(pib, 1e9)
    cmp.renderizar_grafico(
        graficos.grafico_barras(pib_bilhoes, unidade="R$ bilhões", casas=2)
    )


def indicador_050(df: pd.DataFrame):
    cmp.exibir_valor_mais_recente_destaque(df, "PIB per capita", unidade="R$ cheio")
    cmp.renderizar_grafico(
        graficos.grafico_linhas(df, unidade="R$ por habitante", casas=2)
    )


def indicador_051(df: pd.DataFrame):
    vab = _mil_reais(df, "513")
    cmp.exibir_valor_mais_recente_destaque(vab, "VAB agropecuária", unidade="R$")

    vab_milhoes = _escala(vab, 1e6)
    cmp.renderizar_grafico(
        graficos.grafico_linhas(vab_milhoes, unidade="R$ milhões", casas=1, area=True)
    )


def indicador_052(df: pd.DataFrame):
    vab = _mil_reais(df, "517")
    cmp.exibir_valor_mais_recente_destaque(vab, "VAB indústria", unidade="R$")

    vab_milhoes = _escala(vab, 1e6)
    cmp.renderizar_grafico(
        graficos.grafico_linhas(vab_milhoes, unidade="R$ milhões", casas=1, area=True)
    )


def indicador_053(df: pd.DataFrame):
    privados = _mil_reais(df, "6575")
    privados["setor"] = "Serviços privados"

    publicos = _mil_reais(df, "525")
    publicos["setor"] = "Administração pública"

    partes = pd.concat([privados, publicos])

    total_por_ano = partes.groupby("ano", as_index=False)["valor"].sum(min_count=2)
    cmp.exibir_valor_mais_recente_destaque(total_por_ano, "VAB serviços (total)", unidade="R$")

    partes_milhoes = _escala(partes, 1e6)
    cmp.renderizar_grafico(
        graficos.grafico_areas_empilhadas(partes_milhoes, serie="setor", unidade="R$ milhões", casas=1)
    )


def indicador_054(df: pd.DataFrame):
    setores = {
        "516": "Agropecuária",
        "520": "Indústria",
        "6574": "Serviços privados",
        "528": "Administração pública",
    }
    d = dados.filtrar(df, cod_variavel=list(setores))
    d["setor"] = d["cod_variavel"].map(setores)

    cmp.renderizar_grafico(
        graficos.grafico_areas_empilhadas(d, serie="setor", unidade="% do VAB", casas=1)
    )


def indicador_055(df: pd.DataFrame):
    d = dados.filtrar(df, cod_variavel="706")
    ano = cmp.dropdown_anos(d, key="ind055_ano")

    d = dados.filtrar(d, ano=ano)
    d = dados.so_secoes_cnae(d, "categoria_1")
    d = d.dropna(subset=["valor"])
    d = d[d["valor"] > 0]  # o treemap não desenha áreas zeradas

    cmp.renderizar_grafico(
        graficos.grafico_treemap(d, rotulo="categoria_1", unidade="unidades locais")
    )


def indicador_056(df: pd.DataFrame):
    d = dados.filtrar(df, cod_variavel="707")
    d = dados.so_secoes_cnae(d, "categoria_1")

    # compara o primeiro com o último ano disponível
    primeiro = d["ano"].min()
    ultimo = d["ano"].max()
    d = dados.filtrar(d, ano=[primeiro, ultimo])
    d["ano"] = d["ano"].astype(str)  # texto, para virar o nome de cada ponto na legenda

    cmp.renderizar_grafico(
        graficos.grafico_halteres(d, categoria="categoria_1", serie="ano", unidade="pessoas ocupadas")
    )


def _escolher_produto(df: pd.DataFrame, cod_variavel: str, key: str) -> str:
    """Lista de produtos (lavouras) ordenada pela maior área plantada no último ano."""
    area = dados.filtrar(df, cod_variavel=cod_variavel)
    area = dados.sem_total(area, "categoria_1")
    area = area.dropna(subset=["valor"])

    ultimo_ano = area[area["ano"] == area["ano"].max()]
    ranking = ultimo_ano.sort_values("valor", ascending=False)

    return st.selectbox(
        "Produto",
        ranking["categoria_1"].tolist(),
        key=key,
        label_visibility="collapsed"
    )


def indicador_057(df: pd.DataFrame):
    produto = _escolher_produto(df, "109", key="ind057_produto")

    medidas = {"109": "Área plantada", "216": "Área colhida"}
    d = dados.filtrar(df, cod_variavel=list(medidas), categoria_1=produto)
    d["medida"] = d["cod_variavel"].map(medidas)

    d = cmp.slider_anos(d, key="ind057_anos")
    cmp.renderizar_grafico(
        graficos.grafico_linhas(d, serie="medida", unidade="hectares")
    )


def indicador_058(df: pd.DataFrame):
    produto = _escolher_produto(df, "109", key="ind058_produto")
    d = dados.filtrar(df, cod_variavel="214", categoria_1=produto)
    d = d.dropna(subset=["valor"])

    if d.empty:
        cmp.exibir_mensagem_sem_dados()
        return

    unidade = d["uni_medida"].iloc[-1]  # varia por produto (toneladas, mil frutos...)
    d = cmp.slider_anos(d, key="ind058_anos")

    cmp.renderizar_grafico(
        graficos.grafico_barras(d, unidade=unidade)
    )


def indicador_059(df: pd.DataFrame):
    produto = _escolher_produto(df, "109", key="ind059_produto")
    d = dados.filtrar(df, cod_variavel="112", categoria_1=produto)
    d = d.dropna(subset=["valor"])

    if d.empty:
        cmp.exibir_mensagem_sem_dados()
        return

    d = cmp.slider_anos(d, key="ind059_anos")
    cmp.renderizar_grafico(
        graficos.grafico_linhas(d, unidade="kg/ha")
    )


def indicador_060(df: pd.DataFrame):
    # só anos em Real: os anos antigos estão em outras moedas e não são comparáveis
    em_reais = dados.filtrar(df, uni_medida="Mil Reais")
    d = _mil_reais(em_reais, "215")

    ano = cmp.dropdown_anos(d, key="ind060_ano")
    d = dados.filtrar(d, ano=ano)
    d = dados.sem_total(d, "categoria_1")

    maiores = d.nlargest(10, "valor")
    maiores = _escala(maiores, 1e6)

    cmp.renderizar_grafico(
        graficos.grafico_barras_horizontal(maiores, y="categoria_1", unidade="R$ milhões", casas=1)
    )


def indicador_061(df: pd.DataFrame):
    cmp.renderizar_grafico(
        graficos.grafico_pequenos_multiplos(df, serie="nome_variavel", nomes=REBANHOS, unidade="cabeças")
    )


def indicador_062(df: pd.DataFrame):
    nomes = {
        "quant_leite": "Quantidade (litros)",
        "valor_leite": "Valor (R$ a preços de 2010)",
    }
    cmp.renderizar_grafico(
        graficos.grafico_pequenos_multiplos(df, serie="nome_variavel", nomes=nomes, colunas=2)
    )


def indicador_063(silvicultura: pd.DataFrame, extrativismo: pd.DataFrame):
    atividades = {"Silvicultura": silvicultura, "Extração vegetal": extrativismo}

    partes = []
    for nome, df in atividades.items():
        d = dados.filtrar(df, categoria_1="Total", uni_medida="Mil Reais")  # só anos em Real
        d = _escala(d, 1000)  # Mil Reais -> R$ milhões
        d["atividade"] = nome
        partes.append(d)

    cmp.renderizar_grafico(
        graficos.grafico_linhas(pd.concat(partes), serie="atividade", unidade="R$ milhões", casas=1)
    )


def indicador_064(df: pd.DataFrame):
    exportacoes = dados.filtrar(df, nome_variavel="exportacoes")
    cmp.exibir_valor_mais_recente_destaque(exportacoes, "Exportações", unidade="US$")

    exportacoes_milhoes = _escala(exportacoes, 1e6)
    cmp.renderizar_grafico(
        graficos.grafico_barras(exportacoes_milhoes, unidade="US$ milhões FOB", casas=1)
    )


def indicador_065(df: pd.DataFrame):
    importacoes = dados.filtrar(df, nome_variavel="importacoes")
    cmp.exibir_valor_mais_recente_destaque(importacoes, "Importações", unidade="US$")

    importacoes_milhoes = _escala(importacoes, 1e6)
    cmp.renderizar_grafico(
        graficos.grafico_barras(importacoes_milhoes, unidade="US$ milhões FOB", casas=1)
    )


def indicador_066(df: pd.DataFrame):
    saldo = dados.filtrar(df, nome_variavel="saldo_comercial")
    saldo_milhoes = _escala(saldo, 1e6)

    cmp.renderizar_grafico(
        graficos.grafico_barras_com_sinal(saldo_milhoes, unidade="US$ milhões FOB", casas=1)
    )


def indicador_067(df: pd.DataFrame):
    estoque = dados.filtrar(df, nome_variavel="estoque_cred_rural")
    cmp.exibir_valor_mais_recente_destaque(estoque, "Estoque de crédito rural", unidade="R$")

    estoque_milhoes = _escala(estoque, 1e6)
    cmp.renderizar_grafico(
        graficos.grafico_linhas(estoque_milhoes, unidade="R$ milhões (2010)", casas=1, area=True)
    )


def indicador_068(df: pd.DataFrame):
    contratos = dados.filtrar(df, nome_variavel="contratos_cred_rural")
    cmp.renderizar_grafico(
        graficos.grafico_barras(contratos, unidade="contratos")
    )


def indicador_069(df: pd.DataFrame):
    medidas = {
        "1321": "Estabelecimentos",
        "1322": "Unidades habitacionais",
        "9296": "Leitos",
    }

    colunas = st.columns(3)
    for i, cod in enumerate(medidas):
        with colunas[i]:
            medida = dados.filtrar(df, cod_variavel=cod)
            cmp.exibir_total_destaque(medida, medidas[cod])

    leitos = dados.filtrar(df, cod_variavel="9296")
    leitos = dados.sem_total(leitos, "categoria_1")

    cmp.renderizar_grafico(
        graficos.grafico_barras_horizontal(leitos, y="categoria_1", unidade="leitos")
    )


def indicador_070(df: pd.DataFrame):
    investimento = dados.filtrar(df, nome_variavel="invest_publico_municipal")
    cmp.exibir_valor_mais_recente_destaque(investimento, "Investimento", unidade="R$")

    investimento_milhoes = _escala(investimento, 1e6)
    cmp.renderizar_grafico(
        graficos.grafico_barras(investimento_milhoes, unidade="R$ milhões", casas=1)
    )
