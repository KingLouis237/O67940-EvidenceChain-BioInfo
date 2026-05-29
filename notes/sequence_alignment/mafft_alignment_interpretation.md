# Step 6 — MAFFT sequence alignment interpretation

## Aim

This step aligned the extracted chain A sequences from O67940_AQUAE, 2Q6O, and 1RQP using MAFFT.

## Why this step matters

The TM-align structural comparison showed that O67940_AQUAE has strong global fold similarity to both 2Q6O and 1RQP, with a modest structural preference toward 2Q6O. However, global structural similarity does not prove enzyme specificity. Sequence alignment is needed to map corresponding residues across the query and reference proteins.

## Input

The input FASTA file was:

`data/reference_sequences/O67940_2Q6O_1RQP_chainA_sequences.fasta`

It contained:

- O67940_AQUAE AlphaFold chain A
- 2Q6O chain A
- 1RQP chain A

## Output

The MAFFT alignment was written to:

`results/sequence_alignment/O67940_2Q6O_1RQP_chainA_mafft_alignment.fasta`

The alignment summary was written to:

`results/sequence_alignment/O67940_2Q6O_1RQP_alignment_summary.tsv`

## Main results

| Comparison | Identical positions | Compared positions | Pairwise identity excluding gap columns |
|---|---:|---:|---:|
| O67940_AQUAE vs 2Q6O | 74 | 249 | 0.2972 |
| O67940_AQUAE vs 1RQP | 74 | 250 | 0.2960 |
| 2Q6O vs 1RQP | 105 | 267 | 0.3933 |

## Interpretation

At the sequence level, O67940_AQUAE is almost equally similar to 2Q6O and 1RQP. The difference between O67940_AQUAE vs 2Q6O and O67940_AQUAE vs 1RQP is very small: 29.72% versus 29.60% identity over non-gap aligned positions.

Therefore, global sequence identity alone does not strongly distinguish whether O67940_AQUAE is more chlorinase-like or fluorinase-like.

This contrasts slightly with the TM-align structural comparison, where O67940_AQUAE showed a modestly higher reference-normalized TM-score against 2Q6O than against 1RQP. Together, these results suggest that broad sequence and structure evidence support relatedness to both references, but precise functional interpretation requires residue-level mapping.

## Working conclusion

The MAFFT alignment is suitable for the next step: mapping key functional residues discussed in the original article. This is necessary because substrate specificity is more likely to depend on local active-site or binding-pocket residues than on global sequence identity alone.
