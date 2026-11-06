
#!/usr/bin/env python3

import csv
from pathlib import Path


# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

REGISTRY = Path(
    "results/functional_anchor_audit/parsed/"
    "functional_anchor_candidate_registry.tsv"
)

EVIDENCE = Path(
    "results/functional_anchor_audit/parsed/"
    "functional_anchor_evidence.tsv"
)

EVIDENCE_FILES = Path(
    "results/functional_anchor_audit/parsed/"
    "functional_anchor_evidence_files.tsv"
)


# ------------------------------------------------------------
# Expected evidence-table schema
# ------------------------------------------------------------

EXPECTED_FIELDS = [
    "evidence_id",
    "candidate_accession",
    "claim_category",
    "claim",
    "evidence_type",
    "evidence_direction",
    "tested_entity",
    "exact_candidate_tested",
    "construct_state",
    "experiment",
    "result",
    "source_type",
    "source_id",
    "source_locator",
    "raw_evidence_file",
    "year",
    "audit_notes",
]


# ------------------------------------------------------------
# Controlled vocabularies
#
# Keeping these explicit makes scientific categories machine-checkable.
# ------------------------------------------------------------

VALID_CLAIM_CATEGORIES = {
    "biochemical_activity",
    "substrate_specificity",
    "stereoselectivity",
    "catalytic_mechanism",
    "catalytic_residue",
    "experimental_structure",
    "oligomeric_state",
    "in_vivo_role",
    "database_annotation",
}

VALID_EVIDENCE_TYPES = {
    "direct_biochemical_assay",
    "mutagenesis",
    "experimental_structure",
    "genetic_experiment",
    "isotope_labelling",
    "database_annotation",
    "homology_inference",
}

VALID_EVIDENCE_DIRECTIONS = {
    "supports",
    "contradicts",
    "qualifies",
    "neutral",
}

VALID_EXACT_MATCH = {
    "yes",
    "no",
    "unclear",
    "not_applicable",
}

VALID_CONSTRUCT_STATES = {
    "wild_type",
    "mutant",
    "truncated",
    "engineered",
    "not_applicable",
    "unclear",
}

VALID_SOURCE_TYPES = {
    "primary_paper",
    "pdb",
    "uniprot",
    "other_database",
}


# ------------------------------------------------------------
# Evidence-to-file provenance table
# ------------------------------------------------------------

EXPECTED_EVIDENCE_FILE_FIELDS = [
    "evidence_id",
    "file_role",
    "raw_evidence_file",
    "description",
]

VALID_FILE_ROLES = {
    "primary_evidence",
    "identity_bridge",
    "construct_definition",
    "ligand_definition",
}


# ------------------------------------------------------------
# Fields required for every evidence record
# ------------------------------------------------------------

REQUIRED_FIELDS = {
    "evidence_id",
    "candidate_accession",
    "claim_category",
    "claim",
    "evidence_type",
    "evidence_direction",
    "tested_entity",
    "exact_candidate_tested",
    "construct_state",
    "source_type",
    "source_id",
}


def read_tsv(path):
    """Read a TSV file and return both field names and rows."""

    with path.open() as handle:
        reader = csv.DictReader(handle, delimiter="\t")

        # Capture the header while the file handle is still open.
        # For an empty file, DictReader has no field names.
        fieldnames = reader.fieldnames

        if fieldnames is None:
            fail(f"TSV file is empty or has no header: {path}")

        rows = list(reader)

    return fieldnames, rows


def fail(message):
    """Stop immediately with a clear validation error."""

    raise SystemExit(f"VALIDATION ERROR: {message}")


def main():

    # --------------------------------------------------------
    # 1. Confirm required files exist
    # --------------------------------------------------------

    if not REGISTRY.exists():
        fail(f"Missing candidate registry: {REGISTRY}")

    if not EVIDENCE.exists():
        fail(f"Missing evidence table: {EVIDENCE}")

    if not EVIDENCE_FILES.exists():
        fail(
            "Missing evidence-file provenance table: "
            f"{EVIDENCE_FILES}"
        )


    # --------------------------------------------------------
    # 2. Load candidate registry
    # --------------------------------------------------------

    _, registry_rows = read_tsv(REGISTRY)

    valid_accessions = {
        row["accession"].strip()
        for row in registry_rows
        if row["accession"].strip()
    }


    # --------------------------------------------------------
    # 3. Load evidence table and validate schema
    # --------------------------------------------------------

    fields, evidence_rows = read_tsv(EVIDENCE)

    if fields != EXPECTED_FIELDS:
        fail(
            "Evidence-table columns do not match the expected schema.\n"
            f"Expected: {EXPECTED_FIELDS}\n"
            f"Observed: {fields}"
        )


    # --------------------------------------------------------
    # 4. Validate each evidence record
    # --------------------------------------------------------

    seen_ids = set()

    for line_number, row in enumerate(evidence_rows, start=2):

        evidence_id = row["evidence_id"].strip()

        # Required fields must not be blank.
        for field in REQUIRED_FIELDS:
            if not row[field].strip():
                fail(
                    f"Line {line_number}: required field "
                    f"'{field}' is empty."
                )

        # Evidence IDs behave like primary keys.
        if evidence_id in seen_ids:
            fail(
                f"Line {line_number}: duplicate evidence_id "
                f"'{evidence_id}'."
            )

        seen_ids.add(evidence_id)

        # Candidate must belong to the frozen audit registry.
        accession = row["candidate_accession"].strip()

        if accession not in valid_accessions:
            fail(
                f"Line {line_number}: candidate accession "
                f"'{accession}' is not present in the registry."
            )

        # Controlled vocabularies.
        controlled_checks = [
            (
                "claim_category",
                VALID_CLAIM_CATEGORIES,
            ),
            (
                "evidence_type",
                VALID_EVIDENCE_TYPES,
            ),
            (
                "evidence_direction",
                VALID_EVIDENCE_DIRECTIONS,
            ),
            (
                "exact_candidate_tested",
                VALID_EXACT_MATCH,
            ),
            (
                "construct_state",
                VALID_CONSTRUCT_STATES,
            ),
            (
                "source_type",
                VALID_SOURCE_TYPES,
            ),
        ]

        for field, allowed in controlled_checks:
            value = row[field].strip()

            if value not in allowed:
                fail(
                    f"Line {line_number}: invalid value "
                    f"'{value}' for '{field}'. "
                    f"Allowed: {sorted(allowed)}"
                )

        # Year is optional, but if supplied it must be sensible.
        year = row["year"].strip()

        if year:
            if not year.isdigit() or len(year) != 4:
                fail(
                    f"Line {line_number}: invalid year '{year}'."
                )

            year_int = int(year)

            if not 1900 <= year_int <= 2100:
                fail(
                    f"Line {line_number}: year '{year}' "
                    "is outside the accepted range."
                )

        # If a local raw source path is recorded, it must exist.
        raw_file = row["raw_evidence_file"].strip()

        if raw_file:
            raw_path = Path(raw_file)

            if not raw_path.exists():
                fail(
                    f"Line {line_number}: raw evidence file "
                    f"does not exist: {raw_file}"
                )


    # --------------------------------------------------------
    # 5. Validate evidence-to-file provenance links
    # --------------------------------------------------------

    file_fields, evidence_file_rows = read_tsv(EVIDENCE_FILES)

    if file_fields != EXPECTED_EVIDENCE_FILE_FIELDS:
        fail(
            "Evidence-file table columns do not match the "
            "expected schema.\n"
            f"Expected: {EXPECTED_EVIDENCE_FILE_FIELDS}\n"
            f"Observed: {file_fields}"
        )

    seen_file_links = set()
    primary_evidence_ids = set()

    for line_number, row in enumerate(
        evidence_file_rows,
        start=2,
    ):
        evidence_id = row["evidence_id"].strip()
        file_role = row["file_role"].strip()
        raw_file = row["raw_evidence_file"].strip()

        # Every provenance row must point to an existing
        # evidence record: evidence_id acts as a foreign key.
        if evidence_id not in seen_ids:
            fail(
                f"Evidence-file line {line_number}: "
                f"unknown evidence_id '{evidence_id}'."
            )

        if file_role not in VALID_FILE_ROLES:
            fail(
                f"Evidence-file line {line_number}: invalid "
                f"file_role '{file_role}'. "
                f"Allowed: {sorted(VALID_FILE_ROLES)}"
            )

        if not raw_file:
            fail(
                f"Evidence-file line {line_number}: "
                "raw_evidence_file is empty."
            )

        raw_path = Path(raw_file)

        if not raw_path.exists():
            fail(
                f"Evidence-file line {line_number}: "
                f"raw evidence file does not exist: {raw_file}"
            )

        # The same evidence/file/role relationship should not
        # appear twice.
        link_key = (
            evidence_id,
            file_role,
            raw_file,
        )

        if link_key in seen_file_links:
            fail(
                f"Evidence-file line {line_number}: duplicate "
                "evidence/file/role relationship."
            )

        seen_file_links.add(link_key)

        if file_role == "primary_evidence":
            primary_evidence_ids.add(evidence_id)

    # Every evidence record must have at least one raw source
    # explicitly designated as its primary evidence.
    missing_primary = seen_ids - primary_evidence_ids

    if missing_primary:
        fail(
            "Evidence records without a primary_evidence file: "
            f"{sorted(missing_primary)}"
        )

    # --------------------------------------------------------
    # Success summary
    # --------------------------------------------------------

    print("Functional-anchor evidence validation passed.")
    print(f"Registry candidates: {len(valid_accessions)}")
    print(f"Evidence records: {len(evidence_rows)}")
    print(f"Unique evidence IDs: {len(seen_ids)}")
    print(f"Evidence-file links: {len(evidence_file_rows)}")


if __name__ == "__main__":
    main()
