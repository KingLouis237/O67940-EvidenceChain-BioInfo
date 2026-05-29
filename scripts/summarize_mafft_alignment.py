from pathlib import Path
from itertools import combinations

alignment_path = Path("results/sequence_alignment/O67940_2Q6O_1RQP_chainA_mafft_alignment.fasta")
summary_path = Path("results/sequence_alignment/O67940_2Q6O_1RQP_alignment_summary.tsv")

def read_fasta(path):
    records = {}
    current_id = None
    chunks = []

    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith(">"):
                if current_id is not None:
                    records[current_id] = "".join(chunks)

                current_id = line[1:].split()[0]
                chunks = []
            else:
                chunks.append(line)

        if current_id is not None:
            records[current_id] = "".join(chunks)

    return records

records = read_fasta(alignment_path)

if not records:
    raise ValueError("No alignment records found.")

aligned_lengths = {len(seq) for seq in records.values()}
if len(aligned_lengths) != 1:
    raise ValueError(f"Aligned sequences have different lengths: {aligned_lengths}")

aligned_length = aligned_lengths.pop()

def pairwise_identity(seq1, seq2):
    compared = 0
    identical = 0

    for a, b in zip(seq1, seq2):
        # Ignore columns where either sequence has a gap.
        if a == "-" or b == "-":
            continue
        compared += 1
        if a == b:
            identical += 1

    if compared == 0:
        return 0, 0, 0.0

    return identical, compared, identical / compared

with summary_path.open("w") as out:
    out.write("section\titem\tvalue\n")

    out.write(f"alignment\taligned_length\t{aligned_length}\n")

    for record_id, seq in records.items():
        gap_count = seq.count("-")
        ungapped_length = len(seq.replace("-", ""))
        out.write(f"sequence\t{record_id}_ungapped_length\t{ungapped_length}\n")
        out.write(f"sequence\t{record_id}_gap_count\t{gap_count}\n")

    for id1, id2 in combinations(records.keys(), 2):
        identical, compared, identity = pairwise_identity(records[id1], records[id2])
        pair_label = f"{id1}_vs_{id2}"
        out.write(f"pairwise\t{pair_label}_identical_positions\t{identical}\n")
        out.write(f"pairwise\t{pair_label}_compared_positions\t{compared}\n")
        out.write(f"pairwise\t{pair_label}_identity_no_gap_columns\t{identity:.4f}\n")

print(f"Wrote alignment summary to {summary_path}")
