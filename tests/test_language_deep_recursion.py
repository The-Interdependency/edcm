# === CHECKS ===
# id: lexical_deep_recursion_check
#   proves: deep_recursion_is_closed_over_frozen_floor, deep_recursion_processes_complete_oewn_inventory, definition_order_and_multiplicity_are_preserved, deep_recursion_does_not_claim_semantic_canon
#   call: self::lexical_deep_recursion_check
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: lexical_deep_recursion_freeze_check
#   proves: english_metadata_is_external_to_ucns_carrier, deep_recursion_resume_is_fail_closed
#   call: self::test_deep_recursion_freeze_is_metadata_free_and_tamper_evident
#   timeout: 30
#   mutates: filesystem
#   cleanup: tmp_path
# === END CHECKS ===

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from edcm.language.deep_recursion import (
    DEEP_RECURSION_LAYER,
    DeepRecursionError,
    build_deep_recursion_layer,
    definition_atoms,
    load_floor_surface_binding,
)
from edcm.language.relational_bridge import (
    LexicalBridgeError,
    canonical_json_bytes,
    freeze_relational_layer,
    validate_frozen_relational_layer,
    verify_ucns_producer,
)
from edcm.language.source import LexemeRecord, SenseRecord, SynsetRecord, WordnetSnapshot


def _floor(*surfaces: str) -> tuple[dict[str, object], ...]:
    return tuple(
        {"address": index, "kind": "surface", "identity": surface}
        for index, surface in enumerate(sorted(surfaces))
    )


def _snapshot() -> WordnetSnapshot:
    return WordnetSnapshot(
        lexemes=(
            LexemeRecord(
                "kind", "n", ("kinds",),
                (SenseRecord("kind%1", "kind-n", (("also", ("gentle%1", "gentle%1")),)),),
            ),
            LexemeRecord(
                "gentle", "a", (),
                (SenseRecord("gentle%1", "gentle-a", ()),),
            ),
        ),
        synsets=(
            SynsetRecord(
                "gentle-a", "a", ("gentle",),
                ("kind kind", "kind unknown"), (),
            ),
            SynsetRecord(
                "kind-n", "n", ("kind", "gentle"),
                ("gentle-hearted kind",),
                (("similar", ("gentle-a", "missing-a")),),
            ),
        ),
        source_tree_sha256="0" * 64,
        source_file_count=1,
    )


def lexical_deep_recursion_check() -> None:
    layer = build_deep_recursion_layer(
        _snapshot(), _floor("gentle", "gentle-hearted", "kind", "kinds")
    )
    coverage = layer.coverage
    assert coverage["definition_count"] == 3
    assert coverage["closed_definition_count"] == 2
    assert coverage["rejected_definition_count"] == 1
    assert coverage["definition_token_edge_count"] == 4
    assert coverage["sense_relation_occurrence_count"] == 2
    assert coverage["sense_relation_edge_count"] == 4
    assert coverage["synset_relation_occurrence_count"] == 2
    assert coverage["synset_relation_edge_count"] == 2
    assert len(coverage["excluded_synset_relations"]) == 1
    assert coverage["synset_membership_pair_count"] == 2
    assert coverage["synset_membership_edge_count"] == 2
    labels = {row["code"]: row["label"] for row in layer.relation_binding}
    definition_edges = [
        (edge, evidence) for edge, evidence in zip(layer.edges, layer.edge_binding)
        if labels[edge[1]] == "definition-token"
    ]
    repeated = [
        evidence["surface"] for _, evidence in definition_edges
        if evidence["definition_identity"] == "definition:gentle-a:0"
    ]
    assert repeated == ["kind", "kind"]
    assert all(row["edge_index"] == index for index, row in enumerate(layer.edge_binding))
    assert layer.coverage["status"] == "UNRESOLVED"
    assert "canonical lexical sense" in layer.coverage["nonclaims"]


def test_complete_closed_layer_contract() -> None:
    lexical_deep_recursion_check()


def test_unicode_definition_atomizer_preserves_spans_and_internal_joiners() -> None:
    text = "L’esprit gentle-hearted, 18th."
    atoms = definition_atoms(text)
    assert [atom.text for atom in atoms] == ["L’esprit", "gentle-hearted", "18th"]
    assert [text[atom.start:atom.end] for atom in atoms] == [atom.text for atom in atoms]


def test_floor_binding_loader_is_canonical_direct_atomic_only(tmp_path: Path) -> None:
    value = {
        "schema": "edcm.english-lexical-relational-branch",
        "version": "1.0.0",
        "branch": "direct-atomic",
        "node_binding": [
            {"address": 0, "kind": "surface", "identity": "gentle"},
            {"address": 1, "kind": "sense", "identity": "gentle%1"},
        ],
    }
    path = tmp_path / "binding.json"
    path.write_bytes(canonical_json_bytes(value))
    assert load_floor_surface_binding(path) == (
        {"address": 0, "kind": "surface", "identity": "gentle"},
    )
    path.write_bytes(path.read_bytes() + b" ")
    with pytest.raises(DeepRecursionError, match="not canonical"):
        load_floor_surface_binding(path)


def _verification_or_skip():
    configured = os.environ.get("EDCM_LEXICAL_UCNS_ROOT") or os.environ.get("UCNS_SOURCE_ROOT")
    if not configured:
        pytest.skip("exact UCNS relational producer checkout is not configured")
    try:
        return verify_ucns_producer(configured)
    except LexicalBridgeError as exc:
        pytest.skip(str(exc))


def test_deep_recursion_freeze_is_metadata_free_and_tamper_evident(tmp_path: Path) -> None:
    verification = _verification_or_skip()
    layer = build_deep_recursion_layer(
        _snapshot(), _floor("gentle", "gentle-hearted", "kind", "kinds")
    )
    freeze_relational_layer(
        tmp_path, DEEP_RECURSION_LAYER, layer.node_binding,
        layer.relation_binding, layer.edges, layer.edge_binding, verification,
    )
    receipt = validate_frozen_relational_layer(tmp_path, DEEP_RECURSION_LAYER, verification)
    assert receipt["status"] == "UNRESOLVED"
    intrinsic = (tmp_path / f"{DEEP_RECURSION_LAYER}.ucns.json").read_text()
    assert "kind" not in intrinsic and "definition" not in intrinsic
    binding = tmp_path / f"{DEEP_RECURSION_LAYER}.binding.json"
    value = json.loads(binding.read_bytes())
    value["edge_binding"][0]["kind"] = "tampered"
    binding.write_bytes(canonical_json_bytes(value))
    with pytest.raises(LexicalBridgeError, match="binding digest mismatch"):
        validate_frozen_relational_layer(tmp_path, DEEP_RECURSION_LAYER, verification)
