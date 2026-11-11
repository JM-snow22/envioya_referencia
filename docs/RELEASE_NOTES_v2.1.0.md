# EnvíaYa 2.1.0 — Notas de la versión

**Fecha:** 11 de noviembre de 2026

## Novedades
- Nueva zona **insular** (San Andrés) con recargo del 70 %.
- Los envíos insulares **no aplican el cupón ENVIO10**. Si se envía un cupón
  que no existe, sigue siendo error.

## Compatibilidad
Versión compatible con 2.0.0: no cambia la firma de la función y las
llamadas existentes devuelven lo mismo. La única diferencia es que
`"insular"` ahora es una zona válida en lugar de producir error.

## Calidad
- Pruebas: 58 de 58 pasan (53 de regresión + 5 nuevas).
- Cobertura de sentencias y de ramas: 100 %.
