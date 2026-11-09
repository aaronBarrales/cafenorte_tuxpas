# Informes de análisis exploratorio

Los informes Markdown se pueden leer directamente en GitHub. Cada informe de resultados debe identificar fuente, versión, alcance, resultados, importancia, interpretación y limitaciones.

## Exploración aislada por fuente

| Fuente | Informe de resultados | Código | Estado |
|---|---|---|---|
| `sales.csv` | [Resultados de sales](resultados_sales.md) | [01_sales.ipynb](../../notebooks/01_sales.ipynb) | Verificado el 8 de noviembre de 2026; hash y alcance indicados en el informe. |
| `inventory.json` | [Resultados de inventory](resultados_inventory.md) | [03_inventory.ipynb](../../notebooks/03_inventory.ipynb) | Ejecutado el 9 de noviembre de 2026; alcance aislado, fuente y hash identificados. |
| `ecommerce_orders.parquet` | [Resultados de ecommerce](resultados_ecommerce.md) | [04_ecommerce.ipynb](../../notebooks/04_ecommerce.ipynb) | Ejecutado el 9 de noviembre de 2026; análisis aislado, huella y límites identificados. |
| `exchange_rates.csv` | [Resultados de exchange_rates](resultados_exchange_rates.md) | [02_exchange_rates.ipynb](../../notebooks/02_exchange_rates.ipynb) | Ejecutado el 8 de noviembre de 2026; aislado, fuente y hash identificados en el informe. |

**Aislado** significa que los resultados se obtienen únicamente de la fuente indicada, sin cruzarla con otros archivos de datos. No demuestra consistencia entre sistemas. La conciliación se documenta por separado cuando se realiza.

## Conciliación actual entre fuentes

Consulto [05_conjunto.ipynb](../../notebooks/05_conjunto.ipynb) y [resultados_conjunto.md](resultados_conjunto.md) para los conectores comprobados con las cuatro fuentes actuales: cardinalidad, cobertura referencial, ventanas, snapshots, costos vigentes y FX. No repito los perfiles individuales ni aplico equivalencias inferidas. El informe se regenera desde los mismos cálculos del notebook.

## Antecedentes y análisis entre fuentes

- [Perfil inicial de sales](../05_antecedentes/analisis_sales.md): conserva resultados de una versión anterior; no sustituye el informe actual.
- [Análisis previo de e-commerce](../05_antecedentes/analisis_ecommerce.md): esquema, cobertura de handles y exportación de consulta.
- [EDA integral previo](../05_antecedentes/EDA_COMPLETO.md): revisión de varias fuentes y sus cruces; su hash de sales difiere del actual.
- [Conciliación propuesta de handles](../05_antecedentes/conciliacion_handles.md): relaciones candidatas, no confirmadas.
- [Casos de margen](../05_antecedentes/casos_margen.md): cálculos condicionados a supuestos y a cruces entre fuentes.
- [Producto ERP-PROV-MX-057-C](../05_antecedentes/producto_ERP-PROV-MX-057-C.md): caso investigado con información de varias fuentes.
- [Guía de preguntas de negocio](../03_negocio/guia_preguntas_negocio.md): explicación de métricas, no resultados definitivos.

Los hallazgos importantes se resumen en [HALLAZGOS.md](../04_seguimiento/HALLAZGOS.md). La bitácora de IA está en [AI_LOG.md](../../AI_LOG.md).

## Conclusión

Tengo documentadas las cuatro exploraciones aisladas y la conciliación conjunta actual. Consulto los antecedentes por separado para no presentar sus cruces o versiones anteriores como resultados actuales.
