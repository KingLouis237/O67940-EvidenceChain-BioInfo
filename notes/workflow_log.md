# Workflow log — Methods in Bioinformatics re-analysis

## Project aim

This project critically reviews and performs a modern re-analysis of the structure-guided protein function prediction workflow from Mazumder and Vasudevan (2008), using O67940_AQUAE as the case-study protein.

## Directory structure

- `data/`: raw downloaded input files and database records
- `scripts/`: reusable analysis scripts
- `results/`: processed outputs and summary tables
- `figures/`: exported plots, screenshots, and visual outputs
- `notes/`: interpretation notes, workflow decisions, and logs

## Step 1 — UniProt current record retrieval

Date: 2026-05-26

Files generated:

- `data/O67940_AQUAE.fasta`
- `data/O67940_uniprot_record.json`
- `data/O67940_uniprot_record_pretty.json`
- `scripts/parse_uniprot_O67940.py`
- `results/uniprot_O67940_record_summary.txt`
- `notes/step1_uniprot_current_record_interpretation.md`

Main finding:

The current UniProtKB record for O67940_AQUAE remains unreviewed, is still named “Uncharacterized protein,” has PE=3 inferred from homology, and lacks UniProt FUNCTION, GO, and PDB cross-references. However, it includes InterPro, Pfam, eggNOG, KEGG, and AlphaFoldDB cross-references, supporting further modern family/domain and predicted-structure analysis.

## Step 2 — InterPro/Pfam metadata retrieval

Date: 2026-05-26

Files generated:

- `scripts/fetch_interpro_pfam_metadata.py`
- `data/interpro_pfam/*.json`
- `results/O67940_interpro_pfam_metadata.tsv`
- `notes/step2_interpro_pfam_metadata_summary.md`

Main status:

InterPro and Pfam metadata were successfully retrieved for all cross-references found in the current UniProtKB record for O67940_AQUAE. The first attempt failed because of a temporary WSL/DNS name-resolution issue, but rerunning the workflow after restarting Ubuntu succeeded.

Main finding from Step 2:

Modern InterPro/Pfam metadata assigns O67940_AQUAE to the S-adenosyl-L-methionine hydroxide adenosyltransferase family, with predicted N-terminal and C-terminal SAM_HAT domains. This supports broad SAM-related family/domain membership, but does not resolve whether the protein is specifically a chlorinase, fluorinase, or broader halogenase.

## Report organization setup

Date: 2026-05-26

Files added:

- `report/report_skeleton.md`
- `report/workflow_to_report_map.md`
- `notes/project_logic_for_beginners.md`

Purpose:

These files connect the computational workflow to the final article structure required for the course. The report skeleton follows the expected scientific article format: Introduction, Materials and Methods, Results, Discussion, Conclusion, and References. The workflow-to-report map records where each raw file, script, processed result, and interpretation note will appear in the final report.

## Step 3 — AlphaFoldDB file discovery

Date: 2026-05-26

Initial note:

Hardcoded AlphaFoldDB v4 download links returned 127-byte files, which were too small to be valid PDB/mmCIF/PAE files. These files were treated as invalid and discarded. The workflow was corrected to query the AlphaFoldDB API endpoint for O67940 first, then download the current URLs reported by the API.

Reason:

This is more reproducible because the correct AlphaFoldDB filenames and file versions should be discovered from the AlphaFoldDB entry/API rather than assumed manually.

Step 3 update:

The AlphaFoldDB API endpoint for O67940 was queried and returned `latestVersion: 6`. The correct current model URLs are v6 files, not v4 files. The workflow therefore uses the API-reported v6 PDB, mmCIF, binary CIF, and predicted aligned error JSON files.

## Step 3 — AlphaFoldDB predicted structure retrieval

Date: 2026-05-26

Files generated:

- `data/alphafold/O67940_alphafold_api_prediction.json`
- `data/alphafold/O67940_alphafold_api_prediction_pretty.json`
- `data/alphafold/AF-O67940-F1-model_v6.pdb`
- `data/alphafold/AF-O67940-F1-model_v6.cif`
- `data/alphafold/AF-O67940-F1-model_v6.bcif`
- `data/alphafold/AF-O67940-F1-predicted_aligned_error_v6.json`
- `scripts/summarize_alphafold_plddt.py`
- `results/alphafold/O67940_alphafold_plddt_summary.txt`

Main logic:

The current UniProtKB record links O67940_AQUAE to AlphaFoldDB but not to PDB. The AlphaFoldDB API was queried first to avoid assuming a model version manually. The API returned `latestVersion: 6`, so the v6 structure and confidence files were downloaded. This provides a modern predicted-structure evidence layer for the query protein itself.

## Step 3 — AlphaFold PAE confidence analysis

Date: 2026-05-26

Files generated:

- `scripts/summarize_alphafold_pae.py`
- `results/alphafold/O67940_alphafold_pae_summary.txt`
- `notes/alphafold/pae_explanation_and_plan.md`

Purpose:

After summarizing pLDDT local confidence, the PAE file was analyzed to assess confidence in the relative positioning of residues/regions in the AlphaFoldDB model. This is important because O67940_AQUAE has predicted N-terminal and C-terminal SAM_HAT domains, and high local pLDDT alone does not guarantee confident domain-domain orientation.

## Step 3 — Domain-boundary-based PAE refinement
Files generated:

- `notes/alphafold/domain_boundaries_from_uniprot.md`
- `scripts/summarize_alphafold_pae_by_domain.py`
- `results/alphafold/O67940_alphafold_pae_by_domain_summary.txt`

Purpose:

The initial PAE analysis used a rough half-protein split. The UniProt JSON `features` field was inspected and provided specific domain coordinates: residues 3–148 for the N-terminal SAM_HAT domain and residues 171–246 for the C-terminal SAM_HAT domain. These coordinates were then used to calculate a more biologically meaningful domain-level PAE summary.

Step 3 interpretation update:

Domain-level PAE analysis using UniProt-derived domain boundaries showed low internal PAE for both the N-terminal SAM_HAT domain and C-terminal SAM_HAT domain, and a low between-domain mean PAE of 4.03 Å. This suggests that the AlphaFoldDB v6 model is confident enough for downstream structural comparison, while still not proving enzymatic activity or substrate specificity.

## Reproducibility upgrade

Date: 2026-05-26

Files generated or updated:

- `environment.yml`
- `metadata/source_provenance.tsv`
- `metadata/checksums_sha256.txt`
- `metadata/README.md`
- `.gitignore`
- `README.md`

Purpose:

This upgrade improves reproducibility by recording the conda environment, source provenance, file checksums, and project-level documentation. This is important because the re-analysis depends on external databases and APIs whose contents and file versions can change over time.

## Step 4 — Reference PDB structure retrieval

Date: 2026-05-26

Purpose:

The original paper used 2Q6O and 1RQP as key reference structures for interpreting O67940_AQUAE. This step retrieves both structures from RCSB PDB in mmCIF and PDB formats so they can be used for structural comparison and residue mapping.

Planned files:

- `data/pdb/2Q6O.cif`
- `data/pdb/2Q6O.pdb`
- `data/pdb/1RQP.cif`
- `data/pdb/1RQP.pdb`
- `notes/pdb/reference_structure_retrieval_note.md`

## Step 4 — Reference PDB structure retrieval

Date: 2026-05-26

Files generated:

- `scripts/fetch_reference_pdb_structures.py`
- `data/pdb/2Q6O.cif`
- `data/pdb/2Q6O.pdb`
- `data/pdb/1RQP.cif`
- `data/pdb/1RQP.pdb`
- `results/pdb/reference_structure_download_summary.tsv`
- `notes/pdb/reference_structure_retrieval_note.md`

Purpose:

The original article used 2Q6O and 1RQP as key reference structures for interpreting O67940_AQUAE. This step retrieves both structures from RCSB PDB in mmCIF and PDB formats, validates file sizes and ATOM records, and prepares them for structural comparison and residue mapping.

## Step 4B — Reference structure content inspection

Date: 2026-05-26

Files generated:

- `scripts/inspect_reference_pdb_contents.py`
- `results/pdb/reference_pdb_chain_summary.tsv`
- `results/pdb/reference_pdb_heteroatom_summary.tsv`
- `notes/pdb/reference_structure_content_inspection_note.md`

Purpose:

After downloading the reference structures 2Q6O and 1RQP, the workflow inspected their protein chains and HETATM records. This step is necessary because PDB files may contain multiple chains and non-protein molecules. The inspection helps decide which chains and ligands are relevant for structural comparison and residue mapping.

Step 4B interpretation update:

Reference structure inspection showed that 2Q6O contains chains A and B, each with 269 residues, while 1RQP contains chains A, B, and C, each with 291 residues. Both structures contain SAM, and 2Q6O also contains CL. This confirms relevant ligand/cofactor context but also shows that downstream comparison should use representative chains rather than full multi-chain PDB files.

## Step 4C — Representative chain sequence extraction

Date: 2026-05-26

Files generated:

- `scripts/extract_structure_chain_sequences.py`
- `data/reference_sequences/O67940_2Q6O_1RQP_chainA_sequences.fasta`
- `results/pdb/reference_chainA_sequence_summary.tsv`
- `notes/pdb/chain_sequence_extraction_note.md`

Purpose:

The reference structures contain multiple protein chains. This step extracts chain A sequences from the AlphaFold model, 2Q6O, and 1RQP to prepare a clean sequence set for alignment and functional-residue mapping.

## Step 5A — Chain A structure extraction

Date: 2026-05-26

Files generated:

- `scripts/extract_chainA_structure_files.py`
- `data/structure_chains/O67940_AQUAE_AlphaFold_chainA.pdb`
- `data/structure_chains/2Q6O_chainA.pdb`
- `data/structure_chains/1RQP_chainA.pdb`
- `results/structure_chains/chainA_structure_extraction_summary.tsv`
- `notes/structure_chains/chainA_structure_extraction_note.md`

Purpose:

The reference PDB files contain multiple chains. This step extracts representative chain A protein ATOM records from O67940_AQUAE, 2Q6O, and 1RQP to prepare clean inputs for structural alignment. HETATM records are excluded at this stage to keep the first structural comparison focused on protein coordinates only.

## Step 5B — TM-align installation

Date: 2026-05-27

Purpose:

TM-align was installed in the active `methods_bioinfo` conda environment using Bioconda/conda-forge so that pairwise structural comparisons can be performed reproducibly.

Command used:

`conda install -c bioconda -c conda-forge tmalign`

Verification commands:

`which TMalign`
`which tmalign`
`ls $CONDA_PREFIX/bin | grep -i tmalign`
`TMalign 2>&1 | head -20`

A separate installation note was created at:

`notes/structure_chains/tmalign_installation_note.md`

Step 5B verification update:

TM-align was successfully installed and verified in the `methods_bioinfo` conda environment.

Executable:

`/home/abane_ashu/miniconda3/envs/methods_bioinfo/bin/TMalign`

Installed command name:

`TMalign`

Version reported by help output:

`TM-align Version 20240303`

No lowercase `tmalign` executable was found, so downstream scripts should call `TMalign`.

## Step 5C — TM-align runtime failure

Date: 2026-05-27

TM-align was installed and recognized as `TMalign` version 20240303. However, when run on the first pairwise comparison, it failed with `Illegal instruction (core dumped)` and exit code 132. The input PDB files were checked and contained valid ATOM records, so the failure is likely a binary/CPU compatibility issue rather than a structure-file problem. No structural alignment result was interpreted from this failed run.

Step 5B correction:

The initially installed TM-align build reporting Version 20240303 crashed during real alignment with `Illegal instruction (core dumped)` and exit code 132. An older Bioconda package was installed with:

`conda install -y -c bioconda -c conda-forge tmalign=20220227`

The resulting executable still runs as `TMalign` and reports `TM-align Version 20220412`. A test alignment between O67940_AQUAE AlphaFold chain A and 2Q6O chain A completed successfully with exit code 0. This working version will be used for downstream pairwise structural comparisons.

Step 5C interpretation update:

Pairwise TM-align comparisons completed successfully with the working TM-align version. O67940_AQUAE aligned over 250 residues to both 2Q6O and 1RQP, with RMSD 2.01 Å in both comparisons. The TM-score normalized by the reference structure was higher for 2Q6O (0.85311) than for 1RQP (0.78998), suggesting stronger global fold similarity to 2Q6O. This was interpreted only as structural evidence, not as proof of chlorinase or fluorinase activity.

## Step 6A — MAFFT setup for sequence alignment

Date: 2026-05-27

Purpose:

MAFFT was selected for multiple sequence alignment of the extracted chain A sequences from O67940_AQUAE, 2Q6O, and 1RQP. This alignment will support residue mapping, which is necessary because global structural similarity does not by itself prove enzyme activity or substrate specificity.

## Step 6 — MAFFT sequence alignment

Date: 2026-05-27

Files generated:

- `results/sequence_alignment/O67940_2Q6O_1RQP_chainA_mafft_alignment.fasta`
- `scripts/summarize_mafft_alignment.py`
- `results/sequence_alignment/O67940_2Q6O_1RQP_alignment_summary.tsv`
- `notes/sequence_alignment/mafft_alignment_note.md`

Purpose:

The extracted chain A sequences from O67940_AQUAE, 2Q6O, and 1RQP were aligned using MAFFT. This prepares the workflow for functional-residue mapping, which is needed because structural similarity alone cannot establish substrate specificity.

## Step 6 — MAFFT sequence alignment

Date: 2026-05-27

Files generated:

- `results/sequence_alignment/O67940_2Q6O_1RQP_chainA_mafft_alignment.fasta`
- `scripts/summarize_mafft_alignment.py`
- `results/sequence_alignment/O67940_2Q6O_1RQP_alignment_summary.tsv`
- `notes/sequence_alignment/mafft_installation_note.md`
- `notes/sequence_alignment/mafft_alignment_note.md`
- `notes/sequence_alignment/mafft_alignment_interpretation.md`

Purpose:

The extracted chain A sequences from O67940_AQUAE, 2Q6O, and 1RQP were aligned using MAFFT v7.525. The alignment supports residue mapping across the query and reference proteins. Pairwise identity from the alignment showed that O67940_AQUAE is nearly equally similar to 2Q6O and 1RQP at the global sequence level, so functional interpretation must move to residue-level mapping.

## Step 6 — MAFFT sequence alignment

Date: 2026-05-27

Files generated:

- `results/sequence_alignment/O67940_2Q6O_1RQP_chainA_mafft_alignment.fasta`
- `scripts/summarize_mafft_alignment.py`
- `results/sequence_alignment/O67940_2Q6O_1RQP_alignment_summary.tsv`
- `notes/sequence_alignment/mafft_installation_note.md`
- `notes/sequence_alignment/mafft_alignment_note.md`
- `notes/sequence_alignment/mafft_alignment_interpretation.md`

Purpose:

The extracted chain A sequences from O67940_AQUAE, 2Q6O, and 1RQP were aligned using MAFFT v7.525. The alignment supports residue mapping across the query and reference proteins. Pairwise identity from the alignment showed that O67940_AQUAE is nearly equally similar to 2Q6O and 1RQP at the global sequence level, so functional interpretation must move to residue-level mapping.

## Step 7 — Functional-residue mapping using MAFFT alignment

Date: 2026-05-27

Files generated:

- `scripts/map_functional_residues_mafft.py`
- `results/residue_mapping/functional_residue_mapping_mafft.tsv`
- `notes/residue_mapping/functional_residue_mapping_note.md`

Purpose:

Functional residues discussed in the original paper were mapped across O67940_AQUAE, 2Q6O, and 1RQP using the MAFFT alignment. This step moves the analysis from global similarity to local functional determinants, which is necessary because enzyme specificity depends on active-site and binding-pocket residues rather than global fold similarity alone.

## Step 7 — Functional-residue mapping interpretation

Date: 2026-05-27

Main finding:

MAFFT-based residue mapping reproduced the key original-paper mapping of O67940_AQUAE Val67 and Gly127 to specificity-related positions in the reference enzymes. The mapping aligned O67940 Val67 with 1RQP Thr75 and the downloaded 2Q6O residue 70, which appears as Thr70 in the coordinate file. It also aligned O67940 Gly127 with 2Q6O Gly131 and 1RQP Ser158.

Caution:

Three source-residue checks were flagged. The 2Q6O Tyr70 warning is likely explained by the Tyr70Thr mutation noted in the original paper, but 2Q6O Arg250 and Glu252 mapped to Leu250 and Gln252 in the downloaded structure file and require further checking before claiming complete reproduction of Table 2.

## Step 7 — Direct verification of flagged 2Q6O residues

Date: 2026-05-27

Purpose:

The MAFFT-based residue mapping flagged several 2Q6O positions where the expected amino acid from the original paper did not match the downloaded 2Q6O chain A structure. Direct PDB inspection confirmed that the downloaded 2Q6O chain A contains THR70, GLY131, LEU250, and GLN252. The THR70 result is consistent with the Tyr70Thr mutation noted in the original paper. The GLY131 mapping supports the key O67940 Gly127 result. The LEU250 and GLN252 findings remain unresolved and will be treated as a residue-numbering/construct/alignment caution rather than ignored.

## Step 7B — Focused functional-residue summary

Date: 2026-05-27

Files generated:

- `scripts/create_focused_residue_mapping_summary.py`
- `results/residue_mapping/focused_functional_residue_summary.tsv`
- `notes/residue_mapping/focused_residue_summary_note.md`

Purpose:

A focused residue-mapping summary was created from the full MAFFT-based mapping table. The focused table highlights the key Val67/Gly127 mappings in O67940_AQUAE and preserves the important caution that some C-terminal 2Q6O residues listed in the original paper do not match the current downloaded coordinate file directly.

## Step 7B — Focused residue-mapping interpretation

Date: 2026-05-27

Main finding:

The focused residue summary highlights the most biologically important mappings. O67940_AQUAE Val67 maps to the Tyr/Thr specificity-related position, and O67940_AQUAE Gly127 maps to the Gly/Ser specificity-related position. The Gly127 mapping aligns with 2Q6O Gly131 rather than 1RQP Ser158, supporting the original paper's cautious non-fluorinase-specific interpretation. Two C-terminal positions, 2Q6O Arg250 and Glu252, remain discrepant in the current downloaded coordinate file and will be treated as limitations.

## Step 8 — Report figure generation

Date: 2026-05-27

Files generated:

- `scripts/create_report_figures.py`
- `figures/report/figure1_workflow_evidence_chain.png`
- `figures/report/figure1_workflow_evidence_chain.pdf`
- `figures/report/figure2_alphafold_plddt_by_residue.png`
- `figures/report/figure2_alphafold_plddt_by_residue.pdf`
- `figures/report/figure3_tmalign_structural_similarity.png`
- `figures/report/figure3_tmalign_structural_similarity.pdf`
- `notes/figure_generation_note.md`

Purpose:

Figures were generated from reproducible outputs to support the final report. The figures summarize the evidence-chain workflow, AlphaFold local confidence across residues, and TM-align structural similarity results.

## Step 8B — Focused residue-mapping figure generation

Date: 2026-05-27

Files generated:

- `scripts/create_figure4_focused_residue_mapping.py`
- `figures/report/figure4_focused_residue_mapping.png`
- `figures/report/figure4_focused_residue_mapping.pdf`
- `notes/residue_mapping/figure4_focused_residue_mapping_note.md`

Purpose:

A focused residue-mapping figure was generated to visually summarize the two specificity-related aligned sites that are central to the functional interpretation of O67940_AQUAE relative to 2Q6O and 1RQP.

## Step 9 — Evidence integration

Date: 2026-05-28
Files generated:

- `scripts/create_evidence_integration_table.py`
- `scripts/create_evidence_integration_table_short.py`
- `results/evidence_integration/evidence_integration_table.tsv`
- `results/evidence_integration/evidence_integration_table_short.tsv`
- `notes/evidence_integration/evidence_integration_note.md`

Purpose:

The main evidence layers were integrated into a structured table separating observations, supported interpretations, unsupported claims, and limitations. This helps prevent overclaiming and prepares the workflow for conversion into the final report.

## Scope and limitations note

Date: 2026-05-28

A workflow scope and limitations note was added to clarify that the project is a bounded computational re-analysis. It does not include biochemical validation, full homolog phylogenetic reconstruction, or complete reproduction of every historical database/tool step from the original ten-step workflow. The final interpretation should therefore be presented as computational support for a cautious halogenase-related hypothesis, not as experimental proof of exact substrate specificity.

## Step 10 — Report planning

Date: 2026-05-28

Files generated:

- `report/planning/report_claim_control_sheet.md`
- `report/planning/figure_captions.md`

Purpose:

The workflow is now being converted into the final report. A claim-control sheet was created to prevent overclaiming and to separate supported claims, cautious interpretations, avoided claims, and limitations. Figure captions were drafted to connect the generated figures to the final report narrative.

## Project front-door documentation cleanup

Date: 2026-05-28

Files cleaned or confirmed:

- `README.md`
- `REPRODUCIBILITY.md`
- `report/planning/reproduction_modernization_scope_matrix.md`

Purpose:

The project-level documentation was reorganized after confusion during editing. The README now acts as the short project overview, `REPRODUCIBILITY.md` acts as the detailed reproduction guide, and the reproduction/modernization matrix defines what was reproduced, modernized, or not reproduced from the original workflow.

## Results and Discussion control checklist

Date: 2026-05-28

Files generated:

- `report/planning/results_discussion_control_checklist.md`

Purpose:

A control checklist was added to ensure that the final Results and Discussion sections are organized around biological/computational questions rather than scripts. This incorporates the earlier critical review that Results should include provenance, domain annotation, structural comparison, residue mapping, annotation-transfer interpretation, and reproducibility audit, while the Discussion should emphasize supported conclusions, uncertainties, modernization gains, reproducibility problems, and the importance of transparent workflows.

## Results and Discussion control checklist

Date: 2026-05-28

Files generated:

- `report/planning/results_discussion_control_checklist.md`

Purpose:

A control checklist was added to ensure that the final Results and Discussion sections are organized around biological/computational questions rather than scripts. This incorporates the earlier critical review that Results should include provenance, domain annotation, structural comparison, residue mapping, annotation-transfer interpretation, and reproducibility audit, while the Discussion should emphasize supported conclusions, uncertainties, modernization gains, reproducibility problems, and the importance of transparent workflows.

## Draft Materials and Methods section

Date: 2026-05-28

Files updated:

- `report/draft_sections/02_materials_methods.md`

Purpose:

The Materials and Methods section was expanded from a placeholder into a structured report draft. It describes the source article, query protein, data sources, reproducibility organization, UniProt/InterPro/Pfam analysis, AlphaFoldDB confidence analysis, reference structure retrieval, chain extraction, TM-align structural comparison, MAFFT alignment, functional-residue mapping, evidence integration, and figure generation.

## Methods citation update

Date: 2026-05-28

Files updated:

- `report/draft_sections/02_materials_methods.md`
- `report/draft_sections/05_references.md`

Purpose:

Citation placeholders were added to the Materials and Methods draft for the original paper, databases, and tools used in the workflow. A first reference list was created for the report draft.

## Revised Results section with evidence anchoring

Date: 2026-05-28

Files updated:

- `report/draft_sections/03_results.md`

Purpose:

The Results section was revised to keep the seven-subsection structure while anchoring each major result to a compact table, figure, or generated output file. This makes the section more transparent, reproducible, and easier to evaluate.

## Methods reference patch

Date: 2026-05-28

Files updated:

- `report/draft_sections/02_materials_methods.md`
- `report/draft_sections/05_references.md`

Purpose:

The preferred Materials and Methods draft was kept, and tool/database citations were added at first mention. The References section was updated with the original paper and the main database/tool references used in the workflow.

## Methods citation cleanup

Date: 2026-05-28

Files updated:

- `report/draft_sections/02_materials_methods.md`

Purpose:

A duplicated AlphaFoldDB/AlphaFold citation sentence was removed after the Methods reference patch.

## Draft Discussion section

Date: 2026-05-28

Files updated:

- `report/draft_sections/04_discussion.md`
- `report/draft_sections/05_references.md`

Purpose:

The Discussion section was drafted around biological support, remaining uncertainty, modernization gains, reproducibility problems, and the importance of transparent computational workflows. Additional conceptual references were added on enzyme superfamily functional diversity, annotation error, and annotation propagation.

## Expanded Introduction references

Date: 2026-05-28

Files updated:

- `report/draft_sections/01_introduction.md`
- `report/draft_sections/05_references.md`

Purpose:

The Introduction was expanded with stronger external referencing around protein function prediction, annotation-transfer risk, enzyme-superfamily functional diversity, annotation-error propagation, modern protein resources, and reproducibility/auditability. The final finding was intentionally not stated in the Introduction.

## Final report draft assembly

Date: 2026-05-28

Files updated:

- `report/draft_sections/03_results.md`
- `report/final_report_draft.md`

Purpose:

The draft report sections were assembled into a single Markdown report draft. A small Results table header was corrected, and cleaner spacing was added between major report sections.

## Word-ready report draft

Date: 2026-05-28

Files generated:

- `report/final_report_word_ready.md`
- `report/final_report_word_ready.docx`

Purpose:

A Word-editable report draft was generated from the assembled Markdown report. Figure image links were inserted into the Word-ready Markdown for figures 2, 3, and 4 before conversion with Pandoc.
