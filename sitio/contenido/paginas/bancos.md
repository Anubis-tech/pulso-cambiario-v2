---
titulo: "Tipo de cambio por banco en Bolivia hoy | Pulso Económico"
og_titulo: "Tipo de cambio por banco en Bolivia"
descripcion: "Cuánto pagó cada banco por el dólar el {{ D.bancos.fecha_larga }}: promedio del sistema Bs {{ D.bancos.ppp_txt }}. Montos, comparación y evolución por banco."
h1: "Tipo de cambio por banco en Bolivia"
dek: "Si vas a vender dólares, aquí ves qué banco pagó más. Dato oficial del BCB, banco por banco."
resumen: "Es el precio promedio al que cada banco compró dólares a sus clientes, según el BCB. Si vas a vender, te conviene el que paga más{% if D.bancos.mejor %}: el {{ D.bancos.dia_txt }} fue {{ D.bancos.mejor.nombre }}, con Bs {{ D.bancos.mejor.tasa_txt }}{% endif %}."
fuente: "Fuente: Banco Central de Bolivia, datos del {{ D.bancos.fecha_larga }}."
faq:
  - p: "¿Qué banco paga más por el dólar hoy?"
    r: "{% if D.bancos.mejor %}En el último dato publicado, del {{ D.bancos.fecha_larga }}, el banco que más pagó en promedio fue **{{ D.bancos.mejor.nombre }}**, con Bs {{ D.bancos.mejor.tasa_txt }} por dólar. El promedio ponderado de todo el sistema fue Bs {{ D.bancos.ppp_txt }}. Para la comparación se excluyen los bancos con muy pocas operaciones.{% else %}Todavía no hay datos suficientes para el último día.{% endif %}"
  - p: "¿Por qué el precio de mi banco es distinto al de esta tabla?"
    r: "La tabla muestra el **promedio** de todas las compras de dólares del banco en el día, ponderado por monto. Lo que te ofrecen a ti depende del monto, del canal (agencia, banca digital), de si eres cliente y del momento del día. Toma la tabla como una referencia para comparar bancos, no como la cotización de una operación puntual."
  - p: "¿Por qué el dato es del día hábil anterior?"
    r: "El BCB publica estas cifras con al menos un día de rezago y no las publica los fines de semana ni los feriados. Las revisamos cada 3 horas."
  - p: "¿Esta tabla muestra el precio de venta de dólares de los bancos?"
    r: "No. Muestra el precio de **compra**: lo que el banco pagó a sus clientes por cada dólar. Sirve si vas a vender dólares. El precio al que los bancos venden dólares no forma parte de esta publicación del BCB."
---
## Qué muestra esta página

El Banco Central de Bolivia publica, para cada banco, el **precio promedio** al que compró dólares a sus clientes cada día y el **monto** que compró. Con eso se puede responder una pregunta concreta: si vendo dólares, ¿qué banco pagó más?

Algunas claves para leer la tabla:

- **Bs por USD:** lo que el banco pagó, en promedio, por cada dólar comprado ese día.
- **Vs. promedio:** la diferencia con el promedio de todo el sistema. En verde, el banco pagó más que el promedio, lo que conviene a quien vende.
- **Monto y participación:** cuántos dólares compró y qué parte del total del sistema representa. Un banco que compró muy poco puede mostrar un precio extremo por una sola operación (lo marcamos con †).
- **Promedio del sistema:** el precio de todos los bancos, ponderado por el monto que compró cada uno.

## Relación con el tipo de cambio oficial

Desde septiembre de 2026, el [tipo de cambio oficial]({{ url('/tipo-de-cambio-oficial/') }}) se calcula con operaciones parecidas: las compras de dólares de los bancos a sus clientes y, además, al BCB, que esta tabla no incluye. Hay otras dos diferencias con el dato de esta página. El oficial usa la **mediana** ponderada por monto, y aquí mostramos el **promedio** ponderado. Además, el oficial toma una ventana que va de las 17:01 de un día a las 17:00 del siguiente. Por eso los dos números se parecen, pero no son idénticos.

## Límites del dato

- Es un **promedio diario**, no una cotización en tiempo real.
- Llega con al menos un día de rezago y no hay datos de fines de semana ni feriados.
- Diciembre de 2025 tiene precios pero no montos, así que no entra en los cálculos ponderados de la herramienta interactiva.
- Los nombres son los comerciales. El BCB usa la razón social de cada entidad.

Fuente: Banco Central de Bolivia, publicación de tipo de cambio y montos de compra por entidad (`bcb_tco_publico_evolutivo`). Cálculos propios. Ver la [metodología]({{ url('/metodologia/') }}).
