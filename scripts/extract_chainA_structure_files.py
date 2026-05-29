from pathlib import Path

STRUCTURES = [
    {
        "label": "O67940_AQUAE_AlphaFold_chainA",
        "input_pdb": Path("data/alphafold/AF-O67940-F1-model_v6.pdb"),
        "chain": "A",
        "output_pdb": Path("data/structure_chains/O67940_AQUAE_AlphaFold_chainA.pdb"),
    },
    {
        "label": "2Q6O_chainA",
        "input_pdb": Path("data/pdb/2Q6O.pdb"),
        "chain": "A",
        "output_pdb": Path("data/structure_chains/2Q6O_chainA.pdb"),
    },
    {
        "label": "1RQP_chainA",
        "input_pdb": Path("data/pdb/1RQP.pdb"),
        "chain": "A",
        "output_pdb": Path("data/structure_chains/1RQP_chainA.pdb"),
    },
]

RESULTS_DIR = Path("results/structure_chains")
DATA_DIR = Path("data/structure_chains")

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

summary_rows = []

for item in STRUCTURES:
    atom_count = 0
    residue_ids = set()
    first_residue = None
    last_residue = None

    with item["input_pdb"].open(errors="ignore") as inp, item["output_pdb"].open("w") as out:
        out.write(f"REMARK Extracted chain {item['chain']} from {item['input_pdb']}\n")
        out.write(f"REMARK Protein ATOM records only; HETATM records excluded for structural alignment\n")

        for line in inp:
            if not line.startswith("ATOM"):
                continue

            chain_id = line[21].strip() or "_"
            if chain_id != item["chain"]:
                continue

            out.write(line)
            atom_count += 1

            resname = line[17:20].strip()
            resseq = line[22:26].strip()
            icode = line[26].strip()
            residue_key = (resname, resseq, icode)
            residue_ids.add(residue_key)

            residue_label = f"{resname}{resseq}{icode}".strip()
            if first_residue is None:
                first_residue = residue_label
            last_residue = residue_label

        out.write("END\n")

    summary_rows.append({
        "label": item["label"],
        "input_pdb": str(item["input_pdb"]),
        "output_pdb": str(item["output_pdb"]),
        "chain": item["chain"],
        "atom_count": atom_count,
        "residue_count": len(residue_ids),
        "first_residue": first_residue or "NA",
        "last_residue": last_residue or "NA",
        "status": "OK" if atom_count > 0 else "NO_ATOMS_FOUND",
    })

summary_path = RESULTS_DIR / "chainA_structure_extraction_summary.tsv"

with summary_path.open("w") as out:
    out.write("label\tinput_pdb\toutput_pdb\tchain\tatom_count\tresidue_count\tfirst_residue\tlast_residue\tstatus\n")
    for row in summary_rows:
        out.write(
            f"{row['label']}\t{row['input_pdb']}\t{row['output_pdb']}\t"
            f"{row['chain']}\t{row['atom_count']}\t{row['residue_count']}\t"
            f"{row['first_residue']}\t{row['last_residue']}\t{row['status']}\n"
        )

print(f"Wrote chain-specific PDB files to {DATA_DIR}")
print(f"Wrote summary to {summary_path}")
