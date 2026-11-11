"""Solicitud de cambio 0 ((A + F) mod 3 = (4 + 5) mod 3 = 0):
zona insular (San Andrés) con recargo del 70 %; los envíos insulares no
aceptan cupón (el cupón ENVIO10 no se descuenta). Un cupón inexistente
sigue siendo error (R7). Pruebas escritas ANTES de implementar."""
import pytest

from envios import calc


@pytest.mark.parametrize(
    "peso, cliente, dia, cupon, esperado",
    [
        (5, "normal", 2, None, 15300),          # CI01: 9000 x 1,70
        (5, "normal", 2, "ENVIO10", 15300),     # CI02: el cupón no se aplica
        (2, "vip", 6, "ENVIO10", 10700),        # CI03: 6000x1,7x0,85+2000=10670
        (12, "frecuente", 3, None, 17100),      # CI04: 10600x1,7x0,95=17119
    ],
    ids=["CI01", "CI02", "CI03", "CI04"],
)
def test_zona_insular(peso, cliente, dia, cupon, esperado):
    assert calc(peso, "insular", cliente, dia, cupon) == esperado


def test_CI05_insular_con_cupon_inexistente_sigue_siendo_error():
    with pytest.raises(ValueError):
        calc(5, "insular", "normal", 2, "ENVIO20")
