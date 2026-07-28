#!/usr/bin/env python3

from pathlib import Path
import csv
import textwrap

alignment_path = Path("results/sequence_alignment/O67940_reviewed_swissprot_reference_set_mafft_alignment.fasta")
out_fasta = Path("results/phylogeny/O67940_reviewed_swissprot_reference_set_phylogeny_input.fasta")
out_map = Path("results/phylogeny/O67940_reviewed_swissprot_reference_set_label_map.tsv")


def read_fasta(path):
    records = []
    header = None
    seq_parts = []

    for line in path.read_text().splitlines():
        if line.startswith(">"):
            if header is not None:
                records.append((header, "".join(seq_parts)))
            header = line[1:]
            seq_parts = []
        else:
            seq_parts.append(line.strip())

    if header is not None:
        records.append((header, "".join(seq_parts)))

    return records


def short_label(header):
    return header.split("|")[0].strip()


records = read_fasta(alignment_path)

seen = set()

with out_fasta.open("w") as fasta_handle, out_map.open("w", newline="") as map_handle:
    writer = csv.writer(map_handle, delimiter="\t")
    writer.writerow(["short_label", "original_header"])

    for header, sequence in records:
        label = short_label(header)

        if label in seen:
            raise SystemExit(f"Duplicate short label found: {label}")

        seen.add(label)

        fasta_handle.write(f">{label}\n")
        fasta_handle.write("\n".join(textwrap.wrap(sequence, width=80)))
        fasta_handle.write("\n")

        writer.writerow([label, header])

print(f"Wrote {len(records)} records to {out_fasta}")
print(f"Wrote label map to {out_map}")
