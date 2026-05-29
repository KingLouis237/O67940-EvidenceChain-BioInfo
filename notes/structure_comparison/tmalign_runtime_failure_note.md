# Step 5C — TM-align runtime failure

## Aim

The goal of this step was to run pairwise structural alignments between:

- O67940_AQUAE AlphaFold chain A and 2Q6O chain A
- O67940_AQUAE AlphaFold chain A and 1RQP chain A
- 2Q6O chain A and 1RQP chain A

## What happened

TM-align was installed and the executable was found at:

`/home/abane_ashu/miniconda3/envs/methods_bioinfo/bin/TMalign`

The help output reported:

`TM-align Version 20240303`

However, when TM-align was run on the first real structure pair, it failed with:

`Illegal instruction (core dumped)`

The exit code was:

`132`

## Why this matters

The input structure files appear valid. The extracted chain-specific PDB files exist, contain ATOM records, and have expected sizes:

- O67940_AQUAE AlphaFold chain A: 2007 ATOM records
- 2Q6O chain A: 2015 ATOM records
- 1RQP chain A: 2220 ATOM records

Therefore, the failure is most likely not caused by missing or empty input files. An `Illegal instruction` error usually suggests that the installed binary is not compatible with the CPU/WSL environment.

## Decision

No TM-align structural result will be interpreted from this failed run. The next step is to try a different TM-align build/version or another structural alignment tool and document the correction.
tmalign                    20240303         hd63eeec_0            bioconda

## Successful test after version correction

After replacing the crashing TM-align build with the older working build, a test alignment between O67940_AQUAE AlphaFold chain A and 2Q6O chain A completed successfully. The test output was moved to:

`results/structure_comparison/tmalign_raw/test_runs/test_tmalign_O67940_vs_2Q6O.txt`

The final pairwise results are stored separately in:

`results/structure_comparison/tmalign_pairwise_summary.tsv`
