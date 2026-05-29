from pathlib import Path
from urllib.request import urlretrieve
import os

# Reference structures used in the original paper
# 2Q6O: chlorinase-related reference
# 1RQP: fluorinase reference
PDB_IDS = ["2Q6O", "1RQP"]

DATA_DIR = Path("data/pdb")
RESULTS_DIR = Path("results/pdb")
NOTES_DIR = Path("notes/pdb")
FIGURES_DIR = Path("figures/pdb")

for folder in [DATA_DIR, RESULTS_DIR, NOTES_DIR, FIGURES_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

summary_rows = []

for pdb_id in PDB_IDS:
    for ext in ["cif", "pdb"]:
        url = f"https://files.rcsb.org/download/{pdb_id}.{ext}"
        output_path = DATA_DIR / f"{pdb_id}.{ext}"

        print(f"Downloading {url}")
        urlretrieve(url, output_path)

        file_size = output_path.stat().st_size

        atom_count = "NA"
        if ext == "pdb":
            with output_path.open(errors="ignore") as handle:
                atom_count = sum(1 for line in handle if line.startswith("ATOM"))

        status = "OK"
        if file_size < 1000:
            status = "WARNING_SMALL_FILE"

        summary_rows.append({
            "pdb_id": pdb_id,
            "format": ext,
            "url": url,
            "local_file": str(output_path),
            "file_size_bytes": file_size,
            "atom_count_if_pdb": atom_count,
            "status": status,
        })

summary_path = RESULTS_DIR / "reference_structure_download_summary.tsv"

with summary_path.open("w") as out:
    out.write(
        "pdb_id\tformat\turl\tlocal_file\tfile_size_bytes\tatom_count_if_pdb\tstatus\n"
    )
    for row in summary_rows:
        out.write(
            f"{row['pdb_id']}\t{row['format']}\t{row['url']}\t"
            f"{row['local_file']}\t{row['file_size_bytes']}\t"
            f"{row['atom_count_if_pdb']}\t{row['status']}\n"
        )

print(f"Summary written to {summary_path}")
