# Las cuatro preguntas de negocio, explicadas desde cero

Esta guía explica qué te están pidiendo, cómo se calcula y cómo podría verse la respuesta. Los ejemplos son **ficticios**, salvo el caso del proyecto que se identifica expresamente. No son resultados calculados para CaféNorte ni fijan las reglas definitivas del análisis.

## 1. Top 10 SKUs por rotación de inventario en los últimos 6 meses

### Qué te están preguntando

«¿Cuáles son los diez productos que más se venden en relación con la cantidad que mantenemos en inventario durante esos seis meses?»

- **Top 10:** lista de los diez primeros, ordenados de mayor a menor según la métrica solicitada. Si hay menos de diez productos con datos válidos, se muestran los disponibles.
- **SKU (Stock Keeping Unit):** código que identifica una referencia de producto. Por ejemplo, `CAFE-250G` podría representar una bolsa de café de 250 gramos y `CAFE-1KG`, la de un kilo. Aunque sean de la misma marca, son referencias distintas.
- **Inventario o stock:** unidades de producto que la empresa tiene registradas en existencias.
- **Rotación:** cuántas veces lo vendido durante el período equivale al inventario promedio que se mantuvo. Se expresa en **veces durante ese período**.
- **Últimos seis meses:** ventana de fechas que debe definirse con una fecha de corte.

### Ejemplo paso a paso

Imagina estas cifras de seis meses:

| Producto | Unidades vendidas en seis meses | Inventario promedio en unidades | Rotación en seis meses |
|---|---:|---:|---:|
| Café de 250 g | 600 | 100 | 6 veces |
| Taza | 300 | 25 | 12 veces |
| Café de 1 kg | 900 | 300 | 3 veces |

En una versión calculada en unidades:

```text
Rotación = unidades vendidas durante el período / inventario promedio del período

Café de 250 g: 600 / 100 = 6 veces
Taza:         300 / 25  = 12 veces
Café de 1 kg: 900 / 300 = 3 veces
```

La taza ocupa el primer lugar por rotación, aunque el café de un kilo vendió más unidades. Una rotación de 12 significa que las ventas del período equivalen a doce veces las existencias promedio; no demuestra que hubiera exactamente doce entregas o reposiciones.

Si tienes inventario diario, puedes calcular el promedio sumando el stock de cada día y dividiéndolo entre los días con cobertura completa. Por ejemplo, con 10, 20 y 30 unidades en tres días: `(10 + 20 + 30) / 3 = 20` unidades. Para seis meses se usa toda la ventana, no solo esos tres días. No conviene promediar únicamente los días disponibles sin advertir que faltan fechas.

### Dos maneras de medirla

La fórmula habitual en valor es:

```text
Rotación = costo de los productos vendidos / valor promedio del inventario a costo
```

Si vendiste mercancía cuyo costo fue $60,000 y mantuviste un inventario promedio valorado a costo en $10,000, la rotación fue `60,000 / 10,000 = 6 veces`.

La fórmula en unidades también es útil por SKU, siempre que ventas e inventario usen la misma unidad de medida. **Hay que indicar cuál versión se eligió.** No debes dividir ingresos de venta entre inventario a costo y llamarlo la misma métrica: estarías mezclando bases distintas.

### Cómo podría verse la respuesta

Una tabla ordenada por rotación descendente, con posición, SKU, nombre, unidades vendidas, inventario promedio, rotación y fechas del período. Si se elige la versión en valor, se muestran costo vendido e inventario promedio a costo.

Para un ranking de toda la empresa se suman las ventas de las tiendas incluidas y se calcula el inventario promedio de su stock total diario. No se obtiene la rotación de la empresa promediando sin ponderación las rotaciones de sus tiendas.

### Para qué sirve y qué revisar

Ayuda a entender qué productos se mueven con rapidez respecto a las existencias que requieren. Una rotación alta puede reflejar demanda fuerte o inventario demasiado escaso; por sí sola no demuestra una buena gestión ni una mayor rentabilidad.

Se necesitan ventas por producto y fecha, inventario durante el período y equivalencias entre códigos de sistemas. Para la versión en valor también se necesitan costos y una regla de valoración. Un inventario promedio cero impide la división: se debe reportar como caso pendiente o no calculable, no como rotación infinita ni como cero.

## 2. Tiendas con quiebres de stock de más de 3 días en el último trimestre

### Qué te están preguntando

«¿En qué tiendas hubo algún producto agotado durante más de tres días seguidos, dentro del trimestre analizado?»

- **Quiebre de stock:** un producto no está disponible para atender la demanda. Tener cero unidades registradas es una señal para detectarlo, según la definición del inventario.
- **Episodio:** intervalo continuo durante el cual un producto permanece agotado en una tienda.
- **Más de tres días:** con medición por días completos, significa **cuatro días o más**. Tres días exactos no cumplen el criterio.
- **Trimestre:** período de tres meses. Puede referirse a un trimestre calendario o a tres meses móviles; se debe aclarar.

El quiebre se evalúa por **tienda y SKU**. Que falte café en una sucursal no significa que toda la tienda esté sin mercancía ni que el café falte en todas las sucursales.

### Ejemplo paso a paso

Supón estos registros diarios para el mismo café:

| Fecha | Stock en tienda T001 | Stock en tienda T002 |
|---|---:|---:|
| 5 de enero | 8 | 4 |
| 6 de enero | 0 | 0 |
| 7 de enero | 0 | 0 |
| 8 de enero | 0 | 0 |
| 9 de enero | 0 | 6 |
| 10 de enero | 12 | 5 |

Con la regla ilustrativa de «un día con stock cero cuenta como día de quiebre»:

- T001 tiene cuatro días seguidos en cero, del 6 al 9 de enero: **sí cumple**.
- T002 tiene tres días seguidos en cero, del 6 al 8 de enero: **no cumple**.

Si T001 tuviera un día en cero en enero, otro en febrero y dos en marzo, sumaría cuatro días, pero no serían un episodio de cuatro días consecutivos. La interpretación propuesta es buscar continuidad, no sumar días aislados.

### Cómo podría verse la respuesta

| Tienda | SKU | Inicio del quiebre | Último día en quiebre | Días consecutivos observados |
|---|---|---|---|---:|
| T001 | CAFE-250G | 6 de enero | 9 de enero | 4 |

Además del detalle por episodio, se puede entregar una lista de tiendas afectadas, número de productos con quiebre y episodio más largo. Una tienda puede tener varios productos y varios episodios.

### Para qué sirve y qué revisar

Sirve para priorizar reposiciones y detectar problemas de abastecimiento. Un quiebre indica falta de disponibilidad; no permite calcular por sí solo cuánto se dejó de vender.

Se necesitan existencias por día, tienda y producto, y saber si ese producto debía estar disponible en esa tienda. Un artículo descontinuado o fuera del surtido puede requerir un tratamiento distinto.

Hay que definir cómo tratar stock negativo, tiendas cerradas y días sin datos. **Que falte una fila no significa stock cero.** Una fotografía diaria tampoco prueba que el producto estuvo agotado las 24 horas: el resultado debe describirse como días observados con la regla elegida.

Si el episodio empezó antes del trimestre o continúa después, hay que decidir si se evalúa su duración completa o solo los días dentro de la ventana. Si solo se conoce una parte, se debe indicar que el inicio o fin real no está observado.

## 3. Crecimiento mes a mes (MoM) de ventas por canal en el último año

### Qué te están preguntando

«¿Cuánto aumentaron o disminuyeron las ventas de cada mes frente al mes anterior, por separado para tiendas físicas y venta por internet?»

- **MoM (Month over Month):** comparación de un mes con el inmediatamente anterior.
- **Ventas:** aquí se propone medir el dinero vendido, con una definición consistente de ingreso neto. También podrían medirse unidades, pero es otra métrica y debe etiquetarse.
- **Canal:** medio por el que se realiza la venta. En este caso: físico y e-commerce.
- **Físico:** ventas de las tiendas presenciales, agrupadas en ese canal.
- **E-commerce:** ventas por internet.
- **Crecimiento:** cambio porcentual. Puede ser positivo, negativo o cero.

### Ejemplo paso a paso

```text
MoM (%) = ((ventas del mes actual - ventas del mes anterior)
           / ventas del mes anterior) × 100
```

| Mes | Ventas físicas | MoM físico | Ventas e-commerce | MoM e-commerce |
|---|---:|---:|---:|---:|
| Enero | $100,000 | Requiere diciembre | $20,000 | Requiere diciembre |
| Febrero | $120,000 | +20 % | $18,000 | −10 % |
| Marzo | $108,000 | −10 % | $27,000 | +50 % |

Para febrero:

```text
Físico:     ((120,000 - 100,000) / 100,000) × 100 = +20 %
E-commerce: ((18,000 - 20,000) / 20,000) × 100 = −10 %
```

Esto significa que el canal físico vendió 20 % más dinero que en enero y el canal online, 10 % menos. Cada canal se compara con su propio mes anterior. No se compara físico contra e-commerce para calcular este MoM.

En marzo, e-commerce crece más en porcentaje, pero sigue vendiendo menos dinero que el canal físico. Por eso conviene mostrar importes y porcentajes juntos.

### Cómo podría verse la respuesta

Una tabla como la anterior para los doce meses solicitados y, opcionalmente, una gráfica de evolución por canal. Para calcular el MoM del primer mes mostrado necesitas el mes anterior: **doce meses de resultados requieren trece meses de datos mensuales**.

### Para qué sirve y qué revisar

Permite seguir la evolución de cada canal. No explica por sí solo las causas de los cambios. Un aumento puede relacionarse con más unidades, cambios de precio, promociones u otros factores que requieren análisis adicional.

Se necesitan fechas, importes, moneda y canal, además de reglas para descuentos, devoluciones, cancelaciones e impuestos. Si hay monedas distintas, primero hay que convertir a una base común con una regla documentada.

Si el mes anterior tiene ventas cero, no se puede dividir: se informa «no calculable; base cero», junto con los importes y el cambio en dinero. Si falta información de un mes, no se debe asumir que vendió cero. Si el mes anterior es negativo por ajustes o devoluciones, el porcentaje requiere una interpretación especial.

Conviene comparar meses completos: un mes que lleva diez días no es directamente comparable con otro de treinta. MoM tampoco es crecimiento interanual: marzo frente a febrero es MoM; marzo frente a marzo del año anterior es interanual o **YoY (Year over Year)**.

## 4. Productos con margen negativo y en qué tiendas ocurren

### Qué te están preguntando

«¿Qué productos se vendieron por un ingreso menor que su costo, y en cuáles tiendas pasó?»

- **Ingreso neto de venta:** importe de la venta después de los ajustes aplicables, con una base definida y comparable al costo.
- **Costo de los productos vendidos:** costo atribuible a las unidades vendidas. Si se usa costo unitario: `unidades × costo por unidad`.
- **Margen bruto en dinero:** ingreso neto menos costo de lo vendido.
- **Margen bruto negativo:** el resultado es menor que cero; el ingreso no alcanza a cubrir ese costo.
- **Margen bruto porcentual:** margen bruto dividido entre ingreso neto, multiplicado por 100. Con ingreso cero no se puede calcular así.

### Ejemplo paso a paso

Una tienda vende dos bolsas de café a $80 cada una y su costo es de $100 por bolsa, sobre bases comparables:

```text
Ingreso:                  2 × $80  = $160
Costo de lo vendido:      2 × $100 = $200
Margen bruto en dinero:   $160 - $200 = -$40
Margen bruto porcentual:  (-$40 / $160) × 100 = -25 %
```

En esa venta faltaron $40 para cubrir el costo de las dos bolsas. Este margen bruto no incluye necesariamente renta, sueldos y otros gastos: no es el resultado neto total de la tienda.

### Distinguir una venta negativa del resultado acumulado

Supón estas operaciones del mismo producto en una tienda:

| Operación | Ingreso | Costo vendido | Margen bruto |
|---|---:|---:|---:|
| Venta A | $160 | $200 | −$40 |
| Venta B | $300 | $200 | +$100 |
| Total del período | $460 | $400 | +$60 |

Sí hubo una venta con margen negativo, pero el producto acumuló margen positivo en esa tienda durante el período. La solicitud puede referirse a cualquiera de las dos cosas.

Una salida útil es presentar el margen acumulado por **producto y tienda** y, como detalle, cuántas operaciones negativas hubo y cuánto sumaron sus márgenes negativos. El margen porcentual acumulado se calcula sobre los totales: `60 / 460 × 100 ≈ 13.04 %`; no promediando los porcentajes de las filas.

### Cómo podría verse la respuesta

| SKU | Tienda | Ingreso neto del período | Costo vendido | Margen bruto | Margen bruto % |
|---|---|---:|---:|---:|---:|
| CAFE-250G | T001 | $160 | $200 | −$40 | −25 % |
| TAZA | T003 | $450 | $500 | −$50 | −11.11 % |

La tabla mostraría las combinaciones producto–tienda cuyo margen acumulado es negativo, bajo esa definición. También debe indicar el período analizado, que no aparece especificado en esta cuarta pregunta.

### Un caso ya revisado en CaféNorte

Según la revisión documentada en [casos de margen](../05_antecedentes/casos_margen.md), la operación `V00000000` corresponde a una unidad de `CN-00015` en T033, con monto de $355.43 MXN y costo propuesto de $466.56 MXN. El cálculo condicionado es `355.43 − 466.56 = −111.13 MXN`.

Es un **caso candidato**, sujeto a confirmar qué representan el monto, los comprobantes y el costo. No demuestra que todo el producto o toda la tienda tengan margen acumulado negativo.

Para calcularlo se necesitan ventas, cantidades, tienda, producto, fecha y costo aplicable. Si el costo cambia, se debe usar el correspondiente a la fecha de la operación bajo la regla adoptada. No se usa automáticamente el costo actual para todas las ventas históricas. Si falta un costo, el margen queda pendiente de cálculo; reemplazarlo por cero produciría un margen engañoso.

## Fechas: qué significan «últimos seis meses», «último trimestre» y «último año»

La **fecha de corte** es el límite hasta el cual se analiza. No tiene que coincidir con el día en que ejecutas el programa: debe respetar la cobertura de los datos.

Por ejemplo, **si se adoptara** el 31 de marzo de 2026 como corte y se eligieran períodos completos:

| Solicitud | Ventana ilustrativa, con ambos extremos incluidos |
|---|---|
| Últimos seis meses completos | 1 de octubre de 2025 a 31 de marzo de 2026 |
| Último trimestre calendario completo | 1 de enero a 31 de marzo de 2026 |
| Últimos doce meses completos | 1 de abril de 2025 a 31 de marzo de 2026 |
| Mes adicional necesario para el primer MoM | Marzo de 2025 |

El trimestre calendario divide el año en enero–marzo, abril–junio, julio–septiembre y octubre–diciembre. Tres meses móviles se cuentan hacia atrás desde el corte y pueden no coincidir con esos bloques. «Último año» también podría significar el año calendario anterior; aquí se ilustra como doce meses completos hacia atrás.

Estas ventanas son ejemplos, no decisiones confirmadas del proyecto. La cobertura conjunta de las fuentes y la elección definitiva siguen pendientes en [D005](DUDAS.md#d005-fecha-de-corte-de-las-ventanas-del-reto).

## Qué debes dejar definido antes de producir los resultados

| Pregunta | Decisión necesaria |
|---|---|
| Rotación | En unidades o en valor; tiendas y canales incluidos; promedio de inventario; tratamiento de faltantes y empates. |
| Quiebres | Qué stock cuenta como agotado; continuidad de días; surtido por tienda; episodios que cruzan el corte. |
| MoM | Qué importe cuenta como venta; moneda común; meses completos; tratamiento de bases cero y datos faltantes. |
| Margen negativo | Costo y vigencia; bases comparables; período; operación individual o acumulado por producto y tienda. |

En las cuatro preguntas también hay que unificar los identificadores de producto y definir qué operaciones se incluyen como ventas y cómo afectan las devoluciones. Las interpretaciones abiertas de las fuentes están en [DUDAS.md](DUDAS.md); el vocabulario general está en [DEFINICIONES.md](DEFINICIONES.md).

## Conclusión

Interpreto las cuatro preguntas mediante métricas, ventanas y poblaciones explícitas. Antes de calcularlas, debo asegurar que ventas, inventario y costos sean comparables y distinguir los ejemplos explicativos de los resultados reales.
