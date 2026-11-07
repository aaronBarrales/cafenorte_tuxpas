# Dudas y supuestos del proyecto

Registro iniciado el 7 de noviembre de 2026. Cada duda conserva su evidencia, impacto, estado y eventual resolución. Una hipótesis no equivale a una regla confirmada.

Banco completo de consultas: [PREGUNTAS_CLIENTE.md](PREGUNTAS_CLIENTE.md), 60 preguntas con diez prioritarias. Evidencia integral: [EDA completo](docs/EDA_COMPLETO.md). Fecha límite indicada por el autor: martes 10 de noviembre de 2026 antes de las 12:00 p. m., hora de Ciudad de México.

## D009 Obtención de datos y frecuencia de actualización

**Origen:** consulta del autor sobre la operación del pipeline y solicitud de agregar la pregunta. **Estado:** abierta. **Prioridad:** alta para la arquitectura productiva.

**Pregunta al cliente:** ¿Cómo podemos obtener datos de cada sistema y con qué frecuencia necesitan ver los resultados?

**Aspectos por confirmar:** ¿El POS, el ERP y Shopify entregarán archivos manualmente, exportaciones automáticas o acceso mediante API o base de datos de lectura? ¿Quién habilita y mantiene cada acceso? ¿La actualización debe ser diaria, por hora o con otra frecuencia? ¿A qué hora estarán disponibles todas las fuentes del mismo corte y qué hacemos si alguna no llega?

**Evidencia:** el reto proporciona archivos para desarrollar el pipeline, pero no confirma los mecanismos de integración productiva ni proporciona accesos a los sistemas. Recibir archivos manualmente y procesarlos automáticamente son decisiones compatibles.

**Impacto:** determina las integraciones, los permisos, la programación, los controles de disponibilidad, la prevención de duplicados, los costos y los compromisos de actualización. No se puede prometer una conexión directa al ERP sin conocer sus capacidades y accesos.

**Tratamiento actual:** usar los archivos entregados para el reto. Para producción, documentar como propuesta una primera fase basada en archivos, pendiente de acordar responsables y frecuencia; evaluar conexiones directas tras confirmar su viabilidad. No presentar ninguna modalidad ni frecuencia como aceptada por el cliente.

**Resolución y evidencia de confirmación:** pendientes.

## D001 Qué representa tipo_comprobante en sales

**Origen:** pregunta del autor. **Estado:** abierta. **Prioridad:** alta.

**Pregunta:** ¿Qué representa la columna `tipo_comprobante` de `sales.csv`? ¿Usa el catálogo de tipos de CFDI del SAT o un catálogo propio del POS? ¿Cómo debe afectar cada código a los ingresos y a las unidades vendidas?

**Evidencia observada:** aparecen `I` (82,518 filas), `E` (3,079), `N` (288), `P` (451) y `T` (154). Todos tienen cantidades e importes positivos. Los códigos por sí solos no indican el signo analítico que corresponde aplicar.

**Referencia externa:** esas letras coinciden con Ingreso, Egreso, Nómina, Pago y Traslado en la documentación del SAT. Esta coincidencia es una hipótesis sobre la fuente, no confirma el diccionario del POS. Fuente: [SAT, Formato de Factura Anexo 20](https://wwwmat.sat.gob.mx/cs/Satellite?c=ConsultaInfo&childpagename=SatTyR%2FConsultaInfo%2FSAT_LandingConsultaInformacion&cid=1462228635025&packedargs=d%3DTouch&pagename=TySWrapper).

**Impacto:** sumar todos los registros como ventas podría incluir movimientos ajenos a las ventas y sumar egresos con signo equivocado. Tampoco se puede asumir que todo egreso implica devolución física de inventario.

**Tratamiento actual:** conservar código, cantidad e importe originales. El perfil reporta sumas por código, sin presentarlas como ventas netas. Antes de las métricas, documentar una interpretación explícita y comprobar su impacto. Si no hay respuesta del cliente, resolver la ambigüedad como un supuesto justificado del reto.

**Resolución y evidencia de confirmación:** pendientes.

## D002 Qué mide monto

**Estado:** abierta. **Prioridad:** alta.

¿`monto` es el importe total de la fila o el precio por unidad? ¿Incluye IVA, descuentos o devoluciones? ¿Está expresado siempre en la moneda indicada?

**Evidencia:** existe `cantidad`, pero no hay columnas separadas de precio unitario, impuestos o descuento. Todas las filas de esta fuente indican MXN.

**Impacto:** multiplicar un total de línea por `cantidad` duplicaría el efecto de las unidades. El margen exige ingresos y costos con bases comparables.

**Tratamiento actual:** conservar `monto` sin multiplicarlo por `cantidad`; no afirmar todavía que representa ingreso neto ni precio unitario.

## D003 Qué representa una fila y venta_id

**Estado:** abierta. **Prioridad:** alta.

¿Una fila es una línea de ticket, una venta completa o un movimiento contable? ¿`venta_id` identifica el movimiento o el ticket? ¿Existe una referencia entre un egreso y la venta original?

**Evidencia:** los 86,490 IDs son únicos y cada fila tiene un SKU. El archivo no incluye UUID de CFDI, ticket relacionado ni estatus de cancelación.

**Impacto:** define la clave del modelo, la conciliación de devoluciones y la posibilidad de medir tickets. Un ID único en esta muestra no demuestra que sea una clave estable en cargas futuras.

**Tratamiento actual:** trabajar al nivel de registro de origen y no equiparar el conteo de filas con el de tickets.

## D004 Zona horaria de fecha_hora

**Estado:** abierta. **Prioridad:** media.

¿Las marcas de tiempo representan hora local de cada tienda, una zona centralizada o UTC? ¿Existe un catálogo de tiendas con ubicación y zona horaria?

**Evidencia:** `fecha_hora` no incluye desplazamiento horario; el contexto del reto abarca regiones distintas.

**Impacto:** los cortes diarios y mensuales y la conciliación con Shopify pueden cambiar al convertir fechas.

**Tratamiento actual:** conservar la fecha y hora sin asignar una zona no confirmada.

## D005 Fecha de corte de las ventanas del reto

**Estado:** supuesto propuesto, pendiente de conciliar las otras fuentes. **Prioridad:** alta.

Los datos de ventas terminan el 31 de marzo de 2026. Se propone usar un corte explícito basado en la cobertura de las fuentes, en lugar de la fecha de ejecución, para que los resultados sean reproducibles. Falta decidir si el último trimestre es calendario completo o tres meses móviles y comprobar cobertura conjunta.

**Tratamiento actual:** no aplicar todavía ventanas de negocio. Registrar la decisión y sus límites en el README antes de producir las cuatro respuestas. Esta ambigüedad se resolverá con criterio documentado, conforme al reto.

## D006 Origen y variación del precio observado por SKU

**Origen:** observación del autor al filtrar `CN-00003` en Excel. **Estado:** abierta. **Prioridad:** alta.

**Pregunta:** ¿Cómo se determina el importe cobrado por SKU? ¿Existen listas de precios con vigencia, precios por tienda, promociones o descuentos? ¿Se dispone de ese historial para explicar las diferencias?

**Evidencia verificada en sales:** las cuatro filas de la captura son de tipo `N`, por lo que no deben interpretarse automáticamente como ventas. Sus cantidades y montos son: 1 y 165.67; 1 y 164.09; 2 y 321.38; 2 y 326.56. Si `monto` es total de línea, los cocientes por unidad son 165.67, 164.09, 160.69 y 163.28 MXN. Cambian tanto la fecha como la tienda: estas filas no permiten atribuir la variación exclusivamente al tiempo.

El SKU tiene 1,175 registros en total. Aun limitando el análisis a los 1,116 registros tipo `I`, hay 853 cocientes distintos de `monto / cantidad` antes de redondear, con mínimo 155.10 y máximo aproximado 168.528571 MXN. Esto demuestra variación del cociente, no sus causas ni que sea precio de lista.

**Evidencia en inventario:** `catalogo.productos` contiene `cost_history` con `fecha_vigencia`, `costo_mxn` y `proveedor`. Es un historial de costos, no una lista de precios de venta. Existen `sku_mappings` para relacionar claves POS y ERP; su cobertura debe validarse antes de cruzar costos. En esta revisión no se logró leer el esquema de Parquet porque el entorno no tiene `pyarrow`; queda pendiente comprobar los campos de e-commerce. No se afirma que se haya descartado un historial de precios en todas las fuentes.

**Impacto:** confundir monto total, precio unitario, precio de lista y costo puede distorsionar ingresos y márgenes. La variación por sí sola no prueba un error ni una promoción.

**Tratamiento actual:** preservar el monto original. Usar `monto / cantidad` solo como diagnóstico condicionado a confirmar D002, y no reconstruir listas de precios. Para el margen, proponer monto de línea menos cantidad por costo unitario vigente, sujeto a confirmar impuestos, descuentos, unidades, comprobantes y cobertura de costos. Un costo ausente no se sustituirá por cero.

**Resolución y evidencia de confirmación:** pendientes.

## Evidencia adicional para D004

La revisión de `inventory.json` encontró `tiendas_info` con `tienda_id`, `ciudad`, `region` y `timezone`. Sí existe un catálogo de zonas horarias por tienda. Queda pendiente validar su cobertura y confirmar si `fecha_hora` del POS está registrada en esa hora local; el catálogo por sí solo no lo demuestra.

## D007 Base y vigencia de los costos del ERP

**Origen:** investigación de `ERP-PROV-MX-057-C`. **Estado:** abierta. **Prioridad:** alta.

¿`costo_mxn` representa costo por unidad? ¿Qué unidad e impuestos incluye? ¿Cada `fecha_vigencia` marca el inicio de un costo aplicable hasta el siguiente cambio? ¿El costo es global o varía por tienda?

**Evidencia:** el producto corresponde a `CN-00057`, Premium Cafe Grano, y tiene cinco costos con vigencia entre 2024-10-01 y 2025-11-30. Las entradas tienen fecha, costo y proveedor, sin tienda, unidad de medida ni fin explícito de vigencia. Ver [historial investigado](docs/producto_ERP-PROV-MX-057-C.md).

**Tratamiento propuesto:** cruce temporal por SKU con la última vigencia no posterior a la operación, bajo supuesto documentado de costo unitario global. No usar costos futuros ni sustituir costos ausentes por cero. Confirmar la base antes de presentar márgenes como definitivos.

## D008 Handles ausentes y cobertura del mapeo de productos

**Origen:** el autor identificó `handle: null` para `ERP-PROV-MX-015-D`. **Estado:** abierta. **Prioridad:** alta para conciliación con e-commerce.

**Pregunta:** ¿Los handles nulos representan productos que no se venden en Shopify o correspondencias incompletas? ¿Existe una clave alternativa confiable para conciliar esas órdenes? ¿Hay otras correspondencias fuera del archivo?

**Evidencia:** `sku_mappings` tiene 65 registros: 38 con handle nulo y 27 con handle informado. En esta muestra no se encontraron duplicados entre las claves no nulas de cada campo `sku_pos`, `sku_erp` y `handle`. El catálogo contiene 70 productos, por lo que no debemos equiparar automáticamente el número de mapeos con el catálogo completo. No se ha realizado aún la conciliación exhaustiva de cobertura entre conjuntos.

Para el caso indicado, el mapeo POS–ERP sí existe: `CN-00015` → `ERP-PROV-MX-015-D`. El catálogo tiene nombre `Especial Cafe Molido`, categoría `cafe_molido` e historial de costos. Falta de handle no equivale a falta de nombre o descripción. El handle es un identificador usado en la URL del producto en Shopify, según su [documentación oficial](https://shopify.dev/docs/api/storefront/2026-01/objects/Product); la semántica concreta del mapeo del reto aún debe contrastarse con las órdenes.

También se observó el caso `CN-00016` con `sku_erp: null` y `handle: null`, un problema distinto que puede impedir conciliar sus ventas físicas con costos e inventario.

**Tratamiento propuesto:** preservar nulos; mantener las operaciones con estado de conciliación explícito; usar la relación POS–ERP donde esté informada y validada. No inventar un handle desde el nombre ni concluir que no hay ventas online. Si solo se dispone de handle para un cruce, no unir entre sí registros con claves nulas. Revisar las claves reales de Parquet antes de decidir alternativas. No eliminar silenciosamente ventas no conciliadas ni asignarles costo cero.

**Actualización tras leer e-commerce:** el Parquet contiene `product_handle`, sin SKU POS o ERP. Hay 33 handles distintos; 27 coinciden exactamente con el mapeo (8,098 filas) y 6 no tienen correspondencia (1,849 filas). Cuatro de los no conciliados tienen sufijos coincidentes con SKU sin handle (013, 030, 032 y 052), sin que se haya confirmado la regla de sufijos. Por tanto, no adoptar «sin handle = no se vende online». Para 015 no apareció sufijo `-015`, lo que tampoco prueba ausencia de ventas. Ver [análisis](docs/analisis_ecommerce.md).

## Evidencia adicional para D006 y D007

**Seguimiento D008:** al combinar nombre normalizado y número del SKU ERP se identificaron candidatos únicos para los seis handles pendientes. La regla coincide con 23/23 mapeos completos existentes; cuatro mapeos con handle tienen ERP nulo y requieren revisión aparte. Las propuestas y sus límites están en [conciliación de handles](docs/conciliacion_handles.md). No se modificaron las fuentes ni se aplicaron esas relaciones como confirmadas.

Se revisaron las 11 columnas de e-commerce y no contienen una lista de precios fijados, vigencias de tarifas ni campos separados de impuestos o descuentos. Hay amount y cantidad para estudiar los importes de órdenes, sujeto a su semántica. Se documentó la venta V00000000 como [caso candidato de margen negativo](docs/casos_margen.md): 355.43 MXN frente a costo propuesto de una unidad de 466.56 MXN, margen condicionado de −111.13 MXN en T033.

## D009 a D029 Dudas surgidas de la exploración completa

Estado: abiertas, salvo las comprobaciones técnicas expresamente indicadas. Los tratamientos son propuestas para avanzar, no respuestas del cliente.

| ID | Pregunta o asunto | Evidencia o impacto | Tratamiento propuesto |
|---|---|---|---|
| D009 | ¿Qué significa N/A en existencias y cómo se corrige? | 4,417 snapshots con texto N/A; no es cero ni null literal. | Normalizar a desconocido con bandera, conservar origen y reportar cobertura; sin imputación automática. |
| D010 | ¿Qué surtido tienda–SKU debe aparecer en inventario y por qué hay ventas sin snapshot? | 1,268 pares completos de 182 días; 12,687 filas I del semestre con ERP exacto carecen de snapshot. | No asumir todo el catálogo activo en todas las tiendas; alinear numerador y denominador de rotación y reportar el universo no cubierto. |
| D011 | ¿El snapshot representa cierre, inicio, stock físico o disponible y reservas? | 565 filas I coinciden con saldo cero ese día; no prueba error. | No equiparar saldo de cierre con quiebre durante todo el día; conservar definición operativa como límite. |
| D012 | ¿Las órdenes son líneas pagadas, canceladas, reembolsadas o solo creadas y qué incluye amount? | IDs únicos, sin estado ni desglose financiero. | Tratar filas como registros de origen; explicitar supuesto de elegibilidad y monto total, sin afirmar ingreso contable validado. |
| D013 | ¿Cuál es la convención, proveedor, fecha y precisión del tipo de cambio? | 365 tasas por moneda; cobertura diaria completa; EUR = 22.0 en 63 fechas. | Proponer amount por tasa del día y MXN identidad; documentar redondeo y no declarar anomalía de mercado sin validación externa. |
| D014 | ¿Dónde están cancelaciones, sustituciones y vínculo entre devolución y operación original? | POS no incluye estatus ni relación entre comprobantes. | No deduplicar ni restar dos veces por semejanza; separar ajustes financieros y movimientos físicos. |
| D015 | ¿Cuándo se autorizan ventas bajo costo y qué rangos o promociones se esperan? | 2,369 filas I dan margen candidato negativo con costo y mapeo exactos. | Mostrar casos y cobertura; no corregir precios automáticamente ni atribuir fraude/error. |
| D016 | ¿Qué presentación o unidad distingue productos con el mismo nombre? | 23 nombres repetidos; no hay campo explícito de unidad. | Usar SKU como identidad; normalizar nombres solo para proponer relaciones y validar unidad antes de margen/rotación. |
| D017 | ¿Qué calendario operativo y altas/bajas de tiendas debemos usar? | 476 tienda–días sin filas dentro del calendario de sales. | No convertir ausencia de actividad en falla de extracción ni inventar ventas cero confirmadas. |
| D018 | ¿Cuál es la copia original de sales y cómo ocurrió el cambio de fechas? | Hash y formato distintos respecto al perfil inicial; segundos ya no aparecen. | El parser ya acepta ambos formatos observados; conservar hashes y no reconstruir precisión ni sobrescribir la fuente. |
| D019 | ¿Hay claves estables y vigencias de los mapeos ante cambios de SKU o handle? | Mapeos incompletos sin fechas ni product_id/variant_id. | Versionar equivalencias y distinguir exactas, inferidas, incompletas y no conciliadas. |
| D020 | ¿Qué política de costo se utiliza y desde qué instante aplica cada vigencia? | 282 entradas, 70 productos, sin fechas repetidas; sin método de costeo. | Última vigencia no posterior a la fecha como supuesto; no asumir FIFO o promedio de compras a partir de este historial. |
| D021 | ¿Existen movimientos y controles de extracción para reconciliar stock? | Solo snapshots; surtido parcial por tienda. | No exigir ecuación de compras/ventas sin movimientos ni rellenar pares ausentes con cero. |
| D022 | ¿Qué almacén surte Shopify y hay retiros/devoluciones o ventas duplicadas en POS? | Órdenes sin tienda de cumplimiento ni referencia POS. | Canal online separado; no atribuir a tienda por dirección del comprador ni incorporar sus unidades a stock físico sin enlace. |
| D023 | ¿Se redondea por línea, pedido o total y con qué tolerancia? | amount almacenado como double; conversión produce más de dos decimales. | Decimal para cálculo; preservar originales y declarar política de redondeo antes de conciliar. |
| D024 | ¿Quién aprueba los números y qué cierres independientes se usan como control? | Ausencia de nulos no demuestra exactitud comercial. | Conciliar contra origen y pedir reportes de referencia; documentar tolerancias, excepciones y responsable. |
| D025 | ¿Qué puede publicarse y qué información personal requiere el modelo? | Datos de clientes en Parquet; RFC nulo en 8,462 filas, innecesario para estas métricas. | Mantener fuentes/CSV locales; usar esquema y agregados en documentación; modelo analítico con mínimos campos necesarios. |
| D026 | ¿Cómo se extraen datos completos/incrementales, correcciones y cargas tardías? | Archivos estáticos, sin identificador de lote ni contrato de actualizaciones. | Entrega local por lotes reproducible; proponer idempotencia, manifiesto y reconciliación para producción. |
| D027 | ¿Qué decisiones, usuarios, volúmenes y frecuencia determinan la aceptación? | El reto pide cuatro respuestas y demo, no un sistema de tiempo real. | Priorizar pipeline y resultados auditables; dimensionar producción después de confirmar operación. |
| D028 | ¿Qué incluye el presupuesto AWS y qué recursos/región ya existen? | Objetivo de USD 200/mes, sin desglose de BI, soporte o impuestos. | Propuesta con supuestos de carga y costos verificados; no dar por existente un servicio ni tarifa. |
| D029 | ¿Quién opera, qué recuperación es aceptable y cómo se gestionan accesos y alertas? | No hay SLA ni responsables productivos definidos. | Incluir fases, responsable, alertas y recuperación proporcional; no sobredimensionar por supuestos. |

## Decisiones analíticas internas del reto

D005 se resolverá con corte propuesto 2026-03-31 y ventanas de datos, sin esperar una decisión del cliente. La rotación usará una población consistente de ventas e inventario, quiebres requerirán al menos cuatro días consecutivos observados y MoM no tendrá base inventada para abril de 2025 en e-commerce. El margen por operación y el margen agregado por producto–tienda se mostrarán como conceptos distintos. Las definiciones finales y límites deben quedar en el README al implementar; ver [plan de entrega](PLAN_ENTREGA.md).
