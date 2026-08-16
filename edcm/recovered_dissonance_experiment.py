# === MODULE_BUILD ===
# id: recovered_dissonance_controlled_gate
#   module_name: recovered_dissonance_experiment
#   module_kind: experiment
#   summary: executes the frozen absolute-recovery scale falsifier and its sole normalized-positive-pressure escalation without external labels
#   owner: Erin Spencer
#   public_surface: CandidateStatus, recovered_dissonance, accumulated_positive_pressure, normalized_recovered_dissonance, run_controlled_gate, main
#   internal_surface: canonical JSON and frozen-design validation helpers
#   auth_boundary: none
#   storage_boundary: reads the committed preregistration and writes one aggregate report path selected by the caller
#   network_boundary: none
#   user_data_boundary: hand-authored synthetic kappa trajectories only; sealed and external outcome labels are forbidden
#   admin_only: false
#   tests: tests/test_recovered_dissonance_experiment.py
#   rollout: controlled candidate falsification only; external evaluation requires separate UCNS PR #196 transport
#   rollback: remove this module, its tests, and generated controlled report without changing the frozen baseline or historical MultiWOZ evidence
#   requires: maintained EDCM baseline identity and committed recovered-dissonance preregistration
#   since: 2026-08-16
#   unresolved: external outcome validity, temporal sampling comparability, independent replication, and canon authority
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: recovered_dissonance_gate_executes_only_frozen_candidates
#   given: the controlled recovered-dissonance gate runs
#   then: formulas, controls, direction, escalation, and stopping rules match the committed preregistration exactly
#   class: evidence
#   since: 2026-08-16
#
# id: recovered_dissonance_gate_preserves_prior_falsification
#   given: a controlled report is emitted
#   then: the prior MultiWOZ sensitivity result remains FALSIFIED and no transport, validity, or canon promotion is claimed
#   class: safety
#   since: 2026-08-16
# === END CONTRACTS ===

"""Execute the frozen recovered-dissonance controlled contrast.

This module intentionally has no corpus adapter and accepts no outcome-label
input.  It evaluates only the hand-authored controls committed before this
implementation.
"""

from __future__ import annotations

import argparse
import json
from enum import Enum
from fractions import Fraction
from hashlib import sha256
from math import isfinite
from pathlib import Path
from typing import Any, Sequence


DESIGN_RELATIVE_PATH = Path(
    "docs/experiments/2026-08-16-recovered-dissonance-preregistration.json"
)
EXPECTED_SCHEMA = "edcm.recovered-dissonance-preregistration/0.1.0"
EXPECTED_FORMULA_A = "max(kappa_t)-kappa_final"
EXPECTED_FORMULA_B = (
    "(max(kappa_t)-kappa_final)/sum_t(max(kappa_t-kappa_(t-1),0))"
)
EXPECTED_MULTIWOZ_DIGEST = (
    "a726434a533395e7e3bd7d72ba3e9ce68f58c5b62f3b6b10d2b0556b09e85e61"
)


class CandidateStatus(str, Enum):
    SURVIVED = "SURVIVED"
    FALSIFIED = "FALSIFIED"
    UNRESOLVED = "UNRESOLVED"
    BLOCKED = "BLOCKED"


def _admit(kappa: Sequence[int | float]) -> tuple[Fraction, ...]:
    if isinstance(kappa, (str, bytes)) or len(kappa) < 3:
        raise ValueError("kappa must contain at least three ordered states")
    admitted: list[Fraction] = []
    for value in kappa:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("kappa states must be finite real numbers, not booleans")
        if not isfinite(value) or value < 0:
            raise ValueError("kappa states must be finite and nonnegative")
        admitted.append(Fraction(str(value)))
    return tuple(admitted)


def recovered_dissonance(kappa: Sequence[int | float]) -> Fraction:
    values = _admit(kappa)
    return max(values) - values[-1]


def accumulated_positive_pressure(kappa: Sequence[int | float]) -> Fraction:
    values = _admit(kappa)
    return sum(
        (max(current - previous, Fraction(0))
         for previous, current in zip(values, values[1:])),
        Fraction(0),
    )


def normalized_recovered_dissonance(
    kappa: Sequence[int | float],
) -> Fraction:
    recovered = recovered_dissonance(kappa)
    pressure = accumulated_positive_pressure(kappa)
    if pressure == 0:
        raise ZeroDivisionError("zero accumulated positive pressure is UNRESOLVED")
    return recovered / pressure


def _fraction(value: Fraction) -> dict[str, int]:
    return {"denominator": value.denominator, "numerator": value.numerator}


def _design_bytes(path: Path) -> bytes:
    return path.read_bytes()


def _load_and_validate_design(path: Path) -> tuple[dict[str, Any], str]:
    payload_bytes = _design_bytes(path)
    design = json.loads(payload_bytes)
    if design.get("schema") != EXPECTED_SCHEMA:
        raise ValueError("preregistration schema drift")
    if design["candidate_a"]["formula"] != EXPECTED_FORMULA_A:
        raise ValueError("candidate A formula drift")
    if design["candidate_b"]["formula"] != EXPECTED_FORMULA_B:
        raise ValueError("candidate B formula drift")
    if design["prior_multiwoz"] != {
        "report_digest": EXPECTED_MULTIWOZ_DIGEST,
        "sensitivity_hypothesis": "FALSIFIED",
    }:
        raise ValueError("prior MultiWOZ standing drift")
    if design.get("canon_selection") is not None:
        raise ValueError("preregistration canon boundary drift")
    return design, sha256(payload_bytes).hexdigest()


def _evaluate(
    controls: list[dict[str, Any]],
    score_name: str,
) -> dict[str, Any]:
    scorer = (
        recovered_dissonance
        if score_name == "absolute"
        else normalized_recovered_dissonance
    )
    rows = []
    try:
        for case in controls:
            score = scorer(case["kappa"])
            rows.append(
                {
                    "construction_label": case["construction_label"],
                    "kappa": case["kappa"],
                    "pair_id": case["pair_id"],
                    "score": _fraction(score),
                }
            )
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        return {
            "reason": str(exc),
            "rows": rows,
            "status": CandidateStatus.UNRESOLVED.value,
        }

    by_pair: dict[str, dict[str, Fraction]] = {}
    for row in rows:
        by_pair.setdefault(row["pair_id"], {})[row["construction_label"]] = Fraction(
            row["score"]["numerator"], row["score"]["denominator"]
        )
    matched_pass = all(
        labels.get("resolved", Fraction(-1))
        > labels.get("unresolved", Fraction(-1))
        for labels in by_pair.values()
    )
    resolved = [
        Fraction(row["score"]["numerator"], row["score"]["denominator"])
        for row in rows
        if row["construction_label"] == "resolved"
    ]
    unresolved = [
        Fraction(row["score"]["numerator"], row["score"]["denominator"])
        for row in rows
        if row["construction_label"] == "unresolved"
    ]
    lower = max(unresolved)
    upper = min(resolved)
    global_gap = upper > lower
    range_pass = score_name == "absolute" or all(
        Fraction(0)
        <= Fraction(row["score"]["numerator"], row["score"]["denominator"])
        <= Fraction(1)
        for row in rows
    )
    status = (
        CandidateStatus.SURVIVED
        if matched_pass and global_gap and range_pass
        else CandidateStatus.FALSIFIED
    )
    return {
        "global_strict_gap": global_gap,
        "matched_direction": matched_pass,
        "range": range_pass,
        "rows": rows,
        "status": status.value,
        "threshold": _fraction((lower + upper) / 2) if global_gap else None,
    }


def run_controlled_gate(design_path: Path) -> dict[str, Any]:
    design, design_digest = _load_and_validate_design(design_path)
    absolute = _evaluate(design["controls"], "absolute")
    escalation_admitted = (
        absolute["status"] == CandidateStatus.FALSIFIED.value
        and absolute.get("matched_direction") is True
        and absolute.get("global_strict_gap") is False
    )
    normalized = (
        _evaluate(design["controls"], "normalized")
        if escalation_admitted
        else {"status": "NOT_EVALUATED"}
    )
    selected = (
        design["candidate_a"]["id"]
        if absolute["status"] == CandidateStatus.SURVIVED.value
        else (
            design["candidate_b"]["id"]
            if normalized["status"] == CandidateStatus.SURVIVED.value
            else None
        )
    )
    return {
        "candidate_a": absolute,
        "candidate_b": normalized,
        "canon_selection": None,
        "controlled_candidate_selected_for_external_evaluation": selected,
        "external_evaluation_performed": False,
        "measurement_validity": "not-established",
        "preregistration_file_sha256": design_digest,
        "prior_multiwoz": design["prior_multiwoz"],
        "schema": "edcm.recovered-dissonance-controlled-result/0.1.0",
        "sealed_outcome_labels_inspected": False,
        "stopping_rule_reached": True,
        "transport_status": "not-run",
    }


def _canonical_json(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    design_path = args.repository_root.resolve() / DESIGN_RELATIVE_PATH
    report = run_controlled_gate(design_path)
    args.output.write_bytes(_canonical_json(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
