from pathlib import Path
import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

FIGURES_DIR = Path("figures/report")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Figure 1: Workflow / evidence-chain overview
# ------------------------------------------------------------

def create_workflow_figure():
    steps = [
        "O67940_AQUAE\ncase-study protein",
        "Current UniProtKB\nrecord check",
        "InterPro/Pfam\nfamily-domain evidence",
        "AlphaFoldDB v6\nmodel + confidence",
        "Reference structures\n2Q6O and 1RQP",
        "TM-align\nstructural comparison",
        "MAFFT\nsequence alignment",
        "Functional-residue\nmapping",
        "Evidence-integrated\ninterpretation",
    ]

    fig, ax = plt.subplots(figsize=(8, 10))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    box_width = 0.72
    box_height = 0.065
    x = 0.14
    y_start = 0.9
    y_gap = 0.095

    for i, step in enumerate(steps):
        y = y_start - i * y_gap

        rect = Rectangle(
            (x, y - box_height / 2),
            box_width,
            box_height,
            fill=False,
            linewidth=1.5,
        )
        ax.add_patch(rect)

        ax.text(
            x + box_width / 2,
            y,
            step,
            ha="center",
            va="center",
            fontsize=10,
        )

        if i < len(steps) - 1:
            ax.annotate(
                "",
                xy=(0.5, y - box_height / 2 - 0.018),
                xytext=(0.5, y - y_gap + box_height / 2 + 0.018),
                arrowprops=dict(arrowstyle="->", linewidth=1.2),
            )

    ax.set_title(
        "Evidence-chain workflow for the modern re-analysis",
        fontsize=13,
        pad=15,
    )

    out_png = FIGURES_DIR / "figure1_workflow_evidence_chain.png"
    out_pdf = FIGURES_DIR / "figure1_workflow_evidence_chain.pdf"
    fig.tight_layout()
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)

    print(f"Wrote {out_png}")
    print(f"Wrote {out_pdf}")


# ------------------------------------------------------------
# Figure 2: AlphaFold pLDDT by residue
# ------------------------------------------------------------

def extract_plddt_from_pdb(pdb_path):
    plddt_by_residue = {}

    with pdb_path.open() as handle:
        for line in handle:
            if not line.startswith("ATOM"):
                continue

            residue_number = int(line[22:26].strip())
            plddt = float(line[60:66].strip())

            # AlphaFold stores the same pLDDT value on all atoms
            # of a residue, so one value per residue is enough.
            plddt_by_residue[residue_number] = plddt

    residues = sorted(plddt_by_residue)
    scores = [plddt_by_residue[r] for r in residues]
    return residues, scores


def create_plddt_figure():
    pdb_path = Path("data/alphafold/AF-O67940-F1-model_v6.pdb")
    residues, scores = extract_plddt_from_pdb(pdb_path)

    fig, ax = plt.subplots(figsize=(9, 4.8))

    ax.plot(residues, scores, linewidth=1.5)

    # UniProt-derived domain boundaries
    ax.axvline(3, linestyle="--", linewidth=1)
    ax.axvline(148, linestyle="--", linewidth=1)
    ax.axvline(171, linestyle="--", linewidth=1)
    ax.axvline(246, linestyle="--", linewidth=1)

    ax.text(75, 72, "N-terminal\nSAM_HAT\n3–148", ha="center", va="bottom", fontsize=9)
    ax.text(208, 72, "C-terminal\nSAM_HAT\n171–246", ha="center", va="bottom", fontsize=9)

    ax.set_xlabel("Residue number")
    ax.set_ylabel("AlphaFold pLDDT")
    ax.set_title("AlphaFoldDB v6 local confidence for O67940_AQUAE")
    ax.set_ylim(60, 101)

    ax.axhline(90, linestyle=":", linewidth=1)
    ax.text(252, 90, "pLDDT 90", va="center", fontsize=8)

    out_png = FIGURES_DIR / "figure2_alphafold_plddt_by_residue.png"
    out_pdf = FIGURES_DIR / "figure2_alphafold_plddt_by_residue.pdf"
    fig.tight_layout()
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)

    print(f"Wrote {out_png}")
    print(f"Wrote {out_pdf}")


# ------------------------------------------------------------
# Figure 3: TM-align structural comparison
# ------------------------------------------------------------

def create_tmalign_figure():
    summary_path = Path("results/structure_comparison/tmalign_pairwise_summary.tsv")

    labels = []
    tm_scores = []

    with summary_path.open() as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            label = row["structure_1"].replace("_chainA", "").replace("_AlphaFold", "")
            label += "\nvs\n"
            label += row["structure_2"].replace("_chainA", "")
            labels.append(label)

            # Use TM-score normalized by chain 2 because TM-align itself
            # recommends using the reference-normalized score.
            tm_scores.append(float(row["tm_score_norm_chain2"]))

    fig, ax = plt.subplots(figsize=(8, 4.8))

    ax.bar(labels, tm_scores)
    ax.set_ylabel("TM-score normalized by chain 2")
    ax.set_title("Pairwise structural similarity from TM-align")
    ax.set_ylim(0, 1.0)

    for i, score in enumerate(tm_scores):
        ax.text(i, score + 0.02, f"{score:.3f}", ha="center", fontsize=9)

    out_png = FIGURES_DIR / "figure3_tmalign_structural_simipng"
    out_pdf = FIGURES_DIR / "figure3_tmalign_structural_similarity.pdf"
    fig.tight_layout()
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)

    print(f"Wrote {out_png}")
    print(f"Wrote {out_pdf}")


if __name__ == "__main__":
    create_workflow_figure()
    create_plddt_figure()
    create_tmalign_figure()
