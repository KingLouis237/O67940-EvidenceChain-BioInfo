#!/usr/bin/env python3

"""
Reproducible driver for the O67940 post-2008 literature and annotation audit.

Default behaviour is cache-first:
    - validate the canonical O67940 sequence;
    - validate already-preserved raw audit responses;
    - record provenance;
    - do not silently replace historical snapshots.

Live database queries will only occur when --refresh is explicitly used.

Scientific interpretation is deliberately kept outside this script.
The script produces evidence and factual summaries, not a biochemical
function assignment.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------
# Repository paths
# ---------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]

ACCESSION = "O67940"
ENTRY_NAME = "O67940_AQUAE"
EXPECTED_LENGTH = 251
EXPECTED_UNIPARC = "UPI0000056808"
EXPECTED_MD5 = "A7FD3A7D3D0EFE928F0C745A2569BD9D"

FASTA = REPO_ROOT / "data/O67940_AQUAE.fasta"

AUDIT_ROOT = REPO_ROOT / "results/post2008_annotation_audit"
RAW_DIR = AUDIT_ROOT / "raw"
PARSED_DIR = AUDIT_ROOT / "parsed"
UNISAVE_DIR = RAW_DIR / "unisave_versions"

MANIFEST = PARSED_DIR / "O67940_post2008_audit_manifest.tsv"


# ---------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------

def fail(message: str) -> None:
    """Stop immediately rather than continue from inconsistent evidence."""
    raise SystemExit(f"ERROR: {message}")


def sha256(path: Path) -> str:
    """Return SHA256 for one preserved audit artifact."""
    h = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def read_fasta_sequence(path: Path) -> str:
    """Read a single-record FASTA sequence."""

    if not path.exists():
        fail(f"Canonical FASTA not found: {path}")

    sequence = "".join(
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip() and not line.startswith(">")
    ).upper()

    if not sequence:
        fail(f"No sequence recovered from {path}")

    return sequence


def md5_sequence(sequence: str) -> str:
    """UniParc reports an MD5 hash of the amino-acid sequence."""
    return hashlib.md5(sequence.encode()).hexdigest().upper()


def load_json(path: Path):
    """Read JSON with an explicit error on malformed cached evidence."""

    if not path.exists():
        fail(f"Required JSON file missing: {path}")

    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"Malformed JSON in {path}: {exc}")


def latest_matching_file(pattern: str) -> Path:
    """Return the lexicographically latest preserved dated snapshot."""

    matches = sorted(RAW_DIR.glob(pattern))

    if not matches:
        fail(f"No cached files match: {pattern}")

    return matches[-1]


# ---------------------------------------------------------------------
# Canonical sequence validation
# ---------------------------------------------------------------------

def validate_query_sequence() -> dict[str, str]:
    """
    Verify that the sequence used for sequence-based auditing is the
    canonical frozen O67940 project sequence.
    """

    sequence = read_fasta_sequence(FASTA)

    if len(sequence) != EXPECTED_LENGTH:
        fail(
            f"O67940 sequence length is {len(sequence)}, "
            f"expected {EXPECTED_LENGTH}"
        )

    md5 = md5_sequence(sequence)

    if md5 != EXPECTED_MD5:
        fail(
            f"O67940 sequence MD5 is {md5}, "
            f"expected {EXPECTED_MD5}"
        )

    return {
        "sequence_length": str(len(sequence)),
        "sequence_md5": md5,
    }


# ---------------------------------------------------------------------
# Cached evidence validation
# ---------------------------------------------------------------------

def validate_current_uniprot() -> dict[str, str]:
    """Validate the preserved current UniProtKB snapshot."""

    path = latest_matching_file("O67940_uniprot_*.json")
    data = load_json(path)

    accession = data.get("primaryAccession")
    entry_name = data.get("uniProtkbId")
    length = data.get("sequence", {}).get("length")

    if accession != ACCESSION:
        fail(f"Unexpected UniProt accession: {accession}")

    if entry_name != ENTRY_NAME:
        fail(f"Unexpected UniProt entry name: {entry_name}")

    if length != EXPECTED_LENGTH:
        fail(f"Unexpected UniProt sequence length: {length}")

    return {
        "path": str(path.relative_to(REPO_ROOT)),
        "accession": accession,
        "entry_name": entry_name,
        "entry_type": str(data.get("entryType")),
        "sequence_length": str(length),
    }


def validate_uniparc() -> dict[str, str]:
    """Validate the exact-sequence UniParc record."""

    path = RAW_DIR / f"{EXPECTED_UNIPARC}_full_entry.json"
    data = load_json(path)

    upi = data.get("uniParcId")
    length = data.get("sequence", {}).get("length")
    md5 = data.get("sequence", {}).get("md5")

    if upi != EXPECTED_UNIPARC:
        fail(f"Unexpected UniParc identifier: {upi}")

    if length != EXPECTED_LENGTH:
        fail(f"Unexpected UniParc sequence length: {length}")

    if md5 != EXPECTED_MD5:
        fail(f"Unexpected UniParc MD5: {md5}")

    return {
        "path": str(path.relative_to(REPO_ROOT)),
        "uniparc_id": upi,
        "sequence_length": str(length),
        "sequence_md5": md5,
        "cross_reference_count": str(
            len(data.get("uniParcCrossReferences", []))
        ),
    }


def validate_rcsb_results() -> list[dict[str, str]]:
    """
    Validate both preserved RCSB negative searches.

    A zero-hit result is evidence only because the query response itself
    has been preserved.
    """

    checks = [
        (
            "RCSB_UniProt_mapping",
            RAW_DIR / "rcsb_O67940_uniprot_search.json",
        ),
        (
            "RCSB_exact_sequence_100pct",
            RAW_DIR / "rcsb_O67940_exact_sequence_search.json",
        ),
    ]

    results = []

    for label, path in checks:
        data = load_json(path)
        count = int(data.get("total_count", 0))

        results.append({
            "audit_component": label,
            "path": str(path.relative_to(REPO_ROOT)),
            "total_count": str(count),
        })

    return results


def validate_unisave_cache() -> dict[str, str]:
    """Verify that all archived UniSave versions 1–102 are preserved."""

    expected = {
        f"O67940_unisave_v{i:03d}.txt"
        for i in range(1, 103)
    }

    observed = {
        p.name
        for p in UNISAVE_DIR.glob("O67940_unisave_v*.txt")
    }

    missing = sorted(expected - observed)
    extra = sorted(observed - expected)

    if missing:
        fail(
            "Missing UniSave cached versions: "
            + ", ".join(missing)
        )

    if extra:
        fail(
            "Unexpected UniSave cached versions: "
            + ", ".join(extra)
        )

    return {
        "cached_versions": str(len(observed)),
        "version_range": "1-102",
    }


# ---------------------------------------------------------------------
# Derived factual results from frozen cached evidence
# ---------------------------------------------------------------------

def regenerate_uniprot_crossreferences() -> tuple[Path, int]:
    """
    Rebuild the UniProt cross-reference table from the preserved
    current UniProt JSON snapshot.
    """

    source = latest_matching_file("O67940_uniprot_*.json")
    data = load_json(source)

    out = PARSED_DIR / "O67940_uniprot_crossreferences.tsv"

    rows = []

    for xref in data.get("uniProtKBCrossReferences", []):
        properties = {
            p.get("key"): p.get("value")
            for p in xref.get("properties", [])
        }

        rows.append({
            "database": xref.get("database", ""),
            "id": xref.get("id", ""),
            "properties_json": json.dumps(
                properties,
                sort_keys=True,
            ),
        })

    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            lineterminator="\n",
            fieldnames=[
                "database",
                "id",
                "properties_json",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    return out, len(rows)


def regenerate_europepmc_query_summary() -> tuple[Path, int]:
    """
    Summarize all preserved Europe PMC query responses.

    This table records what each frozen query returned without
    deciding whether a hit constitutes direct experimental evidence.
    """

    rows = []

    for path in sorted(RAW_DIR.glob("europepmc_*.json")):
        data = load_json(path)

        request = data.get("request", {})
        results = data.get("resultList", {}).get("result", [])

        identifiers = []
        years = []

        for result in results:
            rid = (
                result.get("pmid")
                or result.get("pmcid")
                or result.get("id")
            )

            if rid:
                identifiers.append(str(rid))

            year = result.get("pubYear")
            if year:
                years.append(str(year))

        rows.append({
            "raw_file": path.name,
            "query": request.get("queryString", ""),
            "hit_count": data.get("hitCount", 0),
            "returned_records": len(results),
            "record_identifiers": ";".join(identifiers),
            "publication_years": ";".join(years),
        })

    out = (
        PARSED_DIR /
        "O67940_europepmc_query_summary.tsv"
    )

    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            lineterminator="\n",
            fieldnames=[
                "raw_file",
                "query",
                "hit_count",
                "returned_records",
                "record_identifiers",
                "publication_years",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    return out, len(rows)


def regenerate_unisave_version_timeline() -> tuple[Path, int]:
    """
    Rebuild the complete UniSave version timeline from the preserved
    history JSON.

    UniSave history metadata, rather than flat-file DT syntax, is the
    authority for entry-version dates.
    """

    source = latest_matching_file(
        "O67940_unisave_history_*.json"
    )

    data = load_json(source)
    records = data.get("results", [])

    if len(records) != 102:
        fail(
            f"Expected 102 UniSave history records, "
            f"found {len(records)}"
        )

    rows = []

    for r in sorted(
        records,
        key=lambda x: int(x["entryVersion"]),
    ):
        rows.append({
            "entry_version": r.get("entryVersion", ""),
            "sequence_version": r.get("sequenceVersion", ""),
            "first_release": r.get("firstRelease", ""),
            "first_release_date": r.get(
                "firstReleaseDate", ""
            ),
            "last_release": r.get("lastRelease", ""),
            "last_release_date": r.get(
                "lastReleaseDate", ""
            ),
            "entry_name": r.get("name", ""),
            "database": r.get("database", ""),
        })

    out = (
        PARSED_DIR /
        "O67940_unisave_version_timeline.tsv"
    )

    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            lineterminator="\n",
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)

    return out, len(rows)


def regenerate_sequence_identical_alias_literature_summary(
) -> tuple[Path, int]:
    """
    Rebuild the focused literature-search summary for sequence-identical
    aliases identified through UniParc.

    This is intentionally separate from the complete Europe PMC query
    summary because it answers the narrower exact-sequence-alias question.
    """

    alias_files = [
        (
            "NP_214509",
            '"NP_214509"',
            RAW_DIR / "europepmc_alias_NP_214509.json",
        ),
        (
            "NP_214509_1",
            '"NP_214509.1"',
            RAW_DIR / "europepmc_alias_NP_214509_1.json",
        ),
        (
            "WP_010881445",
            '"WP_010881445"',
            RAW_DIR / "europepmc_alias_WP_010881445.json",
        ),
        (
            "SEED_224324_1_peg_1524",
            '"fig|224324.1.peg.1524"',
            RAW_DIR /
            "europepmc_alias_SEED_224324_1_peg_1524.json",
        ),
        (
            "SEED_224324_8_peg_1700",
            '"fig|224324.8.peg.1700"',
            RAW_DIR /
            "europepmc_alias_SEED_224324_8_peg_1700.json",
        ),
        (
            "PATRIC_20961220",
            '"20961220" AND "Aquifex"',
            RAW_DIR /
            "europepmc_alias_PATRIC_20961220.json",
        ),
    ]

    rows = []

    for alias, query, path in alias_files:
        data = load_json(path)

        rows.append({
            "alias": alias,
            "query": query,
            "hit_count": data.get("hitCount", 0),
        })

    out = (
        PARSED_DIR /
        "O67940_sequence_identical_alias_literature_summary.tsv"
    )

    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            lineterminator="\n",
            fieldnames=[
                "alias",
                "query",
                "hit_count",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    return out, len(rows)


def regenerate_refseq_summary() -> tuple[Path, int]:
    """
    Extract factual annotation fields from the preserved RefSeq
    GenBank records.

    Multiline GenBank DEFINITION fields, reference TITLE fields and
    quoted feature qualifiers are reconstructed before writing the
    summary. References are retained as record metadata and are not
    interpreted here as direct experimental evidence.
    """

    sources = [
        (
            "WP_010881445.1",
            RAW_DIR / "ncbi_protein_WP_010881445_1.gb",
        ),
        (
            "NP_214509.1",
            RAW_DIR / "ncbi_protein_NP_214509_1.gb",
        ),
    ]

    def collect_top_level_field(
        lines: list[str],
        label: str,
    ) -> str:
        """
        Collect one GenBank top-level field plus its continuation
        lines until another top-level field begins.
        """

        parts = []
        collecting = False

        for line in lines:

            if line.startswith(label):
                collecting = True
                parts.append(line[len(label):].strip())
                continue

            if collecting:
                # GenBank top-level fields occupy columns 1-12.
                # Continuation lines are indented.
                if line.startswith("            "):
                    parts.append(line.strip())
                else:
                    break

        return " ".join(parts).strip()

    def collect_reference_titles(
        lines: list[str],
    ) -> list[str]:
        """
        Recover complete multiline TITLE fields from REFERENCE blocks.
        """

        titles = []
        current = None

        for line in lines:

            if line.startswith("  TITLE"):
                if current is not None:
                    titles.append(" ".join(current).strip())

                current = [
                    line[len("  TITLE"):].strip()
                ]
                continue

            if current is not None:

                # Continuation lines within a reference field.
                if line.startswith("            "):
                    stripped = line.strip()

                    # Stop if the continuation actually begins another
                    # named reference subfield.
                    if (
                        stripped.startswith("JOURNAL")
                        or stripped.startswith("PUBMED")
                        or stripped.startswith("REMARK")
                        or stripped.startswith("AUTHORS")
                        or stripped.startswith("CONSRTM")
                    ):
                        titles.append(
                            " ".join(current).strip()
                        )
                        current = None
                    else:
                        current.append(stripped)

                else:
                    titles.append(
                        " ".join(current).strip()
                    )
                    current = None

        if current is not None:
            titles.append(" ".join(current).strip())

        return titles

    def collect_quoted_qualifiers(
        lines: list[str],
        qualifier: str,
    ) -> list[str]:
        """
        Recover complete quoted GenBank feature qualifiers such as
        /product="..." and /note="..." across continuation lines.
        """

        prefix = f'/{qualifier}="'
        values = []

        collecting = False
        parts = []

        for line in lines:
            stripped = line.strip()

            if not collecting:

                if stripped.startswith(prefix):
                    content = stripped[len(prefix):]

                    # Entire qualifier occurs on one line.
                    if content.endswith('"'):
                        values.append(content[:-1])
                    else:
                        collecting = True
                        parts = [content]

                continue

            # We are inside a multiline quoted qualifier.
            if stripped.endswith('"'):
                parts.append(stripped[:-1])
                values.append(
                    " ".join(parts).strip()
                )
                collecting = False
                parts = []

            else:
                parts.append(stripped)

        if collecting:
            fail(
                f"Unterminated /{qualifier} qualifier "
                "in preserved RefSeq record"
            )

        return values

    rows = []

    for accession, path in sources:

        if not path.exists():
            fail(f"RefSeq GenBank record missing: {path}")

        lines = path.read_text().splitlines()

        definition = collect_top_level_field(
            lines,
            "DEFINITION  ",
        )

        products = collect_quoted_qualifiers(
            lines,
            "product",
        )

        notes = collect_quoted_qualifiers(
            lines,
            "note",
        )

        titles = collect_reference_titles(lines)

        rows.append({
            "accession": accession,
            "raw_file": path.name,
            "definition": definition,
            "product": " | ".join(products),
            "reference_titles": " | ".join(titles),
            "notes": " | ".join(notes),
        })

    out = (
        PARSED_DIR /
        "O67940_refseq_annotation_summary.tsv"
    )

    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            lineterminator="\n",
            fieldnames=[
                "accession",
                "raw_file",
                "definition",
                "product",
                "reference_titles",
                "notes",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    return out, len(rows)



def regenerate_uniparc_crossreferences() -> tuple[Path, int]:
    """
    Rebuild the exact-sequence alias table from the preserved
    UniParc entry.
    """

    source = RAW_DIR / f"{EXPECTED_UNIPARC}_full_entry.json"
    data = load_json(source)

    rows = []

    for xref in data.get("uniParcCrossReferences", []):
        organism = xref.get("organism") or {}

        rows.append({
            "database": xref.get("database", ""),
            "id": xref.get("id", ""),
            "active": xref.get("active", ""),
            "organism": organism.get("scientificName", ""),
            "taxon_id": organism.get("taxonId", ""),
            "version": xref.get("version", ""),
            "created": xref.get("created", ""),
            "last_updated": xref.get("lastUpdated", ""),
        })

    out = (
        PARSED_DIR /
        "O67940_uniparc_crossreferences.tsv"
    )

    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            lineterminator="\n",
            fieldnames=[
                "database",
                "id",
                "active",
                "organism",
                "taxon_id",
                "version",
                "created",
                "last_updated",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    return out, len(rows)


def regenerate_rcsb_summary() -> tuple[Path, int]:
    """
    Rebuild a compact factual summary of the two preserved
    experimental-PDB searches.
    """

    searches = [
        (
            "UniProt_accession_mapping",
            RAW_DIR / "rcsb_O67940_uniprot_search.json",
        ),
        (
            "exact_sequence_100pct_identity",
            RAW_DIR / "rcsb_O67940_exact_sequence_search.json",
        ),
    ]

    rows = []

    for search_name, path in searches:
        data = load_json(path)

        identifiers = [
            str(x.get("identifier"))
            for x in data.get("result_set", [])
            if x.get("identifier")
        ]

        rows.append({
            "search": search_name,
            "raw_file": path.name,
            "http_status": data.get("http_status", ""),
            "total_count": data.get("total_count", 0),
            "query_sequence_length":
                data.get("query_sequence_length", ""),
            "identity_cutoff":
                data.get("identity_cutoff", ""),
            "returned_identifiers":
                ";".join(identifiers),
        })

    out = PARSED_DIR / "O67940_rcsb_search_summary.tsv"

    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            lineterminator="\n",
            fieldnames=[
                "search",
                "raw_file",
                "http_status",
                "total_count",
                "query_sequence_length",
                "identity_cutoff",
                "returned_identifiers",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    return out, len(rows)


def regenerate_unisave_results() -> None:
    """
    Run the specialized UniSave parser against the already-validated
    102-version local cache.

    Because validate_unisave_cache() runs first, this step must not
    require network retrieval.
    """

    script = (
        REPO_ROOT /
        "scripts/05_evolutionary_active_site_context/"
        "audit_unisave_annotation_history.py"
    )

    if not script.exists():
        fail(f"UniSave parser not found: {script}")

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        fail(
            "UniSave parser failed:\n"
            + result.stdout
            + "\n"
            + result.stderr
        )

    required = [
        PARSED_DIR / "O67940_unisave_annotation_history.tsv",
        PARSED_DIR / "O67940_unisave_annotation_change_points.tsv",
    ]

    for path in required:
        if not path.exists():
            fail(
                "Expected UniSave derived result not produced: "
                + str(path)
            )


def regenerate_annotation_milestones() -> tuple[Path, int]:
    """
    Build the small milestone table from the complete UniSave
    annotation-history table.

    Milestones are predefined historical checkpoints rather than
    automatically selected 'interesting' results.
    """

    source = (
        PARSED_DIR /
        "O67940_unisave_annotation_history.tsv"
    )

    if not source.exists():
        fail(f"UniSave history table missing: {source}")

    wanted = {
        1, 7, 8, 33, 44, 70,
        90, 93, 94, 95, 96, 102,
    }

    with source.open() as handle:
        rows = list(
            csv.DictReader(handle, delimiter="\t")
        )

    selected = [
        row
        for row in rows
        if int(row["entry_version"]) in wanted
    ]

    observed_versions = {
        int(row["entry_version"])
        for row in selected
    }

    if observed_versions != wanted:
        missing = sorted(wanted - observed_versions)
        fail(
            "Missing annotation milestone versions: "
            + ", ".join(map(str, missing))
        )

    fields = [
        "entry_version",
        "entry_date",
        "description",
        "protein_existence",
        "function_comment",
        "similarity_comment",
        "InterPro",
        "Pfam",
        "PANTHER",
        "Gene3D",
        "SUPFAM",
    ]

    out = (
        PARSED_DIR /
        "O67940_annotation_history_key_milestones.tsv"
    )

    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            lineterminator="\n",
            fieldnames=fields,
        )

        writer.writeheader()

        for row in selected:
            writer.writerow({
                field: row.get(field, "")
                for field in fields
            })

    return out, len(selected)



# ---------------------------------------------------------------------
# Audit-file manifest
# ---------------------------------------------------------------------

def build_manifest() -> int:
    """
    Record all preserved files currently belonging to the audit layer.

    This gives each raw/parsed artifact a role and checksum without
    interpreting its scientific meaning.
    """

    rows = []

    for path in sorted(AUDIT_ROOT.rglob("*")):
        if not path.is_file():
            continue

        # Do not checksum the manifest while constructing itself.
        if path == MANIFEST:
            continue

        if RAW_DIR in path.parents:
            role = "raw_provenance"

        elif PARSED_DIR in path.parents:
            role = "derived_result"

        elif path.name.endswith("_strategy.md"):
            role = "audit_strategy"

        elif path.name.endswith("_interpretation.md"):
            role = "scientific_interpretation"

        else:
            role = "audit_document"

        rows.append({
            "path": str(path.relative_to(REPO_ROOT)),
            "role": role,
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
        })

    PARSED_DIR.mkdir(parents=True, exist_ok=True)

    with MANIFEST.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            lineterminator="\n",
            fieldnames=[
                "path",
                "role",
                "size_bytes",
                "sha256",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Validate and reproduce the O67940 post-2008 "
            "annotation-audit evidence layer."
        )
    )

    parser.add_argument(
        "--refresh",
        action="store_true",
        help=(
            "Explicitly permit live database refresh. "
            "Not implemented in the first validation stage."
        ),
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.refresh:
        fail(
            "--refresh is intentionally not enabled yet. "
            "First validate the frozen 2026 audit cache."
        )

    print("O67940 post-2008 audit driver")
    print("Mode: cached evidence validation")
    print()

    sequence = validate_query_sequence()

    print(
        "Canonical sequence:",
        sequence["sequence_length"],
        "aa; MD5",
        sequence["sequence_md5"],
    )

    uniprot = validate_current_uniprot()

    print(
        "Current UniProt:",
        uniprot["accession"],
        uniprot["entry_name"],
        uniprot["entry_type"],
    )

    uniparc = validate_uniparc()

    print(
        "UniParc:",
        uniparc["uniparc_id"],
        f"({uniparc['cross_reference_count']} cross-references)",
    )

    for result in validate_rcsb_results():
        print(
            result["audit_component"] + ":",
            result["total_count"],
            "hits",
        )

    unisave = validate_unisave_cache()

    print(
        "UniSave cache:",
        unisave["cached_versions"],
        "versions",
    )

    print()
    print("Regenerating factual derived results from cache...")

    uniprot_xrefs, n_uniprot_xrefs = (
        regenerate_uniprot_crossreferences()
    )

    europepmc_summary, n_europepmc = (
        regenerate_europepmc_query_summary()
    )

    uniparc_xrefs, n_uniparc_xrefs = (
        regenerate_uniparc_crossreferences()
    )

    rcsb_summary, n_rcsb = regenerate_rcsb_summary()

    timeline, n_timeline = (
        regenerate_unisave_version_timeline()
    )

    alias_literature, n_alias_literature = (
        regenerate_sequence_identical_alias_literature_summary()
    )

    refseq_summary, n_refseq = (
        regenerate_refseq_summary()
    )

    regenerate_unisave_results()

    milestones, n_milestones = (
        regenerate_annotation_milestones()
    )

    print(
        "UniProt cross-references:",
        n_uniprot_xrefs,
    )

    print(
        "Europe PMC cached queries:",
        n_europepmc,
    )

    print(
        "UniParc cross-references:",
        n_uniparc_xrefs,
    )

    print(
        "RCSB search summaries:",
        n_rcsb,
    )

    print(
        "UniSave timeline records:",
        n_timeline,
    )

    print(
        "Sequence-identical alias literature queries:",
        n_alias_literature,
    )

    print(
        "RefSeq records summarized:",
        n_refseq,
    )

    print(
        "Annotation milestones:",
        n_milestones,
    )

    manifest_count = build_manifest()

    print()
    print("Validated cached audit evidence.")
    print("Manifest records:", manifest_count)
    print(
        "Manifest:",
        MANIFEST.relative_to(REPO_ROOT),
    )


if __name__ == "__main__":
    main()
