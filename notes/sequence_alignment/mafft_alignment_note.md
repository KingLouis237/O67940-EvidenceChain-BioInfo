# Step 6 — MAFFT sequence alignment

## Aim

This step aligns the representative chain A sequences from O67940_AQUAE, 2Q6O, and 1RQP.

## Why this step matters

TM-align showed that the predicted O67940_AQUAE structure is globally similar to both reference structures. However, functional interpretation depends on more than global fold similarity. Enzyme specificity can depend on a small number of residues in the active site or binding pocket.

Therefore, sequence alignment is needed to map corresponding residue positions between:

- O67940_AQUAE AlphaFold chain A
- 2Q6O chain A
- 1RQP chain A

## Input file

`data/reference_sequences/O67940_2Q6O_1RQP_chainA_sequences.fasta`

This file contains the extracted chain A sequences from the query model and the two reference structures.

## Output files

- `results/sequence_alignment/O67940_2Q6O_1RQP_chainA_mafft_alignment.fasta`
- `results/sequence_alignment/O67940_2Q6O_1RQP_alignment_summary.tsv`

## Interpretation rule

The MAFFT alignment prepares the sequences for residue mapping. It does not by itself prove whether O67940_AQUAE is a chlorinase, fluorinase, or broader halogenase. The next step is to inspect functionally important residue positions in the alignment.
