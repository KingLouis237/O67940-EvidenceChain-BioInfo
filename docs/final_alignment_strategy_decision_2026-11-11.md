# Final alignment-strategy decision for the O67940 reviewed-reference analysis

**Decision date:** 2026-11-11

**Status:** Frozen before generation of the final MAFFT alignment or IQ-TREE topology.

## Purpose

This document freezes the multiple-sequence-alignment strategy for the final 12-taxon reviewed-reference evolutionary analysis of O67940.

The alignment method is selected from sequence architecture and pre-tree diagnostics rather than from whichever alignment later produces the most attractive or biologically convenient phylogenetic topology.

## Input

Canonical biological input:

`results/phylogeny/O67940_final_reviewed_reference_set.fasta`

The input contains 12 biological taxa:

- O67940 query
- 3 direct experimental functional landmarks
- 8 additional reviewed evolutionary-context proteins

PDB-derived 1RQP and 2Q6O records are not separate taxa in the final biological alignment.

## MAFFT environment

Installed MAFFT:

- version: 7.525
- Bioconda build: h031d066_1
- environment: `methods_bioinfo`

The exact installed version is retained rather than changing software version after the analysis design has been frozen.

## Pre-alignment architecture evidence

Sequence lengths in the canonical set range from 251 to 300 aa, a span of 49 residues.

An older exploratory alignment was examined only as a sequence-architecture diagnostic. It was not treated as the final alignment and its topology was not used to select the final alignment method.

After excluding only the non-independent PDB-derived 2Q6O and 1RQP records, the exploratory alignment contained exactly the same 12 biological taxa represented by the final reference-set design.

The 12-taxon exploratory architecture diagnostic showed:

- alignment width: 329 columns
- fully occupied columns: 216 / 329 (65.7%)
- columns with >=50% gaps: 59 / 329 (17.9%)
- columns with >=75% gaps: 28 / 329 (8.5%)
- longest contiguous region with >=50% gaps: 22 columns

O67940 contained 12 internal gap runs in that exploratory alignment, with a longest run of 23 residues. Several HAT-like and SalL-like sequences also contained approximately 20-24-residue internal gap runs.

These observations indicate genuine insertion/deletion heterogeneity, but not a pattern dominated by isolated local homologous blocks separated by extensive unrelated sequence.

## Primary alignment decision

The primary alignment will use **MAFFT G-INS-i**.

Operational command design:

`mafft --globalpair --maxiterate 1000 --thread -1 --threadit 0`

The final canonical FASTA will be supplied as the input and the aligned FASTA will be written to a new results file.

### Rationale

MAFFT describes G-INS-i as appropriate for sequences expected to share global homology.

The reviewed-reference proteins have broadly comparable lengths and an exploratory alignment shows extensive occupancy across the protein length, while longer gaps occur as localized indel-rich regions within that broader homologous framework.

This makes a global-pair alignment model more appropriate as the primary strategy than a local-pair strategy designed around one conserved domain plus unrelated or highly divergent flanking sequence.

## Deterministic refinement

`--threadit 0` will be used.

MAFFT documentation notes that multithreaded iterative refinement can produce different results between runs. Disabling multithreading specifically during the iterative-refinement stage provides a deterministic reconstruction while still allowing parallelism during other computational stages.

The final alignment will be rerun and its SHA256 compared to confirm byte-level reproducibility.

## Alignment-method sensitivity

A separate **E-INS-i sensitivity alignment** is predefined.

Rationale:

- the protein family has a multi-domain context;
- several taxa contain localized 20-24-residue gap runs;
- one approximately 22-column region is highly gappy across the exploratory reference alignment.

E-INS-i therefore provides a useful sensitivity test for whether treatment of multi-block/gappy regions materially changes the downstream evolutionary result.

It is a sensitivity analysis, not a competing primary alignment selected after topology inspection.

## L-INS-i decision

L-INS-i is not selected as the primary method and is not included as a default sensitivity analysis.

Its one-conserved-domain-plus-long-flanking-regions assumption is not the best description of the current 12-sequence architecture.

This decision may only be revisited if a later independent sequence-quality check reveals substantial fragmentary or nonhomologous flanking sequence that is not currently represented in the evidence.

## Trimming policy

The primary alignment will be analysed untrimmed.

Alignment trimming will not be introduced after inspection of the primary topology.

If a trimmed alignment is used, it must be defined in advance as a separate sensitivity analysis with:

- a named trimming tool and exact version;
- frozen parameters;
- retained-column counts;
- an explicit interpretation boundary.

The untrimmed G-INS-i alignment remains the primary evolutionary input.

## Interpretation boundary

Selecting G-INS-i does not establish that every aligned residue pair is biologically equivalent.

A multiple sequence alignment is a model of positional homology.

The final alignment must still be quality-audited before phylogenetic inference, including:

- taxon count
- sequence preservation
- alignment width
- per-sequence gap content
- highly gapped regions
- suspicious isolated columns or blocks
- preservation of relevant mechanistic residue neighborhoods

The alignment strategy cannot establish:

- O67940 biochemical function
- substrate specificity
- orthology
- evolutionary direction
- oligomeric state
- catalytic equivalence of individual residues

These require separate evolutionary, structural, mechanistic and experimental evidence.

## Downstream rule

No final IQ-TREE topology will be generated until:

1. the primary G-INS-i alignment has been generated;
2. alignment integrity and reproducibility have been validated;
3. the primary alignment has been version-controlled.

The phylogenetic method will then be executed according to the previously frozen prospective analysis contract.
