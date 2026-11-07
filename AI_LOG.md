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

## Entradas pendientes durante la implementación

- Registrar los siguientes prompts clave hasta contar con entre tres y cinco.
- Documentar decisiones de stack, conciliación, métricas y validación con evidencia.
- Registrar un caso concreto de propuesta incorrecta o subóptima de IA y la corrección realizada.
- Completar con el autor la autocrítica final: aportaciones propias, aportaciones de IA y comprobaciones de exactitud más allá de la ejecución sin errores.
