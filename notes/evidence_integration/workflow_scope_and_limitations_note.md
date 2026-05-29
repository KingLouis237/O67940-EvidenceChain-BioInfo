# Workflow scope and limitations

## Why this note is needed

The modern re-analysis supports the original paper's cautious functional interpretation, but it should not be presented as a complete experimental or historical reproduction of the original ten-step workflow.

## Biochemical validation not performed

This workflow is computational. It does not experimentally test whether O67940_AQUAE can catalyze halogenation of SAM.

A biochemical validation would require laboratory experiments such as cloning/expression of the O67940_AQUAE protein, protein purification, incubation with SAM and halide ions, and product detection using analytical chemistry methods such as LC-MS or HPLC/MS.

Therefore, the workflow can support a functional hypothesis, but it cannot prove exact enzyme activity or substrate specificity.

## Full phylogenetic reconstruction not performed

The original paper extracted homologous sequences, generated a structure-guided alignment, manually inspected the alignment, and constructed a neighbor-joining phylogenetic tree. This helped evaluate whether O67940_AQUAE clustered directly with 1RQP or 2Q6O.

This modern re-analysis did not retrieve a broad homolog set or reconstruct a full phylogenetic tree. Instead, it focused on the query protein and the two main experimentally characterized reference structures, 2Q6O and 1RQP.

## Complete reproduction of all ten steps not performed

The original paper's ten-step workflow included PSI-BLAST, pairwise alignment, PIRSF/COG/Pfam/PROSITE scans, SCOP/VAST structural searches, homolog extraction, structure-guided alignment, phylogenetic analysis, functional-residue identification, conserved-residue mapping, and final evidence-based assignment.

This project modernized selected evidence layers instead of reproducing every historical tool step. The workflow focused on:

- current UniProtKB status;
- InterPro/Pfam family-domain evidence;
- AlphaFoldDB predicted-structure confidence;
- RCSB PDB reference structures;
- TM-align structural comparison;
- MAFFT sequence alignment;
- functional-residue mapping.

## Final interpretation rule

The project should be described as a bounded modern computational re-analysis. It supports the original paper's cautious halogenase-related interpretation, with evidence leaning closer to the chlorinase-related reference than the fluorinase reference, but it does not experimentally prove exact substrate specificity.
