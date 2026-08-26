# Upgrade decisions

## 2026-07-04 — First homolog-search database

Decision:

Start with UniProtKB/Swiss-Prot as the first JackHMMER database.

Why:

Swiss-Prot is curated and small enough to search locally. It gives a clean first-pass view before moving to broader and noisier databases.

What this can support:

A first look at whether O67940_AQUAE detects reviewed homologs related to known SAM-dependent halogenase-like proteins.

What this cannot prove:

Swiss-Prot alone cannot define the full homolog space around O67940_AQUAE. No hit, or only weak hits, would not mean O67940 lacks homologs. It also cannot prove substrate specificity or enzyme activity.

Next:

Run JackHMMER against the local Swiss-Prot FASTA, then decide whether a broader UniProtKB/UniRef/reference-proteome search is needed.

## Broader homolog-context decisions

### Protein-name annotations are not functional ground truth

The broader UniProtKB candidate survey showed that protein-name queries for fluorinase and chlorinase were almost completely overlapping.

For this reason, UniProt protein names are retained as metadata but are not used as independent functional labels or as the basis for homolog selection.

Broader homolog selection instead uses sequence similarity, coverage, taxonomy, reviewed-reference context, and redundancy structure.

### No hard PHMMER score cutoff was imposed

PHMMER recovered all 4432 PF01887/PF20257 candidates, with no clear score discontinuity separating an obvious homolog subset from the remainder.

Several reviewed functional anchors also showed lower query or target coverage than would survive a strict coverage filter.

In particular, requiring >=90% query and target coverage would retain only two of the eleven reviewed Swiss-Prot anchors.

A hard PHMMER score or coverage threshold was therefore not used to define the broader phylogenetic set.

PHMMER ranking is instead treated as one source of information for later sampling.

### Simple top-N PHMMER selection was rejected

The highest-ranking PHMMER hits are strongly enriched for organisms close to the Aquifex/Aquificota sequence neighbourhood.

Selecting only the top-ranked sequences would therefore overrepresent a narrow taxonomic and evolutionary region.

The final homolog set will instead combine local similarity with taxonomic and sequence diversity.

### Non-prokaryotic candidates were not removed automatically

Ten PF01887/PF20257 candidates fall outside Bacteria and Archaea:

- four Entamoeba proteins
- four Geodia barretti proteins
- two ciliate proteins

All ten are unreviewed and have protein existence inferred from homology.

Several nevertheless show strong PHMMER similarity to O67940.

Their records may represent genuine homologs, horizontal transfer, microbial or symbiont sequence assignment, contamination, assembly artefacts, or annotation/taxonomic problems.

The available evidence cannot distinguish these explanations.

They were therefore retained through the redundancy analysis instead of being removed based on taxonomy alone.

### Redundancy threshold: 90% identity / 80% bidirectional coverage

MMseqs2 clustering was evaluated at 95%, 90%, 80%, and 70% sequence identity with 80% bidirectional coverage.

The resulting cluster counts were:

- 95%: 3606
- 90%: 2858
- 80%: 1816
- 70%: 1181

At 90%, O67940 and all eleven reviewed Swiss-Prot anchors remained in distinct clusters.

At 80% and 70%, several reviewed functional references began collapsing into common clusters.

For this dataset, 90% identity with 80% bidirectional coverage was therefore selected as the first redundancy-pruning level.

This threshold is a sampling decision, not a definition of family membership, orthology, or biochemical function.

### MMseqs2 cluster representatives are not automatically biological representatives

Some reviewed proteins belong to clusters whose MMseqs2 representative is an unreviewed sequence.

The automatically selected cluster representative will therefore not automatically replace reviewed or structurally important references.

O67940 and reviewed anchors will be retained explicitly during construction of the final homolog set.

## Execution-plan review decisions

### DALI precedes the final anchor freeze, not because the cluster table technically depends on it

An independent methodological review highlighted the ordering of the remaining workflow.

DALI is retained before final representative selection because it may reveal additional experimentally characterized structural neighbours that should be considered before phylogenetic inputs are frozen.

This is a reasoned workflow ordering rather than a strict technical dependency: the cluster master table could be built before DALI and subsequently updated.

### Ordinary cluster representatives will not default to PHMMER-best members

Selecting the strongest PHMMER member from every 90% cluster would systematically favour sequences most similar to O67940.

That would introduce query-centred bias into a step whose purpose is redundancy representation.

The working rule is therefore:

- retain O67940 explicitly;
- retain independently verified functional/structural anchors explicitly;
- otherwise use the deterministic MMseqs2 representative.

PHMMER rank remains evidence and metadata rather than the default representative-selection criterion.

### The full 2858-cluster set will be tested before additional sampling

The 2858 clusters will not be reduced solely to make the final tree easier to visualize.

The full representative set will first be evaluated for alignment quality, sequence comparability, phylogenetic information and computational feasibility.

Additional balanced sampling will be introduced only if a documented methodological problem requires it.

Successful computation alone is not sufficient evidence that the full set is scientifically appropriate.

### Global and tree-aware residue analyses are separated

Global residue frequencies require the final MSA but not a phylogenetic tree.

Clade- or neighbourhood-aware residue interpretation requires a supported phylogeny.

Global conservation will therefore be examined after final alignment QC, with phylogenetically informed interpretation performed only after the supported tree is available.

### Phylogenetic software major version will be checked at execution time

The scientific plan requires maximum-likelihood phylogenetic inference, justified substitution-model selection and appropriate support assessment.

It does not require a particular IQ-TREE major version in advance.

The exact stable/local implementation and version will be checked and recorded when the formal phylogenetic analysis begins.

### PLM analysis is not currently justified

Protein-language-model embeddings will not be added as a generic modernization layer.

They will be considered only if a later, explicitly defined scientific question requires information not adequately addressed by the existing sequence, structural and phylogenetic evidence.

This preserves the project rule that scientific questions determine methods, rather than methods generating new scope.

### Structural representation depends on the biological question

The structural analysis uses different representations for different biological questions.

Using one representation throughout would confound protomer tertiary structure, local active-site geometry, and quaternary organization.

**Protomer-level tertiary structure**

Single-chain/protomer comparisons are used for TM-align, DALI, and equivalent fold-level analyses.

For O67940, the AlphaFold monomer is the candidate protomer representation. Its exact PDB sequence, chain composition, residue numbering, and provenance must be validated before it is used as the DALI query.

For experimental references, a particular chain will not be treated as representative solely because it is chain A.

These comparisons address similarity of tertiary architecture independently of differences in oligomeric organization.

**Representative-protomer QC**

Before detailed local comparison, equivalent protein copies within the verified 2Q6O and 1RQP biological assemblies will be compared.

This check will consider whether protomers are effectively equivalent or whether ligand occupancy, interface environment, construct differences, mutations, missing residues, or conformational differences make one copy non-representative.

If the protomers are effectively equivalent, one documented representative chain may be used.

If meaningful differences are present, those differences will be retained rather than choosing a single chain by convention.

**Local ligand and active-site structure**

Local functional interpretation will use experimentally determined ligand-bound reference structures where available.

Mapped O67940 residues will be compared with structurally corresponding residues, neighbouring residues, ligand positions, and local pocket geometry in 2Q6O, 1RQP, and any later validated structural anchor.

Global structural similarity alone will not be treated as evidence of equivalent local chemistry.

**Quaternary and interface structure**

Where the characterized functional site involves neighbouring protomers, the verified biological assemblies of the experimental reference structures will be examined.

The biological assembly will be distinguished from the crystallographic asymmetric unit and from simply taking every chain present in a deposited coordinate file.

**Interpretation of the existing chain-A TM-align results**

The previous O67940-versus-2Q6O and O67940-versus-1RQP chain-A TM-align results remain valid as protomer-level tertiary-structure evidence.

They do not by themselves establish:

- conservation of quaternary architecture;
- conservation of an interface-formed active site;
- equivalent ligand-pocket geometry;
- identical substrate specificity;
- the oligomeric state of O67940.

**O67940 oligomeric state remains unresolved**

The current AlphaFoldDB structure of O67940 is a monomeric prediction.

It does not establish whether O67940 is monomeric, trimeric, hexameric, or adopts another biological assembly.

If the O67940 monomer is later superposed onto a protomer within an experimentally characterized assembly, that comparison may test compatibility with an analogous interface geometry.

It will not be treated as evidence that O67940 actually forms that oligomer.

### DALI will use complementary full-PDB and PDB25 searches

The structural-neighbour search will use both the full experimental PDB and the sequence-redundancy-controlled PDB25 view.

The full PDB is retained because it maximizes recovery of exact experimental structures and closely related entries.

PDB25 is retained because dense deposition of closely related proteins can dominate full-PDB result lists and obscure broader structural-family relationships.

Neither view is treated as independently stronger evidence of function.

The two searches are interpreted together:

- full PDB for comprehensive/exact structural-neighbour recovery;
- PDB25 for a de-redundant structural-family view.

2Q6O and 1RQP remain predefined historical references and will be evaluated separately under DALI rather than counted as independent discoveries.

A DALI Z-score will not be converted into a universal functional or homology threshold. Structural similarity will be evaluated together with aligned length, coverage, domain correspondence, experimental characterization, ligand context, and biological assembly.
