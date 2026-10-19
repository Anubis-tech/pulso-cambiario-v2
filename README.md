# Pulso Económico, versión 2.0 (candidata)

Sitio de datos del dólar en Bolivia: el tipo de cambio oficial del BCB, el dólar paralelo (USDT/BOB), el precio por banco, las reservas, la balanza cambiaria y el tipo de cambio real.

- **Preview (no indexable):** https://anubis-tech.github.io/pulso-cambiario-v2/
- **Sitio oficial actual (v1):** https://elpulsoeconomico.com/, repo `Anubis-tech/pulso-cambiario`. Esta versión no lo toca.

## Documentos

| Documento | Para qué |
|---|---|
| [AUDITORIA.md](AUDITORIA.md) | Cómo estaba la v1, con mediciones |
| [CAMBIOS_V2.md](CAMBIOS_V2.md) | Cada cambio, su evidencia y su estado |
| [DECISIONES.md](DECISIONES.md) | Qué se eligió, qué se descartó y por qué. Incluye las decisiones abiertas para el dueño |
| [REVISION_V1_VS_V2.md](REVISION_V1_VS_V2.md) | Comparación para el dueño, con guía de revisión |
| [EVALUACION_EXTERNA.md](EVALUACION_EXTERNA.md) | Paquete para la IA que evaluará el trabajo |
| [PLAN_CONTENIDO.md](PLAN_CONTENIDO.md) | Qué escribir y en qué orden |
| [QA.md](QA.md) | Resultados de las pruebas |
| [RUNBOOK_LANZAMIENTO.md](RUNBOOK_LANZAMIENTO.md) | Cómo pasar a producción y cómo volver atrás |
| [MANTENIMIENTO.md](MANTENIMIENTO.md) | Rutina semanal y mensual |
| [PROGRESO.md](PROGRESO.md) | Bitácora del trabajo |

## Cómo funciona

```
Cada 15 min (GitHub Actions)
  ├─ scripts/actualizar.py         descarga datos (paralelo y TCO siempre; BCB y noticias cada 3 h)
  ├─ scripts/verificar_frescura.py marca datos atrasados y avisa por correo
  ├─ scripts/construir.py          genera el sitio con las cifras ya escritas en el HTML
  ├─ scripts/publicar_telegram.py  (opcional) publica en un canal de Telegram
  ├─ guarda los datos en la rama "datos"
  └─ publica en GitHub Pages
```

- `main`: código, plantillas (`sitio/plantillas/`), textos (`sitio/contenido/`), estilos y scripts (`sitio/estaticos/`) y configuración (`config/sitio.json`).
- `datos`: `data.json`, `noticias.json` y `estado.json` (salud de cada fuente). Es el respaldo histórico de los datos.

## Configuración (`config/sitio.json`)

| Campo | Qué es | Qué poner |
|---|---|---|
| `responsable.nombre`, `descripcion`, `declaracion_intereses` | Página "Acerca de" | Datos reales. **La declaración de intereses es importante** (DECISIONES D14) |
| `contacto.correo`, `correo_publicidad` | Contacto | Correos reales |
| `adsense.id_editor` | ID de AdSense (`pub-…`) | Genera `ads.txt` automáticamente |
| `adsense.activo` | Mostrar anuncios | `true` solo cuando AdSense apruebe el sitio |
| `analitica.proveedor` / `id` | Medición | `ga4` + `G-XXXX`, `cloudflare` + token o `plausible` + dominio |
| `suscripcion.formulario_accion`, `telegram`, `whatsapp` | Canales de recurrencia | URL del formulario y enlaces a los canales |
| `busqueda.bing` | Verificación de Bing Webmaster Tools | Código `msvalidate.01` |

**Variables y secretos de GitHub** (*Settings → Secrets and variables → Actions*):
- Variable `SITIO_ENTORNO`: `produccion` el día del lanzamiento. Si no existe, el sitio se genera como preview.
- Secretos `TELEGRAM_TOKEN` y `TELEGRAM_CANAL`: activan Telegram, solo en producción.

## Probar en una computadora

```bash
pip install -r requirements.txt
git worktree add datos datos                 # trae la rama de datos a ./datos
python scripts/construir.py --datos datos --salida _site --base ""
python -m http.server 8000 --directory _site # abrir http://localhost:8000
```

Pruebas de calidad (Lighthouse y Playwright deben estar instalados):

```bash
python herramientas/qa/qa.py _site                            # enlaces, JSON-LD, títulos y descripciones
python herramientas/qa/consola.py _site http://localhost:8000 # errores de JavaScript, CSP y estado HTTP
```

## Licencias de terceros

- Tipografías Archivo e IBM Plex: SIL Open Font License (`sitio/estaticos/fuentes/LICENCIA-*.txt`).
- Chart.js 4.4.1: MIT.
- Datos: Banco Central de Bolivia y Binance P2P. Se citan en cada página.
