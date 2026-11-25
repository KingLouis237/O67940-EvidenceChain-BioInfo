#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from pathlib import Path


EXPECTED_FULL_COUNT = 2406
EXPECTED_PDB25_COUNT = 639
EXPECTED_PDB50_COUNT = 859
EXPECTED_PDB90_COUNT = 1062
EXPECTED_QUERY = "s001A"
EXPECTED_DATABASE = "PDB"
QUERY_LENGTH = 251


EXPECTED_TSV_COLUMNS = [
    "query",
    "database",
    "sbjct",
    "z-score",
    "rmsd",
    "ali-length",
    "sbjct-length",
    "seq-identity",
    "sbjct-sequence",
    "compressed-sbjct-dssp",
    "description",
    "qstarts",
    "sstarts",
    "lengths",
    "rotation",
    "translation",
    "all_pfam",
]


SUMMARY_PATTERN = re.compile(
    r"^\s*"
    r"(\d+):\s+"
    r"(\S+)\s+"
    r"([-+]?\d+(?:\.\d+)?)\s+"
    r"([-+]?\d+(?:\.\d+)?)\s+"
    r"(\d+)\s+"
    r"(\d+)\s+"
    r"(\d+)"
    r"(?:\s+(.*))?$"
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            h.update(block)

    return h.hexdigest()


def verify_raw_bundle(raw_dir: Path) -> None:
    checksum_file = (
        raw_dir
        / "O67940_dali_raw_checksums.sha256"
    )

    if not checksum_file.is_file():
        raise SystemExit(
            f"STOP: missing checksum manifest: "
            f"{checksum_file}"
        )

    checked = 0

    for line in checksum_file.read_text(
        encoding="utf-8"
    ).splitlines():

        if not line.strip():
            continue

        digest, filename = line.split(
            maxsplit=1
        )

        filename = filename.strip()

        path = raw_dir / filename

        if not path.is_file():
            raise SystemExit(
                f"STOP: raw file missing: {path}"
            )

        observed = sha256(path)

        if observed != digest:
            raise SystemExit(
                f"STOP: checksum mismatch: {path}"
            )

        checked += 1

    if checked != 11:
        raise SystemExit(
            "STOP: expected 11 entries in raw "
            f"checksum manifest; observed {checked}."
        )

    print(
        f"PASS: verified {checked} frozen "
        "raw DALI artifacts."
    )


def parse_full_tsv(
    path: Path,
) -> list[dict[str, str]]:

    with path.open(
        encoding="utf-8",
        newline="",
    ) as handle:

        noncomment = (
            line
            for line in handle
            if not line.startswith("#")
        )

        reader = csv.DictReader(
            noncomment,
            delimiter="\t",
        )

        if reader.fieldnames != EXPECTED_TSV_COLUMNS:
            raise SystemExit(
                "STOP: unexpected full-PDB "
                "TSV schema."
            )

        rows = list(reader)

    if len(rows) != EXPECTED_FULL_COUNT:
        raise SystemExit(
            "STOP: full-PDB TSV count changed: "
            f"{len(rows)}"
        )

    queries = {
        row["query"]
        for row in rows
    }

    if queries != {EXPECTED_QUERY}:
        raise SystemExit(
            f"STOP: unexpected query IDs: "
            f"{sorted(queries)}"
        )

    databases = {
        row["database"]
        for row in rows
    }

    if databases != {EXPECTED_DATABASE}:
        raise SystemExit(
            f"STOP: unexpected database values: "
            f"{sorted(databases)}"
        )

    return rows


def parse_summary(
    path: Path,
) -> tuple[str, list[dict[str, object]]]:

    query = None
    rows = []

    with path.open(
        encoding="utf-8",
    ) as handle:

        for line in handle:

            if line.startswith("# Query:"):
                query = line.split(
                    ":",
                    1,
                )[1].strip()

            match = SUMMARY_PATTERN.match(
                line.rstrip("\n")
            )

            if not match:
                continue

            (
                rank,
                subject,
                z_score,
                rmsd,
                aligned_length,
                subject_length,
                identity,
                description,
            ) = match.groups()

            rows.append({
                "rank": int(rank),
                "subject": subject,
                "z_score": z_score,
                "rmsd": rmsd,
                "aligned_length": aligned_length,
                "subject_length": subject_length,
                "seq_identity_pct": identity,
                "description": (
                    description or ""
                ).rstrip(),
            })

    if query is None:
        raise SystemExit(
            f"STOP: query header missing: {path}"
        )

    return query, rows


def normalize_txt_subject(
    subject: str,
) -> str:

    # DALI TXT: 2q6i-A
    # DALI TSV: 2q6iA
    #
    # Preserve everything after the four-character
    # PDB ID; chain identifiers are not assumed to
    # be alphabetic or exactly one character long.

    if (
        len(subject) >= 6
        and subject[4] == "-"
    ):
        return (
            subject[:4]
            + subject[5:]
        )

    return subject


def split_subject(
    subject: str,
) -> tuple[str, str]:

    if len(subject) < 5:
        raise SystemExit(
            f"STOP: cannot split DALI subject: "
            f"{subject!r}"
        )

    return (
        subject[:4],
        subject[4:],
    )


def assert_contiguous(
    label: str,
    rows: list[dict[str, object]],
) -> None:

    observed = [
        int(row["rank"])
        for row in rows
    ]

    expected = list(
        range(
            1,
            len(rows) + 1,
        )
    )

    if observed != expected:
        raise SystemExit(
            f"STOP: non-contiguous ranks: "
            f"{label}"
        )


def cross_validate_full(
    tsv_rows: list[dict[str, str]],
    txt_rows: list[dict[str, object]],
) -> None:

    if len(tsv_rows) != len(txt_rows):
        raise SystemExit(
            "STOP: full-PDB TXT/TSV "
            "counts differ."
        )

    mismatches = []

    for rank, (tsv, txt) in enumerate(
        zip(
            tsv_rows,
            txt_rows,
        ),
        start=1,
    ):

        checks = {
            "rank": (
                int(txt["rank"]) == rank
            ),
            "subject": (
                normalize_txt_subject(
                    str(txt["subject"])
                )
                == tsv["sbjct"]
            ),
            "z_score": (
                float(str(txt["z_score"]))
                == float(tsv["z-score"])
            ),
            "rmsd": (
                float(str(txt["rmsd"]))
                == float(tsv["rmsd"])
            ),
            "aligned_length": (
                int(str(txt["aligned_length"]))
                == int(tsv["ali-length"])
            ),
            "subject_length": (
                int(str(txt["subject_length"]))
                == int(tsv["sbjct-length"])
            ),
            "identity": (
                int(str(txt["seq_identity_pct"]))
                == int(tsv["seq-identity"])
            ),
        }

        failed = [
            name
            for name, passed in checks.items()
            if not passed
        ]

        if failed:
            mismatches.append(
                (rank, failed)
            )

    if mismatches:
        raise SystemExit(
            "STOP: full-PDB TXT/TSV "
            f"mismatches: {mismatches[:10]}"
        )


def write_full_table(
    rows: list[dict[str, str]],
    output: Path,
) -> None:

    fields = [
        "search_view",
        "rank",
        "query_id",
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
        "description",
        "subject_sequence",
        "compressed_subject_dssp",
        "qstarts",
        "sstarts",
        "lengths",
        "rotation",
        "translation",
        "all_pfam",
    ]

    with output.open(
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

        for rank, row in enumerate(
            rows,
            start=1,
        ):

            pdb_id, chain_id = split_subject(
                row["sbjct"]
            )

            aligned = int(
                row["ali-length"]
            )

            writer.writerow({
                "search_view": "full_PDB",
                "rank": rank,
                "query_id": row["query"],
                "subject_id": row["sbjct"],
                "pdb_id": pdb_id,
                "chain_id": chain_id,
                "z_score": row["z-score"],
                "rmsd": row["rmsd"],
                "aligned_length": (
                    row["ali-length"]
                ),
                "subject_length": (
                    row["sbjct-length"]
                ),
                "query_length": QUERY_LENGTH,
                "query_coverage": (
                    f"{aligned / QUERY_LENGTH:.6f}"
                ),
                "seq_identity_pct": (
                    row["seq-identity"]
                ),
                "description": (
                    row["description"].rstrip()
                ),
                "subject_sequence": (
                    row["sbjct-sequence"]
                ),
                "compressed_subject_dssp": (
                    row[
                        "compressed-sbjct-dssp"
                    ]
                ),
                "qstarts": row["qstarts"],
                "sstarts": row["sstarts"],
                "lengths": row["lengths"],
                "rotation": row["rotation"],
                "translation": (
                    row["translation"]
                ),
                "all_pfam": row["all_pfam"],
            })


def write_summary_table(
    query: str,
    rows: list[dict[str, object]],
    search_view: str,
    output: Path,
) -> None:

    fields = [
        "search_view",
        "rank",
        "query_id",
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
        "description",
    ]

    with output.open(
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

        for row in rows:

            subject_id = normalize_txt_subject(
                str(row["subject"])
            )

            pdb_id, chain_id = split_subject(
                subject_id
            )

            aligned = int(
                str(row["aligned_length"])
            )

            writer.writerow({
                "search_view": search_view,
                "rank": row["rank"],
                "query_id": query,
                "subject_id": subject_id,
                "pdb_id": pdb_id,
                "chain_id": chain_id,
                "z_score": row["z_score"],
                "rmsd": row["rmsd"],
                "aligned_length": (
                    row["aligned_length"]
                ),
                "subject_length": (
                    row["subject_length"]
                ),
                "query_length": QUERY_LENGTH,
                "query_coverage": (
                    f"{aligned / QUERY_LENGTH:.6f}"
                ),
                "seq_identity_pct": (
                    row["seq_identity_pct"]
                ),
                "description": (
                    row["description"]
                ),
            })


def write_validation(
    output: Path,
    full_count: int,
    pdb25_count: int,
    pdb50_count: int,
    pdb90_count: int,
) -> None:

    rows = [
        (
            "raw_bundle_checksum_validation",
            "PASS",
            "11 files verified",
            "11 files verified",
        ),
        (
            "full_pdb_tsv_schema",
            "PASS",
            "17 columns",
            "17 columns",
        ),
        (
            "full_pdb_record_count",
            "PASS",
            str(full_count),
            str(EXPECTED_FULL_COUNT),
        ),
        (
            "pdb25_record_count",
            "PASS",
            str(pdb25_count),
            str(EXPECTED_PDB25_COUNT),
        ),
        (
            "pdb50_record_count",
            "PASS",
            str(pdb50_count),
            str(EXPECTED_PDB50_COUNT),
        ),
        (
            "pdb90_record_count",
            "PASS",
            str(pdb90_count),
            str(EXPECTED_PDB90_COUNT),
        ),
        (
            "full_pdb_tsv_txt_mismatches",
            "PASS",
            "0",
            "0",
        ),
        (
            "full_pdb_rank_continuity",
            "PASS",
            f"1..{full_count}",
            f"1..{EXPECTED_FULL_COUNT}",
        ),
        (
            "pdb25_rank_continuity",
            "PASS",
            f"1..{pdb25_count}",
            f"1..{EXPECTED_PDB25_COUNT}",
        ),
        (
            "pdb50_rank_continuity",
            "PASS",
            f"1..{pdb50_count}",
            f"1..{EXPECTED_PDB50_COUNT}",
        ),
        (
            "pdb90_rank_continuity",
            "PASS",
            f"1..{pdb90_count}",
            f"1..{EXPECTED_PDB90_COUNT}",
        ),
    ]

    with output.open(
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

        writer.writerows(rows)


def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "Parse and validate the frozen "
            "O67940 DALI structural-neighbour "
            "server outputs."
        )
    )

    parser.add_argument(
        "--raw-dir",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
    )

    args = parser.parse_args()

    raw = args.raw_dir
    out = args.output_dir

    out.mkdir(
        parents=True,
        exist_ok=True,
    )

    verify_raw_bundle(raw)

    full_tsv = parse_full_tsv(
        raw / "s001A.dali.tsv"
    )

    full_query, full_txt = parse_summary(
        raw / "s001A.txt"
    )

    pdb25_query, pdb25 = parse_summary(
        raw / "s001A-25.txt"
    )

    pdb50_query, pdb50 = parse_summary(
        raw / "s001A-50.txt"
    )

    pdb90_query, pdb90 = parse_summary(
        raw / "s001A-90.txt"
    )

    for label, query in [
        ("full_PDB", full_query),
        ("PDB25", pdb25_query),
        ("PDB50", pdb50_query),
        ("PDB90", pdb90_query),
    ]:

        if query != EXPECTED_QUERY:
            raise SystemExit(
                "STOP: unexpected query in "
                f"{label}: {query}"
            )

    expected_counts = {
        "full_PDB": (
            full_txt,
            EXPECTED_FULL_COUNT,
        ),
        "PDB25": (
            pdb25,
            EXPECTED_PDB25_COUNT,
        ),
        "PDB50": (
            pdb50,
            EXPECTED_PDB50_COUNT,
        ),
        "PDB90": (
            pdb90,
            EXPECTED_PDB90_COUNT,
        ),
    }

    for label, (
        rows,
        expected_count,
    ) in expected_counts.items():

        if len(rows) != expected_count:
            raise SystemExit(
                f"STOP: {label} count "
                f"changed: {len(rows)}"
            )

        assert_contiguous(
            label,
            rows,
        )

    cross_validate_full(
        full_tsv,
        full_txt,
    )

    full_output = (
        out
        / "O67940_dali_full_pdb_matches.tsv"
    )

    pdb25_output = (
        out
        / "O67940_dali_pdb25_matches.tsv"
    )

    validation_output = (
        out
        / "O67940_dali_parser_validation.tsv"
    )

    write_full_table(
        full_tsv,
        full_output,
    )

    write_summary_table(
        pdb25_query,
        pdb25,
        "PDB25",
        pdb25_output,
    )

    write_validation(
        validation_output,
        len(full_txt),
        len(pdb25),
        len(pdb50),
        len(pdb90),
    )

    print(
        "PASS: DALI parsing completed."
    )

    print(
        f"full_PDB_rows={len(full_tsv)}"
    )

    print(
        f"PDB25_rows={len(pdb25)}"
    )

    print(
        "PDB50/PDB90 validated but "
        "not emitted as inferential tables."
    )

    print(
        f"wrote={full_output}"
    )

    print(
        f"wrote={pdb25_output}"
    )

    print(
        f"wrote={validation_output}"
    )


if __name__ == "__main__":
    main()
