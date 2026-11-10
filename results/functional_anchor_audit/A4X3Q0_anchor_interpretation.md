# A4X3Q0 / SalL functional-anchor interpretation

## Candidate

- UniProt accession: `A4X3Q0`
- UniProt entry: `SALL_SALTO`
- Organism: *Salinispora tropica* CNB-440
- Final audit status: `direct_functional_anchor`

## Identity bridge

Current A4X3Q0 is a 283-residue reviewed UniProt sequence.

The historical GenBank-linked sequence `ABP53500.1` is exactly identical to
current A4X3Q0 at all 283 residues.

The deposited wild-type SalL polymer in PDB `2Q6I` is also exactly identical
to current A4X3Q0 at all 283 residues.

The primary SalL study states that `salL` was amplified directly from
*S. tropica* CNB-440 genomic DNA, expressed in *E. coli*, and purified after
removal of the N-terminal His8 tag.

Together, these observations resolve the biological candidate identity
strongly enough to connect the direct biochemical experiments to A4X3Q0.

The exact post-cleavage recombinant termini were not independently
reconstructed in this audit. For that reason, the biochemical evidence rows
retain `construct_state = unclear`, even though the candidate identity itself
is resolved.

## Direct biochemical evidence

Wild-type recombinant SalL was directly assayed with SAM and halides.

The study detected formation of halogenated 5'-deoxyadenosine products with:

- chloride;
- bromide;
- iodide.

For chloride, the reported apparent values included approximately:

- `kcat = 0.9 min^-1`;
- `Km(SAM) = 1 uM`;
- `Km(Cl-) = 45 mM`.

The reaction products were analyzed by HPLC and their identities were checked
using authentic standards and LC/(+)ESI-MS.

This is direct biochemical evidence for SAM-dependent halogenation by the
exact A4X3Q0 biological candidate.

## Fluoride result

Fluoride was deliberately tested.

No fluoride-dependent halogenase activity was detected using either the
standard assay or the coupled-enzyme assay used to suppress the reverse
reaction.

This is a genuine negative experiment rather than an absence of evidence.

The supported claim is therefore:

> fluoride-dependent SalL activity was not detected under the reported assay
> conditions.

It should not be expanded into the stronger claim that fluoride chemistry is
impossible under every possible condition.

## Experimental structural evidence

PDB `2Q6I` is assigned by the primary paper to wild-type SalL complexed with
5'-chloro-5'-deoxyadenosine and L-methionine.

The deposited 2Q6I polymer sequence is exactly identical to current A4X3Q0.

This makes 2Q6I an appropriate wild-type SalL structural reference for later
active-site comparison.

The following historical structures must remain distinct:

- `2Q6I` — wild-type SalL;
- `2Q6K` — wild-type SalL;
- `2Q6O` — SalL Y70T mutant;
- `2Q6L` — SalL Y70T/G131S double mutant.

In particular, `2Q6O` must not be used as the wild-type SalL active-site
reference.

## Candidate-level conclusion

A4X3Q0 satisfies the frozen criteria for a `direct_functional_anchor`.

The direct anchor claim is:

> A4X3Q0 / SalL is an experimentally demonstrated SAM-dependent halogenase
> that accepts chloride, bromide and iodide, while fluoride-dependent activity
> was not detected under the tested conditions.

For the O67940 comparative analysis, A4X3Q0 can therefore define the
experimentally grounded SalL-like non-fluorinating halogenase side of the
primary functional comparison.

This classification does not by itself establish:

- the exact halide specificity of O67940;
- that O67940 shares the same active-site mechanism;
- that individual SalL specificity residues are sufficient functional markers;
- that the SalL oligomeric state applies to O67940;
- or that mutant SalL structures represent wild-type pocket geometry.

Mutant-specific mechanistic evidence is intentionally deferred to the later
pocket-specificity stage if that analysis remains necessary after the early
publication-value checkpoint.
