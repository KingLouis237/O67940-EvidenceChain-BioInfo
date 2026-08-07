# Taxonomic audit of non-Bacteria/non-Archaea candidates

## Why this audit was performed

The broader PF01887/PF20257 UniProtKB candidate survey returned 4432 proteins.

Taxonomic queries accounted for:

- 3991 bacterial proteins
- 431 archaeal proteins

This left 10 candidate proteins outside Bacteria and Archaea.

Because some of these sequences ranked relatively highly against O67940 by PHMMER, they were inspected rather than removed automatically.

## Taxonomic composition

The 10 records comprise:

- 2 ciliates
- 4 Entamoeba proteins
- 4 Geodia barretti proteins

Ciliate records:

- Blepharisma stoltei
- Stentor coeruleus

Entamoeba records:

- Entamoeba dispar
- Entamoeba histolytica
- Entamoeba invadens
- Entamoeba nuttalli

Sponge records:

- four proteins assigned to Geodia barretti

## Annotation evidence

All 10 entries are unreviewed UniProtKB records.

All have:

- protein existence: `3: Inferred from homology`
- annotation score: `1.0`

Consequently, protein names such as `Chlorinase MJ1651`, `Adenosyl-chloride synthase`, or `SAM-dependent chlorinase/fluorinase` are not treated as experimental evidence of enzyme activity.

## Sequence evidence

Several of the eukaryotic records show strong direct similarity to O67940.

The two ciliate proteins rank 161 and 189 among 4431 non-self candidates and align over approximately 94-97% of both query and target.

One Geodia barretti protein ranks 344 and also has high query and target coverage.

The Entamoeba proteins rank lower, but three of the four have approximately 98% query and target alignment coverage.

These observations indicate substantial sequence homology rather than isolated short motif matches.

## Interpretation

The current evidence supports the presence of O67940-family-like sequences in records assigned to several eukaryotic taxa.

It does not establish the biological origin of those sequences.

Possible explanations include:

- genuine eukaryotic homologs
- horizontal gene transfer
- microbial or symbiont-derived sequences represented in eukaryotic assemblies
- contamination or assembly artefacts
- taxonomic or annotation errors

The present analysis cannot distinguish among these possibilities.

Repeated occurrence across several Entamoeba species and the presence of homologous sequences in two ciliates make a simple one-off database anomaly less satisfactory as a general explanation, but they do not by themselves establish genuine eukaryotic inheritance.

Likewise, the four Geodia barretti records should not yet be interpreted as four independent host homologs because their sequence redundancy and genomic origin have not been assessed.

## Decision

The 10 sequences will not be removed before redundancy analysis.

Their relationships to each other and to prokaryotic candidates will first be examined by sequence clustering.

The broader phylogenetic analysis can then help determine whether they:

- fall within tight prokaryotic sequence clusters
- form taxon-specific groups
- occur as isolated long branches
- or show another pattern requiring separate treatment

If necessary, they can later be excluded from the primary prokaryotic tree while being retained and documented in a supplementary or sensitivity analysis.

## What this audit supports

The broader candidate space contains strong sequence homologs assigned to eukaryotic taxa, and these records warrant explicit treatment rather than silent removal.

## What it does not prove

This audit does not establish horizontal gene transfer, genuine eukaryotic gene origin, contamination status, enzyme activity, or substrate specificity.
