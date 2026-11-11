# Q70GK9 / fluorinase functional-anchor interpretation

## Candidate

- UniProt accession: `Q70GK9`
- UniProt entry: `FLA_STRCT`
- Historical organism name: *Streptomyces cattleya*
- Current organism name in UniProt: *Streptantibioticus cattleyicolor*
- Final audit status: `direct_functional_anchor`

## Identity bridge

Current Q70GK9 is a 299-residue reviewed UniProt sequence.

The historical `AJ581748` `fla` CDS translation is exactly identical to
current Q70GK9 at all 299 residues.

The deposited polymer in PDB `1RQP` is also exactly identical to current
Q70GK9 at all 299 residues.

These independent sequence checks provide a direct historical-to-current
identity bridge linking the original fluorinase gene and experimental
structure to the modern Q70GK9 entry.

## Direct biochemical evidence

The 2007 mechanistic study used a wild-type `fla` ORF construct expressed in
*E. coli* C43(DE3).

Purified apo wild-type FDAS was incubated with SAM and KF, and enzymatic
activity was measured by analytical HPLC by monitoring formation of
5'-fluoro-5'-deoxyadenosine (5'-FDA) over time.

This provides direct biochemical evidence that the Q70GK9 biological
candidate catalyses SAM-dependent fluorination.

The exact final recombinant termini were not reconstructed from the audited
methods. The construct was generated using a pHisTev expression system, but
the audited text does not explicitly establish whether the affinity tag was
removed before the biochemical assays.

For that reason, the biochemical evidence record retains:

`construct_state = unclear`

This uncertainty concerns the recombinant construct state, not the identity
of the encoded biological candidate.

## Experimental structural evidence

PDB `1RQP` contains a 299-residue fluorinase polymer exactly identical to
current Q70GK9.

The primary structural study reports the sequence and three-dimensional
structure of the *Streptomyces cattleya* fluorination enzyme.

This makes 1RQP an appropriate experimentally determined Q70GK9 structural
anchor for later active-site comparison.

The structural evidence remains distinct from the biochemical evidence:
exact structural identity alone would not establish catalytic activity, but
here it complements an independently audited direct biochemical assay.

## Candidate-level conclusion

Q70GK9 satisfies the frozen criteria for a `direct_functional_anchor`.

The direct anchor claim is:

> Q70GK9 / FDAS is an experimentally demonstrated SAM-dependent fluorinase
> that catalyses formation of 5'-fluoro-5'-deoxyadenosine from SAM and
> fluoride.

For the O67940 comparative analysis, Q70GK9 can therefore define the
experimentally grounded fluorinase side of the primary functional comparison.

This classification does not establish:

- that O67940 has fluorinase activity;
- that structural similarity to 1RQP implies fluoride specificity;
- that individual fluorinase residues are sufficient specificity markers;
- that Q70GK9 kinetic parameters transfer to O67940;
- or that O67940 shares the same oligomeric or mechanistic details.

Mutant-specific and residue-specific fluorinase evidence remains deferred to
the later mechanistic or pocket-specificity analysis if that stage is still
needed after the early publication-value checkpoint.
