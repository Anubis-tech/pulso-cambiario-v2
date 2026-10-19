---
slug: preguntas-frecuentes
titulo: "Preguntas frecuentes sobre el dólar en Bolivia | Pulso Económico"
descripcion: "Respuestas claras a las preguntas más comunes sobre el dólar en Bolivia: oficial, paralelo, bancos, brecha, horarios del BCB y cómo usar los datos de Pulso Económico."
h1: "Preguntas frecuentes"
dek: "Lo que más nos preguntan sobre el dólar en Bolivia y sobre este sitio."
titulo_corto: "Preguntas frecuentes"
actualizado: 2026-10-18
prioridad: 0.5
faq:
  - p: "¿A cuánto está el dólar hoy en Bolivia?"
    r: "A las {{ D.usdt.hora }} del {{ D.usdt.fecha_larga }}: paralelo (USDT/BOB) **Bs {{ D.usdt.valor_txt }}**; oficial del BCB **Bs {{ D.tco.venta_txt }}**; promedio de compra de los bancos **Bs {{ D.bancos.ppp_txt }}** ({{ D.bancos.fecha_corta }}). [Ver todo en la portada]({{ url('/') }})."
  - p: "¿Qué es el tipo de cambio oficial y quién lo fija?"
    r: "Lo calcula y publica el Banco Central de Bolivia. Desde la RD 142/2026 es la mediana ponderada por monto de las compras de dólares de los bancos del día hábil anterior. Se publica a las 23:30 y rige al día siguiente. [Cómo se calcula]({{ url('/tipo-de-cambio-oficial/') }})."
  - p: "¿Qué es el dólar paralelo?"
    r: "Es el precio del dólar fuera del sistema bancario. Lo medimos con el precio del USDT en bolivianos en Binance P2P, la referencia pública más usada. [Más detalles]({{ url('/dolar-paralelo/') }})."
  - p: "¿Por qué el oficial ya no es 6,96?"
    r: "Porque en junio de 2026 Bolivia pasó de un tipo de cambio fijo (6,86 / 6,96, vigente desde noviembre de 2011) a un régimen flexible, en el que el BCB calcula el oficial cada día hábil con operaciones reales de los bancos."
  - p: "¿Qué banco paga más por el dólar?"
    r: "{% if D.bancos.mejor %}Según el último dato del BCB ({{ D.bancos.fecha_larga }}), **{{ D.bancos.mejor.nombre }}**, con Bs {{ D.bancos.mejor.tasa_txt }} en promedio. {% endif %}Cambia de un día a otro: revisa la [tabla por banco]({{ url('/tipo-de-cambio-bancos/') }})."
  - p: "¿Qué es la brecha cambiaria?"
    r: "La diferencia porcentual entre el paralelo y el oficial. Hoy es de {{ D.brecha.pct_txt }}%. Llegó a superar el 160% en mayo de 2025. [Historia de la brecha]({{ url('/brecha-cambiaria/') }})."
  - p: "¿Cada cuánto se actualiza el sitio?"
    r: "El paralelo se intenta medir cada 15 minutos; la hora de la última medición aparece junto a la cifra. El oficial cambia una vez por día hábil. Bancos, reservas, balanza y tipo de cambio real se revisan cada 3 horas y cambian cuando el BCB publica."
  - p: "¿Puedo usar sus datos en mi sitio, trabajo o investigación?"
    r: "Sí, citando a Pulso Económico con un enlace y a la fuente original. Hay archivos JSON en la [metodología]({{ url('/metodologia/') }}) y un [widget]({{ url('/widget/') }}) para sitios web."
  - p: "¿Pulso Económico compra o vende dólares?"
    r: "No. Es un sitio de información. No intermedia divisas ni recomienda operaciones."
  - p: "Encontré un dato que no coincide con otra fuente, ¿qué hago?"
    r: "Escríbenos desde [contacto]({{ url('/contacto/') }}) con la página, la cifra y la fuente que muestra otro valor. Diferencias pequeñas son normales por horarios y métodos distintos; las explicamos en la [metodología]({{ url('/metodologia/') }})."
---
Si tu pregunta no está aquí, escríbenos desde [contacto]({{ url('/contacto/') }}).
