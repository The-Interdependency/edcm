# === MODULE_BUILD ===
# id: edcmucns_provenance
#   module_name: provenance
#   module_kind: schema
#   summary: ProvenanceWitness — anchor-level testimony for edcmucns v0.3.1; provenance is measurement material, not decorative metadata
#   owner: Erin Spencer
#   public_surface: ProvenanceWitness, READOUT_BEARING_FIELDS, canonicalize, witness_hash, bundle_hash
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: transcripts may carry user speech in surface_form; hashes only summarize, they do not redact
#   admin_only: false
#   tests: tests.test_edcmucns_identity_v031
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: none
#   since: 2026-07-06
#   unresolved: constraint_governance vocabulary is not yet enumerated; carried as an opaque readout-bearing string
# === END MODULE_BUILD ===

"""Provenance witnesses for edcmucns v0.3.1.

Geometry needs testimony. A witness records what a host anchor is evidence
of. Only readout-bearing fields participate in provenance hashes; decorative
fields are carried but never hashed.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import dataclass

# The readout-bearing witness fields, in canonical hash order (v0.3.1).
READOUT_BEARING_FIELDS: tuple[str, ...] = (
    "family",
    "ordinal_m_f",
    "residue_r_f",
    "turn_id",
    "speaker_or_source",
    "surface_form",
    "role",
    "constraint_governance",
    "payload_attachment",
)


def canonicalize(value: str) -> str:
    """Stable canonicalization for turn_id / speaker_or_source (idempotent)."""

    return unicodedata.normalize("NFC", value).strip()


@dataclass(frozen=True, slots=True)
class ProvenanceWitness:
    """Anchor witness. Fields mirror the v0.3.1 handoff exactly."""

    family: str | None
    ordinal_m_f: int | None
    residue_r_f: int | None
    turn_id: str
    speaker_or_source: str
    surface_form: str
    role: str
    constraint_governance: str = "none"
    payload_attachment: str | None = None
    # Decorative fields ride along but are excluded from every provenance hash.
    decorative: tuple[tuple[str, str], ...] = ()

    def readout_bearing(self) -> dict[str, object]:
        return {name: getattr(self, name) for name in READOUT_BEARING_FIELDS}


def witness_hash(witness: ProvenanceWitness) -> str:
    """Hash of the readout-bearing fields only (decorative fields excluded)."""

    blob = json.dumps(witness.readout_bearing(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def bundle_hash(witnesses: tuple[ProvenanceWitness, ...] | list[ProvenanceWitness],
                *, exclude_fields: tuple[str, ...] = ()) -> str:
    """Ordered (chronological) hash of a witness bundle.

    Order is readout-bearing: A-then-B and B-then-A are different testimony.
    ``exclude_fields`` lets a readout scope drop out-of-scope fields (for
    example payload_attachment outside payload readouts) without inventing a
    second witness object.
    """

    records = []
    for w in witnesses:
        rec = w.readout_bearing()
        for name in exclude_fields:
            rec.pop(name, None)
        records.append(rec)
    blob = json.dumps(records, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()
