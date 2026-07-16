from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_noncanonical_hash_and_fraction_placement_cannot_reappear():
    placement = _text("edcm/language/placement.py")
    forbidden = (
        "Fraction(vertex, 157)",
        "edcm:direct-atomic:v1",
        "edcm:root-component",
        "edcm:affix-component",
        "def _glyph_vertex",
        "def _vertices",
        "def _component_gonol",
        "shake_256",
    )
    for phrase in forbidden:
        assert phrase not in placement, f"retired placement returned: {phrase!r}"


def test_edcm_contains_no_competing_public_arrangement_builder():
    glyph_floor = _text("edcm/language/glyph_floor.py")
    assert "importlib.import_module(\"ucns\")" in glyph_floor
    assert "EDCM no longer owns a public-gonol copy" in glyph_floor
    assert "PUBLIC_GONOL_SOURCE_COMMIT" in glyph_floor
    assert "PUBLIC_GONOL_157" in glyph_floor
    assert "def _build_public_glyph_floor_157" not in glyph_floor
    assert "UNPAIRED_OPS" not in glyph_floor


def test_noncanonical_oewn_artifact_workflows_are_removed():
    assert not (ROOT / ".github/workflows/build-oewn2025-embeddings.yml").exists()
    assert not (ROOT / ".github/workflows/validate-oewn-interconnectivity-now.yml").exists()
    assert not (ROOT / "tools/finalize_oewn2025_artifacts.py").exists()


def test_correction_document_pins_authority_and_reopening_boundary():
    document = _text("docs/public-gonol-canon-correction.md")
    assert "EDCM does not own the public gonol" in document
    assert "SPACE/ZERO at fixed position 0" in document
    assert "NonCanonicalLanguagePlacementError" in document
    assert "Do not silently" not in document  # use affirmative fail-closed rules below
    assert "move or normalize away the twist origin" in document
    assert "invent angle units or conversion formulas" in document
