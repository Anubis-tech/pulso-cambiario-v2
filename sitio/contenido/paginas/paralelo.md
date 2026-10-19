---
titulo: "Dólar paralelo hoy en Bolivia: Bs {{ D.usdt.valor_txt }} (USDT/BOB) | Pulso Económico"
og_titulo: "Dólar paralelo en Bolivia hoy"
descripcion: "Precio del dólar paralelo en Bolivia hoy: Bs {{ D.usdt.valor_txt }} según USDT/BOB en Binance P2P ({{ D.usdt.hora }}). Gráfico de 24 horas, histórico desde 2023 y comparación con el oficial."
h1: "Dólar paralelo en Bolivia hoy"
dek: "Hoy el dólar paralelo está a Bs {{ D.usdt.valor_txt }}. Lo medimos con el precio del USDT en Binance, la referencia que usa la gente."
resumen: "El dólar paralelo es el precio del dólar fuera de los bancos. Lo medimos con el USDT en Binance P2P, con lo que pagan a quien vende: a las {{ D.usdt.hora }} estaba en Bs {{ D.usdt.valor_txt }}."
fuente: "Fuente: Binance P2P, mediana de los 10 primeros anuncios. Medición de las {{ D.usdt.hora }}."
faq:
  - p: "¿A cuánto está el dólar paralelo hoy?"
    r: "A las {{ D.usdt.hora }} del {{ D.usdt.fecha_larga }} (hora de Bolivia), el USDT cotiza a **Bs {{ D.usdt.valor_txt }}** en Binance P2P.{% if D.usdt.min24_txt %} En las últimas 24 horas se movió entre Bs {{ D.usdt.min24_txt }} y Bs {{ D.usdt.max24_txt }}.{% endif %}"
  - p: "¿Por qué se usa el USDT como dólar paralelo?"
    r: "El USDT (Tether) es una moneda digital diseñada para valer un dólar estadounidense. Durante la escasez de dólares en efectivo, mucha gente en Bolivia empezó a comprar y vender USDT en plataformas entre personas, y su precio en bolivianos se volvió una referencia pública y verificable del mercado paralelo. No es un dólar en billete: es una aproximación."
  - p: "¿El precio que veo aquí es el que voy a conseguir?"
    r: "No necesariamente. Es la mediana de los primeros anuncios publicados en un momento dado. El precio real depende del monto, del medio de pago, del comerciante y de la hora. Comprar y vender no tienen exactamente el mismo precio."
  - p: "¿Es legal comprar USDT en Bolivia?"
    r: "Las reglas sobre activos virtuales en Bolivia cambiaron en los últimos años. Antes de operar, consulta la normativa vigente del Banco Central de Bolivia y de la ASFI. Este sitio solo informa precios y no recomienda operar."
---
## Qué es el dólar paralelo

El dólar paralelo es el precio al que se compran y venden dólares fuera del sistema bancario. Mientras el tipo de cambio oficial estuvo fijo en Bs 6,96, los bancos tenían pocos dólares para vender, y la demanda se fue a cambistas, comercios y plataformas entre personas. Ahí el precio lo marcaban la oferta y la demanda.

No existe un registro oficial de esas operaciones. Por eso hace falta una **referencia observable**, y la más usada hoy es el precio del USDT en bolivianos.

## Cómo lo medimos

- **Fuente:** la API pública de Binance P2P, la sección de anuncios para vender USDT a cambio de bolivianos, es decir, lo que te pagan si vendes USDT.
- **Cálculo:** tomamos los 10 primeros anuncios que muestra Binance y nos quedamos con la **mediana**: el valor del medio, o el promedio de los dos del medio cuando son 10. La mediana no se deja arrastrar por un anuncio con un precio absurdo, como sí lo haría un promedio.
- **Frecuencia:** se intenta medir cada 15 minutos. En la práctica hay huecos de varias horas, porque el servicio que programa las consultas (GitHub Actions) demora u omite ejecuciones y porque Binance a veces no devuelve anuncios a servidores de centros de datos. Por eso mostramos siempre la hora de la última medición exitosa.
- **Control de calidad:** si un valor nuevo difiere más de 25% del anterior, se descarta como probable error. Si Binance no responde, se hacen hasta tres intentos.
- **Valor diario:** el gráfico histórico usa el último valor de cada día.

## Qué no es

El USDT es una aproximación, no el precio del billete de dólar en la calle. Un cambista puede cobrar más o menos, y comprar y vender tienen precios distintos. Tampoco es una cotización garantizada: Binance puede cambiar o cerrar su API sin aviso. Si eso pasa, la cifra de esta página mostrará un aviso de "dato atrasado".

Para comparar con el oficial, mira la [brecha cambiaria]({{ url('/brecha-cambiaria/') }}). Para convertir montos, usa el [conversor]({{ url('/conversor/') }}). Si quieres saber más, lee [qué es el dólar paralelo y cómo leerlo]({{ url('/articulos/que-es-el-dolar-paralelo-usdt-bob/') }}).
