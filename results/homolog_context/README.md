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
