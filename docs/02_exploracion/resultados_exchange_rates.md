# Resultados del análisis exploratorio aislado de exchange_rates.csv

Fecha de documentación y verificación: 8 de noviembre de 2026.

## Alcance y fuente de evidencia

**Analizo únicamente `datos/exchange_rates.csv`, sin consultar ni cruzar el contenido de sales, inventory o ecommerce.** No contrasto cotizaciones externas. Mi análisis no demuestra cobertura de pedidos ni consistencia entre sistemas.

Código de referencia: [02_exchange_rates.ipynb](../../notebooks/02_exchange_rates.ipynb). Las tablas proceden de sus cálculos ejecutados. La IA realizó las comprobaciones técnicas; mi revisión de conclusiones permanece pendiente.

| Identificación | Resultado |
|---|---|
| Archivo | `datos/exchange_rates.csv` |
| Tamaño | 16,562 bytes |
| SHA-256 | `a0e827ec1e048cf397584eca3d692cb5b5b1f6b477fb78efca2fdbd2f488bddf` |
| Registros / columnas originales | 730 / 3 |
| Fecha mínima / máxima | 2025-04-01 / 2026-03-31 |
| Formato de fecha | `YYYY-MM-DD` |
| Fuente modificada durante el análisis | No |

**Por qué importa:** identifico la versión que respalda las cifras, sin confundir una huella estable con exactitud comercial.

## 1. Estructura y granularidad observada

| Columna | tipo_leído | nulos |
|---|---|---|
| fecha | object | 0 |
| currency | object | 0 |
| rate_to_mxn | object | 0 |

Observo una fila por fecha–moneda, sin claves repetidas, conflictos de tasa ni duplicados exactos adicionales. Hay 2 monedas: EUR, USD, con 365 registros cada una. No hay filas MXN.

| Campo | Mi interpretación y límite |
|---|---|
| fecha | Fecha registrada sin hora, zona, fecha de publicación o vigencia explícita. |
| currency | Código observado de tres mayúsculas; no valido un catálogo externo. |
| rate_to_mxn | MXN por una unidad de la moneda indicada en currency; definición confirmada para mi análisis. Convierto a MXN multiplicando el importe extranjero por esta tasa. |

**Qué me dice:** la clave candidata fecha–moneda es única en esta extracción. **Por qué importa:** permitiría buscar una tasa diaria sin multiplicar filas si se conserva esa unicidad. No confirma la política contable ni la vigencia de la cotización.

## 2. Calidad estructural y numérica

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

| currency | registros | fechas_distintas | inicio | fin | días_esperados | días_sin_registro |
|---|---|---|---|---|---|---|
| EUR | 365 | 365 | 2025-04-01 00:00:00 | 2026-03-31 00:00:00 | 365 | 0 |
| USD | 365 | 365 | 2025-04-01 00:00:00 | 2026-03-31 00:00:00 | 365 | 0 |

Entre los extremos hay 365 días calendario y 730 combinaciones fecha–moneda esperadas; faltan 0. Observo 208 filas en fines de semana. La ventana contiene 12 meses completos.

**Qué me dice:** tengo continuidad diaria interna para las dos monedas. **Por qué importa:** no necesito rellenar huecos dentro de esta ventana para esta fuente. No afirmo cobertura antes o después, ni cobertura de transacciones; tampoco sé si las tasas de fin de semana son nuevas, arrastradas o construidas.

## 4. Distribución y precisión de las tasas

| currency | count | mean | std | min | 1% | 25% | 50% | 75% | 99% | max |
|---|---|---|---|---|---|---|---|---|---|---|
| EUR | 365.000000 | 21.751705 | 0.275546 | 20.377000 | 20.615112 | 21.640000 | 21.829000 | 21.957500 | 22.000000 | 22.000000 |
| USD | 365.000000 | 17.823456 | 0.360634 | 17.129500 | 17.288056 | 17.558500 | 17.748700 | 17.962500 | 18.796816 | 18.825300 |

Describo cada moneda por separado y no sumo tasas de monedas distintas. La precisión textual observada es:

| currency | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| EUR | 63 | 3 | 23 | 276 |
| USD | 0 | 4 | 29 | 332 |

**Qué me dice:** USD varía entre 17.1295 y 18.8253; EUR entre 20.3770 y 22.0000. Los valores se escriben con distintas cantidades de decimales.

**Por qué importa:** necesito conservar precisión y fijar una regla de redondeo antes de convertir importes. Menos decimales escritos pueden reflejar omisión de ceros finales; no prueban menor exactitud. La media es descriptiva y no equivale a una tasa ponderada por operaciones.

## 5. Evolución mensual y cambios diarios

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

| currency | cambios_evaluados | cambios_cero | mayor_subida_pct | mayor_bajada_pct |
|---|---|---|---|---|
| EUR | 364 | 33 | 1.847083 | -1.338055 |
| USD | 364 | 0 | 1.240146 | -1.357118 |

Calculo cambios entre fechas consecutivas de la misma moneda; el primer registro de cada serie queda sin variación. En cada moneda evalúo 364 cambios.

**Qué me dice:** las tasas muestran variación temporal y días sin cambio. **Por qué importa:** una tasa agregada podría ocultar diferencias diarias. Un cambio cero no es una tasa cero ni demuestra un fallo de actualización; no atribuyo tendencias a causas económicas con esta fuente aislada.

## 6. Repeticiones y señales exploratorias

| currency | máximo | días_en_máximo | tasas_distintas | porcentaje_en_máximo | racha_máxima_días |
|---|---|---|---|---|---|
| EUR | 22.000000 | 63 | 294 | 17.260274 | 6 |
| USD | 18.825300 | 1 | 355 | 0.273973 | 1 |

EUR aparece exactamente en 22.0 en 63 fechas (17.26% de su serie), entre 2025-05-20 y 2026-03-29. Su mayor racha en ese máximo es de 6 días consecutivos. El notebook muestra los intervalos más largos.

| currency | q1 | q3 | iqr | límite_inferior | límite_superior |
|---|---|---|---|---|---|
| EUR | 21.640000 | 21.957500 | 0.317500 | 21.163750 | 22.433750 |
| USD | 17.558500 | 17.962500 | 0.404000 | 16.952500 | 18.568500 |

| currency | evaluadas | señaladas |
|---|---|---|
| EUR | 365 | 11 |
| USD | 365 | 32 |

**Qué me dice:** el máximo de EUR tiene una concentración que requiere explicación. Las cercas de 1.5×IQR señalan niveles extremos respecto de la distribución de cada moneda, no errores confirmados.

**Por qué importa:** podría existir una metodología, redondeo o límite de generación; son hipótesis. No corrijo, recorto ni elimino tasas. En series temporales, un cambio de nivel también puede activar IQR; no uso este criterio para certificar mercado.

## 7. Dudas conectadas con las preguntas al cliente

| Evidencia aislada | Duda y conexión | Mi tratamiento provisional |
|---|---|---|
| Nombre rate_to_mxn; sin proveedor, hora ni tipo de cotización. | D013 / Q10: procedencia y tipo de cotización; la unidad MXN por unidad extranjera está confirmada para mi análisis. | No adopto una conversión contable definitiva. |
| Hay tasas durante todos los fines de semana de la ventana. | D013 / Q38: publicación, arrastre y vigencia. | No interpreto continuidad de filas como actualización efectiva. |
| EUR repite 22.0 en el máximo observado. | D013 / Q39: metodología o límite. | Conservo tasas y no declaro error de mercado. |
| Precisión textual variable; sin política de redondeo. | D023 / Q40: precisión de cálculo, redondeo y tolerancia. | Mantengo precisión original; no convierto importes. |
| No hay filas MXN. | D013 / Q10: definir el tratamiento operativo de importes ya expresados en MXN. | Identidad MXN = 1 es una propuesta futura, no una fila ausente que deba imputar. |

Conecto el detalle con [la evidencia del banco de preguntas](../03_negocio/PREGUNTAS_CLIENTE.md#evidencia-del-eda-aislado-de-exchange-rates) y [DUDAS.md](../03_negocio/DUDAS.md). Reutilizo Q10 y Q38–Q40, sin duplicar consultas ni darlas por enviadas o respondidas. No resuelvo Q37 con esta exploración porque requiere información de operaciones y liquidaciones ajena al archivo.

## Conclusión

Tengo una fuente internamente consistente y continua para USD y EUR en su ventana observada, con granularidad diaria única y tasas positivas. Mantengo abiertas la procedencia, vigencia, redondeo y concentración de EUR en 22.0; puedo preparar su integración sin presentar todavía conversiones de ventas ni conclusiones de mercado como resultados confirmados.
