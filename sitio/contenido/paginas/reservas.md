---
titulo: "Reservas del BCB hoy: $us {{ D.reservas.rin_txt }} millones | Pulso Económico"
og_titulo: "Reservas internacionales del BCB"
descripcion: "Reservas internacionales netas del BCB al {{ D.reservas.fecha_larga }}: {{ D.reservas.rin_txt }} millones de dólares. Composición en oro y divisas, evolución desde 2016 y qué significan."
h1: "Reservas internacionales del BCB"
dek: "Cuántos activos en moneda extranjera tiene el Banco Central de Bolivia, de qué están hechos y cómo han cambiado."
resumen: "Las reservas internacionales netas del BCB sumaban $us {{ D.reservas.rin_txt }} millones al {{ D.reservas.fecha_larga }}. Son el oro, las divisas y otros activos externos con los que el país respalda su moneda."
fuente: "Fuente: Banco Central de Bolivia, datos al {{ D.reservas.fecha_larga }}."
faq:
  - p: "¿Cuánto tiene Bolivia en reservas internacionales?"
    r: "Al {{ D.reservas.fecha_larga }}, las reservas internacionales netas del BCB suman **{{ D.reservas.rin_txt }} millones de dólares**{% if D.reservas.d12_txt is defined %}, {{ D.reservas.d12_txt }} millones ({{ D.reservas.d12_pct_txt }}%) respecto de un año antes{% endif %}. Alrededor del {{ D.reservas.oro_pct_txt }}% es oro."
  - p: "¿Por qué la mayor parte de las reservas es oro?"
    r: "Porque en los últimos años las divisas (dólares y otras monedas) se gastaron mucho más rápido que el oro: el BCB las usó para pagar obligaciones y abastecer de dólares a la economía con el tipo de cambio fijo. Además, el valor en dólares cambia con el precio internacional del oro: las reservas pueden subir o bajar sin que el BCB compre ni venda nada."
  - p: "¿Qué son las reservas 'netas de obligaciones'?"
    r: "Es una cifra mensual que publica el BCB restando a las reservas algunas obligaciones, como los convenios de crédito recíproco y los pasivos por operaciones con oro. Sale con un mes de rezago, así que aquí no se grafica."
---
## Qué son las reservas internacionales

Las reservas internacionales son los activos en moneda extranjera que administra el Banco Central de Bolivia: oro, divisas (sobre todo dólares), derechos especiales de giro (DEG, una unidad de cuenta del Fondo Monetario Internacional) y el tramo de reserva en el FMI. Sirven para pagar importaciones y deuda externa, para respaldar la moneda y como colchón ante crisis.

El BCB las publica como **reservas internacionales netas (RIN)**, en millones de dólares. Hay una cifra semanal (que usamos para el dato más reciente) y una serie histórica por componentes.

## Qué muestran los datos

- A comienzos de 2016, las RIN superaban los **12.800 millones** de dólares, con más de 11.000 millones en divisas.
- Fueron cayendo año tras año. El punto más bajo de la serie de este sitio es de **febrero de 2024: unos 1.582 millones**.
- Desde entonces se recuperaron. Al {{ D.reservas.fecha_larga }} suman **{{ D.reservas.rin_txt }} millones**, y el **oro** es el componente principal ({{ D.reservas.oro_pct_txt }}%).

Que el oro pese tanto tiene una consecuencia práctica: cuando sube el precio internacional del oro, las reservas suben en dólares aunque el BCB no haga ninguna operación. Por eso conviene mirar también las **divisas**, que son lo que el BCB puede usar directamente para vender dólares al sistema. Al {{ D.reservas.fecha_larga }} eran {{ D.reservas.divisas_txt }} millones.

## Fuentes y notas

- Banco Central de Bolivia, *Reservas Internacionales Netas del BCB por componentes* (serie mensual) y boletín estadístico semanal.
- La serie de este sitio empieza en enero de 2016.
- **Corrección respecto de la versión anterior del sitio:** la versión anterior rotulaba esta cifra como "reservas brutas". El BCB la publica como reservas internacionales **netas**, y así la nombramos ahora.
