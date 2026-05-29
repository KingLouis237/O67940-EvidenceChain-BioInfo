# Step 9 — Evidence integration table

## Aim

This step integrates the main evidence layers from the modern re-analysis into one structured table.

## Why this matters

The project combines multiple forms of evidence: database annotation, family/domain classification, predicted structure confidence, structural comparison, sequence alignment, and functional-residue mapping.

No single layer is sufficient to prove exact function. The evidence integration table makes the interpretation more disciplined by separating:

1. what was observed;
2. what the observation supports;
3. what it does not prove;
4. what limitation remains.

## Outputs

- `results/evidence_integration/evidence_integration_table.tsv`
- `results/evidence_integration/evidence_integration_table_short.tsv`

## Interpretation

The integrated evidence supports that O67940_AQUAE remains uncharacterized at the curated UniProt function level but is consistently associated with a SAM-related family/domain context. The AlphaFold model is confident enough for structural comparison, and TM-align shows strong global fold similarity to both 2Q6O and 1RQP, with a modest structural preference toward 2Q6O. MAFFT sequence identity is nearly equal between the two references, so global sequence similarity alone does not resolve specificity.

The most biologically informative evidence comes from focused residue mapping. O67940_AQUAE Val67 and Gly127 reproduce the key residue-level observations emphasized by the original paper. In particular, Gly127 aligns with 2Q6O Gly131 rather than 1RQP Ser158. This supports the original paper's cautious chlorinase-like/halogenase interpretation rather than direct fluorinase-specific assignment.

## Caution

The analysis is computational and should not be presented as experimental proof of enzyme activity. Also, two C-terminal residues listed for 2Q6O in the original paper did not match direct current PDB coordinate numbering, so the full Table 2 mapping should be described as partially reproduced rather than perfectly reproduced.
