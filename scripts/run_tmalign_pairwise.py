from pathlib import Path
import subprocess
import re

# Chain-specific protein-only PDB files prepared earlier
STRUCTURES = {
    "O67940_AQUAE_AlphaFold_chainA": Path("data/structure_chains/O67940_AQUAE_AlphaFold_chainA.pdb"),
    "2Q6O_chainA": Path("data/structure_chains/2Q6O_chainA.pdb"),
    "1RQP_chainA": Path("data/structure_chains/1RQP_chainA.pdb"),
}

# Pairwise comparisons to run
COMPARISONS = [
    ("O67940_AQUAE_AlphaFold_chainA", "2Q6O_chainA"),
    ("O67940_AQUAE_AlphaFold_chainA", "1RQP_chainA"),
    ("2Q6O_chainA", "1RQP_chainA"),
]

RAW_DIR = Path("results/structure_comparison/tmalign_raw")
SUMMARY_PATH = Path("results/structure_comparison/tmalign_pairwise_summary.tsv")

RAW_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)


def run_tmalign(label_a, label_b):
    """Run TM-align for one pair and save raw output."""
    pdb_a = STRUCTURES[label_a]
    pdb_b = STRUCTURES[label_b]

    output_file = RAW_DIR / f"{label_a}_VS_{label_b}.txt"

    command = ["TMalign", str(pdb_a), str(pdb_b)]

    print("Running:", " ".join(command))

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    output_file.write_text(result.stdout)

    return output_file, result.stdout


def parse_tmalign_output(text):
    """
    Parse key values from TM-align output.

    TM-align usually reports:
    - Length of Chain_1
    - Length of Chain_2
    - Aligned length, RMSD, sequence identity
    - TM-score normalized by chain 1 length
    - TM-score normalized by chain 2 length
    """
    parsed = {
        "chain1_length": "NA",
        "chain2_length": "NA",
        "aligned_length": "NA",
        "rmsd": "NA",
        "seq_identity_aligned": "NA",
        "tm_score_norm_chain1": "NA",
        "tm_score_norm_chain2": "NA",
    }

    chain1_match = re.search(r"Length of Chain_1:\s+(\d+)", text)
    chain2_match = re.search(r"Length of Chain_2:\s+(\d+)", text)

    if chain1_match:
        parsed["chain1_length"] = chain1_match.group(1)
    if chain2_match:
        parsed["chain2_length"] = chain2_match.group(1)

    align_match = re.search(
        r"Aligned length=\s*(\d+),\s*RMSD=\s*([0-9.]+),\s*Seq_ID=n_identical/n_aligned=\s*([0-9.]+)",
        text,
    )

    if align_match:
        parsed["aligned_length"] = align_match.group(1)
        parsed["rmsd"] = align_match.group(2)
        parsed["seq_identity_aligned"] = align_match.group(3)

    tm_scores = re.findall(r"TM-score=\s*([0-9.]+)", text)

    if len(tm_scores) >= 1:
        parsed["tm_score_norm_chain1"] = tm_scores[0]
    if len(tm_scores) >= 2:
        parsed["tm_score_norm_chain2"] = tm_scores[1]

    return parsed


rows = []

for label_a, label_b in COMPARISONS:
    raw_output_path, stdout = run_tmalign(label_a, label_b)
    parsed = parse_tmalign_output(stdout)

    rows.append({
        "structure_1": label_a,
        "structure_2": label_b,
        "raw_output": str(raw_output_path),
        **parsed,
    })


with SUMMARY_PATH.open("w") as out:
    out.write(
        "structure_1\tstructure_2\tchain1_length\tchain2_length\t"
        "aligned_length\trmsd\tseq_identity_aligned\t"
        "tm_score_norm_chain1\ttm_score_norm_chain2\traw_output\n"
    )

    for row in rows:
        out.write(
            f"{row['structure_1']}\t{row['structure_2']}\t"
            f"{row['chain1_length']}\t{row['chain2_length']}\t"
            f"{row['aligned_length']}\t{row['rmsd']}\t"
            f"{row['seq_identity_aligned']}\t"
            f"{row['tm_score_norm_chain1']}\t{row['tm_score_norm_chain2']}\t"
            f"{row['raw_output']}\n"
        )

print(f"Raw TM-align outputs written to: {RAW_DIR}")
print(f"Summary written to: {SUMMARY_PATH}")
