"""Fourth UCNS–EDCM experiment program: discourse-linked scope graphs.

Run with the exact verified UCNS checkout::

    python -m edcm.ucns_edcm_experiments_v4 \
        --ucns-source-root /path/to/ucns \
        --output artifacts/ucns-edcm-v0.4.0.json

The report is pre-canon evidence. It preserves references, competing graph
interpretations, resolver disagreements, and all falsifiers.
"""

# === MODULE_BUILD ===
# id: edcm_ucns_edcm_experiments_v4
#   module_name: ucns_edcm_experiments_v4
#   module_kind: instrument
#   summary: tests cross-turn reference resolution, correction targets, anaphora, nested quotation, suspension, conditional activation, contradiction ownership, and competing discourse graphs
#   owner: Erin Spencer
#   public_surface: DiscourseNode, ReferenceExpression, GraphEdge, GraphInterpretation, GraphResolution, GraphSignatureRecord, GraphPairFinding, V4ExperimentReport, build_v4_program, resolve_case, run_v4_experiments, main
#   internal_surface: _candidate_targets, _apply_edges, _graph_view, _build_ucns_graph_envelope, _resolution_values, _pair_findings
#   auth_boundary: none
#   storage_boundary: writes only caller-selected report path
#   network_boundary: none; exact UCNS checkout and installed package are verified locally
#   user_data_boundary: fixed synthetic transcripts with declared node/reference annotations only
#   admin_only: false
#   tests: tests/test_ucns_edcm_experiments_v4.py
#   rollout: explicit versioned research program; v0.1-v0.3 remain immutable and no canon selection is made
#   rollback: remove v0.4 module, workflow calls, and result; earlier reports and frozen baseline remain unchanged
#   requires: edcm_ucns_edcm_experiments, edcm_ucns_edcm_experiments_v2, edcm_ucns_edcm_experiments_v3, edcmbone_parser_turns_rounds, edcmbone_metrics_compute
#   since: 2026-07-21
#   unresolved: general anaphora, cyclic reference, independent annotation, multilingual discourse, external replication, and joint canon authority
# === END MODULE_BUILD ===

from __future__ import annotations

import argparse
import itertools
import json
import os
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .ucns_edcm_experiments import (
    BASELINE_CANDIDATE_ID,
    CandidateReadout,
    ExperimentCase,
    ExperimentPartition,
    RelationOperator,
    RelationVerdict,
    _digest,
    _evaluate_relation,
    _jsonable,
    _load_ucns,
    _readout_index,
    _verify_ucns_identity,
    baseline_readout,
    EXPECTED_UCNS_COMMIT,
)
from .ucns_edcm_experiments_v3 import scope_assertion_readout

PROGRAM_SCHEMA = "edcm.ucns-edcm-experiment-report/0.4.0"
PROGRAM_VERSION = "0.4.0"
PRIOR_V1_REPORT_DIGEST = "4c8bd8496ec549c1073320bafc995c7c65eaf81c9385e4dc6fff7794ed3b1124"
PRIOR_V2_REPORT_DIGEST = "85d6a9c7504a7e9b7fdb21e0dec5ff8e588d12e9d893f1a22854c1ae2ebbf0e4"
PRIOR_V3_REPORT_DIGEST = "5baf611b5930d271a0fa7dbc977a55c7748b0891196d619b4695e39308cff37b"

EXPLICIT_RESOLVER = "explicit-reference-v1"
NEAREST_RESOLVER = "nearest-compatible-v1"
SAME_SPEAKER_RESOLVER = "same-speaker-nearest-v1"
FAMILY_WIDE_RESOLVER = "family-wide-v1"
AMBIGUITY_RESOLVER = "ambiguity-preserving-v1"
RESOLVER_IDS = (
    EXPLICIT_RESOLVER,
    NEAREST_RESOLVER,
    SAME_SPEAKER_RESOLVER,
    FAMILY_WIDE_RESOLVER,
    AMBIGUITY_RESOLVER,
)

_STATE_ACTIVE = "active"
_STATE_SUSPENDED = "suspended"
_STATE_RETRACTED = "retracted"
_STATE_CONDITIONAL = "conditional-pending"
_STATE_INACTIVE_CONDITION = "inactive-by-condition"
_STATE_QUOTED = "quoted-only"


@dataclass(frozen=True, slots=True)
class DiscourseNode:
    node_id: str
    case_id: str
    turn_index: int
    speaker: str
    family: str
    surface: str
    label: str | None = None
    group: str | None = None
    quoted_parent: str | None = None
    initial_state: str = _STATE_ACTIVE

    def __post_init__(self) -> None:
        if not self.node_id or not self.case_id or not self.family or not self.surface:
            raise ValueError("discourse node fields must be nonempty")
        if self.turn_index < 0:
            raise ValueError("turn_index must be nonnegative")


@dataclass(frozen=True, slots=True)
class ReferenceExpression:
    reference_id: str
    case_id: str
    turn_index: int
    speaker: str
    relation: str
    selector: str
    selector_value: str | int | None
    family: str | None
    group: str | None
    surface: str
    declared_targets: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.reference_id or not self.case_id or not self.relation or not self.selector:
            raise ValueError("reference fields must be nonempty")
        if self.turn_index < 0:
            raise ValueError("turn_index must be nonnegative")
        object.__setattr__(self, "declared_targets", tuple(self.declared_targets))


@dataclass(frozen=True, slots=True)
class GraphCase:
    source: ExperimentCase
    nodes: tuple[DiscourseNode, ...]
    references: tuple[ReferenceExpression, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "nodes", tuple(self.nodes))
        object.__setattr__(self, "references", tuple(self.references))
        if any(node.case_id != self.source.case_id for node in self.nodes):
            raise ValueError("node case identity mismatch")
        if any(ref.case_id != self.source.case_id for ref in self.references):
            raise ValueError("reference case identity mismatch")
        ids = [node.node_id for node in self.nodes]
        if len(ids) != len(set(ids)):
            raise ValueError("node identifiers must be unique per case")


@dataclass(frozen=True, slots=True)
class GraphEdge:
    edge_id: str
    case_id: str
    resolver_id: str
    reference_id: str
    source_turn: int
    target_node_id: str
    relation: str


@dataclass(frozen=True, slots=True)
class NodeState:
    node_id: str
    state: str
    contradictions: int = 0


@dataclass(frozen=True, slots=True)
class GraphInterpretation:
    interpretation_id: str
    case_id: str
    resolver_id: str
    edges: tuple[GraphEdge, ...]
    node_states: tuple[NodeState, ...]
    unresolved_references: tuple[str, ...]
    gold_hits: int
    gold_misses: int

    @property
    def digest(self) -> str:
        return _digest(asdict(self))


@dataclass(frozen=True, slots=True)
class GraphResolution:
    case_id: str
    resolver_id: str
    interpretations: tuple[GraphInterpretation, ...]


@dataclass(frozen=True, slots=True)
class GraphExpectedRelation:
    relation_id: str
    readout: str
    left_resolution: str
    operator: RelationOperator
    right_resolution: str
    rationale: str


@dataclass(frozen=True, slots=True)
class GraphSignatureRecord:
    resolution_id: str
    interpretation_id: str
    support_policy: str
    view_name: str
    signature: str
    information_loss: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class GraphPairFinding:
    pair_id: str
    view_name: str
    readout: str
    left_resolution: str
    right_resolution: str
    structures_equivalent: bool
    readout_equivalent: bool
    status: str
    information_loss: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class V4ExperimentReport:
    schema: str
    program_version: str
    prior_v1_report_digest: str
    prior_v2_report_digest: str
    prior_v3_report_digest: str
    edcm_commit: str
    ucns_commit: str
    ucns_source_manifest: str
    ucns_identity_verified: bool
    cases: tuple[ExperimentCase, ...]
    nodes: tuple[DiscourseNode, ...]
    references: tuple[ReferenceExpression, ...]
    resolver_identities: tuple[tuple[str, str], ...]
    resolutions: tuple[GraphResolution, ...]
    readouts: tuple[CandidateReadout, ...]
    structural_signatures: tuple[GraphSignatureRecord, ...]
    relation_verdicts: tuple[RelationVerdict, ...]
    pair_findings: tuple[GraphPairFinding, ...]
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


def _source(case_id: str, transcript: str, partition: ExperimentPartition, manipulation: str, *tags: str) -> ExperimentCase:
    return ExperimentCase(
        case_id,
        transcript,
        partition,
        manipulation,
        "synthetic declared-graph corpus authored for UCNS-EDCM experiment v0.4",
        tuple(tags),
    )


def _node(case_id: str, node_id: str, turn: int, speaker: str, family: str, surface: str, **kwargs: Any) -> DiscourseNode:
    return DiscourseNode(node_id, case_id, turn, speaker, family, surface, **kwargs)


def _ref(
    case_id: str,
    reference_id: str,
    turn: int,
    speaker: str,
    relation: str,
    selector: str,
    value: str | int | None,
    family: str | None,
    surface: str,
    declared_targets: Sequence[str],
    *,
    group: str | None = None,
) -> ReferenceExpression:
    return ReferenceExpression(
        reference_id,
        case_id,
        turn,
        speaker,
        relation,
        selector,
        value,
        family,
        group,
        surface,
        tuple(declared_targets),
    )


def build_v4_program() -> tuple[tuple[GraphCase, ...], tuple[GraphExpectedRelation, ...]]:
    cases: list[GraphCase] = []

    for target in ("R1", "R2"):
        cid = f"explicit-{target.lower()}"
        cases.append(
            GraphCase(
                _source(
                    cid,
                    f"A: R1: Submit the form.\nA: R2: Attend the briefing.\nA: {target} is withdrawn.",
                    ExperimentPartition.DEVELOPMENT if target == "R1" else ExperimentPartition.HOLDOUT,
                    f"explicitly retract {target}",
                    "explicit-target",
                ),
                (
                    _node(cid, "R1", 0, "A", "requirement", "Submit the form", label="R1", group="requirements"),
                    _node(cid, "R2", 1, "A", "requirement", "Attend the briefing", label="R2", group="requirements"),
                ),
                (_ref(cid, "X1", 2, "A", "retracts", "label", target, "requirement", f"{target} is withdrawn", (target,), group="requirements"),),
            )
        )

    for ordinal, target in ((1, "O1"), (2, "O2")):
        cid = f"ordinal-{ordinal}"
        cases.append(
            GraphCase(
                _source(
                    cid,
                    f"A: Submit the form.\nA: Attend the briefing.\nA: The {'first' if ordinal == 1 else 'second'} requirement is withdrawn.",
                    ExperimentPartition.DEVELOPMENT if ordinal == 1 else ExperimentPartition.HOLDOUT,
                    f"retract ordinal requirement {ordinal}",
                    "ordinal-target",
                ),
                (
                    _node(cid, "O1", 0, "A", "requirement", "Submit the form", group="requirements"),
                    _node(cid, "O2", 1, "A", "requirement", "Attend the briefing", group="requirements"),
                ),
                (_ref(cid, "X1", 2, "A", "retracts", "ordinal", ordinal, "requirement", "ordinal requirement is withdrawn", (target,), group="requirements"),),
            )
        )

    cid = "anaphora-ambiguous"
    cases.append(
        GraphCase(
            _source(cid, "A: Submit the form.\nA: Attend the briefing.\nA: That requirement is suspended.", ExperimentPartition.HOLDOUT, "underspecified compatible antecedent", "anaphora", "ambiguity"),
            (
                _node(cid, "A1", 0, "A", "requirement", "Submit the form", group="requirements"),
                _node(cid, "A2", 1, "A", "requirement", "Attend the briefing", group="requirements"),
            ),
            (_ref(cid, "X1", 2, "A", "suspends", "pronoun", "that requirement", "requirement", "That requirement is suspended", ("A1", "A2"), group="requirements"),),
        )
    )

    cid = "speaker-ownership"
    cases.append(
        GraphCase(
            _source(cid, "A: Submit the form.\nB: Attend the briefing.\nA: I withdraw my requirement.", ExperimentPartition.HOLDOUT, "speaker-owned target competes with nearest target", "ownership"),
            (
                _node(cid, "SA", 0, "A", "requirement", "Submit the form", group="requirements"),
                _node(cid, "SB", 1, "B", "requirement", "Attend the briefing", group="requirements"),
            ),
            (_ref(cid, "X1", 2, "A", "retracts", "self", "my requirement", "requirement", "I withdraw my requirement", ("SA",), group="requirements"),),
        )
    )

    cid = "nested-quotation"
    cases.append(
        GraphCase(
            _source(cid, 'A: Notice N1 says, "Command C1: You must comply."\nA: Notice N1 is rescinded.', ExperimentPartition.HOLDOUT, "outer notice rescinded without automatically retracting inner quoted command", "quotation", "nesting"),
            (
                _node(cid, "N1", 0, "A", "notice", "Notice N1", label="N1", group="notice-stack"),
                _node(cid, "C1", 0, "NOTICE", "requirement", "You must comply", label="C1", group="notice-stack", quoted_parent="N1", initial_state=_STATE_QUOTED),
            ),
            (_ref(cid, "X1", 1, "A", "retracts", "label", "N1", "notice", "Notice N1 is rescinded", ("N1",), group="notice-stack"),),
        )
    )

    cid = "suspend-only"
    cases.append(
        GraphCase(
            _source(cid, "A: R1: Submit the form.\nA: R1 is suspended until noon.", ExperimentPartition.DEVELOPMENT, "temporary suspension without resumption", "suspension"),
            (_node(cid, "R1", 0, "A", "requirement", "Submit the form", label="R1"),),
            (_ref(cid, "X1", 1, "A", "suspends", "label", "R1", "requirement", "R1 is suspended until noon", ("R1",)),),
        )
    )

    cid = "suspend-resumed"
    cases.append(
        GraphCase(
            _source(cid, "A: R1: Submit the form.\nA: R1 is suspended until noon.\nA: Noon has passed; R1 resumes.", ExperimentPartition.HOLDOUT, "suspension followed by explicit resumption", "suspension", "resumption"),
            (_node(cid, "R1", 0, "A", "requirement", "Submit the form", label="R1"),),
            (
                _ref(cid, "X1", 1, "A", "suspends", "label", "R1", "requirement", "R1 is suspended until noon", ("R1",)),
                _ref(cid, "X2", 2, "A", "resumes", "label", "R1", "requirement", "R1 resumes", ("R1",)),
            ),
        )
    )

    for result, relation, final_state in (("fail", "activates", _STATE_ACTIVE), ("pass", "deactivates", _STATE_INACTIVE_CONDITION)):
        cid = f"condition-{result}"
        cases.append(
            GraphCase(
                _source(cid, f"A: C1: Access will be revoked if the audit fails.\nB: The audit did {'fail' if result == 'fail' else 'not fail'}.", ExperimentPartition.HOLDOUT, f"conditional consequence after audit {result}", "condition", result),
                (_node(cid, "C1", 0, "A", "consequence", "Access will be revoked if the audit fails", label="C1", initial_state=_STATE_CONDITIONAL),),
                (_ref(cid, "X1", 1, "B", relation, "label", "C1", "consequence", f"audit {result}", ("C1",)),),
            )
        )

    cid = "contradiction-other"
    cases.append(
        GraphCase(
            _source(cid, "A: R1: Submit the form.\nB: R1 does not apply.", ExperimentPartition.HOLDOUT, "other-speaker contradiction without retraction", "contradiction"),
            (_node(cid, "R1", 0, "A", "requirement", "Submit the form", label="R1"),),
            (_ref(cid, "X1", 1, "B", "contradicts", "label", "R1", "requirement", "R1 does not apply", ("R1",)),),
        )
    )

    cid = "retraction-self"
    cases.append(
        GraphCase(
            _source(cid, "A: R1: Submit the form.\nA: I withdraw R1.", ExperimentPartition.DEVELOPMENT, "speaker retracts own requirement", "retraction"),
            (_node(cid, "R1", 0, "A", "requirement", "Submit the form", label="R1"),),
            (_ref(cid, "X1", 1, "A", "retracts", "label", "R1", "requirement", "I withdraw R1", ("R1",)),),
        )
    )

    cid = "repair-ambiguous"
    cases.append(
        GraphCase(
            _source(cid, "A: Submit the form.\nA: Attend the briefing.\nA: The earlier instruction is corrected.", ExperimentPartition.HOLDOUT, "underspecified repair target", "repair", "ambiguity"),
            (
                _node(cid, "P1", 0, "A", "requirement", "Submit the form", group="instructions"),
                _node(cid, "P2", 1, "A", "requirement", "Attend the briefing", group="instructions"),
            ),
            (_ref(cid, "X1", 2, "A", "repairs", "pronoun", "earlier instruction", "requirement", "The earlier instruction is corrected", ("P1", "P2"), group="instructions"),),
        )
    )

    relations = (
        GraphExpectedRelation("explicit-r1-target", "graph.node.R1.active", f"explicit-r1::{EXPLICIT_RESOLVER}", RelationOperator.LT, f"explicit-r2::{EXPLICIT_RESOLVER}", "explicit labels must preserve which requirement remains active"),
        GraphExpectedRelation("explicit-family-overreach", "graph.active_count_min", f"explicit-r1::{FAMILY_WIDE_RESOLVER}", RelationOperator.LT, f"explicit-r1::{EXPLICIT_RESOLVER}", "family-wide retraction should over-retract the explicit-label case"),
        GraphExpectedRelation("ordinal-first-target", "graph.node.O1.active", f"ordinal-1::{EXPLICIT_RESOLVER}", RelationOperator.LT, f"ordinal-2::{EXPLICIT_RESOLVER}", "ordinal target resolution must preserve first versus second"),
        GraphExpectedRelation("anaphora-explicit-unresolved", "graph.unresolved_count_max", f"anaphora-ambiguous::{EXPLICIT_RESOLVER}", RelationOperator.GT, f"anaphora-ambiguous::{NEAREST_RESOLVER}", "explicit-only resolution must fail closed on an underspecified pronoun"),
        GraphExpectedRelation("anaphora-alternatives", "graph.alternative_count", f"anaphora-ambiguous::{AMBIGUITY_RESOLVER}", RelationOperator.GT, f"anaphora-ambiguous::{NEAREST_RESOLVER}", "ambiguity-preserving resolution must retain multiple alternatives"),
        GraphExpectedRelation("ownership-same-speaker", "graph.gold_hits_min", f"speaker-ownership::{SAME_SPEAKER_RESOLVER}", RelationOperator.GT, f"speaker-ownership::{NEAREST_RESOLVER}", "speaker-owned reference should outperform nearest-only target selection"),
        GraphExpectedRelation("nested-inner-survives", "graph.node.C1.retracted", f"nested-quotation::{EXPLICIT_RESOLVER}", RelationOperator.LT, f"nested-quotation::{FAMILY_WIDE_RESOLVER}", "rescinding the outer notice must not automatically retract the inner quoted command"),
        GraphExpectedRelation("resumption-reactivates", "graph.active_count_min", f"suspend-resumed::{EXPLICIT_RESOLVER}", RelationOperator.GT, f"suspend-only::{EXPLICIT_RESOLVER}", "resumption should restore the suspended requirement"),
        GraphExpectedRelation("condition-fail-activates", "graph.node.C1.active", f"condition-fail::{EXPLICIT_RESOLVER}", RelationOperator.GT, f"condition-pass::{EXPLICIT_RESOLVER}", "audit failure and success must produce different conditional states"),
        GraphExpectedRelation("contradiction-not-retraction", "graph.active_count_min", f"contradiction-other::{EXPLICIT_RESOLVER}", RelationOperator.GT, f"retraction-self::{EXPLICIT_RESOLVER}", "contradiction by another speaker must not silently retract the source event"),
        GraphExpectedRelation("ambiguous-repair-divergence", "graph.state_divergence", f"repair-ambiguous::{AMBIGUITY_RESOLVER}", RelationOperator.GT, f"repair-ambiguous::{NEAREST_RESOLVER}", "ambiguous repair must expose divergent graph outcomes"),
        GraphExpectedRelation("ownership-speaker-state", "graph.speaker.A.active_min", f"speaker-ownership::{SAME_SPEAKER_RESOLVER}", RelationOperator.LT, f"speaker-ownership::{NEAREST_RESOLVER}", "speaker-scoped state must preserve which speaker's requirement remains active"),
        GraphExpectedRelation("nearest-ownership-hypothesis", "graph.gold_hits_min", f"speaker-ownership::{NEAREST_RESOLVER}", RelationOperator.EQ, f"speaker-ownership::{SAME_SPEAKER_RESOLVER}", "nearest-compatible is tested for ownership-sensitive target selection"),
        GraphExpectedRelation("family-wide-specificity-hypothesis", "graph.active_count_min", f"explicit-r1::{FAMILY_WIDE_RESOLVER}", RelationOperator.EQ, f"explicit-r1::{EXPLICIT_RESOLVER}", "family-wide is tested for preserving explicit target specificity without over-retraction"),
        GraphExpectedRelation("explicit-anaphora-hypothesis", "graph.unresolved_count_max", f"anaphora-ambiguous::{EXPLICIT_RESOLVER}", RelationOperator.EQ, f"anaphora-ambiguous::{NEAREST_RESOLVER}", "explicit-only resolution is tested for underspecified anaphora"),
        GraphExpectedRelation("baseline-target-state-hypothesis", "edcm.baseline.kappa_final", "explicit-r1", RelationOperator.NE, "explicit-r2", "the frozen baseline is tested for which-target state sensitivity"),
        GraphExpectedRelation("node-reference-target-state-hypothesis", "ucns.node-reference.W.min", f"explicit-r1::{EXPLICIT_RESOLVER}", RelationOperator.NE, f"explicit-r1::{FAMILY_WIDE_RESOLVER}", "node-reference scalar support is tested for resolver-edge sensitivity"),
        GraphExpectedRelation("node-edge-target-state-control", "ucns.node-edge.W.min", f"explicit-r1::{EXPLICIT_RESOLVER}", RelationOperator.LT, f"explicit-r1::{FAMILY_WIDE_RESOLVER}", "node-edge support should retain the extra family-wide edge"),
        GraphExpectedRelation("local-scope-target-invariant", "edcm.scope.asserted_constraint_events", "explicit-r1", RelationOperator.EQ, "explicit-r2", "local scope event count should remain invariant when only the discourse target changes"),
    )

    return tuple(cases), relations


def _prior_nodes(case: GraphCase, reference: ReferenceExpression) -> tuple[DiscourseNode, ...]:
    return tuple(node for node in case.nodes if node.turn_index < reference.turn_index)


def _compatible(case: GraphCase, reference: ReferenceExpression) -> tuple[DiscourseNode, ...]:
    nodes = _prior_nodes(case, reference)
    if reference.family is not None:
        nodes = tuple(node for node in nodes if node.family == reference.family)
    if reference.group is not None and reference.selector in {"group", "pronoun"}:
        grouped = tuple(node for node in nodes if node.group == reference.group)
        if grouped:
            nodes = grouped
    return nodes


def _candidate_targets(case: GraphCase, reference: ReferenceExpression, resolver_id: str) -> tuple[tuple[str, ...], ...]:
    compatible = _compatible(case, reference)
    if resolver_id == EXPLICIT_RESOLVER:
        if reference.selector == "label":
            targets = tuple(node.node_id for node in compatible if node.label == str(reference.selector_value))
            return (targets,) if targets else ((),)
        if reference.selector == "ordinal":
            index = int(reference.selector_value) - 1
            ordered = sorted(compatible, key=lambda node: (node.turn_index, node.node_id))
            return ((ordered[index].node_id,),) if 0 <= index < len(ordered) else ((),)
        return ((),)
    if resolver_id == NEAREST_RESOLVER:
        if not compatible:
            return ((),)
        target = max(compatible, key=lambda node: (node.turn_index, node.node_id))
        return ((target.node_id,),)
    if resolver_id == SAME_SPEAKER_RESOLVER:
        owned = tuple(node for node in compatible if node.speaker == reference.speaker)
        if not owned:
            return ((),)
        target = max(owned, key=lambda node: (node.turn_index, node.node_id))
        return ((target.node_id,),)
    if resolver_id == FAMILY_WIDE_RESOLVER:
        if reference.group is not None:
            grouped = tuple(node for node in _prior_nodes(case, reference) if node.group == reference.group)
            if grouped:
                compatible = grouped
        return (tuple(node.node_id for node in sorted(compatible, key=lambda node: (node.turn_index, node.node_id))),)
    if resolver_id == AMBIGUITY_RESOLVER:
        if reference.selector in {"label", "ordinal"}:
            return _candidate_targets(case, reference, EXPLICIT_RESOLVER)
        if not compatible:
            return ((),)
        return tuple((node.node_id,) for node in sorted(compatible, key=lambda node: (node.turn_index, node.node_id)))
    raise KeyError(f"unknown resolver: {resolver_id}")


def _transition(state: str, relation: str) -> str:
    if relation in {"retracts", "repairs"}:
        return _STATE_RETRACTED
    if relation == "suspends":
        return _STATE_SUSPENDED
    if relation in {"resumes", "activates"}:
        return _STATE_ACTIVE
    if relation == "deactivates":
        return _STATE_INACTIVE_CONDITION
    return state


def _apply_edges(case: GraphCase, resolver_id: str, choices: Sequence[tuple[str, ...]]) -> GraphInterpretation:
    states: dict[str, NodeState] = {node.node_id: NodeState(node.node_id, node.initial_state, 0) for node in case.nodes}
    edges: list[GraphEdge] = []
    unresolved: list[str] = []
    gold_hits = 0
    gold_misses = 0
    ordered_refs = sorted(case.references, key=lambda ref: (ref.turn_index, ref.reference_id))
    for reference, targets in zip(ordered_refs, choices):
        if not targets:
            unresolved.append(reference.reference_id)
            if reference.declared_targets:
                gold_misses += 1
            continue
        for target in targets:
            edge = GraphEdge(
                f"{case.source.case_id}:{resolver_id}:{reference.reference_id}:{target}",
                case.source.case_id,
                resolver_id,
                reference.reference_id,
                reference.turn_index,
                target,
                reference.relation,
            )
            edges.append(edge)
            if target in reference.declared_targets:
                gold_hits += 1
            else:
                gold_misses += 1
            current = states[target]
            if reference.relation == "contradicts":
                states[target] = NodeState(target, current.state, current.contradictions + 1)
            else:
                states[target] = NodeState(target, _transition(current.state, reference.relation), current.contradictions)
    payload = {
        "case": case.source.case_id,
        "resolver": resolver_id,
        "edges": [asdict(edge) for edge in edges],
        "states": [asdict(states[key]) for key in sorted(states)],
        "unresolved": sorted(unresolved),
    }
    iid = f"{case.source.case_id}:{resolver_id}:{_digest(payload)[:16]}"
    return GraphInterpretation(
        iid,
        case.source.case_id,
        resolver_id,
        tuple(edges),
        tuple(states[key] for key in sorted(states)),
        tuple(sorted(unresolved)),
        gold_hits,
        gold_misses,
    )


def resolve_case(case: GraphCase, resolver_id: str) -> GraphResolution:
    target_options = [_candidate_targets(case, ref, resolver_id) for ref in sorted(case.references, key=lambda item: (item.turn_index, item.reference_id))]
    combinations = itertools.product(*target_options)
    interpretations: list[GraphInterpretation] = []
    for index, choices in enumerate(combinations):
        if index >= 32:
            break
        interpretations.append(_apply_edges(case, resolver_id, choices))
    if not interpretations:
        interpretations.append(_apply_edges(case, resolver_id, ()))
    unique = {interpretation.digest: interpretation for interpretation in interpretations}
    return GraphResolution(case.source.case_id, resolver_id, tuple(unique[key] for key in sorted(unique)))


def _state_map(interpretation: GraphInterpretation) -> dict[str, NodeState]:
    return {state.node_id: state for state in interpretation.node_states}


def _resolution_values(case: GraphCase, resolution: GraphResolution) -> tuple[tuple[str, Any], ...]:
    interpretations = resolution.interpretations
    active_counts = []
    suspended_counts = []
    retracted_counts = []
    unresolved_counts = []
    edge_counts = []
    gold_hits = []
    gold_misses = []
    state_signatures = set()
    node_ids = sorted(node.node_id for node in case.nodes)
    speaker_by_node = {node.node_id: node.speaker for node in case.nodes}
    speaker_ids = sorted(set(speaker_by_node.values()))
    per_node: dict[str, list[float]] = {node_id: [] for node_id in node_ids}
    per_node_retracted: dict[str, list[float]] = {node_id: [] for node_id in node_ids}
    per_speaker_active: dict[str, list[float]] = {speaker: [] for speaker in speaker_ids}
    contradiction_counts = []
    for interpretation in interpretations:
        states = _state_map(interpretation)
        active_counts.append(sum(state.state == _STATE_ACTIVE for state in states.values()))
        suspended_counts.append(sum(state.state == _STATE_SUSPENDED for state in states.values()))
        retracted_counts.append(sum(state.state == _STATE_RETRACTED for state in states.values()))
        contradiction_counts.append(sum(state.contradictions for state in states.values()))
        unresolved_counts.append(len(interpretation.unresolved_references))
        edge_counts.append(len(interpretation.edges))
        gold_hits.append(interpretation.gold_hits)
        gold_misses.append(interpretation.gold_misses)
        state_signatures.add(_digest(tuple((node_id, states[node_id].state, states[node_id].contradictions) for node_id in node_ids)))
        for node_id in node_ids:
            per_node[node_id].append(1.0 if states[node_id].state == _STATE_ACTIVE else 0.0)
            per_node_retracted[node_id].append(1.0 if states[node_id].state == _STATE_RETRACTED else 0.0)
        for speaker in speaker_ids:
            per_speaker_active[speaker].append(
                float(sum(states[node_id].state == _STATE_ACTIVE for node_id in node_ids if speaker_by_node[node_id] == speaker))
            )
    values: list[tuple[str, Any]] = [
        ("graph.alternative_count", float(len(interpretations))),
        ("graph.state_divergence", float(max(0, len(state_signatures) - 1))),
        ("graph.active_count_min", float(min(active_counts))),
        ("graph.active_count_max", float(max(active_counts))),
        ("graph.suspended_count_max", float(max(suspended_counts))),
        ("graph.retracted_count_max", float(max(retracted_counts))),
        ("graph.contradiction_count_max", float(max(contradiction_counts))),
        ("graph.unresolved_count_max", float(max(unresolved_counts))),
        ("graph.edge_count_min", float(min(edge_counts))),
        ("graph.edge_count_max", float(max(edge_counts))),
        ("graph.gold_hits_min", float(min(gold_hits))),
        ("graph.gold_misses_max", float(max(gold_misses))),
    ]
    for node_id in node_ids:
        values.append((f"graph.node.{node_id}.active", float(min(per_node[node_id]))))
        values.append((f"graph.node.{node_id}.retracted", float(max(per_node_retracted[node_id]))))
    for speaker in speaker_ids:
        values.append((f"graph.speaker.{speaker}.active_min", float(min(per_speaker_active[speaker]))))
        values.append((f"graph.speaker.{speaker}.active_max", float(max(per_speaker_active[speaker]))))
    return tuple(values)

def _graph_view(case: GraphCase, interpretation: GraphInterpretation, view_name: str) -> tuple[Any, tuple[str, ...]]:
    nodes = sorted(case.nodes, key=lambda node: (node.turn_index, node.node_id))
    edges = sorted(interpretation.edges, key=lambda edge: (edge.source_turn, edge.reference_id, edge.target_node_id, edge.relation))
    quote_edges = sorted((node.quoted_parent, node.node_id, "quotes") for node in nodes if node.quoted_parent is not None)
    states = _state_map(interpretation)
    if view_name == "exact-ordered-labeled":
        return (
            {
                "nodes": [(node.node_id, node.turn_index, node.speaker, node.family, node.label, node.group, node.quoted_parent, node.initial_state) for node in nodes],
                "references": [(ref.reference_id, ref.turn_index, ref.speaker, ref.relation, ref.selector, ref.selector_value) for ref in sorted(case.references, key=lambda item: (item.turn_index, item.reference_id))],
                "edges": [(edge.reference_id, edge.target_node_id, edge.relation) for edge in edges] + quote_edges,
                "states": [(node.node_id, states[node.node_id].state, states[node.node_id].contradictions) for node in nodes],
            },
            (),
        )
    if view_name == "labeled-multigraph":
        return (
            {
                "nodes": sorted((node.node_id, node.speaker, node.family, node.label, node.group, node.quoted_parent, node.initial_state) for node in nodes),
                "edges": sorted([(edge.reference_id, edge.target_node_id, edge.relation) for edge in edges] + quote_edges),
                "states": sorted((node.node_id, states[node.node_id].state, states[node.node_id].contradictions) for node in nodes),
            },
            ("order",),
        )
    if view_name == "unlabeled-multigraph":
        return (
            {
                "nodes": sorted((node.node_id, node.speaker, node.family) for node in nodes),
                "edges": sorted([(edge.reference_id, edge.target_node_id) for edge in edges] + [(parent, child) for parent, child, _ in quote_edges]),
                "states": sorted((node.node_id, states[node.node_id].state) for node in nodes),
            },
            ("edge-labels", "order"),
        )
    if view_name == "flat-node-multiset":
        return (
            sorted((node.speaker, node.family, node.initial_state) for node in nodes),
            ("edge-direction", "edge-labels", "node-labels", "order", "reference-identity", "state"),
        )
    if view_name == "active-state-summary":
        summary: dict[str, int] = {}
        for state in states.values():
            summary[state.state] = summary.get(state.state, 0) + 1
        return (sorted(summary.items()), ("edge-direction", "edge-labels", "node-labels", "order", "reference-identity", "speaker-ownership"))
    raise KeyError(view_name)

def _build_ucns_graph_envelope(case: GraphCase, interpretation: GraphInterpretation, support_policy: str, ucns_api: Mapping[str, Any]) -> Any:
    Cell = ucns_api["Cell"]
    RetainedLayer = ucns_api["RetainedLayer"]
    make_carrier = ucns_api["make_carrier"]
    make_retained_structure = ucns_api["make_retained_structure"]
    states = _state_map(interpretation)
    cells = []
    for node in sorted(case.nodes, key=lambda item: (item.turn_index, item.node_id)):
        if support_policy in {"node-reference", "node-edge"}:
            mu = 1.0
        elif support_policy == "state-detail":
            state = states[node.node_id]
            mu = 1.0 + (1.0 if state.state == _STATE_ACTIVE else 0.0) + float(state.contradictions > 0)
        else:
            raise KeyError(support_policy)
        cells.append(Cell(coordinate=("node", node.node_id), payload=asdict(node), type_tag="discourse-node", state=(states[node.node_id].state,), provenance=(case.source.case_id, interpretation.interpretation_id), relation=None, mu=mu))
    unresolved = set(interpretation.unresolved_references)
    for reference in sorted(case.references, key=lambda item: (item.turn_index, item.reference_id)):
        reference_state = "unresolved" if reference.reference_id in unresolved else "resolved"
        reference_mu = 1.0 + (1.0 if support_policy == "state-detail" and reference_state == "unresolved" else 0.0)
        cells.append(Cell(coordinate=("reference", reference.reference_id), payload=asdict(reference), type_tag="discourse-reference", state=(reference_state,), provenance=(case.source.case_id, interpretation.interpretation_id), relation=None, mu=reference_mu))
    if support_policy in {"node-edge", "state-detail"}:
        for edge in interpretation.edges:
            cells.append(Cell(coordinate=("edge", edge.edge_id), payload=asdict(edge), type_tag="discourse-edge", state=(edge.relation,), provenance=(case.source.case_id, interpretation.interpretation_id), relation=(edge.reference_id, edge.target_node_id), mu=1.0))
        for node in case.nodes:
            if node.quoted_parent is not None:
                payload = {"source": node.quoted_parent, "target": node.node_id, "relation": "quotes"}
                cells.append(Cell(coordinate=("quote-edge", node.quoted_parent, node.node_id), payload=payload, type_tag="discourse-edge", state=("quotes",), provenance=(case.source.case_id, interpretation.interpretation_id), relation=(node.quoted_parent, node.node_id), mu=1.0))
    carrier = make_carrier(tuple(cells))
    layers = (
        RetainedLayer("references", tuple(asdict(ref) for ref in case.references)),
        RetainedLayer("graph-edges", tuple(asdict(edge) for edge in interpretation.edges)),
        RetainedLayer("node-states", tuple(asdict(state) for state in interpretation.node_states)),
        RetainedLayer("unresolved-references", interpretation.unresolved_references),
    )
    return make_retained_structure(carrier, layers)

def _resolution_readouts(case: GraphCase, resolution: GraphResolution, ucns_api: Mapping[str, Any]) -> list[CandidateReadout]:
    resolution_id = f"{case.source.case_id}::{resolution.resolver_id}"
    readouts = [CandidateReadout(resolution.resolver_id, resolution_id, _resolution_values(case, resolution), f"The-Interdependency/edcm:{resolution.resolver_id}")]
    cell_detail = ucns_api["cell_detail_breadth_candidate"]()
    for support in ("node-reference", "node-edge", "state-detail"):
        values = []
        for interpretation in resolution.interpretations:
            structure = _build_ucns_graph_envelope(case, interpretation, support, ucns_api)
            values.append((float(ucns_api["cell_support_weight"](structure)), float(cell_detail.evaluate(structure))))
        readouts.append(
            CandidateReadout(
                f"ucns-{support}-graph-pack",
                resolution_id,
                (
                    (f"ucns.{support}.W.min", min(value[0] for value in values)),
                    (f"ucns.{support}.W.max", max(value[0] for value in values)),
                    (f"ucns.{support}.B.cell-detail.min", min(value[1] for value in values)),
                    (f"ucns.{support}.B.cell-detail.max", max(value[1] for value in values)),
                ),
                f"The-Interdependency/ucns@{EXPECTED_UCNS_COMMIT}",
            )
        )
    return readouts

def _signatures(case: GraphCase, resolution: GraphResolution, ucns_api: Mapping[str, Any]) -> tuple[GraphSignatureRecord, ...]:
    records = []
    resolution_id = f"{case.source.case_id}::{resolution.resolver_id}"
    views = ("exact-ordered-labeled", "labeled-multigraph", "unlabeled-multigraph", "flat-node-multiset", "active-state-summary")
    bundle_parts: dict[tuple[str, str], list[str]] = {}
    bundle_losses: dict[tuple[str, str], set[str]] = {}
    for interpretation in resolution.interpretations:
        for support in ("node-reference", "node-edge", "state-detail"):
            for view_name in views:
                view, losses = _graph_view(case, interpretation, view_name)
                signature = _digest(view)
                records.append(GraphSignatureRecord(resolution_id, interpretation.interpretation_id, support, view_name, signature, tuple(sorted(losses))))
                key = (support, view_name)
                bundle_parts.setdefault(key, []).append(signature)
                bundle_losses.setdefault(key, set()).update(losses)
    for (support, view_name), parts in sorted(bundle_parts.items()):
        records.append(
            GraphSignatureRecord(
                resolution_id,
                "__bundle__",
                support,
                view_name,
                _digest(tuple(sorted(parts))),
                tuple(sorted(bundle_losses[(support, view_name)])),
            )
        )
    return tuple(records)

def _evaluate_graph_relation(relation: GraphExpectedRelation, index: Mapping[tuple[str, str], Any], comparison: Any) -> RelationVerdict:
    from .ucns_edcm_experiments import ExpectedRelation

    return _evaluate_relation(
        ExpectedRelation(relation.relation_id, relation.readout, relation.left_resolution, relation.operator, relation.right_resolution, relation.rationale),
        index,
        comparison,
    )


def _pair_findings(
    resolutions: Mapping[str, GraphResolution],
    cases: Mapping[str, GraphCase],
    signatures: Iterable[GraphSignatureRecord],
    index: Mapping[tuple[str, str], Any],
    comparison: Any,
) -> tuple[GraphPairFinding, ...]:
    signature_index = {(record.resolution_id, record.interpretation_id, record.view_name): record for record in signatures if record.support_policy == "node-edge"}
    specs = (
        ("explicit-family", f"explicit-r1::{EXPLICIT_RESOLVER}", f"explicit-r1::{FAMILY_WIDE_RESOLVER}", "graph.active_count_min"),
        ("ownership", f"speaker-ownership::{SAME_SPEAKER_RESOLVER}", f"speaker-ownership::{NEAREST_RESOLVER}", "graph.gold_hits_min"),
        ("ambiguity", f"repair-ambiguous::{AMBIGUITY_RESOLVER}", f"repair-ambiguous::{NEAREST_RESOLVER}", "graph.state_divergence"),
    )
    findings: list[GraphPairFinding] = []
    for pair_id, left_id, right_id, readout in specs:
        for view_name in ("exact-ordered-labeled", "labeled-multigraph", "unlabeled-multigraph", "flat-node-multiset", "active-state-summary"):
            left_record = signature_index[(left_id, "__bundle__", view_name)]
            right_record = signature_index[(right_id, "__bundle__", view_name)]
            structures_equal = left_record.signature == right_record.signature
            left_value = index.get((left_id, readout))
            right_value = index.get((right_id, readout))
            readout_equal = left_value is not None and right_value is not None and comparison.matches(left_value, right_value)
            if structures_equal and not readout_equal:
                status = "incompatible-for-readout"
            elif not structures_equal and not readout_equal:
                status = "preserves-observed-distinction"
            elif structures_equal and readout_equal:
                status = "compatible-on-this-pair"
            else:
                status = "structurally-distinct-readout-invariant"
            findings.append(GraphPairFinding(pair_id, view_name, readout, left_id, right_id, structures_equal, readout_equal, status, tuple(sorted(set(left_record.information_loss) | set(right_record.information_loss)))))
    return tuple(findings)

def run_v4_experiments(
    *,
    edcm_commit: str | None = None,
    ucns_commit: str = EXPECTED_UCNS_COMMIT,
    ucns_source_root: str | Path | None = None,
) -> V4ExperimentReport:
    if ucns_commit != EXPECTED_UCNS_COMMIT:
        raise ValueError(f"v0.4 requires UCNS {EXPECTED_UCNS_COMMIT}, got {ucns_commit}")
    source_root = ucns_source_root or os.environ.get("UCNS_SOURCE_ROOT")
    if source_root is None:
        raise ValueError("ucns_source_root or UCNS_SOURCE_ROOT is required")
    ucns_api = _load_ucns()
    verified_commit, manifest = _verify_ucns_identity(Path(source_root), ucns_api)
    comparison = ucns_api["combined_comparison_policy"](rel_tol=1e-9, abs_tol=1e-12, name="ucns-edcm-v0.4-combined", version="1")
    cases, relations = build_v4_program()
    case_map = {case.source.case_id: case for case in cases}
    resolutions: dict[str, GraphResolution] = {}
    readouts: list[CandidateReadout] = []
    signatures: list[GraphSignatureRecord] = []

    for case in cases:
        try:
            baseline = baseline_readout(case.source)
            readouts.append(CandidateReadout(BASELINE_CANDIDATE_ID, case.source.case_id, tuple((f"edcm.baseline.{key}", value) for key, value in sorted(baseline.items())), "The-Interdependency/edcm:edcm-measurement-v1"))
        except Exception as exc:
            readouts.append(CandidateReadout(BASELINE_CANDIDATE_ID, case.source.case_id, (), "The-Interdependency/edcm:edcm-measurement-v1", f"{type(exc).__name__}: {exc}"))
        try:
            scope = scope_assertion_readout(case.source)
            readouts.append(CandidateReadout("edcm-scope-assertion-v1", case.source.case_id, tuple((f"edcm.scope.{key}", value) for key, value in sorted(scope.items())), "The-Interdependency/edcm:edcm-scope-assertion-v1"))
        except Exception as exc:
            readouts.append(CandidateReadout("edcm-scope-assertion-v1", case.source.case_id, (), "The-Interdependency/edcm:edcm-scope-assertion-v1", f"{type(exc).__name__}: {exc}"))
        for resolver_id in RESOLVER_IDS:
            resolution = resolve_case(case, resolver_id)
            rid = f"{case.source.case_id}::{resolver_id}"
            resolutions[rid] = resolution
            readouts.extend(_resolution_readouts(case, resolution, ucns_api))
            signatures.extend(_signatures(case, resolution, ucns_api))

    index = _readout_index(readouts)
    verdicts = tuple(_evaluate_graph_relation(relation, index, comparison) for relation in relations)
    findings = _pair_findings(resolutions, case_map, signatures, index, comparison)
    resolver_identities = tuple((resolver, f"The-Interdependency/edcm:{resolver}") for resolver in RESOLVER_IDS)
    return V4ExperimentReport(
        PROGRAM_SCHEMA,
        PROGRAM_VERSION,
        PRIOR_V1_REPORT_DIGEST,
        PRIOR_V2_REPORT_DIGEST,
        PRIOR_V3_REPORT_DIGEST,
        edcm_commit or os.environ.get("GITHUB_SHA", "unrecorded-edcm-commit"),
        verified_commit,
        manifest,
        True,
        tuple(case.source for case in cases),
        tuple(node for case in cases for node in case.nodes),
        tuple(ref for case in cases for ref in case.references),
        resolver_identities,
        tuple(resolutions[key] for key in sorted(resolutions)),
        tuple(readouts),
        tuple(signatures),
        verdicts,
        findings,
        None,
        (
            "v0.1-v0.3 reports remain immutable prior evidence.",
            "Reference existence, target resolution, graph selection, and state transition remain separate evidence states.",
            "No resolver, relation vocabulary, graph view, support assignment, EDCM axis, M, B, or equivalence relation is selected as canon.",
        ),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--edcm-commit", default=None)
    parser.add_argument("--ucns-commit", default=EXPECTED_UCNS_COMMIT)
    parser.add_argument("--ucns-source-root", type=Path, default=None)
    args = parser.parse_args(argv)
    report = run_v4_experiments(edcm_commit=args.edcm_commit, ucns_commit=args.ucns_commit, ucns_source_root=args.ucns_source_root)
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
