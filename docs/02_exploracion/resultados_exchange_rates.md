# Resultados del análisis exploratorio aislado de exchange_rates.csv

Fecha de documentación y verificación: 8 de noviembre de 2026.

## Alcance y fuente de evidencia

**Analizo únicamente `datos/exchange_rates.csv`, sin consultar ni cruzar el contenido de sales, inventory o ecommerce.** No contrasto cotizaciones externas. Mi análisis no demuestra cobertura de pedidos ni consistencia entre sistemas.

Código de referencia: [02_exchange_rates.ipynb](../../notebooks/02_exchange_rates.ipynb). Las tablas proceden de sus cálculos ejecutados. La IA realizó las comprobaciones técnicas; mi revisión de conclusiones permanece pendiente.

**Tabla. Versión de la fuente. Identifico los bytes y el período que respaldan los resultados; la huella no demuestra exactitud comercial.**

| Identificación | Resultado |
|---|---|
| Archivo | `datos/exchange_rates.csv` |
| Tamaño | 16,562 bytes |
| SHA-256 | `a0e827ec1e048cf397584eca3d692cb5b5b1f6b477fb78efca2fdbd2f488bddf` |
| Registros | 730 |
| Columnas originales | 3 |
| Fecha mínima | 2025-04-01 |
| Fecha máxima | 2026-03-31 |
| Formato de fecha | `YYYY-MM-DD` |
| Fuente modificada durante el análisis | No |

**Por qué importa:** identifico la versión que respalda las cifras, sin confundir una huella estable con exactitud comercial.

## 1. Estructura y granularidad observada

**Tabla. Esquema original. Leo tipo técnico y nulos por columna; no es un diccionario de negocio.**

| Columna | tipo_leído | nulos |
|---|---|---|
| fecha | object | 0 |
| currency | object | 0 |
| rate_to_mxn | object | 0 |

Observo una fila por fecha–moneda, sin claves repetidas, conflictos de tasa ni duplicados exactos adicionales. Hay 2 monedas: EUR, USD, con 365 registros cada una. No hay filas MXN.

**Tabla. Diccionario de campos. Distingo su significado de los límites de lo que el archivo demuestra.**

| Campo | Mi interpretación y límite |
|---|---|
| fecha | Fecha registrada sin hora, zona, fecha de publicación o vigencia explícita. |
| currency | Código observado de tres mayúsculas; no valido un catálogo externo. |
| rate_to_mxn | MXN por una unidad de la moneda indicada en currency; definición confirmada para mi análisis. Convierto a MXN multiplicando el importe extranjero por esta tasa. |

**Qué me dice:** la clave candidata fecha–moneda es única en esta extracción. **Por qué importa:** permitiría buscar una tasa diaria sin multiplicar filas si se conserva esa unicidad. No confirma la política contable ni la vigencia de la cotización.

## 2. Calidad estructural y numérica

**Tabla. Calidad estructural y numérica. Cuento campos o filas afectados según el control; cero significa ninguna incidencia detectada por ese criterio.**

| Control | resultado |
|---|---|
| nulos_originales | 0 |
| campos_vacíos_o_espacios | 0 |
| campos_con_espacios_extremos | 0 |
| fecha_fuera_de_formato_ISO | 0 |
| fecha_no_interpretable | 0 |
| moneda_fuera_de_tres_mayúsculas | 0 |
| tasa_no_interpretable | 0 |
| tasa_infinita | 0 |
| tasa_cero | 0 |
| tasa_negativa | 0 |

**Qué me dice:** las fechas se interpretan, las tasas son finitas y positivas y no detecto vacíos ni espacios extremos. Conservo las columnas originales como texto y las conversiones como derivadas.

**Por qué importa:** separo cero, ausencia de fila y dato no interpretable; no es necesario imputar para describir esta extracción. Los controles no certifican proveedor, autenticidad ni exactitud frente al mercado.

## 3. Cobertura temporal

**Tabla. Cobertura diaria. Registros son filas y fechas_distintas son días; comparo el calendario esperado con los días observados por moneda.**

| currency | registros | fechas_distintas | inicio | fin | días_esperados | días_sin_registro |
|---|---|---|---|---|---|---|
| EUR | 365 | 365 | 2025-04-01 00:00:00 | 2026-03-31 00:00:00 | 365 | 0 |
| USD | 365 | 365 | 2025-04-01 00:00:00 | 2026-03-31 00:00:00 | 365 | 0 |

Entre los extremos hay 365 días calendario y 730 combinaciones fecha–moneda esperadas; faltan 0. Observo 208 filas en fines de semana. La ventana contiene 12 meses completos.

**Qué me dice:** tengo continuidad diaria interna para las dos monedas. **Por qué importa:** no necesito rellenar huecos dentro de esta ventana para esta fuente. No afirmo cobertura antes o después, ni cobertura de transacciones; tampoco sé si las tasas de fin de semana son nuevas, arrastradas o construidas.

### Lectura del calendario y de los fines de semana

Leo `inicio` y `fin` como extremos inclusivos: 365 días × 2 monedas = 730 claves esperadas, con 0 ausentes. Los 208 registros de fin de semana corresponden a 104 fechas distintas con una fila de cada moneda. No confundo filas con días ni continuidad con cotización nueva; Q38 sigue abierta.

En el resumen mensual, comparo registros con los días calendario del mes: abril tiene 30, mayo 31 y febrero de 2026 tiene 28. La media mensual es simple sobre las tasas registradas; no está ponderada por ventas. Mi comprobación se limita a la ventana del archivo, sin afirmar cobertura de transacciones.

## 4. Distribución y precisión de las tasas

**Tabla. Distribución por moneda. count cuenta tasas; mean es media, std desviación muestral y los porcentajes son percentiles; las tasas y la dispersión están en MXN por unidad extranjera.**

| currency | count | mean | std | min | 1% | 25% | 50% | 75% | 99% | max |
|---|---|---|---|---|---|---|---|---|---|---|
| EUR | 365.000000 | 21.751705 | 0.275546 | 20.377000 | 20.615112 | 21.640000 | 21.829000 | 21.957500 | 22.000000 | 22.000000 |
| USD | 365.000000 | 17.823456 | 0.360634 | 17.129500 | 17.288056 | 17.558500 | 17.748700 | 17.962500 | 18.796816 | 18.825300 |

Describo cada moneda por separado y no sumo tasas de monedas distintas. La precisión textual observada es:

**Tabla. Decimales escritos. Los encabezados 1–4 indican cifras tras el punto en el texto original; las celdas cuentan registros, no tasas de cambio.**

| currency | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| EUR | 63 | 3 | 23 | 276 |
| USD | 0 | 4 | 29 | 332 |

**Qué me dice:** USD varía entre 17.1295 y 18.8253; EUR entre 20.3770 y 22.0000. Los valores se escriben con distintas cantidades de decimales.

**Por qué importa:** necesito conservar precisión y fijar una regla de redondeo antes de convertir importes. Menos decimales escritos pueden reflejar omisión de ceros finales; no prueban menor exactitud. La media es descriptiva y no equivale a una tasa ponderada por operaciones.

### Lectura de decimales y fechas de los extremos

Por ejemplo, `22.0` tiene un decimal, `20.377` tres y `17.1295` cuatro. Cada fila de la tabla de decimales suma 365 registros de su moneda: EUR tiene 63 escritos con un decimal y USD tiene 0. `22.0` y `22.0000` representan el mismo valor: no deduzco exactitud económica ni redondeo de los ceros finales (Q40).

**Tabla. Tasas mínimas por moneda. Muestro la primera fila que alcanza el mínimo en el orden de lectura, con fecha y tasa original en MXN por unidad extranjera.**

| índice_original | fecha | currency | rate_to_mxn |
|---|---|---|---|
| 1 | 2025-04-01 | EUR | 20.377 |
| 102 | 2025-05-22 | USD | 17.1295 |

**Tabla. Tasas máximas por moneda. Muestro la primera fila que alcanza el máximo; no es el listado de todas sus fechas empatadas.**

| índice_original | fecha | currency | rate_to_mxn |
|---|---|---|---|
| 99 | 2025-05-20 | EUR | 22.0 |
| 660 | 2026-02-25 | USD | 18.8253 |

`idxmin()` e `idxmax()` seleccionan la primera fila empatada en el orden del archivo; solo coincide con la primera fecha si ese orden es cronológico. EUR alcanza 22.0 en 63 fechas, aunque aquí muestro una. Los índices originales de la izquierda son posiciones de pandas, no claves del negocio ni valores de tasa.

## 5. Evolución mensual y cambios diarios

**Tabla. Resumen mensual. Mínima, media simple y máxima diaria en MXN por unidad extranjera; registros cuenta filas por mes y moneda.**

| mes | currency | registros | mínima | media | máxima |
|---|---|---|---|---|---|
| 2025-04 | EUR | 30 | 20.3770 | 21.3139 | 21.9307 |
| 2025-04 | USD | 30 | 17.4587 | 17.6033 | 17.8280 |
| 2025-05 | EUR | 31 | 21.4006 | 21.7552 | 22.0000 |
| 2025-05 | USD | 31 | 17.1295 | 17.4591 | 17.7589 |
| 2025-06 | EUR | 30 | 21.4229 | 21.7383 | 22.0000 |
| 2025-06 | USD | 30 | 17.3362 | 17.6249 | 17.9426 |
| 2025-07 | EUR | 31 | 21.6939 | 21.9164 | 22.0000 |
| 2025-07 | USD | 31 | 17.5230 | 17.8787 | 18.0528 |
| 2025-08 | EUR | 31 | 21.5472 | 21.8520 | 22.0000 |
| 2025-08 | USD | 31 | 17.8575 | 17.9563 | 18.1183 |
| 2025-09 | EUR | 30 | 21.5935 | 21.8600 | 22.0000 |
| 2025-09 | USD | 30 | 17.8177 | 17.9621 | 18.0386 |
| 2025-10 | EUR | 31 | 21.7020 | 21.9473 | 22.0000 |
| 2025-10 | USD | 31 | 17.3344 | 17.7519 | 17.9528 |
| 2025-11 | EUR | 30 | 21.5927 | 21.8301 | 22.0000 |
| 2025-11 | USD | 30 | 17.3795 | 17.5508 | 17.8352 |
| 2025-12 | EUR | 31 | 21.4529 | 21.8366 | 22.0000 |
| 2025-12 | USD | 31 | 17.3286 | 17.6254 | 17.8727 |
| 2026-01 | EUR | 31 | 21.2281 | 21.6098 | 21.9280 |
| 2026-01 | USD | 31 | 17.4890 | 17.5959 | 17.8256 |
| 2026-02 | EUR | 28 | 21.1247 | 21.4507 | 21.9017 |
| 2026-02 | USD | 28 | 17.7425 | 18.2727 | 18.8253 |
| 2026-03 | EUR | 31 | 21.4549 | 21.8725 | 22.0000 |
| 2026-03 | USD | 31 | 18.3814 | 18.6261 | 18.8036 |

**Tabla. Cambios diarios. Evaluados cuenta pares consecutivos; cero significa tasa igual. pct está en %, mxn en MXN por unidad extranjera; las bajadas conservan signo negativo.**

| currency | cambios_evaluados | cambios_cero | mayor_subida_pct | mayor_bajada_pct | mayor_subida_mxn | mayor_bajada_mxn |
|---|---|---|---|---|---|---|
| EUR | 364 | 33 | 1.847083 | -1.338055 | 0.380900 | -0.293200 |
| USD | 364 | 0 | 1.240146 | -1.357118 | 0.214900 | -0.242000 |

Calculo cambios entre fechas consecutivas de la misma moneda; el primer registro de cada serie queda sin variación calculada (desconocida), no en cero. En cada moneda evalúo 364 cambios.

**Qué me dice:** las tasas muestran variación temporal y días sin cambio. **Por qué importa:** una tasa agregada podría ocultar diferencias diarias. Un cambio cero no es una tasa cero ni demuestra un fallo de actualización; no atribuyo tendencias a causas económicas con esta fuente aislada.

### Lectura de diferencias, porcentajes y mayor movimiento

Calculo `cambio = tasa_actual − tasa_anterior` en MXN por unidad extranjera y `variación_pct = (tasa_actual / tasa_anterior − 1) × 100`. Mi ejemplo didáctico de 18.00 a 18.18 corresponde a +0.18 MXN por USD y +1%; no lo presento como registro del archivo. Ordeno por moneda y fecha y solo comparo días consecutivos de la misma moneda: el primer cambio y los saltos de calendario quedan desconocidos, sin sustituirlos por cero ni rellenar tasas.

Las 364 comparaciones EUR contienen 33 cambios cero; para USD son 0. Cero significa tasa igual al día anterior, no tasa cero ni ausencia demostrada de actualización. Estos recuentos difieren de las 63 fechas con EUR en 22.0. Las mayores subidas y bajadas en MXN por unidad pueden ocurrir en fechas distintas de los extremos porcentuales; no equivalen a ganancias o pérdidas sobre un importe convertido.

**Tabla. Mayor movimiento porcentual por moneda. Selecciono el máximo de `abs(variación_pct)` conservando el signo; la tasa mostrada es la de esa fecha, no la diferencia en pesos. En empates muestro la primera fila.**

| índice_original | fecha | currency | rate_to_mxn | variación_pct |
|---|---|---|---|---|
| 15 | 2025-04-08 | EUR | 21.0026 | 1.847083 |
| 168 | 2025-06-24 | USD | 17.5899 | -1.357118 |

Para EUR aparece una subida y para USD una bajada: selecciono magnitud y no solamente el mayor número positivo. Los índices originales solo localizan filas de pandas. La metodología de repetición sigue abierta en Q38/Q39.

## 6. Repeticiones y señales exploratorias

**Tabla. Concentración en el máximo. Días, porcentaje y racha en el máximo son recuentos distintos de comparaciones diarias sin cambio.**

| currency | máximo | días_en_máximo | tasas_distintas | porcentaje_en_máximo | racha_máxima_días |
|---|---|---|---|---|---|
| EUR | 22.000000 | 63 | 294 | 17.260274 | 6 |
| USD | 18.825300 | 1 | 355 | 0.273973 | 1 |

EUR aparece exactamente en 22.0 en 63 fechas (17.26% de su serie), entre 2025-05-20 y 2026-03-29. Su mayor racha en ese máximo es de 6 días consecutivos. El notebook muestra los intervalos más largos.

**Tabla. Franja IQR. q1=P25, q3=P75 e iqr=q3−q1; los límites son q1−1.5×iqr y q3+1.5×iqr, en MXN por unidad extranjera.**

| currency | q1 | q3 | iqr | límite_inferior | límite_superior |
|---|---|---|---|---|---|
| EUR | 21.640000 | 21.957500 | 0.317500 | 21.163750 | 22.433750 |
| USD | 17.558500 | 17.962500 | 0.404000 | 16.952500 | 18.568500 |

**Tabla. Señales IQR. evaluadas cuenta tasas y señaladas suma las que están estrictamente fuera de la franja; son señales descriptivas, no errores confirmados.**

| currency | evaluadas | señaladas |
|---|---|---|
| EUR | 365 | 11 |
| USD | 365 | 32 |

**Qué me dice:** el máximo de EUR tiene una concentración que requiere explicación. Las cercas de 1.5×IQR señalan niveles extremos respecto de la distribución de cada moneda, no errores confirmados.

**Por qué importa:** podría existir una metodología, redondeo o límite de generación; son hipótesis. No corrijo, recorto ni elimino tasas. En series temporales, un cambio de nivel también puede activar IQR; no uso este criterio para certificar mercado.

### Cómo interpreto las señales de IQR

El 50% central de las tasas queda entre q1 y q3. Las cercas de 1.5×IQR se calculan con todos los niveles del período por moneda; no son extremos observados, intervalos de confianza ni límites de mercado autorizados. Antes el notebook mostraba `size` y `sum`: ahora uso `evaluadas` y `señaladas`; sumar banderas verdaderas cuenta tasas fuera de la franja. Un valor exactamente igual al límite no queda señalado.

EUR en 20.377 queda por debajo de 21.16375; USD en 18.8253 supera 18.56850. Las 11 señales EUR y 32 USD se detallan abajo. No demuestran errores: una tendencia o cambio de nivel puede producirlas. No elimino ni corrijo filas. La concentración de EUR en el máximo y la señal IQR son criterios separados; Q39 investiga metodología, sin declarar anomalías de mercado.

**Tabla. Detalle de señales IQR. Listo las fechas, monedas y tasas originales fuera de la franja, en MXN por unidad extranjera; el índice original es de pandas.**

| índice_original | fecha | currency | rate_to_mxn |
|---|---|---|---|
| 1 | 2025-04-01 | EUR | 20.377 |
| 3 | 2025-04-02 | EUR | 20.4385 |
| 5 | 2025-04-03 | EUR | 20.6359 |
| 7 | 2025-04-04 | EUR | 20.6578 |
| 9 | 2025-04-05 | EUR | 20.6034 |
| 11 | 2025-04-06 | EUR | 20.5424 |
| 13 | 2025-04-07 | EUR | 20.6217 |
| 15 | 2025-04-08 | EUR | 21.0026 |
| 623 | 2026-02-06 | EUR | 21.1325 |
| 629 | 2026-02-09 | EUR | 21.1505 |
| 635 | 2026-02-12 | EUR | 21.1247 |
| 650 | 2026-02-20 | USD | 18.5721 |
| 652 | 2026-02-21 | USD | 18.5865 |
| 654 | 2026-02-22 | USD | 18.6054 |
| 656 | 2026-02-23 | USD | 18.6343 |
| 658 | 2026-02-24 | USD | 18.8185 |
| 660 | 2026-02-25 | USD | 18.8253 |
| 662 | 2026-02-26 | USD | 18.793 |
| 664 | 2026-02-27 | USD | 18.8071 |
| 666 | 2026-02-28 | USD | 18.7802 |
| 668 | 2026-03-01 | USD | 18.8036 |
| 670 | 2026-03-02 | USD | 18.7107 |
| 672 | 2026-03-03 | USD | 18.6809 |
| 674 | 2026-03-04 | USD | 18.6751 |
| 676 | 2026-03-05 | USD | 18.6385 |
| 680 | 2026-03-07 | USD | 18.6733 |
| 682 | 2026-03-08 | USD | 18.6661 |
| 684 | 2026-03-09 | USD | 18.6596 |
| 686 | 2026-03-10 | USD | 18.6098 |
| 688 | 2026-03-11 | USD | 18.709 |
| 690 | 2026-03-12 | USD | 18.7273 |
| 692 | 2026-03-13 | USD | 18.7302 |
| 694 | 2026-03-14 | USD | 18.7765 |
| 696 | 2026-03-15 | USD | 18.6679 |
| 698 | 2026-03-16 | USD | 18.6662 |
| 700 | 2026-03-17 | USD | 18.5985 |
| 702 | 2026-03-18 | USD | 18.6761 |
| 704 | 2026-03-19 | USD | 18.6161 |
| 706 | 2026-03-20 | USD | 18.6567 |
| 708 | 2026-03-21 | USD | 18.7422 |
| 710 | 2026-03-22 | USD | 18.6011 |
| 712 | 2026-03-23 | USD | 18.6117 |
| 726 | 2026-03-30 | USD | 18.5896 |

## 7. Dudas conectadas con las preguntas al cliente

**Tabla. Dudas y tratamiento provisional. Separo evidencia observada, pregunta vinculada y decisiones que todavía requieren definición.**

| Evidencia aislada | Duda y conexión | Mi tratamiento provisional |
|---|---|---|
| Nombre rate_to_mxn; sin proveedor, hora ni tipo de cotización. | D013 / Q10: procedencia y tipo de cotización; la unidad MXN por unidad extranjera está confirmada para mi análisis. | No adopto una conversión contable definitiva. |
| Hay tasas durante todos los fines de semana de la ventana. | D013 / Q38: publicación, arrastre y vigencia. | No interpreto continuidad de filas como actualización efectiva. |
| EUR repite 22.0 en el máximo observado. | D013 / Q39: metodología o límite. | Conservo tasas y no declaro error de mercado. |
| Precisión textual variable; sin política de redondeo. | D023 / Q40: precisión de cálculo, redondeo y tolerancia. | Mantengo precisión original; no convierto importes. |
| No hay filas MXN. | D013 / Q10: definir el tratamiento operativo de importes ya expresados en MXN. | Identidad MXN = 1 es una propuesta futura, no una fila ausente que deba imputar. |

Conecto el detalle con [la evidencia del banco de preguntas](../03_negocio/PREGUNTAS_CLIENTE.md#evidencia-del-eda-aislado-de-exchange-rates) y [DUDAS.md](../03_negocio/DUDAS.md). Reutilizo Q10 y Q38–Q40, sin duplicar consultas ni darlas por enviadas o respondidas. No resuelvo Q37 con esta exploración porque requiere información de operaciones y liquidaciones ajena al archivo.

### Aclaraciones resueltas y próximos pasos

Tengo aclarada la lectura de cobertura interna, decimales escritos, extremos con empates, índices de pandas, variaciones en porcentaje y MXN por unidad y señales IQR. La unidad MXN por unidad extranjera está confirmada para mi análisis; no la vuelvo a presentar como duda pendiente. Estas aclaraciones de interpretación no equivalen a respuestas del cliente.

Mantengo abiertos proveedor/tipo de cotización y tratamiento operativo de MXN (Q10), fecha contable, hora/zona, vigencia y fines de semana (Q38), metodología de EUR repetido en 22.0 (Q39) y precisión/redondeo/tolerancia (Q40). La identidad MXN=1 sigue siendo una propuesta operativa, sin inventar filas faltantes. Q37 requiere información de operaciones ajena al archivo.

Mi próximo paso es documentar supuestos provisionales y preparar controles de unicidad, cobertura y precisión para una integración posterior. Conservo todas las tasas, incluidas las señaladas por IQR, sin rellenar primeros cambios ni huecos. Una conciliación de transacciones o una comparación de mercado se haría por separado; no se ejecutó aquí ni se enviaron consultas.

## Conclusión

Tengo una fuente internamente consistente y continua para USD y EUR en su ventana observada, con granularidad diaria única y tasas positivas. Mantengo abiertas la procedencia, vigencia, redondeo y concentración de EUR en 22.0; puedo preparar su integración sin presentar todavía conversiones de ventas ni conclusiones de mercado como resultados confirmados.
