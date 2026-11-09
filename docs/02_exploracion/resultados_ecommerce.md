# Resultados del análisis exploratorio aislado de ecommerce_orders.parquet

Fecha de documentación y verificación: 9 de noviembre de 2026.

## Alcance y versión

Analizo únicamente `datos/ecommerce_orders.parquet`, sin consultar ni cruzar otros archivos de datos. No valido mapeos a ERP, costos, inventario, correspondencia con POS ni cobertura de tipos de cambio. Los antecedentes entre fuentes conservan su alcance histórico y no forman parte de los resultados aislados siguientes.

El código y las salidas están en [04_ecommerce.ipynb](../../notebooks/04_ecommerce.ipynb). Cuento registros de origen: la unicidad de order_id no confirma pedidos completos, líneas ni estabilidad entre extracciones. La ejecución técnica corresponde a la IA; mi revisión personal y las decisiones comerciales siguen pendientes. No muestro valores personales ni muestras de clientes.


## 1. Identificación de la fuente

Identifico la versión para poder detectar cambios posteriores.


**Leyenda:** Identifico la extracción analizada; tamaño en bytes y conteos enteros. La huella no acredita completitud de origen. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Identificación | Resultado |
| --- | --- |
| Archivo | datos/ecommerce_orders.parquet |
| Tamaño en bytes | 724,121 |
| SHA-256 | 00c560b39425fe7f0088fbe20c66c2b8861d10c2c7006ba6e7335cdd6dfc856e |
| Registros | 9,947 |
| Columnas originales | 11 |


**Qué me dice:** el SHA-256 coincide con el antecedente documentado de esta fuente y se mantiene al finalizar. No modifiqué el Parquet.

**Por qué importa y límite:** la huella identifica bytes, no certifica extracción completa ni operaciones verdaderas. Un cambio posterior requiere documentarlo antes de regenerar evidencia.


## 2. Estructura, diccionario y calidad textual

Describo las columnas originales sin publicar valores de nombre, correo, RFC, ciudad o dirección.


**Leyenda:** Diccionario de todas las columnas originales. Nulos son valores ausentes reconocidos por pandas, no textos vacíos. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Campo | Tipo Parquet | Tipo pandas | Nulos | Interpretación y límite |
| --- | --- | --- | --- | --- |
| order_id | large_string | object | 0 | Identificador de origen; pedido, línea y estabilidad pendientes (Q31). |
| fecha | large_string | object | 0 | Texto temporal; evento y zona pendientes (Q34). |
| product_handle | large_string | object | 0 | Clave textual de producto; variante y estabilidad pendientes (Q32). |
| cantidad | int64 | int64 | 0 | Cantidad registrada; unidad física pendiente (Q16). |
| amount | double | float64 | 0 | Importe original en currency; total de línea y componentes pendientes (Q33). |
| currency | large_string | object | 0 | Código de moneda del importe; no sumo monedas distintas. |
| customer_name | large_string | object | 0 | Nombre personal; excluyo valores de las salidas. |
| customer_email | large_string | object | 0 | Correo personal; excluyo valores de las salidas. |
| customer_rfc | large_string | object | 8,462 | Dato fiscal personal; nulo no implica pedido inválido (Q44). |
| shipping_city | large_string | object | 0 | Ciudad de envío; no acredita tienda de cumplimiento (Q35). |
| shipping_address | large_string | object | 0 | Dirección personal; excluyo valores de las salidas. |


**Leyenda:** Controles agregados en campos textuales; conteo de filas por campo, sin ejemplos personales. Los nulos se cuentan por separado en el esquema. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Campo | Textos vacíos o espacios | Textos con espacios en extremos |
| --- | --- | --- |
| order_id | 0 | 0 |
| fecha | 0 | 0 |
| product_handle | 0 | 0 |
| currency | 0 | 0 |
| customer_name | 0 | 0 |
| customer_email | 0 | 0 |
| customer_rfc | 0 | 0 |
| shipping_city | 0 | 0 |
| shipping_address | 0 | 0 |


**Qué me dice:** la fecha entra como texto y los importes como double. El RFC tiene ausencias, distintas de cadenas vacías; no infiero obligatoriedad fiscal ni invalidez del registro. Los nombres de campos orientan la lectura, pero no confirman semántica.

**Por qué importa y límite:** las cuatro métricas no necesitan identidad del comprador. Propongo excluir estos campos del modelo analítico y mantener solo agregados para documentación (Q44–Q47 / D025); no equivale a una autorización general de publicación.


## 3. Calidad, granularidad y columnas derivadas

Conservo los campos originales y creo las siguientes columnas en una copia:

- `fecha_dt`: interpretación exacta de fecha con `YYYY-MM-DD HH:MM:SS`; valores no interpretables a `NaT`, sin zona añadida. La uso para calendario.
- `dia`: medianoche del día de fecha_dt; mantiene NaT y sirve para presencia diaria.
- `mes`: período mensual de fecha_dt; mantiene NaT y sirve para agrupación mensual.
- `cantidad_num` y `amount_num`: conversión numérica de cantidad y amount; valores no convertibles a NaN. Controlo infinitos y signos por separado.
- `importe_unitario`: amount_num dividido por cantidad_num si ambos son finitos y cantidad es positiva; otros casos a NaN. Es moneda original por unidad registrada, condicionado a total de línea; no es tarifa de lista.

No reemplazo cero, nulo ni ausencia de fila. Los patrones son formas observadas, no contratos del sistema.


**Leyenda:** Controles sobre todas las filas; duplicados adicionales excluyen la primera aparición. Cero alertas no demuestra exactitud comercial. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Control | Registros |
| --- | --- |
| Duplicados exactos adicionales | 0 |
| Repeticiones adicionales de order_id | 0 |
| order_id nulos | 0 |
| order_id fuera de SHOP y siete dígitos | 0 |
| Fechas sin interpretar | 0 |
| Fechas fuera del patrón textual esperado | 0 |
| Monedas fuera de MXN, USD y EUR | 0 |
| Handles nulos | 0 |
| cantidad_num: nulos o no convertibles | 0 |
| cantidad_num: infinitos | 0 |
| cantidad_num: ceros | 0 |
| cantidad_num: negativos | 0 |
| amount_num: nulos o no convertibles | 0 |
| amount_num: infinitos | 0 |
| amount_num: ceros | 0 |
| amount_num: negativos | 0 |
| Cantidades finitas no enteras | 0 |


**Leyenda:** Cuento identidades y coincidencias comerciales exactas de cinco campos no personales; no muestro filas individuales ni considero estas coincidencias duplicados confirmados. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Medida | Resultado |
| --- | --- |
| order_id distintos no nulos | 9,947 |
| Handles distintos no nulos | 33 |
| Grupos con igual fecha, handle, cantidad, amount y currency | 2 |
| Filas en esos grupos | 4 |


**Qué me dice:** no encuentro duplicados exactos adicionales ni IDs repetidos bajo estos controles. Hay coincidencias en fecha, handle, cantidad, amount y currency con identificadores diferentes; no prueban una operación duplicada. No publico sus filas ni las elimino.

**Por qué importa y límite:** no puedo deducir ticket promedio, cesta de compra ni número de pedidos pagados a partir de esta unicidad (Q09/Q31 / D012). Faltan line_item_id, product_id, variant_id, estado, ajustes y enlace a operación original. Signos positivos no demuestran ausencia de reembolsos.


## 4. Cobertura temporal

Uso el calendario inclusivo entre los extremos interpretados, sin inventar actividad antes o después ni asignar zona horaria.


**Leyenda:** Ventana completa del archivo, fechas sin zona confirmada; conteos de días y meses, sin extrapolar fuera de los extremos. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Medida | Resultado |
| --- | --- |
| Primera marca interpretada | 2025-04-01 03:12:00 |
| Última marca interpretada | 2026-03-31 22:31:00 |
| Días calendario inclusivos | 365 |
| Días con registros | 365 |
| Días sin registros | 0 |
| Meses con registros | 12 |
| Marcas con segundos distintos de cero | 0 |


**Leyenda:** Presencia de cada moneda contra el mismo calendario global inclusivo; un hueco no se transforma en importe cero ni prueba extracción incompleta. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Moneda | Primera fecha | Última fecha | Días con registros | Días sin registros en ventana global |
| --- | --- | --- | --- | --- |
| EUR | 2025-04-01 | 2026-03-31 | 261 | 104 |
| MXN | 2025-04-01 | 2026-03-31 | 365 | 0 |
| USD | 2025-04-01 | 2026-03-31 | 364 | 1 |


**Leyenda:** Todos los handles, orden alfabético; filas, días y meses distintos con presencia en la ventana global. No presupongo surtido activo todos los días. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Handle | Registros | Días con registros | Meses con registros |
| --- | --- | --- | --- |
| americano-cafe-grano-032 | 279 | 192 | 12 |
| americano-cafe-molido-024 | 314 | 208 | 12 |
| americano-cafe-molido-052 | 332 | 218 | 12 |
| descafeinado-cafe-grano-010 | 309 | 206 | 12 |
| descafeinado-cafe-grano-014 | 301 | 197 | 12 |
| especial-cafe-grano-045 | 294 | 201 | 12 |
| espresso-cafe-molido-054 | 342 | 212 | 12 |
| estándar-cafe-grano-006 | 303 | 202 | 12 |
| estándar-cafe-grano-069 | 309 | 211 | 12 |
| estándar-cafe-molido-034 | 291 | 201 | 12 |
| estándar-cafe-molido-065 | 297 | 196 | 12 |
| filtros-mercancia-003 | 320 | 218 | 12 |
| filtros-mercancia-043 | 295 | 209 | 12 |
| filtros-mercancia-047 | 293 | 204 | 12 |
| gourmet-cafe-grano-036 | 275 | 194 | 12 |
| gourmet-cafe-molido-019 | 304 | 201 | 12 |
| gourmet-cafe-molido-041 | 297 | 205 | 12 |
| molinillo-mercancia-030 | 319 | 208 | 12 |
| molinillo-mercancia-070 | 315 | 211 | 12 |
| orgánico-cafe-grano-059 | 288 | 208 | 12 |
| premium-cafe-grano-057 | 310 | 212 | 12 |
| premium-cafe-molido-026 | 291 | 203 | 12 |
| prensa-francesa-mercancia-004 | 304 | 195 | 12 |
| selección-cafe-grano-007 | 295 | 199 | 12 |
| selección-cafe-grano-038 | 292 | 198 | 12 |
| selección-cafe-molido-013 | 305 | 206 | 12 |
| taza-mercancia-039 | 300 | 207 | 12 |
| termo-mercancia-029 | 270 | 200 | 12 |
| termo-mercancia-031 | 317 | 218 | 12 |
| termo-mercancia-046 | 270 | 194 | 12 |
| termo-mercancia-055 | 296 | 207 | 12 |
| tradicional-cafe-molido-018 | 308 | 212 | 12 |
| tradicional-cafe-molido-037 | 312 | 220 | 12 |


**Qué me dice:** la presencia global, por moneda y por handle son universos diferentes. Un día sin una moneda puede tener registros en otra; que un handle no aparezca un día no acredita un producto activo sin ventas. Todas las marcas tienen segundos cero, sin que eso demuestre la precisión real del sistema.

**Por qué importa y límite:** continuidad no valida cortes de origen, calendario operativo, cargas tardías ni meses completos en sentido comercial. Necesito evento temporal y zona (Q34), lote y totales independientes (Q41/Q49/Q50). No transformo días ausentes en ventas cero.


## 5. Distribuciones y monedas

Mantengo separados los importes de cada moneda. Las estadísticas son descriptivas de registros, no ventas netas; cantidades sin unidad física confirmada.


**Leyenda:** Todas las filas por moneda; importe en unidades de la moneda indicada, participación sobre filas totales. No sumo la columna de importes entre monedas. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Moneda | Registros | Cantidad registrada | Importe original | Handles | Participación de registros % |
| --- | --- | --- | --- | --- | --- |
| EUR | 470 | 613 | 9,885.8600 | 33 | 4.7250 |
| MXN | 6,942 | 9,231 | 2,912,430.7400 | 33 | 69.7899 |
| USD | 2,535 | 3,448 | 61,796.4600 | 33 | 25.4851 |


**Leyenda:** Distribución de cantidad por registro en toda la extracción; cuantiles con interpolación lineal de pandas, desviación con ddof=1. La suma de cantidades no acredita unidad física comparable. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Estadística | Cantidad registrada |
| --- | --- |
| Observaciones | 9,947.0000 |
| Media | 1.3363 |
| Desviación estándar muestral | 0.8843 |
| Mínimo | 1.0000 |
| Percentil 1 | 1.0000 |
| Cuartil 1 | 1.0000 |
| Mediana | 1.0000 |
| Cuartil 3 | 1.0000 |
| Percentil 99 | 5.0000 |
| Máximo | 15.0000 |


**Leyenda:** Distribución por moneda, sin conversión. Valores en moneda original salvo Observaciones (conteo); importe unitario solo en filas elegibles, sin inferir precio de lista. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Moneda | Medida | Estadística | Valor |
| --- | --- | --- | --- |
| EUR | Importe por registro | Observaciones | 470.0000 |
| EUR | Importe por registro | Media | 21.0337 |
| EUR | Importe por registro | Desviación estándar muestral | 19.8783 |
| EUR | Importe por registro | Mínimo | 3.8500 |
| EUR | Importe por registro | Percentil 1 | 4.0583 |
| EUR | Importe por registro | Cuartil 1 | 9.9525 |
| EUR | Importe por registro | Mediana | 16.7600 |
| EUR | Importe por registro | Cuartil 3 | 27.5975 |
| EUR | Importe por registro | Percentil 99 | 84.1845 |
| EUR | Importe por registro | Máximo | 251.9300 |
| EUR | Importe por unidad registrada | Observaciones | 470.0000 |
| EUR | Importe por unidad registrada | Media | 16.3464 |
| EUR | Importe por unidad registrada | Desviación estándar muestral | 10.0300 |
| EUR | Importe por unidad registrada | Mínimo | 3.8500 |
| EUR | Importe por unidad registrada | Percentil 1 | 4.0169 |
| EUR | Importe por unidad registrada | Cuartil 1 | 8.9375 |
| EUR | Importe por unidad registrada | Mediana | 12.9800 |
| EUR | Importe por unidad registrada | Cuartil 3 | 19.2350 |
| EUR | Importe por unidad registrada | Percentil 99 | 41.8579 |
| EUR | Importe por unidad registrada | Máximo | 42.4200 |
| MXN | Importe por registro | Observaciones | 6,942.0000 |
| MXN | Importe por registro | Media | 419.5377 |
| MXN | Importe por registro | Desviación estándar muestral | 394.1075 |
| MXN | Importe por registro | Mínimo | 80.7300 |
| MXN | Importe por registro | Percentil 1 | 80.7300 |
| MXN | Importe por registro | Cuartil 1 | 193.4100 |
| MXN | Importe por registro | Mediana | 327.5900 |
| MXN | Importe por registro | Cuartil 3 | 555.2400 |
| MXN | Importe por registro | Percentil 99 | 2,141.0178 |
| MXN | Importe por registro | Máximo | 5,016.2000 |
| MXN | Importe por unidad registrada | Observaciones | 6,942.0000 |
| MXN | Importe por unidad registrada | Media | 317.3363 |
| MXN | Importe por unidad registrada | Desviación estándar muestral | 189.1678 |
| MXN | Importe por unidad registrada | Mínimo | 80.7300 |
| MXN | Importe por unidad registrada | Percentil 1 | 80.7300 |
| MXN | Importe por unidad registrada | Cuartil 1 | 192.6700 |
| MXN | Importe por unidad registrada | Mediana | 262.3200 |
| MXN | Importe por unidad registrada | Cuartil 3 | 378.1900 |
| MXN | Importe por unidad registrada | Percentil 99 | 828.3000 |
| MXN | Importe por unidad registrada | Máximo | 828.3000 |
| USD | Importe por registro | Observaciones | 2,535.0000 |
| USD | Importe por registro | Media | 24.3773 |
| USD | Importe por registro | Desviación estándar muestral | 23.8221 |
| USD | Importe por registro | Mínimo | 4.3700 |
| USD | Importe por registro | Percentil 1 | 4.5402 |
| USD | Importe por registro | Cuartil 1 | 11.4600 |
| USD | Importe por registro | Mediana | 18.3500 |
| USD | Importe por registro | Cuartil 3 | 30.5400 |
| USD | Importe por registro | Percentil 99 | 128.8308 |
| USD | Importe por registro | Máximo | 291.7900 |
| USD | Importe por unidad registrada | Observaciones | 2,535.0000 |
| USD | Importe por unidad registrada | Media | 17.9448 |
| USD | Importe por unidad registrada | Desviación estándar muestral | 10.6379 |
| USD | Importe por unidad registrada | Mínimo | 4.3700 |
| USD | Importe por unidad registrada | Percentil 1 | 4.5067 |
| USD | Importe por unidad registrada | Cuartil 1 | 10.6375 |
| USD | Importe por unidad registrada | Mediana | 14.4300 |
| USD | Importe por unidad registrada | Cuartil 3 | 21.4750 |
| USD | Importe por unidad registrada | Percentil 99 | 47.0764 |
| USD | Importe por unidad registrada | Máximo | 48.6875 |


**Qué me dice:** las medias, medianas y extremos describen magnitudes distintas y dependen de la moneda y la cantidad. Un importe alto por fila no prueba error ni precio alto por unidad. La participación de moneda mide registros, no participación en ingresos consolidados.

**Por qué importa y límite:** no sumo amount de MXN, USD y EUR ni aplico tasas en esta exploración. La razón unitaria no reconstruye impuestos, descuentos, envío o tarifa histórica (Q16/Q33). Los cuatro decimales son formato de presentación; double no define precisión económica ni redondeo (Q37/Q38/Q40 / D013/D023).


## 6. Evolución mensual y concentración

Incluyo todos los registros observados sin filtrar por estatus, porque el archivo no lo contiene.


**Leyenda:** Todos los meses y monedas con filas; importe en moneda original y cantidades registradas. No relleno combinaciones ausentes. Handles cuenta claves distintas por mes y moneda. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Mes | Moneda | Registros | Cantidad registrada | Importe original | Handles |
| --- | --- | --- | --- | --- | --- |
| 2025-04 | EUR | 43 | 62 | 1,104.1800 | 23 |
| 2025-04 | MXN | 618 | 827 | 267,327.7200 | 33 |
| 2025-04 | USD | 215 | 294 | 5,255.4700 | 33 |
| 2025-05 | EUR | 36 | 47 | 729.0100 | 24 |
| 2025-05 | MXN | 592 | 779 | 255,221.9100 | 33 |
| 2025-05 | USD | 201 | 303 | 5,383.2800 | 33 |
| 2025-06 | EUR | 35 | 43 | 526.3500 | 19 |
| 2025-06 | MXN | 531 | 746 | 240,541.5600 | 33 |
| 2025-06 | USD | 200 | 287 | 4,956.3900 | 33 |
| 2025-07 | EUR | 39 | 56 | 950.7600 | 22 |
| 2025-07 | MXN | 570 | 759 | 242,019.0100 | 33 |
| 2025-07 | USD | 200 | 264 | 4,904.4000 | 33 |
| 2025-08 | EUR | 44 | 56 | 878.9900 | 26 |
| 2025-08 | MXN | 608 | 793 | 230,023.3100 | 33 |
| 2025-08 | USD | 215 | 291 | 5,264.5400 | 33 |
| 2025-09 | EUR | 34 | 52 | 697.1500 | 22 |
| 2025-09 | MXN | 554 | 726 | 238,023.7400 | 33 |
| 2025-09 | USD | 227 | 280 | 5,131.4800 | 33 |
| 2025-10 | EUR | 36 | 42 | 705.8500 | 20 |
| 2025-10 | MXN | 647 | 861 | 270,414.1300 | 33 |
| 2025-10 | USD | 198 | 285 | 5,100.2900 | 33 |
| 2025-11 | EUR | 43 | 58 | 985.1000 | 22 |
| 2025-11 | MXN | 569 | 738 | 237,685.6000 | 33 |
| 2025-11 | USD | 246 | 316 | 5,704.3400 | 33 |
| 2025-12 | EUR | 38 | 43 | 676.4700 | 24 |
| 2025-12 | MXN | 581 | 766 | 245,381.2400 | 33 |
| 2025-12 | USD | 211 | 279 | 4,908.9600 | 33 |
| 2026-01 | EUR | 38 | 48 | 858.4900 | 21 |
| 2026-01 | MXN | 581 | 759 | 238,493.4000 | 33 |
| 2026-01 | USD | 203 | 281 | 4,992.7800 | 33 |
| 2026-02 | EUR | 37 | 45 | 651.5700 | 23 |
| 2026-02 | MXN | 522 | 708 | 214,671.8600 | 33 |
| 2026-02 | USD | 200 | 281 | 5,171.3900 | 32 |
| 2026-03 | EUR | 47 | 61 | 1,121.9400 | 27 |
| 2026-03 | MXN | 569 | 769 | 232,627.2600 | 33 |
| 2026-03 | USD | 219 | 287 | 5,023.1400 | 33 |


**Leyenda:** Diez handles con mayor importe por moneda durante toda la ventana; desempato por handle alfabético y mantengo diez posiciones. Participación sobre importe total de su moneda; no mide margen ni rotación. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Moneda | Handle | Registros | Cantidad registrada | Importe original | Participación importe % |
| --- | --- | --- | --- | --- | --- |
| EUR | taza-mercancia-039 | 23 | 31 | 1,279.6300 | 12.9440 |
| EUR | termo-mercancia-055 | 15 | 22 | 708.9000 | 7.1708 |
| EUR | prensa-francesa-mercancia-004 | 13 | 16 | 568.7800 | 5.7535 |
| EUR | termo-mercancia-031 | 15 | 18 | 507.1200 | 5.1298 |
| EUR | termo-mercancia-046 | 14 | 18 | 492.0300 | 4.9771 |
| EUR | filtros-mercancia-047 | 15 | 19 | 485.3000 | 4.9090 |
| EUR | descafeinado-cafe-grano-014 | 22 | 26 | 460.7900 | 4.6611 |
| EUR | molinillo-mercancia-070 | 18 | 23 | 441.6200 | 4.4672 |
| EUR | termo-mercancia-029 | 12 | 13 | 420.2400 | 4.2509 |
| EUR | descafeinado-cafe-grano-010 | 13 | 20 | 368.7400 | 3.7300 |
| MXN | taza-mercancia-039 | 208 | 264 | 218,671.2000 | 7.5082 |
| MXN | prensa-francesa-mercancia-004 | 211 | 277 | 198,498.2000 | 6.8156 |
| MXN | termo-mercancia-055 | 200 | 267 | 174,172.1100 | 5.9803 |
| MXN | termo-mercancia-031 | 219 | 290 | 162,953.9000 | 5.5951 |
| MXN | termo-mercancia-029 | 184 | 243 | 157,721.5800 | 5.4155 |
| MXN | filtros-mercancia-047 | 212 | 282 | 145,497.9000 | 4.9958 |
| MXN | termo-mercancia-046 | 191 | 241 | 133,812.8400 | 4.5945 |
| MXN | americano-cafe-molido-024 | 238 | 333 | 112,970.2500 | 3.8789 |
| MXN | molinillo-mercancia-070 | 220 | 283 | 110,930.3400 | 3.8089 |
| MXN | descafeinado-cafe-grano-014 | 210 | 296 | 106,385.3600 | 3.6528 |
| USD | taza-mercancia-039 | 69 | 93 | 4,352.3900 | 7.0431 |
| USD | prensa-francesa-mercancia-004 | 80 | 105 | 4,250.1700 | 6.8777 |
| USD | termo-mercancia-055 | 81 | 111 | 4,087.2200 | 6.6140 |
| USD | termo-mercancia-029 | 74 | 104 | 3,815.8700 | 6.1749 |
| USD | termo-mercancia-031 | 83 | 113 | 3,585.1200 | 5.8015 |
| USD | termo-mercancia-046 | 65 | 98 | 3,076.0600 | 4.9777 |
| USD | filtros-mercancia-047 | 66 | 88 | 2,551.8900 | 4.1295 |
| USD | descafeinado-cafe-grano-010 | 83 | 121 | 2,543.5900 | 4.1161 |
| USD | estándar-cafe-grano-069 | 87 | 117 | 2,490.2400 | 4.0297 |
| USD | molinillo-mercancia-070 | 77 | 98 | 2,161.2700 | 3.4974 |


**Qué me dice:** el resumen permite comparar actividad dentro de una moneda y seguir handles por mes. El ranking conserva diez posiciones por moneda con desempate alfabético, sin atribuir nombres o categorías mediante otras fuentes.

**Por qué importa y límite:** no equivale al crecimiento consolidado del canal ni a un ranking de margen o rotación. El primer mes no tiene mes anterior en esta fuente; no invento base cero. No atribuyo variaciones a estacionalidad, promoción o desempeño. La gráfica SVG del notebook muestra tres paneles mensuales con ejes independientes, desde cero y en la moneda de cada panel; sus alturas no son comparables entre monedas.


## 7. Extremos del importe unitario

Comparo cada handle dentro de su moneda. El resumen derivado contiene q1 y q3 (cuartiles con interpolación lineal), iqr (q3 menos q1), limite_inferior (q1 − 1.5×iqr) y limite_superior (q3 + 1.5×iqr), todos en moneda por unidad registrada. `observaciones` cuenta razones conocidas por grupo.

En una copia analítica sin datos personales, `evaluable` exige razón finita, al menos cuatro observaciones y dispersión positiva; `senal_iqr` indica que rebasa estrictamente una cerca. Si no es evaluable lo cuento aparte: no significa normalidad. Las cercas negativas son límites teóricos, no importes negativos observados.


**Leyenda:** Conteos por moneda de toda la extracción. Señalados es subconjunto de Evaluados; Sin evaluación conserva filas no elegibles. Cercas estrictas por handle y moneda, sin eliminar casos. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Moneda | Registros | Evaluados | Señalados | Sin evaluación |
| --- | --- | --- | --- | --- |
| EUR | 470 | 470 | 4 | 0 |
| MXN | 6,942 | 0 | 0 | 6,942 |
| USD | 2,535 | 2,535 | 0 | 0 |


**Leyenda:** Todos los grupos producto y moneda; IQR cero impide evaluar esta regla y no demuestra ausencia de extremos. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Moneda | Grupos | Grupos con IQR cero |
| --- | --- | --- |
| EUR | 33 | 0 |
| MXN | 33 | 33 |
| USD | 33 | 0 |


**Leyenda:** Todos los grupos con señales, sin filas individuales ni identificadores personales; razones y cercas en moneda original por unidad registrada. Orden alfabético por moneda y handle. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Moneda | Handle | Filas señaladas | Mínimo señalado | Máximo señalado | Cerca inferior | Cerca superior |
| --- | --- | --- | --- | --- | --- | --- |
| EUR | descafeinado-cafe-grano-010 | 1 | 19.1600 | 19.1600 | 17.5400 | 19.1400 |
| EUR | prensa-francesa-mercancia-004 | 3 | 34.4200 | 34.6700 | 35.0600 | 36.7400 |


**Qué me dice:** evalúo 3,005 filas y señalo 4. Las cercas de todos los grupos están calculadas en el notebook, sin seleccionar ejemplos personales.

Los grupos MXN tienen IQR cero: sus filas quedan sin evaluación, no libres de extremos. En esta extracción la razón MXN es constante a dos decimales por handle; diferencias mínimas binarias no demuestran cambios de tarifa. Esa regularidad no acredita tarifa oficial ni base fiscal.

**Por qué importa y límite:** son señales estadísticas para revisar, no errores confirmados. No elimino registros ni valido tarifas por ausencia de señales. La agrupación mezcla fechas de una misma clave y podría ocultar cambios temporales; haría más controles únicamente si cambian una decisión. Para las señales EUR necesito revisar la distribución y las reglas de origen; no infiero una conversión concreta ni consulto tasas.


## 8. Controles de conservación

Contrasto columnas originales, conteos, sumas por moneda y huellas antes de cerrar.


**Leyenda:** Controles internos ejecutados; la tolerancia de coma flotante no es tolerancia contable aprobada. Si la huella difiere del antecedente, debo documentar el cambio. Cada fila corresponde a las etiquetas visibles; omito el índice de pandas.

| Control | Resultado |
| --- | --- |
| Columnas originales conservadas en memoria | Sí |
| Conteos conservados por moneda, mes y producto | Sí |
| Sumas conservadas por moneda; tolerancia técnica 1e-8 | Sí |
| SHA-256 final igual al inicial | Sí |
| SHA-256 igual al antecedente | Sí |


**Qué me dice:** los resúmenes conservan el universo original y la fuente permanece intacta. La tolerancia 1e-8 es una comprobación técnica de coma flotante, no una tolerancia contable aprobada.

**Por qué importa y límite:** demuestra coherencia interna de la implementación; no valida contra cierres del negocio ni acredita compatibilidad entre archivos.


## 9. Dudas y próximos pasos

Conecto los pendientes con [las preguntas existentes](../03_negocio/PREGUNTAS_CLIENTE.md#evidencia-del-eda-aislado-de-ecommerce) y con D012/D013/D019/D022/D023/D025/D026 en el registro de dudas. No doy las preguntas por enviadas ni respondidas. Las propuestas siguientes son supuestos de trabajo pendientes de revisión.

**Leyenda:** priorizo preguntas abiertas por impacto: P0 cambia cifras o conciliación; P1 afecta interpretación y diseño. Evidencia estructural corresponde solo a este Parquet; no acredita estado comercial.

| Prioridad | Preguntas y duda | Evidencia | Cómo propongo avanzar sin respuesta |
|---|---|---|---|
| P0 | Q09/Q31/Q33; D012: estatus, granularidad y base de amount | ID único por fila; sin line_item_id, estatus, devoluciones ni desglose | Contar registros; conservar importes como registrados, con elegibilidad y total de línea solo como supuestos explícitos; no certificar ingresos netos. |
| P0 | Q16/Q32; D019: unidad, producto y variante estable | cantidad y product_handle sin unidad, SKU POS/ERP o variant_id | Conservar handle original; conciliar después con maestro autorizado, sin inferir claves por sufijos. |
| P0 | Q34/Q37/Q38/Q40; D013/D023: evento temporal, liquidación y redondeo | fecha textual sin zona y amount double en varias monedas | Mantener fecha original y monedas separadas; definir conversión y Decimal al implementar, sin aplicar tasas en este análisis. |
| P0 | Q35/Q36; D022: cumplimiento y duplicación entre canales | Sin almacén, tienda o referencia POS | Mantener canal online separado; no atribuir stock o tienda desde envío ni afirmar ausencia de doble conteo. |
| P0 para publicación; P1 para modelo | Q44–Q47; D025: uso y acceso a datos personales | Campos personales y RFC ausentes | Mantener fuentes locales, excluir datos personales del modelo propuesto y usar únicamente agregados en salidas. |
| P1; P0 para certificación de cifras | Q41/Q49/Q50; D026: corte, cargas y control de origen | Sin lote, fecha de extracción ni total independiente | Conservar manifiesto y hash, diseñar cargas idempotentes y pedir totales; no declarar completitud por continuidad del calendario. |

Mi siguiente paso es conciliar claves, fechas, unidades y monedas entre fuentes antes de implementar el pipeline y sus pruebas. No necesito más controles aislados sin impacto claro en una decisión.


## Documentación relacionada

- [Notebook de ecommerce](../../notebooks/04_ecommerce.ipynb).
- [Preguntas al cliente](../03_negocio/PREGUNTAS_CLIENTE.md#evidencia-del-eda-aislado-de-ecommerce).

## Conclusión

Tengo caracterizados los registros online, su cobertura y sus importes por moneda sin exponer datos personales. Uso la evidencia para orientar la conciliación y las preguntas pendientes de identidad, estatus, base financiera, fecha y unidad; no presento consistencia interna como ingresos reconocidos ni como respuestas definitivas de negocio.
