#!/usr/bin/env python3

"""
Build the frozen 12-taxon biological reference FASTA used for the
final O67940 reviewed-reference evolutionary analysis.

Scientific boundary
-------------------
This script implements the already-frozen taxon-selection decision.

It does NOT:
- select taxa;
- infer functional classes;
- align sequences;
- build a phylogenetic tree;
- interpret evolutionary placement.

The decision controlling taxon membership is:

    results/phylogeny/
    O67940_final_reviewed_reference_set_decision.tsv

Sequence sources
----------------
O67940:
    data/O67940_AQUAE.fasta

11 reviewed references:
    data/databases/O67940_uniprot_pfam_candidates/
    candidate_sequences.fasta

Independent sequence checks:
    - candidate universe for all 12 taxa;
    - frozen Swiss-Prot 2026-07-04 for the 11 reviewed references.

Output
------
Canonical FASTA:
    results/phylogeny/
    O67940_final_reviewed_reference_set.fasta

QC table:
    results/phylogeny/
    O67940_final_reviewed_reference_set_qc.tsv
"""

from __future__ import annotations

from pathlib import Path
import csv
import hashlib
import re
import sys


# ============================================================
# Paths
# ============================================================

DECISION_TSV = Path(
    "results/phylogeny/"
    "O67940_final_reviewed_reference_set_decision.tsv"
)

QUERY_FASTA = Path(
    "data/O67940_AQUAE.fasta"
)

CANDIDATE_FASTA = Path(
    "data/databases/O67940_uniprot_pfam_candidates/"
    "candidate_sequences.fasta"
)

SWISSPROT_FASTA = Path(
    "data/databases/uniprot_sprot_2026-07-04/"
    "uniprot_sprot.fasta"
)

OUTPUT_FASTA = Path(
    "results/phylogeny/"
    "O67940_final_reviewed_reference_set.fasta"
)

OUTPUT_QC = Path(
    "results/phylogeny/"
    "O67940_final_reviewed_reference_set_qc.tsv"
)


# ============================================================
# Constants
# ============================================================

STANDARD_AA = set(
    "ACDEFGHIKLMNPQRSTVWY"
)

UNIPROT_HEADER_RE = re.compile(
    r"^(?:sp|tr)\|([^|]+)\|"
)


# ============================================================
# Utility functions
# ============================================================

def fail(message: str) -> None:
    """Stop immediately when a frozen-input assumption fails."""

    raise SystemExit(
        f"STOP: {message}"
    )


def md5_text(text: str) -> str:
    return hashlib.md5(
        text.encode("ascii")
    ).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(
        text.encode("ascii")
    ).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def read_fasta(path: Path):
    """
    Stream FASTA records as (header, sequence).

    Sequence whitespace is removed but residue characters are
    otherwise preserved.
    """

    header = None
    sequence_parts = []

    with path.open(
        "r",
        encoding="utf-8",
        errors="strict",
    ) as handle:

        for raw_line in handle:
            line = raw_line.strip()

            if not line:
                continue

            if line.startswith(">"):

                if header is not None:
                    yield (
                        header,
                        "".join(sequence_parts),
                    )

                header = line[1:].strip()
                sequence_parts = []

            else:

                if header is None:
                    fail(
                        f"sequence encountered before FASTA "
                        f"header in {path}"
                    )

                sequence_parts.append(line)

    if header is not None:
        yield (
            header,
            "".join(sequence_parts),
        )


def uniprot_accession(header: str) -> str | None:
    """Extract accession from standard UniProt sp|ACC| / tr|ACC|."""

    match = UNIPROT_HEADER_RE.match(header)

    if match is None:
        return None

    return match.group(1)


def collect_targets(
    path: Path,
    targets: set[str],
):
    """
    Collect only requested UniProt accessions from a large FASTA.

    Each requested accession must occur at most once.
    """

    found = {}

    for header, sequence in read_fasta(path):

        accession = uniprot_accession(header)

        if accession not in targets:
            continue

        if accession in found:
            fail(
                f"duplicate accession {accession} "
                f"in {path}"
            )

        found[accession] = {
            "header": header,
            "sequence": sequence,
        }

    return found


def validate_sequence(
    accession: str,
    sequence: str,
) -> None:
    """
    Mechanical biological-sequence QC.

    These checks establish sequence integrity only.
    They do not validate biological function.
    """

    if not sequence:
        fail(
            f"{accession} has an empty sequence"
        )

    nonstandard = sorted(
        set(sequence) - STANDARD_AA
    )

    if nonstandard:
        fail(
            f"{accession} contains non-standard "
            f"characters: {nonstandard}"
        )

    if not 200 <= len(sequence) <= 350:
        fail(
            f"{accession} length {len(sequence)} "
            f"is outside the frozen operational "
            f"200-350-aa range"
        )


# ============================================================
# 1. Read the frozen taxon decision.
# ============================================================

if not DECISION_TSV.exists():
    fail(
        f"missing decision table: {DECISION_TSV}"
    )

with DECISION_TSV.open(
    newline="",
    encoding="utf-8",
) as handle:

    decision_rows = list(
        csv.DictReader(
            handle,
            delimiter="\t",
        )
    )


if len(decision_rows) != 12:
    fail(
        f"decision table must contain exactly 12 taxa; "
        f"observed {len(decision_rows)}"
    )


accessions = [
    row["accession"]
    for row in decision_rows
]


if len(set(accessions)) != 12:
    fail(
        "decision table contains duplicate accessions"
    )


if accessions.count("O67940") != 1:
    fail(
        "decision table must contain O67940 exactly once"
    )


for row in decision_rows:

    if row["include_primary"] != "yes":
        fail(
            f"{row['accession']} is not marked "
            f"include_primary=yes"
        )


reference_accessions = {
    accession
    for accession in accessions
    if accession != "O67940"
}


if len(reference_accessions) != 11:
    fail(
        "expected exactly 11 reviewed reference accessions"
    )


# ============================================================
# 2. Read all 12 sequences from the frozen candidate universe.
# ============================================================

candidate_records = collect_targets(
    CANDIDATE_FASTA,
    set(accessions),
)


missing_candidate = sorted(
    set(accessions) - set(candidate_records)
)


if missing_candidate:
    fail(
        "missing from candidate FASTA: "
        + ", ".join(missing_candidate)
    )


# ============================================================
# 3. Read the dedicated O67940 query source.
# ============================================================

query_records = list(
    read_fasta(QUERY_FASTA)
)


if len(query_records) != 1:
    fail(
        f"{QUERY_FASTA} must contain exactly one "
        f"FASTA record; observed {len(query_records)}"
    )


query_header, query_sequence = query_records[0]


# O67940 has a dedicated source, but it must still agree exactly
# with the frozen family-universe copy.
if (
    query_sequence
    != candidate_records["O67940"]["sequence"]
):
    fail(
        "dedicated O67940 sequence differs from "
        "the frozen candidate-universe sequence"
    )


# ============================================================
# 4. Read the reviewed references from frozen Swiss-Prot.
# ============================================================

swissprot_records = collect_targets(
    SWISSPROT_FASTA,
    reference_accessions,
)


missing_swissprot = sorted(
    reference_accessions
    - set(swissprot_records)
)


if missing_swissprot:
    fail(
        "reviewed references missing from frozen "
        "Swiss-Prot snapshot: "
        + ", ".join(missing_swissprot)
    )


# ============================================================
# 5. Assemble canonical sequences in frozen decision order.
# ============================================================

canonical = {}
qc_rows = []


for row in decision_rows:

    accession = row["accession"]

    if accession == "O67940":

        sequence = query_sequence
        source_file = str(QUERY_FASTA)
        source_header = query_header

        candidate_exact = (
            sequence
            == candidate_records[accession]["sequence"]
        )

        swissprot_exact = "not_applicable"

    else:

        source_record = candidate_records[accession]

        sequence = source_record["sequence"]
        source_file = str(CANDIDATE_FASTA)
        source_header = source_record["header"]

        candidate_exact = True

        swissprot_exact = (
            sequence
            == swissprot_records[accession]["sequence"]
        )

        if not swissprot_exact:
            fail(
                f"{accession} differs between frozen "
                f"candidate FASTA and frozen Swiss-Prot"
            )

    validate_sequence(
        accession,
        sequence,
    )

    canonical[accession] = sequence

    qc_rows.append(
        {
            "accession": accession,
            "entry_name": row["entry_name"],
            "primary_role": row["primary_role"],
            "source_file": source_file,
            "source_header": source_header,
            "length_aa": len(sequence),
            "sequence_md5": md5_text(sequence),
            "sequence_sha256": sha256_text(sequence),
            "candidate_universe_exact":
                "PASS"
                if candidate_exact
                else "FAIL",
            "frozen_swissprot_exact":
                swissprot_exact
                if isinstance(swissprot_exact, str)
                else (
                    "PASS"
                    if swissprot_exact
                    else "FAIL"
                ),
        }
    )


# ============================================================
# 6. Reject exact duplicate biological sequences.
# ============================================================

by_md5 = {}

for accession, sequence in canonical.items():
    digest = md5_text(sequence)

    by_md5.setdefault(
        digest,
        [],
    ).append(accession)


duplicate_groups = [
    group
    for group in by_md5.values()
    if len(group) > 1
]


if duplicate_groups:

    formatted = [
        ",".join(group)
        for group in duplicate_groups
    ]

    fail(
        "exact duplicate biological sequences found: "
        + "; ".join(formatted)
    )


# ============================================================
# 7. Write canonical accession-only FASTA.
#
# No functional labels are embedded in the phylogenetic input.
# Taxon order follows the frozen decision table exactly.
# ============================================================

OUTPUT_FASTA.parent.mkdir(
    parents=True,
    exist_ok=True,
)


with OUTPUT_FASTA.open(
    "w",
    encoding="utf-8",
) as handle:

    for accession in accessions:

        sequence = canonical[accession]

        handle.write(
            f">{accession}\n"
        )

        # Fixed-width sequence lines make the FASTA stable and
        # easy to inspect while not affecting downstream biology.
        for start in range(
            0,
            len(sequence),
            60,
        ):
            handle.write(
                sequence[start:start + 60]
                + "\n"
            )


# ============================================================
# 8. Write machine-readable QC table.
# ============================================================

qc_fields = [
    "accession",
    "entry_name",
    "primary_role",
    "source_file",
    "source_header",
    "length_aa",
    "sequence_md5",
    "sequence_sha256",
    "candidate_universe_exact",
    "frozen_swissprot_exact",
]


with OUTPUT_QC.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:

    writer = csv.DictWriter(
        handle,
        fieldnames=qc_fields,
        delimiter="\t",
        lineterminator="\n",
    )

    writer.writeheader()
    writer.writerows(qc_rows)


# ============================================================
# 9. Final output-level validation.
# ============================================================

written_records = list(
    read_fasta(OUTPUT_FASTA)
)


if len(written_records) != 12:
    fail(
        f"written FASTA contains {len(written_records)} "
        f"records instead of 12"
    )


written_headers = [
    header
    for header, _ in written_records
]


if written_headers != accessions:
    fail(
        "written FASTA order or accession-only headers "
        "do not match frozen decision table"
    )


for header, sequence in written_records:

    if sequence != canonical[header]:
        fail(
            f"written sequence differs for {header}"
        )


# ============================================================
# Report
# ============================================================

print(
    "PASS: canonical reviewed-reference FASTA built."
)

print(
    f"Taxa: {len(written_records)}"
)

print(
    f"Query: 1"
)

print(
    f"Reviewed references: {len(reference_accessions)}"
)

print(
    f"Exact sequence duplicates: 0"
)

print(
    f"FASTA: {OUTPUT_FASTA}"
)

print(
    f"QC table: {OUTPUT_QC}"
)

print(
    f"FASTA SHA256: {file_sha256(OUTPUT_FASTA)}"
)

print(
    f"QC SHA256: {file_sha256(OUTPUT_QC)}"
)
