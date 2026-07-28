"""Contract checks for the MultiWOZ 2.1 full-corpus runner."""

from __future__ import annotations

# === CHECKS ===
# id: check_multiwoz21_admission_precedes_execution
#   proves: multiwoz21_admission_precedes_execution
#   call: self::test_archive_mutation_fails_before_dialogue_observation
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_multiwoz21_every_turn_is_observed_exactly_once
#   proves: multiwoz21_every_turn_is_observed_exactly_once
#   call: self::test_full_fixture_run_preserves_order_exact_text_and_profile_counts
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_multiwoz21_completion_requires_reconciliation
#   proves: multiwoz21_completion_requires_reconciliation
#   call: self::test_manifest_count_mismatch_refuses_completion
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_multiwoz21_failure_is_receipted
#   proves: multiwoz21_failure_is_receipted
#   call: self::test_invalid_turn_reports_exact_active_source_position
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_multiwoz21_written_outputs_exclude_raw_text
#   proves: multiwoz21_written_outputs_exclude_raw_text
#   call: self::test_report_and_checkpoint_exclude_source_turn_text
#   mutates: filesystem
#   cleanup: tempdir_teardown
# === END CHECKS ===

import io
import json
from hashlib import sha256
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from edcm.corpora.multiwoz21 import (
    AdmissionManifest,
    CorpusRunError,
    iter_top_level_object,
    run_archive,
)
from edcm.ucns_adapter import ActualUCNSAdapter, PINNED_UCNS_COMMIT


class FixtureAdapter:
    """Small exact-shape adapter used only to exercise corpus accounting."""

    def normalize(self, payload: dict[str, Any]) -> dict[str, Any]:
        records = []
        for turn_index, (speaker_id, text) in enumerate(payload["ucns_turns"]):
            segments = []
            word = []

            def close_word() -> None:
                if not word:
                    return
                segments.append(
                    {
                        "kind": "word-gonol",
                        "tokens": tuple(word),
                    }
                )
                word.clear()

            out_of_alphabet = []
            for offset, value in enumerate(text):
                token = {
                    "alphabet_position": (
                        ord(value) if value == " " or value.isascii() else None
                    ),
                    "code_point": f"U+{ord(value):04X}",
                    "codepoint_offset": offset,
                    "in_alphabet": value == " " or value.isascii(),
                    "value": value,
                }
                if not token["in_alphabet"]:
                    out_of_alphabet.append(token)
                if value == " ":
                    close_word()
                    segments.append(
                        {
                            "kind": "superpositioned-space-boundary",
                            "token": token,
                        }
                    )
                else:
                    word.append(token)
            close_word()
            records.append(
                {
                    "has_complete_alphabet_coverage": not out_of_alphabet,
                    "nesting_boundary_count": text.count(" "),
                    "out_of_alphabet": tuple(out_of_alphabet),
                    "raw_text": text,
                    "segments": tuple(segments),
                    "source_id": payload["source_ref"],
                    "speaker_id": speaker_id,
                    "turn_index": turn_index,
                    "unit_support": 1.0,
                    "word_count": sum(
                        segment["kind"] == "word-gonol" for segment in segments
                    ),
                }
            )
        evidence = {
            "corpus_execution": "full-corpus",
            "evidence_mode": "exact-observation",
            "gonol_initiation": "mobius-twist",
            "measurement_validity_claim": False,
            "normalization_policy": "none-preserve-source",
            "observation_digest": sha256(
                repr(payload["ucns_turns"]).encode("utf-8")
            ).hexdigest(),
            "options": (("normalization", "none-preserve-source"),),
            "profile_id": "fixture.edcm-word-gonol",
            "profile_scope": "edcm-only",
            "profile_version": "test",
            "projection_status": "not-projected",
            "smallest_gonol": "word",
            "source_commit": "fixture-ucns",
            "source_repository": "fixture",
            "support_policy": "one-unit-per-speaker-turn",
            "theorem_status_transfer": False,
            "token_alphabet_sha256": "fixture",
            "token_alphabet_size": 157,
            "turns": tuple(records),
        }
        return {"ucns_profile_observation": evidence}


def _member_records(path: Path) -> list[dict[str, Any]]:
    records = []
    with ZipFile(path) as archive:
        for info in archive.infolist():
            digest = sha256(archive.read(info.filename)).hexdigest()
            records.append(
                {
                    "bytes": info.file_size,
                    "path": info.filename,
                    "sha256": digest,
                }
            )
    return sorted(records, key=lambda value: value["path"])


def _fixture_archive(
    tmp_path: Path,
    *,
    invalid_turn: bool = False,
) -> tuple[Path, AdmissionManifest]:
    dialogues = {
        "A.json": {
            "goal": {
                "hotel": {"fail_book": {"stay": "3"}, "fail_info": {}}
            },
            "log": [
                {"text": "  exact café", "metadata": {}},
                {"text": "line\nbreak", "metadata": {"hotel": {}}},
            ],
        },
        "B.json": {
            "goal": {
                "train": {"fail_book": {}, "fail_info": {"day": "monday"}}
            },
            "log": [
                {"text": 7 if invalid_turn else "final", "metadata": {}},
            ],
        },
    }
    path = tmp_path / "fixture.zip"
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr(
            "MULTIWOZ2.1/data.json",
            json.dumps(dialogues, ensure_ascii=False, indent=2),
        )
        archive.writestr("MULTIWOZ2.1/testListFile.json", "B.json\n")
        archive.writestr("MULTIWOZ2.1/valListFile.json", "")
    archive_bytes = path.read_bytes()
    payload = {
        "corpus_id": "multiwoz-2.1",
        "evidence_state": "represented-evidence",
        "execution_policy": {
            "corpus_execution": "full-corpus",
            "normalization": "none-preserve-source",
            "sampling": False,
        },
        "expected": {
            "dialogue_count": 2,
            "partition_counts": {"test": 1, "train": 1, "validation": 0},
        },
        "hmmm": ["fixture semantic labels remain unresolved"],
        "information_boundaries": {
            "profile_input": "log text",
            "speaker_identity": "even=user, odd=system adapter convention",
        },
        "license": {"spdx": "CC-BY-4.0"},
        "schema_id": "edcm.corpus-admission",
        "schema_version": "1.0.0",
        "source": {
            "archive": {
                "bytes": len(archive_bytes),
                "filename": path.name,
                "logical_members": _member_records(path),
                "sha256": sha256(archive_bytes).hexdigest(),
            },
            "data_member": "MULTIWOZ2.1/data.json",
            "test_member": "MULTIWOZ2.1/testListFile.json",
            "validation_member": "MULTIWOZ2.1/valListFile.json",
        },
        "status": "admitted",
    }
    return path, AdmissionManifest(payload)


def test_streaming_top_level_object_keeps_order_and_exact_value_digest() -> None:
    source = '{"B": {"text": "é"}, "A": [1, 2]}'
    entries = list(iter_top_level_object(io.StringIO(source), chunk_size=3))
    assert [entry[0] for entry in entries] == ["B", "A"]
    assert entries[0][1] == {"text": "é"}
    assert entries[0][2] == sha256('{"text": "é"}'.encode("utf-8")).hexdigest()


def test_full_fixture_run_preserves_order_exact_text_and_profile_counts(
    tmp_path: Path,
) -> None:
    archive, manifest = _fixture_archive(tmp_path)
    report, receipt = run_archive(
        archive,
        adapter=FixtureAdapter(),
        edcm_commit="fixture-edcm",
        ucns_commit="fixture-ucns",
        manifest=manifest,
    )
    assert receipt["status"] == "complete"
    assert report["execution"]["dialogues"] == 2
    assert report["execution"]["source_turns"] == 3
    assert report["execution"]["adapter_turns"] == 3
    assert report["execution"]["profile_unit_support_total"] == 3.0
    assert report["execution"]["first_dialogue_id"] == "A.json"
    assert report["execution"]["last_dialogue_id"] == "B.json"
    assert report["execution"]["partitions"] == {
        "test": 1,
        "train": 1,
        "validation": 0,
    }
    observations = report["failure_seeking_observations"]
    assert observations["space_boundaries"] == 3
    assert observations["repeated_space_excess"] == 1
    assert observations["leading_space_turns"] == 1
    assert observations["newline_turns"] == 1
    assert observations["out_of_alphabet"]["occurrences"] == 1
    assert observations["source_declared_failure_dialogues"] == 2
    assert report["reconciliation"]["complete"] is True
    assert report["canon_selection"] is None


def test_archive_mutation_fails_before_dialogue_observation(tmp_path: Path) -> None:
    archive, manifest = _fixture_archive(tmp_path)
    archive.write_bytes(archive.read_bytes() + b"mutation")
    with pytest.raises(CorpusRunError) as caught:
        run_archive(
            archive,
            adapter=FixtureAdapter(),
            edcm_commit="fixture-edcm",
            ucns_commit="fixture-ucns",
            manifest=manifest,
        )
    assert caught.value.code == "ARCHIVE_BYTES"
    assert caught.value.state == {}


def test_manifest_count_mismatch_refuses_completion(tmp_path: Path) -> None:
    archive, manifest = _fixture_archive(tmp_path)
    payload = dict(manifest.payload)
    payload["expected"] = {
        "dialogue_count": 3,
        "partition_counts": {"test": 1, "train": 2, "validation": 0},
    }
    with pytest.raises(CorpusRunError) as caught:
        run_archive(
            archive,
            adapter=FixtureAdapter(),
            edcm_commit="fixture-edcm",
            ucns_commit="fixture-ucns",
            manifest=AdmissionManifest(payload),
        )
    assert caught.value.code == "RECONCILIATION_FAILED"
    assert caught.value.state["dialogues"] == 2


def test_invalid_turn_reports_exact_active_source_position(tmp_path: Path) -> None:
    archive, manifest = _fixture_archive(tmp_path, invalid_turn=True)
    with pytest.raises(CorpusRunError) as caught:
        run_archive(
            archive,
            adapter=FixtureAdapter(),
            edcm_commit="fixture-edcm",
            ucns_commit="fixture-ucns",
            manifest=manifest,
        )
    error = caught.value
    assert error.code == "TURN_TEXT_TYPE"
    assert error.state["last_completed_dialogue_index"] == 0
    assert error.state["last_completed_dialogue_id"] == "A.json"
    assert error.state["active_dialogue_index"] == 1
    assert error.state["active_dialogue_id"] == "B.json"
    assert error.state["active_turn_index"] == 0


def test_report_and_checkpoint_exclude_source_turn_text(tmp_path: Path) -> None:
    archive, manifest = _fixture_archive(tmp_path)
    checkpoint = tmp_path / "checkpoint.json"
    report, receipt = run_archive(
        archive,
        adapter=FixtureAdapter(),
        edcm_commit="fixture-edcm",
        ucns_commit="fixture-ucns",
        manifest=manifest,
        checkpoint_path=checkpoint,
        checkpoint_every=1,
    )
    serialized = json.dumps(report, ensure_ascii=False) + json.dumps(receipt)
    serialized += checkpoint.read_text(encoding="utf-8")
    assert "exact café" not in serialized
    assert "line\\nbreak" not in serialized
    assert "final" not in serialized

    repeated_report, repeated_receipt = run_archive(
        archive,
        adapter=FixtureAdapter(),
        edcm_commit="fixture-edcm",
        ucns_commit="fixture-ucns",
        manifest=manifest,
        checkpoint_path=checkpoint,
        checkpoint_every=1,
    )
    assert repeated_report == report
    assert repeated_receipt == receipt


def test_actual_pinned_ucns_profile_can_drive_fixture_when_installed(
    tmp_path: Path,
) -> None:
    ucns = pytest.importorskip("ucns")
    archive, manifest = _fixture_archive(tmp_path)
    report, receipt = run_archive(
        archive,
        adapter=ActualUCNSAdapter(ucns),
        edcm_commit="fixture-edcm",
        ucns_commit=PINNED_UCNS_COMMIT,
        manifest=manifest,
    )
    assert receipt["status"] == "complete"
    assert report["profile"]["profile_id"] == "ucns.profile.edcm-word-gonol"
    assert report["profile"]["source_commit"] == PINNED_UCNS_COMMIT
