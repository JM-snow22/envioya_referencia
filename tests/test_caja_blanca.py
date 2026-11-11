"""Pruebas de caja blanca: un caso por cada camino independiente
del grafo de flujo de calc() heredado (V(G) = 14). Ver informe, Parte 4."""
import pytest

from envios import calc


def test_camino_01_base():
    assert calc(2, "urbana", "normal", 3) == 6000


def test_camino_02_peso_invalido():
    with pytest.raises(ValueError):
        calc(0, "urbana", "normal", 3)


def test_camino_03_tramo_2():
    assert calc(5, "urbana", "normal", 3) == 9000


def test_camino_04_tramo_3():
    assert calc(12, "urbana", "normal", 3) == 10600


def test_camino_05_rural():
    assert calc(2, "rural", "normal", 3) == 6900


def test_camino_06_nacional():
    assert calc(2, "nacional", "normal", 3) == 9000


def test_camino_07_zona_invalida():
    with pytest.raises(ValueError):
        calc(2, "marte", "normal", 3)


def test_camino_08_fin_de_semana():
    assert calc(2, "urbana", "normal", 7) == 8000


def test_camino_09_frecuente():
    assert calc(2, "urbana", "frecuente", 3) == 5700


def test_camino_10_vip():
    assert calc(2, "urbana", "vip", 3) == 5100


def test_camino_11_cupon_envio10():
    assert calc(2, "urbana", "normal", 3, "ENVIO10") == 5400


def test_camino_12_cupon_inexistente():
    with pytest.raises(ValueError):
        calc(2, "urbana", "normal", 3, "XYZ")


def test_camino_13_minimo():
    assert calc(2, "urbana", "vip", 3, "ENVIO10") == 5000


def test_camino_14_flag_eliminado():
    """En v1 este camino imprimía con flag=True. En v2 el argumento flag se
    eliminó (cambio de interfaz -> versión MAJOR), así que el camino ya no
    existe: se verifica el mismo resultado y que flag ya no se acepta."""
    assert calc(2, "urbana", "normal", 3, None) == 6000
    with pytest.raises(TypeError):
        calc(2, "urbana", "normal", 3, None, flag=True)
