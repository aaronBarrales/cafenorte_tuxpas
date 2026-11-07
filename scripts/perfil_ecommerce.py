"""Perfila órdenes y concilia handles exactos sin exponer datos de clientes."""

import json
from collections import Counter
from pathlib import Path

import pyarrow.parquet as pq


def perfil_ecommerce(root):
    table = pq.read_table(root / "datos/ecommerce_orders.parquet")
    mappings = json.loads((root / "datos/inventory.json").read_text(encoding="utf-8-sig"))["sku_mappings"]
    known = {m["handle"] for m in mappings if m.get("handle")}
    handles = Counter(table["product_handle"].to_pylist())
    unknown = {h: n for h, n in handles.items() if h not in known}
    dates = table["fecha"].to_pylist()
    return {
        "filas": table.num_rows,
        "columnas": [{"nombre": f.name, "tipo": str(f.type), "nulos": table[f.name].null_count}
                     for f in table.schema],
        "handles_distintos": len(handles),
        "handles_con_mapeo_exacto": len(set(handles) & known),
        "filas_con_mapeo_exacto": sum(n for h, n in handles.items() if h in known),
        "filas_sin_mapeo_exacto": sum(unknown.values()),
        "handles_sin_mapeo_exacto": unknown,
        "monedas": dict(Counter(table["currency"].to_pylist())),
        "fecha_min_texto": min(dates), "fecha_max_texto": max(dates),
    }


if __name__ == "__main__":
    print(json.dumps(perfil_ecommerce(Path(__file__).resolve().parents[1]),
                     ensure_ascii=False, indent=2))
