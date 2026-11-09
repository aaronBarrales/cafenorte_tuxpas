# Exploración inicial de e commerce

La revisión integral posterior está en [EDA completo](EDA_COMPLETO.md): fechas, duplicados, claves hasta ERP, moneda y límites. De 8,098 filas con handle conocido, 1,139 tienen ERP nulo; solo 6,959 llegan a ERP por enlace exacto.

## Fuente y estructura

`datos/ecommerce_orders.parquet` contiene una tabla de 9,947 filas y 11 columnas. Parquet es un formato binario por columnas que conserva tipos; CSV es una representación textual de filas y columnas. Para el pipeline se conservará la fuente Parquet y el CSV servirá para inspección manual. Referencia: [Apache Parquet](https://parquet.apache.org/).

| Columna | Tipo en Parquet | Nulos |
|---|---|---:|
| order_id | large_string | 0 |
| fecha | large_string | 0 |
| product_handle | large_string | 0 |
| cantidad | int64 | 0 |
| amount | double | 0 |
| currency | large_string | 0 |
| customer_name | large_string | 0 |
| customer_email | large_string | 0 |
| customer_rfc | large_string | 8,462 |
| shipping_city | large_string | 0 |
| shipping_address | large_string | 0 |

Las fechas de texto van de `2025-04-01 03:12:00` a `2026-03-31 22:31:00`; falta validar zona horaria, granularidad, duplicados y cobertura temporal. Monedas: MXN (6,942 filas), USD (2,535) y EUR (470). No sumar amount entre monedas sin conciliarlas.

El archivo contiene importe y cantidad de las órdenes, pero no campos separados de precio de lista, tarifa con vigencia, impuestos o descuentos. Por tanto, entre las fuentes entregadas revisadas no se identificó una lista histórica de precios fijados. Los importes de operaciones no explican por sí solos su regla de fijación.

## Handles y cobertura de mapeos

Hay 33 handles distintos. De ellos, 27 tienen correspondencia exacta en `inventory.sku_mappings`, que cubre 8,098 filas. Los otros 6 representan 1,849 filas, que deben conservarse como pendientes de conciliación.

| Handle sin correspondencia exacta | Filas |
|---|---:|
| gourmet-cafe-molido-041 | 297 |
| molinillo-mercancia-030 | 319 |
| selección-cafe-molido-013 | 305 |
| termo-mercancia-031 | 317 |
| americano-cafe-grano-032 | 279 |
| americano-cafe-molido-052 | 332 |

Los sufijos 013, 030, 032 y 052 coinciden con las terminaciones de `CN-00013`, `CN-00030`, `CN-00032` y `CN-00052`, cuyos handles están nulos en el mapeo. Son candidatos para investigar, no enlaces confirmados: no se ha demostrado que el sufijo sea una clave contractual ni se han validado nombre, variante y unicidad para recuperar correspondencias.

Esto impide sostener sin comprobación la regla «handle nulo = producto sin ventas online». Para el producto 015 no apareció un handle terminado en `-015`; eso tampoco prueba ausencia de ventas, porque la equivalencia por sufijo no está confirmada. Parquet no contiene SKU POS o ERP alternativo que permita resolverlo directamente.

## Exportación para Excel

Se generó `outputs/ecommerce_orders.csv` con las 9,947 filas y las 11 columnas, en UTF-8 con BOM, delimitado por coma y con encabezados. Se verificó cada fila contra la serialización esperada de Parquet y se comprobó que el original no cambiara. Su SHA-256 es `00c560b39425fe7f0088fbe20c66c2b8861d10c2c7006ba6e7335cdd6dfc856e`.

Los nulos se exportan como celdas vacías; CSV no conserva los tipos ni la distinción entre null y cadena vacía. Parquet sigue siendo la fuente de referencia. El CSV completo incluye los campos de clientes del origen y permanece local, excluido de Git mediante `/outputs/`.

En Excel, usar **Datos → Desde texto/CSV**, elegir UTF-8 y delimitador coma. Revisar los tipos antes de cargar: identificadores como texto, y `amount` con punto decimal usando la configuración regional adecuada. Para conservar el original, guardar cualquier edición con otro nombre.

## Reproducción

Desde la raíz del proyecto, con Python 3.12 usado en esta exploración:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-exploracion.txt
.\.venv\Scripts\python.exe scripts/exportar_ecommerce.py
.\.venv\Scripts\python.exe scripts/perfil_ecommerce.py
```

El stack final del pipeline sigue pendiente. En el entorno de esta sesión, la instalación requirió permisos de ejecución adicionales y el almacén de certificados del sistema mediante `pip --use-feature=truststore`; no se desactivó la verificación HTTPS.

## Conclusión

Conservo la revisión de estructura, monedas y cobertura de handles como antecedente de e-commerce. La exportación facilita su consulta, pero no resuelve los mapeos incompletos ni confirma el significado contable de los importes.
