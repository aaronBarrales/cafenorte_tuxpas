# CaféNorte — Mi guía de estudio y defensa técnica

Uso esta guía para entender el proyecto antes de presentarlo. Explico decisiones y resultados de la versión entregada; mi comprensión requiere revisar los comandos y poder reproducir los cálculos. La propuesta al cliente es un documento separado de dos páginas.

## 1. Cómo cuento el recorrido del proyecto

Mi problema es que POS, ERP y Shopify tienen identificadores, granularidades y monedas diferentes. Una suma directa no produce una cifra confiable. Empiezo por comprender las fuentes por separado, después compruebo sus conectores y finalmente construyo métricas sobre poblaciones comparables.

Mi recorrido es: requisitos → exploraciones individuales → conciliación conjunta → reglas explícitas → ETL → modelo persistido → respuestas → pruebas independientes → propuesta AWS. En notebooks/ están las cinco exploraciones; en scripts/pipeline.py está el proceso ejecutable; en docs/03_negocio están reglas, resultados y propuesta.

Mis preguntas documentadas aportaron dirección: qué significa tipo_comprobante, por qué cambia el importe de un SKU, si varias filas podían ser una compra, qué significa un handle ausente y si V00000000 estaba por debajo del costo. Esas preguntas ayudan a distinguir una explicación plausible de una relación demostrada.

Mi explicación de 30 segundos: «Integro las fuentes sin perder movimientos y aplico reglas explícitas de moneda y costo vigente. Produzco cuatro respuestas con cobertura visible. La demo se ejecuta localmente y propongo una carga diaria en AWS por USD 75 mensuales bajo sus supuestos. Las excepciones quedan identificadas para que el cliente pueda corregirlas.»

No necesito memorizar cada línea. Debo poder explicar qué entra, cuál es la clave de cada tabla, qué significa cada columna derivada y cómo detectaría un resultado incorrecto.

## 2. Qué conozco de las fuentes y sus conexiones

Leyenda: los conteos corresponden a la versión procesada en la entrega; filas no equivale automáticamente a tickets o pedidos completos.

| Fuente | Filas | Grano de trabajo |
|---|---:|---|
| sales.csv | 86,490 | Un registro POS con venta_id, tienda y SKU |
| ecommerce_orders.parquet | 9,947 | Un registro de orden con order_id y handle |
| inventory.json: snapshots | 230,776 | Una fotografía por día, tienda y SKU ERP |
| exchange_rates.csv | 730 | Una tasa por fecha y divisa extranjera |

Inventory también contiene 70 productos, 40 tiendas, 65 equivalencias y 282 vigencias de costo. Uso SKU POS o handle para llegar a sku_erp mediante el puente entregado. Un handle es un identificador de URL, no una descripción ni una clave ERP garantizada.

En físico encuentro 74,141 filas con ERP exacto y 12,349 sin ERP conciliado. En online son 6,959 y 2,988, respectivamente. No elimino las filas que no cruzan: aún contribuyen al análisis de ingresos si su moneda es interpretable, pero no a margen o rotación que necesiten producto y costo.

No uno por nombre porque existen nombres compartidos y variantes. No completo sufijos por intuición. Tampoco uno ventas con stock solo por SKU: la clave correcta del snapshot incluye día y tienda. Antes de unir exijo unicidad del lado derecho para impedir multiplicación de importes.

SHA-256 identifica bytes de una versión, no calidad comercial. La huella actual de sales cambió frente al EDA anterior y está documentada. El ETL acepta únicamente las versiones revisadas; si el archivo cambia, primero investigo y después actualizo el contrato.

## 3. Cómo funciona el ETL y cómo persisto el modelo

La función run lee los originales y comprueba versiones, claves y valores. Shopify se lee con una lista de columnas que excluye nombres, correos, RFC y direcciones. Mantengo los datos comerciales originales y agrego columnas derivadas.

Creo dia desde la fecha original sin inventar zona horaria. sku_erp viene del puente exacto; estado_mapeo distingue coincidencia, ERP nulo y equivalencia ausente. Una unión izquierda conserva los movimientos. Uso validate='m:1' para que muchas operaciones apunten a una sola fila de dimensión.

attach_cost busca la última vigencia menor o igual al día de la operación por ERP. En el día del cambio ya aplica el costo nuevo. El cliente aclaró que el costo es unitario, global y en MXN. Si falta un costo previo, lo conservo como desconocido; no uso el futuro ni cero.

La conversión usa amount por tasa del día; MXN tiene factor uno. Decimal y HALF_UP determinan el redondeo por registro. Guardo centavos enteros anulables para evitar acumular errores binarios y distinguir cero de costo desconocido.

SQLite guarda dimensiones de producto y tienda, puente, historial, stock, movimientos, tasas y nueve tablas de resultados. La clave del movimiento es canal con fila_id de extracción; conservo además venta_id y order_id con índices únicos. Esto sirve para reconstrucción completa; un incremental productivo requeriría contratos de claves y cambios retroactivos.

Escribo primero una base temporal, compruebo integridad, cierro la conexión y reemplazo la base vigente. Exporto resultados y publico el manifiesto al final con hashes de fuentes, código y artefactos. El validador rechaza un conjunto incompleto. Producción necesitará versiones por ejecución y un puntero a la última publicación completa.

## 4. Cómo explico la rotación y su cobertura

Uso el corte 31 de marzo de 2026 y el semestre del 1 de octubre de 2025 al 31 de marzo de 2026: 182 días. Mi fórmula por SKU es unidades I vendidas entre inventario promedio diario de las mismas tiendas incluidas.

Ejemplo didáctico: si una tienda mantiene 10 unidades un día y 30 el siguiente, el promedio es 20. Si vende 40, la rotación del período es dos veces. Si agrego tiendas, sumo sus existencias promedio y sus unidades; no promedio las rotaciones de cada tienda sin ponderar.

Exijo que cada par tienda–SKU tenga saldo conocido en todos los días del semestre. Solo 36 de 1,268 pares observados cumplen. Esta restricción evita tratar N/A como cero o comparar ventas de toda la cadena con inventario de unas pocas tiendas. El resultado es un ranking parcial y conservador.

El primer SKU del ranking es ERP-PROV-MX-027-B: 29 unidades I y 39.9615 unidades de inventario promedio en una tienda, equivalentes a 0.7257 veces en el semestre. No significa que el producto haya sido repuesto exactamente esa cantidad de veces.

No incluyo online porque desconozco qué almacén cumple los pedidos. No resto unidades E: un egreso puede ser una nota de crédito y el ERP no conserva el momento de una devolución física. Si el denominador es cero, la rotación queda no disponible. Ordeno descendentemente y desempato por SKU.

Si me preguntan cómo ampliar cobertura, propongo recuperar los saldos desconocidos o acordar una regla de estimación y mostrar su sensibilidad por separado. No presento una imputación como observación real ni cambio de regla para mejorar el ranking.

## 5. Cómo explico quiebres y crecimiento

Para quiebres interpreto «más de tres días» como cuatro o más fechas consecutivas con saldo cero por tienda y SKU. Analizo enero a marzo de 2026. Un día sin fila o con N/A rompe la continuidad; dos rachas separadas no se suman como un solo episodio.

Encuentro tres episodios de cuatro días: T015 del 9 al 12 de febrero, T023 del 25 al 28 de enero y T038 del 18 al 21 de marzo. La tabla detallada conserva el SKU y la tabla de tiendas resume productos, episodios y duración máxima. Un snapshot diario en cero es una señal operativa; no prueba agotamiento durante todas las horas del día.

Para crecimiento comparo cada mes con el inmediatamente anterior: (actual / anterior − 1) × 100. Si paso de 100 a 120, el aumento es 20 %. Si la base es cero o falta, el porcentaje no está definido. No salto febrero ausente para comparar marzo contra enero.

Uso abril de 2025 a marzo de 2026 y leo también el mes previo para calcular el primer crecimiento cuando existe. Online no tiene marzo de 2025 y abril queda sin base. La tabla tiene 24 filas, doce por canal.

En físico interpreto I como ingreso y E como egreso; N/P/T no contribuyen a ventas. Esta elección está respaldada por el catálogo SAT, pero el cliente no confirmó un diccionario POS. En online supongo elegibles las órdenes exportadas porque faltan estatus y cancelaciones. Convierto divisas con la tasa del día y mantengo canales separados porque no existe una referencia que descarte doble registro.

## 6. Cómo explico costo y margen negativo

Mi margen estimado es importe total de línea menos cantidad por costo unitario vigente. No multiplico otra vez monto o amount por cantidad. No comparo directamente USD con un costo MXN ni aplico el costo actual a todas las fechas históricas.

Ejemplo didáctico: dos unidades, importe de línea 150 MXN y costo unitario 80 MXN producen 150 − 2 × 80 = −10 MXN. Si el costo cambia de 80 a 90 el día 10, una venta del día 9 usa 80 y una del día 10 usa 90. Un costo del día 15 no puede aplicarse el día 9.

Presento dos vistas. La primera cuenta y suma solo operaciones con margen individual negativo por canal, tienda y SKU. La segunda suma operaciones positivas y negativas del grupo y muestra únicamente acumulados negativos. Una operación negativa no demuestra que todo el producto pierda dinero en el año.

El cálculo usa abril de 2025 a marzo de 2026. Cada vista tiene 80 grupos en esta muestra; que coincidan sus cantidades no las convierte en la misma consulta. Online se etiqueta ONLINE_SIN_ALMACEN para no inventar sucursal. Los costos ausentes quedan visibles en cobertura y excluidos solo del cálculo que los necesita.

La unidad física, impuestos y cargos incluidos en los importes siguen siendo límites: no llamo utilidad neta a este resultado. Tampoco interpreto margen negativo como fraude o error confirmado. Podría haber promociones, bases fiscales distintas o una venta bajo costo autorizada; los archivos no permiten decidir la causa.

Si me piden un caso concreto, uso la operación V00000000 que señalé durante el análisis y consulto sus datos y vigencia en la base. Distingo el diagnóstico histórico de la ventana anual usada en las tablas finales.

## 7. Cómo defiendo AWS y el presupuesto

Propongo una carga diaria: archivos a S3, programación con EventBridge y Step Functions, transformación en Lambda, Parquet curado en S3, esquema en Glue Catalog y consultas en Athena. Uso reportes CSV o BI existente; no contrato una herramienta adicional sin acordar usuarios y costo.

El escenario estima 75 USD mensuales: 35 USD de consumo y reservas operativas más 40 USD de contingencia. Supongo us-east-1, 30 cargas, 50 GB retenidos y 1 TB consultado al mes. El objetivo del reto es aproximadamente 200 USD. No dependo de free tier y dejo explícitas las exclusiones de impuestos, personal, soporte contratado y licencias BI nuevas.

Lambda presupone 4 GB durante 600 segundos por carga: 30 × 600 × 4 = 72,000 GB-segundo al mes. A la tarifa de referencia resulta aproximadamente 1.20 USD más solicitudes. Athena usa 1 TB × 5 USD/TB = 5 USD. El resto combina almacenamiento, solicitudes y reservas documentadas.

No prometo 75 USD con cualquier tráfico. Configuro avisos a 100, 150 y 180 USD, límites de lectura por consulta, particiones mensuales y retención de logs. Las alertas no son un tope automático de gasto. Si el proceso supera tiempo o memoria de Lambda, mido y reestimo antes de adoptar Fargate.

Para producción necesito contratos de extracción, responsables, hora de corte, accesos, retención y un cierre de control firmado. Uso mínimo privilegio, cifrado, bloqueo público de los buckets y logs sin información personal. El repositorio público contiene código y agregados; eso no implica hacer públicos los datos de clientes en S3.

## 8. Cómo demuestro confiabilidad y preparo la entrevista

Mis diez tests sintéticos prueban redondeo, fecha nula, clave duplicada, vigencia exacta y no futura, costo ausente, base cero, mes faltante, racha interrumpida y población de rotación. Debo explicar el error que evita cada control, no solo mostrar que la pantalla dice OK.

El validador independiente recalcula las cuatro respuestas desde las fuentes, con Decimal y búsquedas ordenadas. Contrasta costos por movimiento, MoM, ambos márgenes, ranking y episodios. Comprueba ausencia de columnas personales, hashes e integridad SQLite. Una segunda ejecución desde notebooks/ produce los mismos hashes que la primera: evidencia de idempotencia y rutas estables para esta versión.

También hubo correcciones: la inspección inicial usó quantity cuando el campo real era cantidad; el cierre de SQLite requirió cerrar explícitamente la conexión antes de reemplazar el archivo en Windows. La auditoría detectó estados antiguos en documentación y mejoró tipos monetarios, leyendas y manifiestos. Poder explicar estas correcciones muestra qué se aprendió y qué se controla ahora.

Mi orden de estudio es README → MODELO_ETL → RESPUESTAS_NEGOCIO → pipeline.py → test_pipeline.py y validar_entrega.py → propuesta → AI_LOG. Practico una demo con el ejecutable del entorno y preparo cuatro respuestas breves: por qué no usé un clúster, por qué el ranking es parcial, qué evita un join m:1 y qué falta para pasar a producción.

Ante una pregunta cuya respuesta no consta en la fuente, explico el supuesto y cómo lo validaría. Esa respuesta es defendible; inventar una regla o atribuir una aprobación inexistente no mejora la solución.

## Conclusión

Puedo preparar una defensa basada en claves, ventanas, unidades, cobertura y evidencia de cálculo. Mi objetivo al estudiar es comprender por qué cada decisión evita un error y explicar con claridad qué decisiones del cliente todavía requieren información adicional.
