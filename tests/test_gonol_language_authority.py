from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIVE_SURFACES = (
    ROOT / "CANON.md",
    ROOT / "README.md",
    ROOT / "CLAUDE.md",
    ROOT / "AGENTS.md",
    ROOT / "docs" / "GONOL_LANGUAGE_BOUNDARY.md",
)


def _compact(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_live_surfaces_route_gonol_authority_consistently() -> None:
    boundary = _compact(ROOT / "docs" / "GONOL_LANGUAGE_BOUNDARY.md")
    canon = _compact(ROOT / "CANON.md")
    agents = _compact(ROOT / "AGENTS.md")

    for text in (boundary, canon, agents):
        assert "every admitted character is a gonol" in text
        assert "METAPAT" in text
        assert "UCNS" in text
        assert "EDCM" in text

    assert "METAPAT defines affixiation" in boundary
    assert "UCNS owns any exact geometric realization" in boundary
    assert "EDCM applies affixiation to text-domain gonols" in boundary
    for text in (boundary, canon, agents):
        assert "characters" in text and "words" in text
    assert "This order is load-bearing" in boundary
    assert "edcm.character_word" in boundary
    assert "edcm.definition_gonol" in boundary
    assert "edcm.recursive_gonol" in boundary
    assert "Morphology is not a required stage" in boundary


def test_live_surfaces_do_not_restore_ucns_language_ownership() -> None:
    forbidden = (
        "UCNS owns the gonol construction",
        "UCNS lexical construction remains upstream",
        "UCNS owns lexical/gonol construction surfaces",
        "EDCM owns neither lexical-floor membership nor UCNS character-, word-, or definition-gonol construction",
        "UCNS has authorized a Scrabble dictionary as the replacement lexical source class",
    )
    for path in LIVE_SURFACES:
        text = _compact(path)
        for phrase in forbidden:
            assert phrase not in text, f"stale authority in {path.relative_to(ROOT)}: {phrase}"


def test_unresolved_ucns_operations_remain_hmmm_not_semantics() -> None:
    boundary = _compact(ROOT / "docs" / "GONOL_LANGUAGE_BOUNDARY.md")
    assert "Unicode names, dictionary definitions" in boundary
    assert "An unresolved operation remains `hmmm`" in boundary
    assert "invented carrier" in boundary


def test_measurement_does_not_activate_from_construction() -> None:
    canon = _compact(ROOT / "CANON.md")
    boundary = _compact(ROOT / "docs" / "GONOL_LANGUAGE_BOUNDARY.md")
    assert "EDCM construction does not validate EDCM measurement" in boundary
    assert "EDCM construction and EDCM measurement remain separate" in canon
