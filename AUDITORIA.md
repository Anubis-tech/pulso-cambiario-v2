# Auditoría de la v1 — Pulso Económico (elpulsoeconomico.com)

**Fecha:** 18 de octubre de 2026
**Versión auditada:** repositorio `Anubis-tech/pulso-cambiario`, commit `10e17f0` (18-oct-2026, 21:26 hora Bolivia).
**Método:** lectura del código fuente, del historial completo de git (298 commits) y mediciones locales con Lighthouse 13.5 y Chromium 141.

> **Limitación declarada.** Desde el entorno donde se hizo esta auditoría no hay acceso de red a `elpulsoeconomico.com`, a `bcb.gob.bo` ni a Google Fonts. Por eso las mediciones se hicieron sirviendo los mismos archivos de la v1 en un servidor local, con la conexión móvil lenta que Lighthouse simula. Los números sirven para **comparar v1 contra v2 en igualdad de condiciones**, pero no son las cifras exactas que vería un visitante real. En el sitio real, GitHub Pages comprime los archivos y la página pesa menos que aquí; Google Fonts, en cambio, agrega una demora que aquí no se pudo medir.

---

## 1. Arquitectura

| Elemento | Qué hay |
|---|---|
| Tipo de sitio | HTML estático, sin generador de sitios. Dos páginas hechas a mano. |
| Páginas | `index.html` (70 KB, 1.455 líneas) y `cambiario/bancos.html` (58 KB, 1.098 líneas). Cada una lleva todo su CSS y JavaScript adentro. |
| Datos | `data.json` (389 KB) con todas las series y `noticias.json` (3 KB). |
| Gráficos | En el inicio, un motor de gráficos SVG propio (bien hecho y liviano). En bancos, **Chart.js 4.4.1 desde un CDN externo** (`cdn.jsdelivr.net`), sin verificación de integridad. |
| Tipografía | Archivo, IBM Plex Sans e IBM Plex Mono desde Google Fonts. Es un recurso que bloquea el dibujado de la página. |
| Publicación | GitHub Pages mediante GitHub Actions. El dominio propio está configurado en los ajustes de Pages, no con un archivo `CNAME`. |
| Marca | "Pulso Económico" es el sitio. "Pulso Cambiario" aparece como nombre de la sección de tipo de cambio. |

**Cómo se arma la página:** el HTML llega casi vacío, con guiones ("—") en lugar de los números. El navegador descarga `data.json` (389 KB) y recién ahí JavaScript escribe las cotizaciones y dibuja los gráficos. Esto tiene dos consecuencias:

1. **Para Google:** la versión inicial de la página no contiene el dato principal. Google sí ejecuta JavaScript, pero en una segunda pasada que puede demorar, y el texto que ve primero dice "—".
2. **Para el usuario:** en el celular hay que esperar la descarga completa del archivo de datos antes de ver el número.

## 2. Pipeline de datos

Tres workflows de GitHub Actions:

| Workflow | Frecuencia | Qué hace |
|---|---|---|
| `update-usdt.yml` | Cada 15 min | Consulta Binance P2P, guarda la mediana de los 10 primeros anuncios de venta de USDT por BOB, hace commit de `data.json` y vuelve a publicar el sitio. |
| `update-data.yml` | Cada 3 h | TCO, tasas por banco, reservas, balanza cambiaria, ITCR y noticias. Hace commit y publica. |
| `deploy.yml` | En cada push | Publica el sitio. |

**Fuentes reales:**

| Dato | Fuente en el código | Observación |
|---|---|---|
| TCO oficial | `apibcb.cucu.bo` | **No es el BCB.** Es una API de terceros que replica el dato del BCB. El pie de página dice que los datos vienen "directamente desde las fuentes oficiales", y eso no es exacto. |
| Tasas por banco | `bcb.gob.bo/bcb_tco_publico_evolutivo.php` | Directo del BCB (lectura de una tabla HTML). |
| USDT/BOB | API pública no documentada de Binance P2P | Funciona, pero Binance puede cambiarla o bloquearla sin aviso. El código ya contempla respuestas vacías. |
| Reservas, balanza, ITCR | Planillas Excel del BCB | Directo del BCB. |
| Noticias | Google News RSS | Los enlaces son redirecciones de Google News, no el artículo original. |

**Puntos fuertes:** el código es defensivo. Cada fuente falla por separado, hay chequeos de sensatez (descarta saltos mayores a 15–25 %) y la zona horaria de Bolivia está bien manejada.

**Puntos débiles:**

- **"Cada 15 minutos" no se cumple.** En los 30 días previos a esta auditoría hubo **170 mediciones exitosas del paralelo**, cuando a 15 minutos deberían ser unas 2.880. Eso da entre 4 y 8 por día, separadas típicamente (mediana) por **unas 4 horas**, con huecos de hasta 9,5 horas. Hay dos causas probables, y desde aquí no se pueden separar porque no tengo acceso a los registros de Actions de la v1. La primera es que GitHub demora y omite ejecuciones programadas frecuentes. La segunda es que Binance devuelve listas vacías a servidores de centros de datos (el propio código de la v1 lo menciona). Mientras tanto, el pie de página promete actualización "en vivo cada 15 minutos".
- **Fallas silenciosas.** Si una fuente falla, el workflow igual termina "en verde" (el código lo hace a propósito). Nadie se entera si, por ejemplo, el TCO deja de actualizarse durante una semana.
- **El repositorio crece sin parar.** Cada actualización hace commit de un `data.json` de 389 KB, hasta 96 veces por día. Git comprime las diferencias, pero el historial crece indefinidamente y mezcla cambios de código con ruido automático.
- **Horario del TCO.** Desde la RD 142/2026 el BCB publica el TCO a las 23:30. El workflow de 3 horas lo recoge recién en la corrida de las 02:00 (hora Bolivia).
- **Datos que se muestran como frescos sin serlo:** `data.json` incluye series `forecast` y `garch` que ningún script actualiza (última fecha: septiembre). Hoy no se usan en la página, pero quedan como peso muerto.

## 3. SEO actual

| Aspecto | Estado | Comentario |
|---|---|---|
| `<title>` y meta description | ✅ Buenos | "Tipo de cambio Bolivia hoy: oficial, paralelo y bancario". Bien orientado. |
| Canonical | ✅ Correcto | Apunta a `elpulsoeconomico.com`. |
| Open Graph | ⚠️ Parcial | Sin imagen. Al compartir por WhatsApp se ve solo texto. `twitter:card` es "summary" sin imagen. |
| `lang` | ⚠️ `es` | Mejor `es-BO` para el público boliviano. |
| H1 | ⚠️ Débil | El H1 de la portada es "Pulso Económico" (la marca), no lo que la gente busca ("dólar hoy en Bolivia"). |
| Datos estructurados (JSON-LD) | ❌ Ninguno | |
| Sitemap | ⚠️ Mínimo | 2 URLs, sin `lastmod`. |
| robots.txt | ✅ Correcto | Permite todo y declara el sitemap. |
| Contenido indexable | ❌ Muy escaso | Las cifras se cargan con JavaScript. El texto propio es poco: títulos de sección y notas al pie. |
| Arquitectura | ❌ Una sola página para todo | Tipo de cambio, reservas, balanza e ITCR comparten la misma URL. Google no puede posicionar la página para "reservas internacionales Bolivia" y para "dólar paralelo" a la vez con la misma fuerza. |
| Favicon | ❌ No existe | Error 404. Las pestañas y los resultados de Google muestran un ícono genérico. |
| Página 404 | ❌ La genérica de GitHub | |

## 4. Rendimiento (Lighthouse, servidor local)

| Página | Dispositivo | Rendimiento | LCP | FCP | CLS | Peso total |
|---|---|---|---|---|---|---|
| Inicio | Móvil | **87** | **3,6 s** | 1,7 s | 0 | 453 KB |
| Inicio | Escritorio | 99 | 0,7 s | 0,5 s | 0,015 | 453 KB |
| Bancos | Móvil | **87** | **3,6 s** | 1,8 s | 0 | 438 KB |
| Bancos | Escritorio | 99 | 0,8 s | 0,5 s | 0,001 | 438 KB |

Los reportes completos están en `revision/v1/lighthouse/` (archivos `.json.gz`; se abren en https://googlechrome.github.io/lighthouse/viewer/ después de descomprimirlos).

- **LCP en móvil: 3,6 s.** Google considera "bueno" un valor por debajo de 2,5 s. LCP (*Largest Contentful Paint*) es el tiempo que tarda en aparecer el elemento más grande de la pantalla. Es una de las tres métricas Core Web Vitals que Google usa como señal de ranking.
- **Causas:** la fuente de Google Fonts bloquea el dibujado (Lighthouse estima 480 ms de ahorro); el archivo `data.json` es grande; y todo el contenido arranca **invisible** (`opacity:0`) hasta que una animación lo revela al hacer scroll.
- El escritorio está muy bien. El problema está en el celular, que es donde está la mayoría del público.

## 5. Seguridad

- **Historial de git limpio:** busqué claves, tokens, contraseñas y llaves privadas en los 298 commits y no hay ninguna. El repo puede seguir siendo público sin riesgo.
- **Script de terceros sin verificación:** Chart.js se carga desde `cdn.jsdelivr.net` sin SRI (*Subresource Integrity*, una huella que impide que el navegador ejecute el archivo si alguien lo altera en el CDN). Si el CDN fuera comprometido, el código ajeno correría dentro de tu sitio.
- **Sin Content Security Policy.** No hay ninguna regla que limite qué scripts puede ejecutar la página.
- **Cabeceras HTTP:** GitHub Pages no permite configurarlas (HSTS, X-Frame-Options, etc.). Esto es una limitación del hosting, no un error de la v1.
- **Permisos de los workflows:** todos tienen `contents: write`, `pages: write` e `id-token: write`. El de publicación por push solo necesita lectura del contenido, y ya la tiene. Los de datos necesitan escritura por los commits.
- **Dependencias de Python:** versiones fijadas (bien). No hay Dependabot que avise de vulnerabilidades.

## 6. Accesibilidad y móvil

- Lighthouse: 92 (inicio) y 89 (bancos).
- **Contraste insuficiente** en los valores del ticker (verde sobre blanco) y en textos grises.
- **Sin `<main>`**, el elemento que indica a los lectores de pantalla dónde empieza el contenido.
- En bancos, los botones de selección de banco son demasiado chicos para tocar con el dedo.
- **Primera pantalla del celular:** el encabezado negro con el título ocupa casi media pantalla. El dato del paralelo queda abajo y hay que hacer scroll. Ver `revision/v1/inicio-mobile-primera-pantalla.png`.

## 7. Preparación para AdSense

Requisitos oficiales de elegibilidad ([AdSense, "Eligibility requirements"](https://support.google.com/adsense/answer/9724?hl=en)): contenido propio, original y de calidad que atraiga audiencia; acceso al código HTML; y cumplimiento de las políticas del programa.

| Requisito práctico | v1 |
|---|---|
| Contenido original suficiente (texto, no solo widgets) | ❌ Casi todo son números y gráficos. Es el motivo más común de rechazo por "contenido de poco valor". |
| Política de privacidad (cookies y anuncios de terceros) | ❌ No existe |
| Página "Acerca de" o de responsable | ❌ No existe |
| Contacto | ❌ No existe |
| Navegación clara entre secciones | ⚠️ Solo 2 páginas |
| `ads.txt` | ❌ No existe (se crea al tener el ID de editor) |
| Espacios reservados para anuncios sin mover el contenido | ❌ No existen |

**Conclusión:** con la v1 tal como está, una solicitud a AdSense tiene alta probabilidad de ser rechazada por contenido insuficiente.

## 8. Inventario de URLs de la v1

| URL | Qué es | Destino en la v2 |
|---|---|---|
| `/` | Portada | Se mantiene (`/`) |
| `/cambiario/bancos.html` | Compras por banco | **Se mueve** a `/tipo-de-cambio-bancos/`, con redirección |
| `/google9c83df9ea21fae85.html` | Verificación de Search Console | **Se mantiene igual.** Si desaparece, se pierde la verificación. |
| `/robots.txt`, `/sitemap.xml` | Técnicos | Se regeneran |
| `/data.json`, `/noticias.json` | Datos | Se mantienen en la misma ruta por compatibilidad. La v2 usa archivos más chicos por página. |

## 9. Investigación de palabras clave

**Limitación:** sin herramientas pagas (Ahrefs, Semrush) no hay volúmenes de búsqueda exactos. Esta lectura se basa en los resultados de búsqueda actuales y en los términos que usa la prensa boliviana.

**Contexto clave (2026):** Bolivia abandonó el tipo de cambio fijo de Bs 6,96 en junio de 2026 (RD 88/2026). Desde la RD 142/2026 (24-sep-2026), el BCB calcula el TCO cada día hábil como **mediana ponderada por monto** de las compras de dólares de los bancos y lo publica a las 23:30 ([BDA Abogados](https://www.bda-lawfirm.com/news/asi-se-define-el-precio-del-dolar-en-bolivia-los-nuevos-criterios-del-bcb/); [Los Tiempos, 25-sep-2026](https://www.lostiempos.com/actualidad/economia/20260925/bcb-implementara-nuevo-metodo-calcular-tipo-cambio-oficial)). **El dólar oficial ahora se mueve todos los días.** Eso multiplica las búsquedas diarias de "dólar oficial hoy" y es una oportunidad grande para un sitio de datos.

| Intención de búsqueda | Quién rankea hoy | Qué les falta | Oportunidad |
|---|---|---|---|
| "dólar hoy Bolivia", "dólar paralelo hoy", "cotización dólar Bolivia" | Notas diarias de prensa (eju.tv con una nota por día), herramienta de yo-facturo.com | La prensa: dato estático, una nota nueva cada día, sin gráfico ni histórico. yo-facturo: sin gráficos, sin bancos y depende de una API de terceros | **Alta.** Una página estable que se actualiza sola y con histórico gana a una nota que envejece. |
| "tipo de cambio oficial hoy BCB", "TCO hoy" | Prensa y el propio BCB (PDF y Excel) | Nadie explica el nuevo método de forma simple junto con el dato | **Alta** |
| "tipo de cambio por banco", "a cuánto compra el dólar el Banco X" | Prensa ocasional | **Casi nadie publica el dato banco por banco.** La v1 ya lo tiene | **Muy alta. Es el diferencial del sitio.** |
| "reservas internacionales Bolivia" | Prensa (Correo del Sur, Los Tiempos, Infobae), BCB | Gráfico histórico de fácil lectura | Media |
| "brecha cambiaria Bolivia" | Prensa y análisis | Serie histórica de la brecha | Media |
| "convertir dólares a bolivianos", "100 dólares en bolivianos" | Convertidores genéricos internacionales (Wise y similares) que usan **solo** el tipo oficial | Nadie convierte con oficial, paralelo y banco lado a lado | **Alta** |
| "USDT Bolivia", "Binance P2P Bolivia" | Medios cripto (CriptoNoticias) y prensa | Dato en vivo con explicación | Media |

## 10. Top 10 de problemas y oportunidades (por impacto en tráfico e ingresos)

1. **Sin contenido de texto propio ni páginas legales.** Esto bloquea AdSense y limita el ranking.
2. **Una sola URL para cinco temas distintos.** Hay que dividir en una página por intención de búsqueda.
3. **Las cifras no están en el HTML inicial.** Google y el usuario ven "—" primero.
4. **LCP de 3,6 s en el celular.** Fuentes bloqueantes, archivo de datos de 389 KB y contenido que arranca invisible.
5. **Sin imagen para compartir.** WhatsApp es el canal natural en Bolivia y hoy la vista previa sale pobre.
6. **El dato banco por banco está poco explotado.** Es lo único que la competencia no tiene, y está escondido como "sección 02".
7. **Sin conversor de moneda**, que es una búsqueda de alto volumen.
8. **Fallas silenciosas del pipeline y frecuencia real del paralelo de unas 4 horas, cuando se promete cada 15 minutos.** Si una fuente muere, nadie se entera.
9. **Afirmación inexacta sobre las fuentes.** El TCO viene de una API de terceros y no "directamente del BCB". Para un sitio financiero, la credibilidad es el activo principal.
10. **Sin favicon, sin 404 y sin datos estructurados.** Son detalles menores, pero suman en la percepción de calidad, tanto de Google como de los usuarios.

## 11. Línea base guardada

- Capturas: `revision/v1/*.png` (móvil 390 px y escritorio 1366 px; primera pantalla y página completa).
- Lighthouse: `revision/v1/lighthouse/*.json.gz`.
