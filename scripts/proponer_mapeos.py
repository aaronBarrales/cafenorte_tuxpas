"""Propone candidatos por nombre y sufijo sin modificar mapeos ni aplicarlos."""

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import pyarrow.parquet as pq


def normalizar(text):
    text = "".join(c for c in unicodedata.normalize("NFKD", text.lower())
                   if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def separa_handle(handle):
    match = re.fullmatch(r"(.+)-(\d{3})", handle)
    return (normalizar(match[1]), match[2]) if match else (None, None)


def candidato(product, name, number):
    match = re.fullmatch(r"ERP-PROV-MX-(\d{3})-[A-Z]", product["sku_erp"])
    return (name is not None and number is not None and match is not None
            and normalizar(product["nombre"]) == name and match[1] == number)


def proponer(root):
    inventory = json.loads((root / "datos/inventory.json").read_text(encoding="utf-8-sig"))
    products = inventory["catalogo"]["productos"]
    mappings = inventory["sku_mappings"]
    handles = Counter(pq.read_table(root / "datos/ecommerce_orders.parquet",
                                   columns=["product_handle"])["product_handle"].to_pylist())
    known = {m["handle"] for m in mappings if m.get("handle")}
    controls = []
    incomplete = []
    for mapping in mappings:
        if not mapping.get("handle"):
            continue
        name, number = separa_handle(mapping["handle"])
        matches = [p for p in products if candidato(p, name, number)]
        if not mapping.get("sku_erp"):
            incomplete.append({"sku_pos": mapping.get("sku_pos"), "handle": mapping["handle"],
                               "candidatos_erp": [p["sku_erp"] for p in matches]})
            continue
        controls.append(len(matches) == 1 and matches[0]["sku_erp"] == mapping.get("sku_erp"))
    proposals = []
    for handle, count in sorted(handles.items()):
        if handle in known:
            continue
        name, number = separa_handle(handle)
        matches = [p for p in products if candidato(p, name, number)]
        proposals.append({
            "handle": handle, "filas": count,
            "productos_con_igual_nombre": sum(normalizar(p["nombre"]) == name for p in products),
            "candidatos_por_nombre_y_sufijo": [
                {"sku_erp": p["sku_erp"], "nombre": p["nombre"],
                 "mapeos_existentes": [m for m in mappings if m.get("sku_erp") == p["sku_erp"]]}
                for p in matches],
            "estado": "propuesto_pendiente_de_validacion",
        })
    return {"regla": "nombre normalizado y número de tres dígitos del SKU ERP",
            "controles_con_handle_y_erp_informados": len(controls),
            "controles_coincidentes": sum(controls),
            "mapeos_con_handle_pero_sin_erp": incomplete, "propuestas": proposals}


if __name__ == "__main__":
    print(json.dumps(proponer(Path(__file__).resolve().parents[1]), ensure_ascii=False, indent=2))
