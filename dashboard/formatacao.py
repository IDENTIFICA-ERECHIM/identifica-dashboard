"""
Funções de formatação de números

Autor: Gabriel
Data de criação: 22/11/2026
"""

def numero(valor: float, casas: int = 0) -> str:
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


def percentual(valor: float, casas: int = 1) -> str:
    return f"{numero(valor, casas)}%"


def dinheiro(valor: float, compacto: bool = True, moeda: str = "R$") -> str:
    if compacto:
        if abs(valor) >= 1e9:
            return f"{moeda} {numero(valor / 1e9, 2)} bi"
        if abs(valor) >= 1e6:
            return f"{moeda} {numero(valor / 1e6, 2)} mi"
        if abs(valor) >= 1e3:
            return f"{moeda} {numero(valor / 1e3, 2)} mil"

    return f"{moeda} {numero(valor, 2)}"


def com_unidade(valor: float, unidade: str, casas: int = 0):
    if unidade == "%":
        return percentual(valor, casas)
    if unidade == "R$":
        return dinheiro(valor)
    if unidade == "R$ cheio":
        return dinheiro(valor, compacto=False)
    if unidade == "US$":
        return dinheiro(valor, moeda="US$")
    if unidade:
        return numero(valor, casas) + " " + unidade

    return numero(valor, casas)
