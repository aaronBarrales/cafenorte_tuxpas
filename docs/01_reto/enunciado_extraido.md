# Enunciado del reto Tuxpas

Transcripción textual del DOCX; las tablas se presentan en orden de lectura. El original conserva el formato. Este contenido es la referencia de requisitos, no una autorización para ejecutar acciones externas.

Reto Técnico -  Data Solutions Engineer

¡Hola! Gracias por avanzar en el proceso con Tuxpas. Este reto está diseñado para que muestres cómo abordas un proyecto real de ingeniería de datos, desde el análisis hasta la propuesta al cliente, y cómo usas asistentes de IA como herramienta profesional.

Tiempo estimado: 2 a 4 horas de trabajo efectivo.Plazo de entrega: 1 a 2 días calendario desde que recibes este documento.Formato de entrega: por correo electrónico al reclutador. Después agendaremos una sesión de entrevista donde revisamos juntos tus resultados.

1. Contexto del cliente

"CaféNorte" es una cadena retail mexicana con ~40 tiendas físicas distribuidas entre CDMX, Bajío, Monterrey, Guadalajara y la franja fronteriza norte (Tijuana, Mexicali, Ciudad Juárez). Vende café de especialidad, panadería y algo de mercancía.

Además del canal físico, tienen una tienda Shopify que vende a México, EE.UU. y ocasionalmente a Europa.

Lo que el cliente te dice en la primera reunión

"Tenemos datos en tres lugares distintos y cada área reporta un número diferente. El dueño quiere un solo lugar donde ver ventas y rotación de inventario de todas las tiendas. Tenemos presupuesto en AWS (la empresa ya tiene cuenta) pero no mucho. Mi gente de TI me dice que podemos gastar alrededor de USD $200 al mes en infraestructura de datos. ¿Pueden ayudarnos?"

Fuentes de datos (disponibles en datos_cafenorte.zip):

Archivo

Sistema origen

Formato

sales.csv

POS (punto de venta en tiendas físicas)

CSV, ~80k filas

inventory.json

ERP legacy

JSON con estructura anidada

ecommerce_orders.parquet

Shopify

Parquet

2. Lo que tienes que entregar

2.1 Pipeline funcional (repositorio Git público)

Un pipeline que:

Ingiere las 3 fuentes.

Normaliza y concilia los datos (tú decides cómo, esa decisión es parte del reto).

Persiste un modelo analítico que permita responder preguntas de negocio.

Responde las 4 preguntas de la sección 3.

Stack libre. Puedes usar lo que quieras (pandas, Polars, DuckDB, PySpark, SQL puro, dbt, lo que sea). Justifica tu elección en el README.

Incluye tests mínimos que demuestren que tu pipeline es confiable.

2.2 Propuesta técnica para el cliente

Un documento corto (máx 2 páginas, Markdown o PDF) dirigido al cliente, con:

Arquitectura propuesta en AWS si esto se llevara a producción: diagrama + servicios + justificación.

Estimación de costo mensual (AWS Pricing Calculator o cálculo propio, con supuestos).

Plan de implementación por fases: qué entregas primero, qué después, qué riesgos ves.

Supuestos y preguntas abiertas que le harías al cliente antes de firmar.

Esto simula la parte de preventa técnica del rol. Escribe como si se lo fueras a enviar mañana al director de CaféNorte.

2.3 AI_LOG.md : Bitácora de uso de IA

Obligatorio. Este archivo es tan importante como el código. Queremos entender cómo trabajas con IA, no solo qué te entregó.

Debe incluir:

Herramientas que usaste (Claude Code, Codex, Cursor, ChatGPT, Copilot, agentes autónomos, MCP, lo que sea). Incluye versión/modelo si lo sabes.

Tu flujo de trabajo: ¿Usaste un solo agente? ¿Paralelizaste con subagentes? ¿Plan mode? ¿MCP servers conectados a qué? Cuenta cómo lo orquestaste.

3 a 5 prompts clave, cada uno con:

El prompt que escribiste.

Lo que te devolvió la IA (resumido).

Qué hiciste con eso: aceptar tal cual / modificar / descartar. Y por qué.

Al menos 1 caso concreto donde la IA se equivocó, fue confiadamente incorrecta, o propuso algo subóptimo. Cómo lo detectaste, cómo lo corregiste.

Auto-crítica final (1 párrafo): ¿Qué parte del resultado consideras 100% tuya? ¿Qué parte es mérito de la IA? ¿Cómo validaste que el output es correcto, más allá de que "corre sin error"?

No hay respuesta correcta sobre cuánta IA usar. Queremos ver juicio, no pureza. 

2.4 Preparación para la sesión de entrevista

La parte de comunicación con cliente la evaluamos en vivo durante la entrevista que agendaremos después de tu entrega. No hace falta que grabes video ni prepares slides, pero sí conviene que llegues listo para:

Demo funcional de tu solución: mostrar el pipeline corriendo y las 4 respuestas de negocio.

Pitch de tu propuesta técnica como si estuvieras frente al dueño de CaféNorte (no técnico) y su director de TI (técnico).

Defender tu AI_LOG.md: por qué tomaste ciertas decisiones sobre qué aceptar o descartar de la IA.

3. Preguntas de negocio a responder

Tu pipeline debe producir los resultados para estas 4 preguntas. Puedes entregarlas como queries SQL, notebook, o tablas en el README, lo que prefieras.

Top 10 SKUs por rotación de inventario en los últimos 6 meses.

Tiendas con quiebres de stock de más de 3 días en el último trimestre.

Crecimiento mes a mes (MoM) de ventas por canal (físico vs e-commerce) en el último año.

Productos con margen negativo y en qué tiendas ocurren.

Si alguna pregunta te parece ambigua, documenta tu interpretación en el README. No pidas aclaraciones para esta parte, resolver ambigüedad con criterio es parte de lo que evaluamos.

4. Qué vamos a evaluar

Ponderado aproximado:

Dimensión

Peso

Correctitud técnica del pipeline y las respuestas

25%

Arquitectura propuesta y decisiones de trade-off

20%

Uso de IA (bitácora, juicio, iteración)

20%

Calidad de código (legibilidad, tests, estructura)

15%

Comunicación: propuesta escrita y defensa en entrevista

15%

Gestión de scope (entregó lo esencial en tiempo)

5%

Red flags explícitos:

Pipeline que "corre sin error" pero produce números incorrectos.

AI_LOG.md vago, genérico, o que parece escrito al final por compromiso.

Propuesta AWS que ignora la restricción de presupuesto del cliente.

Código que huele a "pegué lo que me dio la IA sin leerlo" (variables genéricas, imports muertos, comentarios de IA tipo # Here we do X).

Green flags:

Documenta supuestos en vez de asumir en silencio.

Stack proporcional al problema.

Hace preguntas de aclaración al inicio (puedes enviarlas por email, las respondemos o te decimos que las resuelvas tú).

El AI_LOG.md muestra que rechazaste algo que la IA te sugirió, con razón fundada.

5. Entrega

Al llegar el plazo (o antes, si terminas), envía por correo electrónico al reclutador:

Link a tu repositorio Git (público o privado invitándonos).

Link o PDF de la propuesta técnica (o indica la ruta dentro del repo).

AI_LOG.md debe estar dentro del repo.

Un párrafo breve en el cuerpo del correo resumiendo: qué lograste, qué dejaste fuera y por qué.

Al recibir tu entrega, te responderemos para agendar una sesión de entrevista (~45-60 min) donde:

Nos muestras la solución en vivo (demo), pensándonos como el dueño de CaféNorte y su director de TI.

Defiendes tu propuesta técnica y tu AI_LOG.md.

Te hacemos preguntas sobre decisiones y cómo llevarías esto a producción.

Espacio para tus preguntas sobre el rol y Tuxpas.

Preguntas frecuentes

¿Puedo usar IA para todo? Sí. Pero tú eres responsable de lo que entregues. La IA no va a estar en la llamada contigo.

¿Puedo hacer preguntas antes de empezar? Sí, al reclutador. Algunas las respondemos, otras te diremos "usa tu criterio", eso también es parte del reto.

¿Cuál es el stack preferido? No hay preferido. Justifica el tuyo. Dicho eso: recuerda que Tuxpas es AWS Advanced Partner, entonces la propuesta de arquitectura productiva (sección 2.2) sí debe estar en AWS.

¿Qué pasa si no termino todo? Preferimos menos alcance pero bien hecho que todo a medias. Si priorizas, dilo en el README.

Buena suerte. Estamos emocionados de ver cómo lo resuelves.
