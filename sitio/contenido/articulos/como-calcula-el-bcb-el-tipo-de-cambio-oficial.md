---
h1: "Cómo calcula el BCB el tipo de cambio oficial desde 2026"
titulo_corto: "Cómo se calcula el tipo de cambio oficial"
titulo: "Cómo calcula el BCB el tipo de cambio oficial (RD 142/2026), explicado | Pulso Económico"
descripcion: "Del 6,96 fijo al régimen flexible: qué operaciones usa el Banco Central de Bolivia para calcular el tipo de cambio oficial, qué es la mediana ponderada, a qué hora se publica y qué cambió con la RD 142/2026."
resumen: "Qué operaciones entran, qué es la mediana ponderada por monto y por qué el oficial ahora cambia todos los días."
fecha: 2026-10-18
actualizado: 2026-10-18
tipo_og: article
relacionado_con: [oficial, inicio]
---
Durante más de 14 años, la respuesta a "¿a cuánto está el dólar oficial?" fue la misma: Bs 6,96 para la venta y Bs 6,86 para la compra. Ese número quedó fijo en noviembre de 2011 y se mantuvo hasta junio de 2026. Hoy el tipo de cambio oficial (TCO) cambia cada día hábil. Esta guía explica cómo se calcula, de dónde salen los datos y qué significa para quien compra o vende dólares.

## La regla actual en una frase

Desde la **Resolución de Directorio N° 142/2026** del Banco Central de Bolivia (BCB), del 24 de septiembre de 2026, el TCO es la **mediana ponderada por monto** de las compras de dólares que hicieron los bancos en el día hábil.

## Paso a paso

**1. Qué operaciones cuentan.** Entran las compras de dólares con bolivianos que hacen los **bancos múltiples, los bancos PyME y el banco público**, tanto a sus clientes como al propio BCB. Quedan fuera las operaciones entre bancos y los precios a los que los bancos **venden** dólares a sus clientes.

**2. Ventana de tiempo.** Se consideran las operaciones desde las **17:01 del día hábil anterior hasta las 17:00** del día del cálculo.

**3. Reporte.** Los bancos informan sus operaciones a la ASFI (la Autoridad de Supervisión del Sistema Financiero) hasta las 17:30. La ASFI procesa la información y la envía al BCB hasta las 17:40.

**4. Cálculo y publicación.** El BCB calcula el TCO y lo publica a las **23:30**. Antes de esta resolución, la publicación era a las 20:00.

**5. Vigencia.** El valor rige para el **día hábil siguiente**. El que se publica el viernes rige sábado, domingo y lunes. En los feriados se mantiene el del último día hábil.

## ¿Qué es una "mediana ponderada por monto"?

Supongamos que en un día los bancos hicieron tres compras de dólares:

| Operación | Precio (Bs por USD) | Monto (USD) |
|---|---|---|
| A | 11,60 | 100.000 |
| B | 11,70 | 300.000 |
| C | 11,95 | 50.000 |

- El **promedio simple** de los precios sería (11,60 + 11,70 + 11,95) ÷ 3 = 11,75. Trata igual una operación de 50.000 dólares que una de 300.000.
- El **promedio ponderado por monto** pesa cada precio por su monto: (11,60×100.000 + 11,70×300.000 + 11,95×50.000) ÷ 450.000 ≈ 11,71.
- La **mediana ponderada por monto** ordena las operaciones por precio y busca el precio en el que se acumula la mitad del monto total. El total es 450.000, así que la mitad es 225.000. La operación A suma 100.000, y al llegar a la B ya se superan los 225.000. La mediana ponderada es **11,70**.

¿Por qué usar la mediana? Porque resiste mejor los valores extremos. Una operación grande a un precio raro mueve mucho un promedio, pero casi no mueve la mediana. Con la RD 142/2026, el BCB pasó del promedio ponderado a la mediana ponderada.

## Qué cambió en 2026

- **1 de diciembre de 2025.** El oficial sigue en 6,86 / 6,96, pero el BCB empieza a publicar cada día un **valor referencial** del dólar, calculado con las operaciones de los bancos con sus clientes. El primer día ese referencial fue de Bs 7,85 para la compra y Bs 9,32 para la venta.
- **26 de junio de 2026, RD 88/2026.** Bolivia adopta un **régimen de tipo de cambio flexible**. El BCB calcula el oficial cada día y los bancos no pueden vender dólares a más de **10 centavos** por encima de ese valor.
- **24 de septiembre de 2026, RD 142/2026.** Se reemplaza el reglamento de junio. Se cambia el promedio ponderado por la mediana ponderada, se suman las compras al BCB, se amplía la ventana de tiempo, la publicación pasa a las 23:30 y **se elimina el tope de 10 centavos** para la venta de los bancos. Desde entonces el BCB publica un único valor, igual para compra y venta.

## Para qué sirve el oficial (y para qué no)

El TCO es obligatorio para las **operaciones del sector público y del BCB** y para los **registros contables**. Para las operaciones de cambio entre privados (lo que te paga tu banco o un cambista) es una **referencia**. Cada banco fija sus precios de compra y venta, y desde septiembre de 2026 ya no hay un tope legal para su precio de venta.

En la práctica:

- Si vas a **vender** dólares en un banco, mira lo que pagó cada banco en [tipo de cambio por banco]({{ url('/tipo-de-cambio-bancos/') }}). Ese dato sale de las mismas operaciones que usa el BCB para el oficial.
- Si vas a **comprar** dólares en un banco, pregunta su precio de venta. Puede estar por encima del oficial.
- Para **impuestos, facturas en dólares o contratos con el Estado**, se usa el oficial vigente ese día. Consulta siempre con tu contador la norma que aplica a tu caso.

## Dónde verlo

En [tipo de cambio oficial]({{ url('/tipo-de-cambio-oficial/') }}) mostramos el valor vigente, el histórico desde 2024 y la comparación con el paralelo. Hoy, {{ D.tco.fecha_larga }}, el oficial es **Bs {{ D.tco.venta_txt }}**.

<div class="fuentes" markdown="1">

**Fuentes**

- Banco Central de Bolivia, Resolución de Directorio N° 142/2026 (24-sep-2026), resumida por [BDA Abogados](https://www.bda-lawfirm.com/news/asi-se-define-el-precio-del-dolar-en-bolivia-los-nuevos-criterios-del-bcb/) y [Los Tiempos](https://www.lostiempos.com/actualidad/economia/20260925/bcb-implementara-nuevo-metodo-calcular-tipo-cambio-oficial).
- Eliminación del tope de 10 centavos: [Oxígeno](https://oxigeno.bo/nueva-resolucion-del-bcb-no-contempla-el-limite-de-10-centavos-para-la-venta-de-dolares-por-parte-de-los-bancos/).
- Paso al régimen flexible (RD 88/2026): [Panamericana](https://www.panamericana.bo/articulo/economia/fin-tipo-cambio-fijo-gobierno-flexibiliza-cotizacion-dolar-bcb-calculara-diariamente-mercado-financiero/20260626220035016353.html).
- Valor referencial desde el 1-dic-2025: [Los Tiempos](https://www.lostiempos.com/actualidad/economia/20251201/bcb-publica-hoy-valor-referencial-del-dolar-bolivianos).

</div>
