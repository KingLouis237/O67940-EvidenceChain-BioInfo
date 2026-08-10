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

## UniProtKB protein-name query overlap

`O67940_uniprot_name_query_overlap_summary.tsv` measures accession overlap among the fluorinase, chlorinase, and hydrolase protein-name queries within the PF01887/PF20257 candidate space.

Main result:

The fluorinase and chlorinase queries are almost completely overlapping. Of 2033 fluorinase-query entries and 2032 chlorinase-query entries, 2017 occur in both sets.

Only 16 entries were fluorinase-only and 15 were chlorinase-only.

The hydrolase query behaved differently: 112 of 113 entries were hydrolase-only.

Interpretation:

Protein-name searches cannot be treated as independent fluorinase and chlorinase functional classes in this candidate space. These labels will be retained as metadata, but broader homolog selection will be based on sequence similarity, coverage, taxonomy, and redundancy rather than annotation names alone.

## Broader PHMMER analysis

The PF01887/PF20257 UniProtKB candidate set was ranked directly against O67940 using PHMMER.

Detailed outputs are in:

- `broader_phmmer/`

This directory contains the raw PHMMER tables, parsed ranking, coverage and score diagnostics, reviewed-reference checks, rank checkpoints, and the interpretation Markdown.

The analysis showed that neither a strict high-coverage rule nor a simple top-N PHMMER ranking provides a defensible way to define the broader phylogenetic set.

See:

- `O67940_broader_homolog_strategy.md`
- `broader_phmmer/O67940_broader_phmmer_interpretation.md`

## Redundancy analysis

The 4432-sequence broader candidate set was evaluated for sequence redundancy with MMseqs2 before choosing sequences for broader phylogenetic analysis.

Clustering was compared at 95%, 90%, 80%, and 70% sequence identity, with 80% bidirectional sequence coverage.

The resulting cluster counts were:

- 95% identity: 3606 clusters
- 90% identity: 2858 clusters
- 80% identity: 1816 clusters
- 70% identity: 1181 clusters

A 90% identity threshold was retained for the first redundancy-pruning step.

This was not chosen as a universal protein-family cutoff. In this dataset it provided substantial redundancy reduction while keeping O67940 and all 11 reviewed Swiss-Prot anchors in separate clusters. At 80% and 70%, several reviewed reference proteins began to collapse into shared clusters.

O67940 remained a singleton even at 70% identity with 80% bidirectional coverage. This does not contradict the broader homology evidence: the clustering step asks whether sequences are sufficiently similar to be treated as redundant, whereas PHMMER, domain, and structural analyses address broader homologous relationships.

The 10 non-prokaryotic candidates were also followed across the clustering thresholds. Three Entamoeba records clustered together at 90%, while L7FJS4, the four Geodia records, and the two ciliate records remained separate under the tested criteria. This does not establish their biological origin, but shows that they cannot all be dismissed simply as near-identical duplicates.

Main files:

- `O67940_redundancy_clustering_strategy.md`
- `redundancy_mmseqs/O67940_mmseqs_redundancy_summary.tsv`
- `redundancy_mmseqs/O67940_mmseqs_anchor_cluster_membership.tsv`
- `redundancy_mmseqs/O67940_mmseqs_non_prokaryotic_cluster_membership.tsv`
- `redundancy_mmseqs/O67940_exact_duplicate_sequence_groups.tsv`
- `redundancy_mmseqs/O67940_mmseqs_redundancy_interpretation.md`

The MMseqs2 representative of a cluster is not automatically treated as the preferred biological representative. Reviewed anchors and other explicitly important sequences will be retained deliberately during final phylogenetic sampling.
