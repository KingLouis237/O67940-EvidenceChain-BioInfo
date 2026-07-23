#!/usr/bin/env python3

from pathlib import Path
import csv
from collections import Counter, defaultdict

long_path = Path("results/residue_conservation/O67940_reviewed_reference_functional_residue_mapping_long.tsv")
out_path = Path("results/residue_conservation/O67940_reviewed_reference_residue_pattern_summary.tsv")


def residue_counts(rows, group):
    residues = [
        row["residue"]
        for row in rows
        if row["annotation_group"] == group and row["residue"] != "-"
    ]
    counts = Counter(residues)

    if not counts:
        return "", ""

    counts_text = ";".join(f"{res}:{count}" for res, count in sorted(counts.items()))
    major_residue, major_count = counts.most_common(1)[0]

    return counts_text, f"{major_residue}:{major_count}"


def get_single_residue(rows, label):
    matches = [row["residue"] for row in rows if row["sequence_label"] == label]

    if len(matches) != 1:
        return ""

    return matches[0]


rows_by_position = defaultdict(list)

with long_path.open() as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    for row in reader:
        rows_by_position[int(row["O67940_position"])].append(row)


summary_rows = []

for pos in sorted(rows_by_position):
    rows = rows_by_position[pos]

    first = rows[0]
    o67940_residue = get_single_residue(rows, "O67940_AQUAE_AlphaFold_chainA")
    q6o_residue = get_single_residue(rows, "2Q6O_chainA")
    rqp_residue = get_single_residue(rows, "1RQP_chainA")
    sall_residue = get_single_residue(rows, "SALL_SALTO")

    sam_counts, sam_major = residue_counts(rows, "SAM_hydrolase")
    flu_counts, flu_major = residue_counts(rows, "fluorinase")

    sam_major_residue = sam_major.split(":")[0] if sam_major else ""
    flu_major_residue = flu_major.split(":")[0] if flu_major else ""

    matches = []

    if o67940_residue == q6o_residue:
        matches.append("2Q6O")
    if o67940_residue == rqp_residue:
        matches.append("1RQP")
    if o67940_residue == sall_residue:
        matches.append("SalL")
    if o67940_residue == sam_major_residue:
        matches.append("SAM_hydrolase_major")
    if o67940_residue == flu_major_residue:
        matches.append("fluorinase_major")

    if not matches:
        matches_text = "none_of_selected_major_patterns"
    else:
        matches_text = ";".join(matches)

    summary_rows.append({
        "O67940_position": pos,
        "O67940_residue": o67940_residue,
        "site_note": first["site_note"],
        "source_mapping_rows": first["source_mapping_rows"],
        "alignment_column_1based": first["alignment_column_1based"],
        "2Q6O_residue": q6o_residue,
        "1RQP_residue": rqp_residue,
        "SALL_SALTO_residue": sall_residue,
        "SAM_hydrolase_counts": sam_counts,
        "SAM_hydrolase_major": sam_major,
        "fluorinase_counts": flu_counts,
        "fluorinase_major": flu_major,
        "O67940_matches": matches_text,
    })


fieldnames = [
    "O67940_position",
    "O67940_residue",
    "site_note",
    "source_mapping_rows",
    "alignment_column_1based",
    "2Q6O_residue",
    "1RQP_residue",
    "SALL_SALTO_residue",
    "SAM_hydrolase_counts",
    "SAM_hydrolase_major",
    "fluorinase_counts",
    "fluorinase_major",
    "O67940_matches",
]

with out_path.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    writer.writerows(summary_rows)

print(f"Wrote {len(summary_rows)} residue-pattern rows to {out_path}")
