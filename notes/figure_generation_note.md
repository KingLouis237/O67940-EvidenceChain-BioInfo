# Step 8 — Report figure generation

## Aim

This step generates figures for the final report from the reproducible workflow outputs.

## Why figures are needed

Most previous outputs were tables, summaries, and interpretation notes. These are useful for reproducibility, but the final report also needs visual summaries to make the evidence chain easier to understand.

## Figures generated

### Figure 1 — Workflow/evidence-chain overview

File:

- `figures/report/figure1_workflow_evidence_chain.png`
- `figures/report/figure1_workflow_evidence_chain.pdf`

Purpose:

This figure summarizes the logic of the modern re-analysis, from the O67940_AQUAE query protein through UniProt, InterPro/Pfam, AlphaFoldDB, structural comparison, sequence alignment, residue mapping, and final evidence integration.

### Figure 2 — AlphaFold pLDDT by residue

File:

- `figures/report/figure2_alphafold_plddt_by_residue.png`
- `figures/report/figure2_alphafold_plddt_by_residue.pdf`

Purpose:

This figure shows AlphaFold local confidence across the 251 residues of O67940_AQUAE. UniProt-derived SAM_HAT domain boundaries are marked to connect the confidence profile with the domain interpretation.

### Figure 3 — TM-align structural similarity

File:

- `figures/report/figure3_tmalign_structural_similarity.png`
- `figures/report/figure3_tmalign_structural_similarity.pdf`

Purpose:

This figure visualizes the TM-score values from the pairwise structural comparisons. It helps show that O67940_AQUAE is structurally similar to both 2Q6O and 1RQP, with a higher reference-normalized TM-score against 2Q6O.

## Script used

- `scripts/create_report_figures.py`

## Interpretation rule

The figures summarize evidence but do not replace the underlying tables or interpretation notes. In the final report, figures should be used selectively to clarify the workflow, model confidence, and structural-comparison results.
