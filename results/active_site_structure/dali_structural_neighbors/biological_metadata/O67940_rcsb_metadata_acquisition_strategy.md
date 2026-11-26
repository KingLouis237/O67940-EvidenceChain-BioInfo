# O67940 DALI high-Z neighborhood — RCSB metadata acquisition strategy

## Frozen upstream state

Upstream annotation-neutral PDB registry:

`results/active_site_structure/dali_structural_neighbors/pdb_registry/O67940_dali_high_z_pdb_registry.tsv`

Frozen at commit:

`411c0e60a0aaf3687e16cc5385d3488a24531396`

Registry SHA-256:

`127ede4775e0387c33833c799a7e798e361a55264e9eed4016fbb773a96ae35f`

The registry contains 33 unique PDB entries from the empirically defined O67940 high-Z DALI neighborhood.

## Question

How many distinct deposited polymer entities and reference proteins are represented by these 33 PDB entries?

This layer is intended to distinguish:

- repeated chains within one PDB entry;
- repeated PDB structures of the same reference protein;
- exact deposited-sequence duplicates;
- mutant or variant structures of the same reference protein;
- PDB entries representing different reference proteins.

It is not intended to assign O67940 biochemical function.

## External source

RCSB PDB Data API / GraphQL.

The 33 PDB identifiers are fixed by the frozen upstream registry before metadata retrieval.

## Metadata requested

At entry level:

- PDB identifier;
- structure title;
- experimental method;
- reported resolution;
- deposit and initial-release dates.

At polymer-entity level:

- RCSB polymer-entity identifier;
- deposited molecule description;
- polymer type;
- canonical deposited sequence;
- deposited sequence length;
- mutation count;
- author and label chain identifiers;
- reference-sequence database names and accessions;
- source organism and NCBI taxonomy identifier.

## Raw-data policy

The GraphQL request payload, response headers, raw JSON response, retrieval manifest, and SHA-256 checksums will be retained unchanged.

Raw RCSB response content will not be reformatted or manually edited.

Derived tables will be generated separately from the frozen raw response.

## Consolidation logic

No two PDB entries will be declared the same biological protein solely because their descriptions are similar.

Evidence will be retained at multiple levels:

1. PDB entry identity;
2. RCSB polymer-entity identity;
3. exact deposited-sequence identity, represented by SHA-256 of the canonical sequence;
4. external reference-sequence accession where supplied by RCSB.

A shared UniProt or other reference accession will be treated as evidence that structures map to the same reference protein, not as evidence that their deposited experimental sequences are identical.

Mutation status will remain explicit.

## Interpretation limits

RCSB molecule names and database cross-references are metadata, not biochemical validation.

Shared reference accession does not establish that every structure has the same catalytic state, ligand state, mutation state, oligomeric state, or activity.

Different reference accessions do not by themselves establish paralogy, orthology, or functional divergence.

Functional claims will require a later UniProt and primary-literature audit.

## Planned outputs

Raw acquisition bundle:

`results/active_site_structure/dali_structural_neighbors/biological_metadata/raw/rcsb_<retrieval-date>/`

Later derived layer:

- one row per PDB polymer entity;
- exact-sequence hashes;
- reference-accession mappings;
- PDB-to-reference-protein consolidation;
- validation/accounting table.
