# Hallazgos importantes

Actualizado: 7 de noviembre de 2026. Mantener entradas breves; distinguir hechos de relaciones o reglas propuestas.

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
| Los candidatos ERP son 013-B, 030-C, 031-A, 032-D, 041-D y 052-C, con prefijo ERP-PROV-MX-. | Detalle en [conciliación de handles](docs/conciliacion_handles.md). No unir solo por nombre: hay nombres repetidos. |
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

Detalle: [EDA completo](docs/EDA_COMPLETO.md). Preguntas: [PREGUNTAS_CLIENTE.md](PREGUNTAS_CLIENTE.md), 60 consultas con diez prioritarias. Entrega: antes del martes 10 de noviembre de 2026 a las 12:00 p. m., hora CDMX.

Detalle y preguntas: [DUDAS.md](DUDAS.md). Estado y próximos pasos: [CONTINUIDAD.md](CONTINUIDAD.md).
