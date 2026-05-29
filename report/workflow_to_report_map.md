# Workflow-to-report map

This document links each computational step to the final article structure.

| Workflow step | Raw data | Script | Processed result | Interpretation note | Report location |
|---|---|---|---|---|---|
| Step 1: UniProt current record check | `data/O67940_AQUAE.fasta`; `data/O67940_uniprot_record.json`; `data/O67940_uniprot_record_pretty.json` | `scripts/parse_uniprot_O67940.py` | `results/uniprot_O67940_record_summary.txt` | `notes/step1_uniprot_current_record_interpretation.md` | Materials & Methods 2.2; Results 3.1 |
| Step 2: InterPro/Pfam metadata retrieval | `data/interpro_pfam/*.json` | `scripts/fetch_interpro_pfam_metadata.py` | `results/O67940_interpro_pfam_metadata.tsv` | `notes/step2_interpro_pfam_metadata_summary.md` | Materials & Methods 2.3; Results 3.2 |
| Step 3: AlphaFoldDB predicted structure | pending | pending | pending | pending | Materials & Methods 2.4; Results 3.3 |
| Step 4: Structural comparison | pending | pending | pending | pending | Materials & Methods 2.5; Results 3.4 |
| Step 5: Functional-residue mapping | pending | pending | pending | pending | Materials & Methods 2.6; Results 3.5 |
| Step 6: Evidence integration | all previous outputs | pending | evidence matrix | pending | Results 3.6; Discussion |

| Step 3: AlphaFoldDB predicted structure and pLDDT confidence | `data/alphafold/AF-O67940-F1-model_v6.pdb`; `data/alphafold/AF-O67940-F1-model_v6.cif`; `data/alphafold/AF-O67940-F1-predicted_aligned_error_v6.json` | `scripts/summarize_alphafold_plddt.py` | `results/alphafold/O67940_alphafold_plddt_summary.txt` | `notes/alphafold/step3_alphafold_structure_interpretation.md` | Materials & Methods 2.4; Results 3.3 |
