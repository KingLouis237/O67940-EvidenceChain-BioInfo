# O67940 broader-candidate redundancy analysis

## Purpose

The 4432-sequence PF01887/PF20257 candidate universe contains substantial taxonomic and sequence redundancy.

MMseqs2 clustering was therefore evaluated at 95%, 90%, 80%, and 70% sequence identity, using 80% bidirectional coverage.

The purpose was to identify a defensible redundancy threshold for later phylogenetic sampling, not to classify protein function.

## Exact sequence duplication

The input FASTA contains:

- 4432 records
- 4365 unique amino-acid sequences
- 62 exact-duplicate sequence groups
- 67 excess records attributable to exact duplication

Exact duplicates therefore represent only a small fraction of the overall redundancy.

## Clustering sensitivity

The number of clusters decreased as the identity threshold was relaxed:

- 95% identity: 3606 clusters
- 90% identity: 2858 clusters
- 80% identity: 1816 clusters
- 70% identity: 1181 clusters

The corresponding reductions relative to the original 4432 records are approximately:

- 95%: 18.6%
- 90%: 35.5%
- 80%: 59.0%
- 70%: 73.4%

Most clusters remained singletons at every threshold, showing that the candidate universe contains substantial sequence diversity rather than being dominated entirely by near-identical records.

## Reviewed-reference behaviour

The reviewed Swiss-Prot proteins were used as biological controls for how aggressively clustering collapsed known family diversity.

At 90% identity, O67940 and all 11 reviewed anchors remained in distinct clusters.

At 80%, several reviewed proteins began sharing clusters. Examples include:

- A4X4S2 and A8M783
- A0A1G9FQX8, R4LHX8, and W8JNL4
- Q70GK9 and W0W999

At 70%, several reviewed fluorinase-related references were collapsed into the same larger cluster.

This indicates that 80% and especially 70% identity begin to compress sequence diversity that is useful for functional and phylogenetic interpretation.

## O67940

O67940 remained a singleton at every tested identity threshold, including 70%.

This does not indicate absence of homologs.

The clustering required both the sequence-identity threshold and at least 80% bidirectional coverage. O67940 therefore lacks another candidate sufficiently similar to be considered redundant under these criteria, despite the broader family homology demonstrated by PHMMER, domain analysis, and structural evidence.

## Non-prokaryotic candidates

Three closely related Entamoeba proteins clustered together at 90% identity:

- A0ABQ0DRK1
- B0E8J3
- C4M0V6

L7FJS4 remained separate.

The four Geodia barretti proteins remained separate clusters at all tested thresholds, as did the Blepharisma stoltei and Stentor coeruleus candidates.

These observations show that the non-prokaryotic records are not simply one set of near-identical duplicate sequences.

Their biological origin remains unresolved.

## Redundancy decision

A threshold of 90% sequence identity with 80% bidirectional coverage will be used for the first redundancy-pruning stage.

This threshold was selected from the sensitivity analysis because it:

- removes substantial near-neighbour redundancy
- reduces 4432 records to 2858 sequence clusters
- keeps O67940 distinct
- keeps all reviewed functional anchors in separate clusters
- avoids the stronger collapse of reviewed-reference diversity observed at 80% and 70%

This threshold defines redundancy for sampling purposes only. It does not define orthology, functional class, or substrate specificity.

## Representative-sequence caution

The MMseqs2-selected representative will not automatically be used as the biological representative of every cluster.

Several reviewed proteins belong to clusters represented by unreviewed accessions even at 90% identity.

When constructing the phylogenetic sampling pool, reviewed anchors and O67940 will therefore be retained explicitly.

For other clusters, representative selection can additionally consider direct PHMMER similarity and taxonomic sampling rather than relying blindly on the MMseqs2 representative.

## Technical note

The MMseqs2 runtime log reported an intermediate sequence-database size of 4288 during clustering.

Independent FASTA analysis found 4365 unique amino-acid sequences, so exact sequence duplication does not explain that value.

The final cluster TSVs contain 4432 assignments, 4432 unique members, and no duplicate member assignments at every tested threshold.

The 4288 value is therefore not used as an input, unique-sequence, or final-cluster count in the biological interpretation.
