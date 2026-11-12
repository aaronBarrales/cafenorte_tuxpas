# Resumen para retomar el proyecto CaféNorte

## Organización vigente de la documentación — 8 de noviembre de 2026

El punto de entrada es [docs/README.md](../README.md). La documentación se divide en `01_reto/`, `02_exploracion/`, `03_negocio/`, `04_seguimiento/` y `05_antecedentes/`. Los informes aislados actuales están en exploración; los estudios anteriores y casos entre fuentes están en antecedentes. Las referencias a organizaciones anteriores en entradas cronológicas son históricas.

El notebook de sales conserva únicamente su informe en Documentación relacionada; las dudas están centralizadas fuera de los notebooks. Se verificaron 110 enlaces locales de Markdown y notebooks y se conservó el código y las salidas de sus 19 celdas ejecutables. El validador ahora busca las preguntas del cliente en `docs/03_negocio/PREGUNTAS_CLIENTE.md`.

Última actualización: 9 de noviembre de 2026. Este archivo se actualizará con los hallazgos y decisiones relevantes al avanzar. Es el punto de entrada al retomar el proyecto; las dudas detalladas permanecen en `docs/03_negocio/DUDAS.md`.

## Objetivo y estado

Enunciado original guardado en `docs/01_reto/TX Challenge Data Solutions Engineer.docx`, con transcripción en `docs/01_reto/enunciado_extraido.md` y explicación en `docs/01_reto/guia_entrega.md`. La sección 2.2 pide propuesta AWS para producción, no despliegue obligatorio. La propuesta es de máximo dos páginas; demo, pitch y defensa de IA son en entrevista, sin video ni slides obligatorios. La sección 5 permite repo público o privado con acceso para el evaluador.

Resolver el reto Data Solutions Engineer de Tuxpas: integrar ventas físicas, inventario y e-commerce; producir cuatro respuestas de negocio; incluir pruebas, propuesta AWS con presupuesto objetivo de USD 200 al mes y bitácora de IA.

Repositorio: https://github.com/aaronBarrales/cafenorte_tuxpas. Rama: `main`. Exploración completa ejecutada con `scripts/eda_completo.py`, documentada en `docs/05_antecedentes/EDA_COMPLETO.md`; banco de 60 preguntas en `docs/03_negocio/PREGUNTAS_CLIENTE.md` y fases en `docs/04_seguimiento/PLAN_ENTREGA.md`. El pipeline, el modelo analítico, las respuestas finales, sus pruebas y la propuesta AWS siguen pendientes. La visibilidad del repositorio no se ha verificado.

Confirmé la entrega **antes del martes 10 de noviembre de 2026 a las 12:00 p. m., hora de Ciudad de México**. Objetivo interno: revisión el lunes y paquete preparado el martes antes de las 11:00 a. m. No se han enviado consultas ni correos al cliente.

## Resultados históricos de la exploración completa

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
- `sku_mappings` contiene 65 registros: 38 con handle nulo y 27 informado, sin duplicados en los valores no nulos de cada una de las tres claves. El catálogo contiene 70 productos; la cobertura exacta con los movimientos actuales queda cuantificada en el informe conjunto.
- El producto `ERP-PROV-MX-015-D` corresponde a `CN-00015`, tiene nombre `Especial Cafe Molido` y costos, aunque su handle sea nulo. El handle no es la descripción: en Shopify identifica al producto en su URL. Un nulo puede ser un mapeo incompleto o una ausencia de publicación online; aún no se ha determinado la causa.
- Se observó `CN-00016` con SKU ERP y handle nulos. Su conciliación con inventario y costos requiere revisión separada. No inventar claves, cruzar nulos entre sí ni descartar movimientos sin reportarlos.
- Los snapshots son existencias por día, tienda y SKU. Según la metadata, no incluyen movimientos transaccionales. Una fila ausente no demuestra stock cero.
- `exchange_rates.csv` tiene las columnas `fecha`, `currency` y `rate_to_mxn`. La exploración aislada actual valida continuidad diaria interna y tasas positivas; confirmé para mi análisis que fecha indica el día sin hora ni zona explícitas, currency identifica la moneda y rate_to_mxn expresa MXN por unidad extranjera (importe por tasa). Proveedor, fecha contable y vigencia siguen pendientes (Q10/Q38); no es una respuesta del cliente.
- Se leyó `ecommerce_orders.parquet`: 9,947 filas, 11 columnas, 33 handles distintos y fechas entre abril de 2025 y marzo de 2026. Contiene order_id, fecha, product_handle, cantidad, amount, currency y cinco campos de clientes/envío. No incluye SKU POS/ERP, precio de lista, vigencias de tarifas ni columnas separadas de impuestos o descuentos. No se identificó una lista histórica de precios de venta entre las fuentes revisadas.
- En e-commerce, 27 handles tienen mapeo exacto (8,098 filas) y 6 no lo tienen (1,849 filas). Cuatro de estos últimos tienen sufijos coincidentes con SKU sin handle: 013, 030, 032 y 052. Son candidatos, no relaciones confirmadas. No adoptar la regla «sin handle = sin venta online». Para 015 no apareció un handle con sufijo -015; eso no demuestra ausencia de ventas.
- La investigación posterior combinó nombre normalizado y segmento numérico del SKU ERP: encontró un único candidato para los seis handles pendientes, incluido ERP 041-D y 031-A que no tienen fila en el mapeo. La regla coincide con los 23 de 23 mapeos completos handle–ERP de la muestra. Las seis relaciones siguen propuestas, sin aplicar. Ver `docs/05_antecedentes/conciliacion_handles.md` y `scripts/proponer_mapeos.py`.
- Los otros cuatro de los 27 handles informados tienen SKU ERP nulo (POS 006, 026, 036 y 046). También se encontraron candidatos para ellos, sin confirmarlos. Las 8,098 filas con handle reconocido no equivalen automáticamente a filas conciliadas hasta costo ERP.
- Se exportó `outputs/ecommerce_orders.csv` con todas las filas y columnas en UTF-8 con BOM, verificado contra la serialización del Parquet. Es una copia local de consulta, excluida de Git; conserva campos de clientes y representa los nulos como vacíos. El original no se modificó. Ver `docs/05_antecedentes/analisis_ecommerce.md` para esquema, conteos y reproducción.

## Diferencia entre costo y precio

El costo es el valor asociado a adquirir o producir el producto. El catálogo del ERP registra costos, pero aún debe confirmarse su unidad de medida, impuestos y componentes. El precio de venta es lo que se cobra al cliente; el precio de lista es la tarifa establecida antes de los ajustes aplicables.

Si `sales.monto` es el total de la fila, `monto / cantidad` permite obtener un importe efectivo por unidad. No reconstruye la tarifa original ni explica descuentos. La ausencia de una lista de precios no impide analizar ingresos registrados una vez fijadas las reglas; sí limita explicar cómo se fijó cada importe o comprobar que se respetó una tarifa.

El POS registra operaciones y cobros. El ERP administra procesos como inventario, compras y proveedores. Cualquiera puede funcionar en nube, servidores propios o de forma híbrida. Los archivos no confirman el alojamiento de los sistemas actuales.

## Caso que revisé

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

Identifiqué además `V00000000`, del 1 de octubre de 2024, tienda T033, CN-00015, una unidad, monto 355.43 MXN, comprobante I. El mapeo lleva a ERP-PROV-MX-015-D, Especial Cafe Molido, con costo 466.56 MXN vigente desde esa fecha. Bajo las bases propuestas, margen bruto = 355.43 − 466.56 = −111.13 MXN. Se conserva como caso candidato en `docs/05_antecedentes/casos_margen.md`, sujeto a confirmar impuestos, unidades y comprobantes. No generalizarlo a todas las operaciones del producto ni llamarlo pérdida neta total.

## Supuestos todavía sin confirmar

1. D001: significado y efecto de cada comprobante en ingresos y unidades.
2. D002: monto total o precio unitario; impuestos y descuentos incluidos.
3. D003: granularidad de la fila, significado de venta_id y vínculo de devoluciones.
4. D004: zona horaria real de las fechas del POS.
5. D005: corte común y ventanas del reto, una vez revisada la cobertura conjunta.
6. D006: origen de los importes variables y disponibilidad de tarifas o promociones históricas.
7. D007: unidad, base y vigencia del costo; si aplica globalmente o por tienda.
8. D008: causa de handles ausentes, claves alternativas y cobertura real de los mapeos POS–ERP–Shopify.

Mi propuesta de trabajo es conservar los valores originales, documentar cualquier interpretación y resolver las ambigüedades de las preguntas de negocio con criterio, como pide el reto. No considero las propuestas de la IA automáticamente confirmadas por mí.

## Cambio detectado en el CSV local

El perfil original usó SHA-256 `87628a584d30a353f3bcc9dbe20c2d8f1e55c80a0036ecee88e76fce61031276` y fechas `YYYY-MM-DD HH:MM:SS`. En esta revisión el archivo tiene SHA-256 `b62180fc201e4dc01c7e58f781c0b5f55cdf003095d29ad714e708be85b80bb1` y fechas de tipo `DD/MM/YYYY HH:MM`. No se ha determinado quién ni qué proceso lo cambió ni si hubo otros cambios.

El perfilador inicialmente solo aceptaba el formato original; se actualizó durante el EDA completo para admitir también `DD/MM/YYYY HH:MM`. Las 86,490 filas actuales son interpretables, entre 2024-10-01 07:04 y 2026-03-31 21:08. La procedencia del cambio sigue abierta; no se reconstruyen segundos ni se sobrescribe la fuente. La compatibilidad de lectura no prueba que no haya otros cambios respecto al original.

## Próximos pasos al retomar

1. Leer `docs/05_antecedentes/EDA_COMPLETO.md` y `docs/04_seguimiento/PLAN_ENTREGA.md`. No repetir la exploración salvo cambio de fuentes o reglas.
2. Elegir el stack e implementar el pipeline con clasificación de mapeos, desconocidos y controles; PyArrow ya está disponible.
3. Trasladar al README las reglas finales, el corte y las ventanas. No esperar las 60 respuestas para avanzar; distinguir supuestos de confirmaciones.
4. Resolver o mostrar cobertura parcial de inventario antes de presentar rotación global. Mantener importes no conciliados visibles.
5. Implementar consultas y pruebas de monedas, costos vigentes, ceros consecutivos y MoM sin base.
6. Redactar propuesta AWS con precios verificados y fases, revisar personalmente AI_LOG y ensayar demo.
7. Verificar acceso al repositorio y preparar entrega antes del límite. No enviar correos sin instrucción expresa.

## Archivos útiles y hábitos de trabajo

- `docs/03_negocio/guia_preguntas_negocio.md`: guía para principiantes de las cuatro solicitudes, con fórmulas, ejemplos ficticios y ambigüedades. Es material explicativo; no adopta reglas definitivas ni contiene resultados calculados del reto.

- `docs/04_seguimiento/HALLAZGOS.md`: resumen breve de descubrimientos importantes. Pedí mantenerlo actualizado y resumir al máximo; conservar el detalle técnico en documentos enlazados.
- `docs/05_antecedentes/EDA_COMPLETO.md`: exploración integral y límites de las cuatro métricas.
- `docs/03_negocio/PREGUNTAS_CLIENTE.md`: 60 consultas, diez prioritarias; no enviadas.
- `docs/04_seguimiento/PLAN_ENTREGA.md`: fechas, reglas candidatas y validaciones del pipeline pendiente.
- `scripts/eda_completo.py`: genera `outputs/eda_completo.json` con seis controles de conteos.
- `README.md`: alcance y estado general.
- `docs/03_negocio/DUDAS.md`: preguntas, evidencia, impacto y tratamiento propuesto.
- `docs/03_negocio/DEFINICIONES.md`: glosario.
- `docs/05_antecedentes/analisis_sales.md`: perfil original de ventas, con su hash.
- `docs/05_antecedentes/producto_ERP-PROV-MX-057-C.md`: historial de costos investigado.
- `docs/05_antecedentes/analisis_ecommerce.md`: esquema, monedas, mapeos faltantes y lectura en Excel.
- `docs/05_antecedentes/casos_margen.md`: venta candidata a margen negativo para usar como comprobación.
- `scripts/exportar_ecommerce.py`: exportación CSV con validación de todas las filas y hash del origen.
- `scripts/perfil_ecommerce.py`: perfil y conciliación exacta de handles, sin mostrar datos personales.
- `requirements-exploracion.txt`: PyArrow 26.0.1; entorno `.venv` local. Ejecutar los scripts con `.\.venv\Scripts\python.exe`.
- `scripts/perfil_sales.py`: perfilador de CSV con biblioteca estándar de Python; admite los dos formatos observados, sin modificar la fuente.
- `AI_LOG.md`: cinco prompts clave y mis decisiones pendientes.
- `notebooks/01_sales.ipynb`: archivo local vacío, aún fuera de Git.

Mantener commits por avances coherentes y actualizar este resumen al obtener nuevos hallazgos. Los datos originales, credenciales y salidas regenerables están excluidos de Git. No registrar confirmaciones del cliente o mías que no hayan ocurrido. No se ha verificado permiso para redistribuir las fuentes.

Git está instalado; `gh` no estaba disponible al iniciar. La conexión HTTPS funcionó usando el almacén de certificados de Windows con `git -c http.sslBackend=schannel push`, manteniendo activa la validación. La exploración inicial usó Python del runtime de Codex; para Parquet se creó `.venv` con el Python 3.12 instalado y se fijó PyArrow en requirements-exploracion.txt. La instalación necesitó `pip --use-feature=truststore` para validar certificados del sistema; no se desactivó HTTPS. El stack final del pipeline sigue pendiente.

## Reorganización del 8 de noviembre de 2026

La exploración interactiva de ventas está ahora en `notebooks/01_sales.ipynb`, con 13 celdas de código verificadas y salidas actuales. Los informes previos están en `docs/analisis/` y el seguimiento en `docs/proyecto/`. No hay todavía notebooks de las otras tres fuentes: se construirán uno por uno.

**Vigencia de la validación:** al volver a ejecutar el validador, nueve controles pasaron y el control de hashes falló para sales.csv. Las otras tres fuentes coinciden con el reporte previo. No interpretar los diez controles históricos como validación vigente de sales. Antes de reutilizar sus cifras históricas, revisar el cambio de fuente y regenerar el EDA de manera explícita.

### Notebook de ventas ampliado

01_sales.ipynb contiene ahora 19 celdas de código ejecutadas y dos gráficas SVG, controles de calidad y dominios, resúmenes por tienda/SKU/mes, IQR y conclusiones calculadas. Por petición expresa mía, fecha solo convierte DD/MM/YYYY HH:MM; no hay fecha_alternativa. Cero fechas inválidas en la fuente actual. Conteos conciliados y fuente intacta durante la verificación. Hallazgos importantes actualizados en HALLAZGOS.md. Siguiente fuente: inventory.json.

### Documentación de resultados aislados y código comentado

Se añadieron docs/02_exploracion/resultados_sales.md e índice docs/02_exploracion/README.md, con resultados verificados sobre sales.csv y explicación de importancia, interpretación y limitaciones. El informe declara que no se cruzó ni consultó el contenido de las otras fuentes. Los antecedentes históricos se conservan identificados como tales. Cada línea de código del notebook tiene ahora explicación en español; su lógica no cambió según comparación AST. Las 19 celdas volvieron a ejecutarse y sus conteos y suma monetaria se conciliaron; fuente intacta. Se actualizaron HALLAZGOS.md y AI_LOG.md y las convenciones correspondientes en AGENTS.md. Los demás informes aislados permanecen pendientes de sus notebooks.

### Revisión de granularidad por coincidencia temporal

El notebook tiene 20 celdas de código verificadas. Se comprobaron 201 grupos de tienda y fecha/hora con varios SKU (402 filas); al mantener también moneda y comprobante hay 186 grupos (372 filas). Esto no identifica tickets o clientes. Se actualizaron resultados_sales.md, HALLAZGOS y D003 y se amplió Q11 con evidencia y solicitud de claves de ticket/línea y precisión temporal. La tabla de valores distintos no se modificó: pedí justificar su utilidad. No se alteró la fuente.

### Voz editorial de la documentación

Pedí redactar los documentos desde mi perspectiva y registrar mis aclaraciones durante la revisión. La documentación ya no se refiere a mí en tercera persona; el informe usa el encabezado Hipótesis. AI_LOG mantiene la distinción entre mis solicitudes y las acciones verificadas de la IA y reúne mis aclaraciones sobre formato de fechas, granularidad, utilidad de estadísticas y organización documental. El cambio fue editorial y no alteró resultados ni fuentes.

### Cierre de los documentos

Pedí eliminar «Reproducción y vigencia» del informe de sales y terminar los Markdown propios con una conclusión breve. Las instrucciones de ejecución permanecen en README y las verificaciones técnicas en AI_LOG. Las próximas entradas de seguimiento y bitácora deben insertarse antes de la conclusión. No cambiaron el notebook ni las fuentes.

### Convención vigente de comentarios

Pedí usar un comentario en español por bloque de código importante, en lugar de comentar cada línea. El notebook de sales y AGENTS.md ya siguen esta convención; se conservaron lógica, salidas y contadores de ejecución. Las entradas anteriores sobre comentarios línea por línea describen una preferencia histórica, sustituida por esta aclaración.

### 8 de noviembre de 2026 — Exploración aislada de exchange_rates

Pedí un notebook e informe basados en la estructura de resultados_sales, con comentarios por bloque, alcance aislado y dudas conectadas al banco de preguntas. La IA creó [02_exchange_rates.ipynb](../../notebooks/02_exchange_rates.ipynb) y [resultados_exchange_rates.md](../02_exploracion/resultados_exchange_rates.md). El hash de tasas coincide con el antecedente: `a0e827ec1e048cf397584eca3d692cb5b5b1f6b477fb78efca2fdbd2f488bddf`; no se modificó la fuente. Tengo 730 filas, USD/EUR, 365 días por moneda y ninguna clave ausente en la ventana; EUR = 22.0 en 63 fechas. Q10, Q38–Q40 y D013/D023 recogen las dudas sin duplicarlas ni darlas por respondidas. La IA ejecutó el notebook y comprobó unicidad, recuentos y conservación; evidencia en AI_LOG. Inventario y e-commerce siguen pendientes como notebooks aislados. Mi revisión y el pipeline permanecen pendientes.

### 8 de noviembre de 2026 — Numeración consecutiva de notebooks

Pedí que exchange_rates fuera el notebook 02 y que la numeración se obtuviera revisando los archivos existentes en la carpeta de destino. La IA comprobó que sales ocupa el 01, renombró el archivo a [02_exchange_rates.ipynb](../../notebooks/02_exchange_rates.ipynb) y actualizó referencias e instrucciones de ejecución. Conservó sus bytes, código, resultados y contadores; no repitió el análisis porque el cambio fue de nombre y navegación. Guardé el criterio de numeración en AGENTS.md y retiré los números reservados para fuentes pendientes.

### Aclaraciones de lectura de exchange_rates y variaciones en pesos

Pedí conservar las explicaciones de cobertura, decimales, extremos, cambios diarios e IQR en el notebook y el informe, identificar todas las tablas y actualizar las dudas y próximos pasos. La IA añadió leyendas a las 22 tablas del notebook y a todas las tablas del informe; cambió size/sum por evaluadas/señaladas y agregó extremos diarios en MXN por unidad extranjera. La ejecución secuencial y el contraste decimal conservaron la fuente. La sección 9 distingue la unidad ya aclarada y los criterios de lectura de las preguntas Q10/Q38–Q40 aún abiertas sobre procedencia, tratamiento operativo de MXN, vigencia, metodología y redondeo; ninguna pregunta se da por respondida por el cliente.

### 9 de noviembre de 2026 — Claridad en la identificación de la fuente

Pedí separar las medidas que aparecían unidas por barras. El informe de exchange_rates ahora presenta registros, columnas originales y cada fecha extrema en filas independientes. La IA conservó los valores, revisó los demás casos equivalentes en tablas Markdown y registró la convención en AGENTS; no cambió el notebook ni fue necesario repetir el análisis.

### 9 de noviembre de 2026 — Pendientes únicamente abiertos

Pedí retirar de las dudas los puntos que ya aclaré, sin mantener un historial de resueltos en ese registro. La IA ajustó DUDAS, preguntas y secciones de dudas del notebook e informe de exchange_rates; las definiciones se aplican en su explicación correspondiente. Permanecen abiertos proveedor, vigencia, tratamiento operativo de MXN, metodología y redondeo. La regla general queda en AGENTS y no cambian cálculos ni salidas.

### 9 de noviembre de 2026 — Exploración aislada actual de inventory

Pedí explorar inventory.json respetando las reglas y las ubicaciones. La IA revisó los prefijos 01 y 02 y creó [03_inventory.ipynb](../../notebooks/03_inventory.ipynb) y [su informe](../02_exploracion/resultados_inventory.md). El análisis lee solo el JSON y comprueba relaciones entre sus bloques; no es conciliación de fuentes. El SHA-256 `2355c6cab9ff00a707b5505a464a8f7e1a9bf5a2aa6c7a2b6b008f5299c8eada` coincide con el antecedente y se conserva.

Tengo 230,776 snapshots, 182 días y 1,268 pares completos en filas; 1,232 pares contienen algún N/A. Conservo 4,417 desconocidos separados de 11,726 ceros. Las rachas de cuatro ceros trimestrales están en T015, T023 y T038, sin afirmar quiebre operativo. Los mapeos tienen cinco ERP nulos; diez productos del catálogo carecen de referencia ERP informada. Las 282 vigencias cubren temporalmente los 70 productos bajo el escenario de última vigencia no posterior al día; unidad, base y política siguen pendientes. Amplío las preguntas existentes con evidencia aislada y mantengo 60 IDs sin enviarlas.

La IA ejecutó las diez celdas secuencialmente con Python directo y captura de salidas, validó nbformat y contrastó calendario, claves, ceros y rachas mediante biblioteca estándar, así como positividad de costos con Decimal. No se presenta esta ejecución como un kernel Jupyter. Los detalles técnicos están en AI_LOG. Mi revisión personal permanece pendiente. El siguiente notebook aislado será e-commerce, asignando número según los archivos presentes al crearlo; después corresponde conciliar claves, fechas, unidades y poblaciones e implementar el pipeline. Las menciones previas de inventario pendiente describen estados históricos.

### 9 de noviembre de 2026 — Alternativa de conciliación pendiente de aplicación

Pedí mantener visible en HALLAZGOS la posibilidad ya investigada de relacionar productos por nombre normalizado y coincidencia entre el número final del handle y el segmento numérico ERP. Mi decisión actual es tenerla presente para la futura conciliación, sin aplicarla todavía. La evidencia está en [conciliación de handles](../05_antecedentes/conciliacion_handles.md); no convierte los mapeos incompletos en informados ni modifica las exploraciones aisladas. Al retomar la conciliación corresponde revisar vigencia, unicidad y conflictos antes de plantear su uso.

### 9 de noviembre de 2026 — Exploración aislada de ecommerce y cierre de la etapa por fuente

Pedí completar ecommerce_orders.parquet con las reglas acordadas. La IA creó [04_ecommerce.ipynb](../../notebooks/04_ecommerce.ipynb) y [su informe](../02_exploracion/resultados_ecommerce.md); tengo completos los cuatro notebooks aislados. Este estado sustituye las menciones cronológicas anteriores a fuentes pendientes. La conciliación actual entre fuentes, el pipeline y las respuestas de negocio siguen pendientes.

La extracción conserva el SHA-256 `00c560b39425fe7f0088fbe20c66c2b8861d10c2c7006ba6e7335cdd6dfc856e`, igual al antecedente. Hay 9,947 registros, 33 handles y 365 días con presencia global. IDs únicos no confirman pedidos completos o pagados. Las monedas y sus importes se mantienen separados; no se consulta otro archivo de datos ni se reutilizan mapeos históricos como resultados actuales. No hay datos personales en salidas guardadas.

La ejecución técnica directa desde raíz y notebooks/ cubre nueve celdas, 18 tablas con leyendas y una gráfica SVG con escalas monetarias separadas. Los controles conservan columnas, conteos, importes por moneda y fuente. IQR señala cuatro filas EUR y deja sin evaluar las 6,942 filas MXN por IQR cero; ninguna señal es error confirmado. Mi revisión personal permanece pendiente. La evidencia técnica y las limitaciones de ejecución están en AI_LOG.

Mi siguiente paso es conciliar claves, unidades, fechas y monedas sobre las versiones actuales, distinguir enlaces exactos e inferidos, cuantificar cobertura y definir supuestos para implementar el pipeline. Reutilizo Q09/Q16/Q31–Q38/Q40/Q41/Q44–Q50 sin dar preguntas por enviadas o respondidas.

### 9 de noviembre de 2026 — Dudas fuera de los notebooks

Pedí retirar las secciones de dudas y próximos pasos de los cuatro notebooks y concentrar su seguimiento en [DUDAS.md](../03_negocio/DUDAS.md). La IA centralizó allí los tratamientos abiertos con sus identificadores existentes, retiró las secciones y referencias al banco de preguntas de los notebooks y conservó las limitaciones necesarias para leer los resultados. Las operaciones de cálculo, cifras y contadores no cambiaron; solo se ajustaron textos explicativos y sus representaciones guardadas. Los análisis siguen aislados y el estado de conciliación y pipeline no cambia.

## Estado actual: conciliación exploratoria terminada — 9 de noviembre de 2026

Pedí un EDA conjunto sin repetir los aislados. Tengo [05_conjunto.ipynb](../../notebooks/05_conjunto.ipynb), [su informe](../02_exploracion/resultados_conjunto.md) y el ejecutor `scripts/ejecutar_eda_conjunto.py`, que regenera ambos con los mismos resultados. Esta evidencia actual sustituye el uso del EDA histórico para evaluar conectores; las fuentes coinciden con los hashes de los cuatro informes individuales actuales. La diferencia histórica de sales permanece documentada, sin ocultarla ni modificar datos.

Los cruces m:1 y temporales conservan cada movimiento y sus importes originales: 74,141 registros físicos y 6,959 online tienen ERP exacto y costo previo; quedan 12,349 físicos y 2,988 online sin ERP. Las cuatro fuentes comparten 182 días desde 2025-10-01 hasta 2026-03-31. En I del semestre hay 12,687 registros con ERP sin snapshot, 213 con saldo desconocido y 565 con cero. FX cubre todas las órdenes extranjeras, con sensibilidad al redondeo documentada. No apliqué candidatos por nombre y número ni asigné tienda a online.

La IA ejecutó siete celdas con trece tablas desde raíz y notebooks/ mediante IPython y captura de salidas; esta validación no acredita arranque de kernel Jupyter ni revisión manual mía. Mi siguiente fase es implementar pipeline y modelo con conectores exactos, cuarentena explícita de excepciones y reglas financieras declaradas; las respuestas de negocio, pruebas del pipeline y propuesta AWS siguen pendientes. Centralizo las definiciones abiertas y tratamientos en DUDAS.md, reutilizando las preguntas existentes. El detalle de herramientas, verificaciones y limitaciones queda en AI_LOG.

## Estado vigente — 12 de noviembre de 2026

Pedí terminar la entrega e incorporé la respuesta compartida sobre costos unitarios globales en MXN, vigencias y ausencia de otra lista de equivalencias. La IA implementó scripts/pipeline.py y seis pruebas sintéticas; ejecutó el ETL sobre la versión actual de sales documentada en VERSION_FUENTES.md. Tengo modelo SQLite, cuatro respuestas y coberturas, propuesta AWS y correo preparado. Las menciones anteriores a pipeline pendiente describen el estado histórico. No se desplegó AWS ni se envió correo. Mi revisión personal y el acceso de evaluadores deben verificarse antes del envío. Los resultados completos están en outputs/etl y la instantánea agregada en docs/03_negocio/RESPUESTAS_NEGOCIO.md.

## Conclusión

Tengo los cuatro notebooks e informes aislados y la conciliación exploratoria actual ejecutados por la IA. Continúo con el pipeline y el modelo usando conectores comprobados y excepciones visibles, sin dar por confirmadas las unidades, reglas financieras ni respuestas finales.
