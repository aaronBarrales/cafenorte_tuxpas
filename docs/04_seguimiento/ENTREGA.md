# Guion de entrega y entrevista

## Mi demo de cinco minutos

1. Ejecuto `python scripts/pipeline.py` desde la raíz y muestro el manifiesto de fuentes y ventanas.
2. Abro `outputs/etl/RESPUESTAS.md`: explico el universo cubierto del ranking, los episodios de cero, la base previa del crecimiento y la diferencia entre margen puntual y acumulado.
3. Muestro `python -m unittest discover -s scripts -p test_pipeline.py -v` y explico qué errores numéricos previenen las pruebas.
4. Abro la propuesta: carga diaria, servicios bajo demanda y presupuesto previsto de USD 75 mensuales con supuestos.
5. Muestro una excepción de mapeo sin datos personales y explico por qué conservarla evita perder ingresos o inventar costos.

## Mi presentación al director

«Integro las fuentes en un modelo común y dejo visibles los datos que todavía no cruzan. Ya puedo mostrar cuatro respuestas bajo reglas explícitas; no mezclo órdenes sin estatus con cifras contables confirmadas. Propongo comenzar con una carga diaria de bajo costo y un responsable de conciliación. Antes de ampliar tableros, acordamos cómo validar impuestos, unidades y cierres; así el reporte ayuda a decidir y también se puede explicar.»

## Texto preparado para el correo

Asunto: Entrega challenge Data Solutions Engineer — Aaron Barrales

Hola, comparto mi solución en [el repositorio](https://github.com/aaronBarrales/cafenorte_tuxpas). Incluye el ETL reproducible, el modelo analítico local, las cuatro respuestas, pruebas de reglas críticas y AI_LOG.md. La propuesta está en docs/03_negocio/PROPUESTA_TECNICA.md. Dejé fuera el despliegue AWS y las conexiones productivas porque el reto proporciona archivos; documento su arquitectura y presupuesto. Conservo excepciones y explico los límites de equivalencias, estatus e inventario para evitar cifras artificialmente completas. Quedo atento para mostrar la demo y conversar sobre las decisiones.

El texto queda preparado para mi revisión; no se ha enviado. Antes de compartir verificaré acceso de los evaluadores al repositorio y ejecutaré la demo en el entorno de entrevista.

## Conclusión

Tengo una ruta breve para mostrar el resultado, explicar sus límites y defender las decisiones con evidencia; mantengo el envío y mi revisión personal separados de las validaciones automatizadas.
