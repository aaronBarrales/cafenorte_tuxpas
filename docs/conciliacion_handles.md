# Candidatos para relacionar handles con productos del ERP

## Método y evidencia

Para los seis handles sin correspondencia exacta, se compararon dos elementos simultáneamente:

1. El texto antes del último guion con el nombre del catálogo, normalizando mayúsculas, acentos, espacios y guiones para la comparación, sin cambiar los originales.
2. Los tres dígitos finales del handle con el segmento numérico del SKU ERP.

La combinación identifica un único candidato para cada uno de los seis handles. Esto es evidencia de una convención de nombres en la muestra, no una garantía contractual de identidad ni una regla confirmada por el cliente. No se usó precio parecido como prueba de identidad.

La regla coincide con los **23 de 23 mapeos existentes que tienen tanto handle como SKU ERP informados**. Los otros cuatro de los 27 mapeos con handle tienen SKU ERP nulo: no son contradicciones de la regla, pero tampoco sirven para validar su correspondencia ERP de forma independiente.

## Seis relaciones propuestas

| Handle | SKU ERP candidato | Evidencia POS existente | Filas de e-commerce |
|---|---|---|---:|
| gourmet-cafe-molido-041 | ERP-PROV-MX-041-D | Sin fila de mapeo para este ERP | 297 |
| molinillo-mercancia-030 | ERP-PROV-MX-030-C | CN-00030, handle nulo | 319 |
| selección-cafe-molido-013 | ERP-PROV-MX-013-B | CN-00013, handle nulo | 305 |
| termo-mercancia-031 | ERP-PROV-MX-031-A | Sin fila de mapeo para este ERP | 317 |
| americano-cafe-grano-032 | ERP-PROV-MX-032-D | CN-00032, handle nulo | 279 |
| americano-cafe-molido-052 | ERP-PROV-MX-052-C | CN-00052, handle nulo | 332 |

Todos coinciden además con el nombre del catálogo al normalizarlo. **Estado de las seis relaciones: propuestas, sin aplicar al pipeline ni modificar el inventario original.** Para 041 y 031 no se inventa un SKU POS: el candidato es un vínculo directo handle–ERP.

El nombre solo sería insuficiente. El catálogo tiene tres productos llamados Gourmet Cafe Molido, dos Molinillo Mercancia, dos Selección Cafe Molido, seis Termo Mercancia, uno Americano Cafe Grano y dos Americano Cafe Molido. El número distingue los candidatos dentro de esta muestra.

## Otros mapeos incompletos encontrados

| SKU POS con ERP nulo | Handle informado | SKU ERP candidato por la misma regla |
|---|---|---|
| CN-00006 | estándar-cafe-grano-006 | ERP-PROV-MX-006-C |
| CN-00026 | premium-cafe-molido-026 | ERP-PROV-MX-026-A |
| CN-00036 | gourmet-cafe-grano-036 | ERP-PROV-MX-036-A |
| CN-00046 | termo-mercancia-046 | ERP-PROV-MX-046-A |

Estos cuatro casos requieren revisión separada: un handle encontrado en el mapeo no garantiza que pueda llegar a costos e inventario si falta el SKU ERP. Las 8,098 filas con handle conocido no deben describirse automáticamente como completamente conciliadas con el ERP.

## Recomendación para el pipeline

Conservar el mapeo exacto como fuente y crear una tabla adicional de equivalencias recuperadas con handle, SKU ERP candidato, método, evidencia, estado y fecha de revisión. Usar estados explícitos: exacto con ERP válido, inferido, incompleto y no conciliado. No llamar confirmado a un enlace inferido.

Para este reto se puede adoptar la combinación nombre y sufijo como supuesto explícito y reversible, tras validar unicidad, claves existentes y ausencia de conflictos. En producción convendría contrastarla con el ID o SKU de producto/variante de Shopify y el catálogo maestro del cliente. Los archivos de órdenes actuales no incluyen esas claves alternativas.

Si se aplican las propuestas, verificar que no se multipliquen filas ni se alteren importes por moneda, que los seis handles mantengan sus 1,849 registros y que la relación a costos tenga cobertura temporal. Presentar el impacto de las filas inferidas por separado al validar márgenes. Los candidatos aún no se aplicaron: no se han calculado métricas de negocio bajo esta regla.

## Reproducción

```powershell
.\.venv\Scripts\python.exe scripts/proponer_mapeos.py
```

El script consulta el inventario y la columna product_handle de Parquet, emite propuestas en JSON y no modifica las fuentes. El perfil y la exportación CSV siguen documentados en [el análisis de e-commerce](analisis_ecommerce.md).
