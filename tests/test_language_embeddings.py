from __future__ import annotations

import json
from fractions import Fraction

from edcm.language import (
    AtomicForkRelation,
    Attestation,
    CompositionNode,
    GonolRegistry,
    LexicalEvidence,
    PUBLIC_GLYPH_FLOOR_157,
    PUBLIC_GLYPH_FLOOR_SHA256,
    SOURCE_DICTIONARY,
    Soundness,
    compare_atomic_fork,
    embedding_manifest,
    glyph_floor_sha256,
    materialize,
    metadata_free_jsonl,
)
from edcm.language.composition import compose_gonols
from edcm.measurement.ucns.ucns_v04 import AnchorPayload, UCNSObject, unit_obj


def _leaf_gonol(position: int, face: int = 0) -> UCNSObject:
    return UCNSObject(
        n_dec=157,
        n_min=1,
        anchors_pos=(
            AnchorPayload(Fraction(0), None),
            AnchorPayload(Fraction(position, 157), None),
        ),
        faces_pos=(0, face),
    )


def _ilproperlies_fixture() -> tuple[GonolRegistry, CompositionNode]:
    registry = GonolRegistry(
        {
            "il-": _leaf_gonol(11, 1),
            "proper": _leaf_gonol(37),
            "-ly": _leaf_gonol(83),
            "-es": _leaf_gonol(149),
        }
    )
    tree = CompositionNode.compose(
        CompositionNode.leaf("il-"),
        CompositionNode.leaf("proper"),
        CompositionNode.leaf("-ly"),
        CompositionNode.leaf("-es"),
    )
    return registry, tree


def test_manifest_pins_selected_run_without_selection_restrictions() -> None:
    manifest = embedding_manifest()
    assert manifest.source_dictionary == SOURCE_DICTIONARY
    assert manifest.source_dictionary_is_exclusive is True
    assert manifest.public_glyph_floor_vertices == 157
    assert manifest.universal_composition is True
    assert manifest.affix_selection_restrictions is False
    assert manifest.direct_atomic_assignment_is_independent is True
    assert manifest.shared_superposition_count == 1
    assert manifest.scale_changes_operation is False


def test_public_glyph_floor_is_exactly_delineated_and_frozen() -> None:
    assert len(PUBLIC_GLYPH_FLOOR_157) == 157
    assert len(set(PUBLIC_GLYPH_FLOOR_157)) == 157
    assert PUBLIC_GLYPH_FLOOR_157[0] == " "
    assert glyph_floor_sha256(PUBLIC_GLYPH_FLOOR_157) == PUBLIC_GLYPH_FLOOR_SHA256


def test_ilproperlies_is_valid_and_currently_unsound() -> None:
    evidence = LexicalEvidence(
        surface="ilproperlies",
        attestation=Attestation.UNATTESTED,
        soundness=Soundness.UNSOUND,
        source_dictionary=SOURCE_DICTIONARY,
    )
    assert evidence.valid is True


def test_every_declared_affix_and_root_can_enter_the_same_composer() -> None:
    registry, tree = _ilproperlies_fixture()
    generated = materialize(tree, registry)
    assert isinstance(generated, UCNSObject)
    assert tuple(tree.leaves()) == ("il-", "proper", "-ly", "-es")


def test_singleton_composition_preserves_identity_without_unit_copy() -> None:
    gonol = _leaf_gonol(17, 1)
    assert compose_gonols((gonol,)) is gonol
    assert compose_gonols(()).equivalent(unit_obj())


def test_grouping_is_preserved_even_when_current_ucns_product_is_associative() -> None:
    registry = GonolRegistry({"a": _leaf_gonol(2), "b": _leaf_gonol(3), "c": _leaf_gonol(5)})
    left = CompositionNode.compose(
        CompositionNode.compose(CompositionNode.leaf("a"), CompositionNode.leaf("b")),
        CompositionNode.leaf("c"),
    )
    right = CompositionNode.compose(
        CompositionNode.leaf("a"),
        CompositionNode.compose(CompositionNode.leaf("b"), CompositionNode.leaf("c")),
    )
    assert left != right
    assert tuple(left.leaves()) == tuple(right.leaves())
    assert materialize(left, registry).equivalent(materialize(right, registry))


def test_direct_and_generated_atomic_gonols_form_a_real_fork() -> None:
    molecular_registry, tree = _ilproperlies_fixture()
    direct_registry = GonolRegistry({"ilproperlies": _leaf_gonol(7)})
    result = compare_atomic_fork(
        "ilproperlies",
        tree,
        molecular_registry,
        direct_registry,
    )
    assert result.relation is AtomicForkRelation.DIVERGENT


def test_lazy_generated_atomic_cache_is_not_a_fork_when_identity_is_preserved() -> None:
    molecular_registry, tree = _ilproperlies_fixture()
    generated = materialize(tree, molecular_registry)
    direct_registry = GonolRegistry({"ilproperlies": generated})
    result = compare_atomic_fork(
        "ilproperlies",
        tree,
        molecular_registry,
        direct_registry,
    )
    assert result.relation is AtomicForkRelation.EQUIVALENT


def test_metadata_free_gonol_list_contains_only_intrinsic_fields() -> None:
    registry, tree = _ilproperlies_fixture()
    encoded = metadata_free_jsonl([materialize(tree, registry)])
    record = json.loads(encoded)
    assert set(record) == {"n_dec", "n_min", "anchors", "faces"}
    forbidden = (
        "ilproperlies",
        "word",
        "label",
        "dictionary",
        "attestation",
        "soundness",
        "atomic",
        "molecular",
        "provenance",
    )
    assert all(term not in encoded for term in forbidden)
