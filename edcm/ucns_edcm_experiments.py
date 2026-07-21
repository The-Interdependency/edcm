"""Experiment-first UCNS–EDCM joint research runner.

Usage
-----
Run with the exact UCNS commit declared by :data:`EXPECTED_UCNS_COMMIT` installed:

    python -m edcm.ucns_edcm_experiments \
        --output artifacts/ucns-edcm-report.json

The generated report is research evidence. It never selects canon.
"""

# === MODULE_BUILD ===
# id: edcm_ucns_edcm_experiments
#   module_name: ucns_edcm_experiments
#   module_kind: instrument
#   summary: runs fixed contrastive EDCM cases through the maintained EDCM baseline, a transparent candidate, explicit event-to-UCNS encodings, and noncanonical UCNS equivalence/M/B candidates
#   owner: Erin Spencer
#   public_surface: ExperimentPartition, RelationOperator, ExperimentCase, ExpectedRelation, CandidateReadout, RelationVerdict, PolicyPreservationFinding, ExperimentReport, build_default_program, contrastive_readout, baseline_readout, run_default_experiments, main
#   internal_surface: _load_ucns, _split_turns, _turn_signals, _build_ucns_envelope, _structural_signatures, _evaluate_relation, _digest
#   auth_boundary: none
#   storage_boundary: writes only caller-selected report path
#   network_boundary: none; UCNS must already be installed from the pinned commit
#   user_data_boundary: fixed synthetic transcripts only in the default program
#   admin_only: false
#   tests: tests/test_ucns_edcm_experiments.py
#   rollout: explicit research runner; no default canon selection
#   rollback: remove module and workflow; frozen edcm.measurement baseline remains unchanged
#   requires: edcm_package, edcmbone_parser_turns_rounds, edcmbone_metrics_compute
#   since: 2026-07-21
#   unresolved: external holdout custody, independent replication, and first joint canon decision authority
# === END MODULE_BUILD ===

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum
from hashlib import sha256
from pathlib import Path
from statistics import fmean
from typing import Any, Callable, Iterable, Mapping

from .measurement import compute_transcript, parse_transcript

PROGRAM_SCHEMA = "edcm.ucns-edcm-experiment-report/0.1.0"
PROGRAM_VERSION = "0.1.0"
EXPECTED_UCNS_COMMIT = "5331ae9a4cf7eddfa1de72b8caed28e2358cc0ed"
BASELINE_CANDIDATE_ID = "edcm-measurement-v1"
CONTRASTIVE_CANDIDATE_ID = "edcm-contrastive-v0"


class ExperimentPartition(str, Enum):
    DEVELOPMENT = "development"
    HOLDOUT = "holdout"


class RelationOperator(str, Enum):
    LT = "lt"
    GT = "gt"
    EQ = "eq"
    NE = "ne"


@dataclass(frozen=True, slots=True)
class ExperimentCase:
    case_id: str
    transcript: str
    partition: ExperimentPartition
    manipulation: str
    provenance: str
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.case_id.strip() or not self.transcript.strip():
            raise ValueError("experiment case requires identifier and transcript")
        if not self.manipulation.strip() or not self.provenance.strip():
            raise ValueError("experiment case requires manipulation and provenance")
        object.__setattr__(self, "partition", ExperimentPartition(self.partition))
        object.__setattr__(self, "tags", tuple(self.tags))

    @property
    def digest(self) -> str:
        return _digest(
            {
                "case_id": self.case_id,
                "transcript": self.transcript,
                "partition": self.partition.value,
                "manipulation": self.manipulation,
                "provenance": self.provenance,
                "tags": self.tags,
            }
        )


@dataclass(frozen=True, slots=True)
class ExpectedRelation:
    relation_id: str
    readout: str
    left_case: str
    operator: RelationOperator
    right_case: str
    rationale: str

    def __post_init__(self) -> None:
        for value in (
            self.relation_id,
            self.readout,
            self.left_case,
            self.right_case,
            self.rationale,
        ):
            if not value.strip():
                raise ValueError("expected relation fields must be nonempty")
        object.__setattr__(self, "operator", RelationOperator(self.operator))


@dataclass(frozen=True, slots=True)
class CandidateReadout:
    candidate_id: str
    case_id: str
    values: tuple[tuple[str, Any], ...]
    source_identity: str
    error: str | None = None

    def value(self, name: str) -> Any:
        for key, value in self.values:
            if key == name:
                return value
        raise KeyError(f"readout value absent: {name}")


@dataclass(frozen=True, slots=True)
class RelationVerdict:
    relation_id: str
    readout: str
    left_case: str
    right_case: str
    operator: str
    left_value: Any
    right_value: Any
    status: str
    detail: str


@dataclass(frozen=True, slots=True)
class PolicyPreservationFinding:
    pair_id: str
    policy_name: str
    readout: str
    structures_equivalent: bool
    readout_equivalent: bool
    status: str
    information_loss: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ExperimentReport:
    schema: str
    program_version: str
    edcm_commit: str
    ucns_commit: str
    cases: tuple[ExperimentCase, ...]
    candidate_identities: tuple[tuple[str, str], ...]
    readouts: tuple[CandidateReadout, ...]
    relation_verdicts: tuple[RelationVerdict, ...]
    policy_findings: tuple[PolicyPreservationFinding, ...]
    candidate_disagreements: tuple[tuple[str, tuple[tuple[str, Any], ...]], ...]
    canon_selection: None = None
    notes: tuple[str, ...] = ()

    @property
    def digest(self) -> str:
        return _digest(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))

    def to_json(self) -> str:
        payload = self.as_dict()
        payload["report_digest"] = _digest(payload)
        return json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?")
_CONSTRAINT_PHRASES = (
    "must",
    "required",
    "no choice",
    "no alternative",
    "choose now",
    "decide now",
    "immediately",
)
_REFUSAL_PHRASES = (
    "i refuse",
    "refuse",
    "i won't",
    "will not",
    "cannot comply",
    "can't comply",
)
_RESOLUTION_PHRASES = (
    "i agree",
    "agree",
    "accepted",
    "resolved",
    "i will",
    "that works",
    "understood",
    "clarify",
    "clarification",
)


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, set):
        return sorted(_jsonable(item) for item in value)
    return value


def _digest(value: Any) -> str:
    encoded = json.dumps(
        _jsonable(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _tokens(text: str) -> tuple[str, ...]:
    return tuple(token.lower() for token in _TOKEN_RE.findall(text))


def _phrase_hits(text: str, phrases: Iterable[str]) -> int:
    lowered = text.lower()
    return sum(lowered.count(phrase) for phrase in phrases)


def _split_turns(transcript: str) -> tuple[tuple[str, str], ...]:
    parsed = parse_transcript(transcript)
    return tuple((turn.speaker, turn.text) for turn in parsed.turns)


def _turn_signals(
    text: str, normalized_text: str, seen: Mapping[str, int]
) -> dict[str, float]:
    token_count = max(1, len(_tokens(text)))
    constraint = min(1.0, _phrase_hits(text, _CONSTRAINT_PHRASES) / max(1.0, token_count / 8.0))
    refusal = min(1.0, _phrase_hits(text, _REFUSAL_PHRASES) / max(1.0, token_count / 8.0))
    resolution = min(1.0, _phrase_hits(text, _RESOLUTION_PHRASES) / max(1.0, token_count / 8.0))
    repetition = 1.0 if seen.get(normalized_text, 0) > 0 else 0.0
    return {
        "constraint": constraint,
        "refusal": refusal,
        "resolution": resolution,
        "repetition": repetition,
        "token_count": float(token_count),
    }


def contrastive_readout(case: ExperimentCase) -> dict[str, float]:
    """Transparent sequence-sensitive EDCM candidate.

    This candidate is intentionally small and inspectable. It is not canon.
    """

    turns = _split_turns(case.transcript)
    seen: dict[str, int] = {}
    constraint_total = 0.0
    refusal_total = 0.0
    resolution_total = 0.0
    repetition_total = 0.0
    token_total = 0.0
    tension = 0.0

    for _, text in turns:
        normalized = " ".join(_tokens(text))
        signals = _turn_signals(text, normalized, seen)
        seen[normalized] = seen.get(normalized, 0) + 1
        constraint_total += signals["constraint"]
        refusal_total += signals["refusal"]
        resolution_total += signals["resolution"]
        repetition_total += signals["repetition"]
        token_total += signals["token_count"]
        pressure = (
            0.35 * signals["constraint"]
            + 0.35 * signals["refusal"]
            + 0.20 * signals["repetition"]
        )
        release = 0.55 * signals["resolution"]
        tension = min(1.0, max(0.0, 0.72 * tension + pressure - release))

    count = max(1, len(turns))
    return {
        "constraint_pressure": constraint_total / count,
        "refusal_pressure": refusal_total / count,
        "resolution_signal": resolution_total / count,
        "repetition_pressure": repetition_total / count,
        "final_tension": tension,
        "turn_count": float(len(turns)),
        "token_count": token_total,
    }


def baseline_readout(case: ExperimentCase) -> dict[str, float]:
    """Summarize the frozen maintained EDCM measurement baseline."""

    parsed = parse_transcript(case.transcript)
    rounds = compute_transcript(parsed)
    if not rounds:
        raise ValueError("baseline candidate produced no rounds")

    axes = ("C", "R", "F", "E", "D", "N", "I", "O", "L", "P")
    result = {
        f"{axis}_mean": fmean(float(getattr(round_, axis)) for round_ in rounds)
        for axis in axes
    }
    result.update(
        {
            "kappa_final": float(rounds[-1].kappa),
            "energy_mean": fmean(float(round_.dissonance_energy) for round_ in rounds),
            "round_count": float(len(rounds)),
            "token_count": float(sum(round_.token_count for round_ in rounds)),
            "bone_count": float(sum(round_.bone_count for round_ in rounds)),
        }
    )
    return result


def build_default_program() -> tuple[tuple[ExperimentCase, ...], tuple[ExpectedRelation, ...]]:
    cases = (
        ExperimentCase(
            "order-resolution-last",
            "A: You must decide now.\nB: I refuse.\nA: Let me clarify the constraint.\nB: I agree; that works.",
            ExperimentPartition.DEVELOPMENT,
            "same turns, resolution occurs last",
            "synthetic contrast authored for UCNS-EDCM experiment v0",
            ("order", "resolution"),
        ),
        ExperimentCase(
            "order-refusal-last",
            "A: Let me clarify the constraint.\nB: I agree; that works.\nA: You must decide now.\nB: I refuse.",
            ExperimentPartition.DEVELOPMENT,
            "same turns, refusal occurs last",
            "synthetic contrast authored for UCNS-EDCM experiment v0",
            ("order", "refusal"),
        ),
        ExperimentCase(
            "single-refusal",
            "A: You must decide now.\nB: I refuse.",
            ExperimentPartition.DEVELOPMENT,
            "one refusal occurrence",
            "synthetic contrast authored for UCNS-EDCM experiment v0",
            ("multiplicity",),
        ),
        ExperimentCase(
            "repeated-refusal",
            "A: You must decide now.\nB: I refuse.\nB: I refuse.",
            ExperimentPartition.DEVELOPMENT,
            "same unique turns with refusal repeated",
            "synthetic contrast authored for UCNS-EDCM experiment v0",
            ("multiplicity", "repetition"),
        ),
        ExperimentCase(
            "low-constraint",
            "A: Please choose tea or coffee when ready.\nB: I choose tea.",
            ExperimentPartition.HOLDOUT,
            "ordinary choice request",
            "synthetic holdout authored for UCNS-EDCM experiment v0",
            ("constraint", "holdout"),
        ),
        ExperimentCase(
            "high-constraint",
            "A: You must choose now. There is no choice and no alternative.\nB: I refuse.",
            ExperimentPartition.HOLDOUT,
            "forced immediacy and removed alternatives",
            "synthetic holdout authored for UCNS-EDCM experiment v0",
            ("constraint", "holdout"),
        ),
        ExperimentCase(
            "unresolved-pressure",
            "A: You must decide now.\nB: I refuse.",
            ExperimentPartition.HOLDOUT,
            "pressure without repair",
            "synthetic holdout authored for UCNS-EDCM experiment v0",
            ("resolution", "holdout"),
        ),
        ExperimentCase(
            "resolved-pressure",
            "A: You must decide now.\nB: I refuse.\nA: Let me clarify the constraint.\nB: I agree; that works.",
            ExperimentPartition.HOLDOUT,
            "same initial pressure followed by repair",
            "synthetic holdout authored for UCNS-EDCM experiment v0",
            ("resolution", "holdout"),
        ),
    )

    relations = (
        ExpectedRelation(
            "order-contrastive-tension",
            "edcm.contrastive.final_tension",
            "order-resolution-last",
            RelationOperator.LT,
            "order-refusal-last",
            "resolution last should leave less stored tension than refusal last",
        ),
        ExpectedRelation(
            "order-baseline-kappa",
            "edcm.baseline.kappa_final",
            "order-resolution-last",
            RelationOperator.LT,
            "order-refusal-last",
            "the maintained circuit candidate is tested for resolution timing sensitivity",
        ),
        ExpectedRelation(
            "multiplicity-contrastive-refusal",
            "edcm.contrastive.refusal_pressure",
            "repeated-refusal",
            RelationOperator.GT,
            "single-refusal",
            "exact refusal repetition should increase refusal pressure",
        ),
        ExpectedRelation(
            "multiplicity-baseline-refusal",
            "edcm.baseline.R_mean",
            "repeated-refusal",
            RelationOperator.GT,
            "single-refusal",
            "the maintained refusal candidate is tested for occurrence sensitivity",
        ),
        ExpectedRelation(
            "constraint-contrastive",
            "edcm.contrastive.constraint_pressure",
            "high-constraint",
            RelationOperator.GT,
            "low-constraint",
            "forced immediacy and removed alternatives should increase transparent constraint pressure",
        ),
        ExpectedRelation(
            "constraint-baseline",
            "edcm.baseline.C_mean",
            "high-constraint",
            RelationOperator.GT,
            "low-constraint",
            "the maintained marker canon is tested on the holdout phrasing",
        ),
        ExpectedRelation(
            "resolution-contrastive",
            "edcm.contrastive.final_tension",
            "resolved-pressure",
            RelationOperator.LT,
            "unresolved-pressure",
            "repair after refusal should reduce final transparent tension",
        ),
        ExpectedRelation(
            "resolution-baseline",
            "edcm.baseline.kappa_final",
            "resolved-pressure",
            RelationOperator.LT,
            "unresolved-pressure",
            "the maintained circuit candidate is tested for repair sensitivity",
        ),
        ExpectedRelation(
            "pressure-breadth-holdout",
            "ucns.pressure-turn.B.cell-detail",
            "high-constraint",
            RelationOperator.GT,
            "low-constraint",
            "pressure-weighted cell detail should preserve the stronger declared signal",
        ),
        ExpectedRelation(
            "unit-breadth-multiplicity",
            "ucns.unit-turn.B.cell-detail",
            "repeated-refusal",
            RelationOperator.GT,
            "single-refusal",
            "unit-turn cell detail should preserve occurrence multiplicity",
        ),
    )
    return cases, relations


def _load_ucns() -> dict[str, Any]:
    try:
        from ucns import (
            RetainedLayer,
            StructurePolicy,
            apply_policy,
            cell_support_weight,
            combined_comparison_policy,
            make_carrier,
            make_retained_structure,
            ordered_sequence_policy,
            set_policy,
            unordered_multiset_policy,
        )
        from ucns.candidates import (
            cell_detail_breadth_candidate,
            cell_log_support_breadth_candidate,
            geometric_mean_product_candidate,
            maximum_support_product_candidate,
            minimum_support_product_candidate,
            retained_presence_breadth_candidate,
        )
        from ucns.structure import Cell
    except Exception as exc:  # pragma: no cover - exercised in integration workflow
        raise RuntimeError(
            "UCNS experiment dependency is unavailable; install the exact pinned commit"
        ) from exc

    return locals()


def _build_ucns_envelope(
    case: ExperimentCase, support_policy: str, ucns_api: Mapping[str, Any]
) -> Any:
    Cell = ucns_api["Cell"]
    RetainedLayer = ucns_api["RetainedLayer"]
    make_carrier = ucns_api["make_carrier"]
    make_retained_structure = ucns_api["make_retained_structure"]

    turns = _split_turns(case.transcript)
    seen: dict[str, int] = {}
    cells = []
    turn_evidence = []
    previous_speaker: str | None = None

    for index, (speaker, text) in enumerate(turns):
        normalized = " ".join(_tokens(text))
        signals = _turn_signals(text, normalized, seen)
        seen[normalized] = seen.get(normalized, 0) + 1
        if support_policy == "unit-turn":
            mu = 1.0
        elif support_policy == "token-turn":
            mu = signals["token_count"]
        elif support_policy == "pressure-turn":
            mu = 1.0 + sum(
                signals[name]
                for name in ("constraint", "refusal", "resolution", "repetition")
            )
        else:
            raise KeyError(f"unknown support policy: {support_policy}")

        state = tuple(sorted((key, float(value)) for key, value in signals.items()))
        relation = (previous_speaker, speaker)
        cells.append(
            Cell(
                coordinate=index,
                payload=text,
                type_tag=speaker,
                state=state,
                provenance=(case.case_id, support_policy),
                relation=relation,
                mu=mu,
            )
        )
        turn_evidence.append({"speaker": speaker, "text": text})
        previous_speaker = speaker

    carrier = make_carrier(tuple(cells))
    layers = (
        RetainedLayer("turns", tuple(turn_evidence)),
        RetainedLayer("raw-transcript", case.transcript),
        RetainedLayer(
            "case-provenance",
            {
                "case_id": case.case_id,
                "partition": case.partition.value,
                "support_policy": support_policy,
                "case_digest": case.digest,
            },
        ),
    )
    return make_retained_structure(carrier, layers)


def _canonical_projection_view(policy_name: str, projection: Any) -> Any:
    view = projection.view
    if policy_name == "ordered-sequence":
        return _jsonable(view)
    if policy_name == "unordered-multiset":
        groups = []
        for group in view:
            groups.append((str(group.key), int(group.count)))
        return sorted(groups)
    if policy_name == "set":
        return sorted(str(entry.key) for entry in view)
    return _jsonable(view)


def _structural_signatures(envelope: Any, ucns_api: Mapping[str, Any]) -> dict[str, Any]:
    apply_policy = ucns_api["apply_policy"]
    ordered_sequence_policy = ucns_api["ordered_sequence_policy"]
    unordered_multiset_policy = ucns_api["unordered_multiset_policy"]
    set_policy = ucns_api["set_policy"]

    turns_layer = envelope.layer("turns")
    key = lambda item: json.dumps(item, sort_keys=True, separators=(",", ":"))
    policies = (
        ordered_sequence_policy(),
        unordered_multiset_policy(key),
        set_policy(key),
    )
    result: dict[str, Any] = {}
    for policy in policies:
        projection = apply_policy(turns_layer.evidence, policy)
        result[policy.name] = {
            "signature": _digest(_canonical_projection_view(policy.name, projection)),
            "losses": tuple(loss.dimension for loss in projection.losses),
        }
    return result


def _candidate_values_for_case(
    case: ExperimentCase,
    ucns_api: Mapping[str, Any],
) -> tuple[list[CandidateReadout], dict[str, dict[str, Any]]]:
    readouts: list[CandidateReadout] = []

    for candidate_id, evaluator in (
        (BASELINE_CANDIDATE_ID, baseline_readout),
        (CONTRASTIVE_CANDIDATE_ID, contrastive_readout),
    ):
        try:
            values = evaluator(case)
            error = None
        except Exception as exc:
            values = {}
            error = f"{type(exc).__name__}: {exc}"
        prefix = "edcm.baseline" if candidate_id == BASELINE_CANDIDATE_ID else "edcm.contrastive"
        readouts.append(
            CandidateReadout(
                candidate_id,
                case.case_id,
                tuple((f"{prefix}.{key}", value) for key, value in sorted(values.items())),
                f"The-Interdependency/edcm:{candidate_id}",
                error,
            )
        )

    structural: dict[str, dict[str, Any]] = {}
    m_candidates = (
        ("cell-support-geometric-mean", ucns_api["geometric_mean_product_candidate"]()),
        ("cell-support-maximum", ucns_api["maximum_support_product_candidate"]()),
        ("cell-support-minimum", ucns_api["minimum_support_product_candidate"]()),
    )
    b_candidates = (
        ("cell-log-support", ucns_api["cell_log_support_breadth_candidate"]()),
        ("cell-detail", ucns_api["cell_detail_breadth_candidate"]()),
        ("retained-presence", ucns_api["retained_presence_breadth_candidate"]()),
    )

    for support_policy in ("unit-turn", "token-turn", "pressure-turn"):
        envelope = _build_ucns_envelope(case, support_policy, ucns_api)
        structural[support_policy] = _structural_signatures(envelope, ucns_api)
        values: list[tuple[str, Any]] = []
        values.append(
            (
                f"ucns.{support_policy}.W.cell-support",
                float(ucns_api["cell_support_weight"](envelope)),
            )
        )
        for name, candidate in m_candidates:
            values.append((f"ucns.{support_policy}.M.{name}", candidate.evaluate(envelope)))
        for name, candidate in b_candidates:
            values.append((f"ucns.{support_policy}.B.{name}", candidate.evaluate(envelope)))
        readouts.append(
            CandidateReadout(
                f"ucns-{support_policy}-candidate-pack",
                case.case_id,
                tuple(values),
                f"The-Interdependency/ucns@{EXPECTED_UCNS_COMMIT}",
            )
        )
    return readouts, structural


def _readout_index(readouts: Iterable[CandidateReadout]) -> dict[tuple[str, str], Any]:
    index: dict[tuple[str, str], Any] = {}
    for readout in readouts:
        if readout.error is not None:
            continue
        for name, value in readout.values:
            index[(readout.case_id, name)] = value
    return index


def _evaluate_relation(
    relation: ExpectedRelation, index: Mapping[tuple[str, str], Any], comparison: Any
) -> RelationVerdict:
    left_key = (relation.left_case, relation.readout)
    right_key = (relation.right_case, relation.readout)
    if left_key not in index or right_key not in index:
        return RelationVerdict(
            relation.relation_id,
            relation.readout,
            relation.left_case,
            relation.right_case,
            relation.operator.value,
            index.get(left_key),
            index.get(right_key),
            "error",
            "one or both readouts are absent",
        )
    left = index[left_key]
    right = index[right_key]
    try:
        if relation.operator is RelationOperator.EQ:
            passed = comparison.matches(left, right)
        elif relation.operator is RelationOperator.NE:
            passed = not comparison.matches(left, right)
        elif relation.operator is RelationOperator.LT:
            passed = float(left) < float(right) and not comparison.matches(left, right)
        else:
            passed = float(left) > float(right) and not comparison.matches(left, right)
    except Exception as exc:
        return RelationVerdict(
            relation.relation_id,
            relation.readout,
            relation.left_case,
            relation.right_case,
            relation.operator.value,
            left,
            right,
            "error",
            f"{type(exc).__name__}: {exc}",
        )
    return RelationVerdict(
        relation.relation_id,
        relation.readout,
        relation.left_case,
        relation.right_case,
        relation.operator.value,
        left,
        right,
        "supported" if passed else "falsified",
        relation.rationale,
    )


def _policy_findings(
    structural: Mapping[str, Mapping[str, Mapping[str, Any]]],
    index: Mapping[tuple[str, str], Any],
    comparison: Any,
) -> tuple[PolicyPreservationFinding, ...]:
    pair_specs = (
        (
            "order-pair",
            "order-resolution-last",
            "order-refusal-last",
            ("edcm.contrastive.final_tension", "edcm.baseline.kappa_final"),
        ),
        (
            "multiplicity-pair",
            "single-refusal",
            "repeated-refusal",
            ("edcm.contrastive.refusal_pressure", "edcm.baseline.R_mean"),
        ),
        (
            "resolution-pair",
            "unresolved-pressure",
            "resolved-pressure",
            ("edcm.contrastive.final_tension", "edcm.baseline.kappa_final"),
        ),
    )
    findings: list[PolicyPreservationFinding] = []
    for pair_id, left_case, right_case, readout_names in pair_specs:
        for policy_name in ("ordered-sequence", "unordered-multiset", "set"):
            left_view = structural[left_case]["unit-turn"][policy_name]
            right_view = structural[right_case]["unit-turn"][policy_name]
            structures_equivalent = left_view["signature"] == right_view["signature"]
            losses = tuple(sorted(set(left_view["losses"]) | set(right_view["losses"])))
            for readout_name in readout_names:
                left_value = index.get((left_case, readout_name))
                right_value = index.get((right_case, readout_name))
                if left_value is None or right_value is None:
                    readout_equivalent = False
                    status = "inconclusive"
                else:
                    readout_equivalent = comparison.matches(left_value, right_value)
                    if structures_equivalent and not readout_equivalent:
                        status = "incompatible-for-readout"
                    elif not structures_equivalent and not readout_equivalent:
                        status = "preserves-observed-distinction"
                    elif structures_equivalent and readout_equivalent:
                        status = "compatible-on-this-pair"
                    else:
                        status = "structurally-distinct-readout-invariant"
                findings.append(
                    PolicyPreservationFinding(
                        pair_id,
                        policy_name,
                        readout_name,
                        structures_equivalent,
                        readout_equivalent,
                        status,
                        losses,
                    )
                )
    return tuple(findings)


def _candidate_disagreements(
    cases: Iterable[ExperimentCase], index: Mapping[tuple[str, str], Any]
) -> tuple[tuple[str, tuple[tuple[str, Any], ...]], ...]:
    rows = []
    for case in cases:
        rows.append(
            (
                case.case_id,
                tuple(
                    sorted(
                        (
                            name,
                            value,
                        )
                        for (case_id, name), value in index.items()
                        if case_id == case.case_id
                        and (
                            name.startswith("edcm.")
                            or name.startswith("ucns.pressure-turn.B.")
                        )
                    )
                ),
            )
        )
    return tuple(rows)


def run_default_experiments(
    *, edcm_commit: str | None = None, ucns_commit: str = EXPECTED_UCNS_COMMIT
) -> ExperimentReport:
    """Run the fixed v0 joint experiment program.

    The caller is responsible for installing UCNS from ``ucns_commit``. The
    commit is recorded but cannot be inferred from package availability alone.
    """

    if ucns_commit != EXPECTED_UCNS_COMMIT:
        raise ValueError(
            f"this experiment version requires UCNS {EXPECTED_UCNS_COMMIT}, got {ucns_commit}"
        )
    ucns_api = _load_ucns()
    comparison = ucns_api["combined_comparison_policy"](
        rel_tol=1e-9,
        abs_tol=1e-12,
        name="ucns-edcm-combined",
        version="1",
    )
    cases, relations = build_default_program()
    all_readouts: list[CandidateReadout] = []
    structural: dict[str, dict[str, Any]] = {}
    for case in cases:
        case_readouts, case_structural = _candidate_values_for_case(case, ucns_api)
        all_readouts.extend(case_readouts)
        structural[case.case_id] = case_structural

    index = _readout_index(all_readouts)
    verdicts = tuple(_evaluate_relation(relation, index, comparison) for relation in relations)
    findings = _policy_findings(structural, index, comparison)
    candidate_identities = (
        (BASELINE_CANDIDATE_ID, "The-Interdependency/edcm:edcm/measurement@0.1.0"),
        (CONTRASTIVE_CANDIDATE_ID, "The-Interdependency/edcm:edcm.ucns_edcm_experiments"),
        ("ucns-candidate-pack", f"The-Interdependency/ucns@{ucns_commit}"),
        ("comparison-policy", "ucns-edcm-combined/1(rel=1e-9,abs=1e-12)"),
    )
    return ExperimentReport(
        PROGRAM_SCHEMA,
        PROGRAM_VERSION,
        edcm_commit or os.environ.get("GITHUB_SHA", "unrecorded-edcm-commit"),
        ucns_commit,
        cases,
        candidate_identities,
        tuple(all_readouts),
        verdicts,
        findings,
        _candidate_disagreements(cases, index),
        None,
        (
            "Hypothesis failure remains evidence and does not fail the build.",
            "No candidate, policy, axis, threshold, M, B, or equivalence relation is selected as canon.",
        ),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--edcm-commit", default=None)
    parser.add_argument("--ucns-commit", default=EXPECTED_UCNS_COMMIT)
    args = parser.parse_args(argv)

    report = run_default_experiments(
        edcm_commit=args.edcm_commit,
        ucns_commit=args.ucns_commit,
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
                        verdict.status == "supported" for verdict in report.relation_verdicts
                    ),
                    "falsified": sum(
                        verdict.status == "falsified" for verdict in report.relation_verdicts
                    ),
                    "errors": sum(
                        verdict.status == "error" for verdict in report.relation_verdicts
                    ),
                    "canon_selection": None,
                },
                sort_keys=True,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
