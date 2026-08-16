#!/usr/bin/env python3
"""Build the deterministic OEWN 2025 EDCM-on-UCNS lexical floor."""

# === MODULE_BUILD ===
# id: edcm_oewn2025_lexical_floor_builder
#   module_name: build_oewn2025_embeddings
#   module_kind: instrument
#   summary: acquires or verifies the pinned OEWN source and independently freezes direct-atomic and molecular UCNS relational artifacts before comparison
#   owner: Erin Spencer
#   public_surface: command line, build
#   internal_surface: _git, _acquire, _source_manifest
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
#   then: exact repository commit, tag, counts, tree digest, license, and provenance are frozen and completed valid branch receipts may be reused without recomputation
#   class: evidence
#   since: 2026-08-16
#
# id: lexical_comparison_occurs_after_freeze
#   given: a complete lexical-floor build runs
#   then: direct and molecular artifacts are written and receipted before the comparison function reads them
#   class: correctness
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
)
from edcm.language.rendering import normalize_lemma, transformation_inventory
from edcm.language.source import (
    OEWN_COMMIT, OEWN_EXPECTED_RELATION_COUNT, OEWN_EXPECTED_SYNSET_COUNT, OEWN_EXPECTED_WORD_COUNT,
    OEWN_LICENSE, OEWN_RELEASE_DATE, OEWN_REPOSITORY, OEWN_TAG, load_oewn_2025,
)


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
    snapshot = load_oewn_2025(source_repo / "src" / "yaml")
    if len(snapshot.lexemes) != OEWN_EXPECTED_WORD_COUNT:
        raise RuntimeError("OEWN lexical-entry count mismatch")
    if len(snapshot.synsets) != OEWN_EXPECTED_SYNSET_COUNT:
        raise RuntimeError("OEWN synset count mismatch")
    return snapshot


def build(source_repo: Path, output: Path, *, resume: bool = False) -> dict[str, object]:
    snapshot = _verified_snapshot(source_repo.resolve())
    output.mkdir(parents=True, exist_ok=True)
    source_manifest = {
        "schema": "edcm.oewn-2025-source",
        "version": "1.0.0",
        "repository": OEWN_REPOSITORY,
        "tag": OEWN_TAG,
        "commit": OEWN_COMMIT,
        "release_date": OEWN_RELEASE_DATE,
        "license": OEWN_LICENSE,
        "source_tree_sha256": snapshot.source_tree_sha256,
        "source_file_count": snapshot.source_file_count,
        "lexical_entry_count": len(snapshot.lexemes),
        "synset_count": len(snapshot.synsets),
        "sense_count": snapshot.sense_count,
        "relation_count": snapshot.relation_count,
        "release_reported_relation_count": OEWN_EXPECTED_RELATION_COUNT,
        "ucns_commit": UCNS_RELATIONAL_COMMIT,
    }
    (output / "source-manifest.json").write_bytes(canonical_json_bytes(source_manifest))

    direct_receipt = output / "direct-atomic.receipt.json"
    if not (resume and direct_receipt.is_file()):
        freeze_branch(output, "direct-atomic", build_direct_atomic(snapshot))

    molecular_receipt = output / "molecular.receipt.json"
    if not (resume and molecular_receipt.is_file()):
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
        freeze_branch(output, "molecular", build_molecular(graph, affixes))

    comparison = compare_frozen_branches(output)
    files = []
    for path in sorted(output.iterdir()):
        if path.is_file() and path.name != "manifest.json":
            payload = path.read_bytes()
            files.append({"path": path.name, "bytes": len(payload), "sha256": sha256(payload).hexdigest()})
    manifest = {
        "schema": "edcm.english-lexical-floor-artifact-set",
        "version": "1.0.0",
        "source": source_manifest,
        "comparison": comparison,
        "files": files,
        "status": "SURVIVED",
        "nonclaims": ["canonical English morphology", "UCNS geometry", "EDCM measurement validity", "phrase or discourse semantics"],
    }
    (output / "manifest.json").write_bytes(canonical_json_bytes(manifest))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--acquire", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.acquire:
        _acquire(args.source_repo)
    result = build(args.source_repo, args.output, resume=args.resume)
    print(json.dumps(result["comparison"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
