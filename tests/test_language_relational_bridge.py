# === CHECKS ===
# id: language_relational_branch_check
#   proves: lexical_branches_are_independently_constructed, english_metadata_is_external_to_ucns_carrier, lexical_ucns_producer_is_exactly_verified, lexical_relation_multiplicity_is_preserved, lexical_pre_replay_status_is_unresolved, comparison_requires_two_prior_freezes, lexical_manifest_preserves_authority_firewall
#   call: self::test_independent_branches_freeze_before_comparison
#   timeout: 30
#   mutates: tmp_path only
#   cleanup: pytest tmp_path
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
from pathlib import Path

import pytest

from edcm.language.affixes import AffixRecord
from edcm.language.morphology import Decomposition, MorphologyGraph, build_morphology_graph
from edcm.language.manifest import embedding_manifest
from edcm.language.relational_bridge import (
    LexicalBridgeError, UCNSProducerVerification, build_direct_atomic, build_molecular,
    canonical_json_bytes, compare_frozen_branches, freeze_branch,
    validate_frozen_branch, verify_ucns_producer,
)
from edcm.language.source import LexemeRecord, SenseRecord, SynsetRecord, WordnetSnapshot
from tools.build_oewn2025_embeddings import _resume_complete


UCNS_ROOT = Path(__file__).resolve().parents[2] / "ucns"


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


def test_independent_branches_freeze_before_comparison(tmp_path: Path) -> None:
    pytest.importorskip("ucns.relational_carrier")
    verification = verify_ucns_producer(UCNS_ROOT)
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


def test_producer_verification_rejects_stale_identity(tmp_path: Path) -> None:
    verification = verify_ucns_producer(UCNS_ROOT)
    stale = UCNSProducerVerification(
        verification.source_root,
        "0" * 40,
        verification.module_sha256,
    )
    with pytest.raises(LexicalBridgeError, match="commit mismatch"):
        freeze_branch(tmp_path, "direct-atomic", build_direct_atomic(_snapshot()), stale)


def test_resume_revalidates_every_frozen_file_and_fails_closed(tmp_path: Path) -> None:
    pytest.importorskip("ucns.relational_carrier")
    verification = verify_ucns_producer(UCNS_ROOT)
    direct = build_direct_atomic(_snapshot())
    affix = AffixRecord("ness", "-ness", "-ness", "suffix", "derivational_suffixes", "S", ("S",), "", None)
    molecular = build_molecular(build_morphology_graph(("kind", "kindness"), (affix,)), (affix,))
    freeze_branch(tmp_path, "direct-atomic", direct, verification)
    freeze_branch(tmp_path, "molecular", molecular, verification)
    comparison = compare_frozen_branches(tmp_path, verification)
    source = {"fixture": "exact"}
    files = []
    for path in sorted(tmp_path.iterdir()):
        payload = path.read_bytes()
        files.append({"path": path.name, "bytes": len(payload), "sha256": sha256(payload).hexdigest()})
    manifest = {"source": source, "status": "UNRESOLVED", "comparison": comparison, "files": files}
    (tmp_path / "manifest.json").write_bytes(canonical_json_bytes(manifest))
    assert _resume_complete(tmp_path, source, verification) == manifest
    binding = tmp_path / "direct-atomic.binding.json"
    binding.write_bytes(binding.read_bytes() + b" ")
    with pytest.raises(RuntimeError, match="resumable artifact mismatch"):
        _resume_complete(tmp_path, source, verification)


def test_builder_contract_is_pinned_and_freeze_order_is_explicit() -> None:
    source = Path("tools/build_oewn2025_embeddings.py").read_text()
    assert "OEWN_COMMIT" in source and "UCNS_RELATIONAL_COMMIT" in source
    assert "--ucns-source-root" in source and "verify_ucns_producer" in source
    build_source = source[source.index("def build(") :]
    comparison = build_source.index("comparison = compare_frozen_branches")
    assert build_source.index('"direct-atomic", build_direct_atomic') < comparison
    assert build_source.index('"molecular", build_molecular') < comparison
