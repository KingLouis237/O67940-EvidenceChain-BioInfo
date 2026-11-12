# Final mechanistic-landmark interpretation

## Purpose

This analysis asks how experimentally grounded mechanistic positions from three audited reference proteins map onto O67940 within the prospectively defined final 12-taxon evolutionary reference set.

The aim is not to assign enzyme activity from a small number of residues. The aim is to establish reproducible positional correspondence to experimentally supported landmarks and to determine how that evidence changes the earlier chlorinase/fluorinase-focused interpretation.

## Evidence basis

The mapping uses the primary untrimmed MAFFT G-INS-i alignment:

`results/phylogeny/O67940_final_reviewed_reference_set_ginsi.fasta`

The alignment was generated from the frozen 12-sequence biological reference set using MAFFT 7.525 with:

`--globalpair --maxiterate 1000 --thread -1 --threadit 0`

The three experimentally audited functional anchors are:

- O58212 / PH0463, representing the HAT/SAM-hydrolysing mechanistic context
- A4X3Q0 / SalL, representing experimentally demonstrated SAM-dependent non-fluorinating halogenase activity
- Q70GK9 / FDAS, representing experimentally demonstrated SAM-dependent fluorinase activity

The residue landmarks were defined separately from the alignment in:

`results/residue_mapping/O67940_final_mechanistic_landmark_registry.tsv`

Each landmark is linked back to the corresponding audited functional-anchor evidence records. The alignment therefore determines positional correspondence; it does not define which residues were chosen as mechanistically relevant.

## Reproducible mappings

Seven experimentally grounded landmarks were mapped through the final G-INS-i alignment.

For the PH0463/O58212 mechanistic network:

- O58212 D68 maps to O67940 D69 at alignment column 83.
- O58212 R75 maps to O67940 R76 at alignment column 90.
- O58212 H127 maps to O67940 H126 at alignment column 171.

For the SalL and FDAS specificity-related positions:

- SalL Y70 and FDAS T75 occupy the same homologous alignment column, column 81. O67940 contains V67 at this position.
- SalL G131 and FDAS S158 occupy the same homologous alignment column, column 172. O67940 contains G127 at this position.

All seven anchor residues mapped back to their expected identities in their own anchor sequences. Each of these alignment columns was occupied in all 12 sequences in the final reference set.

The long-format mapping table contains 84 rows, corresponding to 7 landmarks across 12 biological sequences.

## Interpretation

The D69/R76/H126 pattern in O67940 is notable because these residues correspond directly to the experimentally grounded D68/R75/H127 positions in PH0463/O58212.

This is stronger evidence than an unguided motif comparison because the positions were defined from an independently audited experimental anchor and then mapped through a frozen alignment. It nevertheless remains positional sequence evidence. Conservation of the three residue identities does not demonstrate that O67940 recreates the same three-dimensional interaction network or performs the same biochemical reaction.

The two positions emphasized historically in the SalL/FDAS comparison also require a more cautious interpretation than a simple chlorinase-versus-fluorinase classification.

At the Y70/T75-related position, O67940 contains V67 and therefore matches neither wild-type SalL Y70 nor FDAS T75.

At the G131/S158-related position, O67940 G127 matches SalL G131 rather than FDAS S158. This remains evidence against direct transfer of an FDAS-like residue pattern. However, the earlier reviewed-reference analysis also showed glycine at this homologous position in the broader SAM-hydrolase context. G127 should therefore not be treated as uniquely diagnostic of SalL-like chlorinase activity.

The broader experimentally anchored comparison changes the evidential meaning of G127 without invalidating the earlier observation. The residue still differs from the FDAS serine state, but its presence is not sufficient to distinguish SalL-like halogenase chemistry from other related SAM-dependent functions.

Taken together, the current sequence evidence introduces a meaningful HAT-like mechanistic context and weakens a simple direct fluorinase-specific interpretation. It does not establish that O67940 is a HAT enzyme, a chlorinase, or another substrate-specific SAM-dependent enzyme.

## Relationship to the earlier residue analysis

The earlier reviewed-reference residue analysis identified G127 as the strongest local signal against a direct fluorinase-specific interpretation and concluded that the remaining active-site pattern was mixed.

That conclusion is retained as the historical interpretation of the evidence available at that stage.

The present analysis adds independently audited functional anchors and a prospectively frozen 12-taxon biological alignment. It therefore refines the interpretation rather than replacing the earlier result.

In particular, G127 is now treated as less functionally discriminating than it appeared in the earlier chlorinase/fluorinase-centered comparison, while the O58212-derived D/R/H positions introduce an additional experimentally grounded mechanistic context that was not represented in the original two-enzyme comparison.

## Reproducibility

The primary G-INS-i alignment was regenerated from the frozen 12-sequence input using the recorded MAFFT 7.525 command and produced a byte-identical output.

Primary alignment SHA256:

`73244b71e955a0fe71e56aa8e94b0898783f50b163256e55e6c40bd7ffc3cef7`

The deterministic landmark mapper was also rerun against the frozen alignment and landmark registry and regenerated a byte-identical mapping table.

Mapper SHA256:

`2194263c61cd6f1be8b3939be84907d61df08c38b0587e17d7705a6848ae6708`

Mapping-table SHA256:

`ddc62b066e4abf6a122cb0c4fe02b9cb3296748091f6f50cef3bce43fe017992`

These checks establish deterministic reconstruction in the recorded software environment. They do not establish that the chosen alignment strategy is uniquely correct biologically.

## Limitations and next test

The current result depends on the primary G-INS-i alignment.

E-INS-i was predefined before final analysis as an alignment-method sensitivity test because several proteins contain localized longer gap regions and the family has a multi-domain context. That sensitivity analysis is therefore required before treating the exact positional correspondences as robust to alignment strategy.

Structural mapping also remains necessary. Sequence correspondence alone cannot show that the homologous residues occupy equivalent three-dimensional geometry, participate in the same interaction network, or confer the same substrate specificity.

The current evidence should therefore be described as an experimentally anchored sequence-level mechanistic comparison, not as biochemical validation of O67940 function.
