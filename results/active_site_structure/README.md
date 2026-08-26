# O67940 structural evidence layer

## Purpose

The structural analysis separates three different biological questions that require different structural representations.

Using one representation for all three would mix tertiary-fold similarity with local active-site geometry and quaternary organization.

## 1. Protomer-level tertiary structure

Question:

Does the predicted O67940 polypeptide have the same underlying tertiary fold as experimentally characterized related proteins?

Representation:

- O67940 AlphaFold monomer
- a verified representative experimental protomer, selected after checking equivalence among relevant copies in the biological assembly

Methods include:

- TM-align
- DALI structural-neighbour search

The previous chain-A TM-align comparisons belong to this level.

A strong protomer-level structural match supports similarity of tertiary architecture. It does not establish conservation of oligomeric state, active-site geometry, or biochemical specificity.

## 2. Local ligand and active-site structure

Question:

Do structurally corresponding O67940 residues occupy local environments comparable with experimentally characterized ligand-binding and catalytic residues?

Representation:

- O67940 monomer
- ligand-bound experimental reference structures

This level will examine mapped positions including the G127/G131/S158 region and other validated SAM-related residues.

Local residue equivalence will be assessed in the context of neighbouring residues and experimental ligand positions, rather than from global RMSD alone.

## 3. Quaternary and interface structure

Question:

How are the experimentally characterized functional sites related to interactions between protomers?

Representation:

- verified biological assemblies of the experimental reference structures

The biological assembly must not be assumed to be identical to the crystallographic asymmetric unit or to every chain present in a downloaded coordinate file.

The assembly definition, chain composition, ligand state, and supporting PDB annotation must be checked before interface interpretation.

O67940 currently has a monomeric AlphaFoldDB model. That model does not establish its biological oligomeric state.

If O67940 is superposed onto a reference protomer within an experimentally supported assembly, the result can test compatibility with an analogous interface geometry. It cannot demonstrate that O67940 forms the same oligomer.

## Representative-protomer QC

Before using a particular reference chain such as chain A as the canonical protomer for local structural analysis, the protomers present in the relevant experimental assembly will be compared.

This check asks whether copies of the protein have effectively equivalent tertiary conformations or whether ligand occupancy, interface context, crystallographic environment, mutations, or other structural differences make one copy non-representative.

If the protomers are effectively equivalent, one documented representative chain can be used.

If meaningful differences are present, the analysis will preserve those differences rather than selecting chain A by convention.

## Current interpretation of previous TM-align results

The existing O67940-versus-2Q6O and O67940-versus-1RQP chain-A TM-align results remain valid as protomer-level tertiary-structure evidence.

They should not be interpreted as evidence that O67940 has:

- the same oligomeric state;
- the same inter-subunit active site;
- identical ligand-pocket geometry;
- identical substrate specificity.

## References

- Mazumder R, Vasudevan S. Structure-Guided Comparative Analysis of Proteins: Principles, Tools, and Applications for Predicting Function. PLoS Computational Biology. 2008;4:e1000151.
- Zhang Y, Skolnick J. TM-align: a protein structure alignment algorithm based on the TM-score. Nucleic Acids Research. 2005;33:2302-2309.
- Holm L. Dali server: structural unification of protein families. Nucleic Acids Research. 2022;50:W210-W215.
- RCSB PDB. Guide to Understanding PDB Data: Biological Assemblies.

## DALI query validation

The AlphaFoldDB v6 PDB file

`data/alphafold/AF-O67940-F1-model_v6.pdb`

was validated before use as the DALI protomer-level structural-search query.

Validation showed:

- one coordinate chain: A;
- 251 C-alpha residues;
- exact sequence identity with `data/O67940_AQUAE.fasta`;
- residue numbering 1-251;
- contiguous residue numbering;
- mean C-alpha pLDDT 96.7048;
- minimum C-alpha pLDDT 77.56.

The PDB SHA256 is:

`0bda0c9e85d92c562f1f82445d8c9e528b6cdc72499d5cbf9812960fddc6fa64`

An independent sequence extraction also recovered 251 residues and an exact match to the project FASTA.

This validates the identity and integrity of the structure used for protomer-level structural searching.

It does not validate the AlphaFold coordinates experimentally and does not provide evidence for the biological oligomeric state of O67940.

Validation output:

`results/active_site_structure/dali_structural_neighbors/O67940_dali_query_validation.tsv`

Validation script:

`scripts/05_evolutionary_active_site_context/validate_dali_query_structure.py`

## DALI query validation

Before structural-neighbour searching, the AlphaFoldDB v6 PDB file

`data/alphafold/AF-O67940-F1-model_v6.pdb`

was checked against the canonical project sequence.

The validation found:

- one coordinate chain: A;
- 251 C-alpha residues;
- exact sequence identity with `data/O67940_AQUAE.fasta`;
- residue numbering from 1 to 251;
- contiguous residue numbering;
- mean C-alpha pLDDT of 96.7048;
- minimum C-alpha pLDDT of 77.56.

The PDB SHA256 is:

`0bda0c9e85d92c562f1f82445d8c9e528b6cdc72499d5cbf9812960fddc6fa64`

A separate direct extraction of the chain-A sequence independently recovered 251 residues and an exact match to the project FASTA.

The file is therefore accepted as the O67940 protomer query for the DALI structural-neighbour search.

This validation establishes query identity and file integrity. It does not experimentally validate the AlphaFold coordinates and does not provide evidence for the biological oligomeric state of O67940.

Validation script:

`scripts/05_evolutionary_active_site_context/validate_dali_query_structure.py`

Validation output:

`results/active_site_structure/dali_structural_neighbors/O67940_dali_query_validation.tsv`
