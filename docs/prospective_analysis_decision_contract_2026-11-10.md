# Prospective analysis and decision contract

Frozen prospectively: 2026-11-10

## Purpose

This document defines the decision rules for the remaining O67940 publication-upgrade analyses before the SalL and fluorinase functional-anchor audits and before the final evolutionary and mechanistic analyses are run.

This is not a preregistration. Several exploratory and historical observations are already known. The purpose is to separate those known observations from the rules that will govern the remaining analyses, so that later analytical choices are not adjusted to favour a preferred interpretation.

The central question remains:

> How has the evidential basis for functional annotation of O67940 changed since its 2008 structure-guided analysis, what functional annotation can contemporary computational evidence support, and where does experimental validation remain necessary?

The main biological comparison is:

> Is O67940 better supported as a SAM hydroxide adenosyltransferase/hydrolase, a SAM-dependent halogenase, or an unresolved member of their shared DUF62-related structural/evolutionary landscape?

Exact halogen specificity will only be considered if the broader halogenase interpretation remains supported.

---

## 1. Observations already known before this contract

The following results already exist and must not be presented as prospectively predicted results.

- The 2008 study interpreted O67940 as a probable SAM-utilizing halogenase and considered it closer to SalL than to the fluorinase, while explicitly stopping short of assigning exact substrate specificity.
- Current UniProt still leaves O67940 experimentally unresolved.
- The post-2008 annotation audit recovered no direct biochemical characterization of O67940 or a sequence-identical alias in the audited resources.
- AlphaFold predicts a high-confidence O67940 monomeric structure.
- TM-align shows strong protomer-level fold similarity to both the SalL-related and fluorinase structural references.
- The historical 2Q6O structure is a SalL Y70T mutant and must not be treated as wild-type SalL active-site geometry.
- O67940 contains the historical Val67/Gly127 configuration discussed in the earlier analysis.
- G127 alone is not sufficient evidence for chlorinase activity.
- Several reviewed hydrolase-like candidate proteins have greater full-sequence similarity to O67940 than the SalL and fluorinase references.
- The exploratory reviewed-reference FastTree places O67940 near the O58212/RSAMH_PYRHO region, but this tree is exploratory and is not the final evolutionary result.
- The operational broader family universe currently contains 4,432 proteins after the predefined Pfam, length and fragment filters.
- MMseqs2 redundancy reductions at 90% and 80% identity have already been generated.
- Protein-name searches within the broader universe show substantial overlap between "fluorinase" and "chlorinase" labels, demonstrating that database names cannot be treated as experimentally validated functional classes.
- O58212/PH0463 has now been audited and classified as a `direct_functional_anchor` for SAM hydroxide adenosyltransferase / SAM-hydrolysing chemistry.

These observations may motivate the remaining analyses but must not determine their decision rules retrospectively.

---

## 2. Functional-anchor classification rules

Each reviewed candidate will be assigned one primary audit status.

Anchor classifications are claim-specific. A candidate classified as a
`direct_functional_anchor` is a direct anchor only for the biochemical
activity or mechanistic claim supported by the audited experiment. The
classification does not imply that every database annotation, substrate
specificity, mechanistic detail or biological role assigned to that protein
has been experimentally validated.

Where more than one evidence type applies, the primary status will be assigned
using the following evidential precedence:

`direct_functional_anchor`
> `partial_experimental_anchor`
> `structural_anchor_only`
> `annotation_supported_candidate`
> `not_validated`

`unresolved` overrides this ordering when conflicting evidence, unresolved
identity or construct ambiguity prevents a defensible classification.

This ordering is used only to assign the candidate-level audit status.
Individual evidence records retain their own evidence type, direction and
limitations.

### `direct_functional_anchor`

Requires:

1. the experimentally studied protein to be linked to the candidate by exact sequence identity or an explicitly resolved construct-to-canonical sequence relationship; and
2. direct biochemical evidence measuring the relevant reaction, substrate conversion or reaction product.

Terminal tags, cleavage products or other recombinant modifications do not automatically disqualify an anchor, but the construct relationship must be documented.

Structural evidence, database annotation or homology alone is insufficient.

### `partial_experimental_anchor`

Used when the exact candidate has experimental functional evidence, but the evidence is insufficient to establish the specific biochemical activity required for a direct functional anchor.

Examples may include incomplete substrate testing, indirect activity evidence or experimental results that establish only part of the relevant function.

### `structural_anchor_only`

Used when the candidate identity is established and an experimental structure exists, but direct biochemical evidence is absent or insufficient for functional classification.

### `annotation_supported_candidate`

Used when the candidate is supported primarily by curated database annotation, sequence similarity or literature-based annotation propagation without sufficient direct experimental evidence on the exact candidate.

### `not_validated`

Used when the defined audit does not recover sufficient evidence for any of
the higher audit statuses for the claimed function.

This means "not validated within the audited evidence", not "experimentally
disproven".

### `unresolved`

Used when identity, construct history or experimental evidence is conflicting or ambiguous enough that a more specific classification would be misleading.

---

## 3. Evidence hierarchy

Evidence will not be counted as independent merely because it comes from different tools.

The main evidence domains are:

1. direct biochemical evidence;
2. mutagenesis or isotope-labelling evidence;
3. experimental structural evidence;
4. evolutionary/sequence evidence;
5. computational structural evidence;
6. database annotation/history.

Multiple methods measuring essentially the same property will be treated as related evidence rather than independent confirmation.

Evidence from a homolog must remain explicitly separated from evidence obtained on the exact candidate.

---

## 4. Final reference-set rules

The final comparative dataset will distinguish between:

### Functional anchors

Only proteins classified as `direct_functional_anchor` will define the
primary experimentally grounded functional classes used for interpretation
of O67940.

Proteins classified as `partial_experimental_anchor` may remain in the
comparative dataset as context or sensitivity references, but they will not
define a primary functional class or be treated as functional ground truth.

### Context sequences

Reviewed candidates that do not meet functional-anchor criteria may remain in the evolutionary analysis for sequence context, but they will not be used as ground truth for functional clade assignment.

### Historical structural references

2Q6O and 1RQP will remain historical references because they were central to the 2008 analysis.

They will not be counted as independent functional anchors when they correspond to the same underlying biological proteins represented elsewhere by audited canonical sequences.

Mutant structures will be explicitly distinguished from wild-type proteins.

### Exclusion

A sequence will be excluded from the primary reference set if:

- its identity cannot be resolved;
- it is a duplicate representation of the same biological protein without a specific analytical reason;
- sequence quality or coverage makes homologous comparison unreliable;
- or its inclusion would incorrectly imply experimentally validated function.

All exclusions will be recorded.

---

## 5. Functional-anchor audit scope

The minimum deep-audit set is:

1. O58212 / PH0463 — hydrolase/HAT anchor — completed;
2. A4X3Q0 / SalL — non-fluorinating halogenase candidate;
3. Q70GK9 / Streptomyces cattleya fluorinase — fluorinase candidate.

The remaining reviewed candidates will be audited sufficiently to determine whether they provide additional independent experimental anchors.

A candidate does not require the same depth of documentation as the three core anchors if available evidence clearly establishes that it is annotation-supported only or redundant with an already validated anchor.

For the primary comparison, the target is at least one
`direct_functional_anchor` for each functional class required by the
biological question:

- SAM hydroxide adenosyltransferase / SAM-hydrolysing chemistry;
- SalL-like non-fluorinating halogenase chemistry;
- fluorinase chemistry.

If a direct anchor cannot be established for one of these classes after the
defined candidate audit, that absence will be reported explicitly. A weaker
candidate class will not be promoted to `direct_functional_anchor` merely to
complete the comparison.

Additional reviewed candidates will be audited only when they could add an
independent experimental anchor, resolve an important ambiguity, or provide
a prespecified sensitivity reference.

---

## 6. Primary evolutionary analysis

The existing FastTree analysis remains exploratory.

The final primary tree will use amino-acid sequences and IQ-TREE.
The exact IQ-TREE version used for the final analysis will be pinned and
recorded in the project environment and workflow metadata before execution.

Primary analysis:

- one canonical biological sequence per selected reference protein;
- MAFFT alignment;
- maximum-likelihood inference with IQ-TREE;
- ModelFinder model selection;
- 1,000 ultrafast-bootstrap replicates;
- 1,000 SH-aLRT replicates.

A branch will be described as strongly supported only when both:

- UFBoot >= 95;
- SH-aLRT >= 80.

These thresholds are descriptive support criteria and will not be interpreted as probabilities that a functional hypothesis is true.

The tree will remain unrooted unless a biologically defensible outgroup is identified before interpretation.

Midpoint rooting will not be used to imply evolutionary direction.

---

## 7. Evolutionary sensitivity analyses

The final interpretation must not depend on one arbitrary alignment or reference-set choice.

At minimum, sensitivity will examine:

1. the primary reference set;
2. a version excluding annotation-supported/context-only candidates;
3. an alignment-trimming sensitivity analysis.

The trimming method and version will be frozen before the final tree is executed and will not be selected according to which result produces the preferred topology.

Structure-based alignment may be used as a mapping or sensitivity analysis where comparable structural information exists.

A structure-derived alignment will not automatically replace the sequence alignment used for the primary phylogenetic inference.

---

## 8. Topology testing

An approximately unbiased (AU) topology test will only be performed if, after the anchor audit, there are biologically defensible alternative placement hypotheses that can be expressed as meaningful constraints.

Possible hypotheses include placement of O67940 with experimentally grounded hydrolase/HAT references versus experimentally grounded halogenase references.

AU testing will not be performed merely because the software permits it.

A rejected topology will be interpreted as incompatibility with the sequence alignment under the tested model, not as biochemical proof of function.

---

## 9. Mechanistic residue mapping

Residues will be mapped by homologous and, where possible, structural equivalence rather than by copying residue numbers between proteins.

The primary mechanistic comparison will include:

- the experimentally supported hydrolase/HAT water-activation network;
- corresponding positions in O67940;
- corresponding positions in audited halogenase anchors.

No single residue will be treated as sufficient to assign biochemical function.

In particular:

- O67940 Gly127 will not be treated as a standalone chlorinase marker;
- conservation of a hydrolase-associated residue will not by itself prove hydrolase activity;
- absence of one canonical residue will not automatically exclude a functional class.

Each residue-level claim must state whether its experimental basis comes from the exact protein or from a homolog.

---

## 10. Mechanistic interpretation categories

The mechanistic configuration of O67940 may be described as:

- hydrolase/HAT-compatible;
- halogenase-compatible;
- mixed;
- non-diagnostic.

These descriptions refer to compatibility with experimentally grounded residue configurations and do not themselves constitute biochemical function assignments.

---

## 11. Integration rules

The final functional interpretation will not be based on majority voting across tools.

A strong biological reinterpretation requires convergence between at least:

- evolutionary placement; and
- mechanistically relevant residue/structural evidence.

Direct biochemical evidence remains unavailable for O67940 and therefore any computational functional assignment must remain explicitly inferential.

If evolutionary and mechanistic evidence disagree, or either remains weak/non-diagnostic, the result will be classified as unresolved or mixed rather than forcing a functional label.

---

## 12. Historical verdict scale

Relative to the 2008 interpretation, the final evidence will be classified as one of:

### Strengthened

The broad 2008 functional interpretation remains supported and gains substantial independent modern evidence.

### Refined

The broad interpretation survives, but modern evidence materially narrows, changes or qualifies the proposed mechanism or specificity.

### Weakened

Important evidence used in the original interpretation is now shown to be non-specific, incomplete or less reliable, while available evidence does not clearly establish an incompatible function.

### Contradicted

Multiple independent and mechanistically relevant evidence layers support a functional interpretation incompatible with the central 2008 conclusion.

### Unresolved

The modern evidence is insufficient or conflicting, preventing a defensible choice among the competing functional interpretations.

---

## 13. Early publication-value checkpoint

The first publication-value checkpoint will occur after:

1. completion of the functional-anchor audit;
2. freezing of the final reference set;
3. final evolutionary analysis;
4. mechanistic residue mapping.

At that point the project will be assigned one of three directions.

### A. Biological reinterpretation

Used if evolutionary and mechanistic evidence converge on a materially different or substantially stronger biological interpretation of O67940.

### B. Longitudinal/reproducibility study

Used if the exact biochemical function remains unresolved but the project demonstrates a substantive change in annotation context, evidential standards or reproducibility relative to the 2008 analysis.

### C. Insufficient additional contribution

Used if neither the biological reinterpretation nor the longitudinal/reproducibility evidence provides a sufficiently substantive contribution.

This checkpoint occurs before additional expensive supporting analyses.

---

## 14. Conditional analyses after the checkpoint

The following analyses are not automatically required:

- pocket-level halogen specificity analysis;
- DALI structural-neighbour search;
- quaternary/interface compatibility analysis;
- broader 4,432-protein mechanistic-residue landscape.

They will be performed only when they answer a specific unresolved question or materially strengthen the main interpretation.

### Pocket specificity

Only pursued if the broader halogenase interpretation remains plausible.

### DALI

Used as independent structural-neighbour context, not as functional proof.

### Interface analysis

May test whether O67940 is geometrically compatible with experimentally observed interface architectures.

It cannot establish O67940 oligomeric state.

The 2008 study already considered interface-associated active sites, so interface analysis will not be presented as a capability unavailable to the original study.

### Broader family analysis

May test how mechanistically important residue states are distributed across the frozen operational family universe.

Database protein names may be overlaid descriptively but will not be treated as experimentally validated mechanistic classes.

The 90% identity reduction will be the primary redundancy-controlled representation and the 80% reduction will be used as a sensitivity analysis unless evidence obtained before running the residue analysis justifies a documented change.

---

## 15. Stop conditions and scope control

No additional method will be introduced solely because it is modern, available or potentially publishable.

Docking, molecular dynamics, protein language models, AlphaFold-Multimer and additional machine-learning analyses are outside the current core plan unless a specific unresolved question cannot be addressed adequately by the predefined analyses.

Every remaining method must answer a stated research question and must have a defined interpretation boundary before it is run.

The project should become narrower from this point onward, not broader.

---

## 16. Required evidence chain

For every remaining analysis:

source/input
→ script/tool
→ output
→ evidence
→ interpretation
→ limitation

External source provenance will continue to be recorded in:

`metadata/source_provenance.tsv`

Integrity-relevant files will continue to be tracked with:

`metadata/checksums_sha256.txt`

Chronological milestones will be recorded concisely in:

`notes/workflow_log.md`

Detailed scientific reasoning belongs in the relevant strategy, interpretation or decision document rather than being duplicated into the workflow log.
