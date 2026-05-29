# Step 7 — Functional-residue mapping interpretation

## Aim

This step mapped functional residues from the original paper across O67940_AQUAE, 2Q6O, and 1RQP using the MAFFT alignment.

## Main result

The mapping reproduced the two most important O67940_AQUAE positions discussed in the original paper:

| Functional position | O67940_AQUAE | 2Q6O | 1RQP |
| Tyr/Thr specificity-related position | Val67 | Thr70 in downloaded 2Q6O chain A | Thr75 |
| Gly/Ser specificity-related position | Gly127 | Gly131 | Ser158 |

This is important because the original article identifies O67940 Val67 and Gly127 as corresponding to key active-site/specificity-related positions in the reference enzymes.

## Important warnings

Three source-residue checks were flagged:

| Source residue from paper | Expected amino acid | Found in downloaded structure/alignment | Comment |
| 2Q6O Tyr70 | Tyr | Thr70 | Likely explained by the Tyr70Thr mutation noted in the original paper/table |
| 2Q6O Arg250 | Arg | Leu250 | Requires further checking |
| 2Q6O Glu252 | Glu | Gln252 | Requires further checking |

The Tyr70 warning is not necessarily an error because the original paper explicitly notes a Tyr70Thr mutation in 2Q6O. However, the Arg250 and Glu252 mismatches should not be ignored. They may reflect residue-numbering differences, construct differences, or differences between the MAFFT sequence alignment and the original structure-guided alignment.

## Interpretation

The MAFFT-based mapping supports the paper's main residue-level observation: O67940_AQUAE has Val67 at the Tyr/Thr specificity-related position and Gly127 at the Gly/Ser specificity-related position.

This pattern is more consistent with a non-fluorinase-like interpretation than with direct transfer of fluorinase specificity, because the corresponding 1RQP positions are Thr75 and Ser158.

However, the full residue table should not yet be treated as perfectly reproduced because two 2Q6O residues near the C-terminal region did not match the expected amino acids when using current PDB residue numbering.

## Working conclusion
The residue mapping strengthens the evidence that O67940_AQUAE is related to SAM-dependent halogenases and reproduces the key Val67/Gly127 mapping from the original paper. The result supports a cautious interpretation closer to broad halogenase/chlorinase-like function than fluorinase-specific assignment, but it remains computational evidence and should not be interpreted as experimental proof.
