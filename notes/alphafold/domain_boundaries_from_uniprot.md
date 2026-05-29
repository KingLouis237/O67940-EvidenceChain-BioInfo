# Step 3 — Domain boundaries from UniProt

## Aim

The first PAE analysis used a rough N-terminal/C-terminal split. To make the analysis more biologically meaningful, the UniProt JSON record was inspected for annotated domain features.

## Result

The UniProt `features` field contains two domain annotations for O67940_AQUAE:

| Domain | Coordinates | Description |
|---|---:|---|
| N-terminal SAM_HAT domain | 3–148 | S-adenosyl-l-methionine hydroxide adenosyltransferase N-terminal |
| C-terminal SAM_HAT domain | 171–246 | S-adenosyl-l-methionine hydroxide adenosyltransferase C-terminal |

This means the protein can be interpreted as having two annotated SAM_HAT domains separated by an intermediate region from approximately residues 149–170.

## Cross-reference check

The UniProt InterPro/Pfam cross-references provide entry names such as SAM_HAT_N and SAM_HAT_C, while the UniProt `features` field provides the residue coordinates. Therefore, the domain-coordinate source used for the refined PAE analysis is the UniProt `features` field.

## Why this matters

PAE measures confidence in the relative positions of residues or regions. Using real domain coordinates is better than splitting the protein in half because it asks a biologically meaningful question:

"Is AlphaFold confident about the relative arrangement of the N-terminal and C-terminal SAM_HAT domains?"

## Interpretation rule

Domain boundaries improve the structural confidence analysis, but they do not prove enzyme activity or substrate specificity. They only help us decide whether the AlphaFold model is reliable enough for downstream structural comparison and residue mapping.
