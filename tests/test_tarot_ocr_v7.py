# === CHECKS ===
# id: check_tarot_ocr_v7_renderer_repair
#   proves: tarot_ocr_v7_repairs_only_renderer_activation
#   call: self::test_v7_command_uses_explicit_renderer_flags
#   mutates: none
#   cleanup: none
#
# id: check_tarot_ocr_v7_inherited_identity
#   proves: tarot_ocr_v7_retains_v6_instrument
#   call: self::test_v7_protocol_and_model_are_frozen
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from pathlib import Path

import pytest

from tools.run_tarot_ocr_v6 import MODEL_FILENAME, MODEL_NAME, MODEL_SHA256
from tools.run_tarot_ocr_v7 import INSTRUMENT, PROTOCOL_COMMIT, PROTOCOL_SHA256, ocr_command


def test_v7_command_uses_explicit_renderer_flags(tmp_path: Path) -> None:
    model = tmp_path / MODEL_FILENAME
    command = ocr_command(Path("/usr/bin/tesseract"), Path("page.png"), Path("page"), model)
    assert command == [
        "/usr/bin/tesseract", "page.png", "page", "--tessdata-dir", str(tmp_path),
        "-l", MODEL_NAME, "--oem", "1", "--psm", "3", "-c",
        "thresholding_method=2", "-c", "tessedit_create_txt=1", "-c",
        "tessedit_create_tsv=1",
    ]
    assert "txt" not in command
    assert "tsv" not in command


def test_v7_protocol_and_model_are_frozen() -> None:
    assert PROTOCOL_COMMIT == "f57f639c02f3f975c4bd7983d3a22cdf59592a77"
    assert PROTOCOL_SHA256 == "43a1568c68ffad1052fa382b08ee8af7793cdc8ef289971707dc27aa0479eccd"
    assert INSTRUMENT["model_sha256"] == MODEL_SHA256
    assert INSTRUMENT["all_other_v6_fields"] == "unchanged"


def test_v7_passes_historic_model_as_top_level_manifest_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    from tools import run_tarot_ocr_v7 as runner

    captured: dict[str, object] = {}
    monkeypatch.setattr(runner.predecessor, "verify_model", lambda path: None)

    def fake_run(*args, **kwargs):
        captured.update(kwargs)
        return {"status": "FALSIFIED"}

    monkeypatch.setattr(runner.core, "run", fake_run)
    runner.run(Path("acquisition"), Path("reference"), Path(MODEL_FILENAME), Path("output"), False)
    assert captured["model_sha256"] == MODEL_SHA256
