---
titulo: "Índice de tipo de cambio real de Bolivia (ITCR) | Pulso Económico"
og_titulo: "Tipo de cambio real de Bolivia (ITCR)"
descripcion: "Índice de tipo de cambio real de Bolivia en {{ D.itcr.mes }}: {{ D.itcr.valor_txt }} (base dic-2022 = 100). Qué mide, cómo leerlo y su evolución desde 2000."
h1: "Índice de tipo de cambio real (ITCR)"
dek: "Una medida de cuán caros o baratos son los precios de Bolivia frente a los de sus socios comerciales, ajustada por inflación."
resumen: "El tipo de cambio real compara los precios de Bolivia con los de sus socios comerciales, corrigiendo por inflación. En {{ D.itcr.mes }} el índice fue {{ D.itcr.valor_txt }} (diciembre de 2022 = 100): si sube, Bolivia se abarata frente a ellos."
fuente: "Fuente: Banco Central de Bolivia, índice multilateral."
faq:
  - p: "¿Qué significa que el índice suba?"
    r: "Que el boliviano se **depreció en términos reales**: los bienes bolivianos se abaratan frente a los de los socios comerciales. Eso ayuda a exportar y encarece lo importado. Si el índice baja, pasa lo contrario: hay apreciación real."
  - p: "¿Por qué saltó el índice a mediados de 2026?"
    r: "Porque el tipo de cambio oficial dejó de estar fijo en junio de 2026 y subió con fuerza. En los datos, el índice pasó de alrededor de 113 en junio a más de 146 en julio de 2026, una depreciación real abrupta."
  - p: "¿Qué es la base diciembre de 2022 = 100?"
    r: "Es el punto de referencia del índice: diciembre de 2022 vale 100, y cualquier otro mes se compara contra él. Un valor de {{ D.itcr.valor_txt }} significa que el tipo de cambio real está {{ D.itcr.vs_base_txt.lstrip('+−') }}% {{ 'por debajo' if D.itcr.vs_base_txt.startswith('−') else 'por encima' }} de ese mes."
---
## Qué mide

El tipo de cambio "nominal" es cuántos bolivianos cuesta un dólar. El tipo de cambio **real** corrige ese número por la diferencia de inflación entre Bolivia y sus socios comerciales. Responde una pregunta práctica: ¿los productos bolivianos se están volviendo más caros o más baratos que los de afuera?

El índice **multilateral** combina a varios socios comerciales, ponderados por su peso en el comercio de Bolivia. El BCB lo publica mensualmente.

## Cómo leerlo

- **Sube:** depreciación real. Bolivia se vuelve más "barata" frente al exterior, lo que favorece a exportadores y encarece importaciones.
- **Baja:** apreciación real. Bolivia se vuelve más "cara", lo que favorece importar y perjudica la competitividad de lo que se produce localmente.

Durante el período de tipo de cambio fijo (2011–2026), el índice tendió a bajar: de cerca de 146 en noviembre de 2011 a 100 en diciembre de 2022. Con el boliviano fijo frente al dólar, los cambios de precios en Bolivia y en sus socios, y el movimiento de las monedas de esos socios frente al dólar, fueron apreciando el boliviano en términos reales. Con el régimen flexible de 2026, el índice dio un salto hacia arriba.

## Fuente

Banco Central de Bolivia, planilla *Índices de tipo de cambio real*, columna multilateral. Base diciembre de 2022 = 100. Datos mensuales desde enero de 2000.
