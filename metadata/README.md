# Metadata files

This folder keeps the reproducibility records for the project.

## source_provenance.tsv

Records where input files or downloaded resources came from.

Expected columns:

- resource
- accession_or_id
- url_or_source
- date_accessed
- local_output_file
- purpose

This file should stay tab-separated and machine-readable.

## checksums_sha256.txt

Records SHA256 checksums for important input, output, script, and report files.

The format is:

checksum  path

If a file is regenerated intentionally, the checksum should be updated.
