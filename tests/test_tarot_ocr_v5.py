# === CHECKS ===
# id: check_tarot_ocr_v5_single_change
#   proves: tarot_ocr_v5_changes_only_frozen_thresholding
#   call: self::test_v5_ocr_command_is_exact_single_threshold_change
#   mutates: none
#   cleanup: none
#
# id: check_tarot_ocr_v5_core_identity
#   proves: tarot_ocr_v5_retains_v4_evidence_contracts
#   call: self::test_v5_protocol_and_instrument_identities_are_frozen
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from pathlib import Path
import sys

from tools.run_tarot_ocr_v5 import INSTRUMENT, PROTOCOL_COMMIT, PROTOCOL_SHA256, ocr_command


def test_v5_usage_command_loads_as_a_direct_script() -> None:
    import subprocess

    result = subprocess.run(
        [sys.executable, "tools/run_tarot_ocr_v5.py", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "--acquisition" in result.stdout


def test_v5_ocr_command_is_exact_single_threshold_change() -> None:
    assert ocr_command(Path("/usr/bin/tesseract"), Path("page.png"), Path("page")) == [
        "/usr/bin/tesseract", "page.png", "page", "-l", "fra", "--oem", "1",
        "--psm", "3", "-c", "thresholding_method=2", "txt", "tsv",
    ]


def test_v5_protocol_and_instrument_identities_are_frozen() -> None:
    assert PROTOCOL_COMMIT == "9199f2dc3830bab11486c359b5e1f9e9974b36fb"
    assert PROTOCOL_SHA256 == "625acfea972dfe882afd4742db3608cf67f7828d898b6725678e19b2b586661c"
    assert INSTRUMENT == {
        "thresholding_method": "2",
        "thresholding_name": "Sauvola",
        "thresholding_window_size": "0.33",
        "thresholding_kfactor": "0.34",
        "all_other_v4_fields": "unchanged",
    }
