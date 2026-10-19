# Bitácora del trabajo

## 18-oct-2026

**Fase 0 — Auditoría (hecha).** Copia de la v1 a un repo nuevo. Mediciones con Lighthouse y capturas de pantalla. Revisión del historial (limpio, sin secretos). Hallazgos principales:
- El paralelo se mide cada ~4 h, no cada 15 min como se promete.
- "Reservas brutas" es un rótulo erróneo: el dato son reservas netas.
- Entre dic-2025 y jun-2026 la serie "oficial" es en realidad el valor referencial.
- Las noticias eran viejas.
- No hay páginas legales ni contenido propio, que AdSense exige.

**Fases 1 y 2 — Base (hecha).** Datos en la rama `datos`, generador en Python, un solo workflow, alertas de datos atrasados, preview publicado con `noindex`.

**Fase 3 — Páginas y diseño (hecha).** 9 páginas de datos, conversor, herramienta por banco, widget, 404 y redirección de la URL vieja.

**Fases 4 y 5 — Seguridad y SEO técnico (hecha).** CSP, fuentes y Chart.js propios, JSON-LD, sitemap, imágenes de vista previa y títulos ajustados. Lighthouse móvil en el inicio: 87 → 99.

**Fase 6 — Contenido (hecha, en revisión).** Páginas institucionales y 5 artículos con fuentes.

**Revisión de marketing independiente (aplicada).** El dueño pidió priorizar atractivo y tráfico recurrente. Cambios:
- Portada con una cifra protagonista y titular del día.
- "¿Dónde vender tus dólares?".
- Imagen para WhatsApp.
- Oficial de mañana, última visita y hace un año.
- Resúmenes mensuales y páginas de montos.
- Telegram opcional.
- Tono menos técnico.

**Noticias (corregido).** Solo notas de los últimos 7 días, con su antigüedad visible.

**En curso:**
- Verificación de datos independiente y estrategia de SEO independiente.
- Después: QA independiente final.

**Pendiente del dueño:** ver la sección "Decisiones abiertas" de `REVISION_V1_VS_V2.md`.
