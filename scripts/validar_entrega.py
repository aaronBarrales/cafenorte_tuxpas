"""Contrasta salidas persistidas con cálculos independientes de las transformaciones."""
import csv
import json
import sqlite3
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validar():
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
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    print('OK: importes mensuales independientes, conservación POS, rachas desde JSON, privacidad y SQLite')


if __name__ == '__main__':
    validar()
