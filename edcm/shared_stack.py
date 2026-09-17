"""Deterministic shared UCNS/METAPAT/EDCM result contract.

Usage guidance
--------------
The supported layer pipeline calls :func:`build_result_contract` after semantic
and measurement stages. The resulting ``edcm_result`` record keeps source
evidence, METAPAT constraints, exact UCNS profile observations, typed UCNS
geometry/factorization absence, EDCM policy identity, implementation selection,
measured readouts, typed absence, unresolved fields, and attachment states in
separate compartments.

``epoch_identity`` changes when the METAPAT canon/provenance identity, UCNS
profile configuration, result schema, EDCM policy manifest, or selected implementation
changes. ``result_identity`` binds every emitted field except its own digest.
Public raw inputs enter through the layer pipeline; this module assembles trusted
in-process layer state and does not authenticate producers.
"""

# === MODULE_BUILD ===
# id: edcm_shared_stack
#   module_name: shared_stack
#   module_kind: schema
#   summary: deterministic final EDCM result contract separating source evidence, METAPAT semantic authority, exact UCNS word-gonol observations, typed UCNS geometry and factorization absence, EDCM policy identity, implementation provenance, readouts/NA, unresolved constraints, and attachment states.
#   owner: Erin Spencer
#   public_surface: RESULT_SCHEMA_ID, RESULT_SCHEMA_VERSION, EDCMResultContract, build_result_contract
#   internal_surface: _canonical_bytes, _digest, _source_evidence, _typed_absence, _readouts, _validate_measurement, _collect_unresolved
#   auth_boundary: none
#   storage_boundary: no persistence; emits deterministic JSON-compatible records
#   network_boundary: none
#   user_data_boundary: hashes caller transcript content and preserves caller source reference without external transmission
#   admin_only: false
#   tests: tests.test_shared_stack_contract, tests.test_ucns_adapter, tests.test_audit_regressions
#   rollout: default_enabled
#   rollback: remove the profile-observation compartment and restore the prior result schema only with a versioned migration
#   requires: edcmucns_manifest, edcm_metapat_adapter, edcm_ucns_adapter, edcm_measurement
#   since: 2026-07-12
#   unresolved: UCNS observation digests provide content identity but not signed producer authentication; profile observations do not supply formal geometry
# === END MODULE_BUILD ===

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Mapping

from .edcmucns.manifest import PolicyManifest

RESULT_SCHEMA_ID = "edcm.shared-stack-result"
RESULT_SCHEMA_VERSION = "2.0.0"


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
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
    measured = payload.get("measurement_computed") is True
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
    _validate_measurement(payload)
    return {
        "state": "measured",
        "rounds": payload.get("rounds"),
        "agent_metrics": payload.get("agent_metrics"),
        "alerts": payload.get("alerts"),
        "structural_density": payload.get("structural_density"),
        "na_fields": (),
    }


def _validate_measurement(payload: Mapping[str, Any]) -> None:
    """Validate completed layer state; this is not producer authentication."""
    def bounded(value: Any, low: float = 0.0) -> bool:
        return (isinstance(value, (int, float)) and not isinstance(value, bool)
                and math.isfinite(value) and low <= value <= 1.0)

    transcript = payload.get("transcript")
    rounds, projections, alerts = (payload.get(name) for name in ("rounds", "agent_metrics", "alerts"))
    if not isinstance(transcript, str) or not transcript.strip():
        raise ValueError("completed measurement requires a non-empty source transcript")
    if not isinstance(rounds, list) or not rounds:
        raise ValueError("completed measurement requires non-empty rounds")
    if not all(isinstance(rows, list) and len(rows) == len(rounds) for rows in (projections, alerts)):
        raise ValueError("measurement projections and alerts must cover every round")
    if not bounded(payload.get("structural_density")):
        raise ValueError("measurement structural density must be finite and bounded")
    axes = ("C", "R", "F", "E", "D", "N", "I", "O", "L", "P", "kappa", "dissonance_energy")
    for index, (row, projection, flags) in enumerate(zip(rounds, projections, alerts, strict=True)):
        if not isinstance(row, Mapping) or not isinstance(projection, Mapping):
            raise ValueError("measurement records must be mappings")
        if any(type(record.get("round_index")) is not int or record["round_index"] != index
               for record in (row, projection)):
            raise ValueError("measurement round indices must be complete and ordered")
        if not all(bounded(row.get(axis), -1.0 if axis == "O" else 0.0) for axis in axes):
            raise ValueError("measurement axes must be present, finite and bounded")
        if not all(type(row.get(key)) is int and row[key] >= 0 for key in ("token_count", "bone_count")):
            raise ValueError("measurement counts must be nonnegative integers")
        if not all(bounded(projection.get(axis)) for axis in ("CM", "DA", "DRIFT", "DVG", "INT", "TBF")):
            raise ValueError("measurement projections must be present, finite and bounded")
        if not isinstance(flags, list) or not all(isinstance(flag, str) for flag in flags):
            raise ValueError("measurement alerts must be a list of names per round")


def _collect_unresolved(payload: Mapping[str, Any]) -> tuple[str, ...]:
    unresolved: list[str] = []
    semantics = payload.get("metapat_semantics")
    if isinstance(semantics, Mapping):
        unresolved.extend(
            str(value) for value in semantics.get("unresolved_constraints", ())
        )
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
    ucns_profile_observation: dict[str, Any]
    ucns_geometry_identity: dict[str, Any]
    ucns_factorization_evidence: dict[str, Any]
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
    """Build from completed, trusted in-process layer state, not raw input.

    Use build_default_layers().run() for public input validation. Python callers
    controlling layer implementations remain trusted; hashes are not signatures.
    """
    if any(key in payload for key in ("ucns_geometry", "ucns_factorization_evidence")):
        raise ValueError("unsupported geometry or factorization evidence in result state")

    source = _source_evidence(payload)
    metapat = payload.get("metapat_semantics")
    if not isinstance(metapat, Mapping):
        metapat_record = _typed_absence(
            "metapat_semantic_constraints",
            "no validated METAPAT module envelope was attached",
        )
    else:
        metapat_record = {"state": "attached", **dict(metapat)}

    profile_observation = payload.get("ucns_profile_observation")
    if not isinstance(profile_observation, Mapping):
        profile_record = _typed_absence(
            "ucns_profile_observation",
            "no exact EDCM UCNS word-gonol observation was attached",
        )
    else:
        profile_record = {"state": "attached", **dict(profile_observation)}

    geometry_record = _typed_absence(
        "ucns_geometry_identity",
        "the EDCM word-gonol observation profile does not supply UCNS geometry",
    )
    factorization_record = _typed_absence(
        "ucns_factorization_evidence",
        "no factorization producer is authorized by this profile",
    )

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
        "ucns_profile_observation_attached": bool(
            ucns_status.get("ucns_profile_observation_attached", False)
        ),
        "ucns_bridge_record_attached": bool(
            ucns_status.get("ucns_bridge_record_attached", False)
        ),
        "ucns_factorization_evidence_attached": bool(
            ucns_status.get("ucns_factorization_evidence_attached", False)
        ),
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
        "evidence_authentication": (
            "content digests verified; cryptographic producer signature not supplied"
        ),
    }
    unresolved = _collect_unresolved(payload)

    epoch_fields = {
        "result_schema_version": RESULT_SCHEMA_VERSION,
        "metapat_canon_digest": metapat_record.get("canon_digest"),
        "metapat_provenance_digest": metapat_record.get("provenance_digest"),
        "ucns_profile_id": profile_record.get("profile_id"),
        "ucns_profile_version": profile_record.get("profile_version"),
        "ucns_profile_scope": profile_record.get("profile_scope"),
        "ucns_profile_source_commit": profile_record.get("source_commit"),
        "ucns_profile_options": profile_record.get("options"),
        "edcm_manifest_hash": manifest_record["manifest_hash"],
        "semantic_authority_implementation": implementation.get("semantic_authority"),
        "ucns_profile_implementation": implementation.get("ucns_profile"),
        "measurement_implementation": implementation.get("measurement"),
    }
    epoch_identity = _digest(epoch_fields)
    result_fields = dict(
        schema_id=RESULT_SCHEMA_ID,
        schema_version=RESULT_SCHEMA_VERSION,
        epoch_identity=epoch_identity,
        source_evidence=source,
        metapat_semantic_constraints=metapat_record,
        ucns_profile_observation=profile_record,
        ucns_geometry_identity=geometry_record,
        ucns_factorization_evidence=factorization_record,
        edcm_policy_manifest=manifest_record,
        implementation_provenance=implementation,
        readouts=readouts,
        status_evidence=status_evidence,
        unresolved_constraints=unresolved,
    )
    return EDCMResultContract(result_identity=_digest(result_fields), **result_fields)


__all__ = [
    "EDCMResultContract",
    "RESULT_SCHEMA_ID",
    "RESULT_SCHEMA_VERSION",
    "build_result_contract",
]
