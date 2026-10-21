---
titulo: "Dólar hoy en Bolivia: paralelo, oficial y por banco | Pulso Económico"
descripcion: "Dólar paralelo hoy: Bs {{ D.usdt.valor_txt }} (Binance P2P). Oficial BCB: Bs {{ D.tco.venta_txt }}. Brecha, precio por banco y conversor, actualizados automáticamente."
h1: "Dólar hoy en Bolivia"
dek: "El tipo de cambio oficial del BCB, el dólar paralelo y lo que pagan los bancos, en un solo lugar y con actualización automática."
faq:
  - p: "¿A cuánto está el dólar hoy en Bolivia?"
    r: "A las {{ D.usdt.hora }} del {{ D.usdt.fecha_larga }}, el dólar paralelo (USDT/BOB en Binance P2P) cotiza a **Bs {{ D.usdt.valor_txt }}**. El tipo de cambio oficial del Banco Central de Bolivia vigente para el {{ D.tco.fecha_larga }} es **Bs {{ D.tco.venta_txt }}**. La diferencia entre ambos es de {{ D.brecha.pct_txt }}%."
  - p: "¿Cuál es la diferencia entre el dólar oficial y el paralelo?"
    r: "El **oficial** lo publica el Banco Central de Bolivia (BCB) cada día hábil a partir de las compras de dólares que hacen los bancos. Se usa para las operaciones del sector público y como referencia para el resto. El **paralelo** es el precio al que las personas compran y venden dólares fuera del sistema bancario. Hoy su referencia más usada es el precio del USDT (una criptomoneda atada al dólar) en Binance P2P. [Ver la diferencia en detalle]({{ url('/brecha-cambiaria/') }})."
  - p: "¿Cada cuánto se actualizan los datos?"
    r: "El dólar paralelo se intenta medir cada 15 minutos, y junto a la cifra se muestra la hora de la última medición exitosa. El tipo de cambio oficial se consulta en cada actualización y cambia una vez por día hábil (el BCB lo publica a las 23:30). Los precios por banco, las reservas, la balanza cambiaria y el tipo de cambio real se revisan cada 3 horas y cambian cuando el BCB publica datos nuevos."
  - p: "¿Puedo comprar o vender dólares en Pulso Económico?"
    r: "No. Pulso Económico es un sitio de información. No compra, no vende ni intermedia divisas, y no recomienda operaciones. Las cifras son referenciales."
---
## Cómo leer estas cifras

En Bolivia conviven hoy tres precios del dólar, y cada uno responde a una pregunta distinta.

**El tipo de cambio oficial del BCB.** Durante más de 14 años, desde noviembre de 2011, estuvo fijo en Bs 6,86 para la compra y Bs 6,96 para la venta. En junio de 2026 el país pasó a un régimen flexible. Desde la Resolución de Directorio 142/2026, de septiembre de 2026, el Banco Central calcula cada día hábil un único valor: la mediana, ponderada por monto, de los dólares que los bancos compraron a sus clientes y al propio BCB. Es la referencia legal, por ejemplo para el sector público y la contabilidad. [Así se calcula]({{ url('/articulos/como-calcula-el-bcb-el-tipo-de-cambio-oficial/') }}).

**El dólar paralelo.** Es el precio al que la gente consigue dólares fuera de los bancos. Como no tiene un registro oficial, aquí se mide con el precio del USDT (una moneda digital diseñada para valer un dólar) en Binance P2P, la plataforma donde personas y comerciantes publican sus ofertas. Tomamos la mediana de los primeros 10 anuncios e intentamos medirlo cada 15 minutos. [Qué mide y qué no]({{ url('/articulos/que-es-el-dolar-paralelo-usdt-bob/') }}).

**El precio de los bancos.** El BCB publica, banco por banco, a qué precio promedio compró dólares cada entidad y cuánto compró. Es el dato más cercano a lo que de verdad pagaron los bancos. Pocas fuentes lo muestran así. [Ver los bancos]({{ url('/tipo-de-cambio-bancos/') }}).

La **brecha** es la distancia entre el paralelo y el oficial. Llegó a superar el 160% en mayo de 2025, cuando el oficial seguía en Bs 6,96 y el paralelo pasó los Bs 18. Desde que el oficial empezó a moverse, la brecha se redujo a pocos puntos y hoy oscila cerca de cero. [Ver la historia de la brecha]({{ url('/brecha-cambiaria/') }}).

## De dónde salen los datos

Todo viene de fuentes públicas: el [Banco Central de Bolivia](https://www.bcb.gob.bo/) para el tipo de cambio oficial, los bancos, las reservas, la balanza cambiaria y el tipo de cambio real, y [Binance P2P](https://p2p.binance.com/) para el paralelo. La [metodología]({{ url('/metodologia/') }}) explica cómo se procesa cada dato y cuáles son sus límites. Si una fuente deja de responder, la cifra afectada lo indica con un aviso de "dato atrasado".

