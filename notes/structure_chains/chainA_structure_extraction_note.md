# Step 5A — Chain A structure extraction for structural comparison

## Aim

This step extracts representative chain A protein coordinates from the AlphaFold model of O67940_AQUAE and from the reference structures 2Q6O and 1RQP.

## Why this step matters

The reference PDB files contain multiple chains:

- 2Q6O contains chains A and B.
- 1RQP contains chains A, B, and C.

The AlphaFold model of O67940_AQUAE represents one predicted protein chain. For a fair first structural comparison, the workflow therefore uses one representative chain from each structure.

## What was extracted

The script `scripts/extract_chainA_structure_files.py` extracts ATOM records for chain A only from:

- `data/alphafold/AF-O67940-F1-model_v6.pdb`
- `data/pdb/2Q6O.pdb`
- `data/pdb/1RQP.pdb`

The output files are:

- `data/structure_chains/O67940_AQUAE_AlphaFold_chainA.pdb`
- `data/structure_chains/2Q6O_chainA.pdb`
- `data/structure_chains/1RQP_chainA.pdb`

## Why HETATM records were excluded

HETATM records include ligands, ions, water molecules, and other non-protein atoms. These are biologically important later for active-site interpretation, but they can interfere with a first global protein-structure alignment.

Therefore, this step keeps only protein ATOM records. Ligands such as SAM and CL remain available in the original PDB files for later active-site interpretation.

## Interpretation rule

This step does not compare structures yet. It prepares clean, chain-specific protein coordinate files for downstream structural alignment.
