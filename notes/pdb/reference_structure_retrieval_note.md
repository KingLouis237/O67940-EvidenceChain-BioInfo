# Step 4 — Reference structure retrieval: 2Q6O and 1RQP

## Aim

This step retrieves the experimentally solved reference structures used in the original article to interpret O67940_AQUAE.

The reference structures are:

- 2Q6O: chlorinase-related reference structure
- 1RQP: fluorinase reference structure

## Why this step matters

The AlphaFoldDB model gives a predicted structure for O67940_AQUAE, but prediction confidence alone does not tell us whether the protein is more chlorinase-like or fluorinase-like.

To test the original interpretation, the query model must be compared against experimentally characterized reference structures. Therefore, 2Q6O and 1RQP are retrieved from RCSB PDB and brought into the same reproducible workflow.

## Why both PDB and mmCIF were downloaded

The mmCIF format is the modern structural-data format and preserves richer metadata. The PDB format is older but easier to inspect quickly from the command line using commands such as `head`, `grep`, and `wc`.

For this reason, both formats were downloaded:

- `.cif`: preferred modern structure record
- `.pdb`: convenient for quick validation and simple parsing

## Quality-control checks

The download script checks:

1. whether each file was downloaded;
2. whether the file size is suspiciously small;
3. how many `ATOM` records are present in the PDB file.

This matters because a `curl` or download command can appear successful even if the downloaded file is actually an error page or incomplete file.

## Interpretation rule

2Q6O and 1RQP are reference structures, not final answers. They provide experimentally solved structural anchors for comparison. Functional interpretation still requires structural comparison, sequence alignment, and functional-residue mapping.

## Download validation result

The download summary confirmed that all four reference structure files were retrieved successfully.

| PDB ID | Format | File size | ATOM records | Status |
| 2Q6O | cif | 493,999 bytes | NA | OK |
| 2Q6O | pdb | 393,660 bytes | 4,030 | OK |
| 1RQP | cif | 1,473,603 bytes | NA | OK |
| 1RQP | pdb | 1,273,482 bytes | 6,660 | OK |

The PDB files contain thousands of ATOM records, confirming that they are valid coordinate files rather than failed downloads or error pages.
