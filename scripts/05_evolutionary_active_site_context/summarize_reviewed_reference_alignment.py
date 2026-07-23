#!/usr/bin/env python3

from pathlib import Path
import csv

alignment_path = Path("results/sequence_alignment/O67940_reviewed_swissprot_reference_set_mafft_alignment.fasta")
out_path = Path("results/sequence_alignment/O67940_reviewed_swissprot_alignment_summary.tsv")


def read_fasta(path):
    records = {}
    header = None
    seq_parts = []

    for line in path.read_text().splitlines():
        if line.startswith(">"):
            if header is not None:
                records[header] = "".join(seq_parts)
            header = line[1:]
            seq_parts = []
        else:
            seq_parts.append(line.strip())

    if header is not None:
        records[header] = "".join(seq_parts)

    return records


def get_field(header, field_name):
    marker = f"{field_name}="
    for part in header.split("|"):
        part = part.strip()
        if part.startswith(marker):
            return part.replace(marker, "", 1)
    return ""


records = read_fasta(alignment_path)

query_header = next(
    h for h in records
    if h.startswith("O67940_AQUAE_AlphaFold_chainA")
)

query_seq = records[query_header]

rows = []

for header, seq in records.items():
    if header == query_header:
        continue

    label = header.split("|")[0].strip()

    compared = 0
    identical = 0
    query_gap_only = 0
    target_gap_only = 0
    both_gap = 0

    for q_res, t_res in zip(query_seq, seq):
        if q_res == "-" and t_res == "-":
            both_gap += 1
        elif q_res == "-":
            query_gap_only += 1
        elif t_res == "-":
            target_gap_only += 1
        else:
            compared += 1
            if q_res == t_res:
                identical += 1

    identity = (identical / compared * 100) if compared else 0

    if label in {"2Q6O_chainA", "1RQP_chainA"}:
        group = "structural_reference"
        domain_pattern = "not_applicable"
        decision = "reference"
    else:
        group = get_field(header, "group")
        domain_pattern = get_field(header, "domain_pattern")
        decision = get_field(header, "decision")

    rows.append({
        "target_label": label,
        "annotation_group": group,
        "domain_pattern": domain_pattern,
        "curation_decision": decision,
        "alignment_length": len(query_seq),
        "compared_non_gap_positions": compared,
        "identical_positions": identical,
        "pairwise_identity_percent": f"{identity:.2f}",
        "query_gap_only_positions": query_gap_only,
        "target_gap_only_positions": target_gap_only,
        "both_gap_positions": both_gap,
        "header": header,
    })

rows.sort(key=lambda r: float(r["pairwise_identity_percent"]), reverse=True)

fieldnames = [
    "target_label",
    "annotation_group",
    "domain_pattern",
    "curation_decision",
    "alignment_length",
    "compared_non_gap_positions",
    "identical_positions",
    "pairwise_identity_percent",
    "query_gap_only_positions",
    "target_gap_only_positions",
    "both_gap_positions",
    "header",
]

with out_path.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} pairwise comparisons to {out_path}")
