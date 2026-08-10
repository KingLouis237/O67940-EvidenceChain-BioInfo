# O67940 broader homolog-context checkpoint

## Current question

The purpose of this analysis is not to identify the highest-scoring homolog and transfer its annotation directly.

The goal is to place O67940 within a broader, reproducibly sampled sequence context before interpreting evolutionary and functional relationships.

## Candidate universe

A UniProtKB search requiring both PF01887 and PF20257, protein length 200-350 aa, and non-fragment status produced 4432 candidates.

The fixed candidate dataset contains:

- 4432 UniProt records
- 4365 unique amino-acid sequences
- 62 exact-duplicate sequence groups
- 67 excess records due to exact sequence duplication

The candidate universe is dominated by Bacteria and Archaea:

- 3991 bacterial records
- 431 archaeal records
- 10 records outside both groups

## Protein-name labels

UniProt protein-name queries do not provide clean independent fluorinase and chlorinase groups.

Of the candidate set:

- 2033 match a fluorinase name query
- 2032 match a chlorinase name query
- 2017 match both

Protein names are therefore retained as metadata rather than treated as ground-truth functional labels.

## PHMMER context

O67940 was searched against the fixed 4432-sequence candidate set.

All candidates were recovered under the exploratory PHMMER significance threshold.

No obvious score breakpoint separated a natural homolog subset.

Strict alignment-coverage filtering was also rejected because it would remove several reviewed functional anchors.

The highest-ranking hits are enriched for organisms close to the Aquifex/Aquificota sequence neighbourhood, meaning a simple top-N selection would strongly bias the final dataset.

## Reviewed anchors

The broader search recovered all eleven reviewed Swiss-Prot anchors previously identified in the reviewed-reference analysis.

They span SAM-hydrolase-like, SalL, and fluorinase annotations.

Their presence provides internal controls for evaluating later sequence-selection and clustering decisions.

## Non-prokaryotic candidates

Ten candidate records fall outside Bacteria and Archaea:

- four Entamoeba proteins
- four Geodia barretti proteins
- Blepharisma stoltei
- Stentor coeruleus

All ten are unreviewed and have protein existence inferred from homology.

Several nevertheless show strong PHMMER similarity to O67940.

The current evidence cannot determine whether these records represent genuine eukaryotic homologs, horizontal transfer, symbiont or microbial sequence assignment, contamination, assembly artefacts, or annotation/taxonomic errors.

They have therefore not been removed automatically.

## Redundancy analysis

MMseqs2 clustering was tested at 95%, 90%, 80%, and 70% sequence identity with 80% bidirectional coverage.

The candidate set produced:

- 3606 clusters at 95%
- 2858 clusters at 90%
- 1816 clusters at 80%
- 1181 clusters at 70%

O67940 remained a singleton at every threshold.

At 90%, O67940 and all eleven reviewed anchors remained in distinct clusters.

At 80% and 70%, several reviewed anchors began collapsing into common clusters.

The 90% identity / 80% bidirectional coverage result was therefore retained as the first redundancy-pruning level.

## Interpretation so far

The broader analysis supports O67940 as part of a diverse SAM-related homologous sequence space.

Its strong structural relationship to the chlorinase/fluorinase reference structures is therefore being interpreted within a much broader sequence context rather than by direct annotation transfer.

The current sequence evidence does not establish whether O67940 is a chlorinase, fluorinase, SAM hydrolase, or another related biochemical activity.

The previously observed G127 residue pattern remains relevant because it resembles the chlorinase/SalL/SAM-hydrolase side of the reviewed comparison more than the reviewed fluorinase pattern, but this remains evidence against a simple direct fluorinase-specific interpretation rather than proof of chlorinase activity.

## What has not yet been done

The 90% clustering step still leaves 2858 clusters, which is too large and too taxonomically uneven for an interpretable phylogenetic analysis.

The next step is therefore to construct a balanced homolog sample that combines:

- the O67940 sequence neighbourhood
- reviewed functional anchors
- broader PHMMER similarity
- taxonomic breadth
- sequence diversity
- explicit handling of the unusual non-prokaryotic records

Only after that selection is frozen should the broader MSA and formal phylogenetic analysis be performed.

Active-site structural mapping and interface/pocket analysis also remain separate unfinished evidence layers.
