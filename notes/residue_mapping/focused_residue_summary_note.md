# Step 7B — Focused functional-residue summary

## Aim

The full MAFFT-based residue mapping table is useful for reproducibility, but it is too detailed for the final report. This step creates a focused summary table containing the most biologically important residue mappings and the main cautionary cases.

## Why this matters

The key functional question is not whether every residue in the table can be listed. The key question is whether the residues most relevant to chlorinase-like versus fluorinase-like interpretation map consistently.

The focused table therefore highlights:

1. the Tyr/Thr specificity-related position;
2. the Gly/Ser specificity-related position;
3. the corresponding O67940_AQUAE residues Val67 and Gly127;
4. the C-terminal residue mismatches that require caution.

## Input

- `results/residue_mapping/functional_residue_mapping_mafft.tsv`

## Output

- `results/residue_mapping/focused_functional_residue_summary.tsv`

## Interpretation rule

The focused table should be used for the final report because it captures the strongest residue-level evidence without overwhelming the reader. The full table remains available as an audit trail.

The key conclusion is that the mapping reproduces the original paper's major O67940 positions, Val67 and Gly127. However, the C-terminal discrepancies in the 2Q6O residue numbering/identity mean the full Table 2 mapping should not be described as perfectly reproduced.
