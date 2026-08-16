#!/usr/bin/env python3
# === MODULE_BUILD ===
# id: edcm_tarot_relation_discovery
#   module_name: tarot_relation_discovery
#   module_kind: instrument
#   summary: validates a sealed Tarot acquisition and discovers only ordered source-envelope assertions and exact-value agreements without selecting Tarot ontology
#   owner: Erin Spencer
#   public_surface: discover_relations, validate_discovery, main
#   internal_surface: _canonical_bytes, _digest, _value_identity, _load_validated_acquisition
#   auth_boundary: none
#   storage_boundary: read sealed acquisition and write one caller-selected report
#   network_boundary: none
#   user_data_boundary: none; public cultural and archival evidence only
#   admin_only: false
#   tests: tests.test_tarot_relation_discovery
#   rollout: explicit CLI after a complete tarot corpus acquisition; no automatic UCNS or EDCM measurement activation
#   rollback: remove this tool, its tests, docs, and generated discovery reports without altering acquisition evidence
#   requires: edcm_tarot_corpus_acquirer
#   since: 2026-08-16
#   unresolved: OCR, image interpretation, cross-source card identity, semantic relation discovery, UCNS recursive representation, and EDCM measurement
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: tarot_discovery_consumes_only_complete_sealed_acquisition
#   given: Tarot relation discovery is requested
#   then: the exact acquisition receipt, manifest identities, evidence index digest, every listed artifact digest, and complete file set validate before discovery
#   class: safety
#   since: 2026-08-16
#
# id: tarot_discovery_preserves_exact_source_order_and_values
#   given: a validated evidence index is discovered
#   then: every source remains in manifest order and every admitted field value remains exact without case folding, tokenization, OCR, or semantic normalization
#   class: evidence
#   since: 2026-08-16
#
# id: tarot_discovery_relations_are_mechanical_and_bounded
#   given: source-envelope relations are emitted
#   then: relations are limited to ordered adjacency, exact field assertions, fetched-artifact binding, and same-field exact-value agreement within declared resource bounds
#   class: correctness
#   since: 2026-08-16
#
# id: tarot_discovery_preserves_typed_absence_and_nonclaims
#   given: a source field is absent or the report completes
#   then: absence remains explicit and the report selects no ontology, card identity, geometry, measurement, or canon
#   class: doctrine
#   since: 2026-08-16
#
# id: tarot_discovery_is_byte_deterministic
#   given: the same validated acquisition and frozen algorithm identity are processed twice
#   then: canonical report bytes are identical
#   class: evidence
#   since: 2026-08-16
# === END CONTRACTS ===

"""Discover exact source-envelope relations in a sealed Tarot acquisition.

Usage:
    python tools/discover_tarot_relations.py \
      --manifest corpus/tarot/sources.v1.json \
      --acquisition artifacts/tarot/acquisition-v1 \
      --output artifacts/tarot/relations-v1.json

This first discovery stage reads no PDF content. It preserves source order,
exact metadata values, explicit absence, and exact equality only. It performs
no OCR, case folding, card matching, semantic normalization, UCNS construction,
EDCM measurement, ontology selection, or canon selection.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from tools.acquire_tarot_corpus import TarotCorpusError, acquire_manifest

DISCOVERY_SCHEMA = "edcm.tarot-source-envelope-relations"
DISCOVERY_VERSION = "1.0.0"
INDEX_SCHEMA = "edcm.tarot-corpus-evidence-index"
INDEX_VERSION = "1.0.0"
DEFAULT_MAX_SOURCES = 10_000
DEFAULT_MAX_ASSERTIONS = 1_000_000

FIELD_ORDER = (
    "title",
    "authority",
    "source_date",
    "locator_url",
    "retrieval_policy",
    "rights_status",
    "rights_url",
    "declared_media_type",
    "curation_note",
    "provenance_note",
    "artifact_path",
    "sha256",
    "bytes",
    "content_type",
    "final_url",
)


class TarotRelationDiscoveryError(ValueError):
    """Raised when sealed evidence or deterministic discovery drifts."""


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8") + b"\n"


def _digest(payload: bytes) -> str:
    return sha256(payload).hexdigest()


def _value_identity(field: str, value: object) -> str:
    return _digest(_canonical_bytes({"field": field, "value": value}))


def _load_validated_acquisition(
    manifest_path: Path,
    acquisition: Path,
) -> tuple[dict[str, Any], dict[str, Any], str]:
    try:
        receipt = acquire_manifest(manifest_path, acquisition, resume=True)
    except (OSError, ValueError, TarotCorpusError) as exc:
        raise TarotRelationDiscoveryError("sealed Tarot acquisition validation failed") from exc
    index_path = acquisition / "evidence-index.json"
    index_bytes = index_path.read_bytes()
    try:
        index = json.loads(index_bytes)
    except json.JSONDecodeError as exc:
        raise TarotRelationDiscoveryError("Tarot evidence index is invalid JSON") from exc
    if _canonical_bytes(index) != index_bytes:
        raise TarotRelationDiscoveryError("Tarot evidence index is not canonical")
    if index.get("schema") != INDEX_SCHEMA or index.get("version") != INDEX_VERSION:
        raise TarotRelationDiscoveryError("Tarot evidence index schema/version mismatch")
    if index.get("ontology_selected") is not False:
        raise TarotRelationDiscoveryError("Tarot evidence index selected an ontology")
    if index.get("manifest_file_sha256") != receipt.get("manifest_file_sha256"):
        raise TarotRelationDiscoveryError("Tarot evidence index manifest identity mismatch")
    if index.get("manifest_canonical_sha256") != receipt.get("manifest_canonical_sha256"):
        raise TarotRelationDiscoveryError("Tarot evidence index canonical manifest mismatch")
    if _digest(index_bytes) != receipt.get("evidence_index_sha256"):
        raise TarotRelationDiscoveryError("Tarot evidence index digest mismatch")
    sources = index.get("sources")
    if not isinstance(sources, list) or len(sources) != receipt.get("source_count"):
        raise TarotRelationDiscoveryError("Tarot evidence source count mismatch")
    return receipt, index, _digest((acquisition / "run-receipt.json").read_bytes())


def discover_relations(
    manifest_path: str | Path,
    acquisition: str | Path,
    *,
    max_sources: int = DEFAULT_MAX_SOURCES,
    max_assertions: int = DEFAULT_MAX_ASSERTIONS,
) -> dict[str, Any]:
    """Return deterministic, pre-ontology relations from one sealed snapshot."""

    if type(max_sources) is not int or max_sources <= 0:
        raise TarotRelationDiscoveryError("max_sources must be a positive exact integer")
    if type(max_assertions) is not int or max_assertions <= 0:
        raise TarotRelationDiscoveryError("max_assertions must be a positive exact integer")
    receipt, index, receipt_sha = _load_validated_acquisition(
        Path(manifest_path), Path(acquisition)
    )
    rows = index["sources"]
    if len(rows) > max_sources:
        raise TarotRelationDiscoveryError("Tarot source resource bound exceeded")

    source_order: list[str] = []
    assertions: list[dict[str, Any]] = []
    absences: list[dict[str, Any]] = []
    exact_groups: dict[tuple[str, str], list[str]] = defaultdict(list)
    values_by_identity: dict[str, object] = {}

    for ordinal, row in enumerate(rows):
        if not isinstance(row, dict) or type(row.get("source_id")) is not str:
            raise TarotRelationDiscoveryError("Tarot evidence source row is malformed")
        source_id = row["source_id"]
        if source_id in source_order:
            raise TarotRelationDiscoveryError("Tarot evidence source identity is duplicated")
        source_order.append(source_id)
        for field in FIELD_ORDER:
            if field not in row:
                raise TarotRelationDiscoveryError(f"Tarot evidence field is missing: {field}")
            value = row[field]
            if value is None:
                absences.append({
                    "source_id": source_id,
                    "source_ordinal": ordinal,
                    "field": field,
                    "state": "NA",
                })
                continue
            identity = _value_identity(field, value)
            previous = values_by_identity.setdefault(identity, value)
            if type(previous) is not type(value) or previous != value:
                raise TarotRelationDiscoveryError("exact-value identity collision")
            assertions.append({
                "source_id": source_id,
                "source_ordinal": ordinal,
                "field": field,
                "value": value,
                "value_identity": identity,
            })
            exact_groups[(field, identity)].append(source_id)
            if len(assertions) > max_assertions:
                raise TarotRelationDiscoveryError("Tarot assertion resource bound exceeded")

    adjacency = [
        {
            "relation": "next-source-in-manifest",
            "source": source_order[index],
            "target": source_order[index + 1],
            "source_ordinal": index,
            "target_ordinal": index + 1,
        }
        for index in range(max(0, len(source_order) - 1))
    ]
    agreements = [
        {
            "relation": "same-field-exact-value",
            "field": field,
            "value_identity": identity,
            "members": members,
        }
        for (field, identity), members in sorted(exact_groups.items())
        if len(members) > 1
    ]
    artifact_bindings = [
        {
            "relation": "source-has-fetched-artifact",
            "source_id": row["source_id"],
            "artifact_path": row["artifact_path"],
            "sha256": row["sha256"],
            "bytes": row["bytes"],
            "content_type": row["content_type"],
        }
        for row in rows
        if row["artifact_path"] is not None
    ]

    report = {
        "schema": DISCOVERY_SCHEMA,
        "version": DISCOVERY_VERSION,
        "algorithm": {
            "identity": "exact-source-envelope-relations-v1",
            "field_order": list(FIELD_ORDER),
            "normalization": "none",
            "ocr": "not-run",
            "image_interpretation": "not-run",
            "max_sources": max_sources,
            "max_assertions": max_assertions,
        },
        "input": {
            "acquisition_receipt_sha256": receipt_sha,
            "evidence_index_sha256": receipt["evidence_index_sha256"],
            "manifest_file_sha256": receipt["manifest_file_sha256"],
            "manifest_canonical_sha256": receipt["manifest_canonical_sha256"],
        },
        "source_order": source_order,
        "assertions": assertions,
        "typed_absences": absences,
        "adjacency_relations": adjacency,
        "artifact_bindings": artifact_bindings,
        "exact_value_agreements": agreements,
        "counts": {
            "sources": len(source_order),
            "assertions": len(assertions),
            "typed_absences": len(absences),
            "adjacency_relations": len(adjacency),
            "artifact_bindings": len(artifact_bindings),
            "exact_value_agreements": len(agreements),
        },
        "status": "UNRESOLVED",
        "ontology_selected": False,
        "cross_source_card_identity_inferred": False,
        "geometry_attached": False,
        "measurement_attached": False,
        "canon_selection": None,
        "nonclaims": [
            "Tarot ontology",
            "cross-source card identity",
            "semantic equivalence",
            "historical truth",
            "UCNS recursive representation or geometry",
            "EDCM measurement validity",
        ],
        "hmmm": [
            "PDF text extraction and OCR are not run",
            "image regions and card boundaries are not interpreted",
            "same-field exact value is identity evidence, not semantic equivalence",
            "cross-source Tarot relations beyond source envelopes remain unresolved",
        ],
    }
    validate_discovery(report)
    return report


def validate_discovery(report: object) -> dict[str, Any]:
    """Fail closed on report status, ordering, counts, or forbidden escalation."""

    if not isinstance(report, dict):
        raise TarotRelationDiscoveryError("Tarot discovery report must be an object")
    if report.get("schema") != DISCOVERY_SCHEMA or report.get("version") != DISCOVERY_VERSION:
        raise TarotRelationDiscoveryError("Tarot discovery schema/version mismatch")
    if report.get("status") != "UNRESOLVED":
        raise TarotRelationDiscoveryError("single Tarot discovery status must remain UNRESOLVED")
    if any(report.get(field) is not False for field in (
        "ontology_selected",
        "cross_source_card_identity_inferred",
        "geometry_attached",
        "measurement_attached",
    )):
        raise TarotRelationDiscoveryError("Tarot discovery crossed a forbidden claim boundary")
    if report.get("canon_selection") is not None:
        raise TarotRelationDiscoveryError("Tarot discovery selected canon")
    counts = report.get("counts")
    if not isinstance(counts, dict):
        raise TarotRelationDiscoveryError("Tarot discovery counts are missing")
    expected = {
        "sources": len(report.get("source_order", ())),
        "assertions": len(report.get("assertions", ())),
        "typed_absences": len(report.get("typed_absences", ())),
        "adjacency_relations": len(report.get("adjacency_relations", ())),
        "artifact_bindings": len(report.get("artifact_bindings", ())),
        "exact_value_agreements": len(report.get("exact_value_agreements", ())),
    }
    if counts != expected:
        raise TarotRelationDiscoveryError("Tarot discovery count mismatch")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--acquisition", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-sources", type=int, default=DEFAULT_MAX_SOURCES)
    parser.add_argument("--max-assertions", type=int, default=DEFAULT_MAX_ASSERTIONS)
    args = parser.parse_args(argv)
    report = discover_relations(
        args.manifest,
        args.acquisition,
        max_sources=args.max_sources,
        max_assertions=args.max_assertions,
    )
    payload = _canonical_bytes(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    print(json.dumps(report["counts"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
