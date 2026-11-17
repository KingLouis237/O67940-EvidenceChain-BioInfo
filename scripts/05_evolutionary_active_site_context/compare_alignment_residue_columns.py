#!/usr/bin/env python3

from pathlib import Path
import argparse
import csv


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Compare absolute residue-column placement "
            "between two alignments of the same sequences."
        )
    )

    parser.add_argument(
        "--primary",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--sensitivity",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
    )

    return parser.parse_args()


def read_fasta(path):
    records = {}
    order = []
    header = None
    parts = []

    for raw in path.read_text(
        encoding="utf-8"
    ).splitlines():

        line = raw.strip()

        if not line:
            continue

        if line.startswith(">"):

            if header is not None:

                if header in records:
                    raise SystemExit(
                        f"STOP: duplicate FASTA header "
                        f"{header} in {path}"
                    )

                records[header] = "".join(parts)
                order.append(header)

            header = line[1:].strip()
            parts = []

        else:

            if header is None:
                raise SystemExit(
                    f"STOP: sequence before header in {path}"
                )

            parts.append(line)

    if header is not None:

        if header in records:
            raise SystemExit(
                f"STOP: duplicate FASTA header "
                f"{header} in {path}"
            )

        records[header] = "".join(parts)
        order.append(header)

    return order, records


def residue_columns(aligned_sequence):
    return [
        column
        for column, residue
        in enumerate(
            aligned_sequence,
            start=1,
        )
        if residue != "-"
    ]


args = parse_args()

primary_order, primary_records = read_fasta(
    args.primary
)

sensitivity_order, sensitivity_records = read_fasta(
    args.sensitivity
)

if primary_order != sensitivity_order:
    raise SystemExit(
        "STOP: taxon order differs between alignments."
    )

if len(primary_order) != 12:
    raise SystemExit(
        "STOP: expected 12 taxa, "
        f"observed {len(primary_order)}."
    )

primary_widths = {
    len(sequence)
    for sequence in primary_records.values()
}

sensitivity_widths = {
    len(sequence)
    for sequence in sensitivity_records.values()
}

if len(primary_widths) != 1:
    raise SystemExit(
        "STOP: primary alignment has inconsistent widths."
    )

if len(sensitivity_widths) != 1:
    raise SystemExit(
        "STOP: sensitivity alignment has inconsistent widths."
    )

primary_width = next(iter(primary_widths))
sensitivity_width = next(iter(sensitivity_widths))

rows = []

total_residues = 0
total_shifted = 0
global_max_abs_shift = 0

for accession in primary_order:

    primary_sequence = primary_records[accession]
    sensitivity_sequence = sensitivity_records[accession]

    primary_ungapped = primary_sequence.replace(
        "-",
        "",
    )

    sensitivity_ungapped = sensitivity_sequence.replace(
        "-",
        "",
    )

    if primary_ungapped != sensitivity_ungapped:
        raise SystemExit(
            "STOP: underlying biological sequence "
            f"differs for {accession}."
        )

    primary_columns = residue_columns(
        primary_sequence
    )

    sensitivity_columns = residue_columns(
        sensitivity_sequence
    )

    if len(primary_columns) != len(
        sensitivity_columns
    ):
        raise SystemExit(
            "STOP: residue count differs for "
            f"{accession}."
        )

    changed_residues = []
    shifts = []

    for residue_number, (
        primary_column,
        sensitivity_column,
    ) in enumerate(
        zip(
            primary_columns,
            sensitivity_columns,
        ),
        start=1,
    ):

        shift = (
            sensitivity_column
            - primary_column
        )

        shifts.append(shift)

        if shift != 0:
            changed_residues.append(
                residue_number
            )

    residue_count = len(primary_columns)
    shifted_count = len(changed_residues)
    unchanged_count = (
        residue_count - shifted_count
    )

    max_abs_shift = (
        max(
            abs(shift)
            for shift in shifts
        )
        if shifts
        else 0
    )

    total_residues += residue_count
    total_shifted += shifted_count

    global_max_abs_shift = max(
        global_max_abs_shift,
        max_abs_shift,
    )

    rows.append(
        {
            "accession": accession,
            "residue_count": residue_count,
            "shifted_residue_count": (
                shifted_count
            ),
            "unchanged_residue_count": (
                unchanged_count
            ),
            "first_shifted_resnum": (
                changed_residues[0]
                if changed_residues
                else ""
            ),
            "last_shifted_resnum": (
                changed_residues[-1]
                if changed_residues
                else ""
            ),
            "max_abs_column_shift": (
                max_abs_shift
            ),
            "primary_alignment_width": (
                primary_width
            ),
            "sensitivity_alignment_width": (
                sensitivity_width
            ),
        }
    )


rows.append(
    {
        "accession": "__TOTAL__",
        "residue_count": total_residues,
        "shifted_residue_count": (
            total_shifted
        ),
        "unchanged_residue_count": (
            total_residues - total_shifted
        ),
        "first_shifted_resnum": "",
        "last_shifted_resnum": "",
        "max_abs_column_shift": (
            global_max_abs_shift
        ),
        "primary_alignment_width": (
            primary_width
        ),
        "sensitivity_alignment_width": (
            sensitivity_width
        ),
    }
)


fieldnames = list(
    rows[0]
)

with args.output.open(
    "w",
    encoding="utf-8",
    newline="",
) as handle:

    writer = csv.DictWriter(
        handle,
        fieldnames=fieldnames,
        delimiter="\t",
        lineterminator="\n",
    )

    writer.writeheader()
    writer.writerows(rows)


print(
    f"Primary width: {primary_width}"
)
print(
    f"Sensitivity width: {sensitivity_width}"
)
print(
    f"Total residues: {total_residues}"
)
print(
    f"Shifted residues: {total_shifted}"
)

o67940 = next(
    row
    for row in rows
    if row["accession"] == "O67940"
)

print(
    "O67940 shifted residues: "
    f"{o67940['shifted_residue_count']}/"
    f"{o67940['residue_count']}"
)
print(
    f"Wrote: {args.output}"
)
