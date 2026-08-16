# === CHECKS ===
# id: check_tarot_text_gate_frozen_thresholds
#   proves: tarot_text_gate_applies_frozen_adequacy_rule, tarot_text_gate_retains_nonclaims_and_failure
#   call: self::test_frozen_thresholds_accept_only_adequate_pages
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from tools.evaluate_tarot_pdf_text_layer import evaluate_pages


def test_frozen_thresholds_accept_only_adequate_pages() -> None:
    adequate = evaluate_pages(["a" * 100] * 5, required_pages=5, required_total=500)
    assert adequate["passed"] is True
    sparse = evaluate_pages(["a" * 100] * 4 + [""], required_pages=5, required_total=500)
    assert sparse["passed"] is False
    corrupt = evaluate_pages(["\ufffd" * 100] * 5, required_pages=5, required_total=500)
    assert corrupt["passed"] is False
