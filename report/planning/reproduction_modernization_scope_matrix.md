
# Reproduction and modernization scope

## Why this note exists

This project revisits the Mazumder and Vasudevan O67940_AQUAE case study using current databases, structural resources, and a more reproducible workflow.

The goal is not to claim perfect historical reproduction.

The more honest framing is:

> a reproducible modern re-analysis of selected evidence layers from a published structure-guided protein function inference workflow.

---

# Status legend

| Symbol | Meaning                            |
| ------ | ---------------------------------- |
| 🟢     | Reproduced                         |
| 🟡     | Modernized or partially reproduced |
| 🔴     | Not reproduced                     |
| ⚠️     | Important limitation or caution    |

---

# Workflow scope summary

| Workflow component               | Status | What was done                                                     | Main limitation                                  |
| -------------------------------- | ------ | ----------------------------------------------------------------- | ------------------------------------------------ |
| O67940_AQUAE query selection     | 🟢     | Same UniProt accession used                                       | Current database state differs from 2008         |
| Current UniProt annotation       | 🟡     | Modern UniProt FASTA + JSON parsed                                | Database annotation ≠ biochemical proof          |
| PSI-BLAST against nr             | 🔴     | Not fully repeated                                                | Original hit space not reproduced                |
| Reference proteins (2Q6O / 1RQP) | 🟡     | Current RCSB structures retrieved                                 | Current numbering may differ                     |
| Domain/family evidence           | 🟡     | InterPro/Pfam metadata retrieved                                  | Original PIRSF/COG workflow not fully reproduced |
| SCOP/VAST structural search      | 🔴     | Replaced by modern structural comparison layer                    | Modernization, not direct reproduction           |
| O67940 structure availability    | 🟡     | AlphaFoldDB model retrieved and assessed                          | Predicted structure, not experimental            |
| Chain extraction                 | 🟡     | Chain A extracted for comparison                                  | Ignores oligomer/interface context               |
| Structural comparison            | 🟡     | TM-align selected for pairwise comparison                         | Structural similarity ≠ identical function       |
| Runtime reproducibility tracking | 🟡     | Conda env, checksums, provenance tables, runtime notes added      | Cannot eliminate all system differences          |
| Multiple sequence alignment      | 🟡     | MAFFT alignment performed                                         | Not full broad homolog alignment                 |
| Homolog extraction               | 🔴     | Not performed                                                     | Limited evolutionary context                     |
| Phylogenetic reconstruction      | 🔴     | No phylogenetic tree built                                        | Evolutionary analysis incomplete                 |
| Functional residue mapping       | 🟡     | Key residues mapped across alignment                              | Mapping depends on alignment quality             |
| Table 2 residue mapping          | 🟡     | Key Val67/Gly127 mapping reproduced                               | Some residue numbering mismatches remained       |
| Biochemical validation           | 🔴     | No wet-lab validation                                             | Function cannot be experimentally confirmed      |
| Final functional interpretation  | 🟡     | Evidence supports SAM-dependent halogenase-related interpretation | Remains computational hypothesis                 |

---

# Important runtime note

⚠️ TM-align was correctly callable in the Conda environment, but pairwise structural alignment failed during execution with exit code 132/SIGILL.

This was documented as a software/runtime reproducibility issue rather than hidden from the workflow narrative.

---

# Final interpretation boundary

This project does not claim full reproduction of the original ten-step workflow.

The strongest defensible conclusion is:

> Current computational evidence still supports interpreting O67940_AQUAE as a SAM-dependent halogenase-related protein, with evidence leaning closer to the chlorinase-related reference than to a direct fluorinase-specific assignment.

Exact biochemical specificity remains experimentally unvalidated.

---

# NB

This project is strongest when understood as a reproducible and cautious modern re-analysis, not as a perfect recreation of the original paper.

