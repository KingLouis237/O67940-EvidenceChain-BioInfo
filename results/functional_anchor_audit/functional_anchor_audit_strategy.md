# O67940 functional-anchor audit strategy

## Purpose

This audit tests which reviewed reference proteins currently used in the
O67940 publication upgrade are supported by direct experimental evidence
for the biochemical functions attributed to them.

The starting set contains 11 reviewed UniProtKB reference proteins recovered
in the existing PHMMER analysis.

Reviewed database status is not treated as equivalent to direct experimental
functional characterization.

## Core question

For each candidate reference protein:

1. What exact biochemical or structural claim is being made?
2. Was the exact candidate protein experimentally studied?
3. What experiment was performed?
4. What result was actually observed?
5. Was the studied protein wild-type, mutant, truncated or engineered?
6. Does the evidence establish biochemical activity, provide structural or
   mechanistic context only, or represent transferred/database annotation?
7. What claim can therefore be used safely in downstream phylogenetic and
   active-site analyses?

## Evidence unit

The basic audit unit is one evidence record addressing one specific claim
about one candidate protein.

A protein may therefore have multiple evidence records.

This prevents different evidence types, such as biochemical activity,
substrate specificity, structure and mutagenesis, from being collapsed into
a single experimental yes/no label.

## Claim categories

Controlled claim categories are:

- biochemical_activity
- substrate_specificity
- stereoselectivity
- catalytic_mechanism
- catalytic_residue
- experimental_structure
- oligomeric_state
- in_vivo_role
- database_annotation

Additional categories should only be introduced if the existing vocabulary
cannot represent a scientifically distinct claim.

## Evidence types

Evidence types may include:

- direct_biochemical_assay
- mutagenesis
- experimental_structure
- genetic_experiment
- isotope_labelling
- database_annotation
- homology_inference

The experimental procedure and observed result must still be recorded
separately.

## Evidence direction

Each evidence record is classified as:

- supports
- contradicts
- qualifies
- neutral

A deliberately tested negative result is evidence.

Failure to find a test or failure of a paper to mention a property is not
treated as evidence that the property is absent.

## Exact-protein rule

Evidence from the exact candidate protein must be distinguished from
evidence obtained from a homolog.

Homolog evidence may support mechanistic interpretation but does not by
itself experimentally validate the candidate protein's exact biochemical
activity.

## Construct-state rule

Experimental structures and assays must distinguish:

- wild_type
- mutant
- truncated
- engineered
- not_applicable
- unclear

Mutant or engineered structures must not be silently interpreted as
wild-type active-site configurations.

## Source hierarchy

Primary experimental publications and primary structural records are used
to establish experimental support.

Current UniProtKB annotations are useful for identifying claims,
cross-references and evidence provenance, but database labels alone are not
treated as biochemical validation.

Reviews and secondary literature may help identify primary evidence but do
not replace the primary source when the primary source is available.

## Source traceability rule

Each evidence record must be traceable to the source from which the claim
was evaluated.

The evidence table will therefore distinguish:

- source_type
- source_id
- source_locator
- raw_evidence_file

`source_type` describes where the evidence came from, such as a primary
publication, PDB record or UniProtKB record.

`evidence_type` describes what kind of evidence was actually obtained, such
as a biochemical assay, mutagenesis experiment, experimental structure or
homology inference.

These concepts must not be collapsed.

When a source is preserved locally, the evidence record should point to the
frozen local source file. `source_locator` should identify the relevant
section, figure, table, assay description or database field closely enough
for the claim to be independently checked.

## Functional-anchor decision

Final anchor status is derived only after evidence collection.

Possible summary states will include:

- direct_functional_anchor
- partial_experimental_anchor
- structural_anchor_only
- annotation_supported_candidate
- not_validated
- unresolved

These states are not stored as properties of individual evidence records.

## Initial priority

The first detailed audits will be:

1. O58212 / RSAMH_PYRHO — SAM hydrolase / hydroxide adenosyltransferase
2. A4X3Q0 / SALL_SALTO — SalL chlorinase
3. Q70GK9 / FLA_STRCT — Streptomyces cattleya fluorinase

These provide the initial hydrolase, chlorinase and fluorinase mechanistic
reference classes.

The remaining reviewed candidates will then be audited using the same rules.

## Claim boundary

Validation as a functional anchor establishes only the experimentally
supported reaction or property.

It does not automatically establish:

- physiological function in the source organism
- substrate preference that was not experimentally tested
- catalytic roles for residues not directly examined
- identical mechanism in O67940
- functional equivalence of sequence or structural homologs
