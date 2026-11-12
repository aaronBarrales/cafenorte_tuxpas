# Análisis exploratorio de CaféNorte

Exploración ejecutada el 7 de noviembre de 2026 sobre todas las filas de las cuatro fuentes. Entrega acordada: antes del martes 10 de noviembre de 2026 a las 12:00 p. m., hora de Ciudad de México. Los diagnósticos financieros están condicionados a las reglas indicadas; no son todavía las cuatro respuestas finales del pipeline.

## Conclusión para avanzar

Las fuentes permiten construir una solución local reproducible, pero requieren reglas explícitas. Las prioridades son la semántica de comprobantes e importes, los mapeos incompletos y la cobertura de inventario. No se deben convertir N/A en cero, mezclar monedas ni excluir operaciones no conciliadas sin reportarlas.

El reporte JSON completo se genera en `outputs/eda_completo.json`; contiene estadísticas y controles, sin datos personales de clientes. Las fuentes originales no se modifican.

## Fuentes y cobertura

| Fuente | Registros | Cobertura de fechas | Claves observadas |
|---|---:|---|---|
| sales.csv | 86,490 | 2024-10-01 a 2026-03-31 | 40 tiendas, 70 SKU POS |
| inventory.json: snapshots | 230,776 | 2025-10-01 a 2026-03-31 | 40 tiendas, 70 SKU ERP, 1,268 pares tienda–SKU |
| inventory.json: catálogo | 70 productos | Costos desde 2024-10-01 | 282 vigencias, 6 categorías |
| inventory.json: mapeos | 65 | Sin fechas de vigencia | POS, ERP y handle |
| ecommerce_orders.parquet | 9,947 | 2025-04-01 a 2026-03-31 | 33 handles, 3 monedas |
| exchange_rates.csv | 730 | 2025-04-01 a 2026-03-31 | 365 fechas por USD y EUR |

El inventario se generó el 23 de abril de 2026, según metadata, pero sus snapshots terminan en marzo. La fecha de generación no extiende la cobertura analítica.

## Calidad de ventas físicas

- No hay campos vacíos, espacios en extremos, IDs repetidos ni duplicados exactos en la fuente actual.
- Las 86,490 fechas actuales son interpretables como `DD/MM/YYYY HH:MM`. El formato original tenía segundos; no se reconstruye esa precisión perdida. La procedencia del cambio de archivo sigue abierta.
- Las cantidades son enteros positivos entre 1 y 16. Los montos son positivos, entre 15.67 y 9,714.87 MXN. Las diferencias de magnitud por sí solas no prueban errores.
- Todos los identificadores cumplen los patrones observados y las 40 tiendas existen en el catálogo.
- Hay registros en los 547 días del período. De 21,880 combinaciones teóricas tienda–día, 476 no tienen ventas registradas. Sin calendario operativo no se puede concluir si son cierres, ausencia real de ventas o extracción incompleta.
- El diagnóstico de `monto / cantidad` dentro de cada SKU y solo para I no encontró observaciones fuera de 1.5 veces el rango intercuartílico, usando cuartiles por observación más cercana. Esto no valida precios, descuentos ni costos; solo describe esa regla estadística en la muestra.

### Comprobantes y sensibilidad de importes

| Tipo | Filas | Unidades registradas | Suma de monto original MXN |
|---|---:|---:|---:|
| I | 82,518 | 127,241 | 29,503,069.84 |
| E | 3,079 | 4,843 | 1,140,985.33 |
| N | 288 | 407 | 100,579.56 |
| P | 451 | 692 | 160,501.27 |
| T | 154 | 200 | 42,117.82 |

Todos tienen signo positivo. Sumar todo da 30,947,253.82 MXN; usar solo I da 29,503,069.84; usar I menos E da 28,362,084.51. Son **escenarios de clasificación**, no ventas netas confirmadas. Demuestran que la decisión afecta materialmente las cifras. Un egreso financiero tampoco confirma que las unidades regresen físicamente al inventario.

## Inventario y costos

No hay claves de snapshot duplicadas ni conflictivas, y todos los SKU y tiendas de snapshots existen en sus catálogos. Los 70 productos y las 40 tiendas tienen al menos un snapshot. Los códigos de producto y tienda de los catálogos son únicos.

### Valores desconocidos y cobertura

- **4,417 snapshots contienen el texto N/A**: son existencias desconocidas, aunque no sean null de JSON. Hay 226,359 cantidades numéricas válidas, todas enteras y no negativas; de ellas 11,726 son cero. Máximo observado: 153 unidades.
- Los 1,268 pares tienda–SKU observados tienen una fila en cada uno de los 182 días: no hay huecos de fila dentro de esos pares. La cobertura numérica por par va de 172 a 182 días por los N/A.
- Cada tienda tiene entre 25 y 40 SKU con snapshots, frente a 70 productos en el catálogo. Sin surtido por tienda y vigencias no se deben asumir 70 productos activos en cada sucursal ni interpretar los pares ausentes como stock cero.

### Cruce de ventas e inventario

Para los **27,288 registros I** entre octubre de 2025 y marzo de 2026, usando solo el mapeo exacto:

| Resultado del cruce por fecha, tienda y SKU | Filas I |
|---|---:|
| Snapshot numérico | 10,515 |
| SKU ERP conocido, pero sin snapshot del par tienda–SKU | 12,687 |
| Sin relación exacta hasta ERP | 3,873 |
| Snapshot con N/A | 213 |
| Total | 27,288 |

Entre las filas con snapshot numérico, 565 tienen stock cero y venta el mismo día. No constituye por sí solo una contradicción: un saldo de cierre puede quedar en cero después de la venta. Hay que conocer el momento y la definición del snapshot.

La ausencia de snapshots para 12,687 registros I con ERP conocido afecta el denominador de rotación. No se puede sumar indiscriminadamente ventas de todas las tiendas y dividir por inventario de un surtido parcial.

### Episodios observados de cero

Sin rellenar N/A ni fechas y exigiendo días calendario consecutivos, se encontraron tres episodios demostrables de cero por más de tres días:

| Tienda | SKU ERP | Inicio | Fin | Días |
|---|---|---|---|---:|
| T015 | ERP-PROV-MX-014-D | 2026-02-09 | 2026-02-12 | 4 |
| T023 | ERP-PROV-MX-046-A | 2026-01-25 | 2026-01-28 | 4 |
| T038 | ERP-PROV-MX-040-A | 2026-03-18 | 2026-03-21 | 4 |

Todos caen en enero–marzo de 2026. Los valores desconocidos podrían ocultar otros episodios: no afirmar que tres sea el total real de quiebres del negocio. Tampoco un snapshot de cierre demuestra indisponibilidad durante todo el día.

### Historial de costos

Los 70 productos tienen historial; todos empiezan el 1 de octubre de 2024. Hay 282 entradas, sin claves producto–vigencia duplicadas ni costos no positivos o fechas inválidas. Los costos registrados van de 7.73 a 478.30 MXN y las últimas modificaciones llegan al 30 de marzo de 2026. No se detectaron campos vacíos en las entradas de costos.

Hay 23 nombres repetidos en el catálogo; un nombre no identifica unívocamente un SKU. No se especifican unidad de medida, impuestos ni si los costos cambian por tienda. La regla candidata es usar la última vigencia no posterior a cada operación, conservando desconocido si no hay costo aplicable.

## Conciliación de productos

### POS y ERP

De los 70 SKU vendidos, cinco no tienen fila en el mapeo: CN-00001, CN-00011, CN-00021, CN-00031 y CN-00041. Otros cinco tienen ERP nulo: CN-00006, CN-00016, CN-00026, CN-00036 y CN-00046.

| Estado de todas las filas físicas | Filas |
|---|---:|
| Relación exacta hasta ERP | 74,141 |
| Sin fila de mapeo | 6,217 |
| Fila de mapeo con ERP nulo | 6,132 |

No hay duplicados entre claves no nulas del mapeo ni SKU ERP informados fuera del catálogo. Existen diez productos del catálogo sin enlace ERP informado en el mapeo; la coincidencia de números es una pista, no una relación confirmada por sí sola.

### Shopify y ERP

| Estado de filas de e-commerce | Filas |
|---|---:|
| Handle y ERP exactos hasta catálogo | 6,959 |
| Handle conocido, pero ERP nulo | 1,139 |
| Handle sin mapeo | 1,849 |

Por tanto, **2,988 filas de e-commerce no llegan a ERP con la fuente de mapeo actual**. Las seis propuestas por nombre y sufijo, y los cuatro enlaces incompletos con handle informado, siguen documentados como inferidos y sin aplicar en [conciliación de handles](conciliacion_handles.md).

## E commerce y moneda

Los 9,947 order_id son únicos y no hay duplicados exactos. Hay un producto por fila, pero eso no demuestra que un pedido real solo tenga una línea: la granularidad debe confirmarse. Las cantidades son enteros positivos entre 1 y 15. No hay estados de pago, cancelación o reembolso en el archivo.

| Moneda | Filas | Suma de amount original |
|---|---:|---:|
| MXN | 6,942 | 2,912,430.74 |
| USD | 2,535 | 61,796.46 |
| EUR | 470 | 9,885.86 |

Estas sumas son controles por moneda, no se suman entre sí directamente. Los importes están almacenados como double; para dinero se propone convertir sus representaciones decimales y fijar una regla explícita de redondeo.

El RFC está nulo en 8,462 filas; no es necesario para las cuatro métricas y su ausencia no prueba error fiscal. La necesidad de factura y del RFC debe confirmarse con el proceso de negocio. Los demás campos de clientes/envío están poblados, pero no se han validado sus valores contra fuentes externas ni son necesarios para las métricas. No se reproducen datos personales en este informe.

El Parquet tiene fechas como texto sin zona horaria. No tiene precio de lista, vigencias de tarifa ni columnas independientes de descuento, impuestos o envío; falta confirmar qué incluye amount. No hay almacén o tienda de cumplimiento, por lo que no se debe atribuir una venta online a una sucursal a partir de la ciudad del cliente.

## Tipos de cambio

Las 730 filas tienen fechas y tasas válidas y positivas, sin nulos ni claves fecha–moneda duplicadas. Hay una tasa USD y una EUR para cada uno de los 365 días cubiertos. Todas las órdenes extranjeras tienen tasa del mismo día de su fecha registrada; no se requiere rellenar faltantes en esta muestra.

| Moneda | Tasa mínima | Tasa máxima |
|---|---:|---:|
| USD | 17.1295 | 18.8253 |
| EUR | 20.3770 | 22.0000 |

EUR aparece exactamente en 22.0 durante 63 fechas: preguntar por redondeo, límites o metodología; no declararlo error sin una fuente de referencia. La denominación rate_to_mxn sugiere pesos por unidad extranjera, pero deben confirmarse proveedor, fecha contable y convención. No se validaron tasas contra el mercado.

Como diagnóstico, multiplicar amount por la tasa del día produce 1,101,529.809677 MXN para las filas USD y 214,922.160303 MXN para las EUR, sin redondeos intermedios. Son controles bajo una regla propuesta, no ingresos netos contables confirmados.

## Viabilidad de las cuatro preguntas

| Pregunta | Ventana propuesta para implementar | Decisiones y límites |
|---|---|---|
| Top 10 de rotación | 2025-10-01 a 2026-03-31 | Unidades físicas elegibles / inventario diario promedio del mismo conjunto de tienda–SKU. Reportar cobertura, N/A y ventas sin inventario; no mezclar e-commerce sin conocer su almacén. No presentar un ranking global completo si solo representa surtido observado. |
| Quiebres mayores de 3 días | 2026-01-01 a 2026-03-31 | Días calendario consecutivos con stock cero; N/A interrumpe evidencia y queda reportado. Más de 3 significa al menos 4 días. |
| MoM por canal | 2025-04-01 a 2026-03-31 | Comparar cada mes contra el anterior con MXN conciliado. E-commerce no tiene marzo de 2025: abril debe quedar sin base previa, no crecimiento cero. Físico sí tiene ese antecedente. |
| Margen negativo y tiendas | Cobertura disponible por fuente, con fechas explícitas | Cálculo por registro con costo vigente; agrupar operación negativa y margen agregado por separado. E-commerce queda como canal sin tienda identificada. Diferenciar costo ausente, margen cero y margen negativo. |

Estas ambigüedades de métricas se resolverán en el README conforme al reto, sin hacer depender la entrega de que el cliente elija la fórmula. Las consultas al cliente se enfocan en la semántica y completitud de las fuentes.

### Diagnóstico de margen físico

Con comprobantes I, mapeo exacto y el supuesto de monto total y costo unitario comparable: 70,721 de 82,518 registros I tienen costo; 11,797 quedan sin costo por conciliación. Entre los que tienen costo, 2,369 registros dan margen negativo en la cobertura de 18 meses. No implica 2,369 productos ni 2,369 tiendas, ni define por sí solo el resultado agregado por SKU. El caso V00000000 está explicado en [casos de margen](casos_margen.md).

## Validación histórica

Conservo el diagnóstico y sus huellas como evidencia de su etapa. Los seis controles de conservación y las diez comprobaciones independientes de esa ejecución pasaron; no representan una validación de versiones posteriores. Retiré los auxiliares exploratorios de la estructura final. Los notebooks conservan la exploración y los comandos actuales del ETL y sus pruebas están en el README principal.

### Identificación de fuentes analizadas

| Archivo | SHA-256 |
|---|---|
| sales.csv | b62180fc201e4dc01c7e58f781c0b5f55cdf003095d29ad714e708be85b80bb1 |
| inventory.json | 2355c6cab9ff00a707b5505a464a8f7e1a9bf5a2aa6c7a2b6b008f5299c8eada |
| ecommerce_orders.parquet | 00c560b39425fe7f0088fbe20c66c2b8861d10c2c7006ba6e7335cdd6dfc856e |
| exchange_rates.csv | a0e827ec1e048cf397584eca3d692cb5b5b1f6b477fb78efca2fdbd2f488bddf |

Preguntas priorizadas: [PREGUNTAS_CLIENTE.md](../03_negocio/PREGUNTAS_CLIENTE.md). Plan hasta la entrega: [PLAN_ENTREGA.md](../04_seguimiento/PLAN_ENTREGA.md).

## Conclusión

Conservo este diagnóstico integral como antecedente de calidad, cobertura y conciliación entre fuentes. Sus resultados dependen de los hashes y supuestos registrados; no sustituyen las métricas finales ni validan automáticamente la versión actual de sales.
