# 3. Results

## 3.1 O67940_AQUAE remains unresolved in current curated annotation

The first result addressed a basic but important question: has O67940_AQUAE become experimentally characterized since the original study, or does the biological problem still remain? The parsed UniProtKB record showed that O67940_AQUAE remains an unreviewed TrEMBL entry and is still named “Uncharacterized protein.” No UniProt FUNCTION comment, Gene Ontology annotation, or PDB cross-reference was found in the parsed record. The protein existence level was PE=3, meaning that the protein is inferred from homology rather than direct protein-level evidence.

These results are summarized in Table 1 and are available in the generated output file `results/uniprot_O67940_record_summary.txt`.

| Field | Result |
|---|---|
| UniProt accession | O67940 |
| Entry name | O67940_AQUAE |
| Entry type | UniProtKB unreviewed / TrEMBL |
| Protein name | Uncharacterized protein |
| Organism | *Aquifex aeolicus* strain VF5 |
| Protein existence | PE=3, inferred from homology |
| Sequence length | 251 amino acids |
| UniProt FUNCTION comment | None found |
| GO annotation | None found |
| PDB cross-reference | None found |
| Modern cross-references | InterPro, Pfam, eggNOG, KEGG, AlphaFoldDB |

**Table 1.** Current UniProtKB annotation status of O67940_AQUAE.

This result matters because it shows that the original problem has not disappeared. O67940_AQUAE is not simply a historical “unknown protein” that has since received a reviewed curated function. It remains unresolved at the curated annotation level, which justifies revisiting the original structure-guided function-inference workflow using current resources (Mazumder and Vasudevan, 2008; UniProt Consortium, 2025).

## 3.2 Current InterPro/Pfam evidence supports a SAM-related family/domain context

The current UniProtKB record was not empty: it contained modern computational cross-references. InterPro and Pfam metadata showed that O67940_AQUAE is associated with N-terminal and C-terminal SAM_HAT domains and with the S-adenosyl-L-methionine hydroxide adenosyltransferase family/domain context. The full output is available in `results/O67940_interpro_pfam_metadata.tsv`.

| Database | Accession | Name / short name | Type |
|---|---|---|---|
| InterPro | IPR046469 | SAM_HAT_N | Domain |
| InterPro | IPR046470 | SAM_HAT_C | Domain |
| InterPro | IPR002747 | SAM_OH_AdoTrfase | Family |
| Pfam | PF01887 | SAM_HAT_N | Domain |
| Pfam | PF20257 | SAM_HAT_C | Domain |

**Table 2.** Main InterPro/Pfam evidence for O67940_AQUAE.

This result adds an important layer of interpretation. O67940_AQUAE is not a completely isolated unknown sequence; it sits inside a recognizable SAM-related family/domain context. However, this evidence remains broad. Family and domain labels can support a general biochemical context, but they do not by themselves distinguish chlorinase, fluorinase, or another halogenase-related activity. For that reason, the InterPro/Pfam result was treated as family-level support, not as direct proof of exact substrate specificity (Blum et al., 2025; Mistry et al., 2021).

## 3.3 AlphaFoldDB provides a high-confidence predicted structural model

The AlphaFoldDB v6 model was analysed to determine whether the predicted structure was suitable for modern structural comparison. The model contained 251 residues. The mean pLDDT was 96.70, the median pLDDT was 97.69, and no residue had pLDDT below 70. Most residues were in the very high confidence range. The complete summary is available in `results/alphafold/O67940_alphafold_plddt_summary.txt`.

| AlphaFold confidence metric | Value |
|---|---:|
| Number of residues | 251 |
| Mean pLDDT | 96.70 |
| Median pLDDT | 97.69 |
| Minimum pLDDT | 77.56 |
| Maximum pLDDT | 98.88 |
| Residues with pLDDT ≥ 90 | 242 |
| Residues with pLDDT 70–90 | 9 |
| Residues with pLDDT < 70 | 0 |

**Table 3.** AlphaFoldDB local confidence summary for O67940_AQUAE.

The domain-level PAE analysis also supported structural inspection. Using UniProt-derived domain boundaries, the internal mean PAE was 2.33 Å for the N-terminal SAM_HAT domain and 1.83 Å for the C-terminal SAM_HAT domain. The mean PAE between the two domains was 4.03 Å. The output is available in `results/alphafold/O67940_alphafold_pae_by_domain_summary.txt`.

| Region compared | Mean PAE (Å) | Interpretation |
|---|---:|---|
| N-terminal SAM_HAT domain internal | 2.33 | Low predicted internal uncertainty |
| C-terminal SAM_HAT domain internal | 1.83 | Low predicted internal uncertainty |
| Between N-terminal and C-terminal domains | 4.03 | Moderate but still relatively low predicted inter-domain uncertainty |

**Table 4.** Domain-level AlphaFold predicted aligned error summary.

Together, the pLDDT and PAE results support using the AlphaFoldDB model as a modern structural evidence layer. This does not mean AlphaFold proves biochemical function. It only means the predicted model appears suitable for structural inspection and comparison in this computational re-analysis (Jumper et al., 2021; Varadi et al., 2024).

**Figure 2.** AlphaFoldDB v6 pLDDT profile for O67940_AQUAE, with UniProt-derived domain boundaries marked.

## 3.4 Structural comparison shows strong fold-level similarity to both reference enzymes

The experimentally solved reference structures 2Q6O and 1RQP were retrieved from RCSB PDB and chain A was extracted from each structure. O67940_AQUAE AlphaFold chain A was then compared with both references using TM-align. The full summary is available in `results/structure_comparison/tmalign_pairwise_summary.tsv`.

| Comparison | Aligned length | RMSD (Å) | Sequence identity over aligned residues | TM-score normalized by reference |
|---|---:|---:|---:|---:|
| O67940_AQUAE vs 2Q6O | 250 | 2.01 | 0.288 | 0.85311 |
| O67940_AQUAE vs 1RQP | 250 | 2.01 | 0.268 | 0.78998 |
| 2Q6O vs 1RQP | 267 | 1.89 | 0.378 | 0.85589 |

**Table 5.** Pairwise TM-align structural comparison summary.

The result shows that O67940_AQUAE is globally structurally similar to both experimentally characterized references. The reference-normalized TM-score was higher against 2Q6O than against 1RQP, suggesting a modest structural preference toward the chlorinase-related reference. However, this must be interpreted carefully. A high fold-level similarity supports structural relatedness, but it does not by itself prove identical enzymatic function or substrate specificity (Zhang and Skolnick, 2005).

**Figure 3.** TM-align structural-comparison summary.

## 3.5 Global sequence identity does not resolve specificity

The MAFFT alignment provided a sequence-level comparison between O67940_AQUAE, 2Q6O chain A, and 1RQP chain A. The output is available in `results/sequence_alignment/O67940_2Q6O_1RQP_alignment_summary.tsv`.

| Pairwise comparison | Identical positions | Compared positions | Identity excluding gap columns |
|---|---:|---:|---:|
| O67940_AQUAE vs 2Q6O | 74 | 249 | 0.2972 |
| O67940_AQUAE vs 1RQP | 74 | 250 | 0.2960 |
| 2Q6O vs 1RQP | 105 | 267 | 0.3933 |

**Table 6.** MAFFT pairwise sequence identity summary.

This result is one of the clearest examples of why direct annotation transfer would be risky. O67940_AQUAE is almost equally similar to 2Q6O and 1RQP at the global sequence level. The difference between 0.2972 and 0.2960 is too small to justify assigning precise function from global sequence identity alone. This supports the original paper’s logic: when global similarity is informative but not decisive, interpretation must move toward structural context and functional-residue analysis (Mazumder and Vasudevan, 2008; Katoh and Standley, 2013).

## 3.6 Functional-residue mapping provides the strongest local evidence

The strongest functional clue came from residue mapping. The full mapping is available in `results/residue_mapping/functional_residue_mapping_mafft.tsv`, and the focused report-level summary is available in `results/residue_mapping/focused_functional_residue_summary.tsv`.

| Focused site | O67940_AQUAE | 2Q6O | 1RQP | Interpretation |
|---|---:|---:|---:|---|
| Tyr/Thr-related site | Val67 | Thr70 | Thr75 | O67940 does not directly match the fluorinase Thr pattern |
| Gly/Ser-related site | Gly127 | Gly131 | Ser158 | O67940 matches the 2Q6O Gly pattern rather than 1RQP Ser158 |
| C-terminal caution | Val229 | Leu250 | Arg277 | Original 2Q6O Arg250 did not match current direct coordinate numbering |
| C-terminal caution | Val231 | Gln252 | Ala279 | Original 2Q6O Glu252 did not match current direct coordinate numbering |

**Table 7.** Focused functional-residue mapping summary.

The key result is the Gly127 position. O67940_AQUAE Gly127 aligns with 2Q6O Gly131 rather than 1RQP Ser158. This supports the original cautious interpretation that O67940_AQUAE should not be assigned direct fluorinase-specific function based on broad similarity alone.

The Val67 position is also informative, but more nuanced. In the current downloaded 2Q6O coordinate file, residue 70 is Thr rather than Tyr, consistent with the Tyr70Thr mutation context discussed in the original paper. This was not treated as an error in the workflow. Instead, it was documented as a construct/mutation context that must be considered during residue interpretation.

The two C-terminal cautions are also important. The original paper listed 2Q6O Arg250 and Glu252, but direct inspection of the downloaded 2Q6O chain A coordinate file showed Leu250 and Gln252. This means the full residue table should not be described as perfectly reproduced. The key Val67/Gly127 mapping is supported, but some residue-numbering or construct-level differences remain.

**Figure 4.** Focused residue mapping at the two specificity-related aligned sites.

## 3.7 Integrated evidence supports cautious annotation transfer, not experimental proof

The final evidence integration table is available in `results/evidence_integration/evidence_integration_table_short.tsv`. It was used to separate what each evidence layer supports from what it does not prove.

| Evidence layer | Main result | Interpretation | Main limitation |
|---|---|---|---|
| UniProtKB status | Entry remains unreviewed and uncharacterized | Original problem remains relevant | Database status is not biochemical evidence |
| InterPro/Pfam | SAM_HAT domains and SAM-related family context | Supports broad family/domain membership | Does not resolve exact specificity |
| AlphaFoldDB | High pLDDT and low domain-level PAE | Supports structural inspection | Predicted structure is not experimental validation |
| TM-align | Strong fold similarity to both references, higher against 2Q6O | Supports relatedness and modest 2Q6O preference | Fold similarity does not prove function |
| MAFFT | O67940 identity nearly tied to 2Q6O and 1RQP | Sequence identity alone is not decisive | No full phylogeny performed |
| Residue mapping | Val67/Gly127 mapping reproduced | Strongest support for cautious non-fluorinase-specific interpretation | Some C-terminal residue discrepancies remain |

**Table 8.** Integrated evidence summary.

Taken together, the results support a SAM-dependent halogenase-related interpretation for O67940_AQUAE, with evidence leaning closer to the chlorinase-related reference than to direct fluorinase-specific assignment. The most important point is not that one tool “solved” the protein. The interpretation comes from the convergence of database status, domain evidence, predicted-structure confidence, structural comparison, sequence alignment, and residue-level mapping.

This remains computational evidence. It supports a functional hypothesis, but it does not experimentally validate enzyme activity or exact substrate specificity.
