# Step 4B — Reference structure content interpretation

## Aim

This step inspected the internal contents of the downloaded reference PDB structures 2Q6O and 1RQP before using them for comparison with the AlphaFold model of O67940_AQUAE.

## Chain summary

| PDB ID | Chains detected | Residues per chain |
| 2Q6O | A, B | 269 |
| 1RQP | A, B, C | 291 |

The structures contain multiple protein chains. Since the AlphaFold model of O67940_AQUAE represents one predicted protein chain, downstream comparison should use a representative chain from each reference structure rather than the full multi-chain PDB file. Chain A will be used first unless later inspection gives a reason to choose another chain.

## Heteroatom summary

| PDB ID | Heteroatom records detected |
| 2Q6O | CL, SAM, HOH |
| 1RQP | SAM, HOH |

SAM is present in both reference structures, which is relevant because the original analysis concerns SAM-dependent halogenase-like function. The presence of CL in 2Q6O is also biologically relevant because 2Q6O is the chlorinase-related reference structure.

Water molecules were also detected in both structures. These are expected in experimental crystal structures and should not be treated as functional ligands without additional context.

## Interpretation

This inspection confirms that both reference PDB files contain valid protein coordinate data and relevant ligand/cofactor context. However, the structures contain multiple chains, so downstream comparison must avoid blindly using the entire PDB file. The next step should extract or focus on representative protein chains, most likely chain A from 2Q6O and chain A from 1RQP.

## Working conclusion

The reference structures are valid and suitable for downstream comparison, but they must be handled carefully. Chain selection and ligand context should be documented before structural alignment or residue mapping.
