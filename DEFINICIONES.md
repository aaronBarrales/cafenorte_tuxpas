# Definiciones importantes del proyecto

Glosario para interpretar las fuentes y explicar las decisiones de CaféNorte. Se distinguen las definiciones generales de los supuestos aún pendientes en este reto.

## Sistemas de origen

| Término | Significado | Aplicación en CaféNorte |
|---|---|---|
| POS | Point of Sale o sistema de punto de venta. Registra operaciones de venta y cobro. Puede incluir cajas, terminales y software. | El reto identifica `sales.csv` como exportación del POS de tiendas físicas. No sabemos si cada tienda tiene un sistema independiente o si comparten una plataforma central. |
| ERP | Enterprise Resource Planning o sistema de planificación de recursos empresariales. Integra procesos como compras, inventario, proveedores y contabilidad, según su configuración. | `inventory.json` procede del ERP legacy e incluye catálogo de productos, historial de costos, existencias diarias, equivalencias de SKU e información de tiendas. |
| Legacy | Sistema heredado de una etapa anterior, que sigue funcionando. | Es la descripción del ERP en el reto. No demuestra que esté desconectado, obsoleto ni instalado localmente. |
| Nube | Infraestructura y servicios accesibles por red y operados en centros de datos de un proveedor. | Tanto un POS como un ERP pueden funcionar en la nube, en servidores propios o de forma híbrida. Los archivos entregados no confirman el alojamiento de los sistemas actuales. AWS corresponde a la propuesta futura del reto. |
| E-commerce | Canal de venta por internet. | Las órdenes de Shopify se entregan en `ecommerce_orders.parquet`. |

## Productos e importes

| Término | Significado | Precaución para este proyecto |
|---|---|---|
| SKU | Stock Keeping Unit: código para identificar una referencia de producto dentro de un sistema. | Un mismo producto puede tener códigos diferentes en POS, ERP y Shopify. No es necesariamente un código universal ni un código de barras. |
| Mapeo de SKU | Correspondencia explícita entre identificadores de distintos sistemas. | `sku_mappings` relaciona `sku_pos`, `sku_erp` y `handle`. Hay que validar cobertura y duplicados antes de cruzar fuentes. |
| Handle | Identificador legible de un producto en Shopify, utilizado en su URL. Es distinto del nombre visible y de la descripción del producto. | Aparece en los mapeos de inventario; la relación con las órdenes de Shopify debe comprobarse. Hay 38 mapeos sin handle de un total de 65; un nulo no demuestra que el producto carezca de nombre ni que no se venda online. |
| Precio de lista | Precio publicado o establecido antes de los ajustes que correspondan. | No se ha identificado una lista histórica de precios de venta en el catálogo del inventario. |
| Monto de una fila | Importe monetario registrado para esa fila. | `sales.monto` no se llama precio unitario. Debemos confirmar si es total de línea y si incluye impuestos y descuentos. |
| Importe efectivo por unidad | Cociente del importe de una línea entre sus unidades, cuando ambos representan esa misma operación. | `monto / cantidad` es un diagnóstico condicionado a confirmar el significado de los campos; no prueba el precio de lista ni explica su variación. |
| Costo | Valor asociado a adquirir o producir un producto; su base depende de la política del sistema. | El ERP contiene `costo_mxn`. Debemos confirmar si es costo por unidad, su unidad de medida, impuestos y componentes incluidos. No equivale al precio de venta. |
| Historial de costos | Valores de costo asociados a fechas de vigencia. | Se encuentra en `catalogo.productos[].cost_history`, con `fecha_vigencia`, `costo_mxn` y `proveedor`. |
| Fecha de vigencia | Fecha desde la que se aplica un valor según una regla temporal. | Se propone elegir el costo con la última fecha de vigencia menor o igual a la fecha de venta; hay que documentar la regla y comprobar que no existan fechas duplicadas por producto. No se debe usar un costo futuro. |
| Margen bruto en dinero | Ingreso neto menos el costo de los bienes vendidos. | Si monto es ingreso de línea y costo es unitario comparable, la fórmula candidata es `monto - cantidad × costo_vigente`. Sigue pendiente validar comprobantes, impuestos, descuentos y unidades. |
| Margen bruto porcentual | Margen bruto dividido entre ingreso neto, multiplicado por 100. | Con ingreso cero requiere tratamiento explícito; no confundir con el recargo sobre costo. |
| MXN | Código de moneda del peso mexicano. | Los montos de sales revisados están en MXN; el costo del catálogo se denomina `costo_mxn`. |

## Inventario y análisis

| Término | Significado | Aplicación o decisión pendiente |
|---|---|---|
| Snapshot | Fotografía del estado de un sistema en un momento o fecha. | El JSON tiene snapshots diarios de existencias por tienda y SKU. No incluye movimientos transaccionales, según su metadata. |
| Stock o existencias | Cantidad de un producto disponible o registrada en inventario. | El campo es `cantidad_en_stock`; hay que revisar su significado y calidad antes de calcular quiebres. |
| Quiebre de stock | Situación en la que un producto no está disponible para atender la demanda. | El reto requiere identificar episodios de más de tres días. Habrá que definir stock cero o negativo, continuidad de fechas y tratamiento de días sin snapshot. La falta de una fila no demuestra stock cero. |
| Rotación de inventario | Medida de cuánto se vende o consume respecto al inventario promedio durante un período. | Debemos documentar si se calcula en unidades o en valor. El numerador y denominador deben usar bases comparables. |
| Granularidad | Qué representa exactamente una fila del conjunto de datos. | En sales aún falta confirmar si es línea de ticket o movimiento. Un ID único no demuestra que cada fila sea un ticket completo. |
| Conciliación | Comparación y ajuste documentado de fuentes para obtener cifras coherentes. | Incluye productos, monedas, fechas, comprobantes y controles de conteos e importes. |
| MoM | Month over Month: crecimiento respecto al mes anterior. | `(ventas_mes_actual / ventas_mes_anterior - 1) × 100`, con tratamiento explícito de meses sin cobertura o base cero. |
| Fecha de corte | Límite temporal fijo del análisis. | Debe basarse en la cobertura de las fuentes y quedar documentado para reproducir las ventanas del reto. |
| Supuesto | Interpretación adoptada cuando falta información suficiente. | Debe tener justificación, impacto y estado en `DUDAS.md`; no se presenta como confirmación del cliente. |

## Cómo se relacionan los conceptos

En Shopify, un handle puede verse como `premium-cafe-grano-057` en una ruta ilustrativa `/products/premium-cafe-grano-057`. La descripción es el texto que explica el producto y el nombre es su título; son conceptos separados. Referencia: [documentación oficial de Shopify sobre Product.handle](https://shopify.dev/docs/api/storefront/2026-01/objects/Product).

El POS aporta operaciones e importes registrados. El ERP aporta catálogo, costos e inventario. El pipeline relacionará los códigos de producto y las fechas para calcular métricas. El alojamiento en nube o servidores propios es una decisión distinta de esas funciones.

Evidencia local: `datos/sales.csv` y `datos/inventory.json`, revisados el 7 de noviembre de 2026. Las interpretaciones abiertas se conservan en [DUDAS.md](DUDAS.md). El caso de costo investigado se encuentra en [el historial de ERP-PROV-MX-057-C](docs/producto_ERP-PROV-MX-057-C.md).
