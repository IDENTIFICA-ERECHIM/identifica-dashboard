import dashboard.cores as tema
import textwrap

def cor_da_serie(cores, nome, num_serie):
    padrao = tema.PALETA[num_serie % len(tema.PALETA)]

    if cores is None:
        return padrao

    if isinstance(cores, dict):
        return cores.get(nome, padrao)

    return cores[num_serie]


def texto_hover(eixo, casas, unidade, nome=None):
    texto = "%{" + eixo + ":,." + str(casas) + "f} " + unidade
    if nome:
        texto = f"{nome}: {texto}"

    return texto + "<extra></extra>" # extra remove a area adicional padrao do plotly


def formatar_eixo_anos(fig, df, unidade=""):
    # padroniza os anos no eixo X dos graficos (que possuem anos no eixo X)
    anos = sorted(df["ano"].unique())

    if len(anos) <= 12:
        fig.update_xaxes(tickformat="d", tickvals=anos)
    else:
        fig.update_xaxes(tickformat="d")

    if unidade:
        fig.add_annotation(
            text=unidade,
            xref="paper",
            yref="paper",
            x=0,
            y=1,
            yshift=8,
            xanchor="left",
            yanchor="bottom",
            showarrow=False,
            font=dict(size=12, color=tema.TEXTO_SUAVE)
        )

        fig.update_layout(margin_t=32)

def quebrar_texto(texto, largura=34):
    # dividir textos muito longos em varias linhas
    linhas_do_texto = textwrap.wrap(str(texto), largura)

    if not linhas_do_texto:
        return str(texto)

    return "<br>".join(linhas_do_texto)


def altura_grafico_horizontal(rotulos, barras_por_categoria=1):
    # calcula automaticamente a altura de um grafico horizontal
    linhas_de_texto = 0

    for rotulo in rotulos:
        linhas_de_texto += rotulo.count("<br>") + 1

    altura = 16 * linhas_de_texto + 20 * barras_por_categoria * len(rotulos) + 70

    return max(altura, 200)
