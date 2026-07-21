"""Third UCNS–EDCM experiment program: assertion and scope topology.

Usage
-----
Run with the exact verified UCNS checkout:

    python -m edcm.ucns_edcm_experiments_v3 \
        --ucns-source-root /path/to/ucns \
        --output artifacts/ucns-edcm-v0.3.0.json

The report is pre-canon evidence. It preserves every mention, scope flag,
falsifier, and structural projection and always leaves canon unselected.
"""

# === MODULE_BUILD ===
# id: edcm_ucns_edcm_experiments_v3
#   module_name: ucns_edcm_experiments_v3
#   module_kind: instrument
#   summary: tests assertion, negation, quotation, hypotheticals, attribution, retraction, and repair order through scope-bearing EDCM events and UCNS structural projections
#   owner: Erin Spencer
#   public_surface: ScopeEvent, ScopeSignatureRecord, ScopePairFinding, V3ExperimentReport, scope_assertion_readout, build_v3_program, run_v3_experiments, main
#   internal_surface: _quote_spans, _mention_events, _repair_events, _extract_scope_events, _build_scope_envelope, _scope_signatures, _pair_findings
#   auth_boundary: none
#   storage_boundary: writes only caller-selected report path
#   network_boundary: none; exact UCNS checkout and installed package are verified locally
#   user_data_boundary: fixed synthetic development and holdout transcripts only
#   admin_only: false
#   tests: tests/test_ucns_edcm_experiments_v3.py
#   rollout: explicit versioned research program; v0.1 and v0.2 remain immutable and no canon selection is made
#   rollback: remove v0.3 module, workflow calls, and result; earlier reports and frozen baseline remain unchanged
#   requires: edcm_ucns_edcm_experiments, edcm_ucns_edcm_experiments_v2, edcmbone_parser_turns_rounds, edcmbone_metrics_compute
#   since: 2026-07-21
#   unresolved: full discourse scope, independent annotation, multilingual scope, external replication, and joint canon decision authority
# === END MODULE_BUILD ===

from __future__ import annotations

import argparse
import json
import os
import re
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
    _canonical_projection_view,
    _digest,
    _evaluate_relation,
    _jsonable,
    _load_ucns,
    _readout_index,
    _split_turns,
    _tokens,
    _verify_ucns_identity,
    baseline_readout,
    EXPECTED_UCNS_COMMIT,
)
from .ucns_edcm_experiments_v2 import (
    OCCURRENCE_CANDIDATE_ID,
    occurrence_coverage_readout,
)

PROGRAM_SCHEMA = "edcm.ucns-edcm-experiment-report/0.3.0"
PROGRAM_VERSION = "0.3.0"
PRIOR_V1_REPORT_DIGEST = "4c8bd8496ec549c1073320bafc995c7c65eaf81c9385e4dc6fff7794ed3b1124"
PRIOR_V2_REPORT_DIGEST = "85d6a9c7504a7e9b7fdb21e0dec5ff8e588d12e9d893f1a22854c1ae2ebbf0e4"
SCOPE_CANDIDATE_ID = "edcm-scope-assertion-v1"

_EVENT_FAMILIES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("constraint", "obligation", ("must", "required", "mandatory", "have to")),
    (
        "constraint",
        "consequence",
        ("penalty", "access will be revoked", "lose access", "access is denied"),
    ),
    (
        "constraint",
        "deadline",
        ("immediately", "decide now", "choose now", "deadline", "before entry"),
    ),
    (
        "constraint",
        "alternatives",
        ("no alternative", "no choice", "only option"),
    ),
    (
        "refusal",
        "refusal",
        ("i refuse", "refuse", "will not comply", "cannot comply", "i decline"),
    ),
)
_REPAIR_MARKERS = (
    "correction",
    "rescinded",
    "withdrawn",
    "retracted",
    "no longer applies",
    "not in force",
    "may decide later",
    "participation is optional",
    "i agree",
    "that works",
)
_ATTRIBUTION_MARKERS = ("said", "reported", "wrote", "claimed", "the notice")
_HYPOTHETICAL_MARKERS = (
    "imagine",
    "suppose",
    "hypothetical",
    "hypothetically",
    "counterfactual",
    "would have",
    "had applied",
    "were to",
)
_NEGATION_RE = re.compile(r"(?:\bno\b|\bnot\b|\bnever\b|\bwithout\b)\s+(?:\w+\s+){0,2}$")


@dataclass(frozen=True, slots=True)
class ScopeEvent:
    event_id: str
    case_id: str
    turn_index: int
    event_index: int
    span_start: int
    speaker: str
    kind: str
    family: str
    phrase: str
    polarity: str
    quoted: bool
    hypothetical: bool
    conditional: bool
    attributed: bool
    retracted: bool
    owned: bool
    active: bool

    def full_view(self, *, include_position: bool) -> dict[str, Any]:
        view = {
            "speaker": self.speaker,
            "kind": self.kind,
            "family": self.family,
            "phrase": self.phrase,
            "polarity": self.polarity,
            "quoted": self.quoted,
            "hypothetical": self.hypothetical,
            "conditional": self.conditional,
            "attributed": self.attributed,
            "retracted": self.retracted,
            "owned": self.owned,
            "active": self.active,
        }
        if include_position:
            view["turn_index"] = self.turn_index
            view["event_index"] = self.event_index
        return view

    def lexical_view(self) -> dict[str, str]:
        return {"kind": self.kind, "family": self.family}


@dataclass(frozen=True, slots=True)
class ScopeSignatureRecord:
    case_id: str
    support_policy: str
    view_name: str
    signature: str
    information_loss: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ScopePairFinding:
    pair_id: str
    view_name: str
    readout: str
    left_case: str
    right_case: str
    structures_equivalent: bool
    readout_equivalent: bool
    status: str
    information_loss: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class V3ExperimentReport:
    schema: str
    program_version: str
    prior_v1_report_digest: str
    prior_v2_report_digest: str
    edcm_commit: str
    ucns_commit: str
    ucns_source_manifest: str
    ucns_identity_verified: bool
    cases: tuple[ExperimentCase, ...]
    scope_events: tuple[ScopeEvent, ...]
    candidate_identities: tuple[tuple[str, str], ...]
    readouts: tuple[CandidateReadout, ...]
    structural_signatures: tuple[ScopeSignatureRecord, ...]
    relation_verdicts: tuple[RelationVerdict, ...]
    pair_findings: tuple[ScopePairFinding, ...]
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


def _quote_spans(text: str) -> tuple[tuple[int, int], ...]:
    return tuple((match.start() + 1, match.end() - 1) for match in re.finditer(r'"[^"\n]*"', text))


def _inside_quote(start: int, end: int, spans: Iterable[tuple[int, int]]) -> bool:
    return any(start >= quote_start and end <= quote_end for quote_start, quote_end in spans)


def _phrase_matches(text: str, phrases: Iterable[str]) -> tuple[tuple[int, int, str], ...]:
    lowered = text.lower()
    candidates: list[tuple[int, int, str]] = []
    for phrase in sorted(set(phrases), key=lambda item: (-len(item), item)):
        for match in re.finditer(rf"(?<!\w){re.escape(phrase)}(?!\w)", lowered):
            candidates.append((match.start(), match.end(), phrase))
    selected: list[tuple[int, int, str]] = []
    for start, end, phrase in sorted(candidates, key=lambda item: (item[0], -(item[1] - item[0]))):
        if any(not (end <= prior_start or start >= prior_end) for prior_start, prior_end, _ in selected):
            continue
        selected.append((start, end, phrase))
    return tuple(sorted(selected))


def _mention_events(case: ExperimentCase, turn_index: int, speaker: str, text: str) -> list[ScopeEvent]:
    lowered = text.lower()
    quote_spans = _quote_spans(text)
    hypothetical_context = any(marker in lowered for marker in _HYPOTHETICAL_MARKERS)
    conditional_context = bool(re.search(r"\bif\b", lowered))
    retracted_context = any(marker in lowered for marker in _REPAIR_MARKERS if marker not in ("correction", "i agree", "that works"))
    attribution_context = any(marker in lowered for marker in _ATTRIBUTION_MARKERS)
    events: list[ScopeEvent] = []
    event_index = 0
    for kind, family, phrases in _EVENT_FAMILIES:
        for start, end, phrase in _phrase_matches(text, phrases):
            quoted = _inside_quote(start, end, quote_spans)
            prefix = lowered[max(0, start - 32):start]
            negated = bool(_NEGATION_RE.search(prefix))
            attributed = quoted and attribution_context
            hypothetical = hypothetical_context
            retracted = retracted_context and (quoted or start < max((lowered.find(marker) for marker in _REPAIR_MARKERS if marker in lowered), default=len(lowered)))
            owned = kind == "refusal" and not quoted and not attributed and bool(re.search(r"\bi\b", lowered[max(0, start - 4):end]))
            active = not negated and not quoted and not hypothetical and not retracted
            event_index += 1
            events.append(
                ScopeEvent(
                    f"{case.case_id}:t{turn_index}:e{event_index}:{kind}:{family}",
                    case.case_id,
                    turn_index,
                    event_index,
                    start,
                    speaker,
                    kind,
                    family,
                    phrase,
                    "negated" if negated else "positive",
                    quoted,
                    hypothetical,
                    conditional_context,
                    attributed,
                    retracted,
                    owned,
                    active,
                )
            )
    return events


def _repair_events(case: ExperimentCase, turn_index: int, speaker: str, text: str, start_index: int) -> list[ScopeEvent]:
    lowered = text.lower()
    events: list[ScopeEvent] = []
    event_index = start_index
    for marker in _REPAIR_MARKERS:
        for match in re.finditer(rf"(?<!\w){re.escape(marker)}(?!\w)", lowered):
            event_index += 1
            events.append(
                ScopeEvent(
                    f"{case.case_id}:t{turn_index}:e{event_index}:repair",
                    case.case_id,
                    turn_index,
                    event_index,
                    match.start(),
                    speaker,
                    "repair",
                    "repair",
                    marker,
                    "positive",
                    _inside_quote(match.start(), match.end(), _quote_spans(text)),
                    False,
                    False,
                    False,
                    False,
                    True,
                    True,
                )
            )
    return events


def _extract_scope_events(case: ExperimentCase) -> tuple[ScopeEvent, ...]:
    events: list[ScopeEvent] = []
    for turn_index, (speaker, text) in enumerate(_split_turns(case.transcript)):
        mentions = _mention_events(case, turn_index, speaker, text)
        repairs = _repair_events(case, turn_index, speaker, text, len(mentions))
        turn_events = sorted(mentions + repairs, key=lambda event: (event.span_start, event.event_index))
        events.extend(turn_events)
    return tuple(events)


def scope_assertion_readout(case: ExperimentCase) -> dict[str, float]:
    events = _extract_scope_events(case)
    active_pressure = 0.0
    peak_pressure = 0.0
    accumulated_pressure = 0.0
    first_pressure_position: int | None = None
    first_later_repair_position: int | None = None

    counts = {
        "lexical_constraint_mentions": 0.0,
        "lexical_refusal_mentions": 0.0,
        "asserted_constraint_events": 0.0,
        "asserted_refusal_events": 0.0,
        "negated_mentions": 0.0,
        "quoted_mentions": 0.0,
        "hypothetical_mentions": 0.0,
        "conditional_mentions": 0.0,
        "attributed_refusal_mentions": 0.0,
        "owned_refusal_events": 0.0,
        "retracted_mentions": 0.0,
        "repair_events": 0.0,
    }

    for position, event in enumerate(events):
        if event.kind == "constraint":
            counts["lexical_constraint_mentions"] += 1.0
        elif event.kind == "refusal":
            counts["lexical_refusal_mentions"] += 1.0
        if event.polarity == "negated":
            counts["negated_mentions"] += 1.0
        if event.quoted:
            counts["quoted_mentions"] += 1.0
        if event.hypothetical:
            counts["hypothetical_mentions"] += 1.0
        if event.conditional:
            counts["conditional_mentions"] += 1.0
        if event.retracted:
            counts["retracted_mentions"] += 1.0
        if event.kind == "refusal" and event.attributed:
            counts["attributed_refusal_mentions"] += 1.0
        if event.kind == "refusal" and event.owned and event.active:
            counts["owned_refusal_events"] += 1.0
        if event.kind == "constraint" and event.active:
            counts["asserted_constraint_events"] += 1.0
        if event.kind == "refusal" and event.active:
            counts["asserted_refusal_events"] += 1.0

        if event.kind == "repair":
            counts["repair_events"] += 1.0
            active_pressure = 0.0
            if first_pressure_position is not None and first_later_repair_position is None:
                first_later_repair_position = position
        elif event.active and event.kind in ("constraint", "refusal"):
            active_pressure += 1.0
            if first_pressure_position is None:
                first_pressure_position = position
        peak_pressure = max(peak_pressure, active_pressure)
        accumulated_pressure += active_pressure

    repair_horizon = (
        -1.0
        if first_pressure_position is None or first_later_repair_position is None
        else float(first_later_repair_position - first_pressure_position)
    )
    return {
        **counts,
        "final_active_pressure": active_pressure,
        "peak_active_pressure": peak_pressure,
        "accumulated_active_pressure": accumulated_pressure,
        "pressure_to_repair_horizon": repair_horizon,
        "event_count": float(len(events)),
    }


def build_v3_program() -> tuple[
    tuple[ExperimentCase, ...],
    tuple[ExpectedRelation, ...],
    tuple[tuple[str, str, str, tuple[str, ...]], ...],
]:
    dev = "synthetic development contrast authored for UCNS-EDCM experiment v0.3"
    holdout = "synthetic holdout contrast authored for UCNS-EDCM experiment v0.3"
    cases = (
        ExperimentCase("penalty-asserted", "A: There is a penalty if you delay.\nB: Noted.", ExperimentPartition.DEVELOPMENT, "penalty asserted", dev, ("scope", "negation")),
        ExperimentCase("penalty-negated", "A: There is no penalty if you delay.\nB: Noted.", ExperimentPartition.HOLDOUT, "same penalty mention negated", holdout, ("scope", "negation", "holdout")),
        ExperimentCase("must-direct", "A: You must comply immediately.\nB: Noted.", ExperimentPartition.DEVELOPMENT, "direct active command", dev, ("scope", "quotation")),
        ExperimentCase("must-quoted-rescinded", "A: The notice said \"You must comply immediately,\" but it was rescinded.\nB: Noted.", ExperimentPartition.HOLDOUT, "same command quoted and rescinded", holdout, ("scope", "quotation", "retraction", "holdout")),
        ExperimentCase("revocation-operative", "A: If you refuse, access will be revoked.\nB: Noted.", ExperimentPartition.DEVELOPMENT, "operative conditional consequence", dev, ("scope", "conditional")),
        ExperimentCase("revocation-hypothetical", "A: Imagine that if you refuse, access will be revoked.\nB: Noted.", ExperimentPartition.HOLDOUT, "same consequence inside imagined condition", holdout, ("scope", "hypothetical", "holdout")),
        ExperimentCase("refusal-owned", "B: I refuse.", ExperimentPartition.DEVELOPMENT, "speaker-owned refusal", dev, ("scope", "attribution")),
        ExperimentCase("refusal-attributed", "B: She said \"I refuse,\" but I agree.", ExperimentPartition.HOLDOUT, "another person's quoted refusal followed by present agreement", holdout, ("scope", "attribution", "quotation", "holdout")),
        ExperimentCase("pressure-repaired", "A: You must decide now.\nA: Correction: you may decide later.", ExperimentPartition.DEVELOPMENT, "pressure followed by repair", dev, ("scope", "repair-order")),
        ExperimentCase("pressure-renewed", "A: You may decide later.\nA: Correction: you must decide now.", ExperimentPartition.HOLDOUT, "same pressure and repair in opposite order", holdout, ("scope", "repair-order", "holdout")),
        ExperimentCase("mandatory-active", "A: Compliance is mandatory before entry.\nB: Noted.", ExperimentPartition.DEVELOPMENT, "mandatory statement remains active", dev, ("scope", "retraction")),
        ExperimentCase("mandatory-withdrawn", "A: Compliance is mandatory before entry, but that requirement is withdrawn.\nB: Noted.", ExperimentPartition.HOLDOUT, "same mandatory statement withdrawn", holdout, ("scope", "retraction", "holdout")),
        ExperimentCase("refusal-positive", "B: I refuse.", ExperimentPartition.DEVELOPMENT, "positive refusal mention", dev, ("scope", "refusal-negation")),
        ExperimentCase("refusal-negated", "B: I do not refuse.", ExperimentPartition.HOLDOUT, "same refusal phrase locally negated", holdout, ("scope", "refusal-negation", "holdout")),
    )

    relations = (
        ExpectedRelation("negation-lexical-equal", "edcm.occurrence.constraint_occurrences", "penalty-asserted", RelationOperator.EQ, "penalty-negated", "lexical occurrence candidate should see the same penalty mention"),
        ExpectedRelation("negation-scope-active", "edcm.scope.asserted_constraint_events", "penalty-asserted", RelationOperator.GT, "penalty-negated", "scope candidate should distinguish assertion from local negation"),
        ExpectedRelation("negation-baseline-C", "edcm.baseline.C_mean", "penalty-asserted", RelationOperator.GT, "penalty-negated", "baseline C is tested for assertion versus negation"),
        ExpectedRelation("negation-active-support", "ucns.active-pressure.W.cell-support", "penalty-asserted", RelationOperator.GT, "penalty-negated", "active-pressure support should retain assertion while preserving the negated event"),
        ExpectedRelation("quote-lexical-equal", "edcm.occurrence.constraint_occurrences", "must-direct", RelationOperator.EQ, "must-quoted-rescinded", "matched command words should remain lexically equal"),
        ExpectedRelation("quote-scope-active", "edcm.scope.asserted_constraint_events", "must-direct", RelationOperator.GT, "must-quoted-rescinded", "direct active command should exceed quoted rescinded command"),
        ExpectedRelation("quote-baseline-C", "edcm.baseline.C_mean", "must-direct", RelationOperator.GT, "must-quoted-rescinded", "baseline C is tested for quotation and retraction"),
        ExpectedRelation("quote-active-support", "ucns.active-pressure.W.cell-support", "must-direct", RelationOperator.GT, "must-quoted-rescinded", "active-pressure support should distinguish direct from scoped-out command"),
        ExpectedRelation("hypothetical-lexical-equal", "edcm.occurrence.constraint_occurrences", "revocation-operative", RelationOperator.EQ, "revocation-hypothetical", "the same consequence phrase appears in both cases"),
        ExpectedRelation("hypothetical-scope-active", "edcm.scope.asserted_constraint_events", "revocation-operative", RelationOperator.GT, "revocation-hypothetical", "operative conditional should exceed imagined condition"),
        ExpectedRelation("hypothetical-baseline-C", "edcm.baseline.C_mean", "revocation-operative", RelationOperator.GT, "revocation-hypothetical", "baseline C is tested for hypothetical scope"),
        ExpectedRelation("ownership-lexical-equal", "edcm.occurrence.refusal_occurrences", "refusal-owned", RelationOperator.EQ, "refusal-attributed", "the same refusal phrase appears directly and in attributed quotation"),
        ExpectedRelation("ownership-scope-owned", "edcm.scope.owned_refusal_events", "refusal-owned", RelationOperator.GT, "refusal-attributed", "speaker-owned refusal should exceed attributed refusal"),
        ExpectedRelation("ownership-baseline-R", "edcm.baseline.R_mean", "refusal-owned", RelationOperator.GT, "refusal-attributed", "baseline R is tested for ownership and quotation"),
        ExpectedRelation("repair-order-scope", "edcm.scope.final_active_pressure", "pressure-repaired", RelationOperator.LT, "pressure-renewed", "repair after pressure should leave less active pressure than pressure after repair"),
        ExpectedRelation("repair-order-occurrence", "edcm.occurrence.final_tension", "pressure-repaired", RelationOperator.LT, "pressure-renewed", "v0.2 occurrence recurrence is retested on repair order"),
        ExpectedRelation("repair-order-baseline", "edcm.baseline.kappa_final", "pressure-repaired", RelationOperator.LT, "pressure-renewed", "baseline circuit is retested on repair topology"),
        ExpectedRelation("retraction-lexical-equal", "edcm.occurrence.constraint_occurrences", "mandatory-active", RelationOperator.EQ, "mandatory-withdrawn", "same mandatory phrase appears in both cases"),
        ExpectedRelation("retraction-scope-active", "edcm.scope.asserted_constraint_events", "mandatory-active", RelationOperator.GT, "mandatory-withdrawn", "withdrawn statement should not remain active"),
        ExpectedRelation("retraction-active-support", "ucns.active-pressure.W.cell-support", "mandatory-active", RelationOperator.GT, "mandatory-withdrawn", "active support should distinguish active from withdrawn mention"),
        ExpectedRelation("refusal-negation-lexical-equal", "edcm.scope.lexical_refusal_mentions", "refusal-positive", RelationOperator.EQ, "refusal-negated", "same refusal phrase remains a lexical mention"),
        ExpectedRelation("refusal-negation-scope", "edcm.scope.owned_refusal_events", "refusal-positive", RelationOperator.GT, "refusal-negated", "negated refusal should not count as active owned refusal"),
        ExpectedRelation("refusal-negation-baseline", "edcm.baseline.R_mean", "refusal-positive", RelationOperator.GT, "refusal-negated", "baseline R is tested for local negation"),
    )

    pair_specs = (
        ("negation", "penalty-asserted", "penalty-negated", ("edcm.scope.asserted_constraint_events", "edcm.occurrence.constraint_occurrences")),
        ("quotation", "must-direct", "must-quoted-rescinded", ("edcm.scope.asserted_constraint_events", "edcm.occurrence.constraint_occurrences")),
        ("hypothetical", "revocation-operative", "revocation-hypothetical", ("edcm.scope.asserted_constraint_events", "edcm.occurrence.constraint_occurrences")),
        ("ownership", "refusal-owned", "refusal-attributed", ("edcm.scope.owned_refusal_events", "edcm.occurrence.refusal_occurrences")),
        ("repair-order", "pressure-repaired", "pressure-renewed", ("edcm.scope.final_active_pressure", "edcm.baseline.kappa_final")),
        ("retraction", "mandatory-active", "mandatory-withdrawn", ("edcm.scope.asserted_constraint_events", "edcm.occurrence.constraint_occurrences")),
        ("refusal-negation", "refusal-positive", "refusal-negated", ("edcm.scope.owned_refusal_events", "edcm.scope.lexical_refusal_mentions")),
    )
    return cases, relations, pair_specs


def _event_payload(event: ScopeEvent, *, include_position: bool) -> dict[str, Any]:
    return event.full_view(include_position=include_position)


def _build_scope_envelope(case: ExperimentCase, support_policy: str, ucns_api: Mapping[str, Any]) -> Any:
    Cell = ucns_api["Cell"]
    RetainedLayer = ucns_api["RetainedLayer"]
    make_carrier = ucns_api["make_carrier"]
    make_retained_structure = ucns_api["make_retained_structure"]
    events = _extract_scope_events(case)
    cells = []
    previous_kind: str | None = None
    for index, event in enumerate(events):
        complexity = sum((event.polarity == "negated", event.quoted, event.hypothetical, event.conditional, event.attributed, event.retracted))
        if support_policy == "mention-event":
            support = 1.0
        elif support_policy == "scope-detail":
            support = 1.0 + float(complexity)
        elif support_policy == "active-pressure":
            support = 1.0 + (2.0 if event.active and event.kind in ("constraint", "refusal") else 0.0)
        else:
            raise KeyError(f"unknown scope support policy: {support_policy}")
        cells.append(
            Cell(
                coordinate=index,
                payload=event.phrase,
                type_tag=f"{event.kind}:{event.family}",
                state=tuple(sorted((key, value) for key, value in event.full_view(include_position=False).items() if isinstance(value, (bool, str)))),
                provenance=(case.case_id, PROGRAM_VERSION, support_policy, event.event_id),
                relation=(previous_kind, event.kind),
                mu=support,
            )
        )
        previous_kind = event.kind
    return make_retained_structure(
        make_carrier(tuple(cells)),
        (
            RetainedLayer("scope-events", tuple(event.full_view(include_position=True) for event in events)),
            RetainedLayer("raw-transcript", case.transcript),
            RetainedLayer("case-provenance", {"case_id": case.case_id, "case_digest": case.digest, "support_policy": support_policy}),
        ),
    )


def _projection_signature(policy_name: str, projection: Any) -> str:
    if policy_name.endswith("multiset"):
        view = tuple(
            sorted((str(group.key), int(group.count)) for group in projection.view)
        )
    elif policy_name.endswith("set"):
        view = tuple(sorted(str(entry.key) for entry in projection.view))
    else:
        view = _jsonable(projection.view)
    return _digest(view)


def _scope_signatures(case: ExperimentCase, support_policy: str, ucns_api: Mapping[str, Any]) -> tuple[ScopeSignatureRecord, ...]:
    events = _extract_scope_events(case)
    apply_policy = ucns_api["apply_policy"]
    ordered_sequence_policy = ucns_api["ordered_sequence_policy"]
    unordered_multiset_policy = ucns_api["unordered_multiset_policy"]
    set_policy = ucns_api["set_policy"]

    full_ordered_source = tuple(event.full_view(include_position=False) for event in events)
    full_key = lambda item: json.dumps(item, sort_keys=True, separators=(",", ":"))
    lexical_source = tuple(event.lexical_view() for event in events)
    lexical_key = lambda item: json.dumps(item, sort_keys=True, separators=(",", ":"))

    projections = (
        ("full-ordered", apply_policy(full_ordered_source, ordered_sequence_policy(name="full-ordered")), ()),
        ("full-multiset", apply_policy(full_ordered_source, unordered_multiset_policy(full_key, name="full-multiset")), ("order",)),
        ("full-set", apply_policy(full_ordered_source, set_policy(full_key, name="full-set")), ("order", "multiplicity")),
        ("lexical-multiset", apply_policy(lexical_source, unordered_multiset_policy(lexical_key, name="lexical-multiset")), ("scope", "surface", "order")),
        ("lexical-set", apply_policy(lexical_source, set_policy(lexical_key, name="lexical-set")), ("scope", "surface", "order", "multiplicity")),
    )
    return tuple(
        ScopeSignatureRecord(case.case_id, support_policy, view_name, _projection_signature(projection.policy_name, projection), losses)
        for view_name, projection, losses in projections
    )


def _candidate_values_for_case(case: ExperimentCase, ucns_api: Mapping[str, Any]) -> tuple[list[CandidateReadout], list[ScopeSignatureRecord], tuple[ScopeEvent, ...]]:
    readouts: list[CandidateReadout] = []
    for candidate_id, prefix, evaluator, identity in (
        (BASELINE_CANDIDATE_ID, "edcm.baseline", baseline_readout, "The-Interdependency/edcm:edcm/measurement@0.1.0"),
        (OCCURRENCE_CANDIDATE_ID, "edcm.occurrence", occurrence_coverage_readout, "The-Interdependency/edcm:edcm.ucns_edcm_experiments_v2"),
        (SCOPE_CANDIDATE_ID, "edcm.scope", scope_assertion_readout, "The-Interdependency/edcm:edcm.ucns_edcm_experiments_v3"),
    ):
        try:
            values = evaluator(case)
            error = None
        except Exception as exc:
            values = {}
            error = f"{type(exc).__name__}: {exc}"
        readouts.append(CandidateReadout(candidate_id, case.case_id, tuple((f"{prefix}.{key}", value) for key, value in sorted(values.items())), identity, error))

    signatures: list[ScopeSignatureRecord] = []
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
    for support_policy in ("mention-event", "scope-detail", "active-pressure"):
        envelope = _build_scope_envelope(case, support_policy, ucns_api)
        signatures.extend(_scope_signatures(case, support_policy, ucns_api))
        values: list[tuple[str, Any]] = [(f"ucns.{support_policy}.W.cell-support", float(ucns_api["cell_support_weight"](envelope)))]
        values.extend((f"ucns.{support_policy}.M.{name}", candidate.evaluate(envelope)) for name, candidate in m_candidates)
        values.extend((f"ucns.{support_policy}.B.{name}", candidate.evaluate(envelope)) for name, candidate in b_candidates)
        readouts.append(CandidateReadout(f"ucns-{support_policy}-candidate-pack-v0.3", case.case_id, tuple(values), f"The-Interdependency/ucns@{EXPECTED_UCNS_COMMIT}"))
    return readouts, signatures, _extract_scope_events(case)


def _pair_findings(pair_specs: Iterable[tuple[str, str, str, tuple[str, ...]]], signatures: Iterable[ScopeSignatureRecord], index: Mapping[tuple[str, str], Any], comparison: Any) -> tuple[ScopePairFinding, ...]:
    signature_index = {(record.case_id, record.support_policy, record.view_name): record for record in signatures}
    findings = []
    for pair_id, left_case, right_case, readouts in pair_specs:
        for view_name in ("full-ordered", "full-multiset", "full-set", "lexical-multiset", "lexical-set"):
            left_record = signature_index[(left_case, "mention-event", view_name)]
            right_record = signature_index[(right_case, "mention-event", view_name)]
            structures_equivalent = left_record.signature == right_record.signature
            losses = tuple(sorted(set(left_record.information_loss) | set(right_record.information_loss)))
            for readout in readouts:
                left_value = index.get((left_case, readout))
                right_value = index.get((right_case, readout))
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
                findings.append(ScopePairFinding(pair_id, view_name, readout, left_case, right_case, structures_equivalent, readout_equivalent, status, losses))
    return tuple(findings)


def run_v3_experiments(*, edcm_commit: str | None = None, ucns_commit: str = EXPECTED_UCNS_COMMIT, ucns_source_root: str | Path | None = None) -> V3ExperimentReport:
    if ucns_commit != EXPECTED_UCNS_COMMIT:
        raise ValueError(f"v0.3 requires UCNS {EXPECTED_UCNS_COMMIT}, got {ucns_commit}")
    source_root_value = ucns_source_root or os.environ.get("UCNS_SOURCE_ROOT")
    if source_root_value is None:
        raise ValueError("ucns_source_root or UCNS_SOURCE_ROOT is required for verified joint evidence")
    ucns_api = _load_ucns()
    verified_commit, source_manifest = _verify_ucns_identity(Path(source_root_value), ucns_api)
    comparison = ucns_api["combined_comparison_policy"](rel_tol=1e-9, abs_tol=1e-12, name="ucns-edcm-v0.3-combined", version="1")
    cases, relations, pair_specs = build_v3_program()
    all_readouts: list[CandidateReadout] = []
    all_signatures: list[ScopeSignatureRecord] = []
    all_events: list[ScopeEvent] = []
    for case in cases:
        readouts, signatures, events = _candidate_values_for_case(case, ucns_api)
        all_readouts.extend(readouts)
        all_signatures.extend(signatures)
        all_events.extend(events)
    index = _readout_index(all_readouts)
    verdicts = tuple(_evaluate_relation(relation, index, comparison) for relation in relations)
    return V3ExperimentReport(
        PROGRAM_SCHEMA,
        PROGRAM_VERSION,
        PRIOR_V1_REPORT_DIGEST,
        PRIOR_V2_REPORT_DIGEST,
        edcm_commit or os.environ.get("GITHUB_SHA", "unrecorded-edcm-commit"),
        verified_commit,
        source_manifest,
        True,
        cases,
        tuple(all_events),
        (
            (BASELINE_CANDIDATE_ID, "The-Interdependency/edcm:edcm/measurement@0.1.0"),
            (OCCURRENCE_CANDIDATE_ID, "The-Interdependency/edcm:edcm.ucns_edcm_experiments_v2"),
            (SCOPE_CANDIDATE_ID, "The-Interdependency/edcm:edcm.ucns_edcm_experiments_v3"),
            ("ucns-scope-candidate-packs", f"The-Interdependency/ucns@{verified_commit}"),
            ("comparison-policy", "ucns-edcm-v0.3-combined/1(rel=1e-9,abs=1e-12)"),
        ),
        tuple(all_readouts),
        tuple(all_signatures),
        verdicts,
        _pair_findings(pair_specs, all_signatures, index, comparison),
        None,
        (
            "v0.1 and v0.2 reports remain immutable prior evidence.",
            "Inactive mentions remain positive retained structure and are not converted to absence.",
            "No scope parser, EDCM axis, UCNS support policy, M, B, equivalence relation, or threshold is selected as canon.",
        ),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--edcm-commit", default=None)
    parser.add_argument("--ucns-commit", default=EXPECTED_UCNS_COMMIT)
    parser.add_argument("--ucns-source-root", type=Path, default=None)
    args = parser.parse_args(argv)
    report = run_v3_experiments(edcm_commit=args.edcm_commit, ucns_commit=args.ucns_commit, ucns_source_root=args.ucns_source_root)
    rendered = report.to_json()
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(json.dumps({
            "output": str(args.output),
            "report_digest": report.digest,
            "supported": sum(item.status == "supported" for item in report.relation_verdicts),
            "falsified": sum(item.status == "falsified" for item in report.relation_verdicts),
            "errors": sum(item.status == "error" for item in report.relation_verdicts),
            "canon_selection": None,
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
