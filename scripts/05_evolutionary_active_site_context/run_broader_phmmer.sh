#!/usr/bin/env bash

set -euo pipefail

QUERY="data/O67940_AQUAE.fasta"
DB="data/databases/O67940_uniprot_pfam_candidates/candidate_sequences.fasta"

OUTDIR="results/homolog_context/broader_phmmer"
PREFIX="${OUTDIR}/O67940_vs_uniprot_pfam_candidates_phmmer"

LOGDIR="logs/05_evolutionary_active_site_context"
LOG="${LOGDIR}/O67940_vs_uniprot_pfam_candidates_phmmer.log"

mkdir -p "$OUTDIR" "$LOGDIR"

if [[ ! -f "$QUERY" ]]; then
    echo "ERROR: query not found: $QUERY" >&2
    exit 1
fi

if [[ ! -f "$DB" ]]; then
    echo "ERROR: candidate FASTA not found: $DB" >&2
    exit 1
fi

if ! command -v phmmer >/dev/null 2>&1; then
    echo "ERROR: phmmer is not available in the current environment." >&2
    exit 1
fi

{
    echo "Started: $(date)"
    echo "Query: $QUERY"
    echo "Database: $DB"
    echo "PHMMER:"
    phmmer -h 2>&1 | sed -n '1,4p'
    echo
    echo "Parameters: --cpu 4 -E 1e-3 --domE 1e-3 --noali"
    echo

    phmmer \
        --cpu 4 \
        -E 1e-3 \
        --domE 1e-3 \
        --noali \
        -o "${PREFIX}.out" \
        --tblout "${PREFIX}.tblout" \
        --domtblout "${PREFIX}.domtblout" \
        "$QUERY" \
        "$DB"

    echo
    echo "Finished: $(date)"
} > "$LOG" 2>&1

echo "PHMMER completed."
echo "Sequence table: ${PREFIX}.tblout"
echo "Domain table:   ${PREFIX}.domtblout"
echo "Full output:    ${PREFIX}.out"
echo "Log:            ${LOG}"
