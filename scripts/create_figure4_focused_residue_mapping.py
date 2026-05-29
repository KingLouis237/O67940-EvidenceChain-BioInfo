from pathlib import Path
import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

INPUT_TSV = Path("results/residue_mapping/focused_functional_residue_summary.tsv")
FIG_DIR = Path("figures/report")
FIG_DIR.mkdir(parents=True, exist_ok=True)

OUT_PNG = FIG_DIR / "figure4_focused_residue_mapping.png"
OUT_PDF = FIG_DIR / "figure4_focused_residue_mapping.pdf"


def load_key_sites(tsv_path):
    """
    Read the focused residue summary table and extract the two main
    specificity-related aligned sites that are central to interpretation.
    """
    rows = []
    with tsv_path.open() as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rows.append(row)

    site1 = None
    site2 = None

    for row in rows:
        source_res = row["source_paper_residue"]

        # Site 1: Tyr70 / Thr75 comparison
        if source_res in {"Tyr70", "Thr75"} and site1 is None:
            site1 = {
                "title": "Specificity-related site 1",
                "alignment_column": row["alignment_column"],
                "O67940": row["O67940_residue"],
                "2Q6O": row["2Q6O_residue"],
                "1RQP": row["1RQP_residue"],
                "note": "Original paper discussed this as a Tyr/Thr-related position."
            }

        # Site 2: Gly131 / Ser158 comparison
        if source_res in {"Gly131", "Ser158"} and site2 is None:
            site2 = {
                "title": "Specificity-related site 2",
                "alignment_column": row["alignment_column"],
                "O67940": row["O67940_residue"],
                "2Q6O": row["2Q6O_residue"],
                "1RQP": row["1RQP_residue"],
                "note": "Original paper discussed this as a Gly/Ser-related position."
            }

    if site1 is None or site2 is None:
        raise ValueError("Could not recover the two focused residue-mapping sites from the TSV.")

    return [site1, site2]


def draw_site_panel(ax, x0, y0, width, height, site):
    """
    Draw one site panel with three protein rows and the aligned residues.
    """
    # Outer box
    ax.add_patch(Rectangle((x0, y0), width, height, fill=False, linewidth=1.5))

    # Title
    ax.text(
        x0 + width / 2,
        y0 + height - 0.06,
        f"{site['title']}  (alignment column {site['alignment_column']})",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold"
    )

    # Rows
    proteins = [
        ("O67940_AQUAE", site["O67940"]),
        ("2Q6O (chlorinase-related)", site["2Q6O"]),
        ("1RQP (fluorinase)", site["1RQP"]),
    ]

    row_y = [y0 + 0.23, y0 + 0.14, y0 + 0.05]

    for (label, residue), yy in zip(proteins, row_y):
        ax.text(x0 + 0.04, yy, label, ha="left", va="center", fontsize=10)

        # Residue box
        rx = x0 + width - 0.18
        rw = 0.12
        rh = 0.055
        ax.add_patch(Rectangle((rx, yy - rh / 2), rw, rh, fill=False, linewidth=1.2))
        ax.text(rx + rw / 2, yy, residue, ha="center", va="center", fontsize=11, fontweight="bold")

    # Note
    ax.text(
        x0 + width / 2,
        y0 + 0.015,
        site["note"],
        ha="center",
        va="bottom",
        fontsize=8
    )


def main():
    sites = load_key_sites(INPUT_TSV)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.set_title(
        "Focused residue mapping at two specificity-related aligned sites",
        fontsize=13,
        pad=12
    )

    draw_site_panel(ax, x0=0.08, y0=0.52, width=0.84, height=0.30, site=sites[0])
    draw_site_panel(ax, x0=0.08, y0=0.14, width=0.84, height=0.30, site=sites[1])

    # Bottom interpretation text
    ax.text(
        0.5,
        0.04,
        "O67940 shares Thr-like alignment at site 1 less clearly (Val67 vs Thr70/Thr75), "
        "but matches the chlorinase-related reference at site 2 (Gly127 ↔ Gly131) "
        "rather than the fluorinase Ser158.",
        ha="center",
        va="center",
        fontsize=9
    )

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    fig.savefig(OUT_PDF, bbox_inches="tight")
    plt.close(fig)

    print(f"Wrote {OUT_PNG}")
    print(f"Wrote {OUT_PDF}")


if __name__ == "__main__":
    main()
