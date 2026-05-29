# Metadata folder

This folder records provenance and reproducibility information for the re-analysis.

## Files

- `source_provenance.tsv`
  - Records the source, accession/ID, URL or API endpoint, access date, local output file, and purpose for the main downloaded inputs.

- `checksums_sha256.txt`
  - Contains SHA256 checksums for key raw and processed files. These act as file fingerprints and help verify that the same files are being used later.

## Why this matters

The original article noted that its analysis reflected the databases available at the time of writing. Because databases change, this re-analysis records access dates, exact downloaded files, API endpoints, and checksums. This makes the workflow more transparent and easier to audit.
