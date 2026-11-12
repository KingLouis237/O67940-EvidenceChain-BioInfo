# Final alignment-method sensitivity decision — E-INS-i

## Purpose

The primary evolutionary alignment for the final 12-taxon O67940 analysis was prospectively defined as MAFFT G-INS-i before the final alignment was generated.

E-INS-i was also predefined at that stage as an alignment-method sensitivity analysis because several proteins contain localized longer gap regions and the family has a multi-domain context.

This sensitivity analysis is not intended to identify an alignment that produces a preferred biological interpretation. Its purpose is to test whether the mechanistic positional correspondences obtained from the primary G-INS-i alignment remain stable when a different MAFFT alignment model is applied to exactly the same biological input.

## Frozen input

The E-INS-i analysis will use exactly the same canonical 12-sequence FASTA used for the primary G-INS-i alignment:

`results/phylogeny/O67940_final_reviewed_reference_set.fasta`

SHA256:

`7ced3945ae2d6c334c7dd6d92b4127dc8b1133d7ad3afb22710ca859af57583f`

No taxa will be added, removed or reordered for the sensitivity analysis.

The alignment will be analysed untrimmed, matching the primary G-INS-i design.

## Sensitivity alignment strategy

MAFFT version 7.525 will be used.

The E-INS-i command will use:

`--genafpair --maxiterate 1000 --thread -1 --threadit 0`

E-INS-i differs from the primary G-INS-i strategy by using generalized affine-gap pairwise alignment information rather than global pairwise alignment information.

The iterative-refinement stage will remain single-threaded through `--threadit 0` so that deterministic rerunning can be tested in the same way as for the primary alignment.

## Frozen mechanistic landmarks

The sensitivity analysis will use exactly the same seven experimentally grounded landmarks already defined for the primary analysis:

`results/residue_mapping/O67940_final_mechanistic_landmark_registry.tsv`

Registry SHA256:

`79f1eb43e93e948f7f3c84a62981a7ec2e2b0b154eb460ab56638ff6edb0d02c`

No landmark will be added, removed or redefined after inspecting the E-INS-i result.

The same mapping logic will be used for the sensitivity alignment.

## Primary robustness criterion

The primary question is whether each experimentally anchored residue maps to the same O67940 residue identity and O67940 residue number under E-INS-i as under the primary G-INS-i alignment.

The predefined G-INS-i correspondences are:

O58212 D68 → O67940 D69

O58212 R75 → O67940 R76

O58212 H127 → O67940 H126

A4X3Q0 Y70 → O67940 V67

A4X3Q0 G131 → O67940 G127

Q70GK9 T75 → O67940 V67

Q70GK9 S158 → O67940 G127

If all seven O67940 residue correspondences are unchanged under E-INS-i, the O67940 mechanistic-landmark mapping will be considered robust to the predefined alignment-method sensitivity test.

If one or more correspondences change, those positions will be classified as alignment-method sensitive and reported explicitly. The primary G-INS-i alignment will not be replaced simply because one method gives a more attractive biological interpretation.

## Secondary sensitivity measures

Absolute alignment-column numbers will be compared but will not be used as the primary robustness criterion. Different alignment algorithms can shift column numbering while preserving the same biological residue correspondence.

For every landmark, the analysis will also compare the mapped residue identity and residue number across all 12 biological sequences. This produces up to 84 pairwise mapping comparisons between the G-INS-i and E-INS-i results.

The number and identity of stable versus changed mappings will be recorded.

Column occupancy at each landmark will also be recorded for both alignments. Changes in occupancy will be treated as evidence about local alignment sensitivity rather than automatically as failure of the O67940 mapping.

Anchor self-mapping must remain internally valid: each predefined anchor residue must map back to its expected residue identity and residue number in its own sequence.

## Interpretation rule

A stable O67940 residue correspondence across G-INS-i and E-INS-i supports robustness of the positional sequence evidence to these two predefined alignment strategies.

It does not establish that either alignment is uniquely correct, that the mapped residues have equivalent three-dimensional geometry, or that O67940 shares catalytic activity or substrate specificity with the experimental anchors.

If the two alignment strategies disagree at a focal position, the disagreement will be retained as uncertainty rather than resolved by selecting whichever result better supports a preferred functional interpretation.

## Expected outputs

The sensitivity analysis should produce a separate E-INS-i alignment, execution records, an E-INS-i mechanistic mapping table, and a direct G-INS-i versus E-INS-i comparison table.

The primary G-INS-i alignment and mapping outputs remain frozen and will not be overwritten.

## Stop condition

This sensitivity layer is complete once the E-INS-i alignment has been generated and reproducibility-checked, the same seven landmarks have been mapped through it, the O67940 and broader reference-set correspondences have been compared with the frozen G-INS-i results, and the resulting sensitivity has been interpreted without changing the predefined primary alignment or landmark definitions.

No additional alignment strategy will be introduced by default unless this comparison exposes a specific unresolved methodological ambiguity that cannot be interpreted from the two prospectively defined methods.
