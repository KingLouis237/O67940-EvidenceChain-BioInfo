from pathlib import Path

# Three-letter to one-letter amino acid code
AA3_TO_AA1 = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
    "SEC": "U", "PYL": "O",
}

STRUCTURES = [
    {
        "label": "O67940_AQUAE_AlphaFold_chainA",
        "pdb_path": Path("data/alphafold/AF-O67940-F1-model_v6.pdb"),
        "chain": "A",
        "description": "AlphaFoldDB v6 predicted structure for O67940_AQUAE",
    },
    {
        "label": "2Q6O_chainA",
        "pdb_path": Path("data/pdb/2Q6O.pdb"),
        "chain": "A",
        "description": "Reference chlorinase-related structure, chain A",
    },
    {
        "label": "1RQP_chainA",
        "pdb_path": Path("data/pdb/1RQP.pdb"),
        "chain": "A",
        "description": "Reference fluorinase structure, chain A",
    },
]

RESULTS_DIR = Path("results/pdb")
DATA_DIR = Path("data/reference_sequences")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

def extract_chain_sequence_from_pdb(pdb_path: Path, chain_id: str):
    """
    Extract one amino-acid sequence from ATOM records in a PDB file.

    Important:
    - We use only ATOM records, not HETATM records.
    - We keep one residue per unique residue number/insertion-code combination.
    - This gives the resolved/modelled protein-chain sequence in the structure file.
    """
    residues = []
    seen_residues = set()

    with pdb_path.open(errors="ignore") as handle:
        for line in handle:
            if not line.startswith("ATOM"):
                continue

            current_chain = line[21].strip() or "_"
            if current_chain != chain_id:
                continue

            resname = line[17:20].strip()
            resseq = line[22:26].strip()
            icode = line[26].strip()
            residue_key = (current_chain, resseq, icode)

            if residue_key in seen_residues:
                continue

            seen_residues.add(residue_key)
            aa = AA3_TO_AA1.get(resname, "X")
            residues.append((residue_key, resname, aa))

    sequence = "".join(aa for _, _, aa in residues)
    return sequence, residues

summary_rows = []
fasta_entries = []

for item in STRUCTURES:
    sequence, residues = extract_chain_sequence_from_pdb(item["pdb_path"], item["chain"])

    fasta_entries.append(
        f">{item['label']} | {item['description']} | source={item['pdb_path']}\n"
        f"{sequence}\n"
    )

    summary_rows.append({
        "label": item["label"],
        "source_file": str(item["pdb_path"]),
        "chain": item["chain"],
        "sequence_length": len(sequence),
        "first_10_aa": sequence[:10],
        "last_10_aa": sequence[-10:],
        "contains_unknown_X": "yes" if "X" in sequence else "no",
    })

# Write combined FASTA for later alignment
fasta_path = DATA_DIR / "O67940_2Q6O_1RQP_chainA_sequences.fasta"
with fasta_path.open("w") as out:
    for entry in fasta_entries:
        out.write(entry)

# Write summary table
summary_path = RESULTS_DIR / "reference_chainA_sequence_summary.tsv"
with summary_path.open("w") as out:
    out.write(
        "label\tsource_file\tchain\tsequence_length\tfirst_10_aa\tlast_10_aa\tcontains_unknown_X\n"
    )
    for row in summary_rows:
        out.write(
            f"{row['label']}\t{row['source_file']}\t{row['chain']}\t"
            f"{row['sequence_length']}\t{row['first_10_aa']}\t"
            f"{row['last_10_aa']}\t{row['contains_unknown_X']}\n"
        )

print(f"Wrote FASTA to: {fasta_path}")
print(f"Wrote summary to: {summary_path}")
