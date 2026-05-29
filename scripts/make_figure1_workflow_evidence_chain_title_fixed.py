from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

# ============================================================
# Figure 1: Reproducible evidence-chain workflow
# FIXED VERSION:
# - Keeps the full layout the same
# ============================================================

W, H = 1600, 1000
output_dir = Path("figures/report")
output_dir.mkdir(parents=True, exist_ok=True)
out_path = output_dir / "figure1_workflow_evidence_chain_title_fixed.png"

# ---------- Soft background ----------
img = Image.new("RGB", (W, H), "#f4f6f9")
draw = ImageDraw.Draw(img)

# subtle radial glow, close to the reference image
cx, cy = W / 2, H / 2
max_r = math.sqrt(cx**2 + cy**2)
pix = img.load()
for y in range(H):
    for x in range(W):
        d = math.sqrt((x - cx)**2 + (y - cy)**2) / max_r
        base = (244, 246, 249)
        glow = (255, 255, 255)
        a = max(0, 1 - d * 1.5)
        r = int(base[0] * (1-a) + glow[0] * a)
        g = int(base[1] * (1-a) + glow[1] * a)
        b = int(base[2] * (1-a) + glow[2] * a)
        pix[x, y] = (r, g, b)

draw = ImageDraw.Draw(img)

# ---------- Fonts ----------
font_dir = Path("/usr/share/fonts/truetype/dejavu")
if not font_dir.exists():
    font_dir = Path(".")

def F(name, size):
    candidates = [
        font_dir / name,
        Path("/Library/Fonts/Arial Unicode.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for p in candidates:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

# Main fonts
header_font = F("DejaVuSans-Bold.ttf", 27)
cell_bold = F("DejaVuSans-Bold.ttf", 24)
cell = F("DejaVuSans.ttf", 22)
cell_small = F("DejaVuSans.ttf", 20)
bottom_title = F("DejaVuSans-Bold.ttf", 28)
bottom_body = F("DejaVuSans.ttf", 21)
small = F("DejaVuSans.ttf", 18)
foot = F("DejaVuSans.ttf", 20)

# ---------- Colors ----------
navy = "#142b4f"
text = "#17263a"

blue_fill = "#e7f1fb"
green_fill = "#edf7ed"
yellow_fill = "#fff3c7"

header_blue = "#e5edf7"
header_green = "#edf6eb"
header_yellow = "#fff1bd"

line_dark = "#566a83"
line_blue = "#1f78e0"
line_teal = "#00aeb0"
line_green = "#4a9d28"
line_purple = "#9b50db"
line_orange = "#f08a00"
evidence_green = "#2d8d3e"

# ---------- Helpers ----------
def text_size(s, font):
    box = draw.textbbox((0, 0), s, font=font)
    return box[2] - box[0], box[3] - box[1]

def fit_font_to_width(text_value, font_name, start_size, max_width, min_size=24):
    """
    Reduces only the title font size until the full title fits inside the canvas.
    This prevents left/right clipping while keeping the rest of the figure unchanged.
    """
    size = start_size
    while size >= min_size:
        font = F(font_name, size)
        tw, _ = text_size(text_value, font)
        if tw <= max_width:
            return font
        size -= 1
    return F(font_name, min_size)

def rounded_box(x, y, w, h, fill, outline, radius=13, width=3):
    draw.rounded_rectangle(
        [x, y, x + w, y + h],
        radius=radius,
        fill=fill,
        outline=outline,
        width=width,
    )

def center_lines(x, y, w, h, lines, font, fill=text, spacing=5):
    if isinstance(lines, str):
        lines = lines.split("\n")
    heights = [text_size(line, font)[1] for line in lines]
    total = sum(heights) + spacing * (len(lines) - 1)
    yy = y + (h - total) / 2
    for line, lh in zip(lines, heights):
        tw, _ = text_size(line, font)
        draw.text((x + (w - tw) / 2, yy), line, font=font, fill=fill)
        yy += lh + spacing

def arrow(x1, y1, x2, y2, color=line_dark, width=3):
    draw.line([x1, y1, x2, y2], fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 13
    p1 = (x2 - size * math.cos(ang - 0.45), y2 - size * math.sin(ang - 0.45))
    p2 = (x2 - size * math.cos(ang + 0.45), y2 - size * math.sin(ang + 0.45))
    draw.polygon([(x2, y2), p1, p2], fill=color)

# ---------- Title: fixed ----------
title = "Modern re-analysis of O67940_AQUAE using a reproducible evidence-chain"

# The only real fix: add safe side margins and auto-fit the title.
title_margin = 35
title_font = fit_font_to_width(
    text_value=title,
    font_name="DejaVuSans-Bold.ttf",
    start_size=40,
    max_width=W - 2 * title_margin,
    min_size=30,
)

tw, th = text_size(title, title_font)
title_x = (W - tw) / 2
title_y = 17
draw.text((title_x, title_y), title, font=title_font, fill=navy)

# ---------- Grid layout ----------
left = 99
gap = 10
col_w = [275, 370, 365, 365]
xs = [left]
for i in range(3):
    xs.append(xs[-1] + col_w[i] + gap)

y_header = 66
h_header = 76
row_y0 = 145
row_h = 103
row_gap = 2
ys = [row_y0 + i * (row_h + row_gap) for i in range(6)]

# ---------- Headers ----------
headers = ["Evidence layer", "Input / source", "Script / tool", "Main output"]
fills = [header_blue, header_blue, header_green, header_yellow]
for i, label in enumerate(headers):
    rounded_box(xs[i], y_header, col_w[i], h_header, fills[i], line_dark, 13, 3)
    center_lines(xs[i], y_header, col_w[i], h_header, label, header_font)

# ---------- Content ----------
row_outlines = [line_blue, line_teal, line_blue, line_green, line_purple, line_orange]

evidence = [
    "Annotation status",
    "Domain context",
    "Predicted\nstructure",
    "Reference\nstructures",
    "Comparison",
    "Residue evidence",
]

inputs = [
    "UniProtKB record for\nO67940_AQUAE",
    "UniProt cross-references to\nInterPro and Pfam",
    "AlphaFoldDB model, pLDDT\nvalues, and PAE file",
    "RCSB PDB structures 2Q6O and\n1RQP",
    "Prepared structures and\nextracted sequences",
    "Multiple alignment and\nreference functional residues",
]

tools = [
    "parse_uniprot_O67940.py",
    "fetch_interpro_pfam_metadata\n.py",
    "AlphaFold confidence\nsummary scripts",
    "PDB retrieval and\nchain-extraction scripts",
    "TM-align and MAFFT",
    "Residue-mapping +\nintegration scripts",
]

outputs = [
    "UniProt annotation summary",
    "Domain and family metadata\ntable",
    "Confidence summaries and\nFigure 2",
    "Prepared Chain A structure\nfiles",
    "Structural and sequence\ncomparison summaries",
    "Focused residue table and\nevidence tables",
]

for r, y in enumerate(ys):
    outline = row_outlines[r]

    rounded_box(xs[0], y, col_w[0], row_h, blue_fill, outline, 9, 3)
    center_lines(xs[0], y, col_w[0], row_h, evidence[r], cell_bold, spacing=1)

    rounded_box(xs[1], y, col_w[1], row_h, blue_fill, outline, 9, 3)
    center_lines(xs[1], y, col_w[1], row_h, inputs[r], cell, spacing=2)

    rounded_box(xs[2], y, col_w[2], row_h, green_fill, outline, 9, 3)
    center_lines(xs[2], y, col_w[2], row_h, tools[r], cell if r != 1 else cell_small, spacing=2)

    rounded_box(xs[3], y, col_w[3], row_h, yellow_fill, outline, 9, 3)
    center_lines(xs[3], y, col_w[3], row_h, outputs[r], cell, spacing=2)

    mid_y = y + row_h / 2
    arrow(xs[1] + col_w[1] - 14, mid_y, xs[2] + 15, mid_y)
    arrow(xs[2] + col_w[2] - 14, mid_y, xs[3] + 15, mid_y)

# ---------- Bottom boxes ----------
bottom_y = 779
bottom_h = 132

# Reproducibility box
rounded_box(xs[0], bottom_y, col_w[0] + 35, bottom_h, blue_fill, line_blue, 11, 3)
rep_title = "Reproducibility"
rtw, _ = text_size(rep_title, bottom_title)
draw.text((xs[0] + (col_w[0] + 35 - rtw) / 2, bottom_y + 16), rep_title, font=bottom_title, fill="#1f65b7")

rep_lines = ["environment.yml", "provenance · checksums", "workflow log"]
rep_start = bottom_y + 51
for i, line in enumerate(rep_lines):
    lw, _ = text_size(line, small)
    draw.text((xs[0] + (col_w[0] + 35 - lw) / 2, rep_start + i * 24), line, font=small, fill=text)

# Evidence integration box
ev_x = xs[1] + 50
ev_w = (xs[3] + col_w[3]) - ev_x
rounded_box(ev_x, bottom_y + 5, ev_w, bottom_h - 5, green_fill, evidence_green, 11, 3)

ev_title = "Evidence integration"
etw, _ = text_size(ev_title, bottom_title)
draw.text((ev_x + (ev_w - etw) / 2, bottom_y + 24), ev_title, font=bottom_title, fill="#2e7d32")

body = [
    "Outputs are combined into a cautious annotation-transfer interpretation,",
    "not biochemical proof.",
]
body_start = bottom_y + 63
for i, line in enumerate(body):
    lw, _ = text_size(line, bottom_body)
    draw.text((ev_x + (ev_w - lw) / 2, body_start + i * 27), line, font=bottom_body, fill=text)

# Down green arrow into evidence integration
start_x = xs[3] + col_w[3] / 2
start_y = ys[-1] + row_h - 5
end_y = bottom_y + 8
draw.line([start_x, start_y, start_x, end_y], fill="#20a657", width=4)
draw.polygon(
    [(start_x, end_y + 19), (start_x - 11, end_y), (start_x + 11, end_y)],
    fill="#20a657",
)

# ---------- Footnote ----------
footnote = "Exact commands, file provenance, checksums, and runtime decisions are documented separately in the repository."
fw, _ = text_size(footnote, foot)
draw.text(((W - fw) / 2, 930), footnote, font=foot, fill="#6b7280")

img.save(out_path, quality=95)
print(f"Saved: {out_path.resolve()}")
print(f"Title font size fitted to avoid clipping.")
