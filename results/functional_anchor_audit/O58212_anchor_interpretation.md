# O58212 functional-anchor interpretation

## Candidate

- UniProt accession: O58212
- Entry name: RSAMH_PYRHO
- Historical protein: PH0463 from *Pyrococcus horikoshii* OT3
- Final audit status: `direct_functional_anchor`

## Functional conclusion

O58212/PH0463 is accepted as a direct functional anchor for
SAM hydroxide adenosyltransferase / SAM-hydrolysing chemistry.

This classification is supported by direct experiments on the
O58212/PH0463 protein sequence rather than by database annotation
or homology alone.

## Direct evidence

### FAE0001 — biochemical activity

Purified recombinant PH0463 showed SAM-dependent enzymatic
conversion, with reported kinetic parameters of approximately
Km(SAM) = 39.2 uM and kcat = 0.14 s^-1.

### FAE0002 — isotope-labelled water

During PH0463-catalysed SAM conversion in H2-18O, approximately
48% 18O incorporation was measured in recovered adenosine.

This directly supports participation of water in the chemistry
leading to the adenosine product.

### FAE0003 — experimental structure

The SAH-bound structure 2WR8 was determined by X-ray diffraction
at 1.77 Angstrom resolution.

The deposited polymer is 259 residues long and consists of an
N-terminal GSH extension followed by the complete unchanged
256-residue O58212 sequence.

The crystallized protein is therefore treated as an engineered
construct of the exact candidate rather than as a distinct homolog.

### FAE0004 — active-site geometry

The PH0463 structure contains the His127-Arg75-Asp68
hydrogen-bonded network and ordered active-site waters near the
SAH C5' region.

The structural observations support hypotheses about water
positioning and activation, but they do not uniquely establish
which water acts as the nucleophile or prove a single
proton-transfer mechanism.

## Homolog-based mechanistic support

The following experiments were performed in a
*Salinispora arenicola* DUF62 homolog rather than directly in
O58212/PH0463:

- FAE0005: D72A, corresponding to PH0463 Asp68, reduced activity
  to a level too low for reliable kinetic determination.
- FAE0006: R79A, corresponding to PH0463 Arg75, retained only
  approximately 0.15% relative turnover.
- FAE0007: H130A retained approximately 25% of wild-type
  catalytic efficiency.
- FAE0008: H130Y retained approximately 5% of wild-type
  catalytic efficiency.

These experiments support a particularly strong functional role
for the Asp and Arg positions while showing that the histidine
position is important but not absolutely required under the
reported assay conditions.

They are mechanistic support from a homolog and must not be
reported as direct O58212 mutagenesis.

## Evidence boundaries

The audit does not establish:

- a uniquely proven proton-relay mechanism;
- unambiguous identity of the true nucleophilic water;
- direct mutational validation of Asp68, Arg75 or His127 in O58212;
- experimentally demonstrated (R)-SAM stereospecificity from the
  evidence audited here;
- an in-vivo physiological role for O58212;
- functional equivalence between O58212 and O67940.

## Audit decision

The combination of exact-sequence biochemical evidence,
isotope-labelling evidence and experimental structural evidence
is sufficient to classify O58212 as a `direct_functional_anchor`
for the hydrolase/HAT side of the DUF62-related
SAM-utilizing landscape.

Mechanistic conclusions beyond that functional classification
remain evidence-calibrated and explicitly qualified.
