#!/usr/bin/env python3

from pathlib import Path
from urllib.request import Request, urlopen
import csv
import json
import time


OUTLIERS = Path(
    "results/homolog_context/"
    "O67940_uniprot_non_bacteria_archaea_candidates.tsv"
)

PHMMER = Path(
    "results/homolog_context/broader_phmmer/"
    "O67940_vs_uniprot_pfam_candidates_phmmer_ranked.tsv"
)

OUT = Path(
    "results/homolog_context/"
    "O67940_non_prokaryotic_candidate_enriched_audit.tsv"
)


with OUTLIERS.open() as handle:
    outlier_rows = list(
        csv.DictReader(handle, delimiter="\t")
    )

with PHMMER.open() as handle:
    phmmer_rows = list(
        csv.DictReader(handle, delimiter="\t")
    )


nonself = [
    row
    for row in phmmer_rows
    if row["is_query_self"] == "no"
]

rank_lookup = {
    row["accession"]: rank
    for rank, row in enumerate(nonself, start=1)
}

phmmer_lookup = {
    row["accession"]: row
    for row in nonself
}


rows = []

for i, record in enumerate(outlier_rows, start=1):
    accession = record["Entry"]

    url = (
        "https://rest.uniprot.org/"
        f"uniprotkb/{accession}.json"
    )

    request = Request(
        url,
        headers={
            "User-Agent":
            "O67940-reproducible-reanalysis"
        },
    )

    with urlopen(request) as response:
        data = json.load(response)

    organism = data.get("organism", {})

    lineage = organism.get("lineage", [])

    protein_existence = data.get(
        "proteinExistence", ""
    )

    annotation_score = data.get(
        "annotationScore", ""
    )

    sequence = data.get("sequence", {})

    ph = phmmer_lookup[accession]

    rows.append({
        "accession": accession,
        "entry_name": record["Entry Name"],
        "organism": record["Organism"],
        "organism_id": record["Organism (ID)"],
        "lineage": "; ".join(lineage),
        "reviewed": record["Reviewed"],
        "protein_name": record["Protein names"],
        "gene_names": record["Gene Names"],
        "protein_existence": protein_existence,
        "annotation_score": annotation_score,
        "sequence_length": sequence.get(
            "length", ""
        ),
        "phmmer_rank": rank_lookup[accession],
        "full_evalue": ph["full_evalue"],
        "full_score": ph["full_score"],
        "query_coverage": ph["query_coverage"],
        "target_coverage": ph["target_coverage"],
        "reported_domain_count":
            ph["reported_domain_count"],
        "uniprot_record_url": url,
    })

    print(
        f"[{i}/{len(outlier_rows)}] "
        f"{accession}"
    )

    time.sleep(0.2)


fields = [
    "accession",
    "entry_name",
    "organism",
    "organism_id",
    "lineage",
    "reviewed",
    "protein_name",
    "gene_names",
    "protein_existence",
    "annotation_score",
    "sequence_length",
    "phmmer_rank",
    "full_evalue",
    "full_score",
    "query_coverage",
    "target_coverage",
    "reported_domain_count",
    "uniprot_record_url",
]


with OUT.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=fields,
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(rows)


print()
print(f"Wrote {len(rows)} records to {OUT}")
