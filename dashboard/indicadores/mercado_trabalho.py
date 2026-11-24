"""
Gráficos dos indicadores 15-28 (mercado de trabalho)

Autor: Gabriel
Data de criação: 23/11/2026
"""

import pandas as pd

import dashboard.componentes as cmp
import dashboard.dados as dados
import dashboard.graficos.grafs as graficos
import dashboard.cores as tema


def _empresarial(df: pd.DataFrame, cod_variavel: str, rotulo: str, unidade_grafico: str,
                 unidade_destaque: str = "", fator: float = 1):
    """Tabela 9509 (poucos anos): número do último ano + barras baixas com a série."""
    serie = dados.filtrar(df, cod_variavel=cod_variavel)
    serie["valor"] = serie["valor"] * fator

    cmp.exibir_valor_mais_recente_destaque(serie, rotulo, unidade=unidade_destaque)

    fig = graficos.grafico_barras(serie, unidade=unidade_grafico)
    fig.update_layout(height=200)
    cmp.renderizar_grafico(fig)


def indicador_015(df: pd.DataFrame):
    _empresarial(df, "707", "Pessoal ocupado", unidade_grafico="pessoas")


def indicador_016(df: pd.DataFrame):
    _empresarial(df, "708", "Pessoal assalariado", unidade_grafico="pessoas")


def indicador_017(df: pd.DataFrame):
    _empresarial(df, "367", "Empresas e organizações", unidade_grafico="unidades")


def indicador_018(df: pd.DataFrame):
    _empresarial(df, "706", "Unidades locais", unidade_grafico="unidades")


def indicador_019(df: pd.DataFrame):
    # a tabela está em Mil Reais -> multiplica por 1000 para ficar em R$
    _empresarial(df, "662", "Salários e remunerações", unidade_grafico="R$", unidade_destaque="R$", fator=1000)


def indicador_020(df: pd.DataFrame):
    _empresarial(df, "10143", "Salário médio mensal", unidade_grafico="R$", unidade_destaque="R$ cheio")


def indicador_021(df: pd.DataFrame):
    media = dados.filtrar(df, cod_variavel="13536")
    cmp.exibir_total_destaque(media, "Rendimento médio", unidade="R$ cheio")

    por_posicao = dados.filtrar(media, categoria_1=["Homens", "Mulheres"])
    por_posicao = dados.sem_total(por_posicao, "categoria_2")

    cmp.renderizar_grafico(
        graficos.grafico_barras_horizontal(
            por_posicao,
            y="categoria_2",
            serie="categoria_1",
            cores=tema.CORES_SEXO,
            unidade="R$"
        )
    )


def indicador_022(df: pd.DataFrame):
    medidas = {"13536": "Média", "13537": "Mediana"}
    d = dados.filtrar(df, cod_variavel=list(medidas), categoria_1="Total")
    d["medida"] = d["cod_variavel"].map(medidas)

    mediana = dados.filtrar(d, medida="Mediana")
    cmp.exibir_total_destaque(mediana, "Rendimento mediano", unidade="R$ cheio")

    por_posicao = dados.sem_total(d, "categoria_2")
    cmp.renderizar_grafico(
        graficos.grafico_halteres(
            por_posicao,
            categoria="categoria_2",
            serie="medida",
            cores=[tema.AZUL, tema.VERDE],
            unidade="R$"
        )
    )


def indicador_023(df: pd.DataFrame):
    d = dados.filtrar(df, cod_variavel="708")
    ano = cmp.dropdown_anos(d, key="ind023_ano")

    d = dados.filtrar(d, ano=ano)
    d = dados.so_secoes_cnae(d, "categoria_1")

    if d.empty:
        cmp.exibir_mensagem_sem_dados()
        return

    cmp.renderizar_grafico(
        graficos.grafico_barras_horizontal(d, y="categoria_1", unidade="pessoas assalariadas")
    )


def _soma_anual(df: pd.DataFrame, nome_variavel: str) -> pd.DataFrame:
    # as séries do Novo Caged são mensais; o ETL guarda só o ano, então somamos os meses
    d = dados.filtrar(df, nome_variavel=nome_variavel)
    return d.groupby("ano", as_index=False)["valor"].sum()


def indicador_024(df: pd.DataFrame):
    admissoes = _soma_anual(df, "admissoes")
    cmp.renderizar_grafico(
        graficos.grafico_barras(admissoes, unidade="admissões")
    )


def indicador_025(df: pd.DataFrame):
    desligamentos = _soma_anual(df, "desligamentos")
    cmp.renderizar_grafico(
        graficos.grafico_barras(desligamentos, unidade="desligamentos")
    )


def indicador_026(df: pd.DataFrame):
    saldo = _soma_anual(df, "saldo_empregos")
    cmp.exibir_valor_mais_recente_destaque(saldo, "Saldo")

    cmp.renderizar_grafico(
        graficos.grafico_barras_com_sinal(saldo, unidade="vínculos")
    )


def indicador_027(df: pd.DataFrame):
    # classificações: 1 sexo, 2 cor ou raça, 3 contribuição p/ previdência, 4 seção de atividade
    dimensoes = {
        "Seção de atividade": "categoria_4",
        "Sexo": "categoria_1",
        "Cor ou raça": "categoria_2",
    }
    cmp.comparar_composicao(df, partes="categoria_3", dimensoes=dimensoes, key="ind027_dim")


def indicador_028(df: pd.DataFrame):
    # classificações: 1 sexo, 2 cor ou raça, 3 nível de instrução, 4 número de trabalhos
    dimensoes = {
        "Sexo": "categoria_1",
        "Cor ou raça": "categoria_2",
        "Número de trabalhos": "categoria_4",
    }
    d = dados.sem_indeterminados(df, "categoria_3")
    cmp.comparar_composicao(d, partes="categoria_3", dimensoes=dimensoes, key="ind028_dim")
