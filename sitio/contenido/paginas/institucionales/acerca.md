---
slug: acerca
titulo: "Acerca de Pulso Económico: quiénes somos y cómo trabajamos"
descripcion: "Qué es Pulso Económico, quién está detrás, de dónde salen los datos y cómo se financia el sitio."
h1: "Acerca de Pulso Económico"
dek: "Datos del mercado cambiario de Bolivia, explicados con claridad y con las fuentes a la vista."
titulo_corto: "Acerca de"
aviso_responsable: true
actualizado: 2026-10-18
prioridad: 0.4
faq: []
---
## Qué es

Pulso Económico es un sitio de información sobre el dólar y el mercado cambiario de Bolivia. Reúne en un solo lugar el tipo de cambio oficial del Banco Central de Bolivia, el precio del dólar paralelo, lo que paga cada banco por el dólar, las reservas internacionales, la balanza cambiaria y el tipo de cambio real. Lo acompaña con textos que explican qué significa cada cifra.

Nació de una necesidad concreta. Desde 2023 el precio del dólar se volvió una pregunta diaria para las familias y las empresas en Bolivia, y la información estaba dispersa entre planillas del BCB, publicaciones en redes y notas de prensa que envejecen en horas.

## Quién está detrás

{% if S.responsable.nombre %}
El sitio lo hace **{{ S.responsable.nombre }}**{% if S.responsable.ciudad %}, desde {{ S.responsable.ciudad }}{% endif %}. {{ S.responsable.descripcion }}
{% if S.responsable.linkedin %}

Perfil profesional: [{{ S.responsable.linkedin }}]({{ S.responsable.linkedin }}).
{% endif %}
{% else %}
*[Pendiente: nombre del responsable, trayectoria y por qué es una fuente confiable en estos temas. Se completa en `config/sitio.json`.]*
{% endif %}

## Independencia y conflictos de interés

{% if S.responsable.declaracion_intereses %}
{{ S.responsable.declaracion_intereses }}
{% else %}
*[Pendiente: declaración de vínculos con entidades financieras. Un sitio que compara bancos debe decir si su responsable trabaja o trabajó en alguno, y comprometerse a no favorecerlo. Se completa en `config/sitio.json`, campo "declaracion_intereses".]*
{% endif %}

Pulso Económico no es una entidad financiera ni una casa de cambio. No compra ni vende divisas, no cobra por mostrar a un banco antes que a otro y no recomienda operaciones. Las tablas se ordenan solo por los datos.

## Cómo se financia

El sitio es gratuito para quien lo lee. Para cubrir sus costos puede mostrar publicidad y espacios patrocinados, siempre identificados como tales y separados de los datos. Ningún anunciante puede cambiar una cifra, el orden de una tabla ni el texto de un artículo. Más información en [Anúnciate]({{ url('/anunciate/') }}).

## Cómo trabajamos

- **Fuentes públicas y citadas.** Cada página dice de dónde sale su dato. La [metodología]({{ url('/metodologia/') }}) explica el cálculo y los límites de cada serie.
- **Errores a la vista.** Si una fuente deja de responder, la cifra muestra un aviso de "dato atrasado". Si encontramos un error, lo corregimos y lo decimos (por ejemplo, la versión anterior rotulaba como "reservas brutas" lo que el BCB publica como reservas internacionales netas).
- **Sin predicciones disfrazadas de datos.** Mostramos lo que pasó y explicamos qué significa, sin pronosticar el precio del dólar.

¿Encontraste un error o tienes una sugerencia? Escríbenos desde [contacto]({{ url('/contacto/') }}).
