# Resumen para retomar el proyecto CaféNorte

Última actualización: 7 de noviembre de 2026. Este archivo se actualizará con los hallazgos y decisiones relevantes al avanzar. Es el punto de entrada al retomar el proyecto; las dudas detalladas permanecen en `DUDAS.md`.

## Objetivo y estado

Resolver el reto Data Solutions Engineer de Tuxpas: integrar ventas físicas, inventario y e-commerce; producir cuatro respuestas de negocio; incluir pruebas, propuesta AWS con presupuesto objetivo de USD 200 al mes y bitácora de IA.

Repositorio: https://github.com/aaronBarrales/cafenorte_tuxpas. Rama: `main`. Ya se subieron la documentación y la exploración inicial. El pipeline, el modelo analítico, las respuestas finales, las pruebas y la propuesta AWS siguen pendientes. La visibilidad del repositorio no se ha verificado.

## Hallazgos confirmados

- `sales.csv` procede del POS de las tiendas físicas, según el documento del reto. El perfil inicial encontró 86,490 filas, 40 tiendas, 70 SKUs y moneda MXN en todas las filas, sin campos vacíos, IDs repetidos ni duplicados exactos.
- Las fechas originales abarcaban del 1 de octubre de 2024 al 31 de marzo de 2026. La cobertura diaria por tienda aún no se ha comprobado.
- `tipo_comprobante` tiene cinco valores: I (82,518), E (3,079), N (288), P (451) y T (154). Cantidades e importes son positivos incluso para E. Las letras coinciden con tipos de CFDI del SAT, pero no se ha confirmado el diccionario del POS.
- `sales` tiene `cantidad` y `monto`, sin columnas independientes de precio unitario, lista de precios, descuentos o impuestos. Los importes por SKU varían; esto no prueba por sí mismo errores, promociones ni cambios temporales de tarifa.
- `inventory.json` contiene metadata, `tiendas_info`, `sku_mappings`, `catalogo` y `snapshots`.
- El catálogo del inventario contiene `cost_history`, con `fecha_vigencia`, `costo_mxn` y `proveedor`. La revisión de todas las claves del JSON no encontró un campo de precio de venta ni una lista de precios.
- El inventario incluye zonas horarias por tienda. Esto no confirma que las fechas del POS representen la hora local de esa tienda.
- Los snapshots son existencias por día, tienda y SKU. Según la metadata, no incluyen movimientos transaccionales. Una fila ausente no demuestra stock cero.
- `exchange_rates.csv` tiene las columnas `fecha`, `currency` y `rate_to_mxn`; aún no se ha validado su cobertura o convención de conversión.
- El esquema de `ecommerce_orders.parquet` todavía no se ha leído: el entorno consultado no tiene `pyarrow`, `fastparquet` ni `duckdb`. No se ha descartado que e-commerce aporte campos adicionales de precio o descuento; unas órdenes tampoco equivaldrían automáticamente a una lista histórica de precios.

## Diferencia entre costo y precio

El costo es el valor asociado a adquirir o producir el producto. El catálogo del ERP registra costos, pero aún debe confirmarse su unidad de medida, impuestos y componentes. El precio de venta es lo que se cobra al cliente; el precio de lista es la tarifa establecida antes de los ajustes aplicables.

Si `sales.monto` es el total de la fila, `monto / cantidad` permite obtener un importe efectivo por unidad. No reconstruye la tarifa original ni explica descuentos. La ausencia de una lista de precios no impide analizar ingresos registrados una vez fijadas las reglas; sí limita explicar cómo se fijó cada importe o comprobar que se respetó una tarifa.

El POS registra operaciones y cobros. El ERP administra procesos como inventario, compras y proveedores. Cualquiera puede funcionar en nube, servidores propios o de forma híbrida. Los archivos no confirman el alojamiento de los sistemas actuales.

## Caso revisado con el autor

`ERP-PROV-MX-057-C` es Premium Cafe Grano y corresponde a `CN-00057` en POS y `premium-cafe-grano-057` en los mapeos de handle.

| Vigente desde | Costo registrado en MXN |
|---|---:|
| 2024-10-01 | 87.40 |
| 2024-11-08 | 86.31 |
| 2024-11-14 | 85.94 |
| 2025-02-01 | 90.56 |
| 2025-11-30 | 96.23 |

La operación `V00009357`, del 28 de noviembre de 2024, tienda T036, tiene SKU `CN-00057`, cantidad 2, monto 385.79 MXN y comprobante I. Se verificó la fila en la fuente actual.

Bajo los supuestos de monto total de línea, costo unitario comparable y vigencia hasta el siguiente cambio: importe por unidad 192.895 MXN, costo de dos unidades 171.88 MXN y margen en dinero 213.91 MXN. Es un ejemplo condicionado, no un margen definitivo: faltan confirmar impuestos, descuentos, unidades y tratamiento de comprobantes. La diferencia entre costo y precio no constituye por sí sola una inconsistencia.

La captura anterior de `CN-00003` corresponde a otro producto y contiene registros N de distintas tiendas y fechas. No mezclar ese ejemplo con el producto 057.

## Supuestos todavía sin confirmar

1. D001: significado y efecto de cada comprobante en ingresos y unidades.
2. D002: monto total o precio unitario; impuestos y descuentos incluidos.
3. D003: granularidad de la fila, significado de venta_id y vínculo de devoluciones.
4. D004: zona horaria real de las fechas del POS.
5. D005: corte común y ventanas del reto, una vez revisada la cobertura conjunta.
6. D006: origen de los importes variables y disponibilidad de tarifas o promociones históricas.
7. D007: unidad, base y vigencia del costo; si aplica globalmente o por tienda.

La propuesta es conservar los valores originales, documentar cualquier interpretación y resolver las ambigüedades de las preguntas de negocio con criterio, como pide el reto. Las propuestas de la IA no se consideran automáticamente confirmadas por el autor.

## Cambio detectado en el CSV local

El perfil original usó SHA-256 `87628a584d30a353f3bcc9dbe20c2d8f1e55c80a0036ecee88e76fce61031276` y fechas `YYYY-MM-DD HH:MM:SS`. En esta revisión el archivo tiene SHA-256 `b62180fc201e4dc01c7e58f781c0b5f55cdf003095d29ad714e708be85b80bb1` y fechas de tipo `DD/MM/YYYY HH:MM`. No se ha determinado quién ni qué proceso lo cambió ni si hubo otros cambios.

El perfilador actual solo acepta el formato original y marca las 86,490 fechas de la versión actual como no interpretables por ese formato. Una comprobación independiente con `DD/MM/YYYY HH:MM` interpretó las 86,490 filas sin errores, entre 2024-10-01 07:04 y 2026-03-31 21:08. No equivale a demostrar que el contenido completo no haya cambiado. Antes de continuar, preservar o recuperar la fuente original y decidir qué formatos admitir, documentando cualquier pérdida de precisión. No sobrescribir silenciosamente los datos del autor.

## Próximos pasos al retomar

1. Resolver la procedencia y el formato de la versión actual de sales y actualizar su perfil reproducible.
2. Elegir el stack proporcional al reto y habilitar lectura de Parquet; revisar el esquema y contenido de e-commerce.
3. Perfilar inventario y tipos de cambio: cobertura, duplicados, unidades, mapeos faltantes o ambiguos y vigencias de costo.
4. Documentar reglas de comprobantes, monto y costos; comparar su impacto y validar controles de origen.
5. Revisar cobertura por fecha y tienda, valores atípicos y claves entre fuentes.
6. Implementar modelo, cuatro respuestas y pruebas que validen cifras, no solo ejecución.
7. Preparar propuesta AWS, estimación de costos, fases y riesgos, y revisión final con el autor de la bitácora.

## Archivos útiles y hábitos de trabajo

- `README.md`: alcance y estado general.
- `DUDAS.md`: preguntas, evidencia, impacto y tratamiento propuesto.
- `DEFINICIONES.md`: glosario.
- `docs/analisis_sales.md`: perfil original de ventas, con su hash.
- `docs/producto_ERP-PROV-MX-057-C.md`: historial de costos investigado.
- `scripts/perfil_sales.py`: perfilador de CSV, biblioteca estándar de Python. Ejecutar desde la raíz con `python scripts/perfil_sales.py`, considerando la limitación de formato anterior.
- `AI_LOG.md`: cinco prompts clave y decisiones pendientes del autor.
- `exploracion.ipynb`: archivo local vacío, aún fuera de Git.

Mantener commits por avances coherentes y actualizar este resumen al obtener nuevos hallazgos. Los datos originales, credenciales y salidas regenerables están excluidos de Git. No registrar confirmaciones del cliente o del autor que no hayan ocurrido. No se ha verificado permiso para redistribuir las fuentes.

Git está instalado; `gh` no estaba disponible al iniciar. La conexión HTTPS funcionó usando el almacén de certificados de Windows con `git -c http.sslBackend=schannel push`, manteniendo activa la validación. El Python usado para la exploración fue el del runtime de dependencias de Codex; no se fijaron aún dependencias del proyecto.
