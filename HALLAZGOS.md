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
| El CSV local de sales cambió de hash y de formato de fechas; ahora usa DD/MM/YYYY HH:MM. | Adaptar lectura y revisar procedencia; no sobrescribir la fuente. |

Detalle y preguntas: [DUDAS.md](DUDAS.md). Estado y próximos pasos: [CONTINUIDAD.md](CONTINUIDAD.md).
