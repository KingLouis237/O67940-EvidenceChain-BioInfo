#!/usr/bin/env python3

from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from datetime import date

out_dir = Path("data/databases/O67940_uniprot_pfam_candidates")
out_dir.mkdir(parents=True, exist_ok=True)

query = (
    "(xref:pfam-PF01887) AND "
    "(xref:pfam-PF20257) AND "
    "(fragment:false) AND "
    "(length:[200 TO 350])"
)

base = "https://rest.uniprot.org/uniprotkb/stream"

metadata_fields = ",".join([
    "accession",
    "id",
    "reviewed",
    "protein_name",
    "gene_names",
    "organism_name",
    "organism_id",
    "length",
])

metadata_url = (
    f"{base}?query={quote(query)}"
    f"&format=tsv&fields={metadata_fields}"
)

fasta_url = (
    f"{base}?query={quote(query)}"
    f"&format=fasta"
)


def download(url, path):
    request = Request(
        url,
        headers={"User-Agent": "O67940-reproducible-reanalysis"},
    )

    with urlopen(request) as response:
        data = response.read()

    path.write_bytes(data)


metadata_path = out_dir / "candidate_metadata.tsv"
fasta_path = out_dir / "candidate_sequences.fasta"
query_path = out_dir / "query.txt"

download(metadata_url, metadata_path)
download(fasta_url, fasta_path)

query_path.write_text(
    f"date_accessed\t{date.today().isoformat()}\n"
    f"query\t{query}\n"
    f"metadata_url\t{metadata_url}\n"
    f"fasta_url\t{fasta_url}\n"
)

metadata_rows = sum(1 for _ in metadata_path.open()) - 1
fasta_records = sum(
    1
    for line in fasta_path.read_text().splitlines()
    if line.startswith(">")
)

print(f"Metadata rows: {metadata_rows}")
print(f"FASTA records: {fasta_records}")
print(f"Metadata: {metadata_path}")
print(f"FASTA: {fasta_path}")
print(f"Query record: {query_path}")

if metadata_rows != fasta_records:
    raise SystemExit(
        f"Count mismatch: metadata={metadata_rows}, FASTA={fasta_records}"
    )
