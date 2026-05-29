# Step 3 — Domain-level PAE interpretation

## Aim

The first PAE analysis used a rough N-terminal/C-terminal split. After inspecting the UniProt JSON record, exact domain boundaries were recovered from the UniProt `features` field. These boundaries were then used to calculate a more biologically meaningful PAE summary.

## Domain boundaries used
| Region | Coordinates |
| N-terminal SAM_HAT domain | 3–148 |
| Inter-domain region | 149–170 |
| C-terminal SAM_HAT domain | 171–246 |

## Result

| Region comparison | Mean PAE | Median PAE | Maximum PAE |
| N-terminal domain internal | 2.33 Å | 2.00 Å | 19.00 Å |
| C-terminal domain internal | 1.83 Å | 2.00 Å | 6.00 Å |
| Between N-terminal and C-terminal domains | 4.03 Å | 3.00 Å | 20.00 Å |
| N-terminal domain vs inter-domain region | 3.47 Å | 3.00 Å | 19.00 Å |
| C-terminal domain vs inter-domain region | 3.21 Å | 3.00 Å | 10.00 Å |

## Interpretation

The domain-level PAE values are low overall. The N-terminal and C-terminal SAM_HAT domains each have low internal mean PAE values, indicating confident internal positioning within each domain. The between-domain mean PAE is 4.03 Å, suggesting that AlphaFold is also reasonably confident about the relative arrangement of the two annotated domains.

This improves on the earlier rough half-protein split because the analysis now uses biologically meaningful UniProt domain boundaries rather than arbitrary residue halves.

## Working conclusion

The AlphaFoldDB v6 model of O67940_AQUAE is supported by both high pLDDT and low domain-level PAE. This makes it reasonable to use the predicted structure in downstream structural comparison.

However, this remains predicted structural evidence. It does not prove enzyme activity, halogenase function, chlorinase specificity, or fluorinase specificity. Those questions require comparison with experimentally characterized reference structures and functional-residue mapping.
