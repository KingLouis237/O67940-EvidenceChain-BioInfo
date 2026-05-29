# Methods in Bioinformatics re-analysis

## Project title

Critical review and modern re-analysis of a structure-guided workflow for protein function prediction.

## Case-study protein

- UniProt accession: O67940
- Entry name: O67940_AQUAE
- Organism: Aquifex aeolicus strain VF5
- Original paper: Mazumder and Vasudevan (2008), Structure-Guided Comparative Analysis of Proteins.

## Project aim

This project critically reviews and performs a modern re-analysis of the evidence chain used to infer the function of O67940_AQUAE. The goal is not to reproduce every historical 2008 database output exactly, but to test whether modern annotation, family/domain, and structural resources still support the original broad functional inference.

## Directory structure

- `data/`: raw downloaded input files and database records
- `scripts/`: reusable scripts
- `results/`: processed tables and outputs
- `figures/`: figures, screenshots, and visual outputs
- `notes/`: interpretation notes, workflow logs, and decisions

## Completed steps

### Step 1 — UniProt current record check

Current UniProtKB record retrieved and parsed.

Main finding:
O67940_AQUAE remains an unreviewed TrEMBL entry named “Uncharacterized protein,” with PE=3 inferred from homology and no UniProt FUNCTION comment, GO annotation, or PDB cross-reference. It contains InterPro, Pfam, eggNOG, KEGG, and AlphaFoldDB cross-references.

### Step 2 — InterPro/Pfam metadata retrieval

InterPro and Pfam metadata were retrieved for all family/domain cross-references found in the current UniProtKB record.

Main finding:
O67940_AQUAE is assigned to the S-adenosyl-L-methionine hydroxide adenosyltransferase family, with predicted N-terminal and C-terminal SAM_HAT domains. This supports broad SAM-related family/domain membership, but does not resolve precise chlorinase or fluorinase specificity.

## Next planned step

Retrieve and analyze the AlphaFoldDB predicted structure for O67940_AQUAE, since the current UniProt record has an AlphaFoldDB cross-reference but no PDB cross-reference.

## Reproducibility notes

The computational workflow is organized around raw data, scripts, processed results, interpretation notes, and report drafts.

Additional reproducibility files:

- `environment.yml`: exported conda environment used for the analysis.
- `metadata/source_provenance.tsv`: source table for downloaded files and API-derived inputs.
- `metadata/checksums_sha256.txt`: SHA256 checksums for key files.
- `notes/workflow_log.md`: chronological workflow log, including errors, corrections, and interpretation decisions.

Important correction:
The AlphaFoldDB model files were not hardcoded blindly. An initial attempt using guessed v4 file names produced invalid 127-byte files. The AlphaFoldDB API was then queried, which returned `latestVersion: 6`. The analysis therefore uses the API-reported v6 files.
