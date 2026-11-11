"""envios.py - Cálculo del costo de envío de EnvíaYa (Riohacha)."""
from decimal import Decimal, ROUND_HALF_UP

# Parámetros del negocio (código estudiantil 0182410095)
PESO_MAXIMO_KG = 50
LIMITE_TRAMO_1_KG = 3          # incluido (D = 0 es par)
LIMITE_TRAMO_2_KG = 10
TARIFA_TRAMO_1 = 6000
TARIFA_TRAMO_2 = 9000
TARIFA_KG_ADICIONAL = 800
RECARGO_RURAL = 0.15
RECARGO_NACIONAL = 0.50
DESCUENTO_FRECUENTE = 0.05
DESCUENTO_VIP = 0.15
DESCUENTO_CUPON_ENVIO10 = 0.10
CUPON_ENVIO10 = "ENVIO10"
RECARGO_FIN_DE_SEMANA = 2000   # después de los descuentos (E = 9 es impar)
COSTO_MINIMO = 5000
MULTIPLO_REDONDEO = 100
SABADO = 6
DOMINGO = 7


def calc(p, z, c, d, cup=None, flag=False):
    if p <= 0 or p > PESO_MAXIMO_KG:
        raise ValueError("peso inválido")
    if d < 1 or d > DOMINGO:
        raise ValueError("dia invalido")
    if p <= LIMITE_TRAMO_1_KG:
        t = TARIFA_TRAMO_1
    elif p <= LIMITE_TRAMO_2_KG:
        t = TARIFA_TRAMO_2
    else:
        t = TARIFA_TRAMO_2 + (p - LIMITE_TRAMO_2_KG) * TARIFA_KG_ADICIONAL
    if z == "urbana":
        pass
    elif z == "rural":
        t = t + t * RECARGO_RURAL
    elif z == "nacional":
        t = t + t * RECARGO_NACIONAL
    else:
        raise ValueError("zona invalida")
    if c == "frecuente":
        t = t - t * DESCUENTO_FRECUENTE
    if c == "vip":
        t = t - t * DESCUENTO_VIP
    if cup is not None:
        if cup == CUPON_ENVIO10:
            t = t - t * DESCUENTO_CUPON_ENVIO10
        else:
            raise ValueError("cupon inexistente")
    if d >= SABADO:
        t = t + RECARGO_FIN_DE_SEMANA
    if t < COSTO_MINIMO:
        t = COSTO_MINIMO
    if flag:
        print("costo:", t)
    redondeado = (Decimal(str(round(t, 2))) / MULTIPLO_REDONDEO).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP)
    return int(redondeado * MULTIPLO_REDONDEO)
