---
h1: "Reservas internacionales del BCB: qué son, de qué están hechas y por qué importan"
titulo_corto: "Reservas internacionales: qué son"
titulo: "Reservas internacionales de Bolivia: qué son y por qué importan | Pulso Económico"
descripcion: "Qué son las reservas internacionales netas del Banco Central de Bolivia, sus componentes (oro, divisas, DEG), cómo evolucionaron desde 2016 y por qué hoy dependen tanto del precio del oro."
resumen: "Oro, divisas y DEG: qué hay en las reservas del BCB y por qué hoy dependen tanto del precio del oro."
fecha: 2026-10-18
actualizado: 2026-10-18
tipo_og: article
relacionado_con: [reservas, balanza]
---
Las reservas internacionales aparecen en cada conversación sobre el dólar en Bolivia, y con razón: son el "colchón" de moneda extranjera del país. Esta guía explica qué son, de qué están hechas, qué pasó con ellas en la última década y cómo leer la cifra que publica el Banco Central.

## Qué son

Las reservas internacionales son los **activos externos que administra el Banco Central de Bolivia (BCB)** y que puede usar para:

- pagar importaciones y deuda externa;
- abastecer de dólares a la economía;
- respaldar la moneda y dar confianza en momentos de tensión.

El BCB publica la cifra como **reservas internacionales netas (RIN)**, en millones de dólares.

## De qué están hechas

| Componente | Qué es |
|---|---|
| **Divisas** | Dólares y otras monedas, en efectivo o en depósitos e inversiones en el exterior. Es lo más "líquido": lo que se puede usar de inmediato. |
| **Oro** | Oro monetario del BCB, valorado a precio internacional. |
| **DEG** | Derechos especiales de giro: una unidad de cuenta del Fondo Monetario Internacional (FMI), canjeable por monedas de otros países miembros. |
| **Tramo de reserva en el FMI** | La parte de la cuota de Bolivia en el FMI que el país puede usar sin condiciones. |

Al {{ D.reservas.fecha_larga }}, la composición era:

{% for c in D.reservas.comp %}- **{{ c.nombre }}:** {{ c.valor_txt }} millones de dólares ({{ c.pct_txt }}%)
{% endfor %}

## Qué pasó desde 2016

Con datos del BCB:

| Fecha | RIN total | Oro | Divisas |
|---|---|---|---|
| Ene-2016 | 12.818 | 1.529 | 11.047 |
| Dic-2018 | 8.946 | 1.768 | 6.909 |
| Dic-2020 | 5.276 | 2.613 | 2.386 |
| Dic-2022 | 3.796 | 2.519 | 709 |
| Dic-2023 | 1.709 | 1.566 | 166 |
| Dic-2024 | 1.977 | 1.889 | 47 |
| Dic-2025 | 3.713 | 3.133 | 505 |
| Jun-2026 | 3.617 | 2.883 | 666 |
| {{ D.reservas.fecha_larga }} | {{ D.reservas.rin_txt }} | — | {{ D.reservas.divisas_txt }} |

*Millones de dólares.*

Se ven dos cosas:

1. **Las divisas casi desaparecieron.** Pasaron de más de 11.000 millones en 2016 a menos de 50 millones a fines de 2024. Esa es la razón de fondo de la escasez de dólares que vivió el país.
2. **El oro pasó a ser casi todo.** Hoy representa alrededor del {{ D.reservas.oro_pct_txt }}% de las reservas. El punto más bajo del total en esta serie fue en febrero de 2024, con unos 1.582 millones.

## Por qué importa que sean sobre todo oro

Cuando las reservas son mayormente oro, su valor en dólares **sube y baja con el precio internacional del oro**, aunque el BCB no haga nada. Una buena racha del oro puede inflar la cifra total sin que haya más dólares disponibles para la economía.

Por eso, para saber cuántos dólares "de verdad" hay para usar, conviene mirar la línea de **divisas** además del total. En la [página de reservas]({{ url('/reservas-internacionales/') }}) se pueden ver ambas.

## Netas, brutas y "netas de obligaciones"

- **Netas (RIN):** la cifra principal que publica el BCB, que es la que mostramos.
- **Netas de obligaciones:** una cifra mensual que resta además algunos compromisos, como convenios de crédito recíproco y pasivos por operaciones con oro. Sale con un mes de rezago.

Una corrección para quien conoce la versión anterior de este sitio: ahí la cifra principal se rotulaba como "reservas brutas". Es el dato que el BCB publica como **reservas internacionales netas**, y así la nombramos ahora.

<div class="fuentes" markdown="1">

**Fuentes**

- Banco Central de Bolivia: *Reservas Internacionales Netas del BCB por componentes* y boletín estadístico semanal. Cálculos propios.
- Reservas a junio de 2026 (3.617,3 millones): [Correo del Sur](https://correodelsur.com/economia/20260723/las-reservas-internacionales-de-bolivia-llegan-a-3-617-3-millones-de-dolares-hasta-junio.html).

</div>
