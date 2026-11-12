#!/usr/bin/env python3

from pathlib import Path
import csv


ALIGNMENT = Path(
    "results/phylogeny/"
    "O67940_final_reviewed_reference_set_ginsi.fasta"
)

REGISTRY = Path(
    "results/residue_mapping/"
    "O67940_final_mechanistic_landmark_registry.tsv"
)

EVIDENCE = Path(
    "results/functional_anchor_audit/parsed/"
    "functional_anchor_evidence.tsv"
)

OUTPUT = Path(
    "results/residue_mapping/"
    "O67940_final_mechanistic_landmark_mapping_long.tsv"
)


def read_fasta(path):
    """Read accession-only aligned FASTA records in file order."""

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
                        f"STOP: duplicate FASTA header {header}"
                    )

                records[header] = "".join(parts)
                order.append(header)

            header = line[1:].strip()
            parts = []

        else:
            parts.append(line)

    if header is not None:

        if header in records:
            raise SystemExit(
                f"STOP: duplicate FASTA header {header}"
            )

        records[header] = "".join(parts)
        order.append(header)

    return order, records


def load_tsv(path):
    """Return a TSV as a list of dictionaries."""

    with path.open(
        encoding="utf-8",
        newline="",
    ) as handle:

        return list(
            csv.DictReader(
                handle,
                delimiter="\t",
            )
        )


def residue_to_column(
    aligned_sequence,
    residue_number,
):
    """
    Convert a 1-based ungapped residue number
    to a 0-based alignment-column index.
    """

    seen = 0

    for index, aa in enumerate(
        aligned_sequence
    ):

        if aa == "-":
            continue

        seen += 1

        if seen == residue_number:
            return index

    raise SystemExit(
        "STOP: residue number "
        f"{residue_number} exceeds sequence length."
    )


def column_to_residue(
    aligned_sequence,
    column_index,
):
    """
    Return residue identity and 1-based ungapped
    residue number at an alignment column.

    A gap returns ('-', '').
    """

    aa = aligned_sequence[column_index]

    if aa == "-":
        return "-", ""

    residue_number = sum(
        character != "-"
        for character
        in aligned_sequence[: column_index + 1]
    )

    return aa, str(residue_number)


# ------------------------------------------------------------
# Load and validate the frozen final alignment.
# ------------------------------------------------------------

order, records = read_fasta(
    ALIGNMENT
)

if len(records) != 12:
    raise SystemExit(
        f"STOP: expected 12 aligned taxa, "
        f"observed {len(records)}."
    )

widths = {
    len(sequence)
    for sequence in records.values()
}

if len(widths) != 1:
    raise SystemExit(
        "STOP: aligned sequences do not share "
        "one alignment width."
    )

alignment_width = next(iter(widths))

required_accessions = {
    "O67940",
    "O58212",
    "A4X3Q0",
    "Q70GK9",
}

missing = sorted(
    required_accessions - set(records)
)

if missing:
    raise SystemExit(
        "STOP: required accessions missing from "
        f"alignment: {', '.join(missing)}"
    )


# ------------------------------------------------------------
# Load curated landmark registry.
# ------------------------------------------------------------

registry = load_tsv(
    REGISTRY
)

if len(registry) != 7:
    raise SystemExit(
        f"STOP: expected 7 landmark rows, "
        f"observed {len(registry)}."
    )

landmark_ids = [
    row["landmark_id"]
    for row in registry
]

if len(landmark_ids) != len(set(landmark_ids)):
    raise SystemExit(
        "STOP: landmark IDs are not unique."
    )


# ------------------------------------------------------------
# Validate every referenced functional-anchor evidence ID.
#
# This does not reinterpret the evidence table. It verifies
# that the registry points to existing audited evidence and
# that those evidence records belong to the stated anchor.
# ------------------------------------------------------------

evidence_rows = load_tsv(
    EVIDENCE
)

evidence_by_id = {
    row["evidence_id"]: row
    for row in evidence_rows
}

for landmark in registry:

    anchor = landmark["anchor_accession"]

    evidence_ids = [
        value
        for value
        in landmark["anchor_evidence_ids"].split(";")
        if value
    ]

    if not evidence_ids:
        raise SystemExit(
            "STOP: no anchor evidence IDs for "
            f"{landmark['landmark_id']}."
        )

    for evidence_id in evidence_ids:

        if evidence_id not in evidence_by_id:
            raise SystemExit(
                "STOP: registry references missing "
                f"evidence ID {evidence_id}."
            )

        evidence_accession = (
            evidence_by_id[evidence_id]
            ["candidate_accession"]
        )

        if evidence_accession != anchor:
            raise SystemExit(
                "STOP: evidence-anchor mismatch for "
                f"{landmark['landmark_id']}: "
                f"{evidence_id} belongs to "
                f"{evidence_accession}, not {anchor}."
            )


# ------------------------------------------------------------
# Map each experimentally grounded anchor residue into the
# frozen G-INS-i alignment and propagate that column across
# all 12 biological taxa.
# ------------------------------------------------------------

output_rows = []

print(
    f"Alignment taxa: {len(records)}"
)
print(
    f"Alignment width: {alignment_width}"
)

print()
print("Validated landmark mappings:")

for landmark in registry:

    landmark_id = landmark["landmark_id"]
    anchor = landmark["anchor_accession"]
    expected_aa = landmark["anchor_residue"]

    try:
        anchor_resnum = int(
            landmark["anchor_resnum"]
        )

    except ValueError as error:
        raise SystemExit(
            "STOP: non-integer anchor residue number "
            f"for {landmark_id}."
        ) from error

    anchor_sequence = records[anchor]

    column_index = residue_to_column(
        anchor_sequence,
        anchor_resnum,
    )

    observed_anchor_aa = (
        anchor_sequence[column_index]
    )

    if observed_anchor_aa != expected_aa:
        raise SystemExit(
            "STOP: anchor residue validation failed "
            f"for {landmark_id}: expected "
            f"{expected_aa}{anchor_resnum}, found "
            f"{observed_anchor_aa}{anchor_resnum}."
        )

    column_occupancy = sum(
        sequence[column_index] != "-"
        for sequence in records.values()
    )

    o67940_aa, o67940_resnum = (
        column_to_residue(
            records["O67940"],
            column_index,
        )
    )

    o67940_label = (
        "-"
        if o67940_aa == "-"
        else f"{o67940_aa}{o67940_resnum}"
    )

    print(
        f"{landmark_id:10s} "
        f"{anchor}:{expected_aa}{anchor_resnum} "
        f"-> column {column_index + 1:3d} "
        f"-> O67940:{o67940_label} "
        f"| occupancy={column_occupancy}/12"
    )

    for accession in order:

        residue, residue_number = (
            column_to_residue(
                records[accession],
                column_index,
            )
        )

        output_rows.append(
            {
                "landmark_id": landmark_id,
                "anchor_accession": anchor,
                "anchor_residue": expected_aa,
                "anchor_resnum": anchor_resnum,
                "alignment_column_1based": (
                    column_index + 1
                ),
                "column_occupancy": (
                    f"{column_occupancy}/12"
                ),
                "sequence_accession": accession,
                "sequence_residue": residue,
                "sequence_resnum": residue_number,
                "matches_anchor_residue": (
                    "yes"
                    if residue == expected_aa
                    else "no"
                ),
                "landmark_role": (
                    landmark["landmark_role"]
                ),
                "evidence_scope": (
                    landmark["evidence_scope"]
                ),
                "anchor_evidence_ids": (
                    landmark["anchor_evidence_ids"]
                ),
                "primary_source_id": (
                    landmark["primary_source_id"]
                ),
                "source_locator": (
                    landmark["source_locator"]
                ),
                "raw_evidence_file": (
                    landmark["raw_evidence_file"]
                ),
                "interpretation_boundary": (
                    landmark[
                        "interpretation_boundary"
                    ]
                ),
            }
        )


# ------------------------------------------------------------
# Deterministic long-format output.
# ------------------------------------------------------------

fieldnames = [
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
    "landmark_role",
    "evidence_scope",
    "anchor_evidence_ids",
    "primary_source_id",
    "source_locator",
    "raw_evidence_file",
    "interpretation_boundary",
]

with OUTPUT.open(
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
    writer.writerows(output_rows)


expected_rows = (
    len(registry) * len(records)
)

if len(output_rows) != expected_rows:
    raise SystemExit(
        "STOP: unexpected output row count."
    )

print()
print(
    f"Wrote: {OUTPUT}"
)
print(
    f"Output rows: {len(output_rows)} "
    f"(7 landmarks x 12 taxa)"
)

print()
print("Interpretation boundary:")
print(
    "This mapping establishes alignment-based "
    "positional correspondence to experimentally "
    "grounded landmarks. It does not transfer "
    "catalytic function or substrate specificity "
    "to O67940."
)
