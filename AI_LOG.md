# Bitácora de uso de IA

Mantengo esta bitácora durante el trabajo. Distingo mis solicitudes y aclaraciones de las acciones realizadas por la IA. Las validaciones automatizadas quedan documentadas; mis valoraciones personales pendientes de revisión no se presentan como decisiones ya tomadas.

## Herramientas y flujo de trabajo

- Asistente: Codex en la aplicación de escritorio. No se ha verificado el identificador exacto del modelo.
- Un solo agente; sin subagentes hasta esta etapa.
- Trabajo en conversación normal, sin activar modo de planificación.
- Herramientas utilizadas: PowerShell y Git para inspección local; lectura de OOXML del documento del reto; búsqueda web de documentación de GitHub; edición de archivos del proyecto.
- Se consultó el catálogo del conector de GitHub. Hasta esta entrada no se han ejecutado operaciones de ese conector contra el repositorio.
- No se utilizaron Notion, Gmail ni otros servicios conectados para este trabajo.

## 2026-11-07 — Preparación del repositorio

### Solicitud 1 — Organización de avances

**Mi prompt:** «Dentro de la carpeta del proyecto encontrarás las instrucciones del proyecto, el proyecto dice que debemos hacer un repositorio en github, recomiendas ir subiendo información al repositorio poco a poco?»

**Respuesta de la IA:** recomendó commits por avances coherentes, mantener esta bitácora desde el inicio y trabajar inicialmente en privado. Identificó que el documento solicita un repositorio público en una sección y permite uno privado con acceso para los evaluadores en la sección de entrega.

**Acción observada:** acepté continuar con la creación del repositorio. La visibilidad efectiva del repositorio remoto no se ha verificado.

### Solicitud 2 — Creación en GitHub

**Mi prompt:** «Perfecto, entonces vamos a generar el repositorio, dame el paso a paso para generarlo».

**Respuesta de la IA:** indicó crear un repositorio privado y vacío, sin README, licencia ni `.gitignore` remotos, para conectar la carpeta local.

**Acción observada:** compartí `https://github.com/aaronBarrales/cafenorte_tuxpas.git`. La IA preparó un README, este registro y un `.gitignore` que excluye los datos originales, credenciales y archivos generados. Elegí un nombre diferente al sugerido por la IA.

### Incidente técnico observado

La primera lectura del documento mediante `ZipFile.OpenRead` falló porque el archivo estaba abierto en otro proceso. La IA detectó el error en la salida de PowerShell y utilizó un flujo de lectura con `FileShare.ReadWrite`, con el que pudo extraer el contenido. Esto registra una corrección operativa; aún está pendiente documentar un caso de juicio técnico sobre el pipeline o sus resultados.

## 2026-11-07 — Exploración inicial de sales

### Solicitud 3 — Análisis y registro de dudas

**Mi prompt:** «Perfecto entonces continuemos, que más hace falta para seguir avanzando con el analisis del archivo "sales", además, quiero que tengamos un archivo en el cuál se escriban las dudas que se tengan, es decir, la primer pregunta es que representa la columna tipo_comprobante en el archivo sales».

**Respuesta y trabajo de la IA:** creó `docs/03_negocio/DUDAS.md`, un script de perfil sin dependencias externas y `docs/05_antecedentes/analisis_sales.md`. Inspeccionó 86,490 registros y separó las sumas por código y moneda. Contrastó las letras con una referencia del SAT sin afirmar que ese catálogo sea el diccionario del POS.

**Validación observada:** ejecutó el script sobre la fuente original. Encontró cinco tipos de comprobante con montos y cantidades positivos, ningún campo vacío, ningún ID repetido y ningún duplicado exacto. Registró un hash del archivo para identificar la versión analizada. Esto valida aspectos estructurales y descriptivos, no la exactitud de las métricas de negocio.

**Decisiones implementadas por la IA, pendientes de mi revisión:** conservar importes originales, no presentar las sumas como ventas netas y dejar explícitas las dudas sobre comprobantes, monto, granularidad, zona horaria y corte temporal. Aún no he confirmado la aceptación de estas interpretaciones.

**Herramientas adicionales:** se consultó la guía de spreadsheets y el localizador de dependencias de Codex; el perfil se ejecutó con el Python proporcionado por ese entorno. La búsqueda web se utilizó para contrastar los tipos de CFDI con documentación del SAT.

### Solicitud 4 — Origen del precio y diferencias por SKU

**Mi prompt:** «Hay algo que me causa especial curiosidad, de donde sale el precio que se muestra, ya que al filtrar por sku se puede ver que un mismo sku tiene diferentes precios a lo largo del tiempo pero ninguno de los archivos entregados tiene esa información».

**Trabajo de la IA:** verificó las cuatro filas de la captura en la fuente, calculó los cocientes de monto y cantidad y revisó también registros tipo `I` del mismo SKU. Encontró historial de costos y catálogo de zonas horarias dentro del JSON. Registró D006 y evidencia adicional de D004. No atribuyó las variaciones a promociones ni reconstruyó precios sin evidencia.

**Error detectado y corrección:** la IA intentó importar `pyarrow` sin verificar su disponibilidad y la ejecución falló antes de leer las fuentes. Repitió el análisis de CSV y JSON con biblioteca estándar, dejando explícitamente pendiente la lectura del esquema Parquet. No presentó esa revisión parcial como inspección completa de todas las fuentes.

**Mi decisión pendiente:** confirmar o adoptar como supuesto la interpretación de monto total de línea y la metodología de margen con costo vigente. Las diferencias entre tiendas y fechas impiden atribuir la variación solo al tiempo con los ejemplos de la captura.

### Solicitud 5 — Historial del producto y definiciones

**Mi prompt:** «Puedes investigar en el inventario el historial de precio de este producto por favor? ERP-PROV-MX-057-C Entonces el POS es el punto de venta de cada tienda física y el erp guarda los precios en la "nube"? por asi decirlo? Puedes generar un md de definiciones importantes?».

**Trabajo de la IA:** consultó el catálogo y los mapeos originales; encontró un producto llamado Premium Cafe Grano, relacionado con `CN-00057`, y cinco entradas de costo. Revisó las claves del catálogo y del historial, que no contienen precio de venta. Creó el historial documentado y `docs/03_negocio/DEFINICIONES.md`, y registró D007 sobre unidades y vigencia de costos.

**Distinción explicada:** un ERP describe funciones empresariales y no implica alojamiento en la nube. La metadata no revela cómo se alojan el ERP ni el POS actuales. Los costos del inventario no equivalen a los precios cobrados por el POS.

**Validación y estado:** se extrajeron los valores de la fuente sin modificarlos y se comprobó que la clave devuelve una entrada de producto y un mapeo. Las reglas de costo vigente y costo unitario son propuestas pendientes de mi revisión, no respuestas confirmadas del cliente.

### Mi seguimiento y archivo de continuidad

Contrasté la venta `V00009357` (dos unidades y monto 385.79 MXN) con el costo vigente propuesto de 85.94 MXN para el producto 057. La IA explicó la diferencia entre costo e importe de venta y dejó los cálculos de margen condicionados a verificar las bases. A petición mía se creó `docs/04_seguimiento/CONTINUIDAD.md` para mantener hallazgos, dudas, estado y siguientes pasos al retomar.

La revisión posterior recorrió las claves completas del JSON y no encontró lista de precios de venta. No se generalizó esa ausencia a Parquet, cuyo esquema sigue pendiente. Se detectó un cambio de hash y formato de fechas en sales respecto al perfil original, se registró sin atribuir autoría y se preservó el archivo. El perfilador señaló incompatibilidad de formato para todas las fechas actuales; queda pendiente decidir cómo tratar esa versión.

Una lectura independiente con el formato día/mes/año y hora:minuto interpretó todas las fechas actuales sin errores. Esto diferencia una incompatibilidad del parser de fechas incorrectas y no prueba que los demás campos permanezcan intactos.

### Seguimiento de mapeos incompletos

Identifiqué `handle: null` en `ERP-PROV-MX-015-D` y propuse que handle fuera la descripción. La IA contrastó el concepto con documentación oficial de Shopify: el handle es un identificador utilizado en la URL, distinto del título y la descripción. Verificó que el producto sí tiene nombre, Especial Cafe Molido, y mapeo POS–ERP válido informado en la fuente.

Se contaron 65 registros de mapeo, 38 sin handle y 27 con handle; no se encontraron duplicados entre valores no nulos por campo. Se documentó el caso adicional de CN-00016 sin SKU ERP. No se concluyó que los productos sin handle no se vendan online: esa hipótesis sigue pendiente de contrastar con Parquet. Se actualizaron glosario, dudas y continuidad; aún no se implementaron reglas de conciliación.

### Seguimiento de Parquet y caso de margen negativo

Pedí comprobar si los handles ausentes podían tratarse como productos sin ventas online y convertir el Parquet a CSV. Durante el trabajo identifiqué V00000000 como venta por debajo del costo. La IA verificó esa operación y la fecha de vigencia del costo: margen candidato de −111.13 MXN para una unidad de CN-00015 en T033, sujeto a bases comparables y reglas de comprobantes.

Para leer Parquet, se creó un entorno local aislado y se instaló PyArrow 26.0.1. La creación del entorno falló inicialmente bajo las restricciones de ejecución; se completó con permisos adicionales. Pip encontró un error de certificados, resuelto usando truststore sin desactivar la validación HTTPS. El esquema tiene 11 columnas, con información de clientes, pero sin SKU alternativos ni listas de precios. Los datos exportados permanecen locales y excluidos de Git.

La IA generó un script de exportación y comprobó la serialización de las 9,947 filas y todas sus columnas, además del hash del original. El CSV no conserva tipos ni la distinción entre null y cadena vacía; se documentó su uso como copia de consulta.

La conciliación exacta encontró 33 handles, 27 con mapeo (8,098 filas) y 6 sin mapeo (1,849 filas). Cuatro tienen sufijos compatibles con SKU sin handle; no se transformó esta coincidencia en una clave confirmada. Se mantuvo el supuesto «sin handle = sin venta online» sin adoptar, y se registraron los candidatos y las verificaciones pendientes. Las cinco solicitudes clave anteriores se conservan; estos seguimientos documentan evidencia adicional.

## Entradas pendientes durante la implementación

### Guía de las cuatro preguntas de negocio

Pedí explicar y documentar desde cero las cuatro solicitudes, con ejemplos. La IA creó `docs/03_negocio/guia_preguntas_negocio.md` y la enlazó desde README, glosario y continuidad. Explicó SKU, rotación en unidades y en valor, quiebres consecutivos por tienda y producto, MoM por canal y margen bruto negativo por operación o acumulado. Incluyó ventanas ilustrativas, divisiones con base cero, cobertura faltante y el mes previo necesario para el primer MoM.

Los ejemplos son ficticios y están identificados; el único caso local citado remite a `docs/05_antecedentes/casos_margen.md` y conserva sus condiciones pendientes. Se revisó coherencia de fórmulas y ejemplos. No se modificaron fuentes ni scripts, no se ejecutaron métricas y no se registraron supuestos como confirmados por mí.

### Consulta sobre entregables y alcance de AWS

Pedí conservar el documento del reto en la base de conocimientos y explicar arquitectura AWS, costos, fases, supuestos, demo, pitch y defensa de IA. La IA leyó el DOCX completo, conservó una copia idéntica verificada por SHA-256 y una transcripción en `docs/reto/`, y preparó una guía. Contrastó las secciones 2.1, 2.2, 2.4 y 5: se pide pipeline funcional con stack libre y propuesta AWS para producción; no se exige desplegarlo en AWS. También identificó que la entrega admite repositorio privado con invitación, aunque 2.1 menciona público. No creó infraestructura, envió correos ni registró como aceptadas decisiones técnicas pendientes. Esta consulta es seguimiento adicional; quedan pendientes la selección de tres a cinco prompts clave y mi autocrítica final.

### Seguimiento de recuperación de relaciones handle y ERP

Pregunté cómo intentar relacionar los handles ausentes. La IA comparó nombre normalizado y segmento numérico del SKU ERP y encontró un candidato único para cada uno de los seis handles. Los nombres solos resultaron ambiguos en cinco casos. Se añadió un script reproducible y una propuesta documentada, sin alterar las fuentes ni aplicar los enlaces.

Al validar la regla, el conteo inicial de controles dio 23 coincidencias sobre 27 handles informados. La inspección de los cuatro restantes mostró SKU ERP nulos, no contradicciones: se corrigió el denominador a 23 controles completos y se registraron los cuatro mapeos incompletos por separado. Esto también reveló que reconocer un handle no garantiza que su cadena de conciliación llegue hasta el costo ERP. La regla observada se presenta como supuesto candidato, no como confirmación del cliente.

### Exploración completa y preparación de preguntas

Pedí completar el análisis exploratorio y reunir preguntas para plantear una solución. Confirmé por consulta asíncrona la entrega antes del martes a las 12:00 p. m.; se registró el martes 10 de noviembre de 2026, hora de Ciudad de México, según el calendario de la sesión.

La IA creó `scripts/eda_completo.py` y perfiló todas las filas de las cuatro fuentes. Detectó 4,417 existencias N/A; 12,687 filas I del semestre con ERP conocido sin snapshot; 12,349 filas POS y 2,988 online sin enlace exacto hasta ERP; y tasas diarias completas. Documentó cobertura, controles, escenarios de comprobantes, margen candidato y episodios de cero. Las cifras financieras no se presentan como respuestas definitivas.

Se actualizaron parser de sales, hallazgos, dudas y continuidad. Se crearon un banco de 60 preguntas con diez prioritarias y un plan hasta la entrega. No se enviaron mensajes al cliente ni se exigieron todas las respuestas; las ambigüedades de métricas se resolverán con supuestos documentados conforme al reto.

**Caso concreto de código subóptimo de la IA:** una ampliación recalculaba min/max de 230,776 fechas de stock dentro del bucle de cada venta. La IA detectó la repetición, interrumpió la ejecución y calculó los límites una sola vez fuera del bucle. La ejecución corregida produjo el reporte y pasó seis controles. No se aceptó el código solo por ser sintácticamente válido. Aún no he evaluado personalmente esta corrección; no la presento como una decisión mía ya revisada.

**Validación y límites:** controles por comprobante, mes, moneda, mapeo y clave de stock; muestras de N/A y costos iniciales contrastadas con origen. Esto no sustituye cierres contables externos ni las pruebas del pipeline pendiente. Se preservaron documentos añadidos en paralelo en la carpeta compartida.

También se agregó `scripts/validar_eda.py` con diez comprobaciones de hashes, controles de origen, tratamiento de N/A, episodios por ventanas de claves cero como método independiente, cobertura, compatibilidad y rechazo de fechas, caso de margen y unicidad de 60 preguntas. Las diez pasaron. La versión actual de sales volvió a perfilarse con cero fechas no interpretables.

- Revisar mis cinco solicitudes clave registradas y actualizar mis decisiones al implementar el pipeline.
- Documentar decisiones de stack, conciliación, métricas y validación con evidencia.
- Registrar un caso concreto de propuesta incorrecta o subóptima de IA y la corrección realizada.
- Completar mi autocrítica final: aportaciones propias, aportaciones de IA y comprobaciones de exactitud más allá de la ejecución sin errores.

### 8 de noviembre de 2026: organización y notebook de ventas

Pedí revisar el notebook guardado y dar más sentido a la estructura del proyecto. La IA movió el notebook a `notebooks/01_sales.ipynb`, los informes a `docs/analisis/` y los documentos de seguimiento a `docs/proyecto/`; actualizó enlaces y la ruta del banco de preguntas en el validador. Conservó las fuentes y los scripts existentes.

Amplió mi base inicial con controles de duplicados, vacíos, cobertura, fechas, cantidades, monedas, comprobantes e importe efectivo por SKU. Sustituyó el diccionario con cifras manuales por descripciones y un resumen calculado, aclaró que la semántica de comprobantes es una hipótesis y eliminó una salida antigua de error. Las salidas se regeneraron ejecutando las 13 celdas de código secuencialmente con Python y guardando resultados; se comprobaron rutas desde la raíz y desde notebooks/. El arranque de kernel con nbclient no terminó y se interrumpió; no se atribuye a esa vía la validación. El notebook cumple el esquema nbformat y no tiene salidas de error.

El validador previo pasó nueve controles y falló en la igualdad de hashes: sales.csv difiere del reporte histórico; las otras tres fuentes coinciden. Conteo e importe original de sales coinciden, lo que no demuestra igualdad del contenido. No se modificó la fuente ni se regeneró el reporte histórico para ocultar esta diferencia. No se usaron subagentes. Todavía tengo pendiente revisar los cambios.

### Reglas persistentes y revisión del notebook

Por solicitud mía se creó `AGENTS.md` en la raíz con las ubicaciones de archivos, convenciones de notebooks y obligación de ampliar las reglas cuando aparezca un tipo de archivo sin ubicación definida. Se enlazó desde README. Se volvió a leer `notebooks/01_sales.ipynb` para identificar pendientes; esta revisión no cambió sus celdas.

### Ampliación y formato de fecha de sales — 8 de noviembre de 2026

Pedí incorporar los pendientes al notebook y registrar hallazgos importantes en HALLAZGOS. Se agregaron identificación por hash/tamaño, controles de formatos y dominios, conversión numérica antes de operar, números finitos, cantidades enteras, distribución por tienda/SKU, calendario mensual completo con importes desconocidos para meses ausentes, IQR por moneda/SKU, dos gráficas SVG y conclusiones calculadas. Se actualizaron docs/04_seguimiento/HALLAZGOS.md y continuidad.

Después, pedí conservar solo la conversión DD/MM/YYYY HH:MM bajo la variable fecha. Se retiraron la conversión ISO y fecha_alternativa. Las 19 celdas se ejecutaron secuencialmente con IPython en proceso y salidas regeneradas; cero fechas inválidas, conteos conciliados por tienda/SKU/mes, calendario completo, dos SVG y hash de fuente sin cambios durante la ejecución. Las gráficas se integraron como SVG porque matplotlib no estaba instalado y su instalación falló por conectividad; no se añadió dependencia. No se usó un kernel externo ni se desplegó nada.

### 8 de noviembre de 2026 — Informes del EDA aislado y comentarios para colegas

**Mis solicitudes:** «Perfecto, dentro de docs puedes crear archivos con los resultados del análisis exploratorio, marcando por que son importantes y que nos están diciendo de los datos, aclara de igual forma que este análisis exploratorio se hizo de forma aislada sin tomar en cuenta el resto de archivos, utiliza formato markdown por favor, o un formato que sea legible después en github, recuerda ir tomando nota de esto de igual forma en el AI_LOG, ya que también lo evaluarán». Después pedí: «De igual forma comenta cada línea de código en español por favor, actúa como un ingeniero de datos profesional, pensando en que esto será entregado y que colegas pueden leerlo de igual forma».

**Trabajo de la IA:** creó docs/02_exploracion/resultados_sales.md con identificación del CSV, esquema, controles, cobertura, estadísticas, comprobantes, principales tiendas y SKU, evolución mensual, IQR e interpretación de gráficas. Cada sección explica resultados, importancia y límites. Declaró que el análisis usa exclusivamente sales.csv y no valida relaciones con inventario, costos, e-commerce o FX. Creó docs/02_exploracion/README.md como índice, enlazó el informe desde los README y distinguió el perfil inicial de la versión actual. Comentó en español cada línea no vacía de código del notebook, preservando mis cambios previos. Agregó estas convenciones a AGENTS.md y resumió los hallazgos relevantes en HALLAZGOS.md.

**Validación:** comparó los árboles sintácticos antes y después de comentar para comprobar que solo cambió la explicación, ejecutó las 19 celdas secuencialmente con IPython en proceso y regeneró las salidas. Concilió conteos por tienda, SKU y mes con el CSV; contrastó la suma total de montos con Decimal (30,947,253.82 MXN como control, no venta neta) y comprobó que SHA-256 no cambiara durante el trabajo. No leyó las otras fuentes de datos para generar los resultados aislados. Validó formato nbformat y enlaces locales. No se usaron subagentes, consultas externas ni publicación en GitHub.

**Corrección de documentación:** el perfil histórico todavía describía el EDA integral previo como correspondiente a la versión actual. La IA retiró esa afirmación y enlazó el informe identificado con el hash actual, sin borrar los resultados históricos ni alterar las fuentes.

**Decisiones y límites:** se implementaron el formato Markdown, alcance aislado y comentarios en español que solicité. Las interpretaciones comerciales permanecen como supuestos: sin reglas confirmadas de comprobantes, monto y granularidad no se presentan ingresos netos ni márgenes. Mi revisión y valoración personal de la entrega sigue pendiente; esta entrada no presupone que ya aprobé los resultados. Los informes de las siguientes fuentes se crearán al explorar sus respectivos notebooks.

### 8 de noviembre de 2026 — Orden documental y navegación desde el notebook

**Mis prompts:** «Puedes organizar de mejor forma la carpeta de Docs?, no siento que haya un orden entendible». Durante el trabajo añadí: «De igual forma ajusta los enlaces para que en el código ipynb se pueda llegar a los archivos por favor».

**Problema y decisión de la IA:** la clasificación anterior mezclaba exploraciones actuales, guías de métricas, estudios anteriores y seguimiento. Se reorganizaron 18 archivos por propósito en cinco carpetas numeradas: docs/01_reto, docs/02_exploracion, docs/03_negocio, docs/04_seguimiento y docs/05_antecedentes. Se conservó todo el contenido y se retiraron únicamente los directorios anteriores que quedaron vacíos. Se creó docs/README.md con recorrido de lectura, inventario y explicación de cada documento. Los antecedentes se presentan como evidencia previa cuya vigencia debe comprobarse, no como información descartada.

**Navegación y reglas:** se actualizaron los enlaces relativos en Markdown y notebooks, referencias de rutas y la ubicación del banco de preguntas en scripts/validar_eda.py. Se agregó al inicio del notebook un bloque de enlaces hacia índice, resultados, HALLAZGOS, dudas, definiciones, guía de negocio y AI_LOG. Se actualizaron README, AGENTS y continuidad para mantener la misma organización al crear archivos futuros.

**Validación:** se comprobaron 110 enlaces locales, incluidas celdas Markdown del notebook, el esquema nbformat, la sintaxis de las celdas ejecutables y la ruta de preguntas usada por el validador. Se verificó que los textos de código, las salidas y los contadores de ejecución del notebook no cambiaron al agregar navegación; no fue necesario repetir el análisis de datos. El hash de sales sigue coincidiendo con el informe de resultados. No se ejecutó el validador histórico completo, cuyo desajuste de hash de sales ya está registrado. No se publicaron cambios ni se usaron subagentes. Todavía tengo pendiente revisar el nuevo orden; no se presupone mi aprobación.

### 8 de noviembre de 2026 — Unicidad de venta_id y coincidencias de posibles líneas de compra

**Mis solicitudes:** pedí explicar por qué un venta_id único no confirma un ticket, comprobar si hay varias filas con igual fecha_hora y tienda pero distintos productos, documentarlo en el notebook e informe y llevar la duda al cliente. También pregunté por la utilidad de valores distintos de monto y cantidad en el resumen de esquema.

**Trabajo realizado:** se incorporó una sección comentada en español al notebook con revisión por venta_id, tienda-fecha y tienda-fecha-moneda-comprobante; incluye conteos y ejemplos verificables. Se encontraron 201 grupos de misma tienda y fecha/hora con varios SKU (402 filas) y 186 grupos con moneda y comprobante iguales (372 filas). Se añadieron resultados e interpretación a resultados_sales.md, HALLAZGOS y D003. Se amplió Q11, que ya preguntaba por granularidad, con evidencia y solicitud de ticket_id, línea, caja y precisión temporal; se mantuvo el banco de 60 preguntas sin duplicar la misma duda. Ninguna pregunta fue enviada al cliente.

**Juicio y límites:** mi propuesta es una hipótesis compatible con las coincidencias; no se confirmó mismo cliente ni ticket. La hora solo tiene precisión de minutos y distintas cajas/clientes pueden coincidir. No se fusionaron registros, no se reconstruyeron tickets con una clave artificial y no se consultaron otras fuentes. Sobre el resumen de esquema, la IA explicó que nunique se aplicó uniformemente: es útil para identificadores y categorías, secundario para cantidad y de utilidad limitada por sí solo para monto. Se conservó esa tabla porque pedí una explicación, no su modificación.

**Validación:** 20 celdas ejecutadas secuencialmente, salidas regeneradas, conteos por tienda/SKU/mes conciliados y coincidencias tienda-fecha contrastadas con Counter como método independiente. Hash de sales intacto durante la ejecución. Notebook válido y nueva sección con comentarios en español. Mi revisión de las conclusiones permanece pendiente.

### Mis aclaraciones durante la revisión de sales

| Propuesta o estado inicial | Mi intervención | Ajuste y evidencia |
|---|---|---|
| El lector de fechas admitía dos formatos observados previamente. | Pedí conservar únicamente el formato de la fuente actual, DD/MM/YYYY HH:MM, y usar la variable fecha. | La IA retiró la conversión alternativa; la ejecución interpretó las 86,490 fechas sin errores. |
| El informe advertía que venta_id único no garantiza un ticket, sin una revisión específica de coincidencias. | Planteé que una compra con varios productos podía estar dividida en filas y pedí comprobar coincidencias por tienda y fecha/hora. | La IA encontró 201 grupos con varios SKU, mostró ejemplos y amplió Q11. Mantengo la hipótesis pendiente de confirmar con la clave real del ticket. |
| El resumen aplicaba valores distintos a todas las columnas. | Cuestioné qué aportaba mostrar ese conteo para monto y cantidad. | La IA explicó que es secundario para esas medidas frente a distribución, percentiles y extremos. La tabla no se modificó porque mi solicitud era explicar su utilidad. |
| La primera organización documental seguía mezclando propósitos y dificultaba la lectura. | Pedí un orden más entendible y enlaces desde el notebook. | La IA separó cinco categorías, creó un índice de lectura y verificó los enlaces, conservando código y salidas. |
| La redacción hablaba de mí como «el autor», incluso al describir mi hipótesis. | Pedí una voz en primera persona y mantener registradas mis aclaraciones. | La IA ajustó la documentación y dejó «Hipótesis» en el informe, conservando la atribución de las acciones técnicas y las revisiones pendientes. |

### 8 de noviembre de 2026 — Corrección de voz editorial

Pedí que los Markdown del proyecto se redactaran desde mi perspectiva y que las correcciones quedaran registradas durante el trabajo. La IA revisó README, reglas, informes, dudas, seguimiento y entradas previas de esta bitácora para sustituir referencias a mí en tercera persona. Conservó literalmente los prompts citados y el enunciado recibido; también mantuvo diferenciadas mis solicitudes y las validaciones que ejecutó la IA.

La corrección incluyó el texto explicativo y un comentario del notebook. Se comparó su árbol sintáctico y se comprobó que código ejecutable, resultados y contadores no cambiaran; no se repitió el análisis porque el cambio fue editorial. Las nuevas reglas de redacción y registro quedaron en AGENTS.md. No se incorporaron aprobaciones, confirmaciones del cliente ni validaciones personales que no consten en el trabajo.

### 8 de noviembre de 2026 — Comprobación del número de tiendas

Pedí verificar si el notebook ya contaba las tiendas y no agregar nada al análisis si existía. La IA comprobó que sales["tienda_id"].nunique() aparece en Fechas y cobertura y en el resumen de conclusiones, con salida guardada de 40 tiendas distintas. No modificó el notebook ni el informe; esta revisión solo verificó contenido existente.

### 8 de noviembre de 2026 — Cierre breve de los documentos

Pedí retirar «Reproducción y vigencia» del informe de sales y cerrar cada Markdown con una conclusión breve. La IA eliminó el bloque indicado, que mezclaba instrucciones de ejecución, comprobaciones técnicas y referencias históricas con los resultados. Las instrucciones siguen disponibles en README y la evidencia de ejecución permanece en esta bitácora; el informe conserva al inicio el hash y el alcance aislado.

La IA añadió conclusiones específicas a los Markdown propios del proyecto y guardó la convención en AGENTS.md, incluida la obligación de insertar nuevas entradas antes del cierre en bitácoras y seguimiento. Conservó sin cambios el enunciado recibido y su transcripción literal. El ajuste fue documental: no modificó código, resultados del notebook ni fuentes de datos. Verificó el cierre de los documentos y la existencia de los destinos de los enlaces locales.

### 8 de noviembre de 2026 — Comentarios por bloque

**Mi aclaración:** pedí sustituir los comentarios línea por línea por un solo comentario por bloque de código importante, y aplicar ese criterio de ahora en adelante.

**Ajuste realizado por la IA:** redujo los comentarios de `notebooks/01_sales.ipynb` de 231 a 35, centrados en lectura, validaciones, agrupaciones, reglas estadísticas y gráficas. Conservó el español y las explicaciones de las decisiones de tratamiento sin repetir cada operación. Actualizó AGENTS.md para sustituir expresamente la convención anterior.

**Comprobación:** comparó los árboles sintácticos de las 20 celdas de código antes y después; la lógica ejecutable es idéntica. Conservó salidas, contadores de ejecución y celdas Markdown y validó el formato del notebook. No repitió la ejecución ni modificó las fuentes o resultados porque el cambio afecta únicamente comentarios y separación visual.

### 8 de noviembre de 2026 — EDA aislado de exchange_rates y reglas de mejora

**Mi solicitud inicial:** pedí explorar exchange_rates, crear un informe Markdown y comentar el código en español. Aclaré que quería un comentario por bloque importante, un análisis aislado basado en resultados_sales.md, dudas conectadas con el archivo de preguntas y estas mejoras guardadas como reglas. Precisé las ubicaciones: notebook numerado en notebooks/ e informes en docs/. También pedí commit y push a GitHub con cada modificación importante y pregunté por el propósito de outputs/.

**Ajuste realizado por la IA:** creó notebooks/04_exchange_rates.ipynb y docs/02_exploracion/resultados_exchange_rates.md. Conservó la regla ya actualizada de comentarios por bloque e incorporó a AGENTS la referencia documental, conexión de dudas, mejora continua y cierre mediante commit/push. Amplió Q10 y Q38–Q40, conservando 60 preguntas y enlazando D013/D023; ninguna pregunta fue enviada o respondida. Actualizó índices, README, HALLAZGOS y CONTINUIDAD. Explicó que outputs/ conserva resultados generados fuera de Git y que los auxiliares temporales de este trabajo se retiran al finalizar.

**Resultados y alcance:** analizó exclusivamente exchange_rates.csv: 730 filas, 365 días por USD/EUR entre 2025-04-01 y 2026-03-31, sin claves duplicadas ni huecos internos; tasas finitas y positivas. EUR = 22.0 en 63 fechas (17.26%), con racha máxima de 6 días. El criterio 1.5×IQR señala 11 tasas EUR y 32 USD; son señales descriptivas, sin corrección ni eliminación y sin validar mercado. El SHA-256 a0e827ec1e048cf397584eca3d692cb5b5b1f6b477fb78efca2fdbd2f488bddf coincide con el antecedente. No leyó ni cruzó las otras fuentes de datos ni consultó tasas externas.

**Validación técnica ejecutada por la IA:** 10 celdas ejecutadas secuencialmente y 22 salidas guardadas, formato nbformat válido y código compilable. La IA repitió la secuencia desde notebooks/ y comprobó ambas rutas de ejecución; contrastó con csv, Counter, datetime y Decimal los recuentos, calendario, positividad y racha de EUR, y verificó conservación de columnas originales y hash. Comprobó enlaces locales y anclas, las 60 preguntas únicas y los cierres Markdown. La primera comprobación de IDs esperaba Q1 en vez de Q01: se corrigió el validador temporal, sin alterar IDs del proyecto. La tabla del índice general se ajustó para mantener la nueva fila dentro de su tabla.

**Entorno y limitaciones:** .venv no tiene pandas; se usó Python 3.12 disponible con pandas 2.2.3, nbformat e IPython. El arranque de kernel de nbclient no se completó en este entorno y Jupyter intentó configurar una ruta restringida; se canceló y se ejecutaron las celdas directamente con IPython y captura de salidas, sin simular resultados ni presentar salidas anteriores como actuales. La captura usa configuración temporal en outputs/. Las salidas guardadas corresponden a esa ejecución directa, no a un kernel Jupyter iniciado por nbclient. Mi revisión y la semántica contable siguen pendientes.

**Control de versiones:** pedí publicar los cambios importantes. El árbol de trabajo ya contenía la reorganización de documentos, reglas y exploración de sales sin commit; la IA los conservó y preparó un cierre coherente con este avance, manteniendo excluidos datos originales, outputs y temporales. La confirmación del push se informa al terminar; no doy por publicado un intento sin comprobar el remoto.

## Conclusión

Registro mis solicitudes y aclaraciones junto con las acciones y comprobaciones realizadas por la IA. Mantengo identificadas las decisiones y revisiones pendientes para explicar cómo evolucionó el trabajo sin atribuirme validaciones que no he realizado.
