"""Controlled goal-vector contradiction experiment over exact UCNS observations.

Usage guidance
--------------
Install EDCM with the exact current ``ucns-profile`` producer and run::

    python -m edcm.goal_vector_experiment \
        --ucns-source-root /path/to/ucns \
        --output /tmp/goal-vector.json

Run the command twice and compare the files byte-for-byte.  The fixed fixture
uses the same four utterance occurrences in two orders.  Its semantic effects
are declared experiment inputs, not language-model inference or METAPAT canon.
The emitted goal projection is a declared-loss candidate readout; complete
component states, contradictions, source locators, and UCNS observations remain
attached.  Formal geometry and formal completion remain typed ``NA``.
"""

# === MODULE_BUILD ===
# id: edcm_goal_vector_experiment
#   module_name: goal_vector_experiment
#   module_kind: experiment
#   summary: runs a controlled same-occurrences/different-order contradiction experiment through the exact current UCNS observation profile and an inspectable EDCM goal-state candidate
#   owner: Erin Spencer
#   public_surface: GoalDimension, DeclaredGoal, GoalClaim, SourceOccurrence, GoalVectorCase, GoalVectorExperimentReport, build_goal_vector_program, evaluate_case, run_goal_vector_experiment, main
#   internal_surface: _canonical_bytes, _digest, _fraction_record, _variance, _state_snapshot, _verify_requested_ucns_source_root, _observe_case, _evaluate_findings
#   auth_boundary: none
#   storage_boundary: writes only caller-selected report path
#   network_boundary: none; exact UCNS producer must already be installed
#   user_data_boundary: fixed synthetic utterances only
#   admin_only: false
#   tests: tests/test_goal_vector_experiment.py
#   rollout: explicit controlled candidate experiment; no default activation or canon selection
#   rollback: remove this module, its test, workflow invocation, design note, and versioned evidence without changing the frozen measurement baseline
#   requires: edcm_ucns_adapter
#   since: 2026-08-02
#   unresolved: independent semantic annotation, real-dialogue goal authority, formal higher-gonol composition, calibration, holdout replication, and human outcome validation
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: edcm_goal_vector_same_occurrences_preserve_order
#   given: the fixed resolved and active-contradiction cases contain the same source occurrences in different orders
#   then: occurrence multiset identity agrees while ordered identity, exact UCNS observation identity, terminal contradiction state, and candidate trajectory remain independently visible
#   class: evidence
#   since: 2026-08-02
#
# id: edcm_goal_vector_na_not_zero
#   given: a goal component has not received an explicit fixture claim
#   then: its state is serialized as NA with no sign or magnitude and scalar projections retain a separate NA count
#   class: safety
#   since: 2026-08-02
#
# id: edcm_goal_vector_no_status_transfer
#   given: the controlled candidate emits a contradiction ledger and goal-motion variance
#   then: formal geometry, formal completion, empirical validity, METAPAT attachment, proof transfer, and canon selection remain absent or false
#   class: doctrine
#   since: 2026-08-02
# === END CONTRACTS ===

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from fractions import Fraction
from hashlib import sha256
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping, Sequence

from .ucns_adapter import (
    ActualUCNSAdapter,
    PINNED_UCNS_COMMIT,
    SUPPORTED_PROFILE,
    select_ucns_adapter,
)


PROGRAM_SCHEMA = "edcm.goal-vector-contradiction-experiment/0.1.0"
PROGRAM_VERSION = "0.1.0"
CANDIDATE_ID = "edcm.goal-vector-state-candidate/0.1.0"
SEMANTIC_FIXTURE_ID = "edcm.goal-vector-meeting-fixture/0.1.0"

STATE_TOWARD = "toward"
STATE_AWAY = "away"
STATE_NA = "NA"
VECTOR_NO_CLAIM = "no-claim"


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return sha256(_canonical_bytes(value)).hexdigest()


def _fraction_record(value: Fraction) -> dict[str, int | str]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "exact": f"{value.numerator}/{value.denominator}",
        "decimal": format(float(value), ".12g"),
    }


def _fraction_from_record(value: Mapping[str, Any]) -> Fraction:
    return Fraction(int(value["numerator"]), int(value["denominator"]))


def _variance(values: Sequence[Fraction]) -> Fraction:
    if not values:
        raise ValueError("variance requires at least one value")
    mean = sum(values, Fraction(0, 1)) / len(values)
    return sum(((value - mean) ** 2 for value in values), Fraction(0, 1)) / len(values)


@dataclass(frozen=True, slots=True)
class GoalDimension:
    dimension_id: str
    description: str

    def __post_init__(self) -> None:
        if not self.dimension_id.strip() or not self.description.strip():
            raise ValueError("goal dimensions require an identifier and description")


@dataclass(frozen=True, slots=True)
class DeclaredGoal:
    goal_id: str
    description: str
    dimensions: tuple[GoalDimension, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "dimensions", tuple(self.dimensions))
        if not self.goal_id.strip() or not self.description.strip():
            raise ValueError("declared goal requires an identifier and description")
        ids = [dimension.dimension_id for dimension in self.dimensions]
        if not ids or len(ids) != len(set(ids)):
            raise ValueError("declared goal dimensions must be nonempty and unique")

    @property
    def dimension_ids(self) -> tuple[str, ...]:
        return tuple(dimension.dimension_id for dimension in self.dimensions)

    @property
    def digest(self) -> str:
        return _digest(asdict(self))


@dataclass(frozen=True, slots=True)
class GoalClaim:
    dimension_id: str
    sign: int
    relation: str
    rationale: str

    def __post_init__(self) -> None:
        if self.sign not in (-1, 1):
            raise ValueError("goal claim sign must be -1 or +1")
        if self.relation not in {"assertion", "revision"}:
            raise ValueError("goal claim relation must be assertion or revision")
        if not self.dimension_id.strip() or not self.rationale.strip():
            raise ValueError("goal claims require dimension and rationale")


@dataclass(frozen=True, slots=True)
class SourceOccurrence:
    occurrence_id: str
    speaker: str
    exact_text: str
    claims: tuple[GoalClaim, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "claims", tuple(self.claims))
        if not self.occurrence_id.strip() or not self.speaker.strip():
            raise ValueError("source occurrence requires identifier and speaker")
        if not self.exact_text.strip() or not self.claims:
            raise ValueError("source occurrence requires exact text and claims")
        dimensions = [claim.dimension_id for claim in self.claims]
        if len(dimensions) != len(set(dimensions)):
            raise ValueError("one occurrence may claim each dimension at most once")

    @property
    def identity_digest(self) -> str:
        return _digest(asdict(self))


@dataclass(frozen=True, slots=True)
class GoalVectorCase:
    case_id: str
    occurrence_order: tuple[str, ...]
    manipulation: str
    provenance: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "occurrence_order", tuple(self.occurrence_order))
        if not self.case_id.strip() or not self.occurrence_order:
            raise ValueError("goal-vector case requires identifier and occurrences")
        if not self.manipulation.strip() or not self.provenance.strip():
            raise ValueError("goal-vector case requires manipulation and provenance")


@dataclass(frozen=True, slots=True)
class GoalVectorExperimentReport:
    schema: str
    program_version: str
    candidate_id: str
    semantic_fixture_id: str
    edcm_commit: str
    ucns_commit: str
    ucns_profile_id: str
    ucns_profile_version: str
    ucns_identity_verified: bool
    ucns_source_root_verified: bool
    goal: dict[str, Any]
    occurrences: tuple[dict[str, Any], ...]
    case_results: tuple[dict[str, Any], ...]
    findings: tuple[dict[str, Any], ...]
    metapat_semantic_constraints: dict[str, Any]
    ucns_geometry_identity: dict[str, Any]
    formal_completion: dict[str, Any]
    composition_boundary: dict[str, Any]
    candidate_measurement_status: str
    empirical_validity_claim: bool
    proof_status_transfer: bool
    canon_selection: None = None
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return _digest(self.as_dict())

    def to_json(self) -> str:
        payload = self.as_dict()
        payload["report_digest"] = _digest(payload)
        return json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def build_goal_vector_program() -> tuple[
    DeclaredGoal,
    tuple[SourceOccurrence, ...],
    tuple[GoalVectorCase, ...],
]:
    """Return the fixed same-occurrences/different-order controlled program."""

    goal = DeclaredGoal(
        goal_id="meeting-tuesday-1500-mutual-explicit-agreement-v1",
        description="Both participants are available and explicitly agree to meet Tuesday at 15:00.",
        dimensions=(
            GoalDimension("a_availability", "participant A states the time works"),
            GoalDimension("b_availability", "participant B states the time works"),
            GoalDimension("a_agreement", "participant A explicitly agrees"),
            GoalDimension("b_agreement", "participant B explicitly agrees"),
        ),
    )
    occurrences = (
        SourceOccurrence(
            "a-available",
            "A",
            "Tuesday at three works for me.",
            (
                GoalClaim(
                    "a_availability",
                    1,
                    "assertion",
                    "controlled fixture declares explicit A availability",
                ),
            ),
        ),
        SourceOccurrence(
            "b-unavailable",
            "B",
            "Tuesday at three does not work for me.",
            (
                GoalClaim(
                    "b_availability",
                    -1,
                    "assertion",
                    "controlled fixture declares explicit B unavailability",
                ),
            ),
        ),
        SourceOccurrence(
            "b-revision",
            "B",
            "My schedule changed; Tuesday at three now works for me, and I agree.",
            (
                GoalClaim(
                    "b_availability",
                    1,
                    "revision",
                    "controlled fixture declares a revision to B availability when an earlier opposing claim exists",
                ),
                GoalClaim(
                    "b_agreement",
                    1,
                    "assertion",
                    "controlled fixture declares explicit B agreement",
                ),
            ),
        ),
        SourceOccurrence(
            "a-agreement",
            "A",
            "Agreed.",
            (
                GoalClaim(
                    "a_agreement",
                    1,
                    "assertion",
                    "controlled fixture declares explicit A agreement",
                ),
            ),
        ),
    )
    cases = (
        GoalVectorCase(
            "contradiction-resolved",
            ("a-available", "b-unavailable", "b-revision", "a-agreement"),
            "opposing B-availability claim is followed by an explicit schedule-change revision",
            "synthetic controlled fixture approved for the 2026-08-02 goal-vector experiment",
        ),
        GoalVectorCase(
            "contradiction-active",
            ("b-revision", "a-agreement", "a-available", "b-unavailable"),
            "the same occurrences are reordered so the opposing B-availability claim occurs last",
            "synthetic controlled fixture approved for the 2026-08-02 goal-vector experiment",
        ),
    )
    return goal, occurrences, cases


def _state_snapshot(
    goal: DeclaredGoal,
    states: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], ...]:
    return tuple(dict(states[dimension_id]) for dimension_id in goal.dimension_ids)


def _projection(
    goal: DeclaredGoal,
    states: Mapping[str, Mapping[str, Any]],
) -> tuple[Fraction, dict[str, int]]:
    counts = {
        "toward_count": sum(
            states[dimension_id]["state"] == STATE_TOWARD
            for dimension_id in goal.dimension_ids
        ),
        "away_count": sum(
            states[dimension_id]["state"] == STATE_AWAY
            for dimension_id in goal.dimension_ids
        ),
        "NA_count": sum(
            states[dimension_id]["state"] == STATE_NA
            for dimension_id in goal.dimension_ids
        ),
    }
    value = Fraction(
        counts["toward_count"] - counts["away_count"],
        len(goal.dimension_ids),
    )
    return value, counts


def evaluate_case(
    goal: DeclaredGoal,
    occurrences: Sequence[SourceOccurrence],
    case: GoalVectorCase,
    *,
    ucns_profile_observation: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate one controlled case without inferring any semantic relation.

    The fixture claims are explicit inputs.  Component ``NA`` states and
    per-turn ``no-claim`` vector entries have ``sign=None`` and
    ``magnitude=None``.  The scalar projection retains separate state counts
    and therefore does not equate unavailable evidence with numeric zero.
    """

    by_id = {occurrence.occurrence_id: occurrence for occurrence in occurrences}
    if len(by_id) != len(tuple(occurrences)):
        raise ValueError("source occurrence identifiers must be unique")
    missing = [item for item in case.occurrence_order if item not in by_id]
    if missing:
        raise ValueError("case references unknown occurrences: " + ", ".join(missing))
    if set(case.occurrence_order) != set(by_id) or len(case.occurrence_order) != len(by_id):
        raise ValueError("each controlled case must contain every occurrence exactly once")

    goal_dimensions = set(goal.dimension_ids)
    for occurrence in occurrences:
        unknown = [
            claim.dimension_id
            for claim in occurrence.claims
            if claim.dimension_id not in goal_dimensions
        ]
        if unknown:
            raise ValueError("occurrence claims unknown goal dimensions: " + ", ".join(unknown))

    states: dict[str, dict[str, Any]] = {
        dimension_id: {
            "dimension_id": dimension_id,
            "state": STATE_NA,
            "sign": None,
            "magnitude": None,
            "source_occurrence_id": None,
        }
        for dimension_id in goal.dimension_ids
    }
    contradiction_ledger: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    projections: list[Fraction] = []
    motions: list[Fraction] = []
    previous_projection = Fraction(0, 1)

    for turn_ordinal, occurrence_id in enumerate(case.occurrence_order, start=1):
        occurrence = by_id[occurrence_id]
        claims_by_dimension = {
            claim.dimension_id: claim for claim in occurrence.claims
        }
        vector = []
        for dimension_id in goal.dimension_ids:
            claim = claims_by_dimension.get(dimension_id)
            if claim is None:
                vector.append(
                    {
                        "dimension_id": dimension_id,
                        "state": VECTOR_NO_CLAIM,
                        "sign": None,
                        "magnitude": None,
                    }
                )
            else:
                vector.append(
                    {
                        "dimension_id": dimension_id,
                        "state": STATE_TOWARD if claim.sign == 1 else STATE_AWAY,
                        "sign": claim.sign,
                        "magnitude": _fraction_record(Fraction(1, 1)),
                    }
                )

        relation_outcomes: list[dict[str, Any]] = []
        for claim in occurrence.claims:
            prior = dict(states[claim.dimension_id])
            outcome = "new-claim"
            contradiction_id: str | None = None
            if prior["state"] == STATE_NA:
                if claim.relation == "revision":
                    outcome = "revision-target-NA"
            elif int(prior["sign"]) == claim.sign:
                outcome = "reinforcement"
            else:
                contradiction_id = (
                    f"{case.case_id}:{claim.dimension_id}:"
                    f"{prior['source_occurrence_id']}:{occurrence.occurrence_id}"
                )
                status = "resolved" if claim.relation == "revision" else "active"
                contradiction_ledger.append(
                    {
                        "contradiction_id": contradiction_id,
                        "dimension_id": claim.dimension_id,
                        "prior_occurrence_id": prior["source_occurrence_id"],
                        "prior_sign": prior["sign"],
                        "opposing_occurrence_id": occurrence.occurrence_id,
                        "opposing_sign": claim.sign,
                        "status": status,
                        "resolved_by_occurrence_id": (
                            occurrence.occurrence_id if status == "resolved" else None
                        ),
                    }
                )
                outcome = (
                    "resolved-contradiction"
                    if status == "resolved"
                    else "active-contradiction"
                )

            states[claim.dimension_id] = {
                "dimension_id": claim.dimension_id,
                "state": STATE_TOWARD if claim.sign == 1 else STATE_AWAY,
                "sign": claim.sign,
                "magnitude": _fraction_record(Fraction(1, 1)),
                "source_occurrence_id": occurrence.occurrence_id,
            }
            relation_outcomes.append(
                {
                    "dimension_id": claim.dimension_id,
                    "declared_relation": claim.relation,
                    "prior_state": prior,
                    "outcome": outcome,
                    "contradiction_id": contradiction_id,
                    "rationale": claim.rationale,
                }
            )

        projection, counts = _projection(goal, states)
        motion = projection - previous_projection
        projections.append(projection)
        motions.append(motion)
        previous_projection = projection
        traces.append(
            {
                "turn_ordinal": turn_ordinal,
                "source_locator": {
                    "case_id": case.case_id,
                    "turn_ordinal": turn_ordinal,
                    "occurrence_id": occurrence.occurrence_id,
                    "speaker": occurrence.speaker,
                    "exact_text": occurrence.exact_text,
                },
                "declared_goal_vector": tuple(vector),
                "relation_outcomes": tuple(relation_outcomes),
                "component_state_after": _state_snapshot(goal, states),
                "state_counts": counts,
                "goal_projection": _fraction_record(projection),
                "goal_motion": _fraction_record(motion),
                "active_contradiction_ids": tuple(
                    item["contradiction_id"]
                    for item in contradiction_ledger
                    if item["status"] == "active"
                ),
                "resolved_contradiction_ids": tuple(
                    item["contradiction_id"]
                    for item in contradiction_ledger
                    if item["status"] == "resolved"
                ),
            }
        )

    active_contradictions = tuple(
        item for item in contradiction_ledger if item["status"] == "active"
    )
    terminal_projection, terminal_counts = _projection(goal, states)
    candidate_completion = (
        "candidate-complete"
        if terminal_counts["toward_count"] == len(goal.dimension_ids)
        and not active_contradictions
        else "unresolved"
    )
    ordered_occurrence_digest = _digest(case.occurrence_order)
    occurrence_multiset_digest = _digest(
        tuple(sorted(by_id[item].identity_digest for item in case.occurrence_order))
    )

    if ucns_profile_observation is None:
        profile_record: dict[str, Any] = {
            "state": STATE_NA,
            "reason": "exact UCNS profile observation was not supplied to pure case evaluation",
        }
    else:
        profile_turns = tuple(ucns_profile_observation.get("turns", ()))
        if len(profile_turns) != len(case.occurrence_order):
            raise ValueError("UCNS profile turn count does not match the controlled case")
        for index, occurrence_id in enumerate(case.occurrence_order):
            occurrence = by_id[occurrence_id]
            observed = profile_turns[index]
            if (
                observed.get("turn_index") != index
                or observed.get("speaker_id") != occurrence.speaker
                or observed.get("raw_text") != occurrence.exact_text
            ):
                raise ValueError("UCNS profile observation does not preserve exact case order")
        profile_record = {"state": "attached", **dict(ucns_profile_observation)}

    return {
        "case_id": case.case_id,
        "manipulation": case.manipulation,
        "provenance": case.provenance,
        "occurrence_order": case.occurrence_order,
        "ordered_occurrence_digest": ordered_occurrence_digest,
        "occurrence_multiset_digest": occurrence_multiset_digest,
        "turn_trace": tuple(traces),
        "contradiction_ledger": tuple(contradiction_ledger),
        "terminal_active_contradictions": active_contradictions,
        "terminal_component_state": _state_snapshot(goal, states),
        "terminal_state_counts": terminal_counts,
        "terminal_goal_projection": _fraction_record(terminal_projection),
        "goal_motion_variance": _fraction_record(_variance(motions)),
        "goal_trajectory_variance": _fraction_record(_variance(projections)),
        "candidate_completion_state": candidate_completion,
        "formal_completion": {
            "state": STATE_NA,
            "reason": "the controlled EDCM state candidate does not assign formal UCNS completion",
        },
        "ucns_profile_observation": profile_record,
    }


def _run_git(root: Path, *arguments: str) -> str:
    environment = {
        name: value for name, value in os.environ.items() if not name.startswith("GIT_")
    }
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )
    return completed.stdout


def _verify_requested_ucns_source_root(source_root: Path | None) -> bool:
    if source_root is None:
        return False
    root = source_root.resolve()
    try:
        module = importlib.import_module("ucns")
        module_file = Path(str(module.__file__)).resolve()
        module_file.relative_to(root)
        commit = _run_git(root, "rev-parse", "HEAD").strip().lower()
        status = _run_git(root, "status", "--porcelain", "--untracked-files=all")
    except (AttributeError, OSError, subprocess.CalledProcessError, ValueError) as exc:
        raise ValueError("requested UCNS source root cannot be verified") from exc
    if commit != PINNED_UCNS_COMMIT:
        raise ValueError(
            f"goal-vector experiment requires UCNS {PINNED_UCNS_COMMIT}, observed {commit}"
        )
    if status:
        raise ValueError("requested UCNS source root is not clean")
    return True


def _observe_case(
    adapter: ActualUCNSAdapter,
    case: GoalVectorCase,
    occurrences: Mapping[str, SourceOccurrence],
) -> dict[str, Any]:
    turns = tuple(
        (occurrences[item].speaker, occurrences[item].exact_text)
        for item in case.occurrence_order
    )
    state = adapter.normalize(
        {
            "source_ref": f"synthetic://edcm-goal-vector/{case.case_id}",
            "ucns_turns": turns,
        }
    )
    observation = state.get("ucns_profile_observation")
    status = state.get("ucns_integration")
    if not isinstance(observation, Mapping) or not isinstance(status, Mapping):
        raise RuntimeError("exact UCNS profile did not attach controlled observation evidence")
    if not status.get("ucns_profile_observation_attached"):
        raise RuntimeError("UCNS integration status did not record attached observation evidence")
    return dict(observation)


def _finding(
    finding_id: str,
    supported: bool,
    *,
    observed: Any,
    expected: str,
    rationale: str,
) -> dict[str, Any]:
    return {
        "finding_id": finding_id,
        "status": "supported" if supported else "falsified",
        "observed": observed,
        "expected": expected,
        "rationale": rationale,
    }


def _evaluate_findings(case_results: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any], ...]:
    by_id = {str(item["case_id"]): item for item in case_results}
    resolved = by_id["contradiction-resolved"]
    active = by_id["contradiction-active"]
    resolved_projection = _fraction_from_record(resolved["terminal_goal_projection"])
    active_projection = _fraction_from_record(active["terminal_goal_projection"])
    resolved_variance = _fraction_from_record(resolved["goal_motion_variance"])
    active_variance = _fraction_from_record(active["goal_motion_variance"])
    resolved_observation = resolved["ucns_profile_observation"]
    active_observation = active["ucns_profile_observation"]
    all_component_states = tuple(
        component
        for result in case_results
        for trace in result["turn_trace"]
        for component in trace["component_state_after"]
    )
    na_records = tuple(item for item in all_component_states if item["state"] == STATE_NA)

    return (
        _finding(
            "same-occurrence-multiset",
            resolved["occurrence_multiset_digest"] == active["occurrence_multiset_digest"],
            observed={
                "resolved": resolved["occurrence_multiset_digest"],
                "active": active["occurrence_multiset_digest"],
            },
            expected="equal",
            rationale="the manipulation changes order only",
        ),
        _finding(
            "ordered-occurrence-identity-differs",
            resolved["ordered_occurrence_digest"] != active["ordered_occurrence_digest"],
            observed={
                "resolved": resolved["ordered_occurrence_digest"],
                "active": active["ordered_occurrence_digest"],
            },
            expected="different",
            rationale="ordered occurrence identity must retain chronology",
        ),
        _finding(
            "ucns-observation-identity-differs",
            resolved_observation.get("observation_digest")
            != active_observation.get("observation_digest"),
            observed={
                "resolved": resolved_observation.get("observation_digest"),
                "active": active_observation.get("observation_digest"),
            },
            expected="different",
            rationale="the exact UCNS profile must retain the changed turn order",
        ),
        _finding(
            "resolved-terminal-contradiction-clears",
            len(resolved["terminal_active_contradictions"]) == 0,
            observed=len(resolved["terminal_active_contradictions"]),
            expected="0 active contradictions",
            rationale="the later declared schedule-change revision resolves the opposing availability claim",
        ),
        _finding(
            "reordered-terminal-contradiction-remains",
            len(active["terminal_active_contradictions"]) == 1,
            observed=len(active["terminal_active_contradictions"]),
            expected="1 active contradiction",
            rationale="the opposing availability assertion occurs after the revision and remains active",
        ),
        _finding(
            "resolved-terminal-goal-projection-greater",
            resolved_projection > active_projection,
            observed={
                "resolved": resolved["terminal_goal_projection"],
                "active": active["terminal_goal_projection"],
            },
            expected="resolved > active",
            rationale="the resolved order ends with every declared goal component toward the goal",
        ),
        _finding(
            "goal-motion-variance-differs",
            resolved_variance != active_variance,
            observed={
                "resolved": resolved["goal_motion_variance"],
                "active": active["goal_motion_variance"],
            },
            expected="different",
            rationale="ordered state changes, not the utterance multiset, determine the path variance",
        ),
        _finding(
            "NA-remains-typed",
            bool(na_records)
            and all(item["sign"] is None and item["magnitude"] is None for item in na_records),
            observed={"NA_records": len(na_records), "numeric_NA_records": 0},
            expected="all NA states have null sign and magnitude",
            rationale="unavailable goal components must not become measured zero",
        ),
    )


def run_goal_vector_experiment(
    *,
    edcm_commit: str | None = None,
    ucns_source_root: str | Path | None = None,
) -> GoalVectorExperimentReport:
    """Run the fixed current-profile goal-vector contradiction experiment."""

    source_root = Path(ucns_source_root) if ucns_source_root is not None else None
    if source_root is not None:
        # Editable producer verification requires a completely clean checkout.
        # Prevent this verification process from creating an untracked cache in
        # the producer it is about to authenticate.
        sys.dont_write_bytecode = True
    source_root_verified = _verify_requested_ucns_source_root(source_root)
    selection = select_ucns_adapter()
    if selection.adapter is None or not isinstance(selection.adapter, ActualUCNSAdapter):
        detail = "; ".join(selection.status.errors) or "exact UCNS profile unavailable"
        raise RuntimeError(detail)
    adapter = selection.adapter
    goal, occurrences, cases = build_goal_vector_program()
    by_occurrence = {item.occurrence_id: item for item in occurrences}
    case_results = tuple(
        evaluate_case(
            goal,
            occurrences,
            case,
            ucns_profile_observation=_observe_case(adapter, case, by_occurrence),
        )
        for case in cases
    )
    findings = _evaluate_findings(case_results)
    return GoalVectorExperimentReport(
        schema=PROGRAM_SCHEMA,
        program_version=PROGRAM_VERSION,
        candidate_id=CANDIDATE_ID,
        semantic_fixture_id=SEMANTIC_FIXTURE_ID,
        edcm_commit=edcm_commit or os.environ.get("GITHUB_SHA", "unrecorded-edcm-commit"),
        ucns_commit=PINNED_UCNS_COMMIT,
        ucns_profile_id=SUPPORTED_PROFILE[0],
        ucns_profile_version=SUPPORTED_PROFILE[1],
        ucns_identity_verified=True,
        ucns_source_root_verified=source_root_verified,
        goal={**asdict(goal), "goal_digest": goal.digest},
        occurrences=tuple(
            {**asdict(occurrence), "identity_digest": occurrence.identity_digest}
            for occurrence in occurrences
        ),
        case_results=case_results,
        findings=findings,
        metapat_semantic_constraints={
            "state": STATE_NA,
            "reason": "controlled semantic effects are explicit fixture declarations; no METAPAT envelope is attached",
        },
        ucns_geometry_identity={
            "state": STATE_NA,
            "reason": "the exact word-gonol observation profile does not supply formal UCNS geometry",
        },
        formal_completion={
            "state": STATE_NA,
            "reason": "candidate EDCM goal state is not formal UCNS completion",
        },
        composition_boundary={
            "word_observation": "attached-exact-ucns-profile",
            "turn_order": "preserved",
            "dialogue_trajectory": "candidate-edcm-state-sequence",
            "formal_higher_gonol_composition": STATE_NA,
        },
        candidate_measurement_status="candidate-measured-evidence",
        empirical_validity_claim=False,
        proof_status_transfer=False,
        canon_selection=None,
        notes=(
            "Hypothesis failure remains evidence and is not converted into a build failure.",
            "Scalar projections retain complete component states, NA counts, exact source locators, and declared information loss.",
            "Contradiction does not imply dishonesty, intention, diagnosis, morality, consciousness, or external truth.",
        ),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--edcm-commit", default=None)
    parser.add_argument("--ucns-source-root", type=Path, default=None)
    args = parser.parse_args(argv)

    report = run_goal_vector_experiment(
        edcm_commit=args.edcm_commit,
        ucns_source_root=args.ucns_source_root,
    )
    rendered = report.to_json()
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(
            json.dumps(
                {
                    "output": str(args.output),
                    "report_digest": report.digest,
                    "supported": sum(
                        item["status"] == "supported" for item in report.findings
                    ),
                    "falsified": sum(
                        item["status"] == "falsified" for item in report.findings
                    ),
                    "canon_selection": None,
                },
                sort_keys=True,
            )
        )
    return 0


__all__ = [
    "CANDIDATE_ID",
    "PROGRAM_SCHEMA",
    "PROGRAM_VERSION",
    "SEMANTIC_FIXTURE_ID",
    "DeclaredGoal",
    "GoalClaim",
    "GoalDimension",
    "GoalVectorCase",
    "GoalVectorExperimentReport",
    "SourceOccurrence",
    "build_goal_vector_program",
    "evaluate_case",
    "main",
    "run_goal_vector_experiment",
]


if __name__ == "__main__":
    raise SystemExit(main())
