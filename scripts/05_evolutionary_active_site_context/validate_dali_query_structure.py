#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
import csv


FASTA = Path("data/O67940_AQUAE.fasta")
PDB = Path("data/alphafold/AF-O67940-F1-model_v6.pdb")

OUTDIR = Path(
    "results/active_site_structure/dali_structural_neighbors"
)

OUTDIR.mkdir(parents=True, exist_ok=True)

OUT = OUTDIR / "O67940_dali_query_validation.tsv"


AA3_TO_AA1 = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
    "MSE": "M",
}


def read_fasta(path):
    sequence = []

    with path.open() as handle:
        for line in handle:
            line = line.strip()

            if not line or line.startswith(">"):
                continue

            sequence.append(line)

    return "".join(sequence)


reference = read_fasta(FASTA)

chains = defaultdict(list)
seen_residues = defaultdict(set)
plddt = defaultdict(list)


with PDB.open() as handle:

    for line in handle:

        if not line.startswith("ATOM"):
            continue

        atom = line[12:16].strip()

        # One CA atom gives one residue-level observation.
        if atom != "CA":
            continue

        altloc = line[16]

        if altloc not in (" ", "A"):
            continue

        resname = line[17:20].strip()
        chain = line[21].strip() or "<blank>"
        resseq = int(line[22:26])
        icode = line[26].strip()

        residue_id = (resseq, icode)

        if residue_id in seen_residues[chain]:
            continue

        seen_residues[chain].add(residue_id)

        if resname not in AA3_TO_AA1:
            raise SystemExit(
                f"Unsupported residue {resname} "
                f"at chain {chain} residue {resseq}{icode}"
            )

        chains[chain].append(
            (
                resseq,
                icode,
                AA3_TO_AA1[resname],
            )
        )

        # AlphaFold stores pLDDT in the PDB B-factor field.
        try:
            plddt[chain].append(
                float(line[60:66])
            )
        except ValueError:
            pass


rows = []

for chain, residues in sorted(chains.items()):

    residues = sorted(
        residues,
        key=lambda x: (x[0], x[1]),
    )

    sequence = "".join(
        residue[2]
        for residue in residues
    )

    numbers = [
        residue[0]
        for residue in residues
    ]

    exact_match = sequence == reference

    numbering_contiguous = (
        numbers
        == list(
            range(
                numbers[0],
                numbers[0] + len(numbers),
            )
        )
    )

    first_mismatch = ""

    if not exact_match:

        max_len = max(
            len(sequence),
            len(reference),
        )

        for i in range(max_len):

            pdb_aa = (
                sequence[i]
                if i < len(sequence)
                else "-"
            )

            ref_aa = (
                reference[i]
                if i < len(reference)
                else "-"
            )

            if pdb_aa != ref_aa:
                first_mismatch = (
                    f"{i + 1}:"
                    f"PDB={pdb_aa},"
                    f"FASTA={ref_aa}"
                )
                break

    confidence = plddt.get(chain, [])

    rows.append({
        "chain": chain,
        "pdb_ca_residues": len(sequence),
        "fasta_length": len(reference),
        "sequence_exact_match":
            "yes" if exact_match else "no",
        "first_residue_number":
            numbers[0] if numbers else "",
        "last_residue_number":
            numbers[-1] if numbers else "",
        "numbering_contiguous":
            "yes"
            if numbering_contiguous
            else "no",
        "first_mismatch":
            first_mismatch,
        "mean_ca_plddt":
            (
                f"{sum(confidence) / len(confidence):.4f}"
                if confidence
                else ""
            ),
        "min_ca_plddt":
            (
                f"{min(confidence):.2f}"
                if confidence
                else ""
            ),
        "max_ca_plddt":
            (
                f"{max(confidence):.2f}"
                if confidence
                else ""
            ),
    })


with OUT.open("w", newline="") as handle:

    fields = [
        "chain",
        "pdb_ca_residues",
        "fasta_length",
        "sequence_exact_match",
        "first_residue_number",
        "last_residue_number",
        "numbering_contiguous",
        "first_mismatch",
        "mean_ca_plddt",
        "min_ca_plddt",
        "max_ca_plddt",
    ]

    writer = csv.DictWriter(
        handle,
        fieldnames=fields,
        delimiter="\t",
    )

    writer.writeheader()
    writer.writerows(rows)


print(f"Reference FASTA length: {len(reference)}")
print(f"PDB chains found: {len(chains)}")

for row in rows:

    print()
    print(f"Chain: {row['chain']}")
    print(
        "CA residues: "
        f"{row['pdb_ca_residues']}"
    )
    print(
        "Exact FASTA match: "
        f"{row['sequence_exact_match']}"
    )
    print(
        "Residue numbering: "
        f"{row['first_residue_number']}"
        "-"
        f"{row['last_residue_number']}"
    )
    print(
        "Numbering contiguous: "
        f"{row['numbering_contiguous']}"
    )

    if row["first_mismatch"]:
        print(
            "First mismatch: "
            f"{row['first_mismatch']}"
        )

    if row["mean_ca_plddt"]:
        print(
            "Mean CA pLDDT: "
            f"{row['mean_ca_plddt']}"
        )
        print(
            "Minimum CA pLDDT: "
            f"{row['min_ca_plddt']}"
        )

print()
print(f"Wrote: {OUT}")

# This script is a QC gate, not only a descriptive summary.
# Fail the run if the structure is not the expected O67940 protomer.
validation_passed = (
    len(rows) == 1
    and rows[0]["chain"] == "A"
    and rows[0]["pdb_ca_residues"] == len(reference)
    and rows[0]["sequence_exact_match"] == "yes"
    and rows[0]["first_residue_number"] == 1
    and rows[0]["last_residue_number"] == len(reference)
    and rows[0]["numbering_contiguous"] == "yes"
)

if not validation_passed:
    raise SystemExit(
        "FAIL: structure did not satisfy the O67940 DALI-query validation gate."
    )

print("Validation status: PASS")
