"""Perfil de sales.csv sin modificar la fuente ni aplicar reglas de negocio."""

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


def parse_fecha(value):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError(f"Formato de fecha no admitido: {value!r}")


def perfil_sales(path):
    raw = path.read_bytes()
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        columns = reader.fieldnames
        rows = list(reader)
    nulls = {col: sum(not (r.get(col) or "").strip() for r in rows) for col in columns}
    ids = Counter(r["venta_id"] for r in rows)
    signatures = Counter(tuple(r.get(c) for c in columns) for r in rows)
    dates, invalid_dates = [], 0
    groups = defaultdict(lambda: {"filas": 0, "cantidad_negativa": 0, "cantidad_cero": 0,
                                  "monto_negativo": 0, "monto_cero": 0,
                                  "cantidad_invalida": 0, "monto_invalido": 0,
                                  "signos_opuestos": 0, "suma_monto_original": Decimal(0)})
    months = Counter()
    for row in rows:
        try:
            date = parse_fecha(row["fecha_hora"])
            dates.append(date)
            months[date.strftime("%Y-%m")] += 1
        except ValueError:
            invalid_dates += 1
        group = groups[(row["tipo_comprobante"], row["moneda"])]
        group["filas"] += 1
        numbers = {}
        for col in ("cantidad", "monto"):
            try:
                value = Decimal(row[col])
                if not value.is_finite():
                    raise InvalidOperation
                numbers[col] = value
                group[f"{col}_negativ{'a' if col == 'cantidad' else 'o'}"] += value < 0
                group[f"{col}_cero"] += value == 0
                if col == "monto":
                    group["suma_monto_original"] += value
            except InvalidOperation:
                group[f"{col}_invalid{'a' if col == 'cantidad' else 'o'}"] += 1
        if len(numbers) == 2:
            group["signos_opuestos"] += numbers["cantidad"] * numbers["monto"] < 0
    return {
        "archivo": path.name, "sha256": hashlib.sha256(raw).hexdigest(),
        "filas": len(rows), "columnas": columns, "vacios_por_columna": nulls,
        "ids_distintos": len(ids), "ids_repetidos": sum(n > 1 for n in ids.values()),
        "filas_extra_por_id_repetido": sum(n - 1 for n in ids.values()),
        "duplicados_exactos_extra": sum(n - 1 for n in signatures.values()),
        "fecha_min": min(dates).isoformat(sep=" ") if dates else None,
        "fecha_max": max(dates).isoformat(sep=" ") if dates else None,
        "fechas_invalidas": invalid_dates,
        "tiendas_distintas": len({r["tienda_id"] for r in rows}),
        "skus_distintos": len({r["sku"] for r in rows}),
        "filas_por_mes": dict(sorted(months.items())),
        "por_tipo_y_moneda": [dict(tipo_comprobante=t, moneda=m, **g)
                              for (t, m), g in sorted(groups.items())],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archivo", nargs="?", type=Path,
                        default=Path(__file__).resolve().parents[1] / "datos" / "sales.csv")
    args = parser.parse_args()
    print(json.dumps(perfil_sales(args.archivo), ensure_ascii=False, indent=2, default=str))
