#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict, Counter
import csv
import hashlib
import statistics


FASTA = Path(
    "data/databases/O67940_uniprot_pfam_candidates/"
    "candidate_sequences.fasta"
)

CLUSTER_DIR = Path(
    "results/homolog_context/redundancy_mmseqs"
)

OUT_SUMMARY = CLUSTER_DIR / "O67940_mmseqs_redundancy_summary.tsv"

OUT_ANCHORS = (
    CLUSTER_DIR /
    "O67940_mmseqs_anchor_cluster_membership.tsv"
)

OUT_EUK = (
    CLUSTER_DIR /
    "O67940_mmseqs_non_prokaryotic_cluster_membership.tsv"
)

OUT_DUPLICATES = (
    CLUSTER_DIR /
    "O67940_exact_duplicate_sequence_groups.tsv"
)

OUT_LARGEST = (
    CLUSTER_DIR /
    "O67940_mmseqs_largest_clusters.tsv"
)

EUK_FILE = Path(
    "results/homolog_context/"
    "O67940_uniprot_non_bacteria_archaea_candidates.tsv"
)


REVIEWED = {
    "O58212",
    "Q5SLF5",
    "Q70GK9",
    "A0A1G9FQX8",
    "W0W999",
    "R4LHX8",
    "W8JNL4",
    "A4X3Q0",
    "A4X4S2",
    "A8M783",
    "Q59045",
}

ANCHORS = {"O67940"} | REVIEWED


def accession(identifier):
    """
    Extract UniProt accession from identifiers such as:
    tr|O67940|O67940_AQUAE
    sp|Q70GK9|FLA_STRCT

    If no pipes are present, return the identifier itself.
    """
    identifier = identifier.strip().split()[0]

    parts = identifier.split("|")

    if len(parts) >= 2:
        return parts[1]

    return identifier


def read_fasta(path):
    records = []

    header = None
    seq = []

    with path.open() as handle:
        for line in handle:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                if header is not None:
                    records.append(
                        (header, "".join(seq))
                    )

                header = line[1:]
                seq = []

            else:
                seq.append(line)

    if header is not None:
        records.append(
            (header, "".join(seq))
        )

    return records


def percentile(values, fraction):
    values = sorted(values)

    index = round(
        (len(values) - 1) * fraction
    )

    return values[index]


# --------------------------------------------------
# 1. Exact sequence duplication in the input FASTA
# --------------------------------------------------

records = read_fasta(FASTA)

if len(records) != 4432:
    raise SystemExit(
        f"Expected 4432 FASTA records, found {len(records)}"
    )

sequence_groups = defaultdict(list)

for header, sequence in records:
    sequence_groups[sequence].append(
        accession(header)
    )

unique_sequence_count = len(sequence_groups)

duplicate_groups = [
    (sequence, members)
    for sequence, members in sequence_groups.items()
    if len(members) > 1
]

duplicate_record_count = sum(
    len(members) - 1
    for _, members in duplicate_groups
)

with OUT_DUPLICATES.open("w", newline="") as handle:
    writer = csv.writer(
        handle,
        delimiter="\t",
    )

    writer.writerow([
        "sequence_sha256",
        "sequence_length",
        "group_size",
        "accessions",
    ])

    for sequence, members in sorted(
        duplicate_groups,
        key=lambda item: (
            -len(item[1]),
            sorted(item[1])[0],
        ),
    ):
        digest = hashlib.sha256(
            sequence.encode()
        ).hexdigest()

        writer.writerow([
            digest,
            len(sequence),
            len(members),
            ",".join(sorted(members)),
        ])


# --------------------------------------------------
# 2. Non-prokaryotic accessions
# --------------------------------------------------

with EUK_FILE.open() as handle:
    euk_accessions = {
        row["Entry"]
        for row in csv.DictReader(
            handle,
            delimiter="\t",
        )
    }


# --------------------------------------------------
# 3. Parse each clustering threshold
# --------------------------------------------------

thresholds = ["95", "90", "80", "70"]

summary_rows = []
anchor_rows = []
euk_rows = []
largest_rows = []


for threshold in thresholds:

    path = CLUSTER_DIR / (
        f"O67940_mmseqs_id{threshold}_"
        "cov80_clusters.tsv"
    )

    clusters = defaultdict(list)
    member_seen = Counter()

    with path.open() as handle:
        for raw in handle:
            raw = raw.rstrip("\n")

            if not raw:
                continue

            fields = raw.split("\t")

            if len(fields) < 2:
                raise SystemExit(
                    f"Malformed cluster row in {path}: "
                    f"{raw}"
                )

            representative = accession(fields[0])
            member = accession(fields[1])

            clusters[representative].append(member)
            member_seen[member] += 1


    assignment_count = sum(
        len(members)
        for members in clusters.values()
    )

    unique_members = len(member_seen)

    duplicated_assignments = sum(
        count - 1
        for count in member_seen.values()
        if count > 1
    )

    cluster_sizes = [
        len(members)
        for members in clusters.values()
    ]

    singleton_count = sum(
        size == 1
        for size in cluster_sizes
    )

    multi_count = sum(
        size > 1
        for size in cluster_sizes
    )

    largest_size = max(cluster_sizes)

    summary_rows.append({
        "identity_threshold":
            f"0.{threshold}",
        "coverage_threshold":
            "0.80",
        "input_records":
            len(records),
        "unique_input_sequences":
            unique_sequence_count,
        "exact_duplicate_excess_records":
            duplicate_record_count,
        "assignment_rows":
            assignment_count,
        "unique_members":
            unique_members,
        "duplicate_member_assignments":
            duplicated_assignments,
        "cluster_count":
            len(clusters),
        "singleton_clusters":
            singleton_count,
        "multi_member_clusters":
            multi_count,
        "largest_cluster":
            largest_size,
        "median_cluster_size":
            f"{statistics.median(cluster_sizes):.2f}",
        "mean_cluster_size":
            f"{statistics.mean(cluster_sizes):.4f}",
        "p90_cluster_size":
            percentile(cluster_sizes, 0.90),
    })


    member_to_rep = {}

    for representative, members in clusters.items():
        for member in members:
            member_to_rep[member] = representative


    # ----------------------------------------------
    # Track O67940 + reviewed anchors
    # ----------------------------------------------

    for anchor in sorted(ANCHORS):

        representative = member_to_rep.get(anchor)

        if representative is None:
            anchor_rows.append({
                "identity_threshold":
                    f"0.{threshold}",
                "accession":
                    anchor,
                "representative":
                    "",
                "cluster_size":
                    "",
                "is_representative":
                    "",
            })

            continue

        anchor_rows.append({
            "identity_threshold":
                f"0.{threshold}",
            "accession":
                anchor,
            "representative":
                representative,
            "cluster_size":
                len(clusters[representative]),
            "is_representative":
                "yes"
                if representative == anchor
                else "no",
        })


    # ----------------------------------------------
    # Track 10 eukaryotic candidates
    # ----------------------------------------------

    for candidate in sorted(euk_accessions):

        representative = member_to_rep.get(candidate)

        if representative is None:
            euk_rows.append({
                "identity_threshold":
                    f"0.{threshold}",
                "accession":
                    candidate,
                "representative":
                    "",
                "cluster_size":
                    "",
                "is_representative":
                    "",
                "cluster_contains_other_euk":
                    "",
                "other_euk_accessions":
                    "",
            })

            continue

        members = clusters[representative]

        other_euk = sorted(
            set(members) &
            euk_accessions -
            {candidate}
        )

        euk_rows.append({
            "identity_threshold":
                f"0.{threshold}",
            "accession":
                candidate,
            "representative":
                representative,
            "cluster_size":
                len(members),
            "is_representative":
                "yes"
                if representative == candidate
                else "no",
            "cluster_contains_other_euk":
                "yes"
                if other_euk
                else "no",
            "other_euk_accessions":
                ",".join(other_euk),
        })


    # ----------------------------------------------
    # Top 20 largest clusters
    # ----------------------------------------------

    sorted_clusters = sorted(
        clusters.items(),
        key=lambda item: (
            -len(item[1]),
            item[0],
        ),
    )

    for rank, (
        representative,
        members,
    ) in enumerate(
        sorted_clusters[:20],
        start=1,
    ):

        largest_rows.append({
            "identity_threshold":
                f"0.{threshold}",
            "size_rank":
                rank,
            "representative":
                representative,
            "cluster_size":
                len(members),
            "contains_O67940":
                "yes"
                if "O67940" in members
                else "no",
            "reviewed_anchor_count":
                len(
                    set(members) &
                    REVIEWED
                ),
            "non_prokaryotic_count":
                len(
                    set(members) &
                    euk_accessions
                ),
        })


# --------------------------------------------------
# Write summaries
# --------------------------------------------------

with OUT_SUMMARY.open("w", newline="") as handle:

    fields = [
        "identity_threshold",
        "coverage_threshold",
        "input_records",
        "unique_input_sequences",
        "exact_duplicate_excess_records",
        "assignment_rows",
        "unique_members",
        "duplicate_member_assignments",
        "cluster_count",
        "singleton_clusters",
        "multi_member_clusters",
        "largest_cluster",
        "median_cluster_size",
        "mean_cluster_size",
        "p90_cluster_size",
    ]

    writer = csv.DictWriter(
        handle,
        fieldnames=fields,
        delimiter="\t",
    )

    writer.writeheader()
    writer.writerows(summary_rows)


with OUT_ANCHORS.open("w", newline="") as handle:

    fields = [
        "identity_threshold",
        "accession",
        "representative",
        "cluster_size",
        "is_representative",
    ]

    writer = csv.DictWriter(
        handle,
        fieldnames=fields,
        delimiter="\t",
    )

    writer.writeheader()
    writer.writerows(anchor_rows)


with OUT_EUK.open("w", newline="") as handle:

    fields = [
        "identity_threshold",
        "accession",
        "representative",
        "cluster_size",
        "is_representative",
        "cluster_contains_other_euk",
        "other_euk_accessions",
    ]

    writer = csv.DictWriter(
        handle,
        fieldnames=fields,
        delimiter="\t",
    )

    writer.writeheader()
    writer.writerows(euk_rows)


with OUT_LARGEST.open("w", newline="") as handle:

    fields = [
        "identity_threshold",
        "size_rank",
        "representative",
        "cluster_size",
        "contains_O67940",
        "reviewed_anchor_count",
        "non_prokaryotic_count",
    ]

    writer = csv.DictWriter(
        handle,
        fieldnames=fields,
        delimiter="\t",
    )

    writer.writeheader()
    writer.writerows(largest_rows)


print(f"Input FASTA records: {len(records)}")
print(f"Unique amino-acid sequences: {unique_sequence_count}")
print(f"Exact duplicate groups: {len(duplicate_groups)}")
print(f"Excess records due to exact duplicates: {duplicate_record_count}")
print()

for row in summary_rows:
    print(
        f"identity={row['identity_threshold']} "
        f"clusters={row['cluster_count']} "
        f"singletons={row['singleton_clusters']} "
        f"largest={row['largest_cluster']}"
    )

print()
print(f"Wrote: {OUT_SUMMARY}")
print(f"Wrote: {OUT_ANCHORS}")
print(f"Wrote: {OUT_EUK}")
print(f"Wrote: {OUT_DUPLICATES}")
print(f"Wrote: {OUT_LARGEST}")
