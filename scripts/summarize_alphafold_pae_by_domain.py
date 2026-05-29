from pathlib import Path
import json
import statistics

pae_path = Path("data/alphafold/AF-O67940-F1-predicted_aligned_error_v6.json")
out_path = Path("results/alphafold/O67940_alphafold_pae_by_domain_summary.txt")
out_path.parent.mkdir(parents=True, exist_ok=True)

with pae_path.open() as f:
    data = json.load(f)

if isinstance(data, list):
    record = data[0]
elif isinstance(data, dict):
    record = data
else:
    raise TypeError(f"Unexpected PAE JSON structure: {type(data)}")

pae = record["predicted_aligned_error"]

# UniProt domain coordinates are 1-based inclusive.
# Python list indices are 0-based and end-exclusive.
domains = {
    "N-terminal SAM_HAT domain (3-148)": (3, 148),
    "C-terminal SAM_HAT domain (171-246)": (171, 246),
    "Inter-domain region (149-170)": (149, 170),
}

def region_values(region_a, region_b):
    start_a, end_a = region_a
    start_b, end_b = region_b

    values = []
    for i in range(start_a - 1, end_a):
        for j in range(start_b - 1, end_b):
            values.append(float(pae[i][j]))
    return values

def summarize(values):
    return {
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values),
        "n_pairs": len(values),
    }

comparisons = [
    (
        "N-terminal domain internal",
        domains["N-terminal SAM_HAT domain (3-148)"],
        domains["N-terminal SAM_HAT domain (3-148)"],
    ),
    (
        "C-terminal domain internal",
        domains["C-terminal SAM_HAT domain (171-246)"],
        domains["C-terminal SAM_HAT domain (171-246)"],
    ),
    (
        "Between N-terminal and C-terminal domains",
        domains["N-terminal SAM_HAT domain (3-148)"],
        domains["C-terminal SAM_HAT domain (171-246)"],
    ),
    (
        "N-terminal domain vs inter-domain region",
        domains["N-terminal SAM_HAT domain (3-148)"],
        domains["Inter-domain region (149-170)"],
    ),
    (
        "C-terminal domain vs inter-domain region",
        domains["C-terminal SAM_HAT domain (171-246)"],
        domains["Inter-domain region (149-170)"],
    ),
]

with out_path.open("w") as out:
    out.write("AlphaFold PAE summary by UniProt domain boundaries for O67940_AQUAE\n")
    out.write("=" * 75 + "\n\n")

    out.write("Domain boundaries used\n")
    out.write("-" * 30 + "\n")
    for name, (start, end) in domains.items():
        out.write(f"{name}: residues {start}-{end}\n")

    out.write("\nPAE interpretation\n")
    out.write("-" * 30 + "\n")
    out.write("Lower PAE means AlphaFold is more confident about relative positioning.\n")
    out.write("Higher PAE means relative positioning should be interpreted more cautiously.\n\n")

    out.write("Domain-level PAE summaries\n")
    out.write("-" * 30 + "\n")

    for label, region_a, region_b in comparisons:
        values = region_values(region_a, region_b)
        stats = summarize(values)

        out.write(f"{label}\n")
        out.write(f"  Residue-pair count: {stats['n_pairs']}\n")
        out.write(f"  Mean PAE: {stats['mean']:.2f} Å\n")
        out.write(f"  Median PAE: {stats['median']:.2f} Å\n")
        out.write(f"  Minimum PAE: {stats['min']:.2f} Å\n")
        out.write(f"  Maximum PAE: {stats['max']:.2f} Å\n\n")

print(f"Wrote domain-level PAE summary to {out_path}")
