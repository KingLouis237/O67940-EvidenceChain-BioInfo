# Step 4B — Reference structure content inspection

## Aim

After downloading the reference structures 2Q6O and 1RQP, the next step was to inspect what each PDB file contains before using them for comparison.

This matters because a PDB file may contain more than one protein chain, ligands, ions, crystallographic molecules, and water molecules. A valid file download does not automatically tell us which chain should be used for comparison.

## What was inspected

The script `scripts/inspect_reference_pdb_contents.py` reads the PDB-format files:

- `data/pdb/2Q6O.pdb`
- `data/pdb/1RQP.pdb`

It summarizes:

1. protein chains;
2. ATOM records per chain;
3. approximate residue counts per chain;
4. HETATM records, including ligands, ions, cofactors, and water.

## Why this is useful

The AlphaFold model of O67940_AQUAE represents one predicted protein chain. To compare it properly against experimental structures, we need to know which chains in 2Q6O and 1RQP correspond to the protein structures of interest.

The heteroatom table is also useful because ligands/cofactors can reveal the biochemical context of a structure. However, not every HETATM record is functionally important. Water molecules and crystallization components must be distinguished from biologically meaningful ligands.

## Interpretation rule

This inspection step does not yet compare structures or infer function. It only prepares the reference structures for careful downstream comparison by identifying chains and non-protein molecules.
