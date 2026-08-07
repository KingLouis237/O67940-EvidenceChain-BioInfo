#!/usr/bin/env python3

from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import csv


METADATA = Path(
    "data/databases/O67940_uniprot_pfam_candidates/"
    "candidate_metadata.tsv"
)

OUT = Path(
    "results/homolog_context/"
    "O67940_uniprot_non_bacteria_archaea_candidates.tsv"
)

BASE = (
    "(xref:pfam-PF01887) AND "
    "(xref:pfam-PF20257) AND "
    "(fragment:false) AND "
    "(length:[200 TO 350])"
)


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


# Read the exact accession universe from the frozen metadata snapshot.
with METADATA.open() as handle:
    metadata_rows = list(
        csv.DictReader(handle, delimiter="\t")
    )

all_accessions = {
    row["Entry"]
    for row in metadata_rows
}

bacteria = fetch_accessions(
    f"{BASE} AND (taxonomy_id:2)"
)

archaea = fetch_accessions(
    f"{BASE} AND (taxonomy_id:2157)"
)

other = all_accessions - bacteria - archaea


selected = [
    row
    for row in metadata_rows
    if row["Entry"] in other
]

selected.sort(
    key=lambda row: (
        row["Organism"],
        row["Entry"],
    )
)


fields = [
    "Entry",
    "Entry Name",
    "Reviewed",
    "Protein names",
    "Gene Names",
    "Organism",
    "Organism (ID)",
    "Length",
]

with OUT.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=fields,
        delimiter="\t",
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(selected)


print(f"All candidates: {len(all_accessions)}")
print(f"Bacteria: {len(bacteria)}")
print(f"Archaea: {len(archaea)}")
print(f"Neither Bacteria nor Archaea: {len(other)}")
print(f"Wrote: {OUT}")

if len(other) != len(selected):
    raise SystemExit(
        "ERROR: accession/metadata mismatch for outlier set"
    )
