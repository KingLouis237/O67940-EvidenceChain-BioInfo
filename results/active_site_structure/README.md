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
