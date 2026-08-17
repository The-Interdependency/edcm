#!/usr/bin/env python3
"""Build the deterministic OEWN 2025 EDCM-on-UCNS lexical floor."""

# === MODULE_BUILD ===
# id: edcm_oewn2025_lexical_floor_builder
#   module_name: build_oewn2025_embeddings
#   module_kind: instrument
#   summary: acquires or verifies the pinned OEWN source and independently freezes direct-atomic and molecular UCNS relational artifacts before comparison
#   owner: Erin Spencer
#   public_surface: command line, build
#   internal_surface: _git, _acquire, _verify_oewn_source_tree_clean, _expected_source_manifest, _resume_complete
#   auth_boundary: verifies exact OEWN and UCNS commits
#   storage_boundary: caller-selected cache and output directories
#   network_boundary: git clone only when --acquire is explicitly supplied
#   user_data_boundary: public licensed lexical evidence only
#   admin_only: false
#   tests: tests.test_language_relational_bridge
#   rollout: explicit builder
#   rollback: remove builder and generated artifacts
#   requires: edcm_language_relational_bridge
#   since: 2026-08-16
#   unresolved: upstream cryptographic signatures are unavailable; Git and tree digests are identity, not authentication
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: oewn_source_is_exact_pinned_and_resumable
#   given: the lexical-floor builder consumes or acquires OEWN
#   then: exact repository commit, tag, counts, tree digest, license, and provenance are frozen and a complete run may be reused only after every listed artifact, branch, producer, status, and comparison identity validates
#   class: evidence
#   since: 2026-08-16
#
# id: lexical_comparison_occurs_after_freeze
#   given: a complete lexical-floor build runs
#   then: direct and molecular artifacts are written and receipted before the comparison function reads them
#   class: correctness
#   since: 2026-08-16
#
# id: incomplete_or_altered_lexical_resume_fails_closed
#   given: resume state is partial, noncanonical, stale, producer-mismatched, status-promoted, missing, or digest-altered
#   then: no completed run is reused and altered complete state raises an explicit error
#   class: safety
#   since: 2026-08-16
# === END CONTRACTS ===

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from edcm.language.affixes import affix_inventory_record, load_affix_inventory
from edcm.language.morphology import build_morphology_graph
from edcm.language.relational_bridge import (
    UCNS_RELATIONAL_COMMIT,
    build_direct_atomic,
    build_molecular,
    canonical_json_bytes,
    compare_frozen_branches,
    freeze_branch,
    validate_frozen_branch,
    verify_ucns_producer,
)
from edcm.language.rendering import normalize_lemma, transformation_inventory
from edcm.language.source import (
    OEWN_COMMIT, OEWN_EXPECTED_RELATION_COUNT, OEWN_EXPECTED_SYNSET_COUNT, OEWN_EXPECTED_WORD_COUNT,
    OEWN_LICENSE, OEWN_RELEASE_DATE, OEWN_REPOSITORY, OEWN_TAG, load_oewn_2025,
)

REQUIRED_ARTIFACT_FILES = frozenset({
    "affix-inventory.json",
    "comparison.json",
    "direct-atomic.binding.json",
    "direct-atomic.receipt.json",
    "direct-atomic.ucns.json",
    "molecular.binding.json",
    "molecular.receipt.json",
    "molecular.ucns.json",
    "morphology-evidence.json",
    "source-manifest.json",
    "transformations.json",
})
OEWN_SOURCE_TREE_SHA256 = "3a46546a1ffbb4aed98990535ad5155c69be12ad09fdf093701b257d2a3e468f"
OEWN_EXPECTED_SOURCE_FILE_COUNT = 73
OEWN_EXPECTED_SENSE_COUNT = 185_129
OEWN_OBSERVED_RELATION_COUNT = 244_727


def _git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def _acquire(target: Path) -> None:
    if target.exists():
        if not (target / ".git").is_dir():
            raise RuntimeError("source cache exists but is not a Git checkout")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "clone", "--filter=blob:none", "--no-checkout", f"https://github.com/{OEWN_REPOSITORY}.git", str(target)],
        check=True,
    )
    subprocess.run(["git", "-C", str(target), "checkout", "--detach", OEWN_COMMIT], check=True)


def _verified_snapshot(source_repo: Path):
    if _git(source_repo, "rev-parse", "HEAD") != OEWN_COMMIT:
        raise RuntimeError("OEWN checkout commit mismatch")
    if _git(source_repo, "rev-list", "-n", "1", OEWN_TAG) != OEWN_COMMIT:
        raise RuntimeError("OEWN release tag mismatch")
    _verify_oewn_source_tree_clean(source_repo)
    snapshot = load_oewn_2025(source_repo / "src" / "yaml")
    if len(snapshot.lexemes) != OEWN_EXPECTED_WORD_COUNT:
        raise RuntimeError("OEWN lexical-entry count mismatch")
    if len(snapshot.synsets) != OEWN_EXPECTED_SYNSET_COUNT:
        raise RuntimeError("OEWN synset count mismatch")
    if snapshot.sense_count != OEWN_EXPECTED_SENSE_COUNT:
        raise RuntimeError("OEWN sense count mismatch")
    if snapshot.relation_count != OEWN_OBSERVED_RELATION_COUNT:
        raise RuntimeError("OEWN observed relation count mismatch")
    if (
        snapshot.source_tree_sha256 != OEWN_SOURCE_TREE_SHA256
        or snapshot.source_file_count != OEWN_EXPECTED_SOURCE_FILE_COUNT
    ):
        raise RuntimeError("OEWN source tree identity mismatch")
    return snapshot


def _resume_source_tree_digest(source_repo: Path) -> tuple[str, int]:
    root = source_repo / "src" / "yaml"
    paths = tuple(sorted(root.rglob("*.yaml")))
    digest = sha256()
    for path in paths:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        payload = path.read_bytes()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest(), len(paths)


def _verify_oewn_source_tree_clean(source_repo: Path) -> tuple[str, int]:
    """Require the complete working source tree to equal the pinned Git tree."""

    changed = subprocess.run(
        ["git", "-C", str(source_repo), "diff", "--quiet", "HEAD", "--", "src/yaml"],
        check=False,
    )
    if changed.returncode != 0:
        raise RuntimeError("OEWN source tree has tracked changes")
    if _git(source_repo, "ls-files", "--others", "--", "src/yaml"):
        raise RuntimeError("OEWN source tree has untracked files")
    digest, file_count = _resume_source_tree_digest(source_repo)
    if digest != OEWN_SOURCE_TREE_SHA256 or file_count != OEWN_EXPECTED_SOURCE_FILE_COUNT:
        raise RuntimeError("OEWN source tree identity mismatch")
    return digest, file_count


def _expected_source_manifest() -> dict[str, object]:
    return {
        "schema": "edcm.oewn-2025-source",
        "version": "1.0.0",
        "repository": OEWN_REPOSITORY,
        "tag": OEWN_TAG,
        "commit": OEWN_COMMIT,
        "release_date": OEWN_RELEASE_DATE,
        "license": OEWN_LICENSE,
        "source_tree_sha256": OEWN_SOURCE_TREE_SHA256,
        "source_file_count": OEWN_EXPECTED_SOURCE_FILE_COUNT,
        "lexical_entry_count": OEWN_EXPECTED_WORD_COUNT,
        "synset_count": OEWN_EXPECTED_SYNSET_COUNT,
        "sense_count": OEWN_EXPECTED_SENSE_COUNT,
        "relation_count": OEWN_OBSERVED_RELATION_COUNT,
        "release_reported_relation_count": OEWN_EXPECTED_RELATION_COUNT,
        "ucns_commit": UCNS_RELATIONAL_COMMIT,
    }


def _verify_resumable_source(source_repo: Path, source: object) -> dict[str, object]:
    if not isinstance(source, dict):
        raise RuntimeError("resumable source manifest is missing")
    if _git(source_repo, "rev-parse", "HEAD") != OEWN_COMMIT:
        raise RuntimeError("OEWN checkout commit mismatch")
    if _git(source_repo, "rev-list", "-n", "1", OEWN_TAG) != OEWN_COMMIT:
        raise RuntimeError("OEWN release tag mismatch")
    _verify_oewn_source_tree_clean(source_repo)
    expected = _expected_source_manifest()
    if source != expected:
        raise RuntimeError("resumable OEWN source identity mismatch")
    return expected


def _resume_complete(
    output: Path,
    source_manifest: dict[str, object],
    verification,
) -> dict[str, object]:
    manifest_bytes = (output / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    if canonical_json_bytes(manifest) != manifest_bytes:
        raise RuntimeError("resumable manifest is not canonical")
    if manifest.get("source") != source_manifest or manifest.get("status") != "UNRESOLVED":
        raise RuntimeError("resumable manifest identity or status mismatch")
    source_manifest_bytes = (output / "source-manifest.json").read_bytes()
    stored_source_manifest = json.loads(source_manifest_bytes)
    if canonical_json_bytes(stored_source_manifest) != source_manifest_bytes:
        raise RuntimeError("resumable source manifest is not canonical")
    if stored_source_manifest != source_manifest:
        raise RuntimeError("resumable source manifest mismatch")
    records = manifest.get("files")
    if not isinstance(records, list) or any(not isinstance(record, dict) for record in records):
        raise RuntimeError("resumable artifact inventory is invalid")
    listed_files = {record.get("path") for record in records}
    actual_files = {
        path.relative_to(output).as_posix()
        for path in output.rglob("*")
        if path.is_file()
    }
    if listed_files != REQUIRED_ARTIFACT_FILES or actual_files != REQUIRED_ARTIFACT_FILES | {"manifest.json"}:
        raise RuntimeError("resumable artifact file set mismatch")
    if len(records) != len(REQUIRED_ARTIFACT_FILES):
        raise RuntimeError("resumable artifact inventory contains duplicates")
    for record in records:
        path = output / record["path"]
        payload = path.read_bytes()
        if len(payload) != record["bytes"] or sha256(payload).hexdigest() != record["sha256"]:
            raise RuntimeError(f"resumable artifact mismatch: {record['path']}")
    for branch in ("direct-atomic", "molecular"):
        validate_frozen_branch(output, branch, verification)
    comparison = compare_frozen_branches(output, verification)
    if comparison != manifest.get("comparison"):
        raise RuntimeError("resumable comparison mismatch")
    return manifest


def build(
    source_repo: Path,
    ucns_source_root: Path,
    output: Path,
    *,
    resume: bool = False,
) -> dict[str, object]:
    source_repo = source_repo.resolve()
    verification = verify_ucns_producer(ucns_source_root)
    output.mkdir(parents=True, exist_ok=True)
    if resume and (output / "manifest.json").is_file():
        existing = json.loads((output / "manifest.json").read_bytes())
        source_manifest = _verify_resumable_source(
            source_repo, existing.get("source") if isinstance(existing, dict) else None
        )
        return _resume_complete(output, source_manifest, verification)

    if any(output.iterdir()):
        raise RuntimeError("fresh lexical output directory must be empty")

    snapshot = _verified_snapshot(source_repo)
    source_manifest = _expected_source_manifest()
    (output / "source-manifest.json").write_bytes(canonical_json_bytes(source_manifest))

    freeze_branch(
        output, "direct-atomic", build_direct_atomic(snapshot), verification
    )

    surfaces = {
        normalize_lemma(value)
        for lexeme in snapshot.lexemes
        for value in (lexeme.lemma, *lexeme.forms)
        if normalize_lemma(value)
    }
    affixes = load_affix_inventory()
    graph = build_morphology_graph(surfaces, affixes)
    (output / "affix-inventory.json").write_bytes(
        canonical_json_bytes(affix_inventory_record(affixes))
    )
    (output / "transformations.json").write_bytes(
        canonical_json_bytes(transformation_inventory())
    )
    (output / "morphology-evidence.json").write_bytes(
        canonical_json_bytes(graph.metadata_record())
    )
    freeze_branch(
        output, "molecular", build_molecular(graph, affixes), verification
    )

    comparison = compare_frozen_branches(output, verification)
    actual_files = {
        path.relative_to(output).as_posix()
        for path in output.rglob("*")
        if path.is_file()
    }
    if actual_files != REQUIRED_ARTIFACT_FILES:
        raise RuntimeError("fresh lexical artifact file set mismatch")
    files = []
    for name in sorted(REQUIRED_ARTIFACT_FILES):
        path = output / name
        payload = path.read_bytes()
        files.append({"path": name, "bytes": len(payload), "sha256": sha256(payload).hexdigest()})
    manifest = {
        "schema": "edcm.english-lexical-floor-artifact-set",
        "version": "1.0.0",
        "source": source_manifest,
        "comparison": comparison,
        "files": files,
        "status": "UNRESOLVED",
        "nonclaims": ["canonical English morphology", "UCNS geometry", "EDCM measurement validity", "phrase or discourse semantics"],
    }
    (output / "manifest.json").write_bytes(canonical_json_bytes(manifest))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--ucns-source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--acquire", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.acquire:
        _acquire(args.source_repo)
    result = build(
        args.source_repo,
        args.ucns_source_root,
        args.output,
        resume=args.resume,
    )
    print(json.dumps(result["comparison"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
