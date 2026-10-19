---
h1: "Brecha cambiaria: qué es, cómo se calcula y qué pasó en Bolivia"
titulo_corto: "Brecha cambiaria: qué es y cómo se calcula"
titulo: "Brecha cambiaria: qué es y cómo se calcula | Pulso Económico"
descripcion: "Qué es la brecha cambiaria, la fórmula para calcularla con un ejemplo, qué indica una brecha alta y cómo pasó en Bolivia de más de 160% en 2025 a casi cero en 2026."
resumen: "La fórmula, un ejemplo con números y la historia de una brecha que pasó de 160% a casi cero."
fecha: 2026-10-18
actualizado: 2026-10-18
tipo_og: article
relacionado_con: [brecha, paralelo, inicio]
---
La brecha cambiaria es uno de esos indicadores que se mencionan todo el tiempo y pocas veces se explican. En pocas palabras, dice **cuánto más caro está el dólar en el mercado paralelo que en el oficial**. En Bolivia, esa diferencia contó buena parte de la historia económica de 2024 a 2026.

## La fórmula

> Brecha (%) = (dólar paralelo − dólar oficial) ÷ dólar oficial × 100

Un detalle: el paralelo que usamos es lo que pagan en Binance P2P a quien vende USDT (el lado comprador). Hasta junio de 2026 lo comparamos con el oficial de venta (6,96 y luego la venta del valor referencial). Desde el 29 de junio de 2026 el BCB calcula un único valor, y ese es el que usamos. Comparar un precio de compra con uno de venta achica un poco la brecha; con un oficial único, ese efecto desaparece.

**Ejemplo.** Si el paralelo está a Bs 12,00 y el oficial a Bs 10,00:

- Diferencia: 12,00 − 10,00 = 2,00 Bs
- Brecha: 2,00 ÷ 10,00 × 100 = **20%**

Es decir, en el paralelo el dólar cuesta un 20% más que al precio oficial.

La brecha también puede ser **negativa**: si el paralelo está más barato que el oficial. Pasa cuando hay más dólares ofrecidos fuera del sistema que demanda, o cuando el oficial se ajusta con algo de retraso.

## Qué indica una brecha alta

Una brecha grande suele indicar que **al precio oficial no hay dólares para todos**. Quienes los necesitan los buscan en otro lado y pagan más. Una brecha alta y persistente suele traer problemas:

- Los precios de lo importado se ajustan al paralelo, no al oficial.
- Aparecen incentivos para el arbitraje: comprar barato en el oficial (si se consigue) y vender caro en el paralelo.
- Las estadísticas oficiales se alejan de los precios reales.

Una brecha cercana a cero indica que los dos mercados están alineados: el precio oficial refleja lo que la gente efectivamente paga.

## Qué pasó en Bolivia

Los datos de Pulso Económico empiezan en junio de 2024. Este es el recorrido, medido como paralelo (USDT/BOB) frente al oficial que usamos en cada etapa:

| Fecha | Paralelo (Bs) | Oficial / referencial (Bs) | Brecha |
|---|---|---|---|
| 14-jun-2024 | 8,88 | 6,96 | 28% |
| 31-dic-2024 | 11,10 | 6,96 | 59% |
| 15-may-2025 | 18,27 | 6,96 | **162%** (máximo) |
| 30-sep-2025 | 12,56 | 6,96 | 80% |
| 15-dic-2025 | 9,20 | 8,77 (referencial) | 5% |
| 15-jul-2026 | 10,74 | 10,75 | −0,1% |
| {{ D.usdt.fecha_corta }} | {{ D.usdt.valor_txt }} | {{ D.tco.venta_txt }} | {{ D.brecha.pct_txt }}% |

Tres etapas:

1. **Brecha creciente (2024 – mayo de 2025).** Con el oficial fijo en 6,96, cada subida del paralelo agrandaba la brecha. En mayo de 2025 el paralelo superó los Bs 18 y la brecha pasó el 160%.
2. **Precio de referencia (diciembre de 2025 – junio de 2026).** El BCB empezó a publicar un **valor referencial** mientras el oficial legal seguía en 6,96. Su compra era el promedio de las compras de los bancos a sus clientes y su venta, el precio máximo que podían cobrar. Comparado con esa venta, el paralelo quedó a menos de 10 puntos en promedio (8,8% en diciembre de 2025, con picos de hasta 23%).
3. **Régimen flexible (desde fines de junio de 2026).** El oficial pasó a calcularse cada día con las compras de los bancos, y la brecha oscila alrededor de cero.

## Un detalle importante sobre la etapa 2

Entre diciembre de 2025 y junio de 2026 hay dos "oficiales" posibles: el **legal** (Bs 6,96, que seguía vigente) y el **referencial** que publicaba el BCB. Si se calcula la brecha contra 6,96, sigue siendo enorme. Si se calcula contra el referencial, es pequeña. En Pulso Económico usamos la venta del referencial, que era el precio con el que operaban los bancos aunque fuera un precio máximo, y marcamos ese tramo con sombreado en los gráficos. Conviene tenerlo en cuenta al comparar con otras fuentes.

## Dónde seguirla

La [página de brecha cambiaria]({{ url('/brecha-cambiaria/') }}) muestra el valor de hoy, el gráfico completo y el promedio de cada mes. Los datos se pueden descargar en formato JSON desde la [metodología]({{ url('/metodologia/') }}).

<div class="fuentes" markdown="1">

**Fuentes**

- Datos propios: paralelo (USDT/BOB, Binance P2P) y tipo de cambio oficial y referencial del BCB. Cifras de la tabla redondeadas.
- Valor referencial del BCB desde el 1-dic-2025: [Los Tiempos](https://www.lostiempos.com/actualidad/economia/20251201/bcb-publica-hoy-valor-referencial-del-dolar-bolivianos).

</div>
