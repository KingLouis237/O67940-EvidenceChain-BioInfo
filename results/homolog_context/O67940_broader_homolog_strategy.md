# Broader homolog strategy for O67940_AQUAE

## Why this step was added

The first homolog analysis used Swiss-Prot as a small reviewed reference set.

That was useful because the annotations were curated and easy to inspect, but it contained only 11 relevant reviewed proteins. The resulting alignment and tree therefore provide controlled context rather than a broad evolutionary reconstruction.

The next step is to expand the homolog space without treating thousands of unreviewed annotations as if they were experimentally validated functions.

## Candidate-space definition

The broader UniProtKB candidate space was defined using:

- Pfam PF01887
- Pfam PF20257
- non-fragment proteins
- sequence length 200–350 aa

This returned 4432 proteins.

Breakdown:

- 11 reviewed
- 4421 unreviewed
- 3991 bacterial
- 431 archaeal

Tightening the sequence-length range had little effect on the size of the candidate set, so length alone is not useful for meaningful further selection.

## Why protein names cannot drive the selection

Protein-name searches initially suggested large fluorinase and chlorinase groups:

- fluorinase query: 2033
- chlorinase query: 2032

However, 2017 accessions occurred in both sets.

Only:

- 16 were fluorinase-only
- 15 were chlorinase-only

The two name-based searches therefore describe almost the same annotation space and cannot be treated as independent functional classes.

The hydrolase name query behaved differently:

- 113 total
- 112 hydrolase-only

These names will remain useful metadata, but they will not be used as ground-truth functional labels for broader homolog selection.

## Downloaded candidate set

The complete Pfam-constrained candidate set was downloaded from UniProtKB.

Files:

- `data/databases/O67940_uniprot_pfam_candidates/candidate_metadata.tsv`
- `data/databases/O67940_uniprot_pfam_candidates/candidate_sequences.fasta`
- `data/databases/O67940_uniprot_pfam_candidates/query.txt`

Validation:

- metadata rows: 4432
- FASTA records: 4432

The metadata and sequence counts agree.

## Selection principle

The broader homolog set will be selected primarily from sequence evidence rather than annotation names.

The planned sequence is:

1. rank the 4432 candidates by direct similarity to O67940
2. inspect alignment coverage as well as significance
3. remove weak, partial, or otherwise unsuitable matches
4. reduce redundancy so highly similar sequence clusters do not dominate the analysis
5. preserve useful taxonomic and sequence diversity
6. retain the known reviewed proteins and structural references as labelled anchors
7. create a manageable curated homolog set for multiple-sequence alignment and phylogeny

Protein names will be carried as metadata for interpretation after sequence-based selection.

## Why direct similarity ranking comes next

The Pfam query defines proteins sharing the relevant domain context, but it does not tell us which proteins are the closest homologs of O67940.

A direct O67940-versus-candidate sequence search is therefore needed before phylogenetic sampling.

The next analysis will use PHMMER against the 4432-sequence candidate FASTA.

PHMMER is being used here as a direct pairwise-profile-style sequence search rather than another iterative JackHMMER expansion. This gives a clean ranking of the already defined candidate universe relative to O67940.

## Important limitations

This candidate set is still not an exhaustive universe of all possible O67940 homologs.

It is conditioned on the presence of PF01887 and PF20257 in UniProtKB annotation. Divergent proteins lacking those annotations could therefore be absent.

UniProtKB protein names, particularly among unreviewed entries, are also not treated as biochemical validation.

The resulting broader phylogeny will therefore provide evolutionary context rather than proof of enzyme activity or substrate specificity.

## Direct O67940 similarity ranking

The 4432-sequence candidate universe will next be searched directly with O67940 using PHMMER.

This step is intended to rank candidates by direct sequence evidence after the broader Pfam-defined universe has already been fixed.

The first PHMMER run will not itself define the final phylogenetic set.

Candidate evaluation will consider:

- full-sequence E-value
- full-sequence score
- domain-level significance
- query coverage
- target coverage
- sequence length
- taxonomic representation
- redundancy

Protein names will not be used to decide whether a hit is kept.

No final identity, E-value, or coverage threshold will be chosen until the score and coverage distributions have been inspected. This avoids imposing an arbitrary cutoff without seeing how the candidate space behaves.

Known reviewed proteins and structural references will remain as labelled anchors even if broader sampling later reduces redundancy around them.

## PHMMER ranking of the broader candidate universe

PHMMER was run using O67940 against the fixed 4432-sequence Pfam-constrained UniProtKB candidate set.

The query itself was present in the candidate set and appeared as the top hit. It will be excluded from homolog sampling but retained as a positive-control observation.

All 4432 sequences passed the permissive PHMMER reporting threshold. This is expected because the candidate universe was already restricted to proteins carrying both relevant Pfam domains.

Among the 4431 non-self candidates:

- median query coverage was approximately 0.745
- median target coverage was approximately 0.695
- 1960 sequences had at least 70% coverage of both query and target
- 990 had at least 80% coverage of both
- 861 had at least 90% coverage of both
- 560 had at least 95% coverage of both

Most candidates produced one reported domain match (4315), while 116 produced two.

The top PHMMER hits are enriched in several organisms related to the Aquificota/thermophilic neighbourhood of O67940. This likely contains genuine evolutionary signal, but taking only the highest-scoring hits would risk strong taxonomic and sequence-redundancy bias.

The broader phylogenetic set will therefore not be selected by rank alone.

Before fixing a coverage threshold, the known reviewed Swiss-Prot anchors will be checked explicitly to make sure that biologically relevant fluorinase, SalL, and SAM-hydrolase references are not unintentionally removed by a simple full-length coverage rule.
