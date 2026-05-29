# Data folder

This folder contains raw downloaded records and database outputs.

## Current files

- `O67940_AQUAE.fasta`
  - FASTA sequence downloaded from UniProt REST API.

- `O67940_uniprot_record.json`
  - Full UniProtKB JSON record for O67940.

- `O67940_uniprot_record_pretty.json`
  - Human-readable formatted version of the full UniProtKB JSON record.

- `interpro_pfam/`
  - Raw JSON metadata files downloaded from the EBI InterPro API for InterPro and Pfam cross-references associated with O67940_AQUAE.

- `alphafold/`
  - Contains AlphaFoldDB API response files and downloaded v6 predicted structure/confidence files for O67940_AQUAE.
  - The API was queried first to identify the current model version and download URLs.
