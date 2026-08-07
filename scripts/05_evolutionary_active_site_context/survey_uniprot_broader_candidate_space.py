#!/usr/bin/env python3

from urllib.parse import quote
from urllib.request import Request, urlopen
from pathlib import Path
import csv

out_path = Path("results/homolog_context/O67940_uniprot_pfam_broader_candidate_space_survey.tsv")

base = "(xref:pfam-PF01887) AND (xref:pfam-PF20257) AND (fragment:false)"

queries = [
    ("pfam_both_len_200_350_all", f"{base} AND (length:[200 TO 350])"),
    ("pfam_both_len_200_350_reviewed", f"{base} AND (length:[200 TO 350]) AND (reviewed:true)"),
    ("pfam_both_len_200_350_unreviewed", f"{base} AND (length:[200 TO 350]) AND (reviewed:false)"),
    ("pfam_both_len_220_320_all", f"{base} AND (length:[220 TO 320])"),
    ("pfam_both_len_230_310_all", f"{base} AND (length:[230 TO 310])"),
    ("pfam_both_len_200_350_bacteria", f"{base} AND (length:[200 TO 350]) AND (taxonomy_id:2)"),
    ("pfam_both_len_200_350_archaea", f"{base} AND (length:[200 TO 350]) AND (taxonomy_id:2157)"),
    ("pfam_both_len_200_350_fluorinase_name", f"{base} AND (length:[200 TO 350]) AND (protein_name:fluorinase)"),
    ("pfam_both_len_200_350_chlorinase_name", f"{base} AND (length:[200 TO 350]) AND (protein_name:chlorinase)"),
    ("pfam_both_len_200_350_hydrolase_name", f"{base} AND (length:[200 TO 350]) AND (protein_name:hydrolase)"),
]

rows = []

for label, query in queries:
    url = (
        "https://rest.uniprot.org/uniprotkb/search?"
        f"query={quote(query)}&format=tsv&size=1&fields=accession"
    )

    request = Request(url, headers={"User-Agent": "O67940-reproducible-reanalysis"})
    with urlopen(request) as response:
        count = response.headers.get("x-total-results", "")

    rows.append({
        "label": label,
        "count": count,
        "query": query,
    })

with out_path.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=["label", "count", "query"], delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} survey rows to {out_path}")
