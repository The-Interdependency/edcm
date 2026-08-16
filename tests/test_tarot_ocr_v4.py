# === CHECKS ===
# id: check_tarot_ocr_v4_identity_and_resume
#   proves: tarot_ocr_v4_verifies_every_frozen_identity, tarot_ocr_v4_resume_fails_closed
#   call: self::test_frozen_identity_constants_and_record_verification
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_tarot_ocr_v4_raw_evidence
#   proves: tarot_ocr_v4_preserves_raw_page_evidence
#   call: self::test_record_preserves_hashes_confidence_and_page_identity
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_tarot_ocr_v4_accuracy
#   proves: tarot_ocr_v4_applies_frozen_accuracy_rule
#   call: self::test_normalization_distance_and_empty_page_rule
#   mutates: none
#   cleanup: none
#
# id: check_tarot_ocr_v4_determinism
#   proves: tarot_ocr_v4_serialization_is_deterministic
#   call: self::test_canonical_serialization_is_byte_deterministic
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from tools.run_tarot_ocr_v4 import (
    MODEL_SHA256,
    MUTOOL_SHA256,
    REFERENCE_SHA256,
    TESSERACT_SHA256,
    SOURCES,
    canonical_bytes,
    levenshtein,
    normalize,
    record_for,
    score,
    verify_record,
)


def test_frozen_identity_constants_and_record_verification(tmp_path: Path) -> None:
    assert len({MUTOOL_SHA256, TESSERACT_SHA256, MODEL_SHA256, REFERENCE_SHA256}) == 4
    source = SOURCES[0]
    root = tmp_path / "run"
    base = root / "raw" / source.source_id / "page-0001"
    base.parent.mkdir(parents=True)
    base.with_suffix(".png").write_bytes(b"png")
    base.with_suffix(".txt").write_text("texte\n", encoding="utf-8")
    base.with_suffix(".tsv").write_text(
        "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n"
        "5\t1\t1\t1\t1\t1\t0\t0\t5\t5\t92.5\ttexte\n",
        encoding="utf-8",
    )
    record = record_for(source, 1, base.with_suffix(".png"), base.with_suffix(".txt"), base.with_suffix(".tsv"))
    assert verify_record(root, source, record)
    base.with_suffix(".txt").write_text("changed", encoding="utf-8")
    assert not verify_record(root, source, record)


def test_record_preserves_hashes_confidence_and_page_identity(tmp_path: Path) -> None:
    source = SOURCES[1]
    files = [tmp_path / f"page-0002.{suffix}" for suffix in ("png", "txt", "tsv")]
    files[0].write_bytes(b"image")
    files[1].write_text("mot", encoding="utf-8")
    files[2].write_text(
        "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n"
        "5\t1\t1\t1\t1\t1\t1\t2\t3\t4\t87.125\tmot\n",
        encoding="utf-8",
    )
    record = record_for(source, 2, *files)
    assert record["source_id"] == source.source_id
    assert record["page"] == 2
    assert record["png"]["sha256"] == sha256(b"image").hexdigest()
    assert record["tsv"]["word_confidences"] == ["87.125"]


def test_normalization_distance_and_empty_page_rule() -> None:
    assert normalize("  é  mot\r\n\r\n") == "é mot"
    assert levenshtein("abc", "adc") == 1
    assert score("", "") == {"reference_characters": 0, "candidate_characters": 0, "exact_empty": True}
    assert score("", "hallucination")["exact_empty"] is False
    assert score("abc", "adc")["cer"] == 1 / 3


def test_canonical_serialization_is_byte_deterministic() -> None:
    assert canonical_bytes({"b": 1, "a": "é"}) == canonical_bytes({"a": "é", "b": 1})
    assert canonical_bytes({"b": 1, "a": "é"}) == b'{"a":"\xc3\xa9","b":1}\n'
