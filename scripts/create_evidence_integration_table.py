from pathlib import Path
import csv

OUT_PATH = Path("results/evidence_integration/evidence_integration_table.tsv")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

rows = [
    {
        "evidence_layer": "Current UniProtKB record",
        "result": "O67940_AQUAE remains an unreviewed TrEMBL entry named 'Uncharacterized protein'; no UniProt FUNCTION comment, no GO term, and no PDB cross-reference were found.",
        "supports": "The biological problem remains relevant: the protein still lacks curated experimental functional annotation.",
        "does_not_prove": "Does not by itself identify the protein's function.",
        "limitation_or_caution": "UniProt status reflects current database annotation, not direct biochemical evidence.",
        "main_output": "results/uniprot_O67940_record_summary.txt",
    },
    {
        "evidence_layer": "InterPro/Pfam family-domain evidence",
        "result": "The protein is associated with SAM_HAT N-terminal and C-terminal domains and the S-adenosyl-L-methionine hydroxide adenosyltransferase family/domain context.",
        "supports": "Broad SAM-related family/domain membership.",
        "does_not_prove": "Does not distinguish chlorinase, fluorinase, brominase, iodinating activity, or broader halogenase specificity.",
        "limitation_or_caution": "Family/domain labels are useful but can be too broad for exact substrate specificity.",
        "main_output": "results/O67940_interpro_pfam_metadata.tsv",
    },
    {
        "evidence_layer": "AlphaFoldDB model confidence",
        "result": "The AlphaFoldDB v6 model has high local confidence: mean pLDDT 96.70, median pLDDT 97.69, and no residues below 70.",
        "supports": "The predicted structure is reliable enough for downstream structural inspection/comparison.",
        "does_not_prove": "Does not prove enzyme activity, ligand binding, or halide specificity.",
        "limitation_or_caution": "AlphaFold confidence estimates structural reliability, not biochemical function.",
        "main_output": "results/alphafold/O67940_alphafold_plddt_summary.txt",
    },
    {
        "evidence_layer": "Domain-level AlphaFold PAE",
        "result": "Using UniProt domain boundaries, the between-domain mean PAE was 4.03 Å; internal mean PAE values were 2.33 Å for the N-terminal SAM_HAT domain and 1.83 Å for the C-terminal SAM_HAT domain.",
        "supports": "The relative arrangement of the two annotated domains is predicted with reasonably low uncertainty.",
        "does_not_prove": "Does not confirm catalytic mechanism or substrate specificity.",
        "limitation_or_caution": "Domain-level PAE supports model confidence but remains predicted structural evidence.",
        "main_output": "results/alphafold/O67940_alphafold_pae_by_domain_summary.txt",
    },
    {
        "evidence_layer": "Reference structure retrieval and chain selection",
        "result": "2Q6O and 1RQP were retrieved from RCSB PDB; representative chain A structures were extracted. 2Q6O chain A has 269 residues and 1RQP chain A has 291 residues.",
        "supports": "A clean one-chain-per-protein comparison setup for structural alignment and residue mapping.",
        "does_not_prove": "Does not itself compare structures or infer function.",
        "limitation_or_caution": "Using chain A is a controlled first choice, but ligand/interface context may involve multimeric structure.",
        "main_output": "results/structure_chains/chainA_structure_extraction_summary.tsv",
    },
    {
        "evidence_layer": "TM-align structural comparison",
        "result": "O67940_AQUAE aligned over 250 residues to both 2Q6O and 1RQP, with RMSD 2.01 Å in both cases. Reference-normalized TM-score was higher for 2Q6O (0.85311) than for 1RQP (0.78998).",
        "supports": "Strong global fold similarity to both references, with a modest structural preference toward 2Q6O.",
        "does_not_prove": "Does not prove chlorinase activity or exclude fluorinase-related function.",
        "limitation_or_caution": "Global structural similarity can miss local active-site differences that determine specificity.",
        "main_output": "results/structure_comparison/tmalign_pairwise_summary.tsv",
    },
    {
        "evidence_layer": "MAFFT sequence alignment",
        "result": "O67940_AQUAE showed nearly equal pairwise identity to 2Q6O and 1RQP in the MAFFT alignment: 0.2972 versus 0.2960 excluding gap columns.",
        "supports": "The query is sequence-related to both reference structures.",
        "does_not_prove": "Does not clearly distinguish chlorinase-like from fluorinase-like specificity.",
        "limitation_or_caution": "Global sequence identity is almost tied, so residue-level interpretation is required.",
        "main_output": "results/sequence_alignment/O67940_2Q6O_1RQP_alignment_summary.tsv",
    },
    {
        "evidence_layer": "Functional-residue mapping",
        "result": "Focused mapping showed O67940 Val67 aligned with the Tyr/Thr specificity-related site and O67940 Gly127 aligned with 2Q6O Gly131 and 1RQP Ser158.",
        "supports": "Key residue-level evidence is consistent with the original cautious chlorinase-like/halogenase interpretation rather than direct fluorinase-specific assignment.",
        "does_not_prove": "Does not experimentally validate substrate use.",
        "limitation_or_caution": "Mapping is based on MAFFT alignment and should be interpreted with structural/experimental context.",
        "main_output": "results/residue_mapping/focused_functional_residue_summary.tsv",
    },
    {
        "evidence_layer": "Residue-mapping cautions",
        "result": "Two C-terminal 2Q6O residues listed in the original paper, Arg250 and Glu252, did not match direct current PDB coordinate numbering; downloaded 2Q6O chain A has Leu250 and Gln252.",
        "supports": "The key Val67/Gly127 mapping is stronger than a claim of complete Table 2 reproduction.",
        "does_not_prove": "Does not invalidate the key specificity-related mapping.",
        "limitation_or_caution": "Full Table 2 should be described as partially reproduced with numbering/construct/alignment cautions.",
        "main_output": "notes/residue_mapping/flagged_2Q6O_residue_verification.md",
    },
    {
        "evidence_layer": "Overall interpretation",
        "result": "The combined evidence supports broad SAM-dependent halogenase/chlorinase-like relatedness, with no basis for direct fluorinase-specific assignment.",
        "supports": "A bounded modern re-analysis broadly agrees with the original paper's cautious conclusion.",
        "does_not_prove": "Does not prove exact substrate specificity or biochemical activity.",
        "limitation_or_caution": "The workflow is computational and does not include biochemical validation, full phylogenetic reconstruction, or complete reproduction of all original ten steps.",
        "main_output": "results/evidence_integration/evidence_integration_table.tsv",
    },
]

with OUT_PATH.open("w") as out:
    fieldnames = [
        "evidence_layer",
        "result",
        "supports",
        "does_not_prove",
        "limitation_or_caution",
        "main_output",
    ]

    writer = csv.DictWriter(out, delimiter="\t", fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote evidence integration table to {OUT_PATH}")
