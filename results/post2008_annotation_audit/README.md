# O67940 post-2008 annotation audit

This directory contains the frozen evidence layer used to test whether
O67940 / aq_2196 acquired direct experimental functional characterization
after the 2008 structure-guided analysis.

The audit was completed on 2026-10-15. Individual external-source snapshots
were retrieved on 2026-10-14 and 2026-10-15.

## Scientific question

Has O67940 / aq_2196 acquired direct experimental functional evidence,
a revised experimentally supported identity, or an experimental structure
since the 2008 analysis?

## Evidence structure

`raw/`

Preserved responses and records from UniProt, UniSave, Europe PMC, RCSB,
UniParc and NCBI RefSeq.

`parsed/`

Factual tables regenerated from the preserved raw evidence.

`O67940_post2008_audit_strategy.md`

Defines the audit question, evidence categories and stopping rule.

`O67940_post2008_audit_interpretation.md`

Human-reviewed scientific interpretation.

## Reproduction

Run:

```bash
python scripts/05_evolutionary_active_site_context/run_O67940_post2008_annotation_audit.py
```

Historical UniProt annotation changes are parsed with:

```bash
python scripts/05_evolutionary_active_site_context/audit_unisave_annotation_history.py
```

The driver uses the frozen cached evidence and regenerates factual result
tables. It does not generate the scientific interpretation.

## Main result

Within the defined audit, no direct experimental biochemical
characterization of O67940 / aq_2196 or a sequence-identical alias was
recovered.

The O67940 sequence remained unchanged across 102 UniSave entry versions,
while its annotation changed substantially over time.

Modern databases provide substantially richer family-level context but do
not establish the exact biochemical activity of O67940.

This is a documented negative result across defined resources, not proof
that no experiment exists anywhere.
