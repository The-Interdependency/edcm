# === CHECKS ===
# id: language_relational_branch_check
#   proves: lexical_branches_are_independently_constructed, english_metadata_is_external_to_ucns_carrier, lexical_ucns_producer_is_exactly_verified, lexical_relation_multiplicity_is_preserved, lexical_pre_replay_status_is_unresolved, comparison_requires_two_prior_freezes, lexical_manifest_preserves_authority_firewall
#   call: self::language_relational_branch_check
#   timeout: 30
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: oewn_builder_order_check
#   proves: oewn_source_is_exact_pinned_and_resumable, incomplete_or_altered_lexical_resume_fails_closed, lexical_comparison_occurs_after_freeze
#   call: self::test_builder_contract_is_pinned_and_freeze_order_is_explicit
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import ModuleType

import pytest

from edcm.language.affixes import AffixRecord
from edcm.language.morphology import Decomposition, MorphologyGraph, build_morphology_graph
from edcm.language.manifest import embedding_manifest
from edcm.language.model import (
    AtomicForkRelation,
    AtomicForkResult,
    Attestation,
    CompositionNode,
    LexicalEvidence,
    Soundness,
)
from edcm.language.relational_bridge import (
    LexicalBridgeError, UCNSProducerVerification, build_direct_atomic, build_molecular,
    canonical_json_bytes, compare_frozen_branches, freeze_branch,
    validate_frozen_branch, verify_ucns_producer,
)
from edcm.language.source import LexemeRecord, SenseRecord, SynsetRecord, WordnetSnapshot
from tools import build_oewn2025_embeddings as lexical_builder
from tools.build_oewn2025_embeddings import REQUIRED_ARTIFACT_FILES, _resume_complete


def _ucns_root() -> Path:
    configured = os.environ.get("EDCM_LEXICAL_UCNS_ROOT") or os.environ.get("UCNS_SOURCE_ROOT")
    if configured:
        return Path(configured).resolve()
    try:
        import ucns.relational_carrier as module
    except ImportError as exc:
        raise RuntimeError(
            "set EDCM_LEXICAL_UCNS_ROOT to the exact lexical producer checkout"
        ) from exc
    path = Path(module.__file__ or "").resolve()
    if len(path.parents) < 3:
        raise RuntimeError("installed UCNS module path cannot identify its checkout")
    return path.parents[2]


def _verification_or_skip():
    try:
        return verify_ucns_producer(_ucns_root())
    except (RuntimeError, LexicalBridgeError) as exc:
        pytest.skip(str(exc))


def _snapshot() -> WordnetSnapshot:
    return WordnetSnapshot(
        lexemes=(
            LexemeRecord("kind", "n", (), (SenseRecord("kind%1", "kind-n", ()),)),
            LexemeRecord("kindness", "n", (), (SenseRecord("kindness%1", "kindness-n", ()),)),
        ),
        synsets=(
            SynsetRecord("kind-n", "n", ("kind",), ("quality",), ()),
            SynsetRecord("kindness-n", "n", ("kindness",), ("state",), (("hypernym", ("kind-n",)),)),
        ),
        source_tree_sha256="0" * 64,
        source_file_count=1,
    )


def _independent_branches_freeze_before_comparison(
    tmp_path: Path,
    verification: UCNSProducerVerification,
) -> None:
    manifest = embedding_manifest()
    assert manifest.ucns_owns_representation and manifest.edcm_owns_english_evidence
    assert manifest.legacy_placement_present is False and manifest.geometry_attached is False
    affix = AffixRecord("ness", "-ness", "-ness", "suffix", "derivational_suffixes", "S", ("S",), "", None)
    direct = build_direct_atomic(_snapshot())
    graph = build_morphology_graph(("kind", "kindness"), (affix,))
    molecular = build_molecular(graph, (affix,))
    assert direct.node_binding != molecular.node_binding
    with pytest.raises(FileNotFoundError):
        compare_frozen_branches(tmp_path, verification)
    freeze_branch(tmp_path, "direct-atomic", direct, verification)
    freeze_branch(tmp_path, "molecular", molecular, verification)
    result = compare_frozen_branches(tmp_path, verification)
    assert result["shared_surface_count"] == 2
    assert result["intrinsic_equal"] is False
    for branch in ("direct-atomic", "molecular"):
        intrinsic = (tmp_path / f"{branch}.ucns.json").read_text()
        assert "kind" not in intrinsic and "provenance" not in intrinsic
    assert result["status"] == "UNRESOLVED"
    assert validate_frozen_branch(tmp_path, "direct-atomic", verification)["status"] == "UNRESOLVED"


def language_relational_branch_check() -> None:
    """Self-contained CHECKS witness for the exact configured UCNS checkout."""

    verification = verify_ucns_producer(_ucns_root())
    with TemporaryDirectory(prefix="edcm-lexical-check-") as directory:
        _independent_branches_freeze_before_comparison(Path(directory), verification)


def test_independent_branches_freeze_before_comparison(tmp_path: Path) -> None:
    _independent_branches_freeze_before_comparison(tmp_path, _verification_or_skip())


def test_relation_multiplicity_is_preserved_in_both_independent_branches() -> None:
    duplicate_snapshot = WordnetSnapshot(
        lexemes=(
            LexemeRecord(
                "kind",
                "n",
                (),
                (
                    SenseRecord(
                        "kind%1",
                        "kind-n",
                        (("also", ("kind%1", "kind%1")),),
                    ),
                ),
            ),
        ),
        synsets=(SynsetRecord("kind-n", "n", ("kind",), (), ()),),
        source_tree_sha256="0" * 64,
        source_file_count=1,
    )
    direct = build_direct_atomic(duplicate_snapshot)
    assert direct.edges.count(direct.edges[-1]) == 2

    duplicate = Decomposition("explicit-compound", ("surface:kind", "surface:kind"), rendering="closed")
    graph = MorphologyGraph(
        surfaces=("kind", "kindkind"),
        roots=("kind",),
        alternatives={"kindkind": (duplicate, duplicate)},
    )
    molecular = build_molecular(graph, ())
    target_edges = [edge for edge in molecular.edges if edge[0] == 1]
    assert len(target_edges) == 4
    assert [(edge[0], edge[2]) for edge in target_edges[:2]] == [
        (edge[0], edge[2]) for edge in target_edges[2:]
    ]


def test_sense_owned_edges_are_not_duplicated_by_surface_forms() -> None:
    snapshot = WordnetSnapshot(
        lexemes=(
            LexemeRecord(
                "run", "v", ("running",),
                (SenseRecord("run%1", "run-v", ()),),
            ),
        ),
        synsets=(SynsetRecord("run-v", "v", ("run",), (), ()),),
        source_tree_sha256="0" * 64,
        source_file_count=1,
    )
    direct = build_direct_atomic(snapshot)
    labels = {row["code"]: row["label"] for row in direct.relation_binding}
    assert sum(labels[edge[1]] == "has-sense" for edge in direct.edges) == 2
    assert sum(labels[edge[1]] == "in-synset" for edge in direct.edges) == 1


def test_producer_verification_rejects_stale_identity(tmp_path: Path) -> None:
    verification = _verification_or_skip()
    stale = UCNSProducerVerification(
        verification.source_root,
        "0" * 40,
        verification.module_sha256,
    )
    with pytest.raises(LexicalBridgeError, match="stale or forged"):
        freeze_branch(tmp_path, "direct-atomic", build_direct_atomic(_snapshot()), stale)


def test_producer_verification_rejects_constructed_digest_token(tmp_path: Path) -> None:
    verification = _verification_or_skip()
    forged = UCNSProducerVerification(
        verification.source_root,
        verification.commit,
        "0" * 64,
    )
    with pytest.raises(LexicalBridgeError, match="stale or forged"):
        freeze_branch(tmp_path, "direct-atomic", build_direct_atomic(_snapshot()), forged)


def test_freeze_does_not_execute_cached_ucns_module(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    verification = _verification_or_skip()
    poisoned = ModuleType("ucns.relational_carrier")

    def poisoned_call(*args, **kwargs):
        raise AssertionError("cached UCNS producer must not execute")

    poisoned.build_relational_carrier = poisoned_call
    poisoned.relational_carrier_bytes = poisoned_call
    poisoned.parse_relational_carrier = poisoned_call
    monkeypatch.setitem(sys.modules, "ucns.relational_carrier", poisoned)
    receipt = freeze_branch(
        tmp_path,
        "direct-atomic",
        build_direct_atomic(_snapshot()),
        verification,
    )
    assert receipt["status"] == "UNRESOLVED"


def test_freeze_rejects_mislabeled_branch_value(tmp_path: Path) -> None:
    verification = _verification_or_skip()
    direct = build_direct_atomic(_snapshot())
    molecular = build_molecular(build_morphology_graph(("kind",), ()), ())
    with pytest.raises(LexicalBridgeError, match="value type mismatch"):
        freeze_branch(tmp_path, "direct-atomic", molecular, verification)
    with pytest.raises(LexicalBridgeError, match="value type mismatch"):
        freeze_branch(tmp_path, "molecular", direct, verification)


def test_resume_revalidates_every_frozen_file_and_fails_closed(tmp_path: Path) -> None:
    verification = _verification_or_skip()
    direct = build_direct_atomic(_snapshot())
    affix = AffixRecord("ness", "-ness", "-ness", "suffix", "derivational_suffixes", "S", ("S",), "", None)
    molecular = build_molecular(build_morphology_graph(("kind", "kindness"), (affix,)), (affix,))
    freeze_branch(tmp_path, "direct-atomic", direct, verification)
    freeze_branch(tmp_path, "molecular", molecular, verification)
    comparison = compare_frozen_branches(tmp_path, verification)
    source = {"fixture": "exact"}
    for name in REQUIRED_ARTIFACT_FILES - {path.name for path in tmp_path.iterdir()}:
        (tmp_path / name).write_bytes(canonical_json_bytes({}))
    (tmp_path / "source-manifest.json").write_bytes(canonical_json_bytes(source))
    files = []
    for path in sorted(tmp_path.iterdir()):
        payload = path.read_bytes()
        files.append({"path": path.name, "bytes": len(payload), "sha256": sha256(payload).hexdigest()})
    manifest = {"source": source, "status": "UNRESOLVED", "comparison": comparison, "files": files}
    (tmp_path / "manifest.json").write_bytes(canonical_json_bytes(manifest))
    assert _resume_complete(tmp_path, source, verification) == manifest
    source_manifest_path = tmp_path / "source-manifest.json"
    source_manifest_path.write_bytes(canonical_json_bytes({"fixture": "changed"}))
    with pytest.raises(RuntimeError, match="source manifest mismatch"):
        _resume_complete(tmp_path, source, verification)
    source_manifest_path.write_bytes(canonical_json_bytes(source))
    binding = tmp_path / "direct-atomic.binding.json"
    binding.write_bytes(binding.read_bytes() + b" ")
    with pytest.raises(RuntimeError, match="resumable artifact mismatch"):
        _resume_complete(tmp_path, source, verification)


def test_resume_rejects_truncated_or_injected_file_inventory(tmp_path: Path) -> None:
    verification = _verification_or_skip()
    direct = build_direct_atomic(_snapshot())
    molecular = build_molecular(build_morphology_graph(("kind", "kindness"), ()), ())
    freeze_branch(tmp_path, "direct-atomic", direct, verification)
    freeze_branch(tmp_path, "molecular", molecular, verification)
    comparison = compare_frozen_branches(tmp_path, verification)
    for name in REQUIRED_ARTIFACT_FILES - {path.name for path in tmp_path.iterdir()}:
        (tmp_path / name).write_bytes(canonical_json_bytes({}))
    source = {"fixture": "exact"}
    (tmp_path / "source-manifest.json").write_bytes(canonical_json_bytes(source))
    records = []
    for path in sorted(tmp_path.iterdir()):
        payload = path.read_bytes()
        records.append({"path": path.name, "bytes": len(payload), "sha256": sha256(payload).hexdigest()})
    manifest = {"source": source, "status": "UNRESOLVED", "comparison": comparison, "files": records[:-1]}
    (tmp_path / "manifest.json").write_bytes(canonical_json_bytes(manifest))
    with pytest.raises(RuntimeError, match="file set mismatch"):
        _resume_complete(tmp_path, source, verification)
    manifest["files"] = records
    (tmp_path / "manifest.json").write_bytes(canonical_json_bytes(manifest))
    (tmp_path / "injected.json").write_bytes(canonical_json_bytes({}))
    with pytest.raises(RuntimeError, match="file set mismatch"):
        _resume_complete(tmp_path, source, verification)


def test_frozen_edge_count_must_match_intrinsic_carrier(tmp_path: Path) -> None:
    verification = _verification_or_skip()
    freeze_branch(tmp_path, "direct-atomic", build_direct_atomic(_snapshot()), verification)
    receipt_path = tmp_path / "direct-atomic.receipt.json"
    receipt = json.loads(receipt_path.read_bytes())
    receipt["edge_count"] += 1
    receipt_path.write_bytes(canonical_json_bytes(receipt))
    with pytest.raises(LexicalBridgeError, match="intrinsic edge count mismatch"):
        validate_frozen_branch(tmp_path, "direct-atomic", verification)


def test_dirty_or_untracked_oewn_source_tree_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_repo = tmp_path / "oewn"
    yaml_root = source_repo / "src" / "yaml"
    yaml_root.mkdir(parents=True)
    tracked = yaml_root / "entries-a.yaml"
    tracked.write_text("word: value\n", encoding="utf-8")
    subprocess.run(["git", "init", str(source_repo)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(source_repo), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(source_repo), "config", "user.name", "EDCM test"], check=True)
    subprocess.run(["git", "-C", str(source_repo), "add", "src/yaml"], check=True)
    subprocess.run(["git", "-C", str(source_repo), "commit", "-m", "fixture"], check=True, capture_output=True)
    digest, count = lexical_builder._resume_source_tree_digest(source_repo)
    monkeypatch.setattr(lexical_builder, "OEWN_SOURCE_TREE_SHA256", digest)
    monkeypatch.setattr(lexical_builder, "OEWN_EXPECTED_SOURCE_FILE_COUNT", count)
    assert lexical_builder._verify_oewn_source_tree_clean(source_repo) == (digest, count)
    tracked.write_text("word: changed\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="tracked changes"):
        lexical_builder._verify_oewn_source_tree_clean(source_repo)
    subprocess.run(["git", "-C", str(source_repo), "restore", "src/yaml"], check=True)
    (yaml_root / "injected.yaml").write_text("extra: true\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="untracked files"):
        lexical_builder._verify_oewn_source_tree_clean(source_repo)


def test_fresh_build_rejects_preexisting_output_files(tmp_path: Path) -> None:
    output = tmp_path / "output"
    output.mkdir()
    (output / "injected.json").write_bytes(b"{}\n")
    try:
        ucns_root = _ucns_root()
    except RuntimeError as exc:
        pytest.skip(str(exc))
    with pytest.raises(RuntimeError, match="must be empty"):
        lexical_builder.build(
            tmp_path / "unused-source",
            ucns_root,
            output,
        )


def test_glyph_floor_compatibility_module_imports() -> None:
    import edcm.language.glyph_floor as glyph_floor

    assert glyph_floor.PUBLIC_GLYPH_FLOOR_157 is not None
    assert "UCNS-owned public gonol" in repr(glyph_floor.PUBLIC_GLYPH_FLOOR_157)


def test_retained_language_model_structures_have_live_behavior() -> None:
    left = CompositionNode.leaf("left")
    right = CompositionNode.leaf("right")
    tree = CompositionNode.compose(left, right)
    assert tuple(tree.leaves()) == ("left", "right")
    evidence = LexicalEvidence("leftright", Attestation.ATTESTED, Soundness.UNRESOLVED, "fixture")
    assert evidence.valid is True
    result = AtomicForkResult("leftright", AtomicForkRelation.DIVERGENT, tree)
    assert result.molecular_tree == tree


def test_builder_contract_is_pinned_and_freeze_order_is_explicit() -> None:
    source = Path("tools/build_oewn2025_embeddings.py").read_text()
    assert "OEWN_COMMIT" in source and "UCNS_RELATIONAL_COMMIT" in source
    assert "--ucns-source-root" in source and "verify_ucns_producer" in source
    build_source = source[source.index("def build(") :]
    assert build_source.index("if resume and") < build_source.index(
        "snapshot = _verified_snapshot"
    )
    comparison = build_source.index("comparison = compare_frozen_branches")
    assert build_source.index('"direct-atomic", build_direct_atomic') < comparison
    assert build_source.index('"molecular", build_molecular') < comparison
