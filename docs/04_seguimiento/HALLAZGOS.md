# Hallazgos importantes

Actualizado: 8 de noviembre de 2026. Mantener entradas breves; distinguir hechos de relaciones o reglas propuestas. Las cifras del EDA integral son antecedentes; su hash de sales no coincide con la fuente actual.

## Notebook de ventas actualizado

Resultados de [01_sales.ipynb](../../notebooks/01_sales.ipynb), ejecutado sobre la fuente actual. Esta exploración es aislada: no consulta ni cruza las otras fuentes. Interpretación e importancia en el [informe de resultados de sales](../02_exploracion/resultados_sales.md).

| Hallazgo | Impacto o estado |
|---|---|
| Las 86,490 fechas se interpretan con DD/MM/YYYY HH:MM; cobertura del 1 de octubre de 2024 al 31 de marzo de 2026. | El notebook usa únicamente este formato por mi decisión; formatos diferentes quedan como NaT. |
| Hay 476 combinaciones tienda–día sin registros; no faltan meses completos entre los extremos de la fuente. | No demuestra ventas cero ni cierres; se requiere calendario operativo para explicar los huecos. |
| No se detectaron nulos, duplicados exactos, IDs repetidos, números infinitos o formatos de identificadores fuera de los patrones observados. | Son controles de estructura y consistencia, no validación comercial. |
| No hay importes unitarios I señalados por la regla 1.5×IQR dentro de moneda–SKU; se evaluaron 82,518 filas. | No valida precios ni descarta otras anomalías. |
| T037 registra el mayor importe acumulado I: 812,902.26 MXN. Las diez primeras tiendas concentran 26.28% del importe I. | Toda la cobertura; importes registrados, no ventas netas ni margen. |
| Hay 201 grupos de misma tienda y fecha/hora con SKU diferentes: 402 filas. En 186 grupos también coinciden moneda y comprobante (372 filas). | Compatible con compras divididas por producto, pero no confirma mismo cliente o ticket: la hora tiene precisión de minutos. Q11 solicita clave real de ticket y significado de venta_id; no se fusionaron registros. |
| CN-00039 tiene el mayor importe I acumulado: 1,481,814.86 MXN, con 1,862 unidades. | Ranking por importe de la fuente aislada; no implica mayor rotación o rentabilidad. |
| Octubre de 2025 presenta el mayor importe mensual I (1,723,372.26 MXN); febrero de 2025, el menor (1,487,252.95 MXN). | No explica causas; los meses tienen distinta duración y falta confirmar completitud operativa. |
| El hash actual de sales difiere del reporte histórico, aunque coinciden conteo e importe total. | Revisar procedencia antes de considerar vigente la validación histórica; no se modificó la fuente. |

| Hallazgo | Impacto o estado |
|---|---|
| Sales: 86,490 filas, 40 tiendas, 70 SKUs y moneda MXN. | Perfil inicial sin vacíos ni IDs repetidos; no prueba exactitud comercial. |
| Comprobantes I, E, N, P y T con montos positivos. | Confirmar significado y signo antes de calcular ventas netas. |
| El inventario guarda historial de costos; ninguna fuente revisada incluye listas históricas de precios de venta. | No confundir costo, monto registrado y precio de lista. |
| Un mismo SKU tiene distintos cocientes monto/cantidad. | No se conoce la causa; no prueba descuentos ni errores. |
| V00000000: una unidad de CN-00015 en T033 por 355.43 MXN, frente a costo vigente propuesto de 466.56 MXN. | Margen candidato: −111.13 MXN, condicionado a bases comparables. |
| 38 de 65 mapeos no tienen handle. | No implica que el producto no se venda online; handle no es descripción. |
| E-commerce: 9,947 filas, 33 handles y monedas MXN, USD y EUR. | Normalizar monedas antes de sumar importes. |
| Seis handles no aparecen en el mapeo: representan 1,849 filas. | Conservar y reportar pendientes de conciliación. |
| Nombre normalizado + número del SKU ERP identifica un candidato para cada uno de esos seis handles. | Regla consistente con 23/23 mapeos completos; relaciones inferidas, aún sin aplicar. |
| Los candidatos ERP son 013-B, 030-C, 031-A, 032-D, 041-D y 052-C, con prefijo ERP-PROV-MX-. | Detalle en [conciliación de handles](../05_antecedentes/conciliacion_handles.md). No unir solo por nombre: hay nombres repetidos. |
| Cuatro mapeos con handle tienen ERP nulo: POS 006, 026, 036 y 046. | Reconocer el handle no garantiza llegar a costos del ERP. |
| Inventario incluye zonas horarias por tienda y snapshots diarios, sin movimientos transaccionales. | Confirmar zona del POS; ausencia de snapshot no equivale a stock cero. |
| Sales original llega a marzo de 2026; e-commerce abarca abril de 2025 a marzo de 2026. | Fijar corte con cobertura conjunta, no con la fecha de ejecución. |
| El CSV local de sales cambió de hash y de formato de fechas; ahora usa DD/MM/YYYY HH:MM. | Lectura adaptada; procedencia pendiente, sin modificar la fuente. |

## Exploración completa

| Hallazgo | Impacto o estado |
|---|---|
| Inventario: 230,776 snapshots; 4,417 contienen N/A. | Desconocido, no cero. |
| Los 1,268 pares tienda–SKU tienen filas en los 182 días; cada tienda muestra de 25 a 40 SKU. | Hay surtido parcial por tienda; no confundir fila ausente con stock cero. |
| 12,687 filas I del semestre tienen ERP conocido pero ningún snapshot de su tienda–SKU. | La rotación exige alinear ventas e inventario y declarar cobertura. |
| 565 filas I coinciden con stock cero el mismo día. | Puede ser saldo de cierre; no prueba inconsistencia. |
| Se observaron tres secuencias de cuatro días en cero, en T015, T023 y T038, dentro de enero–marzo de 2026. | Evidencia parcial; N/A puede ocultar otras secuencias. |
| POS: 12,349 filas no llegan a ERP; e-commerce: 2,988 tampoco. | No confundir handle conocido con costo conciliado. |
| Los 70 productos tienen costos desde 2024-10-01: 282 vigencias sin conflictos de fecha detectados. | Falta confirmar unidad/base de costo. |
| 2,369 filas I con enlace exacto dan margen candidato negativo en 18 meses; 11,797 filas I carecen de costo conciliado. | Diagnóstico condicionado, no resultado global definitivo. |
| FX: 730 tasas positivas, una por día y moneda; ninguna orden extranjera queda sin tasa del día. | Confirmar convención y política de redondeo. |
| EUR = 22.0 en 63 fechas. | Preguntar metodología; no declararlo error sin evidencia. |
| E-commerce empieza en abril de 2025. | Su primer MoM no tiene mes anterior; no sustituirlo por cero. |

Detalle: [EDA completo](../05_antecedentes/EDA_COMPLETO.md). Preguntas: [PREGUNTAS_CLIENTE.md](../03_negocio/PREGUNTAS_CLIENTE.md), 60 consultas con diez prioritarias. Entrega: antes del martes 10 de noviembre de 2026 a las 12:00 p. m., hora CDMX.

Detalle y preguntas: [DUDAS.md](../03_negocio/DUDAS.md). Estado y próximos pasos: [CONTINUIDAD.md](CONTINUIDAD.md).

## Exploración aislada actual de exchange_rates

En [mi informe de tasas](../02_exploracion/resultados_exchange_rates.md) y [04_exchange_rates.ipynb](../../notebooks/04_exchange_rates.ipynb) documento 730 filas: una por día y moneda (USD/EUR), del 2025-04-01 al 2026-03-31, sin huecos internos, claves duplicadas ni tasas inválidas, cero o negativas. No consulto ni cruzo otras fuentes; no afirmo cobertura de pedidos. EUR = 22.0 en 63 fechas requiere explicación metodológica. Conecto convención y procedencia con Q10, fines de semana y vigencia con Q38, repetición con Q39 y precisión/redondeo con Q40; siguen pendientes de respuesta.

## Conclusión

Distingo los hallazgos estructurales de las interpretaciones comerciales pendientes. Uso este resumen para orientar los siguientes pasos, sin confundir coincidencias temporales, mapeos propuestos o márgenes candidatos con hechos confirmados del negocio.
