# Modelo y reglas de la entrega

Elijo pandas para leer CSV, JSON y Parquet y SQLite para persistir un modelo consultable sin servidor. El tamaño cabe en memoria y no requiere un clúster. Conservo las fuentes y sus columnas comerciales originales; excluyo nombres, correos, RFC y direcciones incluso de la lectura de Shopify.

## Tablas y granularidad

Leyenda: cada fila de la tabla describe una relación SQLite; claves y medidas son nombres técnicos, no unidades físicas confirmadas.

| Tabla | Grano y clave | Función |
|---|---|---|
| dim_producto | Un sku_erp | Nombre y categoría |
| dim_tienda | Una tienda_id | Ubicación y zona declarada |
| puente_producto | Una equivalencia entregada | SKU POS y handle hacia ERP; sin inferencias |
| historial_costo | sku_erp, vigencia | Costo unitario global MXN hasta siguiente cambio |
| fact_stock | dia, tienda_id, sku_erp | Snapshot diario con saldo original y stock_num |
| fact_movimiento | canal, fila_id de extracción | Un registro comercial conservado, con conversión y costo |
| tasas | dia, currency | MXN por unidad de divisa |
| rotacion_top10 | sku_erp | Ranking del semestre en población cubierta |
| quiebres_tiendas | tienda_id | Resumen de productos, episodios y duración máxima |
| quiebres_episodios | tienda, SKU, inicio | Ceros consecutivos observados |
| crecimiento_mensual | canal, mes | Importe, base previa y crecimiento porcentual |
| margen_negativo_operaciones | canal, tienda, SKU | Operaciones individuales negativas acumuladas |
| margen_negativo_acumulado | canal, tienda, SKU | Resultado total negativo del período |
| cobertura | canal, estado_mapeo | Conteos de excepciones y enlaces exactos |

## Derivaciones y tratamientos

`dia` interpreta la fecha original sin inventar zona horaria. `stock_num` convierte cantidad_en_stock a número; N/A permanece desconocido. `sku_erp` viene exclusivamente del puente; `estado_mapeo` distingue sin equivalencia, ERP nulo y exacto. Una clave desconocida se conserva y no recibe costo cero. Un duplicado en una dimensión detiene la carga.

`vigencia` interpreta fecha_vigencia. `costo_mxn` es el costo unitario confirmado por la respuesta compartida; tomo el último costo menor o igual al día del movimiento. `rate_to_mxn` viene de la tasa de ese día y moneda; MXN usa 1. Si falta una tasa extranjera detengo la carga. `importe_original` copia monto o amount, tratados como total de línea. `importe_centavos` aplica conversión con Decimal y ROUND_HALF_UP por registro. `signo_ingreso` aplica +1 a I, −1 a E y cero a N/P/T; órdenes online usan +1. `ingreso_centavos` multiplica ese signo por el importe convertido. `costo_centavos` multiplica cantidad por costo unitario vigente y redondea a centavos; queda ausente sin costo. `margen_centavos` resta costo a importe únicamente en I y órdenes, sin inferir restitución física desde E.

`fila_id` identifica la posición dentro de cada extracción; no reemplaza una clave incremental productiva. Conservo venta_id y order_id. La demo reconstruye el modelo completo en una base temporal, comprueba integridad y reemplaza la base vigente al cerrar la conexión. Publico el manifiesto al final con huellas de código, fuentes y artefactos. El validador rechaza un conjunto incompleto o alterado; una interrupción entre exportaciones exige regenerarlo. Producción debe aislar las ejecuciones por prefijo y apuntar a una versión completa. Guardo costo y margen en centavos enteros con nulos explícitos.

## Ventanas y límites

Mi corte es el último día observado común a ventas, online e inventario: 31 de marzo de 2026. Semestre: octubre de 2025 a marzo de 2026; trimestre calendario: enero a marzo de 2026; año: abril de 2025 a marzo de 2026. MoM calcula también marzo de 2025 si existe para disponer de base previa: online no la tiene y abril queda sin crecimiento calculable.

Rotación es unidades I divididas entre la suma del inventario promedio diario de las mismas tiendas por SKU. Incluyo únicamente pares con todos los días del semestre conocidos; excluyo online por falta de almacén. No descuento cantidades E porque no prueban devoluciones físicas. Stock cero como denominador produce desconocido, nunca infinito. Los empates se ordenan por SKU ascendente. Es un ranking parcial bajo equivalencia de unidades, no de toda la cadena.

Quiebres exige al menos cuatro fechas consecutivas con cero en el trimestre. Un hueco o N/A rompe el episodio; reporto si toca bordes de ventana. No afirmo agotamiento durante 24 horas ni fechas reales fuera del intervalo observado. MoM es (mes/base anterior − 1) × 100 en MXN; no salto meses ausentes ni divido entre cero. Mantengo canales separados porque no existe referencia para verificar doble registro.

Margen negativo muestra tanto operaciones individuales como grupos cuyo margen total es negativo, para no confundir una promoción puntual con pérdida agregada. Uso el mismo año del crecimiento. Online se etiqueta ONLINE_SIN_ALMACEN y no se atribuye a una sucursal. Impuestos, descuentos, gastos y unidad física siguen siendo límites de interpretación. No hay estado de pago o cancelación online: trato las órdenes exportadas como elegibles para el escenario, sin llamarlas ingreso contable certificado.

## Conclusión

Persisto un modelo reproducible que permite rastrear cálculos y excepciones, aplico el costo confirmado y mantengo explícitos los supuestos que condicionan las cuatro respuestas.
