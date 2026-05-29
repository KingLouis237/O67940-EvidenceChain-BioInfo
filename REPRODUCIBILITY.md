# Reproducibility guide

## Purpose

This file explains how to reproduce and audit the main computational workflow for the O67940_AQUAE modern re-analysis.

The project can be reproduced at two levels:

1. **Re-run from included data**
   - Uses the data files already present in the repository.
   - Regenerates processed outputs, summary tables, and figures.

2. **Full fresh reproduction**
   - Re-downloads raw data from UniProtKB, AlphaFoldDB, InterPro/Pfam, and RCSB PDB.
   - Then reruns downstream scripts.
   - This may not produce byte-identical results forever because public databases, APIs, and software packages change over time.

The goal is not only to make the workflow rerunnable, but also to make it auditable.

## Environment

The workflow was developed in a conda environment named:

    methods_bioinfo

To recreate the environment:

    conda env create -f environment.yml
    conda activate methods_bioinfo

Important tools used include:

- Python
- MAFFT
- TM-align
- matplotlib

Tool setup and version notes are documented in:

- `notes/sequence_alignment/mafft_installation_note.md`
- `notes/structure_chains/tmalign_installation_note.md`
- `notes/environment_note.md`

## Provenance

Input data and external records were obtained from:

- UniProtKB
- EBI InterPro / Pfam
- AlphaFoldDB
- RCSB PDB

Source URLs, local file paths, access dates, and purposes are recorded in:

- `metadata/source_provenance.tsv`

## Checksums

Key files are tracked with SHA256 checksums:

- `metadata/checksums_sha256.txt`

To verify a file manually:

    sha256sum path/to/file

Before final submission or GitHub release, a clean checksum manifest can be regenerated.

## Re-running the workflow from included data

From the project root:

    conda activate methods_bioinfo

Then run the main scripts in this approximate order:

    python scripts/parse_uniprot_O67940.py
    python scripts/fetch_interpro_pfam_metadata.py
    python scripts/summarize_alphafold_plddt.py
    python scripts/summarize_alphafold_pae.py
    python scripts/summarize_alphafold_pae_by_domain.py
    python scripts/fetch_reference_pdb_structures.py
    python scripts/inspect_reference_pdb_contents.py
    python scripts/extract_structure_chain_sequences.py
    python scripts/extract_chainA_structure_files.py
    python scripts/run_tmalign_pairwise.py
    python scripts/summarize_mafft_alignment.py
    python scripts/map_functional_residues_mafft.py
    python scripts/create_focused_residue_mapping_summary.py
    python scripts/create_report_figures.py
    python scripts/create_figure4_focused_residue_mapping.py
    python scripts/create_evidence_integration_table.py
    python scripts/create_evidence_integration_table_short.py

## Manual or semi-manual steps

Some steps were not fully automated during workflow development.

### AlphaFoldDB retrieval

Initial assumed AlphaFold v4 file URLs produced invalid tiny files. The AlphaFoldDB API was queried directly to identify the current latest version, which was v6 at the time of the workflow.

This is documented in:

- `notes/alphafold/alphafold_file_discovery_note.md`
- `notes/workflow_log.md`

### MAFFT alignment

The MAFFT alignment was generated with:

    mafft --auto data/reference_sequences/O67940_2Q6O_1RQP_chainA_sequences.fasta \
      > results/sequence_alignment/O67940_2Q6O_1RQP_chainA_mafft_alignment.fasta

The summary script then parsed the generated alignment.

### TM-align runtime correction

A newer TM-align build was callable but failed during real structural alignment with:

    Illegal instruction (core dumped)

An older Bioconda build was installed and used successfully.

This is documented in:

- `notes/structure_chains/tmalign_installation_note.md`
- `notes/structure_comparison/tmalign_runtime_failure_note.md`

## Important outputs to check

After rerunning the workflow, key outputs should include:

- `results/uniprot_O67940_record_summary.txt`
- `results/O67940_interpro_pfam_metadata.tsv`
- `results/alphafold/O67940_alphafold_plddt_summary.txt`
- `results/alphafold/O67940_alphafold_pae_by_domain_summary.txt`
- `results/structure_comparison/tmalign_pairwise_summary.tsv`
- `results/sequence_alignment/O67940_2Q6O_1RQP_alignment_summary.tsv`
- `results/residue_mapping/focused_functional_residue_summary.tsv`
- `results/evidence_integration/evidence_integration_table_short.tsv`
- `figures/report/`

## Runtime failures are part of the record

This project does not hide corrected or failed steps. Runtime problems are documented because they are part of real computational reproducibility.

Examples include:

- invalid AlphaFold version assumptions;
- TM-align binary/runtime compatibility problems;
- residue-numbering cautions in the current 2Q6O coordinate file.

## Interpretation rule

Reproducing the workflow regenerates computational evidence. It does not experimentally validate the function of O67940_AQUAE.

The strongest defensible conclusion remains:

> Current computational evidence supports a SAM-dependent halogenase-related interpretation for O67940_AQUAE, with evidence leaning closer to the chlorinase-related reference than to direct fluorinase-specific assignment.
