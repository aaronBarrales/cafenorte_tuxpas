# Respuestas calculadas de CaféNorte

Mi corte es 2026-03-31; analizo conjuntamente las cuatro fuentes identificadas en el manifiesto. Aplico las interpretaciones del README; no certifico ingresos contables ni unidades equivalentes.

Para rotación uso unidades I y pares tienda–SKU con cobertura diaria completa. Para quiebres cuento ceros consecutivos observados, sin completar ausencias. MoM usa I menos E y órdenes online sin estatus. Margen compara importe con costo vigente y es anterior a gastos e impuestos no identificados.

## rotacion_top10

Leyenda: muestro todas las filas sin índice; centavos son centésimas de MXN; crecimiento_pct es porcentaje y rotacion_veces son vueltas del semestre. No disponible expresa ausencia de base o denominador válido; tiendas cuenta sucursales incluidas. Ordeno el ranking por rotación descendente y SKU ascendente para desempatar.

| sku_erp | inventario_promedio | tiendas | unidades_I | rotacion_veces |
| --- | --- | --- | --- | --- |
| ERP-PROV-MX-027-B | 39.9615 | 1 | 29 | 0.7257 |
| ERP-PROV-MX-005-C | 83.3462 | 2 | 48 | 0.5759 |
| ERP-PROV-MX-034-D | 39.6978 | 1 | 20 | 0.5038 |
| ERP-PROV-MX-003-D | 36.4396 | 1 | 18 | 0.4940 |
| ERP-PROV-MX-040-A | 36.7033 | 1 | 17 | 0.4632 |
| ERP-PROV-MX-032-D | 39.0824 | 1 | 18 | 0.4606 |
| ERP-PROV-MX-013-B | 36.1484 | 1 | 16 | 0.4426 |
| ERP-PROV-MX-061-D | 40.8077 | 1 | 18 | 0.4411 |
| ERP-PROV-MX-007-D | 77.3132 | 2 | 34 | 0.4398 |
| ERP-PROV-MX-054-B | 163.8956 | 4 | 72 | 0.4393 |

## quiebres_episodios

Leyenda: muestro todas las filas sin índice; centavos son centésimas de MXN; crecimiento_pct es porcentaje y rotacion_veces son vueltas del semestre. No disponible expresa ausencia de base o denominador válido; tiendas cuenta sucursales incluidas. Ordeno el ranking por rotación descendente y SKU ascendente para desempatar.

| tienda_id | sku_erp | inicio | fin | dias | toca_inicio_ventana | toca_fin_ventana |
| --- | --- | --- | --- | --- | --- | --- |
| T015 | ERP-PROV-MX-014-D | 2026-02-09 00:00:00 | 2026-02-12 00:00:00 | 4 | False | False |
| T023 | ERP-PROV-MX-046-A | 2026-01-25 00:00:00 | 2026-01-28 00:00:00 | 4 | False | False |
| T038 | ERP-PROV-MX-040-A | 2026-03-18 00:00:00 | 2026-03-21 00:00:00 | 4 | False | False |

## crecimiento_mensual

Leyenda: muestro todas las filas sin índice; centavos son centésimas de MXN; crecimiento_pct es porcentaje y rotacion_veces son vueltas del semestre. No disponible expresa ausencia de base o denominador válido; tiendas cuenta sucursales incluidas. Ordeno el ranking por rotación descendente y SKU ascendente para desempatar.

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

## margen_negativo_operaciones

Leyenda: muestro todas las filas sin índice; centavos son centésimas de MXN; crecimiento_pct es porcentaje y rotacion_veces son vueltas del semestre. No disponible expresa ausencia de base o denominador válido; tiendas cuenta sucursales incluidas. Ordeno el ranking por rotación descendente y SKU ascendente para desempatar.

| canal | tienda_id | sku_erp | operaciones_negativas | margen_negativo_centavos |
| --- | --- | --- | --- | --- |
| fisico | T001 | ERP-PROV-MX-002-B | 20 | -80,878.0000 |
| fisico | T001 | ERP-PROV-MX-015-D | 24 | -393,801.0000 |
| fisico | T002 | ERP-PROV-MX-002-B | 13 | -100,912.0000 |
| fisico | T002 | ERP-PROV-MX-015-D | 17 | -321,954.0000 |
| fisico | T003 | ERP-PROV-MX-002-B | 12 | -52,789.0000 |
| fisico | T003 | ERP-PROV-MX-015-D | 21 | -285,319.0000 |
| fisico | T004 | ERP-PROV-MX-002-B | 15 | -71,800.0000 |
| fisico | T004 | ERP-PROV-MX-015-D | 21 | -441,397.0000 |
| fisico | T005 | ERP-PROV-MX-002-B | 23 | -115,635.0000 |
| fisico | T005 | ERP-PROV-MX-015-D | 21 | -271,253.0000 |
| fisico | T006 | ERP-PROV-MX-002-B | 22 | -127,540.0000 |
| fisico | T006 | ERP-PROV-MX-015-D | 25 | -402,788.0000 |
| fisico | T007 | ERP-PROV-MX-002-B | 19 | -115,387.0000 |
| fisico | T007 | ERP-PROV-MX-015-D | 27 | -445,243.0000 |
| fisico | T008 | ERP-PROV-MX-002-B | 21 | -103,977.0000 |
| fisico | T008 | ERP-PROV-MX-015-D | 14 | -230,427.0000 |
| fisico | T009 | ERP-PROV-MX-002-B | 22 | -126,487.0000 |
| fisico | T009 | ERP-PROV-MX-015-D | 16 | -210,653.0000 |
| fisico | T010 | ERP-PROV-MX-002-B | 11 | -63,176.0000 |
| fisico | T010 | ERP-PROV-MX-015-D | 13 | -161,662.0000 |
| fisico | T011 | ERP-PROV-MX-002-B | 24 | -155,343.0000 |
| fisico | T011 | ERP-PROV-MX-015-D | 18 | -482,059.0000 |
| fisico | T012 | ERP-PROV-MX-002-B | 14 | -74,298.0000 |
| fisico | T012 | ERP-PROV-MX-015-D | 14 | -292,712.0000 |
| fisico | T013 | ERP-PROV-MX-002-B | 28 | -232,316.0000 |
| fisico | T013 | ERP-PROV-MX-015-D | 14 | -267,202.0000 |
| fisico | T014 | ERP-PROV-MX-002-B | 31 | -151,597.0000 |
| fisico | T014 | ERP-PROV-MX-015-D | 20 | -393,022.0000 |
| fisico | T015 | ERP-PROV-MX-002-B | 16 | -106,884.0000 |
| fisico | T015 | ERP-PROV-MX-015-D | 19 | -274,924.0000 |
| fisico | T016 | ERP-PROV-MX-002-B | 17 | -158,516.0000 |
| fisico | T016 | ERP-PROV-MX-015-D | 21 | -455,049.0000 |
| fisico | T017 | ERP-PROV-MX-002-B | 11 | -53,195.0000 |
| fisico | T017 | ERP-PROV-MX-015-D | 21 | -331,027.0000 |
| fisico | T018 | ERP-PROV-MX-002-B | 20 | -140,047.0000 |
| fisico | T018 | ERP-PROV-MX-015-D | 13 | -313,395.0000 |
| fisico | T019 | ERP-PROV-MX-002-B | 11 | -69,628.0000 |
| fisico | T019 | ERP-PROV-MX-015-D | 27 | -422,321.0000 |
| fisico | T020 | ERP-PROV-MX-002-B | 20 | -140,356.0000 |
| fisico | T020 | ERP-PROV-MX-015-D | 19 | -261,237.0000 |
| fisico | T021 | ERP-PROV-MX-002-B | 13 | -82,497.0000 |
| fisico | T021 | ERP-PROV-MX-015-D | 15 | -211,878.0000 |
| fisico | T022 | ERP-PROV-MX-002-B | 20 | -96,300.0000 |
| fisico | T022 | ERP-PROV-MX-015-D | 28 | -414,782.0000 |
| fisico | T023 | ERP-PROV-MX-002-B | 16 | -117,339.0000 |
| fisico | T023 | ERP-PROV-MX-015-D | 22 | -574,717.0000 |
| fisico | T024 | ERP-PROV-MX-002-B | 15 | -94,534.0000 |
| fisico | T024 | ERP-PROV-MX-015-D | 15 | -248,598.0000 |
| fisico | T025 | ERP-PROV-MX-002-B | 19 | -118,520.0000 |
| fisico | T025 | ERP-PROV-MX-015-D | 18 | -334,011.0000 |
| fisico | T026 | ERP-PROV-MX-002-B | 16 | -66,770.0000 |
| fisico | T026 | ERP-PROV-MX-015-D | 26 | -552,707.0000 |
| fisico | T027 | ERP-PROV-MX-002-B | 25 | -116,730.0000 |
| fisico | T027 | ERP-PROV-MX-015-D | 28 | -496,729.0000 |
| fisico | T028 | ERP-PROV-MX-002-B | 15 | -71,508.0000 |
| fisico | T028 | ERP-PROV-MX-015-D | 14 | -218,794.0000 |
| fisico | T029 | ERP-PROV-MX-002-B | 22 | -175,865.0000 |
| fisico | T029 | ERP-PROV-MX-015-D | 19 | -432,263.0000 |
| fisico | T030 | ERP-PROV-MX-002-B | 21 | -103,465.0000 |
| fisico | T030 | ERP-PROV-MX-015-D | 28 | -467,777.0000 |
| fisico | T031 | ERP-PROV-MX-002-B | 22 | -147,909.0000 |
| fisico | T031 | ERP-PROV-MX-015-D | 19 | -393,924.0000 |
| fisico | T032 | ERP-PROV-MX-002-B | 21 | -113,689.0000 |
| fisico | T032 | ERP-PROV-MX-015-D | 28 | -506,898.0000 |
| fisico | T033 | ERP-PROV-MX-002-B | 23 | -136,861.0000 |
| fisico | T033 | ERP-PROV-MX-015-D | 24 | -402,592.0000 |
| fisico | T034 | ERP-PROV-MX-002-B | 18 | -133,921.0000 |
| fisico | T034 | ERP-PROV-MX-015-D | 17 | -445,842.0000 |
| fisico | T035 | ERP-PROV-MX-002-B | 18 | -81,061.0000 |
| fisico | T035 | ERP-PROV-MX-015-D | 17 | -259,575.0000 |
| fisico | T036 | ERP-PROV-MX-002-B | 27 | -176,780.0000 |
| fisico | T036 | ERP-PROV-MX-015-D | 33 | -906,168.0000 |
| fisico | T037 | ERP-PROV-MX-002-B | 21 | -170,465.0000 |
| fisico | T037 | ERP-PROV-MX-015-D | 17 | -301,487.0000 |
| fisico | T038 | ERP-PROV-MX-002-B | 19 | -101,073.0000 |
| fisico | T038 | ERP-PROV-MX-015-D | 26 | -516,350.0000 |
| fisico | T039 | ERP-PROV-MX-002-B | 19 | -102,458.0000 |
| fisico | T039 | ERP-PROV-MX-015-D | 23 | -372,356.0000 |
| fisico | T040 | ERP-PROV-MX-002-B | 22 | -119,037.0000 |
| fisico | T040 | ERP-PROV-MX-015-D | 20 | -314,675.0000 |

## margen_negativo_acumulado

Leyenda: muestro todas las filas sin índice; centavos son centésimas de MXN; crecimiento_pct es porcentaje y rotacion_veces son vueltas del semestre. No disponible expresa ausencia de base o denominador válido; tiendas cuenta sucursales incluidas. Ordeno el ranking por rotación descendente y SKU ascendente para desempatar.

| canal | tienda_id | sku_erp | operaciones | margen_total_centavos |
| --- | --- | --- | --- | --- |
| fisico | T001 | ERP-PROV-MX-002-B | 20 | -80,878.0000 |
| fisico | T001 | ERP-PROV-MX-015-D | 24 | -393,801.0000 |
| fisico | T002 | ERP-PROV-MX-002-B | 13 | -100,912.0000 |
| fisico | T002 | ERP-PROV-MX-015-D | 17 | -321,954.0000 |
| fisico | T003 | ERP-PROV-MX-002-B | 12 | -52,789.0000 |
| fisico | T003 | ERP-PROV-MX-015-D | 21 | -285,319.0000 |
| fisico | T004 | ERP-PROV-MX-002-B | 15 | -71,800.0000 |
| fisico | T004 | ERP-PROV-MX-015-D | 21 | -441,397.0000 |
| fisico | T005 | ERP-PROV-MX-002-B | 23 | -115,635.0000 |
| fisico | T005 | ERP-PROV-MX-015-D | 21 | -271,253.0000 |
| fisico | T006 | ERP-PROV-MX-002-B | 22 | -127,540.0000 |
| fisico | T006 | ERP-PROV-MX-015-D | 25 | -402,788.0000 |
| fisico | T007 | ERP-PROV-MX-002-B | 19 | -115,387.0000 |
| fisico | T007 | ERP-PROV-MX-015-D | 27 | -445,243.0000 |
| fisico | T008 | ERP-PROV-MX-002-B | 21 | -103,977.0000 |
| fisico | T008 | ERP-PROV-MX-015-D | 14 | -230,427.0000 |
| fisico | T009 | ERP-PROV-MX-002-B | 22 | -126,487.0000 |
| fisico | T009 | ERP-PROV-MX-015-D | 16 | -210,653.0000 |
| fisico | T010 | ERP-PROV-MX-002-B | 11 | -63,176.0000 |
| fisico | T010 | ERP-PROV-MX-015-D | 13 | -161,662.0000 |
| fisico | T011 | ERP-PROV-MX-002-B | 24 | -155,343.0000 |
| fisico | T011 | ERP-PROV-MX-015-D | 18 | -482,059.0000 |
| fisico | T012 | ERP-PROV-MX-002-B | 14 | -74,298.0000 |
| fisico | T012 | ERP-PROV-MX-015-D | 14 | -292,712.0000 |
| fisico | T013 | ERP-PROV-MX-002-B | 28 | -232,316.0000 |
| fisico | T013 | ERP-PROV-MX-015-D | 14 | -267,202.0000 |
| fisico | T014 | ERP-PROV-MX-002-B | 31 | -151,597.0000 |
| fisico | T014 | ERP-PROV-MX-015-D | 20 | -393,022.0000 |
| fisico | T015 | ERP-PROV-MX-002-B | 16 | -106,884.0000 |
| fisico | T015 | ERP-PROV-MX-015-D | 19 | -274,924.0000 |
| fisico | T016 | ERP-PROV-MX-002-B | 17 | -158,516.0000 |
| fisico | T016 | ERP-PROV-MX-015-D | 21 | -455,049.0000 |
| fisico | T017 | ERP-PROV-MX-002-B | 11 | -53,195.0000 |
| fisico | T017 | ERP-PROV-MX-015-D | 21 | -331,027.0000 |
| fisico | T018 | ERP-PROV-MX-002-B | 20 | -140,047.0000 |
| fisico | T018 | ERP-PROV-MX-015-D | 13 | -313,395.0000 |
| fisico | T019 | ERP-PROV-MX-002-B | 11 | -69,628.0000 |
| fisico | T019 | ERP-PROV-MX-015-D | 27 | -422,321.0000 |
| fisico | T020 | ERP-PROV-MX-002-B | 20 | -140,356.0000 |
| fisico | T020 | ERP-PROV-MX-015-D | 19 | -261,237.0000 |
| fisico | T021 | ERP-PROV-MX-002-B | 13 | -82,497.0000 |
| fisico | T021 | ERP-PROV-MX-015-D | 15 | -211,878.0000 |
| fisico | T022 | ERP-PROV-MX-002-B | 20 | -96,300.0000 |
| fisico | T022 | ERP-PROV-MX-015-D | 28 | -414,782.0000 |
| fisico | T023 | ERP-PROV-MX-002-B | 16 | -117,339.0000 |
| fisico | T023 | ERP-PROV-MX-015-D | 22 | -574,717.0000 |
| fisico | T024 | ERP-PROV-MX-002-B | 15 | -94,534.0000 |
| fisico | T024 | ERP-PROV-MX-015-D | 15 | -248,598.0000 |
| fisico | T025 | ERP-PROV-MX-002-B | 19 | -118,520.0000 |
| fisico | T025 | ERP-PROV-MX-015-D | 18 | -334,011.0000 |
| fisico | T026 | ERP-PROV-MX-002-B | 16 | -66,770.0000 |
| fisico | T026 | ERP-PROV-MX-015-D | 26 | -552,707.0000 |
| fisico | T027 | ERP-PROV-MX-002-B | 25 | -116,730.0000 |
| fisico | T027 | ERP-PROV-MX-015-D | 28 | -496,729.0000 |
| fisico | T028 | ERP-PROV-MX-002-B | 15 | -71,508.0000 |
| fisico | T028 | ERP-PROV-MX-015-D | 14 | -218,794.0000 |
| fisico | T029 | ERP-PROV-MX-002-B | 22 | -175,865.0000 |
| fisico | T029 | ERP-PROV-MX-015-D | 19 | -432,263.0000 |
| fisico | T030 | ERP-PROV-MX-002-B | 21 | -103,465.0000 |
| fisico | T030 | ERP-PROV-MX-015-D | 28 | -467,777.0000 |
| fisico | T031 | ERP-PROV-MX-002-B | 22 | -147,909.0000 |
| fisico | T031 | ERP-PROV-MX-015-D | 19 | -393,924.0000 |
| fisico | T032 | ERP-PROV-MX-002-B | 21 | -113,689.0000 |
| fisico | T032 | ERP-PROV-MX-015-D | 28 | -506,898.0000 |
| fisico | T033 | ERP-PROV-MX-002-B | 23 | -136,861.0000 |
| fisico | T033 | ERP-PROV-MX-015-D | 24 | -402,592.0000 |
| fisico | T034 | ERP-PROV-MX-002-B | 18 | -133,921.0000 |
| fisico | T034 | ERP-PROV-MX-015-D | 17 | -445,842.0000 |
| fisico | T035 | ERP-PROV-MX-002-B | 18 | -81,061.0000 |
| fisico | T035 | ERP-PROV-MX-015-D | 17 | -259,575.0000 |
| fisico | T036 | ERP-PROV-MX-002-B | 27 | -176,780.0000 |
| fisico | T036 | ERP-PROV-MX-015-D | 33 | -906,168.0000 |
| fisico | T037 | ERP-PROV-MX-002-B | 21 | -170,465.0000 |
| fisico | T037 | ERP-PROV-MX-015-D | 17 | -301,487.0000 |
| fisico | T038 | ERP-PROV-MX-002-B | 19 | -101,073.0000 |
| fisico | T038 | ERP-PROV-MX-015-D | 26 | -516,350.0000 |
| fisico | T039 | ERP-PROV-MX-002-B | 19 | -102,458.0000 |
| fisico | T039 | ERP-PROV-MX-015-D | 23 | -372,356.0000 |
| fisico | T040 | ERP-PROV-MX-002-B | 22 | -119,037.0000 |
| fisico | T040 | ERP-PROV-MX-015-D | 20 | -314,675.0000 |

## cobertura

Leyenda: muestro todas las filas sin índice; centavos son centésimas de MXN; crecimiento_pct es porcentaje y rotacion_veces son vueltas del semestre. No disponible expresa ausencia de base o denominador válido; tiendas cuenta sucursales incluidas. Ordeno el ranking por rotación descendente y SKU ascendente para desempatar.

| canal | estado_mapeo | registros |
| --- | --- | --- |
| fisico | erp_nulo | 6132 |
| fisico | exacto | 74141 |
| fisico | sin_equivalencia | 6217 |
| online | erp_nulo | 1139 |
| online | exacto | 6959 |
| online | sin_equivalencia | 1849 |

## cobertura_margen

Leyenda: muestro todas las filas sin índice; centavos son centésimas de MXN; crecimiento_pct es porcentaje y rotacion_veces son vueltas del semestre. No disponible expresa ausencia de base o denominador válido; tiendas cuenta sucursales incluidas. Ordeno el ranking por rotación descendente y SKU ascendente para desempatar.

| canal | costo_disponible | registros |
| --- | --- | --- |
| fisico | False | 12349 |
| fisico | True | 74141 |
| online | False | 2988 |
| online | True | 6959 |

## cobertura_rotacion

Leyenda: muestro todas las filas sin índice; centavos son centésimas de MXN; crecimiento_pct es porcentaje y rotacion_veces son vueltas del semestre. No disponible expresa ausencia de base o denominador válido; tiendas cuenta sucursales incluidas. Ordeno el ranking por rotación descendente y SKU ascendente para desempatar.

| medida | valor |
| --- | --- |
| pares_observados | 1268 |
| pares_cobertura_completa | 36 |
| dias_exigidos | 182 |

## Conclusión

Obtengo cuatro respuestas reproducibles con cobertura explícita y excepciones conservadas. Interpreto los resultados como escenarios operativos sujetos a los límites de las fuentes.
