# Step 3 — AlphaFoldDB confidence interpretation for O67940_AQUAE

## Aim

This step evaluated the AlphaFoldDB v6 predicted structure for O67940_AQUAE. The goal was not to assign function directly, but to decide whether the predicted structure is reliable enough to use as a modern structural evidence layer.

## Why this step matters

The current UniProtKB record contains an AlphaFoldDB cross-reference for O67940_AQUAE but no PDB cross-reference. This means that no experimentally solved structure is directly linked to the protein in UniProt, but a predicted structure is available.

In the original 2008 article, structural reasoning had to rely on related solved structures such as 1RQP and 2Q6O. In this modern re-analysis, AlphaFoldDB gives us a predicted model for the query protein itself. However, because the model is predicted rather than experimentally solved, its confidence must be checked before using it for interpretation.

## Files used

- `data/alphafold/AF-O67940-F1-model_v6.pdb`
- `data/alphafold/AF-O67940-F1-model_v6.cif`
- `data/alphafold/AF-O67940-F1-model_v6.bcif`
- `data/alphafold/AF-O67940-F1-predicted_aligned_error_v6.json`

## Scripts used

- `scripts/summarize_alphafold_plddt.py`
- `scripts/summarize_alphafold_pae.py`

## pLDDT interpretation

pLDDT measures local confidence. It asks whether AlphaFold is confident about the local structure around each residue.

The pLDDT summary showed:

| Metric | Result |
|---|---:|
| Number of residues | 251 |
| Mean pLDDT | 96.70 |
| Median pLDDT | 97.69 |
| Minimum pLDDT | 77.56 |
| Maximum pLDDT | 98.88 |
| Residues with pLDDT >= 90 | 242 |
| Residues with pLDDT 70-90 | 9 |
| Residues with pLDDT < 70 | 0 |

Interpretation:
The model is locally high confidence across essentially the whole protein. This supports using the model for structural inspection and comparison.

## PAE interpretation

PAE measures confidence in relative positioning. It asks whether AlphaFold is confident about the position of one residue or region relative to another.

The PAE summary showed:

| Metric | Result |
|---|---:|
| PAE matrix size | 251 × 251 |
| Mean PAE | 3.32 Å |
| Median PAE | 3.00 Å |
| Maximum PAE | 22.00 Å |
| Low PAE pairs (<5 Å) | 50,308 |
| Moderate PAE pairs (5-10 Å) | 11,336 |
| High PAE pairs (10-20 Å) | 1,341 |
| Very high PAE pairs (>=20 Å) | 16 |

Approximate region-level PAE:

| Region comparison | Mean PAE |
|---|---:|
| N-terminal half internal | 2.52 Å |
| C-terminal half internal | 3.02 Å |
| Between halves | 3.85 Å |

Interpretation:
The low overall PAE and low between-halves mean PAE suggest that AlphaFold is reasonably confident not only in local residue structure, but also in the relative arrangement of the main regions of the protein. This matters because the protein is predicted to contain N-terminal and C-terminal SAM_HAT domains.

## Working conclusion

The AlphaFoldDB v6 model of O67940_AQUAE is sufficiently confident to use as a modern structural evidence layer. Both pLDDT and PAE support this: pLDDT indicates high local confidence, and PAE suggests low uncertainty in residue/region positioning.

However, this does not prove enzyme activity, halogenase function, or substrate specificity. The structure can support the next step — structural comparison and functional-residue mapping — but it cannot replace biochemical validation.
