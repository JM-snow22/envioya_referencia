"""Pruebas de caja negra para calc() de EnvíaYa.

Especificación de Jesús Enrique Mendoza González (código 0182410095 -> A=4 B=1 C=0 D=0 E=9 F=5):
PMAX=50 kg, L1=3 kg (incluido, D par), L2=10 kg, RR=15 %, RN=50 %,
V=15 %, S=$2.000 (después de descuentos, E impar),
descuentos combinados (cliente y luego cupón, B impar),
cupón inexistente = error (F impar).

Los resultados esperados se calcularon a mano (ver informe, Parte 3).
"""
import pytest

from envios import calc

ERROR = "ERROR"

# (id, peso, zona, cliente, dia, cupon, esperado)
CASOS = [
    # Valores límite de peso
    ("CP01", 0, "urbana", "normal", 2, None, ERROR),
    ("CP02", 0.01, "urbana", "normal", 2, None, 6000),
    ("CP03", 2.99, "urbana", "normal", 2, None, 6000),
    ("CP04", 3, "urbana", "normal", 2, None, 6000),
    ("CP05", 3.01, "urbana", "normal", 2, None, 9000),
    ("CP06", 9.99, "urbana", "normal", 2, None, 9000),
    ("CP07", 10, "urbana", "normal", 2, None, 9000),
    ("CP08", 10.01, "urbana", "normal", 2, None, 9000),
    ("CP09", 49.99, "urbana", "normal", 2, None, 41000),
    ("CP10", 50, "urbana", "normal", 2, None, 41000),
    ("CP11", 50.01, "urbana", "normal", 2, None, ERROR),
    ("CP12", -5, "urbana", "normal", 2, None, ERROR),
    # Particiones de zona
    ("CP13", 5, "rural", "normal", 2, None, 10400),
    ("CP14", 5, "nacional", "normal", 2, None, 13500),
    ("CP15", 5, "internacional", "normal", 2, None, ERROR),
    ("CP16", 12.5, "nacional", "normal", 2, None, 16500),
    # Particiones y límites de día
    ("CP17", 5, "urbana", "normal", 0, None, ERROR),
    ("CP18", 5, "urbana", "normal", 8, None, ERROR),
    ("CP19", 5, "urbana", "normal", 5, None, 9000),
    # Tabla de decisión cliente x cupón x fin de semana
    ("CP20", 5, "urbana", "normal", 3, None, 9000),
    ("CP21", 5, "urbana", "normal", 6, None, 11000),
    ("CP22", 5, "urbana", "normal", 3, "ENVIO10", 8100),
    ("CP23", 5, "urbana", "normal", 7, "ENVIO10", 10100),
    ("CP24", 5, "urbana", "frecuente", 3, None, 8600),
    ("CP25", 5, "urbana", "frecuente", 6, None, 10600),
    ("CP26", 5, "urbana", "frecuente", 3, "ENVIO10", 7700),
    ("CP27", 5, "urbana", "frecuente", 7, "ENVIO10", 9700),
    ("CP28", 5, "urbana", "vip", 3, None, 7700),
    ("CP29", 5, "urbana", "vip", 7, None, 9700),
    ("CP30", 5, "urbana", "vip", 3, "ENVIO10", 6900),
    ("CP31", 5, "urbana", "vip", 6, "ENVIO10", 8900),
    ("CP32", 5, "urbana", "vip", 3, "ENVIO20", ERROR),
    # Mínimo, redondeo y combinados
    ("CP33", 2, "urbana", "vip", 1, "ENVIO10", 5000),
    ("CP34", 4, "rural", "vip", 6, "ENVIO10", 9900),
    ("CP35", 20, "rural", "frecuente", 7, "ENVIO10", 18700),
    ("CP36", 3, "rural", "frecuente", 4, None, 6600),
]


@pytest.mark.parametrize(
    "peso, zona, cliente, dia, cupon, esperado",
    [caso[1:] for caso in CASOS],
    ids=[caso[0] for caso in CASOS],
)
def test_calc_caja_negra(peso, zona, cliente, dia, cupon, esperado):
    if esperado == ERROR:
        with pytest.raises(ValueError):
            calc(peso, zona, cliente, dia, cupon)
    else:
        assert calc(peso, zona, cliente, dia, cupon) == esperado


@pytest.mark.parametrize("peso", [0, 50.01, -5], ids=["CP01-msg", "CP11-msg", "CP12-msg"])
def test_mensaje_peso_invalido(peso):
    """R1: el error debe decir exactamente 'peso inválido'."""
    with pytest.raises(ValueError, match="^peso inválido$"):
        calc(peso, "urbana", "normal", 2)
