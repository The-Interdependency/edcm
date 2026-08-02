# === CHECKS ===
# id: check_goal_vector_same_occurrences_order
#   proves: edcm_goal_vector_same_occurrences_preserve_order
#   call: self::test_same_occurrences_different_order_preserve_distinct_trajectories
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_goal_vector_contradiction_and_variance
#   proves: edcm_goal_vector_same_occurrences_preserve_order
#   call: self::test_resolved_and_active_contradictions_have_exact_candidate_variances
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_goal_vector_na_boundary
#   proves: edcm_goal_vector_na_not_zero, edcm_goal_vector_no_status_transfer
#   call: self::test_na_is_typed_and_nonclaims_remain_absent
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_goal_vector_exact_ucns_report
#   proves: edcm_goal_vector_same_occurrences_preserve_order, edcm_goal_vector_na_not_zero, edcm_goal_vector_no_status_transfer
#   call: self::test_exact_ucns_report_is_deterministic_and_no_canon
#   requires: python3
#   timeout: 30
#   mutates: temporary report only
#   cleanup: pytest tmp_path
#
# id: check_goal_vector_sealed_evidence
#   proves: edcm_goal_vector_same_occurrences_preserve_order, edcm_goal_vector_na_not_zero, edcm_goal_vector_no_status_transfer
#   call: self::test_sealed_goal_vector_evidence_matches_exact_producer
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from fractions import Fraction
from hashlib import sha256
import json
import os
from pathlib import Path

import pytest

from edcm.goal_vector_experiment import (
    PROGRAM_SCHEMA,
    _digest,
    build_goal_vector_program,
    evaluate_case,
    main,
    run_goal_vector_experiment,
)


def _case_result(case_id: str) -> dict:
    goal, occurrences, cases = build_goal_vector_program()
    case = next(item for item in cases if item.case_id == case_id)
    return evaluate_case(goal, occurrences, case)


def _fraction(record: dict) -> Fraction:
    return Fraction(record["numerator"], record["denominator"])


def test_same_occurrences_different_order_preserve_distinct_trajectories() -> None:
    goal, occurrences, cases = build_goal_vector_program()
    assert len(goal.dimensions) == 4
    assert len(occurrences) == 4
    assert len(cases) == 2
    assert cases[0].occurrence_order != cases[1].occurrence_order
    assert sorted(cases[0].occurrence_order) == sorted(cases[1].occurrence_order)

    resolved = evaluate_case(goal, occurrences, cases[0])
    active = evaluate_case(goal, occurrences, cases[1])
    assert resolved["occurrence_multiset_digest"] == active["occurrence_multiset_digest"]
    assert resolved["ordered_occurrence_digest"] != active["ordered_occurrence_digest"]
    assert tuple(
        trace["source_locator"]["exact_text"] for trace in resolved["turn_trace"]
    ) != tuple(
        trace["source_locator"]["exact_text"] for trace in active["turn_trace"]
    )
    assert {
        trace["source_locator"]["exact_text"] for trace in resolved["turn_trace"]
    } == {
        trace["source_locator"]["exact_text"] for trace in active["turn_trace"]
    }


def test_resolved_and_active_contradictions_have_exact_candidate_variances() -> None:
    resolved = _case_result("contradiction-resolved")
    active = _case_result("contradiction-active")

    assert resolved["candidate_completion_state"] == "candidate-complete"
    assert active["candidate_completion_state"] == "unresolved"
    assert resolved["terminal_active_contradictions"] == ()
    assert len(active["terminal_active_contradictions"]) == 1
    assert resolved["contradiction_ledger"][0]["status"] == "resolved"
    assert active["contradiction_ledger"][0]["status"] == "active"

    assert _fraction(resolved["terminal_goal_projection"]) == Fraction(1, 1)
    assert _fraction(active["terminal_goal_projection"]) == Fraction(1, 2)
    assert _fraction(resolved["goal_motion_variance"]) == Fraction(1, 8)
    assert _fraction(active["goal_motion_variance"]) == Fraction(9, 64)
    assert _fraction(resolved["goal_trajectory_variance"]) == Fraction(5, 32)
    assert _fraction(active["goal_trajectory_variance"]) == Fraction(11, 256)

    assert [
        _fraction(trace["goal_motion"]) for trace in resolved["turn_trace"]
    ] == [Fraction(1, 4), Fraction(-1, 4), Fraction(3, 4), Fraction(1, 4)]
    assert [
        _fraction(trace["goal_motion"]) for trace in active["turn_trace"]
    ] == [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4), Fraction(-1, 2)]


def test_na_is_typed_and_nonclaims_remain_absent() -> None:
    resolved = _case_result("contradiction-resolved")
    na_states = [
        component
        for trace in resolved["turn_trace"]
        for component in trace["component_state_after"]
        if component["state"] == "NA"
    ]
    no_claim_vectors = [
        component
        for trace in resolved["turn_trace"]
        for component in trace["declared_goal_vector"]
        if component["state"] == "no-claim"
    ]
    assert na_states
    assert no_claim_vectors
    assert all(item["sign"] is None and item["magnitude"] is None for item in na_states)
    assert all(
        item["sign"] is None and item["magnitude"] is None
        for item in no_claim_vectors
    )
    assert resolved["formal_completion"]["state"] == "NA"
    assert resolved["ucns_profile_observation"]["state"] == "NA"


def test_exact_ucns_report_is_deterministic_and_no_canon(tmp_path: Path) -> None:
    pytest.importorskip("ucns")
    source_root = os.environ.get("UCNS_SOURCE_ROOT")
    first = run_goal_vector_experiment(
        edcm_commit="test-goal-vector-edcm",
        ucns_source_root=source_root,
    )
    second = run_goal_vector_experiment(
        edcm_commit="test-goal-vector-edcm",
        ucns_source_root=source_root,
    )
    assert first.to_json() == second.to_json()
    assert first.schema == PROGRAM_SCHEMA
    assert first.canon_selection is None
    assert first.ucns_identity_verified is True
    assert first.empirical_validity_claim is False
    assert first.proof_status_transfer is False
    assert first.metapat_semantic_constraints["state"] == "NA"
    assert first.ucns_geometry_identity["state"] == "NA"
    assert first.formal_completion["state"] == "NA"
    assert first.composition_boundary["formal_higher_gonol_composition"] == "NA"
    assert {item["status"] for item in first.findings} == {"supported"}
    assert len(first.findings) == 8

    resolved, active = first.case_results
    assert resolved["ucns_profile_observation"]["state"] == "attached"
    assert active["ucns_profile_observation"]["state"] == "attached"
    assert (
        resolved["ucns_profile_observation"]["observation_digest"]
        != active["ucns_profile_observation"]["observation_digest"]
    )
    for result in first.case_results:
        observation_turns = result["ucns_profile_observation"]["turns"]
        source_turns = result["turn_trace"]
        assert tuple(turn["raw_text"] for turn in observation_turns) == tuple(
            turn["source_locator"]["exact_text"] for turn in source_turns
        )
        assert tuple(turn["speaker_id"] for turn in observation_turns) == tuple(
            turn["source_locator"]["speaker"] for turn in source_turns
        )

    first_path = tmp_path / "goal-vector.json"
    second_path = tmp_path / "goal-vector-repeat.json"
    args = ["--edcm-commit", "test-goal-vector-edcm"]
    if source_root:
        args.extend(("--ucns-source-root", source_root))
    assert main([*args, "--output", str(first_path)]) == 0
    assert main([*args, "--output", str(second_path)]) == 0
    assert first_path.read_bytes() == second_path.read_bytes()
    payload = json.loads(first_path.read_text(encoding="utf-8"))
    assert payload["report_digest"]
    assert payload["canon_selection"] is None


def test_sealed_goal_vector_evidence_matches_exact_producer() -> None:
    path = Path("experiments/results/2026-08-02-goal-vector-contradiction-v0.1.0.json")
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == (
        "03b35230c22724b908d3d8733376da035b9b748ef54513dab1e8f2466a3519ee"
    )
    payload = json.loads(raw)
    report_digest = payload.pop("report_digest")
    assert report_digest == (
        "8a1e3d4548b6b6ee4b3df4f55769b8707a42264450223cdcc88e64f9119c0e30"
    )
    assert _digest(payload) == report_digest
    assert payload["edcm_commit"] == (
        "14c87440eedd213c1533b0cf9633c0286f09cb09"
    )
    assert payload["ucns_commit"] == (
        "a98c9e6c69804a8a08d0786b1d8b450bb2c49a97"
    )
    assert payload["canon_selection"] is None
    assert payload["ucns_geometry_identity"]["state"] == "NA"
    assert payload["metapat_semantic_constraints"]["state"] == "NA"
    assert payload["formal_completion"]["state"] == "NA"
    assert {item["status"] for item in payload["findings"]} == {"supported"}

    cases = {item["case_id"]: item for item in payload["case_results"]}
    assert cases["contradiction-resolved"]["terminal_goal_projection"]["exact"] == "1/1"
    assert cases["contradiction-resolved"]["goal_motion_variance"]["exact"] == "1/8"
    assert cases["contradiction-resolved"]["terminal_active_contradictions"] == []
    assert cases["contradiction-active"]["terminal_goal_projection"]["exact"] == "1/2"
    assert cases["contradiction-active"]["goal_motion_variance"]["exact"] == "9/64"
    assert len(cases["contradiction-active"]["terminal_active_contradictions"]) == 1
