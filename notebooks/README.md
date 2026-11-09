# Exploración por fuente

Ejecuta cada notebook de principio a fin con las fuentes en `datos/`.

- [01_sales.ipynb](01_sales.ipynb): ventas físicas; primer notebook disponible.
- [Informe de resultados de sales](../docs/02_exploracion/resultados_sales.md): tablas, interpretación, importancia y límites de la exploración aislada, legibles en GitHub.
- [02_exchange_rates.ipynb](02_exchange_rates.ipynb): exploración aislada de tipos de cambio, con comentarios en español por bloque importante.
- [Informe de exchange_rates](../docs/02_exploracion/resultados_exchange_rates.md): resultados, interpretación, límites y conexión con preguntas.
- [03_inventory.ipynb](03_inventory.ipynb): exploración aislada de inventario, equivalencias, catálogo e historial de costos.
- [Informe de inventory](../docs/02_exploracion/resultados_inventory.md): cobertura, saldos desconocidos, rachas de ceros y dudas abiertas.
- Siguiente fuente por explorar: ecommerce. Asigno su prefijo numérico al crearlas, después de revisar los notebooks existentes en esta carpeta.

Estructura común: objetivo y granularidad, lectura, esquema, diccionario, calidad, cobertura temporal, distribución de valores y conclusiones. Cada fuente añade sus controles particulares.

Los notebooks exploran y documentan; no corrigen ni sobrescriben las fuentes. Los scripts de `../scripts/` conservan los perfiles automáticos existentes. Las salidas guardadas pueden quedar desactualizadas si cambia el archivo: vuelve a ejecutar antes de interpretarlas.

## Conclusión

Uso un notebook por fuente para conocer su estructura, calidad y cobertura antes de conciliarlas. Mantengo los originales intactos y vinculo cada exploración con su informe de resultados.
