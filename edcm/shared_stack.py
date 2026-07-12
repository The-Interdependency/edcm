"""Deterministic shared UCNS/METAPAT/EDCM result contract.

Usage guidance
--------------
The supported layer pipeline calls :func:`build_result_contract` after semantic
and measurement stages. The resulting ``edcm_result`` record keeps source
evidence, METAPAT constraints, UCNS geometry identity, EDCM policy identity,
implementation selection, measured readouts, typed absence, unresolved fields,
and attached status evidence in separate compartments.

``epoch_identity`` changes when the METAPAT canon/provenance identity, UCNS
geometry identity, EDCM policy manifest, or selected implementation changes.
``result_identity`` additionally binds the measured source and readouts.
"""

# === MODULE_BUILD ===
# id: edcm_shared_stack
#   module_name: shared_stack
#   module_kind: schema
#   summary: deterministic final EDCM result contract separating source evidence, METAPAT semantic authority, UCNS geometry, EDCM policy identity, implementation provenance, readouts/NA, unresolved constraints, and attached status evidence.
#   owner: Erin Spencer
#   public_surface: RESULT_SCHEMA_ID, RESULT_SCHEMA_VERSION, EDCMResultContract, build_result_contract
#   internal_surface: _canonical_bytes, _digest, _source_evidence, _typed_absence, _readouts, _collect_unresolved
#   auth_boundary: none
#   storage_boundary: no persistence; emits deterministic JSON-compatible records
#   network_boundary: none
#   user_data_boundary: hashes caller transcript content and preserves caller source reference without external transmission
#   admin_only: false
#   tests: tests.test_shared_stack_contract
#   rollout: default_enabled
#   rollback: remove edcm_result assembly and restore local composition fallback
#   requires: edcmucns_manifest, edcm_metapat_adapter, edcm_ucns_adapter, edcm_measurement
#   since: 2026-07-12
#   unresolved: official negative-certification and theorem-status envelopes remain unattached until their validated schemas are supplied
# === END MODULE_BUILD ===

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping

from .edcmucns.manifest import PolicyManifest

RESULT_SCHEMA_ID = "edcm.shared-stack-result"
RESULT_SCHEMA_VERSION = "1.0.0"


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _typed_absence(kind: str, reason: str) -> dict[str, Any]:
    return {
        "state": "NA",
        "kind": kind,
        "value": None,
        "reason": reason,
    }


def _source_evidence(payload: Mapping[str, Any]) -> dict[str, Any]:
    transcript = payload.get("transcript")
    source_ref = payload.get("source_ref")
    if not isinstance(transcript, str) or not transcript.strip():
        absent = _typed_absence("transcript", "no non-empty transcript was supplied")
        absent["source_ref"] = str(source_ref) if source_ref is not None else None
        return absent
    encoded = transcript.encode("utf-8")
    return {
        "state": "attached",
        "kind": "transcript",
        "source_ref": str(source_ref) if source_ref is not None else None,
        "sha256": hashlib.sha256(encoded).hexdigest(),
        "utf8_bytes": len(encoded),
        "characters": len(transcript),
    }


def _readouts(payload: Mapping[str, Any]) -> dict[str, Any]:
    measured = "rounds" in payload
    if not measured:
        return {
            "state": "NA",
            "reason": "no transcript measurement was produced",
            "rounds": None,
            "agent_metrics": None,
            "alerts": None,
            "structural_density": None,
            "na_fields": (
                "rounds",
                "agent_metrics",
                "alerts",
                "structural_density",
            ),
        }
    return {
        "state": "measured",
        "rounds": payload.get("rounds"),
        "agent_metrics": payload.get("agent_metrics"),
        "alerts": payload.get("alerts"),
        "structural_density": payload.get("structural_density"),
        "na_fields": (),
    }


def _collect_unresolved(payload: Mapping[str, Any]) -> tuple[str, ...]:
    unresolved: list[str] = []
    semantics = payload.get("metapat_semantics")
    if isinstance(semantics, Mapping):
        unresolved.extend(str(value) for value in semantics.get("unresolved_constraints", ()))
    provenance = payload.get("layer_provenance")
    if isinstance(provenance, Mapping):
        for record in provenance.values():
            if isinstance(record, Mapping):
                unresolved.extend(
                    str(value) for value in record.get("unresolved_constraints", ())
                )
    return tuple(dict.fromkeys(unresolved))


@dataclass(frozen=True, slots=True)
class EDCMResultContract:
    schema_id: str
    schema_version: str
    epoch_identity: str
    result_identity: str
    source_evidence: dict[str, Any]
    metapat_semantic_constraints: dict[str, Any]
    ucns_geometry_identity: dict[str, Any]
    edcm_policy_manifest: dict[str, Any]
    implementation_provenance: dict[str, Any]
    readouts: dict[str, Any]
    status_evidence: dict[str, Any]
    unresolved_constraints: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    def canonical_json(self) -> str:
        return _canonical_bytes(self.as_dict()).decode("utf-8")


def build_result_contract(
    payload: Mapping[str, Any],
    manifest: PolicyManifest,
) -> EDCMResultContract:
    """Build the deterministic final contract from completed layer state."""

    source = _source_evidence(payload)
    metapat = payload.get("metapat_semantics")
    if not isinstance(metapat, Mapping):
        metapat_record = _typed_absence(
            "metapat_semantic_constraints",
            "no validated METAPAT module envelope was attached",
        )
    else:
        metapat_record = {"state": "attached", **dict(metapat)}

    ucns = payload.get("ucns_geometry")
    if not isinstance(ucns, Mapping):
        ucns_record = _typed_absence(
            "ucns_geometry_identity",
            "no actual UCNS object or validated bridge record was attached",
        )
    else:
        ucns_record = {"state": "attached", **dict(ucns)}

    manifest_record = {
        "schema": "edcm.policy-manifest.v031",
        "manifest_hash": manifest.manifest_hash(),
        "canonical_json": manifest.canonical_json(),
        "policy_fields": json.loads(manifest.canonical_json()),
    }
    implementation = dict(payload.get("layer_provenance", {}))
    readouts = _readouts(payload)
    metapat_status = dict(payload.get("metapat_integration", {}))
    ucns_status = dict(payload.get("ucns_integration", {}))
    status_evidence = {
        "metapat": metapat_status,
        "ucns": ucns_status,
        "ucns_theorem_status_attached": bool(
            ucns_status.get("ucns_theorem_status_attached", False)
        ),
        "ucns_negative_certification_attached": bool(
            ucns_status.get("ucns_negative_certification_attached", False)
        ),
        "metapat_theorem_status_attached": bool(
            metapat_status.get("metapat_theorem_status_attached", False)
        ),
        "proof_status_transfers_to_measurement_validity": False,
        "semantic_labels_are_measurement_values": False,
        "measurement_validity_basis": "EDCM declared measurement contract only",
    }
    unresolved = _collect_unresolved(payload)

    epoch_fields = {
        "metapat_canon_digest": metapat_record.get("canon_digest"),
        "metapat_provenance_digest": metapat_record.get("provenance_digest"),
        "ucns_stable_hash": ucns_record.get("stable_hash"),
        "ucns_schema": ucns_record.get("ucns_serialization_version"),
        "edcm_manifest_hash": manifest_record["manifest_hash"],
        "semantic_authority_implementation": implementation.get("semantic_authority"),
        "geometry_implementation": implementation.get("geometry"),
        "measurement_implementation": implementation.get("measurement"),
    }
    epoch_identity = _digest(epoch_fields)
    result_identity = _digest(
        {
            "epoch_identity": epoch_identity,
            "source_evidence": source,
            "readouts": readouts,
        }
    )

    return EDCMResultContract(
        schema_id=RESULT_SCHEMA_ID,
        schema_version=RESULT_SCHEMA_VERSION,
        epoch_identity=epoch_identity,
        result_identity=result_identity,
        source_evidence=source,
        metapat_semantic_constraints=metapat_record,
        ucns_geometry_identity=ucns_record,
        edcm_policy_manifest=manifest_record,
        implementation_provenance=implementation,
        readouts=readouts,
        status_evidence=status_evidence,
        unresolved_constraints=unresolved,
    )


__all__ = [
    "EDCMResultContract",
    "RESULT_SCHEMA_ID",
    "RESULT_SCHEMA_VERSION",
    "build_result_contract",
]
