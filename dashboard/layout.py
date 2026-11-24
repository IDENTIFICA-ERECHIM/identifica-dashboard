"""
Componentes reutilizáveis para a interface

Autor: Gabriel
Data de criação: 22/11/2026
"""

from itertools import groupby
from PIL import Image

import streamlit as st

import dashboard.dados as dados
from dashboard.indicadores import GRAFICOS

import dashboard.icones as icones

MENSAGENS_STATUS = {
    "em_desenvolvimento":  f"{icones.DEV} Em desenvolvimento",
}


def grafico(ind: dict):
    status = ind.get("status", "ativo")
    if status != "ativo":
        st.caption(MENSAGENS_STATUS[status])
        return

    funcao = GRAFICOS.get(ind["cod"])
    if funcao is None:
        st.caption(":material/construction: Gráfico ainda não implementado.")
        return

    faltando = [t for t in ind["tabelas"] if t not in dados.get_tabelas_existentes()]
    if faltando:
        st.caption(f":material/database_off: Tabela(s) ainda não carregada(s) pelo ETL: `{', '.join(faltando)}`")
        return

    try:
        funcao(*[dados.carregar_tabela(t) for t in ind["tabelas"]])
    except Exception as erro:
        st.error(f"Não foi possível montar este indicador: {erro!r}", icon=":material/error:")


@st.fragment
def render_indicador(ind: dict):
    with st.container(border=True):
        st.markdown(f"##### {ind['cod']}: {ind['titulo']}")
        st.markdown(ind["descricao"])

        if ind.get("colapsavel"):
            with st.expander("Ver gráfico", expanded=False):
                grafico(ind)
        else:
            grafico(ind)

        if ind.get("fonte"):
            st.caption(f"{icones.BD} {ind['fonte']}")
        if ind.get("aviso"):
            st.caption(f"{icones.AVISO} {ind['aviso']}")


def linha(indicadores: list[dict]):
    if not indicadores:
        return

    for coluna, ind in zip(st.columns(2, gap="medium"), indicadores):
        with coluna:
            render_indicador(ind)

def grade(indicadores: list[dict]):
    """
    Dois cards de indicador por linha, a nao ser que:
    o indicador tenha largo=true no indicadores.toml. Nessa caso, ele ocupa a linha inteira.
    """
    fila = []

    for ind in indicadores:
        if ind.get("largo"):
            linha(fila)
            fila = []
            render_indicador(ind)
        else:
            fila.append(ind)
            if len(fila) == 2:
                linha(fila)
                fila = []

    linha(fila)


def render_eixo(eixo: str):
    indicadores = [ind for ind in dados.carregar_metadados() if ind["eixo"] == eixo]

    for tema, grupo in groupby(indicadores, key=lambda ind: ind["tema"]):
        st.subheader(tema, divider="gray")
        grade(list(grupo))



# painel de boas vindas
@st.dialog("Bem-vindo ao dashboard municipal de Erechim!", width="large")
def modal_boas_vindas():
    st.markdown(
      f"""
        Este dashboard é o resultado do projeto IDENTIFICA, um projeto público realizado pelo
        [IFRS – Campus Erechim](https://ifrs.edu.br/erechim/),
        [UFFS – Campus Erechim](https://www.uffs.edu.br/uffs/nossos-campi/campus-erechim) e
        [URI – Erechim](https://www.uricer.edu.br/site/)
        em parceria com a Prefeitura de Erechim e o CODER,
        visando elaborar um diagnóstico socioeconômico do município.

        O dashboard possui 70 indicadores, que surgiram de uma análise que buscou
        identificar os dados mais importantes para compor um painel municipal.

        Os indicadores se organizam em quatro eixos principais: Demografia,
        Mercado de Trabalho, Indicadores Sociais e Economia e Setores Produtivos, e
        são mostrados em gráficos, para que qualquer pessoa consiga entender.

        Para qualquer dúvida adicional sobre algum indicador, consulte as informações oficiais da respectiva base de dados.
        A fonte de cada indicador fica logo abaixo de seu gráfico, indicada pelo ícone: {icones.BD}
    """
    )
    if st.button("Continuar", type="primary", width="stretch"):
        st.rerun()


# Footer
def preparar_img(path, largura_canvas=900, altura_canvas=240):
    imagem = Image.open(path).convert("RGBA")

    bbox = imagem.getchannel("A").getbbox()
    if bbox:
        imagem = imagem.crop(bbox)

    # Redimensiona para ocupar toda a altura
    fator = altura_canvas / imagem.height
    nova_largura = round(imagem.width * fator)
    nova_altura = altura_canvas

    # Evita que logos muito largos ultrapassem o canvas
    if nova_largura > largura_canvas:
        fator = largura_canvas / imagem.width
        nova_largura = largura_canvas
        nova_altura = round(imagem.height * fator)

    imagem = imagem.resize(
        (nova_largura, nova_altura),
        Image.Resampling.LANCZOS
    )

    # Canvas transparente com dimensões padronizadas
    canvas = Image.new(
        "RGBA",
        (largura_canvas, altura_canvas),
        (0, 0, 0, 0)
    )

    x = (largura_canvas - nova_largura) // 2
    y = (altura_canvas - nova_altura) // 2

    canvas.alpha_composite(imagem, (x, y))

    return canvas


def render_footer():
    DESENVOLVEDORES = [
        ("img/logo_if.png",   "https://ifrs.edu.br/erechim/"),
        ("img/logo_uri.png",  "https://www.uricer.edu.br/site/"),
        ("img/logo_uffs.png", "https://www.uffs.edu.br/uffs/nossos-campi/campus-erechim"),
    ]

    APOIADORES = [
        ("img/logo_prefeitura.png", "https://www.pmerechim.rs.gov.br/"),
        ("img/logo_coder.png",      "https://www.codererechim.com.br/"),
    ]

    LARGURA_LOGO = 250

    def secao(titulo):
        st.space("small")
        st.caption(titulo, text_alignment="center")
        return st.container(horizontal=True, horizontal_alignment="center",
                            vertical_alignment="center", gap="large")

    def render_logos(titulo, logos):
        with secao(titulo):
            for caminho, url in logos:
                st.image(preparar_img(caminho), width=LARGURA_LOGO, link=url)

    st.divider()

    render_logos("DESENVOLVIDO POR:", DESENVOLVEDORES)
    render_logos("COM APOIO DE:", APOIADORES)

    with secao("CÓDIGO FONTE:"):
        st.link_button(
            "Acesse no GitHub",
            "https://github.com/IDENTIFICA-ERECHIM",
            icon=":material/code:",
        )
