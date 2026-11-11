# Changelog

Todos los cambios importantes de este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto sigue [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

## [2.1.0] - 2026-11-11

### Added
- Zona `insular` (San Andrés) con recargo del 70 %, implementada como una
  nueva estrategia (`ZonaInsular`) sin modificar las demás zonas.
- Pruebas CI01 a CI05 de la zona insular, escritas antes de implementar.

### Changed
- Los envíos insulares no aplican el cupón ENVIO10. Un cupón inexistente
  sigue produciendo error.
- La prueba CP15 usa ahora la zona `internacional` como ejemplo de zona
  inválida, porque `insular` pasó a ser válida.

## [2.0.0] - 2026-11-11

### Added
- Suite de pruebas automatizadas con pytest: 36 casos de caja negra, 3 de
  mensaje de error y 14 de caja blanca (uno por camino independiente).
- Medición de cobertura de sentencias y ramas con pytest-cov.
- Función `calcular_costo_envio()` con nombres de parámetros descriptivos.

### Changed
- Las zonas se implementan con el patrón Estrategia (`EstrategiaZona`,
  `ZonaUrbana`, `ZonaRural`, `ZonaNacional`).
- Los números mágicos se reemplazaron por constantes con nombre.
- El cálculo se dividió en funciones pequeñas (validaciones, tarifa base,
  descuentos, recargo de fin de semana, redondeo).
- Los montos se calculan con `Decimal` en lugar de `float`.

### Removed
- **BREAKING:** el argumento `flag` de `calc()` (imprimía el costo en
  consola). Quien lo necesite debe imprimir el valor devuelto.

### Fixed
- DEF-01: el sábado no cobraba el recargo de fin de semana.
- DEF-02: el recargo de fin de semana se sumaba antes de los descuentos.
- DEF-03: una zona no válida se cobraba como urbana en lugar de dar error.
- DEF-04: un día fuera de 1 a 7 no daba error.
- DEF-05: un cupón inexistente se ignoraba en lugar de dar error.
- DEF-06: el redondeo truncaba en vez de ir al múltiplo de $100 más cercano.
- DEF-07: el mensaje de error de peso no decía exactamente "peso inválido".

## [1.0.0] - 2026-11-11

### Added
- Código heredado de `calc()` con la configuración de mis parámetros.
