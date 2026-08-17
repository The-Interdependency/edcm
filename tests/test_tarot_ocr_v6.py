# === CHECKS ===
# id: check_tarot_ocr_v6_model_identity
#   proves: tarot_ocr_v6_verifies_historic_model
#   call: self::test_v6_model_verification_fails_closed
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_tarot_ocr_v6_single_change
#   proves: tarot_ocr_v6_changes_only_frozen_model
#   call: self::test_v6_ocr_command_is_exact_model_change
#   mutates: none
#   cleanup: none
#
# id: check_tarot_ocr_v6_core_identity
#   proves: tarot_ocr_v6_retains_v4_evidence_contracts
#   call: self::test_v6_protocol_and_instrument_identities_are_frozen
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from pathlib import Path

import pytest

from tools.run_tarot_ocr_v4 import ProtocolBlocked
from tools.run_tarot_ocr_v6 import (
    INSTRUMENT,
    MODEL_BYTES,
    MODEL_FILENAME,
    MODEL_NAME,
    MODEL_SHA256,
    PROTOCOL_COMMIT,
    PROTOCOL_SHA256,
    ocr_command,
    verify_model,
)


def test_v6_model_verification_fails_closed(tmp_path: Path) -> None:
    wrong_name = tmp_path / "wrong.traineddata"
    wrong_name.write_bytes(b"x")
    with pytest.raises(ProtocolBlocked, match="filename"):
        verify_model(wrong_name)
    right_name = tmp_path / MODEL_FILENAME
    right_name.write_bytes(b"x")
    with pytest.raises(ProtocolBlocked, match="identity"):
        verify_model(right_name)
    assert MODEL_BYTES == 3_421_140


def test_v6_ocr_command_is_exact_model_change(tmp_path: Path) -> None:
    model = tmp_path / MODEL_FILENAME
    assert ocr_command(Path("/usr/bin/tesseract"), Path("page.png"), Path("page"), model) == [
        "/usr/bin/tesseract", "page.png", "page", "--tessdata-dir", str(tmp_path),
        "-l", MODEL_NAME, "--oem", "1", "--psm", "3", "-c",
        "thresholding_method=2", "txt", "tsv",
    ]


def test_v6_protocol_and_instrument_identities_are_frozen() -> None:
    assert PROTOCOL_COMMIT == "c63ad40d71b60a1d944ad6ce21e9d7e4cf8d2a3b"
    assert PROTOCOL_SHA256 == "07c4540d4be3ab1affb30184d7eb6290361b5b470bb55ac23cc3adf64c34a216"
    assert INSTRUMENT["model_sha256"] == MODEL_SHA256
    assert INSTRUMENT["all_other_v5_fields"] == "unchanged"
