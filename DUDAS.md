# Dudas y supuestos del proyecto

Registro iniciado el 7 de noviembre de 2026. Cada duda conserva su evidencia, impacto, estado y eventual resolución. Una hipótesis no equivale a una regla confirmada.

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
