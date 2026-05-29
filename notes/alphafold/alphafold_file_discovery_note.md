# Step 3 — How the AlphaFoldDB files were identified

The AlphaFoldDB file names were not assumed manually. The current UniProtKB record for O67940_AQUAE contains an AlphaFoldDB cross-reference, indicating that a predicted structure exists for the protein.

The corresponding AlphaFoldDB entry page is:

https://alphafold.ebi.ac.uk/entry/O67940

For reproducibility, the current downloadable file URLs were retrieved programmatically from the AlphaFoldDB API:

https://alphafold.ebi.ac.uk/api/prediction/O67940

This API is used because AlphaFoldDB file versions can change. Instead of hardcoding a guessed file name such as `model_v4`, the workflow asks AlphaFoldDB directly for the current `pdbUrl`, `cifUrl`, and `paeDocUrl`.

An initial attempt to download hardcoded `v4` files returned 127-byte files, indicating that the downloads were not valid structure files. These files were discarded before analysis. This check is important because a small file can look like a successful `curl` download but may actually contain an error response rather than biological data.

Interpretation rule:
The AlphaFold structure will be treated as predicted structural evidence, not as experimental proof of enzymatic activity or substrate specificity.

## API result for O67940

The AlphaFoldDB API returned `latestVersion: 6` for O67940. Therefore, the correct downloadable files for this analysis are:

- `AF-O67940-F1-model_v6.pdb`
- `AF-O67940-F1-model_v6.cif`
- `AF-O67940-F1-model_v6.bcif`
- `AF-O67940-F1-predicted_aligned_error_v6.json`

This corrected the earlier assumption that the current model version was v4. The v4 downloads produced only 127-byte files and were removed before analysis.

## Downloaded AlphaFoldDB files

After querying the AlphaFoldDB API, the workflow downloaded the current v6 files for O67940_AQUAE:

- `data/alphafold/AF-O67940-F1-model_v6.pdb`
- `data/alphafold/AF-O67940-F1-model_v6.cif`
- `data/alphafold/AF-O67940-F1-model_v6.bcif`
- `data/alphafold/AF-O67940-F1-predicted_aligned_error_v6.json`

The downloaded file sizes were much larger than the earlier invalid 127-byte v4 files, supporting that these are valid structure/confidence files rather than failed downloads.

Interpretation:
The AlphaFoldDB files provide a predicted structural model and confidence information for O67940_AQUAE. This adds a modern structural evidence layer that was not available in the same way to the original 2008 analysis. However, this remains predicted structural evidence, not experimental proof of enzyme activity.
