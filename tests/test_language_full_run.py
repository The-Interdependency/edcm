from __future__ import annotations

from dataclasses import replace

import pytest

from edcm.language.affixes import AffixRecord, load_affix_inventory
from edcm.language.morphology import build_morphology_graph
from edcm.language.placement import (
    NonCanonicalLanguagePlacementError,
    assign_affix_gonol,
    assign_direct_atomic_gonol,
    assign_root_gonol,
    superpose_gonols,
)
from edcm.language.rendering import inverse_affix_candidates, render_affix_candidates
from tools.build_oewn2025_embeddings import main as build_oewn_main


def _find_affix(surface: str, primary: str | None = None) -> AffixRecord:
    matches = [record for record in load_affix_inventory() if record.surface == surface]
    if primary is not None:
        matches = [record for record in matches if record.primary == primary]
    assert matches
    return matches[0]


def test_every_affix_is_universally_applicable_and_variants_are_materialized() -> None:
    inventory = load_affix_inventory()
    assert inventory
    assert all(record.universally_applicable for record in inventory)
    assert any(record.surface == "il-" and record.variant_of for record in inventory)
    assert len([record for record in inventory if record.surface == "-s"]) >= 2


def test_rendering_preserves_literal_and_conventional_surfaces() -> None:
    ness = _find_affix("-ness")
    assert "happyness" in render_affix_candidates("happy", ness)
    assert "happiness" in render_affix_candidates("happy", ness)
    assert "happy" in inverse_affix_candidates("happiness", ness)

    ing = _find_affix("-ing")
    assert "running" in render_affix_candidates("run", ing)
    assert "run" in inverse_affix_candidates("running", ing)


def test_ilproperlies_is_a_retained_morphology_reading_without_gonol_placement() -> None:
    il = _find_affix("il-")
    ly = _find_affix("-ly")
    es = _find_affix("-es")
    surfaces = {"proper", "ilproper", "ilproperly", "ilproperlies"}
    graph = build_morphology_graph(surfaces, (il, ly, es))
    assert graph.immediate("ilproperlies")
    assert graph.primary_tree("ilproperlies")


def test_complete_graph_preserves_multiple_affix_readings() -> None:
    agent_er = _find_affix("-er", "S")
    comparative_er = replace(agent_er, affix_id="comparative-er", primary="K")
    graph = build_morphology_graph({"fast", "faster"}, (agent_er, comparative_er))
    assert len(graph.immediate("faster")) == 2


def test_indexed_affix_candidates_match_brute_reversible_renderer() -> None:
    selected = tuple(
        _find_affix(surface)
        for surface in ("un-", "-ness", "-ing", "-s", "-es")
    )
    surfaces = {
        "happy",
        "happiness",
        "run",
        "running",
        "wolf",
        "wolves",
        "lock",
        "unlock",
    }
    graph = build_morphology_graph(surfaces, selected)
    surface_set = frozenset(surfaces)
    expected: dict[str, set[tuple[str, tuple[str, ...]]]] = {}
    for surface in surfaces:
        rows: set[tuple[str, tuple[str, ...]]] = set()
        for affix in selected:
            for base in inverse_affix_candidates(surface, affix):
                if base not in surface_set or len(base) >= len(surface):
                    continue
                affix_leaf = f"affix:{affix.affix_id}"
                surface_leaf = f"surface:{base}"
                parts = (
                    (affix_leaf, surface_leaf)
                    if affix.kind == "prefix"
                    else (surface_leaf, affix_leaf)
                )
                rows.add((affix.affix_id, parts))
        if rows:
            expected[surface] = rows
    observed = {
        surface: {(item.affix_id or "", item.parts) for item in graph.immediate(surface)}
        for surface in surfaces
        if graph.immediate(surface)
    }
    assert observed == expected


def test_all_noncanonical_language_gonol_construction_fails_closed() -> None:
    with pytest.raises(NonCanonicalLanguagePlacementError):
        assign_affix_gonol(_find_affix("un-"))
    with pytest.raises(NonCanonicalLanguagePlacementError):
        assign_root_gonol("root", ())
    with pytest.raises(NonCanonicalLanguagePlacementError):
        assign_direct_atomic_gonol("word", (), {})
    with pytest.raises(NonCanonicalLanguagePlacementError):
        superpose_gonols(())


def test_retired_oewn_builder_fails_before_reading_or_writing_corpus_data() -> None:
    with pytest.raises(NonCanonicalLanguagePlacementError):
        build_oewn_main()
