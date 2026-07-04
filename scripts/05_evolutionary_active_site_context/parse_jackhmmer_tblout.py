#!/usr/bin/env python3

from pathlib import Path
import argparse
import csv


COLUMNS = [
    "target_id",
    "target_accession",
    "query_id",
    "query_accession",
    "full_evalue",
    "full_score",
    "full_bias",
    "best_domain_evalue",
    "best_domain_score",
    "best_domain_bias",
    "domain_exp",
    "domain_reg",
    "domain_clu",
    "domain_ov",
    "domain_env",
    "domain_dom",
    "domain_rep",
    "domain_inc",
    "description",
]


def safe_float(value):
    try:
        return float(value)
    except ValueError:
        return float("inf")


def parse_tblout(tblout_path):
    rows = []

    for line in Path(tblout_path).read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue

        parts = line.split(maxsplit=18)

        if len(parts) < 18:
            continue

        if len(parts) == 18:
            parts.append("")

        row = dict(zip(COLUMNS, parts))
        rows.append(row)

    rows.sort(
        key=lambda row: (
            safe_float(row["full_evalue"]),
            -safe_float(row["full_score"]),
        )
    )

    return rows


def main():
    parser = argparse.ArgumentParser(
        description="Parse JackHMMER tblout into a simple TSV file."
    )
    parser.add_argument("--tblout", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    rows = parse_tblout(args.tblout)

    with open(args.out, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} hits to {args.out}")


if __name__ == "__main__":
    main()
