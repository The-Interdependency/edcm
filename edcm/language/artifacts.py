"""Canonical metadata-free serialization for intrinsic gonol lists."""

# === MODULE_BUILD ===
# id: edcm_language_artifacts
#   module_name: artifacts
#   module_kind: adapter
#   summary: serializes ordered UCNS gonols as intrinsic-only canonical JSONL with no words, labels, evidence, source ids, or embedding classifications
#   owner: Erin Spencer
#   public_surface: intrinsic_gonol_record, metadata_free_jsonl, write_metadata_free_gonol_list
#   internal_surface: _anchor_record
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_embeddings
#   rollout: default_enabled
#   rollback: remove language embedding package before any published artifact depends on this serialization
#   requires: edcmbone_ucns_v04
#   since: 2026-07-13
#   unresolved: producer signatures and authenticated transport remain outside intrinsic gonol serialization
# === END MODULE_BUILD ===

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from edcm.measurement.ucns.ucns_v04 import AnchorPayload, UCNSObject


def _anchor_record(anchor: AnchorPayload) -> dict[str, Any]:
    return {
        "theta": [anchor.theta.numerator, anchor.theta.denominator],
        "payload": None if anchor.payload is None else intrinsic_gonol_record(anchor.payload),
    }


def intrinsic_gonol_record(gonol: UCNSObject) -> dict[str, Any]:
    """Return only intrinsic UCNS object data, recursively."""

    if not isinstance(gonol, UCNSObject):
        raise TypeError("gonol must be a UCNSObject")
    return {
        "n_dec": gonol.n_dec,
        "n_min": gonol.n_min,
        "anchors": [_anchor_record(anchor) for anchor in gonol.anchors_pos],
        "faces": list(gonol.faces_pos),
    }


def metadata_free_jsonl(gonols: Iterable[UCNSObject]) -> str:
    """Encode an ordered gonol sequence with no external metadata."""

    lines = [
        json.dumps(intrinsic_gonol_record(gonol), sort_keys=True, separators=(",", ":"))
        for gonol in gonols
    ]
    return "\n".join(lines) + ("\n" if lines else "")


def write_metadata_free_gonol_list(path: str | Path, gonols: Iterable[UCNSObject]) -> None:
    """Write the intrinsic-only JSONL artifact at a caller-selected path."""

    Path(path).write_text(metadata_free_jsonl(gonols), encoding="utf-8")


__all__ = [
    "intrinsic_gonol_record",
    "metadata_free_jsonl",
    "write_metadata_free_gonol_list",
]
