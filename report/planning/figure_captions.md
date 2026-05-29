# Figure captions for final report

## Figure 1 — Evidence-chain workflow

Modern re-analysis workflow used for O67940_AQUAE. The analysis begins with the current UniProtKB record, then adds InterPro/Pfam family-domain evidence, AlphaFoldDB structural confidence, reference PDB structures, TM-align structural comparison, MAFFT sequence alignment, and focused functional-residue mapping. The purpose of the workflow is not to assign function from one database hit, but to integrate multiple evidence layers before reaching a cautious interpretation.

## Figure 2 — AlphaFold local confidence

AlphaFoldDB v6 pLDDT profile for O67940_AQUAE. The model shows high local confidence across the protein sequence, supporting its use for downstream structural comparison. UniProt-derived SAM_HAT domain boundaries are marked to connect confidence values with the N-terminal and C-terminal domain architecture. pLDDT supports predicted structural reliability but does not prove biochemical function.

## Figure 3 — TM-align structural comparison

Reference-normalized TM-scores from pairwise structural comparisons between O67940_AQUAE AlphaFold chain A, 2Q6O chain A, and 1RQP chain A. O67940_AQUAE aligns strongly with both reference structures, with a higher reference-normalized TM-score against 2Q6O than against 1RQP. This supports broad fold-level relatedness but does not by itself establish substrate specificity.

## Figure 4 — Focused residue mapping

Focused residue mapping at two specificity-related aligned positions. O67940_AQUAE Val67 maps to the Tyr/Thr-related position, while O67940_AQUAE Gly127 maps with 2Q6O Gly131 rather than 1RQP Ser158. This residue-level evidence is more directly relevant to functional interpretation than global sequence identity alone, but remains computational and should not be treated as experimental proof.
