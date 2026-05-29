from pathlib import Path

ALIGNMENT_PATH = Path("results/sequence_alignment/O67940_2Q6O_1RQP_chainA_mafft_alignment.fasta")
OUTPUT_PATH = Path("results/residue_mapping/functional_residue_mapping_mafft.tsv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

STRUCTURE_PDBS = {
    "O67940_AQUAE_AlphaFold_chainA": Path("data/structure_chains/O67940_AQUAE_AlphaFold_chainA.pdb"),
    "2Q6O_chainA": Path("data/structure_chains/2Q6O_chainA.pdb"),
    "1RQP_chainA": Path("data/structure_chains/1RQP_chainA.pdb"),
}

AA3_TO_AA1 = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
}

AA1_TO_AA3 = {
    "A": "Ala", "R": "Arg", "N": "Asn", "D": "Asp", "C": "Cys",
    "Q": "Gln", "E": "Glu", "G": "Gly", "H": "His", "I": "Ile",
    "L": "Leu", "K": "Lys", "M": "Met", "F": "Phe", "P": "Pro",
    "S": "Ser", "T": "Thr", "W": "Trp", "Y": "Tyr", "V": "Val",
    "-": "Gap", "X": "Xaa",
}

# Functional residues from Table 2 of Mazumder and Vasudevan (2008).
# Stars in the paper indicate catalytic sites.
# The Tyr70Thr mutation note is represented in the role column.
TARGET_RESIDUES = [
    # 2Q6O functional residues
    ("2Q6O_chainA", 11, "D", "Asp11", "functional_site"),
    ("2Q6O_chainA", 18, "A", "Ala18", "functional_site"),
    ("2Q6O_chainA", 70, "Y", "Tyr70", "catalytic_site_Tyr70Thr_mutation_position"),
    ("2Q6O_chainA", 72, "Y", "Tyr72", "functional_site"),
    ("2Q6O_chainA", 131, "G", "Gly131", "catalytic_site_specificity_relevant"),
    ("2Q6O_chainA", 183, "D", "Asp183", "functional_site"),
    ("2Q6O_chainA", 188, "N", "Asn188", "functional_site"),
    ("2Q6O_chainA", 242, "S", "Ser242", "functional_site"),
    ("2Q6O_chainA", 243, "R", "Arg243", "functional_site"),
    ("2Q6O_chainA", 250, "R", "Arg250", "functional_site"),
    ("2Q6O_chainA", 252, "E", "Glu252", "functional_site"),

    # 1RQP functional residues
    ("1RQP_chainA", 16, "D", "Asp16", "functional_site"),
    ("1RQP_chainA", 23, "S", "Ser23", "functional_site"),
    ("1RQP_chainA", 75, "T", "Thr75", "catalytic_site_specificity_relevant"),
    ("1RQP_chainA", 77, "Y", "Tyr77", "functional_site"),
    ("1RQP_chainA", 158, "S", "Ser158", "catalytic_site_specificity_relevant"),
    ("1RQP_chainA", 210, "D", "Asp210", "functional_site"),
    ("1RQP_chainA", 215, "N", "Asn215", "functional_site"),
    ("1RQP_chainA", 269, "S", "Ser269", "functional_site"),
    ("1RQP_chainA", 270, "R", "Arg270", "functional_site"),
    ("1RQP_chainA", 277, "R", "Arg277", "functional_site"),
    ("1RQP_chainA", 279, "A", "Ala279", "functional_site"),
]


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


def extract_residue_order_from_pdb(pdb_path):
    """
    Return two mappings:
    - pdb_resnum_to_seq_index: actual PDB residue number -> ungapped sequence index
    - seq_index_to_pdb_residue: ungapped sequence index -> residue label
    """
    pdb_resnum_to_seq_index = {}
    seq_index_to_pdb_residue = {}

    seen = set()
    seq_index = 0

    with pdb_path.open(errors="ignore") as handle:
        for line in handle:
            if not line.startswith("ATOM"):
                continue

            resname = line[17:20].strip()
            resnum_text = line[22:26].strip()
            icode = line[26].strip()

            key = (resnum_text, icode)
            if key in seen:
                continue

            seen.add(key)
            seq_index += 1

            aa1 = AA3_TO_AA1.get(resname, "X")
            try:
                pdb_resnum = int(resnum_text)
            except ValueError:
                continue

            label = f"{AA1_TO_AA3.get(aa1, 'Xaa')}{pdb_resnum}{icode}".strip()

            pdb_resnum_to_seq_index[pdb_resnum] = seq_index
            seq_index_to_pdb_residue[seq_index] = {
                "pdb_resnum": pdb_resnum,
                "aa1": aa1,
                "label": label,
            }

    return pdb_resnum_to_seq_index, seq_index_to_pdb_residue


def build_alignment_maps(aligned_sequence):
    """
    Build mappings between ungapped sequence positions and alignment columns.

    Alignment columns are reported as 1-based for readability.
    Ungapped positions are also 1-based.
    """
    seq_pos_to_alignment_column = {}
    alignment_column_to_seq_pos = {}

    ungapped_pos = 0

    for col_index, aa in enumerate(aligned_sequence, start=1):
        if aa != "-":
            ungapped_pos += 1
            seq_pos_to_alignment_column[ungapped_pos] = col_index
            alignment_column_to_seq_pos[col_index] = ungapped_pos
        else:
            alignment_column_to_seq_pos[col_index] = None

    return seq_pos_to_alignment_column, alignment_column_to_seq_pos


alignment = read_fasta(ALIGNMENT_PATH)

pdb_maps = {}
alignment_maps = {}

for label, pdb_path in STRUCTURE_PDBS.items():
    if label not in alignment:
        raise KeyError(f"{label} not found in alignment file.")

    pdb_maps[label] = extract_residue_order_from_pdb(pdb_path)
    alignment_maps[label] = build_alignment_maps(alignment[label])


def residue_at_alignment_column(label, alignment_column):
    aligned_aa = alignment[label][alignment_column - 1]

    if aligned_aa == "-":
        return "Gap", "-", "NA"

    seq_pos = alignment_maps[label][1][alignment_column]
    seq_index_to_pdb_residue = pdb_maps[label][1]
    residue_info = seq_index_to_pdb_residue.get(seq_pos)

    if residue_info is None:
        return "NA", aligned_aa, "NA"

    return residue_info["label"], residue_info["aa1"], residue_info["pdb_resnum"]


with OUTPUT_PATH.open("w") as out:
    out.write(
        "source_structure\tsource_paper_residue\tsource_expected_aa\trole\t"
        "alignment_column\t"
        "O67940_residue\tO67940_aa\tO67940_resnum\t"
        "2Q6O_residue\t2Q6O_aa\t2Q6O_resnum\t"
        "1RQP_residue\t1RQP_aa\t1RQP_resnum\t"
        "source_residue_check\n"
    )

    for source_label, source_resnum, expected_aa, paper_label, role in TARGET_RESIDUES:
        pdb_resnum_to_seq_index = pdb_maps[source_label][0]

        source_seq_index = pdb_resnum_to_seq_index.get(source_resnum)

        if source_seq_index is None:
            alignment_column = "NA"
            source_check = "source_residue_not_found"
            mapped_values = {
                "O67940_AQUAE_AlphaFold_chainA": ("NA", "NA", "NA"),
                "2Q6O_chainA": ("NA", "NA", "NA"),
                "1RQP_chainA": ("NA", "NA", "NA"),
            }
        else:
            alignment_column = alignment_maps[source_label][0][source_seq_index]
            source_label_at_col, source_aa_at_col, _ = residue_at_alignment_column(source_label, alignment_column)

            source_check = "OK" if source_aa_at_col == expected_aa else f"expected_{expected_aa}_found_{source_aa_at_col}"

            mapped_values = {
                label: residue_at_alignment_column(label, alignment_column)
                for label in STRUCTURE_PDBS
            }

        o_res, o_aa, o_num = mapped_values["O67940_AQUAE_AlphaFold_chainA"]
        q_res, q_aa, q_num = mapped_values["2Q6O_chainA"]
        r_res, r_aa, r_num = mapped_values["1RQP_chainA"]

        out.write(
            f"{source_label}\t{paper_label}\t{expected_aa}\t{role}\t"
            f"{alignment_column}\t"
            f"{o_res}\t{o_aa}\t{o_num}\t"
            f"{q_res}\t{q_aa}\t{q_num}\t"
            f"{r_res}\t{r_aa}\t{r_num}\t"
            f"{source_check}\n"
        )

print(f"Wrote functional residue mapping to {OUTPUT_PATH}")
