from __future__ import annotations

from dataclasses import replace
import gzip
from hashlib import sha256
import json
from pathlib import Path

from edcm.language.affixes import AffixRecord, load_affix_inventory
from edcm.language.artifacts import intrinsic_gonol_record
from edcm.language.morphology import build_morphology_graph
from edcm.language.placement import (
    assign_affix_gonol,
    assign_direct_atomic_gonol,
    assign_root_gonol,
    compare_gonols,
    superpose_gonols,
)
from edcm.language.rendering import inverse_affix_candidates, render_affix_candidates
from edcm.language.source import LexemeRecord, SenseRecord, SynsetRecord


def _find_affix(surface: str, primary: str | None = None) -> AffixRecord:
    matches = [record for record in load_affix_inventory() if record.surface == surface]
    if primary is not None:
        matches = [record for record in matches if record.primary == primary]
    assert matches
    return matches[0]


def _lexeme(lemma: str, synset: str = "00000001-n") -> LexemeRecord:
    return LexemeRecord(
        lemma=lemma,
        part_of_speech="n",
        forms=(),
        senses=(SenseRecord(f"{lemma}%1:00:00::", synset, ()),),
    )


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


def test_ilproperlies_is_valid_and_can_remain_unsound() -> None:
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


def test_direct_atomic_and_molecular_placements_are_independent() -> None:
    lexeme = _lexeme("help")
    synset = SynsetRecord(
        synset_id="00000001-n",
        part_of_speech="n",
        members=("help", "aid"),
        definitions=("the activity of contributing",),
        relations=(("hypernym", ("00000002-n",)),),
    )
    root = assign_root_gonol("help", (lexeme,))
    direct = assign_direct_atomic_gonol("help", (lexeme,), {synset.synset_id: synset})
    comparison = compare_gonols(direct, root)
    assert not comparison["equivalent"]
    assert comparison["direct_sha256"] != comparison["generated_sha256"]


def test_alternative_superposition_retains_payloads() -> None:
    a = assign_root_gonol("lock", (_lexeme("lock"),))
    b = assign_affix_gonol(_find_affix("un-"))
    combined = superpose_gonols((a, b))
    assert len(combined.anchors_pos) == 3
    assert sum(anchor.payload is not None for anchor in combined.anchors_pos) == 2


def test_intrinsic_record_contains_no_linguistic_metadata() -> None:
    gonol = assign_root_gonol("help", (_lexeme("help"),))
    record = intrinsic_gonol_record(gonol)
    text = json.dumps(record, sort_keys=True)
    for forbidden in ("help", "surface", "attestation", "soundness", "source", "embedding"):
        assert forbidden not in text


def test_generated_artifact_manifest_when_present() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest_path = root / "artifacts" / "oewn2025" / "manifest.json"
    if not manifest_path.exists():
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["summary"]["surface_count"] > 100_000
    assert manifest["summary"]["root_count"] > 0
    for record in manifest["files"]:
        path = root / "artifacts" / record["path"]
        assert path.is_file()
        assert path.stat().st_size == record["bytes"]
        assert sha256(path.read_bytes()).hexdigest() == record["sha256"]

    pure_path = root / "artifacts" / "oewn2025" / "atomic-direct.gonols.jsonl.gz"
    with gzip.open(pure_path, "rt", encoding="utf-8") as handle:
        first = json.loads(handle.readline())
    serialized = json.dumps(first, sort_keys=True)
    assert "surface" not in serialized
    assert "source" not in serialized
