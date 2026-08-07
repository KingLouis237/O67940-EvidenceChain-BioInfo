# Homolog context

This folder contains the first homolog-search layer for the O67940_AQUAE re-analysis.

## Swiss-Prot JackHMMER first pass

The first controlled homolog search used O67940_AQUAE as query against a local UniProtKB/Swiss-Prot database.

Swiss-Prot was used first because it is curated and easier to interpret than a very broad unreviewed database.

Main outputs:

- `O67940_vs_swissprot_jackhmmer_N5.tblout`
- `O67940_vs_swissprot_jackhmmer_N5.domtblout`
- `O67940_vs_swissprot_jackhmmer_N5.parsed_hits.tsv`
- `O67940_vs_swissprot_jackhmmer_N5.domain_summary.tsv`
- `O67940_vs_swissprot_jackhmmer_N5.initial_curation.tsv`

## Interpretation

The reviewed Swiss-Prot hits place O67940_AQUAE in a SAM-dependent hydrolase / halogenase-related neighborhood.

The hit set includes SAM hydrolase-like proteins, fluorinases, and SalL/adensosyl-chloride synthase.

This supports family-level context, not exact substrate specificity.

## Caution

This is not the full homolog universe.

The Swiss-Prot result should be treated as a curated first-pass reference set, not as the final evolutionary analysis.

## Reviewed-reference FASTA

`O67940_reviewed_swissprot_reference_set.fasta` contains the small reviewed/reference set prepared for alignment.

It includes:

- O67940_AQUAE AlphaFold-derived chain sequence
- 2Q6O chain A
- 1RQP chain A
- the 11 curated Swiss-Prot JackHMMER hits

This file is meant for a controlled MAFFT alignment, not for final broad evolutionary sampling.

## Broader UniProtKB Pfam candidate-space survey

`O67940_uniprot_pfam_broader_candidate_space_survey.tsv` records API result counts for proteins carrying both PF01887 and PF20257, with additional length, review-status, taxonomy, and protein-name filters.

Main findings:

- 4432 entries matched the initial domain and length query
- only 11 were reviewed
- 4421 were unreviewed
- tighter length limits reduced the set only slightly
- most candidates were bacterial, with a smaller archaeal component

The fluorinase and chlorinase protein-name counts were nearly identical. These labels must therefore be checked for overlap and must not be treated as independent functional classes.

This survey defines a candidate space. It is not itself a final homolog set.
