"""Contract checks for the MultiWOZ 2.1 full-corpus runner."""

from __future__ import annotations

# === CHECKS ===
# id: check_multiwoz21_admission_precedes_execution
#   proves: multiwoz21_admission_precedes_execution
#   call: self::test_archive_mutation_fails_before_dialogue_observation
#   requires: python3
#   timeout: 30
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_multiwoz21_every_turn_is_observed_exactly_once
#   proves: multiwoz21_every_turn_is_observed_exactly_once
#   call: self::test_full_fixture_run_preserves_order_exact_text_and_profile_counts
#   requires: python3
#   timeout: 30
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_multiwoz21_completion_requires_reconciliation
#   proves: multiwoz21_completion_requires_reconciliation
#   call: self::test_manifest_count_mismatch_refuses_completion
#   requires: python3
#   timeout: 30
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_multiwoz21_failure_is_receipted
#   proves: multiwoz21_failure_is_receipted
#   call: self::test_invalid_turn_reports_exact_active_source_position
#   requires: python3
#   timeout: 30
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_multiwoz21_written_outputs_exclude_raw_text
#   proves: multiwoz21_written_outputs_exclude_raw_text
#   call: self::test_report_and_checkpoint_exclude_source_turn_text
#   requires: python3
#   timeout: 30
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_multiwoz21_ucns_v0141_receipt_matches_source_native_run
#   proves: multiwoz21_ucns_v0141_receipt_requires_matching_source_native_run
#   call: self::test_full_fixture_run_preserves_order_exact_text_and_profile_counts
#   requires: python3
#   timeout: 30
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_multiwoz21_ucns_v0141_false_receipt_rejected
#   proves: multiwoz21_ucns_v0141_receipt_requires_matching_source_native_run
#   call: self::test_claimed_gate_without_source_exhaustion_cannot_complete
#   requires: python3
#   timeout: 30
#   mutates: filesystem
#   cleanup: tempdir_teardown
# === END CHECKS ===

import importlib.util
import io
import json
from hashlib import sha256
import os
from pathlib import Path
import py_compile
import shutil
import subprocess
from types import ModuleType
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

import edcm.corpora.multiwoz21 as multiwoz21_module
from edcm.corpora.multiwoz21 import (
    AdmissionManifest,
    CorpusRunError,
    UCNSFullCorpusGate,
    iter_top_level_object,
    run_archive,
)
from edcm.ucns_adapter import (
    ActualUCNSAdapter,
    PINNED_UCNS_COMMIT,
    UCNSAdapterConstructionError,
)


SPACE_MANIFESTATIONS = frozenset(
    {
        *(chr(value) for value in range(0x0009, 0x000E)),
        "\u0020",
        "\u0085",
        "\u00a0",
        "\u1680",
        *(chr(value) for value in range(0x2000, 0x200B)),
        "\u2028",
        "\u2029",
        "\u202f",
        "\u205f",
        "\u3000",
    }
)
SPACE_CODE_POINT_LABELS = tuple(
    f"U+{ord(value):04X}"
    for value in (
        *(chr(code_point) for code_point in range(0x0009, 0x000E)),
        "\u0020",
        "\u0085",
        "\u00a0",
        "\u1680",
        *(chr(code_point) for code_point in range(0x2000, 0x200B)),
        "\u2028",
        "\u2029",
        "\u202f",
        "\u205f",
        "\u3000",
    )
)


def _canonical_digest_without(payload: dict[str, Any], field: str) -> str:
    return sha256(
        json.dumps(
            {key: value for key, value in payload.items() if key != field},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


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
                is_space = value in SPACE_MANIFESTATIONS
                alphabet_position = (
                    0
                    if is_space
                    else ord(value)
                    if value.isascii()
                    else None
                )
                token = {
                    "alphabet_position": alphabet_position,
                    "carrier_position": alphabet_position,
                    "carrier_token": (
                        " "
                        if is_space
                        else value
                        if alphabet_position is not None
                        else None
                    ),
                    "code_point": f"U+{ord(value):04X}",
                    "codepoint_offset": offset,
                    "in_alphabet": alphabet_position is not None,
                    "has_carrier_assignment": alphabet_position is not None,
                    "is_space_manifestation": is_space,
                    "is_public_gonol_token": (
                        value == " "
                        or (value.isascii() and not is_space)
                    ),
                    "source_code_point": f"U+{ord(value):04X}",
                    "source_value": value,
                    "value": value,
                }
                if not token["in_alphabet"]:
                    out_of_alphabet.append(token)
                if is_space:
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
            for segment in segments:
                if segment["kind"] != "word-gonol":
                    continue
                unassigned = tuple(
                    token
                    for token in segment["tokens"]
                    if not token["has_carrier_assignment"]
                )
                segment["carrier_unassigned"] = unassigned
                segment["out_of_alphabet"] = unassigned
            records.append(
                {
                    "carrier_unassigned": tuple(out_of_alphabet),
                    "has_complete_carrier_assignment": not out_of_alphabet,
                    "has_complete_alphabet_coverage": not out_of_alphabet,
                    "nesting_boundary_count": sum(
                        value in SPACE_MANIFESTATIONS for value in text
                    ),
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
            "source_domain": "unicode-scalar-values",
            "space_assignment_policy": "unicode-white-space-origin-v1",
            "space_code_point_labels": SPACE_CODE_POINT_LABELS,
            "space_code_points_sha256": (
                "a5dc5ec34775d511a02b17911aa385c5d92908ee58749ea16d721cd53d19b944"
            ),
            "source_commit": "fixture-ucns",
            "source_repository": "fixture",
            "support_policy": "one-unit-per-speaker-turn",
            "theorem_status_transfer": False,
            "token_alphabet_sha256": "fixture",
            "token_alphabet_size": 157,
            "turns": tuple(records),
        }
        return {"ucns_profile_observation": evidence}


class FixtureFullCorpusGate:
    """Dependency-free stand-in that consumes the complete exact turn iterator."""

    def execute(
        self,
        manifest: AdmissionManifest,
        turns,
    ) -> dict[str, Any]:
        digest = sha256(b"fixture-full-corpus-v1")
        processed = 0
        for speaker_id, text in turns:
            speaker_bytes = speaker_id.encode("utf-8")
            text_bytes = text.encode("utf-8")
            digest.update(len(speaker_bytes).to_bytes(8, "big"))
            digest.update(speaker_bytes)
            digest.update(len(text_bytes).to_bytes(8, "big"))
            digest.update(text_bytes)
            processed += 1
        complete = processed == int(manifest.expected["turn_count"])
        stream_digest = digest.hexdigest()
        return {
            "exact_observation_stream_sha256": stream_digest,
            "exact_source_stream_sha256": stream_digest,
            "failure": None,
            "gate_effect": (
                "open-for-failure-seeking-analysis-only"
                if complete
                else "closed-incomplete-corpus-execution"
            ),
            "iterator_exhausted": True,
            "processed_turn_count": processed,
            "receipt": (
                {
                    "receipt_id": sha256(
                        f"fixture:{stream_digest}".encode("utf-8")
                    ).hexdigest()
                }
                if complete
                else None
            ),
            "schema_id": "ucns.edcm.full-corpus-execution",
            "schema_version": "0.14.1",
            "status": "complete" if complete else "incomplete",
        }


class NonConsumingFullCorpusGate:
    """Adversarial gate that claims completion without reading the source."""

    def execute(
        self,
        manifest: AdmissionManifest,
        turns,
    ) -> dict[str, Any]:
        return {
            "gate_effect": "open-for-failure-seeking-analysis-only",
            "processed_turn_count": int(manifest.expected["turn_count"]),
            "receipt": {"receipt_id": "f" * 64},
            "status": "complete",
        }


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
                {"text": " \texact café", "metadata": {}},
                {"text": "line\nbreak\u00a0", "metadata": {"hotel": {}}},
            ],
        },
        "B.json": {
            "goal": {
                "train": {"fail_book": {}, "fail_info": {"day": "monday"}}
            },
            "log": [
                {
                    "text": (
                        7
                        if invalid_turn
                        else "ZXQ_SOURCE_SENTINEL_49"
                    ),
                    "metadata": {},
                },
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
            "turn_count": 3,
        },
        "hmmm": ["fixture semantic labels remain unresolved"],
        "information_boundaries": {
            "profile_input": "log text",
            "speaker_identity": "even=user, odd=system adapter convention",
        },
        "license": {"spdx": "CC-BY-4.0"},
        "schema_id": "edcm.corpus-admission",
        "schema_version": "1.1.0",
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
        "ucns_full_corpus": {
            "adapter": {
                "adapter_id": "fixture.multiwoz21",
                "adapter_version": "test",
                "code_reference": "tests.test_multiwoz21_corpus:_fixture_archive",
            },
            "admission_decision_id": "fixture-admission/1",
            "corpus_version": "fixture",
            "privacy_treatment": "synthetic-no-personal-data",
            "redaction_policy": "none-synthetic-source",
        },
    }
    return path, AdmissionManifest(payload)


def test_streaming_top_level_object_keeps_order_and_exact_value_digest() -> None:
    source = '{"B": {"text": "é"}, "A": [1, 2]}'
    entries = list(iter_top_level_object(io.StringIO(source), chunk_size=3))
    assert [entry[0] for entry in entries] == ["B", "A"]
    assert entries[0][1] == {"text": "é"}
    assert entries[0][2] == sha256('{"text": "é"}'.encode("utf-8")).hexdigest()


def test_historical_report_is_superseded_by_exact_sealed_rerun() -> None:
    root = Path(__file__).resolve().parents[1]
    current_manifest = json.loads(
        (
            root / "edcm/corpora/data/multiwoz_2_1_admission.json"
        ).read_text(encoding="utf-8")
    )
    historical_manifest = json.loads(
        (
            root
            / "edcm/corpora/data/multiwoz_2_1_admission_v1_0_0.json"
        ).read_text(encoding="utf-8")
    )
    assert sha256(
        json.dumps(
            historical_manifest,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest() == (
        "aba3ebbac5e6f6ef0505cd9349361ba8bde7586fae21049e2d120fa362033ed6"
    )
    assert current_manifest["historical_manifest"] == {
        "path": "edcm/corpora/data/multiwoz_2_1_admission_v1_0_0.json",
        "sha256": (
            "aba3ebbac5e6f6ef0505cd9349361ba8bde7586fae21049e2d120fa362033ed6"
        ),
    }
    assert current_manifest["expected"]["turn_count"] == 143048
    record = json.loads(
        (
            root
            / "experiments/corpora/supersessions/"
            "2026-07-28-multiwoz-2.1-space-origin.json"
        ).read_text(encoding="utf-8")
    )
    historical = json.loads(
        (
            root
            / "experiments/corpora/results/"
            "2026-07-28-multiwoz-2.1-full.json"
        ).read_text(encoding="utf-8")
    )
    replacement_report_path = root / record["replacement"]["report_path"]
    replacement_receipt_path = root / record["replacement"]["receipt_path"]
    replacement = json.loads(replacement_report_path.read_text(encoding="utf-8"))
    replacement_receipt = json.loads(
        replacement_receipt_path.read_text(encoding="utf-8")
    )
    assert record["status"] == "superseded-by-sealed-rerun"
    assert record["superseded"]["report_digest"] == historical["report_digest"]
    assert record["replacement"]["status"] == "sealed-full-corpus-complete"
    assert record["replacement"]["report_digest"] == replacement["report_digest"]
    assert (
        record["replacement"]["receipt_digest"]
        == replacement_receipt["receipt_digest"]
    )
    assert record["replacement"]["report_sha256"] == sha256(
        replacement_report_path.read_bytes()
    ).hexdigest()
    assert record["replacement"]["receipt_sha256"] == sha256(
        replacement_receipt_path.read_bytes()
    ).hexdigest()
    assert replacement_receipt["status"] == "complete"
    assert replacement_receipt["identities"] == {
        "archive_sha256": "d377a176f5ec82dc9f6a97e4653d4eddc6cad917704c1aaaa5a8ee3e79f63a8e",
        "edcm_commit": "fbee2ee57f765b47c362a6877521493cc1afe20a",
        "ucns_commit": "c799b3547afc91a6039a5d3b15f997426eed138a",
    }
    assert record["information_boundaries"]["corrected_aggregate_claimed"] is True
    assert sum(
        item["historical_occurrences"]
        for item in record["reason"]["affected_source_code_points"]
    ) == 4094
    historical_observations = historical["failure_seeking_observations"]
    replacement_observations = replacement["failure_seeking_observations"]
    assert replacement_observations["carrier_unassigned"]["occurrences"] == 0
    assert replacement_observations["out_of_alphabet"]["occurrences"] == 0
    assert (
        replacement_observations["space_boundaries"]
        - historical_observations["space_boundaries"]
        == 4094
    )
    assert (
        replacement["identities"]["source_dialogue_digest_chain"]
        == historical["identities"]["source_dialogue_digest_chain"]
    )
    assert (
        replacement["identities"]["turn_evidence_digest_chain"]
        == historical["identities"]["turn_evidence_digest_chain"]
    )

    current_report_path = (
        root
        / "experiments/corpora/results/"
        "2026-07-31-multiwoz-2.1-ucns-v0.14.1-full.json"
    )
    current_receipt_path = (
        root
        / "experiments/corpora/receipts/"
        "2026-07-31-multiwoz-2.1-ucns-v0.14.1-complete.json"
    )
    current = json.loads(current_report_path.read_text(encoding="utf-8"))
    current_receipt = json.loads(current_receipt_path.read_text(encoding="utf-8"))
    handoff = json.loads(
        (root / "handoffs/ucns-profile-consumer-status.json").read_text(
            encoding="utf-8"
        )
    )["sealed_ucns_v0141_corpus_evidence"]

    assert current["report_digest"] == (
        "ff4718ba80d40028cc18fc222eae53295d8ab9efebe4a5da6b0e7c47e6088b77"
    )
    assert current_receipt["receipt_digest"] == (
        "4ebbb9a69be3690c01271e6a041de227e91615c073ad9e8601bdb9096fe41783"
    )
    assert current["report_digest"] == _canonical_digest_without(
        current, "report_digest"
    )
    assert current_receipt["receipt_digest"] == _canonical_digest_without(
        current_receipt, "receipt_digest"
    )
    assert sha256(current_report_path.read_bytes()).hexdigest() == (
        "f2044a4c1555b7fa52f9f05a562136f24b8960902630dc32cfce7fcdb0af7fde"
    )
    assert sha256(current_receipt_path.read_bytes()).hexdigest() == (
        "2730dd5413187fc7c2c33092c83cce8cb93d2606f9df8c4e0bf148085fccfb79"
    )
    assert current_receipt["report_digest"] == current["report_digest"]
    assert current_receipt["report_sha256"] == handoff["report_sha256"]
    assert current["execution"] == replacement["execution"]
    assert (
        current["failure_seeking_observations"]
        == replacement["failure_seeking_observations"]
    )
    assert current["identities"]["source_dialogue_digest_chain"] == (
        replacement["identities"]["source_dialogue_digest_chain"]
    )
    assert current["identities"]["turn_evidence_digest_chain"] == (
        replacement["identities"]["turn_evidence_digest_chain"]
    )

    expected_identities = {
        "archive_sha256": (
            "d377a176f5ec82dc9f6a97e4653d4eddc6cad917704c1aaaa5a8ee3e79f63a8e"
        ),
        "edcm_commit": "2e667f648bfcfa9f067997eb7e56d2346a4ba30c",
        "ucns_commit": "868d80878c9ecd93ff30e91ca289122ded805a49",
    }
    assert current_receipt["identities"] == expected_identities
    assert current["identities"]["archive"]["sha256"] == (
        expected_identities["archive_sha256"]
    )
    assert current["identities"]["edcm_commit"] == expected_identities["edcm_commit"]
    assert current["identities"]["ucns_commit"] == expected_identities["ucns_commit"]

    gate = current["ucns_full_corpus_gate"]
    source_native = gate["source_native_reconciliation"]
    receipt_id = "921ceacad026de1d884eec3e049b090246014706c937c062bd32f40bbff01f0c"
    assert gate["schema_version"] == "0.14.1"
    assert gate["status"] == "complete"
    assert gate["iterator_exhausted"] is True
    assert gate["processed_turn_count"] == 143048
    assert gate["exact_source_stream_sha256"] == (
        gate["exact_observation_stream_sha256"]
    )
    assert source_native["complete"] is True
    assert all(source_native["checks"].values())
    assert gate["receipt"]["receipt_id"] == receipt_id
    assert current_receipt["ucns_full_corpus"]["receipt_id"] == receipt_id
    assert gate["activations"] == {
        "edcm": "inactive",
        "metapat": "inactive",
        "selection_effect": "none",
    }
    assert current["canon_selection"] is None
    assert current["information_boundaries"]["candidate_measurement"] == "not-run"
    assert current["information_boundaries"]["formal_ucns_geometry"] == "NA"
    assert current["information_boundaries"]["raw_source_committed"] is False

    assert handoff == {
        "corpus_id": "multiwoz-2.1",
        "edcm_commit": expected_identities["edcm_commit"],
        "exact_stream_sha256": gate["exact_source_stream_sha256"],
        "receipt_digest": current_receipt["receipt_digest"],
        "receipt_id": receipt_id,
        "receipt_path": str(current_receipt_path.relative_to(root)),
        "receipt_sha256": sha256(current_receipt_path.read_bytes()).hexdigest(),
        "report_digest": current["report_digest"],
        "report_path": str(current_report_path.relative_to(root)),
        "report_sha256": sha256(current_report_path.read_bytes()).hexdigest(),
        "status": "complete",
        "ucns_commit": expected_identities["ucns_commit"],
    }

    v019_report_path = (
        root
        / "experiments/corpora/results/"
        "2026-07-31-multiwoz-2.1-ucns-v0.19-full.json"
    )
    v019_receipt_path = (
        root
        / "experiments/corpora/receipts/"
        "2026-07-31-multiwoz-2.1-ucns-v0.19-complete.json"
    )
    v019 = json.loads(v019_report_path.read_text(encoding="utf-8"))
    v019_receipt = json.loads(v019_receipt_path.read_text(encoding="utf-8"))
    v019_handoff = json.loads(
        (root / "handoffs/ucns-profile-consumer-status.json").read_text(
            encoding="utf-8"
        )
    )["sealed_ucns_v019_corpus_evidence"]

    assert v019["report_digest"] == (
        "45cfa7ef2406453f91d8d0e911e6d31823bdbdc14caea5da07458d8f0653a8e6"
    )
    assert v019_receipt["receipt_digest"] == (
        "0280942e6b887453ec490fa3163ebcf0e1534242dc40ef1dd2dbd69eeb856eb8"
    )
    assert v019["schema_version"] == "1.3.0"
    assert v019_receipt["schema_version"] == "1.3.0"
    assert v019["report_digest"] == _canonical_digest_without(
        v019, "report_digest"
    )
    assert v019_receipt["receipt_digest"] == _canonical_digest_without(
        v019_receipt, "receipt_digest"
    )
    assert sha256(v019_report_path.read_bytes()).hexdigest() == (
        "7303e045b805293d64a83263d0af2e22e956fe86149dd33c6fe887caaff38842"
    )
    assert sha256(v019_receipt_path.read_bytes()).hexdigest() == (
        "8552332c2072f88ccf0e52030a706e938328ad9f88410d405ccabf3bf74a30c6"
    )
    v019_identities = {
        "archive_sha256": (
            "d377a176f5ec82dc9f6a97e4653d4eddc6cad917704c1aaaa5a8ee3e79f63a8e"
        ),
        "edcm_tree": "5c39683c8e7b1fb77c893c08de41a76ea0b0bb4e",
        "ucns_commit": "872f53571d5dc2f133ff1813b7bdffd3a9c309f8",
    }
    assert v019_receipt["identities"] == v019_identities
    assert v019["identities"]["edcm_tree"] == v019_identities["edcm_tree"]
    assert v019["identities"]["ucns_commit"] == v019_identities["ucns_commit"]
    assert v019["profile"]["source_commit"] == v019_identities["ucns_commit"]
    assert v019_receipt["report_digest"] == v019["report_digest"]
    assert v019_receipt["report_sha256"] == sha256(
        v019_report_path.read_bytes()
    ).hexdigest()

    assert v019["execution"] == current["execution"]
    assert (
        v019["failure_seeking_observations"]
        == current["failure_seeking_observations"]
    )
    assert v019["identities"]["source_dialogue_digest_chain"] == (
        current["identities"]["source_dialogue_digest_chain"]
    )
    assert v019["identities"]["turn_evidence_digest_chain"] == (
        current["identities"]["turn_evidence_digest_chain"]
    )
    v019_gate = v019["ucns_full_corpus_gate"]
    assert v019_gate["schema_version"] == "0.14.1"
    assert v019_gate["status"] == "complete"
    assert v019_gate["processed_turn_count"] == 143048
    assert v019_gate["exact_source_stream_sha256"] == (
        "e94ba2e5e1e9d52b23fd5b9c33303be009dae32f4c3bc6a1d5186a353acb40b5"
    )
    assert (
        v019_gate["exact_observation_stream_sha256"]
        == v019_gate["exact_source_stream_sha256"]
    )
    assert v019_gate["receipt"]["receipt_id"] == receipt_id
    assert v019_receipt["ucns_full_corpus"]["receipt_id"] == receipt_id
    assert v019_gate["activations"] == {
        "edcm": "inactive",
        "metapat": "inactive",
        "selection_effect": "none",
    }
    assert v019["canon_selection"] is None
    assert v019["information_boundaries"]["candidate_measurement"] == "not-run"
    assert v019["information_boundaries"]["formal_ucns_geometry"] == "NA"
    assert v019["information_boundaries"]["raw_source_committed"] is False

    assert v019_handoff == {
        "corpus_id": "multiwoz-2.1",
        "edcm_tree": v019_identities["edcm_tree"],
        "exact_stream_sha256": v019_gate["exact_source_stream_sha256"],
        "receipt_digest": v019_receipt["receipt_digest"],
        "receipt_id": receipt_id,
        "receipt_path": str(v019_receipt_path.relative_to(root)),
        "receipt_sha256": sha256(v019_receipt_path.read_bytes()).hexdigest(),
        "report_digest": v019["report_digest"],
        "report_path": str(v019_report_path.relative_to(root)),
        "report_sha256": sha256(v019_report_path.read_bytes()).hexdigest(),
        "status": "complete",
        "ucns_commit": v019_identities["ucns_commit"],
    }


def test_full_fixture_run_preserves_order_exact_text_and_profile_counts(
    tmp_path: Path,
) -> None:
    archive, manifest = _fixture_archive(tmp_path)
    report, receipt = run_archive(
        archive,
        adapter=FixtureAdapter(),
        full_corpus_gate=FixtureFullCorpusGate(),
        edcm_tree="fixture-edcm-tree",
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
    assert report["schema_version"] == "1.3.0"
    assert receipt["schema_version"] == "1.3.0"
    assert report["identities"]["edcm_tree"] == "fixture-edcm-tree"
    assert receipt["identities"]["edcm_tree"] == "fixture-edcm-tree"
    assert report["profile"]["space_assignment_policy"] == (
        "unicode-white-space-origin-v1"
    )
    assert report["profile"]["source_domain"] == "unicode-scalar-values"
    assert report["profile"]["space_code_point_labels"] == list(
        SPACE_CODE_POINT_LABELS
    )
    assert report["profile"]["space_code_points_sha256"] == (
        "a5dc5ec34775d511a02b17911aa385c5d92908ee58749ea16d721cd53d19b944"
    )
    assert observations["space_boundaries"] == 5
    assert observations["repeated_space_excess"] == 1
    assert observations["leading_space_turns"] == 1
    assert observations["trailing_space_turns"] == 1
    assert observations["newline_turns"] == 1
    assert observations["out_of_alphabet"]["occurrences"] == 1
    assert observations["carrier_unassigned"] == observations["out_of_alphabet"]
    assert observations["source_declared_failure_dialogues"] == 2
    assert report["reconciliation"]["complete"] is True
    assert report["canon_selection"] is None
    gate = report["ucns_full_corpus_gate"]
    assert gate["status"] == "complete"
    assert gate["processed_turn_count"] == 3
    assert gate["receipt"]["receipt_id"] == (
        receipt["ucns_full_corpus"]["receipt_id"]
    )
    assert gate["source_native_reconciliation"]["complete"] is True
    assert gate["source_native_reconciliation"]["checks"] == {
        "dialogue_count_matches_source_native_pass": True,
        "turn_count_matches_source_native_pass": True,
        "turn_evidence_chain_matches_source_native_pass": True,
    }


def test_archive_mutation_fails_before_dialogue_observation(tmp_path: Path) -> None:
    archive, manifest = _fixture_archive(tmp_path)
    archive.write_bytes(archive.read_bytes() + b"mutation")
    with pytest.raises(CorpusRunError) as caught:
        run_archive(
            archive,
            adapter=FixtureAdapter(),
            full_corpus_gate=FixtureFullCorpusGate(),
            edcm_tree="fixture-edcm-tree",
            ucns_commit="fixture-ucns",
            manifest=manifest,
        )
    assert caught.value.code == "ARCHIVE_BYTES"
    assert caught.value.state == {}


def test_adapter_construction_failure_writes_incomplete_receipt(
    monkeypatch,
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "ucns-source"
    module_path = source_root / "src/ucns/__init__.py"
    module_path.parent.mkdir(parents=True)
    module_path.write_text("# fixture\n", encoding="utf-8")
    module = ModuleType("ucns")
    module.__file__ = str(module_path)

    monkeypatch.setitem(multiwoz21_module.sys.modules, "ucns", module)
    monkeypatch.setattr(
        multiwoz21_module,
        "_git_commit",
        lambda root, *, require_clean, verify_tree=None, producer_name="EDCM", expected_commit=None: PINNED_UCNS_COMMIT,
    )
    monkeypatch.setattr(
        multiwoz21_module,
        "_git_tree_identity",
        lambda root, pathspec, *, treeish="HEAD": "fixture-edcm-tree",
    )

    def reject_adapter(candidate):
        raise UCNSAdapterConstructionError("fixture identity rejection")

    monkeypatch.setattr(multiwoz21_module, "ActualUCNSAdapter", reject_adapter)
    receipt_path = tmp_path / "receipt.json"
    exit_code = multiwoz21_module._sealed_main(
        [
            "--archive",
            str(tmp_path / "archive.zip"),
            "--ucns-source-root",
            str(source_root),
            "--output",
            str(tmp_path / "report.json"),
            "--receipt",
            str(receipt_path),
        ]
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert exit_code == 1
    assert receipt["status"] == "incomplete"
    assert receipt["error"]["code"] == "UCNS_ADAPTER_CONSTRUCTION"
    assert "fixture identity rejection" in receipt["error"]["reason"]


def test_public_main_uses_fresh_isolated_edcm_module_graph(
    monkeypatch,
) -> None:
    def reject_in_process(argv):
        raise AssertionError("sealed work reused the already-loaded module graph")

    monkeypatch.setattr(multiwoz21_module, "_sealed_main", reject_in_process)

    assert multiwoz21_module.main(["--help"]) == 0


def test_direct_worker_flag_is_not_a_worker_capability(monkeypatch) -> None:
    for name in (
        multiwoz21_module._SEALED_REPOSITORY_ROOT_ENV,
        multiwoz21_module._SEALED_EDCM_COMMIT_ENV,
        multiwoz21_module._SEALED_EDCM_TREE_ENV,
        multiwoz21_module._SEALED_SNAPSHOT_ROOT_ENV,
    ):
        monkeypatch.delenv(name, raising=False)

    assert (
        multiwoz21_module._sealed_worker_arguments(
            ["--edcm-sealed-worker", "--archive=untrusted.zip"]
        )
        is None
    )


def test_isolated_bootstrap_avoids_post_311_extraction_filter_apis() -> None:
    bootstrap = multiwoz21_module._ISOLATED_WORKER_BOOTSTRAP

    assert "tarfile.data_filter" not in bootstrap
    assert ".extractall(" not in bootstrap
    assert "member.isfile()" in bootstrap
    assert "member.isdir()" in bootstrap
    assert multiwoz21_module._BOOTSTRAP_ADMISSION_DIGEST == (
        multiwoz21_module.load_admission_manifest().digest
    )


@pytest.mark.parametrize("equals_form", [False, True], ids=["split", "equals"])
def test_bootstrap_git_failure_writes_incomplete_receipt(
    tmp_path: Path,
    equals_form: bool,
) -> None:
    repository = tmp_path / "not-a-repository"
    repository.mkdir()
    receipt_path = tmp_path / "bootstrap-receipt.json"
    archive_path = tmp_path / "archive.zip"

    archive_arguments = (
        [f"--archive={archive_path}"]
        if equals_form
        else ["--archive", str(archive_path)]
    )
    receipt_arguments = (
        [f"--receipt={receipt_path}"]
        if equals_form
        else ["--receipt", str(receipt_path)]
    )
    exit_code = multiwoz21_module._run_in_fresh_process(
        [
            *archive_arguments,
            "--ucns-source-root",
            str(tmp_path / "ucns"),
            "--output",
            str(tmp_path / "report.json"),
            *receipt_arguments,
        ],
        repository_root=repository,
    )

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert exit_code == 1
    assert receipt["schema_id"] == multiwoz21_module.RECEIPT_SCHEMA_ID
    assert receipt["schema_version"] == multiwoz21_module.RECEIPT_SCHEMA_VERSION
    assert receipt["admission_digest"] == (
        multiwoz21_module.load_admission_manifest().digest
    )
    assert receipt["status"] == "incomplete"
    assert receipt["error"]["code"] == "GIT_IDENTITY"
    assert receipt["source_artifact_filename"] == archive_path.name
    assert receipt["receipt_digest"] == _canonical_digest_without(
        receipt,
        "receipt_digest",
    )


def test_worker_output_failure_uses_output_io_receipt(
    monkeypatch,
    tmp_path: Path,
) -> None:
    output_path = (tmp_path / "report.json").resolve()
    receipt_path = (tmp_path / "receipt.json").resolve()
    original_write = multiwoz21_module._write_json_atomic

    monkeypatch.setattr(
        multiwoz21_module,
        "_git_commit",
        lambda root, *, require_clean, verify_tree=None, producer_name="EDCM", expected_commit=None: "fixture-commit",
    )
    monkeypatch.setattr(
        multiwoz21_module,
        "_git_tree_identity",
        lambda root, pathspec, *, treeish="HEAD": "fixture-edcm-tree",
    )
    monkeypatch.setattr(
        multiwoz21_module,
        "_load_pinned_runtime",
        lambda source_root: (object(), object()),
    )
    monkeypatch.setattr(
        multiwoz21_module,
        "run_archive",
        lambda *args, **kwargs: ({}, {}),
    )

    def fail_report_write(path, payload):
        if path == output_path:
            raise PermissionError("fixture report path is unwritable")
        return original_write(path, payload)

    monkeypatch.setattr(
        multiwoz21_module,
        "_write_json_atomic",
        fail_report_write,
    )
    exit_code = multiwoz21_module._sealed_main(
        [
            "--archive",
            str(tmp_path / "archive.zip"),
            "--ucns-source-root",
            str(tmp_path / "ucns"),
            "--output",
            str(output_path),
            "--receipt",
            str(receipt_path),
        ]
    )

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert exit_code == 1
    assert receipt["status"] == "incomplete"
    assert receipt["error"]["code"] == "OUTPUT_IO"
    assert "PermissionError" in receipt["error"]["reason"]
    assert receipt["receipt_digest"] == _canonical_digest_without(
        receipt,
        "receipt_digest",
    )


def _committed_edcm_fixture(tmp_path: Path) -> Path:
    repository = tmp_path / "repository"
    shutil.copytree(
        Path(multiwoz21_module.__file__).resolve().parents[1],
        repository / "edcm",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    subprocess.run(
        ["git", "init", str(repository)],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(repository), "add", "edcm"],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "git",
            "-C",
            str(repository),
            "-c",
            "user.name=EDCM Test",
            "-c",
            "user.email=edcm-test@example.invalid",
            "commit",
            "-m",
            "trusted EDCM fixture",
        ],
        check=True,
        capture_output=True,
    )
    return repository


def test_isolated_bootstrap_rejects_altered_runner_cache(
    tmp_path: Path,
) -> None:
    repository = _committed_edcm_fixture(tmp_path)
    source = repository / "edcm/corpora/multiwoz21.py"
    original_source = source.read_bytes()
    altered_source = original_source.replace(
        b"if not _is_runtime_cache(cached_path):",
        b"if     _is_runtime_cache(cached_path):",
        1,
    )
    assert altered_source != original_source
    assert len(altered_source) == len(original_source)
    source.write_bytes(altered_source)
    cache = Path(importlib.util.cache_from_source(str(source)))
    py_compile.compile(str(source), cfile=str(cache), doraise=True)
    compiled_stat = source.stat()
    source.write_bytes(original_source)
    os.utime(
        source,
        ns=(compiled_stat.st_atime_ns, compiled_stat.st_mtime_ns),
    )

    receipt = tmp_path / "cache-rejection-receipt.json"
    exit_code = multiwoz21_module._run_in_fresh_process(
        [
            "--archive",
            str(tmp_path / "archive.zip"),
            "--ucns-source-root",
            str(tmp_path / "ucns"),
            "--output",
            str(tmp_path / "report.json"),
            "--receipt",
            str(receipt),
        ],
        repository_root=repository,
    )

    assert exit_code == 1
    assert json.loads(receipt.read_text(encoding="utf-8"))["error"]["code"] == (
        "EDCM_DIRTY"
    )


def test_isolated_bootstrap_preserves_caller_relative_paths(
    monkeypatch,
    tmp_path: Path,
) -> None:
    repository = _committed_edcm_fixture(tmp_path)
    caller = tmp_path / "caller"
    caller.mkdir()
    monkeypatch.chdir(caller)

    exit_code = multiwoz21_module._run_in_fresh_process(
        [
            "--archive",
            "archive.zip",
            "--ucns-source-root",
            "ucns",
            "--output",
            "report.json",
            "--receipt",
            "receipt.json",
        ],
        repository_root=repository,
    )

    assert exit_code == 1
    assert (caller / "receipt.json").is_file()
    assert not (repository / "receipt.json").exists()


def test_ucns_tree_is_authenticated_before_import(
    monkeypatch,
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "ucns-source"
    module_path = source_root / "src/ucns/__init__.py"
    module_path.parent.mkdir(parents=True)
    module_path.write_text("# fixture\n", encoding="utf-8")
    events: list[str] = []
    module = ModuleType("ucns")
    module.__file__ = str(module_path)
    module.V014_FULL_CORPUS_SCHEMA_ID = (
        multiwoz21_module.UCNS_FULL_CORPUS_SCHEMA_ID
    )
    module.V014_FULL_CORPUS_SCHEMA_VERSION = (
        multiwoz21_module.UCNS_FULL_CORPUS_SCHEMA_VERSION
    )
    for name in UCNSFullCorpusGate._REQUIRED_SURFACES:
        setattr(module, name, lambda *args, **kwargs: None)

    def verify(
        root,
        *,
        require_clean,
        verify_tree=None,
        producer_name="EDCM",
        expected_commit=None,
    ):
        events.append("verify")
        assert verify_tree == "src/ucns"
        assert producer_name == "UCNS"
        return PINNED_UCNS_COMMIT

    def import_module(name):
        events.append("import")
        assert name == "ucns"
        assert "ucns" not in multiwoz21_module.sys.modules
        return module

    class FixtureAdapter:
        def __init__(self, candidate):
            events.append("adapter")
            self._module = candidate

    monkeypatch.setitem(multiwoz21_module.sys.modules, "ucns", ModuleType("ucns"))
    monkeypatch.setattr(multiwoz21_module, "_git_commit", verify)
    monkeypatch.setattr(
        multiwoz21_module.importlib,
        "import_module",
        import_module,
    )
    monkeypatch.setattr(multiwoz21_module, "ActualUCNSAdapter", FixtureAdapter)

    multiwoz21_module._load_pinned_runtime(source_root)

    assert events == ["verify", "import", "adapter"]


def test_sealed_git_identity_disables_replacement_refs(tmp_path: Path) -> None:
    checkout = tmp_path / "edcm"
    checkout.mkdir()
    subprocess.run(["git", "init", str(checkout)], check=True, capture_output=True)
    tracked = checkout / "producer.py"
    tracked.write_text("VALUE = 'trusted'\n", encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(checkout), "add", "producer.py"],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "git",
            "-C",
            str(checkout),
            "-c",
            "user.name=EDCM Test",
            "-c",
            "user.email=edcm-test@example.invalid",
            "commit",
            "-m",
            "trusted fixture",
        ],
        check=True,
        capture_output=True,
    )
    commit = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    tracked.write_text("VALUE = 'altered'\n", encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(checkout), "add", "producer.py"],
        check=True,
        capture_output=True,
    )
    replacement_tree = subprocess.run(
        ["git", "-C", str(checkout), "write-tree"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    replacement_commit = subprocess.run(
        [
            "git",
            "-C",
            str(checkout),
            "-c",
            "user.name=EDCM Test",
            "-c",
            "user.email=edcm-test@example.invalid",
            "commit-tree",
            replacement_tree,
            "-p",
            commit,
            "-m",
            "replacement fixture",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    subprocess.run(
        ["git", "-C", str(checkout), "reset", "--hard", commit],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(checkout), "replace", commit, replacement_commit],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(checkout), "reset", "--hard", commit],
        check=True,
        capture_output=True,
    )
    assert "altered" in tracked.read_text(encoding="utf-8")

    with pytest.raises(CorpusRunError, match="tracked files must be clean"):
        multiwoz21_module._git_commit(checkout, require_clean=True)


def test_sealed_git_identity_rejects_hidden_package_mutation(
    tmp_path: Path,
) -> None:
    checkout = tmp_path / "repository"
    package = checkout / "edcm"
    package.mkdir(parents=True)
    tracked = package / "producer.py"
    tracked.write_text("VALUE = 'trusted'\n", encoding="utf-8")
    subprocess.run(["git", "init", str(checkout)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(checkout), "add", "edcm/producer.py"],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "git",
            "-C",
            str(checkout),
            "-c",
            "user.name=EDCM Test",
            "-c",
            "user.email=edcm-test@example.invalid",
            "commit",
            "-m",
            "trusted fixture",
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "git",
            "-C",
            str(checkout),
            "update-index",
            "--assume-unchanged",
            "--",
            "edcm/producer.py",
        ],
        check=True,
        capture_output=True,
    )
    tracked.write_text("VALUE = 'altered'\n", encoding="utf-8")
    status = subprocess.run(
        ["git", "-C", str(checkout), "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert status == ""

    with pytest.raises(CorpusRunError, match="differs from the sealed commit"):
        multiwoz21_module._git_commit(
            checkout,
            require_clean=True,
            verify_tree="edcm",
        )


def test_edcm_tree_identity_survives_evidence_only_commit(
    tmp_path: Path,
) -> None:
    checkout = tmp_path / "repository"
    package = checkout / "edcm"
    package.mkdir(parents=True)
    (package / "producer.py").write_text(
        "VALUE = 'trusted'\n",
        encoding="utf-8",
    )
    evidence = checkout / "evidence.json"
    evidence.write_text('{"run": 1}\n', encoding="utf-8")
    subprocess.run(["git", "init", str(checkout)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(checkout), "add", "edcm", "evidence.json"],
        check=True,
        capture_output=True,
    )
    commit_command = [
        "git",
        "-C",
        str(checkout),
        "-c",
        "user.name=EDCM Test",
        "-c",
        "user.email=edcm-test@example.invalid",
        "commit",
        "-m",
    ]
    subprocess.run(
        [*commit_command, "producer"],
        check=True,
        capture_output=True,
    )
    producer_commit = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    producer_tree = multiwoz21_module._git_tree_identity(checkout, "edcm")

    evidence.write_text('{"run": 2}\n', encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(checkout), "add", "evidence.json"],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [*commit_command, "evidence"],
        check=True,
        capture_output=True,
    )

    assert multiwoz21_module._git_tree_identity(checkout, "edcm") == (
        producer_tree
    )
    assert multiwoz21_module._git_tree_identity(
        checkout,
        "edcm",
        treeish=producer_commit,
    ) == producer_tree
    with pytest.raises(CorpusRunError, match="changed after sealed snapshot"):
        multiwoz21_module._git_commit(
            checkout,
            require_clean=True,
            verify_tree="edcm",
            expected_commit=producer_commit,
        )


def test_claimed_gate_without_source_exhaustion_cannot_complete(
    tmp_path: Path,
) -> None:
    archive, manifest = _fixture_archive(tmp_path)
    with pytest.raises(CorpusRunError) as caught:
        run_archive(
            archive,
            adapter=FixtureAdapter(),
            full_corpus_gate=NonConsumingFullCorpusGate(),
            edcm_tree="fixture-edcm-tree",
            ucns_commit="fixture-ucns",
            manifest=manifest,
        )
    error = caught.value
    assert error.code == "UCNS_FULL_CORPUS_INCOMPLETE"
    gate = error.state["ucns_full_corpus_gate"]
    assert gate["status"] == "complete"
    assert gate["source_native_reconciliation"]["complete"] is False
    assert gate["source_native_reconciliation"]["turns"] == 0


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
            full_corpus_gate=FixtureFullCorpusGate(),
            edcm_tree="fixture-edcm-tree",
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
            full_corpus_gate=FixtureFullCorpusGate(),
            edcm_tree="fixture-edcm-tree",
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
        full_corpus_gate=FixtureFullCorpusGate(),
        edcm_tree="fixture-edcm-tree",
        ucns_commit="fixture-ucns",
        manifest=manifest,
        checkpoint_path=checkpoint,
        checkpoint_every=1,
    )
    serialized = json.dumps(report, ensure_ascii=False) + json.dumps(receipt)
    serialized += checkpoint.read_text(encoding="utf-8")
    assert "exact café" not in serialized
    assert "line\\nbreak" not in serialized
    assert "ZXQ_SOURCE_SENTINEL_49" not in serialized

    repeated_report, repeated_receipt = run_archive(
        archive,
        adapter=FixtureAdapter(),
        full_corpus_gate=FixtureFullCorpusGate(),
        edcm_tree="fixture-edcm-tree",
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
        full_corpus_gate=UCNSFullCorpusGate(ucns),
        edcm_tree="fixture-edcm-tree",
        ucns_commit=PINNED_UCNS_COMMIT,
        manifest=manifest,
    )
    assert receipt["status"] == "complete"
    assert report["profile"]["profile_id"] == "ucns.profile.edcm-word-gonol"
    assert report["profile"]["source_commit"] == PINNED_UCNS_COMMIT
    gate = report["ucns_full_corpus_gate"]
    assert gate["schema_id"] == "ucns.edcm.full-corpus-execution"
    assert gate["schema_version"] == "0.14.1"
    assert gate["status"] == "complete"
    assert gate["iterator_exhausted"] is True
    assert gate["processed_turn_count"] == 3
    assert (
        gate["exact_source_stream_sha256"]
        == gate["exact_observation_stream_sha256"]
    )
    assert gate["manifest"]["source_artifact_sha256"] == (
        manifest.archive["sha256"]
    )
    assert gate["manifest"]["expected_turn_count"] == 3
    assert gate["receipt"]["selection_effect"] == "none"
    assert gate["receipt"]["edcm_activation"] == "inactive"
    assert gate["receipt"]["metapat_activation"] == "inactive"
    assert gate["source_native_reconciliation"]["complete"] is True
