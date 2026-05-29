from pathlib import Path
import csv

IN_PATH = Path("results/evidence_integration/evidence_integration_table.tsv")
OUT_PATH = Path("results/evidence_integration/evidence_integration_table_short.tsv")

with IN_PATH.open() as f:
    reader = csv.DictReader(f, delimiter="\t")
    rows = list(reader)

with OUT_PATH.open("w") as out:
    fieldnames = ["evidence_layer", "main_result", "interpretation", "main_limitation"]
    writer = csv.DictWriter(out, delimiter="\t", fieldnames=fieldnames)
    writer.writeheader()

    for row in rows:
        writer.writerow({
            "evidence_layer": row["evidence_layer"],
            "main_result": row["result"],
            "interpretation": row["supports"],
            "main_limitation": row["limitation_or_caution"],
        })

print(f"Wrote short evidence table to {OUT_PATH}")
