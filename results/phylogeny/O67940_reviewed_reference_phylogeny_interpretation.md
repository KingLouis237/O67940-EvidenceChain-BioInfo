# Reviewed-reference phylogeny interpretation

## Purpose

This note interprets the first reviewed-reference phylogeny for O67940_AQUAE.

It is based on:

- `results/phylogeny/O67940_reviewed_swissprot_reference_set_phylogeny_input.fasta`
- `results/phylogeny/O67940_reviewed_swissprot_reference_set_fasttree.nwk`
- `results/phylogeny/O67940_reviewed_swissprot_reference_set_label_map.tsv`

This tree uses the 14-sequence reviewed/reference alignment:

- O67940_AQUAE
- 2Q6O chain A
- 1RQP chain A
- 11 curated Swiss-Prot JackHMMER hits

## Main observations

In this small reviewed-reference tree, O67940_AQUAE groups closest to RSAMH_METJA.

This is consistent with the reviewed-reference pairwise identity summary, where RSAMH_METJA had the highest identity to O67940 among the 13 comparison sequences.

The tree also shows a tight 2Q6O/SALL_SALTO pairing.

This is expected and useful, because SalL is the adenosyl-chloride synthase/chlorinase-related Swiss-Prot reference in this set, while 2Q6O is the chlorinase-related structural reference used in the earlier comparison.

The 1RQP/FLA_STRCT pairing is also tight in the tree. This is consistent with 1RQP being the fluorinase structural reference and FLA_STRCT being a reviewed fluorinase sequence.

## Interpretation

The reviewed-reference tree supports the same cautious direction as the sequence-identity and residue-pattern analyses.

O67940 does not sit directly with the 1RQP/fluorinase reference pair in this small tree.

Instead, it falls closer to the SAM hydrolase-like part of the reviewed Swiss-Prot set, especially RSAMH_METJA.

This supports a broad SAM-related placement for O67940_AQUAE.

## Important caution

This tree should not be treated as a final evolutionary reconstruction.

Reasons:

- it contains only 14 sequences
- it is based on a curated reviewed-reference set, not a broad homolog sample
- FastTree support values are local SH-like supports, not full bootstrap analysis
- the deeper relationships among the groups should not be overinterpreted
- the tree alone cannot prove enzyme activity or substrate specificity

The tree is useful because it checks whether the reviewed-reference homolog set tells the same story as the pairwise identity and residue mapping layers.

## Current conclusion

The reviewed-reference phylogeny supports SAM-related placement of O67940_AQUAE and does not support direct fluorinase-specific annotation.

Together with the residue-pattern result at O67940 G127, this strengthens the cautious interpretation that O67940 is related to the SAM-dependent halogenase/SAM-hydrolase space, but should not be assigned a precise chlorinase or fluorinase function without broader evolutionary context and biochemical validation.

## Next decision

The next major decision is whether this reviewed-reference tree is enough for the manuscript upgrade, or whether we need a broader homolog search and a larger curated phylogeny.

My current view is that a broader homolog search is still useful, because Swiss-Prot is curated but incomplete.
