# Step 6A — MAFFT installation and verification

## Aim

This step documents the installation and verification of MAFFT, which will be used to align the extracted chain A sequences from O67940_AQUAE, 2Q6O, and 1RQP.

## Why this matters

TM-align compares 3D structures, but sequence alignment is needed to map residue positions between proteins. This is important for functional interpretation because enzyme specificity often depends on specific residues rather than global fold similarity alone.

## Installation command

```bash
conda install -y -c bioconda -c conda-forge mafft
