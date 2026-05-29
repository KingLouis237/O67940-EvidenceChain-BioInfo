# Step 7 — Functional-residue mapping using the MAFFT alignment

## Aim

This step maps functional residues discussed in the original paper across O67940_AQUAE, 2Q6O, and 1RQP using the MAFFT multiple sequence alignment.

## Why this matters

The previous steps showed that O67940_AQUAE is related to both 2Q6O and 1RQP at the sequence, family/domain, and structural levels. However, broad relatedness is not enough to infer exact biochemical specificity.

The original paper therefore moved from global similarity to functional residues. It discussed SAM-binding and catalytic residues, including positions that distinguish chlorinase-like and fluorinase-like behavior. In particular, it highlighted Gly131 in 2Q6O versus Ser158 in 1RQP, and Tyr70 in 2Q6O versus Thr70 in 1RQP. The paper mapped the corresponding residues in O67940_AQUAE as Gly127 and Val67.

## Input files

- `results/sequence_alignment/O67940_2Q6O_1RQP_chainA_mafft_alignment.fasta`
- `data/structure_chains/O67940_AQUAE_AlphaFold_chainA.pdb`
- `data/structure_chains/2Q6O_chainA.pdb`
- `data/structure_chains/1RQP_chainA.pdb`

## Script used

- `scripts/map_functional_residues_mafft.py`

## Output file

- `results/residue_mapping/functional_residue_mapping_mafft.tsv`

## What the script does

The script connects three coordinate systems:

1. PDB residue numbers from the structure files;
2. ungapped sequence positions extracted from each chain;
3. alignment columns in the MAFFT multiple sequence alignment.

This allows each functional residue from the original paper to be mapped to the corresponding aligned residues in O67940_AQUAE, 2Q6O, and 1RQP.

## Interpretation rule

This mapping is a residue-level evidence layer. It is more functionally informative than global sequence identity or fold similarity, but it is still computational. It should be interpreted as support for a functional hypothesis, not as experimental proof of substrate specificity.

Because this mapping uses a MAFFT sequence alignment, important conclusions should later be cross-checked against structure-guided alignment or structural superposition.
