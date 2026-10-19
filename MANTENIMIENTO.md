# Rutina de mantenimiento (una página)

## Cada semana (10 minutos)

1. **Abrir el sitio en el celular.** ¿Las cifras tienen la fecha y hora de hoy o de ayer? ¿Hay algún aviso amarillo de "dato atrasado"?
2. **Revisar el correo.** Si GitHub envió un aviso de "Run failed" del flujo *Actualizar datos y publicar*, significa que una fuente se atrasó. El sitio sigue publicado igual, con el aviso visible. Hay que mirar qué fuente es (ver "Si algo falla").
3. **Search Console** (cuando el sitio esté lanzado): revisar *Rendimiento* (clics e impresiones de la semana) y *Páginas* (¿hay páginas nuevas sin indexar o con errores?).
4. **AdSense** (cuando esté activo): revisar los ingresos de la semana y la pestaña *Políticas* por si hay avisos.
5. **Analítica:** usuarios de la semana, páginas más vistas y porcentaje que vuelve.

## Cada mes (30 minutos)

1. **Publicar al menos un artículo** del plan de contenidos (`PLAN_CONTENIDO.md`). Los textos van en `sitio/contenido/articulos/` y se publican solos al guardarlos en GitHub.
2. **Revisar los pull requests de Dependabot** (avisos automáticos de librerías nuevas). Si la marca verde de las pruebas aparece y el cambio es menor (por ejemplo, 4.12 → 4.15), se puede aceptar. Los cambios de versión mayor de las acciones de GitHub conviene probarlos antes en el preview.
3. **Verificar que el dominio se renueva solo** y que la tarjeta de pago del registrador no venció.
4. **Mirar la frecuencia real del paralelo:** en la rama `datos`, `estado.json` muestra el último éxito y los errores de cada fuente.

## Si algo falla

| Síntoma | Qué mirar | Qué hacer |
|---|---|---|
| "Dato atrasado" en el paralelo | `estado.json` → `usdt` → `ultimo_error` | Si Binance cambió su API, hay que ajustar `scripts/update_data.py` (función `_query_binance_p2p`). |
| "Dato atrasado" en el oficial | `estado.json` → `tco` | Si `apibcb.cucu.bo` dejó de funcionar, hay que cambiar la fuente del TCO (ver DECISIONES, D10.4). |
| Bancos, reservas, balanza o ITCR atrasados | `estado.json` y el registro de la corrida | El BCB suele cambiar el formato de sus planillas. Hay que ajustar la lectura en `scripts/update_data.py`. |
| El sitio no se actualiza en absoluto | Pestaña *Actions* del repo | Si dice que los workflows programados se desactivaron por inactividad, hay que entrar al workflow y tocar **Enable workflow**. GitHub los apaga en repos públicos tras 60 días sin actividad. |
| Una página se ve rota | Pestaña *Actions*, última corrida, paso "Generar el sitio" | Normalmente es un error de formato en un texto recién editado (por ejemplo, un `{{` sin cerrar). Revertir el último cambio. |

## Para editar textos sin programar

- **Textos de las páginas:** `sitio/contenido/paginas/*.md` (páginas de datos) y `sitio/contenido/paginas/institucionales/*.md`.
- **Artículos:** `sitio/contenido/articulos/*.md`. Se copia uno existente y se cambia el encabezado (título, descripción, fecha).
- **Datos de contacto, anuncios y analítica:** `config/sitio.json`.
- Se pueden editar desde la web de GitHub: abrir el archivo, ícono del lápiz y "Commit changes". En unos 2 minutos el sitio se publica de nuevo.
