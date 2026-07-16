from __future__ import annotations

import importlib.util
import json
from fractions import Fraction

import pytest

from edcm.language import (
    AtomicForkRelation,
    Attestation,
    CompositionNode,
    GonolRegistry,
    LexicalEvidence,
    NonCanonicalLanguagePlacementError,
    PUBLIC_GLYPH_FLOOR_157,
    SOURCE_DICTIONARY,
    Soundness,
    UCNSPublicGonolDependencyError,
    assign_affix_gonol,
    assign_direct_atomic_gonol,
    assign_root_gonol,
    build_public_glyph_floor_157,
    compare_atomic_fork,
    embedding_manifest,
    materialize,
    metadata_free_jsonl,
    superpose_gonols,
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


def test_manifest_retires_noncanonical_placement_and_names_ucns_authority() -> None:
    manifest = embedding_manifest()
    assert manifest.source_dictionary == SOURCE_DICTIONARY
    assert manifest.source_dictionary_is_exclusive is True
    assert "The-Interdependency/ucns@" in manifest.public_glyph_floor_source
    assert manifest.canonical_public_gonol_required is True
    assert manifest.edcm_owns_public_gonol is False
    assert manifest.legacy_hash_placement_retired is True
    assert manifest.universal_composition is False
    assert manifest.direct_atomic_assignment_is_independent is False
    assert manifest.molecular_results_generate_atomic_views is False
    assert manifest.shared_superposition_count == 0


def test_public_gonol_is_lazy_and_requires_canonical_ucns() -> None:
    assert "UCNS-owned public gonol" in repr(PUBLIC_GLYPH_FLOOR_157)
    if importlib.util.find_spec("ucns") is None:
        with pytest.raises(UCNSPublicGonolDependencyError):
            build_public_glyph_floor_157()
    else:
        import ucns

        assert build_public_glyph_floor_157() == tuple(ucns.PUBLIC_GONOL_157)


def test_ilproperlies_remains_structurally_valid_and_currently_unsound() -> None:
    evidence = LexicalEvidence(
        surface="ilproperlies",
        attestation=Attestation.UNATTESTED,
        soundness=Soundness.UNSOUND,
        source_dictionary=SOURCE_DICTIONARY,
    )
    assert evidence.valid is True


def test_existing_local_composition_helpers_remain_read_only_compatible() -> None:
    registry, tree = _ilproperlies_fixture()
    generated = materialize(tree, registry)
    assert isinstance(generated, UCNSObject)
    assert tuple(tree.leaves()) == ("il-", "proper", "-ly", "-es")


def test_singleton_composition_preserves_identity_without_unit_copy() -> None:
    gonol = _leaf_gonol(17, 1)
    assert compose_gonols((gonol,)) is gonol
    assert compose_gonols(()).equivalent(unit_obj())


def test_existing_direct_generated_comparison_remains_an_inspection_surface() -> None:
    molecular_registry, tree = _ilproperlies_fixture()
    direct_registry = GonolRegistry({"ilproperlies": _leaf_gonol(7)})
    result = compare_atomic_fork(
        "ilproperlies",
        tree,
        molecular_registry,
        direct_registry,
    )
    assert result.relation is AtomicForkRelation.DIVERGENT
    assert result.molecular_tree is tree


def test_new_language_gonol_placement_fails_closed() -> None:
    with pytest.raises(NonCanonicalLanguagePlacementError):
        assign_affix_gonol(None)
    with pytest.raises(NonCanonicalLanguagePlacementError):
        assign_root_gonol("word", ())
    with pytest.raises(NonCanonicalLanguagePlacementError):
        assign_direct_atomic_gonol("word", (), {})
    with pytest.raises(NonCanonicalLanguagePlacementError):
        superpose_gonols((_leaf_gonol(1), _leaf_gonol(2)))


def test_metadata_free_compatibility_record_contains_only_intrinsic_fields() -> None:
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
