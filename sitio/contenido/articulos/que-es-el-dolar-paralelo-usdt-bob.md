---
h1: "Dólar paralelo en Bolivia: qué es el USDT/BOB y cómo leer su precio"
titulo_corto: "Qué es el dólar paralelo (USDT/BOB)"
titulo: "Qué es el dólar paralelo (USDT/BOB) | Pulso Económico"
descripcion: "Por qué el precio del USDT en Binance P2P se convirtió en la referencia del dólar paralelo en Bolivia, cómo se calcula, qué tan confiable es y qué no te dice."
resumen: "Por qué una criptomoneda terminó marcando el precio del dólar paralelo, y qué tan confiable es como referencia."
fecha: 2026-10-18
actualizado: 2026-10-18
tipo_og: article
relacionado_con: [paralelo, brecha]
---
Cuando alguien en Bolivia pregunta "¿a cuánto está el paralelo?", muchas veces la respuesta sale de una pantalla de Binance. Suena raro que una criptomoneda marque el precio del dólar, pero tiene una explicación. Esta guía cuenta qué es el USDT/BOB, por qué se volvió la referencia y qué precauciones hay que tener al leerlo.

## Primero, qué es el dólar paralelo

El dólar paralelo es el precio al que se compran y venden dólares **fuera del sistema bancario**: con cambistas, en comercios o entre personas. Aparece cuando, al precio oficial, no hay dólares suficientes para todos los que los quieren.

En Bolivia eso pasó con fuerza desde 2023. El oficial seguía fijo en Bs 6,96, pero los bancos tenían cada vez menos dólares para vender. Quien necesitaba dólares para importar, viajar o ahorrar empezó a pagar más en otros canales. Así nació un precio paralelo, sin un registro oficial que lo publique.

## Qué es el USDT

El USDT (Tether) es una **stablecoin**: una moneda digital diseñada para mantener un valor de un dólar estadounidense. Se compra y se vende en plataformas de intercambio, y una de las más usadas en la región es **Binance P2P** (*peer to peer*, "entre personas"). Ahí, personas y comerciantes publican anuncios con el precio al que compran o venden USDT a cambio de bolivianos, y la plataforma hace de intermediaria del pago.

## Por qué se volvió la referencia

1. **Es público.** Cualquiera puede ver los anuncios y sus precios en cualquier momento.
2. **Es continuo.** El mercado funciona las 24 horas, todos los días.
3. **Tiene volumen.** Con la escasez de dólares en efectivo, muchas personas y empresas empezaron a usar USDT para ahorrar o pagar al exterior. Medios bolivianos e internacionales documentaron ese crecimiento.
4. **Sigue al dólar.** Como el USDT busca valer un dólar, su precio en bolivianos es, en la práctica, el precio del dólar en ese mercado.

Por eso la prensa boliviana empezó a reportar el "dólar paralelo" junto con el precio del USDT, y muchas personas lo usan para negociar con cambistas.

## Cómo lo medimos en Pulso Económico

- Intentamos consultar cada 15 minutos la API pública de Binance P2P, en la sección de anuncios para vender USDT a cambio de bolivianos.
- Tomamos los **10 primeros anuncios** y publicamos la **mediana**: si ordenas los 10 precios de menor a mayor, es el valor del medio. A diferencia del promedio, un anuncio con un precio absurdo no la mueve.
- Si Binance no responde, reintentamos. Si el precio nuevo salta más de 25% respecto del anterior, lo descartamos por probable error.

El resultado se ve en [dólar paralelo]({{ url('/dolar-paralelo/') }}). Hoy, a las {{ D.usdt.hora }}, es **Bs {{ D.usdt.valor_txt }}**.

## Lo que el USDT/BOB no te dice

- **No es el precio del billete.** Un cambista en la calle puede cobrar más o menos. Influyen el efectivo, el monto, la confianza y el lugar.
- **No es un precio garantizado.** Es la mediana de anuncios publicados en un momento. Al operar, el precio final depende del comerciante, del medio de pago y del monto.
- **Comprar y vender no cuestan lo mismo.** En cualquier mercado de cambio hay una diferencia entre el precio de compra y el de venta.
- **Tiene riesgos propios.** Operar con criptomonedas tiene riesgos de fraude, de bloqueo de cuentas y regulatorios. Antes de hacerlo, infórmate sobre la normativa vigente del BCB y de la ASFI.

## ¿Y ahora que el oficial es flexible?

Desde junio de 2026, el tipo de cambio oficial se calcula cada día con operaciones reales de los bancos. Desde entonces, el paralelo y el oficial quedaron muy cerca: la [brecha]({{ url('/brecha-cambiaria/') }}) pasó de más de 160% en mayo de 2025 a unos pocos puntos, a veces incluso negativa. El paralelo sigue siendo útil como termómetro: si vuelve a separarse mucho del oficial, es una señal de que al precio oficial no hay dólares suficientes.

<div class="fuentes" markdown="1">

**Fuentes**

- Datos propios: mediana de anuncios de USDT/BOB en Binance P2P, desde septiembre de 2023. Ver la [metodología]({{ url('/metodologia/') }}).
- Rol del USDT y de las plataformas P2P en el mercado boliviano: [Correo del Sur](https://correodelsur.com/economia/20260319/dolar-paralelo-en-bolivia-el-rol-de-las-plataformas-p2p.html) y [CriptoNoticias](https://www.criptonoticias.com/mercados/usdt-parte-fundamental-dolar-paralelo-bolivia/).

</div>
