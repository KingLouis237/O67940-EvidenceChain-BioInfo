# Step 7B — Focused residue-mapping interpretation

## Aim

This step condenses the full functional-residue mapping into a focused table suitable for interpretation and eventual inclusion in the final report.

## Main result

The focused table highlights two key specificity-related positions:

| Position type | O67940_AQUAE | 2Q6O | 1RQP |
| Tyr/Thr specificity-related position | Val67 | Thr70 | Thr75 |
| Gly/Ser specificity-related position | Gly127 | Gly131 | Ser158 |

The mapping shows that O67940_AQUAE has Val67 at the Tyr/Thr-related position and Gly127 at the Gly/Ser-related position.

## Interpretation

The Gly127 result is especially important because it aligns O67940_AQUAE with 2Q6O Gly131 rather than 1RQP Ser158. This supports the original paper's cautious interpretation that O67940_AQUAE should not be directly assigned fluorinase specificity from global similarity alone.

The Val67 position is also informative. In the downloaded 2Q6O coordinate file, residue 70 is Thr rather than Tyr, which is consistent with the Tyr70Thr mutation context noted in the original paper. O67940_AQUAE has Val67 at the corresponding alignment column, not Thr.

## Caution

Two C-terminal positions from the original paper remain discrepant when using direct current PDB residue numbering:

| Paper residue | Found in downloaded 2Q6O chain A |
| Arg250 | Leu250 |
| Glu252 | Gln252 |

These mismatches should not be ignored. They may reflect numbering differences, construct differences, or differences between the original structure-guided alignment and the current MAFFT-based alignment.

## Working conclusion

The focused residue mapping supports the key Val67/Gly127 observations and strengthens the interpretation that O67940_AQUAE is broadly related to SAM-dependent halogenase-like enzymes while not supporting a direct fluorinase-specific assignment. However, because some C-terminal positions do not match directly, the full original residue table should be described as partially reproduced rather than perfectly reproduced.
