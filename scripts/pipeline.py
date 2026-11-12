"""ETL local reproducible; originales intactos y modelo SQLite sin datos personales."""
import argparse
from contextlib import closing
import hashlib
import json
import os
import sqlite3
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FILES = ['sales.csv', 'inventory.json', 'ecommerce_orders.parquet', 'exchange_rates.csv']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(frame, keys):
    require(not frame[keys].isna().any().any(), f'Clave nula: {keys}')
    require(not frame.duplicated(keys).any(), f'Clave duplicada: {keys}')


def cents(amount, rate=1):
    return int((Decimal(str(amount)) * Decimal(str(rate)) * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def attach_cost(frame, costs):
    # Selecciono la última vigencia no futura sin perder filas sin equivalencia.
    matched = frame[frame.sku_erp.notna()].copy()
    unmatched = frame[frame.sku_erp.isna()].copy()
    matched = pd.merge_asof(matched.sort_values('dia'), costs.sort_values('vigencia'),
                            left_on='dia', right_on='vigencia', by='sku_erp', direction='backward')
    result = pd.concat([matched, unmatched], ignore_index=True).sort_values('fila_id')
    require(len(result) == len(frame), 'El costo multiplicó filas')
    require((result.vigencia.isna() | (result.vigencia <= result.dia)).all(), 'Costo futuro')
    return result.reset_index(drop=True)


def stockouts(stock, start, end):
    # Un hueco temporal o saldo desconocido interrumpe la continuidad observada.
    z = stock[stock.dia.between(start, end) & stock.stock_num.eq(0)].copy()
    z = z.sort_values(['tienda_id', 'sku_erp', 'dia'])
    keys = ['tienda_id', 'sku_erp']
    z['episodio'] = z.groupby(keys).dia.diff().dt.days.ne(1).cumsum()
    runs = z.groupby(keys + ['episodio']).agg(inicio=('dia', 'min'), fin=('dia', 'max'), dias=('dia', 'size')).reset_index()
    runs = runs[runs.dias > 3].drop(columns='episodio')
    runs['toca_inicio_ventana'] = runs.inicio.eq(start)
    runs['toca_fin_ventana'] = runs.fin.eq(end)
    return runs


def rotation(sales, stock, start, end):
    # Restrinjo ambos lados a pares tienda–SKU con todos los días conocidos del semestre.
    s = stock[stock.dia.between(start, end)]
    days = (end - start).days + 1
    pairs = s.groupby(['tienda_id', 'sku_erp']).agg(dias_conocidos=('stock_num', 'count'),
                                                  stock_promedio=('stock_num', 'mean')).reset_index()
    pairs = pairs[pairs.dias_conocidos.eq(days)]
    v = sales[sales.dia.between(start, end) & sales.tipo_comprobante.eq('I')]
    v = v.merge(pairs[['tienda_id', 'sku_erp']], on=['tienda_id', 'sku_erp'], how='inner', validate='m:1')
    units = v.groupby('sku_erp').cantidad.sum()
    result = pairs.groupby('sku_erp').agg(inventario_promedio=('stock_promedio', 'sum'), tiendas=('tienda_id', 'nunique'))
    result['unidades_I'] = units.reindex(result.index, fill_value=0)
    result['rotacion_veces'] = result.unidades_I.div(result.inventario_promedio.where(result.inventario_promedio > 0))
    return result.reset_index().sort_values(['rotacion_veces', 'sku_erp'], ascending=[False, True]).head(10)


def monthly(fact, start, end):
    f = fact[fact.dia.between(start - pd.DateOffset(months=1), end)].copy()
    f['mes'] = f.dia.dt.to_period('M').astype(str)
    agg = f.groupby(['canal', 'mes']).agg(ingreso_centavos=('ingreso_centavos', 'sum'), registros=('fila_id', 'size'))
    index = pd.MultiIndex.from_product([['fisico', 'online'], pd.period_range(start - pd.DateOffset(months=1), end, freq='M').astype(str)], names=['canal', 'mes'])
    agg = agg.reindex(index).reset_index()
    agg['ingreso_mxn'] = agg.ingreso_centavos / 100
    agg['anterior_mxn'] = agg.groupby('canal').ingreso_mxn.shift()
    agg['crecimiento_pct'] = (agg.ingreso_mxn / agg.anterior_mxn.where(agg.anterior_mxn.ne(0)) - 1) * 100
    return agg[agg.mes >= str(start.to_period('M'))].drop(columns='ingreso_centavos')


def markdown(frame):
    def fmt(v):
        if pd.isna(v):
            return 'No disponible'
        return (f'{v:,.4f}' if isinstance(v, float) else str(v)).replace('|', '\\|')
    return '\n'.join(['| ' + ' | '.join(frame.columns) + ' |', '| ' + ' | '.join(['---'] * len(frame.columns)) + ' |'] +
                     ['| ' + ' | '.join(fmt(v) for v in row) + ' |' for row in frame.itertuples(index=False, name=None)])


def run(data_dir=ROOT / 'datos', output_dir=ROOT / 'outputs/etl'):
    data_dir, output_dir = Path(data_dir), Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    hashes = {f: hashlib.sha256((data_dir / f).read_bytes()).hexdigest() for f in FILES}
    baseline = (ROOT / 'docs/02_exploracion/resultados_conjunto.md').read_text(encoding='utf-8')
    baseline += (ROOT / 'docs/04_seguimiento/VERSION_FUENTES.md').read_text(encoding='utf-8')
    require(all(h in baseline for h in hashes.values()), 'Fuente distinta a versiones documentadas')
    inv = json.loads((data_dir / 'inventory.json').read_text(encoding='utf-8-sig'))
    pos = pd.read_csv(data_dir / 'sales.csv')
    online = pd.read_parquet(data_dir / 'ecommerce_orders.parquet', columns=['order_id', 'fecha', 'product_handle', 'cantidad', 'amount', 'currency'])
    fx = pd.read_csv(data_dir / 'exchange_rates.csv')
    mappings = pd.DataFrame(inv['sku_mappings'])
    products = pd.DataFrame(inv['catalogo']['productos']).drop(columns='cost_history')
    stores = pd.DataFrame(inv['tiendas_info'])
    stock = pd.DataFrame(inv['snapshots'])
    costs = pd.DataFrame([dict(sku_erp=p['sku_erp'], vigencia=h['fecha_vigencia'], costo_mxn=h['costo_mxn'])
                          for p in inv['catalogo']['productos'] for h in p['cost_history']])
    costs['vigencia'] = pd.to_datetime(costs.vigencia, errors='raise')
    stock['dia'] = pd.to_datetime(stock.fecha, errors='raise')
    stock['stock_num'] = pd.to_numeric(stock.cantidad_en_stock, errors='coerce')
    fx['dia'] = pd.to_datetime(fx.fecha, errors='raise')
    for frame, keys in [(products, ['sku_erp']), (stores, ['tienda_id']), (stock, ['dia', 'tienda_id', 'sku_erp']),
                         (costs, ['sku_erp', 'vigencia']), (fx, ['dia', 'currency']), (pos, ['venta_id']), (online, ['order_id'])]:
        unique(frame, keys)
    require((costs.costo_mxn > 0).all() and np.isfinite(costs.costo_mxn).all(), 'Costo inválido')
    require((fx.rate_to_mxn > 0).all() and np.isfinite(fx.rate_to_mxn).all(), 'FX inválido')
    require(stock.stock_num.dropna().ge(0).all(), 'Stock negativo no soportado')
    require(set(pos.tipo_comprobante) <= set('IENTP'), 'Código POS desconocido')
    require(pos.moneda.eq('MXN').all(), 'Moneda POS no soportada')
    require(pos.tienda_id.isin(stores.tienda_id).all(), 'Tienda desconocida')
    frames = []
    for source, key, mapkey, datecol, datefmt, channel in [(pos, 'sku', 'sku_pos', 'fecha_hora', '%d/%m/%Y %H:%M', 'fisico'),
                                                         (online, 'product_handle', 'handle', 'fecha', None, 'online')]:
        f = source.copy()
        f['fila_id'] = np.arange(len(f))
        f['dia'] = pd.to_datetime(f[datecol], format=datefmt, errors='raise').dt.normalize()
        m = mappings[mappings[mapkey].notna()][[mapkey, 'sku_erp']]
        unique(m, [mapkey])
        f = f.merge(m, left_on=key, right_on=mapkey, how='left', validate='m:1', indicator=True)
        f['estado_mapeo'] = np.where(f._merge.eq('left_only'), 'sin_equivalencia', np.where(f.sku_erp.isna(), 'erp_nulo', 'exacto'))
        require(f.sku_erp.dropna().isin(products.sku_erp).all(), 'ERP fuera de catálogo')
        f = attach_cost(f.drop(columns='_merge'), costs)
        f['canal'] = channel
        f['currency'] = f['moneda'] if channel == 'fisico' else f.currency
        f['importe_original'] = f['monto'] if channel == 'fisico' else f.amount
        require(f.cantidad.gt(0).all() and np.isfinite(f.importe_original).all() and f.importe_original.ge(0).all(), 'Cantidad o importe no soportado')
        f = f.merge(fx[['dia', 'currency', 'rate_to_mxn']], on=['dia', 'currency'], how='left', validate='m:1')
        f.loc[f.currency.eq('MXN'), 'rate_to_mxn'] = 1
        require(f.rate_to_mxn.notna().all(), 'Falta tasa del día')
        f['importe_centavos'] = [cents(a, r) for a, r in zip(f.importe_original, f.rate_to_mxn)]
        f['signo_ingreso'] = f.tipo_comprobante.map({'I': 1, 'E': -1, 'N': 0, 'P': 0, 'T': 0}) if channel == 'fisico' else 1
        f['ingreso_centavos'] = f.importe_centavos * f.signo_ingreso
        f['costo_centavos'] = [cents(c, q) if pd.notna(c) else None for c, q in zip(f.costo_mxn, f.cantidad)]
        if channel == 'online':
            f['tienda_id'] = 'ONLINE_SIN_ALMACEN'
            f['tipo_comprobante'] = 'ORDEN'
        f['margen_centavos'] = (f.importe_centavos - f.costo_centavos).where(f.tipo_comprobante.isin(['I', 'ORDEN']))
        require(len(f) == len(source) and f.cantidad.sum() == source.cantidad.sum(), 'Pérdida de registros o cantidades')
        require(np.isclose(f.importe_original.sum(), source['monto' if channel == 'fisico' else 'amount'].sum(), atol=1e-7, rtol=0), 'Importes alterados')
        frames.append(f)
    fact = pd.concat(frames, ignore_index=True)
    end = min(pos.pipe(lambda x: pd.to_datetime(x.fecha_hora, format='%d/%m/%Y %H:%M').max()).normalize(), frames[1].dia.max(), stock.dia.max())
    require(end.is_month_end, 'Corte incompleto: necesito un último mes cerrado')
    year = end.to_period('M').start_time - pd.DateOffset(months=11)
    half = end.to_period('M').start_time - pd.DateOffset(months=5)
    quarter = end.to_period('Q').start_time
    results = {'rotacion_top10': rotation(frames[0], stock, half, end), 'quiebres_episodios': stockouts(stock, quarter, end),
               'crecimiento_mensual': monthly(fact, year, end)}
    margins = fact[fact.margen_centavos.notna() & fact.dia.between(year, end)]
    negative = margins[margins.margen_centavos < 0]
    results['margen_negativo_operaciones'] = negative.groupby(['canal', 'tienda_id', 'sku_erp']).agg(
        operaciones_negativas=('fila_id', 'size'), margen_negativo_centavos=('margen_centavos', 'sum')).reset_index()
    aggregate = margins.groupby(['canal', 'tienda_id', 'sku_erp']).agg(operaciones=('fila_id', 'size'), margen_total_centavos=('margen_centavos', 'sum')).reset_index()
    results['margen_negativo_acumulado'] = aggregate[aggregate.margen_total_centavos < 0]
    results['cobertura'] = fact.groupby(['canal', 'estado_mapeo']).agg(registros=('fila_id', 'size')).reset_index()
    results['cobertura_margen'] = fact.assign(costo_disponible=fact.costo_centavos.notna()).groupby(['canal', 'costo_disponible']).agg(registros=('fila_id', 'size')).reset_index()
    eligible_stock = stock[stock.dia.between(half, end)].groupby(['tienda_id', 'sku_erp']).stock_num.count()
    results['cobertura_rotacion'] = pd.DataFrame({'medida': ['pares_observados', 'pares_cobertura_completa', 'dias_exigidos'],
                                               'valor': [len(eligible_stock), int(eligible_stock.eq((end-half).days+1).sum()), (end-half).days+1]})
    temp = output_dir / 'modelo.tmp.sqlite'
    # Publico la base solamente después de completar las validaciones y la carga.
    with closing(sqlite3.connect(temp)) as db, db:
        for name, frame in dict(dim_producto=products, dim_tienda=stores, puente_producto=mappings, historial_costo=costs,
                                fact_stock=stock, fact_movimiento=fact, tasas=fx, **results).items():
            frame.to_sql(name, db, if_exists='replace', index=False)
        db.execute('CREATE UNIQUE INDEX IF NOT EXISTS movimiento_pk ON fact_movimiento(canal, fila_id)')
        db.execute('CREATE UNIQUE INDEX IF NOT EXISTS stock_pk ON fact_stock(dia, tienda_id, sku_erp)')
        require(db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok', 'SQLite inconsistente')
    require(hashes == {f: hashlib.sha256((data_dir / f).read_bytes()).hexdigest() for f in FILES}, 'La fuente cambió durante la ejecución')
    os.replace(temp, output_dir / 'modelo.sqlite')
    for name, frame in results.items():
        frame.to_csv(output_dir / f'{name}.csv', index=False)
    manifest = dict(hashes=hashes, corte=str(end.date()), inicio_semestre=str(half.date()), inicio_trimestre=str(quarter.date()),
                    inicio_anio=str(year.date()), filas_pos=len(pos), filas_online=len(online), filas_stock=len(stock),
                    python=__import__('platform').python_version(), pandas=pd.__version__)
    (output_dir / 'manifiesto.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    sections = ['# Respuestas calculadas de CaféNorte',
                f'Mi corte es {end.date()}; analizo conjuntamente las cuatro fuentes identificadas en el manifiesto. Aplico las interpretaciones del README; no certifico ingresos contables ni unidades equivalentes.',
                'Para rotación uso unidades I y pares tienda–SKU con cobertura diaria completa. Para quiebres cuento ceros consecutivos observados, sin completar ausencias. MoM usa I menos E y órdenes online sin estatus. Margen compara importe con costo vigente y es anterior a gastos e impuestos no identificados.']
    for name, frame in results.items():
        sections += [f'## {name}', 'Leyenda: muestro todas las filas sin índice; centavos son centésimas de MXN; crecimiento_pct es porcentaje y rotacion_veces son vueltas del semestre. No disponible expresa ausencia de base o denominador válido; tiendas cuenta sucursales incluidas. Ordeno el ranking por rotación descendente y SKU ascendente para desempatar.', markdown(frame)]
    sections += ['## Conclusión', 'Obtengo cuatro respuestas reproducibles con cobertura explícita y excepciones conservadas. Interpreto los resultados como escenarios operativos sujetos a los límites de las fuentes.']
    (output_dir / 'RESPUESTAS.md').write_text('\n\n'.join(sections) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))
    print({k: len(v) for k, v in results.items()})
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datos', type=Path, default=ROOT / 'datos')
    parser.add_argument('--salida', type=Path, default=ROOT / 'outputs/etl')
    args = parser.parse_args()
    run(args.datos, args.salida)
