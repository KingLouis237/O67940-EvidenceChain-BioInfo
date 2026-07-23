#!/usr/bin/env python3

from pathlib import Path
import csv

alignment_path = Path("results/sequence_alignment/O67940_reviewed_swissprot_reference_set_mafft_alignment.fasta")
old_mapping_path = Path("results/residue_mapping/functional_residue_mapping_mafft.tsv")

out_long = Path("results/residue_conservation/O67940_reviewed_reference_functional_residue_mapping_long.tsv")
out_matrix = Path("results/residue_conservation/O67940_reviewed_reference_functional_residue_matrix.tsv")


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


def label_from_header(header):
    return header.split("|")[0].strip()


def group_from_header(header):
    if header.startswith("O67940_AQUAE"):
        return "query"
    if header.startswith("2Q6O_chainA"):
        return "structural_reference_chlorinase_related"
    if header.startswith("1RQP_chainA"):
        return "structural_reference_fluorinase"

    for part in header.split("|"):
        part = part.strip()
        if part.startswith("group="):
            return part.replace("group=", "", 1)

    return "unknown"


def ungapped_position_at_column(seq, col_index):
    residue = seq[col_index]

    if residue == "-":
        return ""

    return str(sum(1 for char in seq[: col_index + 1] if char != "-"))


def load_focal_positions(path):
    focal = {}

    with path.open() as handle:
        reader = csv.DictReader(handle, delimiter="\t")

        for row in reader:
            pos = int(row["O67940_resnum"])
            aa = row["O67940_aa"]
            role = row["role"]

            if pos not in focal:
                focal[pos] = {
                    "O67940_position": pos,
                    "O67940_expected_residue": aa,
                    "site_note": role,
                    "source_mapping_rows": 1,
                }
            else:
                focal[pos]["source_mapping_rows"] += 1

                if focal[pos]["O67940_expected_residue"] != aa:
                    raise SystemExit(
                        f"Conflicting O67940 residue for position {pos}: "
                        f"{focal[pos]['O67940_expected_residue']} vs {aa}"
                    )

    return [focal[pos] for pos in sorted(focal)]


records = read_fasta(alignment_path)
focal_positions = load_focal_positions(old_mapping_path)

query_header = next(
    header for header in records
    if header.startswith("O67940_AQUAE_AlphaFold_chainA")
)

query_seq = records[query_header]

rows_long = []
rows_matrix = []

for focal in focal_positions:
    o_pos = focal["O67940_position"]
    expected_residue = focal["O67940_expected_residue"]
    site_note = focal["site_note"]

    residue_count = 0
    aln_col = None

    for idx, residue in enumerate(query_seq):
        if residue != "-":
            residue_count += 1

        if residue_count == o_pos:
            aln_col = idx
            break

    if aln_col is None:
        raise SystemExit(f"Could not map O67940 position {o_pos}")

    actual_query_residue = query_seq[aln_col]

    if actual_query_residue != expected_residue:
        raise SystemExit(
            f"Position check failed for O67940 {o_pos}: "
            f"expected {expected_residue}, found {actual_query_residue}"
        )

    matrix_row = {
        "O67940_position": o_pos,
        "O67940_expected_residue": expected_residue,
        "alignment_column_1based": aln_col + 1,
        "site_note": site_note,
        "source_mapping_rows": focal["source_mapping_rows"],
    }

    for header, seq in records.items():
        label = label_from_header(header)
        group = group_from_header(header)
        residue = seq[aln_col]
        ungapped_pos = ungapped_position_at_column(seq, aln_col)

        rows_long.append({
            "O67940_position": o_pos,
            "O67940_expected_residue": expected_residue,
            "alignment_column_1based": aln_col + 1,
            "site_note": site_note,
            "source_mapping_rows": focal["source_mapping_rows"],
            "sequence_label": label,
            "annotation_group": group,
            "residue": residue,
            "sequence_ungapped_position": ungapped_pos,
            "header": header,
        })

        matrix_row[label] = residue

    rows_matrix.append(matrix_row)


long_fields = [
    "O67940_position",
    "O67940_expected_residue",
    "alignment_column_1based",
    "site_note",
    "source_mapping_rows",
    "sequence_label",
    "annotation_group",
    "residue",
    "sequence_ungapped_position",
    "header",
]

with out_long.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=long_fields, delimiter="\t")
    writer.writeheader()
    writer.writerows(rows_long)


matrix_fields = [
    "O67940_position",
    "O67940_expected_residue",
    "alignment_column_1based",
    "site_note",
    "source_mapping_rows",
] + [label_from_header(header) for header in records]

with out_matrix.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=matrix_fields, delimiter="\t")
    writer.writeheader()
    writer.writerows(rows_matrix)

print(f"Wrote long mapping: {out_long}")
print(f"Wrote matrix mapping: {out_matrix}")
print(f"Mapped {len(focal_positions)} O67940 positions across {len(records)} sequences.")
