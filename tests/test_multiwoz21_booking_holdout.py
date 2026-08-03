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
#
# id: check_multiwoz_booking_outcome_runtime_matches_recorded_checkout
#   proves: multiwoz_booking_outcome_runtime_matches_recorded_checkout
#   call: self::test_runtime_binding_rejects_a_foreign_score_helper
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_multiwoz_booking_outcome_repeat_requires_complete_execution
#   proves: multiwoz_booking_outcome_repeat_requires_complete_execution
#   call: self::test_single_run_leaves_complete_repeat_not_evaluated
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_multiwoz_booking_outcome_destinations_do_not_collide
#   proves: multiwoz_booking_outcome_destinations_do_not_collide
#   call: self::test_output_destinations_reject_aliases_before_any_write
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from hashlib import sha256
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace
from typing import Any

import pytest

import edcm.corpora.multiwoz21_booking_holdout as holdout
from edcm.corpora.multiwoz21_booking_holdout import (
    ARCHIVE_SHA256,
    BOOTSTRAP_REPLICATES,
    OutcomeHoldoutError,
    OutcomeEvent,
    PlattCalibration,
    _build_report,
    _digest,
    _extract_partition,
    _finding,
    _require_distinct_output_destinations,
    _verify_represented_evidence_seal,
    _verify_runtime_checkout,
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


def test_runtime_binding_authenticates_the_loaded_package_tree(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: dict[str, Any] = {}

    def verify_tree(root: Path, pathspec: str, **kwargs: Any) -> None:
        observed.update({"pathspec": pathspec, "root": root, **kwargs})

    monkeypatch.setattr(holdout, "_verify_git_tree", verify_tree)
    _verify_runtime_checkout(Path.cwd(), "a" * 40)
    assert observed["root"] == Path.cwd()
    assert observed["pathspec"] == "edcm"
    assert observed["treeish"] == "a" * 40
    assert observed["producer_name"] == "EDCM_RUNTIME"
    assert observed["observed_root"] == Path(holdout.__file__).resolve().parents[2]


def test_runtime_binding_accepts_the_exact_recorded_checkout() -> None:
    commit = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD^{commit}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    _verify_runtime_checkout(Path.cwd(), commit)


def test_runtime_binding_rejects_a_mixed_measurement_import(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def foreign_compute(*args: Any, **kwargs: Any) -> list[Any]:
        return []

    monkeypatch.setattr(holdout, "compute_transcript", foreign_compute)
    with pytest.raises(OutcomeHoldoutError) as raised:
        _verify_runtime_checkout(Path.cwd(), "a" * 40)
    assert raised.value.code == "RUNTIME_CHECKOUT_IDENTITY"


@pytest.mark.parametrize(
    ("module_name", "helper_name"),
    (
        ("_measurement_compute_module", "novelty"),
        ("_measurement_compute_module", "fixation_risk"),
        ("_measurement_risk_module", "clamp"),
    ),
    ids=("compute-stats", "compute-risk", "risk-stats"),
)
def test_runtime_binding_rejects_a_foreign_score_helper(
    monkeypatch: pytest.MonkeyPatch,
    module_name: str,
    helper_name: str,
) -> None:
    def foreign_helper(*args: Any, **kwargs: Any) -> float:
        return 0.0

    module = getattr(holdout, module_name)
    monkeypatch.setattr(module, helper_name, foreign_helper)
    with pytest.raises(OutcomeHoldoutError) as raised:
        _verify_runtime_checkout(Path.cwd(), "a" * 40)
    assert raised.value.code == "RUNTIME_CHECKOUT_IDENTITY"


def test_run_holdout_reverifies_one_in_memory_canon_after_scoring(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []
    loaded_canon = object()

    monkeypatch.setattr(holdout, "_git_commit", lambda *args, **kwargs: "a" * 40)
    monkeypatch.setattr(
        holdout,
        "_verify_runtime_checkout",
        lambda *args, **kwargs: events.append("verify"),
    )

    def load_canon() -> object:
        events.append("canon-load")
        return loaded_canon

    monkeypatch.setattr(holdout, "CanonLoader", load_canon)
    monkeypatch.setattr(holdout, "_git_tree_identity", lambda *args, **kwargs: "b" * 40)
    monkeypatch.setattr(holdout, "_verify_represented_evidence_seal", lambda root: {})
    monkeypatch.setattr(
        holdout,
        "load_admission_manifest",
        lambda: SimpleNamespace(
            digest="c" * 64,
            source={
                "data_member": "data.json",
                "test_member": "test.txt",
                "validation_member": "validation.txt",
            },
        ),
    )

    class FakeArchive:
        def close(self) -> None:
            events.append("archive-close")

    monkeypatch.setattr(
        holdout,
        "_archive_identity",
        lambda *args, **kwargs: ({"sha256": "d" * 64}, FakeArchive()),
    )
    monkeypatch.setattr(holdout, "_load_partition_ids", lambda *args: set())
    source_rows = {str(index): {} for index in range(10438)}
    monkeypatch.setattr(holdout, "_load_json_member", lambda *args: source_rows)

    def candidate_score(context: tuple[str, ...], *, canon: object) -> float:
        assert context == ("turn",)
        assert canon is loaded_canon
        events.append("score")
        return 0.5

    monkeypatch.setattr(holdout, "_candidate_score", candidate_score)

    def extract(*, partition: str, score_fn: Any, **kwargs: Any) -> tuple[Any, Any]:
        score = score_fn(("turn",))
        return (
            [_event(f"{partition}-dialogue", 1, score)],
            {
                "candidate_input_digest_chain": "e" * 64,
                "source_event_digest_chain": "f" * 64,
            },
        )

    monkeypatch.setattr(holdout, "_extract_partition", extract)
    monkeypatch.setattr(holdout, "_require_expected_inventory", lambda *args: None)
    calibration = PlattCalibration(0.5, 0.1, 0.0, 1.0, 1, True)
    monkeypatch.setattr(holdout, "fit_platt_calibration", lambda rows: calibration)
    monkeypatch.setattr(
        holdout,
        "select_operating_threshold",
        lambda rows, fitted: (0.5, {}, 1),
    )
    monkeypatch.setattr(holdout, "evaluate_outcomes", lambda *args: {})
    monkeypatch.setattr(
        holdout,
        "_build_report",
        lambda **kwargs: {
            "findings": [],
            "work_graph": {"work_graph_sha256": "1" * 64},
        },
    )

    report, receipt = holdout.run_holdout(
        archive_path=tmp_path / "source.zip",
        repository_root=tmp_path,
        edcm_commit="a" * 40,
    )

    assert report["findings"] == []
    assert receipt["status"] == "complete"
    assert events == [
        "verify",
        "canon-load",
        "verify",
        "archive-close",
        "score",
        "score",
        "score",
        "verify",
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


def test_single_run_leaves_complete_repeat_not_evaluated() -> None:
    report = _aggregate_report_fixture()
    repeat = next(
        finding
        for finding in report["findings"]
        if finding["finding_id"] == "byte-identical-render-repeat"
    )
    assert repeat == {
        "expected": "a separate complete execution produces the same aggregate report",
        "finding_id": "byte-identical-render-repeat",
        "observed": None,
        "status": "not-evaluated",
    }


def test_output_destinations_reject_aliases_before_any_write(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    ordinary_report = tmp_path / "report.json"
    ordinary_receipt = tmp_path / "receipt.json"
    ordinary_archive = tmp_path / "source.zip"
    ordinary_archive.write_bytes(b"source archive")
    _require_distinct_output_destinations(
        ordinary_report,
        ordinary_receipt,
        archive_path=ordinary_archive,
    )

    with pytest.raises(OutcomeHoldoutError) as identical:
        _require_distinct_output_destinations(ordinary_report, ordinary_report)
    assert identical.value.code == "OUTPUT_DESTINATION_COLLISION"

    hard_report = tmp_path / "hard-report.json"
    hard_receipt = tmp_path / "hard-receipt.json"
    hard_report.write_text("preserve", encoding="utf-8")
    hard_receipt.hardlink_to(hard_report)
    with pytest.raises(OutcomeHoldoutError) as hard_linked:
        _require_distinct_output_destinations(hard_report, hard_receipt)
    assert hard_linked.value.code == "OUTPUT_DESTINATION_COLLISION"

    symbolic_report = tmp_path / "symbolic-report.json"
    symbolic_receipt = tmp_path / "symbolic-receipt.json"
    symbolic_report.write_text("preserve", encoding="utf-8")
    symbolic_receipt.symlink_to(symbolic_report.name)
    with pytest.raises(OutcomeHoldoutError) as symbolic_linked:
        _require_distinct_output_destinations(symbolic_report, symbolic_receipt)
    assert symbolic_linked.value.code == "OUTPUT_DESTINATION_COLLISION"

    atomic_receipt = tmp_path / "atomic-receipt.json"
    atomic_report = tmp_path / ".atomic-receipt.json.tmp"
    with pytest.raises(OutcomeHoldoutError) as atomic_alias:
        _require_distinct_output_destinations(atomic_report, atomic_receipt)
    assert atomic_alias.value.code == "OUTPUT_DESTINATION_COLLISION"

    with pytest.raises(OutcomeHoldoutError) as source_output:
        _require_distinct_output_destinations(
            ordinary_archive,
            ordinary_receipt,
            archive_path=ordinary_archive,
        )
    assert source_output.value.code == "OUTPUT_SOURCE_COLLISION"

    hard_source_output = tmp_path / "hard-source-output.json"
    hard_source_output.hardlink_to(ordinary_archive)
    with pytest.raises(OutcomeHoldoutError) as hard_source:
        _require_distinct_output_destinations(
            hard_source_output,
            ordinary_receipt,
            archive_path=ordinary_archive,
        )
    assert hard_source.value.code == "OUTPUT_SOURCE_COLLISION"

    symbolic_source_receipt = tmp_path / "symbolic-source-receipt.json"
    symbolic_source_receipt.symlink_to(ordinary_archive.name)
    with pytest.raises(OutcomeHoldoutError) as symbolic_source:
        _require_distinct_output_destinations(
            ordinary_report,
            symbolic_source_receipt,
            archive_path=ordinary_archive,
        )
    assert symbolic_source.value.code == "OUTPUT_SOURCE_COLLISION"

    temporary_source = tmp_path / ".temporary-source-report.json.tmp"
    temporary_source.write_bytes(b"temporary source archive")
    with pytest.raises(OutcomeHoldoutError) as temporary_source_alias:
        _require_distinct_output_destinations(
            tmp_path / "temporary-source-report.json",
            ordinary_receipt,
            archive_path=temporary_source,
        )
    assert temporary_source_alias.value.code == "OUTPUT_SOURCE_COLLISION"

    def forbidden_run(**kwargs: Any) -> tuple[dict[str, Any], dict[str, Any]]:
        raise AssertionError("colliding destinations must fail before evaluation")

    monkeypatch.setattr(holdout, "run_holdout", forbidden_run)
    command_path = tmp_path / "command-collision.json"
    exit_code = holdout.main(
        [
            "--archive",
            str(tmp_path / "unused.zip"),
            "--edcm-repository-root",
            str(tmp_path),
            "--edcm-commit",
            "b" * 40,
            "--output",
            str(command_path),
            "--receipt",
            str(command_path),
        ]
    )
    assert exit_code == 2
    assert not command_path.exists()
    assert json.loads(capsys.readouterr().out) == {
        "failure": "OUTPUT_DESTINATION_COLLISION",
        "status": "incomplete",
    }

    source_receipt = tmp_path / "source-collision-receipt.json"
    source_bytes = ordinary_archive.read_bytes()
    exit_code = holdout.main(
        [
            "--archive",
            str(ordinary_archive),
            "--edcm-repository-root",
            str(tmp_path),
            "--edcm-commit",
            "b" * 40,
            "--output",
            str(ordinary_archive),
            "--receipt",
            str(source_receipt),
        ]
    )
    assert exit_code == 2
    assert ordinary_archive.read_bytes() == source_bytes
    assert not source_receipt.exists()
    assert json.loads(capsys.readouterr().out) == {
        "failure": "OUTPUT_SOURCE_COLLISION",
        "status": "incomplete",
    }


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
    # Historical producer c2924307 was externally repeated before release.
    assert findings["byte-identical-render-repeat"] == "supported"
    assert report["canon_selection"] is None
