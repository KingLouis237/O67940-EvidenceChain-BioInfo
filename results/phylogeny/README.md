# Phylogeny outputs

This folder contains tree-related files for the O67940_AQUAE publication-upgrade analysis.

## Reviewed-reference phylogeny input

`O67940_reviewed_swissprot_reference_set_phylogeny_input.fasta` is a cleaned-label version of the 14-sequence reviewed-reference MAFFT alignment.

It was created because the original FASTA headers contain spaces, pipes, and metadata fields that can make Newick labels difficult to parse.

The label map is kept in:

- `O67940_reviewed_swissprot_reference_set_label_map.tsv`

This reviewed-reference tree input contains:

- O67940_AQUAE
- 2Q6O chain A
- 1RQP chain A
- 11 curated Swiss-Prot hits

Caution:

This is a small reviewed-reference phylogeny input, not a final broad evolutionary dataset.
