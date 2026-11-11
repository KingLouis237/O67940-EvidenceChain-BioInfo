# Final reviewed-reference set decision for O67940 evolutionary analysis

Frozen prospectively: 2026-11-11

## Purpose

This document defines the biological taxa to be used in the primary
reviewed-reference evolutionary analysis of O67940 before any final MAFFT
alignment or IQ-TREE topology is generated.

The purpose of freezing the set at this stage is to prevent reference
selection from being influenced by the final tree.

## Biological question

The primary evolutionary analysis asks where O67940 is positioned relative
to a high-confidence reviewed reference context spanning the experimentally
supported SAM-hydroxide-adenosyltransferase / SAM-hydrolase and
SAM-dependent halogenase sides of the shared family landscape.

The tree is not intended to assign biochemical activity by itself.

## Operational family universe

The reference-selection basis was defined previously and independently of
the final phylogenetic result.

The frozen UniProt query retrieved proteins satisfying:

- Pfam `PF01887`;
- Pfam `PF20257`;
- `fragment:false`;
- sequence length from 200 to 350 amino acids.

The query was accessed on 2026-08-07.

Frozen candidate-universe files:

- `data/databases/O67940_uniprot_pfam_candidates/query.txt`
- `data/databases/O67940_uniprot_pfam_candidates/candidate_metadata.tsv`
- `data/databases/O67940_uniprot_pfam_candidates/candidate_sequences.fasta`

The frozen operational universe contains 4,432 proteins.

The observed sequence-length range in the retrieved universe is 201–346
amino acids.

## Reviewed-reference selection rule

The primary reviewed-reference set uses every reviewed UniProt entry present
in the frozen 4,432-protein operational universe.

There are exactly 11 such reviewed entries.

No reviewed entry satisfying the frozen operational query was omitted.

No additional reviewed protein was added because of:

- its database functional name;
- its PHMMER score;
- its position in the exploratory FastTree analysis;
- similarity to a preferred functional hypothesis;
- or class balancing.

O67940 is added separately as the query protein.

The resulting primary biological set therefore contains 12 taxa:

- 1 query protein;
- 11 reviewed reference proteins.

## Functional-evidence roles

Reviewed database status and experimental functional validation are kept
separate.

Three reviewed proteins have undergone direct functional-anchor audits:

- `O58212` — direct experimental anchor for SAM
  hydroxide-adenosyltransferase / SAM-hydrolysing chemistry;
- `A4X3Q0` — direct experimental anchor for SalL-like
  non-fluorinating SAM-dependent halogenase chemistry;
- `Q70GK9` — direct experimental anchor for SAM-dependent
  fluorinase chemistry.

These three proteins may be used as experimentally grounded functional
landmarks when interpreting the evolutionary analysis.

The remaining eight reviewed proteins are retained as evolutionary context.
Their current UniProt protein names are annotations and are not treated here
as equivalent to independently audited biochemical ground truth.

## Sequence-integrity checks completed before freezing

All 12 biological sequences were checked before this decision.

The checks established that:

- every expected biological accession is present exactly once;
- no expected accession is missing;
- no exact duplicate biological sequence is present;
- all sequences contain standard amino-acid characters;
- the reviewed-reference sequences agree exactly with the frozen candidate
  universe;
- all 11 reviewed sequences agree exactly with the frozen Swiss-Prot
  2026-07-04 snapshot;
- O67940 agrees exactly with `data/O67940_AQUAE.fasta`;
- the current independently audited O58212, A4X3Q0 and Q70GK9 sequences
  agree exactly with the corresponding sequences in the reviewed set.

## PHMMER information

PHMMER similarity values are retained as descriptive sequence-similarity
information.

They are not used as an inclusion threshold.

A hard score, top-N or 90% query/target coverage cutoff was rejected earlier
because no biologically justified breakpoint was identified and because such
rules would selectively remove relevant reviewed SalL/fluorinase references.

## Structural records are not additional biological taxa

The earlier 14-record exploratory FASTA contained the biological reference
set plus `2Q6O_chainA` and `1RQP_chainA`.

These PDB-derived sequences will not be included as separate taxa in the
primary biological phylogeny.

`1RQP` represents the experimentally characterized Q70GK9 fluorinase and
would duplicate that biological protein.

`2Q6O` represents the SalL Y70T mutant and is neither an independent
biological taxon nor the appropriate wild-type SalL sequence.

More generally, PDB constructs or chains representing proteins already in
the canonical biological reference set will not be added as independent
phylogenetic taxa.

They remain available for structural and active-site analyses.

## Primary-set interpretation boundary

The 12-taxon analysis is a high-confidence reviewed-reference phylogeny.

It is not intended to reconstruct the complete evolutionary history of all
4,432 operational candidate proteins.

The primary tree may support statements about the evolutionary placement of
O67940 relative to reviewed and experimentally grounded reference context.

It cannot by itself demonstrate:

- O67940 biochemical activity;
- substrate specificity;
- fluorination, chlorination or hydrolysis;
- orthology;
- evolutionary direction;
- ancestral functional state;
- or biological oligomeric state.

Functional interpretation requires convergence with the independently
defined mechanistic residue/structural evidence layer.

## Primary set

The frozen primary taxa are:

- `O67940`
- `O58212`
- `Q5SLF5`
- `Q59045`
- `A8M783`
- `A4X4S2`
- `A4X3Q0`
- `R4LHX8`
- `Q70GK9`
- `W0W999`
- `A0A1G9FQX8`
- `W8JNL4`

Any later change to this primary set requires an explicit documented reason
and must not be made simply because of an observed tree topology.

## Sensitivity analyses

Sensitivity analyses may later test whether O67940 placement is robust to
predefined changes such as:

- excluding reviewed context proteins that lack direct functional audits;
- alignment-treatment changes defined before the sensitivity run;
- or other explicitly justified reference-set perturbations.

Sensitivity analyses will remain separate from the frozen primary analysis.

## Next step

After this decision is validated and version-controlled, a canonical
12-sequence FASTA will be generated from frozen source sequences with
accession-based headers and mechanical integrity checks.

No final alignment or phylogenetic tree should be generated before that
canonical FASTA is validated.
