---
slug: metodologia
titulo: "Metodología y fuentes de datos | Pulso Económico"
descripcion: "De dónde salen los datos de Pulso Económico, cada cuánto se actualizan, cómo se calculan el paralelo, la brecha y el promedio de bancos, y sus límites."
h1: "Metodología y fuentes"
dek: "Cómo se obtiene, se controla y se calcula cada cifra del sitio, y qué no se puede concluir de ella."
titulo_corto: "Metodología"
actualizado: 2026-10-18
prioridad: 0.5
faq: []
---
## Resumen

| Dato | Fuente | Frecuencia de consulta | Rezago típico |
|---|---|---|---|
| Dólar paralelo (USDT/BOB) | API pública de Binance P2P | Se intenta cada 15 minutos | De minutos a varias horas (ver abajo) |
| Tipo de cambio oficial (TCO) | Servicio independiente que replica la publicación del BCB (`apibcb.cucu.bo`) | Cada 15 minutos | El BCB lo publica a las 23:30 de cada día hábil |
| Precio y monto por banco | Banco Central de Bolivia, publicación por entidad | Cada 3 horas | Un día hábil o más |
| Reservas internacionales netas | BCB: boletín semanal y planilla por componentes | Cada 3 horas | Días o semanas |
| Balanza cambiaria | BCB, planilla mensual | Cada 3 horas | Semanas |
| Tipo de cambio real (ITCR) | BCB, planilla mensual | Cada 3 horas | Semanas |
| Titulares de prensa | Google News, filtrado a medios bolivianos y a notas de los últimos 7 días | Cada 3 horas | Horas |

Las consultas las ejecuta un proceso automático en GitHub Actions. Los horarios son aproximados: GitHub puede demorar algunas ejecuciones varios minutos.

## Dólar paralelo

- Se consulta la sección de anuncios para vender USDT a cambio de bolivianos en Binance P2P (lo que te pagan si vendes USDT) y se toman los **10 primeros anuncios** que muestra la plataforma.
- Se publica la **mediana** de esos 10 precios. La mediana resiste mejor que el promedio a un anuncio con un precio fuera de lugar.
- **Controles:** si Binance devuelve una lista vacía, se hacen hasta 3 intentos. Si el valor nuevo difiere más de 25% del anterior, se descarta.
- **Valor diario:** para el histórico se guarda el último valor de cada día (hora de Bolivia).
- **Frecuencia real:** aunque la consulta se programa cada 15 minutos, en los 30 días previos al 18-oct-2026 hubo en promedio entre 4 y 8 mediciones exitosas por día, con una separación típica (mediana) de unas 4 horas. Las causas son las demoras y omisiones de los horarios de GitHub Actions y las respuestas vacías de Binance a servidores de centros de datos. Por eso mostramos siempre la hora exacta de la última medición.
- **Límites:** el USDT es una aproximación al dólar paralelo, no el precio del billete. El precio de compra y el de venta difieren. Binance puede cambiar o restringir su API sin aviso.

## Tipo de cambio oficial

- Se toma el valor de compra y venta publicado por el BCB, a través de `apibcb.cucu.bo`, un servicio de terceros que replica la publicación oficial. Lo usamos porque entrega el dato en un formato estable. **No es una fuente oficial en sí misma.**
- **Control:** se descarta un valor nuevo que difiera más de 15% del anterior.
- **Tramo referencial:** entre el 1 de diciembre de 2025 y fines de junio de 2026, el oficial legal estaba fijo en Bs 6,86 / 6,96. En esas fechas nuestra serie contiene el **valor referencial** que publicaba el BCB, no el oficial legal. Los gráficos marcan ese tramo con sombreado.

## Precio por banco

- El BCB publica, por entidad y por día, el precio promedio de las compras de dólares a clientes y el monto comprado.
- **Promedio del sistema:** promedio de los precios de todos los bancos, ponderado por el monto que compró cada uno.
- **Vs. mercado (herramienta interactiva):** diferencia entre el promedio ponderado del banco y el del mercado en los mismos días, ponderada por el monto del banco.
- **Muestra delgada (†):** bancos PyME o con menos de 0,2% del monto del mercado, o con datos en menos de la mitad de los días del período. Su precio puede depender de muy pocas operaciones.
- **Para comparar bancos** ("el que más pagó / el que menos pagó") se excluyen los bancos con muestra delgada.

## Brecha cambiaria

Brecha (%) = (paralelo − oficial) ÷ oficial × 100. El paralelo es el precio que pagan en Binance P2P a quien vende USDT. El oficial es la venta publicada hasta junio de 2026 (6,96 y luego la venta del valor referencial, que era un precio máximo) y, desde el 29 de junio de 2026, el valor único que calcula el BCB. Entre julio y septiembre de 2026 el BCB publicaba además una "venta" igual al oficial más 10 centavos, que era el tope de venta de los bancos y no se usa. La cifra de hoy usa la última medición del paralelo. El histórico usa el último valor de cada día y el oficial vigente ese día.

## Reservas, balanza e ITCR

Se leen de las planillas Excel que publica el BCB. Para evitar errores de lectura, un valor nuevo que salte más de cierto umbral respecto de su vecino se descarta: 20% en reservas y 35% en el ITCR, umbral elevado por el salto real de mediados de 2026. La balanza no tiene umbral, porque su flujo cambia de signo legítimamente.

## Avisos de dato atrasado

Después de cada actualización se revisa la antigüedad del último dato de cada serie. Si supera un límite razonable (por ejemplo, 3 horas para el paralelo o 4 días para el oficial, contando fines de semana), la cifra muestra "dato atrasado" y el responsable del sitio recibe una alerta.

## Correcciones

- **Octubre de 2026:** la versión anterior del sitio rotulaba como "reservas brutas" la serie que el BCB publica como **reservas internacionales netas**. Corregido.
- **Octubre de 2026:** se aclara que entre diciembre de 2025 y junio de 2026 la serie "oficial" es el valor referencial del BCB.

## Datos abiertos

Los datos que alimentan los gráficos están disponibles en formato JSON: [tipo de cambio oficial]({{ url('/datos/tco.json') }}), [paralelo]({{ url('/datos/usdt.json') }}), [brecha]({{ url('/datos/brecha.json') }}), [bancos]({{ url('/datos/bancos.json') }}), [reservas]({{ url('/datos/reservas.json') }}), [balanza]({{ url('/datos/balanza.json') }}), [ITCR]({{ url('/datos/itcr.json') }}) y un [resumen del día]({{ url('/datos/resumen.json') }}). Si los usas, te pedimos citar a Pulso Económico y a la fuente original de cada serie.
