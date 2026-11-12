# CaféNorte — Reto Data Solutions Engineer

Integro POS, ERP y Shopify en un modelo SQLite reproducible y respondo cuatro preguntas de negocio. El ETL conserva los registros no conciliados y los importes originales; excluyo datos personales de Shopify desde la lectura. Mi propuesta productiva en AWS estima USD 75 mensuales frente al objetivo de USD 200.

## Revisar la entrega

1. [Cuatro respuestas y cobertura](docs/03_negocio/RESPUESTAS_NEGOCIO.md).
2. [Propuesta AWS: arquitectura, costos y fases](docs/03_negocio/PROPUESTA_TECNICA.md).
3. [Bitácora de IA](AI_LOG.md): mis intervenciones, propuestas, correcciones y evidencia.
4. [Modelo, granularidad y reglas](docs/03_negocio/MODELO_ETL.md).
5. [Lista de entrega y guion de entrevista](docs/04_seguimiento/ENTREGA.md).

Conservo el [enunciado original](docs/01_reto/TX%20Challenge%20Data%20Solutions%20Engineer.docx), su [transcripción](docs/01_reto/enunciado_extraido.md), los [requisitos](docs/01_reto/guia_entrega.md) y el [índice completo](docs/README.md). La solución local no requiere AWS; el reto solicita una propuesta productiva y no un despliegue.

## Ejecutar desde cero

Requiero Python 3.12. En una terminal PowerShell desde la raíz:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python scripts/pipeline.py
.venv/Scripts/python -m unittest discover -s scripts -p test_pipeline.py -v
.venv/Scripts/python scripts/validar_entrega.py
```

Antes de ejecutar coloco los cuatro archivos originales del reto en `datos/`: sales.csv, inventory.json, ecommerce_orders.parquet y exchange_rates.csv. El reclutador puede utilizar sus copias originales. No redistribuyo fuentes con información personal. La [versión de entrega](docs/04_seguimiento/VERSION_FUENTES.md) identifica sus huellas; una copia distinta detiene el ETL y requiere revisión explícita de SOURCE_HASHES en el código. La instalación nueva necesita acceso HTTPS a PyPI. El entorno local de validación reutiliza paquetes ya disponibles, circunstancia documentada en AI_LOG.

El comando genera en `outputs/etl/` el modelo SQLite, nueve CSV, RESPUESTAS.md y manifiesto.json. Este último identifica fuentes, código y hashes de cada artefacto; el validador detecta archivos alterados o una publicación incompleta. La instantánea agregada versionada está en el enlace de respuestas. Para actualizarla después de validar:

```powershell
Copy-Item outputs/etl/RESPUESTAS.md docs/03_negocio/RESPUESTAS_NEGOCIO.md
```

Resuelvo rutas desde el script; puedo ejecutarlo desde otra carpeta o indicar `--datos` y `--salida`. Para consultar la base sin software adicional:

```powershell
.venv/Scripts/python -c "import sqlite3; c=sqlite3.connect('outputs/etl/modelo.sqlite'); print(c.execute('SELECT * FROM quiebres_tiendas').fetchall()); c.close()"
```

Para generar el PDF de dos páginas instalo las dependencias opcionales y ejecuto:

```powershell
.venv/Scripts/python -m pip install -r requirements-entrega.txt
.venv/Scripts/python scripts/generar_propuesta_pdf.py
.venv/Scripts/python scripts/generar_guia_estudio.py
```

## Stack y confiabilidad

Elijo pandas para los tres formatos y las uniones temporales, Decimal para el redondeo financiero y SQLite para persistir y consultar sin servidor. El volumen cabe en memoria; un clúster aumentaría complejidad sin una necesidad demostrada. Fijo las versiones ejecutadas en requirements.txt. El PDF usa dependencias opcionales separadas del ETL.

Controlo claves únicas, relaciones m:1, fechas nulas, cantidades, monedas, stock finito, costos positivos y referencias de catálogo. Conservo filas, cantidades e importes antes y después de enriquecer; un costo o equivalente ausente nunca se vuelve cero. Guardo centavos monetarios enteros y publico la base al cerrar su conexión, después de comprobar integridad. Reconstruyo la carga completa, de modo que repetirla no duplica registros. El manifiesto se publica al final; una interrupción entre exportaciones puede dejar una versión incompleta que debe rechazarse y regenerarse.

Diez pruebas sintéticas cubren límites de fechas, claves, costo vigente, redondeo, huecos, base cero y población compatible. Un contraste independiente usa CSV/JSON/PyArrow, Decimal y búsquedas ordenadas para recalcular las cuatro respuestas, cada costo enlazado, integridad y hashes. Esto verifica transformación, no sustituye un cierre contable autorizado.

## Interpretación de las métricas

Mi corte reproducible es **2026-03-31**. El semestre abarca octubre de 2025 a marzo de 2026, el trimestre enero a marzo de 2026 y el año abril de 2025 a marzo de 2026.

Investigué el [catálogo SAT](https://wwwmat.sat.gob.mx/consultas/35025/formato-de-factura-electronica-%28anexo-20%29): I ingreso, E egreso, N nómina, P pago y T traslado. Adopto esta interpretación para el POS, que no dispone de diccionario confirmado. Conservo todos los códigos; para ingreso estimado aplico I menos E y contribución cero a N/P/T. No convierto egresos en devoluciones físicas, pues el ERP solo guarda fotografías diarias. El cliente sí aclaró costo unitario global en MXN y vigencia desde el cambio hasta el siguiente.

| Pregunta | Mi definición y límite |
|---|---|
| Top 10 por rotación | Unidades I entre inventario promedio de las mismas tiendas por SKU, con todos los saldos diarios conocidos. Solo 36 de 1,268 pares observados cumplen: es un ranking parcial, no de toda la cadena. Excluyo online sin almacén asignable y no resto unidades E. Denominador cero produce desconocido; desempato por SKU ascendente. |
| Quiebres mayores de tres días | Al menos cuatro fechas consecutivas de saldo cero por tienda–SKU, dentro del trimestre. Huecos y N/A rompen la racha. Reporto tres episodios en T015, T023 y T038; no pruebo agotamiento durante 24 horas. |
| Crecimiento mensual | (Ingreso MXN actual / anterior − 1) × 100, por canal y sin saltar meses. Base cero o ausente queda desconocida; abril online no tiene marzo previo. Uso FX del día y MXN=1, con HALF_UP por registro. Las órdenes online se suponen elegibles por falta de estatus. |
| Margen negativo | Importe de línea menos cantidad por costo unitario vigente. Distingo operaciones negativas de margen acumulado negativo por producto y tienda. Online figura sin almacén. Uso el mismo año del crecimiento; excluyo solo del margen las operaciones sin costo, conservándolas en el modelo. |

Leyenda: cada fila define una pregunta; cantidades en unidades de catálogo bajo equivalencia física supuesta, dinero en MXN y crecimiento en porcentaje. Monto y amount se tratan como totales de línea; no los multiplico otra vez por cantidad. Impuestos, descuentos y unidades físicas comparables siguen siendo límites de interpretación. Mantengo canales separados sin afirmar ausencia de duplicación. Las excepciones quedan documentadas en [DUDAS](docs/03_negocio/DUDAS.md) y en las coberturas de resultados; no bloquean la ejecución del escenario declarado.

## Organización y alcance

```text
datos/              Originales locales excluidos de Git.
notebooks/          Cuatro exploraciones individuales y conciliación conjunta.
scripts/            ETL, tests, validadores, perfiles y generador PDF.
outputs/            Modelo, CSV, manifiesto, PDF y paquete de entrega; excluidos.
docs/01_reto/       Enunciado original y requisitos.
docs/02_exploracion/ Resultados exploratorios de su versión de fuentes.
docs/03_negocio/    Respuestas finales, modelo, propuesta, definiciones y dudas.
docs/04_seguimiento/ Entrega, continuidad, plan y versiones.
docs/05_antecedentes/ Estudios y casos históricos.
AI_LOG.md           Intervenciones, uso de IA y evidencia técnica.
```

Las convenciones están en [AGENTS](AGENTS.md), la navegación en [docs/README](docs/README.md) y el estado en [CONTINUIDAD](docs/04_seguimiento/CONTINUIDAD.md). Preservo notebooks y resultados de su versión sin presentarlos como recalculados sobre el cambio de sales. Las instrucciones de exploración están en [notebooks/README](notebooks/README.md); sus dependencias se reúnen en requirements-exploracion.txt.

Entrego ETL local, persistencia, cuatro respuestas, pruebas, propuesta AWS y bitácora. Dejo fuera despliegue cloud, conectores productivos, BI nuevo y certificación contable: requieren accesos, responsables y definiciones que los archivos no proporcionan. El [guion de entrega](docs/04_seguimiento/ENTREGA.md) contiene la matriz de cumplimiento, los adjuntos y el correo preparado.

## Conclusión

Tengo una entrega ejecutable y trazable, con cuatro respuestas bajo reglas explícitas, pruebas y contrastes independientes. Presento las excepciones y la cobertura real para defender los resultados y una propuesta AWS proporcionada al presupuesto.
