# Runbook de lanzamiento: de la v1 a la v2

> **No ejecutar sin decisión explícita del dueño.** Este documento describe cómo hacer que `elpulsoeconomico.com` pase a mostrar la v2, y cómo volver atrás. Asume la opción recomendada en DECISIONES (D6): seguir en GitHub Pages.

**Duración estimada:** 30–45 minutos de trabajo, más hasta 24 horas de propagación del certificado HTTPS (normalmente es mucho menos).

**Idea central:** el dominio no se "mueve" en el registrador. Se cambia en la configuración de GitHub Pages: se quita del repo v1 y se agrega al repo v2. El DNS sigue apuntando a GitHub, igual que hoy.

---

## 0. Antes del día del lanzamiento

- [ ] Completar en `config/sitio.json`: `responsable` (nombre, descripción y **declaración de intereses**) y `contacto.correo`. Las páginas "Acerca de", "Contacto" y "Privacidad" muestran avisos mientras estos campos estén vacíos.
- [ ] Revisar con un abogado la política de privacidad y los términos (`sitio/contenido/paginas/institucionales/`).
- [ ] Decidir la analítica (DECISIONES D6 y `README.md`) y obtener el ID.
- [ ] Confirmar que la v1 sigue igual que en el commit base `10e17f0`. Si alguien la cambió, revisar qué cambió e incorporarlo a la v2.
- [ ] Anotar la configuración actual de DNS del dominio (captura de pantalla del registrador). Es el respaldo.

## 1. Elegir el momento

Entre **las 01:00 y las 06:00 (hora de Bolivia)** de un día hábil. Es el horario de menor tráfico y queda margen para corregir antes de la mañana. Evitar viernes y vísperas de feriado.

## 2. Respaldo de la v1 (5 minutos)

- [ ] En GitHub, repo `pulso-cambiario`: *Settings → Pages*. Anotar el dominio y si "Enforce HTTPS" está activo.
- [ ] Crear un *tag* en la v1 para marcar el último estado: *Releases → Draft a new release → tag* `v1-final`.

## 3. Pasar la v2 a modo producción (5 minutos)

En el repo `pulso-cambiario-v2`:

- [ ] *Settings → Secrets and variables → Actions → Variables → New repository variable*: nombre `SITIO_ENTORNO`, valor `produccion`.
  - Con esto el sitio se genera **sin** `noindex`, con `robots.txt` de producción y con rutas en la raíz del dominio.
- [ ] Todavía **no** activar los anuncios.

## 4. Mover el dominio (10 minutos)

GitHub no permite que dos repos tengan el mismo dominio. El orden importa:

1. [ ] Repo **v1** → *Settings → Pages → Custom domain*: borrar `elpulsoeconomico.com` → **Save**. Desde ese momento la v1 queda solo en `anubis-tech.github.io/pulso-cambiario`.
2. [ ] Repo **v2** → *Settings → Pages → Custom domain*: escribir `elpulsoeconomico.com` → **Save**. GitHub verifica el DNS (puede tardar unos minutos).
3. [ ] En la v2, marcar **Enforce HTTPS** cuando GitHub lo habilite.
4. [ ] En la v2, *Actions → Actualizar datos y publicar → Run workflow* con "Publicar sin descargar datos nuevos" marcado, para generar el sitio en modo producción.

> **DNS:** si el dominio ya apuntaba a GitHub Pages (registros A a 185.199.108–111.153, o un CNAME a `anubis-tech.github.io`), **no hay que tocar el DNS**. Confirmar la configuración vigente en la [documentación de GitHub Pages sobre dominios personalizados](https://docs.github.com/es/pages/configuring-a-custom-domain-for-your-github-pages-site) antes de cambiar cualquier registro.

## 5. Verificar (10 minutos)

- [ ] `https://elpulsoeconomico.com/` muestra la v2, **sin** la franja amarilla de "Versión de prueba".
- [ ] El código fuente de la portada **no** tiene `noindex`. Buscar "robots" con Ctrl+U: debe decir `index, follow`.
- [ ] `https://elpulsoeconomico.com/robots.txt` incluye la línea `Sitemap:`.
- [ ] `https://elpulsoeconomico.com/cambiario/bancos.html` lleva a `/tipo-de-cambio-bancos/`.
- [ ] `https://elpulsoeconomico.com/google9c83df9ea21fae85.html` responde: es la verificación de Search Console.
- [ ] El candado de HTTPS se ve bien en el celular.
- [ ] Compartir la portada por WhatsApp (a uno mismo) y ver que aparece la imagen con la cotización.

## 6. Avisar a Google (5 minutos)

- [ ] Search Console → *Sitemaps* → enviar `https://elpulsoeconomico.com/sitemap.xml`.
- [ ] *Inspección de URLs* → solicitar indexación de: `/`, `/dolar-paralelo/`, `/tipo-de-cambio-oficial/`, `/tipo-de-cambio-bancos/`, `/conversor/`.
- [ ] Si se eligió Bing: registrar el sitio en Bing Webmaster Tools (permite importar desde Search Console).

## 7. Apagar la v1 (5 minutos, después de verificar)

- [ ] Repo v1 → *Actions*: desactivar los tres workflows (*Disable workflow*). Así deja de consultar las APIs y de publicar.
- [ ] Repo v1 → *Settings → Pages*: elegir **Source: None** para despublicar `anubis-tech.github.io/pulso-cambiario` y evitar contenido duplicado.
- [ ] **No borrar** el repo v1: archivarlo (*Settings → Archive this repository*) recién después de 4 semanas estables.

## 8. AdSense (cuando el sitio lleve unas semanas con tráfico)

- [ ] Solicitar AdSense con el dominio. Cuando Google entregue el ID de editor (`pub-…`), escribirlo en `config/sitio.json` → `adsense.id_editor`. El archivo `ads.txt` se genera solo.
- [ ] Cuando la cuenta esté aprobada: `adsense.activo: true`. Los espacios reservados pasan a mostrar anuncios.
- [ ] Si se recibe tráfico relevante de Europa, configurar el mensaje de consentimiento de Google (CMP certificada) desde AdSense → *Privacidad y mensajes*.

---

## Plan de reversión (menos de 15 minutos)

Si algo sale mal (sitio caído, cifras incorrectas, HTTPS roto):

1. Repo **v2** → *Settings → Pages → Custom domain*: borrar el dominio → Save.
2. Repo **v1** → *Settings → Pages*: si se puso en None, volver a **Source: GitHub Actions** → *Custom domain*: `elpulsoeconomico.com` → Save.
3. Repo **v1** → *Actions*: reactivar los workflows y ejecutar *Publicar sitio al subir cambios* manualmente.
4. Repo **v2** → borrar la variable `SITIO_ENTORNO`, o ponerla en `preview`, para que la v2 vuelva a ser no indexable.

La v1 queda exactamente como estaba, porque nunca se modificó su código.

## Monitoreo después del lanzamiento

**Primeras 72 horas**
- Revisar el sitio en la mañana, al mediodía y en la noche.
- Search Console → *Páginas*: que las URLs nuevas se descubran y no aparezcan errores 404 masivos.
- Que lleguen los datos nuevos: hora del paralelo y fecha del oficial.

**Primeras 4 semanas**
- **Es normal** que el tráfico desde Google baje o se mueva durante 1 a 4 semanas mientras Google reprocesa un sitio con URLs y estructura nuevas. Lo que no es normal es que las búsquedas por la marca ("pulso económico") desaparezcan.
- Comparar semana contra semana: impresiones y clics en Search Console para "dólar hoy bolivia", "dólar paralelo bolivia" y "tipo de cambio por banco".
- Si a las 4 semanas el tráfico total está más de 30% por debajo del de antes del lanzamiento, revisar en Search Console qué páginas perdieron y por qué, antes de cambiar nada más.
