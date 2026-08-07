# O67940 broader PHMMER analysis

## Purpose

PHMMER was used to rank O67940 against the fixed UniProtKB candidate set defined by PF01887 and PF20257.

The candidate database contained 4432 proteins. The purpose of this search was not to assign function directly, but to measure how the broader domain-defined candidate space relates to O67940 by direct sequence similarity.

## Search result

PHMMER reported all 4432 sequences at the permissive reporting threshold used for this exploratory ranking.

O67940 itself was present in the downloaded UniProtKB candidate set and was the highest-scoring hit. After removing this self-hit, 4431 candidates remained.

This broad recovery is expected because the database had already been restricted to proteins carrying both relevant Pfam domains.

## Coverage and domain behaviour

For the 4431 non-self candidates:

- median query coverage was 0.7450
- median target coverage was 0.6947
- 1960 sequences had at least 70% query and target coverage
- 990 had at least 80%
- 861 had at least 90%
- 560 had at least 95%

Most candidates produced one reported PHMMER domain match:

- 4315 candidates had one reported domain
- 116 had two reported domains

These values describe PHMMER local alignment behaviour. They are not, by themselves, evidence that sequences below a particular coverage value belong to a different functional family.

## Check against known reviewed proteins

All 11 reviewed Swiss-Prot reference proteins were recovered.

The coverage values of these known anchors showed that a strict high-coverage filter would be inappropriate.

For example:

- RSAMH_PYRHO: qcov 0.9801, tcov 0.9844
- RSAMH_THET8: qcov 0.9761, tcov 0.9804
- RSAMH_METJA: qcov 0.7729, tcov 0.6996
- SALL_SALTO: qcov 0.7450, tcov 0.6749

The reviewed fluorinases had query coverage around 0.73–0.74 and target coverage around 0.63–0.64.

A qcov/tcov >= 0.90 filter would therefore retain some SAM-hydrolase-like references while removing SalL and all of the reviewed fluorinases.

For that reason, PHMMER coverage will be retained as descriptive evidence rather than used as a simple hard exclusion threshold.

## Score ranking

The PHMMER score declines gradually rather than showing an obvious single breakpoint.

Representative checkpoints include:

- rank 10: score 274.2
- rank 25: score 205.7
- rank 50: score 188.5
- rank 100: score 175.8
- rank 250: score 163.0
- rank 500: score 147.7
- rank 1000: score 127.3
- rank 2000: score 112.8
- rank 4431: score 30.6

There is therefore no obvious evidence-based score or rank threshold that defines a natural final phylogenetic set.

Taking only the highest-ranking sequences would also overrepresent the sequence neighbourhood closest to O67940.

## Taxonomic observation

The strongest non-self hits include several Aquificota and other thermophilic bacterial or archaeal proteins, which is consistent with a close sequence neighbourhood around the Aquifex query.

However, the candidate set also contains a small number of entries outside Bacteria and Archaea. These entries will be inspected explicitly before any taxonomic restriction is applied.

They will not be removed automatically without documenting why.

## Decision

The final broader homolog set will not be chosen using:

- UniProt protein names as ground-truth functional labels
- a qcov/tcov >= 0.90 rule
- an arbitrary PHMMER score threshold
- a simple top-N ranking

The next stage will examine redundancy and taxonomic composition.

The eventual broader phylogenetic set should preserve:

1. the sequence neighbourhood closest to O67940
2. the reviewed Swiss-Prot and structural functional anchors
3. broader non-redundant sequence and taxonomic diversity

## What this analysis supports

PHMMER confirms that O67940 sits within a large sequence space sharing the same broad domain context and provides a reproducible ranking of that space relative to the query.

## What it does not prove

PHMMER similarity does not establish substrate specificity or enzyme activity.

Protein names among the unreviewed candidates are not treated as biochemical validation.

The candidate universe is also conditioned on PF01887/PF20257 annotation, so it is not an exhaustive search for every possible divergent homolog.
