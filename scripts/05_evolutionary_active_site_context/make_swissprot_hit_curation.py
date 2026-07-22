#!/usr/bin/env python3

import csv
from collections import defaultdict
from pathlib import Path

parsed_hits = Path("results/homolog_context/O67940_vs_swissprot_jackhmmer_N5.parsed_hits.tsv")
domain_summary = Path("results/homolog_context/O67940_vs_swissprot_jackhmmer_N5.domain_summary.tsv")
out_path = Path("results/homolog_context/O67940_vs_swissprot_jackhmmer_N5.initial_curation.tsv")

domain_counts = defaultdict(int)
domain_spans = defaultdict(list)

with domain_summary.open() as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    for row in reader:
        target = row["target"]
        domain_counts[target] += 1
        domain_spans[target].append(
            f"hmm:{row['hmm_from']}-{row['hmm_to']};ali:{row['ali_from']}-{row['ali_to']}"
        )

def classify_hit(target_id, description, domain_count):
    desc = description.lower()

    if "sall" in target_id.lower() or "adenosyl-chloride synthase" in desc:
        return (
            "SalL_chlorinase_related",
            "single_domain_match" if domain_count == 1 else "multi_domain_match",
            "include",
            "SalL/chlorinase-related reviewed hit; important reference, but not proof of O67940 substrate specificity",
        )

    if "fluorinase" in desc:
        return (
            "fluorinase",
            "split_domain_match" if domain_count > 1 else "single_domain_match",
            "include_with_caution",
            "reviewed fluorinase hit; kept because it is relevant, but domain segmentation must be considered",
        )

    if "s-adenosyl-l-methionine hydrolase" in desc:
        return (
            "SAM_hydrolase",
            "single_domain_match" if domain_count == 1 else "multi_domain_match",
            "include",
            "reviewed SAM hydrolase-like hit with broad domain-level similarity",
        )

    return (
        "other",
        "needs_manual_review",
        "review",
        "annotation did not match the expected Swiss-Prot hit categories",
    )

rows = []

with parsed_hits.open() as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    for row in reader:
        target = row["target_id"]
        accession = target.split("|")[1] if "|" in target else target
        short_name = target.split("|")[2] if target.count("|") >= 2 else target
        dcount = domain_counts.get(target, 0)

        group, domain_pattern, decision, rationale = classify_hit(
            target,
            row["description"],
            dcount,
        )

        rows.append({
            "target_id": target,
            "accession": accession,
            "short_name": short_name,
            "annotation_group": group,
            "domain_count": dcount,
            "domain_pattern": domain_pattern,
            "full_evalue": row["full_evalue"],
            "full_score": row["full_score"],
            "best_domain_evalue": row["best_domain_evalue"],
            "best_domain_score": row["best_domain_score"],
            "curation_decision": decision,
            "curation_rationale": rationale,
            "domain_spans": " | ".join(domain_spans.get(target, [])),
            "description": row["description"],
        })

fieldnames = [
    "target_id",
    "accession",
    "short_name",
    "annotation_group",
    "domain_count",
    "domain_pattern",
    "full_evalue",
    "full_score",
    "best_domain_evalue",
    "best_domain_score",
    "curation_decision",
    "curation_rationale",
    "domain_spans",
    "description",
]

with out_path.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} curated Swiss-Prot hits to {out_path}")
