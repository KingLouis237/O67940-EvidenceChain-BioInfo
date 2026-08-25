# Workflow log - Methods in Bioinformatics re-analysis

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

## 2026-07-01 — Version freeze before publication upgrade

### What was done
Tagged the current repository state as `v0.1-course-report-state` and prepared a new publication-upgrade branch for broader homolog, phylogenetic, residue-conservation, active-site, ligand-pocket, and interface analyses.

### Why it was done
The current report represents the completed report-level reproducible re-analysis. Before adding the publication-upgrade analyses, the original state was preserved so that the evidence chain remains transparent.

### Input files/sources
Current repository state, including `data/`, `scripts/`, `results/`, `figures/`, `metadata/`, `notes/`, `report/`, `README.md`, `REPRODUCIBILITY.md`, and `environment.yml`.

### Command or script used
`git tag v0.1-course-report-state`
`git switch -c publication-upgrade-homolog-active-site`

### Output files generated
No new biological output files. A Git version tag and publication-upgrade branch were created.

### Main result
The original course/report-level project state is preserved as `v0.1-course-report-state`.

### Interpretation
This separates the original reproducible report from the publication-upgrade extension.

### Limitation/caution
This is version-control provenance only. It does not add biological evidence and does not support any new functional claim about O67940_AQUAE.

### Next step
Create the publication-upgrade module structure and begin the homolog-search evidence layer.


## 2026-07-01 — Version freeze before publication upgrade

### What was done
Prepared the current repository state for tagging as `v0.1-course-report-state` and for branching into `publication-upgrade-homolog-active-site`.

### Why it was done
The current report represents the completed course/report-level reproducible re-analysis. Before adding the publication-upgrade module — homolog search, broader MSA, phylogenetic analysis, residue conservation, active-site structural mapping, SAM/ligand pocket context, and interface context — the current state is being frozen as a permanent checkpoint. This keeps the original report state separate from the publication extension.

### Input files/sources
Current repository state, including:
- `data/`
- `scripts/`
- `results/`
- `figures/`
- `metadata/`
- `notes/`
- `report/`
- `README.md`
- `REPRODUCIBILITY.md`
- `environment.yml`

### Commands used
```bash
git status --short --branch
git add metadata/version_history.tsv notes/workflow_log.md
git commit -m "Document v0.1 course-report state before publication upgrade"
git tag -a v0.1-course-report-state -m "Course report state before homolog and active-site publication upgrade"
git push origin main
git push origin v0.1-course-report-state
git switch -c publication-upgrade-homolog-active-site
git push -u origin publication-upgrade-homolog-active-site
```

### Commit hash at time of freeze
To be filled after tagging using:
```bash
git rev-parse v0.1-course-report-state
```

### Output files generated
No new biological output files.

Infrastructure/provenance outputs:
- `metadata/version_history.tsv`
- updated `notes/workflow_log.md`
- Git tag: `v0.1-course-report-state`
- Git branch: `publication-upgrade-homolog-active-site`

### Main result
The original course/report-level project state will be preserved as `v0.1-course-report-state`, while new publication-upgrade analyses will be developed on a separate branch.

### Interpretation
This separates the original reproducible report from the publication-upgrade extension and keeps the project history auditable.

### Limitation/caution
This is version-control and documentation provenance only. It does not add biological evidence and does not support any new functional claim about O67940_AQUAE.

### Verification
- [ ] Tag visible on GitHub tags page
- [ ] Branch visible on GitHub branches page
- [ ] Commit hash recorded in this workflow log

### Next step
Create the publication-upgrade module structure, then begin the homolog-search evidence layer.


### Commit hash recorded after freeze
`a2c52bdeac88ffae28262641682578a029be22b7`


## 2026-07-01 — Cleanup after version-freeze setup

### What was done
Cleaned the repository state after the initial version-freeze setup. The accidental untracked shell artifacts `fi` and `printf` were inspected and removed if confirmed to be non-project files. The empty `metadata/version_history.tsv` file was replaced with a proper version-history table. The accidental local tag `v0.1-report-state` was checked and removed locally if it was not present on GitHub.

### Why it was done
The publication-upgrade branch should start from a clean and interpretable repository state. Accidental shell artifacts and duplicate local tags could confuse the audit trail.

### Input files/sources
- Current Git repository state
- Git tag `v0.1-course-report-state`
- Current branch `publication-upgrade-homolog-active-site`
- `metadata/version_history.tsv`
- `notes/workflow_log.md`

### Commands used
```bash
ls -l fi printf
file fi printf
sed -n '1,20p' fi
sed -n '1,20p' printf
rm -- fi printf
git rev-parse v0.1-course-report-state
git rev-parse HEAD
cat > metadata/version_history.tsv
git ls-remote --tags origin "refs/tags/v0.1-report-state"
git tag -d v0.1-report-state
```

### Output files generated
No biological output files.

Infrastructure/provenance outputs:
- corrected `metadata/version_history.tsv`
- updated `notes/workflow_log.md`
- cleaner Git tag state

### Main result
The repository is cleaner and the version transition from `v0.1-course-report-state` to the publication-upgrade branch is now explicitly documented.

### Interpretation
This improves traceability before starting the next biological evidence layer.

### Limitation/caution
This step does not add homologs, alignments, phylogenetic trees, structural mappings, or any biological evidence.

### Next step
Create the publication-upgrade module folders and begin the homolog-search workflow.


## 2026-07-01 — Created publication-upgrade module scaffold

### What was done
Created the folder scaffold for the publication-upgrade analyses, including homolog context, phylogeny, residue conservation, active-site structural analysis, interface context, publication figures, logs, and basic test infrastructure.

### Why it was done
The next phase of the project adds broader homolog, phylogenetic, residue-conservation, active-site, ligand-pocket, and interface-context analyses. These outputs need to be separated from the original v0.1 workflow so the evidence chain remains clean and traceable.

### Input files/sources
Current Git repository state on the `publication-upgrade-homolog-active-site` branch.

### Commands used
```bash
mkdir -p scripts/05_evolutionary_active_site_context/tests
mkdir -p results/homolog_context
mkdir -p results/phylogeny
mkdir -p results/residue_conservation
mkdir -p results/active_site_structure
mkdir -p results/interface_context
mkdir -p figures/publication
mkdir -p logs/05_evolutionary_active_site_context

for d in scripts/05_evolutionary_active_site_context scripts/05_evolutionary_active_site_context/tests results/homolog_context results/phylogeny results/residue_conservation results/active_site_structure results/interface_context figures/publication logs/05_evolutionary_active_site_context; do touch "$d/.gitkeep"; done
```

### Output files generated
No biological output files.

Infrastructure outputs:
- `scripts/05_evolutionary_active_site_context/.gitkeep`
- `scripts/05_evolutionary_active_site_context/tests/.gitkeep`
- `results/homolog_context/.gitkeep`
- `results/phylogeny/.gitkeep`
- `results/residue_conservation/.gitkeep`
- `results/active_site_structure/.gitkeep`
- `results/interface_context/.gitkeep`
- `figures/publication/.gitkeep`
- `logs/05_evolutionary_active_site_context/.gitkeep`

### Main result
A clean publication-upgrade workspace now exists.

### Interpretation
The new analyses can now be developed as a traceable extension of the original project rather than being mixed into earlier workflow outputs.

### Limitation/caution
This step creates project infrastructure only. It does not generate homologs, alignments, trees, conservation tables, structural mappings, or functional evidence.

### Next step
Identify the existing O67940_AQUAE FASTA input and prepare the first homolog-search step.


## 2026-07-01 — Validated O67940_AQUAE FASTA query input

### What was done
Checked the existing O67940_AQUAE FASTA file before using it as the query for the broader homolog-search module.

### Why it was done
The homolog-search step depends on one exact query sequence. Before running JackHMMER or any other search tool, I needed to confirm that the FASTA file exists, contains one proper sequence record, has the expected length, is tracked by Git, and is already represented in provenance and checksum metadata.

### Input files/sources
- data/O67940_AQUAE.fasta
- metadata/source_provenance.tsv
- metadata/checksums_sha256.txt

### Commands used
```bash
grep "^>" data/O67940_AQUAE.fasta
grep -c "^>" data/O67940_AQUAE.fasta

ls -lh data/O67940_AQUAE.fasta
wc -l data/O67940_AQUAE.fasta
wc -c data/O67940_AQUAE.fasta
head -5 data/O67940_AQUAE.fasta

awk '
  /^>/ {next}
  {
    gsub(/[[:space:]]/, "", $0)
    seq = seq $0
  }
  END {
    print "length=" length(seq)
    print "first20=" substr(seq, 1, 20)
    print "last20=" substr(seq, length(seq)-19, 20)
  }
' data/O67940_AQUAE.fasta

git ls-files data/O67940_AQUAE.fasta
grep -n "O67940_AQUAE.fasta\|O67940" metadata/source_provenance.tsv | head -20 || true
grep -n "data/O67940_AQUAE.fasta\|O67940_AQUAE.fasta" metadata/checksums_sha256.txt || true


### Output files generated

No new biological output files. This was an input-validation step.

### Main result

The query FASTA is present at:

`data/O67940_AQUAE.fasta`

The FASTA contains one record:

`tr|O67940|O67940_AQUAE Uncharacterized protein OS=Aquifex aeolicus (strain VF5) OX=224324 GN=aq_2196 PE=3 SV=1`

The sequence length is 251 amino acids.

First 20 residues:

`MAIVLLTDFGTKDGFVGAVK`

Last 20 residues:

`DNAREKFNLKEGEKIKFFII`

The file is tracked by Git. It is also already present in `metadata/source_provenance.tsv` and `metadata/checksums_sha256.txt`.

Checksum recorded:

`6efb6e2e79d1f1df42de3a00281800ed88ee046c2928820c6401d8ca27ce5eb4  data/O67940_AQUAE.fasta`

### Interpretation

`data/O67940_AQUAE.fasta` is suitable to use as the official query input for the homolog-search module.

### Limitation / caution

This step only validates the query input. It does not recover homologs, build an alignment, infer phylogeny, test residue conservation, or support any new functional claim about `O67940_AQUAE`.

### Next step

Install HMMER/JackHMMER inside the `methods_bioinfo` Conda environment so the broader homolog search can be run reproducibly.

## 2026-07-01 — Installed HMMER for homolog search

I installed HMMER inside the methods_bioinfo Conda environment because JackHMMER was missing.

Checked result:

- jackhmmer path: /home/abane_ashu/miniconda3/envs/methods_bioinfo/bin/jackhmmer
- HMMER version: 3.4
- MAFFT version: 7.525

Files updated:

- environment.yml
- metadata/environment_before_hmmer_install.yml

Interpretation:

The environment is ready for the first homolog-search run.

Caution:

This does not add biological evidence. No homologs have been searched yet.

Next:

Choose the search database, record it properly, then run JackHMMER.

## 2026-07-04 — Downloaded Swiss-Prot for first homolog-search pass

I downloaded UniProtKB/Swiss-Prot as the first local database for the publication-upgrade homolog search.

Why this database:

Swiss-Prot is curated and manageable. It is a good first controlled pass before using broader but noisier databases.

Source:

https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz

Local files:

- data/databases/uniprot_sprot_2026-07-04/uniprot_sprot.fasta.gz
- data/databases/uniprot_sprot_2026-07-04/uniprot_sprot.fasta

Checks:

- download completed
- gzip integrity check passed
- uncompressed FASTA created
- sequence count: 575503
- first headers inspected
- O67940 was not found inside Swiss-Prot, which is expected because the query protein is unreviewed/TrEMBL
- checksums added to metadata/checksums_sha256.txt
- source recorded in metadata/source_provenance.tsv

Interpretation:

The project now has a local curated protein database for the first JackHMMER search.

Caution:

Swiss-Prot is not the full homolog universe. It is curated but incomplete for this question. Results from this database are a first controlled pass, not the final evolutionary answer.

Next:

Run JackHMMER using data/O67940_AQUAE.fasta as query against the local Swiss-Prot FASTA.

## 2026-07-04 — Ran first JackHMMER search against Swiss-Prot

I ran JackHMMER using `data/O67940_AQUAE.fasta` as the query against the local Swiss-Prot database.

Main settings:

- database: `data/databases/uniprot_sprot_2026-07-04/uniprot_sprot.fasta`
- tool: HMMER 3.4 / JackHMMER
- iterations: 5
- E-value threshold: 1e-5
- CPU: 4

Output files:

- `results/homolog_context/O67940_vs_swissprot_jackhmmer_N5.out`
- `results/homolog_context/O67940_vs_swissprot_jackhmmer_N5.tblout`
- `results/homolog_context/O67940_vs_swissprot_jackhmmer_N5.domtblout`
- `results/homolog_context/O67940_vs_swissprot_jackhmmer_N5.sto`
- `results/homolog_context/O67940_vs_swissprot_jackhmmer_N5.parsed_hits.tsv`
- `logs/05_evolutionary_active_site_context/O67940_vs_swissprot_jackhmmer_N5.log`

Main result:

JackHMMER found 11 non-comment Swiss-Prot sequence hits.

The hits include proteins annotated as:

- `(R)-S-adenosyl-L-methionine hydrolase`
- `Fluorinase`
- `Adenosyl-chloride synthase / SalL`

Interpretation:

This supports that O67940_AQUAE sits in a reviewed Swiss-Prot neighborhood related to SAM-dependent halogenase/SAM-hydrolase/fluorinase-chlorinase-like proteins.

Caution:

This is a first controlled pass against Swiss-Prot only. It is useful, but it is not the full homolog universe. The hit list does not prove enzyme activity or substrate specificity.

Next:

Inspect the domain-level output and then decide how to curate the first homolog set for alignment and residue comparison.

## 2026-07-04 — Inspected JackHMMER domain-level hits

I inspected the JackHMMER domain-level output from the Swiss-Prot search.

Main result:

The Swiss-Prot hits show two patterns.

Most SAM hydrolase / SalL-like hits appear as one broad domain-level match across most of the O67940 query.

The fluorinase hits appear as two domain-level matches, roughly splitting the query into an N-terminal region and a larger C-terminal region.

Output file:

- `results/homolog_context/O67940_vs_swissprot_jackhmmer_N5.domain_summary.tsv`

Interpretation:

The Swiss-Prot hit set is relevant, but not uniform. The one-domain SAM hydrolase / SalL-like hits and the split-domain fluorinase hits should be kept separate during curation instead of being treated as identical evidence.

Caution:

This does not prove function or substrate specificity. It only shows how the reviewed Swiss-Prot hits align at the domain level.

Next:

Create a first curation table for the 11 Swiss-Prot hits, keeping annotation type and domain-pattern differences visible.

## 2026-07-04 — Made first Swiss-Prot hit curation table

I made a first curation table for the 11 Swiss-Prot JackHMMER hits.

Why:

The hit list is useful, but the hits are not all the same. SAM hydrolase-like and SalL-like hits mostly behaved as one broad domain match, while the fluorinase hits were split into two domain matches. I wanted that difference visible before building an alignment.

Output:

- `results/homolog_context/O67940_vs_swissprot_jackhmmer_N5.initial_curation.tsv`

Main result:

All 11 Swiss-Prot hits were kept at this stage, but labelled by annotation group and domain pattern.

Interpretation:

This gives a cleaner starting point for the first homolog set. It avoids cherry-picking only the hits that support one story.

Caution:

This is still first-pass curation. It does not prove function, and it is not the final homolog set.

Next:

Use the curated Swiss-Prot hit list to prepare a small reviewed-reference FASTA for alignment with O67940, 2Q6O, and 1RQP.

## 2026-07-04 — Cleaned metadata tables

I checked the metadata files before continuing with homolog curation.

Main issue:

`metadata/source_provenance.tsv` was not consistently tab-separated. Most older rows were being read as one field instead of six.

Fix:

- backed up the old provenance and checksum files
- rebuilt `source_provenance.tsv` as a proper six-column TSV
- deduplicated checksum paths
- added `metadata/README.md`

Interpretation:

The metadata layer is cleaner before the next biological curation step.

Caution:

This was metadata cleanup, not new biological evidence.

Next:

Continue with the first Swiss-Prot hit curation table.

## 2026-07-04 — Made first Swiss-Prot hit curation table

I made a first curation table for the 11 reviewed Swiss-Prot JackHMMER hits.

Main point:

The hit list was kept whole, but the hits were labelled by annotation group and domain pattern.

This keeps the curation honest before alignment. It avoids keeping only the hits that support one interpretation.

Output:

- `results/homolog_context/O67940_vs_swissprot_jackhmmer_N5.initial_curation.tsv`
- `results/homolog_context/README.md`

Caution:

This is first-pass curation only. It does not prove O67940 function or substrate specificity.

Next:

Prepare a reviewed-reference FASTA for alignment.

## 2026-07-04 — Built reviewed-reference FASTA for alignment

I built a small reviewed/reference FASTA for the next MAFFT alignment.

Input:

- existing O67940 / 2Q6O / 1RQP reference FASTA
- initial Swiss-Prot hit curation table
- local Swiss-Prot FASTA database

Output:

- `results/homolog_context/O67940_reviewed_swissprot_reference_set.fasta`

Main result:

The FASTA contains 14 sequences: O67940, 2Q6O chain A, 1RQP chain A, and the 11 curated Swiss-Prot hits.

Caution:

This is a controlled reviewed-reference alignment set, not the final broad homolog universe.

Next:

Run MAFFT on this reviewed-reference FASTA.

## 2026-07-04 — Ran MAFFT on reviewed-reference FASTA

I aligned the 14-sequence reviewed/reference FASTA with MAFFT.

Input:

- `results/homolog_context/O67940_reviewed_swissprot_reference_set.fasta`

Output:

- `results/sequence_alignment/O67940_reviewed_swissprot_reference_set_mafft_alignment.fasta`

Check:

The alignment contains 14 records, and all aligned sequences have length 329.

Interpretation:

This gives a controlled reviewed-reference alignment for residue-level comparison.

Caution:

This is not a final broad evolutionary alignment. It is a curated reference alignment for the next residue-mapping step.

Next:

Summarize pairwise identity and residue conservation patterns from this alignment.

## 2026-07-04 — Summarized reviewed-reference MAFFT alignment

I summarized pairwise identity between O67940 and the other 13 sequences in the reviewed-reference MAFFT alignment.

Output:

- `results/sequence_alignment/O67940_reviewed_swissprot_alignment_summary.tsv`

Main result:

The highest pairwise identities to O67940 were in the SAM hydrolase group, with RSAMH_METJA at 41.13%.

The chlorinase/fluorinase structural references remained lower and close to each other:

- SALL_SALTO: 28.69%
- 2Q6O_chainA: 28.63%
- 1RQP_chainA: 27.82%

Interpretation:

This supports a broader SAM-related homologous context. It also shows that sequence identity alone does not justify direct substrate-specific transfer from 2Q6O or 1RQP.

Caution:

This is based on the controlled reviewed-reference alignment only. It is not yet a full phylogenetic analysis.

Next:

Map selected functional residues across this reviewed-reference alignment.

## 2026-07-04 — Mapped functional residues across reviewed-reference alignment

I mapped the focal O67940 functional-site positions across the 14-sequence reviewed-reference MAFFT alignment.

Input:

- `results/residue_mapping/functional_residue_mapping_mafft.tsv`
- `results/sequence_alignment/O67940_reviewed_swissprot_reference_set_mafft_alignment.fasta`

Output:

- `results/residue_conservation/O67940_reviewed_reference_functional_residue_mapping_long.tsv`
- `results/residue_conservation/O67940_reviewed_reference_functional_residue_matrix.tsv`

Main result:

The mapping covered 11 O67940 positions across 14 sequences.

The strongest specificity-relevant pattern is at O67940 G127. This position matches 2Q6O, SalL, and the SAM hydrolase-like hits, while 1RQP and the fluorinase hits mostly carry S.

Interpretation:

This supports a cautious residue-level signal away from a direct fluorinase-specific interpretation.

Caution:

The active-site pattern is still mixed. This does not prove O67940 function or substrate specificity.

Next:

Create a compact residue-pattern summary for reporting.

## 2026-07-04 — Summarized reviewed-reference residue patterns

I summarized the reviewed-reference functional residue matrix into a compact report-friendly table.

Output:

- `results/residue_conservation/O67940_reviewed_reference_residue_pattern_summary.tsv`

Main result:

The clearest specificity-relevant signal is at O67940 G127. O67940 matches 2Q6O, SalL, and the SAM hydrolase-major pattern at this position, while 1RQP and the fluorinase-major pattern carry S.

Interpretation:

This supports a cautious residue-level signal away from a direct fluorinase-specific interpretation.

Caution:

The active-site pattern is still mixed across other positions. This evidence is supportive, not definitive.

Next:

Use the reviewed-reference alignment and residue-pattern summary to prepare a short report-ready interpretation section.

## 2026-07-04 — Wrote residue interpretation note

I wrote a short Markdown interpretation of the reviewed-reference residue mapping.

Output:

- `results/residue_conservation/O67940_reviewed_reference_residue_interpretation.md`

Main point:

The G127 pattern is the strongest specificity-relevant signal. O67940 matches 2Q6O, SalL, and the SAM hydrolase-major pattern at this site, while 1RQP and the fluorinase-major pattern carry S.

Caution:

The broader active-site pattern remains mixed. This supports a cautious interpretation but does not prove chlorinase activity or substrate specificity.

Next:

Use this interpretation to guide the next decision: either broader homolog search or a first phylogeny from the reviewed-reference alignment.

## 2026-07-04 — Prepared phylogeny-safe reviewed-reference alignment

I created a cleaned-label version of the 14-sequence reviewed-reference MAFFT alignment for tree building.

Input:

- `results/sequence_alignment/O67940_reviewed_swissprot_reference_set_mafft_alignment.fasta`

Outputs:

- `results/phylogeny/O67940_reviewed_swissprot_reference_set_phylogeny_input.fasta`
- `results/phylogeny/O67940_reviewed_swissprot_reference_set_label_map.tsv`

Why:

The original alignment headers contain spaces, pipes, and metadata fields. These are useful for interpretation, but they can make Newick tree labels messy. The cleaned FASTA keeps simple labels, while the label map preserves the full metadata.

Caution:

This prepares a small reviewed-reference tree input. It is not a final broad evolutionary dataset.

Next:

Check available tree-building tools and run a first reviewed-reference phylogeny.

## 2026-07-04 — Installed FastTree for reviewed-reference phylogeny

I checked for available tree-building tools and none were present in the active environment.

I installed FastTree through Conda/Bioconda for the first reviewed-reference context tree.

Why FastTree:

This next tree uses only the small 14-sequence reviewed-reference alignment. The goal is to inspect broad placement in this curated set, not to claim a final phylogenetic reconstruction.

Caution:

FastTree output will be treated as a first contextual tree. A broader or publication-final phylogeny may require a larger curated homolog set and a more formal tree workflow.

Next:

Run FastTree on the cleaned-label reviewed-reference alignment.

## 2026-07-30 — Wrote reviewed-reference phylogeny interpretation

I wrote a short interpretation note for the first reviewed-reference FastTree result.

Output:

- `results/phylogeny/O67940_reviewed_reference_phylogeny_interpretation.md`

Main point:

O67940_AQUAE groups closest to RSAMH_METJA in the small reviewed-reference tree. 2Q6O/SALL_SALTO and 1RQP/FLA_STRCT form close reference pairs.

Interpretation:

The tree is consistent with the pairwise identity and residue-pattern layers. It supports broad SAM-related placement and does not support direct fluorinase-specific annotation.

Caution:

This is a small reviewed-reference context tree only. It is not a final broad phylogenetic reconstruction.

Next:

Decide whether to expand to a broader homolog search for a larger curated phylogeny.

## 2026-08-07 — Surveyed broader UniProtKB Pfam candidate space

I queried UniProtKB for non-fragment proteins carrying both PF01887 and PF20257.

Output:

- `results/homolog_context/O67940_uniprot_pfam_broader_candidate_space_survey.tsv`

Main result:

The initial length-filtered query returned 4432 candidates: 11 reviewed and 4421 unreviewed. Tightening the length range did little to reduce the set.

The fluorinase and chlorinase protein-name counts were almost identical, suggesting extensive label overlap. These names will not be used as independent functional classes.

Caution:

This is a Pfam-constrained candidate survey, not a final homolog set or functional classification.

Next:

Measure overlap among the protein-name queries before downloading broader metadata.

## 2026-08-07 — Measured UniProtKB protein-name query overlap

I compared accession sets returned by the fluorinase, chlorinase, and hydrolase protein-name queries within the broader PF01887/PF20257 candidate space.

Main result:

The fluorinase and chlorinase result sets were almost completely overlapping: 2017 entries occurred in both sets, leaving only 16 fluorinase-only and 15 chlorinase-only entries.

The hydrolase set was much more distinct, with 112 of 113 entries unique to that query.

Interpretation:

Fluorinase and chlorinase protein-name searches cannot be used as independent functional classes here. Broader homolog selection will therefore rely on sequence evidence rather than these annotation names.

Next:

Download the complete PF01887/PF20257 candidate metadata and sequences, then rank candidates by direct similarity to O67940.

## 2026-08-07 — Broader UniProtKB candidate set and PHMMER ranking

Downloaded and validated the 4432-sequence PF01887/PF20257 UniProtKB candidate set, then ranked it against O67940 with PHMMER.

PHMMER returned 4432 hits (4431 non-self). Diagnostic checks recovered all 11 reviewed anchors and showed that neither a strict coverage cutoff nor a simple top-N ranking is appropriate.

Details:
- `results/homolog_context/O67940_broader_homolog_strategy.md`
- `results/homolog_context/broader_phmmer/O67940_broader_phmmer_interpretation.md`

Next: inspect taxonomic outliers and redundancy before broader phylogenetic sampling.

## 2026-08-07 — Audited non-prokaryotic broader-homolog candidates

Ten PF01887/PF20257 candidates fell outside Bacteria and Archaea: four Entamoeba, four Geodia barretti, and two ciliates.

All are unreviewed and inferred from homology, but several show strong PHMMER similarity to O67940. They will not be removed before redundancy analysis.

Detailed audit:

- `results/homolog_context/O67940_non_prokaryotic_candidate_taxonomic_audit.md`

## 2026-08-09 — Broader-candidate redundancy sensitivity analysis

MMseqs2 clustering was compared at 95%, 90%, 80%, and 70% identity with 80% bidirectional coverage.

The 90% threshold was retained for redundancy pruning: it produced 2858 clusters while keeping O67940 and all reviewed anchors in distinct clusters. Lower thresholds began merging reviewed-reference diversity.

Details:

- `results/homolog_context/redundancy_mmseqs/O67940_mmseqs_redundancy_interpretation.md`

## 2026-08-25 — Remaining execution plan reviewed and frozen

The publication-upgrade roadmap was revised after an independent methodological review.

Key clarifications concern DALI ordering, neutral cluster-representative selection, full-set analysis before additional sampling, separation of global and tree-aware residue analysis, and avoiding method additions without a defined scientific question.

Canonical plan:

- `docs/publication_upgrade_remaining_execution_plan.md`

Review record:

- `docs/review_notes/2026-08-25_execution_plan_independent_review.md`
