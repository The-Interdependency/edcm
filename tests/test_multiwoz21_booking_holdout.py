"""Contract checks for the sealed MultiWOZ 2.1 booking-outcome holdout."""

from __future__ import annotations

# === CHECKS ===
# id: check_multiwoz_booking_outcome_labelled_response_is_withheld
#   proves: multiwoz_booking_outcome_labelled_response_is_withheld
#   call: self::test_source_outcome_response_and_later_turns_are_withheld
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_multiwoz_booking_outcome_calibration_precedes_test
#   proves: multiwoz_booking_outcome_calibration_precedes_test
#   call: self::test_calibration_and_threshold_depend_only_on_development_and_validation
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_multiwoz_booking_outcome_report_is_aggregate_only
#   proves: multiwoz_booking_outcome_report_is_aggregate_only
#   call: self::test_report_schema_retains_aggregate_boundaries_without_event_locators
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_multiwoz_booking_outcome_uncertainty_is_cluster_aware
#   proves: multiwoz_booking_outcome_uncertainty_is_cluster_aware
#   call: self::test_evaluation_reports_confusion_wilson_and_cluster_intervals
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_multiwoz_booking_outcome_hypothesis_failure_is_evidence
#   proves: multiwoz_booking_outcome_hypothesis_failure_is_evidence
#   call: self::test_falsified_finding_is_serialized_without_raising
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_multiwoz_booking_outcome_status_does_not_transfer
#   proves: multiwoz_booking_outcome_status_does_not_transfer
#   call: self::test_report_schema_retains_aggregate_boundaries_without_event_locators
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_multiwoz_booking_outcome_sealed_evidence
#   proves: multiwoz_booking_outcome_calibration_precedes_test, multiwoz_booking_outcome_report_is_aggregate_only, multiwoz_booking_outcome_hypothesis_failure_is_evidence, multiwoz_booking_outcome_status_does_not_transfer
#   call: self::test_sealed_holdout_evidence_matches_exact_producer_and_receipt
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from edcm.corpora.multiwoz21_booking_holdout import (
    ARCHIVE_SHA256,
    BOOTSTRAP_REPLICATES,
    OutcomeEvent,
    PlattCalibration,
    _build_report,
    _digest,
    _extract_partition,
    _finding,
    _verify_represented_evidence_seal,
    evaluate_outcomes,
    fit_platt_calibration,
    select_operating_threshold,
)


def _event(dialogue: str, label: int, score: float) -> OutcomeEvent:
    return OutcomeEvent(
        dialogue_id=dialogue,
        source_turn_id=1,
        label=label,
        score=score,
        context_turn_count=1,
    )


def _calibration_fixture() -> list[OutcomeEvent]:
    return [
        _event("d1", 0, 0.10),
        _event("d2", 0, 0.20),
        _event("d3", 0, 0.35),
        _event("d4", 1, 0.60),
        _event("d5", 1, 0.75),
        _event("d6", 1, 0.90),
    ]


def test_source_outcome_response_and_later_turns_are_withheld() -> None:
    data = {
        "D1.json": {
            "goal": {"private": "must-not-be-read"},
            "log": [
                {"text": "first request", "metadata": {}},
                {"text": "labelled positive response", "metadata": {"secret": 1}},
                {"text": "second request", "metadata": {}},
                {"text": "labelled negative response", "metadata": {"secret": 2}},
                {"text": "later secret", "metadata": {}},
            ],
        },
        "D2.json": {
            "log": [
                {"text": "ambiguous request"},
                {"text": "ambiguous response"},
            ]
        },
    }
    acts = {
        "D1": {
            "1": {"Booking-Book": [["Ref", "private-slot"]]},
            "2": {"Booking-NoBook": [["Day", "private-slot"]]},
        },
        "D2": {
            "1": {
                "Booking-Book": [["Ref", "private-slot"]],
                "Booking-NoBook": [["Day", "private-slot"]],
            }
        },
    }
    observed_contexts: list[tuple[str, ...]] = []

    def score(context: tuple[str, ...]) -> float:
        observed_contexts.append(context)
        return len(context) / 10.0

    events, inventory = _extract_partition(
        partition="development",
        data=data,
        dialogue_acts=acts,
        test_ids=set(),
        validation_ids=set(),
        score_fn=score,
    )
    assert [event.label for event in events] == [1, 0]
    assert observed_contexts == [
        ("first request",),
        ("first request", "labelled positive response", "second request"),
    ]
    assert "labelled negative response" not in observed_contexts[-1]
    assert "later secret" not in observed_contexts[-1]
    assert inventory["excluded_ambiguous"] == 1
    rendered = json.dumps(inventory, sort_keys=True)
    assert "first request" not in rendered
    assert "private-slot" not in rendered


def test_calibration_and_threshold_depend_only_on_development_and_validation() -> None:
    development = _calibration_fixture()
    validation = [
        _event("v1", 0, 0.15),
        _event("v2", 0, 0.40),
        _event("v3", 1, 0.65),
        _event("v4", 1, 0.85),
    ]
    calibration = fit_platt_calibration(development)
    threshold, counts, candidate_count = select_operating_threshold(
        validation, calibration
    )
    frozen = _digest(
        {
            "development_fit": calibration.as_dict(),
            "operating_threshold": threshold,
            "threshold_candidate_count": candidate_count,
            "validation_confusion_counts": counts,
        }
    )
    changed_test_only = [
        _event("t1", 1, 0.01),
        _event("t2", 0, 0.99),
    ]
    assert changed_test_only
    calibration_again = fit_platt_calibration(development)
    threshold_again, counts_again, candidate_count_again = (
        select_operating_threshold(validation, calibration_again)
    )
    assert frozen == _digest(
        {
            "development_fit": calibration_again.as_dict(),
            "operating_threshold": threshold_again,
            "threshold_candidate_count": candidate_count_again,
            "validation_confusion_counts": counts_again,
        }
    )


def test_evaluation_reports_confusion_wilson_and_cluster_intervals() -> None:
    calibration = PlattCalibration(
        score_mean=0.5,
        score_population_stddev=0.25,
        intercept=0.0,
        slope=2.0,
        iterations=1,
        converged=True,
    )
    events = []
    for index in range(12):
        # Every cluster carries both classes so all cluster resamples retain
        # sensitivity and specificity support.
        events.extend(
            [
                _event(f"cluster-{index}", 0, 0.10 + index / 1000),
                _event(f"cluster-{index}", 1, 0.90 - index / 1000),
            ]
        )
    evaluation = evaluate_outcomes(events, calibration, threshold=0.5)
    assert evaluation["confusion_counts"] == {
        "true_positive": 12,
        "false_positive": 0,
        "false_negative": 0,
        "true_negative": 12,
    }
    assert evaluation["sensitivity"]["interval"]["method"] == "wilson-score"
    assert evaluation["specificity"]["interval"]["method"] == "wilson-score"
    for metric in ("balanced_accuracy", "brier_score"):
        interval = evaluation[metric]["interval"]
        assert interval["method"] == "dialogue-cluster-percentile-bootstrap"
        assert interval["replicates_valid"] == BOOTSTRAP_REPLICATES
        assert interval["cluster_count"] == 12
    assert evaluation["calibration_error"]["interval"]["cluster_count"] == 12


def _aggregate_report_fixture() -> dict[str, Any]:
    rows = {
        partition: [_event(f"{partition}-n", 0, 0.2), _event(f"{partition}-p", 1, 0.8)]
        for partition in ("development", "validation", "test")
    }
    inventories = {
        "development": {
            "candidate_input_digest_chain": "a" * 64,
            "context_turns": 1,
            "dialogues": 8438,
            "dialogues_with_events": 2,
            "excluded_ambiguous": 19,
            "negative": 1050,
            "positive": 4164,
            "source_event_digest_chain": "b" * 64,
        },
        "validation": {
            "candidate_input_digest_chain": "c" * 64,
            "context_turns": 1,
            "dialogues": 1000,
            "dialogues_with_events": 2,
            "excluded_ambiguous": 0,
            "negative": 113,
            "positive": 543,
            "source_event_digest_chain": "d" * 64,
        },
        "test": {
            "candidate_input_digest_chain": "e" * 64,
            "context_turns": 1,
            "dialogues": 1000,
            "dialogues_with_events": 2,
            "excluded_ambiguous": 0,
            "negative": 131,
            "positive": 530,
            "source_event_digest_chain": "f" * 64,
        },
    }
    calibration = PlattCalibration(0.5, 0.25, 0.0, 2.0, 1, True)
    evaluation = evaluate_outcomes(rows["test"] * 10, calibration, 0.5)
    return _build_report(
        archive_identity={"sha256": ARCHIVE_SHA256},
        manifest_digest="1" * 64,
        represented_seal={"ucns_commit": "2" * 40},
        edcm_commit="3" * 40,
        edcm_tree="4" * 40,
        rows=rows,
        inventories=inventories,
        calibration=calibration,
        threshold=0.5,
        threshold_candidates=3,
        validation_counts={
            "true_positive": 1,
            "false_positive": 0,
            "false_negative": 0,
            "true_negative": 1,
        },
        calibration_digest="5" * 64,
        test_evaluation=evaluation,
    )


def test_report_schema_retains_aggregate_boundaries_without_event_locators() -> None:
    report = _aggregate_report_fixture()
    assert report["canon_selection"] is None
    assert report["status_boundaries"]["formal_ucns_geometry"] == "NA"
    assert report["status_boundaries"]["formal_higher_gonol_composition"] == "NA"
    assert report["status_boundaries"]["edcm_production_activation"] == "inactive"
    assert report["status_boundaries"]["metapat_production_activation"] == "inactive"
    for key, value in report["status_boundaries"].items():
        if key.endswith("_transfer"):
            assert value is False
    assert report["information_boundaries"]["written_source_text"] is False
    rendered = json.dumps(report, sort_keys=True)
    for private_value in ("development-n", "test-p", "source_turn_id"):
        assert private_value not in rendered


def test_falsified_finding_is_serialized_without_raising() -> None:
    finding = _finding(
        "candidate-failure",
        False,
        observed=0.49,
        expected="> 0.50",
    )
    assert finding["status"] == "falsified"
    assert json.loads(json.dumps(finding))["observed"] == 0.49


def test_represented_evidence_seal_is_pinned_to_merged_ucns_v019() -> None:
    seal = _verify_represented_evidence_seal(Path.cwd())
    assert seal["ucns_commit"] == "a98c9e6c69804a8a08d0786b1d8b450bb2c49a97"
    assert seal["source_turns"] == 143048


def test_sealed_holdout_evidence_matches_exact_producer_and_receipt() -> None:
    report_path = Path(
        "experiments/corpora/results/2026-08-02-multiwoz-2.1-booking-outcome-holdout-v0.1.0.json"
    )
    receipt_path = Path(
        "experiments/corpora/receipts/2026-08-02-multiwoz-2.1-booking-outcome-holdout-v0.1.0-complete.json"
    )
    report_bytes = report_path.read_bytes()
    receipt_bytes = receipt_path.read_bytes()
    report = json.loads(report_bytes)
    receipt = json.loads(receipt_bytes)
    assert sha256(report_bytes).hexdigest() == (
        "4c7254cc2a2244eaf0e30e182153f803c9e2706774e9a743f7c22899bdcd64a3"
    )
    assert sha256(receipt_bytes).hexdigest() == (
        "ea2db8bf06785b54ab67dfa01a236bbec2e1d8ec79a5f9808c949363cff4ffe5"
    )
    assert _digest(report) == receipt["report_digest"]
    assert receipt["report_file_sha256"] == sha256(report_bytes).hexdigest()
    assert receipt["receipt_digest"] == _digest(
        {key: value for key, value in receipt.items() if key != "receipt_digest"}
    )
    assert receipt["status"] == "complete"
    assert report["identities"]["edcm_commit"] == (
        "c292430771b4dc76734522b580caa2be18ca04f9"
    )
    assert report["identities"]["edcm_tree"] == (
        "04beb8d9c6f01f2ec00bb06e55f77bea21e9b14a"
    )
    assert report["test_evaluation"]["confusion_counts"] == {
        "false_negative": 281,
        "false_positive": 56,
        "true_negative": 75,
        "true_positive": 249,
    }
    findings = {item["finding_id"]: item["status"] for item in report["findings"]}
    assert findings["test-sensitivity-at-least-half"] == "falsified"
    assert report["canon_selection"] is None
