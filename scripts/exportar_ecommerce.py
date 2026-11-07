"""Exporta Parquet a CSV de consulta sin modificar la fuente original."""

import argparse
import csv
import hashlib
import json
from datetime import date, datetime
from pathlib import Path

import pyarrow.parquet as pq


def texto_csv(value):
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, default=str)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return str(value)


def exportar(source, destination):
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    table = pq.read_table(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(table.column_names)
        for batch in table.to_batches(max_chunksize=10000):
            for row in batch.to_pylist():
                writer.writerow([texto_csv(row[col]) for col in table.column_names])
    # Verifica todos los valores serializados, además del conteo y encabezado.
    with destination.open(encoding="utf-8-sig", newline="") as output:
        reader = csv.reader(output)
        if next(reader) != table.column_names:
            raise ValueError("El encabezado CSV difiere del origen")
        count = 0
        for batch in table.to_batches(max_chunksize=10000):
            for row in batch.to_pylist():
                if next(reader, None) != [texto_csv(row[col]) for col in table.column_names]:
                    raise ValueError(f"La fila {count + 1} difiere de la serialización esperada")
                count += 1
        if next(reader, None) is not None or count != table.num_rows:
            raise ValueError("El conteo CSV difiere del origen")
    if hashlib.sha256(source.read_bytes()).hexdigest() != before:
        raise ValueError("La fuente cambió durante la exportación")
    print(json.dumps({"csv": str(destination), "filas": count, "columnas": table.column_names,
                      "sha256_parquet": before, "verificacion": "Todas las filas verificadas"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origen", type=Path, default=root / "datos/ecommerce_orders.parquet")
    parser.add_argument("--destino", type=Path, default=root / "outputs/ecommerce_orders.csv")
    args = parser.parse_args()
    if args.origen.resolve() == args.destino.resolve():
        parser.error("Origen y destino deben ser diferentes")
    exportar(args.origen, args.destino)
