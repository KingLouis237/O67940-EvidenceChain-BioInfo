# Independent review of the remaining execution plan

## Context

An independent methodological review was obtained before beginning the remaining publication-upgrade analyses.

The reviewer considered the overall evidence hierarchy and ordering scientifically coherent. In particular, the review supported:

- separating fold similarity, local functional-site evidence, and exact biochemical activity;
- preserving explicit limitations for DALI, phylogeny, and structural interpretation;
- testing the broader sequence set before introducing an arbitrary small phylogenetic sample;
- allowing broader residue analysis to weaken, rather than automatically confirm, the existing G127 interpretation;
- using explicit stop conditions and drift guardrails.

The review also identified several points that required clarification before execution.

## Evaluation of the review

The review was useful but was not adopted uncritically.

Several statements described reasoned workflow choices as hard technical dependencies. The execution plan was therefore refined as follows.

### DALI ordering

DALI is not technically required before a cluster master table can be constructed.

It is placed before the final representative and structural-anchor freeze because an independent structural-neighbour search may identify additional experimentally characterized structures that should be considered before the phylogenetic input is fixed.

The master table could technically be built first and updated later, but performing DALI first avoids rebuilding that annotation layer.

### Cluster representative selection

The earlier idea of selecting the strongest PHMMER-scoring member from every ordinary cluster was rejected as the default rule.

PHMMER measures similarity to O67940. Choosing the PHMMER-best member in every cluster would therefore systematically bias cluster representatives toward the query.

The working representative hierarchy is instead:

1. retain O67940 in its own cluster;
2. explicitly retain verified functional or structural anchors where present;
3. otherwise retain the deterministic MMseqs2 cluster representative.

Any exception must have an independently documented biological reason.

### Full 2858-cluster analysis

The 2858-cluster set will not be reduced simply because a tree containing 2858 tips is difficult to visualize.

However, successful computation alone is not sufficient justification for retaining the full set.

The decision will consider:

- alignment quality;
- sequence/domain comparability;
- phylogenetic information content;
- anomalous sequences or branches;
- computational feasibility.

Reduction will be introduced only if a documented methodological reason requires it.

### Residue-conservation ordering

Global residue frequencies require the final multiple sequence alignment but not a phylogenetic tree.

Tree-aware or clade-aware residue interpretation does require a supported phylogeny.

Therefore:

MSA → global residue-conservation diagnostics

and later:

MSA + supported phylogeny → clade/neighbourhood-aware residue interpretation.

### Phylogenetic software version

The plan will not hard-code a particular IQ-TREE major version before execution.

The current stable and locally usable implementation will be checked when the phylogenetic step begins.

The methodological requirement is:

- maximum-likelihood inference;
- justified amino-acid model selection;
- appropriate branch-support assessment;
- exact tool/version/parameters recorded.

### Protein language models

A PLM/embedding analysis will not be added solely because it is modern or potentially complementary.

It will be considered only if a later, explicitly defined scientific question cannot be addressed adequately by the existing sequence, structural and phylogenetic evidence.

## Outcome

The independent review did not require a change in the central scientific question.

It strengthened the execution plan by:

- removing unnecessary O67940-centred representative-selection bias;
- distinguishing hard dependencies from reasoned ordering;
- making full-set retention conditional on scientific quality rather than computation alone;
- separating global from phylogeny-dependent residue analysis;
- preserving method choice as question-driven rather than novelty-driven.

The project therefore remains focused on determining what current sequence, structural and evolutionary evidence can support about O67940 without treating computational agreement as proof of exact enzymatic activity or substrate specificity.
