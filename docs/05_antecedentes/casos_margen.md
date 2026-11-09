# Casos revisados de margen

Estos casos permiten contrastar futuras reglas y resultados con operaciones concretas. Margen bruto negativo no equivale automáticamente a pérdida neta total del negocio.

## Venta V00000000 del producto CN 00015

Identifiqué esta operación como una venta por debajo del costo. Se verificó en `sales.csv` y se relacionó con el catálogo usando el mapeo POS–ERP explícito:

| Dato | Valor |
|---|---|
| Fecha de la fuente actual | 01/10/2024 08:24 |
| Tienda | T033 |
| SKU POS | CN-00015 |
| SKU ERP | ERP-PROV-MX-015-D |
| Nombre | Especial Cafe Molido |
| Comprobante | I |
| Cantidad | 1 |
| Monto | 355.43 MXN |
| Costo registrado | 466.56 MXN |
| Vigencia inicial del costo | 2024-10-01 |

La siguiente entrada de costo empieza el 20 de diciembre de 2024. Con la regla propuesta de última vigencia no posterior a la venta, el costo aplicable sería 466.56 MXN.

Si `monto` es ingreso total de línea y `costo_mxn` es costo por unidad sobre una base comparable:

```text
Ingreso registrado:       355.43
Costo:                1 × 466.56 = 466.56
Margen bruto:         355.43 − 466.56 = −111.13 MXN
```

**Conclusión:** caso candidato a margen bruto negativo para CN-00015 en T033, por 111.13 MXN en esta operación. Antes de clasificarlo como resultado definitivo deben documentarse D001, D002 y D007: tratamiento de comprobantes, impuestos, descuentos, unidad y base del costo. No se afirma que todas las ventas del producto sean negativas.

El handle del producto está nulo, pero no impide este cruce físico POS–ERP, ya que los dos SKU están informados. El caso debe mantenerse como ejemplo de comprobación al implementar la consulta de productos con margen negativo.

## Conclusión

Conservo el caso como comprobación de un margen candidato bajo supuestos de costo, cantidad e importe comparables. No lo generalizo al producto o a la tienda ni lo presento como resultado definitivo sin resolver esas bases.
