# Decisiones de la versión 2.0

Cada decisión indica qué se eligió, qué alternativas se descartaron y por qué. Las marcadas con **[a decidir por el dueño]** quedan abiertas para el lanzamiento.

---

## D1. Punto de partida: copia sin historial

- **Elegido:** repositorio nuevo (`Anubis-tech/pulso-cambiario-v2`, no es fork), con una copia exacta de los archivos de la v1 en el commit **`10e17f0562c240227a8d46398986ed889634c089`** (18-oct-2026, 21:26 hora Bolivia). Es el primer commit de este repo: `837e3ed`.
- **Descartado:** fork (queda vinculado a la v1 en GitHub) y rama dentro de la v1 (mezcla versiones).
- **Por qué:** independencia total. La v2 se puede borrar sin tocar la v1. Además, revisé el historial completo de la v1 (298 commits) y no tiene secretos, así que no había nada que limpiar.
- **Workflows de la v1:** no se copiaron como activos. Se habrían puesto a consultar las APIs y a publicar desde este repo.

## D2. Datos en una rama separada (`datos`)

- **Elegido:** `main` tiene solo código y textos. Los datos (`data.json`, `noticias.json`, `estado.json`) viven en la rama `datos`, que el proceso automático actualiza.
- **Descartado:** guardar los datos en `main` como la v1. Hacía que el 85% de los commits fueran automáticos (250 de 298) y mezclaba cambios de código con ruido.
- **Por qué:** el historial de `main` queda legible y revertible, y el historial de `datos` funciona como respaldo de cada versión de los datos.
- **Riesgo conocido:** GitHub desactiva los workflows programados de repos públicos tras 60 días sin actividad. No está claro si los commits en una rama que no es la principal cuentan como actividad. Ver `MANTENIMIENTO.md`.

## D3. Generador propio en Python (sin framework)

- **Elegido:** un script (`scripts/construir.py`, con Jinja2 y Markdown) que genera HTML estático con las cifras del día ya escritas.
- **Descartado:** Astro y Eleventy (agregan Node.js, `node_modules` y un segundo lenguaje al proyecto) y seguir con HTML a mano (dos páginas de 60–70 KB cada una con todo repetido).
- **Por qué:** el pipeline ya era Python. Un solo lenguaje, cuatro dependencias y ningún paso de compilación de JavaScript. Es lo más fácil de mantener para alguien que no es desarrollador.

## D4. Cifras en el HTML, gráficos con JavaScript

- **Elegido:** cada página trae sus cifras escritas en el HTML. Los gráficos se dibujan después, con archivos de datos chicos (`/datos/*.json`) en lugar del `data.json` completo de 389 KB.
- **Por qué:** Google lee el dato sin ejecutar JavaScript, el usuario lo ve antes y la página no depende de que todo cargue bien.
- **Compatibilidad:** se sigue publicando `/data.json` en la misma ruta, por si alguien lo usa.

## D5. Una página por intención de búsqueda

- **Elegido:** URLs separadas para dólar hoy (`/`), paralelo, oficial, bancos, brecha, conversor, reservas, balanza e ITCR. Las URLs son cortas, en español y terminan en `/`.
- **Descartado:** mantener todo en una sola página.
- **Por qué:** cada página puede posicionarse para su búsqueda ("dólar paralelo Bolivia", "reservas internacionales Bolivia") y aumenta el inventario de páginas con contenido propio para AdSense.
- **Redirección:** `/cambiario/bancos.html` → `/tipo-de-cambio-bancos/`. En GitHub Pages se hace con una página que redirige y declara el canonical nuevo; Google lo trata como una redirección. En Cloudflare Pages se hace con un 301 real (archivo `_redirects`, ya generado).

## D6. Hosting definitivo **[a decidir por el dueño]**

| | GitHub Pages (actual) | Cloudflare Pages |
|---|---|---|
| Costo | Gratis | Gratis |
| Cabeceras de seguridad (HSTS, X-Frame-Options, CSP real) | No se pueden configurar | Sí (`_headers` ya generado) |
| Redirección 301 real | No (se usa meta refresh + canonical) | Sí (`_redirects` ya generado) |
| Analítica sin cookies | No incluida | Cloudflare Web Analytics, gratis |
| Medir el paralelo cada 15 minutos de verdad | No (depende del cron de GitHub) | Posible con un *Worker* programado, gratis |
| Complejidad para el dueño | Ninguna (ya funciona) | Mover el DNS a Cloudflare, crear la cuenta y conectar el repo |

**Recomendación:** lanzar en **GitHub Pages**, con el menor cambio posible el día de la migración, y evaluar Cloudflare un mes después con datos de tráfico. La v2 ya funciona en los dos sin tocar código.

## D7. Política de seguridad de contenido (CSP)

- **Sin anuncios (preview y producción sin AdSense):** CSP estricta. Solo se permiten scripts propios, ninguna conexión a terceros y ningún iframe. Está verificado: las 27 páginas abren sin errores ni violaciones de CSP.
- **Con AdSense activo:** CSP mínima (`object-src 'none'; base-uri 'self'; upgrade-insecure-requests`).
- **Por qué:** AdSense carga código desde muchos dominios de Google que cambian sin aviso. Una lista cerrada termina bloqueando anuncios, y eso significa ingresos perdidos sin que nadie lo note. Google documenta el uso de CSP estricta con *nonces*, pero eso requiere un servidor que genere un nonce por visita, y un sitio estático no lo tiene.
- **Limitación:** en GitHub Pages la CSP va en una etiqueta `<meta>`, que no admite `frame-ancestors` ni reportes de violaciones.

## D8. Tipografías y librerías servidas desde el sitio

- Archivo, IBM Plex Sans e IBM Plex Mono se descargan desde el propio dominio, solo en los 4 pesos que se usan (unos 77 KB en total).
- Chart.js 4.4.1 (la misma versión de la v1) se sirve desde el sitio y se carga solo cuando el lector llega a la herramienta por banco.
- **Por qué:** elimina el bloqueo de Google Fonts (480 ms según Lighthouse) y la dependencia de un CDN externo sin verificación de integridad. Como los archivos son propios, no hace falta SRI.

## D9. Herramienta por banco desde el punto de vista de quien vende dólares

- **Cambio:** en la v1, verde significaba "el banco compró más barato que el mercado", que es la mirada del banco. En la v2, verde significa "el banco pagó más que el promedio", que es la mirada de la persona que vende dólares.
- **Por qué:** el público del sitio son personas y empresas que cambian dólares, no los bancos.
- **Reversible:** son 10 líneas en `sitio/estaticos/js/bancos.js` (comentadas al inicio del archivo).

## D10. Correcciones de datos de la v1

1. **"Reservas brutas" → reservas internacionales netas (RIN).** El campo `neta` viene de la planilla del BCB "Reservas Internacionales Netas por componentes". La etiqueta de la v1 era incorrecta.
2. **Tramo 1-dic-2025 a fines de junio de 2026 de la serie "TCO":** son los valores del **valor referencial** que el BCB publicó desde el 1-dic-2025 (fuente: Los Tiempos, 1-dic-2025), mientras el oficial legal seguía en 6,86 / 6,96. Los gráficos lo marcan con sombreado y el texto lo explica. No se modificaron los datos; solo se etiquetaron.
3. **Frecuencia del paralelo:** la v1 promete "en vivo cada 15 minutos". En los 30 días previos hubo 170 mediciones (mediana: una cada ~4 horas). La v2 muestra siempre la hora de la última medición y dice que se *intenta* medir cada 15 minutos.
4. **Fuente del TCO:** la v1 decía "directamente desde las fuentes oficiales", pero el TCO venía de `apibcb.cucu.bo`, un servicio de terceros. La v2 lo declara en la metodología. **[A decidir]** si se reemplaza por una lectura directa del sitio del BCB. No lo hice porque desde este entorno no tengo acceso a `bcb.gob.bo` para probarlo, y prefiero no cambiar la fuente de la cifra principal sin poder verificarla.

## D11. Frecuencia de consulta de las fuentes

- **Paralelo y TCO en cada corrida (cada 15 minutos programados).** Es una consulta liviana a cada uno. El TCO se publica a las 23:30, y así aparece en el sitio en minutos y no a las 02:00 como en la v1.
- **BCB (bancos, reservas, balanza, ITCR) y noticias:** cada 3 horas, como en la v1.
- **Carga sobre las APIs:** mientras la v1 y la v2 convivan, Binance recibe hasta 2 consultas cada 15 minutos en lugar de 1. Es un volumen despreciable y no pone en riesgo a la v1.

## D12. Alertas de datos atrasados

Umbrales: paralelo 8 h, TCO 4 días, bancos 6 días, reservas 21 días, balanza e ITCR 80 días, noticias 3 días. El del paralelo es de 8 horas y no de 3 porque, con la frecuencia real actual (unas 4 horas entre mediciones), un umbral de 3 horas dispararía alertas falsas todo el tiempo. Se avisa **una vez por problema y por día**, con un correo automático de GitHub al marcar la corrida en rojo.

## D13. Anuncios: espacios reservados, no activados

En el preview, los anuncios son recuadros grises con la etiqueta "Espacio publicitario". Reservan su alto, así que cuando haya anuncios reales el contenido no salta (CLS ≈ 0). Hay 3 posiciones por página como máximo: superior (banner horizontal), medio e inferior. Se activan con dos campos de `config/sitio.json`.

## D14. Conflicto de interés **[a decidir por el dueño]**

El sitio compara bancos, y el responsable trabaja en uno de ellos (Banco Fortaleza). En el dato del 16-oct-2026, Banco Fortaleza aparece primero ("el que más pagó") por puro orden de los datos. Recomiendo:
1. Declarar el vínculo en "Acerca de" (campo `responsable.declaracion_intereses` en `config/sitio.json`). Mientras está vacío, la página muestra un aviso.
2. Consultar las políticas de su empleador sobre actividades externas y uso de información del sistema financiero, aunque los datos sean públicos.

No es un problema técnico, pero si un lector lo descubre por su cuenta, la credibilidad del sitio se resiente.
