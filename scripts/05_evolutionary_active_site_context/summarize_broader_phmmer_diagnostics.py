#!/usr/bin/env python3

from pathlib import Path
import csv


INPUT = Path(
    "results/homolog_context/broader_phmmer/"
    "O67940_vs_uniprot_pfam_candidates_phmmer_ranked.tsv"
)

OUT_DIR = Path("results/homolog_context/broader_phmmer")
OUT_DIR.mkdir(parents=True, exist_ok=True)

COVERAGE_OUT = OUT_DIR / "O67940_broader_phmmer_coverage_summary.tsv"
ANCHOR_OUT = OUT_DIR / "O67940_broader_phmmer_reviewed_anchor_summary.tsv"
RANK_OUT = OUT_DIR / "O67940_broader_phmmer_rank_checkpoints.tsv"


with INPUT.open() as handle:
    all_rows = list(csv.DictReader(handle, delimiter="\t"))

rows = [
    row for row in all_rows
    if row["is_query_self"] == "no"
]


def percentile(values, p):
    values = sorted(values)
    i = round((len(values) - 1) * p)
    return values[i]


# ---------------------------------------------------------
# 1. Coverage / score distribution summary
# ---------------------------------------------------------

qcov = [float(r["query_coverage"]) for r in rows]
tcov = [float(r["target_coverage"]) for r in rows]
scores = [float(r["full_score"]) for r in rows]

coverage_rows = []

for metric_name, values in [
    ("query_coverage", qcov),
    ("target_coverage", tcov),
    ("full_score", scores),
]:
    for p in [0, 0.10, 0.25, 0.50, 0.75, 0.90, 1.00]:
        coverage_rows.append({
            "summary_type": "percentile",
            "metric": metric_name,
            "threshold_or_percentile": f"{p:.2f}",
            "count_or_value": f"{percentile(values, p):.4f}",
        })

for cutoff in [0.70, 0.80, 0.90, 0.95]:
    n = sum(
        1 for r in rows
        if float(r["query_coverage"]) >= cutoff
        and float(r["target_coverage"]) >= cutoff
    )

    coverage_rows.append({
        "summary_type": "joint_coverage_count",
        "metric": "query_and_target_coverage",
        "threshold_or_percentile": f"{cutoff:.2f}",
        "count_or_value": str(n),
    })

domain_counts = {}

for r in rows:
    n = int(r["reported_domain_count"])
    domain_counts[n] = domain_counts.get(n, 0) + 1

for domain_count in sorted(domain_counts):
    coverage_rows.append({
        "summary_type": "reported_domain_count",
        "metric": "domain_count",
        "threshold_or_percentile": str(domain_count),
        "count_or_value": str(domain_counts[domain_count]),
    })

with COVERAGE_OUT.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "summary_type",
            "metric",
            "threshold_or_percentile",
            "count_or_value",
        ],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(coverage_rows)


# ---------------------------------------------------------
# 2. Reviewed-anchor diagnostic
# ---------------------------------------------------------

reviewed_accessions = {
    "O58212",
    "Q5SLF5",
    "Q70GK9",
    "A0A1G9FQX8",
    "W0W999",
    "R4LHX8",
    "W8JNL4",
    "A4X3Q0",
    "A4X4S2",
    "A8M783",
    "Q59045",
}

anchor_rows = [
    row for row in rows
    if row["accession"] in reviewed_accessions
]

anchor_rows.sort(key=lambda r: float(r["full_evalue"]))

anchor_fields = [
    "accession",
    "entry_name",
    "full_evalue",
    "full_score",
    "query_coverage",
    "target_coverage",
    "reported_domain_count",
    "reviewed",
    "protein_names",
    "organism",
]

with ANCHOR_OUT.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=anchor_fields,
        delimiter="\t",
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(anchor_rows)


# ---------------------------------------------------------
# 3. Rank checkpoints
# ---------------------------------------------------------

rank_points = [10, 25, 50, 100, 250, 500, 861, 1000, 2000, len(rows)]

rank_rows = []

for rank in rank_points:
    row = rows[rank - 1]

    rank_rows.append({
        "rank": rank,
        "accession": row["accession"],
        "entry_name": row["entry_name"],
        "full_evalue": row["full_evalue"],
        "full_score": row["full_score"],
        "query_coverage": row["query_coverage"],
        "target_coverage": row["target_coverage"],
        "organism": row["organism"],
    })

with RANK_OUT.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "rank",
            "accession",
            "entry_name",
            "full_evalue",
            "full_score",
            "query_coverage",
            "target_coverage",
            "organism",
        ],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(rank_rows)


print(f"Non-self candidates: {len(rows)}")
print(f"Reviewed anchors recovered: {len(anchor_rows)} / 11")
print(f"Wrote: {COVERAGE_OUT}")
print(f"Wrote: {ANCHOR_OUT}")
print(f"Wrote: {RANK_OUT}")
