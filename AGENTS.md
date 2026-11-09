# Reglas del proyecto CaféNorte

Estas convenciones aplican a todos los archivos del proyecto. Antes de crear o mover archivos, consulta este documento y conserva mi trabajo existente.

## Ubicación de archivos

| Ubicación | Contenido |
|---|---|
| `datos/` | Fuentes originales. No sobrescribir ni corregir los archivos de entrada. Mantenerlos fuera de Git según `.gitignore`. |
| `notebooks/` | Exploración interactiva; un notebook por fuente. |
| `scripts/` | Perfiles reproducibles, exportaciones y validaciones ejecutables. |
| `outputs/` | Reportes, exportaciones y demás resultados generados; fuera de Git. |
| `docs/README.md` | Entrada principal a la documentación, ruta de lectura e inventario de documentos. |
| `docs/01_reto/` | Enunciado original, transcripción y requisitos de entrega. |
| `docs/02_exploracion/` | Informes de resultados actuales por fuente e índice de exploraciones. |
| `docs/03_negocio/` | Guías de métricas, definiciones, dudas, supuestos y preguntas al cliente. |
| `docs/04_seguimiento/` | Hallazgos resumidos, continuidad y plan de entrega. |
| `docs/05_antecedentes/` | Estudios previos y casos investigados, con vigencia y limitaciones explícitas. |
| Raíz | `README.md`, `AGENTS.md`, `AI_LOG.md`, dependencias y configuración del proyecto. |

No colocar nuevos análisis, notebooks o documentos de seguimiento en la raíz.

## Nuevos archivos y evolución de la estructura

1. Antes de crear cada archivo, clasificarlo y elegir su ubicación con la tabla anterior.
2. Si ya existe una regla que lo cubra, reutilizarla sin duplicarla por cada archivo.
3. Si aparece un tipo de archivo que todavía no encaja —por ejemplo, código del pipeline, consultas SQL o pruebas—, definir su carpeta y agregar aquí la regla correspondiente como parte del mismo cambio. No crear carpetas vacías para trabajo futuro.
4. Actualizar la estructura del `README.md` cuando cambien carpetas o convenciones. Añadir enlaces a los nuevos puntos de entrada relevantes.
5. Al mover archivos, actualizar referencias en documentación, notebooks y scripts; comprobar enlaces y rutas de ejecución afectados.
6. Separar fuentes, código y resultados. No duplicar un notebook para conservar versiones: usar Git. Mantener archivos temporales fuera de la estructura definitiva y retirarlos al finalizar.

## Notebooks de exploración

- Tomar `docs/02_exploracion/resultados_sales.md` como referencia de estructura y profundidad para nuevos informes aislados: alcance y versión, resultados calculados, interpretación, importancia y limitaciones; adaptar los controles a cada fuente.
- Aplicar la referencia de estructura como guía interna: no incluir en notebooks ni informes de exploración frases que indiquen que sigo el informe de sales u otra plantilla. En su lista de «Documentación relacionada», incluir únicamente resultados de la fuente y preguntas al cliente, según corresponda; omitir índice de exploraciones, DUDAS, HALLAZGOS, CONTINUIDAD y AI_LOG. Esta regla de navegación no elimina las referencias específicas a dudas o preguntas necesarias para interpretar un hallazgo.
- Vincular las dudas de cada exploración con los identificadores de `docs/03_negocio/PREGUNTAS_CLIENTE.md` y, cuando corresponda, con `DUDAS.md`. Reutilizar y ampliar preguntas existentes antes de duplicarlas; distinguir evidencia de hipótesis y no dar preguntas por enviadas o respondidas.
- Nombrar como `NN_fuente.ipynb`. Antes de crear o renombrar un notebook, revisar los archivos existentes en su carpeta de destino y comparar sus prefijos numéricos; asignar el siguiente número al mayor existente, con al menos dos dígitos y sin colisiones. No reservar números por fuente ni anticipar la numeración de notebooks pendientes. Al renumerar uno existente, excluirlo del cálculo y actualizar sus referencias sin modificar código, resultados ni contadores de ejecución. Actualmente: `01_sales.ipynb` y `02_exchange_rates.ipynb`.
- Mantener un estilo progresivo y legible: objetivo y granularidad, lectura, esquema, diccionario, calidad, cobertura temporal, distribuciones, hallazgos y pendientes.
- Agregar los controles específicos de cada fuente y explicar qué implican sus resultados.
- Por petición mía, usar un solo comentario en español por bloque de código importante, explicando su propósito o una decisión de tratamiento. No comentar cada línea ni repetir lo que expresa el código; esta convención sustituye la anterior y aplica a partir de ahora. Verificar que los cambios de comentarios no alteren la lógica.
- Calcular conteos y estadísticas con código; evitar cifras manuales que puedan quedar desactualizadas.
- Conservar los valores originales y separar columnas derivadas. Distinguir cero, nulo y ausencia de registro.
- Resolver rutas desde la raíz del proyecto o desde `notebooks/`; evitar rutas absolutas personales.
- Al modificar código, verificar las celdas afectadas y la ejecución secuencial cuando proceda. Regenerar salidas si se ejecuta; si no se logra ejecutar, comunicar la limitación y no presentar salidas antiguas como actuales.
- Distinguir observaciones, supuestos y reglas confirmadas. No presentar un diagnóstico exploratorio como respuesta definitiva del negocio.
- No incluir datos personales de clientes en salidas guardadas o informes.

## Documentación y continuidad

- Por petición mía, cerrar cada modificación importante con un commit descriptivo y un push al repositorio de GitHub después de validar el cambio. Revisar el estado de Git, conservar trabajo previo y no versionar fuentes, resultados excluidos ni temporales; informar si el push no se logra.

- Incorporar aquí las mejoras de método que vaya solicitando durante los análisis como convenciones reutilizables, sin duplicarlas por archivo. Registrar la aclaración y su aplicación en `AI_LOG.md`; no convertir observaciones particulares en reglas de negocio confirmadas.
- Cerrar cada Markdown propio del proyecto con una sección final `## Conclusión` de un párrafo breve, escrita desde mi perspectiva y centrada en lo que aporta el documento. No agregar contenido después de ella; al actualizar bitácoras o seguimiento, insertar las entradas antes de la conclusión y ajustar el cierre si hace falta. Conservar sin alteraciones el enunciado recibido y su transcripción literal.
- No incluir una sección «Reproducción y vigencia» en los informes de resultados. Mantener instrucciones de ejecución en el README y evidencia técnica de validación en AI_LOG; conservar la identificación de la fuente dentro del alcance del informe.
- Redactar los Markdown propios del proyecto y el texto explicativo de los notebooks en primera persona desde mi perspectiva. Usar «Hipótesis», «Pedí», «Revisé» o «Mi decisión» en lugar de referencias a mí en tercera persona. Conservar literalmente los documentos originales recibidos y los prompts citados.
- Distinguir mis solicitudes, hipótesis y correcciones de las acciones y validaciones ejecutadas por la IA; el cambio de voz no debe atribuirme pruebas manuales o aprobaciones que no he realizado.
- Registrar en `AI_LOG.md` cada avance y corrección del trabajo, indicando la propuesta inicial, mi aclaración cuando exista, el ajuste realizado y su evidencia. Respetar las indicaciones explícitas de excluir una conversación del registro.
- Usar `README.md` como punto de entrada y mantener sus instrucciones coherentes con los archivos existentes.
- Mantener breves los hallazgos en `docs/04_seguimiento/HALLAZGOS.md`; conservar el detalle de las exploraciones actuales en `docs/02_exploracion/`.
- Documentar los resultados de cada exploración por fuente en `docs/02_exploracion/resultados_<fuente>.md`, en Markdown legible en GitHub. Incluir identificación de la versión, resultados calculados, qué nos dicen, por qué importan y limitaciones; enlazar notebook y actualizar `docs/02_exploracion/README.md` y `docs/README.md`.
- Conservar cinco categorías numeradas por propósito; no volver a mezclar guías, seguimiento, resultados actuales y antecedentes. Solo agregar una categoría cuando exista contenido que la necesite.
- Al mover documentación, actualizar y comprobar también los enlaces relativos de las celdas Markdown de todos los notebooks; conservar intactos su código y resultados si el cambio es solo de navegación.
- Declarar expresamente cuándo un análisis es aislado y no consulta ni cruza otros archivos de datos. Separar esos resultados de las conciliaciones entre fuentes y distinguir informes actuales de antecedentes históricos.
- Actualizar `docs/04_seguimiento/CONTINUIDAD.md` al cambiar el estado del trabajo o detectar cambios relevantes en las fuentes.
- Registrar intervenciones relevantes de IA en `AI_LOG.md`, indicando validaciones y limitaciones sin atribuirme decisiones o validaciones que no he revisado.
- Ante una diferencia de hashes, documentarla; no modificar la fuente ni ocultar el cambio regenerando evidencia sin explicarlo.

## Redacción de la bitácora de IA

- Presentar `AI_LOG.md` como evidencia de mi criterio y de cómo dirijo el trabajo con IA. Abrir con mis intervenciones documentadas y su efecto; continuar con el flujo de herramientas, los prompts clave y las iteraciones verificables.
- En cada avance relevante, priorizar problema o intención, mi intervención concreta, propuesta recibida, tratamiento dado y evidencia del resultado. Usar aceptar, modificar o descartar solo cuando esa acción conste; si todavía no hay decisión, identificar la propuesta como pendiente.
- Describir la delegación técnica como apoyo para agilizar el trabajo, sin deducir falta de capacidad por utilizar IA ni afirmar habilidades que no se hayan demostrado. Explicar qué se delegó una vez por sección cuando resulte suficiente; conservar la atribución de autoría y validaciones relevantes sin repetirla en cada frase.
- Dar protagonismo a mis preguntas, hipótesis, detección de casos y correcciones reales. No atribuirme código, pruebas manuales, detección de errores o aprobaciones realizadas únicamente por la IA. Los casos de error deben identificar quién los detectó y corrigió.
- Mejorar claridad, ortografía y estructura en los resúmenes de intención. Conservar literalmente los prompts citados; cualquier reformulación debe rotularse «Intención de mi consulta (paráfrasis)» y mantener el sentido original. No presentar una versión editada como el prompt que escribí.
- Mantener concisos los incidentes operativos y ajustes editoriales; agrupar repeticiones sin perder evidencias, limitaciones materiales ni cambios de versión. Conservar los requisitos del reto: flujo de trabajo, tres a cinco prompts clave, respuesta resumida, tratamiento de propuestas, caso de error y autocrítica final.
- Centralizar pendientes comunes para evitar advertencias repetidas; conservar junto a cada resultado las condiciones específicas que afectan su interpretación. No presentar revisiones pendientes como aprobadas ni ocultar fallos relevantes para la entrega.
- Respetar las conversaciones excluidas del registro: no añadir sus prompts, evaluaciones personales ni una entrada sobre la conversación excluida. Aplicar los cambios de archivos expresamente solicitados sin reconstruirla en la bitácora.

## Conclusión

Mantengo una estructura por propósito, documentación en primera persona y trazabilidad de los cambios. Cierro cada documento propio con una conclusión breve y conservo separadas las observaciones, las hipótesis y las decisiones confirmadas.
