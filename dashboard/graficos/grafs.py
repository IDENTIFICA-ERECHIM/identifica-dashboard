import math

import pandas as pd
from plotly.colors import hex_to_rgb
from plotly.subplots import make_subplots

import plotly.graph_objects as go
import plotly.io as pio

import dashboard.graficos.template
import dashboard.graficos.configs_grafs as cfg
import dashboard.graficos.utils as utg

import dashboard.cores as tema
import dashboard.formatacao as fmt


# GRÁFICOS DE LINHAS
def grafico_linhas(df, serie=None, cores=None, unidade="",
                   casas=0, area=False, linha_ref=None, faixa_y=None) -> go.Figure:
    # suporta uma ou varias linhas:
    if serie is None:
        grupos = [(None, df)]
    else:
        grupos = df.groupby(serie, sort=False)

    fig = go.Figure()

    for i, (nome, dtf) in enumerate(grupos):
        dtf = dtf.sort_values("ano")
        cor = utg.cor_da_serie(cores, nome, i)

        r, g, b = hex_to_rgb(cor)

        fig.add_scatter(
            x=dtf["ano"], y=dtf["valor"],
            name=nome,
            mode="lines+markers" if len(dtf) <= 15 else "lines",
            line=dict(
                color=cor,
                width=2
            ),
            marker=dict(
                size=8,
                line=dict(
                    color="white",
                    width=2
                )
            ),
            fill="tozeroy" if area else None,
            fillcolor=f"rgba({r},{g},{b},0.1)",  # opacidade 10%
            hovertemplate=utg.texto_hover("y", casas, unidade, nome),
        )

    # linha pontilhada de referencia:
    if linha_ref is not None:
        fig.add_hline(y=linha_ref, line_color=tema.TEXTO_SUAVE, line_dash="dot", line_width=1)

    # espacamento no eixo x
    folga_eixo_x = max(
        (df["ano"].max() - df["ano"].min()) * 0.03,
        0.5
    )
    fig.update_xaxes(
        range=[
            df["ano"].min() - folga_eixo_x,
            df["ano"].max() + folga_eixo_x
        ]
    )

    fig.update_layout(
        showlegend=serie is not None,
        yaxis_range=faixa_y # limites do eixo y
    )

    utg.formatar_eixo_anos(fig, df, unidade)

    return fig


# GRÁFICOS DE BARRAS
def grafico_barras(df, cor_barra=tema.AZUL, unidade="", casas=0) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=df["ano"],
        y=df["valor"],
        marker_color=cor_barra,
        width=None, # padrao
        hovertemplate=utg.texto_hover("y", casas, unidade),
    ))

    utg.formatar_eixo_anos(fig, df, unidade)

    return fig


def grafico_barras_com_sinal(df, unidade="", casas=0, linha_ref=True) -> go.Figure:
    cores_barras = []
    for v in df["valor"]:
        if v >= 0:
            cores_barras.append(tema.POSITIVO)
        else:
            cores_barras.append(tema.NEGATIVO)

    fig = go.Figure(go.Bar(
        x=df["ano"],
        y=df["valor"],
        marker_color=cores_barras,
        hovertemplate=utg.texto_hover("y", casas, unidade)
    ))

    # linha de referencia em y = 0
    if linha_ref:
        fig.add_hline(
            y=0,
            line_color=tema.TEXTO_SUAVE,
            line_width=1
        )

    utg.formatar_eixo_anos(fig, df, unidade)

    return fig

def grafico_barras_empilhadas(df, serie, cores=None, unidade="", casas=0, tipo_empilhamento="group") -> go.Figure:
    fig = go.Figure()

    grupos = df.groupby(serie, sort=False)
    for i, (nome, dtf) in enumerate(grupos):
        fig.add_bar(
            x=dtf["ano"],
            y=dtf["valor"],
            name=nome,
            marker_color=utg.cor_da_serie(cores, nome, i),
            marker_line=dict(
                color="white",
                width=1.5
            ),
            hovertemplate=utg.texto_hover("y", casas, unidade, nome)
        )

    # barras empilhadas:
    fig.update_layout(barmode=tipo_empilhamento) # tipos: 'stack', 'group', 'overlay'

    utg.formatar_eixo_anos(fig, df, unidade)

    return fig


def grafico_barras_com_media_movel(df, janela=3, unidade="", casas=1) -> go.Figure:
    dtf = df.sort_values("ano")

    media_movel = dtf["valor"].rolling(
        janela,
        min_periods=janela
    ).mean()

    fig = go.Figure()

    fig.add_bar(
        x=dtf["ano"],
        y=dtf["valor"],
        name="Anual",
        marker_color=tema.AZUL_CLARO,
        hovertemplate=utg.texto_hover("y", casas, unidade, "Anual")
    )

    fig.add_scatter(
        x=dtf["ano"],
        y=media_movel,
        name=f"Média móvel ({janela} anos)",
        mode="lines",
        line=dict(
            color=tema.AZUL,
            width=2
        ),
        hovertemplate=utg.texto_hover("y", casas, unidade, "Média")
    )

    utg.formatar_eixo_anos(fig, dtf, unidade)

    return fig


# Barras horizontais (eixo y representa a categoria)
def grafico_barras_horizontal(df, y, serie=None, cores=None, unidade="", casas=0, ordenar=True, linha_ref=None) -> go.Figure:
    if ordenar:
        ordem = (
            df.groupby(y, sort=False)["valor"]
            .sum()
            .sort_values()
            .index
        )
    else:
        ordem = pd.unique(df[y])[::-1]  # inverte a ordem, pois o plotly desenha a 1a cat. embaixo

    rotulos = []
    for texto in ordem:
        rotulos.append( utg.quebrar_texto(texto) )

    if serie is None:
        # todo o dataframe eh tratado como um unico grupo (cada categoria vai virar uma barra)
        grupos = [(None, df)]
        n_series = 1
    else:
        # o dataframe sera dividido conforme a coluna indicada (o nome da col eh passado como o argumento 'serie')
        grupos = df.groupby(serie, sort=False)
        n_series = df[serie].nunique()

    fig = go.Figure()

    for i, (nome, dtf) in enumerate(grupos):
        if serie is None:
            cor = tema.AZUL
        else:
            cor = utg.cor_da_serie(cores, nome, i)

        fig.add_bar(
            y=[utg.quebrar_texto(c) for c in dtf[y]],
            x=dtf["valor"],
            name=nome,
            orientation="h", # define q as barras vao ser horizontais
            marker_color=cor,
            hovertemplate=utg.texto_hover("x", casas, unidade, nome)
        )

    # linha pontilhada de referencia
    if linha_ref is not None:
        fig.add_vline(
            x=linha_ref,
            line_color=tema.TEXTO_SUAVE,
            line_dash="dot",
            line_width=1
        )

    fig.update_yaxes(
        categoryorder="array",
        categoryarray=rotulos,
        showgrid=False
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=tema.GRADE
    )

    fig.update_layout(
        height=utg.altura_grafico_horizontal(rotulos, n_series),
        hovermode="y unified",
        barmode="group",
        showlegend=serie is not None,
        xaxis_title=unidade
    )

    return fig

# Graf. de barras horizontais 100% empilhadas.
# Todas as barras sao normalizadas, e representam alguma categoria principal
# As barras sao divididas em segmentos que mostram a participacao percentual de suas partes
def grafico_barras_horizontais_composicao(df, linhas, partes, cores=None, casas=1) -> go.Figure:
    # normalizar:
    total_da_linha = df.groupby(linhas)["valor"].transform("sum")
    df = df.assign(valor=df["valor"] / total_da_linha * 100)

    n_partes = df[partes].nunique()

    if cores is None:
        cores = tema.rampa(n_partes)

    fig = go.Figure()

    grupos = df.groupby(partes, sort=False)
    for i, (nome, dtf) in enumerate(grupos):
        fig.add_bar(
            y=[utg.quebrar_texto(c) for c in dtf[linhas]],
            x=dtf["valor"],
            name=nome,
            orientation="h",
            marker_color=utg.cor_da_serie(cores, nome, i),
            marker_line=dict( # borda entre os segmentos da barra
                color="white",
                width=1.5
            ),
            hovertemplate=utg.texto_hover("x", casas, "%", nome)
        )

    rotulos = []
    for texto in pd.unique(df[linhas]):
        rotulos.append( utg.quebrar_texto(texto) )

    altura = utg.altura_grafico_horizontal(rotulos, 2) + 18 * (n_partes // 3)

    fig.update_yaxes(
        categoryorder="array",
        categoryarray=rotulos,
        autorange="reversed"
    )

    fig.update_xaxes(
        range=[0, 101],
        ticksuffix="%",
        showgrid=False
    )

    fig.update_layout(
        barmode="stack",
        hovermode="y unified",
        barcornerradius=0,
        height=altura,
        legend=dict(traceorder="normal")
    )

    return fig


# GRAFICOS DE ÁREAS
def grafico_areas_empilhadas(df, serie, cores=None, unidade="", casas=0, percentual=False) -> go.Figure:
    # se 'percentual=True', cada categoria representa sua participacao naquele ano
    if percentual:
        unidade = "%"
        normalizacao = "percent"
    else:
        normalizacao = ""

    fig = go.Figure()

    grupos = df.groupby(serie, sort=False)
    for i, (nome, dtf) in enumerate(grupos):
        dtf = dtf.sort_values("ano")

        fig.add_scatter(
            x=dtf["ano"],
            y=dtf["valor"],
            name=nome,
            mode="lines", # linhas sem marcadores
            stackgroup="um", # empilha as linhas
            groupnorm=normalizacao,
            line=dict(
                color="white",
                width=1
            ),
            fillcolor=utg.cor_da_serie(cores, nome, i),
            hovertemplate=utg.texto_hover("y", casas, unidade, nome)
        )

    utg.formatar_eixo_anos(fig, df, unidade)

    return fig


# PEQUENOS MULTIPLOS
def grafico_pequenos_multiplos(df, serie, nomes=None, colunas=3, unidade="", casas=0) -> go.Figure:
    if nomes is None:
        nomes = {}

    series   = list(df.groupby(serie, sort=False))
    n_linhas = math.ceil(len(series) / colunas) # quantas linhas vai precisar p/ todos os mini graficos

    # titulos de cada painel:
    titulos = []

    for nome, _ in series:
        titulos.append(nomes.get(nome, nome))

    espaco_vertical = 0
    if n_linhas > 1:
        espaco_vertical = 0.25

    fig = make_subplots(
        rows=n_linhas,
        cols=colunas,
        subplot_titles=titulos,
        vertical_spacing=espaco_vertical,
        horizontal_spacing=0.07
    )

    for i, (nome, dtf) in enumerate(series):
        dtf = dtf.sort_values("ano")

        linha = i // colunas + 1
        coluna = i % colunas + 1

        fig.add_scatter(
            x=dtf["ano"],
            y=dtf["valor"],
            mode="lines",
            line=dict(
                color=tema.AZUL,
                width=2
            ),
            hovertemplate=utg.texto_hover("y", casas, unidade),
            row=linha,
            col=coluna
        )

    # annotations = titulos dos paineis
    fig.update_annotations(
        font=dict(
            size=cfg.TAM_TITULO,
            color=tema.TEXTO
        )
    )

    fig.update_xaxes(tickformat="d") # anos sao inteiros
    fig.update_yaxes(rangemode="tozero") # eixo y inclui 0

    fig.update_layout(
        height=230 * n_linhas,
        margin_t=36,
        showlegend=False,
        hovermode="x"
    )

    return fig


# PIRÂMIDE ETÁRIA
def grafico_piramide_etaria(df, faixa="faixa", sexo="sexo", ordem=None) -> go.Figure:
    if ordem is None:
        ordem = list(pd.unique(df[faixa]))

    fig = go.Figure()

    # valor negativo para os homens p/ ficarem na esquerda do grafico
    for nome_sexo, sinal in (("Homens", -1), ("Mulheres", 1)):
        dtf = df[df[sexo] == nome_sexo]

        fig.add_bar(
            y=dtf[faixa],
            x=dtf["valor"] * sinal,
            customdata=dtf["valor"],
            name=nome_sexo,
            orientation="h",
            marker_color=tema.CORES_SEXO[nome_sexo],
            hovertemplate=nome_sexo + ": %{customdata:,.0f}<extra></extra>"
        )

    metade = df["valor"].max() / 2 # divide o valor maximo por 2, para encontrar a metade
    base = 10 ** math.floor(math.log10(metade)) # ordem de grandeza de 'metade'

    for multiplo in (1, 2, 2.5, 5, 10):
        passo = multiplo * base
        if passo >= metade:
            break

    marcas = [-2 * passo, -passo, 0, passo, 2 * passo]

    textos = []
    for m in marcas:
        textos.append( fmt.numero(abs(m)) )


    faixas_presentes = set(df[faixa])

    ordem_presente = []
    for f in ordem:
        if f in faixas_presentes:
            ordem_presente.append(f)

    fig.update_xaxes(
        tickvals=marcas,
        ticktext=textos,
        showgrid=True,
        gridcolor=tema.GRADE
    )

    fig.update_yaxes(
        categoryorder="array",
        categoryarray=ordem_presente
    )

    fig.update_layout(
        barmode="relative",
        bargap=0.08,
        hovermode="y unified",
        barcornerradius=2,
        height=max(18 * len(ordem) + 90, cfg.ALTURA_GRAFICO)
    )

    return fig


# GRÁFICO DE ROSCA
def grafico_rosca(df, rotulo, cores=None, texto_central="", casas=1, tam_furo_central=0.6) -> go.Figure:
    cores_fatias = []
    for i, nome in enumerate(df[rotulo]):
        cores_fatias.append( utg.cor_da_serie(cores, nome, i) )

    fig = go.Figure(go.Pie(
        labels=df[rotulo],
        values=df["valor"],
        hole=tam_furo_central,
        sort=False,
        direction="clockwise",
        marker=dict(
            colors=cores_fatias,
            line=dict(
                color="white",
                width=2
            )
        ),
        textinfo="percent",
        texttemplate="%{percent:." + str(casas) + "%}",
        hovertemplate="%{label}: %{percent:.1%}<extra></extra>",
    ))

    # titulo no centro
    fig.add_annotation(
        text=texto_central,
        showarrow=False,
        font=dict(size=cfg.TAM_TITULO, color=tema.TEXTO)
    )

    fig.update_layout(
        legend=dict(
            orientation="v",
            x=1,
            y=0.5,
            yanchor="middle"
        )
    )

    return fig


# GRÁFICO MAPA DE ÁRVORE
def grafico_treemap(df, rotulo, unidade="", casas=0) -> go.Figure:
    rotulos = []
    for texto in df[rotulo]:
        rotulos.append( utg.quebrar_texto(texto, 22) )

    fig = go.Figure(go.Treemap(
        labels=rotulos,
        parents=[""] * len(df), # sem hierarquia
        values=df["valor"],
        marker=dict(
            # aparencia dos retangulos
            colors=df["valor"],
            colorscale=[
                [0, tema.RAMPA_AZUL[0]],
                [1, tema.RAMPA_AZUL[-1]]
            ],
            line=dict(
                color="white",
                width=2
            ),
            pad=dict(t=2, l=2, r=2, b=2) # espacamento interno
        ),
        textinfo="label+percent root",
        tiling=dict(
            pad=2
        ),
        hovertemplate="%{label}<br>%{value:,." + str(casas) + "f} " + unidade + "<extra></extra>",
    ))

    fig.update_layout(
        height=420,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig


# GRÁFICO DE HALTERES
def grafico_halteres(df, categoria, serie, cores=None, unidade="", casas=0) -> go.Figure:
    # formato longo -> largo
    tabela = df.pivot_table(
        index=categoria,
        columns=serie,
        values="valor",
        sort=False
    ).dropna()

    # pegando o nome das colunas
    a = tabela.columns[0]
    b = tabela.columns[1]

    tabela = tabela.sort_values(b)

    rotulos = []
    for texto in tabela.index:
        rotulos.append( utg.quebrar_texto(texto) )

    fig = go.Figure()

    x_segmentos = []
    y_segmentos = []

    for rotulo, valor_a, valor_b in zip(rotulos, tabela[a], tabela[b]):
        x_segmentos += [valor_a, valor_b, None]
        y_segmentos += [rotulo, rotulo, None]

    fig.add_scatter(
        x=x_segmentos,
        y=y_segmentos,
        mode="lines",
        line=dict(
            color=tema.NEUTRO,
            width=3
        ),
        hoverinfo="skip",
        showlegend=False
    )

    for i, coluna in enumerate((a, b)):
        fig.add_scatter(
            x=tabela[coluna],
            y=rotulos,
            mode="markers",
            name=str(coluna),
            marker=dict(
                size=11,
                color=utg.cor_da_serie(cores, coluna, i),
                line=dict(color="white", width=2)
            ),
            hovertemplate=utg.texto_hover("x", casas, unidade, coluna)
        )

    fig.update_yaxes(
        categoryorder="array",
        categoryarray=rotulos,
        showgrid=False
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=tema.GRADE
    )

    fig.update_layout(
        height=utg.altura_grafico_horizontal(rotulos),
        hovermode="y unified",
        xaxis_title=unidade
    )

    return fig
