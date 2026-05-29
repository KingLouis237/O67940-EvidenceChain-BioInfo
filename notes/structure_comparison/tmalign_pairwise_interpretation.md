# Step 5C — TM-align pairwise structural comparison interpretation

## Aim

This step used TM-align to compare the chain-specific O67940_AQUAE AlphaFold model with the experimentally solved reference structures 2Q6O and 1RQP.

## Comparisons performed

| Comparison | Purpose |
|---|---|
| O67940_AQUAE AlphaFold chain A vs 2Q6O chain A | Compare query model with chlorinase-related reference |
| O67940_AQUAE AlphaFold chain A vs 1RQP chain A | Compare query model with fluorinase reference |
| 2Q6O chain A vs 1RQP chain A | Compare the two reference structures |

## Results

| Comparison | Aligned length | RMSD | Sequence identity over aligned residues | TM-score normalized by chain 1 | TM-score normalized by chain 2 |
| O67940_AQUAE vs 2Q6O | 250 | 2.01 Å | 0.288 | 0.91010 | 0.85311 |
| O67940_AQUAE vs 1RQP | 250 | 2.01 Å | 0.268 | 0.90673 | 0.78998 |
| 2Q6O vs 1RQP | 267 | 1.89 Å | 0.378 | 0.92203 | 0.85589 |

## Interpretation

The AlphaFold model of O67940_AQUAE aligns strongly with both reference structures. In both O67940 comparisons, 250 residues are aligned and the RMSD is 2.01 Å. This indicates that O67940_AQUAE has a predicted global fold compatible with both 2Q6O and 1RQP.

The TM-score normalized by the reference structure is higher for 2Q6O than for 1RQP. This suggests that, at the global fold level, the O67940_AQUAE model is somewhat closer to 2Q6O than to 1RQP.

However, this result should not be overinterpreted. TM-align measures structural similarity, not enzyme activity. A high structural similarity score cannot prove whether O67940_AQUAE is a chlorinase, fluorinase, or broader halogenase.

## Working conclusion

The TM-align result supports strong fold-level relatedness between O67940_AQUAE and the two reference enzymes, with a modest structural preference toward the 2Q6O chlorinase-related reference. The next step must be sequence alignment and functional-residue mapping, because substrate specificity depends on local active-site features rather than global fold similarity alone.
