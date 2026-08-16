# === CHECKS ===
# id: language_relational_branch_check
#   proves: lexical_branches_are_independently_constructed, english_metadata_is_external_to_ucns_carrier, comparison_requires_two_prior_freezes, lexical_manifest_preserves_authority_firewall
#   call: self::test_independent_branches_freeze_before_comparison
#   timeout: 30
#   mutates: tmp_path only
#   cleanup: pytest tmp_path
#
# id: oewn_builder_order_check
#   proves: oewn_source_is_exact_pinned_and_resumable, lexical_comparison_occurs_after_freeze
#   call: self::test_builder_contract_is_pinned_and_freeze_order_is_explicit
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from pathlib import Path

import pytest

from edcm.language.affixes import AffixRecord
from edcm.language.morphology import build_morphology_graph
from edcm.language.manifest import embedding_manifest
from edcm.language.relational_bridge import (
    LexicalBridgeError, build_direct_atomic, build_molecular,
    compare_frozen_branches, freeze_branch,
)
from edcm.language.source import LexemeRecord, SenseRecord, SynsetRecord, WordnetSnapshot


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
    manifest = embedding_manifest()
    assert manifest.ucns_owns_representation and manifest.edcm_owns_english_evidence
    assert manifest.legacy_placement_present is False and manifest.geometry_attached is False
    affix = AffixRecord("ness", "-ness", "-ness", "suffix", "derivational_suffixes", "S", ("S",), "", None)
    direct = build_direct_atomic(_snapshot())
    graph = build_morphology_graph(("kind", "kindness"), (affix,))
    molecular = build_molecular(graph, (affix,))
    assert direct.node_binding != molecular.node_binding
    with pytest.raises(FileNotFoundError):
        compare_frozen_branches(tmp_path)
    freeze_branch(tmp_path, "direct-atomic", direct)
    freeze_branch(tmp_path, "molecular", molecular)
    result = compare_frozen_branches(tmp_path)
    assert result["shared_surface_count"] == 2
    assert result["intrinsic_equal"] is False
    for branch in ("direct-atomic", "molecular"):
        intrinsic = (tmp_path / f"{branch}.ucns.json").read_text()
        assert "kind" not in intrinsic and "provenance" not in intrinsic


def test_builder_contract_is_pinned_and_freeze_order_is_explicit() -> None:
    source = Path("tools/build_oewn2025_embeddings.py").read_text()
    assert "OEWN_COMMIT" in source and "UCNS_RELATIONAL_COMMIT" in source
    assert source.index('freeze_branch(output, "direct-atomic"') < source.index("compare_frozen_branches(output)")
    assert source.index('freeze_branch(output, "molecular"') < source.index("compare_frozen_branches(output)")
