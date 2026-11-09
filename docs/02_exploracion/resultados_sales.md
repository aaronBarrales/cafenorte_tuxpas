# Resultados del análisis exploratorio aislado de sales.csv

Fecha de documentación y verificación: 8 de noviembre de 2026.

## Alcance y fuente de evidencia

**Este análisis se realizó de forma aislada sobre `datos/sales.csv`, sin tomar en cuenta el contenido de los otros archivos de datos.** No se realizaron cruces con `inventory.json`, `ecommerce_orders.parquet` ni `exchange_rates.csv`. Los resultados describen únicamente la extracción de ventas físicas y no validan su correspondencia con catálogo, inventario, costos, pedidos online o tipos de cambio.

Código de referencia: [01_sales.ipynb](../../notebooks/01_sales.ipynb). Las tablas siguientes se obtuvieron de la ejecución de sus celdas sobre la fuente identificada abajo. Los nombres de los campos y los patrones observados no sustituyen un diccionario confirmado del POS.

| Identificación | Resultado |
|---|---|
| Archivo | `datos/sales.csv` |
| Tamaño | 4,904,088 bytes |
| SHA-256 | `1a456213c5590cf8c8d93438caf52c872ba4abd64a1b7003c74cc43acec8d01b` |
| Registros | 86,490 |
| Columnas | 8 |
| Fecha mínima interpretada | 2024-10-01 07:04:00 |
| Fecha máxima interpretada | 2026-03-31 21:08:00 |
| Formato de fecha utilizado | `DD/MM/YYYY HH:MM` |
| Fuente modificada durante la exploración | No |

**Por qué importa:** tamaño y huella identifican qué versión respaldó estas cifras. Si cambia el CSV, se debe volver a ejecutar y actualizar el informe. El hash no demuestra que los movimientos sean verdaderos o completos.

## 1. Estructura y granularidad observada

Cada fila contiene un identificador de registro, fecha/hora, tienda, SKU POS, cantidad, monto, moneda y comprobante. `venta_id` es único en la extracción, pero eso no confirma que cada fila represente un ticket completo ni que identifique de la misma forma las operaciones en el sistema origen.

| Columna | Tipo leído | Nulos | Valores distintos |
| --- | --- | --- | --- |
| venta_id | object | 0 | 86,490 |
| fecha_hora | object | 0 | 77,844 |
| tienda_id | object | 0 | 40 |
| sku | object | 0 | 70 |
| cantidad | int64 | 0 | 16 |
| monto | float64 | 0 | 45,514 |
| moneda | object | 0 | 1 |
| tipo_comprobante | object | 0 | 5 |

**Qué nos dice:** hay 40 tiendas y 70 códigos POS distintos; los 86,490 identificadores no se repiten. Existen 77,844 textos de fecha/hora distintos: varias operaciones pueden compartir minuto. El campo de fecha entra como texto y se convierte en una columna derivada; los tipos de lectura no equivalen al significado del campo.

**Por qué importa:** establece qué podemos contar y agrupar. La cantidad de filas se informa como registros, sin presentarla como cantidad de clientes o tickets. Los SKU y tiendas solo están identificados dentro de esta fuente; no se verificó su existencia en otros archivos.

### 1.1. Validación de coincidencias: tienda, fecha/hora y producto

**Hipótesis:** una compra con varios productos podría exportarse en varias filas, cada una con un `venta_id` distinto. Es una posibilidad compatible con la estructura, no una conclusión confirmada.

Se comprobó si hay varias filas en la misma tienda y fecha/hora interpretada, y si contienen SKU diferentes. La fuente tiene precisión de minutos. Adicionalmente se exigió la misma moneda y comprobante para identificar un subconjunto de coincidencias más restrictivo.

| Control | Resultado |
| --- | --- |
| venta_id_con_varias_filas | 0 |
| grupos_tienda_fecha_con_varias_filas | 201 |
| filas_en_coincidencias_tienda_fecha | 402 |
| grupos_tienda_fecha_con_varios_sku | 201 |
| filas_en_grupos_tienda_fecha_multisku | 402 |
| grupos_multisku_misma_moneda_y_comprobante | 186 |
| filas_en_grupos_multisku_misma_moneda_y_comprobante | 372 |
| filas_excluidas_por_tienda_o_fecha_ausente | 0 |

**Qué nos dice:** sí hay 201 grupos tienda–fecha/hora con productos diferentes (402 filas). De ellos pueden derivarse 186 grupos con moneda y comprobante iguales, que reúnen 372 filas. Son conteos de coincidencias bajo dos agrupaciones distintas; no representan compras confirmadas y un grupo temporal puede dividirse en varios grupos al exigir comprobante y moneda.

Ejemplos de las filas de los grupos más numerosos con igual tienda, fecha/hora, moneda y comprobante (hasta doce filas; el notebook muestra hasta cinco grupos completos):

| tienda_id | fecha_hora | venta_id | sku | cantidad | monto | moneda | tipo_comprobante |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T001 | 04/01/2025 12:17 | V00015071 | CN-00021 | 1.00 | 26.54 | MXN | I |
| T001 | 04/01/2025 12:17 | V00015073 | CN-00048 | 3.00 | 72.07 | MXN | I |
| T001 | 20/07/2025 13:59 | V00046307 | CN-00023 | 1.00 | 154.24 | MXN | I |
| T001 | 20/07/2025 13:59 | V00046331 | CN-00058 | 1.00 | 77.75 | MXN | I |
| T001 | 08/09/2025 15:39 | V00054285 | CN-00031 | 1.00 | 555.49 | MXN | I |
| T001 | 08/09/2025 15:39 | V00054313 | CN-00045 | 1.00 | 96.99 | MXN | I |
| T001 | 20/12/2025 07:48 | V00070557 | CN-00013 | 1.00 | 206.49 | MXN | I |
| T001 | 20/12/2025 07:48 | V00070556 | CN-00017 | 1.00 | 168.98 | MXN | I |
| T001 | 25/01/2026 08:07 | V00076329 | CN-00017 | 1.00 | 162.10 | MXN | I |
| T001 | 25/01/2026 08:07 | V00076280 | CN-00038 | 2.00 | 693.50 | MXN | I |

**Por qué importa:** estas coincidencias justifican preguntar por la granularidad antes de calcular número de tickets, artículos por compra o ticket promedio. En los datos observados no hay `venta_id` compartidos entre filas, por lo que esa clave no permite reunir estas coincidencias como una misma compra.

**Límite de la comprobación:** no identifica al cliente ni demuestra un ticket común. Distintos clientes o cajas pueden registrar compras en el mismo minuto; una misma compra también puede abarcar varios minutos. No se construyó una clave de ticket con tienda y hora, no se fusionaron movimientos y no se eliminaron filas. Se necesita confirmar el significado de `venta_id` y disponer de `ticket_id`, identificador de línea y, si aplica, caja/terminal y marca temporal con mayor precisión. Véase [Q11 y su evidencia](../03_negocio/PREGUNTAS_CLIENTE.md#evidencia-del-eda-aislado-para-q11).

## 2. Calidad estructural y numérica

| Control | Resultado | Interpretación |
|---|---|---|
| Nulos reconocidos por pandas | 0 en todas las columnas | No hay campos ausentes bajo esta lectura. |
| Textos vacíos o compuestos por espacios | 0 | No se detectan vacíos ocultos por este patrón. |
| Espacios en extremos | 0 | No hay diferencias por espacios iniciales o finales. |
| Duplicados exactos adicionales | 0 | No se repite una fila completa. |
| Repeticiones adicionales de venta_id | 0 | La clave es única en la extracción. |
| Fechas sin interpretar | 0 | Todas admiten el formato elegido. |
| Cantidades o montos cero o negativos | 0 | Los signos originales no distinguen ajustes de ingresos. |
| Cantidades o montos no numéricos, nulos o infinitos | 0 | Los campos admiten operaciones aritméticas en esta versión. |
| Cantidades finitas no enteras | 0 | Todas las cantidades registradas son enteras. |
| Identificadores fuera de los patrones observados | 0 | Cumplen V + 8 dígitos, T + 3 dígitos y CN- + 5 dígitos. |
| Monedas fuera de MXN | 0 | Solo se registra MXN en esta extracción. |
| Comprobantes fuera de I/E/N/P/T | 0 | No aparecen otras claves en la muestra. |

**Qué nos dice:** el archivo tiene buena consistencia estructural bajo estos controles. No necesita reemplazar valores ausentes para poder explorar sus campos numéricos actuales.

**Por qué importa:** disminuye el riesgo de errores de lectura y duplicación al agregar. **No demuestra exactitud comercial:** puede haber operaciones faltantes, cantidades incorrectas o códigos inexistentes que cumplan todos los patrones. Tampoco se evaluó aquí la validez fiscal de los comprobantes.

## 3. Cobertura temporal y por tienda

Hay registros en los 18 meses de octubre de 2024 a marzo de 2026. Cada mes contiene las 40 tiendas y los 70 SKU observados, pero esto no significa que todos los productos aparezcan en todas las tiendas ni que cada día esté completo.

El intervalo contiene 547 días calendario: 40 tiendas × 547 días = 21,880 combinaciones teóricas tienda–día. De ellas, **476 no tienen registros** (aproximadamente 2.18%). Cada tienda tiene entre 7 y 19 días sin registros. T035 tiene 19, T034 tiene 18 y T025 tiene 17.

<details>
<summary>Ver cobertura diaria de las 40 tiendas</summary>

| Tienda | Días con registros | Días sin registros |
| --- | --- | --- |
| T035 | 528 | 19 |
| T034 | 529 | 18 |
| T025 | 530 | 17 |
| T011 | 531 | 16 |
| T014 | 531 | 16 |
| T026 | 531 | 16 |
| T033 | 531 | 16 |
| T002 | 532 | 15 |
| T015 | 532 | 15 |
| T024 | 532 | 15 |
| T009 | 533 | 14 |
| T016 | 533 | 14 |
| T021 | 533 | 14 |
| T030 | 533 | 14 |
| T004 | 534 | 13 |
| T008 | 534 | 13 |
| T013 | 534 | 13 |
| T003 | 535 | 12 |
| T031 | 535 | 12 |
| T001 | 536 | 11 |
| T007 | 536 | 11 |
| T012 | 536 | 11 |
| T019 | 536 | 11 |
| T023 | 536 | 11 |
| T028 | 536 | 11 |
| T029 | 536 | 11 |
| T020 | 537 | 10 |
| T039 | 537 | 10 |
| T010 | 538 | 9 |
| T018 | 538 | 9 |
| T036 | 538 | 9 |
| T038 | 538 | 9 |
| T005 | 539 | 8 |
| T006 | 539 | 8 |
| T022 | 539 | 8 |
| T027 | 539 | 8 |
| T040 | 539 | 8 |
| T017 | 540 | 7 |
| T032 | 540 | 7 |
| T037 | 540 | 7 |

</details>

**Qué nos dice:** una cobertura mensual aparentemente continua puede esconder ausencias de actividad por tienda y día.

**Por qué importa:** una ausencia puede relacionarse con cierres, días sin operaciones o problemas de extracción; la fuente aislada no permite decidir cuál. No se rellenaron esas ausencias como ventas cero y no se dispone de calendario operativo para validar completitud. Las fechas carecen de zona horaria confirmada.

## 4. Distribución de cantidades e importes

Las estadísticas siguientes incluyen todos los comprobantes. Se muestran dos decimales en valores no enteros; son estadísticas descriptivas, no un cálculo contable.

| Estadística | Cantidad | Monto MXN |
| --- | --- | --- |
| count | 86,490 | 86,490 |
| mean | 1.54 | 357.81 |
| std | 1.18 | 447.93 |
| min | 1 | 15.67 |
| 1% | 1 | 16.98 |
| 25% | 1 | 103.00 |
| 50% | 1 | 225.40 |
| 75% | 2 | 433.66 |
| 99% | 6 | 2,322.46 |
| max | 16 | 9,714.87 |

**Qué nos dice:** la mediana es una unidad y 225.40 MXN por registro; el promedio de monto es 357.81 MXN, mayor que la mediana. Hay una distribución con importes altos que elevan el promedio. El monto máximo es 9,714.87 MXN y la cantidad máxima es 16.

**Por qué importa:** media y mediana cuentan aspectos diferentes del archivo. El monto por fila depende del producto y la cantidad: un valor alto no demuestra un error, y estas estadísticas no equivalen a ticket promedio confirmado. La unidad de medida y la base del monto siguen pendientes.

## 5. Moneda y tipo de comprobante

| Moneda | Comprobante | Registros | Unidades registradas | Importe registrado MXN |
| --- | --- | --- | --- | --- |
| MXN | E | 3,079 | 4,843 | 1,140,985.33 |
| MXN | I | 82,518 | 127,241 | 29,503,069.84 |
| MXN | N | 288 | 407 | 100,579.56 |
| MXN | P | 451 | 692 | 160,501.27 |
| MXN | T | 154 | 200 | 42,117.82 |

La suma aritmética de todos los montos originales es **30,947,253.82 MXN**. Se usa exclusivamente como control de conservación: **no se presenta como ventas netas**. Los comprobantes I suman 29,503,069.84 MXN y 127,241 unidades registradas.

**Qué nos dice:** todos los tipos contienen cantidades e importes positivos, incluido E. El signo de la columna no revela por sí solo si una operación aumenta o disminuye ingresos.

**Por qué importa:** debemos definir el tratamiento de cada comprobante antes de producir métricas. Las letras sugieren tipos de CFDI, pero su significado en el POS es una hipótesis pendiente. No se descontaron E automáticamente ni se sumaron pagos como ingresos confirmados. El análisis usa moneda MXN sin conversiones porque esta fuente no contiene otras monedas.

## 6. Concentración por tienda y producto

Para este diagnóstico se seleccionaron únicamente registros I con cantidad positiva y monto conocido. Todas las cifras abarcan la cobertura completa del CSV; no son un ranking de margen o rotación.

### Diez tiendas con mayor importe I

| Tienda | Importe I MXN | Participación % |
| --- | --- | --- |
| T037 | 812,902.26 | 2.76 |
| T017 | 804,949.45 | 2.73 |
| T035 | 792,192.31 | 2.69 |
| T023 | 779,666.87 | 2.64 |
| T001 | 766,100.54 | 2.60 |
| T016 | 762,374.23 | 2.58 |
| T039 | 761,487.69 | 2.58 |
| T003 | 760,317.08 | 2.58 |
| T027 | 758,138.05 | 2.57 |
| T022 | 756,548.33 | 2.56 |

Las diez primeras concentran **26.28%** del importe I. T037 tiene el mayor importe, con **812,902.26 MXN**. La participación usa como base el importe I de las 40 tiendas.

**Qué nos dice:** permite ubicar dónde se concentra el importe registrado; las diez primeras suman aproximadamente una cuarta parte del total I.

**Por qué importa:** orienta revisiones y permite comprobar que los resúmenes conserven el total de origen. No mide eficiencia: faltan contexto de tamaño, horarios, costos y objetivos por tienda.

### Diez SKU con mayor importe I

| SKU POS | Registros I | Unidades I | Importe I MXN |
| --- | --- | --- | --- |
| CN-00039 | 1,203 | 1,862 | 1,481,814.86 |
| CN-00004 | 1,175 | 1,882 | 1,295,156.69 |
| CN-00009 | 1,219 | 1,833 | 1,131,836.43 |
| CN-00055 | 1,174 | 1,773 | 1,112,110.68 |
| CN-00020 | 1,169 | 1,761 | 1,056,721.58 |
| CN-00029 | 1,129 | 1,670 | 1,041,275.54 |
| CN-00046 | 1,212 | 1,918 | 1,020,981.74 |
| CN-00031 | 1,155 | 1,833 | 990,126.57 |
| CN-00051 | 1,161 | 1,843 | 891,625.10 |
| CN-00047 | 1,194 | 1,793 | 888,284.87 |

**Qué nos dice:** muestra qué códigos POS acumulan más importe y permite distinguir unidades de valor monetario.

**Por qué importa:** los productos con mayor importe no necesariamente venden más unidades ni rotan más rápido. No se asignaron nombres, categorías, costos o claves ERP, ya que eso requeriría consultar otras fuentes. Los resúmenes completos del notebook mantienen separación por moneda y comprobante; estas tablas muestran el subconjunto I de MXN.

## 7. Evolución mensual

La siguiente tabla muestra registros, unidades e importes I por mes; no aplica ajustes de otros comprobantes ni constituye el crecimiento mensual definitivo solicitado en el reto.

| Mes | Registros I | Unidades I | Importe I MXN |
| --- | --- | --- | --- |
| 2024-10 | 4,621 | 6,921 | 1,636,016.67 |
| 2024-11 | 4,677 | 7,337 | 1,717,735.60 |
| 2024-12 | 4,665 | 7,109 | 1,621,347.27 |
| 2025-01 | 4,681 | 7,170 | 1,651,207.03 |
| 2025-02 | 4,213 | 6,426 | 1,487,252.95 |
| 2025-03 | 4,563 | 7,227 | 1,649,055.66 |
| 2025-04 | 4,529 | 6,851 | 1,594,506.88 |
| 2025-05 | 4,626 | 7,174 | 1,708,351.71 |
| 2025-06 | 4,577 | 6,989 | 1,639,309.10 |
| 2025-07 | 4,774 | 7,340 | 1,704,654.40 |
| 2025-08 | 4,799 | 7,471 | 1,703,266.74 |
| 2025-09 | 4,505 | 6,978 | 1,611,576.62 |
| 2025-10 | 4,686 | 7,267 | 1,723,372.26 |
| 2025-11 | 4,508 | 6,852 | 1,607,278.43 |
| 2025-12 | 4,678 | 7,404 | 1,705,453.24 |
| 2026-01 | 4,629 | 7,041 | 1,620,102.45 |
| 2026-02 | 4,216 | 6,557 | 1,497,393.29 |
| 2026-03 | 4,571 | 7,127 | 1,625,189.54 |

El mes de mayor importe I es **2025-10**, con **1,723,372.26 MXN**. El menor es **2025-02**, con **1,487,252.95 MXN**.

**Qué nos dice:** hay variaciones mensuales de actividad aun cuando todos los meses tienen registros. El notebook también contiene las series separadas de los otros comprobantes.

**Por qué importa:** proporciona la base temporal para investigar cambios y después definir el crecimiento por canal. Dieciocho meses de datos no bastan para atribuir los cambios a estacionalidad, promociones o desempeño; los meses tienen diferente número de días y falta confirmar completitud operativa. No se mezcló información de e-commerce para esta lectura.

## 8. Importe efectivo unitario y valores atípicos

Se calculó `monto / cantidad` sobre registros I elegibles, agrupando por moneda y SKU. Esta razón solo equivale a importe efectivo unitario si monto representa el total de línea y cantidad está expresada en una unidad consistente. No es una reconstrucción del precio de lista.

La regla de revisión usa Q1 y Q3 de pandas con su interpolación predeterminada, `IQR = Q3 − Q1` y límites `Q1 − 1.5 × IQR` y `Q3 + 1.5 × IQR`. Se exige al menos cuatro observaciones y dispersión positiva por grupo.

| Resultado IQR | Filas |
|---|---:|
| Evaluadas | 82,518 |
| Sin evaluación dentro del subconjunto elegible | 0 |
| Señaladas como atípicas | 0 |

**Qué nos dice:** no se detectaron extremos con esta regla dentro de cada producto y moneda. No se compararon como si fueran equivalentes los importes de productos diferentes.

**Por qué importa:** permite investigar valores inusuales sin borrar operaciones. La ausencia de alertas no valida tarifas ni descuentos y puede coexistir con errores sistemáticos. Este análisis no afirma resultados IQR sobre comprobantes distintos de I.

## 9. Lectura de las gráficas del notebook

| Gráfica | Qué muestra | Por qué importa y qué no concluye |
|---|---|---|
| Importe mensual I, MXN | Evolución de los importes del subconjunto I | Facilita detectar cambios; no demuestra causas ni representa ingresos netos confirmados. |
| Diez tiendas con mayor importe I, MXN | Concentración acumulada en toda la ventana | Facilita comparar magnitudes; no representa margen, rotación ni eficiencia. |

Las gráficas están integradas como SVG en el notebook. La línea interrumpe la continuidad ante meses con importes desconocidos; no convierte una ausencia en cero. Las tablas de este informe permiten consultar sus cifras directamente en GitHub.

## 10. Conclusiones y límites para continuar

1. La fuente puede explorarse sin corregir nulos, duplicados o números inválidos bajo los controles actuales. Esto respalda su lectura técnica, no su exactitud comercial.
2. Hay cobertura de 18 meses, 40 tiendas y 70 SKU, con 476 combinaciones tienda–día sin registros que deben conservarse como ausencia de evidencia.
3. La principal decisión pendiente para agregar ventas es el significado de comprobantes y monto. Los importes originales positivos no resuelven esa decisión.
4. La distribución por tienda, SKU y mes permite conocer la actividad registrada, pero no permite calcular rentabilidad ni rotación sin otros datos.
5. No se detectaron atípicos con la regla IQR elegida; no hay base para concluir que los precios sean correctos.

| Pendiente | Motivo |
|---|---|
| Definir granularidad y alcance de venta_id | Evitar confundir registros con tickets o líneas. |
| Confirmar comprobantes, impuestos, descuentos y significado de monto | Definir ingresos sobre una base coherente. |
| Confirmar unidad de cantidad y zona horaria | Evitar agregaciones incompatibles o desplazamientos de fecha. |
| Revisar días sin registros con calendario operativo | Distinguir ausencia de extracción de ausencia de operaciones. |
| Conciliar tiendas y productos en una etapa posterior | Validar existencia y cobertura fuera de la fuente aislada. |

**No se calcularon con esta exploración aislada:** rotación, episodios de stock cero, margen por tienda, conciliación POS–ERP–Shopify ni crecimiento comparativo entre canales. El notebook tampoco confirma causas de variaciones de importe, cancelaciones o devoluciones.

## Conclusión

Encuentro una fuente estructuralmente consistente bajo los controles aplicados, con 40 tiendas, 70 SKU y 18 meses de registros. Mantengo pendientes la interpretación de comprobantes y montos, las ausencias por tienda y día y la granularidad del ticket; las coincidencias temporales y la ausencia de alertas IQR no resuelven esas dudas. Este análisis aislado no permite concluir sobre inventario, margen o consistencia entre canales.
