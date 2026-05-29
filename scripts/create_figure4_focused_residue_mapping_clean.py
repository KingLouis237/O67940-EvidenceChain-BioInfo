from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

out_dir = Path("figures/report")
out_dir.mkdir(parents=True, exist_ok=True)

png_path = out_dir / "figure4_focused_residue_mapping.png"
pdf_path = out_dir / "figure4_focused_residue_mapping.pdf"

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

def draw_panel(y, title, site_note, rows):
    """
    Draw one clean residue-mapping panel.
    y = top coordinate of panel.
    """

    panel_x = 0.07
    panel_w = 0.86
    panel_h = 0.30

    # Outer panel
    ax.add_patch(
        Rectangle(
            (panel_x, y - panel_h),
            panel_w,
            panel_h,
            fill=False,
            edgecolor="0.25",
            linewidth=1.2,
        )
    )

    # Panel title
    ax.text(
        0.5,
        y - 0.045,
        title,
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
    )

    # Site note below title, above table
    ax.text(
        0.5,
        y - 0.085,
        site_note,
        ha="center",
        va="center",
        fontsize=10.5,
        color="0.25",
    )

    # Table dimensions
    table_x = 0.17
    table_w = 0.66
    table_top = y - 0.12
    table_h = 0.15
    row_h = table_h / 4
    col1_w = 0.43
    col2_w = table_w - col1_w

    # Header
    ax.add_patch(
        Rectangle(
            (table_x, table_top - row_h),
            table_w,
            row_h,
            facecolor="0.92",
            edgecolor="0.55",
            linewidth=0.9,
        )
    )

    ax.text(table_x + col1_w / 2, table_top - row_h / 2,
            "Protein", ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(table_x + col1_w + col2_w / 2, table_top - row_h / 2,
            "Residue", ha="center", va="center", fontsize=12, fontweight="bold")

    # Data rows
    for i, (protein, residue) in enumerate(rows):
        y_row = table_top - (i + 2) * row_h

        ax.add_patch(
            Rectangle(
                (table_x, y_row),
                table_w,
                row_h,
                facecolor="white",
                edgecolor="0.65",
                linewidth=0.8,
            )
        )

        ax.text(
            table_x + col1_w / 2,
            y_row + row_h / 2,
            protein,
            ha="center",
            va="center",
            fontsize=11.5,
        )

        ax.text(
            table_x + col1_w + col2_w / 2,
            y_row + row_h / 2,
            residue,
            ha="center",
            va="center",
            fontsize=13.5,
            fontweight="bold",
        )

    # Vertical divider
    ax.plot(
        [table_x + col1_w, table_x + col1_w],
        [table_top - table_h, table_top],
        color="0.55",
        linewidth=0.9,
    )


# Title
ax.text(
    0.5,
    0.965,
    "Focused residue mapping at two specificity-related aligned sites",
    ha="center",
    va="top",
    fontsize=18,
    fontweight="bold",
)

# Panel 1
draw_panel(
    y=0.88,
    title="Site 1 — alignment column 68",
    site_note="Tyr/Thr-related position discussed in the original paper",
    rows=[
        ("O67940_AQUAE", "Val67"),
        ("2Q6O (chlorinase-related)", "Thr70"),
        ("1RQP (fluorinase)", "Thr75"),
    ],
)

# Panel 2
draw_panel(
    y=0.50,
    title="Site 2 — alignment column 151",
    site_note="Gly/Ser-related position discussed in the original paper",
    rows=[
        ("O67940_AQUAE", "Gly127"),
        ("2Q6O (chlorinase-related)", "Gly131"),
        ("1RQP (fluorinase)", "Ser158"),
    ],
)

# Bottom interpretation box
footer_x = 0.07
footer_y = 0.055
footer_w = 0.86
footer_h = 0.105

ax.add_patch(
    Rectangle(
        (footer_x, footer_y),
        footer_w,
        footer_h,
        facecolor="0.96",
        edgecolor="0.35",
        linewidth=1.0,
    )
)

ax.text(
    0.5,
    footer_y + footer_h / 2,
    "Main signal: O67940 matches the chlorinase-related Gly pattern at site 2 "
    "(Gly127 ↔ Gly131),\n"
    "rather than the fluorinase Ser158. Site 1 is less direct because O67940 has Val67.",
    ha="center",
    va="center",
    fontsize=11.5,
)

fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(pdf_path, bbox_inches="tight")
plt.close(fig)

print(f"Wrote: {png_path}")
print(f"Wrote: {pdf_path}")
