# === CHECKS ===
# id: check_ucns_edcm_program_structure
#   proves: edcm_ucns_edcm_experiments
#   call: self::test_default_program_structure
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_contrastive_order_multiplicity_resolution
#   proves: edcm_ucns_edcm_experiments
#   call: self::test_contrastive_order_multiplicity_resolution
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_joint_runner_preserves_no_canon
#   proves: edcm_ucns_edcm_experiments
#   call: self::test_joint_runner_preserves_no_canon
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import json
import os
from pathlib import Path

import pytest

from edcm.ucns_edcm_experiments import (
    EXPECTED_UCNS_COMMIT,
    ExperimentPartition,
    baseline_readout,
    build_default_program,
    contrastive_readout,
    main,
    run_default_experiments,
)


def _case(case_id):
    cases, _ = build_default_program()
    return next(case for case in cases if case.case_id == case_id)


def _ucns_source_root() -> Path:
    value = os.environ.get("UCNS_SOURCE_ROOT")
    if not value:
        pytest.skip("joint source-identity test requires UCNS_SOURCE_ROOT")
    return Path(value)


def test_default_program_structure() -> None:
    cases, relations = build_default_program()
    assert len(cases) == 8
    assert len({case.case_id for case in cases}) == len(cases)
    assert {case.partition for case in cases} == {
        ExperimentPartition.DEVELOPMENT,
        ExperimentPartition.HOLDOUT,
    }
    assert len(relations) == 10
    assert all(relation.rationale for relation in relations)
    assert all(case.digest == case.digest for case in cases)


def test_contrastive_order_multiplicity_resolution() -> None:
    resolved_last = contrastive_readout(_case("order-resolution-last"))
    refusal_last = contrastive_readout(_case("order-refusal-last"))
    assert resolved_last["final_tension"] < refusal_last["final_tension"]

    single = contrastive_readout(_case("single-refusal"))
    repeated = contrastive_readout(_case("repeated-refusal"))
    assert repeated["refusal_pressure"] > single["refusal_pressure"]
    assert repeated["repetition_pressure"] > single["repetition_pressure"]
    assert repeated["final_tension"] > single["final_tension"]

    low = contrastive_readout(_case("low-constraint"))
    high = contrastive_readout(_case("high-constraint"))
    assert high["constraint_pressure"] > low["constraint_pressure"]

    unresolved = contrastive_readout(_case("unresolved-pressure"))
    resolved = contrastive_readout(_case("resolved-pressure"))
    assert resolved["final_tension"] < unresolved["final_tension"]


def test_baseline_candidate_is_readable_but_not_assumed_correct() -> None:
    values = baseline_readout(_case("single-refusal"))
    for key in (
        "C_mean",
        "R_mean",
        "F_mean",
        "E_mean",
        "D_mean",
        "N_mean",
        "I_mean",
        "O_mean",
        "L_mean",
        "P_mean",
        "kappa_final",
        "energy_mean",
    ):
        assert key in values
        assert isinstance(values[key], float)


def test_joint_runner_preserves_no_canon(tmp_path) -> None:
    pytest.importorskip("ucns")
    source_root = _ucns_source_root()
    report = run_default_experiments(
        edcm_commit="test-edcm-commit",
        ucns_commit=EXPECTED_UCNS_COMMIT,
        ucns_source_root=source_root,
    )
    assert report.canon_selection is None
    assert report.ucns_commit == EXPECTED_UCNS_COMMIT
    assert report.ucns_identity_verified
    assert report.ucns_source_manifest
    assert report.edcm_commit == "test-edcm-commit"
    assert report.readouts
    assert report.structural_signatures
    assert report.relation_verdicts
    assert all(
        verdict.status in {"supported", "falsified", "error"}
        for verdict in report.relation_verdicts
    )

    transparent = {
        verdict.relation_id: verdict.status for verdict in report.relation_verdicts
    }
    assert transparent["order-contrastive-tension"] == "supported"
    assert transparent["multiplicity-contrastive-refusal"] == "supported"
    assert transparent["constraint-contrastive"] == "supported"
    assert transparent["resolution-contrastive"] == "supported"

    order_set_findings = [
        finding
        for finding in report.policy_findings
        if finding.pair_id == "order-pair"
        and finding.policy_name == "set"
        and finding.readout == "edcm.contrastive.final_tension"
    ]
    assert len(order_set_findings) == 1
    assert order_set_findings[0].status == "incompatible-for-readout"
    assert "order" in order_set_findings[0].information_loss

    multiplicity_set_findings = [
        finding
        for finding in report.policy_findings
        if finding.pair_id == "multiplicity-pair"
        and finding.policy_name == "set"
        and finding.readout == "edcm.contrastive.refusal_pressure"
    ]
    assert len(multiplicity_set_findings) == 1
    assert multiplicity_set_findings[0].status == "incompatible-for-readout"
    assert "multiplicity" in multiplicity_set_findings[0].information_loss

    order_signatures = [
        item
        for item in report.structural_signatures
        if item.case_id in {"order-resolution-last", "order-refusal-last"}
        and item.support_policy == "unit-turn"
    ]
    assert len(order_signatures) == 6
    by_case_policy = {
        (item.case_id, item.policy_name): item.signature for item in order_signatures
    }
    assert (
        by_case_policy[("order-resolution-last", "ordered-sequence")]
        != by_case_policy[("order-refusal-last", "ordered-sequence")]
    )
    assert (
        by_case_policy[("order-resolution-last", "set")]
        == by_case_policy[("order-refusal-last", "set")]
    )

    output = tmp_path / "report.json"
    assert main(
        [
            "--output",
            str(output),
            "--edcm-commit",
            "test-edcm-commit",
            "--ucns-commit",
            EXPECTED_UCNS_COMMIT,
            "--ucns-source-root",
            str(source_root),
        ]
    ) == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["canon_selection"] is None
    assert payload["ucns_identity_verified"] is True
    assert payload["structural_signatures"]
    assert payload["report_digest"]
    assert payload["schema"].startswith("edcm.ucns-edcm-experiment-report/")


def test_runner_rejects_wrong_ucns_identity() -> None:
    pytest.importorskip("ucns")
    source_root = _ucns_source_root()
    with pytest.raises(ValueError):
        run_default_experiments(
            ucns_commit="wrong",
            ucns_source_root=source_root,
        )
