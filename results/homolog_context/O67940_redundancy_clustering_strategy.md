# O67940 broader-candidate redundancy clustering strategy

## Purpose

The broader PF01887/PF20257 UniProtKB candidate set contains 4432 proteins.

PHMMER showed that simple top-hit selection would overrepresent the sequence neighbourhood closest to O67940. Before choosing a manageable phylogenetic set, the amount and structure of sequence redundancy therefore need to be measured.

This clustering step is a sampling analysis. It is not a functional classification.

## Input

The fixed candidate FASTA is:

`data/databases/O67940_uniprot_pfam_candidates/candidate_sequences.fasta`

It contains 4432 sequences.

## Tool

Redundancy analysis uses the project-local SSE4.1 build of MMseqs2 release 18-8cc5c.

The executable path is:

`tools/mmseqs2_18-8cc5c_sse41/bin/mmseqs`

The explicit path is used so that the analysis does not accidentally call the incompatible Conda MMseqs2 executable.

## Sensitivity design

Four sequence-identity thresholds will be tested:

- 95%
- 90%
- 80%
- 70%

All runs will use:

- bidirectional coverage mode: `--cov-mode 0`
- minimum coverage: `-c 0.80`
- exact alignment identity calculation: `--alignment-mode 3`
- single-step clustering: `--single-step-clustering 1`

The 80% coverage criterion is being used here to decide whether two already-defined family candidates are sufficiently overlapping to be treated as redundant.

It is not the same as the earlier PHMMER coverage question, where coverage was tested as a possible family-membership filter and rejected.

## Why several identity thresholds are tested

No single sequence-identity value is assumed in advance to be the correct redundancy threshold.

The sensitivity analysis will determine how strongly the 4432-sequence set collapses at 95%, 90%, 80%, and 70% identity.

The final sampling decision will be made after inspecting:

- number of clusters
- cluster-size distribution
- O67940 cluster membership
- reviewed-reference membership
- non-prokaryotic candidate membership
- taxonomic and sequence diversity

## Anchor handling

Clustering will not automatically determine which biologically important reference sequences survive into the final phylogenetic set.

O67940 and the reviewed functional reference proteins will be tracked explicitly.

The structural reference sequences 2Q6O and 1RQP are not members of the downloaded 4432-sequence UniProtKB candidate FASTA and will be added explicitly at the later phylogenetic-set construction stage.

## Non-prokaryotic candidates

The 10 candidates assigned to eukaryotic taxa will also be tracked across all clustering thresholds.

Their cluster behaviour may help determine whether they group tightly with other family members, form redundant taxon-specific groups, or require separate treatment.

## Limitation

Sequence clustering reduces redundancy but does not establish orthology, biochemical activity, substrate specificity, or evolutionary direction.

The selected threshold will therefore be used only as one component of broader phylogenetic sampling.

## Decision after sensitivity analysis

The sensitivity analysis supported 90% sequence identity with 80% bidirectional coverage as the first redundancy-pruning threshold.

At this level, the 4432 records formed 2858 clusters while O67940 and all reviewed functional anchors remained in distinct clusters.

At 80% and 70%, multiple reviewed reference proteins began collapsing into shared clusters, indicating loss of biologically useful family diversity.

The 90% cluster set will therefore define the non-redundant candidate pool for the next sampling stage.

The MMseqs2 representative sequence will not automatically be treated as the preferred biological representative where a cluster contains a reviewed anchor or another explicitly retained reference.
