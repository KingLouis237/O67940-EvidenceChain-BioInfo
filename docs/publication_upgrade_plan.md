# Publication upgrade plan

This branch extends the original O67940_AQUAE course/report-level re-analysis.

The goal is not to prove enzyme activity. The goal is to make the annotation-transfer argument more careful by adding the evidence layers that were still missing: broader homolog context, phylogenetic placement, residue conservation, and active-site/interface context.

## Why this upgrade is needed

The first report already had useful evidence:

- current UniProt/InterPro annotation status;
- AlphaFold model confidence;
- structural comparison to 2Q6O and 1RQP;
- three-sequence MAFFT alignment;
- mapped functional residues.

The weak point is that the comparison is still narrow. A reviewer can fairly ask:

- Is O67940 sitting in a broader 2Q6O-like/chlorinase-related neighborhood?
- Is it closer to 1RQP-like/fluorinase-related proteins?
- Or is the signal mixed and not specific enough?

That is why the next phase adds broader evolutionary and active-site context.

## Planned evidence layers

1. Homolog search

Question:
What broader set of detectable homologs is recovered around O67940_AQUAE?

Expected outputs:
- raw JackHMMER output;
- parseable hit table;
- candidate homolog FASTA;
- curation table.

Can support:
O67940 belongs to a broader detectable homolog family.

Cannot prove:
substrate specificity or enzyme activity.

2. Homolog curation

Question:
Which hits are useful enough for alignment/tree/residue interpretation?

Expected outputs:
- inclusion/exclusion table;
- final curated homolog FASTA.

Can support:
a transparent analysis set.

Cannot prove:
that excluded sequences are biologically irrelevant.

3. Multiple sequence alignment and tree

Question:
Where does O67940 sit relative to relevant homologs and references?

Expected outputs:
- MSA;
- alignment statistics;
- tree file;
- tree figure.

Can support:
relative placement in the sampled homolog space.

Cannot prove:
exact function or substrate specificity.

4. Residue conservation

Question:
Do the mapped O67940 residues follow a pattern closer to 2Q6O-like or 1RQP-like references?

Expected outputs:
- residue conservation table;
- focused residue-pattern summary;
- figure if useful.

Can support:
local residue-pattern consistency.

Cannot prove:
activity or substrate preference by itself.

5. Active-site and interface context

Question:
Are the important residues spatially sensible, and does interface context affect interpretation?

Expected outputs:
- structural superposition notes;
- active-site figure;
- pocket/interface tables if useful.

Can support:
structural plausibility and better caution.

Cannot prove:
ligand binding, catalytic activity, or biological oligomeric state.

## Claim boundaries

Allowed wording:

- supports a SAM-dependent halogenase-related interpretation;
- is consistent with a chlorinase-related pattern;
- leans closer to the 2Q6O-associated residue pattern;
- still requires biochemical validation.

Forbidden wording:

- proves O67940 is a chlorinase;
- confirms substrate specificity;
- demonstrates enzyme activity;
- validates chlorination;
- rules out fluorination completely.

## Working standard

For each major step, record:

- why the step was needed;
- input used;
- command or script used;
- output files generated;
- what the output supports;
- what it does not prove;
- next decision.

Keep the language direct. No inflated claims.
