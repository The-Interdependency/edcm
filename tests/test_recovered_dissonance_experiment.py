# === TEST_METADATA ===
# id: check_recovered_dissonance_frozen_gate
#   proves: recovered_dissonance_gate_executes_only_frozen_candidates, recovered_dissonance_gate_preserves_prior_falsification
#   call: self::test_frozen_gate_falsifies_absolute_and_stops_after_normalized_survival
#   class: evidence
#   level: integration
#   covers: edcm/recovered_dissonance_experiment.py
#   requires: pytest
#   fixtures: committed recovered-dissonance preregistration
#   negative_cases: malformed kappa, zero pressure, design drift, absolute scale confound
#   assertions: exact statuses, exact scores, frozen prior result, nonpromotion, deterministic bytes
#   since: 2026-08-16
# === END TEST_METADATA ===

import json
from pathlib import Path

import pytest

from edcm.recovered_dissonance_experiment import (
    DESIGN_RELATIVE_PATH,
    accumulated_positive_pressure,
    normalized_recovered_dissonance,
    recovered_dissonance,
    run_controlled_gate,
)


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / DESIGN_RELATIVE_PATH


def test_frozen_gate_falsifies_absolute_and_stops_after_normalized_survival():
    result = run_controlled_gate(DESIGN)
    assert result["candidate_a"]["status"] == "FALSIFIED"
    assert result["candidate_a"]["matched_direction"] is True
    assert result["candidate_a"]["global_strict_gap"] is False
    assert result["candidate_b"]["status"] == "SURVIVED"
    assert result["candidate_b"]["threshold"] == {
        "denominator": 5,
        "numerator": 3,
    }
    assert result["controlled_candidate_selected_for_external_evaluation"].endswith(
        "normalized-positive-pressure/0.1.0"
    )
    assert result["prior_multiwoz"]["sensitivity_hypothesis"] == "FALSIFIED"
    assert result["sealed_outcome_labels_inspected"] is False
    assert result["external_evaluation_performed"] is False
    assert result["measurement_validity"] == "not-established"
    assert result["canon_selection"] is None
    assert result["stopping_rule_reached"] is True


def test_exact_formulas_and_scale_invariance():
    assert recovered_dissonance([0, 10, 8]) == 2
    assert accumulated_positive_pressure([0, 10, 8]) == 10
    assert normalized_recovered_dissonance([0, 10, 8]) == pytest.approx(0.2)
    assert normalized_recovered_dissonance([0, 10, 8]) == (
        normalized_recovered_dissonance([0, 100, 80])
    )


@pytest.mark.parametrize(
    "trajectory,exception",
    [
        ([0, 1], ValueError),
        ([0, True, 0], TypeError),
        ([0, float("inf"), 0], ValueError),
        ([0, -1, 0], ValueError),
    ],
)
def test_admission_fails_closed(trajectory, exception):
    with pytest.raises(exception):
        recovered_dissonance(trajectory)


def test_zero_accumulated_pressure_is_unresolved():
    with pytest.raises(ZeroDivisionError, match="UNRESOLVED"):
        normalized_recovered_dissonance([1, 1, 0])


def test_design_drift_fails_closed(tmp_path):
    payload = json.loads(DESIGN.read_text())
    payload["candidate_a"]["formula"] = "tuned-after-results"
    drifted = tmp_path / "design.json"
    drifted.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="formula drift"):
        run_controlled_gate(drifted)
