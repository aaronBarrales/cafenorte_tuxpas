# Entrega final y preparación de entrevista

## Lo que envío al reclutador

1. Repositorio público: [aaronBarrales/cafenorte_tuxpas](https://github.com/aaronBarrales/cafenorte_tuxpas). El acceso anónimo se comprueba después de publicar el cierre.
2. Propuesta técnica: adjunto `outputs/entrega/Propuesta_CafeNorte_Aaron_Barrales.pdf`, de exactamente dos páginas. La [versión Markdown](../03_negocio/PROPUESTA_TECNICA.md) queda en el repositorio.
3. Bitácora: [AI_LOG.md](../../AI_LOG.md), dentro del repositorio; no necesito adjuntarla por separado.
4. Cuatro respuestas: [RESPUESTAS_NEGOCIO.md](../03_negocio/RESPUESTAS_NEGOCIO.md), dentro del repositorio.
5. Resumen en el correo: uso el texto preparado más abajo.

Como respaldo opcional adjunto `outputs/entrega/CafeNorte_Aaron_Barrales.zip`: código y documentación versionada, sin originales, bases locales, entorno, credenciales ni datos personales. El ZIP no sustituye el enlace al repositorio. No necesito enviar video, diapositivas ni desplegar AWS; la demo y la defensa son en entrevista.

## Matriz de cumplimiento del reto

Leyenda: relaciono cada requisito con evidencia entregable. La validación es automatizada por la IA; no equivale a revisión personal ni certificación contable.

| Requisito | Evidencia | Estado y alcance |
|---|---|---|
| Ingerir tres fuentes | [ETL](../../scripts/pipeline.py) | CSV POS, JSON ERP y Parquet Shopify, más FX auxiliar |
| Normalizar y conciliar | [Modelo y reglas](../03_negocio/MODELO_ETL.md) | Equivalencias exactas, moneda, costo temporal y excepciones conservadas |
| Persistir modelo | outputs/etl/modelo.sqlite | Hechos, dimensiones, claves verificadas y nueve tablas de resultados |
| Responder cuatro preguntas | [Respuestas](../03_negocio/RESPUESTAS_NEGOCIO.md) | Ranking parcial, episodios y tiendas, MoM y dos vistas de margen |
| Justificar stack y ambigüedades | [README](../../README.md) | pandas, SQLite, ventanas, signos y límites explícitos |
| Tests mínimos | [Diez tests](../../scripts/test_pipeline.py) | Límites numéricos y temporales, sin depender de los datos privados |
| Correctitud más allá de ejecución | [Contraste independiente](../../scripts/validar_entrega.py) | Cuatro métricas, costos, conservación, hashes y privacidad |
| Propuesta AWS de máximo dos páginas | PDF adjunto y [Markdown](../03_negocio/PROPUESTA_TECNICA.md) | Dos páginas verificadas; diagrama, servicios, fases, riesgos y acuerdos |
| Presupuesto aproximado USD 200 | Presupuesto de la propuesta | Escenario USD 75 mensuales, sin free tier y con USD 40 de contingencia |
| Bitácora de IA | [AI_LOG](../../AI_LOG.md) | Herramientas, flujo, cinco prompts iniciales, iteraciones, errores y autocrítica |
| Repositorio público | Enlace anterior | Publicado con mi autorización expresa |
| Correo y preparación | Este documento | Mensaje listo; envío a cargo mío, sin darlo por realizado |

## Correo listo para enviar

**Asunto:** Entrega challenge Data Solutions Engineer — Aaron Barrales

Hola,

Comparto mi solución al challenge de CaféNorte:

- Repositorio público: https://github.com/aaronBarrales/cafenorte_tuxpas
- Propuesta: adjunto el PDF de dos páginas; también está en docs/03_negocio/PROPUESTA_TECNICA.md.
- Respuestas de negocio: docs/03_negocio/RESPUESTAS_NEGOCIO.md.
- Bitácora de uso de IA: AI_LOG.md, dentro del repositorio.

Implementé un ETL reproducible que integra POS, ERP y Shopify, persiste el modelo analítico y genera las cuatro respuestas, con diez pruebas y validación independiente de los cálculos. La propuesta AWS estima USD 75 mensuales bajo sus supuestos. Conservé los productos sin equivalencia y documenté la cobertura reducida del ranking de rotación, así como los límites de estatus e impuestos. Dejé fuera el despliegue cloud y las conexiones productivas, que requieren accesos y acuerdos adicionales; la demo se ejecuta localmente con los archivos del reto.

Quedo atento para coordinar la sesión de revisión y mostrar la demo.

Saludos,
Aaron Barrales

## Mi demo de cinco minutos

1. Desde la raíz ejecuto `.venv/Scripts/python scripts/pipeline.py`; muestro fuentes y ventanas del manifiesto.
2. Abro las respuestas: explico los 36 pares con cobertura completa, los tres episodios y las tablas de crecimiento y margen.
3. Ejecuto `.venv/Scripts/python -m unittest discover -s scripts -p test_pipeline.py -v` y `.venv/Scripts/python scripts/validar_entrega.py`.
4. Abro el PDF y explico presupuesto, carga diaria y publicación de la última versión válida.
5. Muestro una excepción de equivalencia y explico por qué conservarla evita perder importe o asignar un costo inventado.

## Lo que estudio antes de la entrevista

Uso mi [guía de estudio de ocho capítulos](GUIA_ESTUDIO.md), disponible también en outputs/entrega/Guia_estudio_CafeNorte_Aaron_Barrales.pdf. Este PDF es para mi preparación; no hace falta adjuntarlo al reclutador.

**Rotación:** numerador y denominador usan las mismas tiendas por SKU; una métrica parcial no permite conclusiones globales. Exijo todos los días conocidos en lugar de rellenar N/A. No incorporo online sin almacén ni deduzco devoluciones físicas desde E.

**Ventas y margen:** I menos E es mi interpretación documentada, basada en SAT; no prueba el diccionario del POS. La respuesta recibida sí fija costo unitario global en MXN y vigencia. Monto y amount se tratan como total de línea; unidad física, impuestos y estatus online limitan la lectura contable. Margen negativo por operación y acumulado responden preguntas diferentes.

**AWS:** propongo carga diaria y servicios bajo demanda. Los USD 75 son un escenario con 50 GB, 30 cargas y 1 TB consultado; no prometo ese costo ante cualquier volumen. Las alertas no bloquean gasto. Si Lambda no cabe en tiempo o memoria, reviso capacidad y presupuesto antes de pasar a Fargate. Necesito responsables, accesos y cierres de control antes de operar.

**IA:** mis preguntas y aclaraciones están registradas; la implementación y pruebas automatizadas se atribuyen a la IA. Puedo explicar los errores de esquema y publicación SQLite y cómo se corrigieron. No afirmaré haber escrito código o validado manualmente algo que no hice.

## Conclusión

Tengo identificados los entregables, el mensaje de envío y la ruta de estudio para defender el proyecto. Envío código, resultados y propuesta con supuestos visibles, sin convertir limitaciones de los datos en certezas de negocio.
