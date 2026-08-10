# Evolutionary and active-site context module

This module contains the publication-upgrade analyses for O67940_AQUAE.

The point is not to make a louder claim. The point is to test whether the earlier interpretation still holds when broader homolog context, residue conservation, and active-site/interface evidence are added.

## Main input

Validated query FASTA:

`data/O67940_AQUAE.fasta`

This file contains one O67940_AQUAE sequence of 251 amino acids and is already tracked in provenance and checksums.

## Current tool state

Available:

- HMMER / JackHMMER
- MAFFT

Already checked:

- `jackhmmer` is available inside the `methods_bioinfo` Conda environment.
- HMMER version: 3.4
- MAFFT version: 7.525

## Planned order

1. choose and document the homolog-search database;
2. run JackHMMER using `data/O67940_AQUAE.fasta`;
3. inspect and parse hits;
4. curate the homolog set;
5. build a multiple sequence alignment;
6. infer phylogenetic placement;
7. map key residues across the alignment;
8. compare O67940, 2Q6O, and 1RQP residue patterns;
9. add active-site and interface context.

## Output folders

Homolog search:

`results/homolog_context/`

Phylogeny and alignment:

`results/phylogeny/`

Residue conservation:

`results/residue_conservation/`

Active-site structure:

`results/active_site_structure/`

Interface context:

`results/interface_context/`

Figures:

`figures/publication/`

Logs:

`logs/05_evolutionary_active_site_context/`

## Interpretation rule

This module can strengthen or weaken the computational annotation-transfer argument.

It cannot prove enzyme activity.

It cannot prove substrate specificity.

It cannot replace biochemical validation.



## Reproducing the broader homolog-context analysis

The current broader-homolog evidence layer can be reproduced in the following order.

### 1. Candidate-space survey

```bash
python scripts/05_evolutionary_active_site_context/survey_uniprot_broader_candidate_space.py
```

This records the size and broad annotation/taxonomic composition of the PF01887/PF20257 UniProtKB candidate space.

### 2. Protein-name overlap

```bash
python scripts/05_evolutionary_active_site_context/measure_uniprot_name_query_overlap.py
```

This tests whether fluorinase, chlorinase, and hydrolase protein-name queries behave as independent annotation classes.

### 3. Freeze the broader candidate set

```bash
python scripts/05_evolutionary_active_site_context/download_uniprot_pfam_candidate_set.py
```

This creates the fixed candidate FASTA and metadata used for downstream sequence analysis.

### 4. PHMMER ranking

```bash
scripts/05_evolutionary_active_site_context/run_broader_phmmer.sh
```

Then:

```bash
python scripts/05_evolutionary_active_site_context/parse_broader_phmmer_results.py
python scripts/05_evolutionary_active_site_context/summarize_broader_phmmer_diagnostics.py
```

These steps rank the frozen candidate set relative to O67940 and examine score, coverage, and reviewed-anchor behaviour.

### 5. Audit candidates outside Bacteria and Archaea

```bash
python scripts/05_evolutionary_active_site_context/audit_non_prokaryotic_uniprot_candidates.py
python scripts/05_evolutionary_active_site_context/enrich_non_prokaryotic_candidate_audit.py
```

These scripts identify the ten non-Bacteria/non-Archaea records and retrieve their UniProt taxonomy and annotation-evidence context.

### 6. Prepare the CPU-compatible MMseqs2 binary

```bash
scripts/05_evolutionary_active_site_context/setup_mmseqs2_sse41.sh
```

The project uses the explicitly pinned SSE4.1 binary documented in `tools/README.md`.

### 7. Redundancy sensitivity analysis

```bash
scripts/05_evolutionary_active_site_context/run_mmseqs_redundancy_survey.sh
```

Then:

```bash
python scripts/05_evolutionary_active_site_context/summarize_mmseqs_redundancy_survey.py
```

The survey compares 95%, 90%, 80%, and 70% identity at 80% bidirectional coverage.

### 8. Independent checks used for the redundancy decision

Cluster counts were independently checked directly from the raw MMseqs membership files:

```bash
for ID in 95 90 80 70
do
    FILE="results/homolog_context/redundancy_mmseqs/O67940_mmseqs_id${ID}_cov80_clusters.tsv"

    printf "ID%s\t" "$ID"

    cut -f1 "$FILE" |
        sort -u |
        wc -l
done
```

Expected current results:

```text
ID95    3606
ID90    2858
ID80    1816
ID70    1181
```

The number of distinct clusters occupied by O67940 plus the eleven reviewed anchors at the selected 90% threshold was checked with:

```bash
awk -F'\t' '
NR > 1 && $1 == "0.90" {
    print $3
}
' results/homolog_context/redundancy_mmseqs/O67940_mmseqs_anchor_cluster_membership.tsv |
    sort -u |
    wc -l
```

Expected result:

```text
12
```

This confirms that all twelve tracked sequences remain in distinct clusters at the selected redundancy threshold.
