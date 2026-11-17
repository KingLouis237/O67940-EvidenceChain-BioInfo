# O67940 DALI pre-execution strategy addendum

## Purpose

The prospective O67940 DALI structural-neighbour search strategy was frozen on 2026-08-26 before inspection of any DALI search results.

The original strategy remains the governing analysis design:

`results/active_site_structure/dali_structural_neighbors/O67940_dali_search_strategy.md`

No DALI database-search result has been generated or inspected at the time of this addendum.

This addendum does not change the query, database searches, scoring interpretation or discovery logic. It records additional experimentally grounded reference structures identified through independent functional-anchor audits completed after the original DALI strategy was frozen but before DALI execution.

## Unchanged query

The DALI query remains:

`data/alphafold/AF-O67940-F1-model_v6.pdb`

SHA256:

`0bda0c9e85d92c562f1f82445d8c9e528b6cdc72499d5cbf9812960fddc6fa64`

The validated query contains one chain, 251 residues numbered continuously from 1 to 251, and matches the canonical O67940 sequence exactly.

The query represents a predicted O67940 protomer. It does not constitute experimental evidence for O67940 structure or oligomeric state.

## Unchanged structural-neighbour searches

The same two prospectively defined database searches will be retained:

1. full experimental PDB;
2. PDB25 sequence-redundancy-controlled representative set.

The purpose remains independent recovery of the experimentally determined structural neighbourhood of O67940.

No functional-class restriction will be applied to the database search.

AlphaFoldDB-wide structural searching remains outside this evidence layer.

## Expanded predefined reference audit set

The original strategy predefined 2Q6O and 1RQP because they were the structures central to the historical O67940 case study.

Subsequent functional-anchor audits independently established additional experimentally grounded structural references.

The predefined reference audit set before DALI execution is therefore:

### Historical references

- `2Q6O` — SalL Y70T mutant structure retained because of its role in the historical O67940 comparison.
- `1RQP` — wild-type FDAS/fluorinase structure retained as both a historical and experimentally grounded functional reference.

### Additional experimentally grounded mechanistic references

- `2Q6I` — wild-type SalL structure. This is the preferred wild-type SalL reference for subsequent biological and local structural interpretation.
- `2WR8` — PH0463/O58212 SAM hydroxide adenosyltransferase structure associated with the experimentally grounded HAT-related mechanistic context.

These four structures are known before DALI execution and therefore will not be counted as independent DALI discoveries.

Their DALI placement will instead be used to calibrate the independently recovered structural neighbourhood.

If an exact reference structure is absent from PDB25 because another sequence-redundancy representative was selected, absence from PDB25 will not be interpreted as absence of structural similarity. The corresponding full-PDB result or a direct DALI comparison will be used where necessary.

## Search-result preservation

For both full-PDB and PDB25 searches, the raw result should be preserved before biological curation.

At minimum, preserve for every returned match where available:

- DALI rank;
- PDB identifier;
- chain;
- Z-score;
- RMSD;
- structurally aligned length;
- sequence identity;
- structure description;
- search/database type.

The raw ranking will not be altered to favour known functional classes.

Redundant structures may subsequently be grouped for biological interpretation, but the unfiltered result must remain available.

## Interpretation boundary

DALI Z-score will be interpreted as evidence of structural similarity.

It will not independently establish:

- biochemical activity;
- substrate specificity;
- catalytic mechanism;
- orthology;
- biological oligomeric state.

The functional meaning of relevant structural neighbours must be audited independently using experimental structure metadata, UniProt mapping, primary literature, ligand state, biological assembly and domain architecture.

A known reference structure occurring among high-ranking DALI hits is evidence that its structural context lies within the O67940 structural neighbourhood. It is not by itself evidence that O67940 shares its reaction or substrate specificity.

## Updated stop condition

The DALI structural-neighbour layer is complete when:

1. full-PDB results have been preserved;
2. PDB25 results have been preserved;
3. the meaningful nonredundant structural neighbourhood has been reviewed;
4. the DALI placement or direct DALI relationship of 2Q6O, 1RQP, 2Q6I and 2WR8 has been established;
5. any additional experimentally characterized structural neighbours promoted to interpretive importance have been independently audited;
6. further inspection is no longer materially changing the structural interpretation.

Additional structural-search algorithms will not be introduced by default unless the DALI analysis exposes a specific unresolved structural-search ambiguity.

## Chronology and limitation

The original DALI strategy was frozen on 2026-08-26.

The additional reference structures were identified through independent functional-anchor work completed after that date and before DALI execution.

This addendum is therefore a prospective update to the predefined reference-audit layer, not a response to observed DALI search results.

The original frozen strategy remains unchanged and is retained as the historical decision record.
