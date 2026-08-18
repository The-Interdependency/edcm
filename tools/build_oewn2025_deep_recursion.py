#!/usr/bin/env python3
"""Build the complete first closed OEWN semantic/definition recursion layer."""

# === MODULE_BUILD ===
# id: edcm_oewn_deep_recursion_builder
#   module_name: build_oewn2025_deep_recursion
#   module_kind: adapter
#   summary: validates a sealed OEWN lexical floor, exhaustively constructs depth-one closed definitions and semantic relations, and freezes deterministic UCNS artifacts
#   owner: Erin Spencer
#   public_surface: REQUIRED_ARTIFACT_FILES, build, main
#   internal_surface: _digest, _canonical_read, _source_receipt, _resume_complete
#   auth_boundary: exact OEWN and merged UCNS identities are inherited and revalidated
#   storage_boundary: caller-selected output directory
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_deep_recursion
#   rollout: run twice in clean directories and compare bytes before sealing an evidence receipt
#   rollback: remove generated layer artifacts without altering lexical-floor artifacts
#   requires: edcm_language_deep_recursion, edcm_language_relational_bridge, edcm_oewn_complete_builder
#   since: 2026-08-18
#   unresolved: independent replay outcome, dictionary coverage, geometry, measurement, higher language
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: deep_recursion_requires_sealed_floor
#   given: the depth-one builder runs or resumes
#   then: the exact frozen direct-atomic floor, its source identity, and every digest are validated before construction or reuse
#   class: safety
#   since: 2026-08-18
#
# id: deep_recursion_resume_is_fail_closed
#   given: a completed depth-one output is resumed
#   then: unexpected, missing, noncanonical, or digest-mismatched files abort reuse
#   class: safety
#   since: 2026-08-18
# === END CONTRACTS ===

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

from edcm.language.deep_recursion import (
    DEEP_RECURSION_LAYER,
    build_deep_recursion_layer,
    load_floor_surface_binding,
)
from edcm.language.relational_bridge import (
    canonical_json_bytes,
    freeze_relational_layer,
    validate_frozen_branch,
    validate_frozen_relational_layer,
    verify_ucns_producer,
)
from tools.build_oewn2025_embeddings import (
    _expected_source_manifest,
    _verified_snapshot,
)

REQUIRED_ARTIFACT_FILES = frozenset({
    "coverage.json",
    "floor-receipt.json",
    "source-manifest.json",
    f"{DEEP_RECURSION_LAYER}.binding.json",
    f"{DEEP_RECURSION_LAYER}.receipt.json",
    f"{DEEP_RECURSION_LAYER}.ucns.json",
})


def _digest(payload: bytes) -> str:
    return sha256(payload).hexdigest()


def _canonical_read(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    value = json.loads(payload)
    if not isinstance(value, dict) or canonical_json_bytes(value) != payload:
        raise RuntimeError(f"noncanonical artifact: {path.name}")
    return value


def _source_receipt(floor: Path, verification) -> dict[str, object]:
    floor_branch = validate_frozen_branch(floor, "direct-atomic", verification)
    floor_source = _canonical_read(floor / "source-manifest.json")
    if floor_source != _expected_source_manifest():
        raise RuntimeError("lexical floor source identity mismatch")
    records = []
    for name in (
        "source-manifest.json", "direct-atomic.ucns.json",
        "direct-atomic.binding.json", "direct-atomic.receipt.json",
    ):
        payload = (floor / name).read_bytes()
        records.append({"path": name, "bytes": len(payload), "sha256": _digest(payload)})
    return {
        "schema": "edcm.english-lexical-floor-input-receipt",
        "version": "1.0.0",
        "direct_atomic_receipt": floor_branch,
        "files": records,
    }


def _resume_complete(output: Path, floor_receipt: dict[str, object], verification) -> dict[str, object]:
    manifest = _canonical_read(output / "manifest.json")
    if manifest.get("status") != "UNRESOLVED" or manifest.get("floor") != floor_receipt:
        raise RuntimeError("resumable deep-recursion identity or status mismatch")
    actual = {path.name for path in output.iterdir() if path.is_file()}
    if actual != REQUIRED_ARTIFACT_FILES | {"manifest.json"}:
        raise RuntimeError("resumable deep-recursion file set mismatch")
    records = manifest.get("files")
    if not isinstance(records, list) or len(records) != len(REQUIRED_ARTIFACT_FILES):
        raise RuntimeError("resumable deep-recursion inventory is invalid")
    if {record.get("path") for record in records if isinstance(record, dict)} != REQUIRED_ARTIFACT_FILES:
        raise RuntimeError("resumable deep-recursion inventory mismatch")
    for record in records:
        payload = (output / record["path"]).read_bytes()
        if len(payload) != record.get("bytes") or _digest(payload) != record.get("sha256"):
            raise RuntimeError(f"resumable deep-recursion artifact mismatch: {record['path']}")
    validate_frozen_relational_layer(output, DEEP_RECURSION_LAYER, verification)
    coverage = _canonical_read(output / "coverage.json")
    if coverage != manifest.get("coverage"):
        raise RuntimeError("resumable deep-recursion coverage mismatch")
    return manifest


def build(
    source_repo: Path,
    ucns_source_root: Path,
    lexical_floor_root: Path,
    output: Path,
    *,
    resume: bool = False,
) -> dict[str, object]:
    verification = verify_ucns_producer(ucns_source_root)
    floor_receipt = _source_receipt(lexical_floor_root, verification)
    output.mkdir(parents=True, exist_ok=True)
    if resume and (output / "manifest.json").is_file():
        return _resume_complete(output, floor_receipt, verification)
    if any(output.iterdir()):
        raise RuntimeError("fresh deep-recursion output directory must be empty")

    snapshot = _verified_snapshot(source_repo.resolve())
    source_manifest = _expected_source_manifest()
    surfaces = load_floor_surface_binding(lexical_floor_root / "direct-atomic.binding.json")
    layer = build_deep_recursion_layer(snapshot, surfaces)
    (output / "source-manifest.json").write_bytes(canonical_json_bytes(source_manifest))
    (output / "floor-receipt.json").write_bytes(canonical_json_bytes(floor_receipt))
    (output / "coverage.json").write_bytes(canonical_json_bytes(layer.coverage))
    freeze_relational_layer(
        output, DEEP_RECURSION_LAYER, layer.node_binding, layer.relation_binding,
        layer.edges, layer.edge_binding, verification,
    )
    validate_frozen_relational_layer(output, DEEP_RECURSION_LAYER, verification)

    actual = {path.name for path in output.iterdir() if path.is_file()}
    if actual != REQUIRED_ARTIFACT_FILES:
        raise RuntimeError("fresh deep-recursion artifact file set mismatch")
    files = []
    for name in sorted(REQUIRED_ARTIFACT_FILES):
        payload = (output / name).read_bytes()
        files.append({"path": name, "bytes": len(payload), "sha256": _digest(payload)})
    manifest = {
        "schema": "edcm.english-lexical-deep-recursion-artifact-set",
        "version": "1.0.0",
        "source": source_manifest,
        "floor": floor_receipt,
        "coverage": layer.coverage,
        "files": files,
        "status": "UNRESOLVED",
        "nonclaims": layer.coverage["nonclaims"],
    }
    (output / "manifest.json").write_bytes(canonical_json_bytes(manifest))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--ucns-source-root", type=Path, required=True)
    parser.add_argument("--lexical-floor-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    result = build(
        args.source_repo, args.ucns_source_root, args.lexical_floor_root,
        args.output, resume=args.resume,
    )
    print(json.dumps(result["coverage"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
