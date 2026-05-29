# Step 1 — Current UniProt record check for O67940_AQUAE

## Aim

The first step of the modern re-analysis was to retrieve the current UniProtKB record for O67940_AQUAE, the same *Aquifex aeolicus* protein used in Mazumder and Vasudevan's 2008 case study.

This step was necessary because the original paper explicitly states that its analysis reflected the databases available at the time of writing. Therefore, a modern re-analysis should first establish whether the current annotation status of O67940_AQUAE has changed before running new BLAST, InterPro, structural, or residue-mapping analyses.

## Data retrieved

Source files:

- FASTA sequence: `data/O67940_AQUAE.fasta`
- Full UniProt JSON record: `data/O67940_uniprot_record.json`
- Parsed UniProt summary: `results/uniprot_O67940_record_summary.txt`

Current UniProtKB summary:

| Field | Result |
|---|---|
| Accession | O67940 |
| UniProt ID | O67940_AQUAE |
| Entry type | UniProtKB unreviewed / TrEMBL |
| Protein name | Uncharacterized protein |
| Organism | *Aquifex aeolicus* strain VF5 |
| Taxon ID | 224324 |
| Protein existence | PE=3, inferred from homology |
| Sequence length | 251 amino acids |
| Molecular weight | 28,322 Da |
| InterPro | IPR046470, IPR046469, IPR002747, IPR023227, IPR023228 |
| Pfam | PF20257, PF01887 |
| AlphaFoldDB | O67940 |
| PDB | None found |
| GO | None found |
| eggNOG | COG1912 |
| KEGG | aae:aq_2196 |
| UniProt FUNCTION comment | None found |

## Interpretation

The current UniProtKB record shows that O67940_AQUAE has not become a reviewed, experimentally characterized protein. It remains an unreviewed TrEMBL entry, is still named “Uncharacterized protein,” and has no UniProt FUNCTION comment. This means that the original biological problem has not disappeared: the protein still requires functional interpretation from indirect computational evidence rather than direct curated functional annotation.

At the same time, the current record is richer than a plain unknown entry. It contains InterPro, Pfam, eggNOG, KEGG, and AlphaFoldDB cross-references. These provide modern evidence layers for family/domain analysis and predicted-structure-based investigation. This is important because the modern project is not trying to reproduce every historical database output from 2008; instead, it tests whether updated resources still support the original paper's broad functional inference.

The absence of a PDB cross-reference is also meaningful. It suggests that no experimentally solved structure is directly linked to O67940_AQUAE in the current UniProt record. The presence of an AlphaFoldDB cross-reference means that modern predicted-structure evidence can be added, but this should be interpreted cautiously because predicted structural similarity cannot by itself prove enzymatic activity or substrate specificity.

The absence of GO terms is also relevant. UniProt does not currently assign molecular function, biological process, or cellular component terms to this protein. Therefore, even though InterPro and Pfam provide family-level information, UniProt itself remains cautious at the curated functional annotation level.

## Working conclusion from Step 1

Modern UniProtKB has not resolved the function of O67940_AQUAE, but it has expanded the computational evidence context around the protein. This supports the relevance of a modern re-analysis: O67940_AQUAE remains functionally unresolved at the curated annotation level, while current databases provide additional family/domain and predicted-structure evidence that can be compared with the original 2008 workflow.
