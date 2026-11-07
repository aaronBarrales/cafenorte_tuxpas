"""Contrasta el reporte exploratorio con controles independientes de las fuentes."""

import csv
import hashlib
import json
import re
from collections import Counter
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pyarrow.parquet as pq

from perfil_sales import parse_fecha


def validar(root):
    report = json.loads((root / "outputs/eda_completo.json").read_text(encoding="utf-8"))
    with (root / "datos/sales.csv").open(encoding="utf-8-sig", newline="") as f:
        sales = list(csv.DictReader(f))
    inv = json.loads((root / "datos/inventory.json").read_text(encoding="utf-8-sig"))
    table = pq.read_table(root / "datos/ecommerce_orders.parquet")
    checks = {}
    checks["fuentes_sin_cambios"] = all(
        hashlib.sha256((root / "datos" / name).read_bytes()).hexdigest() == entry["sha256"]
        for name, entry in report["fuentes"].items())
    checks["conteos_por_fuente"] = (len(sales) == report["sales"]["filas"]
        and len(inv["snapshots"]) == report["inventario"]["snapshots"]["filas"]
        and table.num_rows == report["ecommerce"]["filas"])
    checks["importe_original_sales"] = sum(Decimal(r["monto"]) for r in sales) == Decimal(
        report["sales"]["sensibilidad_monto_total"]["todos_comprobantes_positivos"])
    checks["NA_distinto_de_cero"] = sum(r["cantidad_en_stock"] == "N/A" for r in inv["snapshots"]) == (
        report["inventario"]["snapshots"]["numericos"]["cantidad_en_stock"]["invalidos"])
    # Método alternativo al recorrido de rachas: conjuntos de claves cero y ventanas de cuatro días.
    zeros = {(date.fromisoformat(r["fecha"]), r["tienda_id"], r["sku_erp"])
             for r in inv["snapshots"] if r["cantidad_en_stock"] == 0}
    starts = {(day, store, sku) for day, store, sku in zeros
              if (day - timedelta(days=1), store, sku) not in zeros
              and all((day + timedelta(days=n), store, sku) in zeros for n in (1, 2, 3))}
    checks["episodios_cero_por_metodo_independiente"] = len(starts) == report["inventario"]["snapshots"][
        "episodios_cero_mas_3_dias_observados"]["cantidad"]
    pairs = Counter((r["tienda_id"], r["sku_erp"]) for r in inv["snapshots"])
    observed_days = [date.fromisoformat(r["fecha"]) for r in inv["snapshots"]]
    span = (max(observed_days) - min(observed_days)).days + 1
    checks["cobertura_pares"] = (len(pairs) == report["inventario"]["snapshots"]["cobertura"][
        "pares_tienda_sku_observados"] and sum(n == span for n in pairs.values()) ==
        report["inventario"]["snapshots"]["cobertura"]["pares_con_cobertura_en_todas_las_fechas"])
    checks["compatibilidad_fechas_sin_inventar_precision"] = (
        parse_fecha("2024-10-01 08:24:57") == datetime(2024, 10, 1, 8, 24, 57)
        and parse_fecha("01/10/2024 08:24") == datetime(2024, 10, 1, 8, 24))
    try:
        parse_fecha("31/02/2026 08:00")
        checks["rechazo_fecha_imposible"] = False
    except ValueError:
        checks["rechazo_fecha_imposible"] = True
    row = next(r for r in sales if r["venta_id"] == "V00000000")
    product = next(p for p in inv["catalogo"]["productos"] if p["sku_erp"] == "ERP-PROV-MX-015-D")
    eligible = [h for h in product["cost_history"] if date.fromisoformat(h["fecha_vigencia"]) <= parse_fecha(row["fecha_hora"]).date()]
    cost = Decimal(str(max(eligible, key=lambda h: h["fecha_vigencia"])["costo_mxn"]))
    checks["caso_margen_con_costo_vigente"] = Decimal(row["monto"]) - Decimal(row["cantidad"]) * cost == Decimal("-111.13")
    questions = re.findall(r"\| (Q\d{2}) \|", (root / "PREGUNTAS_CLIENTE.md").read_text(encoding="utf-8"))
    checks["60_preguntas_sin_ids_repetidos"] = len(questions) == 60 and set(questions) == {f"Q{i:02}" for i in range(1, 61)}
    if not all(checks.values()):
        raise ValueError(f"Fallaron controles: {checks}")
    print(json.dumps(checks, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    validar(Path(__file__).resolve().parents[1])
