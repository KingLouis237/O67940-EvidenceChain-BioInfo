import json
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# InterPro and Pfam entries found in the current UniProtKB record for O67940_AQUAE
ENTRIES = [
    ("interpro", "IPR046470"),
    ("interpro", "IPR046469"),
    ("interpro", "IPR002747"),
    ("interpro", "IPR023227"),
    ("interpro", "IPR023228"),
    ("pfam", "PF20257"),
    ("pfam", "PF01887"),
]

DATA_DIR = Path("data/interpro_pfam")
RESULTS_DIR = Path("results")
NOTES_DIR = Path("notes")

DATA_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
NOTES_DIR.mkdir(parents=True, exist_ok=True)


def fetch_json(entry_type: str, accession: str) -> dict:
    """
    Download metadata for one InterPro/Pfam entry using the EBI InterPro API.
    """
    url = f"https://www.ebi.ac.uk/interpro/api/entry/{entry_type}/{accession}"
    request = Request(url, headers={"User-Agent": "methods-bioinfo-reanalysis/1.0"})

    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise RuntimeError(
            f"HTTP error for {entry_type}:{accession}: {error.code} {error.reason}"
        ) from error
    except URLError as error:
        raise RuntimeError(
            f"URL/DNS error for {entry_type}:{accession}: {error.reason}"
        ) from error


def extract_name_fields(metadata: dict) -> tuple[str, str]:
    """
    Extract full and short names from InterPro API metadata.

    Some entries store metadata['name'] as:
        {"name": "...", "short": "..."}
    Others may store it as a simple string.
    """
    raw_name = metadata.get("name", "NA")

    if isinstance(raw_name, dict):
        full_name = raw_name.get("name", "NA")
        short_name = raw_name.get("short", "NA")
    else:
        full_name = raw_name
        short_name = metadata.get("short_name", "NA")

    return full_name, short_name


rows = []

for entry_type, accession in ENTRIES:
    print(f"Fetching {entry_type}:{accession}")

    record = fetch_json(entry_type, accession)

    # Save raw API response for reproducibility
    raw_path = DATA_DIR / f"{accession}.json"
    with raw_path.open("w") as file:
        json.dump(record, file, indent=2)

    metadata = record.get("metadata", {})

    name, short_name = extract_name_fields(metadata)
    entry_kind = metadata.get("type", "NA")

    description = metadata.get("description", "NA")
    if isinstance(description, str):
        description = description.replace("\n", " ")
    else:
        description = "NA"

    rows.append({
        "database": entry_type,
        "accession": accession,
        "name": name,
        "short_name": short_name,
        "type": entry_kind,
        "description": description,
    })

    # Be gentle with the API
    time.sleep(0.5)


# Write TSV results
tsv_path = RESULTS_DIR / "O67940_interpro_pfam_metadata.tsv"
with tsv_path.open("w") as out:
    out.write("database\taccession\tname\tshort_name\ttype\tdescription\n")
    for row in rows:
        out.write(
            f"{row['database']}\t{row['accession']}\t{row['name']}\t"
            f"{row['short_name']}\t{row['type']}\t{row['description']}\n"
        )


# Write markdown summary
md_path = NOTES_DIR / "step2_interpro_pfam_metadata_summary.md"
with md_path.open("w") as out:
    out.write("# Step 2 — InterPro/Pfam metadata for O67940_AQUAE\n\n")

    out.write("## Aim\n\n")
    out.write(
        "This step decodes the InterPro and Pfam cross-references found in the current "
        "UniProtKB record for O67940_AQUAE. The goal is to determine whether modern "
        "family/domain signatures support the broad functional interpretation proposed "
        "in the original article.\n\n"
    )

    out.write("## Retrieved entries\n\n")
    out.write("| Database | Accession | Name | Short name | Type |\n")
    out.write("|---|---|---|---|---|\n")

    for row in rows:
        out.write(
            f"| {row['database']} | {row['accession']} | {row['name']} | "
            f"{row['short_name']} | {row['type']} |\n"
        )

    out.write("\n## Interpretation placeholder\n\n")
    out.write(
        "Interpretation to be added after reviewing the names and descriptions of the "
        "retrieved InterPro/Pfam entries.\n"
    )


print(f"Metadata table written to: {tsv_path}")
print(f"Markdown summary written to: {md_path}")
