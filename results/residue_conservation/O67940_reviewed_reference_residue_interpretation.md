# Reviewed-reference residue interpretation

## Purpose

This note summarizes what the reviewed-reference residue mapping adds to the O67940_AQUAE annotation question.

It is based on:

- `results/residue_conservation/O67940_reviewed_reference_functional_residue_matrix.tsv`
- `results/residue_conservation/O67940_reviewed_reference_residue_pattern_summary.tsv`

The aim is not to prove function. The aim is to record what the residue-level evidence supports and what it does not support.

## Main observations

Several focal residues are strongly conserved across the reviewed-reference set.

These include:

- O67940 D8
- O67940 D177
- O67940 N181
- O67940 S221

This supports that the alignment is capturing a real conserved SAM-related functional-site context.

The clearest specificity-relevant signal is at O67940 G127.

At this position:

- O67940 has G
- 2Q6O has G
- SalL has G
- the SAM hydrolase group has G as the major pattern
- 1RQP has S
- the fluorinase group has S as the major pattern

This is the strongest local residue-level evidence against a direct fluorinase-specific interpretation.

## Mixed active-site pattern

The residue pattern is not simply chlorinase-like across all positions.

For example:

- O67940 V67 matches the SAM hydrolase-major pattern, while 2Q6O, 1RQP, and the fluorinases carry T, and SalL carries Y.
- O67940 D69 matches the SAM hydrolase-major pattern, while 2Q6O, 1RQP, SalL, and the fluorinases carry Y.
- O67940 F15, F222, and V231 do not match the selected major reference patterns.
- O67940 V229 matches the SAM hydrolase-major pattern, but not 2Q6O, 1RQP, SalL, or the fluorinase-major pattern.

So the residue evidence is supportive, but not decisive.

## Interpretation

The reviewed-reference residue layer supports a SAM-related homologous context.

The G127 pattern is the strongest specificity-relevant result. At this site, O67940 is closer to the 2Q6O/SalL/SAM-hydrolase-like pattern than to the 1RQP/fluorinase pattern.

This strengthens the argument that O67940 should not be annotated directly as a fluorinase based on the current evidence.

However, the broader active-site pattern remains mixed. The data do not justify a definitive chlorinase or substrate-specific claim.

## Current conclusion

The safest interpretation is:

O67940_AQUAE remains best described as a SAM-related protein with halogenase/SAM-hydrolase-family context. The residue-level evidence supports a cautious chlorinase/SAM-hydrolase-related signal at G127, but biochemical validation would still be needed to assign enzyme activity or substrate specificity.
