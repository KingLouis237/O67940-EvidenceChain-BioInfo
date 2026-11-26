#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import defaultdict
from pathlib import Path


EXPECTED_INPUT_SHA256 = (
    "90fe7b463846841a5b1d7a3294a1543d54e1a6688f719e76d62467a7deff329e"
)

EXPECTED_FULL_CHAIN_HITS = 93
EXPECTED_PDB25_CHAIN_HITS = 3


def sha256(path: Path) -> str:

    h = hashlib.sha256()

    with path.open("rb") as handle:

        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            h.update(block)

    return h.hexdigest()


def read_tsv(path: Path):

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


def aggregate_hits(
    hits: list[dict[str, str]],
) -> dict[str, str]:

    if not hits:
        return {
            "present": "no",
            "chain_hit_count": "0",
            "subject_ids": "NA",
            "chains": "NA",
            "ranks": "NA",
            "best_rank": "NA",
            "z_max": "NA",
            "z_min": "NA",
            "query_coverage_max": "NA",
            "seq_identity_pct_max": "NA",
        }

    hits = sorted(
        hits,
        key=lambda row: int(
            row["rank"]
        ),
    )

    z_values = [
        float(row["z_score"])
        for row in hits
    ]

    coverage_values = [
        float(row["query_coverage"])
        for row in hits
    ]

    identity_values = [
        float(row["seq_identity_pct"])
        for row in hits
    ]

    return {
        "present": "yes",
        "chain_hit_count": str(
            len(hits)
        ),
        "subject_ids": ",".join(
            row["subject_id"]
            for row in hits
        ),
        "chains": ",".join(
            row["chain_id"]
            for row in hits
        ),
        "ranks": ",".join(
            row["rank"]
            for row in hits
        ),
        "best_rank": hits[0]["rank"],
        "z_max": f"{max(z_values):.1f}",
        "z_min": f"{min(z_values):.1f}",
        "query_coverage_max": (
            f"{max(coverage_values):.6f}"
        ),
        "seq_identity_pct_max": (
            f"{max(identity_values):.0f}"
        ),
    }


def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "Collapse the frozen O67940 DALI "
            "high-Z chain-level neighborhood "
            "to a unique-PDB registry."
        )
    )

    parser.add_argument(
        "--high-z-cluster",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
    )

    args = parser.parse_args()

    observed_hash = sha256(
        args.high_z_cluster
    )

    if observed_hash != EXPECTED_INPUT_SHA256:

        raise SystemExit(
            "STOP: frozen high-Z input "
            "checksum mismatch."
        )

    rows = read_tsv(
        args.high_z_cluster
    )

    full = [
        row
        for row in rows
        if row["search_view"]
        == "full_PDB"
    ]

    pdb25 = [
        row
        for row in rows
        if row["search_view"]
        == "PDB25"
    ]

    if len(full) != EXPECTED_FULL_CHAIN_HITS:

        raise SystemExit(
            "STOP: full-PDB chain-hit "
            f"count changed: {len(full)}"
        )

    if len(pdb25) != EXPECTED_PDB25_CHAIN_HITS:

        raise SystemExit(
            "STOP: PDB25 chain-hit "
            f"count changed: {len(pdb25)}"
        )

    full_by_pdb = defaultdict(list)
    pdb25_by_pdb = defaultdict(list)

    for row in full:

        full_by_pdb[
            row["pdb_id"].upper()
        ].append(row)

    for row in pdb25:

        pdb25_by_pdb[
            row["pdb_id"].upper()
        ].append(row)

    all_pdb_ids = (
        set(full_by_pdb)
        | set(pdb25_by_pdb)
    )

    def sort_key(pdb_id):

        full_hits = full_by_pdb.get(
            pdb_id,
            [],
        )

        pdb25_hits = pdb25_by_pdb.get(
            pdb_id,
            [],
        )

        if full_hits:

            return (
                0,
                min(
                    int(row["rank"])
                    for row in full_hits
                ),
                pdb_id,
            )

        return (
            1,
            min(
                int(row["rank"])
                for row in pdb25_hits
            ),
            pdb_id,
        )

    registry_rows = []

    for pdb_id in sorted(
        all_pdb_ids,
        key=sort_key,
    ):

        full_summary = aggregate_hits(
            full_by_pdb.get(
                pdb_id,
                [],
            )
        )

        pdb25_summary = aggregate_hits(
            pdb25_by_pdb.get(
                pdb_id,
                [],
            )
        )

        registry_rows.append({
            "pdb_id": pdb_id,

            "full_pdb_present":
                full_summary["present"],

            "full_chain_hit_count":
                full_summary[
                    "chain_hit_count"
                ],

            "full_subject_ids":
                full_summary[
                    "subject_ids"
                ],

            "full_chains":
                full_summary["chains"],

            "full_ranks":
                full_summary["ranks"],

            "full_best_rank":
                full_summary[
                    "best_rank"
                ],

            "full_z_max":
                full_summary["z_max"],

            "full_z_min":
                full_summary["z_min"],

            "full_query_coverage_max":
                full_summary[
                    "query_coverage_max"
                ],

            "full_seq_identity_pct_max":
                full_summary[
                    "seq_identity_pct_max"
                ],

            "pdb25_present":
                pdb25_summary[
                    "present"
                ],

            "pdb25_chain_hit_count":
                pdb25_summary[
                    "chain_hit_count"
                ],

            "pdb25_subject_ids":
                pdb25_summary[
                    "subject_ids"
                ],

            "pdb25_chains":
                pdb25_summary["chains"],

            "pdb25_ranks":
                pdb25_summary["ranks"],

            "pdb25_best_rank":
                pdb25_summary[
                    "best_rank"
                ],

            "pdb25_z_max":
                pdb25_summary["z_max"],

            "pdb25_z_min":
                pdb25_summary["z_min"],

            "pdb25_query_coverage_max":
                pdb25_summary[
                    "query_coverage_max"
                ],

            "pdb25_seq_identity_pct_max":
                pdb25_summary[
                    "seq_identity_pct_max"
                ],
        })

    output_dir = args.output_dir

    registry_path = (
        output_dir
        / "O67940_dali_high_z_pdb_registry.tsv"
    )

    validation_path = (
        output_dir
        / "O67940_dali_high_z_pdb_registry_validation.tsv"
    )

    existing_outputs = [
        path
        for path in (
            registry_path,
            validation_path,
        )
        if path.exists()
    ]

    if existing_outputs:

        raise SystemExit(
            "STOP: refusing to overwrite "
            "existing PDB-registry output(s):\n"
            + "\n".join(
                str(path)
                for path in existing_outputs
            )
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    fields = [
        "pdb_id",
        "full_pdb_present",
        "full_chain_hit_count",
        "full_subject_ids",
        "full_chains",
        "full_ranks",
        "full_best_rank",
        "full_z_max",
        "full_z_min",
        "full_query_coverage_max",
        "full_seq_identity_pct_max",
        "pdb25_present",
        "pdb25_chain_hit_count",
        "pdb25_subject_ids",
        "pdb25_chains",
        "pdb25_ranks",
        "pdb25_best_rank",
        "pdb25_z_max",
        "pdb25_z_min",
        "pdb25_query_coverage_max",
        "pdb25_seq_identity_pct_max",
    ]

    with registry_path.open(
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
            registry_rows
        )

    registry_ids = [
        row["pdb_id"]
        for row in registry_rows
    ]

    full_accounted = sum(
        int(
            row[
                "full_chain_hit_count"
            ]
        )
        for row in registry_rows
    )

    pdb25_accounted = sum(
        int(
            row[
                "pdb25_chain_hit_count"
            ]
        )
        for row in registry_rows
    )

    full_unique_count = len(
        full_by_pdb
    )

    pdb25_unique_count = len(
        pdb25_by_pdb
    )

    pdb25_in_full = len(
 set(pdb25_by_pdb)
        & set(full_by_pdb)
    )

    validation_rows = [
        [
            "high_z_input_sha256",
            "PASS",
            observed_hash,
            EXPECTED_INPUT_SHA256,
        ],
        [
            "full_pdb_chain_hits",
            (
                "PASS"
                if len(full)
                == EXPECTED_FULL_CHAIN_HITS
                else "FAIL"
            ),
            str(len(full)),
            str(
                EXPECTED_FULL_CHAIN_HITS
            ),
        ],
        [
            "pdb25_chain_hits",
            (
                "PASS"
                if len(pdb25)
                == EXPECTED_PDB25_CHAIN_HITS
                else "FAIL"
            ),
            str(len(pdb25)),
            str(
                EXPECTED_PDB25_CHAIN_HITS
            ),
        ],
        [
            "registry_pdb_ids_unique",
            (
                "PASS"
                if len(registry_ids)
                == len(set(registry_ids))
                else "FAIL"
            ),
            str(
                len(set(registry_ids))
            ),
            str(
                len(registry_ids)
            ),
        ],
        [
            "full_chain_hits_accounted",
            (
                "PASS"
                if full_accounted
                == len(full)
                else "FAIL"
            ),
            str(full_accounted),
            str(len(full)),
        ],
        [
            "pdb25_chain_hits_accounted",
            (
                "PASS"
                if pdb25_accounted
                == len(pdb25)
                else "FAIL"
            ),
            str(pdb25_accounted),
            str(len(pdb25)),
        ],
        [
            "full_pdb_unique_entries",
            "OBSERVED",
            str(full_unique_count),
            "not_prespecified",
        ],
        [
            "pdb25_unique_entries",
            "OBSERVED",
            str(pdb25_unique_count),
            "not_prespecified",
        ],
        [
            "union_unique_pdb_entries",
            "OBSERVED",
            str(
                len(all_pdb_ids)
            ),
            "not_prespecified",
        ],
        [
            "pdb25_entries_also_in_full_high_z",
            "OBSERVED",
            (
                f"{pdb25_in_full}/"
                f"{pdb25_unique_count}"
            ),
            "not_prespecified",
        ],
    ]

    if any(
        row[1] == "FAIL"
        for row in validation_rows
    ):

        raise SystemExit(
            "STOP: PDB-registry "
            "validation failed."
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
        "PASS: annotation-neutral "
        "PDB registry completed."
    )

    print(
        f"full_PDB_chain_hits={len(full)}"
    )

    print(
        "full_PDB_unique_pdb_entries="
        f"{full_unique_count}"
    )

    print(
        f"PDB25_chain_hits={len(pdb25)}"
    )

    print(
        "PDB25_unique_pdb_entries="
        f"{pdb25_unique_count}"
    )

    print(
        "union_unique_pdb_entries="
        f"{len(all_pdb_ids)}"
    )

    print(
        "PDB25_entries_also_in_full_high_z="
        f"{pdb25_in_full}/"
        f"{pdb25_unique_count}"
    )

    print(
        f"wrote={registry_path}"
    )

    print(
        f"wrote={validation_path}"
    )


if __name__ == "__main__":
    main()
