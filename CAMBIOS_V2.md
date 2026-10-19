# Cambios de la v2 frente a la v1

**Estado de cada cambio:**
- ✅ **verificado**: medido o probado.
- ⏳ **no verificable aún**: solo se puede comprobar después del lanzamiento.
- 💡 **propuesto**: preparado, pero falta una acción del dueño.

**¿Se ve?** indica si el lector lo nota a simple vista. **¿A la v1?** indica si podría llevarse a la v1 por separado, sin migrar todo.

## Contenido y experiencia

| # | Cambio | Por qué mejora | Evidencia | ¿Se ve? | ¿A la v1? | Estado |
|---|---|---|---|---|---|---|
| C1 | Portada con una cifra protagonista, variación contra ayer y titular del día por reglas fijas | Contesta "¿a cuánto está y se movió?" en 3 segundos. El titular cambia según el movimiento y deja de sonar robótico | `inicio.html`, función `enriquecer()` en `scripts/construir.py`; capturas en `revision/v2/` | Sí | Parcial | ✅ |
| C2 | Conversor de una línea en la primera pantalla y página de conversor completa | Es la tarea más común en el celular | `/conversor/`, `vivo.js`, `conversor.js` | Sí | Sí | ✅ |
| C3 | "¿Dónde vender tus dólares?": los 3 bancos que más pagaron, con monto editable | Convierte el dato diferencial (precio por banco) en plata concreta | Portada; los bancos con poco volumen quedan excluidos | Sí | Sí | ✅ |
| C4 | Imagen del día para WhatsApp (1080×1350) y estados (1080×1920), con botón para mandarla | WhatsApp es el canal principal en Bolivia, y cada imagen reenviada lleva la marca | `/img/hoy-cuadrado.png`, `/img/hoy-estado.png` | Sí | Sí | ✅ |
| C5 | "Ya salió el oficial de mañana" (después de las 23:30) | Da un dato que la prensa recién publica al día siguiente | Bloque condicional en la portada | Sí (de noche) | Sí | ⏳ (falta verlo en una noche real) |
| C6 | "Desde tu última visita…", "Hace un año" y montos recordados | Premia volver a la página | `vivo.js` (se guarda solo en el navegador del lector) | Sí | Sí | ✅ |
| C7 | Una página por tema (9 páginas de datos) | Cada página puede posicionarse para su propia búsqueda | `sitemap.xml`: 57 URLs (la v1 tenía 2) | Sí | No | ✅ |
| C8 | Resúmenes mes a mes desde junio de 2024 (29 páginas) | Fecha fija de regreso y búsquedas como "dólar octubre 2026 Bolivia" | `/dolar-bolivia/` | Sí | No | ✅ |
| C9 | Páginas de 100, 500 y 1.000 dólares en bolivianos | Búsquedas de alto volumen, con el dato propio por banco | `/100-dolares-en-bolivianos/` y siguientes | Sí | No | ✅ |
| C10 | 5 artículos explicativos con fuentes | Contenido original, necesario para AdSense y para el ranking | `/articulos/` | Sí | Sí | ✅ (pendiente de la revisión del verificador independiente) |
| C11 | Páginas de confianza: acerca de, metodología, privacidad, términos, contacto, anúnciate y preguntas frecuentes | Requisitos de AdSense y señales de confianza (E-E-A-T) en temas de dinero | `/acerca/`, `/metodologia/`, etc. | Sí | Sí | 💡 (faltan datos del responsable y revisión legal) |
| C12 | Noticias de los últimos 7 días, con su antigüedad visible | La v1 mostraba titulares de hace meses como "de hoy" | `update_news.py` (`when:7d`, `MAX_EDAD_DIAS`) y `construir.py` | Sí | Sí | ✅ (código); ⏳ (la primera tanda real llega con la próxima actualización) |
| C13 | Herramienta por banco desde el punto de vista de quien vende | El público son personas, no bancos | `bancos.js` (ver DECISIONES, D9) | Sí | Sí | ✅ |
| C14 | Widget embebible con enlace de atribución | Genera enlaces entrantes y presencia en otros sitios | `/widget/`, `/embed/cotizacion/` | Sí | Sí | ✅ |
| C15 | Telegram automático: mañana, oficial nocturno y movimientos fuertes | Canal de recurrencia que no depende de que el lector se acuerde | `scripts/publicar_telegram.py` | No | Sí | 💡 (falta crear el bot y el canal) |
| C16 | Suscripción por correo (formulario) | Recurrencia | Macro `suscripcion()`; se configura en `config/sitio.json` | Sí | Sí | 💡 (falta elegir el servicio) |

## Correcciones de datos y de credibilidad

| # | Cambio | Evidencia | ¿Se ve? | Estado |
|---|---|---|---|---|
| K1 | "Reservas brutas" → reservas internacionales **netas** | Nombre de la planilla del BCB en `update_data.py` (`XLSX_SOURCES["reservas"]`) | Sí | ✅ |
| K2 | El tramo dic-2025 a jun-2026 de la serie "oficial" se identifica como **valor referencial** del BCB | Los Tiempos (1-dic-2025); valores 7,85 / 9,32 del 1-dic-2025 en `data.json` | Sí (sombreado) | ✅ |
| K3 | Se deja de prometer "en vivo cada 15 minutos"; se muestra la hora real de la última medición | 170 mediciones en 30 días, mediana de unas 4 h (AUDITORIA §2) | Sí | ✅ |
| K4 | Se declara que el TCO viene de un servicio de terceros (`apibcb.cucu.bo`), no directamente del BCB | `/metodologia/` | Sí | ✅ |
| K5 | Se quitan del `data.json` público las series de pronóstico (`forecast`, `garch`), que nadie actualiza | `construir.py` | No | ✅ |
| K6 | Titulares de prensa escapados en el servidor (la v1 los insertaba con `innerHTML`) | Plantilla Jinja con escape automático | No | ✅ |

## Rendimiento, SEO técnico y accesibilidad

Medido con Lighthouse 13.5 en un servidor local, en modo producción y con conexión móvil simulada. Mismo método para la v1 y la v2. Reportes en `revision/v1/lighthouse/` y `revision/v2/lighthouse/`.

| Métrica (móvil) | v1 inicio | v2 inicio | v1 bancos | v2 bancos |
|---|---|---|---|---|
| Rendimiento | 87 | 99 | 87 | 95 |
| LCP | 3,6 s | 2,1 s | 3,6 s | 1,8 s |
| Accesibilidad | 92 | 100 | 89 | 100 |
| Buenas prácticas | 96 | 100 | 96 | 100 |
| SEO (Lighthouse) | 100 | 100 | 100 | 100 |

| # | Cambio | ¿Se ve? | Estado |
|---|---|---|---|
| T1 | Cifras escritas en el HTML (antes las escribía JavaScript tras descargar 389 KB) | No | ✅ |
| T2 | Fuentes servidas desde el sitio (sin Google Fonts) | No | ✅ |
| T3 | Contenido visible desde el inicio (la v1 lo ocultaba con `opacity:0` hasta el scroll) | Algo | ✅ |
| T4 | Chart.js servido desde el sitio y cargado solo al llegar a la herramienta por banco | No | ✅ |
| T5 | Datos estructurados: WebSite, Organization, Dataset, BreadcrumbList, FAQPage, Article, WebApplication | No | ✅ (JSON válido en las 61 páginas) |
| T6 | Títulos y descripciones únicos y dentro del largo que muestra Google | En Google | ✅ (QA: 0 observaciones) |
| T7 | Sitemap con `lastmod` real, robots.txt de producción, 404 útil y favicon | No | ✅ |
| T8 | Redirección de `/cambiario/bancos.html` | No | ✅ (meta refresh + canonical en GitHub Pages; 301 listo para Cloudflare) |
| T9 | Imagen de vista previa (Open Graph) por página, con la cifra del día | Al compartir | ✅ |
| T10 | Espacios publicitarios con alto reservado (CLS ≈ 0) | Sí (marcadores en el preview) | ✅ |
| T11 | Posición en Google | — | ⏳ |
| T12 | Aprobación de AdSense | — | ⏳ |

## Seguridad y operación

| # | Cambio | Estado |
|---|---|---|
| S1 | Content Security Policy estricta sin anuncios (0 violaciones en 60 páginas) y mínima con AdSense (DECISIONES D7) | ✅ |
| S2 | Ningún script de terceros sin anuncios ni analítica | ✅ |
| S3 | Permisos mínimos por trabajo en GitHub Actions | ✅ |
| S4 | Dependabot para librerías de Python y acciones (ya abrió sus primeros avisos) | ✅ |
| S5 | Alertas de datos atrasados (una por problema y por día) | ✅ (probado con fechas simuladas) |
| S6 | Datos en la rama `datos`; `main` solo con código | ✅ |
| S7 | Cabeceras HSTS, X-Frame-Options, etc. | 💡 (solo con Cloudflare Pages; `_headers` ya generado) |
| S8 | Revisión del historial de la v1 en busca de secretos | ✅ (limpio) |
