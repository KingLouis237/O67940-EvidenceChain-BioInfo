#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


EXPECTED_FULL_SHA256 = (
    "f23da6edcb8c0962c803b5a6a0dbfa968cf6bb8e172c6ca296174269c8d09d15"
)

EXPECTED_PDB25_SHA256 = (
    "f945016edd1e3bbdd8976cf798f440c81755ae3b5310b880d1c710c7ca5f8946"
)

EXPECTED_FULL_COUNT = 2406
EXPECTED_PDB25_COUNT = 639


REFERENCES = [
    {
        "reference_pdb": "2q6i",
        "reference_role": "WT_SalL",
    },
    {
        "reference_pdb": "2q6o",
        "reference_role": "SalL_Y70T_historical_mutant",
    },
    {
        "reference_pdb": "1rqp",
        "reference_role": "WT_FDAS",
    },
    {
        "reference_pdb": "2wr8",
        "reference_role": "PH0463_HAT_related",
    },
]


def sha256(path: Path) -> str:

    digest = hashlib.sha256()

    with path.open("rb") as handle:

        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def check_hash(
    path: Path,
    expected: str,
) -> None:

    observed = sha256(path)

    if observed != expected:
        raise SystemExit(
            "STOP: source checksum mismatch:\n"
            f"{path}\n"
            f"observed={observed}\n"
            f"expected={expected}"
        )


def read_tsv(
    path: Path,
) -> list[dict[str, str]]:

    with path.open(
        encoding="utf-8",
        newline="",
    ) as handle:

        rows = list(
            csv.DictReader(
                handle,
                delimiter="\t",
            )
        )

    return rows


def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "Extract prospectively defined "
            "O67940 DALI calibration references "
            "from frozen full-PDB and PDB25 tables."
        )
    )

    parser.add_argument(
        "--full-pdb",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--pdb25",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
    )

    args = parser.parse_args()

    check_hash(
        args.full_pdb,
        EXPECTED_FULL_SHA256,
    )

    check_hash(
        args.pdb25,
        EXPECTED_PDB25_SHA256,
    )

    print(
        "PASS: frozen parsed-input "
        "checksums verified."
    )

    full = read_tsv(
        args.full_pdb
    )

    pdb25 = read_tsv(
        args.pdb25
    )

    if len(full) != EXPECTED_FULL_COUNT:
        raise SystemExit(
            "STOP: full-PDB cardinality changed: "
            f"{len(full)}"
        )

    if len(pdb25) != EXPECTED_PDB25_COUNT:
        raise SystemExit(
            "STOP: PDB25 cardinality changed: "
            f"{len(pdb25)}"
        )

    views = [
        (
            "full_PDB",
            full,
            args.full_pdb,
        ),
        (
            "PDB25",
            pdb25,
            args.pdb25,
        ),
    ]

    output_rows = []

    for reference in REFERENCES:

        reference_pdb = (
            reference["reference_pdb"]
        )

        role = (
            reference["reference_role"]
        )

        for (
            search_view,
            rows,
            source_path,
        ) in views:

            matches = [
                row
                for row in rows
                if (
                    row["pdb_id"].lower()
                    == reference_pdb
                )
            ]

            matches = sorted(
                matches,
                key=lambda row: int(
                    row["rank"]
                ),
            )

            if not matches:

                output_rows.append({
                    "reference_pdb": (
                        reference_pdb.upper()
                    ),
                    "reference_role": role,
                    "search_view": search_view,
                    "exact_pdb_present": "no",
                    "exact_hit_count_in_view": 0,
                    "rank": "NA",
                    "subject_id": "NA",
                    "chain_id": "NA",
                    "z_score": "NA",
                    "rmsd": "NA",
                    "aligned_length": "NA",
                    "subject_length": "NA",
                    "query_length": "NA",
                    "query_coverage": "NA",
                    "seq_identity_pct": "NA",
                    "description": (
                        "exact PDB entry absent "
                        "from this view"
                    ),
                    "source_table": str(
                        source_path
                    ),
                })

                continue

            for row in matches:

                output_rows.append({
                    "reference_pdb": (
                        reference_pdb.upper()
                    ),
                    "reference_role": role,
                    "search_view": search_view,
                    "exact_pdb_present": "yes",
                    "exact_hit_count_in_view": (
                        len(matches)
                    ),
                    "rank": row["rank"],
                    "subject_id": (
                        row["subject_id"]
                    ),
                    "chain_id": (
                        row["chain_id"]
                    ),
                    "z_score": (
                        row["z_score"]
                    ),
                    "rmsd": (
                        row["rmsd"]
                    ),
                    "aligned_length": (
                        row["aligned_length"]
                    ),
                    "subject_length": (
                        row["subject_length"]
                    ),
                    "query_length": (
                        row["query_length"]
                    ),
                    "query_coverage": (
                        row["query_coverage"]
                    ),
                    "seq_identity_pct": (
                        row["seq_identity_pct"]
                    ),
                    "description": (
                        row["description"]
                    ),
                    "source_table": str(
                        source_path
                    ),
                })

    out = args.output_dir

    out.mkdir(
        parents=True,
        exist_ok=True,
    )

    audit_path = (
        out
        / "O67940_dali_calibration_reference_hits.tsv"
    )

    fields = [
        "reference_pdb",
        "reference_role",
        "search_view",
        "exact_pdb_present",
        "exact_hit_count_in_view",
        "rank",
        "subject_id",
        "chain_id",
        "z_score",
        "rmsd",
        "aligned_length",
        "subject_length",
        "query_length",
        "query_coverage",
        "seq_identity_pct",
        "description",
        "source_table",
    ]

    with audit_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
        )

        writer.writeheader()
        writer.writerows(
            output_rows
        )

    full_presence = {
        ref["reference_pdb"]:
        [
            row
            for row in full
            if (
                row["pdb_id"].lower()
                == ref["reference_pdb"]
            )
        ]
        for ref in REFERENCES
    }

    pdb25_presence = {
        ref["reference_pdb"]:
        [
            row
            for row in pdb25
            if (
                row["pdb_id"].lower()
                == ref["reference_pdb"]
            )
        ]
        for ref in REFERENCES
    }

    full_present_count = sum(
        bool(
            full_presence[
                ref["reference_pdb"]
            ]
        )
        for ref in REFERENCES
    )

    pdb25_present_count = sum(
        bool(
            pdb25_presence[
                ref["reference_pdb"]
            ]
        )
        for ref in REFERENCES
    )

    expected_audit_rows = sum(
        max(
            1,
            len(
                full_presence[
                    ref["reference_pdb"]
                ]
            ),
        )
        +
        max(
            1,
            len(
                pdb25_presence[
                    ref["reference_pdb"]
                ]
            ),
        )
        for ref in REFERENCES
    )

    represented_pairs = {
        (
            row["reference_pdb"],
            row["search_view"],
        )
        for row in output_rows
    }

    validation_rows = [
        [
            "full_pdb_input_sha256",
            "PASS",
            sha256(args.full_pdb),
            EXPECTED_FULL_SHA256,
        ],
        [
            "pdb25_input_sha256",
            "PASS",
            sha256(args.pdb25),
            EXPECTED_PDB25_SHA256,
        ],
        [
            "full_pdb_record_count",
            "PASS",
            str(len(full)),
            str(EXPECTED_FULL_COUNT),
        ],
        [
            "pdb25_record_count",
            "PASS",
            str(len(pdb25)),
            str(EXPECTED_PDB25_COUNT),
        ],
        [
            "predefined_reference_count",
            "PASS",
            str(len(REFERENCES)),
            "4",
        ],
        [
            "reference_view_pairs_represented",
            (
                "PASS"
                if len(represented_pairs) == 8
                else "FAIL"
            ),
            str(len(represented_pairs)),
            "8",
        ],
        [
            "audit_output_rows",
            (
                "PASS"
                if len(output_rows)
                == expected_audit_rows
                else "FAIL"
            ),
            str(len(output_rows)),
            str(expected_audit_rows),
        ],
        [
            "full_pdb_predefined_refs_present",
            "OBSERVED",
            str(full_present_count),
            "not_prespecified",
        ],
        [
            "pdb25_exact_predefined_refs_present",
            "OBSERVED",
            str(pdb25_present_count),
            "not_prespecified",
        ],
    ]

    if any(
        row[1] == "FAIL"
        for row in validation_rows
    ):
        raise SystemExit(
            "STOP: calibration-reference "
            "validation failed."
        )

    validation_path = (
        out
        / "O67940_dali_calibration_reference_validation.tsv"
    )

    with validation_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.writer(
            handle,
            delimiter="\t",
            lineterminator="\n",
        )

        writer.writerow([
            "check",
            "status",
            "observed",
            "expected",
        ])

        writer.writerows(
            validation_rows
        )

    print(
        "PASS: calibration-reference "
        "audit completed."
    )

    print(
        f"audit_rows={len(output_rows)}"
    )

    print(
        "full_PDB_predefined_refs_present="
        f"{sum(bool(x) for x in full_presence.values())}/4"
    )

    print(
        "PDB25_exact_predefined_refs_present="
        f"{sum(bool(x) for x in pdb25_presence.values())}/4"
    )

    print(
        f"wrote={audit_path}"
    )

    print(
        f"wrote={validation_path}"
    )


if __name__ == "__main__":
    main()
