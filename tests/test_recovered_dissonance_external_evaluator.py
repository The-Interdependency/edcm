"""Contract checks for the frozen recovered-dissonance external evaluator."""

from __future__ import annotations

# === CHECKS ===
# id: check_recovered_dissonance_external_evaluator_frozen
#   proves: recovered_dissonance_external_evaluator_is_frozen
#   call: self::test_frozen_request_emits_only_aggregate_survival
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_recovered_dissonance_external_evaluator_aggregate_only
#   proves: recovered_dissonance_external_evaluator_is_aggregate_only
#   call: self::test_frozen_request_emits_only_aggregate_survival
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_recovered_dissonance_external_evaluator_failure_propagation
#   proves: recovered_dissonance_external_evaluator_fails_closed
#   call: self::test_structural_drift_exits_nonzero_and_metric_undefined_is_unresolved
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_recovered_dissonance_external_evaluator_nonpromotion
#   proves: recovered_dissonance_external_evaluator_does_not_promote
#   call: self::test_frozen_request_emits_only_aggregate_survival
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_recovered_dissonance_external_packet_identity
#   proves: recovered_dissonance_external_evaluator_is_frozen, recovered_dissonance_external_evaluator_does_not_promote
#   call: self::test_packet_pins_executable_protocol_and_nonpromotion
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess

import pytest

from edcm import recovered_dissonance_external_evaluator as evaluator


ROOT = Path(__file__).resolve().parents[1]
EXECUTABLE = ROOT / "edcm" / "recovered_dissonance_external_evaluator.py"
PACKET = ROOT / "docs" / "experiments" / (
    "2026-08-17-recovered-dissonance-external-evaluation-packet.json"
)


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _state(value: int) -> dict[str, int]:
    return {"denominator": 1, "numerator": value}


def _records() -> list[dict[str, object]]:
    records = []
    for index in range(evaluator.EXPECTED_POSITIVE):
        records.append(
            {
                "event_commitment": sha256(f"positive-{index}".encode()).hexdigest(),
                "kappa": [_state(0), _state(1), _state(0)],
                "label": evaluator.POSITIVE_LABEL,
            }
        )
    for index in range(evaluator.EXPECTED_NEGATIVE):
        records.append(
            {
                "event_commitment": sha256(f"negative-{index}".encode()).hexdigest(),
                "kappa": [_state(0), _state(1), _state(1)],
                "label": evaluator.NEGATIVE_LABEL,
            }
        )
    return records


def _request() -> dict[str, object]:
    payload = {
        "candidate": deepcopy(evaluator.EXPECTED_CANDIDATE),
        "event_contract": deepcopy(evaluator.EXPECTED_EVENT_CONTRACT),
        "records": _records(),
        "schema_id": evaluator.CASE_SCHEMA_ID,
        "schema_version": evaluator.CASE_SCHEMA_VERSION,
        "source": deepcopy(evaluator.EXPECTED_SOURCE),
    }
    executable_digest = sha256(EXECUTABLE.read_bytes()).hexdigest()
    return {
        "cases": [
            {
                "case_id": evaluator.CASE_ID,
                "custody_reference": evaluator.CUSTODY_REFERENCE,
                "disclosure_authority_id": evaluator.DISCLOSURE_AUTHORITY_ID,
                "payload": payload,
                "subject_digest": sha256(_canonical(payload)).hexdigest(),
            }
        ],
        "evaluator": {
            "code_reference": "fixture:exact-evaluator-bytes",
            "evaluator_id": evaluator.EVALUATOR_ID,
            "evaluator_version": evaluator.EVALUATOR_VERSION,
            "executable_sha256": executable_digest,
            "protocol_version": evaluator.PROTOCOL_VERSION,
        },
        "execution": {
            "argv": [str(EXECUTABLE.resolve())],
            "environment_keys": [],
            "max_input_bytes": evaluator.MAX_INPUT_BYTES,
            "max_output_bytes": evaluator.MAX_OUTPUT_BYTES,
            "network_policy": "caller-isolated",
            "timeout_seconds": evaluator.TIMEOUT_SECONDS,
        },
        "plan_id": evaluator.PLAN_ID,
        "plan_version": evaluator.PLAN_VERSION,
        "question": evaluator.QUESTION,
        "schema_id": evaluator.REQUEST_SCHEMA_ID,
        "schema_version": evaluator.PROTOCOL_VERSION,
        "upstream": {
            "completion_receipt_id": "a" * 64,
            "corpus_manifest_evidence_identity": list(
                evaluator.EXPECTED_UPSTREAM_EVIDENCE_IDENTITY
            ),
        },
    }


def _run(request: dict[str, object]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [str(EXECUTABLE.resolve())],
        check=False,
        input=_canonical(request),
        capture_output=True,
        env={},
        timeout=10,
    )


def test_frozen_request_emits_only_aggregate_survival() -> None:
    completed = _run(_request())
    assert completed.returncode == 0
    assert completed.stderr == b""
    response = json.loads(completed.stdout)
    assert response["schema_id"] == evaluator.RESPONSE_SCHEMA_ID
    result = response["results"][0]
    assert result["status"] == "ok"
    assert result["output"]["decision"] == "SURVIVED"
    assert result["output"]["sensitivity"] == {"denominator": 1, "numerator": 1}
    assert result["output"]["specificity"] == {"denominator": 1, "numerator": 1}
    assert result["output"]["balanced_accuracy"] == {"denominator": 1, "numerator": 1}
    assert result["output"]["absolute_recovered_dissonance_status"] == "FALSIFIED"
    assert result["output"]["controlled_normalized_status"] == "SURVIVED"
    assert result["output"]["historical_multiwoz_sensitivity_status"] == "FALSIFIED"
    assert result["output"]["measurement_validity"] == "not-established"
    rendered = completed.stdout.decode("utf-8")
    for forbidden in ("event_commitment", "kappa", "positive-0", "negative-0"):
        assert forbidden not in rendered


def test_structural_drift_exits_nonzero_and_metric_undefined_is_unresolved() -> None:
    drifted = _request()
    drifted["execution"]["timeout_seconds"] = 31  # type: ignore[index]
    completed = _run(drifted)
    assert completed.returncode == 2
    assert completed.stdout == b""
    assert completed.stderr == b"recovered-dissonance-external-evaluator: execution-policy\n"

    unresolved = _request()
    first = unresolved["cases"][0]["payload"]["records"][0]  # type: ignore[index]
    first["kappa"] = [_state(0), _state(0), _state(0)]
    payload = unresolved["cases"][0]["payload"]  # type: ignore[index]
    unresolved["cases"][0]["subject_digest"] = sha256(_canonical(payload)).hexdigest()  # type: ignore[index]
    completed = _run(unresolved)
    assert completed.returncode == 0
    result = json.loads(completed.stdout)["results"][0]
    assert result["status"] == "unresolved"
    assert result["output"]["decision"] == "UNRESOLVED"
    assert result["output"]["unresolved_by_reason"] == {"zero-positive-pressure": 1}


@pytest.mark.parametrize(
    "mutation",
    (
        "subject-digest",
        "class-inventory",
        "duplicate-commitment",
        "candidate-formula",
        "upstream-manifest",
    ),
)
def test_identity_and_inventory_disagreement_fail_closed(mutation: str) -> None:
    request = _request()
    case = request["cases"][0]  # type: ignore[index]
    payload = case["payload"]
    records = payload["records"]
    if mutation == "subject-digest":
        case["subject_digest"] = "0" * 64
    elif mutation == "class-inventory":
        records[0]["label"] = evaluator.NEGATIVE_LABEL
        case["subject_digest"] = sha256(_canonical(payload)).hexdigest()
    elif mutation == "duplicate-commitment":
        records[1]["event_commitment"] = records[0]["event_commitment"]
        case["subject_digest"] = sha256(_canonical(payload)).hexdigest()
    elif mutation == "candidate-formula":
        payload["candidate"] = deepcopy(evaluator.EXPECTED_CANDIDATE)
        payload["candidate"]["formula"] = "outcome-tuned"
        case["subject_digest"] = sha256(_canonical(payload)).hexdigest()
    else:
        request["upstream"]["corpus_manifest_evidence_identity"][0] = "other"  # type: ignore[index]
    assert _run(request).returncode == 2


def test_packet_pins_executable_protocol_and_nonpromotion() -> None:
    packet = json.loads(PACKET.read_text(encoding="utf-8"))
    assert packet["schema"] == "edcm.recovered-dissonance.external-evaluation-packet/0.1.0"
    assert packet["freeze"]["selectable_fields_frozen"] is True
    assert packet["freeze"]["external_case_generated"] is False
    assert packet["freeze"]["external_outcome_labels_inspected"] is False
    assert packet["evaluator"] == {
        "code_reference": "The-Interdependency/edcm@14e2c16c8fa76f994afe9939e1a2e2a2bfcd5414:edcm/recovered_dissonance_external_evaluator.py",
        "evaluator_id": evaluator.EVALUATOR_ID,
        "evaluator_version": evaluator.EVALUATOR_VERSION,
        "executable_sha256": sha256(EXECUTABLE.read_bytes()).hexdigest(),
        "protocol_version": evaluator.PROTOCOL_VERSION,
    }
    assert packet["plan"] == {
        "plan_id": evaluator.PLAN_ID,
        "plan_version": evaluator.PLAN_VERSION,
        "question": evaluator.QUESTION,
    }
    assert packet["execution"]["timeout_seconds"] == evaluator.TIMEOUT_SECONDS
    assert packet["execution"]["max_input_bytes"] == evaluator.MAX_INPUT_BYTES
    assert packet["execution"]["max_output_bytes_per_stream"] == evaluator.MAX_OUTPUT_BYTES
    assert packet["upstream_corpus_receipt"]["required_manifest_evidence_identity"] == evaluator.EXPECTED_UPSTREAM_EVIDENCE_IDENTITY
    assert packet["prior_statuses"] == {
        "absolute_recovered_dissonance": "FALSIFIED",
        "historical_multiwoz_sensitivity_at_least_0_50": "FALSIFIED",
        "historical_multiwoz_report_digest": "a726434a533395e7e3bd7d72ba3e9ce68f58c5b62f3b6b10d2b0556b09e85e61",
        "measurement_validity": "not-established",
        "normalized_recovered_dissonance_per_accumulated_positive_pressure_controlled_gate": "SURVIVED",
    }
    assert packet["evidence_receipt_requirements"]["receipt_nonpromotion"] == {
        "canon_status": "none",
        "edcm_activation": "inactive",
        "evidence_status": "candidate-measured-evidence",
        "measurement_validity": "not-established",
        "selection_effect": "none",
    }
