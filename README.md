# CaféNorte — Reto Data Solutions Engineer

Proyecto para integrar las ventas de tiendas físicas, las órdenes de e-commerce y el inventario de CaféNorte en un modelo analítico reproducible.

## Estado

Hallazgos clave resumidos en [HALLAZGOS.md](HALLAZGOS.md), actualizado conforme avance el análisis.

Para retomar el trabajo, leer primero [CONTINUIDAD.md](CONTINUIDAD.md): hallazgos, supuestos, cambios de fuentes y próximos pasos. Se actualizará al avanzar el proyecto.

Exploración de las cuatro fuentes ejecutada y documentada en [EDA completo](docs/EDA_COMPLETO.md), con [preguntas priorizadas](PREGUNTAS_CLIENTE.md) y [plan de entrega](PLAN_ENTREGA.md). Fecha límite: martes 10 de noviembre de 2026 antes de las 12:00 p. m., hora de Ciudad de México. El pipeline, sus pruebas y la propuesta técnica están pendientes de implementación.

Consulta [el análisis inicial de ventas](docs/analisis_sales.md) y [el registro de dudas y supuestos](DUDAS.md). Para reproducir el perfil sin dependencias externas, ejecuta `python scripts/perfil_sales.py` desde la raíz del proyecto.

## Alcance previsto

- Ingerir `sales.csv`, `inventory.json` y `ecommerce_orders.parquet`.
- Revisar `exchange_rates.csv` como fuente auxiliar para la conciliación de monedas.
- Documentar y aplicar reglas de normalización y conciliación.
- Persistir un modelo analítico y responder las cuatro preguntas de negocio.
- Incluir pruebas de calidad y validaciones de los resultados.
- Preparar una propuesta de arquitectura AWS con un presupuesto objetivo de USD 200 al mes.
- Registrar el uso de IA y las decisiones del autor en `AI_LOG.md`.

## Preguntas de negocio

1. Top 10 SKUs por rotación de inventario en los últimos seis meses.
2. Tiendas con quiebres de stock de más de tres días en el último trimestre.
3. Crecimiento mensual de ventas por canal en el último año.
4. Productos con margen negativo y las tiendas en las que ocurren.

Las definiciones de métricas, ventanas temporales y supuestos se documentarán después de explorar las fuentes.

## Archivos actuales

- [Candidatos de conciliación](docs/conciliacion_handles.md): evidencia para recuperar relaciones handle–ERP, sin aplicarlas automáticamente.
- [Análisis de e-commerce](docs/analisis_ecommerce.md): esquema, cobertura de handles y exportación CSV para Excel.
- [Casos de margen](docs/casos_margen.md): operaciones concretas para comprobar los cálculos.
- [DEFINICIONES.md](DEFINICIONES.md): conceptos de sistemas, importes, inventario y análisis.
- [Historial del producto ERP-PROV-MX-057-C](docs/producto_ERP-PROV-MX-057-C.md): costos, vigencias y equivalencia POS.
- `datos/README.md`: instrucciones para colocar los archivos originales.
- `AI_LOG.md`: registro del uso de IA durante el desarrollo.

Los datos originales se mantienen fuera del control de versiones mientras no se confirme que pueden redistribuirse. El notebook local `exploracion.ipynb` está vacío y no forma parte de esta entrega inicial.

## Ejecución

El pipeline sigue pendiente. Para leer y exportar e-commerce, consultar [los comandos de exploración](docs/analisis_ecommerce.md). El CSV de consulta se genera en `outputs/ecommerce_orders.csv` y permanece fuera de Git.

Para regenerar la exploración completa, después de instalar `requirements-exploracion.txt` en `.venv`:

```powershell
.\.venv\Scripts\python.exe scripts/eda_completo.py
```

El reporte detallado se guarda en `outputs/eda_completo.json`, sin modificar las fuentes. El perfilador de sales admite los dos formatos de fecha observados. Las reglas candidatas y limitaciones están documentadas en el plan; todavía no se aplican como decisiones confirmadas del cliente.

## Entregables pendientes

- [x] Exploración de datos y registro de dudas y supuestos propuestos.
- [ ] Elección y justificación del stack.
- [ ] Pipeline y modelo analítico.
- [ ] Respuestas de negocio y pruebas.
- [ ] Propuesta AWS con diagrama, costos, fases y riesgos.
- [ ] Instrucciones reproducibles para la demo.
- [ ] Revisión final de la bitácora de IA con el autor.
