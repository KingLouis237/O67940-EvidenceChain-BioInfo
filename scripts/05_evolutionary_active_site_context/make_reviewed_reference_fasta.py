#!/usr/bin/env python3

import csv
from pathlib import Path
import textwrap

curation_path = Path("results/homolog_context/O67940_vs_swissprot_jackhmmer_N5.initial_curation.tsv")
swissprot_fasta = Path("data/databases/uniprot_sprot_2026-07-04/uniprot_sprot.fasta")
reference_fasta = Path("data/reference_sequences/O67940_2Q6O_1RQP_chainA_sequences.fasta")
out_path = Path("results/homolog_context/O67940_reviewed_swissprot_reference_set.fasta")


def read_fasta(path):
    records = {}
    header = None
    seq_parts = []

    for line in path.read_text().splitlines():
        if line.startswith(">"):
            if header is not None:
                records[header] = "".join(seq_parts)
            header = line[1:]
            seq_parts = []
        else:
            seq_parts.append(line.strip())

    if header is not None:
        records[header] = "".join(seq_parts)

    return records


def write_record(handle, header, sequence):
    handle.write(f">{header}\n")
    handle.write("\n".join(textwrap.wrap(sequence, width=60)))
    handle.write("\n")


curated = []

with curation_path.open() as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    for row in reader:
        curated.append(row)

swissprot_records = read_fasta(swissprot_fasta)
reference_records = read_fasta(reference_fasta)

with out_path.open("w") as out:
    for header, sequence in reference_records.items():
        write_record(out, header, sequence)

    for row in curated:
        target_id = row["target_id"]
        matches = [
            (header, seq)
            for header, seq in swissprot_records.items()
            if header.startswith(target_id)
        ]

        if len(matches) != 1:
            raise SystemExit(f"Expected 1 match for {target_id}, found {len(matches)}")

        original_header, sequence = matches[0]

        new_header = (
            f"{row['short_name']} | {row['target_id']} | "
            f"group={row['annotation_group']} | "
            f"domain_pattern={row['domain_pattern']} | "
            f"decision={row['curation_decision']}"
        )

        write_record(out, new_header, sequence)

print(f"Wrote {len(reference_records) + len(curated)} sequences to {out_path}")
