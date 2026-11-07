# Historial de costos de ERP PROV MX 057 C

## Identificación

- SKU ERP: `ERP-PROV-MX-057-C`.
- Nombre exacto en el catálogo: `Premium Cafe Grano`.
- Categoría: `cafe_grano`.
- SKU POS según `sku_mappings`: `CN-00057`.
- Handle según el mismo mapeo: `premium-cafe-grano-057`.

La búsqueda encontró una entrada de producto y una correspondencia en los mapeos para esta clave ERP. Este es un producto diferente de `CN-00003`, usado en la captura de la revisión anterior.

## Historial encontrado

Fuente: `datos/inventory.json`, dentro de `catalogo.productos`, producto con `sku_erp` igual a `ERP-PROV-MX-057-C`, arreglo `cost_history`.

| Fecha de vigencia | costo_mxn | Proveedor |
|---|---:|---|
| 2024-10-01 | 87.40 | Jurado, Sanches y Tirado |
| 2024-11-08 | 86.31 | Quezada y Blanco S. R.L. de C.V. |
| 2024-11-14 | 85.94 | Preciado e Hijos |
| 2025-02-01 | 90.56 | Zayas-Henríquez A.C. |
| 2025-11-30 | 96.23 | Girón-Velásquez |

Estos valores son **costos en MXN**, no precios de venta. No confirman impuestos, unidad de medida ni si el costo incluye gastos adicionales. El catálogo no tiene un campo de precio de venta: sus claves de producto son `sku_erp`, `nombre`, `categoria` y `cost_history`.

## Uso temporal propuesto

Si se interpreta la fecha como inicio de vigencia, para una operación del 15 de junio de 2025 correspondería el costo de 90.56 MXN. Para una del 1 de diciembre de 2025 correspondería 96.23 MXN. La última entrada no tiene fecha de fin explícita: aplicarla hasta el corte del análisis es una regla propuesta, no una confirmación del cliente.

Se encontraron 2,184 snapshots del producto, con fechas entre el 1 de octubre de 2025 y el 31 de marzo de 2026. Esto no demuestra cobertura completa por tienda y día. La metadata describe snapshots diarios y señala que no incluyen movimientos transaccionales.

El archivo identifica su origen como ERP CaféNorte v2.3 (legacy), pero no indica si el ERP funciona en nube, en servidores propios o de forma híbrida.
