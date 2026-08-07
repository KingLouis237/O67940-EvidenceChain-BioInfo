#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
import csv


TBL = Path(
    "results/homolog_context/broader_phmmer/"
    "O67940_vs_uniprot_pfam_candidates_phmmer.tblout"
)

DOMTBL = Path(
    "results/homolog_context/broader_phmmer/"
    "O67940_vs_uniprot_pfam_candidates_phmmer.domtblout"
)

METADATA = Path(
    "data/databases/O67940_uniprot_pfam_candidates/"
    "candidate_metadata.tsv"
)

OUT = Path(
    "results/homolog_context/broader_phmmer/"
    "O67940_vs_uniprot_pfam_candidates_phmmer_ranked.tsv"
)


def accession_from_target(target):
    parts = target.split("|")
    if len(parts) >= 2:
        return parts[1]
    return target


def interval_union_length(intervals):
    if not intervals:
        return 0

    intervals = sorted(intervals)
    merged = [list(intervals[0])]

    for start, end in intervals[1:]:
        if start <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return sum(end - start + 1 for start, end in merged)


metadata = {}

with METADATA.open() as handle:
    reader = csv.DictReader(handle, delimiter="\t")

    for row in reader:
        metadata[row["Entry"]] = row


sequence_hits = {}

for line in TBL.read_text().splitlines():
    if not line.strip() or line.startswith("#"):
        continue

    parts = line.split(maxsplit=18)

    target = parts[0]
    accession = accession_from_target(target)

    sequence_hits[accession] = {
        "target_id": target,
        "full_evalue": float(parts[4]),
        "full_score": float(parts[5]),
        "full_bias": float(parts[6]),
        "best_domain_evalue_tblout": float(parts[7]),
        "best_domain_score_tblout": float(parts[8]),
        "description_tblout": parts[18] if len(parts) > 18 else "",
    }


domains = defaultdict(list)

for line in DOMTBL.read_text().splitlines():
    if not line.strip() or line.startswith("#"):
        continue

    parts = line.split(maxsplit=22)

    target = parts[0]
    accession = accession_from_target(target)

    domains[accession].append({
        "target_length": int(parts[2]),
        "query_length": int(parts[5]),
        "domain_number": int(parts[9]),
        "domain_of": int(parts[10]),
        "conditional_evalue": float(parts[11]),
        "independent_evalue": float(parts[12]),
        "domain_score": float(parts[13]),
        "query_from": int(parts[15]),
        "query_to": int(parts[16]),
        "target_from": int(parts[17]),
        "target_to": int(parts[18]),
        "env_from": int(parts[19]),
        "env_to": int(parts[20]),
        "accuracy": float(parts[21]),
    })


rows = []

for accession, hit in sequence_hits.items():
    drows = domains.get(accession, [])

    if not drows:
        continue

    best = min(
        drows,
        key=lambda d: (
            d["independent_evalue"],
            -d["domain_score"],
        ),
    )

    q_intervals = [
        (d["query_from"], d["query_to"])
        for d in drows
    ]

    t_intervals = [
        (d["target_from"], d["target_to"])
        for d in drows
    ]

    query_union = interval_union_length(q_intervals)
    target_union = interval_union_length(t_intervals)

    query_length = best["query_length"]
    target_length = best["target_length"]

    qcov = query_union / query_length
    tcov = target_union / target_length

    meta = metadata.get(accession, {})

    rows.append({
        "accession": accession,
        "target_id": hit["target_id"],
        "is_query_self": "yes" if accession == "O67940" else "no",
        "full_evalue": hit["full_evalue"],
        "full_score": hit["full_score"],
        "full_bias": hit["full_bias"],
        "domain_rows": len(drows),
        "reported_domain_count": max(d["domain_of"] for d in drows),
        "best_domain_evalue": best["independent_evalue"],
        "best_domain_score": best["domain_score"],
        "query_length": query_length,
        "target_length": target_length,
        "query_union_aligned_residues": query_union,
        "target_union_aligned_residues": target_union,
        "query_coverage": f"{qcov:.4f}",
        "target_coverage": f"{tcov:.4f}",
        "reviewed": meta.get("Reviewed", ""),
        "entry_name": meta.get("Entry Name", ""),
        "protein_names": meta.get("Protein names", ""),
        "gene_names": meta.get("Gene Names", ""),
        "organism": meta.get("Organism", ""),
        "organism_id": meta.get("Organism (ID)", ""),
        "metadata_length": meta.get("Length", ""),
    })


rows.sort(
    key=lambda row: (
        row["is_query_self"] != "yes",
        row["full_evalue"],
        -row["full_score"],
    )
)


fieldnames = [
    "accession",
    "target_id",
    "is_query_self",
    "full_evalue",
    "full_score",
    "full_bias",
    "domain_rows",
    "reported_domain_count",
    "best_domain_evalue",
    "best_domain_score",
    "query_length",
    "target_length",
    "query_union_aligned_residues",
    "target_union_aligned_residues",
    "query_coverage",
    "target_coverage",
    "reviewed",
    "entry_name",
    "protein_names",
    "gene_names",
    "organism",
    "organism_id",
    "metadata_length",
]


with OUT.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=fieldnames,
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(rows)


print(f"Wrote {len(rows)} ranked PHMMER hits to {OUT}")

self_hits = sum(
    1 for row in rows
    if row["is_query_self"] == "yes"
)

print(f"Self hits: {self_hits}")
print(f"Non-self candidates: {len(rows) - self_hits}")
