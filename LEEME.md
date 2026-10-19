# Rama de datos de Pulso Económico v2

Esta rama guarda solo los datos que actualiza el proceso automático
(`.github/workflows/actualizar-y-publicar.yml` en la rama `main`):

- `data.json`: series de tipo de cambio, bancos, reservas, balanza e ITCR.
- `noticias.json`: titulares de prensa.
- `estado.json`: salud de cada fuente (últimos intentos, errores, avisos).

El historial de esta rama es el respaldo de los datos: para recuperar una
versión anterior de `data.json`, buscar el commit en esta rama.

Punto de partida: copia de `data.json` y `noticias.json` de la v1
(`Anubis-tech/pulso-cambiario`, commit 10e17f0, 18-oct-2026).
