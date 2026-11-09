# Resultados del análisis exploratorio aislado de inventory.json

Fecha de documentación: 9 de noviembre de 2026.

## Alcance y fuente de evidencia

Analizo exclusivamente `datos/inventory.json`, sin leer ni cruzar `sales.csv`, `ecommerce_orders.parquet` o `exchange_rates.csv`. Las uniones entre tiendas, productos, costos, equivalencias y snapshots son controles internos del mismo JSON; no demuestran compatibilidad entre sistemas. Conservo los originales, los nulos literales y el texto `N/A`, y separo columnas derivadas.

Mi código y las salidas calculadas están en [03_inventory.ipynb](../../notebooks/03_inventory.ipynb). Los resultados siguientes proceden de sus tablas ejecutadas. Redondeo decimales a un máximo de cuatro posiciones para mostrarlos; no altero los valores originales ni los cálculos. Los campos orientan mi interpretación, pero no sustituyen un diccionario confirmado del ERP.


**Leyenda:** Identifico la extracción exacta; bytes es tamaño físico y metadata es una declaración del archivo, no verificación del ERP. No incluyo el índice de pandas.

| Medida | Resultado |
|---|---|
| Archivo | datos/inventory.json |
| Bytes | 31671112 |
| SHA-256 | 2355c6cab9ff00a707b5505a464a8f7e1a9bf5a2aa6c7a2b6b008f5299c8eada |
| Generado según metadata | 2026-04-23T08:22:39.344087 |
| Sistema declarado | ERP CaféNorte v2.3 (legacy) |
| Descripción declarada | Snapshots diarios de inventario. No incluye movimientos transaccionales. |
| Claves repetidas en objetos JSON | 0 |

La huella coincide con el antecedente de inventario del EDA integral; no detecto cambio de versión respecto de esa evidencia. La fecha de generación carece de zona explícita y no extiende la cobertura de los snapshots. Un hash idéntico no prueba integridad comercial ni fidelidad del ERP.

## 1. Estructura, diccionario y granularidad

Distingo cinco colecciones: tiendas, equivalencias, productos, vigencias de costo y snapshots. Aplano el historial sin perder su SKU padre; la fecha–tienda–SKU ERP es la clave candidata del saldo diario.


**Leyenda:** Reviso todos los registros por bloque y campo; las cuatro últimas columnas cuentan registros afectados. list identifica el historial anidado; costos añade sku_erp como vínculo derivado al padre. No incluyo el índice de pandas.

| Bloque | Campo | Registros | Tipos JSON leídos | Campo ausente | Null literal | Texto vacío | Espacios extremos |
|---|---|---|---|---|---|---|---|
| tiendas | ciudad | 40 | str | 0 | 0 | 0 | 0 |
| tiendas | region | 40 | str | 0 | 0 | 0 | 0 |
| tiendas | tienda_id | 40 | str | 0 | 0 | 0 | 0 |
| tiendas | timezone | 40 | str | 0 | 0 | 0 | 0 |
| mapeos | handle | 65 | NoneType, str | 0 | 38 | 0 | 0 |
| mapeos | sku_erp | 65 | NoneType, str | 0 | 5 | 0 | 0 |
| mapeos | sku_pos | 65 | str | 0 | 0 | 0 | 0 |
| productos | categoria | 70 | str | 0 | 0 | 0 | 0 |
| productos | cost_history | 70 | list | 0 | 0 | 0 | 0 |
| productos | nombre | 70 | str | 0 | 0 | 0 | 0 |
| productos | sku_erp | 70 | str | 0 | 0 | 0 | 0 |
| costos | costo_mxn | 282 | float | 0 | 0 | 0 | 0 |
| costos | fecha_vigencia | 282 | str | 0 | 0 | 0 | 0 |
| costos | proveedor | 282 | str | 0 | 0 | 0 | 0 |
| costos | sku_erp | 282 | str | 0 | 0 | 0 | 0 |
| snapshots | cantidad_en_stock | 230776 | int, str | 0 | 0 | 0 | 0 |
| snapshots | fecha | 230776 | str | 0 | 0 | 0 | 0 |
| snapshots | sku_erp | 230776 | str | 0 | 0 | 0 | 0 |
| snapshots | tienda_id | 230776 | str | 0 | 0 | 0 | 0 |



**Leyenda:** Diccionario de lectura de los campos del JSON; no constituye un contrato de negocio confirmado. No incluyo el índice de pandas.

| Bloque | Campos originales | Interpretación y límite |
|---|---|---|
| metadata | generado, fuente, descripcion | Marca de generación sin zona explícita; sistema y alcance declarados. |
| tiendas_info | tienda_id, ciudad, region, timezone | Identidad y atributos de tienda; timezone no confirma la hora del POS. |
| sku_mappings | sku_pos, sku_erp, handle | Equivalencias declaradas; null no es una clave y no se enlaza con otro null. |
| catalogo.productos | sku_erp, nombre, categoria | Identidad ERP y descripción; un nombre compartido no demuestra mismo producto. |
| cost_history | fecha_vigencia, costo_mxn, proveedor | Historial por producto; MXN según nombre del campo, unidad/base y política pendientes. |
| snapshots | fecha, tienda_id, sku_erp, cantidad_en_stock | Saldo diario observado; no son movimientos. N/A conserva estado desconocido; unidad y momento pendientes. |

**Qué me dice y por qué importa:** puedo separar dimensiones e historiales de los saldos diarios. Un snapshot es una observación, no una entrada o salida de mercancía. El costo pertenece al producto y no tiene tienda; necesito confirmar si esa cobertura global corresponde al negocio. No interpreto el nombre del producto como identidad ni el costo como precio de venta.

## 2. Calidad de claves y existencias

### Columnas que creo para analizar los snapshots

Mantengo `cantidad_en_stock` y `fecha` tal como llegaron en el JSON. Añado las siguientes columnas únicamente en la tabla de trabajo; no las escribo en la fuente.

**Leyenda:** describo las tres columnas derivadas de esta etapa, su campo de origen y su uso. `NaN` representa un valor numérico ausente en pandas y `NaT` una fecha ausente; ninguno equivale a cero. La unidad física de existencias sigue pendiente de confirmar.

| Columna derivada | Campo de origen | Qué significa y cómo la obtengo | Para qué la uso |
|---|---|---|---|
| `stock_num` | `cantidad_en_stock` | Es la versión convertida a número con `pd.to_numeric(..., errors="coerce")`. Conservo los valores interpretables como números; lo que no se puede convertir queda como `NaN`. La conversión por sí sola no certifica que el saldo sea válido. | Calculo estadísticas de saldos conocidos y detecto ceros; consulto `estado_stock` para distinguir el motivo y las características del valor original. |
| `estado_stock` | `cantidad_en_stock` | Es una etiqueta que clasifica el valor original: null literal, N/A, otro no numérico, no finito, booleano, negativo, cero o positivo. | Distingo un saldo desconocido de un cero y cuento cada condición sin perder la evidencia original. |
| `fecha_dt` | `fecha` | Es la fecha interpretada con el formato `AAAA-MM-DD`, mediante `pd.to_datetime(..., errors="coerce")`. Si no se puede interpretar queda como `NaT`; no añado hora de captura ni zona horaria. | Ordeno los snapshots, comparo días y construyo calendarios y rachas consecutivas. |

Por ejemplo, si el saldo original es `31`, obtengo `stock_num = 31` y `estado_stock = "Positivo"`; si es `0`, obtengo `stock_num = 0` y `estado_stock = "Cero"`. Si el original es el texto `"N/A"`, obtengo `stock_num = NaN` y `estado_stock = "N/A"`. Son ejemplos ilustrativos de la conversión, no nuevos resultados calculados ni filas seleccionadas del archivo.

### Significado de las etiquetas de estado_stock

**Leyenda:** explico todas las categorías previstas por el control, aunque alguna no aparezca en esta extracción. Las etiquetas describen el valor de una fila existente, no la ausencia de un snapshot.

| Etiqueta | Cómo interpreto la clasificación |
|---|---|
| `Null literal` | El valor original es `null` en el JSON; no contiene una cantidad informada. |
| `N/A` | El original contiene exactamente el texto `"N/A"`. Mantengo pendiente su significado operativo con Q06 / D009; no lo convierto en cero. |
| `No numérico distinto de N/A` | El original no se puede interpretar como número y no es el texto exacto `"N/A"`. |
| `No finito` | El valor se interpreta como número, pero es infinito o no representa un número finito. |
| `Booleano` | El original es `true` o `false`. Lo separo de las cantidades, aunque Python pueda tratar booleanos como números. |
| `Negativo` | El valor numérico finito es menor que cero. La etiqueta no confirma por sí sola un error del ERP. |
| `Cero` | El valor numérico finito es exactamente cero: existe una fila que informa ese saldo. |
| `Positivo` | El valor numérico finito es mayor que cero. |

Si no existe una fila para cierta fecha, tienda y producto, no hay valor que clasificar: no creo automáticamente un `estado_stock` ni un saldo cero para esa ausencia. Los estados de calidad no equivalen a respuestas del negocio; por ejemplo, un cero diario todavía requiere confirmar momento de captura y definición de disponible antes de interpretarlo como quiebre.



**Leyenda:** Controles sobre la extracción completa; duplicados adicionales excluye la primera aparición de cada clave o fila. No elimino registros ni los declaro errores del ERP por ausencia de un catálogo externo. No incluyo el índice de pandas.

| Medida | Resultado |
|---|---|
| Snapshots | 230776 |
| Duplicados exactos adicionales | 0 |
| Claves tienda–SKU–fecha adicionales | 0 |
| Fechas sin interpretar | 0 |
| Fechas fuera de formato ISO diario | 0 |
| Tiendas duplicadas adicionales | 0 |
| Productos ERP duplicados adicionales | 0 |
| Snapshots con tienda fuera del catálogo interno | 0 |
| Snapshots con SKU fuera del catálogo interno | 0 |
| SKU ERP de mapeos fuera del catálogo interno | 0 |
| Stock numérico finito no entero | 0 |
| Tienda con patrón distinto de T y tres dígitos | 0 |
| ERP con patrón distinto del observado | 0 |
| POS con patrón distinto de CN y cinco dígitos | 0 |



**Leyenda:** Cuento todos los snapshots por estado exclusivo; porcentaje sobre todas las filas, no sobre productos o unidades. Mantengo categorías con cero casos para distinguirlas de controles omitidos. No incluyo el índice de pandas.

| Estado del saldo | Registros | Porcentaje de snapshots |
|---|---|---|
| Null literal | 0 | 0 |
| N/A | 4417 | 1.914 |
| No numérico distinto de N/A | 0 | 0 |
| No finito | 0 | 0 |
| Booleano | 0 | 0 |
| Negativo | 0 | 0 |
| Cero | 11726 | 5.0811 |
| Positivo | 214633 | 93.0049 |

**Qué me dice:** encuentro 230,776 snapshots, sin duplicados de clave ni referencias ajenas al catálogo interno. Los 4,417 textos `N/A` son desconocidos, frente a 11,726 ceros numéricos y 214,633 saldos positivos. No detecto negativos, null literal ni valores numéricos no enteros en esta versión.

**Por qué importa:** convertir `N/A` a cero alteraría inventario promedio y rachas. La ausencia de errores estructurales no demuestra que el saldo sea correcto o completo. Mi decisión de tratamiento es conservar el valor original, añadir estado y saldo numérico derivados y reportar desconocidos sin imputarlos (Q06 / D009).

## 3. Cobertura temporal y surtido observado


**Leyenda:** Cobertura del calendario completo; día-par es una fecha para una tienda y SKU. El escenario cartesiano no es surtido confirmado; no asigno saldo a sus pares ausentes. No incluyo el índice de pandas.

| Medida | Resultado |
|---|---|
| Primera fecha snapshot | 2025-10-01 |
| Última fecha snapshot | 2026-03-31 |
| Días del calendario inclusivo | 182 |
| Fechas distintas observadas | 182 |
| Tiendas observadas | 40 |
| SKU ERP observados | 70 |
| Pares tienda–SKU observados | 1268 |
| Pares con todos los días observados | 1268 |
| Días-par ausentes dentro de pares observados | 0 |
| Pares con al menos un saldo desconocido | 1232 |
| Pares cartesianos de tiendas y catálogo | 2800 |
| Pares cartesianos nunca observados | 1532 |



**Leyenda:** Todas las tiendas, ordenadas por tienda_id; SKU y días son valores distintos, snapshots y saldos son registros. El porcentaje desconocido usa las filas de cada tienda; no presupongo que todas deban vender el catálogo completo. No incluyo el índice de pandas.

| tienda_id | SKU_observados | Dias_observados | Snapshots | Saldos_desconocidos | Ceros_observados | Porcentaje_desconocido |
|---|---|---|---|---|---|---|
| T001 | 40 | 182 | 7280 | 131 | 393 | 1.799 |
| T002 | 26 | 182 | 4732 | 92 | 250 | 1.944 |
| T003 | 34 | 182 | 6188 | 117 | 319 | 1.891 |
| T004 | 38 | 182 | 6916 | 119 | 348 | 1.721 |
| T005 | 36 | 182 | 6552 | 116 | 343 | 1.77 |
| T006 | 40 | 182 | 7280 | 150 | 400 | 2.06 |
| T007 | 28 | 182 | 5096 | 100 | 228 | 1.962 |
| T008 | 25 | 182 | 4550 | 105 | 220 | 2.308 |
| T009 | 31 | 182 | 5642 | 108 | 287 | 1.914 |
| T010 | 30 | 182 | 5460 | 125 | 264 | 2.289 |
| T011 | 27 | 182 | 4914 | 88 | 257 | 1.791 |
| T012 | 35 | 182 | 6370 | 143 | 337 | 2.245 |
| T013 | 26 | 182 | 4732 | 86 | 247 | 1.817 |
| T014 | 34 | 182 | 6188 | 118 | 307 | 1.907 |
| T015 | 35 | 182 | 6370 | 115 | 277 | 1.805 |
| T016 | 29 | 182 | 5278 | 119 | 266 | 2.255 |
| T017 | 30 | 182 | 5460 | 85 | 275 | 1.557 |
| T018 | 26 | 182 | 4732 | 101 | 237 | 2.134 |
| T019 | 37 | 182 | 6734 | 134 | 357 | 1.99 |
| T020 | 26 | 182 | 4732 | 105 | 238 | 2.219 |
| T021 | 37 | 182 | 6734 | 120 | 312 | 1.782 |
| T022 | 27 | 182 | 4914 | 117 | 240 | 2.381 |
| T023 | 34 | 182 | 6188 | 128 | 319 | 2.069 |
| T024 | 28 | 182 | 5096 | 85 | 248 | 1.668 |
| T025 | 40 | 182 | 7280 | 139 | 385 | 1.909 |
| T026 | 28 | 182 | 5096 | 88 | 251 | 1.727 |
| T027 | 28 | 182 | 5096 | 94 | 284 | 1.845 |
| T028 | 25 | 182 | 4550 | 92 | 222 | 2.022 |
| T029 | 31 | 182 | 5642 | 82 | 298 | 1.453 |
| T030 | 28 | 182 | 5096 | 113 | 279 | 2.217 |
| T031 | 27 | 182 | 4914 | 79 | 264 | 1.608 |
| T032 | 36 | 182 | 6552 | 104 | 310 | 1.587 |
| T033 | 39 | 182 | 7098 | 146 | 335 | 2.057 |
| T034 | 31 | 182 | 5642 | 95 | 308 | 1.684 |
| T035 | 39 | 182 | 7098 | 129 | 357 | 1.817 |
| T036 | 36 | 182 | 6552 | 132 | 340 | 2.015 |
| T037 | 30 | 182 | 5460 | 96 | 292 | 1.758 |
| T038 | 28 | 182 | 5096 | 91 | 259 | 1.786 |
| T039 | 27 | 182 | 4914 | 113 | 230 | 2.3 |
| T040 | 36 | 182 | 6552 | 117 | 343 | 1.786 |



**Leyenda:** Todos los meses observados en orden cronológico; desconocidos y ceros cuentan filas, no días completos ni unidades. El denominador porcentual son snapshots de cada mes. No incluyo el índice de pandas.

| mes | Dias | Snapshots | Desconocidos | Ceros | Porcentaje_desconocido |
|---|---|---|---|---|---|
| 2025-10 | 31 | 39308 | 743 | 2022 | 1.89 |
| 2025-11 | 30 | 38040 | 753 | 1912 | 1.979 |
| 2025-12 | 31 | 39308 | 763 | 2023 | 1.941 |
| 2026-01 | 31 | 39308 | 745 | 1993 | 1.895 |
| 2026-02 | 28 | 35504 | 662 | 1824 | 1.865 |
| 2026-03 | 31 | 39308 | 751 | 1952 | 1.911 |



**Leyenda:** Agrupo el catálogo interno de tiendas por región y zona declarada; no interpreto fechas diarias como instantes ni valido la zona del POS. No incluyo el índice de pandas.

| region | timezone | Tiendas |
|---|---|---|
| centro | America/Chihuahua | 3 |
| centro | America/Mexico_City | 15 |
| centro | America/Monterrey | 3 |
| frontera | America/Matamoros | 4 |
| frontera | America/Ojinaga | 2 |
| frontera | America/Tijuana | 4 |
| noroeste | America/Hermosillo | 3 |
| sureste | America/Cancun | 3 |
| sureste | America/Merida | 3 |

**Qué me dice:** tengo 1,268 pares observados y cada uno aparece en los 182 días inclusivos entre 2025-10-01 y 2026-03-31. Sin embargo, 1,232 pares contienen al menos un saldo desconocido. Cada tienda muestra entre 25 y 40 SKU.

**Por qué importa:** las filas cubren todo el calendario de los pares observados, pero no todos sus saldos son utilizables. El escenario cartesiano contiene 1,532 pares nunca observados y no equivale al surtido autorizado. No les asigno cero ni declaro fallos de extracción sin evidencia (Q07/Q28/Q29 / D010/D021).

**Límites:** no he comprobado ventas sin inventario ni cobertura por canal. El catálogo timezone es una declaración por tienda; no prueba zona del POS ni hora de corte del saldo. Para rotación tendré que alinear población, fechas y unidades con ventas después de su conciliación.

## 4. Distribución de saldos

Mi objetivo aquí es responder: **¿qué cantidades de inventario aparecen habitualmente en los snapshots y cuánto varían?** Para eso reviso los valores de `stock_num` de todos los productos, tiendas y días del archivo.

Cada observación es **el saldo de un producto en una tienda para un día**. Si ese mismo producto y tienda aparecen en varias fechas, cada fecha aporta una observación. Incluyo los saldos cero porque son cantidades informadas; excluyo los `N/A` porque su cantidad es desconocida.

### Qué hago en el código

1. **Resumo todos los saldos conocidos.** Con `describe(...)` calculo cuántas observaciones tienen número, su promedio, dispersión, percentiles y extremos. Estos resultados aparecen en la primera tabla.
2. **Repito parte del resumen por categoría.** Con `merge(...)` añado a cada snapshot la categoría de su producto, usando el SKU ERP del catálogo de este mismo JSON. Después agrupo por categoría para contar productos y registros y describir sus saldos.
3. **Busco dónde aparece el saldo más alto.** Selecciono las filas cuyo saldo coincide con el máximo global para identificar fecha, tienda y producto. Si hay varios empates, muestro hasta diez, ordenados por fecha, tienda y SKU.

### Cómo leo la primera tabla

**Leyenda:** explico las medidas de la tabla de saldos conocidos que aparece después del código. Las observaciones cuentan registros; las demás medidas describen cantidades de stock, cuya unidad física todavía necesito confirmar. Esta tabla explica conceptos y no añade nuevos resultados.

| Medida | Qué significa |
|---|---|
| Observaciones | Cantidad de snapshots que tienen un saldo numérico conocido. No es cantidad de productos ni suma de existencias. |
| Media | Promedio de los saldos conocidos: sumo sus valores y divido entre la cantidad de observaciones. Cada snapshot tiene el mismo peso. |
| Desviación estándar | Mide cuánto se dispersan los saldos alrededor de la media. Un valor mayor indica más dispersión; no significa que todos los saldos estén a esa distancia de la media. |
| Mínimo | Menor saldo conocido que aparece en el archivo. |
| Percentil 25 | Valor que deja aproximadamente el 25 % de los saldos en él o por debajo, después de ordenarlos de menor a mayor. |
| Mediana | Valor central de los saldos ordenados; corresponde al percentil 50. |
| Percentil 75 | Valor que deja aproximadamente el 75 % de los saldos en él o por debajo. |
| Percentil 95 | Valor que deja aproximadamente el 95 % de los saldos en él o por debajo. Me ayuda a reconocer niveles altos dentro del archivo. |
| Percentil 99 | Valor que deja aproximadamente el 99 % de los saldos en él o por debajo. Describe la parte más alta de la distribución. |
| Máximo | Mayor saldo conocido que aparece en el archivo. |

Para entender los percentiles, imagino todos los saldos **ordenados de menor a mayor** y ubico el punto que corresponde al porcentaje indicado. Los porcentajes se refieren a observaciones del saldo, no a productos, tiendas o unidades vendidas.

### Cómo leo las otras dos tablas

En la tabla por categoría, `Productos` cuenta SKU ERP distintos y `Snapshots` cuenta filas. `Saldos_conocidos` cuenta filas con cantidad numérica, `Saldos_desconocidos` cuenta filas sin cantidad interpretable y `Ceros` cuenta filas que informan cero. `Mediana_saldo` y `Maximo_saldo` describen únicamente los saldos conocidos de esa categoría. Un producto puede aportar muchas filas porque aparece en varias tiendas y fechas.

La última tabla localiza el máximo: `fecha` indica el día observado, `tienda_id` la tienda, `sku_erp` el producto y `cantidad_en_stock` el saldo original. Encontrar el máximo me permite revisar un caso extremo; no demuestra un error de captura.

### Para qué me sirve y qué no puedo concluir todavía

Uso estas tablas para conocer los niveles habituales y extremos del archivo y ver diferencias entre categorías. Para decidir si hay poco o demasiado inventario necesito además demanda, presentación y unidad de medida, entre otros criterios del negocio (Q16/Q21 / D016). No aplico un único límite de error a todos los productos.

**Este resumen no representa el inventario total disponible en un momento.** Por ejemplo, si ayer un producto tenía diez unidades en una tienda y hoy tiene doce, son dos observaciones de su saldo. Sumarlas como veintidós unidades disponibles contaría existencias de momentos diferentes. Este ejemplo es ilustrativo, no una selección de filas del archivo. Tampoco interpreto la diferencia entre dos saldos como ventas: podrían intervenir compras, devoluciones u otros movimientos que este JSON no contiene.



**Leyenda:** Todos los saldos numéricos conocidos: Observaciones cuenta snapshots; la media no se pondera, la desviación es muestral y los percentiles describen la posición del saldo en la distribución. La unidad física del saldo queda pendiente de confirmar. No incluyo el índice de pandas.

| Estadístico | Saldo observado |
|---|---|
| Observaciones | 226,359 |
| Media | 39.8177 |
| Desviación estándar | 26.0387 |
| Mínimo | 0 |
| Percentil 25 | 18 |
| Mediana | 37 |
| Percentil 75 | 58 |
| Percentil 95 | 86 |
| Percentil 99 | 104 |
| Máximo | 153 |



**Leyenda:** Todas las categorías del catálogo vinculadas internamente por ERP; mediana y máximo usan solo saldos conocidos. Productos cuenta SKU distintos, el resto de conteos son filas; no comparo unidades económicas entre categorías. No incluyo el índice de pandas.

| categoria | Productos | Snapshots | Saldos_conocidos | Saldos_desconocidos | Ceros | Mediana_saldo | Maximo_saldo |
|---|---|---|---|---|---|---|---|
| bebidas | 8 | 29848 | 29278 | 570 | 1532 | 37 | 153 |
| cafe_grano | 12 | 38038 | 37281 | 757 | 1911 | 38 | 143 |
| cafe_molido | 17 | 55692 | 54658 | 1034 | 2822 | 37 | 146 |
| comida_caliente | 11 | 34580 | 33918 | 662 | 1747 | 37 | 142 |
| mercancia | 15 | 49140 | 48202 | 938 | 2481 | 37 | 146 |
| panaderia | 7 | 23478 | 23022 | 456 | 1233 | 37 | 138 |



**Leyenda:** Hasta diez snapshots empatados en el máximo global numérico; ordeno fecha, tienda y SKU de forma ascendente y conservo todos los empates si no superan diez. Un máximo es una señal descriptiva, no un error confirmado. No incluyo el índice de pandas.

| fecha | tienda_id | sku_erp | cantidad_en_stock |
|---|---|---|---|
| 2026-03-28 | T004 | ERP-PROV-MX-049-A | 153 |

**Qué me dice y por qué importa:** describo el nivel y dispersión de saldos conocidos, incluidos ceros, y los separo por categoría para evitar que una media global oculte diferencias. No sumo snapshots de fechas distintas como unidades movidas ni uso el máximo como umbral de error. Las unidades físicas y presentaciones siguen pendientes (Q16/Q21 / D016); tampoco pondero por demanda.

## 5. Rachas de ceros observados

Construyo rachas por tienda–SKU con fechas consecutivas y saldo numérico cero. Un desconocido, una fecha ausente o un saldo no cero interrumpe la evidencia; un desconocido no demuestra recuperación. Calculo primero la secuencia completa y luego su intersección con el último trimestre calendario disponible.


**Leyenda:** Cuento secuencias y tiendas por separado; el trimestre deriva del máximo snapshot, no de la fecha de ejecución. Las rachas en bordes tienen duración observada mínima; no afirmo quiebre operativo confirmado. No incluyo el índice de pandas.

| Medida | Resultado |
|---|---|
| Inicio trimestre de referencia | 2026-01-01 |
| Fin trimestre de referencia | 2026-03-31 |
| Rachas cero en toda la ventana | 11094 |
| Mayor racha cero en toda la ventana (días) | 4 |
| Rachas de más de tres días en toda la ventana | 3 |
| Rachas de más de tres días dentro del trimestre | 3 |
| Tiendas con esas rachas trimestrales | 3 |
| Rachas que tocan primera fecha del archivo | 60 |
| Rachas que tocan última fecha del archivo | 61 |



**Leyenda:** Todas las rachas con al menos cuatro días cero dentro del trimestre, sin selección top; Dias_cero mide toda la secuencia observada y Dias_cero_en_trimestre su intersección trimestral. Las fechas son inclusivas. No incluyo el índice de pandas.

| tienda_id | sku_erp | Inicio | Fin | Dias_cero | Dias_cero_en_trimestre |
|---|---|---|---|---|---|
| T015 | ERP-PROV-MX-014-D | 2026-02-09 | 2026-02-12 | 4 | 4 |
| T023 | ERP-PROV-MX-046-A | 2026-01-25 | 2026-01-28 | 4 | 4 |
| T038 | ERP-PROV-MX-040-A | 2026-03-18 | 2026-03-21 | 4 | 4 |

**Qué me dice:** las secuencias anteriores reúnen al menos cuatro días consecutivos con saldo cero dentro del trimestre. Muestro todas las que cumplen el criterio, no una selección de ejemplos.

**Por qué importa y límite:** son candidatas para investigar la pregunta de quiebres, no una confirmación de desabasto durante las 24 horas. Faltan definición de disponible y hora de corte (Q08/Q30 / D011); `N/A` puede ocultar otras rachas. Los bordes del archivo censuran posibles extensiones de otras secuencias. No uso la fecha actual como corte ni relleno el calendario con ceros.

## 6. Equivalencias y catálogo


**Leyenda:** Todas las equivalencias declaradas; los valores null no participan en unicidad ni permiten unir registros. No se compara con claves presentes en sales o e-commerce. No incluyo el índice de pandas.

| Clave | Filas | Null literal | Valores no nulos distintos | Duplicados adicionales no nulos |
|---|---|---|---|---|
| sku_pos | 65 | 0 | 65 | 0 |
| sku_erp | 65 | 5 | 60 | 0 |
| handle | 65 | 38 | 27 | 0 |



**Leyenda:** Todas las combinaciones observadas de presencia ERP y handle: True significa informado y False significa null literal. Equivalencias cuenta filas del mapeo, no ventas. No incluyo el índice de pandas.

| ERP_informado | Handle_informado | Equivalencias |
|---|---|---|
| False | False | 1 |
| False | True | 4 |
| True | False | 37 |
| True | True | 23 |



**Leyenda:** Todas las filas de mapeo con ERP null; <null> es solo representación visible de un nulo original, no clave creada. No incluyo el índice de pandas.

| sku_pos | sku_erp | handle |
|---|---|---|
| CN-00006 | <null> | estándar-cafe-grano-006 |
| CN-00016 | <null> | <null> |
| CN-00026 | <null> | premium-cafe-molido-026 |
| CN-00036 | <null> | gourmet-cafe-grano-036 |
| CN-00046 | <null> | termo-mercancia-046 |



**Leyenda:** Todos los productos ERP sin referencia no nula en sku_mappings; no significa que falten en POS ni que no se vendan online. No incluyo el índice de pandas.

| sku_erp | nombre | categoria |
|---|---|---|
| ERP-PROV-MX-001-A | Sándwich Comida Caliente | comida_caliente |
| ERP-PROV-MX-006-C | Estándar Cafe Grano | cafe_grano |
| ERP-PROV-MX-011-C | Bolillo Panaderia | panaderia |
| ERP-PROV-MX-016-C | Quiche Comida Caliente | comida_caliente |
| ERP-PROV-MX-021-A | Concha Panaderia | panaderia |
| ERP-PROV-MX-026-A | Premium Cafe Molido | cafe_molido |
| ERP-PROV-MX-031-A | Termo Mercancia | mercancia |
| ERP-PROV-MX-036-A | Gourmet Cafe Grano | cafe_grano |
| ERP-PROV-MX-041-D | Gourmet Cafe Molido | cafe_molido |
| ERP-PROV-MX-046-A | Termo Mercancia | mercancia |



**Leyenda:** Cuento nombres exactos y productos afectados por separado; un nombre compartido no permite deduplicar ni reconstruir equivalencias comerciales. No incluyo el índice de pandas.

| Medida | Resultado |
|---|---|
| Productos del catálogo | 70 |
| Categorías | 6 |
| Nombres distintos | 36 |
| Nombres usados por más de un ERP | 23 |
| Productos con un nombre compartido | 57 |
| Productos sin snapshots en esta extracción | 0 |

**Qué me dice:** de las 65 equivalencias, 5 tienen ERP nulo y 38 tienen handle nulo. No se repiten las claves no nulas. Hay 10 productos del catálogo sin referencia ERP informada en las equivalencias; eso no demuestra que no existan o no se vendan en otros canales. Encuentro 23 nombres compartidos por 57 productos.

**Por qué importa:** llegar a un handle no garantiza llegar a ERP y costos. Necesito equivalencias autorizadas y vigentes (Q04/Q05/Q22/Q23 / D008/D019). No uno nulos entre sí, no deduplico por nombre ni adopto inferencias por sufijo. El JSON aislado no permite contar los SKU o handles que realmente faltan en las otras fuentes.

## 7. Historial de costos


**Leyenda:** Todos los historiales; entradas cuenta versiones de costo y claves adicionales excluye la primera. La cobertura es potencial bajo última vigencia anterior o igual, sin afirmar método contable ni costo por unidad confirmado. No incluyo el índice de pandas.

| Medida | Resultado |
|---|---|
| Entradas de costo | 282 |
| Productos con historial no vacío | 70 |
| Primera vigencia | 2024-10-01 |
| Última vigencia | 2026-03-30 |
| Fechas inválidas | 0 |
| Fechas fuera de formato ISO diario | 0 |
| Claves SKU–vigencia adicionales | 0 |
| Costos no numéricos o no finitos | 0 |
| Costos cero | 0 |
| Costos negativos | 0 |
| Historiales no ordenados en origen | 0 |
| Vigencias posteriores al último snapshot | 0 |
| Productos observados sin costo desde su primer snapshot | 0 |



**Leyenda:** Todas las versiones de costo; Observaciones cuenta vigencias y el resto expresa MXN por la unidad de costo pendiente de confirmar. Media y percentiles no se ponderan por tiempo, compras ni ventas y no representan el costo vigente promedio. No incluyo el índice de pandas.

| Estadístico | Costo registrado |
|---|---|
| Observaciones | 282 |
| Media | 127.7098 |
| Desviación estándar | 98.9124 |
| Mínimo | 7.73 |
| Percentil 25 | 45.7425 |
| Mediana | 102.115 |
| Percentil 75 | 186.6 |
| Percentil 95 | 288.0035 |
| Máximo | 478.3 |



**Leyenda:** Comparo cada costo con la vigencia previa del mismo ERP, sin ponderar por compras; las primeras entradas no tienen cambio calculable. Los extremos porcentuales son señales y no errores demostrados. No incluyo el índice de pandas.

| Medida | Resultado |
|---|---|
| Cambios comparables | 212 |
| Aumentos | 117 |
| Bajadas | 95 |
| Sin cambio | 0 |
| Mayor subida porcentual | 9.8793 |
| Mayor bajada porcentual | -7.9589 |



**Leyenda:** Incluyo todos los empates de mayor subida y bajada porcentual de costo; cambio_mxn está en MXN por la unidad de costo aún por confirmar, cambio_pct es porcentaje sobre el costo anterior. No son márgenes. No incluyo el índice de pandas.

| sku_erp | fecha_vigencia | costo_previo | costo_mxn | cambio_mxn | cambio_pct |
|---|---|---|---|---|---|
| ERP-PROV-MX-006-C | 2025-05-28 | 110.82 | 102 | -8.82 | -7.9589 |
| ERP-PROV-MX-011-C | 2025-06-20 | 13.26 | 14.57 | 1.31 | 9.8793 |

**Qué me dice:** encuentro 282 vigencias para 70 productos; no detecto claves SKU–vigencia repetidas, costos inválidos o no positivos. Hay 212 cambios comparables: 117 aumentos y 95 bajadas. Todos los productos observados tienen una vigencia no posterior a su primer snapshot; bajo el escenario de última vigencia anterior o igual no habría huecos temporales iniciales.

**Por qué importa y límite:** puedo preparar una búsqueda temporal sin inventar costos. No confirma costo unitario, impuestos, gastos, política contable ni alcance por tienda (Q03/Q16/Q24–Q26 / D007/D016/D020). La media de todas las versiones no es el costo vigente medio ni el promedio ponderado de compras. Una variación extrema no demuestra error de captura. No calculo margen ni importo ventas en este análisis.

## 8. Dudas y próximos pasos

Conecto la evidencia con [las preguntas existentes](../03_negocio/PREGUNTAS_CLIENTE.md#evidencia-del-eda-aislado-de-inventory); no añado IDs duplicados ni doy preguntas por enviadas o respondidas.

**Leyenda:** priorizo dudas abiertas por impacto; P0 afecta cifras o conciliación y P1 afecta interpretación o diseño. La propuesta de avance es un supuesto de trabajo pendiente de revisión, no una regla del cliente.

| Prioridad | Pregunta y duda | Evidencia que la justifica | Cómo propongo avanzar sin respuesta |
|---|---|---|---|
| P0 | Q06 / D009: significado y recuperación de N/A | 4,417 saldos desconocidos | Conservar desconocidos y reportar cobertura; no imputar cero ni atravesarlos como continuidad demostrada. |
| P0 | Q07/Q28/Q29 / D010/D021: surtido, vigencias y ausencia de filas | 1,268 pares observados frente a 2,800 posibles | Usar pares observados y declarar población excluida; conciliar ventas después y no inventar surtido. |
| P0 | Q08/Q30 / D011: momento de captura y físico frente a disponible | 3 rachas trimestrales de al menos cuatro ceros diarios | Informar secuencias observadas, límites por desconocidos y ausencia de validación intradía. |
| P0 | Q03/Q16/Q24–Q26 / D007/D016/D020: unidad, base, alcance y política de costo | Historial global por producto sin campo de tienda, unidad ni base fiscal | Proponer última vigencia no posterior al día, explicitar base no validada y no imputar costo cero. |
| P0 | Q04/Q05 / D008: maestro y autoridad de equivalencias | ERP nulos y productos del catálogo sin equivalencia informada | Usar enlaces exactos completos y reportar no conciliados sin inferir por nombre o sufijo. |
| P1 | Q21/Q22/Q23 / D016/D019: variantes, vigencia y mantenimiento de claves | Nombres repetidos y mapeos sin fechas de vigencia | Conservar ERP como identidad y separar equivalencias declaradas de propuestas. |
| P1 | Q27/Q49/Q50 / D021/D026: movimientos y control de extracción | Metadata declara solo snapshots y no aporta lote ni control de origen | Conservar manifiesto local y huella; no reconciliar movimientos inexistentes ni afirmar integridad del ERP. |

Mi siguiente paso es completar la exploración aislada de e-commerce y conciliar fuentes antes de implementar el pipeline. Para rotación necesitaré ventas elegibles y el mismo universo de pares, fechas y unidades; para margen necesitaré costo y monto comparables; para quiebres necesitaré interpretación operativa del saldo. Mi revisión personal de esta propuesta sigue pendiente.

## Documentación relacionada

- [Notebook de inventory](../../notebooks/03_inventory.ipynb).
- [Preguntas al cliente](../03_negocio/PREGUNTAS_CLIENTE.md#evidencia-del-eda-aislado-de-inventory).

## Conclusión

Tengo documentada la estructura y la cobertura interna de inventario, diferenciando saldos desconocidos, ceros y ausencia de pares. Uso las rachas observadas y los controles de equivalencias y costos para preparar preguntas y orientar la conciliación; no presento este diagnóstico aislado como una respuesta definitiva de rotación, quiebres o margen.
