from pathlib import Path
import csv

input_path = Path("results/residue_mapping/functional_residue_mapping_mafft.tsv")
output_path = Path("results/residue_mapping/focused_functional_residue_summary.tsv")
output_path.parent.mkdir(parents=True, exist_ok=True)

# Rows we want to highlight in the report.
# These are the most biologically interpretable positions from the mapping.
FOCUS_ROWS = [
    {
        "focus": "Tyr/Thr specificity-related position",
        "source_structure": "2Q6O_chainA",
        "source_paper_residue": "Tyr70",
        "why_keep": "Key position discussed in the original paper; downloaded 2Q6O structure contains Thr70, consistent with Tyr70Thr mutation context.",
    },
    {
        "focus": "Gly/Ser specificity-related position",
        "source_structure": "2Q6O_chainA",
        "source_paper_residue": "Gly131",
        "why_keep": "Key specificity-related position; mapping reproduces O67940 Gly127 aligned with 2Q6O Gly131 and 1RQP Ser158.",
    },
    {
        "focus": "Fluorinase comparison residue",
        "source_structure": "1RQP_chainA",
        "source_paper_residue": "Thr75",
        "why_keep": "Fluorinase reference position corresponding to O67940 Val67.",
    },
    {
        "focus": "Fluorinase comparison residue",
        "source_structure": "1RQP_chainA",
        "source_paper_residue": "Ser158",
        "why_keep": "Fluorinase reference position corresponding to O67940 Gly127.",
    },
    {
        "focus": "C-terminal mapping caution",
        "source_structure": "2Q6O_chainA",
        "source_paper_residue": "Arg250",
        "why_keep": "Flagged mismatch: current 2Q6O coordinate file has Leu250, not Arg250.",
    },
    {
        "focus": "C-terminal mapping caution",
        "source_structure": "2Q6O_chainA",
        "source_paper_residue": "Glu252",
        "why_keep": "Flagged mismatch: current 2Q6O coordinate file has Gln252, not Glu252.",
    },
]

with input_path.open() as f:
    reader = csv.DictReader(f, delimiter="\t")
    rows = list(reader)

focused = []

for focus in FOCUS_ROWS:
    match = None

    for row in rows:
        if (
            row["source_structure"] == focus["source_structure"]
            and row["source_paper_residue"] == focus["source_paper_residue"]
        ):
            match = row
            break

    if match is None:
        focused.append({
            "focus": focus["focus"],
            "source_structure": focus["source_structure"],
            "source_paper_residue": focus["source_paper_residue"],
            "alignment_column": "NA",
            "O67940_residue": "NA",
            "2Q6O_residue": "NA",
            "1RQP_residue": "NA",
            "source_residue_check": "not_found",
            "interpretation": focus["why_keep"],
        })
    else:
        focused.append({
            "focus": focus["focus"],
            "source_structure": match["source_structure"],
            "source_paper_residue": match["source_paper_residue"],
            "alignment_column": match["alignment_column"],
            "O67940_residue": match["O67940_residue"],
            "2Q6O_residue": match["2Q6O_residue"],
            "1RQP_residue": match["1RQP_residue"],
            "source_residue_check": match["source_residue_check"],
            "interpretation": focus["why_keep"],
        })

with output_path.open("w") as out:
    fieldnames = [
        "focus",
        "source_structure",
        "source_paper_residue",
        "alignment_column",
        "O67940_residue",
        "2Q6O_residue",
        "1RQP_residue",
        "source_residue_check",
        "interpretation",
    ]

    writer = csv.DictWriter(out, delimiter="\t", fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(focused)

print(f"Wrote focused residue mapping summary to {output_path}")
