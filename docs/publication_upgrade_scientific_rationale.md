# O67940 publication upgrade — scientific rationale and research questions

## Purpose of this document

This document defines the scientific logic of the O67940 publication upgrade.

It is not a retrospective preregistration.

Several analyses were already completed before the present research question was fully clarified. Those observations are kept as observations that helped reshape the project rather than being presented as hypotheses specified in advance.

The purpose here is to separate:

1. the question asked in the 2008 O67940 case study;
2. what the original course-report reanalysis established;
3. what the publication-upgrade analyses have already observed;
4. what remains unresolved;
5. the questions that will guide the remaining work.

The project should not be organized around proving that O67940 is a chlorinase, fluorinase, hydrolase, or any other predefined function.

The goal is to determine what level of functional resolution current evidence can legitimately support.

---

# 1. Historical problem

O67940_AQUAE is a 251-residue protein from *Aquifex aeolicus* that was used as the worked example in the 2008 structure-guided protein-function inference study of Mazumder and Vasudevan.

At that time, O67940 was annotated as an uncharacterized conserved protein.

The original analysis identified two experimentally characterized structural relatives:

- 2Q6O / SalL from *Salinispora tropica*, a SAM-dependent chlorinase;
- 1RQP / FlA from *Streptomyces cattleya*, a SAM-dependent fluorinase.

The reported sequence identities to O67940 were approximately:

- 32% to 2Q6O;
- 26% to 1RQP.

The authors correctly treated those identities as too low for direct functional transfer.

Their working question was therefore whether O67940 was:

- chlorinase-like;
- fluorinase-like;
- or more generally a SAM-dependent halogenase.

Additional sequence, structural, phylogenetic and functional-site evidence was then assembled.

The original study eventually emphasized two O67940 positions:

- Val67;
- Gly127.

These were mapped to functionally discussed positions in SalL and FlA.

The authors concluded that O67940 appeared closer to the SalL/chlorinase configuration than to the canonical fluorinase configuration and proposed that chloride, bromide or iodide chemistry might be plausible.

They explicitly stated that the precise specificity could not be established without additional experimental evidence.

The original paper was primarily a tutorial and methodological framework for evidence-based annotation transfer. O67940 was its worked biological example.

---

# 2. Important development that changes the modern question

The modern functional landscape is broader than the chlorinase-versus-fluorinase framing used in the original case study.

In 2008, Eustáquio and colleagues characterized S-adenosyl-L-methionine hydrolase activity in proteins related to SAM-dependent halogenases and argued that many members of the broader family are SAM adenosylhydrolases rather than halogenases.

Subsequent mechanistic work on SAM hydroxide adenosyltransferases identified a conserved water-activation network involving approximately:

- Asp68;
- Arg75;
- His127

in the *Pyrococcus horikoshii* reference enzyme.

The Asp–Arg interaction plays an important role in positioning/activating water for nucleophilic attack on SAM.

Later evolutionary and structural analyses placed SAM-dependent halogenases and SAM hydroxide adenosyltransferases in a closely related sequence/structural landscape.

Both can share strong overall tertiary-structure similarity while differing in active-site organization and nucleophile handling.

Therefore, the modern first-order functional question is not simply:

> chlorinase or fluorinase?

It is:

> hydrolase, halogenase, or unresolved member of their shared SAM-utilizing structural/evolutionary family?

Only if the halogenase branch is supported does detailed halide specificity become the next question.

---

# 3. Modern evidence also changes how halide specificity should be interpreted

The original O67940 discussion placed considerable weight on positions corresponding to SalL Tyr70/Gly131 and FlA Thr/Ser states.

Those positions remain mechanistically interesting, but later experimental work shows that they should not be treated as simple one-residue specificity switches.

Recent SalL engineering demonstrated that:

- Tyr70 strongly affects acquisition of fluorination activity;
- G131S alone did not confer fluorination;
- additional pocket changes such as W129F further altered activity.

Modern specificity interpretation must therefore consider a local residue configuration and pocket geometry rather than treating O67940 Gly127 as a standalone chlorinase marker.

The historical Val67/Gly127 positions remain valuable because they were specified before the present reanalysis.

They should now be treated as historical hypotheses whose discriminative value can be tested against a much larger modern sequence and structural landscape.

---

# 4. Original course-report reanalysis: what was actually done

The first modern O67940 reanalysis was intentionally bounded.

It was not a literal reproduction of every 2008 analysis.

The project modernized selected evidence layers using current resources and tools.

The principal completed layers were:

- current UniProtKB sequence and annotation state;
- InterPro/Pfam domain context;
- AlphaFoldDB predicted structure;
- AlphaFold confidence assessment;
- direct structural comparison with 2Q6O and 1RQP using TM-align;
- MAFFT sequence alignment;
- mapping of historically discussed functional residues;
- provenance, checksums and environment documentation.

The original report did not yet contain:

- a broad modern homolog universe;
- publication-level phylogenetic inference;
- an independent structural-neighbour search;
- explicit hydrolase-versus-halogenase testing;
- biological-assembly/interface analysis.

Those limitations motivated the publication upgrade.

---

# 5. Result from the original reanalysis: current annotation remained unresolved

The project snapshot retrieved for O67940 remained an unreviewed UniProtKB entry annotated as an uncharacterized protein.

No experimentally solved O67940 structure was associated with the project record.

Interpretation:

This shows that the principal annotation resource used by the project had not resolved O67940 to a specific experimentally supported biochemical activity.

It does not prove that no later experimental characterization exists.

A formal post-2008 literature and annotation-history audit is therefore still required.

---

# 6. Result from the original reanalysis: SAM-related family/domain context

InterPro/Pfam analysis supported the expected SAM-related domain architecture.

Earlier project wording tended to interpret this as support for a SAM-dependent halogenase-related protein.

The publication-upgrade interpretation is deliberately broader.

Current evidence supports membership in the broader DUF62-related SAM-utilizing structural/evolutionary landscape containing SAM hydroxide adenosyltransferases and SAM-dependent halogenases.

The domain result does not by itself discriminate:

- water/hydroxide attack;
- fluoride attack;
- chloride/bromide/iodide attack.

This is family-level evidence rather than exact-function evidence.

---

# 7. Result from the original reanalysis: AlphaFold provides a high-confidence O67940 structural model

AlphaFoldDB v6 provides a full 251-residue predicted structure for O67940.

The project confidence analysis found approximately:

- mean pLDDT: 96.70;
- median pLDDT: 97.69;
- 242 residues with pLDDT >= 90;
- 9 residues between 70 and 90;
- no residues below 70.

The predicted structure is therefore sufficiently confident for careful computational structural comparison.

Interpretation:

This is an important modernization relative to 2008 because O67940 itself can now be used as a structural query.

However:

- pLDDT is coordinate-confidence evidence, not functional confidence;
- the AlphaFold monomer does not establish the biological oligomeric state;
- predicted structural similarity cannot by itself establish biochemical activity.

---

# 8. Result from the original reanalysis: strong protomer-level structural similarity to both historical references

TM-align comparisons gave approximately:

- O67940 vs 2Q6O: reference-normalized TM-score 0.853, RMSD approximately 2.0 Å;
- O67940 vs 1RQP: reference-normalized TM-score 0.790, RMSD approximately 2.0 Å.

O67940 therefore has strong tertiary-structure similarity to both historical reference proteins, with a modest numerical preference toward 2Q6O.

Earlier project interpretation treated this as part of the evidence leaning toward the chlorinase reference.

The revised interpretation is narrower:

> O67940 strongly shares the protomer-level tertiary architecture of this SAM-utilizing family.

This result does not discriminate hydrolase from halogenase reliably because SAM hydroxide adenosyltransferases can share closely related tertiary structures with SAM-dependent halogenases.

The existing TM-align result remains valid.

Its functional interpretation has become more conservative as the biological comparison space has expanded.

---

# 9. Result from the original reanalysis: historical Val67/Gly127 mapping was reproduced

The first alignment/mapping layer recovered O67940:

- Val67;
- Gly127

at the historically discussed regions corresponding to SalL/FlA specificity-associated positions.

This reproduced an important part of the 2008 argument.

Interpretation:

Gly127 means that O67940 does not simply carry the canonical FlA serine state at the corresponding historical position.

However, Gly127 cannot be interpreted as sufficient evidence for chlorinase activity.

Modern mutagenesis shows that the corresponding SalL G131S change alone does not generate fluorination and that other positions, including the Tyr70 region and neighbouring pocket residues, are important.

Therefore the historical residues should now be evaluated as part of a multi-residue active-site architecture.

---

# 10. Publication upgrade: reviewed Swiss-Prot reference context

The publication upgrade first introduced a deliberately small, higher-confidence reviewed Swiss-Prot reference context.

Reviewed status indicates manual UniProtKB curation but does not by itself establish that every assigned biochemical activity has been experimentally demonstrated for that exact protein. Experimental support for individual functional anchors must therefore be audited separately.

The reviewed set included:

- five SAM-hydrolase-like proteins;
- five fluorinases;
- SalL;
- the historical structures/references;
- O67940.

In the 14-sequence MAFFT context, O67940 sequence identities included approximately:

- RSAMH_METJA: 41.13%;
- RSAMH_PYRHO: 38.66%;
- RSAMH_THET8: 34.16%;
- RSAMH_SALAI: 32.50%;
- RSAMH_SALTO: 32.08%;
- SalL / relevant chlorinase reference: approximately 28.7%;
- fluorinase references: approximately 27-29%.

This was one of the first results that materially changed the direction of the project.

Interpretation:

Several reviewed SAM hydrolase-like proteins are more similar to O67940 at the sequence level than the canonical SalL/FlA halogenase references.

This does not prove O67940 is a SAM hydrolase.

It does mean that a halogenase-only hypothesis space is no longer justified.

Hydrolase-versus-halogenase discrimination must become an explicit research question.

---

# 11. Publication upgrade: exploratory reviewed-reference phylogeny

An exploratory FastTree analysis of the small reviewed-reference set placed O67940 near the reviewed RSAMH_METJA SAM-hydrolase-like sequence, with local support around 0.77.

SalL-related and fluorinase reference relationships were strongly recovered locally, while several deeper relationships were weak.

Interpretation:

This exploratory tree does not establish O67940 function.

Its small sample size and approximate inference make it insufficient as the final phylogenetic result.

However, it independently reinforced the sequence-similarity observation that O67940 should not automatically be analysed only against halogenase references.

A stronger broad phylogenetic test is therefore scientifically justified.

---

# 12. Publication upgrade: frozen operational candidate universe

A current UniProt/Pfam-defined operational candidate space was constructed using the selected PF01887/PF20257 domain architecture, length constraints and fragment exclusion.

This is a reproducible search universe, not a claim that every biologically relevant member of the broader DUF62-related family is captured by these filters.

The frozen dataset contains:

- 4,432 candidate proteins;
- 11 reviewed reference anchors;
- 4,421 unreviewed entries.

This is vastly larger than the homolog context available in the original 2008 worked example.

Interpretation:

The large number of sequences provides modern evolutionary context.

It does not provide thousands of experimentally known functions.

Sequence-database expansion should not be confused with equivalent expansion of functional evidence.

---

# 13. Publication upgrade: annotation-name overlap exposed a database interpretation problem

Within the broader candidate space, protein-name searches showed approximately:

- 2,033 fluorinase-name matches;
- 2,032 chlorinase-name matches;
- 2,017 records appearing in both name-query sets.

Interpretation:

Protein names in this largely unreviewed sequence universe cannot be treated as biochemical ground truth.

The overlap demonstrates that the fluorinase and chlorinase protein-name query categories are highly non-independent.

Annotation propagation, shared naming conventions and broad computational annotation are plausible contributors, but the overlap alone does not establish which mechanism produced the labels.

This result reinforces the central annotation-transfer problem that motivated the original 2008 paper.

Modern databases contain far more sequences, but annotation labels remain weaker evidence than experimentally characterized anchors.

---

# 14. Publication upgrade: PHMMER ranking again highlighted reviewed SAM hydrolases

PHMMER was run against the frozen 4,432-sequence candidate universe.

Among the reviewed anchors, several SAM hydrolase-like proteins ranked more strongly against O67940 than the canonical halogenase references.

Approximate reviewed-anchor scores included:

- RSAMH_PYRHO: 170.8;
- RSAMH_THET8: 128.6;
- RSAMH_METJA: 122.4;
- RSAMH_SALAI: 106.9;
- RSAMH_SALTO: 104.2;
- SalL: 91.9;
- reviewed fluorinases: approximately 73-80.

Interpretation:

Several reviewed hydrolase-like references have higher PHMMER full-sequence scores against O67940 than SalL/FlA.

Together with the reviewed-reference alignment, this provides a second sequence-based observation favouring investigation of the hydrolase-like neighbourhood. PHMMER score is not itself a measure of evolutionary distance or biochemical function.

PHMMER similarity still does not establish biochemical activity.

The repeated observation instead motivates a prospective hydrolase-versus-halogenase test.

---

# 15. Why no simple PHMMER cutoff was retained

Reviewed anchors themselves showed heterogeneous coverage.

A strict 90% query-and-target coverage filter would remove SalL and the reviewed fluorinases while retaining only a small subset of reviewed anchors.

The PHMMER score distribution also did not provide a clear biological breakpoint.

Therefore the project rejected:

- arbitrary top-N ranking;
- hard score cutoff;
- hard 90% coverage cutoff;
- protein-name-defined functional classes.

This is a methodological decision rather than a biological result.

Its purpose is to prevent the phylogenetic set from being constructed to favour a predetermined interpretation.

---

# 16. Publication upgrade: redundancy analysis

The 4,432 candidate sequences were clustered with MMseqs2 at several identity thresholds using 80% bidirectional coverage.

The resulting cluster counts were:

- 95% identity: 3,606 clusters;
- 90% identity: 2,858 clusters;
- 80% identity: 1,816 clusters;
- 70% identity: 1,181 clusters.

At 90% identity, O67940 and all eleven reviewed anchors remained in distinct clusters.

At lower thresholds, several characterized anchors began collapsing into shared clusters.

The 90% / 80%-coverage level was therefore selected as the first redundancy-pruning threshold.

Interpretation:

This is a sampling and data-structure decision.

It does not define family membership, orthology or biochemical function.

The 2,858 cluster representatives are appropriate candidates for broad evolutionary analysis, but they must not automatically be treated as an unbiased residue-frequency dataset.

---

# 17. Important distinction for future residue analysis

Three related but different datasets should be distinguished.

## Raw database-level composition

All 4,432 qualified records.

This measures the residue distribution in the frozen database snapshot but is affected by uneven sequence/taxon sampling.

## Cluster-aware or sequence-weighted composition

All 4,432 sequences analysed while accounting for redundancy.

This can provide a more balanced estimate of residue-state prevalence.

## Diversity-representative set

The 2,858 90%-identity cluster representatives.

This equalizes sequence groups for phylogenetic tractability but deliberately changes sequence-frequency weighting.

The project should also measure within-cluster heterogeneity at mechanistically relevant positions.

If a 90%-identity cluster contains multiple residue states at an important position, a single representative may hide relevant functional diversity.

---

# 18. Current evidence summary

The project currently supports the following statements.

## Strongly supported

O67940 is strongly supported as a member of the broader DUF62-related SAM-utilizing structural/evolutionary landscape containing SAM-dependent halogenases and SAM hydroxide adenosyltransferases.

O67940 has a high-confidence predicted tertiary structure.

Its protomer-level tertiary structure is strongly similar to SalL and FlA.

## Supported as observations requiring further testing

Several reviewed Swiss-Prot hydrolase-like references show higher pairwise sequence identity to O67940 than the canonical SalL/FlA halogenase references.

The exploratory reviewed-reference tree is compatible with that same hydrolase-like sequence neighbourhood.

O67940 does not carry the straightforward canonical FlA residue state at the historically emphasized Gly/Ser position.

## Not currently established

O67940 is a SAM hydrolase.

O67940 is a SAM-dependent halogenase.

O67940 is a chlorinase.

O67940 is a fluorinase.

O67940 uses chloride, bromide, iodide or fluoride in vivo.

O67940 shares the biological oligomeric state of SalL or FlA.

The exact physiological role of O67940 in *Aquifex aeolicus*.

---

# 19. Revised primary research question

The publication upgrade is now guided by the following primary question:

> How has the evidential basis for functional annotation of O67940 changed since its 2008 structure-guided analysis, what functional annotation can contemporary computational evidence support, and where does experimental validation remain necessary?

The central biological discrimination is:

> Is O67940 better supported as a SAM hydroxide adenosyltransferase/hydrolase, a SAM-dependent halogenase, or an unresolved member of their shared structural/evolutionary family?

Only if the halogenase branch is supported should detailed halide specificity become a primary downstream question.

---

# 20. Prospective research questions

The following questions are prospective from this checkpoint onward.

## RQ1 — Current functional-family placement

Do supported evolutionary relationships to experimentally characterized anchors place O67940 preferentially with:

- SAM hydroxide adenosyltransferases;
- SAM-dependent halogenases;
- or neither with adequate confidence?

## RQ2 — Mechanistic active-site architecture

Does O67940 conserve the structural equivalents of the Asp–Arg–His water-activation network described in experimentally characterized DUF62 hydrolase references, a halogenase-compatible nucleophile-binding environment, or a mixed/other configuration?

Residue numbering from one protein must not be transferred directly to O67940 without sequence/structural mapping.

## RQ3 — Independent structural neighbourhood

When the validated O67940 AlphaFold protomer is searched against the modern experimental structural database, which experimentally characterized functions occur among meaningful structural neighbours?

Relevant possibilities include:

- SAM hydrolases;
- chlorinases;
- fluorinases;
- other related functions.

Global structural similarity alone will not assign biochemical activity.

## RQ4 — Broader residue evolution

Across the frozen 4,432-sequence operational candidate universe defined by the project filters:

- how are historically and mechanistically relevant residue states distributed?
- are the 90%-identity clusters internally homogeneous at these positions?
- do residue configurations associate with supported evolutionary neighbourhoods?

Raw, weighted/cluster-aware and representative-set summaries must not be conflated.

## RQ5 — Halide specificity, conditionally

Only if O67940 is supported as a halogenase:

Does its multi-residue active-site configuration and pocket geometry more closely resemble:

- canonical fluorinase chemistry;
- SalL-like non-fluorinating halogenase chemistry;
- or neither clearly?

No single residue will be treated as a sufficient specificity determinant.

## RQ6 — Historical stability of annotation transfer

Does modern evidence:

- strengthen;
- refine;
- weaken;
- contradict;
- or leave unresolved

the functional inference made for O67940 in 2008?

---

# 21. Required near-term analyses

The revised questions change the reason for several already planned analyses.

## Post-2008 literature and annotation audit

Purpose:

Determine whether O67940 / aq_2196 has acquired experimental characterization, alternative identifiers, new database evidence or direct literature since the original study.

This must be completed before claiming novelty or unresolved status.

## Functional-anchor audit

Purpose:

Determine which reviewed hydrolase-, chlorinase- and fluorinase-like references have direct experimental support for the biochemical activity being used as their functional label.

For each candidate anchor, record where possible:

- exact accession and organism;
- experimental biochemical evidence;
- primary literature supporting the activity;
- structural evidence, if available;
- ligand/substrate state;
- whether the exact protein or only a close homolog was experimentally characterized.

Reviewed Swiss-Prot status alone will not qualify a sequence as an experimentally validated functional anchor.

Only audited anchors will be used as ground-truth functional landmarks in the final phylogenetic and mechanistic interpretation.

## Functional-anchor audit

Purpose:

Determine which reviewed hydrolase-, chlorinase- and fluorinase-like references have direct experimental support for the biochemical activity being used as their functional label.

For each candidate anchor, record where possible:

- exact accession and organism;
- experimental biochemical evidence;
- primary literature supporting the activity;
- structural evidence, if available;
- ligand/substrate state;
- whether the exact protein or only a close homolog was experimentally characterized.

Reviewed Swiss-Prot status alone will not qualify a sequence as an experimentally validated functional anchor.

Only audited anchors will be used as ground-truth functional landmarks in the final phylogenetic and mechanistic interpretation.

## Hydrolase-mechanism residue mapping

Purpose:

Map the experimentally characterized hydrolase active-site network onto O67940, SalL, FlA and reviewed hydrolase anchors.

This requires alignment/structural correspondence rather than copied residue numbers.

## DALI structural-neighbour search

Purpose:

Not merely to modernize the old VAST step.

The biological question is now:

> does the modern structural neighbourhood recover experimentally characterized hydrolases, halogenases, both, or neither as the closest meaningful functional anchors?

## Broad phylogeny

Purpose:

Not merely to replace FastTree with a more publication-grade program.

The question is:

> where does O67940 lie relative to experimentally characterized hydrolase and halogenase lineages, and how strongly is that placement supported?

## Broader residue analysis

Purpose:

Test whether the historical Val67/Gly127 interpretation remains discriminative in modern sequence space and whether broader active-site configurations are more informative.

## Local structural analysis

Purpose:

Compare O67940 against at least:

- an experimentally characterized SAM hydrolase;
- SalL;
- FlA;

at the level of active-site geometry, ligand environment and relevant interface context.

The structural comparison should not remain a two-reference chlorinase-versus-fluorinase analysis.

---

# 22. Conditional evidence layers

## Genomic neighbourhood

Genomic context may provide an independent evidence axis.

It is not automatically added as a large new project.

It should be used only if the sequence, phylogenetic and structural evidence leaves a defined ambiguity that genomic context can plausibly help resolve.

## Additional methods

PLM embeddings, docking, molecular dynamics, AlphaFold-Multimer and additional structural aligners are not justified merely because they are modern.

A new method requires a specific unresolved question and a predefined interpretation/stop condition.

---

# 23. Publication-level stopping rules

## Novel functional reinterpretation

A claim that O67940 has a newly resolved biochemical function requires material evidence beyond reproducing the 2008 inference.

Computational evidence should converge across multiple relevant layers and remain explicitly distinct from biochemical validation.

## Longitudinal/reproducibility contribution

If the final biological inference remains similar to 2008, a manuscript may still be justified only if the study demonstrates a transferable insight concerning:

- annotation stability;
- database expansion versus functional resolution;
- annotation propagation;
- evidence calibration;
- or reproducible modernization of protein-function inference.

## Insufficient publication contribution

If the project only reproduces the 2008 conclusion with newer software and produces no meaningful biological refinement or transferable methodological insight, it should not be presented as a novel research discovery.

The repository and reproducible case study would still remain scientifically useful.

---

# 24. Claim boundaries

The project must preserve the following distinctions.

Sequence similarity is not function.

Domain membership is not exact catalytic activity.

A high DALI Z-score is not function.

A high TM-score is not function.

A phylogenetic neighbourhood is not biochemical validation.

A single residue is not a specificity assignment.

Protein names in unreviewed databases are not experimental labels.

AlphaFold confidence is not biochemical confidence.

A monomeric AlphaFold model is not an oligomeric-state measurement.

Agreement between several computational tools measuring related properties is not equivalent to independent biochemical evidence.

---

# 25. Current working interpretation

At this checkpoint, the strongest scientifically defensible interpretation is:

> O67940 is a structurally well-defined member of the broader DUF62-related SAM-utilizing landscape containing SAM hydroxide adenosyltransferases and SAM-dependent halogenases. The original 2008 analysis proposed a SalL-like halogenase interpretation, but modern sequence evidence in this project shows that several reviewed Swiss-Prot hydrolase-like references have greater sequence similarity to O67940 than the canonical SalL/FlA references. The current evidence therefore does not justify choosing between hydrolase and halogenase activity. The remaining work should explicitly test that distinction before attempting detailed halide-specificity inference.

This interpretation is provisional.

The remaining analyses must be allowed to:

- strengthen it;
- weaken it;
- contradict it;
- or leave the functional assignment unresolved.

---

# 26. Evidence chronology

The project history should be represented honestly as:

2008 historical hypothesis
→ O67940 likely belongs to the SAM-dependent halogenase family and appears more SalL-like than FlA-like.

v0.1 modern course reanalysis
→ reproduced the broad structural/family relationship and historical residue mapping using modern resources.

publication-upgrade exploration
→ expanded reviewed homolog context and broader sequence space.

unexpected modern observation
→ multiple reviewed Swiss-Prot hydrolase-like references show greater sequence similarity to O67940 than the canonical SalL/FlA references.

revised prospective question
→ hydrolase versus halogenase must be tested before detailed halide specificity.

remaining analyses
→ literature audit, mechanistic residue mapping, DALI, supported broad phylogeny, broad residue analysis and local active-site/interface comparison.

This chronology should not be rewritten later to make the final result appear predetermined.

---

# References guiding the revised scientific rationale

1. Mazumder R, Vasudevan S. Structure-Guided Comparative Analysis of Proteins: Principles, Tools, and Applications for Predicting Function. PLoS Computational Biology. 2008;4:e1000151. doi:10.1371/journal.pcbi.1000151.

2. Eustáquio AS, Härle J, Noel JP, Moore BS. S-Adenosyl-L-Methionine Hydrolase (Adenosine-Forming), a Conserved Bacterial and Archeal Protein Related to SAM-Dependent Halogenases. ChemBioChem. 2008;9:2215-2219. doi:10.1002/cbic.200800341.

3. Deng H, McMahon SA, Eustáquio AS, Moore BS, Naismith JH, O'Hagan D. Mechanistic Insights into Water Activation in SAM Hydroxide Adenosyltransferase (duf-62). ChemBioChem. 2009;10:2455-2459. doi:10.1002/cbic.200900369.

4. Xu G, Wang BG. Independent Evolution of Six Families of Halogenating Enzymes. PLoS ONE. 2016;11:e0154619. doi:10.1371/journal.pone.0154619.

5. Enzyme Engineering Renders Chlorinase the Activity of Fluorinase. Journal of Agricultural and Food Chemistry. 2024;72:1203-1212. doi:10.1021/acs.jafc.3c08185.

6. He K, Yan Y, Feng S, Wang P, Zhang Z, Wang N. Two fluorinases prioritized from protein families of fluorinase, SAM-dependent chlorinase and hydroxide adenosyltransferase. Organic & Biomolecular Chemistry. 2025;23:318-322. doi:10.1039/D4OB01638F.
