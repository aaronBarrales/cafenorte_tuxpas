# Respuestas calculadas de CaféNorte

Mi corte es 2026-03-31; analizo conjuntamente las cuatro fuentes identificadas en el manifiesto. Aplico las interpretaciones del README; no certifico ingresos contables ni unidades equivalentes.

Para rotación uso unidades I y pares tienda–SKU con cobertura diaria completa. Para quiebres cuento ceros consecutivos observados, sin completar ausencias. MoM usa I menos E y órdenes online sin estatus. Margen compara importe con costo vigente y es anterior a gastos e impuestos no identificados.

## Lectura ejecutiva

Mi ranking se limita a 36 de 1268 pares tienda–SKU observados; no extrapolo a la cadena. Encuentro 3 episodios y 3 tiendas con más de tres ceros diarios consecutivos. El año contiene 24 filas canal–mes. Identifico 80 grupos canal–tienda–SKU con margen acumulado negativo; las operaciones sin costo permanecen fuera del cálculo, visibles en cobertura.

## 1. Top 10 por rotación — octubre a marzo

Leyenda: Unidades I e inventario promedio en unidades de catálogo; rotación en veces del semestre, solo pares con 182 días conocidos. Tiendas cuenta sucursales incluidas por SKU. Orden descendente y desempate por SKU. Muestro todas las filas sin índice. No disponible indica dato o base ausente.

| sku_erp | inventario_promedio | tiendas | unidades_I | rotacion_veces | nombre |
| --- | --- | --- | --- | --- | --- |
| ERP-PROV-MX-027-B | 39.9615 | 1 | 29 | 0.7257 | Latte Bebidas |
| ERP-PROV-MX-005-C | 83.3462 | 2 | 48 | 0.5759 | Croissant Panaderia |
| ERP-PROV-MX-034-D | 39.6978 | 1 | 20 | 0.5038 | Estándar Cafe Molido |
| ERP-PROV-MX-003-D | 36.4396 | 1 | 18 | 0.4940 | Filtros Mercancia |
| ERP-PROV-MX-040-A | 36.7033 | 1 | 17 | 0.4632 | Chocolate Bebidas |
| ERP-PROV-MX-032-D | 39.0824 | 1 | 18 | 0.4606 | Americano Cafe Grano |
| ERP-PROV-MX-013-B | 36.1484 | 1 | 16 | 0.4426 | Selección Cafe Molido |
| ERP-PROV-MX-061-D | 40.8077 | 1 | 18 | 0.4411 | Descafeinado Cafe Molido |
| ERP-PROV-MX-007-D | 77.3132 | 2 | 34 | 0.4398 | Selección Cafe Grano |
| ERP-PROV-MX-054-B | 163.8956 | 4 | 72 | 0.4393 | Espresso Cafe Molido |

## 2. Episodios observados — enero a marzo

Leyenda: Fechas inclusivas por tienda y SKU; días cuenta ceros consecutivos. Los indicadores de borde solo señalan que el episodio toca el límite consultado, sin afirmar su duración real fuera de él. Muestro todas las filas sin índice. No disponible indica dato o base ausente.

| tienda_id | sku_erp | inicio | fin | dias | toca_inicio_ventana | toca_fin_ventana | nombre |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T015 | ERP-PROV-MX-014-D | 2026-02-09 00:00:00 | 2026-02-12 00:00:00 | 4 | False | False | Descafeinado Cafe Grano |
| T023 | ERP-PROV-MX-046-A | 2026-01-25 00:00:00 | 2026-01-28 00:00:00 | 4 | False | False | Termo Mercancia |
| T038 | ERP-PROV-MX-040-A | 2026-03-18 00:00:00 | 2026-03-21 00:00:00 | 4 | False | False | Chocolate Bebidas |

## 3. Crecimiento por canal — abril a marzo

Leyenda: Ingresos estimados y base anterior en MXN; crecimiento en porcentaje. Registros incluye todos los códigos conservados aunque N/P/T contribuyen cero. Base ausente o cero: no disponible. Muestro todas las filas sin índice. No disponible indica dato o base ausente.

| canal | mes | registros | ingreso_mxn | anterior_mxn | crecimiento_pct |
| --- | --- | --- | --- | --- | --- |
| fisico | 2025-04 | 4,746.0000 | 1,532,102.3500 | 1,598,907.0000 | -4.1781 |
| fisico | 2025-05 | 4,851.0000 | 1,639,657.5000 | 1,532,102.3500 | 7.0201 |
| fisico | 2025-06 | 4,786.0000 | 1,577,691.0000 | 1,639,657.5000 | -3.7792 |
| fisico | 2025-07 | 5,016.0000 | 1,644,239.2900 | 1,577,691.0000 | 4.2181 |
| fisico | 2025-08 | 5,023.0000 | 1,642,587.4600 | 1,644,239.2900 | -0.1005 |
| fisico | 2025-09 | 4,718.0000 | 1,563,129.3800 | 1,642,587.4600 | -4.8374 |
| fisico | 2025-10 | 4,910.0000 | 1,648,071.3700 | 1,563,129.3800 | 5.4341 |
| fisico | 2025-11 | 4,713.0000 | 1,544,897.0900 | 1,648,071.3700 | -6.2603 |
| fisico | 2025-12 | 4,893.0000 | 1,648,254.7800 | 1,544,897.0900 | 6.6903 |
| fisico | 2026-01 | 4,876.0000 | 1,553,376.6600 | 1,648,254.7800 | -5.7563 |
| fisico | 2026-02 | 4,442.0000 | 1,434,264.5700 | 1,553,376.6600 | -7.6679 |
| fisico | 2026-03 | 4,788.0000 | 1,543,956.2700 | 1,434,264.5700 | 7.6479 |
| online | 2025-04 | 876.0000 | 383,213.0400 | No disponible | No disponible |
| online | 2025-05 | 829.0000 | 365,088.1800 | 383,213.0400 | -4.7297 |
| online | 2025-06 | 766.0000 | 339,352.2700 | 365,088.1800 | -7.0492 |
| online | 2025-07 | 809.0000 | 350,578.5000 | 339,352.2700 | 3.3081 |
| online | 2025-08 | 867.0000 | 343,799.7400 | 350,578.5000 | -1.9336 |
| online | 2025-09 | 815.0000 | 345,453.7700 | 343,799.7400 | 0.4811 |
| online | 2025-10 | 881.0000 | 376,497.0900 | 345,453.7700 | 8.9862 |
| online | 2025-11 | 858.0000 | 359,337.6800 | 376,497.0900 | -4.5576 |
| online | 2025-12 | 830.0000 | 346,649.1800 | 359,337.6800 | -3.5311 |
| online | 2026-01 | 822.0000 | 344,899.0400 | 346,649.1800 | -0.5049 |
| online | 2026-02 | 759.0000 | 323,250.6000 | 344,899.0400 | -6.2767 |
| online | 2026-03 | 835.0000 | 350,763.4500 | 323,250.6000 | 8.5113 |

## 4. Operaciones con margen negativo — abril a marzo

Leyenda: Por canal, tienda y SKU: cuento operaciones I u órdenes negativas y sumo únicamente su margen en MXN. No representa el margen de todas las operaciones del grupo. Muestro todas las filas sin índice. No disponible indica dato o base ausente.

| canal | tienda_id | sku_erp | operaciones_negativas | margen_negativo_mxn | nombre |
| --- | --- | --- | --- | --- | --- |
| fisico | T001 | ERP-PROV-MX-002-B | 20 | -808.7800 | Sándwich Comida Caliente |
| fisico | T001 | ERP-PROV-MX-015-D | 24 | -3,938.0100 | Especial Cafe Molido |
| fisico | T002 | ERP-PROV-MX-002-B | 13 | -1,009.1200 | Sándwich Comida Caliente |
| fisico | T002 | ERP-PROV-MX-015-D | 17 | -3,219.5400 | Especial Cafe Molido |
| fisico | T003 | ERP-PROV-MX-002-B | 12 | -527.8900 | Sándwich Comida Caliente |
| fisico | T003 | ERP-PROV-MX-015-D | 21 | -2,853.1900 | Especial Cafe Molido |
| fisico | T004 | ERP-PROV-MX-002-B | 15 | -718.0000 | Sándwich Comida Caliente |
| fisico | T004 | ERP-PROV-MX-015-D | 21 | -4,413.9700 | Especial Cafe Molido |
| fisico | T005 | ERP-PROV-MX-002-B | 23 | -1,156.3500 | Sándwich Comida Caliente |
| fisico | T005 | ERP-PROV-MX-015-D | 21 | -2,712.5300 | Especial Cafe Molido |
| fisico | T006 | ERP-PROV-MX-002-B | 22 | -1,275.4000 | Sándwich Comida Caliente |
| fisico | T006 | ERP-PROV-MX-015-D | 25 | -4,027.8800 | Especial Cafe Molido |
| fisico | T007 | ERP-PROV-MX-002-B | 19 | -1,153.8700 | Sándwich Comida Caliente |
| fisico | T007 | ERP-PROV-MX-015-D | 27 | -4,452.4300 | Especial Cafe Molido |
| fisico | T008 | ERP-PROV-MX-002-B | 21 | -1,039.7700 | Sándwich Comida Caliente |
| fisico | T008 | ERP-PROV-MX-015-D | 14 | -2,304.2700 | Especial Cafe Molido |
| fisico | T009 | ERP-PROV-MX-002-B | 22 | -1,264.8700 | Sándwich Comida Caliente |
| fisico | T009 | ERP-PROV-MX-015-D | 16 | -2,106.5300 | Especial Cafe Molido |
| fisico | T010 | ERP-PROV-MX-002-B | 11 | -631.7600 | Sándwich Comida Caliente |
| fisico | T010 | ERP-PROV-MX-015-D | 13 | -1,616.6200 | Especial Cafe Molido |
| fisico | T011 | ERP-PROV-MX-002-B | 24 | -1,553.4300 | Sándwich Comida Caliente |
| fisico | T011 | ERP-PROV-MX-015-D | 18 | -4,820.5900 | Especial Cafe Molido |
| fisico | T012 | ERP-PROV-MX-002-B | 14 | -742.9800 | Sándwich Comida Caliente |
| fisico | T012 | ERP-PROV-MX-015-D | 14 | -2,927.1200 | Especial Cafe Molido |
| fisico | T013 | ERP-PROV-MX-002-B | 28 | -2,323.1600 | Sándwich Comida Caliente |
| fisico | T013 | ERP-PROV-MX-015-D | 14 | -2,672.0200 | Especial Cafe Molido |
| fisico | T014 | ERP-PROV-MX-002-B | 31 | -1,515.9700 | Sándwich Comida Caliente |
| fisico | T014 | ERP-PROV-MX-015-D | 20 | -3,930.2200 | Especial Cafe Molido |
| fisico | T015 | ERP-PROV-MX-002-B | 16 | -1,068.8400 | Sándwich Comida Caliente |
| fisico | T015 | ERP-PROV-MX-015-D | 19 | -2,749.2400 | Especial Cafe Molido |
| fisico | T016 | ERP-PROV-MX-002-B | 17 | -1,585.1600 | Sándwich Comida Caliente |
| fisico | T016 | ERP-PROV-MX-015-D | 21 | -4,550.4900 | Especial Cafe Molido |
| fisico | T017 | ERP-PROV-MX-002-B | 11 | -531.9500 | Sándwich Comida Caliente |
| fisico | T017 | ERP-PROV-MX-015-D | 21 | -3,310.2700 | Especial Cafe Molido |
| fisico | T018 | ERP-PROV-MX-002-B | 20 | -1,400.4700 | Sándwich Comida Caliente |
| fisico | T018 | ERP-PROV-MX-015-D | 13 | -3,133.9500 | Especial Cafe Molido |
| fisico | T019 | ERP-PROV-MX-002-B | 11 | -696.2800 | Sándwich Comida Caliente |
| fisico | T019 | ERP-PROV-MX-015-D | 27 | -4,223.2100 | Especial Cafe Molido |
| fisico | T020 | ERP-PROV-MX-002-B | 20 | -1,403.5600 | Sándwich Comida Caliente |
| fisico | T020 | ERP-PROV-MX-015-D | 19 | -2,612.3700 | Especial Cafe Molido |
| fisico | T021 | ERP-PROV-MX-002-B | 13 | -824.9700 | Sándwich Comida Caliente |
| fisico | T021 | ERP-PROV-MX-015-D | 15 | -2,118.7800 | Especial Cafe Molido |
| fisico | T022 | ERP-PROV-MX-002-B | 20 | -963.0000 | Sándwich Comida Caliente |
| fisico | T022 | ERP-PROV-MX-015-D | 28 | -4,147.8200 | Especial Cafe Molido |
| fisico | T023 | ERP-PROV-MX-002-B | 16 | -1,173.3900 | Sándwich Comida Caliente |
| fisico | T023 | ERP-PROV-MX-015-D | 22 | -5,747.1700 | Especial Cafe Molido |
| fisico | T024 | ERP-PROV-MX-002-B | 15 | -945.3400 | Sándwich Comida Caliente |
| fisico | T024 | ERP-PROV-MX-015-D | 15 | -2,485.9800 | Especial Cafe Molido |
| fisico | T025 | ERP-PROV-MX-002-B | 19 | -1,185.2000 | Sándwich Comida Caliente |
| fisico | T025 | ERP-PROV-MX-015-D | 18 | -3,340.1100 | Especial Cafe Molido |
| fisico | T026 | ERP-PROV-MX-002-B | 16 | -667.7000 | Sándwich Comida Caliente |
| fisico | T026 | ERP-PROV-MX-015-D | 26 | -5,527.0700 | Especial Cafe Molido |
| fisico | T027 | ERP-PROV-MX-002-B | 25 | -1,167.3000 | Sándwich Comida Caliente |
| fisico | T027 | ERP-PROV-MX-015-D | 28 | -4,967.2900 | Especial Cafe Molido |
| fisico | T028 | ERP-PROV-MX-002-B | 15 | -715.0800 | Sándwich Comida Caliente |
| fisico | T028 | ERP-PROV-MX-015-D | 14 | -2,187.9400 | Especial Cafe Molido |
| fisico | T029 | ERP-PROV-MX-002-B | 22 | -1,758.6500 | Sándwich Comida Caliente |
| fisico | T029 | ERP-PROV-MX-015-D | 19 | -4,322.6300 | Especial Cafe Molido |
| fisico | T030 | ERP-PROV-MX-002-B | 21 | -1,034.6500 | Sándwich Comida Caliente |
| fisico | T030 | ERP-PROV-MX-015-D | 28 | -4,677.7700 | Especial Cafe Molido |
| fisico | T031 | ERP-PROV-MX-002-B | 22 | -1,479.0900 | Sándwich Comida Caliente |
| fisico | T031 | ERP-PROV-MX-015-D | 19 | -3,939.2400 | Especial Cafe Molido |
| fisico | T032 | ERP-PROV-MX-002-B | 21 | -1,136.8900 | Sándwich Comida Caliente |
| fisico | T032 | ERP-PROV-MX-015-D | 28 | -5,068.9800 | Especial Cafe Molido |
| fisico | T033 | ERP-PROV-MX-002-B | 23 | -1,368.6100 | Sándwich Comida Caliente |
| fisico | T033 | ERP-PROV-MX-015-D | 24 | -4,025.9200 | Especial Cafe Molido |
| fisico | T034 | ERP-PROV-MX-002-B | 18 | -1,339.2100 | Sándwich Comida Caliente |
| fisico | T034 | ERP-PROV-MX-015-D | 17 | -4,458.4200 | Especial Cafe Molido |
| fisico | T035 | ERP-PROV-MX-002-B | 18 | -810.6100 | Sándwich Comida Caliente |
| fisico | T035 | ERP-PROV-MX-015-D | 17 | -2,595.7500 | Especial Cafe Molido |
| fisico | T036 | ERP-PROV-MX-002-B | 27 | -1,767.8000 | Sándwich Comida Caliente |
| fisico | T036 | ERP-PROV-MX-015-D | 33 | -9,061.6800 | Especial Cafe Molido |
| fisico | T037 | ERP-PROV-MX-002-B | 21 | -1,704.6500 | Sándwich Comida Caliente |
| fisico | T037 | ERP-PROV-MX-015-D | 17 | -3,014.8700 | Especial Cafe Molido |
| fisico | T038 | ERP-PROV-MX-002-B | 19 | -1,010.7300 | Sándwich Comida Caliente |
| fisico | T038 | ERP-PROV-MX-015-D | 26 | -5,163.5000 | Especial Cafe Molido |
| fisico | T039 | ERP-PROV-MX-002-B | 19 | -1,024.5800 | Sándwich Comida Caliente |
| fisico | T039 | ERP-PROV-MX-015-D | 23 | -3,723.5600 | Especial Cafe Molido |
| fisico | T040 | ERP-PROV-MX-002-B | 22 | -1,190.3700 | Sándwich Comida Caliente |
| fisico | T040 | ERP-PROV-MX-015-D | 20 | -3,146.7500 | Especial Cafe Molido |

## 4.1 Margen acumulado negativo — abril a marzo

Leyenda: Sumo operaciones positivas y negativas elegibles con costo dentro del año por canal, tienda y SKU; muestro solo grupos negativos. Margen en MXN, anterior a gastos y ajuste fiscal no disponible. Muestro todas las filas sin índice. No disponible indica dato o base ausente.

| canal | tienda_id | sku_erp | operaciones | margen_total_mxn | nombre |
| --- | --- | --- | --- | --- | --- |
| fisico | T001 | ERP-PROV-MX-002-B | 20 | -808.7800 | Sándwich Comida Caliente |
| fisico | T001 | ERP-PROV-MX-015-D | 24 | -3,938.0100 | Especial Cafe Molido |
| fisico | T002 | ERP-PROV-MX-002-B | 13 | -1,009.1200 | Sándwich Comida Caliente |
| fisico | T002 | ERP-PROV-MX-015-D | 17 | -3,219.5400 | Especial Cafe Molido |
| fisico | T003 | ERP-PROV-MX-002-B | 12 | -527.8900 | Sándwich Comida Caliente |
| fisico | T003 | ERP-PROV-MX-015-D | 21 | -2,853.1900 | Especial Cafe Molido |
| fisico | T004 | ERP-PROV-MX-002-B | 15 | -718.0000 | Sándwich Comida Caliente |
| fisico | T004 | ERP-PROV-MX-015-D | 21 | -4,413.9700 | Especial Cafe Molido |
| fisico | T005 | ERP-PROV-MX-002-B | 23 | -1,156.3500 | Sándwich Comida Caliente |
| fisico | T005 | ERP-PROV-MX-015-D | 21 | -2,712.5300 | Especial Cafe Molido |
| fisico | T006 | ERP-PROV-MX-002-B | 22 | -1,275.4000 | Sándwich Comida Caliente |
| fisico | T006 | ERP-PROV-MX-015-D | 25 | -4,027.8800 | Especial Cafe Molido |
| fisico | T007 | ERP-PROV-MX-002-B | 19 | -1,153.8700 | Sándwich Comida Caliente |
| fisico | T007 | ERP-PROV-MX-015-D | 27 | -4,452.4300 | Especial Cafe Molido |
| fisico | T008 | ERP-PROV-MX-002-B | 21 | -1,039.7700 | Sándwich Comida Caliente |
| fisico | T008 | ERP-PROV-MX-015-D | 14 | -2,304.2700 | Especial Cafe Molido |
| fisico | T009 | ERP-PROV-MX-002-B | 22 | -1,264.8700 | Sándwich Comida Caliente |
| fisico | T009 | ERP-PROV-MX-015-D | 16 | -2,106.5300 | Especial Cafe Molido |
| fisico | T010 | ERP-PROV-MX-002-B | 11 | -631.7600 | Sándwich Comida Caliente |
| fisico | T010 | ERP-PROV-MX-015-D | 13 | -1,616.6200 | Especial Cafe Molido |
| fisico | T011 | ERP-PROV-MX-002-B | 24 | -1,553.4300 | Sándwich Comida Caliente |
| fisico | T011 | ERP-PROV-MX-015-D | 18 | -4,820.5900 | Especial Cafe Molido |
| fisico | T012 | ERP-PROV-MX-002-B | 14 | -742.9800 | Sándwich Comida Caliente |
| fisico | T012 | ERP-PROV-MX-015-D | 14 | -2,927.1200 | Especial Cafe Molido |
| fisico | T013 | ERP-PROV-MX-002-B | 28 | -2,323.1600 | Sándwich Comida Caliente |
| fisico | T013 | ERP-PROV-MX-015-D | 14 | -2,672.0200 | Especial Cafe Molido |
| fisico | T014 | ERP-PROV-MX-002-B | 31 | -1,515.9700 | Sándwich Comida Caliente |
| fisico | T014 | ERP-PROV-MX-015-D | 20 | -3,930.2200 | Especial Cafe Molido |
| fisico | T015 | ERP-PROV-MX-002-B | 16 | -1,068.8400 | Sándwich Comida Caliente |
| fisico | T015 | ERP-PROV-MX-015-D | 19 | -2,749.2400 | Especial Cafe Molido |
| fisico | T016 | ERP-PROV-MX-002-B | 17 | -1,585.1600 | Sándwich Comida Caliente |
| fisico | T016 | ERP-PROV-MX-015-D | 21 | -4,550.4900 | Especial Cafe Molido |
| fisico | T017 | ERP-PROV-MX-002-B | 11 | -531.9500 | Sándwich Comida Caliente |
| fisico | T017 | ERP-PROV-MX-015-D | 21 | -3,310.2700 | Especial Cafe Molido |
| fisico | T018 | ERP-PROV-MX-002-B | 20 | -1,400.4700 | Sándwich Comida Caliente |
| fisico | T018 | ERP-PROV-MX-015-D | 13 | -3,133.9500 | Especial Cafe Molido |
| fisico | T019 | ERP-PROV-MX-002-B | 11 | -696.2800 | Sándwich Comida Caliente |
| fisico | T019 | ERP-PROV-MX-015-D | 27 | -4,223.2100 | Especial Cafe Molido |
| fisico | T020 | ERP-PROV-MX-002-B | 20 | -1,403.5600 | Sándwich Comida Caliente |
| fisico | T020 | ERP-PROV-MX-015-D | 19 | -2,612.3700 | Especial Cafe Molido |
| fisico | T021 | ERP-PROV-MX-002-B | 13 | -824.9700 | Sándwich Comida Caliente |
| fisico | T021 | ERP-PROV-MX-015-D | 15 | -2,118.7800 | Especial Cafe Molido |
| fisico | T022 | ERP-PROV-MX-002-B | 20 | -963.0000 | Sándwich Comida Caliente |
| fisico | T022 | ERP-PROV-MX-015-D | 28 | -4,147.8200 | Especial Cafe Molido |
| fisico | T023 | ERP-PROV-MX-002-B | 16 | -1,173.3900 | Sándwich Comida Caliente |
| fisico | T023 | ERP-PROV-MX-015-D | 22 | -5,747.1700 | Especial Cafe Molido |
| fisico | T024 | ERP-PROV-MX-002-B | 15 | -945.3400 | Sándwich Comida Caliente |
| fisico | T024 | ERP-PROV-MX-015-D | 15 | -2,485.9800 | Especial Cafe Molido |
| fisico | T025 | ERP-PROV-MX-002-B | 19 | -1,185.2000 | Sándwich Comida Caliente |
| fisico | T025 | ERP-PROV-MX-015-D | 18 | -3,340.1100 | Especial Cafe Molido |
| fisico | T026 | ERP-PROV-MX-002-B | 16 | -667.7000 | Sándwich Comida Caliente |
| fisico | T026 | ERP-PROV-MX-015-D | 26 | -5,527.0700 | Especial Cafe Molido |
| fisico | T027 | ERP-PROV-MX-002-B | 25 | -1,167.3000 | Sándwich Comida Caliente |
| fisico | T027 | ERP-PROV-MX-015-D | 28 | -4,967.2900 | Especial Cafe Molido |
| fisico | T028 | ERP-PROV-MX-002-B | 15 | -715.0800 | Sándwich Comida Caliente |
| fisico | T028 | ERP-PROV-MX-015-D | 14 | -2,187.9400 | Especial Cafe Molido |
| fisico | T029 | ERP-PROV-MX-002-B | 22 | -1,758.6500 | Sándwich Comida Caliente |
| fisico | T029 | ERP-PROV-MX-015-D | 19 | -4,322.6300 | Especial Cafe Molido |
| fisico | T030 | ERP-PROV-MX-002-B | 21 | -1,034.6500 | Sándwich Comida Caliente |
| fisico | T030 | ERP-PROV-MX-015-D | 28 | -4,677.7700 | Especial Cafe Molido |
| fisico | T031 | ERP-PROV-MX-002-B | 22 | -1,479.0900 | Sándwich Comida Caliente |
| fisico | T031 | ERP-PROV-MX-015-D | 19 | -3,939.2400 | Especial Cafe Molido |
| fisico | T032 | ERP-PROV-MX-002-B | 21 | -1,136.8900 | Sándwich Comida Caliente |
| fisico | T032 | ERP-PROV-MX-015-D | 28 | -5,068.9800 | Especial Cafe Molido |
| fisico | T033 | ERP-PROV-MX-002-B | 23 | -1,368.6100 | Sándwich Comida Caliente |
| fisico | T033 | ERP-PROV-MX-015-D | 24 | -4,025.9200 | Especial Cafe Molido |
| fisico | T034 | ERP-PROV-MX-002-B | 18 | -1,339.2100 | Sándwich Comida Caliente |
| fisico | T034 | ERP-PROV-MX-015-D | 17 | -4,458.4200 | Especial Cafe Molido |
| fisico | T035 | ERP-PROV-MX-002-B | 18 | -810.6100 | Sándwich Comida Caliente |
| fisico | T035 | ERP-PROV-MX-015-D | 17 | -2,595.7500 | Especial Cafe Molido |
| fisico | T036 | ERP-PROV-MX-002-B | 27 | -1,767.8000 | Sándwich Comida Caliente |
| fisico | T036 | ERP-PROV-MX-015-D | 33 | -9,061.6800 | Especial Cafe Molido |
| fisico | T037 | ERP-PROV-MX-002-B | 21 | -1,704.6500 | Sándwich Comida Caliente |
| fisico | T037 | ERP-PROV-MX-015-D | 17 | -3,014.8700 | Especial Cafe Molido |
| fisico | T038 | ERP-PROV-MX-002-B | 19 | -1,010.7300 | Sándwich Comida Caliente |
| fisico | T038 | ERP-PROV-MX-015-D | 26 | -5,163.5000 | Especial Cafe Molido |
| fisico | T039 | ERP-PROV-MX-002-B | 19 | -1,024.5800 | Sándwich Comida Caliente |
| fisico | T039 | ERP-PROV-MX-015-D | 23 | -3,723.5600 | Especial Cafe Molido |
| fisico | T040 | ERP-PROV-MX-002-B | 22 | -1,190.3700 | Sándwich Comida Caliente |
| fisico | T040 | ERP-PROV-MX-015-D | 20 | -3,146.7500 | Especial Cafe Molido |

## Cobertura de equivalencias — toda la fuente

Leyenda: Registros por canal y estado excluyente: exacto, sin equivalencia y equivalencia con ERP nulo. Sin filtrado temporal de negocio. Muestro todas las filas sin índice. No disponible indica dato o base ausente.

| canal | estado_mapeo | registros |
| --- | --- | --- |
| fisico | erp_nulo | 6132 |
| fisico | exacto | 74141 |
| fisico | sin_equivalencia | 6217 |
| online | erp_nulo | 1139 |
| online | exacto | 6959 |
| online | sin_equivalencia | 1849 |

## Cobertura de costo — toda la fuente

Leyenda: Cuento todos los registros, incluidos comprobantes no elegibles, según costo disponible. No es el denominador de operaciones de margen del año. Muestro todas las filas sin índice. No disponible indica dato o base ausente.

| canal | costo_disponible | registros |
| --- | --- | --- |
| fisico | False | 12349 |
| fisico | True | 74141 |
| online | False | 2988 |
| online | True | 6959 |

## Cobertura del ranking

Leyenda: Conteos de pares observados, pares con todos los saldos conocidos y días exigidos del semestre; desconocido nunca equivale a cero. Muestro todas las filas sin índice. No disponible indica dato o base ausente.

| medida | valor |
| --- | --- |
| pares_observados | 1268 |
| pares_cobertura_completa | 36 |
| dias_exigidos | 182 |

## 2.1 Tiendas afectadas

Leyenda: Una fila por tienda; productos distintos, cantidad de episodios y duración máxima observada en días. Muestro todas las filas sin índice. No disponible indica dato o base ausente.

| tienda_id | productos | episodios | duracion_maxima_dias |
| --- | --- | --- | --- |
| T015 | 1 | 1 | 4 |
| T023 | 1 | 1 | 4 |
| T038 | 1 | 1 | 4 |

## Conclusión

Obtengo cuatro respuestas reproducibles con cobertura explícita y excepciones conservadas. Interpreto los resultados como escenarios operativos sujetos a los límites de las fuentes.
