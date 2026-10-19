---
slug: contacto
titulo: "Contacto | Pulso Económico"
descripcion: "Cómo contactar a Pulso Económico para reportar un error en los datos, hacer una consulta, proponer una alianza o anunciar."
h1: "Contacto"
dek: "Para reportar un error, sugerir un dato nuevo o consultar por publicidad."
titulo_corto: "Contacto"
actualizado: 2026-10-18
prioridad: 0.3
faq: []
---
{% if S.contacto.correo %}
Escríbenos a **{{ S.contacto.correo }}**.
{% else %}
*[Pendiente: correo de contacto. Se completa en `config/sitio.json`, sección "contacto".]*
{% endif %}

Para que podamos ayudarte más rápido:

- **Si encontraste un error en un dato:** indica la página, la cifra que ves, la fecha y hora en que la viste y, si la tienes, la fuente que muestra otro valor.
- **Si quieres que agreguemos un dato:** cuéntanos qué serie, para qué la usarías y si conoces una fuente pública confiable.
- **Si eres medio de comunicación o investigador:** puedes usar los datos citando la fuente. Los archivos están en la [metodología]({{ url('/metodologia/') }}#datos-abiertos).
- **Para publicidad o patrocinios:** revisa [Anúnciate]({{ url('/anunciate/') }}){% if S.contacto.correo_publicidad %} o escribe a **{{ S.contacto.correo_publicidad }}**{% endif %}.

Pulso Económico no compra ni vende dólares ni responde consultas sobre operaciones personales de cambio.
