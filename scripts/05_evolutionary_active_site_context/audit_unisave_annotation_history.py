#!/usr/bin/env python3

"""
Reconstruct function-relevant annotation changes across all archived
UniSave versions of O67940.

This script deliberately tracks annotation evidence rather than every
administrative/taxonomic change in the UniProt record.
"""

import csv
import json
import re
import time
import urllib.request
from pathlib import Path


ACCESSION = "O67940"

RAW_ROOT = Path(
    "results/post2008_annotation_audit/raw/unisave_versions"
)

OUT_ROOT = Path(
    "results/post2008_annotation_audit/parsed"
)

RAW_ROOT.mkdir(parents=True, exist_ok=True)
OUT_ROOT.mkdir(parents=True, exist_ok=True)


def fetch_version(version):
    """Download one archived UniSave record, unless already cached."""

    path = RAW_ROOT / f"O67940_unisave_v{version:03d}.txt"

    if path.exists():
        return path

    url = (
        "https://rest.uniprot.org/unisave/"
        f"{ACCESSION}?format=txt&versions={version}"
    )

    with urllib.request.urlopen(url) as response:
        text = response.read().decode("utf-8")

    path.write_text(text)

    # Small delay: this is an audit, not a high-throughput download.
    time.sleep(0.1)

    return path


def parse_record(path, history_record):
    """Extract the function-relevant evidence fields from one entry."""

    text = path.read_text()
    lines = text.splitlines()

    # Version/date metadata come from the UniSave history endpoint.
    # This avoids dependence on historical flat-file DT syntax, which
    # differs substantially across older TrEMBL releases.
    entry_version = int(history_record["entryVersion"])
    entry_date = history_record["firstReleaseDate"]
    description = []
    protein_existence = None

    function_parts = []
    similarity_parts = []
    active_comment = None

    tracked_dbs = {
        "InterPro",
        "Pfam",
        "PANTHER",
        "PIRSF",
        "Gene3D",
        "SUPFAM",
    }

    database_refs = {db: [] for db in tracked_dbs}

    for line in lines:

        # Example:
        # DT   22-JUL-2008, entry version 33.
        if line.startswith("DT   ") and "entry version" in line:
            m = re.search(
                r"DT\s+([^,]+), entry version (\d+)",
                line
            )
            if m:
                entry_date = m.group(1)
                entry_version = int(m.group(2))

        elif line.startswith("DE   "):
            description.append(line[5:].strip())

        elif line.startswith("PE   "):
            protein_existence = line[5:].strip().rstrip(";")

        # Start of a UniProt comment block.
        elif line.startswith("CC   -!- "):
            m = re.match(
                r"CC   -!- ([A-Z ]+):\s*(.*)",
                line
            )

            active_comment = None

            if m:
                active_comment = m.group(1).strip()
                content = m.group(2).strip()

                if active_comment == "FUNCTION":
                    function_parts.append(content)

                elif active_comment == "SIMILARITY":
                    similarity_parts.append(content)

        # Continuation of the previous CC block.
        elif line.startswith("CC       "):

            content = line[5:].strip()

            if active_comment == "FUNCTION":
                function_parts.append(content)

            elif active_comment == "SIMILARITY":
                similarity_parts.append(content)

        elif line.startswith("DR   "):
            content = line[5:].strip()

            parts = [
                x.strip().rstrip(".")
                for x in content.split(";")
            ]

            if parts and parts[0] in tracked_dbs:
                db = parts[0]
                database_refs[db].append(
                    "; ".join(parts[1:])
                )

    return {
        "entry_version": entry_version,
        "entry_date": entry_date,
        "description": " ".join(description),
        "protein_existence": protein_existence or "",
        "function_comment": " ".join(function_parts),
        "similarity_comment": " ".join(similarity_parts),
        "InterPro": " | ".join(database_refs["InterPro"]),
        "Pfam": " | ".join(database_refs["Pfam"]),
        "PANTHER": " | ".join(database_refs["PANTHER"]),
        "PIRSF": " | ".join(database_refs["PIRSF"]),
        "Gene3D": " | ".join(database_refs["Gene3D"]),
        "SUPFAM": " | ".join(database_refs["SUPFAM"]),
    }


# Use the already preserved UniSave history as the version authority.
history_files = sorted(
    Path("results/post2008_annotation_audit/raw")
    .glob("O67940_unisave_history_*.json")
)

if not history_files:
    raise SystemExit("UniSave history JSON not found.")

history = json.loads(
    history_files[-1].read_text()
)["results"]

versions = sorted(
    int(r["entryVersion"])
    for r in history
)

history_by_version = {
    int(r["entryVersion"]): r
    for r in history
}

records = []

for version in versions:
    path = fetch_version(version)
    records.append(
        parse_record(
            path,
            history_by_version[version]
        )
    )


# Full function-relevant history table.
full_out = OUT_ROOT / "O67940_unisave_annotation_history.tsv"

fieldnames = list(records[0].keys())

with full_out.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        delimiter="\t",
        fieldnames=fieldnames
    )
    writer.writeheader()
    writer.writerows(records)


# Identify only versions where a tracked field changed.
tracked_fields = [
    "description",
    "protein_existence",
    "function_comment",
    "similarity_comment",
    "InterPro",
    "Pfam",
    "PANTHER",
    "PIRSF",
    "Gene3D",
    "SUPFAM",
]

change_rows = []
previous = None

for record in records:

    if previous is None:
        changed = tracked_fields.copy()
    else:
        changed = [
            field
            for field in tracked_fields
            if record[field] != previous[field]
        ]

    if changed:
        row = record.copy()
        row["changed_fields"] = ",".join(changed)
        change_rows.append(row)

    previous = record


changes_out = (
    OUT_ROOT /
    "O67940_unisave_annotation_change_points.tsv"
)

change_fieldnames = [
    "entry_version",
    "entry_date",
    "changed_fields",
] + tracked_fields

with changes_out.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        delimiter="\t",
        fieldnames=change_fieldnames
    )
    writer.writeheader()

    for row in change_rows:
        writer.writerow({
            field: row.get(field, "")
            for field in change_fieldnames
        })


print("Archived versions:", len(records))
print("Function-relevant change points:", len(change_rows))
print()

for row in change_rows:
    print(
        f"v{row['entry_version']:>3}",
        row["entry_date"],
        "changed:",
        row["changed_fields"],
    )

print()
print("Wrote:", full_out)
print("Wrote:", changes_out)
