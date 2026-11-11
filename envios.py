"""envios.py - Cálculo del costo de envío de EnvíaYa (Riohacha).

Especificación personalizada (código 0182410095):
A=4 B=1 C=0 D=0 E=9 F=5 -> PMAX=50, L1=3 (incluido), L2=10, RR=15 %,
RN=50 %, V=15 %, S=$2.000 después de descuentos, descuentos combinados
(cliente y luego cupón), cupón inexistente = error.
"""
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

# ---------------------------------------------------------------- constantes
PESO_MAXIMO_KG = Decimal("50")
LIMITE_TRAMO_1_KG = Decimal("3")       # incluido (D = 0 es par)
LIMITE_TRAMO_2_KG = Decimal("10")
TARIFA_TRAMO_1 = Decimal("6000")
TARIFA_TRAMO_2 = Decimal("9000")
TARIFA_KG_ADICIONAL = Decimal("800")

RECARGO_RURAL = Decimal("0.15")
RECARGO_NACIONAL = Decimal("0.50")
RECARGO_INSULAR = Decimal("0.70")       # solicitud de cambio 0 (San Andrés)

DESCUENTOS_CLIENTE = {
    "normal": Decimal("0"),
    "frecuente": Decimal("0.05"),
    "vip": Decimal("0.15"),
}
CUPONES = {"ENVIO10": Decimal("0.10")}

RECARGO_FIN_DE_SEMANA = Decimal("2000")  # después de descuentos (E = 9 impar)
DIAS_FIN_DE_SEMANA = (6, 7)              # sábado y domingo
PRIMER_DIA, ULTIMO_DIA = 1, 7

COSTO_MINIMO = Decimal("5000")
MULTIPLO_REDONDEO = Decimal("100")


# ------------------------------------------------- patrón Estrategia (zonas)
class EstrategiaZona(ABC):
    """Cada zona sabe cómo aplicar su recargo sobre la tarifa base."""

    porcentaje_recargo = Decimal("0")
    acepta_cupon = True

    def aplicar_recargo(self, tarifa: Decimal) -> Decimal:
        return tarifa * (1 + self.porcentaje_recargo)

    @abstractmethod
    def nombre(self) -> str:
        """Nombre de la zona tal como llega a la función."""


class ZonaUrbana(EstrategiaZona):
    def nombre(self) -> str:
        return "urbana"


class ZonaRural(EstrategiaZona):
    porcentaje_recargo = RECARGO_RURAL

    def nombre(self) -> str:
        return "rural"


class ZonaNacional(EstrategiaZona):
    porcentaje_recargo = RECARGO_NACIONAL

    def nombre(self) -> str:
        return "nacional"


class ZonaInsular(EstrategiaZona):
    """San Andrés: recargo del 70 % y no acepta cupón."""

    porcentaje_recargo = RECARGO_INSULAR
    acepta_cupon = False

    def nombre(self) -> str:
        return "insular"


ZONAS = {
    z.nombre(): z
    for z in (ZonaUrbana(), ZonaRural(), ZonaNacional(), ZonaInsular())
}


# ------------------------------------------------------ funciones extraídas
def validar_peso(peso: Decimal) -> None:
    if not 0 < peso <= PESO_MAXIMO_KG:
        raise ValueError("peso inválido")


def validar_dia(dia: int) -> None:
    if not PRIMER_DIA <= dia <= ULTIMO_DIA:
        raise ValueError("día inválido")


def obtener_zona(zona: str) -> EstrategiaZona:
    if zona not in ZONAS:
        raise ValueError("zona inválida")
    return ZONAS[zona]


def validar_cupon(cupon) -> None:
    if cupon is not None and cupon not in CUPONES:
        raise ValueError("cupón inexistente")


def tarifa_base(peso: Decimal) -> Decimal:
    if peso <= LIMITE_TRAMO_1_KG:
        return TARIFA_TRAMO_1
    if peso <= LIMITE_TRAMO_2_KG:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (peso - LIMITE_TRAMO_2_KG) * TARIFA_KG_ADICIONAL


def aplicar_descuentos(tarifa: Decimal, cliente: str, cupon) -> Decimal:
    """Regla B impar: primero el descuento del cliente y luego el cupón."""
    tarifa = tarifa * (1 - DESCUENTOS_CLIENTE.get(cliente, Decimal("0")))
    if cupon is not None:
        tarifa = tarifa * (1 - CUPONES[cupon])
    return tarifa


def aplicar_recargo_fin_de_semana(tarifa: Decimal, dia: int) -> Decimal:
    if dia in DIAS_FIN_DE_SEMANA:
        return tarifa + RECARGO_FIN_DE_SEMANA
    return tarifa


def redondear_a_100(valor: Decimal) -> int:
    """Múltiplo de $100 más cercano; los $50 redondean hacia arriba."""
    centenas = (valor / MULTIPLO_REDONDEO).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(centenas * MULTIPLO_REDONDEO)


# ------------------------------------------------------------ función pública
def calcular_costo_envio(peso, zona, cliente, dia, cupon=None) -> int:
    """Devuelve el costo del envío en pesos (múltiplo de 100)."""
    peso = Decimal(str(peso))
    validar_peso(peso)
    validar_dia(dia)
    estrategia_zona = obtener_zona(zona)
    validar_cupon(cupon)

    costo = tarifa_base(peso)
    costo = estrategia_zona.aplicar_recargo(costo)
    cupon_aplicable = cupon if estrategia_zona.acepta_cupon else None
    costo = aplicar_descuentos(costo, cliente, cupon_aplicable)
    costo = aplicar_recargo_fin_de_semana(costo, dia)
    costo = max(costo, COSTO_MINIMO)
    return redondear_a_100(costo)


# Nombre anterior, conservado para no romper a quien ya llama a calc().
calc = calcular_costo_envio
