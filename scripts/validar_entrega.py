"""Contrasta salidas persistidas con cálculos independientes de las transformaciones."""
import csv
import hashlib
import json
import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from bisect import bisect_right

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]


def validar():
    manifest = json.loads((ROOT / 'outputs/etl/manifiesto.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((ROOT / 'scripts/pipeline.py').read_bytes()).hexdigest() == manifest['codigo_sha256'], 'El código cambió desde la ejecución'
    for name, digest in manifest['artefactos_sha256'].items():
        assert hashlib.sha256((ROOT / 'outputs/etl' / name).read_bytes()).hexdigest() == digest, name
    for name, digest in manifest['hashes'].items():
        assert hashlib.sha256((ROOT / 'datos' / name).read_bytes()).hexdigest() == digest, name
    # Recalculo ventas físicas mensuales desde CSV sin pandas ni funciones del ETL.
    totals = defaultdict(int)
    rows = list(csv.DictReader((ROOT / 'datos/sales.csv').open(encoding='utf-8-sig')))
    for row in rows:
        month = datetime.strptime(row['fecha_hora'], '%d/%m/%Y %H:%M').strftime('%Y-%m')
        sign = {'I': 1, 'E': -1, 'N': 0, 'P': 0, 'T': 0}[row['tipo_comprobante']]
        totals[month] += int((Decimal(row['monto']) * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP)) * sign
    with sqlite3.connect(ROOT / 'outputs/etl/modelo.sqlite') as db:
        assert db.execute("SELECT count(*) FROM fact_movimiento WHERE canal='fisico'").fetchone()[0] == len(rows)
        for month, amount in db.execute("SELECT mes, ingreso_mxn FROM crecimiento_mensual WHERE canal='fisico'"):
            assert abs(Decimal(str(amount)) * 100 - totals[month]) < Decimal('0.0001'), month
        columns = [r[1] for r in db.execute('PRAGMA table_info(fact_movimiento)')]
        assert not any(x in columns for x in ['customer_name', 'customer_email', 'customer_rfc', 'shipping_address', 'shipping_city'])
        # Recalculo rachas con un recorrido secuencial de la fuente JSON, incluidos desconocidos.
        source = json.loads((ROOT / 'datos/inventory.json').read_text(encoding='utf-8-sig'))
        grouped = defaultdict(list)
        for row in source['snapshots']:
            if '2026-01-01' <= row['fecha'] <= '2026-03-31':
                grouped[(row['tienda_id'], row['sku_erp'])].append(row)
        expected = []
        for (store, sku), values in grouped.items():
            run = []
            for row in sorted(values, key=lambda r: r['fecha']):
                day = datetime.fromisoformat(row['fecha'])
                if row['cantidad_en_stock'] == 0:
                    if run and (day - run[-1]).days != 1:
                        if len(run) > 3:
                            expected.append((store, sku, run[0].strftime('%Y-%m-%d'), len(run)))
                        run = []
                    run.append(day)
                else:
                    if len(run) > 3:
                        expected.append((store, sku, run[0].strftime('%Y-%m-%d'), len(run)))
                    run = []
            if len(run) > 3:
                expected.append((store, sku, run[0].strftime('%Y-%m-%d'), len(run)))
        actual = [(a, b, c[:10], d) for a, b, c, d in db.execute('SELECT tienda_id, sku_erp, inicio, dias FROM quiebres_episodios')]
        assert sorted(expected) == sorted(actual)
        # Contrasto online, costo y margen desde fuentes comerciales sin usar las funciones del ETL.
        rate = {(r['fecha'], r['currency']): Decimal(r['rate_to_mxn']) for r in csv.DictReader((ROOT / 'datos/exchange_rates.csv').open(encoding='utf-8-sig'))}
        mappings = {r['sku_pos']: r['sku_erp'] for r in source['sku_mappings']}
        handles = {r['handle']: r['sku_erp'] for r in source['sku_mappings'] if r['handle'] is not None}
        costs = {p['sku_erp']: sorted((h['fecha_vigencia'], Decimal(str(h['costo_mxn']))) for h in p['cost_history']) for p in source['catalogo']['productos']}
        all_margin, negative_margin = defaultdict(lambda: [0, 0]), defaultdict(lambda: [0, 0])
        online_totals = defaultdict(int)
        commerce = pq.read_table(ROOT / 'datos/ecommerce_orders.parquet', columns=['order_id', 'fecha', 'product_handle', 'cantidad', 'amount', 'currency']).to_pylist()
        for channel, records in [('fisico', rows), ('online', commerce)]:
            for row in records:
                day = datetime.strptime(row['fecha_hora'], '%d/%m/%Y %H:%M').strftime('%Y-%m-%d') if channel == 'fisico' else row['fecha'][:10]
                amount = Decimal(str(row['monto'] if channel == 'fisico' else row['amount']))
                currency = 'MXN' if channel == 'fisico' else row['currency']
                converted = int((amount * (Decimal(1) if currency == 'MXN' else rate[(day, currency)]) * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))
                if channel == 'online':
                    online_totals[day[:7]] += converted
                sku = mappings.get(row['sku']) if channel == 'fisico' else handles.get(row['product_handle'])
                if not sku or (channel == 'fisico' and row['tipo_comprobante'] != 'I'):
                    continue
                versions = costs[sku]
                position = bisect_right([v[0] for v in versions], day) - 1
                if position < 0:
                    continue
                unit_cost = versions[position][1]
                cost = int((unit_cost * int(row['cantidad']) * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))
                identifier = row['venta_id'] if channel == 'fisico' else row['order_id']
                id_column = 'venta_id' if channel == 'fisico' else 'order_id'
                actual_cost = db.execute(f'SELECT costo_centavos FROM fact_movimiento WHERE canal=? AND {id_column}=?', (channel, identifier)).fetchone()[0]
                assert actual_cost == cost, identifier
                if not '2025-04-01' <= day <= '2026-03-31':
                    continue
                key = (channel, row['tienda_id'] if channel == 'fisico' else 'ONLINE_SIN_ALMACEN', sku)
                margin = converted - cost
                all_margin[key][0] += 1
                all_margin[key][1] += margin
                if margin < 0:
                    negative_margin[key][0] += 1
                    negative_margin[key][1] += margin
        for month, amount in db.execute("SELECT mes, ingreso_mxn FROM crecimiento_mensual WHERE canal='online'"):
            assert abs(Decimal(str(amount)) * 100 - online_totals[month]) < Decimal('0.0001'), month
        for channel, month, actual_growth in db.execute('SELECT canal, mes, crecimiento_pct FROM crecimiento_mensual'):
            first_day = datetime.strptime(month, '%Y-%m')
            previous = (first_day - timedelta(days=1)).strftime('%Y-%m')
            amounts = totals if channel == 'fisico' else online_totals
            if previous not in amounts or amounts[previous] == 0:
                assert actual_growth is None
            else:
                expected_growth = (Decimal(amounts[month]) / amounts[previous] - 1) * 100
                assert abs(Decimal(str(actual_growth)) - expected_growth) < Decimal('0.000000001')
        expected_margin = {k: tuple(v) for k, v in all_margin.items() if v[1] < 0}
        actual_margin = {tuple(r[:3]): tuple(r[3:]) for r in db.execute('SELECT canal, tienda_id, sku_erp, operaciones, margen_total_centavos FROM margen_negativo_acumulado')}
        assert expected_margin == actual_margin
        actual_negative = {tuple(r[:3]): tuple(r[3:]) for r in db.execute('SELECT canal, tienda_id, sku_erp, operaciones_negativas, margen_negativo_centavos FROM margen_negativo_operaciones')}
        assert {k: tuple(v) for k, v in negative_margin.items()} == actual_negative
        # Recalculo el ranking desde las 182 observaciones por par y las unidades I de CSV.
        stocks = defaultdict(list)
        for row in source['snapshots']:
            if '2025-10-01' <= row['fecha'] <= '2026-03-31':
                stocks[(row['tienda_id'], row['sku_erp'])].append(row['cantidad_en_stock'])
        complete = {k: v for k, v in stocks.items() if len(v) == 182 and all(isinstance(x, (int, float)) for x in v)}
        denominator, units = defaultdict(float), defaultdict(int)
        for (_, sku), values in complete.items():
            denominator[sku] += sum(values) / 182
        for row in rows:
            day = datetime.strptime(row['fecha_hora'], '%d/%m/%Y %H:%M').strftime('%Y-%m-%d')
            sku = mappings.get(row['sku'])
            if '2025-10-01' <= day <= '2026-03-31' and row['tipo_comprobante'] == 'I' and (row['tienda_id'], sku) in complete:
                units[sku] += int(row['cantidad'])
        ranking = sorted([(sku, units[sku] / total) for sku, total in denominator.items() if total > 0], key=lambda r: (-r[1], r[0]))[:10]
        actual_ranking = db.execute('SELECT sku_erp, rotacion_veces FROM rotacion_top10 ORDER BY rotacion_veces DESC, sku_erp').fetchall()
        assert [r[0] for r in ranking] == [r[0] for r in actual_ranking]
        assert all(abs(a[1]-b[1]) < 1e-12 for a, b in zip(ranking, actual_ranking))
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    print('OK: cuatro métricas independientes, costo por movimiento, hashes de fuentes y artefactos, privacidad y SQLite')


if __name__ == '__main__':
    validar()
