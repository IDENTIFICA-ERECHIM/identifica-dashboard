from ctypes import alignment
from pydoc import text

import streamlit as st

import dashboard.layout as layout

TABS = {
    "Demografia":          ":material/groups:",
    "Mercado de trabalho": ":material/work:",
    "Social":              ":material/diversity_3:",
    "Economia":            ":material/trending_up:",
}

st.set_page_config(
    page_title="Identifica Erechim",
    page_icon="img/icone.png",
    layout="wide"
)
if "boas_vindas" not in st.session_state:
    st.session_state.boas_vindas = True
    layout.modal_boas_vindas()


with st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center"):
    st.image("img/logo.png", width=120)
    st.title("IDENTIFICA - Dashboard Municipal Erechim/RS", width="content")

st.caption(
    "Diagnóstico socioeconômico de Erechim, integrando dados públicos de diversas fontes.",
    text_alignment="center",
)

abas = st.tabs([f"{icone} {nome}" for nome, icone in TABS.items()], key="eixo", on_change="rerun")

for aba, eixo in zip(abas, TABS):
    if aba.open:
        with aba:
            layout.render_eixo(eixo)

layout.render_footer()
