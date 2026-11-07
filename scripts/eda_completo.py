"""Exploración reproducible de las cuatro fuentes; no modifica datos ni aplica correcciones."""

import argparse
import csv
import hashlib
import json
import re
import statistics
from bisect import bisect_right
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path

import pyarrow.parquet as pq


DATE_FORMATS = ("%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M", "%Y-%m-%d")


def parse_date(value):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt), fmt
        except (ValueError, TypeError):
            pass
    raise ValueError(f"Fecha no interpretable: {value!r}")


def number(value):
    try:
        result = Decimal(str(value))
        return result if result.is_finite() else None
    except (InvalidOperation, ValueError):
        return None


def distribution(values):
    values = sorted(values)
    if not values:
        return None
    q = lambda p: values[round((len(values) - 1) * p)]
    return {"n": len(values), "min": values[0], "p25": q(.25),
            "mediana": statistics.median(values), "p75": q(.75), "p95": q(.95), "max": values[-1]}


def profile(rows, columns, id_column=None):
    signatures = Counter(json.dumps(r, sort_keys=True, default=str) for r in rows)
    result = {"filas": len(rows), "columnas": columns,
              "nulos_o_vacios": {c: sum(r.get(c) is None or
                                       (isinstance(r.get(c), str) and not r[c].strip()) for r in rows)
                                 for c in columns},
              "espacios_en_extremos": {c: sum(isinstance(r.get(c), str) and r[c] != r[c].strip()
                                               for r in rows) for c in columns},
              "duplicados_exactos_extra": sum(n - 1 for n in signatures.values())}
    if id_column:
        ids = Counter(r.get(id_column) for r in rows)
        result.update({"ids_distintos": len(ids), "ids_repetidos": sum(n > 1 for n in ids.values()),
                       "filas_extra_por_id": sum(n - 1 for n in ids.values())})
    return result


def date_profile(rows, column):
    formats, parsed = Counter(), []
    invalid = 0
    for row in rows:
        try:
            value, fmt = parse_date(row[column])
            formats[fmt] += 1
            parsed.append(value)
        except ValueError:
            invalid += 1
    return {"min": min(parsed).isoformat(sep=" ") if parsed else None,
            "max": max(parsed).isoformat(sep=" ") if parsed else None,
            "invalidas": invalid, "formatos": dict(formats)}, parsed


def csv_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return list(reader), reader.fieldnames


def dates_between(start, end):
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


def numeric_profile(rows, columns):
    result = {}
    for column in columns:
        vals = [number(r.get(column)) for r in rows]
        valid = [v for v in vals if v is not None]
        result[column] = {"invalidos": sum(v is None for v in vals),
                          "negativos": sum(v < 0 for v in valid), "ceros": sum(v == 0 for v in valid),
                          "no_enteros": sum(v != v.to_integral_value() for v in valid),
                          "distribucion": distribution(valid)}
    return result


def explore(root):
    data = root / "datos"
    files = ["sales.csv", "inventory.json", "ecommerce_orders.parquet", "exchange_rates.csv"]
    manifest = {name: {"bytes": (data / name).stat().st_size,
                       "sha256": hashlib.sha256((data / name).read_bytes()).hexdigest()} for name in files}
    sales, sales_columns = csv_rows(data / "sales.csv")
    fx, fx_columns = csv_rows(data / "exchange_rates.csv")
    inventory = json.loads((data / "inventory.json").read_text(encoding="utf-8-sig"))
    ecommerce_table = pq.read_table(data / "ecommerce_orders.parquet")
    ecommerce = ecommerce_table.to_pylist()
    products, snapshots = inventory["catalogo"]["productos"], inventory["snapshots"]
    mappings, stores = inventory["sku_mappings"], inventory["tiendas_info"]
    product_by_erp = {p["sku_erp"]: p for p in products}
    map_by_pos = {m["sku_pos"]: m for m in mappings}
    map_by_handle = {m["handle"]: m for m in mappings if m.get("handle")}
    store_ids = {s["tienda_id"] for s in stores}

    sales_report = profile(sales, sales_columns, "venta_id")
    sales_report["fechas"], sales_dates = date_profile(sales, "fecha_hora")
    sales_report["numericos"] = numeric_profile(sales, ["cantidad", "monto"])
    sales_report["monedas"] = dict(Counter(r["moneda"] for r in sales))
    sales_report["tiendas"] = len({r["tienda_id"] for r in sales})
    sales_report["skus"] = len({r["sku"] for r in sales})
    sales_report["tiendas_sin_catalogo"] = sorted({r["tienda_id"] for r in sales} - store_ids)
    sales_report["formatos_identificador_invalidos"] = {
        c: sum(re.fullmatch(pattern, r[c]) is None for r in sales)
        for c, pattern in [("venta_id", r"V\d{8}"), ("tienda_id", r"T\d{3}"), ("sku", r"CN-\d{5}")]}
    per_type, per_month = {}, {}
    store_days, daily_counts = set(), Counter()
    per_sku_units = defaultdict(list)
    for row in sales:
        group = per_type.setdefault(row["tipo_comprobante"], {"filas": 0, "cantidad": Decimal(0), "monto": Decimal(0)})
        group["filas"] += 1
        quantity, amount = number(row["cantidad"]), number(row["monto"])
        if quantity is not None:
            group["cantidad"] += quantity
        if amount is not None:
            group["monto"] += amount
        try:
            dt, _ = parse_date(row["fecha_hora"])
        except ValueError:
            continue
        month = per_month.setdefault(dt.strftime("%Y-%m"), {"filas": 0, "I_monto": Decimal(0), "E_monto": Decimal(0)})
        month["filas"] += 1
        if row["tipo_comprobante"] in {"I", "E"} and amount is not None:
            month[row["tipo_comprobante"] + "_monto"] += amount
        store_days.add((row["tienda_id"], dt.date()))
        daily_counts[dt.date()] += 1
        if row["tipo_comprobante"] == "I" and quantity and quantity > 0 and amount is not None:
            per_sku_units[row["sku"]].append(amount / quantity)
    sales_report["por_comprobante"] = per_type
    sales_report["por_mes"] = dict(sorted(per_month.items()))
    calendar = dates_between(min(sales_dates).date(), max(sales_dates).date())
    sales_report["cobertura"] = {"dias_calendario": len(calendar), "dias_con_filas": len(daily_counts),
                                 "tienda_dias_con_filas": len(store_days),
                                 "tienda_dias_sin_filas_en_calendario": len(store_ids) * len(calendar) - len(store_days),
                                 "filas_por_dia": distribution(list(daily_counts.values())),
                                 "nota": "Ausencia de venta no demuestra falla de extracción; falta calendario operativo"}
    outliers = []
    for sku, vals in sorted(per_sku_units.items()):
        stats = distribution(vals)
        iqr = stats["p75"] - stats["p25"]
        low, high = stats["p25"] - Decimal("1.5") * iqr, stats["p75"] + Decimal("1.5") * iqr
        outliers.append({"sku": sku, "distribucion_monto_por_unidad_I": stats,
                         "fuera_de_1_5_iqr": sum(v < low or v > high for v in vals)})
    sales_report["diagnostico_por_sku"] = outliers

    stock_keys = defaultdict(list)
    for row in snapshots:
        stock_keys[(row["fecha"], row["tienda_id"], row["sku_erp"])].append(row["cantidad_en_stock"])
    snap_report = profile(snapshots, list(snapshots[0]))
    snap_report["fechas"], stock_dates = date_profile(snapshots, "fecha")
    snap_report["numericos"] = numeric_profile(snapshots, ["cantidad_en_stock"])
    snap_report["valores_no_numericos"] = dict(Counter(str(r["cantidad_en_stock"]) for r in snapshots
                                                      if number(r["cantidad_en_stock"]) is None))
    snap_report["claves_duplicadas"] = sum(len(v) > 1 for v in stock_keys.values())
    snap_report["claves_con_stock_conflictivo"] = sum(len(set(v)) > 1 for v in stock_keys.values())
    snap_report["tiendas_sin_catalogo"] = sorted({r["tienda_id"] for r in snapshots} - store_ids)
    snap_report["skus_sin_catalogo"] = sorted({r["sku_erp"] for r in snapshots} - set(product_by_erp))
    pairs = defaultdict(dict)
    for (day, store, sku), values in stock_keys.items():
        if len(set(values)) == 1:
            pairs[(store, sku)][date.fromisoformat(day)] = values[0]
    gaps, zeros_long = [], []
    for (store, sku), observations in sorted(pairs.items()):
        days = sorted(observations)
        internal_missing = (days[-1] - days[0]).days + 1 - len(days)
        if internal_missing:
            gaps.append({"tienda_id": store, "sku_erp": sku, "dias_ausentes_entre_extremos": internal_missing})
        run_start, previous, length = None, None, 0
        for day in days + [days[-1] + timedelta(days=2)]:
            zero = day in observations and observations[day] == 0
            consecutive = previous is not None and day == previous + timedelta(days=1)
            if length and not (zero and consecutive):
                if length > 3:
                    zeros_long.append({"tienda_id": store, "sku_erp": sku,
                                       "inicio": str(run_start), "fin": str(previous), "dias": length})
                length = 0
            if zero:
                if not length:
                    run_start = day
                length += 1
            previous = day
    stock_calendar = dates_between(min(stock_dates).date(), max(stock_dates).date())
    snap_report["cobertura"] = {"dias_calendario": len(stock_calendar),
                                "dias_con_filas": len({d.date() for d in stock_dates}),
                                "pares_tienda_sku_observados": len(pairs),
                                "pares_con_huecos_internos": len(gaps),
                                "pares_con_cobertura_en_todas_las_fechas": sum(len(v) == len(stock_calendar) for v in pairs.values()),
                                "pares_por_tienda": dict(sorted(Counter(store for store, _ in pairs).items())),
                                "dias_ausentes_internos_total": sum(x["dias_ausentes_entre_extremos"] for x in gaps),
                                "huecos_ejemplos": gaps[:10],
                                "combinaciones_teoricas_si_todas_las_tiendas_vendieran_todo": len(store_ids) * len(products) * len(stock_calendar),
                                "nota": "Universo teórico no equivale a surtido esperado"}
    snap_report["episodios_cero_mas_3_dias_observados"] = {"cantidad": len(zeros_long),
        "tiendas": len({r["tienda_id"] for r in zeros_long}), "ejemplos": zeros_long[:10],
        "nota": "Diagnóstico de todo el período observado; sin rellenar ausencias ni asumir surtido"}
    costs = []
    cost_anomalies = []
    histories = {}
    for product in products:
        history = product.get("cost_history", [])
        entries = []
        for entry in history:
            cost = number(entry.get("costo_mxn"))
            try:
                day = date.fromisoformat(entry["fecha_vigencia"])
            except (ValueError, TypeError):
                day = None
            costs.append({"sku_erp": product["sku_erp"], **entry})
            if day is None or cost is None or cost <= 0:
                cost_anomalies.append(product["sku_erp"])
            if day is not None and cost is not None:
                entries.append((day, cost))
        histories[product["sku_erp"]] = sorted(entries)
    cost_key = defaultdict(list)
    for entry in costs:
        cost_key[(entry["sku_erp"], entry["fecha_vigencia"])].append(entry["costo_mxn"])
    inv_report = {"metadata": inventory["metadata"], "tiendas": len(stores), "productos": len(products),
                  "tiendas_duplicadas": len(stores) - len(store_ids),
                  "productos_duplicados": len(products) - len(product_by_erp),
                  "skus_con_snapshot": len({r["sku_erp"] for r in snapshots}),
                  "tiendas_con_snapshot": len({r["tienda_id"] for r in snapshots}),
                  "categorias": dict(Counter(p["categoria"] for p in products)),
                  "nombres_repetidos": {k: n for k, n in Counter(p["nombre"] for p in products).items() if n > 1},
                  "snapshots": snap_report,
                  "costos": {"entradas": len(costs), "sin_historial": [p["sku_erp"] for p in products if not p.get("cost_history")],
                             "productos_con_fecha_o_costo_invalido": sorted(set(cost_anomalies)),
                             "claves_fecha_repetidas": sum(len(v) > 1 for v in cost_key.values()),
                             "claves_fecha_costos_conflictivos": sum(len(set(v)) > 1 for v in cost_key.values()),
                             "vigencia_min": min(c["fecha_vigencia"] for c in costs),
                             "vigencia_max": max(c["fecha_vigencia"] for c in costs),
                             "distribucion": distribution([number(c["costo_mxn"]) for c in costs if number(c["costo_mxn"]) is not None])}}

    fx_report = profile(fx, fx_columns)
    fx_report["fechas"], fx_dates = date_profile(fx, "fecha")
    fx_report["numericos"] = numeric_profile(fx, ["rate_to_mxn"])
    rate_keys = defaultdict(list)
    for row in fx:
        rate_keys[(row["fecha"], row["currency"])].append(number(row["rate_to_mxn"]))
    fx_report["claves_repetidas"] = sum(len(v) > 1 for v in rate_keys.values())
    fx_report["claves_conflictivas"] = sum(len(set(v)) > 1 for v in rate_keys.values())
    fx_report["por_moneda"] = {}
    for currency in sorted({r["currency"] for r in fx}):
        rates = sorted((date.fromisoformat(r["fecha"]), number(r["rate_to_mxn"])) for r in fx if r["currency"] == currency)
        missing = sorted(set(dates_between(rates[0][0], rates[-1][0])) - {x[0] for x in rates})
        changes = [(day, abs(rate / previous - 1)) for (_, previous), (day, rate) in zip(rates, rates[1:])
                   if rate is not None and previous is not None and previous > 0]
        fx_report["por_moneda"][currency] = {"filas": len(rates), "dias_sin_tasa_entre_extremos": len(missing),
            "distribucion": distribution([x[1] for x in rates if x[1] is not None]),
            "mayor_cambio_relativo_entre_observaciones": max((x[1] for x in changes), default=None)}

    ecom_report = profile(ecommerce, ecommerce_table.column_names, "order_id")
    ecom_report["fechas"], _ = date_profile(ecommerce, "fecha")
    ecom_report["numericos"] = numeric_profile(ecommerce, ["cantidad", "amount"])
    ecom_report["monedas"] = dict(Counter(r["currency"] for r in ecommerce))
    ecom_report["tipos"] = {f.name: str(f.type) for f in ecommerce_table.schema}
    ecom_months, ecom_controls = Counter(), defaultdict(lambda: {"filas": 0, "amount_original": Decimal(0), "amount_mxn_diagnostico": Decimal(0)})
    missing_fx, unavailable_fx = Counter(), 0
    mapped_status = Counter()
    for row in ecommerce:
        dt, _ = parse_date(row["fecha"])
        ecom_months[dt.strftime("%Y-%m")] += 1
        currency, amount = row["currency"], number(row["amount"])
        group = ecom_controls[currency]
        group["filas"] += 1
        if amount is not None:
            group["amount_original"] += amount
        rates = [Decimal(1)] if currency == "MXN" else rate_keys.get((dt.date().isoformat(), currency), [])
        if not rates:
            missing_fx[f"{dt.date()}|{currency}"] += 1
        if not rates or len(set(rates)) != 1 or rates[0] is None or rates[0] <= 0:
            unavailable_fx += 1
        elif amount is not None:
            group["amount_mxn_diagnostico"] += amount * rates[0]
        mapping = map_by_handle.get(row["product_handle"])
        if mapping is None:
            status = "handle_sin_mapeo"
        elif not mapping.get("sku_erp"):
            status = "handle_con_erp_nulo"
        elif mapping["sku_erp"] not in product_by_erp:
            status = "erp_fuera_catalogo"
        else:
            status = "mapeo_exacto_hasta_erp"
        mapped_status[status] += 1
    ecom_report["por_mes_filas"] = dict(sorted(ecom_months.items()))
    ecom_report["controles_por_moneda"] = dict(ecom_controls)
    ecom_report["distribuciones_por_moneda"] = {
        currency: numeric_profile([r for r in ecommerce if r["currency"] == currency], ["cantidad", "amount"])
        for currency in ecom_controls}
    ecom_report["conversion_diagnostica"] = {"regla_propuesta": "amount por rate_to_mxn del día de fecha; MXN identidad, sin redondear antes de sumar",
        "filas_sin_tasa_del_dia": sum(missing_fx.values()), "claves_faltantes": dict(missing_fx),
        "filas_con_conversion_no_disponible": unavailable_fx}
    ecom_report["conciliacion_exacta_filas"] = dict(mapped_status)
    handles_count = Counter(r["product_handle"] for r in ecommerce)
    ecom_report["handles_distintos"] = len(handles_count)
    ecom_report["handles_sin_mapeo"] = {h: n for h, n in sorted(handles_count.items()) if h not in map_by_handle}

    pos_skus = {r["sku"] for r in sales}
    map_report = {"filas": len(mappings), "sin_handle": sum(not m.get("handle") for m in mappings),
                  "sin_erp": [m["sku_pos"] for m in mappings if not m.get("sku_erp")],
                  "pos_sin_fila_mapeo": sorted(pos_skus - set(map_by_pos)),
                  "erp_sin_fila_mapeo": sorted(set(product_by_erp) - {m["sku_erp"] for m in mappings if m.get("sku_erp")}),
                  "erp_mapeados_fuera_catalogo": sorted({m["sku_erp"] for m in mappings if m.get("sku_erp")} - set(product_by_erp)),
                  "duplicados_no_nulos": {c: {k: n for k, n in Counter(m[c] for m in mappings if m.get(c)).items() if n > 1}
                                           for c in ["sku_pos", "sku_erp", "handle"]}}
    physical_status = Counter()
    six_month_stock = Counter()
    stock_start, stock_end = min(stock_dates).date(), max(stock_dates).date()
    margin = {"filas_I": 0, "filas_I_con_costo": 0, "filas_I_sin_costo": 0, "filas_I_margen_negativo": 0,
              "nota": "Solo diagnóstico de mapeo exacto; monto total y costo unitario comparables son supuestos"}
    for row in sales:
        mapping = map_by_pos.get(row["sku"])
        status = "sin_fila_mapeo" if mapping is None else "erp_nulo" if not mapping.get("sku_erp") else "exacto_hasta_erp"
        physical_status[status] += 1
        if row["tipo_comprobante"] != "I":
            continue
        margin["filas_I"] += 1
        dt, _ = parse_date(row["fecha_hora"])
        if stock_start <= dt.date() <= stock_end:
            erp = mapping.get("sku_erp") if mapping else None
            values = stock_keys.get((dt.date().isoformat(), row["tienda_id"], erp))
            if erp is None:
                six_month_stock["sin_relacion_erp"] += 1
            elif values is None:
                six_month_stock["sin_snapshot_del_par_tienda_sku"] += 1
            elif len(set(values)) != 1:
                six_month_stock["snapshot_conflictivo"] += 1
            elif number(values[0]) is None:
                six_month_stock["snapshot_NA_o_no_numerico"] += 1
            else:
                six_month_stock["con_snapshot_numerico"] += 1
                if number(values[0]) == 0:
                    six_month_stock["de_ellos_stock_cero_con_venta_mismo_dia"] += 1
        history = histories.get(mapping.get("sku_erp") if mapping else None, [])
        index = bisect_right([h[0] for h in history], dt.date()) - 1
        if index < 0 or number(row["monto"]) is None or number(row["cantidad"]) is None:
            margin["filas_I_sin_costo"] += 1
            continue
        margin["filas_I_con_costo"] += 1
        if number(row["monto"]) - number(row["cantidad"]) * history[index][1] < 0:
            margin["filas_I_margen_negativo"] += 1
    map_report["filas_sales_por_estado"] = dict(physical_status)
    map_report["diagnostico_margen_exacto"] = margin
    map_report["ventas_I_en_periodo_inventario"] = dict(six_month_stock)

    # Reconciliación de cantidades originales por grupo; no son ventas netas confirmadas.
    sales_report["sensibilidad_monto_total"] = {
        "todos_comprobantes_positivos": sum(g["monto"] for g in per_type.values()),
        "solo_I": per_type.get("I", {}).get("monto", Decimal(0)),
        "I_menos_E": per_type.get("I", {}).get("monto", Decimal(0)) - per_type.get("E", {}).get("monto", Decimal(0)),
        "nota": "Escenarios de clasificación, no decisiones confirmadas"}

    # Identidades de control: fallar si el reporte pierde filas en agrupaciones.
    checks = {
        "sales_por_tipo": sum(g["filas"] for g in per_type.values()) == len(sales),
        "sales_por_mes_mas_fechas_invalidas": sum(g["filas"] for g in per_month.values()) + sales_report["fechas"]["invalidas"] == len(sales),
        "sales_por_mapeo": sum(physical_status.values()) == len(sales),
        "ecommerce_por_mapeo": sum(mapped_status.values()) == len(ecommerce),
        "ecommerce_por_moneda": sum(g["filas"] for g in ecom_controls.values()) == len(ecommerce),
        "snapshots_por_clave": sum(len(v) for v in stock_keys.values()) == len(snapshots),
    }
    if not all(checks.values()):
        raise ValueError(f"Falló conciliación del perfil: {checks}")
    return {"alcance": "EDA de todas las filas; controles y diagnósticos, no respuestas finales de negocio",
            "fuentes": manifest, "sales": sales_report, "inventario": inv_report,
            "ecommerce": ecom_report, "tipos_cambio": fx_report, "mapeos": map_report,
            "controles": checks}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, default=Path("outputs/eda_completo.json"))
    args = parser.parse_args()
    result = explore(Path(__file__).resolve().parents[1])
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"EDA generado: {args.salida}; controles: {result['controles']}")
