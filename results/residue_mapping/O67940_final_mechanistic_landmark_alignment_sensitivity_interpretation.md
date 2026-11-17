# Final G-INS-i versus E-INS-i mechanistic-landmark sensitivity interpretation

## Purpose

The final mechanistic-landmark analysis used MAFFT G-INS-i as the prospectively defined primary alignment strategy.

E-INS-i was predefined before sensitivity execution as an alternative alignment model because several proteins in the final 12-taxon reference set contain localized longer gap regions and the broader family has multi-domain sequence context.

The purpose of this analysis was therefore not to select whichever alignment produced a preferred functional interpretation. It was to test whether the experimentally anchored positional correspondences used in the O67940 analysis remain stable under the predefined change in alignment strategy.

## Frozen analysis design

The sensitivity test used exactly the same canonical 12-sequence biological input as the primary analysis:

`results/phylogeny/O67940_final_reviewed_reference_set.fasta`

The same seven experimentally grounded mechanistic landmarks were retained without modification:

`results/residue_mapping/O67940_final_mechanistic_landmark_registry.tsv`

The same mechanistic-landmark mapping implementation was used for both alignments after its input and output paths were parameterized and regression-tested against the frozen G-INS-i result.

The primary robustness criterion was defined before E-INS-i execution: all seven experimentally anchored positions had to map to the same O67940 residue identity and residue number under both alignment strategies.

Changes in absolute alignment-column number or broader reference-set mapping were recorded separately and were not allowed to redefine the primary criterion after inspection of the result.

## E-INS-i alignment

The E-INS-i alignment was generated with MAFFT 7.525 using:

`--genafpair --maxiterate 1000 --thread -1 --threadit 0`

The canonical input SHA256 was:

`7ced3945ae2d6c334c7dd6d92b4127dc8b1133d7ad3afb22710ca859af57583f`

The resulting E-INS-i alignment SHA256 was:

`f6df74873c0649dae339e194461f99335847835981d74bc34c1785f22afa6d9a`

The alignment retained all 12 expected taxa in canonical input order. Removing gaps from every aligned sequence reconstructed the corresponding frozen source sequence exactly.

An independent MAFFT rerun generated a byte-identical E-INS-i alignment.

## Global alignment difference

The E-INS-i alignment is not globally identical to the primary G-INS-i alignment.

The primary G-INS-i alignment has width 329, whereas the E-INS-i alignment has width 333.

A residue-column diagnostic across the same 12 biological sequences compared 3,325 ungapped residue positions and found that 960 residues occupy different absolute alignment columns between the two strategies.

For O67940, 73 of 251 residues changed absolute alignment-column placement.

This establishes that the sensitivity analysis involved a meaningful change in global alignment geometry rather than simply reproducing the primary alignment.

The global residue-column diagnostic is reproduced in:

`results/phylogeny/O67940_final_ginsi_vs_einsi_residue_column_shift_summary.tsv`

using:

`scripts/05_evolutionary_active_site_context/compare_alignment_residue_columns.py`

The 960/3,325 result is supporting diagnostic evidence generated during the sensitivity audit rather than part of the predefined primary robustness criterion.

## Mechanistic-landmark result

Despite the global alignment differences, all seven experimentally anchored O67940 residue correspondences were unchanged.

The mappings remained:

- O58212 D68 → O67940 D69
- O58212 R75 → O67940 R76
- O58212 H127 → O67940 H126
- SalL Y70 → O67940 V67
- SalL G131 → O67940 G127
- FDAS T75 → O67940 V67
- FDAS S158 → O67940 G127

All seven focal columns retained 12/12 occupancy.

At these focal positions, the absolute alignment-column numbers were also unchanged between the two strategies.

The predefined primary sensitivity criterion therefore passed:

`7/7 O67940 mechanistic-landmark correspondences stable`

## Broader 12-taxon mapping

The comparison was also extended across all seven landmarks and all 12 sequences, producing 84 landmark-by-sequence comparisons.

All 84 residue correspondences were unchanged:

`84/84 stable residue correspondences`

No mechanistic-landmark correspondence changed between G-INS-i and E-INS-i.

The complete E-INS-i mapping table has SHA256:

`ddc62b066e4abf6a122cb0c4fe02b9cb3296748091f6f50cef3bce43fe017992`

This is identical to the SHA256 of the previously frozen G-INS-i mapping table. The two complete mechanistic-landmark mapping tables are therefore byte-identical despite the global differences between the underlying alignments.

## Reproducibility

The E-INS-i mechanistic mapping was regenerated independently and reproduced byte-for-byte.

The G-INS-i versus E-INS-i comparison table was also regenerated and reproduced byte-for-byte.

Comparison-table SHA256:

`396530b1b75fb96f78a026518e13b5c9a77cefe09fbde12ab8bbadc86d716635`

Sensitivity-summary SHA256:

`4104f7d202d203a2ddb3810e0a4d7cf8b019bc33c09ec5a9598dc5952ccb8d3e`

Comparator-script SHA256:

`37b8e34a02950ad037dcf543b5abb55b3e5f9441638f7d16e2be88c0e414b494`

The comparator implementation itself was written after the E-INS-i alignment had been generated. The comparison criteria, however, had already been defined and committed before E-INS-i execution. In addition, the principal result does not depend solely on the comparator because the complete G-INS-i and E-INS-i mapping tables are independently byte-identical.

## Interpretation

The experimentally anchored O67940 positional correspondences are robust to the prospectively specified G-INS-i versus E-INS-i alignment-method sensitivity test.

This is meaningful because the two methods produced different global alignment geometry while retaining exactly the same mechanistic-landmark mappings.

The sensitivity result strengthens confidence that the O67940 D69/R76/H126, V67 and G127 correspondences are not artifacts of the specific primary G-INS-i alignment strategy tested here.

It does not establish that the alignments are equivalent globally, that either alignment is uniquely biologically correct, or that these correspondences would remain invariant under every possible alignment method.

Most importantly, alignment robustness does not convert positional sequence correspondence into biochemical evidence. The result does not demonstrate that O67940 is a HAT enzyme, a chlorinase, a fluorinase, or another substrate-specific SAM-dependent enzyme.

## Relationship to the mechanistic interpretation

The earlier mechanistic analysis concluded that O67940 contains D69/R76/H126 at positions corresponding to the experimentally grounded O58212/PH0463 D68/R75/H127 network, while its V67/G127 pattern does not support direct transfer of an FDAS-like residue pattern.

The present sensitivity analysis does not change that interpretation.

Instead, it strengthens one methodological component of it: the relevant positional correspondences remain unchanged when the predefined alternative alignment strategy is used.

The appropriate sequence-level interpretation therefore remains that O67940 contains experimentally anchored HAT-related positional context and lacks a direct FDAS-like residue pattern at the tested specificity-related sites, while functional assignment still requires independent structural and biochemical evidence.

## Remaining limitation and next evidence layer

This analysis resolves the predefined alignment-method sensitivity question for the current mechanistic landmarks.

It does not test whether the corresponding residues occupy equivalent three-dimensional positions or reproduce the same interaction networks in O67940.

The next independent evidence layer should therefore be structural mapping of the experimentally grounded landmarks rather than additional alignment-method searching.

Additional alignment strategies should not be introduced by default unless a later analysis reveals a specific unresolved alignment ambiguity.
