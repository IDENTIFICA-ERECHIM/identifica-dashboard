import plotly.graph_objects as go
import plotly.io as pio

import dashboard.cores as tema
import dashboard.graficos.configs_grafs as cfg

# configuracoes comuns aos eixos x e y
CONFIG_EIXOS = dict(
    automargin=True, # aumenta a margem automaticamente se necessario
    fixedrange=True, # p/ zoom n alterar o intervalo do graf
    separatethousands=True,
    exponentformat="none", # n usar notacao cientifica
    title=dict(
        font=dict(
            size=cfg.TAM_TITULO,
            color=tema.TEXTO_SUAVE
        )
    ),
    tickfont=dict(
        color=tema.TEXTO_SUAVE
    ),
)

# template plotly
pio.templates["identifica"] = go.layout.Template(layout=dict(
    # Fonte:
    font=dict(
        family='"Source Sans 3", "Source Sans Pro", sans-serif',
        size=cfg.TAM_FONTE,
        color=tema.TEXTO
    ),
    # Paleta:
    colorway=tema.PALETA,

    # separadores (, para decimal; . para milhar)
    separators=",.",

    # cores de fundo:
    paper_bgcolor="rgba(0,0,0,0)", # fundo que fica ao redor
    plot_bgcolor="rgba(0,0,0,0)",

    # altura padrao dos graficos:
    height=cfg.ALTURA_GRAFICO,

    # margem:
    margin=dict(l=0, r=8, t=8, b=0),

    # hover:
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="white",
        bordercolor=tema.GRADE,
        align="left",
        font=dict(
            family='"JetBrains Mono", monospace',
            size=cfg.TAM_FONTE_PEQUENA,
            color=tema.TEXTO
        )
    ),

    # legenda
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.12,
        x=0,
        title_text=""
    ),

    # barras
    barcornerradius=cfg.AREDONDAMENTO_BARRAS,
    bargap=cfg.ESPACAMENTO_BARRAS,

    # eixos
    xaxis=dict(
        **CONFIG_EIXOS,
        showgrid=False,
        linecolor=tema.GRADE,
        ticks=""
    ),

    yaxis=dict(
        **CONFIG_EIXOS,
        gridcolor=tema.GRADE,
        zeroline=False
    ),
))

pio.templates.default = "identifica"
