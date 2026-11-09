"""Ejecuta el quinto notebook y genera su informe desde los mismos resultados."""

from pathlib import Path

import nbformat
import pandas as pd
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output
from traitlets.config import Config


def tabla_markdown(tabla):
    """Exporta tablas sin requerir tabulate ni perder etiquetas o valores ausentes."""
    def formato(valor):
        if valor is None or (not isinstance(valor, str) and pd.isna(valor)):
            return 'No disponible'
        if isinstance(valor, float):
            return f'{valor:,.4f}'
        return str(valor).replace('|', '\\|').replace('\n', ' ')

    filas = ['| ' + ' | '.join(map(str, tabla.columns)) + ' |',
             '| ' + ' | '.join(['---'] * len(tabla.columns)) + ' |']
    filas.extend('| ' + ' | '.join(formato(v) for v in fila) + ' |'
                 for fila in tabla.itertuples(index=False, name=None))
    return '\n'.join(filas)


def ejecutar():
    # Capturo resultados secuenciales con IPython y un historial en memoria, sin simular un kernel Jupyter.
    raiz = Path(__file__).resolve().parents[1]
    ruta = raiz / 'notebooks/05_conjunto.ipynb'
    notebook = nbformat.read(ruta, 4)
    config = Config()
    config.HistoryManager.hist_file = ':memory:'
    config.HistoryManager.enabled = False
    shell = InteractiveShell.instance(config=config)
    celdas = [c for c in notebook.cells if c.cell_type == 'code']
    for numero, celda in enumerate(celdas, 1):
        compile(celda.source, f'celda_{numero}', 'exec')
        with capture_output() as captura:
            resultado = shell.run_cell(celda.source, store_history=False)
        error = resultado.error_before_exec or resultado.error_in_exec
        if error:
            raise RuntimeError(f'Falló la celda {numero}; no se actualizaron entregables') from error
        celda.execution_count = numero
        celda.outputs = []
        for nombre, texto in [('stdout', captura.stdout), ('stderr', captura.stderr)]:
            if texto:
                celda.outputs.append(nbformat.v4.new_output('stream', name=nombre, text=texto))
        celda.outputs.extend(nbformat.v4.new_output('display_data', data=s.data, metadata=s.metadata)
                             for s in captura.outputs)

    # Derivo el Markdown de las explicaciones y tablas del notebook para evitar cifras mantenidas a mano.
    tablas = shell.user_ns['tablas']
    iterador = iter(tablas)
    partes = []
    for celda in notebook.cells:
        if celda.cell_type == 'markdown':
            texto = celda.source.replace(
                '# EDA conjunto: conectores entre las cuatro fuentes',
                '# Resultados del EDA conjunto: conectores entre fuentes')
            texto = texto.replace(
                '[Informe de resultados del análisis conjunto](../docs/02_exploracion/resultados_conjunto.md)',
                '[Notebook del análisis conjunto](../../notebooks/05_conjunto.ipynb).\n'
                '- [Preguntas al cliente](../03_negocio/PREGUNTAS_CLIENTE.md#evidencia-del-eda-conjunto)')
            partes.append(texto)
        else:
            for salida in celda.outputs:
                if salida.output_type == 'display_data' and 'text/html' in salida.data:
                    titulo, tabla, leyenda = next(iterador)
                    partes.append('**' + titulo + '**\n\n**Leyenda:** ' + leyenda
                                  + ' Muestro todas las filas; omito el índice de pandas.\n\n'
                                  + tabla_markdown(tabla))
    assert next(iterador, None) is None, 'Faltan tablas por exportar'
    informe = '\n\n'.join(partes) + '\n'
    nbformat.validate(notebook)
    nbformat.write(notebook, ruta)
    (raiz / 'docs/02_exploracion/resultados_conjunto.md').write_text(informe, encoding='utf-8')
    print(f'EDA conjunto: {len(celdas)} celdas y {len(tablas)} tablas; notebook e informe actualizados.')


if __name__ == '__main__':
    ejecutar()
