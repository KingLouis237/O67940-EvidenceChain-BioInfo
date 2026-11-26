# O67940 DALI neighborhood — UniProt reference audit strategy

## Purpose

The frozen RCSB entity-consolidation layer showed that the 33 unique PDB entries in the empirically defined O67940 high-Z DALI neighborhood map to nine RCSB-linked UniProt accessions.

This layer asks what the current authoritative UniProtKB records report for those nine reference proteins before any broader biological or primary-literature interpretation is performed.

## Frozen upstream state

Frozen commit:

`fdc6895f666b258b7c97b5dee9e9574fb2c3c8b3`

Frozen UniProt consolidation table:

`results/active_site_structure/dali_structural_neighbors/biological_metadata/derived/entity_consolidation/O67940_rcsb_uniprot_consolidation.tsv`

Expected SHA-256:

`619f275436b038ce27d1b4dfece408e21ba5807a77105638786b5be13b42c37f`

The nine accessions must be derived programmatically from this frozen table rather than manually transcribed.

## External source

UniProtKB REST API:

`https://rest.uniprot.org/uniprotkb/{ACCESSION}.json`

One JSON record will be retrieved independently for each accession.

Response headers will be retained alongside each JSON response.

## Raw-data policy

Raw UniProt response bodies and response headers are external evidence.

They must be preserved byte-for-byte after retrieval.

No formatting, newline conversion, JSON reserialization, field removal, or manual editing is permitted in the raw acquisition directory.

Derived tables must be generated separately.

## Initial acquisition validation

The raw acquisition will validate only computational and provenance invariants:

- the frozen upstream table has the expected SHA-256;
- exactly nine unique UniProt accessions are extracted;
- each requested accession returns an HTTP-success response;
- each JSON body parses successfully;
- the returned primary accession matches the requested accession;
- no requested accession is missing;
- no unexpected accession is returned.

Reviewed/unreviewed status, protein names, functional comments, evidence codes, references, catalytic annotations, and cross-references are biological observations and must not be encoded as prespecified PASS criteria.

## Planned annotation fields

After the raw records are frozen, a deterministic parser may extract:

- primary accession;
- UniProtKB entry name;
- reviewed versus unreviewed status;
- protein description and recommended/submitted names;
- organism and taxonomy;
- sequence length and sequence checksum;
- gene names;
- protein existence level;
- UniProt entry version and sequence version;
- annotation update date;
- function comments;
- catalytic activity comments;
- cofactor comments;
- pathway comments;
- subunit comments;
- domain comments;
- sequence-similarity comments;
- keywords;
- EC numbers;
- GO terms;
- InterPro/Pfam cross-references;
- PDB cross-references;
- literature citations linked to the record.

Evidence-bearing annotations must retain their UniProt evidence metadata where available.

## Evidence interpretation policy

A UniProt record is an annotation source, not automatically primary experimental evidence.

Reviewed Swiss-Prot annotation and unreviewed TrEMBL annotation must remain distinguishable.

Protein names, EC numbers, GO terms, domains, family labels, and functional comments must not automatically be converted into claims of experimentally demonstrated activity.

Primary experimental claims relevant to the O67940 interpretation will subsequently be audited against the cited primary literature.

Previously audited experimental anchors remain separate from newly encountered database annotations.

## Biological questions for the later audit

The later audit will determine:

1. which of the nine reference proteins have experimentally supported biochemical functions;
2. which are primarily database/family annotations;
3. which represent already audited calibration proteins;
4. whether the two PDB25-level reference proteins add genuinely independent biological information;
5. whether structural similarity spans proteins with distinct demonstrated or annotated activities.

## Interpretation limits

This UniProt acquisition alone cannot establish:

- O67940 enzymatic activity;
- O67940 substrate specificity;
- orthology;
- evolutionary direction;
- catalytic equivalence;
- shared biochemical state between PDB structures;
- functional equivalence merely from structural similarity.
