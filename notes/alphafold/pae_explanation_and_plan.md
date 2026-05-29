#  Why Predicted Aligned Error (PAE) matters
## What PAE means

AlphaFold provides more than a predicted 3D structure. It also provides confidence information.

The pLDDT score tells us how confident AlphaFold is about the local structure around each residue. This is useful for asking whether a local region is well predicted.

Predicted Aligned Error, or PAE, answers a different question: how confident is AlphaFold about the relative position of one residue or region compared with another residue or region?

A simple way to understand the difference is:

- pLDDT: "Is this local part of the protein reliable?"
- PAE: "Are these two parts of the protein positioned reliably relative to each other?"

## Why this matters for O67940_AQUAE

The InterPro/Pfam results suggest that O67940_AQUAE contains N-terminal and C-terminal SAM_HAT domains. For a protein with more than one domain, it is possible for each domain to be locally well predicted while the relative orientation between domains remains uncertain.

Therefore, after summarizing pLDDT, the next step is to summarize PAE. This helps us avoid overinterpreting the AlphaFold model.

## What the PAE script does

The script `scripts/summarize_alphafold_pae.py` reads the AlphaFoldDB PAE JSON file:

`data/alphafold/AF-O67940-F1-predicted_aligned_error_v6.json`

It calculates:

- the size of the PAE matrix;
- mean, median, minimum, and maximum PAE;
- how many residue pairs have low, moderate, high, or very high PAE;
- approximate PAE within the N-terminal half, within the C-terminal half, and between the two halves.

The N-terminal/C-terminal split is only a first approximation. Later, if exact InterPro/Pfam domain coordinates are available, the analysis can be refined using those boundaries.

## Interpretation rule

Low PAE supports confidence in the relative positions of regions/domains. High PAE means the relative arrangement should be interpreted cautiously.

PAE does not prove enzymatic function. It only helps decide whether the predicted structure is reliable enough for structural interpretation.
