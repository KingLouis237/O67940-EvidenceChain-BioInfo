# 2. Materials and Methods

## 2.1 Source article and project scope

This project re-analysed selected evidence layers from the protein function inference workflow described by Mazumder and Vasudevan (2008), using O67940_AQUAE as the case-study protein. The original article used O67940_AQUAE to illustrate how sequence comparison, domain/family annotation, structural comparison, phylogenetic context, and functional-residue mapping can be combined to support cautious protein-function prediction.

The aim of this work was not to fully reproduce every historical tool and database step from the original ten-step workflow. Instead, the project was designed as a bounded modern computational re-analysis. The focus was on asking whether current databases and modern structural resources still support the original cautious interpretation of O67940_AQUAE as a SAM-dependent halogenase-related protein, while documenting what was reproduced, what was modernized, and what remained outside scope.

## 2.2 Query protein and data sources

The query protein was O67940_AQUAE, corresponding to UniProt accession O67940 from *Aquifex aeolicus* strain VF5. The current UniProtKB FASTA sequence and full JSON record were retrieved using the UniProt REST API (UniProt Consortium, 2025). The JSON record was parsed to extract entry status, protein name, organism, protein existence level, sequence length, molecular weight, database cross-references, Gene Ontology status, PDB cross-reference status, and UniProt FUNCTION comments.

Domain and family evidence was obtained from current InterPro and Pfam cross-references listed in the UniProtKB record (Blum et al., 2025; Mistry et al., 2021). Metadata for the InterPro and Pfam accessions was retrieved from the EBI InterPro API and summarized into a tabular file. This step was used to translate database accessions into interpretable family/domain labels rather than relying only on accession numbers.

Predicted structural information for O67940_AQUAE was obtained from AlphaFoldDB (Varadi et al., 2024). Instead of assuming a fixed model version manually, the AlphaFoldDB API was queried first to identify the current available file URLs and latest version. The v6 AlphaFoldDB model files were then downloaded, including the PDB, mmCIF, binary CIF, and predicted aligned error files. AlphaFoldDB models are based on the AlphaFold protein-structure prediction method (Jumper et al., 2021).

Experimentally solved reference structures were downloaded from RCSB PDB (Burley et al., 2021). The two reference structures were 2Q6O, used as the chlorinase-related reference, and 1RQP, used as the fluorinase reference. Both PDB and mmCIF formats were downloaded. The PDB files were used for command-line inspection, chain extraction, sequence extraction, and structural comparison.

All downloaded source files, URLs, access dates, local paths, and file purposes were documented in the project provenance files.

## 2.3 Project organization and reproducibility

The project was organized into separate directories for raw data, scripts, results, figures, interpretation notes, metadata, and report drafts. This structure was used to keep raw downloaded records separate from processed outputs and final interpretation.

The main folders were:

- `data/` for downloaded database records and structural files;
- `scripts/` for reusable Python scripts;
- `results/` for processed outputs and summary tables;
- `figures/` for report-ready visual outputs;
- `notes/` for workflow decisions, interpretation notes, and troubleshooting;
- `metadata/` for provenance files, checksums, and project inventory;
- `report/` for draft report sections and planning files.

The computational environment was managed with Conda and exported to `environment.yml`. Key files were tracked with SHA256 checksums. Runtime issues and corrections were documented in `notes/workflow_log.md` and in dedicated notes. This was important because the project was treated not only as a biological re-analysis, but also as a reproducibility audit of a published bioinformatics workflow.

## 2.4 UniProt and InterPro/Pfam annotation analysis

The UniProtKB JSON record was parsed using a Python script to produce a concise summary of the current annotation status of O67940_AQUAE. The script extracted whether the entry was reviewed or unreviewed, whether a curated function comment was present, whether Gene Ontology annotations were available, and whether any experimentally solved PDB structure was cross-referenced.

InterPro and Pfam metadata were then retrieved for the cross-references present in the UniProtKB record. The metadata was summarized into a TSV table containing database name, accession, domain or family name, short name, entry type, and available description. This allowed the domain/family interpretation to be based on current database labels rather than only on the original paper.

## 2.5 AlphaFoldDB model retrieval and confidence analysis

The AlphaFoldDB API was queried for O67940 to avoid assuming an outdated file version (Varadi et al., 2024). An initial attempt to download older v4 files produced invalid tiny files, so the API response was used to identify the current v6 model files. The v6 PDB, mmCIF, binary CIF, and predicted aligned error JSON files were then downloaded.

Local model confidence was assessed using pLDDT values stored in the B-factor column of the AlphaFold PDB file. A Python script extracted one pLDDT value per residue and summarized the mean, median, minimum, maximum, and confidence-range counts.

Predicted aligned error was analysed to estimate uncertainty in relative residue positioning. UniProt-derived domain boundaries were used to summarize PAE within the N-terminal SAM_HAT domain, within the C-terminal SAM_HAT domain, and between the two domains. This was used only as predicted structural-confidence evidence, not as proof of biochemical activity.

## 2.6 Reference structure retrieval, inspection, and chain extraction

The reference structures 2Q6O and 1RQP were downloaded from RCSB PDB in both PDB and mmCIF formats. File sizes and ATOM record counts were checked to ensure the downloaded files were valid structural files rather than incomplete downloads or error pages.

The PDB files were inspected to summarize chain content and heteroatom content. Chain A was selected from each reference structure for controlled one-chain comparison. Chain A was also extracted from the O67940_AQUAE AlphaFoldDB model. This produced three comparable chain-level PDB files: O67940_AQUAE AlphaFold chain A, 2Q6O chain A, and 1RQP chain A.

The chain-only approach simplified structural comparison and residue mapping. However, this is also a limitation because ligand binding, oligomeric context, and interface-level effects may not be fully represented by a single-chain comparison.

## 2.7 Structural comparison with TM-align

Pairwise structural comparisons were performed using TM-align (Zhang and Skolnick, 2005). The comparisons were:

1. O67940_AQUAE AlphaFold chain A versus 2Q6O chain A;
2. O67940_AQUAE AlphaFold chain A versus 1RQP chain A;
3. 2Q6O chain A versus 1RQP chain A.

For each comparison, the raw TM-align output was saved, and a summary table was generated containing chain lengths, aligned length, RMSD, sequence identity over aligned residues, and TM-scores normalized by each chain length.

A newer TM-align build initially failed during real structural alignment with an illegal-instruction runtime error. The input PDB files had already been checked and contained valid ATOM records, so this was treated as a likely binary/runtime compatibility issue rather than a biological-data problem. An older Bioconda TM-align build was installed and used successfully. This correction was documented as part of the reproducibility audit.

## 2.8 Sequence alignment with MAFFT

The extracted chain A sequences from O67940_AQUAE, 2Q6O, and 1RQP were aligned using MAFFT with the `--auto` option (Katoh and Standley, 2013). The purpose of this alignment was not to build a full phylogeny, but to create a controlled alignment for residue mapping across the query and the two reference structures.

A Python script summarized the alignment length, gap counts, ungapped sequence lengths, and pairwise sequence identities excluding gap-containing columns. This allowed global sequence similarity to be compared with the structural comparison results.

## 2.9 Functional-residue mapping

Functional residues discussed in the original paper were mapped onto the MAFFT alignment. A custom Python script connected three coordinate systems: PDB residue numbers, ungapped sequence positions, and alignment columns. This allowed residues from 2Q6O and 1RQP to be mapped to corresponding aligned residues in O67940_AQUAE.

A full residue-mapping table was first generated for audit purposes. A focused summary table was then created for the most biologically relevant positions, especially the Val67/Gly127 mapping in O67940_AQUAE. The mapping was interpreted cautiously because it depends on the MAFFT alignment and current PDB residue numbering.

During this step, some C-terminal residues listed for 2Q6O in the original paper did not match the current downloaded coordinate file directly. These discrepancies were verified by direct PDB inspection and kept as limitations rather than ignored.

## 2.10 Evidence integration and figure generation

The main results were integrated into an evidence table separating: the observed result, what it supports, what it does not prove, and the remaining limitation. This table was used to control interpretation and avoid overclaiming.

Report figures were generated from the reproducible outputs. These included a workflow/evidence-chain figure, an AlphaFold pLDDT confidence plot with domain boundaries, a TM-align structural-comparison plot, and a focused residue-mapping figure.

The final interpretation was based on integration of multiple evidence layers rather than on any single tool. Structural similarity, domain annotation, and residue mapping were treated as computational support for a functional hypothesis, not as experimental validation of enzyme activity.
