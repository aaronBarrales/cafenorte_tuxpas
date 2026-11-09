# Preguntas para validar la solución CaféNorte

Actualizado el 8 de noviembre de 2026. Banco de 60 preguntas relevantes para los datos entregados y una eventual implementación. No se ha enviado al cliente. Las primeras diez son las prioritarias; el banco completo sirve para descubrimiento, no para enviar 60 preguntas de golpe.

P0: afecta cifras o conciliación. P1: afecta interpretación, alcance o diseño. P2: mejora o decisión productiva que puede posponerse. Si no hay respuesta a una P0, la entrega debe explicitar el supuesto y cuantificar su impacto; no se detiene automáticamente todo el trabajo.

## Diez preguntas prioritarias

| ID | Pregunta | Prioridad y evidencia |
|---|---|---|
| Q01 | ¿Qué representa cada código I/E/N/P/T del POS y qué efecto debe tener sobre ingresos y unidades? | P0; todos sus importes son positivos. D001. |
| Q02 | ¿monto es el total de la línea o precio por unidad, y qué impuestos, descuentos o cargos incluye? | P0; falta desglose. D002. |
| Q03 | ¿costo_mxn es costo unitario, en qué unidad y con qué impuestos y gastos incluidos? | P0; determina margen. D007. |
| Q04 | ¿Existe un catálogo maestro completo que relacione SKU POS, SKU ERP y producto/variante de Shopify? | P0; diez SKU POS no llegan a ERP. D008. |
| Q05 | ¿El número final de los handles representa oficialmente el mismo producto que el número del SKU ERP? | P0; seis enlaces propuestos y cuatro ERP nulos, aún inferidos. D008. |
| Q06 | ¿Qué significa N/A en cantidad_en_stock y cómo se obtiene el saldo real en esos casos? | P0; 4,417 snapshots desconocidos. D009. |
| Q07 | ¿El archivo de inventario incluye todo el surtido por tienda o un subconjunto? ¿Por qué hay ventas de pares tienda–SKU sin snapshots? | P0; 12,687 filas I del semestre con ERP conocido y sin snapshot. D010. |
| Q08 | ¿A qué hora se toma el snapshot y representa stock físico, disponible o saldo después de reservas? | P0; 565 filas I coinciden con saldo cero. D011. |
| Q09 | ¿Las órdenes exportadas están pagadas y vigentes? ¿Dónde están cancelaciones, reembolsos y devoluciones? | P0; no hay estatus en Parquet. D012. |
| Q10 | ¿rate_to_mxn significa MXN por unidad extranjera y qué proveedor, tipo de cotización y fecha contable deben usarse? ¿MXN se trata con identidad 1? | P0; D013. [Evidencia aislada de tasas](#evidencia-del-eda-aislado-de-exchange-rates); la cobertura de operaciones pertenece al antecedente entre fuentes. |

## Ventas físicas y trazabilidad

| ID | Pregunta | Prioridad |
|---|---|---|
| Q11 | ¿Una compra con varios productos se exporta en varias filas con venta_id por línea? ¿Qué identifica venta_id y es estable entre extracciones? ¿Existe ticket_id e identificador de línea para reunir la compra sin depender de tienda y minuto? | P0; D003 y evidencia del EDA aislado detallada abajo. |
| Q12 | ¿Cómo se identifican ventas anuladas, sustituidas o corregidas y su vínculo con el registro original? | P0; no hay estatus ni vínculo. D014. |
| Q13 | ¿Un egreso siempre devuelve unidades al stock o también representa descuentos o ajustes sin movimiento físico? | P0; D001/D014. |
| Q14 | ¿Existe historial de precios de lista con inicio y fin de vigencia por producto, canal y tienda? | P1; D006. |
| Q15 | ¿Hay detalle de promociones, cupones, descuentos y autorizaciones de venta por debajo del costo? | P1; D006/D015. |
| Q16 | ¿Cantidad se expresa en piezas, bolsas, paquetes, gramos o unidades equivalentes, y coincide entre los tres sistemas? | P0; D007/D016. |
| Q17 | ¿Las tiendas o regiones aplican tarifas e impuestos distintos para el mismo SKU? | P1; D002/D006. |
| Q18 | ¿fecha_hora es hora local de cada tienda o una zona centralizada? ¿Cómo se manejan cambios de horario? | P0; D004. |
| Q19 | ¿Tenemos fechas de apertura/cierre y calendario operativo de las tiendas para interpretar días sin ventas? | P1; 476 tienda–días sin filas. D017. |
| Q20 | ¿Cuál es la copia original autorizada de sales y por qué cambió su formato de fechas y precisión? | P0 para trazabilidad; D018. |

## Evidencia del EDA aislado para Q11

La revisión de [sales](../02_exploracion/resultados_sales.md#11-validación-de-coincidencias-tienda-fechahora-y-producto), realizada sin cruzar otras fuentes, encontró **201 grupos con igual tienda y fecha/hora y SKU diferentes**, que reúnen 402 filas. Al exigir también moneda y comprobante iguales hay 186 grupos y 372 filas. `venta_id` no se repite entre filas.

**Pregunta ampliada para el cliente (Q11):** ¿una compra con varios productos se exporta en distintas filas con un venta_id por línea? ¿Qué identifica exactamente venta_id y es estable entre extracciones? ¿Existe un ticket_id compartido y un identificador de línea que permitan reconstruir la compra? ¿Las coincidencias por tienda y minuto pueden incluir distintas cajas o clientes, y se dispone de caja/terminal y hora con segundos?

**Motivo:** confirmar cómo contar tickets y evitar confundir coincidencias temporales con compras del mismo cliente. La evidencia es compatible con compras divididas por producto, pero no lo demuestra. No se propone agrupar tickets únicamente por fecha/hora y tienda. Esta ampliación desarrolla Q11, sin duplicar el banco de 60 preguntas. Pendiente de respuesta; no se ha enviado al cliente.

## Catálogo, costos e inventario

| ID | Pregunta | Prioridad |
|---|---|---|
| Q21 | ¿Qué atributos distinguen SKU con el mismo nombre: tamaño, presentación, receta o variante? | P1; 23 nombres repetidos. D016. |
| Q22 | ¿Los SKU y handles pueden cambiar o reutilizarse, y hay vigencias de sus equivalencias? | P1; D019. |
| Q23 | ¿Quién mantiene y aprueba las equivalencias entre sistemas y corrige los enlaces faltantes? | P1; D008/D019. |
| Q24 | ¿Los costos son globales o varían por tienda, almacén, proveedor, lote o canal? | P0; D007. |
| Q25 | ¿Una fecha de vigencia aplica desde el comienzo de ese día hasta el siguiente cambio, incluso si hay varias actualizaciones? | P0; D007/D020. |
| Q26 | ¿El costo usado para margen es estándar, promedio, último costo, FIFO u otra política? | P0; D020. |
| Q27 | ¿Cómo se registran compras, devoluciones, traslados, mermas y ajustes para reconciliar la evolución del stock? | P1; snapshots no incluyen movimientos. D021. |
| Q28 | ¿Existe un catálogo de surtido tienda–SKU con fechas de alta, baja y cierres temporales? | P0; D010. |
| Q29 | ¿Una fila ausente significa producto fuera de surtido, falta de extracción u otra condición? | P0; D010/D021. |
| Q30 | ¿Qué sistema permite distinguir stock físico, reservado, en tránsito y disponible para vender? | P1; D011. |

## E commerce y conciliación financiera

| ID | Pregunta | Prioridad |
|---|---|---|
| Q31 | ¿order_id identifica al pedido o a una línea? ¿Puede repetirse al agregar más productos o actualizaciones? | P0; D003/D012. |
| Q32 | ¿Se puede exportar product_id, variant_id, SKU de variante y line_item_id para tener claves más estables que handle? | P0; D008/D019. |
| Q33 | ¿amount corresponde al total de línea e incluye impuestos, envío, descuentos, comisiones o propinas? | P0; D002/D012. |
| Q34 | ¿fecha representa creación, pago, envío o reconocimiento de ingreso y en qué zona horaria está? | P0; D004/D012. |
| Q35 | ¿Qué tienda o almacén surte cada orden y ese stock está incluido en inventory.json? | P0 para inventario por canal; D022. |
| Q36 | ¿Hay pedidos con retiro en tienda, devoluciones cruzadas o ventas registradas tanto en POS como en Shopify? | P0; riesgo de doble conteo. D022. |
| Q37 | ¿Las operaciones extranjeras ya incluyen conversión o liquidación del procesador distinta de la moneda del pedido? | P0; D013. |
| Q38 | ¿Qué hora/zona y fecha de venta, pago o liquidación aplica a las tasas? ¿Cómo se tratan fines de semana, vigencias y diferencias cambiarias? | P0; D013. [Evidencia aislada](#evidencia-del-eda-aislado-de-exchange-rates). |
| Q39 | ¿Por qué EUR aparece exactamente en 22.0 en 63 fechas: precisión, límite del generador o política de tipo de cambio? | P1; observación, no error confirmado. D013. |
| Q40 | ¿Qué precisión de tasa y cálculo debe conservarse, en producción se redondea por línea, pedido o total y cuál es la tolerancia de conciliación? | P0; D023. [Evidencia aislada](#evidencia-del-eda-aislado-de-exchange-rates). |

## Calidad, validación y uso de la información

| ID | Pregunta | Prioridad |
|---|---|---|
| Q41 | ¿Qué reporte de cierre firmado o total de control por canal y mes puede usarse como referencia independiente? | P0; D024. |
| Q42 | ¿Qué política permite distinguir ventas debajo del costo reales de errores de captura o bases fiscales diferentes? | P1; D015/D024. |
| Q43 | ¿Hay márgenes o rangos de precios esperados por categoría y excepciones documentadas? | P1; D015. |
| Q44 | ¿Qué campos son obligatorios para el análisis y cuáles solo aplican a facturación o atención al cliente? | P1; RFC nulo en 8,462 órdenes. D025. |
| Q45 | ¿Podemos usar datos anonimizados y publicar código, muestras y resultados derivados del reto? | P0 para entrega; D025. |
| Q46 | ¿Se requieren nombres, correos, RFC y direcciones en el modelo analítico o pueden excluirse? | P1; las cuatro métricas no los necesitan. D025. |
| Q47 | ¿Quién puede acceder a información de clientes, cuánto tiempo debe conservarse y cómo se atienden correcciones? | P1 para producción; D025. |
| Q48 | ¿Qué equipo recibe los registros no conciliados y cuál es el plazo esperado para resolverlos? | P1; D024. |
| Q49 | ¿Los archivos son cargas completas o incrementales y pueden llegar cambios retroactivos? | P1; D026. |
| Q50 | ¿Se dispone de identificador de extracción, fecha de corte y conteos de origen para detectar faltantes? | P1; D026. |

## Operación y propuesta productiva

| ID | Pregunta | Prioridad |
|---|---|---|
| Q51 | ¿Qué persona aprueba las cifras y qué decisiones concretas tomará con el reporte? | P1; D024/D027. |
| Q52 | ¿Qué granularidad y frecuencia necesita el negocio: diaria, horaria o casi en tiempo real? | P1; D027. |
| Q53 | ¿Cuántos datos nuevos y usuarios habrá al mes y qué crecimiento se espera? | P1; D027. |
| Q54 | ¿Los USD 200 mensuales incluyen BI, impuestos, soporte, transferencias y servicios existentes, o solo infraestructura nueva? | P0 para propuesta; D028. |
| Q55 | ¿Qué región, servicios, redes, permisos y herramientas de BI ya están habilitados en la cuenta AWS? | P1; D028. |
| Q56 | ¿Cómo se extraen los sistemas actuales: archivos, API o base de datos, con qué límites y costos? | P1; D026/D028. |
| Q57 | ¿Qué retraso y pérdida de datos son aceptables y cómo se espera recuperar una carga fallida? | P1; D029. |
| Q58 | ¿Quién operará las cargas y recibirá alertas de fallos o sobrecostos? | P1; D029. |
| Q59 | ¿Qué requisito de auditoría, cifrado, acceso por rol y separación de ambientes exige el cliente? | P1; D025/D029. |
| Q60 | ¿Qué funcionalidad puede quedar para una segunda fase y qué evidencia define la aceptación de la primera? | P1; D027. |

## Decisiones que resolveremos dentro del reto

La consigna pide resolver las ambigüedades de sus cuatro métricas con criterio propio. Se propone documentar corte 2026-03-31, semestre octubre–marzo, trimestre enero–marzo, MoM abril–marzo y una definición explícita de rotación y margen. Estas decisiones no se agregan como preguntas que obliguen al reclutador a diseñar la solución.

Se solicitaría al cliente únicamente la semántica, completitud y referencias de control de las fuentes. Si no responde, mostrar escenarios y cobertura, conservar desconocidos y evitar afirmar resultados globales con datos parciales. Ninguna pregunta de este archivo ha sido enviada por correo.

## Evidencia del EDA aislado de exchange rates

Conecto estas dudas con [resultados_exchange_rates.md](../02_exploracion/resultados_exchange_rates.md), calculado únicamente desde exchange_rates.csv; no uso operaciones de otras fuentes ni tasas externas como evidencia.

| Pregunta existente | Evidencia observada y motivo |
|---|---|
| Q10 y Q38 / D013 | Hay USD y EUR con una fila diaria por moneda durante 365 días, incluidos fines de semana; no hay filas MXN, proveedor, hora/zona o tipo de cotización. Necesito confirmar unidad y vigencia antes de aplicar una conversión; continuidad no demuestra actualización efectiva. |
| Q39 / D013 | EUR repite exactamente 22.0 en 63 fechas y es su máximo observado. Necesito confirmar metodología, precisión o posibles límites; no es un error demostrado. |
| Q40 / D023 | Hay distinta cantidad de decimales escritos y falta una política de precisión y redondeo. No deduzco precisión económica solo de los ceros finales omitidos. |

Mantengo las 60 preguntas, ampliando las existentes en lugar de duplicarlas. No las he enviado ni he recibido confirmaciones; Q37 requiere revisar operaciones y queda fuera de este análisis aislado.

## Conclusión

Priorizo confirmar la semántica y completitud de las fuentes, incluida la clave real del ticket. Mantengo estas preguntas pendientes de respuesta y no condiciono todo el avance a recibirlas; documentaré los supuestos y límites que adopte.
