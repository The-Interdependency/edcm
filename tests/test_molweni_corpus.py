"""Contract checks for the Molweni full-corpus runner."""

from __future__ import annotations

# === CHECKS ===
# id: check_molweni_admission_precedes_execution
#   proves: molweni_admission_precedes_execution
#   call: self::test_source_mutation_fails_before_profile_observation
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_molweni_every_dp_turn_and_relation_is_retained_once
#   proves: molweni_every_dp_turn_and_relation_is_retained_once
#   call: self::test_complete_fixture_observes_exact_dp_once_and_retains_graph
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_molweni_every_mrc_annotation_is_validated_without_duplicate_measurement
#   proves: molweni_every_mrc_annotation_is_validated_without_duplicate_measurement
#   call: self::test_complete_fixture_validates_mrc_spans_without_remeasuring_turns
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_molweni_completion_requires_cross_view_reconciliation
#   proves: molweni_completion_requires_cross_view_reconciliation
#   call: self::test_manifest_count_mismatch_refuses_completion
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_molweni_failure_is_receipted_at_source_position
#   proves: molweni_failure_is_receipted_at_source_position
#   call: self::test_invalid_answer_span_reports_exact_mrc_position
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_molweni_written_outputs_exclude_raw_source_text
#   proves: molweni_written_outputs_exclude_raw_source_text
#   call: self::test_report_receipt_and_checkpoint_exclude_raw_text
#   mutates: filesystem
#   cleanup: tempdir_teardown
# === END CHECKS ===

import copy
import json
import subprocess
from hashlib import sha256
from pathlib import Path
from typing import Any

import pytest

from edcm.corpora.molweni import (
    AdmissionManifest,
    CorpusRunError,
    _build_receipt,
    run_source,
)


class FixtureAdapter:
    """Exact-shape local profile adapter with an observable call boundary."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def normalize(self, payload: dict[str, Any]) -> dict[str, Any]:
        self.calls.append(payload)
        records = []
        for turn_index, (speaker_id, text) in enumerate(payload["ucns_turns"]):
            segments = []
            word = []

            def close_word() -> None:
                if word:
                    segments.append(
                        {"kind": "word-gonol", "tokens": tuple(word)}
                    )
                    word.clear()

            out_of_alphabet = []
            for offset, value in enumerate(text):
                token = {
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
                    "nesting_boundary_count": text.count(" "),
                    "out_of_alphabet": tuple(out_of_alphabet),
                    "raw_text": text,
                    "segments": tuple(segments),
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


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _git(path: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _fixture_source(
    tmp_path: Path,
    *,
    invalid_span: bool = False,
) -> tuple[Path, AdmissionManifest]:
    root = tmp_path / "Molweni"
    root.mkdir()
    edus = [
        {"speaker": "alice", "text": "  exact"},
        {"speaker": "", "text": "café\nreply"},
    ]
    dp_relation = [{"x": 0, "y": 1, "type": "QAP"}]
    dp_dialogue = {"id": "D1", "edus": edus, "relations": dp_relation}
    for split, dialogues in {
        "train": [dp_dialogue],
        "dev": [],
        "test": [],
    }.items():
        _write_json(root / "DP" / f"{split}.json", dialogues)

    context = "alice:   exact\nbob: café\nreply"
    answer = "exact"
    answer_start = context.index(answer) + int(invalid_span)
    mrc_dialogue = {
        "context": context,
        "edus": edus,
        "relations": [
            {"x": 0, "y": 1, "type": "Comment"},
            {"x": 1, "y": 2, "type": "Elaboration"},
        ],
        "qas": [
            {
                "answers": [{"answer_start": answer_start, "text": answer}],
                "id": "q1",
                "is_impossible": False,
                "question": "What?",
            },
            {
                "answers": [],
                "id": "q2",
                "is_impossible": True,
                "plausible_answers": [
                    {
                        "answer_start": context.index("reply"),
                        "text": "reply",
                    }
                ],
                "question": "Why?",
            },
        ],
    }
    for split, dialogues in {
        "train": [mrc_dialogue],
        "dev": [],
        "test": [],
    }.items():
        _write_json(
            root / "MRC(withDiscourse)" / f"{split}.json",
            {"data": {"title": split, "dialogues": dialogues}},
        )
    (root / "LICENSE").write_text("fixture Apache-2.0\n", encoding="utf-8")

    _git(root, "init")
    _git(root, "config", "user.name", "Fixture")
    _git(root, "config", "user.email", "fixture@example.invalid")
    _git(root, "add", ".")
    _git(root, "commit", "-m", "fixture")
    commit = _git(root, "rev-parse", "HEAD")
    tree = _git(root, "rev-parse", "HEAD^{tree}")

    files = []
    for relative in (
        "DP/dev.json",
        "DP/test.json",
        "DP/train.json",
        "MRC(withDiscourse)/dev.json",
        "MRC(withDiscourse)/test.json",
        "MRC(withDiscourse)/train.json",
        "LICENSE",
    ):
        data = (root / relative).read_bytes()
        files.append(
            {
                "bytes": len(data),
                "path": relative,
                "sha256": sha256(data).hexdigest(),
            }
        )
    empty_dp = {"dialogues": 0, "relations": 0, "turns": 0}
    empty_mrc = {
        "answerable_questions": 0,
        "dialogues": 0,
        "plausible_answers": 0,
        "questions": 0,
        "relations": 0,
        "turns": 0,
        "unanswerable_questions": 0,
    }
    payload = {
        "corpus_id": "molweni",
        "evidence_state": "represented-evidence",
        "execution_policy": {
            "corpus_execution": "full-corpus",
            "normalization": "none-preserve-source",
            "sampling": False,
        },
        "expected": {
            "cross_view": {"relation_graph_disagreements": 1},
            "dp": {
                "dialogues": 1,
                "partitions": {
                    "train": {"dialogues": 1, "relations": 1, "turns": 2},
                    "dev": empty_dp,
                    "test": empty_dp,
                },
                "relations": 1,
                "turns": 2,
            },
            "mrc": {
                "answerable_questions": 1,
                "dialogues": 1,
                "invalid_relation_endpoint_dialogues": 1,
                "invalid_relation_endpoints": 1,
                "partitions": {
                    "train": {
                        "answerable_questions": 1,
                        "dialogues": 1,
                        "plausible_answers": 1,
                        "questions": 2,
                        "relations": 2,
                        "turns": 2,
                        "unanswerable_questions": 1,
                    },
                    "dev": empty_mrc,
                    "test": empty_mrc,
                },
                "plausible_answers": 1,
                "questions": 2,
                "relations": 2,
                "turns": 2,
                "unanswerable_questions": 1,
            },
        },
        "hmmm": ["fixture boundaries"],
        "information_boundaries": {
            "profile_input": "DP edus only",
            "projection": "none",
        },
        "license": {"spdx": "Apache-2.0"},
        "privacy_and_removal": {"raw_source_in_git": False},
        "schema_id": "edcm.corpus-admission",
        "schema_version": "1.0.0",
        "source": {
            "commit": commit,
            "dp_files": {
                "train": "DP/train.json",
                "dev": "DP/dev.json",
                "test": "DP/test.json",
            },
            "files": files,
            "mrc_files": {
                "train": "MRC(withDiscourse)/train.json",
                "dev": "MRC(withDiscourse)/dev.json",
                "test": "MRC(withDiscourse)/test.json",
            },
            "repository": "fixture",
            "tree": tree,
        },
        "status": "admitted",
    }
    return root, AdmissionManifest(payload)


def test_complete_fixture_observes_exact_dp_once_and_retains_graph(
    tmp_path: Path,
) -> None:
    source, manifest = _fixture_source(tmp_path)
    adapter = FixtureAdapter()
    report, receipt = run_source(
        source,
        adapter=adapter,
        edcm_commit="fixture-edcm",
        ucns_commit="fixture-ucns",
        manifest=manifest,
    )
    assert receipt["status"] == "complete"
    assert report["discourse_parsing_execution"]["dialogues"] == 1
    assert report["discourse_parsing_execution"]["source_turns"] == 2
    assert report["discourse_parsing_execution"]["adapter_turns"] == 2
    assert report["discourse_parsing_execution"]["relations"] == 1
    assert len(adapter.calls) == 1
    assert adapter.calls[0]["ucns_turns"] == (
        ("alice", "  exact"),
        ("edcm.molweni/source-empty-speaker/D1/1", "café\nreply"),
    )
    assert report["discourse_relation_evidence"]["label_counts"] == [
        {"label": "QAP", "relations": 1}
    ]
    assert (
        report["failure_seeking_observations"]["source_empty_speaker_turns"]
        == 1
    )


def test_complete_fixture_validates_mrc_spans_without_remeasuring_turns(
    tmp_path: Path,
) -> None:
    source, manifest = _fixture_source(tmp_path)
    adapter = FixtureAdapter()
    report, _receipt = run_source(
        source,
        adapter=adapter,
        edcm_commit="fixture-edcm",
        ucns_commit="fixture-ucns",
        manifest=manifest,
    )
    assert len(adapter.calls) == 1
    assert report["mrc_annotation_execution"] == {
        "answerable_questions": 1,
        "dialogues": 1,
        "partitions": manifest.expected["mrc"]["partitions"],
        "plausible_answers": 1,
        "questions": 2,
        "relations": 2,
        "turns_reconciled_not_remeasured": 2,
        "unanswerable_questions": 1,
    }
    assert report["cross_view_evidence"]["relation_graph_disagreements"] == 1
    assert report["failure_seeking_observations"]["answer_span_mismatches"] == 0
    assert (
        report["failure_seeking_observations"][
            "mrc_invalid_relation_endpoints"
        ]
        == 1
    )


def test_source_mutation_fails_before_profile_observation(tmp_path: Path) -> None:
    source, manifest = _fixture_source(tmp_path)
    (source / "DP/train.json").write_text("[]\n", encoding="utf-8")
    adapter = FixtureAdapter()
    with pytest.raises(CorpusRunError) as captured:
        run_source(
            source,
            adapter=adapter,
            edcm_commit="fixture-edcm",
            ucns_commit="fixture-ucns",
            manifest=manifest,
        )
    assert captured.value.code == "EDCM_DIRTY"
    assert adapter.calls == []


def test_manifest_count_mismatch_refuses_completion(tmp_path: Path) -> None:
    source, manifest = _fixture_source(tmp_path)
    payload = copy.deepcopy(manifest.payload)
    payload["expected"]["dp"]["turns"] = 3
    with pytest.raises(CorpusRunError) as captured:
        run_source(
            source,
            adapter=FixtureAdapter(),
            edcm_commit="fixture-edcm",
            ucns_commit="fixture-ucns",
            manifest=AdmissionManifest(payload),
        )
    assert captured.value.code == "RECONCILIATION_FAILED"


def test_invalid_answer_span_reports_exact_mrc_position(tmp_path: Path) -> None:
    source, manifest = _fixture_source(tmp_path, invalid_span=True)
    with pytest.raises(CorpusRunError) as captured:
        run_source(
            source,
            adapter=FixtureAdapter(),
            edcm_commit="fixture-edcm",
            ucns_commit="fixture-ucns",
            manifest=manifest,
        )
    error = captured.value
    assert error.code == "ANSWER_SPAN"
    assert error.state["active_variant"] == "MRC(withDiscourse)"
    assert error.state["active_split"] == "train"
    assert error.state["active_dialogue_index"] == 0
    assert error.state["active_question_index"] == 0
    receipt = _build_receipt(
        manifest=manifest,
        state=error.state,
        status="incomplete",
        error_code=error.code,
        error_reason=str(error),
    )
    assert receipt["progress"]["active_question_index"] == 0
    assert receipt["error"]["code"] == "ANSWER_SPAN"


def test_report_receipt_and_checkpoint_exclude_raw_text(tmp_path: Path) -> None:
    source, manifest = _fixture_source(tmp_path)
    checkpoint = tmp_path / "checkpoint.json"
    report, receipt = run_source(
        source,
        adapter=FixtureAdapter(),
        edcm_commit="fixture-edcm",
        ucns_commit="fixture-ucns",
        manifest=manifest,
        checkpoint_path=checkpoint,
        checkpoint_every=1,
    )
    serialized = "\n".join(
        (
            json.dumps(report, ensure_ascii=False),
            json.dumps(receipt, ensure_ascii=False),
            checkpoint.read_text(encoding="utf-8"),
        )
    )
    for raw_value in (
        "  exact",
        "café\nreply",
        "alice",
        "What?",
        "Why?",
    ):
        assert raw_value not in serialized


def test_completed_checkpoint_rerun_is_byte_identical(tmp_path: Path) -> None:
    source, manifest = _fixture_source(tmp_path)
    checkpoint = tmp_path / "checkpoint.json"
    report_a, receipt_a = run_source(
        source,
        adapter=FixtureAdapter(),
        edcm_commit="fixture-edcm",
        ucns_commit="fixture-ucns",
        manifest=manifest,
        checkpoint_path=checkpoint,
        checkpoint_every=1,
    )
    resumed_adapter = FixtureAdapter()
    report_b, receipt_b = run_source(
        source,
        adapter=resumed_adapter,
        edcm_commit="fixture-edcm",
        ucns_commit="fixture-ucns",
        manifest=manifest,
        checkpoint_path=checkpoint,
        checkpoint_every=1,
    )
    assert resumed_adapter.calls == []
    assert report_b == report_a
    assert receipt_b == receipt_a
