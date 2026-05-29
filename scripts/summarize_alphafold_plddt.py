from pathlib import Path
import statistics

# AlphaFoldDB v6 PDB model downloaded from the API-reported URL
pdb_path = Path("data/alphafold/AF-O67940-F1-model_v6.pdb")

# Output summary file
out_path = Path("results/alphafold/O67940_alphafold_plddt_summary.txt")
out_path.parent.mkdir(parents=True, exist_ok=True)

plddt_by_residue = {}

with pdb_path.open() as handle:
    for line in handle:
        if not line.startswith("ATOM"):
            continue

        # PDB format uses fixed columns.
        # Residue number is in columns 23-26, Python slice [22:26].
        # AlphaFold stores pLDDT in the B-factor column, columns 61-66, Python slice [60:66].
        residue_number = int(line[22:26].strip())
        plddt = float(line[60:66].strip())

        # Multiple atoms belong to the same residue.
        # AlphaFold assigns the same pLDDT to all atoms in that residue,
        # so we only need one pLDDT value per residue.
        plddt_by_residue[residue_number] = plddt

scores = list(plddt_by_residue.values())

def count_range(low, high=None):
    if high is None:
        return sum(score >= low for score in scores)
    return sum(low <= score < high for score in scores)

with out_path.open("w") as out:
    out.write("AlphaFold pLDDT summary for O67940_AQUAE\n")
    out.write("=" * 50 + "\n\n")
    out.write(f"Input PDB: {pdb_path}\n")
    out.write(f"Number of residues with pLDDT values: {len(scores)}\n")
    out.write(f"Mean pLDDT: {statistics.mean(scores):.2f}\n")
    out.write(f"Median pLDDT: {statistics.median(scores):.2f}\n")
    out.write(f"Minimum pLDDT: {min(scores):.2f}\n")
    out.write(f"Maximum pLDDT: {max(scores):.2f}\n\n")

    out.write("pLDDT confidence ranges\n")
    out.write("-" * 30 + "\n")
    out.write(f"Very high confidence (>=90): {count_range(90)} residues\n")
    out.write(f"Confident (70-90): {count_range(70, 90)} residues\n")
    out.write(f"Low confidence (50-70): {count_range(50, 70)} residues\n")
    out.write(f"Very low confidence (<50): {sum(score < 50 for score in scores)} residues\n\n")

    out.write("Interpretation guide\n")
    out.write("-" * 30 + "\n")
    out.write("pLDDT >= 90: very high local confidence\n")
    out.write("70 <= pLDDT < 90: generally confident local structure\n")
    out.write("50 <= pLDDT < 70: low confidence; interpret cautiously\n")
    out.write("pLDDT < 50: very low confidence; may be flexible/disordered or unreliable\n")

print(f"Wrote summary to {out_path}")
