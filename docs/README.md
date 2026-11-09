# Documentación de CaféNorte

Empieza aquí para encontrar los requisitos, los resultados y el estado del proyecto. Las carpetas siguen un orden de lectura; no representan fases terminadas.

## Ruta de lectura recomendada

1. [Guía de entrega](01_reto/guia_entrega.md): qué debemos entregar.
2. [Preguntas de negocio explicadas](03_negocio/guia_preguntas_negocio.md): qué significan las cuatro solicitudes.
3. [Resultados aislados de sales](02_exploracion/resultados_sales.md): qué sabemos de la fuente actual y qué no podemos concluir.
4. [Hallazgos importantes](04_seguimiento/HALLAZGOS.md): resumen del conocimiento acumulado, con su alcance y limitaciones.
5. [Continuidad](04_seguimiento/CONTINUIDAD.md) y [plan](04_seguimiento/PLAN_ENTREGA.md): dónde estamos y qué falta.

## Dónde está cada documento

### 01_reto — Qué nos pidieron

| Documento | Para qué leerlo |
|---|---|
| [Documento original](01_reto/TX%20Challenge%20Data%20Solutions%20Engineer.docx) | Consultar el enunciado recibido, conservado en su formato original. |
| [Transcripción del enunciado](01_reto/enunciado_extraido.md) | Leer y buscar los requisitos directamente en GitHub. |
| [Guía de entrega](01_reto/guia_entrega.md) | Identificar los entregables y cómo se evaluarán. |

### 02_exploracion — Qué nos dicen las fuentes actuales

| Documento | Para qué leerlo |
|---|---|
| [Índice de exploraciones](02_exploracion/README.md) | Ver qué fuentes ya tienen notebook e informe aislado y cuáles faltan. |
| [Resultados de sales](02_exploracion/resultados_sales.md) | Revisar resultados, importancia e interpretación del CSV actual, sin cruzarlo con otras fuentes. |
| [Resultados de exchange_rates](02_exploracion/resultados_exchange_rates.md) | Revisar calidad, cobertura, distribución y variaciones de tasas, sin cruces; dudas conectadas con Q10 y Q38–Q40. |
| [Resultados de inventory](02_exploracion/resultados_inventory.md) | Revisar estructura, cobertura, saldos, rachas observadas, equivalencias y costos del JSON aislado. |

Los notebooks ejecutables están en [notebooks/](../notebooks/README.md). Esta carpeta guarda los informes de resultados, no copias del código.

### 03_negocio — Cómo entendemos las preguntas y los datos

| Documento | Para qué leerlo |
|---|---|
| [Guía de preguntas de negocio](03_negocio/guia_preguntas_negocio.md) | Entender fórmulas, ejemplos y ambigüedades; no contiene respuestas finales. |
| [Definiciones](03_negocio/DEFINICIONES.md) | Consultar el vocabulario del proyecto. |
| [Dudas y supuestos](03_negocio/DUDAS.md) | Revisar incertidumbres, evidencia e impacto de interpretaciones propuestas. |
| [Preguntas para el cliente](03_negocio/PREGUNTAS_CLIENTE.md) | Consultar el banco priorizado de preguntas; no significa que se hayan enviado o respondido. |

### 04_seguimiento — Qué encontramos y qué falta

| Documento | Para qué leerlo |
|---|---|
| [Hallazgos](04_seguimiento/HALLAZGOS.md) | Ver conclusiones importantes de forma breve; cada entrada debe distinguir alcance y supuestos. |
| [Continuidad](04_seguimiento/CONTINUIDAD.md) | Retomar el trabajo con estado, cambios de fuentes y próximos pasos. |
| [Plan de entrega](04_seguimiento/PLAN_ENTREGA.md) | Consultar prioridades, fases y validaciones pendientes. |

La bitácora evaluable de IA se mantiene en la raíz: [AI_LOG.md](../AI_LOG.md).

### 05_antecedentes — Qué se investigó antes

Estos documentos conservan evidencia previa y propuestas entre fuentes. No son informes aislados actuales ni respuestas definitivas. Comprueba sus hashes, fechas y supuestos antes de reutilizar cifras. Que estén aquí no significa que todas sus observaciones se hayan descartado.

| Documento | Alcance y precaución |
|---|---|
| [Perfil inicial de sales](05_antecedentes/analisis_sales.md) | Versión anterior del CSV; conserva su hash original. |
| [Análisis previo de e-commerce](05_antecedentes/analisis_ecommerce.md) | Esquema y exportación; incluye revisión de mapeos entre fuentes. |
| [EDA integral previo](05_antecedentes/EDA_COMPLETO.md) | Revisa varias fuentes y cruces; el hash de sales difiere del actual. |
| [Propuesta de conciliación de handles](05_antecedentes/conciliacion_handles.md) | Enlaces inferidos, todavía sujetos a confirmación. |
| [Casos de margen](05_antecedentes/casos_margen.md) | Cálculos condicionados a costos, mapeos y reglas propuestas. |
| [Caso del producto ERP-PROV-MX-057-C](05_antecedentes/producto_ERP-PROV-MX-057-C.md) | Investigación de un producto concreto con información de varias fuentes. |

## Cómo mantener este orden

- Requisitos recibidos → `01_reto/`.
- Resultados de exploración por fuente → `02_exploracion/resultados_<fuente>.md`.
- Explicaciones de métricas, vocabulario y supuestos → `03_negocio/`.
- Hallazgos resumidos y estado del trabajo → `04_seguimiento/`.
- Estudios anteriores y casos ya investigados → `05_antecedentes/`, identificando su vigencia.

No crear documentos para fases todavía no implementadas. Cuando exista una nueva categoría de trabajo, definir su ubicación en [AGENTS.md](../AGENTS.md) y actualizar este índice y los enlaces afectados.

## Conclusión

Organizo la lectura desde los requisitos hasta los resultados y el seguimiento. Distingo los informes actuales de los antecedentes para consultar cada documento con su alcance y vigencia correspondientes.
