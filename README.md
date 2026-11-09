# CaféNorte — Reto Data Solutions Engineer

Proyecto para integrar las ventas de tiendas físicas, las órdenes de e-commerce y el inventario de CaféNorte en un modelo analítico reproducible.

## Base de conocimientos del reto

Empieza por el [índice de documentación](docs/README.md): incluye la ruta de lectura, el propósito de cada documento y la distinción entre resultados actuales y antecedentes.

El [documento original](docs/01_reto/TX%20Challenge%20Data%20Solutions%20Engineer.docx), su [transcripción consultable](docs/01_reto/enunciado_extraido.md) y la [guía de entregables](docs/01_reto/guia_entrega.md) están conservados en `docs/01_reto/`. El reto exige un pipeline funcional y una propuesta de arquitectura productiva en AWS; no exige desplegar la demo en AWS.

## Estado

Hallazgos clave resumidos en [HALLAZGOS.md](docs/04_seguimiento/HALLAZGOS.md), actualizado conforme avance el análisis.

Para retomar el trabajo, leer primero [CONTINUIDAD.md](docs/04_seguimiento/CONTINUIDAD.md): hallazgos, supuestos, cambios de fuentes y próximos pasos. Se actualizará al avanzar el proyecto.

Existe una exploración previa de las cuatro fuentes en el [EDA integral histórico](docs/05_antecedentes/EDA_COMPLETO.md); su hash de sales difiere del actual. Tengo completos los cuatro notebooks aislados de sales, exchange_rates, inventory y ecommerce; la conciliación actual entre fuentes sigue pendiente. Consulta las [preguntas priorizadas](docs/03_negocio/PREGUNTAS_CLIENTE.md) y el [plan de entrega](docs/04_seguimiento/PLAN_ENTREGA.md). Fecha límite: martes 10 de noviembre de 2026 antes de las 12:00 p. m., hora de Ciudad de México. El pipeline, sus pruebas y la propuesta técnica están pendientes de implementación.

Consulta los [resultados del análisis aislado de ventas](docs/02_exploracion/resultados_sales.md), el [índice de informes](docs/02_exploracion/README.md) y [el registro de dudas y supuestos](docs/03_negocio/DUDAS.md). El [análisis inicial de ventas](docs/05_antecedentes/analisis_sales.md) conserva el perfil histórico. Para reproducir el perfil sin dependencias externas, ejecuta `python scripts/perfil_sales.py` desde la raíz del proyecto.

## Alcance previsto

- Ingerir `sales.csv`, `inventory.json` y `ecommerce_orders.parquet`.
- Revisar `exchange_rates.csv` como fuente auxiliar para la conciliación de monedas.
- Documentar y aplicar reglas de normalización y conciliación.
- Persistir un modelo analítico y responder las cuatro preguntas de negocio.
- Incluir pruebas de calidad y validaciones de los resultados.
- Preparar una propuesta de arquitectura AWS con un presupuesto objetivo de USD 200 al mes.
- Registrar el uso de IA y mis decisiones en `AI_LOG.md`.

## Preguntas de negocio

Consulta [la guía desde cero de las cuatro preguntas](docs/03_negocio/guia_preguntas_negocio.md): significado, fórmulas, ejemplos y decisiones necesarias para calcularlas.

1. Top 10 SKUs por rotación de inventario en los últimos seis meses.
2. Tiendas con quiebres de stock de más de tres días en el último trimestre.
3. Crecimiento mensual de ventas por canal en el último año.
4. Productos con margen negativo y las tiendas en las que ocurren.

Las definiciones de métricas, ventanas temporales y supuestos se documentarán después de explorar las fuentes.

## Archivos actuales

- [Candidatos de conciliación](docs/05_antecedentes/conciliacion_handles.md): evidencia para recuperar relaciones handle–ERP, sin aplicarlas automáticamente.
- [Análisis de e-commerce](docs/05_antecedentes/analisis_ecommerce.md): esquema, cobertura de handles y exportación CSV para Excel.
- [Casos de margen](docs/05_antecedentes/casos_margen.md): operaciones concretas para comprobar los cálculos.
- [DEFINICIONES.md](docs/03_negocio/DEFINICIONES.md): conceptos de sistemas, importes, inventario y análisis.
- [Historial del producto ERP-PROV-MX-057-C](docs/05_antecedentes/producto_ERP-PROV-MX-057-C.md): costos, vigencias y equivalencia POS.
- `datos/README.md`: instrucciones para colocar los archivos originales.
- `AI_LOG.md`: registro del uso de IA durante el desarrollo.

Los datos originales se mantienen fuera del control de versiones mientras no se confirme que pueden redistribuirse. La exploración interactiva de ventas está en [notebooks/01_sales.ipynb](notebooks/01_sales.ipynb).

## Organización del proyecto

Las convenciones para crear, ubicar y mover archivos están en [AGENTS.md](AGENTS.md). Si aparece un tipo de archivo nuevo, su regla de ubicación debe incorporarse allí como parte del mismo cambio.

La [convención de la bitácora de IA](AGENTS.md#redacción-de-la-bitácora-de-ia) organiza [AI_LOG.md](AI_LOG.md) por mis intervenciones, el trabajo delegado y la evidencia de resultados. Las citas de prompts se conservan literalmente y las reformulaciones se identifican como paráfrasis.

```text
datos/                  Fuentes originales; no se modifican ni se versionan.
notebooks/              Exploración interactiva, un notebook por fuente.
  01_sales.ipynb         Estructura, calidad y cobertura de ventas físicas.
  02_exchange_rates.ipynb Calidad, cobertura y variaciones de tipos de cambio.
  03_inventory.ipynb     Saldos, cobertura, rachas, equivalencias y costos.
  04_ecommerce.ipynb     Pedidos registrados, monedas, cobertura y privacidad.
scripts/                Perfiles reproducibles, exportaciones y validaciones.
outputs/                Reportes y exportaciones generados; fuera de Git.
docs/
  README.md             Índice general y recorrido de lectura.
  01_reto/              Enunciado original y requisitos de entrega.
  02_exploracion/       Resultados actuales por fuente.
  03_negocio/           Métricas, definiciones, dudas y preguntas.
  04_seguimiento/       Hallazgos, continuidad y plan de entrega.
  05_antecedentes/      Estudios anteriores y casos investigados.
README.md               Entrada al proyecto e instrucciones de ejecución.
AGENTS.md               Reglas de organización y mantenimiento.
AI_LOG.md               Bitácora de uso de IA requerida por el reto.
```

Primero revisa el [índice de documentación](docs/README.md) y los notebooks para conocer las fuentes. Los resultados actuales están en `docs/02_exploracion/`, los supuestos en `docs/03_negocio/` y el estado en `docs/04_seguimiento/`. El pipeline se incorporará cuando empecemos su implementación.

Para preparar el entorno de exploración:

```powershell
python -m pip install -r requirements-exploracion.txt
python -m jupyter lab
```

Selecciona como kernel el mismo entorno donde instalaste las dependencias. Los notebooks de sales, exchange_rates, inventory y ecommerce admiten ejecución desde la raíz o desde `notebooks/` y conservan las columnas originales. Uso el entorno donde instalé las dependencias; `.venv` puede no tenerlas instaladas todavía. Para ejecutar y guardar las salidas de tasas desde la raíz:

```powershell
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/02_exchange_rates.ipynb
```

Consulto [los resultados de exchange_rates](docs/02_exploracion/resultados_exchange_rates.md) y [los resultados de inventory](docs/02_exploracion/resultados_inventory.md) para interpretación y límites de cada análisis aislado. Para ejecutar inventario y actualizar sus salidas desde la raíz:

```powershell
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/03_inventory.ipynb
```

El notebook de inventario requiere pandas, NumPy e IPython, disponibles al instalar las dependencias de exploración. No requiere tabulate ni lee las demás fuentes. El informe identifica la versión analizada; si cambia el JSON, debo ejecutar de nuevo y actualizar el informe, sus preguntas y el seguimiento con los resultados calculados.

## Ejecución

El pipeline sigue pendiente. Para leer y exportar e-commerce, consultar [los comandos de exploración](docs/05_antecedentes/analisis_ecommerce.md). El CSV de consulta se genera en `outputs/ecommerce_orders.csv` y permanece fuera de Git.

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
- [ ] Mi revisión final de la bitácora de IA.

## Exploración aislada de ecommerce

Consulto [04_ecommerce.ipynb](notebooks/04_ecommerce.ipynb) y [su informe](docs/02_exploracion/resultados_ecommerce.md) para revisar estructura, calidad, granularidad, calendario, distribuciones por moneda y señales IQR. Solo lee ecommerce_orders.parquet, conserva originales y guarda agregados sin datos personales. Requiere pandas, NumPy, PyArrow e IPython del entorno de exploración; no requiere tabulate ni matplotlib.

Para ejecutar de principio a fin y guardar salidas con un kernel preparado:

```powershell
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/04_ecommerce.ipynb
```

Si cambia la fuente, debo documentar la diferencia de huella, ejecutar de nuevo y actualizar el informe, las preguntas y el seguimiento con tablas calculadas. Los importes se conservan por moneda; no representan ingresos netos confirmados.

## Conclusión

Tengo completos los cuatro notebooks e informes aislados. Mi siguiente paso es conciliar las fuentes y construir el pipeline, dejando explícitas las reglas y limitaciones de las cuatro respuestas de negocio.
