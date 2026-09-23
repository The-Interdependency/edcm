"""Prevent active instructions from restoring superseded construction ownership."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE_SURFACES = tuple(ROOT / name for name in (
    "CANON.md", "README.md", "CLAUDE.md", "AGENTS.md", "docs/GONOL_LANGUAGE_BOUNDARY.md",
))


def test_live_surfaces_route_active_construction_to_stack_and_ucns():
    for path in LIVE_SURFACES:
        text = " ".join(path.read_text(encoding="utf-8").split())
        assert "| UCNS | Gonol objects, constructors, and geometry |" in text, path
        assert "| Stack | Active language-gonol construction research and source/admission profiles |" in text, path
        assert "| EDCM | Measurement/evaluation only |" in text, path
        assert "research/english-gonol" in text, path
        assert "research/python-gonol" in text, path
        assert "EDCM applies affixiation to text-domain gonols" not in text, path
        assert "edcm.gonol" in text and "historical" in text.lower(), path


def test_unknown_operations_and_evaluation_validity_stay_separate():
    text = " ".join((ROOT / "docs/GONOL_LANGUAGE_BOUNDARY.md").read_text().split())
    assert "An unresolved operation remains `hmmm`" in text
    assert "no universal mandatory adjacent-scale ladder" in text
    assert "Construction reproducibility does not validate EDCM measurement" in text
    assert "projection, information-loss account, metric, baseline, partitions" in text
