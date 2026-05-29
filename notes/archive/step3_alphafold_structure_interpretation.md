# Step 3 — AlphaFoldDB predicted structure interpretation

## Aim

This step retrieved and evaluated the AlphaFoldDB predicted structure for O67940_AQUAE. The purpose was to add a modern structural evidence layer because the current UniProtKB record links O67940_AQUAE to AlphaFoldDB but not to any experimentally solved PDB structure.

## What was done

The AlphaFoldDB API was queried first instead of assuming file names manually. The API returned `latestVersion: 6`, so the v6 PDB, mmCIF, binary CIF, and predicted aligned error files were downloaded.

The PDB file was then validated by checking the header and confirming the presence of ATOM coordinate lines. The model contains 2007 ATOM lines and covers 251 residues, matching the UniProt sequence length.

## pLDDT result

The pLDDT confidence values were extracted from the B-factor column of the AlphaFold PDB file.

Summary:

| Metric | Result |
|---|---:|
| Number of residues | 251 |
| Mean pLDDT | 96.70 |
| Median pLDDT | 97.69 |
| Minimum pLDDT | 77.56 |
| Maximum pLDDT | 98.88 |
| Very high confidence residues (>=90) | 242 |
| Confident residues (70-90) | 9 |
| Low-confidence residues (50-70) | 0 |
| Very low-confidence residues (<50) | 0 |

## Interpretation

The AlphaFoldDB model is locally high confidence across essentially the whole protein. Most residues are in the very high-confidence pLDDT range, and no residues fall below 70. This means the predicted local fold is likely reliable enough to use as a structural evidence layer in the modern re-analysis.

However, this does not prove enzyme activity or substrate specificity. pLDDT measures local structural confidence, not biochemical function. Therefore, this model can support structural comparison with known chlorinase/fluorinase structures, but it cannot by itself establish whether O67940_AQUAE is a chlorinase, fluorinase, or broader halogenase.

## Working conclusion

The modern AlphaFoldDB evidence strengthens the structural side of the re-analysis because a high-confidence predicted structure is now available for the query protein itself. This improves on the original 2008 situation, where structural inference relied on related solved structures rather than a direct model of O67940_AQUAE. The next step should be structural comparison and residue-level analysis, not direct functional assignment.
