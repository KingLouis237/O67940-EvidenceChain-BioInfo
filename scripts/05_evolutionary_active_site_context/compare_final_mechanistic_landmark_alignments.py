#!/usr/bin/env python3

from pathlib import Path
import argparse
import csv


KEY_FIELDS = (
    "landmark_id",
    "sequence_accession",
)

INVARIANT_FIELDS = (
    "anchor_accession",
    "anchor_residue",
    "anchor_resnum",
    "landmark_role",
    "evidence_scope",
    "anchor_evidence_ids",
    "primary_source_id",
    "source_locator",
    "raw_evidence_file",
    "interpretation_boundary",
)

REQUIRED_FIELDS = (
    "landmark_id",
    "anchor_accession",
    "anchor_residue",
    "anchor_resnum",
    "alignment_column_1based",
    "column_occupancy",
    "sequence_accession",
    "sequence_residue",
    "sequence_resnum",
    "matches_anchor_residue",
    *INVARIANT_FIELDS[3:],
)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Compare mechanistic-landmark mappings "
            "between primary and sensitivity alignments."
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

    parser.add_argument(
        "--summary",
        type=Path,
        required=True,
    )

    return parser.parse_args()


def load_mapping(path):
    with path.open(
        encoding="utf-8",
        newline="",
    ) as handle:

        reader = csv.DictReader(
            handle,
            delimiter="\t",
        )

        fields = reader.fieldnames

        if fields is None:
            raise SystemExit(
                f"STOP: no TSV header in {path}"
            )

        missing = [
            field
            for field in REQUIRED_FIELDS
            if field not in fields
        ]

        if missing:
            raise SystemExit(
                "STOP: missing required fields in "
                f"{path}: {', '.join(missing)}"
            )

        rows = list(reader)

    if len(rows) != 84:
        raise SystemExit(
            f"STOP: expected 84 rows in {path}, "
            f"observed {len(rows)}."
        )

    keyed = {}

    for row in rows:
        key = tuple(
            row[field]
            for field in KEY_FIELDS
        )

        if key in keyed:
            raise SystemExit(
                "STOP: duplicate comparison key "
                f"{key} in {path}."
            )

        keyed[key] = row

    if len(keyed) != 84:
        raise SystemExit(
            f"STOP: expected 84 unique keys in {path}."
        )

    return rows, keyed


args = parse_args()

primary_rows, primary = load_mapping(
    args.primary
)

_, sensitivity = load_mapping(
    args.sensitivity
)

if set(primary) != set(sensitivity):
    only_primary = sorted(
        set(primary) - set(sensitivity)
    )

    only_sensitivity = sorted(
        set(sensitivity) - set(primary)
    )

    raise SystemExit(
        "STOP: mapping key sets differ.\n"
        f"Only primary: {only_primary}\n"
        f"Only sensitivity: {only_sensitivity}"
    )


comparison_rows = []

for primary_row in primary_rows:

    key = tuple(
        primary_row[field]
        for field in KEY_FIELDS
    )

    sensitivity_row = sensitivity[key]

    for field in INVARIANT_FIELDS:
        if (
            primary_row[field]
            != sensitivity_row[field]
        ):
            raise SystemExit(
                "STOP: frozen metadata differs for "
                f"{key}, field {field}: "
                f"{primary_row[field]!r} vs "
                f"{sensitivity_row[field]!r}"
            )

    residue_identity_same = (
        primary_row["sequence_residue"]
        == sensitivity_row["sequence_residue"]
    )

    residue_number_same = (
        primary_row["sequence_resnum"]
        == sensitivity_row["sequence_resnum"]
    )

    residue_correspondence_same = (
        residue_identity_same
        and residue_number_same
    )

    alignment_column_same = (
        primary_row["alignment_column_1based"]
        == sensitivity_row["alignment_column_1based"]
    )

    occupancy_same = (
        primary_row["column_occupancy"]
        == sensitivity_row["column_occupancy"]
    )

    comparison_rows.append(
        {
            "landmark_id": (
                primary_row["landmark_id"]
            ),
            "anchor_accession": (
                primary_row["anchor_accession"]
            ),
            "anchor_residue": (
                primary_row["anchor_residue"]
            ),
            "anchor_resnum": (
                primary_row["anchor_resnum"]
            ),
            "sequence_accession": (
                primary_row["sequence_accession"]
            ),
            "primary_alignment_column_1based": (
                primary_row[
                    "alignment_column_1based"
                ]
            ),
            "sensitivity_alignment_column_1based": (
                sensitivity_row[
                    "alignment_column_1based"
                ]
            ),
            "alignment_column_same": (
                "yes"
                if alignment_column_same
                else "no"
            ),
            "primary_column_occupancy": (
                primary_row["column_occupancy"]
            ),
            "sensitivity_column_occupancy": (
                sensitivity_row["column_occupancy"]
            ),
            "column_occupancy_same": (
                "yes"
                if occupancy_same
                else "no"
            ),
            "primary_sequence_residue": (
                primary_row["sequence_residue"]
            ),
            "primary_sequence_resnum": (
                primary_row["sequence_resnum"]
            ),
            "sensitivity_sequence_residue": (
                sensitivity_row["sequence_residue"]
            ),
            "sensitivity_sequence_resnum": (
                sensitivity_row["sequence_resnum"]
            ),
            "residue_identity_same": (
                "yes"
                if residue_identity_same
                else "no"
            ),
            "residue_number_same": (
                "yes"
                if residue_number_same
                else "no"
            ),
            "residue_correspondence_same": (
                "yes"
                if residue_correspondence_same
                else "no"
            ),
            "is_o67940": (
                "yes"
                if primary_row["sequence_accession"]
                == "O67940"
                else "no"
            ),
        }
    )


fieldnames = list(
    comparison_rows[0]
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
    writer.writerows(comparison_rows)


total = len(comparison_rows)

stable = sum(
    row["residue_correspondence_same"] == "yes"
    for row in comparison_rows
)

changed = total - stable

o67940_rows = [
    row
    for row in comparison_rows
    if row["is_o67940"] == "yes"
]

if len(o67940_rows) != 7:
    raise SystemExit(
        "STOP: expected 7 O67940 comparisons, "
        f"observed {len(o67940_rows)}."
    )

o67940_stable = sum(
    row["residue_correspondence_same"] == "yes"
    for row in o67940_rows
)

o67940_changed = (
    len(o67940_rows) - o67940_stable
)

column_same = sum(
    row["alignment_column_same"] == "yes"
    for row in comparison_rows
)

occupancy_same = sum(
    row["column_occupancy_same"] == "yes"
    for row in comparison_rows
)

primary_pass = (
    o67940_stable == 7
)


summary_rows = [
    {
        "metric": "total_mapping_comparisons",
        "value": str(total),
    },
    {
        "metric": "stable_residue_correspondences",
        "value": str(stable),
    },
    {
        "metric": "changed_residue_correspondences",
        "value": str(changed),
    },
    {
        "metric": "o67940_total_landmarks",
        "value": str(len(o67940_rows)),
    },
    {
        "metric": "o67940_stable_correspondences",
        "value": str(o67940_stable),
    },
    {
        "metric": "o67940_changed_correspondences",
        "value": str(o67940_changed),
    },
    {
        "metric": "identical_alignment_columns",
        "value": str(column_same),
    },
    {
        "metric": "identical_column_occupancies",
        "value": str(occupancy_same),
    },
    {
        "metric": "primary_robustness_pass",
        "value": (
            "yes"
            if primary_pass
            else "no"
        ),
    },
]


with args.summary.open(
    "w",
    encoding="utf-8",
    newline="",
) as handle:

    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "metric",
            "value",
        ],
        delimiter="\t",
        lineterminator="\n",
    )

    writer.writeheader()
    writer.writerows(summary_rows)


print(
    f"Total comparisons: {total}"
)
print(
    "Stable residue correspondences: "
    f"{stable}/{total}"
)
print(
    "O67940 stable correspondences: "
    f"{o67940_stable}/7"
)
print(
    "Identical alignment columns: "
    f"{column_same}/{total}"
)
print(
    "Identical column occupancies: "
    f"{occupancy_same}/{total}"
)
print(
    "Primary robustness criterion: "
    + (
        "PASS"
        if primary_pass
        else "FAIL"
    )
)

changed_rows = [
    row
    for row in comparison_rows
    if row["residue_correspondence_same"]
    == "no"
]

if changed_rows:
    print()
    print("Changed residue correspondences:")

    for row in changed_rows:
        print(
            f"{row['landmark_id']} "
            f"{row['sequence_accession']}: "
            f"{row['primary_sequence_residue']}"
            f"{row['primary_sequence_resnum']} -> "
            f"{row['sensitivity_sequence_residue']}"
            f"{row['sensitivity_sequence_resnum']}"
        )
