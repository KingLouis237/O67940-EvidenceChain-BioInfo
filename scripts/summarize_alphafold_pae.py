from pathlib import Path
import json
import statistics

pae_path = Path("data/alphafold/AF-O67940-F1-predicted_aligned_error_v6.json")
out_path = Path("results/alphafold/O67940_alphafold_pae_summary.txt")
out_path.parent.mkdir(parents=True, exist_ok=True)

with pae_path.open() as f:
    data = json.load(f)

# AlphaFoldDB PAE JSON is commonly a list with one dictionary inside.
# We inspect both possibilities to make the script robust.
if isinstance(data, list):
    record = data[0]
elif isinstance(data, dict):
    record = data
else:
    raise TypeError(f"Unexpected PAE JSON structure: {type(data)}")

pae = record.get("predicted_aligned_error")
max_pae = record.get("max_predicted_aligned_error", "NA")

if pae is None:
    raise KeyError("Could not find 'predicted_aligned_error' in the PAE JSON file.")

n = len(pae)

# Flatten all pairwise PAE values into one list
values = [float(x) for row in pae for x in row]

def count_range(low, high=None):
    if high is None:
        return sum(v >= low for v in values)
    return sum(low <= v < high for v in values)

def mean_region(row_start, row_end, col_start, col_end):
    region_values = []
    for i in range(row_start, row_end):
        for j in range(col_start, col_end):
            region_values.append(float(pae[i][j]))
    return statistics.mean(region_values)

# Approximate domain split for beginner-level first pass:
# N-terminal half = residues 1-125
# C-terminal half = residues 126-251
# Later, we can refine this using InterPro domain boundaries if available.
mid = n // 2

nterm_mean = mean_region(0, mid, 0, mid)
cterm_mean = mean_region(mid, n, mid, n)
between_mean_1 = mean_region(0, mid, mid, n)
between_mean_2 = mean_region(mid, n, 0, mid)
between_mean = statistics.mean([between_mean_1, between_mean_2])

with out_path.open("w") as out:
    out.write("AlphaFold PAE summary for O67940_AQUAE\n")
    out.write("=" * 50 + "\n\n")

    out.write(f"Input PAE JSON: {pae_path}\n")
    out.write(f"PAE matrix size: {n} x {n}\n")
    out.write(f"Maximum possible/reported PAE: {max_pae}\n\n")

    out.write("Overall PAE statistics\n")
    out.write("-" * 30 + "\n")
    out.write(f"Mean PAE: {statistics.mean(values):.2f} Å\n")
    out.write(f"Median PAE: {statistics.median(values):.2f} Å\n")
    out.write(f"Minimum PAE: {min(values):.2f} Å\n")
    out.write(f"Maximum PAE: {max(values):.2f} Å\n\n")

    out.write("PAE ranges across residue pairs\n")
    out.write("-" * 30 + "\n")
    out.write(f"Low PAE (<5 Å): {sum(v < 5 for v in values)} residue pairs\n")
    out.write(f"Moderate PAE (5-10 Å): {count_range(5, 10)} residue pairs\n")
    out.write(f"High PAE (10-20 Å): {count_range(10, 20)} residue pairs\n")
    out.write(f"Very high PAE (>=20 Å): {count_range(20)} residue pairs\n\n")

    out.write("Approximate region-level PAE\n")
    out.write("-" * 30 + "\n")
    out.write(f"N-terminal half internal mean PAE: {nterm_mean:.2f} Å\n")
    out.write(f"C-terminal half internal mean PAE: {cterm_mean:.2f} Å\n")
    out.write(f"Between-halves mean PAE: {between_mean:.2f} Å\n\n")

    out.write("Interpretation guide\n")
    out.write("-" * 30 + "\n")
    out.write("Low PAE between regions means AlphaFold is confident about their relative positions.\n")
    out.write("High PAE between regions means each region may be locally well predicted, but their relative arrangement is uncertain.\n")
    out.write("This first summary uses a rough N-terminal/C-terminal split; later, domain boundaries can be refined using InterPro/Pfam coordinates if available.\n")

print(f"Wrote summary to {out_path}")
