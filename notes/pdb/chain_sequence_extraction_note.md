# Step 4C — Chain sequence extraction

## Aim

This step extracts representative protein-chain sequences from the AlphaFold model of O67940_AQUAE and from the reference PDB structures 2Q6O and 1RQP.

## Why this step matters

The downloaded reference PDB files contain multiple protein chains. The AlphaFold model contains one predicted chain, while 2Q6O contains chains A and B and 1RQP contains chains A, B, and C.

For sequence alignment and residue mapping, it is clearer to start with one representative chain from each structure:

- O67940_AQUAE AlphaFold model, chain A
- 2Q6O, chain A
- 1RQP, chain A

This prevents accidentally comparing the query protein to a full multi-chain structure.

## What the script does

The script `scripts/extract_structure_chain_sequences.py` reads ATOM records from the PDB files and converts three-letter amino-acid residue names into one-letter amino-acid codes.

It writes:

- `data/reference_sequences/O67940_2Q6O_1RQP_chainA_sequences.fasta`
- `results/pdb/reference_chainA_sequence_summary.tsv`

## Interpretation rule

This step prepares the sequences for alignment. It does not yet determine function. The next meaningful biological step is to align these sequences and inspect whether key functional residues from the original paper map consistently across O67940_AQUAE, 2Q6O, and 1RQP.

## Output check

The chain sequence extraction produced three clean sequences:

| Sequence | Length | Unknown residues |
| O67940_AQUAE AlphaFold chain A | 251 | No |
| 2Q6O chain A | 269 | No |
| 1RQP chain A | 291 | No |

This confirms that the extracted chain A sequences are suitable for downstream multiple sequence alignment.

Note:
The TSV table should be viewed with:

```bash
column -t -s $'\t' results/pdb/reference_chainA_sequence_summary.tsv
