# Bitácora de uso de IA

Este archivo se actualiza durante el trabajo. Las respuestas y acciones de la IA se registran como hechos observados; las valoraciones personales del autor quedan pendientes hasta que él las revise.

## Herramientas y flujo de trabajo

- Asistente: Codex en la aplicación de escritorio. No se ha verificado el identificador exacto del modelo.
- Un solo agente; sin subagentes hasta esta etapa.
- Trabajo en conversación normal, sin activar modo de planificación.
- Herramientas utilizadas: PowerShell y Git para inspección local; lectura de OOXML del documento del reto; búsqueda web de documentación de GitHub; edición de archivos del proyecto.
- Se consultó el catálogo del conector de GitHub. Hasta esta entrada no se han ejecutado operaciones de ese conector contra el repositorio.
- No se utilizaron Notion, Gmail ni otros servicios conectados para este trabajo.

## 2026-11-07 — Preparación del repositorio

### Solicitud 1 — Organización de avances

**Prompt del usuario:** «Dentro de la carpeta del proyecto encontrarás las instrucciones del proyecto, el proyecto dice que debemos hacer un repositorio en github, recomiendas ir subiendo información al repositorio poco a poco?»

**Respuesta de la IA:** recomendó commits por avances coherentes, mantener esta bitácora desde el inicio y trabajar inicialmente en privado. Identificó que el documento solicita un repositorio público en una sección y permite uno privado con acceso para los evaluadores en la sección de entrega.

**Acción observada:** el usuario aceptó continuar con la creación del repositorio. La visibilidad efectiva del repositorio remoto no se ha verificado.

### Solicitud 2 — Creación en GitHub

**Prompt del usuario:** «Perfecto, entonces vamos a generar el repositorio, dame el paso a paso para generarlo».

**Respuesta de la IA:** indicó crear un repositorio privado y vacío, sin README, licencia ni `.gitignore` remotos, para conectar la carpeta local.

**Acción observada:** el usuario compartió `https://github.com/aaronBarrales/cafenorte_tuxpas.git`. La IA preparó un README, este registro y un `.gitignore` que excluye los datos originales, credenciales y archivos generados. El usuario eligió un nombre diferente al sugerido por la IA.

### Incidente técnico observado

La primera lectura del documento mediante `ZipFile.OpenRead` falló porque el archivo estaba abierto en otro proceso. La IA detectó el error en la salida de PowerShell y utilizó un flujo de lectura con `FileShare.ReadWrite`, con el que pudo extraer el contenido. Esto registra una corrección operativa; aún está pendiente documentar un caso de juicio técnico sobre el pipeline o sus resultados.

## 2026-11-07 — Exploración inicial de sales

### Solicitud 3 — Análisis y registro de dudas

**Prompt del usuario:** «Perfecto entonces continuemos, que más hace falta para seguir avanzando con el analisis del archivo "sales", además, quiero que tengamos un archivo en el cuál se escriban las dudas que se tengan, es decir, la primer pregunta es que representa la columna tipo_comprobante en el archivo sales».

**Respuesta y trabajo de la IA:** creó `DUDAS.md`, un script de perfil sin dependencias externas y `docs/analisis_sales.md`. Inspeccionó 86,490 registros y separó las sumas por código y moneda. Contrastó las letras con una referencia del SAT sin afirmar que ese catálogo sea el diccionario del POS.

**Validación observada:** ejecutó el script sobre la fuente original. Encontró cinco tipos de comprobante con montos y cantidades positivos, ningún campo vacío, ningún ID repetido y ningún duplicado exacto. Registró un hash del archivo para identificar la versión analizada. Esto valida aspectos estructurales y descriptivos, no la exactitud de las métricas de negocio.

**Decisiones implementadas por la IA, pendientes de revisión del autor:** conservar importes originales, no presentar las sumas como ventas netas y dejar explícitas las dudas sobre comprobantes, monto, granularidad, zona horaria y corte temporal. No se ha recibido aún aceptación de estas interpretaciones por parte del autor.

**Herramientas adicionales:** se consultó la guía de spreadsheets y el localizador de dependencias de Codex; el perfil se ejecutó con el Python proporcionado por ese entorno. La búsqueda web se utilizó para contrastar los tipos de CFDI con documentación del SAT.

### Solicitud 4 — Origen del precio y diferencias por SKU

**Prompt del usuario:** «Hay algo que me causa especial curiosidad, de donde sale el precio que se muestra, ya que al filtrar por sku se puede ver que un mismo sku tiene diferentes precios a lo largo del tiempo pero ninguno de los archivos entregados tiene esa información».

**Trabajo de la IA:** verificó las cuatro filas de la captura en la fuente, calculó los cocientes de monto y cantidad y revisó también registros tipo `I` del mismo SKU. Encontró historial de costos y catálogo de zonas horarias dentro del JSON. Registró D006 y evidencia adicional de D004. No atribuyó las variaciones a promociones ni reconstruyó precios sin evidencia.

**Error detectado y corrección:** la IA intentó importar `pyarrow` sin verificar su disponibilidad y la ejecución falló antes de leer las fuentes. Repitió el análisis de CSV y JSON con biblioteca estándar, dejando explícitamente pendiente la lectura del esquema Parquet. No presentó esa revisión parcial como inspección completa de todas las fuentes.

**Decisión pendiente del autor:** confirmar o adoptar como supuesto la interpretación de monto total de línea y la metodología de margen con costo vigente. Las diferencias entre tiendas y fechas impiden atribuir la variación solo al tiempo con los ejemplos de la captura.

### Solicitud 5 — Historial del producto y definiciones

**Prompt del usuario:** «Puedes investigar en el inventario el historial de precio de este producto por favor? ERP-PROV-MX-057-C Entonces el POS es el punto de venta de cada tienda física y el erp guarda los precios en la "nube"? por asi decirlo? Puedes generar un md de definiciones importantes?».

**Trabajo de la IA:** consultó el catálogo y los mapeos originales; encontró un producto llamado Premium Cafe Grano, relacionado con `CN-00057`, y cinco entradas de costo. Revisó las claves del catálogo y del historial, que no contienen precio de venta. Creó el historial documentado y `DEFINICIONES.md`, y registró D007 sobre unidades y vigencia de costos.

**Distinción explicada:** un ERP describe funciones empresariales y no implica alojamiento en la nube. La metadata no revela cómo se alojan el ERP ni el POS actuales. Los costos del inventario no equivalen a los precios cobrados por el POS.

**Validación y estado:** se extrajeron los valores de la fuente sin modificarlos y se comprobó que la clave devuelve una entrada de producto y un mapeo. Las reglas de costo vigente y costo unitario son propuestas pendientes de revisión del autor, no respuestas confirmadas del cliente.

### Seguimiento del autor y archivo de continuidad

El autor contrastó la venta `V00009357` (dos unidades y monto 385.79 MXN) con el costo vigente propuesto de 85.94 MXN para el producto 057. La IA explicó la diferencia entre costo e importe de venta y dejó los cálculos de margen condicionados a verificar las bases. A petición del autor se creó `CONTINUIDAD.md` para mantener hallazgos, dudas, estado y siguientes pasos al retomar.

La revisión posterior recorrió las claves completas del JSON y no encontró lista de precios de venta. No se generalizó esa ausencia a Parquet, cuyo esquema sigue pendiente. Se detectó un cambio de hash y formato de fechas en sales respecto al perfil original, se registró sin atribuir autoría y se preservó el archivo. El perfilador señaló incompatibilidad de formato para todas las fechas actuales; queda pendiente decidir cómo tratar esa versión.

Una lectura independiente con el formato día/mes/año y hora:minuto interpretó todas las fechas actuales sin errores. Esto diferencia una incompatibilidad del parser de fechas incorrectas y no prueba que los demás campos permanezcan intactos.

## Entradas pendientes durante la implementación

### Seguimiento de mapeos incompletos

El autor identificó `handle: null` en `ERP-PROV-MX-015-D` y propuso que handle fuera la descripción. La IA contrastó el concepto con documentación oficial de Shopify: el handle es un identificador utilizado en la URL, distinto del título y la descripción. Verificó que el producto sí tiene nombre, Especial Cafe Molido, y mapeo POS–ERP válido informado en la fuente.

Se contaron 65 registros de mapeo, 38 sin handle y 27 con handle; no se encontraron duplicados entre valores no nulos por campo. Se documentó el caso adicional de CN-00016 sin SKU ERP. No se concluyó que los productos sin handle no se vendan online: esa hipótesis sigue pendiente de contrastar con Parquet. Se actualizaron glosario, dudas y continuidad; aún no se implementaron reglas de conciliación.

- Revisar con el autor las cinco solicitudes clave registradas y actualizar sus decisiones al implementar el pipeline.
- Documentar decisiones de stack, conciliación, métricas y validación con evidencia.
- Registrar un caso concreto de propuesta incorrecta o subóptima de IA y la corrección realizada.
- Completar con el autor la autocrítica final: aportaciones propias, aportaciones de IA y comprobaciones de exactitud más allá de la ejecución sin errores.
