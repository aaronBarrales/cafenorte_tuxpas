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

## Entradas pendientes durante la implementación

- Ampliar las tres solicitudes registradas si nuevas decisiones justifican llegar hasta cinco prompts clave.
- Documentar decisiones de stack, conciliación, métricas y validación con evidencia.
- Registrar un caso concreto de propuesta incorrecta o subóptima de IA y la corrección realizada.
- Completar con el autor la autocrítica final: aportaciones propias, aportaciones de IA y comprobaciones de exactitud más allá de la ejecución sin errores.
