# Guía de entregables del reto CaféNorte

Revisión del 7 de noviembre de 2026 basada en el documento original conservado en esta carpeta. Esta guía explica requisitos; no constituye la propuesta final para el cliente ni afirma que el pipeline esté terminado.

## Alcance de AWS

El enunciado pide una arquitectura propuesta en AWS «si esto se llevara a producción». No exige desplegar infraestructura real para entregar el reto. El pipeline puede ejecutarse localmente: el stack es libre y debe justificarse en el README. Debe funcionar, persistir un modelo analítico y producir resultados comprobables.

La demo local y la propuesta productiva deben distinguirse y guardar coherencia: explicar qué componentes se trasladarían a AWS y qué cambios requerirían. La cuenta AWS mencionada pertenece al cliente ficticio; el documento no proporciona acceso ni solicita crear una cuenta personal.

## Lo que se envía

- Repositorio Git accesible al evaluador con pipeline, instrucciones, justificación del stack, pruebas mínimas y las cuatro respuestas de negocio.
- Propuesta técnica para el cliente de máximo dos páginas, Markdown o PDF: arquitectura AWS, diagrama, servicios y justificación; costo mensual con supuestos; fases, riesgos y preguntas abiertas.
- AI_LOG.md dentro del repositorio.
- Correo al reclutador con enlaces o PDF y un párrafo sobre lo logrado, lo excluido y el motivo. Enviar el correo requiere una instrucción explícita mía; esta guía no lo envía.

La sección 2.1 dice repositorio público, pero la sección 5 admite público o privado invitando al evaluador. Asegurar que pueda acceder; no afirmar que solo se admite público.

## Cómo interpretar cada sección consultada

### Arquitectura AWS

Entregar un diagrama del recorrido de datos y explicar dónde se guardan los originales, dónde se procesa el pipeline, dónde persiste el modelo y cómo se consultan los resultados. Indicar también ejecución programada, permisos, monitoreo y tratamiento de fallos. Cada servicio elegido debe tener una función y una razón proporcional al volumen y al presupuesto. Diseñar esto no equivale a desplegarlo.

### Estimación mensual

Presentar una tabla por servicio y un total, usando AWS Pricing Calculator o cálculo propio. Indicar región, moneda, volumen almacenado, frecuencia y duración del procesamiento, consultas y datos leídos, retención, transferencias y cualquier costo fijo o licencia relevante. Explicar exclusiones. Contrastar el total con el presupuesto objetivo de aproximadamente USD 200 al mes. Verificar precios vigentes al elaborar la propuesta; esta guía no incluye una cotización ni una arquitectura elegida. La implementación y el mantenimiento humano se distinguen del gasto mensual de infraestructura.

### Fases y riesgos

Ejemplo de secuencia, pendiente de adoptar en la propuesta: primero acordar reglas y validar fuentes; después entregar pipeline, modelo y cuatro respuestas; luego desplegar y programar en AWS; finalmente agregar operación, alertas y mejoras. Para cada fase, concretar una entrega y una forma de aceptarla. Riesgos ya observados: comprobantes ambiguos, mapeos incompletos, bases de costo y cambios de formato de fechas. Incluir mitigación y decisiones pendientes.

### Supuestos y preguntas abiertas

Separar lo que se asume para resolver el reto de lo que se confirmaría antes de comprometer una solución productiva. Ejemplos: significado de comprobantes y montos, impuestos, costo unitario, devoluciones, cobertura de inventario, moneda, responsable de mapeos, frecuencia de actualización, accesos, retención, seguridad y presupuesto. DUDAS.md contiene la evidencia detallada.

Para las preguntas de negocio, el enunciado pide resolver la ambigüedad con criterio y documentar la interpretación en el README. No condicionar la entrega a que el cliente responda las preguntas abiertas.

### Demo funcional

Durante la entrevista, ejecutar el pipeline desde las fuentes, mostrar el modelo persistido, sus cuatro resultados y las comprobaciones de calidad. Explicar casos excluidos o inciertos y sus efectos. Un comando que termina sin error no demuestra cifras correctas. El enunciado no pide URL pública, video ni slides.

Las cuatro salidas son: top 10 SKUs por rotación en seis meses; tiendas con quiebres mayores a tres días en el último trimestre; crecimiento mensual por canal en el último año; productos con margen negativo y sus tiendas. Documentar las ventanas y definiciones empleadas.

### Pitch

Preparar una explicación oral de la misma propuesta para dos audiencias. Para el dueño: qué problema resuelve, qué decisiones habilita, costo, etapas y limitaciones. Para TI: fuentes, modelo, reglas de calidad, servicios AWS, permisos, monitoreo y alternativas descartadas. La entrevista evalúa esta comunicación; no exige presentación grabada ni diapositivas.

### Defensa de AI_LOG.md

Explicar decisiones reales con evidencia: qué pedí, qué sugirió la IA, qué se aceptó, modificó o descartó y por qué. El archivo debe incluir herramientas y modelo si se conoce, flujo de trabajo, entre tres y cinco prompts clave, al menos un error o sugerencia subóptima y su corrección, y una autocrítica final sobre aportes y validación. No inventar decisiones, errores ni mi aceptación para cumplir el requisito. Los seguimientos actuales deben condensarse en una versión final clara y revisada por mí.

## Estado y preparación pendiente

El repositorio ya contiene exploración, dudas y bitácora. Según el estado documentado al iniciar esta revisión, faltan el pipeline final, el modelo, las cuatro respuestas, las pruebas y la propuesta AWS. Esta revisión conserva el enunciado y aclara el alcance; no verifica ni completa esos entregables.

## Conclusión

Entiendo la entrega como un pipeline funcional con cuatro respuestas comprobables, una propuesta productiva en AWS y una bitácora de IA. Mi prioridad es completar esos entregables y preparar su explicación con evidencia; la propuesta de arquitectura no exige un despliegue real.
