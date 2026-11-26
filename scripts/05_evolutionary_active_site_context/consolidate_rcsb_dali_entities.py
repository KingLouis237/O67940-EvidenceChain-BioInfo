#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


EXPECTED_REGISTRY_SHA256 = (
    "127ede4775e0387c33833c799a7e798e361a55264e9eed4016fbb773a96ae35f"
)

EXPECTED_RESPONSE_SHA256 = (
    "94501c04ab30ccb29a964bd230c2ee557cfa8813ad1af006705203d7bebd5dd7"
)

EXPECTED_PDB_ENTRIES = 33


def sha256_file(path: Path) -> str:

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:

    with path.open(
        encoding="utf-8",
        newline="",
    ) as handle:

        return list(
            csv.DictReader(
                handle,
                delimiter="\t",
            )
        )


def join_values(
    values,
    separator: str = "|",
) -> str:

    cleaned = sorted({
        str(value)
        for value in values
        if value is not None
        and str(value) != ""
    })

    return (
        separator.join(cleaned)
        if cleaned
        else "NA"
    )


def int_or_large(value: str) -> int:

    if value in (
        "",
        "NA",
        None,
    ):
        return 10**9

    return int(value)


def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "Consolidate frozen RCSB metadata "
            "for the O67940 high-Z DALI "
            "structural neighborhood."
        )
    )

    parser.add_argument(
        "--pdb-registry",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--rcsb-response",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
    )

    args = parser.parse_args()


    # --------------------------------------------------
    # Frozen-input integrity
    # --------------------------------------------------

    registry_sha = sha256_file(
        args.pdb_registry
    )

    response_sha = sha256_file(
        args.rcsb_response
    )


    if (
        registry_sha
        != EXPECTED_REGISTRY_SHA256
    ):
        raise SystemExit(
            "STOP: frozen PDB-registry "
            "checksum mismatch."
        )

    if (
        response_sha
        != EXPECTED_RESPONSE_SHA256
    ):
        raise SystemExit(
            "STOP: frozen RCSB-response "
            "checksum mismatch."
        )


    # --------------------------------------------------
    # Read annotation-neutral DALI registry
    # --------------------------------------------------

    registry_rows = read_tsv(
        args.pdb_registry
    )

    registry = {}

    for row in registry_rows:

        pdb_id = (
            row["pdb_id"]
            .upper()
        )

        if pdb_id in registry:
            raise SystemExit(
                "STOP: duplicate PDB ID "
                f"in registry: {pdb_id}"
            )

        registry[pdb_id] = row


    if len(registry) != EXPECTED_PDB_ENTRIES:

        raise SystemExit(
            "STOP: expected "
            f"{EXPECTED_PDB_ENTRIES} "
            "PDB registry entries, got "
            f"{len(registry)}."
        )


    # --------------------------------------------------
    # Read frozen raw RCSB response
    # --------------------------------------------------

    response = json.loads(
        args.rcsb_response.read_text(
            encoding="utf-8"
        )
    )


    if response.get("errors"):

        raise SystemExit(
            "STOP: frozen RCSB response "
            "contains GraphQL errors."
        )


    entries = (
        response.get(
            "data",
            {}
        ).get(
            "entries"
        )
    )


    if not isinstance(
        entries,
        list,
    ):
        raise SystemExit(
            "STOP: response entries "
            "object is not a list."
        )


    if len(entries) != EXPECTED_PDB_ENTRIES:

        raise SystemExit(
            "STOP: expected "
            f"{EXPECTED_PDB_ENTRIES} "
            "RCSB entries, got "
            f"{len(entries)}."
        )


    # --------------------------------------------------
    # Flatten one polymer entity per PDB entry
    # --------------------------------------------------

    entity_rows = []

    length_checks = 0
    single_entity_checks = 0
    single_uniprot_checks = 0


    for entry in entries:

        if entry is None:

            raise SystemExit(
                "STOP: null RCSB entry "
                "encountered."
            )


        pdb_id = (
            entry["rcsb_id"]
            .upper()
        )


        entities = (
            entry.get(
                "polymer_entities"
            )
            or []
        )


        if len(entities) != 1:

            raise SystemExit(
                f"STOP: {pdb_id} has "
                f"{len(entities)} polymer "
                "entities; frozen acquisition "
                "observed exactly one."
            )

        single_entity_checks += 1


        entity = entities[0]

        entity_poly = (
            entity.get(
                "entity_poly"
            )
            or {}
        )

        identifiers = (
            entity.get(
                "rcsb_polymer_entity_"
                "container_identifiers"
            )
            or {}
        )


        refs = (
            identifiers.get(
                "reference_sequence_identifiers"
            )
            or []
        )


        uniprot_refs = sorted({
            ref.get(
                "database_accession"
            )
            for ref in refs
            if (
                ref.get(
                    "database_name"
                )
                == "UniProt"
            )
            and ref.get(
                "database_accession"
            )
        })


        if len(uniprot_refs) != 1:

            raise SystemExit(
                f"STOP: {pdb_id} has "
                f"{len(uniprot_refs)} "
                "UniProt reference accessions; "
                "frozen acquisition observed "
                "exactly one."
            )

        single_uniprot_checks += 1

        uniprot = uniprot_refs[0]


        # The hash below represents RCSB's canonical
        # one-letter sequence representation
        # (pdbx_seq_one_letter_code_can). It is used
        # for deterministic sequence grouping, but it
        # must not be interpreted as proof of identical
        # chemical, modification, mutation, ligand, or
        # experimental state. RCSB mutation metadata is
        # therefore retained independently.
        raw_sequence = (
            entity_poly.get(
                "pdbx_seq_one_letter_code_can"
            )
            or ""
        )

        sequence = "".join(
            raw_sequence.split()
        ).upper()


        if not sequence:

            raise SystemExit(
                "STOP: missing deposited "
                f"canonical sequence for {pdb_id}."
            )


        try:

            sequence_bytes = (
                sequence.encode(
                    "ascii"
                )
            )

        except UnicodeEncodeError:

            raise SystemExit(
                "STOP: non-ASCII character "
                f"in canonical sequence for {pdb_id}."
            )


        sequence_sha256 = (
            hashlib.sha256(
                sequence_bytes
            ).hexdigest()
        )


        reported_length = (
            entity_poly.get(
                "rcsb_sample_sequence_length"
            )
        )


        if reported_length is None:

            raise SystemExit(
                "STOP: missing reported "
                f"sequence length for {pdb_id}."
            )


        if (
            int(reported_length)
            != len(sequence)
        ):

            raise SystemExit(
                f"STOP: sequence-length mismatch "
                f"for {pdb_id}: "
                f"RCSB={reported_length}; "
                f"computed={len(sequence)}."
            )

        length_checks += 1


        description = (
            (
                entity.get(
                    "rcsb_polymer_entity"
                )
                or {}
            ).get(
                "pdbx_description"
            )
            or "NA"
        )


        organisms = (
            entity.get(
                "rcsb_entity_source_organism"
            )
            or []
        )

        organism_names = [
            organism.get(
                "ncbi_scientific_name"
            )
            for organism in organisms
            if organism.get(
                "ncbi_scientific_name"
            )
        ]

        taxonomy_ids = [
            organism.get(
                "ncbi_taxonomy_id"
            )
            for organism in organisms
            if organism.get(
                "ncbi_taxonomy_id"
            )
            is not None
        ]


        mutation_count = (
            entity_poly.get(
                "rcsb_mutation_count"
            )
        )


        if mutation_count is None:

            raise SystemExit(
                "STOP: missing RCSB "
                f"mutation count for {pdb_id}."
            )


        experimental_methods = [
            item.get("method")
            for item in (
                entry.get("exptl")
                or []
            )
            if item.get("method")
        ]


        entry_info = (
            entry.get(
                "rcsb_entry_info"
            )
            or {}
        )

        resolutions = (
            entry_info.get(
                "resolution_combined"
            )
            or []
        )


        accession_info = (
            entry.get(
                "rcsb_accession_info"
            )
            or {}
        )


        title = (
            (
                entry.get(
                    "struct"
                )
                or {}
            ).get(
                "title"
            )
            or "NA"
        )


        if pdb_id not in registry:

            raise SystemExit(
                "STOP: RCSB PDB ID absent "
                f"from DALI registry: {pdb_id}"
            )


        dali = registry[
            pdb_id
        ]


        entity_rows.append({
            "pdb_id": pdb_id,

            "rcsb_polymer_entity_id": (
                entity.get(
                    "rcsb_id"
                )
                or "NA"
            ),

            "entity_id": (
                identifiers.get(
                    "entity_id"
                )
                or "NA"
            ),

            "uniprot_accession": (
                uniprot
            ),

            "pdbx_description": (
                description
            ),

            "polymer_type": (
                entity_poly.get(
                    "rcsb_entity_polymer_type"
                )
                or "NA"
            ),

            "canonical_sequence_length": (
                str(
                    len(sequence)
                )
            ),

            "canonical_sequence_sha256": (
                sequence_sha256
            ),

            "rcsb_mutation_count": (
                str(
                    mutation_count
                )
            ),

            "auth_chains": join_values(
                identifiers.get(
                    "auth_asym_ids"
                )
                or [],
                ",",
            ),

            "label_chains": join_values(
                identifiers.get(
                    "asym_ids"
                )
                or [],
                ",",
            ),

            "source_organisms": (
                join_values(
                    organism_names
                )
            ),

            "ncbi_taxonomy_ids": (
                join_values(
                    taxonomy_ids
                )
            ),

            "experimental_methods": (
                join_values(
                    experimental_methods
                )
            ),

            "resolution_combined": (
                join_values(
                    resolutions,
                    ",",
                )
            ),

            "deposit_date": (
                accession_info.get(
                    "deposit_date"
                )
                or "NA"
            ),

            "initial_release_date": (
                accession_info.get(
                    "initial_release_date"
                )
                or "NA"
            ),

            "structure_title": (
                title
            ),

            "full_chain_hit_count": (
                dali[
                    "full_chain_hit_count"
                ]
            ),

            "full_best_rank": (
                dali[
                    "full_best_rank"
                ]
            ),

            "full_z_max": (
                dali[
                    "full_z_max"
                ]
            ),

            "full_z_min": (
                dali[
                    "full_z_min"
                ]
            ),

            "pdb25_present": (
                dali[
                    "pdb25_present"
                ]
            ),

            "pdb25_chain_hit_count": (
                dali[
                    "pdb25_chain_hit_count"
                ]
            ),

            "pdb25_best_rank": (
                dali[
                    "pdb25_best_rank"
                ]
            ),

            "pdb25_z_max": (
                dali[
                    "pdb25_z_max"
                ]
            ),
        })


    entity_ids = {
        row["pdb_id"]
        for row in entity_rows
    }

    registry_ids = set(
        registry
    )


    if entity_ids != registry_ids:

        raise SystemExit(
            "STOP: PDB-ID mismatch "
            "between RCSB entity table "
            "and DALI registry."
        )


    # --------------------------------------------------
    # Group RCSB canonical-sequence states
    # --------------------------------------------------

    by_sequence = defaultdict(
        list
    )


    for row in entity_rows:

        by_sequence[
            row[
                "canonical_sequence_sha256"
            ]
        ].append(row)


    sequence_groups = []


    for sequence_hash, rows in (
        by_sequence.items()
    ):

        accessions = {
            row[
                "uniprot_accession"
            ]
            for row in rows
        }


        if len(accessions) != 1:

            raise SystemExit(
                "STOP: identical RCSB canonical "
                "sequence maps to multiple "
                "UniProt accessions: "
                f"{sequence_hash}"
            )


        best_row = min(
            rows,
            key=lambda row: int(
                row[
                    "full_best_rank"
                ]
            ),
        )


        sequence_groups.append({
            "sequence_sha256": (
                sequence_hash
            ),

            "uniprot_accession": (
                next(
                    iter(
                        accessions
                    )
                )
            ),

            "canonical_sequence_length": (
                best_row[
                    "canonical_sequence_length"
                ]
            ),

            "pdb_entry_count": (
                str(
                    len(rows)
                )
            ),

            "pdb_ids": (
                ",".join(
                    sorted(
                        (
                            row[
                                "pdb_id"
                            ]
                            for row in rows
                        ),
                        key=lambda pdb_id: int(
                            registry[
                                pdb_id
                            ][
                                "full_best_rank"
                            ]
                        ),
                    )
                )
            ),

            "rcsb_mutation_counts": (
                join_values(
                    (
                        row[
                            "rcsb_mutation_count"
                        ]
                        for row in rows
                    ),
                    ",",
                )
            ),

            "best_full_rank": (
                best_row[
                    "full_best_rank"
                ]
            ),

            "best_full_z": (
                best_row[
                    "full_z_max"
                ]
            ),

            "pdb25_entries": (
                ",".join(
                    sorted(
                        (
                            row[
                                "pdb_id"
                            ]
                            for row in rows
                            if (
                                row[
                                    "pdb25_present"
                                ]
                                == "yes"
                            )
                        ),
                        key=lambda pdb_id: int(
                            registry[
                                pdb_id
                            ][
                                "pdb25_best_rank"
                            ]
                        ),
                    )
                )
                or "none"
            ),
        })


    sequence_groups.sort(
        key=lambda row: (
            int(
                row[
                    "best_full_rank"
                ]
            ),
            row[
                "uniprot_accession"
            ],
            row[
                "sequence_sha256"
            ],
        )
    )


    for index, row in enumerate(
        sequence_groups,
        start=1,
    ):

        row[
            "sequence_state_id"
        ] = (
            f"SEQSTATE_{index:02d}"
        )


    hash_to_state = {
        row[
            "sequence_sha256"
        ]: row[
            "sequence_state_id"
        ]
        for row in sequence_groups
    }


    for row in entity_rows:

        row[
            "sequence_state_id"
        ] = hash_to_state[
            row[
                "canonical_sequence_sha256"
            ]
        ]


    # --------------------------------------------------
    # Group by UniProt reference accession
    # --------------------------------------------------

    by_uniprot = defaultdict(
        list
    )


    for row in entity_rows:

        by_uniprot[
            row[
                "uniprot_accession"
            ]
        ].append(row)


    uniprot_rows = []


    for accession, rows in (
        by_uniprot.items()
    ):

        best_row = min(
            rows,
            key=lambda row: int(
                row[
                    "full_best_rank"
                ]
            ),
        )


        states = sorted(
            {
                row[
                    "sequence_state_id"
                ]
                for row in rows
            },
            key=lambda state: int(
                state.split(
                    "_"
                )[1]
            ),
        )


        pdb_ids = sorted(
            (
                row[
                    "pdb_id"
                ]
                for row in rows
            ),
            key=lambda pdb_id: int(
                registry[
                    pdb_id
                ][
                    "full_best_rank"
                ]
            ),
        )


        pdb25_entries = sorted(
            (
                row[
                    "pdb_id"
                ]
                for row in rows
                if (
                    row[
                        "pdb25_present"
                    ]
                    == "yes"
                )
            ),
            key=lambda pdb_id: int(
                registry[
                    pdb_id
                ][
                    "pdb25_best_rank"
                ]
            ),
        )


        uniprot_rows.append({
            "uniprot_accession": (
                accession
            ),

            "pdb_entry_count": (
                str(
                    len(rows)
                )
            ),

            "pdb_ids": (
                ",".join(
                    pdb_ids
                )
            ),

            "sequence_state_count": (
                str(
                    len(states)
                )
            ),

            "sequence_state_ids": (
                ",".join(
                    states
                )
            ),

            "sequence_lengths": (
                join_values(
                    (
                        row[
                            "canonical_sequence_length"
                        ]
                        for row in rows
                    ),
                    ",",
                )
            ),

            "rcsb_mutation_counts": (
                join_values(
                    (
                        row[
                            "rcsb_mutation_count"
                        ]
                        for row in rows
                    ),
                    ",",
                )
            ),

            "source_organisms": (
                join_values(
                    (
                        row[
                            "source_organisms"
                        ]
                        for row in rows
                    )
                )
            ),

            "best_full_rank": (
                best_row[
                    "full_best_rank"
                ]
            ),

            "best_full_z": (
                best_row[
                    "full_z_max"
                ]
            ),

            "pdb25_entries": (
                ",".join(
                    pdb25_entries
                )
                or "none"
            ),
        })


    uniprot_rows.sort(
        key=lambda row: (
            int(
                row[
                    "best_full_rank"
                ]
            ),
            row[
                "uniprot_accession"
            ],
        )
    )


    entity_rows.sort(
        key=lambda row: (
            int(
                row[
                    "full_best_rank"
                ]
            ),
            row[
                "pdb_id"
            ],
        )
    )


    # --------------------------------------------------
    # Output paths / overwrite protection
    # --------------------------------------------------

    entity_path = (
        args.output_dir
        / "O67940_rcsb_polymer_entity_registry.tsv"
    )

    sequence_path = (
        args.output_dir
        / "O67940_rcsb_sequence_state_registry.tsv"
    )

    uniprot_path = (
        args.output_dir
        / "O67940_rcsb_uniprot_consolidation.tsv"
    )

    validation_path = (
        args.output_dir
        / "O67940_rcsb_entity_consolidation_validation.tsv"
    )


    output_paths = [
        entity_path,
        sequence_path,
        uniprot_path,
        validation_path,
    ]


    existing_outputs = [
        path
        for path in output_paths
        if path.exists()
    ]


    if existing_outputs:

        raise SystemExit(
            "STOP: refusing to overwrite "
            "existing entity-consolidation "
            "output(s):\n"
            + "\n".join(
                str(path)
                for path in existing_outputs
            )
        )


    args.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


    # --------------------------------------------------
    # Write entity registry
    # --------------------------------------------------

    entity_fields = [
        "pdb_id",
        "rcsb_polymer_entity_id",
        "entity_id",
        "uniprot_accession",
        "pdbx_description",
        "polymer_type",
        "sequence_state_id",
        "canonical_sequence_length",
        "canonical_sequence_sha256",
        "rcsb_mutation_count",
        "auth_chains",
        "label_chains",
        "source_organisms",
        "ncbi_taxonomy_ids",
        "experimental_methods",
        "resolution_combined",
        "deposit_date",
        "initial_release_date",
        "structure_title",
        "full_chain_hit_count",
        "full_best_rank",
        "full_z_max",
        "full_z_min",
        "pdb25_present",
        "pdb25_chain_hit_count",
        "pdb25_best_rank",
        "pdb25_z_max",
    ]


    with entity_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=entity_fields,
            delimiter="\t",
            lineterminator="\n",
        )

        writer.writeheader()

        writer.writerows(
            entity_rows
        )


    # --------------------------------------------------
    # Write sequence-state registry
    # --------------------------------------------------

    sequence_fields = [
        "sequence_state_id",
        "uniprot_accession",
        "sequence_sha256",
        "canonical_sequence_length",
        "pdb_entry_count",
        "pdb_ids",
        "rcsb_mutation_counts",
        "best_full_rank",
        "best_full_z",
        "pdb25_entries",
    ]


    with sequence_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=sequence_fields,
            delimiter="\t",
            lineterminator="\n",
        )

        writer.writeheader()

        writer.writerows(
            sequence_groups
        )


    # --------------------------------------------------
    # Write UniProt consolidation
    # --------------------------------------------------

    uniprot_fields = [
        "uniprot_accession",
        "pdb_entry_count",
        "pdb_ids",
        "sequence_state_count",
        "sequence_state_ids",
        "sequence_lengths",
        "rcsb_mutation_counts",
        "source_organisms",
        "best_full_rank",
        "best_full_z",
        "pdb25_entries",
    ]


    with uniprot_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=uniprot_fields,
            delimiter="\t",
            lineterminator="\n",
        )

        writer.writeheader()

        writer.writerows(
            uniprot_rows
        )


    # --------------------------------------------------
    # Validation / observations
    # --------------------------------------------------

    mutation_distribution = Counter(
        row[
            "rcsb_mutation_count"
        ]
        for row in entity_rows
    )


    mutation_summary = ";".join(
        f"{count_value}:{entry_count}"
        for count_value, entry_count
        in sorted(
            mutation_distribution.items(),
            key=lambda item: int(
                item[0]
            ),
        )
    )


    pdb25_uniprot = {
        row[
            "uniprot_accession"
        ]
        for row in entity_rows
        if (
            row[
                "pdb25_present"
            ]
            == "yes"
        )
    }


    cross_uniprot_sequence_hashes = 0

    for rows in by_sequence.values():

        accessions = {
            row[
                "uniprot_accession"
            ]
            for row in rows
        }

        if len(accessions) > 1:

            cross_uniprot_sequence_hashes += 1


    sequence_state_pdb_accounting = sum(
        int(
            row["pdb_entry_count"]
        )
        for row in sequence_groups
    )

    uniprot_pdb_accounting = sum(
        int(
            row["pdb_entry_count"]
        )
        for row in uniprot_rows
    )

    unique_sequence_state_ids = len({
        row["sequence_state_id"]
        for row in sequence_groups
    })

    entity_state_assignments = sum(
        1
        for row in entity_rows
        if row.get(
            "sequence_state_id"
        )
    )


    if (
        sequence_state_pdb_accounting
        != EXPECTED_PDB_ENTRIES
    ):
        raise SystemExit(
            "STOP: canonical-sequence-state "
            "groups do not account for all "
            "PDB entries."
        )

    if (
        uniprot_pdb_accounting
        != EXPECTED_PDB_ENTRIES
    ):
        raise SystemExit(
            "STOP: UniProt groups do not "
            "account for all PDB entries."
        )

    if (
        unique_sequence_state_ids
        != len(sequence_groups)
    ):
        raise SystemExit(
            "STOP: duplicate sequence-state "
            "identifier detected."
        )

    if (
        entity_state_assignments
        != EXPECTED_PDB_ENTRIES
    ):
        raise SystemExit(
            "STOP: one or more entities lack "
            "a canonical sequence-state ID."
        )


    validation_rows = [
        [
            "pdb_registry_sha256",
            "PASS",
            registry_sha,
            EXPECTED_REGISTRY_SHA256,
        ],
        [
            "rcsb_response_sha256",
            "PASS",
            response_sha,
            EXPECTED_RESPONSE_SHA256,
        ],
        [
            "pdb_registry_entries",
            "PASS",
            str(
                len(registry)
            ),
            str(
                EXPECTED_PDB_ENTRIES
            ),
        ],
        [
            "rcsb_entries",
            "PASS",
            str(
                len(entries)
            ),
            str(
                EXPECTED_PDB_ENTRIES
            ),
        ],
        [
            "one_polymer_entity_per_pdb",
            "PASS",
            (
                f"{single_entity_checks}/"
                f"{EXPECTED_PDB_ENTRIES}"
            ),
            (
                f"{EXPECTED_PDB_ENTRIES}/"
                f"{EXPECTED_PDB_ENTRIES}"
            ),
        ],
        [
            "one_uniprot_reference_per_entity",
            "PASS",
            (
                f"{single_uniprot_checks}/"
                f"{EXPECTED_PDB_ENTRIES}"
            ),
            (
                f"{EXPECTED_PDB_ENTRIES}/"
                f"{EXPECTED_PDB_ENTRIES}"
            ),
        ],
        [
            "sequence_length_checks",
            "PASS",
            (
                f"{length_checks}/"
                f"{EXPECTED_PDB_ENTRIES}"
            ),
            (
                f"{EXPECTED_PDB_ENTRIES}/"
                f"{EXPECTED_PDB_ENTRIES}"
            ),
        ],
        [
            "registry_response_pdb_sets_match",
            "PASS",
            str(
                entity_ids
                == registry_ids
            ),
            "True",
        ],
        [
            "entity_output_rows",
            "PASS",
            str(
                len(entity_rows)
            ),
            str(
                EXPECTED_PDB_ENTRIES
            ),
        ],
        [
            "canonical_sequence_state_pdb_accounting",
            "PASS",
            str(
                sequence_state_pdb_accounting
            ),
            str(
                EXPECTED_PDB_ENTRIES
            ),
        ],
        [
            "uniprot_group_pdb_accounting",
            "PASS",
            str(
                uniprot_pdb_accounting
            ),
            str(
                EXPECTED_PDB_ENTRIES
            ),
        ],
        [
            "sequence_state_ids_unique",
            "PASS",
            str(
                unique_sequence_state_ids
            ),
            str(
                len(sequence_groups)
            ),
        ],
        [
            "entity_sequence_state_assignments",
            "PASS",
            str(
                entity_state_assignments
            ),
            str(
                EXPECTED_PDB_ENTRIES
            ),
        ],
        [
            "unique_uniprot_accessions",
            "OBSERVED",
            str(
                len(by_uniprot)
            ),
            "not_prespecified",
        ],
        [
            "unique_canonical_sequence_states",
            "OBSERVED",
            str(
                len(sequence_groups)
            ),
            "not_prespecified",
        ],
        [
            "sequence_hashes_crossing_uniprot_accessions",
            "OBSERVED",
            str(
                cross_uniprot_sequence_hashes
            ),
            "not_prespecified",
        ],
        [
            "pdb25_unique_uniprot_accessions",
            "OBSERVED",
            str(
                len(pdb25_uniprot)
            ),
            "not_prespecified",
        ],
        [
            "rcsb_mutation_count_distribution",
            "OBSERVED",
            mutation_summary,
            "not_prespecified",
        ],
    ]


    with validation_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.writer(
            handle,
            delimiter="\t",
            lineterminator="\n",
        )

        writer.writerow([
            "check",
            "status",
            "observed",
            "expected",
        ])

        writer.writerows(
            validation_rows
        )


    # --------------------------------------------------
    # Console summary
    # --------------------------------------------------

    print(
        "PASS: RCSB entity consolidation "
        "completed."
    )

    print(
        f"pdb_entries={len(entity_rows)}"
    )

    print(
        "unique_uniprot_accessions="
        f"{len(by_uniprot)}"
    )

    print(
        "unique_canonical_sequence_states="
        f"{len(sequence_groups)}"
    )

    print(
        "sequence_hashes_crossing_"
        "uniprot_accessions="
        f"{cross_uniprot_sequence_hashes}"
    )

    print(
        "pdb25_unique_uniprot_accessions="
        f"{len(pdb25_uniprot)}"
    )

    print(
        "mutation_count_distribution="
        f"{mutation_summary}"
    )

    for path in output_paths:

        print(
            f"wrote={path}"
        )


if __name__ == "__main__":
    main()
