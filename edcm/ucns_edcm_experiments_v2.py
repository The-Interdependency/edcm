"""Second UCNS–EDCM experiment program: falsifier expansion and calibration.

Usage
-----
Run only with the exact verified UCNS checkout required by v0.1:

    python -m edcm.ucns_edcm_experiments_v2 \
        --ucns-source-root /path/to/ucns \
        --output artifacts/ucns-edcm-v0.2.0.json

The report preserves every supported, falsified, and errored relation. It never
selects canon or mutates the immutable v0.1 result.
"""

# === MODULE_BUILD ===
# id: edcm_ucns_edcm_experiments_v2
#   module_name: ucns_edcm_experiments_v2
#   module_kind: instrument
#   summary: expands the joint UCNS-EDCM falsifier program across refusal dose, constraint paraphrase coverage, resolution latency, and explicit support-assignment stability
#   owner: Erin Spencer
#   public_surface: V2ExperimentReport, DoseCurveFinding, PhraseCoverageFinding, LatencyFinding, SupportStabilityFinding, occurrence_coverage_readout, build_v2_program, run_v2_experiments, main
#   internal_surface: _phrase_counts, _v2_turn_signals, _build_v2_envelope, _candidate_values_for_case, _dose_curve_findings, _phrase_coverage_findings, _latency_findings, _support_findings
#   auth_boundary: none
#   storage_boundary: writes only caller-selected report path
#   network_boundary: none; exact UCNS checkout and installed package are verified locally
#   user_data_boundary: fixed synthetic development and holdout transcripts only
#   admin_only: false
#   tests: tests/test_ucns_edcm_experiments_v2.py
#   rollout: explicit versioned research program; v0.1 evidence remains immutable and no canon selection is made
#   rollback: remove v0.2 module, workflow calls, and result; v0.1 and frozen baseline remain unchanged
#   requires: edcm_ucns_edcm_experiments, edcmbone_parser_turns_rounds, edcmbone_metrics_compute
#   since: 2026-07-21
#   unresolved: independent paraphrase corpus, external outcome labels, sealed holdout custody, replication, and joint canon decision authority
# === END MODULE_BUILD ===

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .ucns_edcm_experiments import (
    BASELINE_CANDIDATE_ID,
    CandidateReadout,
    ExpectedRelation,
    ExperimentCase,
    ExperimentPartition,
    RelationOperator,
    RelationVerdict,
    StructuralSignatureRecord,
    _digest,
    _evaluate_relation,
    _flatten_structural_signatures,
    _jsonable,
    _load_ucns,
    _readout_index,
    _split_turns,
    _structural_signatures,
    _tokens,
    _verify_ucns_identity,
    baseline_readout,
    EXPECTED_UCNS_COMMIT,
)

PROGRAM_SCHEMA = "edcm.ucns-edcm-experiment-report/0.2.0"
PROGRAM_VERSION = "0.2.0"
PRIOR_PROGRAM_SCHEMA = "edcm.ucns-edcm-experiment-report/0.1.0"
PRIOR_REPORT_DIGEST = "4c8bd8496ec549c1073320bafc995c7c65eaf81c9385e4dc6fff7794ed3b1124"
OCCURRENCE_CANDIDATE_ID = "edcm-occurrence-coverage-v1"

_CONSTRAINT_FAMILIES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("obligation", ("must", "required", "have to", "need to", "mandatory")),
    (
        "alternatives-removed",
        (
            "no choice",
            "no alternative",
            "only option",
            "only one permitted option",
            "nothing else is allowed",
        ),
    ),
    (
        "immediacy-deadline",
        (
            "decide now",
            "choose now",
            "immediately",
            "window closes",
            "before noon",
            "by noon",
            "deadline",
        ),
    ),
    (
        "consequence",
        (
            "will be revoked",
            "will lose access",
            "penalty",
            "or else",
            "access is denied",
        ),
    ),
)
_REFUSAL_PHRASES = (
    "i refuse",
    "i won't",
    "will not comply",
    "cannot comply",
    "can't comply",
    "i decline",
)
_RESOLUTION_PHRASES = (
    "i agree",
    "accepted",
    "that works",
    "clarification",
    "clarify",
    "compromise",
    "resolved",
    "understood",
)


@dataclass(frozen=True, slots=True)
class DoseCurveFinding:
    candidate_id: str
    readout: str
    case_ids: tuple[str, ...]
    values: tuple[float, ...]
    strictly_increasing: bool
    nondecreasing: bool
    plateau_pairs: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class PhraseCoverageFinding:
    candidate_id: str
    readout: str
    family: str
    high_case: str
    low_case: str
    high_value: float
    low_value: float
    detected_high: bool
    false_positive_low: bool
    status: str


@dataclass(frozen=True, slots=True)
class LatencyFinding:
    candidate_id: str
    readout: str
    immediate_case: str
    delayed_case: str
    unresolved_case: str
    immediate_value: float
    delayed_value: float
    unresolved_value: float
    status: str


@dataclass(frozen=True, slots=True)
class SupportStabilityFinding:
    pair_id: str
    readout: str
    support_policy: str
    left_case: str
    right_case: str
    left_value: float
    right_value: float
    expected_direction: str
    status: str


@dataclass(frozen=True, slots=True)
class V2ExperimentReport:
    schema: str
    program_version: str
    prior_program_schema: str
    prior_report_digest: str
    edcm_commit: str
    ucns_commit: str
    ucns_source_manifest: str
    ucns_identity_verified: bool
    cases: tuple[ExperimentCase, ...]
    candidate_identities: tuple[tuple[str, str], ...]
    readouts: tuple[CandidateReadout, ...]
    structural_signatures: tuple[StructuralSignatureRecord, ...]
    relation_verdicts: tuple[RelationVerdict, ...]
    dose_curves: tuple[DoseCurveFinding, ...]
    phrase_coverage: tuple[PhraseCoverageFinding, ...]
    latency_findings: tuple[LatencyFinding, ...]
    support_stability: tuple[SupportStabilityFinding, ...]
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


def _phrase_occurrences(text: str, phrases: Iterable[str]) -> int:
    lowered = text.lower()
    return sum(lowered.count(phrase) for phrase in phrases)


def _phrase_counts(text: str) -> dict[str, int]:
    family_counts = {
        family: _phrase_occurrences(text, phrases)
        for family, phrases in _CONSTRAINT_FAMILIES
    }
    return {
        **{f"constraint.{family}": count for family, count in family_counts.items()},
        "constraint.total": sum(family_counts.values()),
        "refusal.total": _phrase_occurrences(text, _REFUSAL_PHRASES),
        "resolution.total": _phrase_occurrences(text, _RESOLUTION_PHRASES),
    }


def _v2_turn_signals(
    text: str, normalized_text: str, seen: Mapping[str, int]
) -> dict[str, float]:
    counts = _phrase_counts(text)
    return {
        "constraint": float(counts["constraint.total"]),
        "constraint_families": float(
            sum(counts[f"constraint.{family}"] > 0 for family, _ in _CONSTRAINT_FAMILIES)
        ),
        "refusal": float(counts["refusal.total"]),
        "resolution": float(counts["resolution.total"]),
        "repetition": 1.0 if seen.get(normalized_text, 0) > 0 else 0.0,
        "token_count": float(max(1, len(_tokens(text)))),
    }


def occurrence_coverage_readout(case: ExperimentCase) -> dict[str, float]:
    """Occurrence-preserving, phrase-family EDCM candidate.

    This candidate pressures the two v0.1 falsifiers. It records raw event
    occurrences rather than clipping each axis to [0, 1]. It remains a candidate
    and intentionally exposes its simple recurrence.
    """

    turns = _split_turns(case.transcript)
    seen: dict[str, int] = {}
    totals = {
        "constraint": 0.0,
        "constraint_families": 0.0,
        "refusal": 0.0,
        "resolution": 0.0,
        "repetition": 0.0,
        "token_count": 0.0,
    }
    tension = 0.0
    tension_area = 0.0
    peak_tension = 0.0
    first_pressure: int | None = None
    first_resolution_after_pressure: int | None = None

    for index, (_, text) in enumerate(turns):
        normalized = " ".join(_tokens(text))
        signals = _v2_turn_signals(text, normalized, seen)
        seen[normalized] = seen.get(normalized, 0) + 1
        for name in totals:
            totals[name] += signals[name]

        pressure = (
            0.30 * signals["constraint"]
            + 0.55 * signals["refusal"]
            + 0.20 * signals["repetition"]
        )
        release = 0.65 * signals["resolution"]
        if pressure > 0.0 and first_pressure is None:
            first_pressure = index
        if (
            first_pressure is not None
            and signals["resolution"] > 0.0
            and first_resolution_after_pressure is None
        ):
            first_resolution_after_pressure = index

        tension = max(0.0, 0.78 * tension + pressure - release)
        tension_area += tension
        peak_tension = max(peak_tension, tension)

    turn_count = float(len(turns))
    latency = (
        -1.0
        if first_pressure is None or first_resolution_after_pressure is None
        else float(first_resolution_after_pressure - first_pressure)
    )
    return {
        "constraint_occurrences": totals["constraint"],
        "constraint_family_hits": totals["constraint_families"],
        "refusal_occurrences": totals["refusal"],
        "resolution_occurrences": totals["resolution"],
        "repetition_occurrences": totals["repetition"],
        "refusal_rate": totals["refusal"] / max(1.0, turn_count),
        "final_tension": tension,
        "tension_area": tension_area,
        "peak_tension": peak_tension,
        "resolution_latency": latency,
        "resolution_latency_horizon": (
            float(len(turns) + 1)
            if first_pressure is not None and first_resolution_after_pressure is None
            else latency
        ),
        "turn_count": turn_count,
        "token_count": totals["token_count"],
    }


def build_v2_program() -> tuple[
    tuple[ExperimentCase, ...],
    tuple[ExpectedRelation, ...],
    tuple[tuple[str, str, str], ...],
]:
    provenance_dev = "synthetic development contrast authored for UCNS-EDCM experiment v0.2"
    provenance_holdout = "synthetic holdout contrast authored for UCNS-EDCM experiment v0.2"
    cases = (
        ExperimentCase(
            "refusal-dose-0",
            "A: Please decide when ready.\nB: I will consider it.",
            ExperimentPartition.DEVELOPMENT,
            "zero explicit refusal occurrences",
            provenance_dev,
            ("refusal-dose", "zero"),
        ),
        ExperimentCase(
            "refusal-dose-1",
            "A: Please decide when ready.\nB: I refuse.",
            ExperimentPartition.DEVELOPMENT,
            "one explicit refusal occurrence",
            provenance_dev,
            ("refusal-dose", "one"),
        ),
        ExperimentCase(
            "refusal-dose-2",
            "A: Please decide when ready.\nB: I refuse.\nB: I will not comply.",
            ExperimentPartition.DEVELOPMENT,
            "two refusal phrasings",
            provenance_dev,
            ("refusal-dose", "two", "paraphrase"),
        ),
        ExperimentCase(
            "refusal-dose-4",
            "A: Please decide when ready.\nB: I refuse.\nB: I will not comply.\nB: I cannot comply.\nB: I decline.",
            ExperimentPartition.HOLDOUT,
            "four refusal phrasings",
            provenance_holdout,
            ("refusal-dose", "four", "holdout", "paraphrase"),
        ),
        ExperimentCase(
            "constraint-known-low",
            "A: You may choose any option when ready.\nB: I will consider it.",
            ExperimentPartition.DEVELOPMENT,
            "low-pressure control for known marker phrasing",
            provenance_dev,
            ("constraint", "control", "known"),
        ),
        ExperimentCase(
            "constraint-known-high",
            "A: You must choose now; there is no alternative.\nB: I refuse.",
            ExperimentPartition.DEVELOPMENT,
            "obligation, immediacy, and removed alternatives",
            provenance_dev,
            ("constraint", "high", "known"),
        ),
        ExperimentCase(
            "constraint-option-low",
            "A: Several options remain available until noon.\nB: I will consider them.",
            ExperimentPartition.HOLDOUT,
            "available alternatives and time",
            provenance_holdout,
            ("constraint", "control", "option"),
        ),
        ExperimentCase(
            "constraint-option-high",
            "A: Only one permitted option remains and the window closes at noon.\nB: I decline.",
            ExperimentPartition.HOLDOUT,
            "only permitted option plus deadline",
            provenance_holdout,
            ("constraint", "high", "option", "paraphrase"),
        ),
        ExperimentCase(
            "constraint-consequence-low",
            "A: You can decide later without penalty.\nB: I will consider it.",
            ExperimentPartition.HOLDOUT,
            "no deadline and no adverse consequence",
            provenance_holdout,
            ("constraint", "control", "consequence"),
        ),
        ExperimentCase(
            "constraint-consequence-high",
            "A: Decide immediately or access will be revoked.\nB: I cannot comply.",
            ExperimentPartition.HOLDOUT,
            "immediacy plus explicit adverse consequence",
            provenance_holdout,
            ("constraint", "high", "consequence", "paraphrase"),
        ),
        ExperimentCase(
            "constraint-authority-low",
            "A: This is a suggestion; participation is optional.\nB: Understood.",
            ExperimentPartition.DEVELOPMENT,
            "optional suggestion control",
            provenance_dev,
            ("constraint", "control", "authority"),
        ),
        ExperimentCase(
            "constraint-authority-high",
            "A: Compliance is mandatory before entry.\nB: I refuse.",
            ExperimentPartition.HOLDOUT,
            "mandatory compliance condition",
            provenance_holdout,
            ("constraint", "high", "authority", "paraphrase"),
        ),
        ExperimentCase(
            "resolution-immediate",
            "A: You must decide now.\nB: I refuse.\nA: Let me clarify.\nB: I agree; that works.",
            ExperimentPartition.DEVELOPMENT,
            "repair immediately follows first refusal",
            provenance_dev,
            ("resolution-latency", "immediate"),
        ),
        ExperimentCase(
            "resolution-delayed",
            "A: You must decide now.\nB: I refuse.\nA: Compliance is required immediately.\nB: I will not comply.\nA: Let me clarify.\nB: I agree; that works.",
            ExperimentPartition.HOLDOUT,
            "repair follows a second pressure-refusal cycle",
            provenance_holdout,
            ("resolution-latency", "delayed"),
        ),
        ExperimentCase(
            "resolution-absent",
            "A: You must decide now.\nB: I refuse.\nA: Compliance is required immediately.\nB: I will not comply.",
            ExperimentPartition.HOLDOUT,
            "no repair follows repeated pressure",
            provenance_holdout,
            ("resolution-latency", "absent"),
        ),
        ExperimentCase(
            "resolution-preemptive",
            "A: Let me clarify.\nB: I agree; that works.\nA: You must decide now.\nB: I refuse.",
            ExperimentPartition.DEVELOPMENT,
            "same repair and pressure events with repair before pressure",
            provenance_dev,
            ("resolution-latency", "preemptive", "order"),
        ),
    )

    relations: list[ExpectedRelation] = []
    dose_cases = ("refusal-dose-0", "refusal-dose-1", "refusal-dose-2", "refusal-dose-4")
    for left, right in zip(dose_cases, dose_cases[1:]):
        relations.extend(
            (
                ExpectedRelation(
                    f"dose-occurrence-{left}-{right}",
                    "edcm.occurrence.refusal_occurrences",
                    left,
                    RelationOperator.LT,
                    right,
                    "raw refusal occurrences should rise with the declared dose",
                ),
                ExpectedRelation(
                    f"dose-tension-area-{left}-{right}",
                    "edcm.occurrence.tension_area",
                    left,
                    RelationOperator.LT,
                    right,
                    "accumulated candidate tension should rise with refusal dose",
                ),
                ExpectedRelation(
                    f"dose-baseline-R-{left}-{right}",
                    "edcm.baseline.R_mean",
                    left,
                    RelationOperator.LT,
                    right,
                    "the frozen baseline refusal axis is retested for unsaturated dose sensitivity",
                ),
            )
        )

    phrase_pairs = (
        ("known", "constraint-known-low", "constraint-known-high"),
        ("option", "constraint-option-low", "constraint-option-high"),
        ("consequence", "constraint-consequence-low", "constraint-consequence-high"),
        ("authority", "constraint-authority-low", "constraint-authority-high"),
    )
    for family, low, high in phrase_pairs:
        relations.extend(
            (
                ExpectedRelation(
                    f"coverage-occurrence-{family}",
                    "edcm.occurrence.constraint_occurrences",
                    high,
                    RelationOperator.GT,
                    low,
                    "the phrase-family candidate should detect declared constraint pressure",
                ),
                ExpectedRelation(
                    f"coverage-baseline-{family}",
                    "edcm.baseline.C_mean",
                    high,
                    RelationOperator.GT,
                    low,
                    "the frozen baseline constraint axis is retested across paraphrase families",
                ),
                ExpectedRelation(
                    f"coverage-ucns-dissonance-{family}",
                    "ucns.dissonance-turn.B.cell-detail",
                    high,
                    RelationOperator.GT,
                    low,
                    "dissonance-weighted support should preserve the declared high/low contrast",
                ),
            )
        )

    relations.extend(
        (
            ExpectedRelation(
                "latency-occurrence-horizon-immediate-delayed",
                "edcm.occurrence.resolution_latency_horizon",
                "resolution-immediate",
                RelationOperator.LT,
                "resolution-delayed",
                "delayed repair should have a longer pressure-to-resolution horizon",
            ),
            ExpectedRelation(
                "latency-occurrence-horizon-delayed-absent",
                "edcm.occurrence.resolution_latency_horizon",
                "resolution-delayed",
                RelationOperator.LT,
                "resolution-absent",
                "absence of repair should exceed the delayed-repair horizon",
            ),
            ExpectedRelation(
                "latency-occurrence-area-immediate-delayed",
                "edcm.occurrence.tension_area",
                "resolution-immediate",
                RelationOperator.LT,
                "resolution-delayed",
                "delayed repair should accumulate more tension than immediate repair",
            ),
            ExpectedRelation(
                "latency-occurrence-terminal-delayed-absent",
                "edcm.occurrence.final_tension",
                "resolution-delayed",
                RelationOperator.LT,
                "resolution-absent",
                "completed delayed repair should leave less terminal tension than absent repair",
            ),
            ExpectedRelation(
                "latency-baseline-immediate-delayed",
                "edcm.baseline.energy_mean",
                "resolution-immediate",
                RelationOperator.LT,
                "resolution-delayed",
                "the baseline energy summary is tested for repair latency",
            ),
            ExpectedRelation(
                "latency-baseline-delayed-absent",
                "edcm.baseline.energy_mean",
                "resolution-delayed",
                RelationOperator.LT,
                "resolution-absent",
                "the baseline energy summary is tested for absent repair",
            ),
            ExpectedRelation(
                "preemptive-order-occurrence",
                "edcm.occurrence.final_tension",
                "resolution-immediate",
                RelationOperator.LT,
                "resolution-preemptive",
                "repair before later pressure must not count as equivalent to repair after pressure",
            ),
            ExpectedRelation(
                "refusal-occurrence-breadth",
                "ucns.occurrence-turn.B.cell-detail",
                "refusal-dose-1",
                RelationOperator.LT,
                "refusal-dose-4",
                "occurrence-weighted breadth should retain the refusal-dose contrast",
            ),
        )
    )
    return cases, tuple(relations), phrase_pairs


def _build_v2_envelope(
    case: ExperimentCase,
    support_policy: str,
    ucns_api: Mapping[str, Any],
) -> Any:
    Cell = ucns_api["Cell"]
    RetainedLayer = ucns_api["RetainedLayer"]
    make_carrier = ucns_api["make_carrier"]
    make_retained_structure = ucns_api["make_retained_structure"]

    seen: dict[str, int] = {}
    cells = []
    turns_layer = []
    previous_speaker: str | None = None
    for index, (speaker, text) in enumerate(_split_turns(case.transcript)):
        normalized = " ".join(_tokens(text))
        signals = _v2_turn_signals(text, normalized, seen)
        seen[normalized] = seen.get(normalized, 0) + 1
        if support_policy == "unit-turn":
            support = 1.0
        elif support_policy == "token-turn":
            support = signals["token_count"]
        elif support_policy == "occurrence-turn":
            support = 1.0 + sum(
                signals[name]
                for name in ("constraint", "refusal", "resolution", "repetition")
            )
        elif support_policy == "dissonance-turn":
            support = 1.0 + sum(
                signals[name] for name in ("constraint", "refusal", "repetition")
            )
        else:
            raise KeyError(f"unknown v0.2 support policy: {support_policy}")

        cells.append(
            Cell(
                coordinate=index,
                payload=text,
                type_tag=speaker,
                state=tuple(sorted((key, float(value)) for key, value in signals.items())),
                provenance=(case.case_id, PROGRAM_VERSION, support_policy),
                relation=(previous_speaker, speaker),
                mu=support,
            )
        )
        turns_layer.append({"speaker": speaker, "text": text})
        previous_speaker = speaker

    return make_retained_structure(
        make_carrier(tuple(cells)),
        (
            RetainedLayer("turns", tuple(turns_layer)),
            RetainedLayer("raw-transcript", case.transcript),
            RetainedLayer(
                "v0.2-signals",
                {
                    "case_id": case.case_id,
                    "case_digest": case.digest,
                    "support_policy": support_policy,
                },
            ),
        ),
    )


def _candidate_values_for_case(
    case: ExperimentCase, ucns_api: Mapping[str, Any]
) -> tuple[list[CandidateReadout], dict[str, dict[str, Any]]]:
    readouts: list[CandidateReadout] = []
    for candidate_id, prefix, evaluator in (
        (BASELINE_CANDIDATE_ID, "edcm.baseline", baseline_readout),
        (OCCURRENCE_CANDIDATE_ID, "edcm.occurrence", occurrence_coverage_readout),
    ):
        try:
            values = evaluator(case)
            error = None
        except Exception as exc:
            values = {}
            error = f"{type(exc).__name__}: {exc}"
        readouts.append(
            CandidateReadout(
                candidate_id,
                case.case_id,
                tuple((f"{prefix}.{key}", value) for key, value in sorted(values.items())),
                (
                    "The-Interdependency/edcm:edcm/measurement@0.1.0"
                    if candidate_id == BASELINE_CANDIDATE_ID
                    else "The-Interdependency/edcm:edcm.ucns_edcm_experiments_v2"
                ),
                error,
            )
        )

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
    structural: dict[str, dict[str, Any]] = {}
    for support_policy in (
        "unit-turn",
        "token-turn",
        "occurrence-turn",
        "dissonance-turn",
    ):
        envelope = _build_v2_envelope(case, support_policy, ucns_api)
        structural[support_policy] = _structural_signatures(envelope, ucns_api)
        values: list[tuple[str, Any]] = [
            (
                f"ucns.{support_policy}.W.cell-support",
                float(ucns_api["cell_support_weight"](envelope)),
            )
        ]
        values.extend(
            (f"ucns.{support_policy}.M.{name}", candidate.evaluate(envelope))
            for name, candidate in m_candidates
        )
        values.extend(
            (f"ucns.{support_policy}.B.{name}", candidate.evaluate(envelope))
            for name, candidate in b_candidates
        )
        readouts.append(
            CandidateReadout(
                f"ucns-{support_policy}-candidate-pack-v0.2",
                case.case_id,
                tuple(values),
                f"The-Interdependency/ucns@{EXPECTED_UCNS_COMMIT}",
            )
        )
    return readouts, structural


def _dose_curve_findings(
    index: Mapping[tuple[str, str], Any]
) -> tuple[DoseCurveFinding, ...]:
    case_ids = ("refusal-dose-0", "refusal-dose-1", "refusal-dose-2", "refusal-dose-4")
    specs = (
        (OCCURRENCE_CANDIDATE_ID, "edcm.occurrence.refusal_occurrences"),
        (OCCURRENCE_CANDIDATE_ID, "edcm.occurrence.tension_area"),
        (BASELINE_CANDIDATE_ID, "edcm.baseline.R_mean"),
        ("ucns-occurrence", "ucns.occurrence-turn.B.cell-detail"),
    )
    findings = []
    for candidate_id, readout in specs:
        values = tuple(float(index[(case_id, readout)]) for case_id in case_ids)
        plateau = tuple(
            (left, right)
            for left, right, left_value, right_value in zip(
                case_ids, case_ids[1:], values, values[1:]
            )
            if left_value == right_value
        )
        findings.append(
            DoseCurveFinding(
                candidate_id,
                readout,
                case_ids,
                values,
                all(left < right for left, right in zip(values, values[1:])),
                all(left <= right for left, right in zip(values, values[1:])),
                plateau,
            )
        )
    return tuple(findings)


def _phrase_coverage_findings(
    index: Mapping[tuple[str, str], Any],
    phrase_pairs: Iterable[tuple[str, str, str]],
) -> tuple[PhraseCoverageFinding, ...]:
    specs = (
        (OCCURRENCE_CANDIDATE_ID, "edcm.occurrence.constraint_occurrences"),
        (BASELINE_CANDIDATE_ID, "edcm.baseline.C_mean"),
        ("ucns-dissonance", "ucns.dissonance-turn.B.cell-detail"),
    )
    findings = []
    for family, low_case, high_case in phrase_pairs:
        for candidate_id, readout in specs:
            high = float(index[(high_case, readout)])
            low = float(index[(low_case, readout)])
            detected = high > low
            false_positive = low > 0.0 if not readout.endswith("cell-detail") else False
            status = (
                "detected-with-clean-control"
                if detected and not false_positive
                else "detected-with-control-signal"
                if detected
                else "missed"
            )
            findings.append(
                PhraseCoverageFinding(
                    candidate_id,
                    readout,
                    family,
                    high_case,
                    low_case,
                    high,
                    low,
                    detected,
                    false_positive,
                    status,
                )
            )
    return tuple(findings)


def _latency_findings(
    index: Mapping[tuple[str, str], Any]
) -> tuple[LatencyFinding, ...]:
    specs = (
        (OCCURRENCE_CANDIDATE_ID, "edcm.occurrence.resolution_latency_horizon"),
        (OCCURRENCE_CANDIDATE_ID, "edcm.occurrence.peak_tension"),
        (OCCURRENCE_CANDIDATE_ID, "edcm.occurrence.final_tension"),
        (BASELINE_CANDIDATE_ID, "edcm.baseline.energy_mean"),
        (BASELINE_CANDIDATE_ID, "edcm.baseline.kappa_final"),
    )
    findings = []
    for candidate_id, readout in specs:
        immediate = float(index[("resolution-immediate", readout)])
        delayed = float(index[("resolution-delayed", readout)])
        unresolved = float(index[("resolution-absent", readout)])
        status = (
            "strict-latency-order"
            if immediate < delayed < unresolved
            else "partial-latency-order"
            if immediate <= delayed <= unresolved
            and (immediate < delayed or delayed < unresolved)
            else "latency-collapsed"
        )
        findings.append(
            LatencyFinding(
                candidate_id,
                readout,
                "resolution-immediate",
                "resolution-delayed",
                "resolution-absent",
                immediate,
                delayed,
                unresolved,
                status,
            )
        )
    return tuple(findings)


def _support_findings(
    index: Mapping[tuple[str, str], Any],
    phrase_pairs: Iterable[tuple[str, str, str]],
) -> tuple[SupportStabilityFinding, ...]:
    pairs = [
        ("refusal-dose", "refusal-dose-4", "refusal-dose-1", "gt"),
        *((f"constraint-{family}", high, low, "gt") for family, low, high in phrase_pairs),
    ]
    findings = []
    for pair_id, left_case, right_case, direction in pairs:
        for support_policy in (
            "unit-turn",
            "token-turn",
            "occurrence-turn",
            "dissonance-turn",
        ):
            readout = f"ucns.{support_policy}.B.cell-detail"
            left = float(index[(left_case, readout)])
            right = float(index[(right_case, readout)])
            passed = left > right if direction == "gt" else left < right
            findings.append(
                SupportStabilityFinding(
                    pair_id,
                    readout,
                    support_policy,
                    left_case,
                    right_case,
                    left,
                    right,
                    direction,
                    "preserved" if passed else "collapsed-or-reversed",
                )
            )
    return tuple(findings)


def run_v2_experiments(
    *,
    edcm_commit: str | None = None,
    ucns_commit: str = EXPECTED_UCNS_COMMIT,
    ucns_source_root: str | Path | None = None,
) -> V2ExperimentReport:
    if ucns_commit != EXPECTED_UCNS_COMMIT:
        raise ValueError(f"v0.2 requires UCNS {EXPECTED_UCNS_COMMIT}, got {ucns_commit}")
    source_root_value = ucns_source_root or os.environ.get("UCNS_SOURCE_ROOT")
    if source_root_value is None:
        raise ValueError(
            "ucns_source_root or UCNS_SOURCE_ROOT is required for verified joint evidence"
        )
    ucns_api = _load_ucns()
    verified_commit, source_manifest = _verify_ucns_identity(Path(source_root_value), ucns_api)
    comparison = ucns_api["combined_comparison_policy"](
        rel_tol=1e-9,
        abs_tol=1e-12,
        name="ucns-edcm-v0.2-combined",
        version="1",
    )
    cases, relations, phrase_pairs = build_v2_program()
    all_readouts: list[CandidateReadout] = []
    structural: dict[str, dict[str, Any]] = {}
    for case in cases:
        case_readouts, case_structural = _candidate_values_for_case(case, ucns_api)
        all_readouts.extend(case_readouts)
        structural[case.case_id] = case_structural

    index = _readout_index(all_readouts)
    verdicts = tuple(_evaluate_relation(relation, index, comparison) for relation in relations)
    return V2ExperimentReport(
        PROGRAM_SCHEMA,
        PROGRAM_VERSION,
        PRIOR_PROGRAM_SCHEMA,
        PRIOR_REPORT_DIGEST,
        edcm_commit or os.environ.get("GITHUB_SHA", "unrecorded-edcm-commit"),
        verified_commit,
        source_manifest,
        True,
        cases,
        (
            (BASELINE_CANDIDATE_ID, "The-Interdependency/edcm:edcm/measurement@0.1.0"),
            (
                OCCURRENCE_CANDIDATE_ID,
                "The-Interdependency/edcm:edcm.ucns_edcm_experiments_v2",
            ),
            ("ucns-candidate-packs-v0.2", f"The-Interdependency/ucns@{verified_commit}"),
            ("comparison-policy", "ucns-edcm-v0.2-combined/1(rel=1e-9,abs=1e-12)"),
        ),
        tuple(all_readouts),
        _flatten_structural_signatures(structural),
        verdicts,
        _dose_curve_findings(index),
        _phrase_coverage_findings(index, phrase_pairs),
        _latency_findings(index),
        _support_findings(index, phrase_pairs),
        None,
        (
            "v0.1 result remains immutable prior evidence.",
            "Falsified relations and collapsed candidate curves remain evidence.",
            "No EDCM axis, UCNS support policy, M, B, equivalence relation, or threshold is selected as canon.",
        ),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--edcm-commit", default=None)
    parser.add_argument("--ucns-commit", default=EXPECTED_UCNS_COMMIT)
    parser.add_argument("--ucns-source-root", type=Path, default=None)
    args = parser.parse_args(argv)
    report = run_v2_experiments(
        edcm_commit=args.edcm_commit,
        ucns_commit=args.ucns_commit,
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
                    "supported": sum(item.status == "supported" for item in report.relation_verdicts),
                    "falsified": sum(item.status == "falsified" for item in report.relation_verdicts),
                    "errors": sum(item.status == "error" for item in report.relation_verdicts),
                    "canon_selection": None,
                },
                sort_keys=True,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
