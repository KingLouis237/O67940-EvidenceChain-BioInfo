# O67940 DALI structural-neighbour search strategy

## Scientific question

Which experimentally determined protein structures are independently recovered as close protomer/domain-level structural neighbours of O67940?

The search is not designed to retrieve structures that confirm a chlorinase or fluorinase interpretation.

Its purpose is to determine the structural neighbourhood recovered independently from the previously selected 2Q6O and 1RQP references.

## Query

The query is:

`data/alphafold/AF-O67940-F1-model_v6.pdb`

This is the AlphaFoldDB v6 O67940 model.

Before DALI submission it was validated as:

- one chain, A;
- 251 residues;
- residues numbered 1-251;
- continuous numbering;
- exact sequence match to `data/O67940_AQUAE.fasta`.

Query SHA256:

`0bda0c9e85d92c562f1f82445d8c9e528b6cdc72499d5cbf9812960fddc6fa64`

The query represents the O67940 protomer for tertiary-structure comparison.

It does not represent an experimentally determined O67940 biological assembly.

## Search design

Two database views will be used with the same validated query.

### 1. Full PDB search

Purpose:

Recover the experimentally determined structural neighbourhood as comprehensively as the DALI server search permits.

This search retains exact PDB entries and closely related deposited structures.

Its limitation is redundancy: heavily represented structural families may occupy many high-ranking positions.

### 2. PDB25 search

Purpose:

Provide a sequence-redundancy-controlled view of the experimentally determined structural neighbourhood.

PDB25 reduces repeated closely related entries and can make broader structural-family relationships easier to inspect.

Its limitation is that the exact historically important structures, including 2Q6O or 1RQP, need not themselves be selected as PDB25 representatives.

The full-PDB and PDB25 searches therefore answer complementary questions and will be interpreted together.

## Historical reference comparison

2Q6O and 1RQP are retained as predefined historical structural references because they were central to the original O67940 case study.

They will not be treated as successful DALI discoveries merely because they are already known.

Their DALI relationship to O67940 will be examined separately using direct pairwise/one-against-many comparison where necessary.

This allows their DALI scores and alignments to be compared with the independently recovered structural neighbourhood without making them the search target.

## Result fields to preserve

For relevant DALI matches, preserve at minimum:

- DALI rank;
- PDB identifier;
- chain;
- Z-score;
- RMSD;
- number of structurally aligned residues;
- query coverage where derivable;
- sequence identity;
- structure description;
- database/search type.

For biologically important candidates, also audit independently:

- experimental method;
- resolution where applicable;
- protein/function annotation;
- UniProt mapping;
- ligand state;
- biological assembly;
- domain architecture;
- whether the sequence is already present in the broader O67940 candidate set.

## Interpretation rules

DALI Z-score is treated as a structural-similarity statistic, not as a biochemical-function score.

No universal Z-score cutoff will be used to assign function.

Interpretation will consider structural similarity together with:

- aligned length and coverage;
- domain correspondence;
- sequence relationship;
- experimental characterization;
- ligand context;
- biological-assembly context.

A high-ranking DALI hit does not automatically become a phylogenetic or functional anchor.

A new anchor must have independently documented biological or experimental justification.

## Search scope exclusions

The initial search will not include an AlphaFoldDB-wide structural search.

The project already contains a broad sequence candidate universe, whereas the present structural question specifically seeks experimentally determined structural anchors.

Whole-oligomer DALI comparison is also outside this step.

DALI/TM-align at this stage address protomer/domain-level tertiary structure. Quaternary and interface organization will be analysed separately using verified experimental biological assemblies.

## Stop condition

The DALI layer is complete when:

1. the full-PDB and PDB25 results have been preserved;
2. the meaningful high-ranking structural neighbourhood has been reviewed;
3. the placement or direct DALI relationship of 2Q6O and 1RQP has been established;
4. any newly identified experimentally characterized structural anchors have been independently audited;
5. additional inspection is no longer changing the structural interpretation materially.

DALI similarity alone will not be used to claim exact enzymatic activity, substrate specificity, oligomeric state, or orthology.
