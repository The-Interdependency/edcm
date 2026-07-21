# === CHECKS ===
# id: check_ucns_edcm_v2_program
#   proves: edcm_ucns_edcm_experiments_v2
#   call: self::test_v2_program_structure
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_occurrence_coverage_candidate
#   proves: edcm_ucns_edcm_experiments_v2
#   call: self::test_occurrence_coverage_candidate_invariants
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_ucns_edcm_v2_joint_report
#   proves: edcm_ucns_edcm_experiments_v2
#   call: self::test_v2_joint_report_preserves_prior_evidence_and_no_canon
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import json
import os
from pathlib import Path

import pytest

from edcm.ucns_edcm_experiments import EXPECTED_UCNS_COMMIT
from edcm.ucns_edcm_experiments_v2 import (
    OCCURRENCE_CANDIDATE_ID,
    PRIOR_REPORT_DIGEST,
    ExperimentPartition,
    build_v2_program,
    main,
    occurrence_coverage_readout,
    run_v2_experiments,
)


def _case(case_id):
    cases, _, _ = build_v2_program()
    return next(case for case in cases if case.case_id == case_id)


def test_v2_program_structure() -> None:
    cases, relations, phrase_pairs = build_v2_program()
    assert len(cases) == 16
    assert len({case.case_id for case in cases}) == len(cases)
    assert {case.partition for case in cases} == {
        ExperimentPartition.DEVELOPMENT,
        ExperimentPartition.HOLDOUT,
    }
    assert len(relations) == 29
    assert len(phrase_pairs) == 4
    assert all(case.digest == case.digest for case in cases)
    assert all(relation.rationale for relation in relations)


def test_occurrence_coverage_candidate_invariants() -> None:
    dose_values = tuple(
        occurrence_coverage_readout(_case(case_id))["refusal_occurrences"]
        for case_id in (
            "refusal-dose-0",
            "refusal-dose-1",
            "refusal-dose-2",
            "refusal-dose-4",
        )
    )
    assert dose_values == (0.0, 1.0, 2.0, 4.0)

    dose_area = tuple(
        occurrence_coverage_readout(_case(case_id))["tension_area"]
        for case_id in (
            "refusal-dose-0",
            "refusal-dose-1",
            "refusal-dose-2",
            "refusal-dose-4",
        )
    )
    assert all(left < right for left, right in zip(dose_area, dose_area[1:]))

    for low_case, high_case in (
        ("constraint-known-low", "constraint-known-high"),
        ("constraint-option-low", "constraint-option-high"),
        ("constraint-consequence-low", "constraint-consequence-high"),
        ("constraint-authority-low", "constraint-authority-high"),
    ):
        low = occurrence_coverage_readout(_case(low_case))["constraint_occurrences"]
        high = occurrence_coverage_readout(_case(high_case))["constraint_occurrences"]
        assert high > low

    immediate = occurrence_coverage_readout(_case("resolution-immediate"))
    delayed = occurrence_coverage_readout(_case("resolution-delayed"))
    absent = occurrence_coverage_readout(_case("resolution-absent"))
    preemptive = occurrence_coverage_readout(_case("resolution-preemptive"))
    assert (
        immediate["resolution_latency_horizon"]
        < delayed["resolution_latency_horizon"]
        < absent["resolution_latency_horizon"]
    )
    assert immediate["tension_area"] < delayed["tension_area"]
    assert delayed["final_tension"] < absent["final_tension"]
    assert immediate["final_tension"] < preemptive["final_tension"]


def test_v2_joint_report_preserves_prior_evidence_and_no_canon(tmp_path) -> None:
    pytest.importorskip("ucns")
    source_root = os.environ.get("UCNS_SOURCE_ROOT")
    if source_root is None:
        pytest.skip("verified UCNS source checkout is not available")

    report = run_v2_experiments(
        edcm_commit="test-edcm-v2",
        ucns_commit=EXPECTED_UCNS_COMMIT,
        ucns_source_root=source_root,
    )
    assert report.canon_selection is None
    assert report.prior_report_digest == PRIOR_REPORT_DIGEST
    assert report.ucns_identity_verified
    assert report.edcm_commit == "test-edcm-v2"
    assert len(report.structural_signatures) == 16 * 4 * 3
    assert report.dose_curves
    assert report.phrase_coverage
    assert report.latency_findings
    assert report.support_stability
    assert all(
        verdict.status in {"supported", "falsified", "error"}
        for verdict in report.relation_verdicts
    )
    occurrence_curve = next(
        finding
        for finding in report.dose_curves
        if finding.candidate_id == OCCURRENCE_CANDIDATE_ID
        and finding.readout == "edcm.occurrence.refusal_occurrences"
    )
    assert occurrence_curve.strictly_increasing

    output = tmp_path / "v0.2.json"
    assert main(
        [
            "--output",
            str(output),
            "--edcm-commit",
            "test-edcm-v2",
            "--ucns-source-root",
            source_root,
        ]
    ) == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["schema"].endswith("/0.2.0")
    assert payload["prior_report_digest"] == PRIOR_REPORT_DIGEST
    assert payload["canon_selection"] is None
    assert payload["report_digest"]


def test_v2_rejects_wrong_ucns_identity() -> None:
    pytest.importorskip("ucns")
    with pytest.raises(ValueError):
        run_v2_experiments(ucns_commit="wrong", ucns_source_root=Path("."))
