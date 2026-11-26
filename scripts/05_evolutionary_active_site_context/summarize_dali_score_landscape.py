#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import hashlib
import statistics
from pathlib import Path


EXPECTED = {
    "full_PDB": {
        "sha256": (
            "f23da6edcb8c0962c803b5a6a0dbfa968cf6bb8e172c6ca296174269c8d09d15"
        ),
        "rows": 2406,
    },
    "PDB25": {
        "sha256": (
            "f945016edd1e3bbdd8976cf798f440c81755ae3b5310b880d1c710c7ca5f8946"
        ),
        "rows": 639,
    },
}


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


def percentile(values, p):

    values = sorted(values)

    pos = (
        len(values) - 1
    ) * p

    lo = int(pos)
    hi = min(
        lo + 1,
        len(values) - 1,
    )

    frac = pos - lo

    return (
        values[lo]
        + frac
        * (
            values[hi]
            - values[lo]
        )
    )


def analyse_view(
    label,
    path,
):

    expected = EXPECTED[label]

    observed_hash = sha256(path)

    if observed_hash != expected["sha256"]:
        raise SystemExit(
            f"STOP: checksum mismatch: {label}"
        )

    rows = read_tsv(path)

    if len(rows) != expected["rows"]:
        raise SystemExit(
            f"STOP: record-count mismatch: {label}"
        )

    ranks = [
        int(row["rank"])
        for row in rows
    ]

    if ranks != list(
        range(
            1,
            len(rows) + 1,
        )
    ):
        raise SystemExit(
            f"STOP: rank discontinuity: {label}"
        )

    z = [
        float(row["z_score"])
        for row in rows
    ]

    if any(
        z[i] < z[i + 1]
        for i in range(
            len(z) - 1
        )
    ):
        raise SystemExit(
            f"STOP: Z ranking not non-increasing: {label}"
        )

    gaps = []

    for i in range(
        len(rows) - 1
    ):

        gaps.append({
            "search_view": label,
            "left_rank": i + 1,
            "right_rank": i + 2,
            "left_subject_id": (
                rows[i]["subject_id"]
            ),
            "right_subject_id": (
                rows[i + 1]["subject_id"]
            ),
            "z_left": z[i],
            "z_right": z[i + 1],
            "z_drop": round(
                z[i] - z[i + 1],
                3,
            ),
        })

    boundary = max(
        gaps,
        key=lambda x: (
            x["z_drop"],
            -x["left_rank"],
        ),
    )

    boundary_rank = (
        boundary["left_rank"]
    )

    cluster = rows[
        :boundary_rank
    ]

    positive_first100 = [
        gap["z_drop"]
        for gap in gaps
        if (
            gap["left_rank"] <= 100
            and gap["z_drop"] > 0
        )
    ]

    median_positive_gap = (
        statistics.median(
            positive_first100
        )
    )

    summary = {
        "search_view": label,
        "record_count": len(rows),
        "z_max": round(
            max(z),
            3,
        ),
        "z_median": round(
            statistics.median(z),
            3,
        ),
        "z_p75": round(
            percentile(z, 0.75),
            3,
        ),
        "z_p90": round(
            percentile(z, 0.90),
            3,
        ),
        "z_p95": round(
            percentile(z, 0.95),
            3,
        ),
        "z_p99": round(
            percentile(z, 0.99),
            3,
        ),
        "largest_gap_left_rank": (
            boundary["left_rank"]
        ),
        "largest_gap_right_rank": (
            boundary["right_rank"]
        ),
        "largest_gap_z_left": round(
            boundary["z_left"],
            3,
        ),
        "largest_gap_z_right": round(
            boundary["z_right"],
            3,
        ),
        "largest_gap_size": round(
            boundary["z_drop"],
            3,
        ),
        "high_z_cluster_size": (
            len(cluster)
        ),
        "high_z_cluster_min_z": round(
            float(
                cluster[-1][
                    "z_score"
                ]
            ),
            3,
        ),
        "first_tail_z": round(
            boundary["z_right"],
            3,
        ),
        "first100_positive_gap_median": round(
            median_positive_gap,
            3,
        ),
        "largest_to_median_gap_ratio": round(
            (
                boundary["z_drop"]
                / median_positive_gap
            ),
            3,
        ),
        "boundary_rule": (
            "largest_adjacent_z_score_drop"
        ),
    }

    return (
        rows,
        cluster,
        gaps,
        summary,
    )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--full-pdb",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--pdb25",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
    )

    args = parser.parse_args()

    output_names = [
        "O67940_dali_score_landscape_summary.tsv",
        "O67940_dali_adjacent_z_gaps.tsv",
        "O67940_dali_high_z_cluster.tsv",
    ]

    existing_outputs = [
        args.output_dir / name
        for name in output_names
        if (
            args.output_dir / name
        ).exists()
    ]

    if existing_outputs:
        joined = "\n".join(
            str(path)
            for path in existing_outputs
        )

        raise SystemExit(
            "STOP: refusing to overwrite existing "
            "score-landscape output(s):\n"
            f"{joined}"
        )

    args.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    analyses = []

    for label, path in [
        (
            "full_PDB",
            args.full_pdb,
        ),
        (
            "PDB25",
            args.pdb25,
        ),
    ]:

        analyses.append(
            (
                label,
                path,
                *analyse_view(
                    label,
                    path,
                ),
            )
        )

    summary_path = (
        args.output_dir
        / "O67940_dali_score_landscape_summary.tsv"
    )

    summary_fields = [
        "search_view",
        "record_count",
        "z_max",
        "z_median",
        "z_p75",
        "z_p90",
        "z_p95",
        "z_p99",
        "largest_gap_left_rank",
        "largest_gap_right_rank",
        "largest_gap_z_left",
        "largest_gap_z_right",
        "largest_gap_size",
        "high_z_cluster_size",
        "high_z_cluster_min_z",
        "first_tail_z",
        "first100_positive_gap_median",
        "largest_to_median_gap_ratio",
        "boundary_rule",
    ]

    with summary_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=summary_fields,
            delimiter="\t",
            lineterminator="\n",
        )

        writer.writeheader()

        for (
            label,
            path,
            rows,
            cluster,
            gaps,
            summary,
        ) in analyses:

            writer.writerow(
                summary
            )

    gaps_path = (
        args.output_dir
        / "O67940_dali_adjacent_z_gaps.tsv"
    )

    gap_fields = [
        "search_view",
        "left_rank",
        "right_rank",
        "left_subject_id",
        "right_subject_id",
        "z_left",
        "z_right",
        "z_drop",
    ]

    with gaps_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=gap_fields,
            delimiter="\t",
            lineterminator="\n",
        )

        writer.writeheader()

        for analysis in analyses:
            for gap in analysis[4]:
                writer.writerow(
                    gap
                )

    cluster_path = (
        args.output_dir
        / "O67940_dali_high_z_cluster.tsv"
    )

    cluster_fields = [
        "search_view",
        "rank",
        "subject_id",
        "pdb_id",
        "chain_id",
        "z_score",
        "rmsd",
        "aligned_length",
        "subject_length",
        "query_length",
        "query_coverage",
        "seq_identity_pct",
    ]

    with cluster_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=cluster_fields,
            delimiter="\t",
            lineterminator="\n",
        )

        writer.writeheader()

        for (
            label,
            path,
            rows,
            cluster,
            gaps,
            summary,
        ) in analyses:

            for row in cluster:

                writer.writerow({
                    "search_view": label,
                    "rank": row["rank"],
                    "subject_id": (
                        row["subject_id"]
                    ),
                    "pdb_id": (
                        row["pdb_id"]
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
                })

    print(
        "PASS: DALI score-landscape "
        "analysis completed."
    )

    for analysis in analyses:

        summary = analysis[5]

        print(
            f"{summary['search_view']}: "
            f"cluster_size="
            f"{summary['high_z_cluster_size']}, "
            f"boundary="
            f"{summary['largest_gap_left_rank']}"
            f"->{summary['largest_gap_right_rank']}, "
            f"Z="
            f"{summary['largest_gap_z_left']}"
            f"->{summary['largest_gap_z_right']}, "
            f"drop="
            f"{summary['largest_gap_size']}"
        )

    print(
        f"wrote={summary_path}"
    )

    print(
        f"wrote={gaps_path}"
    )

    print(
        f"wrote={cluster_path}"
    )


if __name__ == "__main__":
    main()
