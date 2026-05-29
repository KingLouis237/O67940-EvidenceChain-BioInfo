# Step 7 — Direct verification of flagged 2Q6O residue positions

## Aim

The MAFFT-based functional-residue mapping flagged several 2Q6O positions where the expected amino acid from the original paper did not match the amino acid found in the downloaded 2Q6O chain A structure.

The flagged positions were:

- Tyr70 expected, but Thr70 found
- Arg250 expected, but Leu250 found
- Glu252 expected, but Gln252 found

This check directly inspected the downloaded 2Q6O chain A PDB file to determine whether these mismatches were caused by a parsing error or were actually present in the structure file.

## Direct PDB inspection result

The downloaded 2Q6O chain A coordinate file contains:

| PDB residue number | Residue found |
| 70 | THR |
| 131 | GLY |
| 250 | LEU |
| 252 | GLN |
The local region from residue 240 to 260 is:

| Residue number | Residue |
| 240 | LEU |
| 241 | ASN |
| 242 | SER |
| 243 | ARG |
| 244 | GLY |
| 245 | ARG |
| 246 | LEU |
| 247 | ALA |
| 248 | LEU |
| 249 | GLY |
| 250 | LEU |
| 251 | ASN |
| 252 | GLN |
| 253 | SER |
| 254 | ASN |
| 255 | PHE |
| 256 | ILE |
| 257 | GLU |
| 258 | LYS |
| 259 | TRP |
| 260 | PRO |

## Interpretation

The Tyr70 mismatch is explainable because the original paper notes a Tyr70Thr mutation in 2Q6O. Therefore, seeing THR at residue 70 in the downloaded coordinate file is expected.

The Gly131 position matches correctly and is one of the most important specificity-related positions. The mapping supports:

O67940 Gly127 ↔ 2Q6O Gly131 ↔ 1RQP Ser158

The Arg250 and Glu252 mismatches are not resolved by direct PDB inspection. In the downloaded coordinate file, residues 250 and 252 are LEU and GLN, respectively. This means the mismatch is not caused by a simple parsing error. It may reflect numbering differences, construct differences, or differences between the original paper's residue mapping and direct current PDB coordinate numbering.
## Conclusion
The residue mapping strongly supports the key Val67/Gly127 interpretation, but the full Table 2 mapping should not be described as perfectly reproduced. The report should explicitly mention that some C-terminal positions require caution.
