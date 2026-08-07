#!/usr/bin/env python3

from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import csv

OUT_DIR = Path("results/homolog_context/uniprot_name_query_overlap")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SUMMARY = Path(
    "results/homolog_context/O67940_uniprot_name_query_overlap_summary.tsv"
)

BASE = (
    "(xref:pfam-PF01887) AND "
    "(xref:pfam-PF20257) AND "
    "(fragment:false) AND "
    "(length:[200 TO 350])"
)

QUERIES = {
    "fluorinase": f"{BASE} AND (protein_name:fluorinase)",
    "chlorinase": f"{BASE} AND (protein_name:chlorinase)",
    "hydrolase": f"{BASE} AND (protein_name:hydrolase)",
}


def fetch_accessions(query):
    url = (
        "https://rest.uniprot.org/uniprotkb/stream?"
        f"query={quote(query)}&format=list"
    )

    request = Request(
        url,
        headers={"User-Agent": "O67940-reproducible-reanalysis"},
    )

    with urlopen(request) as response:
        text = response.read().decode("utf-8")

    return {
        line.strip()
        for line in text.splitlines()
        if line.strip()
    }


sets = {}

for label, query in QUERIES.items():
    accessions = fetch_accessions(query)
    sets[label] = accessions

    out_file = OUT_DIR / f"{label}_accessions.txt"
    out_file.write_text(
        "\n".join(sorted(accessions)) + "\n"
    )

    print(f"{label}: {len(accessions)}")


flu = sets["fluorinase"]
chl = sets["chlorinase"]
hyd = sets["hydrolase"]

rows = [
    ("fluorinase_total", len(flu)),
    ("chlorinase_total", len(chl)),
    ("hydrolase_total", len(hyd)),
    ("fluorinase_and_chlorinase", len(flu & chl)),
    ("fluorinase_and_hydrolase", len(flu & hyd)),
    ("chlorinase_and_hydrolase", len(chl & hyd)),
    ("all_three", len(flu & chl & hyd)),
    ("fluorinase_only", len(flu - chl - hyd)),
    ("chlorinase_only", len(chl - flu - hyd)),
    ("hydrolase_only", len(hyd - flu - chl)),
]

with SUMMARY.open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["comparison", "count"])
    writer.writerows(rows)

print(f"Wrote overlap summary to {SUMMARY}")
