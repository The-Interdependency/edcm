#!/usr/bin/python3 -I
# === MODULE_BUILD ===
# id: recovered_dissonance_external_evaluator
#   module_name: recovered_dissonance_external_evaluator
#   module_kind: experiment
#   summary: evaluates one frozen aggregate MultiWOZ booking batch with normalized recovered dissonance through the UCNS PR 196 external protocol
#   owner: Erin Spencer
#   public_surface: main
#   internal_surface: canonical request validation, exact rational metric evaluation, aggregate confusion and decision rendering
#   auth_boundary: source custody and disclosure authority are caller supplied and must match the frozen public-source authority identifiers
#   storage_boundary: reads one process-local protocol request and emits one aggregate response; retains no raw text, event locator, per-event label, or per-event score
#   network_boundary: no network code or environment inputs; caller-isolated enforcement remains the harness caller's responsibility
#   user_data_boundary: receives only opaque event commitments, source booking labels, and exact rational kappa trajectories derived from pre-response public-source context
#   admin_only: false
#   tests: tests/test_recovered_dissonance_external_evaluator.py
#   rollout: one preregistered retrospective external-label replay through UCNS PR 196 after an execution-generated full-corpus receipt
#   rollback: remove this evaluator and supersede its unopened packet identity without changing controlled or historical findings
#   requires: recovered_dissonance_controlled_gate, edcm_multiwoz21_booking_outcome_holdout, UCNS PR 196 external evaluation protocol
#   since: 2026-08-17
#   unresolved: measurement validity, independent hidden custody, temporal sampling comparability, label construct validity, and independent replication
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: recovered_dissonance_external_evaluator_is_frozen
#   given: the external evaluator receives a UCNS PR 196 request
#   then: it accepts only the exact plan, evaluator, upstream manifest, command policy, single batch case, source identities, threshold, metric, and class inventory frozen before outcome inspection
#   class: evidence
#   since: 2026-08-17
#
# id: recovered_dissonance_external_evaluator_is_aggregate_only
#   given: the frozen batch is evaluated
#   then: stdout contains only aggregate admission, confusion, metric, and decision evidence without event commitments, per-event labels, trajectories, or scores
#   class: privacy
#   since: 2026-08-17
#
# id: recovered_dissonance_external_evaluator_fails_closed
#   given: structure, identity, custody, disclosure, limits, protocol, or metric admission disagrees with the frozen packet
#   then: structural disagreement exits nonzero for an incomplete UCNS receipt while mathematically undefined admitted rows produce one aggregate UNRESOLVED result
#   class: safety
#   since: 2026-08-17
#
# id: recovered_dissonance_external_evaluator_does_not_promote
#   given: the evaluator emits SURVIVED, FALSIFIED, or UNRESOLVED candidate evidence
#   then: absolute recovered dissonance and the historical MultiWOZ sensitivity remain FALSIFIED, normalized controlled evidence remains SURVIVED, and measurement validity, activation, selection, and canon remain unestablished
#   class: doctrine
#   since: 2026-08-17
# === END CONTRACTS ===

"""Frozen aggregate evaluator for the recovered-dissonance external packet.

The executable reads exactly one UCNS external-evaluator request from standard
input and writes exactly one protocol response to standard output.  It has no
case-production mode and no network or environment input.  Source acquisition,
pre-response trajectory production, disclosure, and the execution-generated
UCNS full-corpus receipt remain separate caller responsibilities.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from math import gcd
import sys
from typing import Any


REQUEST_SCHEMA_ID = "ucns.edcm.external-evaluator-request"
RESPONSE_SCHEMA_ID = "ucns.edcm.external-evaluator-response"
PROTOCOL_VERSION = "1.0.0"
PLAN_ID = "edcm.recovered-dissonance.multiwoz21-test/0.1.0"
PLAN_VERSION = "0.1.0"
QUESTION = (
    "On the frozen MultiWOZ 2.1 test booking-event batch, does normalized "
    "recovered dissonance per accumulated positive pressure at the control-only "
    "threshold 3/5 discriminate Booking-Book from Booking-NoBook under the "
    "preregistered aggregate rule?"
)
EVALUATOR_ID = "edcm.recovered-dissonance.external-batch"
EVALUATOR_VERSION = "0.1.0"
CASE_ID = "multiwoz21-test-booking-batch-v1"
CASE_SCHEMA_ID = "edcm.recovered-dissonance.external-batch-case"
CASE_SCHEMA_VERSION = "0.1.0"
CUSTODY_REFERENCE = (
    "doi:10.17863/CAM.41572;archive-sha256:"
    "d377a176f5ec82dc9f6a97e4653d4eddc6cad917704c1aaaa5a8ee3e79f63a8e"
)
DISCLOSURE_AUTHORITY_ID = "edcm.multiwoz21-public-cc-by-4.0/1.0.0"
ARCHIVE_SHA256 = "d377a176f5ec82dc9f6a97e4653d4eddc6cad917704c1aaaa5a8ee3e79f63a8e"
DATA_MEMBER_SHA256 = "cb88bd0070bf11b04974cee54c84ad16cfee723c86b096bea04d2cebad098d58"
ACTS_MEMBER_SHA256 = "54d02ef40aed0e00e5aa84b62ccf7f23df901d07f54c2376d5e8130909c2546f"
TEST_MEMBER_SHA256 = "56fff5bf8c7b0a64fba8672241a7bdd947c3a58986bf06f46d37f33288f73ce0"
POSITIVE_LABEL = "Booking-Book"
NEGATIVE_LABEL = "Booking-NoBook"
EXPECTED_POSITIVE = 530
EXPECTED_NEGATIVE = 131
EXPECTED_RECORDS = EXPECTED_POSITIVE + EXPECTED_NEGATIVE
CANDIDATE_ID = "edcm.recovered-dissonance.normalized-positive-pressure/0.1.0"
CANDIDATE_FORMULA = (
    "(max(kappa_t)-kappa_final)/sum_t(max(kappa_t-kappa_(t-1),0))"
)
THRESHOLD = Fraction(3, 5)
TIMEOUT_SECONDS = 30
MAX_INPUT_BYTES = 8_388_608
MAX_OUTPUT_BYTES = 65_536

EXPECTED_UPSTREAM_EVIDENCE_IDENTITY = [
    "multiwoz-2.1",
    "2.1",
    ARCHIVE_SHA256,
    "143048",
    "CC-BY-4.0",
    "aggregate-only; raw dialogue text remains in caller-held source custody and outside Git",
    "none-preserve-source; no transformed or redacted substitute is used for exact execution",
    "sha256:aba3ebbac5e6f6ef0505cd9349361ba8bde7586fae21049e2d120fa362033ed6",
    "edcm.corpora.multiwoz21",
    "1.2.0",
    "edcm.corpora.multiwoz21:_iter_ucns_full_corpus_turns",
]

EXPECTED_SOURCE = {
    "archive_sha256": ARCHIVE_SHA256,
    "data_member": "MULTIWOZ2.1/data.json",
    "data_member_sha256": DATA_MEMBER_SHA256,
    "dialogue_acts_member": "MULTIWOZ2.1/dialogue_acts.json",
    "dialogue_acts_member_sha256": ACTS_MEMBER_SHA256,
    "partition": "test",
    "test_membership_member": "MULTIWOZ2.1/testListFile.json",
    "test_membership_member_sha256": TEST_MEMBER_SHA256,
}

EXPECTED_EVENT_CONTRACT = {
    "candidate_context": "exact data.json turns 0 through response_index-1",
    "event_order": "unicode-dialogue-id-ascending-then-decimal-source-turn-id-ascending",
    "expected_negative": EXPECTED_NEGATIVE,
    "expected_positive": EXPECTED_POSITIVE,
    "expected_records": EXPECTED_RECORDS,
    "labelled_response_disclosed_to_candidate": False,
    "negative_label": NEGATIVE_LABEL,
    "positive_label": POSITIVE_LABEL,
    "response_index": "2*decimal-source-turn-id-1",
    "source_labels_are_targets_only": True,
}

EXPECTED_CANDIDATE = {
    "candidate_id": CANDIDATE_ID,
    "direction": "higher-means-more-recovery",
    "formula": CANDIDATE_FORMULA,
    "initial_state": {"denominator": 1, "numerator": 0},
    "kappa_state_encoding": "reduced-nonnegative-rational",
    "minimum_ordered_states": 3,
    "prediction_above_threshold": POSITIVE_LABEL,
    "prediction_below_threshold": NEGATIVE_LABEL,
    "threshold": {"denominator": 5, "numerator": 3},
    "threshold_equality": "UNRESOLVED",
    "zero_accumulated_positive_pressure": "UNRESOLVED",
}


class PacketError(ValueError):
    """A non-outcome disagreement that must make the harness receipt incomplete."""


def _canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise PacketError("canonical-json") from exc


def _sha(value: Any, field: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise PacketError(field)
    try:
        int(value, 16)
    except ValueError as exc:
        raise PacketError(field) from exc
    return value.lower()


def _exact_keys(value: Any, expected: set[str], field: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        raise PacketError(field)
    return value


def _fraction_record(value: Any, field: str) -> Fraction:
    record = _exact_keys(value, {"denominator", "numerator"}, field)
    numerator = record["numerator"]
    denominator = record["denominator"]
    if (
        isinstance(numerator, bool)
        or not isinstance(numerator, int)
        or numerator < 0
        or isinstance(denominator, bool)
        or not isinstance(denominator, int)
        or denominator <= 0
        or gcd(numerator, denominator) != 1
    ):
        raise PacketError(field)
    return Fraction(numerator, denominator)


def _fraction_output(value: Fraction) -> dict[str, int]:
    return {"denominator": value.denominator, "numerator": value.numerator}


def _validate_request(request: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    request = _exact_keys(
        request,
        {
            "cases",
            "evaluator",
            "execution",
            "plan_id",
            "plan_version",
            "question",
            "schema_id",
            "schema_version",
            "upstream",
        },
        "request-fields",
    )
    if (
        request["schema_id"] != REQUEST_SCHEMA_ID
        or request["schema_version"] != PROTOCOL_VERSION
        or request["plan_id"] != PLAN_ID
        or request["plan_version"] != PLAN_VERSION
        or request["question"] != QUESTION
    ):
        raise PacketError("request-identity")

    upstream = _exact_keys(
        request["upstream"],
        {"completion_receipt_id", "corpus_manifest_evidence_identity"},
        "upstream-fields",
    )
    _sha(upstream["completion_receipt_id"], "completion-receipt-id")
    if upstream["corpus_manifest_evidence_identity"] != EXPECTED_UPSTREAM_EVIDENCE_IDENTITY:
        raise PacketError("upstream-manifest")

    evaluator = _exact_keys(
        request["evaluator"],
        {
            "code_reference",
            "evaluator_id",
            "evaluator_version",
            "executable_sha256",
            "protocol_version",
        },
        "evaluator-fields",
    )
    if (
        evaluator["evaluator_id"] != EVALUATOR_ID
        or evaluator["evaluator_version"] != EVALUATOR_VERSION
        or evaluator["protocol_version"] != PROTOCOL_VERSION
        or not isinstance(evaluator["code_reference"], str)
        or not evaluator["code_reference"]
    ):
        raise PacketError("evaluator-identity")
    _sha(evaluator["executable_sha256"], "executable-sha256")

    execution = _exact_keys(
        request["execution"],
        {
            "argv",
            "environment_keys",
            "max_input_bytes",
            "max_output_bytes",
            "network_policy",
            "timeout_seconds",
        },
        "execution-fields",
    )
    if (
        not isinstance(execution["argv"], list)
        or len(execution["argv"]) != 1
        or not isinstance(execution["argv"][0], str)
        or not execution["argv"][0].startswith("/")
        or execution["environment_keys"] != []
        or execution["network_policy"] != "caller-isolated"
        or execution["timeout_seconds"] != TIMEOUT_SECONDS
        or execution["max_input_bytes"] != MAX_INPUT_BYTES
        or execution["max_output_bytes"] != MAX_OUTPUT_BYTES
    ):
        raise PacketError("execution-policy")

    cases = request["cases"]
    if not isinstance(cases, list) or len(cases) != 1:
        raise PacketError("case-count")
    case = _exact_keys(
        cases[0],
        {
            "case_id",
            "custody_reference",
            "disclosure_authority_id",
            "payload",
            "subject_digest",
        },
        "case-fields",
    )
    if (
        case["case_id"] != CASE_ID
        or case["custody_reference"] != CUSTODY_REFERENCE
        or case["disclosure_authority_id"] != DISCLOSURE_AUTHORITY_ID
        or _sha(case["subject_digest"], "subject-digest")
        != sha256(_canonical(case["payload"])).hexdigest()
    ):
        raise PacketError("case-identity")
    return evaluator, cases


def _validate_payload(payload: Any) -> list[dict[str, Any]]:
    payload = _exact_keys(
        payload,
        {"candidate", "event_contract", "records", "schema_id", "schema_version", "source"},
        "payload-fields",
    )
    if (
        payload["schema_id"] != CASE_SCHEMA_ID
        or payload["schema_version"] != CASE_SCHEMA_VERSION
        or payload["source"] != EXPECTED_SOURCE
        or payload["event_contract"] != EXPECTED_EVENT_CONTRACT
        or payload["candidate"] != EXPECTED_CANDIDATE
    ):
        raise PacketError("payload-identity")
    records = payload["records"]
    if not isinstance(records, list) or len(records) != EXPECTED_RECORDS:
        raise PacketError("record-count")
    commitments: set[str] = set()
    labels: Counter[str] = Counter()
    normalized: list[dict[str, Any]] = []
    for record in records:
        record = _exact_keys(record, {"event_commitment", "kappa", "label"}, "record-fields")
        commitment = _sha(record["event_commitment"], "event-commitment")
        if commitment in commitments:
            raise PacketError("event-commitment-uniqueness")
        commitments.add(commitment)
        label = record["label"]
        if label not in {POSITIVE_LABEL, NEGATIVE_LABEL}:
            raise PacketError("source-label")
        labels[label] += 1
        kappa = record["kappa"]
        if not isinstance(kappa, list):
            raise PacketError("kappa-shape")
        values = tuple(
            _fraction_record(value, "kappa-state") for value in kappa
        )
        if values and values[0] != 0:
            raise PacketError("initial-kappa-state")
        normalized.append({"label": label, "kappa": values})
    if labels != Counter({POSITIVE_LABEL: EXPECTED_POSITIVE, NEGATIVE_LABEL: EXPECTED_NEGATIVE}):
        raise PacketError("class-inventory")
    return normalized


def _score(values: tuple[Fraction, ...]) -> tuple[Fraction | None, str | None]:
    if len(values) < 3:
        return None, "fewer-than-three-states"
    recovered = max(values) - values[-1]
    pressure = sum(
        (max(current - previous, Fraction(0)) for previous, current in zip(values, values[1:])),
        Fraction(0),
    )
    if pressure == 0:
        return None, "zero-positive-pressure"
    score = recovered / pressure
    if score < 0 or score > 1:
        raise PacketError("normalized-score-range")
    if score == THRESHOLD:
        return None, "threshold-equality"
    return score, None


def _evaluate(records: list[dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    unresolved: Counter[str] = Counter()
    counts = {
        "false_negative": 0,
        "false_positive": 0,
        "true_negative": 0,
        "true_positive": 0,
    }
    for record in records:
        score, reason = _score(record["kappa"])
        if reason is not None:
            unresolved[reason] += 1
            continue
        predicted_positive = score > THRESHOLD
        actual_positive = record["label"] == POSITIVE_LABEL
        if predicted_positive and actual_positive:
            counts["true_positive"] += 1
        elif predicted_positive:
            counts["false_positive"] += 1
        elif actual_positive:
            counts["false_negative"] += 1
        else:
            counts["true_negative"] += 1

    common = {
        "absolute_recovered_dissonance_status": "FALSIFIED",
        "candidate_id": CANDIDATE_ID,
        "controlled_normalized_status": "SURVIVED",
        "evaluated_records": EXPECTED_RECORDS - sum(unresolved.values()),
        "expected_records": EXPECTED_RECORDS,
        "historical_multiwoz_sensitivity_status": "FALSIFIED",
        "measurement_validity": "not-established",
        "threshold": _fraction_output(THRESHOLD),
        "unresolved_by_reason": dict(sorted(unresolved.items())),
    }
    if unresolved:
        return "unresolved", {
            **common,
            "decision": "UNRESOLVED",
            "decision_rule": "all records must admit a strict-threshold prediction",
        }

    sensitivity = Fraction(
        counts["true_positive"], counts["true_positive"] + counts["false_negative"]
    )
    specificity = Fraction(
        counts["true_negative"], counts["true_negative"] + counts["false_positive"]
    )
    balanced_accuracy = (sensitivity + specificity) / 2
    survived = sensitivity >= Fraction(1, 2) and specificity >= Fraction(1, 2) and balanced_accuracy > Fraction(1, 2)
    return "ok", {
        **common,
        "balanced_accuracy": _fraction_output(balanced_accuracy),
        "confusion_counts": counts,
        "decision": "SURVIVED" if survived else "FALSIFIED",
        "decision_rule": "sensitivity>=1/2 and specificity>=1/2 and balanced_accuracy>1/2",
        "sensitivity": _fraction_output(sensitivity),
        "specificity": _fraction_output(specificity),
    }


def _response(request: Any) -> dict[str, Any]:
    evaluator, cases = _validate_request(request)
    records = _validate_payload(cases[0]["payload"])
    status, output = _evaluate(records)
    return {
        "evaluator": {
            "evaluator_id": evaluator["evaluator_id"],
            "evaluator_version": evaluator["evaluator_version"],
        },
        "plan_id": request["plan_id"],
        "results": [
            {
                "case_id": CASE_ID,
                "error": None,
                "evidence": [
                    "aggregate-only MultiWOZ 2.1 test booking-event replay",
                    "frozen normalized recovered-dissonance metric and 3/5 threshold",
                    "measurement validity remains not-established",
                ],
                "output": output,
                "status": status,
            }
        ],
        "schema_id": RESPONSE_SCHEMA_ID,
        "schema_version": PROTOCOL_VERSION,
    }


def main() -> int:
    try:
        request = json.load(sys.stdin)
        response = _response(request)
        sys.stdout.buffer.write(_canonical(response))
        return 0
    except (PacketError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        code = str(exc) if isinstance(exc, PacketError) else "request-json"
        sys.stderr.write(f"recovered-dissonance-external-evaluator: {code}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
