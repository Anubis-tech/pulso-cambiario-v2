---
titulo: "Brecha cambiaria en Bolivia hoy: {{ D.brecha.pct_txt }}% | Pulso Económico"
og_titulo: "Brecha cambiaria en Bolivia"
descripcion: "La brecha entre el dólar paralelo (Bs {{ D.usdt.valor_txt }}) y el oficial del BCB (Bs {{ D.tco.venta_txt }}) es de {{ D.brecha.pct_txt }}%. Historia de la brecha desde 2024 y promedio mensual."
h1: "Brecha cambiaria en Bolivia"
dek: "Cuánto más caro (o más barato) está el dólar paralelo que el oficial, hoy y a lo largo del tiempo."
faq:
  - p: "¿Cuál es la brecha cambiaria hoy?"
    r: "Con el paralelo a Bs {{ D.usdt.valor_txt }} ({{ D.usdt.hora }}) y el oficial a Bs {{ D.tco.venta_txt }}, la brecha es de **{{ D.brecha.pct_txt }}%**: el paralelo está {{ D.brecha.bs_txt }} Bs por dólar {{ 'por encima' if D.brecha.pct >= 0 else 'por debajo' }} del oficial."
  - p: "¿Cómo se calcula la brecha cambiaria?"
    r: "Brecha (%) = (dólar paralelo − tipo de cambio oficial de venta) ÷ tipo de cambio oficial de venta × 100. Por ejemplo, con un paralelo de Bs 12 y un oficial de Bs 10, la brecha es (12 − 10) ÷ 10 × 100 = 20%."
  - p: "¿Puede ser negativa la brecha?"
    r: "Sí. Si el paralelo está más barato que el oficial, la brecha es negativa. Pasó varias veces después de junio de 2026, cuando el oficial empezó a moverse todos los días y ambos precios quedaron muy cerca."
---
## Qué es la brecha cambiaria

La brecha cambiaria mide cuánto se aleja el precio del dólar en el mercado paralelo del tipo de cambio oficial. Una brecha grande indica que, al precio oficial, no hay dólares suficientes para todos los que los quieren, así que la gente paga más en otro lado. Una brecha cercana a cero indica que los dos mercados están alineados.

## Qué pasó en Bolivia

Los datos de esta página empiezan en junio de 2024, cuando el oficial estaba fijo en Bs 6,96 y el paralelo (medido con USDT/BOB) rondaba los Bs 8,9. La brecha ya era de casi 28%.

- **2024 y comienzos de 2025:** con el oficial congelado, cada subida del paralelo agrandaba la brecha. A fines de 2024 superaba el 59%.
- **Mayo de 2025:** el máximo de la serie. El paralelo llegó a Bs 18,27 y la brecha a **{{ D.brecha.max_txt }}%** ({{ D.brecha.max_fecha }}).
- **Diciembre de 2025 a junio de 2026:** el BCB empieza a publicar un valor referencial con operaciones reales de los bancos. Comparada contra ese valor, la brecha cae a pocos puntos (en el gráfico, el tramo sombreado).
- **Desde fines de junio de 2026:** con el régimen flexible, el oficial se mueve cada día y la brecha oscila alrededor de cero, a veces positiva y a veces negativa.

## Cómo se calcula aquí

Para cada día cruzamos el **último valor del paralelo** (USDT/BOB en Binance P2P) con el **tipo de cambio oficial de venta vigente ese día**. La cifra de hoy usa la medición más reciente del paralelo, de las {{ D.usdt.hora }}. Por eso puede diferir un poco del último punto del gráfico, que usa el último valor de cada día.

**Advertencia de lectura.** Entre el 1 de diciembre de 2025 y fines de junio de 2026, la serie oficial de este sitio es el valor referencial del BCB y no el oficial legal de Bs 6,96. Si se midiera contra 6,96, la brecha de ese período sería mucho mayor. Elegimos el referencial porque reflejaba precios reales de operaciones. Lo explicamos en [tipo de cambio oficial]({{ url('/tipo-de-cambio-oficial/') }}) y en el artículo [brecha cambiaria: qué es y cómo se calcula]({{ url('/articulos/brecha-cambiaria-que-es-y-como-se-calcula/') }}).
