# Resultados del EDA conjunto: conectores entre fuentes

## 1. Objetivo y alcance

Pedí comprobar si puedo conectar ventas físicas, pedidos online, inventario y tipos de cambio, sin repetir los perfiles individuales. Este análisis **cruza las cuatro fuentes actuales**: evalúo cobertura referencial, cardinalidad, fechas, costo vigente y conservación de registros. No recalculo distribuciones aisladas ni presento respuestas finales de negocio.

Trabajo al nivel de registro de origen en cada canal. Uso el catálogo y las equivalencias explícitas de inventory como dimensiones; no uno ventas físicas con pedidos online como si fueran una misma transacción. Mantengo sin aplicar los candidatos por nombre y número. Una coincidencia técnica no confirma unidad física, estatus comercial ni ausencia de doble conteo.

## 2. Lectura y versión conjunta

Leo del Parquet únicamente claves y medidas comerciales; excluyo los campos personales incluso de la lectura. Conservo las columnas originales y añado derivadas en copias. `dia`, desde fecha_hora POS o fecha online, elimina la hora sin asignar zona; los textos no interpretables producirían NaT y detendrían el cruce. `dia` en snapshots y tasas interpreta fecha. Comparo las huellas con los informes individuales actuales, no con el estudio histórico de sales.

**Manifiesto de esta conciliación**

**Leyenda:** Identifico los cuatro archivos; SHA-256 es una huella de bytes, no una certificación comercial. Una diferencia exige documentar la nueva versión antes de interpretar resultados. Muestro todas las filas; omito el índice de pandas.

| Fuente | SHA-256 | Coincide con informe individual |
| --- | --- | --- |
| sales.csv | 1a456213c5590cf8c8d93438caf52c872ba4abd64a1b7003c74cc43acec8d01b | True |
| inventory.json | 2355c6cab9ff00a707b5505a464a8f7e1a9bf5a2aa6c7a2b6b008f5299c8eada | True |
| ecommerce_orders.parquet | 00c560b39425fe7f0088fbe20c66c2b8861d10c2c7006ba6e7335cdd6dfc856e | True |
| exchange_rates.csv | a0e827ec1e048cf397584eca3d692cb5b5b1f6b477fb78efca2fdbd2f488bddf | True |

## 3. Contratos de unión: clave y granularidad

Compruebo la unicidad del lado derecho antes de cada unión muchos a uno (`m:1`): varias filas de movimientos pueden apuntar a una sola fila de dimensión. Excluyo claves nulas de las dimensiones de equivalencias para impedir que pandas enlace nulos entre sí. No elimino duplicados para hacer pasar una validación: una repetición detendría la ejecución.

`sku_erp` se incorpora desde sku_mappings usando sku POS o product_handle, con igualdad literal; no normalizo ni completo claves. `estado_enlace` diferencia ausencia de equivalencia, ERP nulo, ERP fuera de catálogo y enlace exacto. Esto permite separar falta de mapeo de falta de costo o snapshot. Las claves de las tablas de diagnóstico son conteos; no expongo identificadores de clientes.

**Cardinalidad de los conectores**

**Leyenda:** Claves candidatas del lado derecho; conteos antes de unir. La dimensión de handles excluye sus nulos; no sustituyo duplicados por una fila arbitraria. Muestro todas las filas; omito el índice de pandas.

| Conector | Clave derecha | Filas derechas | Claves nulas | Repeticiones adicionales |
| --- | --- | --- | --- | --- |
| POS a equivalencia | sku_pos | 65 | 0 | 0 |
| Online a equivalencia | handle | 27 | 0 | 0 |
| ERP a producto | sku_erp | 70 | 0 | 0 |
| POS a tienda | tienda_id | 40 | 0 | 0 |
| Movimiento a saldo diario | dia, tienda_id, sku_erp | 230776 | 0 | 0 |
| Moneda extranjera a tasa diaria | dia, currency | 730 | 0 | 0 |

**Cobertura real de producto por canal**

**Leyenda:** Toda la ventana de cada canal; importes en la moneda indicada, cantidades sin equivalencia física confirmada. Cada registro pertenece a un solo estado. Claves se cuentan dentro de moneda; no se suman como claves únicas globales. Muestro todas las filas; omito el índice de pandas.

| Canal | Estado | Moneda | Claves de origen | Registros | Cantidad registrada | Importe original | Cobertura registros del canal % |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Físico | ERP exacto en catálogo | MXN | 60 | 74141 | 114284 | 26,989,097.6200 | 85.7220 |
| Físico | Equivalencia con ERP nulo | MXN | 5 | 6132 | 9552 | 2,524,147.6800 | 7.0898 |
| Físico | Sin equivalencia | MXN | 5 | 6217 | 9547 | 1,434,008.5200 | 7.1881 |
| Online | ERP exacto en catálogo | EUR | 23 | 335 | 444 | 7,667.7300 | 3.3678 |
| Online | ERP exacto en catálogo | MXN | 23 | 4875 | 6463 | 2,200,251.6500 | 49.0098 |
| Online | ERP exacto en catálogo | USD | 23 | 1749 | 2382 | 46,201.2800 | 17.5832 |
| Online | Equivalencia con ERP nulo | EUR | 4 | 46 | 54 | 915.4500 | 0.4625 |
| Online | Equivalencia con ERP nulo | MXN | 4 | 799 | 1052 | 318,970.0400 | 8.0326 |
| Online | Equivalencia con ERP nulo | USD | 4 | 294 | 403 | 7,053.6400 | 2.9557 |
| Online | Sin equivalencia | EUR | 6 | 89 | 115 | 1,302.6800 | 0.8947 |
| Online | Sin equivalencia | MXN | 6 | 1268 | 1716 | 393,209.0500 | 12.7476 |
| Online | Sin equivalencia | USD | 6 | 492 | 663 | 8,541.5400 | 4.9462 |

**Puentes de producto y tienda**

**Leyenda:** Intersecciones calculadas en toda la cobertura. La presencia global de un ERP en snapshots no demuestra saldo disponible para una tienda, fecha o pedido concreto. Muestro todas las filas; omito el índice de pandas.

| Medida | Resultado |
| --- | --- |
| ERP presentes en ambos canales con enlace exacto | 23 |
| ERP físicos enlazados sin presencia global en snapshots | 0 |
| ERP online enlazados sin presencia global en snapshots | 0 |
| Registros POS sin tienda en catálogo | 0 |
| Tiendas de snapshots fuera del catálogo | 0 |

**Interpretación e importancia.** Puedo usar inventory como puente parcial de identidad entre los canales y como dimensión de tienda del POS. Las cantidades e importes de filas sin enlace permanecen visibles: perderlas con un inner join sesgaría margen y rotación. Compartir un producto no identifica una transacción común. No vinculo pedidos a tienda desde dirección de envío ni uso IDs distintos como prueba de ausencia de doble conteo.

## 4. Compatibilidad temporal para los cruces

Calculo ventanas por intersección de extremos y presencia de días en las fuentes participantes. Es cobertura global diaria, no cobertura de cada producto, tienda o moneda. Una ventana común no prueba que los extractos estén completos. El corte propuesto depende de los datos y no de la fecha de ejecución; mantengo la hora original y no afirmo que el día POS equivalga al día contable de Shopify.

**Ventanas utilizables de conexión**

**Leyenda:** Días calendario con alguna fila por fuente; la cobertura por divisa y por tienda–SKU se valida más adelante. No relleno fechas ausentes. Muestro todas las filas; omito el índice de pandas.

| Cruce | Inicio común | Fin común | Días entre extremos | Días presentes en todas |
| --- | --- | --- | --- | --- |
| POS con snapshots | 2025-10-01 | 2026-03-31 | 182 | 182 |
| Online con tasas | 2025-04-01 | 2026-03-31 | 365 | 365 |
| Cuatro fuentes | 2025-10-01 | 2026-03-31 | 182 | 182 |

**Calendario comparado para las ventanas del reto**

**Leyenda:** Días con alguna fila por fuente en cada mes observado; cero significa ausencia de registros en esa fuente, no ventas ni stock cero. Este cuadro compara cobertura, no repite importes mensuales individuales. Muestro todas las filas; omito el índice de pandas.

| Mes | Días POS | Días online | Días snapshots | Días FX |
| --- | --- | --- | --- | --- |
| 2024-10 | 31 | 0 | 0 | 0 |
| 2024-11 | 30 | 0 | 0 | 0 |
| 2024-12 | 31 | 0 | 0 | 0 |
| 2025-01 | 31 | 0 | 0 | 0 |
| 2025-02 | 28 | 0 | 0 | 0 |
| 2025-03 | 31 | 0 | 0 | 0 |
| 2025-04 | 30 | 30 | 0 | 30 |
| 2025-05 | 31 | 31 | 0 | 31 |
| 2025-06 | 30 | 30 | 0 | 30 |
| 2025-07 | 31 | 31 | 0 | 31 |
| 2025-08 | 31 | 31 | 0 | 31 |
| 2025-09 | 30 | 30 | 0 | 30 |
| 2025-10 | 31 | 31 | 31 | 31 |
| 2025-11 | 30 | 30 | 30 | 30 |
| 2025-12 | 31 | 31 | 31 | 31 |
| 2026-01 | 31 | 31 | 31 | 31 |
| 2026-02 | 28 | 28 | 28 | 28 |
| 2026-03 | 31 | 31 | 31 | 31 |

**Interpretación e importancia.** Puedo comparar actividad por canal dentro del año común POS–online, pero el primer mes online no tiene una base online del mes anterior. Para rotación restrinjo las ventas al período con inventario y después compruebo tienda–SKU–día; la intersección temporal por sí sola no basta. FX es necesario para moneda extranjera: su ausencia antes del período online no impide conservar POS en MXN.

## 5. Ventas físicas frente a snapshots: cobertura utilizable

`stock_num`, desde cantidad_en_stock, convierte textos no interpretables a NaN sin convertirlos a cero. Uno por **dia, tienda_id y sku_erp**, con validación m:1; unir solo por producto multiplicaría filas y mezclaría tiendas y fechas. `estado_stock` prioriza falta de ERP, fecha fuera del período de snapshots, ausencia de fila y después saldo desconocido, cero, positivo u otro valor numérico. Un snapshot ausente no es un nulo de saldo ni una existencia cero.

Conservo todos los comprobantes en el diagnóstico global y separo I en el semestre como escenario de elegibilidad, sin confirmar que sea la definición final de ventas. Los porcentajes usan el total de cada población, incluidos los registros sin mapeo. No sumo saldos diarios como inventario disponible ni igualo ventas con variaciones de stock: faltan compras, traslados y ajustes.

**Efecto de la conexión al inventario**

**Leyenda:** Estados excluyentes por movimiento; importes MXN sin signo analítico aplicado y cantidades originales. Solo I es un escenario, no ingreso neto confirmado. Muestro todas las filas; omito el índice de pandas.

| Población | Estado de conexión | Registros | Cantidad registrada | Importe original MXN | Registros de la población % |
| --- | --- | --- | --- | --- | --- |
| Todos los comprobantes; toda la cobertura | Fuera de ventana de snapshots | 49585 | 76258 | 18,012,284.6300 | 57.3303 |
| Todos los comprobantes; toda la cobertura | Saldo cero | 593 | 914 | 222,341.2200 | 0.6856 |
| Todos los comprobantes; toda la cobertura | Saldo desconocido | 217 | 327 | 72,619.1100 | 0.2509 |
| Todos los comprobantes; toda la cobertura | Saldo positivo | 10473 | 16240 | 3,810,220.2400 | 12.1089 |
| Todos los comprobantes; toda la cobertura | Sin ERP conciliado | 12349 | 19099 | 3,958,156.2000 | 14.2780 |
| Todos los comprobantes; toda la cobertura | Sin fila de snapshot | 13273 | 20545 | 4,871,632.4200 | 15.3463 |
| Solo I; ventana de snapshots | Saldo cero | 565 | 866 | 210,818.6600 | 2.0705 |
| Solo I; ventana de snapshots | Saldo desconocido | 213 | 317 | 70,228.2700 | 0.7806 |
| Solo I; ventana de snapshots | Saldo positivo | 9950 | 15437 | 3,599,073.9100 | 36.4629 |
| Solo I; ventana de snapshots | Sin ERP conciliado | 3873 | 5988 | 1,245,482.0000 | 14.1931 |
| Solo I; ventana de snapshots | Sin fila de snapshot | 12687 | 19640 | 4,653,186.3700 | 46.4930 |

**Cobertura de conexión por mes en el escenario I**

**Leyenda:** Conteos de registros I durante la ventana de snapshots, por estado. Cero en una celda significa que ningún movimiento cae en ese estado; no imputa stock. Muestro todas las filas; omito el índice de pandas.

| Mes | Saldo cero | Saldo desconocido | Saldo positivo | Sin ERP conciliado | Sin fila de snapshot |
| --- | --- | --- | --- | --- | --- |
| 2025-10 | 86 | 42 | 1729 | 642 | 2187 |
| 2025-11 | 97 | 34 | 1658 | 627 | 2092 |
| 2025-12 | 97 | 30 | 1709 | 703 | 2139 |
| 2026-01 | 103 | 45 | 1667 | 644 | 2170 |
| 2026-02 | 92 | 27 | 1509 | 617 | 1971 |
| 2026-03 | 90 | 35 | 1678 | 640 | 2128 |

**Interpretación e importancia.** La identidad ERP puede ser correcta y aun así faltar el par tienda–producto en inventario. Por ello, para rotación necesito una población compatible en numerador y denominador y cobertura de saldos conocidos; no extrapolo el subconjunto conciliado a todo el canal. Ventas con saldo cero el mismo día son una coincidencia temporal observada: sin hora ni definición del snapshot no prueban sobreventa ni quiebre continuo.

## 6. Costo vigente: conexión temporal al catálogo

Expando cost_history en `vigencia` (fecha_vigencia interpretada) y `costo_num` (costo_mxn numérico); detengo el análisis si encuentro fechas desconocidas, claves repetidas o costos no positivos. Con `merge_asof` busco por ERP la última vigencia menor o igual al día del registro, aceptando coincidencia en el mismo día. `dias_desde_vigencia` es día del movimiento menos vigencia; mide antigüedad, no vencimiento. No uso un costo futuro ni el costo actual para todo el histórico.

`estado_costo` distingue sin ERP, sin vigencia previa y costo temporal encontrado. Supongo para este diagnóstico que la vigencia comienza ese día y el costo es global; no confirmo base fiscal, unidad o método contable. No calculo margen hasta que esas bases sean comparables.

**Clave temporal del historial usado en el cruce**

**Leyenda:** Cada ERP puede tener varias vigencias; la combinación ERP–vigencia debe ser única, con fecha conocida y costo finito positivo. La selección temporal devuelve a lo sumo una vigencia por movimiento. Muestro todas las filas; omito el índice de pandas.

| Conector | Clave derecha | Filas derechas | Claves nulas | Repeticiones adicionales |
| --- | --- | --- | --- | --- |
| Movimiento a historial de costo | sku_erp, vigencia | 282 | 0 | 0 |

**Cobertura de costo aplicable por fecha**

**Leyenda:** Toda la ventana y comprobantes; cuento registros, no márgenes. Costos en MXN por unidad ERP pendiente de confirmar; los extremos son días calendario y quedan ausentes si no hay enlace. Muestro todas las filas; omito el índice de pandas.

| Canal | Moneda original | Estado de costo | Registros | ERP distintos | Días mínimos desde vigencia | Días máximos desde vigencia |
| --- | --- | --- | --- | --- | --- | --- |
| Físico | MXN | Costo temporal encontrado | 74141 | 60 | 0.0000 | 497.0000 |
| Físico | MXN | Sin ERP conciliado | 12349 | 0 | No disponible | No disponible |
| Online | EUR | Costo temporal encontrado | 335 | 23 | 1.0000 | 422.0000 |
| Online | MXN | Costo temporal encontrado | 4875 | 23 | 0.0000 | 429.0000 |
| Online | USD | Costo temporal encontrado | 1749 | 23 | 0.0000 | 422.0000 |
| Online | EUR | Sin ERP conciliado | 135 | 0 | No disponible | No disponible |
| Online | MXN | Sin ERP conciliado | 2067 | 0 | No disponible | No disponible |
| Online | USD | Sin ERP conciliado | 786 | 0 | No disponible | No disponible |

**Interpretación e importancia.** La cobertura temporal del costo debe evaluarse después del enlace de producto. Una fila sin ERP no es un costo cero ni un producto sin costo en catálogo. El resultado habilita una comparación condicionada, pero no certifica márgenes: cantidad del canal, unidad ERP, impuestos, descuentos y signos requieren bases comparables.

## 7. Monedas: conector diario e independencia del mapeo

Uno online a tasas por dia y currency con m:1; `tasa_aplicada` toma rate_to_mxn para divisas y 1 para MXN como identidad matemática, sin exigir una fila MXN en FX. `estado_fx` distingue identidad MXN, tasa diaria positiva y ausencia o invalidez. Para POS en MXN no necesito cotización extranjera.

Calculo solo un **importe convertido diagnóstico**, amount × tasa, con Decimal construido desde la representación textual; no recupera una precisión original perdida en double. Comparo redondear cada registro a dos decimales frente a redondear su suma, usando ROUND_HALF_UP como escenario técnico. No establezco una política contable ni presento el convertido como ingreso reconocido. Mantengo monedas originales separadas y no aplico relleno temporal de tasas.

**Conexión financiera y sensibilidad del redondeo**

**Leyenda:** Todo online, incluso productos no conciliados. Sumas en MXN bajo dos escenarios de redondeo a centavos; no son ingresos netos ni sustituyen importes originales. Muestro todas las filas; omito el índice de pandas.

| Moneda original | Estado FX | Registros | Registros convertibles | Suma MXN redondeada por registro | Suma MXN redondeada al final | Diferencia MXN |
| --- | --- | --- | --- | --- | --- | --- |
| EUR | Tasa diaria positiva | 470 | 470 | 214922.15 | 214922.16 | -0.01 |
| MXN | Identidad MXN | 6942 | 6942 | 2912430.74 | 2912430.74 | 0.00 |
| USD | Tasa diaria positiva | 2535 | 2535 | 1101529.65 | 1101529.81 | -0.16 |

**Cobertura conjunta online: producto, costo y moneda**

**Leyenda:** Conteo de registros en todas las combinaciones observadas. Una tasa disponible no repara un ERP faltante; un costo encontrado no identifica almacén ni valida unidad. Muestro todas las filas; omito el índice de pandas.

| Producto | Costo | Conversión | Moneda original | Registros |
| --- | --- | --- | --- | --- |
| ERP exacto en catálogo | Costo temporal encontrado | Identidad MXN | MXN | 4875 |
| ERP exacto en catálogo | Costo temporal encontrado | Tasa diaria positiva | EUR | 335 |
| ERP exacto en catálogo | Costo temporal encontrado | Tasa diaria positiva | USD | 1749 |
| Equivalencia con ERP nulo | Sin ERP conciliado | Identidad MXN | MXN | 799 |
| Equivalencia con ERP nulo | Sin ERP conciliado | Tasa diaria positiva | EUR | 46 |
| Equivalencia con ERP nulo | Sin ERP conciliado | Tasa diaria positiva | USD | 294 |
| Sin equivalencia | Sin ERP conciliado | Identidad MXN | MXN | 1268 |
| Sin equivalencia | Sin ERP conciliado | Tasa diaria positiva | EUR | 89 |
| Sin equivalencia | Sin ERP conciliado | Tasa diaria positiva | USD | 492 |

**Interpretación e importancia.** El conector FX y el conector de producto resuelven problemas independientes: puedo convertir un registro extranjero aunque no llegue a ERP, pero no asignarle costo o inventario automáticamente. La diferencia entre escenarios de redondeo justifica declarar cuándo se redondea antes de conciliar totales. No sumo canales como ingreso consolidado mientras no pueda controlar estatus y doble conteo.

## 8. Conservación y comprobaciones de los cruces

Compruebo que los left joins conserven cada registro, cantidades y sumas en su moneda; las sumas son controles técnicos, no cierres contables. Verifico de nuevo las huellas y que las columnas originales permanezcan iguales. La tolerancia 1e-8 solo absorbe diferencias de coma flotante al agregar. La asignación temporal no debe tener vigencias futuras y ningún enlace técnico puede multiplicar filas.

**Controles finales de integración**

**Leyenda:** Validaciones ejecutables de este notebook. Ante una falla detengo la ejecución; no reparo fuentes ni oculto movimientos sin correspondencia. Muestro todas las filas; omito el índice de pandas.

| Control | Resultado |
| --- | --- |
| Físico: registros, originales y sumas conservados | Cumple |
| Físico: última vigencia no futura contrastada con búsqueda ordenada | Cumple |
| Online: registros, originales y sumas conservados | Cumple |
| Online: última vigencia no futura contrastada con búsqueda ordenada | Cumple |
| Cuatro SHA-256 finales iguales a los iniciales | Cumple |

## 9. Qué conexiones puedo usar

Puedo usar el SKU POS y el handle como entradas separadas a las equivalencias explícitas del ERP, tienda_id para enriquecer el POS y la clave compuesta día–tienda–ERP para consultar snapshots. Puedo conectar ERP con su última vigencia de costo no futura y día–moneda con la tasa diaria extranjera. La cobertura es parcial y queda cuantificada en las tablas; aplico uniones que conservan los movimientos no conciliados.

Para crecimiento por canal dispongo de un calendario común, condicionado por estados comerciales, signos y moneda. Para rotación necesito restringir las ventas y los saldos a la misma población y ventana; no incorporo online al inventario de tiendas sin almacén de cumplimiento. Para quiebres, las ventas coincidentes con cero no demuestran falta continua de disponibilidad. Para margen, el enlace de costo no confirma que cantidad, impuestos y base financiera sean comparables.

Mi análisis no establece una relación transaccional POS–online: no hay una referencia común que permita comprobar duplicación entre canales. No uso nombre, sufijo, cercanía horaria ni dirección de envío para inventarla. Mantengo esas limitaciones al construir el modelo.

## Documentación relacionada

- [Notebook del análisis conjunto](../../notebooks/05_conjunto.ipynb).
- [Preguntas al cliente](../03_negocio/PREGUNTAS_CLIENTE.md#evidencia-del-eda-conjunto).

## Conclusión

Tengo comprobados los conectores técnicos y su cobertura entre las cuatro fuentes actuales, con protección contra multiplicación de filas y pérdida silenciosa de movimientos. Puedo avanzar al modelo con equivalencias exactas y excepciones visibles, conservando como límites la identidad incompleta, la cobertura tienda–producto, las unidades y la interpretación financiera y temporal.
