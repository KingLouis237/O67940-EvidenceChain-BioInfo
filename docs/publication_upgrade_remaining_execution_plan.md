# O67940 publication upgrade — remaining execution plan

## Purpose

This document is the canonical guide for the remaining publication-upgrade work.

The project asks what modern sequence, structural and evolutionary evidence supports about O67940_AQUAE.

The goal is not to reproduce a preferred functional annotation.

For every remaining evidence layer, preserve:

source/input → method → output → validation → evidence → interpretation → limitation → decision.

A new method should be introduced only when a defined unresolved question requires it.

---

## Current checkpoint

Completed evidence layers include:

- current O67940 sequence and UniProt context;
- InterPro/Pfam domain context;
- AlphaFold structure/confidence;
- TM-align comparisons with 2Q6O and 1RQP;
- initial three-sequence residue mapping;
- eleven reviewed Swiss-Prot functional/reference homologs;
- reviewed-reference MAFFT and exploratory FastTree context;
- broader PF01887/PF20257 UniProt candidate universe;
- frozen 4432-sequence candidate dataset;
- protein-name overlap audit;
- PHMMER ranking and diagnostics;
- audit of ten records outside Bacteria and Archaea;
- MMseqs2 redundancy sensitivity analysis.

The selected first redundancy level is:

90% sequence identity + 80% bidirectional coverage

giving:

2858 clusters from 4432 candidate records.

O67940 and all eleven reviewed anchors remain in separate clusters at this threshold.

---

# Remaining execution order

## Step 1 — bounded DALI structural-neighbour search

### Structural level

This step is a protomer-level tertiary-structure search.

The 251-residue O67940 AlphaFold monomer will be used as the query only after its PDB sequence, chain composition, residue numbering, provenance, and checksum have been validated. DALI results are interpreted as structural-neighbour evidence for protomer/domain-level tertiary structure, not as evidence of conserved quaternary organization.

### Question

What experimentally determined protein structures are independently recovered as close protomer/domain-level structural neighbours of the O67940 AlphaFold model?

### Why

TM-align quantified similarity to the already selected 2Q6O and 1RQP structures.

It did not independently search structural space.

DALI therefore addresses the previously incomplete structural-neighbour-search layer.

### Required work

- validate the exact O67940 query structure;
- record its checksum;
- submit a bounded PDB-focused DALI search;
- save the raw result;
- parse meaningful high-ranking structural neighbours;
- independently verify biological annotation of relevant hits;
- map relevant PDB hits to UniProt sequences and existing 90% clusters.

### Decision rule

A DALI hit does not automatically become a functional or phylogenetic anchor.

New anchors require independent evidence such as experimental characterization and compatible sequence/domain context.

### Stop condition

Stop after the meaningful characterized structural neighbourhood has been audited and the structural-anchor list is frozen.

### Cannot prove

DALI cannot establish exact activity, substrate specificity, oligomeric state or orthology.

---

## Step 2 — build the 2858-cluster master evidence table

### Question

What biological and sequence evidence is associated with every 90%-identity cluster?

### Integrate

For each cluster record:

- MMseqs representative;
- cluster size;
- member accessions;
- best PHMMER rank/score;
- PHMMER coverage;
- organism/taxonomy;
- reviewed state;
- protein name as metadata only;
- O67940 flag;
- reviewed-anchor flag;
- validated structural-anchor flag;
- non-prokaryotic-audit flag.

### Validation

- exactly 2858 cluster rows;
- every original candidate maps to one cluster;
- all reviewed/structural anchors are recoverable;
- no duplicate cluster IDs.

### Stop condition

Do not perform representative selection until the integrated table passes QC.

---

## Step 3 — freeze representative-selection logic

### Working hierarchy

For each 90% cluster:

1. O67940 cluster → retain O67940.
2. Cluster containing a verified functional/structural anchor → retain the anchor explicitly.
3. Ordinary unanchored cluster → retain the deterministic MMseqs2 representative.

If a cluster contains more than one independently important characterized sequence, preserve that fact explicitly rather than silently discarding biological information.

PHMMER-best membership will be retained as metadata but will not be the default representative criterion because this would systematically bias representatives toward O67940.

### Output

- representative-selection TSV;
- reason-for-selection column;
- representative FASTA.

### Stop condition

Exactly one canonical ordinary representative per cluster, with explicitly retained anchors handled reproducibly.

---

## Step 4 — evaluate the full 2858-representative dataset

Do not assume that 2858 sequences require downsampling.

First test the full dataset.

### Evaluate

- MAFFT feasibility;
- sequence-length distribution;
- alignment length;
- gap behaviour;
- domain comparability;
- anomalous sequences;
- anchor mapping;
- preliminary global residue conservation;
- exploratory tree feasibility.

### Decision gate

Keep the full set if the data are scientifically coherent and computationally tractable.

Introduce additional sampling only if there is a documented problem involving alignment quality, information content, sequence heterogeneity or computational feasibility.

Tree readability alone is not sufficient justification for downsampling.

---

## Step 5 — conditional balanced reduction

Execute only if Step 4 demonstrates that reduction is needed.

Any reduced dataset must preserve:

- O67940;
- reviewed functional anchors;
- validated structural anchors;
- O67940 local sequence context;
- broader sequence diversity;
- taxonomic breadth.

Reject:

- arbitrary top-N PHMMER sampling;
- protein-name-defined functional classes;
- arbitrary equal taxon quotas;
- aesthetic tree-size targets.

The sampling rule and target size must be defined before examining a desired final topology.

---

## Step 6 — freeze and QC the final multiple sequence alignment

Use MAFFT with a strategy appropriate to the final dataset size and divergence.

Record:

- MAFFT version;
- exact command;
- sequence count;
- alignment length;
- sequence gap fractions;
- column gap fractions;
- anchor positions;
- mapping of validated functional residues;
- important insertion/deletion regions.

Do not trim or manually edit the alignment without an explicit, reproducible rule.

Preserve both unmodified and masked/trimmed alignments if masking becomes justified.

---

## Step 7 — preliminary global residue-conservation analysis

Once the final MSA is available, calculate global residue frequencies at previously validated O67940-equivalent positions.

At minimum revisit:

- D8;
- V67;
- D69;
- G127;
- D177;
- N181;
- S221;
- F222;
- L229;
- V231.

This stage does not require a phylogenetic tree.

Its purpose is also to test whether previously interesting residue patterns remain informative in broader sequence space.

If G127 is nearly universal, its specificity value weakens.

If its distribution is structured, that becomes a hypothesis for later tree-aware analysis.

No functional conclusion is fixed at this stage.

---

## Step 8 — exploratory broad tree

Use an efficient method to inspect the large alignment before committing to expensive final inference.

Assess:

- O67940 neighbourhood;
- reviewed-anchor placement;
- structural-anchor placement;
- unusually long branches;
- obvious sequence-quality problems;
- non-prokaryotic candidate behaviour;
- feasibility of final ML analysis.

This is a diagnostic tree, not the final publication phylogeny.

---

## Step 9 — freeze the final phylogenetic input

Using the results of Steps 4–8, decide whether the final inference uses:

- the full representative set; or
- a documented reduced set.

Freeze:

- exact FASTA;
- exact alignment;
- accession list;
- inclusion/exclusion reasons.

No topology-driven post hoc sequence selection.

---

## Step 10 — formal maximum-likelihood phylogeny

At execution time:

- check the current stable/local IQ-TREE implementation;
- record exact version;
- use data-driven amino-acid model selection;
- perform ML inference;
- calculate appropriate branch support;
- record exact commands and logs.

Do not invent an outgroup.

If no defensible outgroup exists, interpret the primary tree as unrooted.

Midpoint rooting, if used for visualization, must be labelled as a display choice and not evidence of evolutionary direction.

### Interpret carefully

The tree may support relative sequence relationships.

It cannot by itself establish:

- orthology;
- enzyme activity;
- substrate specificity;
- horizontal transfer;
- evolutionary direction.

Weakly supported deep relationships remain unresolved.

---

## Step 11 — tree-aware residue analysis

Combine the final MSA with the supported phylogeny.

Ask:

- how are key residues distributed around O67940?
- are patterns associated with reviewed functional-reference neighbourhoods?
- does G127 remain informative?
- are mixed patterns present?
- are relevant relationships adequately supported?

This stage must be allowed to weaken the earlier chlorinase-related interpretation.

Do not label unreviewed clades functionally from UniProt protein names alone.

---

## Step 12 — PyMOL local structural / active-site / interface analysis

### Structural representation hierarchy

The structural representation depends on the biological question.

**Protomer-level tertiary structure**

Use single protein chains/protomers for TM-align, DALI, and equivalent fold-level comparisons.

This level asks whether the underlying tertiary architecture is conserved while keeping quaternary-structure differences separate.

A reference chain will not be treated as representative merely because it is chain A.

**Representative-protomer QC**

Before detailed local analysis, compare equivalent protein copies within the verified 2Q6O and 1RQP biological assemblies.

Check whether protomers are effectively equivalent or whether ligand occupancy, interface environment, mutations, construct differences, missing residues, or conformational differences make one copy non-representative.

If equivalent, retain one documented representative protomer.

If meaningful differences exist, preserve those differences in the analysis.

**Local ligand and active-site structure**

Use ligand-bound experimental reference structures to examine residue equivalence, neighbouring residues, ligand contacts, and pocket geometry.

This level asks whether structurally corresponding positions occupy comparable local chemical environments.

**Quaternary and interface structure**

Use verified biological assemblies of experimental reference structures when examining functional sites formed at monomer interfaces.

Do not equate the crystallographic asymmetric unit with the biological assembly without verification.

O67940 currently has a monomeric AlphaFold prediction. This does not establish its biological oligomeric state.

Superposing O67940 onto a protomer within an experimental oligomer may test geometric compatibility with the reference interface, but cannot demonstrate that O67940 forms the same oligomer.

Use:

- O67940 AlphaFold model;
- 2Q6O experimental structure;
- 1RQP experimental structure;
- any additional validated structural anchor justified by DALI.

Verify:

- chain mapping;
- construct differences;
- mutations;
- missing residues;
- ligand identity;
- residue numbering;
- biological assembly.

Use reproducible PyMOL scripts where possible.

Examine:

- G127 / G131 / S158 structural equivalence;
- V67 and corresponding specificity-region residues;
- D177 / N181 / S221 and other validated SAM-related positions;
- ligand-contact environment;
- local pocket geometry;
- loop differences;
- interface context.

Global RMSD alone is not sufficient evidence of equivalent chemistry.

An AlphaFold monomer cannot prove O67940 forms the same biological oligomer as the experimental references.

---

## Step 13 — integrate the evidence

Construct a final claim/evidence table.

For every biological claim record:

- evidence source;
- evidence strength;
- contradictory evidence;
- limitation;
- confidence.

Maintain three levels:

### Stronger computationally supportable claims

Family/domain relationship and strong fold relationship.

### Inferential mechanistic claims

Local residue/pocket similarities or differences that may favour one interpretation.

### Unsupported without biochemical validation

Exact catalytic activity, halide specificity and physiological substrate.

The project must not conclude that O67940 is definitively a chlorinase or fluorinase without appropriate experimental evidence.

---

## Step 14 — publication figures and manuscript update

Only after the core analyses are frozen:

- broader phylogenetic figure;
- structural-neighbour summary;
- active-site/pocket figure;
- functional-residue conservation figure;
- evidence-chain overview where useful.

Large diagnostics and complete trees belong in supplementary/archive material when appropriate.

Update:

- README;
- scope matrix;
- Methods;
- Results;
- Discussion;
- Limitations;
- figure legends;
- supplementary methods.

Preserve the v0.1 historical state rather than rewriting it.

---

## Step 15 — reproducibility and claim audit

### Reproducibility

Check:

- scripts;
- syntax/tests;
- input validation;
- environment versions;
- provenance;
- checksums;
- expected record counts;
- anchor recovery;
- sequence/structure mappings;
- deterministic outputs;
- manual DALI checkpoint documentation.

Rerun critical analysis layers from frozen inputs where feasible.

### Scientific claim audit

For every major conclusion ask:

- is this directly observed or inferred?
- is the evidence computational or experimental?
- does structural similarity get mistaken for functional proof?
- does clustering get mistaken for orthology?
- do annotation names get mistaken for biochemical evidence?
- is contradictory evidence reported?
- would the conclusion survive removal of the historically preferred reference?

Mixed evidence must remain mixed.

---

## Step 16 — freeze publication state

Only after the analyses and audits are coherent:

- clean Git working tree;
- final version history;
- push branch;
- tag publication state;
- update main branch when appropriate;
- preserve v0.1 course-report tag.

---

# Drift guardrails

Do not add the following without a specific unresolved scientific question:

- additional homolog-search tools merely to collect more hits;
- more arbitrary MMseqs thresholds;
- an HGT project around the ten unusual eukaryotic records;
- docking screens;
- molecular dynamics;
- AlphaFold-Multimer solely because interfaces are interesting;
- PLM embeddings solely because they are modern;
- generative models;
- multiple structural aligners only to accumulate RMSD values;
- literal recreation of every obsolete 2008 database search.

The rule is:

question → method → evidence → stop condition.

Not:

tool → result → invented justification.

---

# Final project stopping condition

The computational project is complete when it can reproducibly state:

what modern sequence, structural and evolutionary evidence supports about O67940,

and

where that evidence stops.

A scientifically valid final result may remain unable to determine exact enzymatic activity or substrate specificity.

That is not failure.

It is the boundary of the available evidence.
