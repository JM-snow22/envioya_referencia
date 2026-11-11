# EnvíaYa 2.0.0 — Notas de la versión

**Fecha:** 11 de noviembre de 2026

## Resumen
Esta versión corrige los 7 defectos encontrados en la función heredada,
reorganiza el código para que sea fácil de mantener y agrega una suite de
53 pruebas automatizadas. Todas las pruebas pasan.

## Lo que cambia para quien usa la función
- **Cambio incompatible:** `calc()` ya no recibe `flag`. Si se pasa, se
  produce `TypeError`. Para ver el costo, imprima el valor devuelto.
- Ahora se lanza `ValueError` cuando la zona, el día o el cupón no son
  válidos. Antes se aceptaban en silencio y se cobraba un valor incorrecto.
- El sábado cobra el recargo de fin de semana ($2.000), sumado después de
  los descuentos.
- El resultado se redondea al múltiplo de $100 más cercano ($50 hacia arriba).

## Migración
Reemplace `calc(p, z, c, d, cup, True)` por
`print(calcular_costo_envio(p, z, c, d, cup))`. Las llamadas sin `flag`
siguen funcionando igual, con `calc` o con `calcular_costo_envio`.

## Calidad
- Pruebas: 53 de 53 pasan.
- Cobertura de sentencias y de ramas: 100 %.
