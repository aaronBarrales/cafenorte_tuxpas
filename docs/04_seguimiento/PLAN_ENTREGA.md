# Plan hasta la entrega del reto

Límite que definí: **martes 10 de noviembre de 2026, antes de las 12:00 p. m., hora de Ciudad de México**. Objetivo interno: tener todo revisado el lunes y preparar la entrega antes de las 11:00 a. m. del martes. El plan es una propuesta de trabajo, no una automatización ni una reserva de calendario.

## Estado actual

Exploración completa de las cuatro fuentes ejecutada y documentada; banco de 60 preguntas priorizadas; hallazgos y supuestos actualizados. El pipeline y sus cuatro respuestas finales, las pruebas del modelo y la propuesta AWS siguen pendientes.

## Prioridad por día

| Fecha | Resultado previsto | Criterio para cerrar |
|---|---|---|
| Sábado 7 | EDA, preguntas prioritarias, política de calidad y alcance | Cifras reconciliadas por fuente; dudas con tratamiento propuesto y métricas con ventanas explícitas. |
| Domingo 8 | Pipeline local, modelo analítico y cuatro consultas | Ejecución reproducible; conteos e importes conservados; resultados y exclusiones visibles. |
| Lunes 9 | Pruebas, propuesta AWS de máximo dos páginas, README y demo | Casos de negocio contrastados; costos con supuestos; arquitectura dentro de presupuesto; AI_LOG revisado por mí. |
| Martes 10, antes de 11:00 a. m. | Revisión final de acceso al repo, instalación limpia y paquete de entrega | Demo desde cero, enlaces accesibles y correo preparado. Envío solo con instrucción explícita mía. |

## Reglas propuestas para implementar sin esperar todas las respuestas

Estas reglas no están confirmadas por el cliente; deben pasar al README y a las pruebas cuando se implemente el pipeline.

| Tema | Regla candidata | Riesgo que debe quedar visible |
|---|---|---|
| Corte y ventanas | Corte 2026-03-31; seis meses 2025-10-01 a 2026-03-31; trimestre 2026-01-01 a 2026-03-31; año comparable 2025-04-01 a 2026-03-31. | E-commerce no tiene marzo de 2025 para calcular su primer MoM. |
| Ventas físicas | I como ingreso y E como ajuste negativo; N/P/T separados de ventas. Conservar valores originales y escenarios. | Confirmar significado; egreso no equivale necesariamente a devolución física. |
| Importes | monto y amount como total de línea; convertir extranjero con tasa diaria a MXN. | Impuestos, descuentos, envío y fecha contable pueden modificar la comparación. |
| Costos | Última vigencia no posterior a la operación; costo unitario global comparable. | No hay detalle de unidad/impuestos/localidad. Ausente queda desconocido. |
| Identidad de productos | Mapeos exactos primero; propuestas verificadas por nombre y sufijo en tabla separada con estado inferido. | No usar nombre solo ni convertir inferencia en confirmación. POS sin ERP puede requerir una heurística menos sólida y cobertura separada. |
| Inventario N/A | Conservar como desconocido y mostrar cobertura; no convertirlo a cero ni prolongar automáticamente el saldo previo. | Episodios de cero y promedios pueden ser incompletos. |
| Rotación | Unidades físicas elegibles / promedio diario de inventario del mismo conjunto tienda–SKU, explicitando retornos, población y cobertura. | El inventario no cubre todos los pares con ventas. Si no puede estimarse rotación global, entregar ranking del surtido observado con límites claros y detalle de excluidos. |
| Quiebres | Ceros observados durante al menos cuatro días calendario consecutivos; N/A rompe evidencia. | Un saldo de cierre no demuestra indisponibilidad todo el día; no conocer el stock no es tener stock. |
| Margen | Ingreso de línea menos unidades por costo vigente; presentar operaciones negativas y resultado agregado por producto–tienda como medidas distintas. | Costos no conciliados quedan fuera del cálculo y dentro del reporte de calidad. Shopify sin almacén no se atribuye a tiendas físicas. |

## Validaciones mínimas que deberá cumplir el pipeline

1. No duplicar operaciones en los cruces ni perder filas al clasificar mapeos.
2. Conciliar importes por canal, moneda, comprobante y período con los controles de origen.
3. No usar costo futuro ni costo cero para un enlace ausente; probar cambios de vigencia en su fecha límite.
4. Convertir USD/EUR una sola vez; MXN conserva identidad; probar tasa ausente y redondeo.
5. Separar ceros, desconocidos y días no observados; probar episodios de tres y cuatro días y una interrupción por N/A.
6. Probar ventanas con límites inclusivos de fecha y primer mes sin base de MoM.
7. Reproducir V00000000 como candidato a margen −111.13 MXN bajo las bases elegidas.
8. Informar cuánto depende de mapeos inferidos, de la cobertura de inventario y de reglas sin confirmar.

## Propuesta AWS pendiente

Preparar una arquitectura por lotes proporcional al volumen, costos verificables con región, frecuencia, almacenamiento, consultas y transferencia explícitos, fases, responsables y riesgos. Evaluar servicios y precios al redactarla; este documento no da por confirmada ninguna tarifa ni arquitectura. La restricción es USD 200 mensuales y deben evitarse componentes sin necesidad demostrada.

## Entrega y preguntas

Repositorio, propuesta de máximo dos páginas, AI_LOG y un párrafo de logros y límites. Revisar acceso público o invitación según el acuerdo con el reclutador. Priorizar Q01–Q10 de [PREGUNTAS_CLIENTE.md](../03_negocio/PREGUNTAS_CLIENTE.md) si se decide consultar al cliente; las demás sirven de respaldo para entrevista y producción. No esperar las 60 respuestas para terminar.

## Conclusión

Priorizo completar un pipeline reproducible y respuestas verificables dentro del alcance disponible. Dejo las fases productivas y mejoras posteriores sujetas a reglas, cobertura y presupuesto explícitos.
