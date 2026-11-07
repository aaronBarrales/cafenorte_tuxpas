# Exploración inicial de sales

## Alcance y reproducción

Perfil de la fuente original, sin limpieza ni filtros de negocio. No constituye aún el cálculo de ventas netas ni las respuestas del reto.

Desde la raíz del repositorio, con Python 3 y sin dependencias externas:

```powershell
python scripts/perfil_sales.py
```

El script imprime JSON, conserva los importes con `Decimal` y separa sus sumas por tipo de comprobante y moneda. No modifica la fuente.

Archivo: `datos/sales.csv`. SHA-256 analizado: `87628a584d30a353f3bcc9dbe20c2d8f1e55c80a0036ecee88e76fce61031276`.

## Hallazgos

| Revisión | Resultado |
|---|---|
| Filas | 86,490 |
| Columnas | 8 |
| Tiendas distintas | 40 |
| SKUs distintos | 70 |
| Primera fecha y hora | 2024-10-01 07:04:36 |
| Última fecha y hora | 2026-03-31 21:08:44 |
| Meses con registros | 18 |
| Vacíos o espacios en blanco | 0 en cada columna |
| IDs distintos | 86,490 |
| IDs repetidos | 0 |
| Filas duplicadas exactas adicionales | 0 |
| Fechas con formato inválido | 0 |
| Cantidades o importes no numéricos o no finitos | 0 |
| Cantidades o importes negativos o cero | 0 |
| Monedas | MXN |

Que un mes tenga registros no demuestra que todos sus días y tiendas estén completos. Tampoco la ausencia de nulos confirma la exactitud de las cifras.

## Tipo de comprobante

| Código | Filas | Suma del monto original en MXN |
|---|---:|---:|
| I | 82,518 | 29,503,069.84 |
| E | 3,079 | 1,140,985.33 |
| N | 288 | 100,579.56 |
| P | 451 | 160,501.27 |
| T | 154 | 42,117.82 |

Los cinco grupos tienen cantidades y montos positivos. Estas sumas son controles de origen; su significado comercial depende de resolver D001 y D002 en [DUDAS.md](../DUDAS.md). No se han aplicado signos ni exclusiones.

## Columnas y asuntos pendientes

| Columna | Evidencia o revisión pendiente |
|---|---|
| venta_id | Único en esta muestra; confirmar qué identifica y su estabilidad. |
| fecha_hora | Todas las filas cumplen el formato; zona horaria desconocida. |
| tienda_id | 40 valores; validar existencia y formato contra inventario o catálogo. |
| sku | 70 valores; validar cobertura y normalización contra las otras fuentes. |
| cantidad | Numérica y positiva; confirmar unidad e interpretación de devoluciones. |
| monto | Numérico y positivo; confirmar total de línea, impuestos y descuentos. |
| moneda | MXN en todas las filas; falta revisar monedas de e-commerce. |
| tipo_comprobante | Cinco códigos; falta confirmar semántica y efecto por métrica. |

## Siguientes pasos

La revisión posterior del SKU `CN-00003` confirmó que el cociente `monto / cantidad` varía incluso dentro de los comprobantes tipo `I`. El detalle y las limitaciones se registran en D006 de [DUDAS.md](../DUDAS.md). La captura del autor contiene cuatro registros tipo `N`, con diferentes tiendas y fechas, y no demuestra por sí sola una evolución temporal del precio de venta.

En inventario se identificó `catalogo.productos.cost_history`, con costos y fechas de vigencia, y `tiendas_info.timezone`. Estos campos permiten avanzar en el estudio de márgenes y zonas horarias, sujeto a validar claves, cobertura y semántica. Un historial de costos no equivale a un historial de precios de venta.

1. Registrar una interpretación explícita de comprobantes, cantidades e importes.
2. Revisar cobertura por día y tienda y posibles valores atípicos por SKU, sin descartar automáticamente precios o cantidades extremos.
3. Comparar claves de tienda y SKU contra inventario y órdenes de e-commerce.
4. Identificar costos y su vigencia para calcular márgenes sin mezclar bases distintas.
5. Fijar una fecha de corte y ventanas tras revisar la cobertura conjunta.
6. Implementar transformaciones con controles de conciliación por tipo, moneda y período, y pruebas de las reglas elegidas.
