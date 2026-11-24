"""
Tema: https://tailwindcss.com/docs/colors
Cores do Dashbord

Autor: Gabriel
Data de criação: 22/11/2026
"""

from plotly.colors import sample_colorscale

"""
# cores da logo (identificadas com o site: https://imagecolorpicker.com/)
MARINHO = "#142863"
VERDE   = "#059c57"

# cores do tema
AZUL     = "#1d4ed8"
LARANJA  = "#ea580c"
VIOLETA  = "#7c3aed"
CEU      = "#0284c7"
VERMELHO = "#be123c"
LIMA     = "#65a30d"
ROSA     = "#c026d3"

POSITIVO = "#059669"
NEGATIVO = "#be123c"

TEXTO       = "#0f172a"
TEXTO_SUAVE = "#64748b"
NEUTRO      = "#cbd5e1"
GRADE       = "#e2e8f0"
FUNDO_SUAVE = "#f8fafc"
AZUL_CLARO  = "#bfdbfe"


# sequencia de cores q o plotly vai usar automaticamente (colorway do plotly)
PALETA = [AZUL, VERDE, LARANJA, VIOLETA, CEU, VERMELHO, LIMA, ROSA]

RAMPA_AZUL = ["#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8", "#1e40af", "#1e3a8a", "#172554"]  # blue-400 .. blue-950
"""

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


PALETA = [AZUL, VERMELHO, AMARELO, CEU, ROSA, VERDE, LARANJA]


RAMPA_AZUL = ["#98BEDE", "#719CDF", "#0099BD", "#0074BE", "#007299"]

CORES_SEXO = {
    "Homens": AZUL,
    "Mulheres": ROSA,
    "Total": MARINHO
}

def rampa(n: int) -> list[str]:
    if n <= 1:
        return [AZUL]

    escala = [[i / (len(RAMPA_AZUL) - 1), cor] for i, cor in enumerate(RAMPA_AZUL)]
    return sample_colorscale(escala, [i / (n - 1) for i in range(n)])
