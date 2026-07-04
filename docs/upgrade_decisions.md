# Upgrade decisions

## 2026-07-04 — First homolog-search database

Decision:

Start with UniProtKB/Swiss-Prot as the first JackHMMER database.

Why:

Swiss-Prot is curated and small enough to search locally. It gives a clean first-pass view before moving to broader and noisier databases.

What this can support:

A first look at whether O67940_AQUAE detects reviewed homologs related to known SAM-dependent halogenase-like proteins.

What this cannot prove:

Swiss-Prot alone cannot define the full homolog space around O67940_AQUAE. No hit, or only weak hits, would not mean O67940 lacks homologs. It also cannot prove substrate specificity or enzyme activity.

Next:

Run JackHMMER against the local Swiss-Prot FASTA, then decide whether a broader UniProtKB/UniRef/reference-proteome search is needed.
