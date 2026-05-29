from pathlib import Path
from collections import defaultdict

PDB_FILES = {
    "2Q6O": Path("data/pdb/2Q6O.pdb"),
    "1RQP": Path("data/pdb/1RQP.pdb"),
}

RESULTS_DIR = Path("results/pdb")
NOTES_DIR = Path("notes/pdb")

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
NOTES_DIR.mkdir(parents=True, exist_ok=True)

summary_rows = []
ligand_rows = []

for pdb_id, pdb_path in PDB_FILES.items():
    atom_counts_by_chain = defaultdict(int)
    residue_ids_by_chain = defaultdict(set)
    hetatm_counts_by_resname = defaultdict(int)
    hetatm_chains_by_resname = defaultdict(set)

    with pdb_path.open(errors="ignore") as handle:
        for line in handle:
            record = line[0:6].strip()

            if record == "ATOM":
                chain_id = line[21].strip() or "_"
                resname = line[17:20].strip()
                resseq = line[22:26].strip()
                icode = line[26].strip()

                atom_counts_by_chain[chain_id] += 1
                residue_ids_by_chain[chain_id].add((resname, resseq, icode))

            elif record == "HETATM":
                chain_id = line[21].strip() or "_"
                resname = line[17:20].strip()

                # HOH is water. We keep it in the table, but later interpretation
                # should separate water from biologically meaningful ligands/cofactors.
                hetatm_counts_by_resname[resname] += 1
                hetatm_chains_by_resname[resname].add(chain_id)

    for chain_id in sorted(atom_counts_by_chain):
        summary_rows.append({
            "pdb_id": pdb_id,
            "chain": chain_id,
            "atom_count": atom_counts_by_chain[chain_id],
            "residue_count": len(residue_ids_by_chain[chain_id]),
        })

    for resname in sorted(hetatm_counts_by_resname):
        ligand_rows.append({
            "pdb_id": pdb_id,
            "hetatm_resname": resname,
            "hetatm_atom_count": hetatm_counts_by_resname[resname],
            "chains": ",".join(sorted(hetatm_chains_by_resname[resname])),
        })

chain_summary_path = RESULTS_DIR / "reference_pdb_chain_summary.tsv"
ligand_summary_path = RESULTS_DIR / "reference_pdb_heteroatom_summary.tsv"

with chain_summary_path.open("w") as out:
    out.write("pdb_id\tchain\tatom_count\tresidue_count\n")
    for row in summary_rows:
        out.write(
            f"{row['pdb_id']}\t{row['chain']}\t"
            f"{row['atom_count']}\t{row['residue_count']}\n"
        )

with ligand_summary_path.open("w") as out:
    out.write("pdb_id\thetatm_resname\thetatm_atom_count\tchains\n")
    for row in ligand_rows:
        out.write(
            f"{row['pdb_id']}\t{row['hetatm_resname']}\t"
            f"{row['hetatm_atom_count']}\t{row['chains']}\n"
        )

print(f"Wrote chain summary to: {chain_summary_path}")
print(f"Wrote heteroatom summary to: {ligand_summary_path}")
