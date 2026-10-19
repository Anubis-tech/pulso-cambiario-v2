---
titulo: "Tipo de cambio oficial hoy en Bolivia: Bs {{ D.tco.venta_txt }} (BCB) | Pulso Económico"
og_titulo: "Tipo de cambio oficial del BCB hoy"
descripcion: "Tipo de cambio oficial del BCB vigente el {{ D.tco.fecha_larga }}: Bs {{ D.tco.venta_txt }}. Cómo se calcula desde la RD 142/2026 e histórico."
h1: "Tipo de cambio oficial del BCB hoy"
dek: "El oficial del BCB está en Bs {{ D.tco.venta_txt }}. Cambia cada día hábil y el nuevo valor sale a las 23:30."
faq:
  - p: "¿Cuál es el tipo de cambio oficial hoy?"
    r: "El tipo de cambio oficial vigente para el {{ D.tco.fecha_larga }} es **Bs {{ D.tco.venta_txt }}** por dólar{% if not D.tco.iguales %} para la venta y Bs {{ D.tco.compra_txt }} para la compra{% endif %}."
  - p: "¿A qué hora publica el BCB el tipo de cambio oficial?"
    r: "Desde la RD 142/2026, el BCB lo publica cada día hábil a las 23:30 y rige para el día hábil siguiente. El valor publicado el viernes rige sábado, domingo y lunes. En feriados se mantiene el del último día hábil."
  - p: "¿Sigue existiendo el 6,96?"
    r: "No como tipo de cambio oficial. El valor fijo de Bs 6,96 para la venta rigió desde noviembre de 2011 hasta junio de 2026, cuando el BCB adoptó un régimen de tipo de cambio flexible."
  - p: "¿Por qué el oficial es distinto del precio que me dan en el banco?"
    r: "El oficial es una mediana de muchas operaciones del día hábil anterior. Cada banco fija sus propios precios de compra y venta para sus clientes. Desde septiembre de 2026 ya no existe el tope que limitaba el precio de venta de los bancos a 10 centavos por encima del oficial. Puedes ver lo que pagó cada banco en [tipo de cambio por banco]({{ url('/tipo-de-cambio-bancos/') }})."
---
## Cómo se calcula hoy

Desde la **Resolución de Directorio N° 142/2026** del BCB, del 24 de septiembre de 2026, el tipo de cambio oficial (TCO) se calcula así:

1. **Qué operaciones entran:** las compras de dólares con bolivianos que hacen los bancos múltiples, los bancos PyME y el banco público, tanto a sus clientes como al propio BCB. Las operaciones entre bancos y los precios de venta de los bancos a sus clientes quedan fuera.
2. **Ventana de tiempo:** desde las 17:01 del día hábil anterior hasta las 17:00 del día del cálculo.
3. **Estadístico:** la **mediana ponderada por monto**. Si se ordenan todas las compras por precio, es el precio en el que se acumula la mitad del monto total. A diferencia de un promedio, una sola operación grande a un precio raro no lo mueve mucho.
4. **Reporte y publicación:** los bancos informan a la ASFI hasta las 17:30, la ASFI envía los datos al BCB hasta las 17:40 y el BCB publica el TCO a las 23:30.
5. **Vigencia:** rige para el día hábil siguiente. El del viernes vale sábado, domingo y lunes.

El TCO se usa para las operaciones del sector público y del BCB y para los registros contables. Para las operaciones de cambio entre privados es una referencia.

## Cómo llegamos aquí

- **Noviembre de 2011 a junio de 2026:** tipo de cambio fijo, Bs 6,86 la compra y Bs 6,96 la venta.
- **Desde el 1 de diciembre de 2025:** el oficial sigue en 6,96, pero el BCB empieza a publicar un **valor referencial** del dólar, calculado con operaciones reales de los bancos con sus clientes. En el gráfico, ese tramo aparece sombreado, porque la línea muestra el referencial y no el oficial legal.
- **26 de junio de 2026, RD 88/2026:** régimen de tipo de cambio flexible. El BCB calcula un oficial diario y los bancos no pueden vender a más de 10 centavos por encima de él.
- **24 de septiembre de 2026, RD 142/2026:** el cálculo pasa del promedio ponderado a la mediana ponderada por monto, se suman las compras al BCB, la publicación se mueve a las 23:30 y se elimina el tope de 10 centavos. Desde entonces el BCB publica un único valor para compra y venta.

Más detalle en [cómo calcula el BCB el tipo de cambio oficial]({{ url('/articulos/como-calcula-el-bcb-el-tipo-de-cambio-oficial/') }}).

## Fuentes

- Banco Central de Bolivia, [tipos de cambio](https://www.bcb.gob.bo/).
- Resolución de Directorio 142/2026, resumida por [BDA Abogados](https://www.bda-lawfirm.com/news/asi-se-define-el-precio-del-dolar-en-bolivia-los-nuevos-criterios-del-bcb/) y [Los Tiempos (25-sep-2026)](https://www.lostiempos.com/actualidad/economia/20260925/bcb-implementara-nuevo-metodo-calcular-tipo-cambio-oficial).
- Valor referencial desde diciembre de 2025: [Los Tiempos (1-dic-2025)](https://www.lostiempos.com/actualidad/economia/20251201/bcb-publica-hoy-valor-referencial-del-dolar-bolivianos).
- Datos de esta página: el TCO se obtiene de un servicio independiente que replica la publicación del BCB (apibcb.cucu.bo), no directamente del sitio del BCB. Un control automático descarta cualquier valor que salte más de 15% respecto del anterior. Ver la [metodología]({{ url('/metodologia/') }}).
