# Evolutionary and active-site context module

This module contains the publication-upgrade analyses for O67940_AQUAE.

The point is not to make a louder claim. The point is to test whether the earlier interpretation still holds when broader homolog context, residue conservation, and active-site/interface evidence are added.

## Main input

Validated query FASTA:

`data/O67940_AQUAE.fasta`

This file contains one O67940_AQUAE sequence of 251 amino acids and is already tracked in provenance and checksums.

## Current tool state

Available:

- HMMER / JackHMMER
- MAFFT

Already checked:

- `jackhmmer` is available inside the `methods_bioinfo` Conda environment.
- HMMER version: 3.4
- MAFFT version: 7.525

## Planned order

1. choose and document the homolog-search database;
2. run JackHMMER using `data/O67940_AQUAE.fasta`;
3. inspect and parse hits;
4. curate the homolog set;
5. build a multiple sequence alignment;
6. infer phylogenetic placement;
7. map key residues across the alignment;
8. compare O67940, 2Q6O, and 1RQP residue patterns;
9. add active-site and interface context.

## Output folders

Homolog search:

`results/homolog_context/`

Phylogeny and alignment:

`results/phylogeny/`

Residue conservation:

`results/residue_conservation/`

Active-site structure:

`results/active_site_structure/`

Interface context:

`results/interface_context/`

Figures:

`figures/publication/`

Logs:

`logs/05_evolutionary_active_site_context/`

## Interpretation rule

This module can strengthen or weaken the computational annotation-transfer argument.

It cannot prove enzyme activity.

It cannot prove substrate specificity.

It cannot replace biochemical validation.
