# Report claim-control sheet

## Purpose

This sheet controls what the final report is allowed to claim. It separates strong claims, cautious interpretations, and claims that should be avoided.

## Strong claims supported by the workflow

1. O67940_AQUAE remains unreviewed/uncharacterized at the current UniProtKB curated-function level.
   - Evidence: `results/uniprot_O67940_record_summary.txt`

2. O67940_AQUAE has modern InterPro/Pfam support for SAM_HAT N-terminal and C-terminal domain context.
   - Evidence: `results/O67940_interpro_pfam_metadata.tsv`

3. The AlphaFoldDB v6 model has high local confidence and low domain-level PAE.
   - Evidence:
     - `results/alphafold/O67940_alphafold_plddt_summary.txt`
     - `results/alphafold/O67940_alphafold_pae_by_domain_summary.txt`

4. O67940_AQUAE is globally structurally similar to both 2Q6O and 1RQP, with a modest TM-align preference toward 2Q6O.
   - Evidence: `results/structure_comparison/tmalign_pairwise_summary.tsv`

5. Global MAFFT sequence identity is nearly tied between O67940 vs 2Q6O and O67940 vs 1RQP.
   - Evidence: `results/sequence_alignment/O67940_2Q6O_1RQP_alignment_summary.tsv`

6. Focused residue mapping reproduces the key O67940 Val67 and Gly127 positions discussed in the original paper.
   - Evidence:
     - `results/residue_mapping/focused_functional_residue_summary.tsv`
     - `notes/residue_mapping/focused_residue_summary_interpretation.md`

## Cautious interpretations allowed

1. The combined evidence supports a SAM-dependent halogenase-related interpretation.
2. The evidence leans closer to the chlorinase-related reference than to direct fluorinase-specific assignment.
3. The modern re-analysis broadly agrees with the original paper's cautious conclusion.
4. The workflow supports a functional hypothesis, not experimental proof.

## Claims to avoid

1. Do not claim that O67940_AQUAE is experimentally proven to be a chlorinase.
2. Do not claim that AlphaFold proves function.
3. Do not claim that TM-align proves enzyme activity.
4. Do not claim that MAFFT alone resolves specificity.
5. Do not claim complete reproduction of all ten original workflow steps.
6. Do not claim full reproduction of the original phylogenetic analysis.
7. Do not claim full reproduction of the original Table 2 without mentioning C-terminal discrepancies.

## Main limitations to mention

1. The workflow is computational.
2. No biochemical validation was performed.
3. No full homolog phylogenetic reconstruction was performed.
4. Not all ten original steps were reproduced.
5. Functional-residue mapping used MAFFT and current PDB numbering, leading to some C-terminal discrepancies in 2Q6O.
