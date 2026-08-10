#!/usr/bin/env bash

set -euo pipefail

MMSEQS="tools/mmseqs2_18-8cc5c_sse41/bin/mmseqs"

EXPECTED_MMSEQS_SHA256="0930c12e79b78d5f3546adac8cd7e302a1a0a308b30edb8178f7466f3855ec4f"

INPUT="data/databases/O67940_uniprot_pfam_candidates/candidate_sequences.fasta"

OUTDIR="results/homolog_context/redundancy_mmseqs"
LOGDIR="logs/05_evolutionary_active_site_context"
LOG="${LOGDIR}/O67940_mmseqs_redundancy_survey.log"

mkdir -p "$OUTDIR" "$LOGDIR"

if [[ ! -x "$MMSEQS" ]]; then
    echo "ERROR: MMseqs2 executable not found: $MMSEQS" >&2
    exit 1
fi

if [[ ! -f "$INPUT" ]]; then
    echo "ERROR: input FASTA not found: $INPUT" >&2
    exit 1
fi

ACTUAL_SHA256=$(sha256sum "$MMSEQS" | awk '{print $1}')

if [[ "$ACTUAL_SHA256" != "$EXPECTED_MMSEQS_SHA256" ]]; then
    echo "ERROR: MMseqs2 binary checksum mismatch." >&2
    echo "Expected: $EXPECTED_MMSEQS_SHA256" >&2
    echo "Observed: $ACTUAL_SHA256" >&2
    exit 1
fi

INPUT_COUNT=$(grep -c '^>' "$INPUT")

if [[ "$INPUT_COUNT" -ne 4432 ]]; then
    echo "ERROR: expected 4432 input sequences, observed $INPUT_COUNT" >&2
    exit 1
fi

WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

DB="${WORKDIR}/candidates_db"

{
    echo "Started: $(date)"
    echo "Input: $INPUT"
    echo "Input sequences: $INPUT_COUNT"
    echo "MMseqs2 executable: $MMSEQS"
    echo "MMseqs2 SHA256: $ACTUAL_SHA256"
    echo -n "MMseqs2 version: "
    "$MMSEQS" version
    echo

    "$MMSEQS" createdb \
        "$INPUT" \
        "$DB"

    for SPEC in \
        "95 0.95" \
        "90 0.90" \
        "80 0.80" \
        "70 0.70"
    do
        LABEL=$(echo "$SPEC" | awk '{print $1}')
        IDENTITY=$(echo "$SPEC" | awk '{print $2}')

        CLUSTER_DB="${WORKDIR}/cluster_${LABEL}"
        TMP="${WORKDIR}/tmp_${LABEL}"

        mkdir -p "$TMP"

        echo
        echo "=== Identity ${IDENTITY}; coverage 0.80 ==="

        "$MMSEQS" cluster \
            "$DB" \
            "$CLUSTER_DB" \
            "$TMP" \
            --min-seq-id "$IDENTITY" \
            -c 0.80 \
            --cov-mode 0 \
            --alignment-mode 3 \
            --single-step-clustering 1 \
            --threads 4

        "$MMSEQS" createtsv \
            "$DB" \
            "$DB" \
            "$CLUSTER_DB" \
            "${OUTDIR}/O67940_mmseqs_id${LABEL}_cov80_clusters.tsv"
    done

    echo
    echo "Finished: $(date)"
} > "$LOG" 2>&1

cat > "${OUTDIR}/O67940_mmseqs_redundancy_parameters.tsv" <<'PARAMS'
identity_thresholdcoveragecov_modealignment_modesingle_step_clustering
0.950.80031
0.900.80031
0.800.80031
0.700.80031
PARAMS

echo "MMseqs2 redundancy survey completed."

for FILE in "$OUTDIR"/O67940_mmseqs_id*_cov80_clusters.tsv
do
    printf "%s\t%s pairs\n" \
        "$(basename "$FILE")" \
        "$(wc -l < "$FILE")"
done

echo
echo "Log: $LOG"
