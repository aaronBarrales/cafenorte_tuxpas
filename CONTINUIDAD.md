# Resumen para retomar el proyecto CaféNorte

Última actualización: 7 de noviembre de 2026. Este archivo se actualizará con los hallazgos y decisiones relevantes al avanzar. Es el punto de entrada al retomar el proyecto; las dudas detalladas permanecen en `DUDAS.md`.

## Objetivo y estado

Resolver el reto Data Solutions Engineer de Tuxpas: integrar ventas físicas, inventario y e-commerce; producir cuatro respuestas de negocio; incluir pruebas, propuesta AWS con presupuesto objetivo de USD 200 al mes y bitácora de IA.

Repositorio: https://github.com/aaronBarrales/cafenorte_tuxpas. Rama: `main`. Exploración completa ejecutada con `scripts/eda_completo.py`, documentada en `docs/EDA_COMPLETO.md`; banco de 60 preguntas en `PREGUNTAS_CLIENTE.md` y fases en `PLAN_ENTREGA.md`. El pipeline, el modelo analítico, las respuestas finales, sus pruebas y la propuesta AWS siguen pendientes. La visibilidad del repositorio no se ha verificado.

El autor confirmó entrega **antes del martes 10 de noviembre de 2026 a las 12:00 p. m., hora de Ciudad de México**. Objetivo interno: revisión el lunes y paquete preparado el martes antes de las 11:00 a. m. No se han enviado consultas ni correos al cliente.

## Resultados de la exploración completa

- Inventario: 230,776 filas; 4,417 valores N/A, 11,726 ceros numéricos y ningún stock numérico negativo. No convertir desconocidos en cero.
- Sus 1,268 pares tienda–SKU tienen filas en los 182 días, pero cada tienda cubre entre 25 y 40 SKU. Para 12,687 registros I del semestre con ERP conocido falta snapshot del par: la rotación exige población consistente y cobertura explícita.
- Hay 565 registros I con venta y stock cero el mismo día; puede ser saldo de cierre. Tres secuencias observadas de cuatro días en cero ocurren en T015, T023 y T038 en enero–marzo de 2026; desconocidos pueden ocultar más casos.
- Cinco SKU POS carecen de fila de mapeo y otros cinco tienen ERP nulo. En total 12,349 filas físicas no llegan a ERP por enlace exacto. En Shopify son 2,988: 1,849 sin handle mapeado y 1,139 con handle pero ERP nulo.
- Los 70 productos tienen costo desde 2024-10-01, con 282 vigencias sin claves de fecha conflictivas. Con reglas candidatas, 2,369 registros I físicos con costo dan margen negativo y 11,797 I quedan sin costo conciliado; son diagnósticos de 18 meses, no respuesta final agregada por producto–tienda.
- FX tiene 730 tasas válidas, sin huecos diarios ni conflictos; todas las órdenes extranjeras tienen tasa del mismo día. EUR = 22.0 en 63 fechas requiere preguntar metodología, no declarar error. El primer MoM online carece de marzo de 2025.
- Seis controles de conteos del EDA pasaron. Detalles y hashes en `outputs/eda_completo.json`, local y excluido de Git. El perfilador de sales ya admite ambos formatos observados, sin cambiar el archivo ni inventar segundos.

## Hallazgos confirmados

- `sales.csv` procede del POS de las tiendas físicas, según el documento del reto. El perfil inicial encontró 86,490 filas, 40 tiendas, 70 SKUs y moneda MXN en todas las filas, sin campos vacíos, IDs repetidos ni duplicados exactos.
- Las fechas originales abarcaban del 1 de octubre de 2024 al 31 de marzo de 2026. La cobertura diaria por tienda aún no se ha comprobado.
- `tipo_comprobante` tiene cinco valores: I (82,518), E (3,079), N (288), P (451) y T (154). Cantidades e importes son positivos incluso para E. Las letras coinciden con tipos de CFDI del SAT, pero no se ha confirmado el diccionario del POS.
- `sales` tiene `cantidad` y `monto`, sin columnas independientes de precio unitario, lista de precios, descuentos o impuestos. Los importes por SKU varían; esto no prueba por sí mismo errores, promociones ni cambios temporales de tarifa.
- `inventory.json` contiene metadata, `tiendas_info`, `sku_mappings`, `catalogo` y `snapshots`.
- El catálogo del inventario contiene `cost_history`, con `fecha_vigencia`, `costo_mxn` y `proveedor`. La revisión de todas las claves del JSON no encontró un campo de precio de venta ni una lista de precios.
- El inventario incluye zonas horarias por tienda. Esto no confirma que las fechas del POS representen la hora local de esa tienda.
- `sku_mappings` contiene 65 registros: 38 con handle nulo y 27 informado, sin duplicados en los valores no nulos de cada una de las tres claves. El catálogo contiene 70 productos; falta conciliar la cobertura exacta entre conjuntos.
- El producto `ERP-PROV-MX-015-D` corresponde a `CN-00015`, tiene nombre `Especial Cafe Molido` y costos, aunque su handle sea nulo. El handle no es la descripción: en Shopify identifica al producto en su URL. Un nulo puede ser un mapeo incompleto o una ausencia de publicación online; aún no se ha determinado la causa.
- Se observó `CN-00016` con SKU ERP y handle nulos. Su conciliación con inventario y costos requiere revisión separada. No inventar claves, cruzar nulos entre sí ni descartar movimientos sin reportarlos.
- Los snapshots son existencias por día, tienda y SKU. Según la metadata, no incluyen movimientos transaccionales. Una fila ausente no demuestra stock cero.
- `exchange_rates.csv` tiene las columnas `fecha`, `currency` y `rate_to_mxn`; aún no se ha validado su cobertura o convención de conversión.
- Se leyó `ecommerce_orders.parquet`: 9,947 filas, 11 columnas, 33 handles distintos y fechas entre abril de 2025 y marzo de 2026. Contiene order_id, fecha, product_handle, cantidad, amount, currency y cinco campos de clientes/envío. No incluye SKU POS/ERP, precio de lista, vigencias de tarifas ni columnas separadas de impuestos o descuentos. No se identificó una lista histórica de precios de venta entre las fuentes revisadas.
- En e-commerce, 27 handles tienen mapeo exacto (8,098 filas) y 6 no lo tienen (1,849 filas). Cuatro de estos últimos tienen sufijos coincidentes con SKU sin handle: 013, 030, 032 y 052. Son candidatos, no relaciones confirmadas. No adoptar la regla «sin handle = sin venta online». Para 015 no apareció un handle con sufijo -015; eso no demuestra ausencia de ventas.
- La investigación posterior combinó nombre normalizado y segmento numérico del SKU ERP: encontró un único candidato para los seis handles pendientes, incluido ERP 041-D y 031-A que no tienen fila en el mapeo. La regla coincide con los 23 de 23 mapeos completos handle–ERP de la muestra. Las seis relaciones siguen propuestas, sin aplicar. Ver `docs/conciliacion_handles.md` y `scripts/proponer_mapeos.py`.
- Los otros cuatro de los 27 handles informados tienen SKU ERP nulo (POS 006, 026, 036 y 046). También se encontraron candidatos para ellos, sin confirmarlos. Las 8,098 filas con handle reconocido no equivalen automáticamente a filas conciliadas hasta costo ERP.
- Se exportó `outputs/ecommerce_orders.csv` con todas las filas y columnas en UTF-8 con BOM, verificado contra la serialización del Parquet. Es una copia local de consulta, excluida de Git; conserva campos de clientes y representa los nulos como vacíos. El original no se modificó. Ver `docs/analisis_ecommerce.md` para esquema, conteos y reproducción.

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

El autor identificó además `V00000000`, del 1 de octubre de 2024, tienda T033, CN-00015, una unidad, monto 355.43 MXN, comprobante I. El mapeo lleva a ERP-PROV-MX-015-D, Especial Cafe Molido, con costo 466.56 MXN vigente desde esa fecha. Bajo las bases propuestas, margen bruto = 355.43 − 466.56 = −111.13 MXN. Se conserva como caso candidato en `docs/casos_margen.md`, sujeto a confirmar impuestos, unidades y comprobantes. No generalizarlo a todas las operaciones del producto ni llamarlo pérdida neta total.

## Supuestos todavía sin confirmar

1. D001: significado y efecto de cada comprobante en ingresos y unidades.
2. D002: monto total o precio unitario; impuestos y descuentos incluidos.
3. D003: granularidad de la fila, significado de venta_id y vínculo de devoluciones.
4. D004: zona horaria real de las fechas del POS.
5. D005: corte común y ventanas del reto, una vez revisada la cobertura conjunta.
6. D006: origen de los importes variables y disponibilidad de tarifas o promociones históricas.
7. D007: unidad, base y vigencia del costo; si aplica globalmente o por tienda.
8. D008: causa de handles ausentes, claves alternativas y cobertura real de los mapeos POS–ERP–Shopify.

La propuesta es conservar los valores originales, documentar cualquier interpretación y resolver las ambigüedades de las preguntas de negocio con criterio, como pide el reto. Las propuestas de la IA no se consideran automáticamente confirmadas por el autor.

## Cambio detectado en el CSV local

El perfil original usó SHA-256 `87628a584d30a353f3bcc9dbe20c2d8f1e55c80a0036ecee88e76fce61031276` y fechas `YYYY-MM-DD HH:MM:SS`. En esta revisión el archivo tiene SHA-256 `b62180fc201e4dc01c7e58f781c0b5f55cdf003095d29ad714e708be85b80bb1` y fechas de tipo `DD/MM/YYYY HH:MM`. No se ha determinado quién ni qué proceso lo cambió ni si hubo otros cambios.

El perfilador inicialmente solo aceptaba el formato original; se actualizó durante el EDA completo para admitir también `DD/MM/YYYY HH:MM`. Las 86,490 filas actuales son interpretables, entre 2024-10-01 07:04 y 2026-03-31 21:08. La procedencia del cambio sigue abierta; no se reconstruyen segundos ni se sobrescribe la fuente. La compatibilidad de lectura no prueba que no haya otros cambios respecto al original.

## Próximos pasos al retomar

1. Leer `docs/EDA_COMPLETO.md` y `PLAN_ENTREGA.md`. No repetir la exploración salvo cambio de fuentes o reglas.
2. Elegir el stack e implementar el pipeline con clasificación de mapeos, desconocidos y controles; PyArrow ya está disponible.
3. Trasladar al README las reglas finales, el corte y las ventanas. No esperar las 60 respuestas para avanzar; distinguir supuestos de confirmaciones.
4. Resolver o mostrar cobertura parcial de inventario antes de presentar rotación global. Mantener importes no conciliados visibles.
5. Implementar consultas y pruebas de monedas, costos vigentes, ceros consecutivos y MoM sin base.
6. Redactar propuesta AWS con precios verificados y fases, revisar AI_LOG con el autor y ensayar demo.
7. Verificar acceso al repositorio y preparar entrega antes del límite. No enviar correos sin instrucción expresa.

## Archivos útiles y hábitos de trabajo

- `HALLAZGOS.md`: resumen breve de descubrimientos importantes. El autor pidió mantenerlo actualizado y resumir al máximo; conservar el detalle técnico en documentos enlazados.
- `docs/EDA_COMPLETO.md`: exploración integral y límites de las cuatro métricas.
- `PREGUNTAS_CLIENTE.md`: 60 consultas, diez prioritarias; no enviadas.
- `PLAN_ENTREGA.md`: fechas, reglas candidatas y validaciones del pipeline pendiente.
- `scripts/eda_completo.py`: genera `outputs/eda_completo.json` con seis controles de conteos.
- `README.md`: alcance y estado general.
- `DUDAS.md`: preguntas, evidencia, impacto y tratamiento propuesto.
- `DEFINICIONES.md`: glosario.
- `docs/analisis_sales.md`: perfil original de ventas, con su hash.
- `docs/producto_ERP-PROV-MX-057-C.md`: historial de costos investigado.
- `docs/analisis_ecommerce.md`: esquema, monedas, mapeos faltantes y lectura en Excel.
- `docs/casos_margen.md`: venta candidata a margen negativo para usar como comprobación.
- `scripts/exportar_ecommerce.py`: exportación CSV con validación de todas las filas y hash del origen.
- `scripts/perfil_ecommerce.py`: perfil y conciliación exacta de handles, sin mostrar datos personales.
- `requirements-exploracion.txt`: PyArrow 26.0.1; entorno `.venv` local. Ejecutar los scripts con `.\.venv\Scripts\python.exe`.
- `scripts/perfil_sales.py`: perfilador de CSV con biblioteca estándar de Python; admite los dos formatos observados, sin modificar la fuente.
- `AI_LOG.md`: cinco prompts clave y decisiones pendientes del autor.
- `exploracion.ipynb`: archivo local vacío, aún fuera de Git.

Mantener commits por avances coherentes y actualizar este resumen al obtener nuevos hallazgos. Los datos originales, credenciales y salidas regenerables están excluidos de Git. No registrar confirmaciones del cliente o del autor que no hayan ocurrido. No se ha verificado permiso para redistribuir las fuentes.

Git está instalado; `gh` no estaba disponible al iniciar. La conexión HTTPS funcionó usando el almacén de certificados de Windows con `git -c http.sslBackend=schannel push`, manteniendo activa la validación. La exploración inicial usó Python del runtime de Codex; para Parquet se creó `.venv` con el Python 3.12 instalado y se fijó PyArrow en requirements-exploracion.txt. La instalación necesitó `pip --use-feature=truststore` para validar certificados del sistema; no se desactivó HTTPS. El stack final del pipeline sigue pendiente.
