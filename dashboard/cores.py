"""
Cores do Dashbord

Autor: Gabriel
Data de criação: 22/11/2026
"""

from plotly.colors import sample_colorscale

# Tema: seoul256
LARANJA  = "#9A7200"  # 94
CEU      = "#70BDDF"  # 74
VERDE    = "#719872"  # 65
AMARELO  = "#BDBB72"  # 143
AZUL     = "#0074BE"  # 25
VERMELHO = "#9B1300"  # 88
ROSA     = "#9B1D72"  # 89

POSITIVO = "#009799"  # 23
NEGATIVO = VERMELHO   # 88

TEXTO       = "#4B4B4B"  # 237
TEXTO_SUAVE = "#616161"  # 239
NEUTRO      = "#BFBFBF"  # 249
GRADE       = "#D1D0D1"  # 251
FUNDO_SUAVE = "#E1E1E1"  # 253
AZUL_CLARO  = "#BCE0FF"  # 153
MARINHO     = "#007299"  # 24


# graficos com multiplas linhas usam as seguintes cores, em sequencia.
PALETA = [AZUL, VERMELHO, AMARELO, CEU, ROSA, VERDE, LARANJA]


CORES_SEXO = {
    "Homens": AZUL,
    "Mulheres": ROSA,
    "Total": MARINHO
}

RAMPA_AZUL = ["#98BEDE", "#719CDF", "#0099BD", "#0074BE", "#007299"]

def rampa(n: int) -> list[str]:
    if n <= 1:
        return [AZUL]

    escala = [[i / (len(RAMPA_AZUL) - 1), cor] for i, cor in enumerate(RAMPA_AZUL)]
    return sample_colorscale(escala, [i / (n - 1) for i in range(n)])
