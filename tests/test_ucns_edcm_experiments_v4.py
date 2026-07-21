# === CHECKS ===
# id: check_ucns_edcm_v4_program
#   proves: edcm_ucns_edcm_experiments_v4
#   call: self::test_v4_program_structure
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_ucns_edcm_v4_resolvers
#   proves: edcm_ucns_edcm_experiments_v4
#   call: self::test_v4_resolver_contrasts
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_ucns_edcm_v4_joint_report
#   proves: edcm_ucns_edcm_experiments_v4
#   call: self::test_v4_joint_report_preserves_graphs_and_no_canon
#   requires: python3
#   timeout: 30
#   mutates: temporary report only
#   cleanup: pytest tmp_path
# === END CHECKS ===

from dataclasses import replace
import json
import os
from pathlib import Path

import pytest

from edcm.ucns_edcm_experiments_v4 import (
    AMBIGUITY_RESOLVER,
    EXPLICIT_RESOLVER,
    FAMILY_WIDE_RESOLVER,
    NEAREST_RESOLVER,
    PRIOR_V1_REPORT_DIGEST,
    PRIOR_V2_REPORT_DIGEST,
    PRIOR_V3_REPORT_DIGEST,
    SAME_SPEAKER_RESOLVER,
    _graph_view,
    build_v4_program,
    main,
    resolve_case,
    run_v4_experiments,
)


def _case(case_id):
    cases, _ = build_v4_program()
    return next(case for case in cases if case.source.case_id == case_id)


def _states(resolution):
    assert len(resolution.interpretations) == 1
    return {state.node_id: state for state in resolution.interpretations[0].node_states}


def test_v4_program_structure() -> None:
    cases, relations = build_v4_program()
    assert len(cases) == 14
    assert len({case.source.case_id for case in cases}) == len(cases)
    assert len(relations) == 19
    assert {case.source.partition.value for case in cases} == {"development", "holdout"}
    assert all(case.nodes for case in cases)
    assert all(case.references for case in cases)
    assert all(reference.declared_targets for case in cases for reference in case.references)


def test_v4_resolver_contrasts() -> None:
    explicit_r1 = _states(resolve_case(_case("explicit-r1"), EXPLICIT_RESOLVER))
    explicit_r2 = _states(resolve_case(_case("explicit-r2"), EXPLICIT_RESOLVER))
    assert explicit_r1["R1"].state == "retracted"
    assert explicit_r1["R2"].state == "active"
    assert explicit_r2["R1"].state == "active"
    assert explicit_r2["R2"].state == "retracted"

    family = _states(resolve_case(_case("explicit-r1"), FAMILY_WIDE_RESOLVER))
    assert family["R1"].state == "retracted"
    assert family["R2"].state == "retracted"

    ambiguous = resolve_case(_case("anaphora-ambiguous"), AMBIGUITY_RESOLVER)
    assert len(ambiguous.interpretations) == 2
    assert {
        tuple((state.node_id, state.state) for state in interpretation.node_states)
        for interpretation in ambiguous.interpretations
    } == {
        (("A1", "active"), ("A2", "suspended")),
        (("A1", "suspended"), ("A2", "active")),
    }
    explicit_ambiguous = resolve_case(_case("anaphora-ambiguous"), EXPLICIT_RESOLVER)
    assert explicit_ambiguous.interpretations[0].unresolved_references == ("X1",)

    ownership_same = resolve_case(_case("speaker-ownership"), SAME_SPEAKER_RESOLVER)
    ownership_nearest = resolve_case(_case("speaker-ownership"), NEAREST_RESOLVER)
    assert ownership_same.interpretations[0].gold_hits == 1
    assert ownership_nearest.interpretations[0].gold_hits == 0

    nested_case = _case("nested-quotation")
    nested_resolution = resolve_case(nested_case, EXPLICIT_RESOLVER)
    nested_view, _ = _graph_view(nested_case, nested_resolution.interpretations[0], "exact-ordered-labeled")
    stripped_case = replace(nested_case, nodes=tuple(replace(node, quoted_parent=None) for node in nested_case.nodes))
    stripped_view, _ = _graph_view(stripped_case, nested_resolution.interpretations[0], "exact-ordered-labeled")
    assert nested_view != stripped_view

    nested_explicit = _states(nested_resolution)
    nested_wide = _states(resolve_case(nested_case, FAMILY_WIDE_RESOLVER))
    assert nested_explicit["N1"].state == "retracted"
    assert nested_explicit["C1"].state == "quoted-only"
    assert nested_wide["C1"].state == "retracted"

    suspended = _states(resolve_case(_case("suspend-only"), EXPLICIT_RESOLVER))
    resumed = _states(resolve_case(_case("suspend-resumed"), EXPLICIT_RESOLVER))
    assert suspended["R1"].state == "suspended"
    assert resumed["R1"].state == "active"

    failed = _states(resolve_case(_case("condition-fail"), EXPLICIT_RESOLVER))
    passed = _states(resolve_case(_case("condition-pass"), EXPLICIT_RESOLVER))
    assert failed["C1"].state == "active"
    assert passed["C1"].state == "inactive-by-condition"

    contradicted = _states(resolve_case(_case("contradiction-other"), EXPLICIT_RESOLVER))
    retracted = _states(resolve_case(_case("retraction-self"), EXPLICIT_RESOLVER))
    assert contradicted["R1"].state == "active"
    assert contradicted["R1"].contradictions == 1
    assert retracted["R1"].state == "retracted"

    repair = resolve_case(_case("repair-ambiguous"), AMBIGUITY_RESOLVER)
    assert len(repair.interpretations) == 2
    assert len({tuple((state.node_id, state.state) for state in item.node_states) for item in repair.interpretations}) == 2


def test_v4_joint_report_preserves_graphs_and_no_canon(tmp_path) -> None:
    pytest.importorskip("ucns")
    source_root = os.environ.get("UCNS_SOURCE_ROOT")
    if not source_root:
        pytest.skip("verified UCNS source checkout not supplied")

    report = run_v4_experiments(edcm_commit="test-v4-edcm", ucns_source_root=source_root)
    assert report.canon_selection is None
    assert report.prior_v1_report_digest == PRIOR_V1_REPORT_DIGEST
    assert report.prior_v2_report_digest == PRIOR_V2_REPORT_DIGEST
    assert report.prior_v3_report_digest == PRIOR_V3_REPORT_DIGEST
    assert report.ucns_identity_verified is True
    assert len(report.cases) == 14
    assert len(report.resolutions) == 70
    assert report.structural_signatures
    assert report.pair_findings
    assert all(item.status in {"supported", "falsified", "error"} for item in report.relation_verdicts)

    verdicts = {item.relation_id: item.status for item in report.relation_verdicts}
    for relation_id in (
        "explicit-r1-target",
        "explicit-family-overreach",
        "ordinal-first-target",
        "anaphora-explicit-unresolved",
        "anaphora-alternatives",
        "ownership-same-speaker",
        "nested-inner-survives",
        "resumption-reactivates",
        "condition-fail-activates",
        "contradiction-not-retraction",
        "ambiguous-repair-divergence",
        "ownership-speaker-state",
        "node-edge-target-state-control",
        "local-scope-target-invariant",
    ):
        assert verdicts[relation_id] == "supported"
    for relation_id in (
        "nearest-ownership-hypothesis",
        "family-wide-specificity-hypothesis",
        "explicit-anaphora-hypothesis",
        "baseline-target-state-hypothesis",
        "node-reference-target-state-hypothesis",
    ):
        assert verdicts[relation_id] == "falsified"

    def readout(case_id, name):
        for row in report.readouts:
            if row.case_id == case_id and row.error is None:
                try:
                    return row.value(name)
                except KeyError:
                    pass
        raise AssertionError((case_id, name))

    assert readout("anaphora-ambiguous::explicit-reference-v1", "ucns.node-reference.W.min") == readout(
        "anaphora-ambiguous::nearest-compatible-v1", "ucns.node-reference.W.min"
    )
    assert readout("speaker-ownership::same-speaker-nearest-v1", "graph.speaker.A.active_min") == 0.0
    assert readout("speaker-ownership::nearest-compatible-v1", "graph.speaker.A.active_min") == 1.0

    ambiguity_bundle = next(
        item for item in report.structural_signatures
        if item.resolution_id == "repair-ambiguous::ambiguity-preserving-v1"
        and item.interpretation_id == "__bundle__"
        and item.support_policy == "node-edge"
        and item.view_name == "exact-ordered-labeled"
    )
    nearest_bundle = next(
        item for item in report.structural_signatures
        if item.resolution_id == "repair-ambiguous::nearest-compatible-v1"
        and item.interpretation_id == "__bundle__"
        and item.support_policy == "node-edge"
        and item.view_name == "exact-ordered-labeled"
    )
    assert ambiguity_bundle.signature != nearest_bundle.signature
    ambiguity_finding = next(item for item in report.pair_findings if item.pair_id == "ambiguity" and item.view_name == "exact-ordered-labeled")
    assert ambiguity_finding.structures_equivalent is False
    assert ambiguity_finding.status == "preserves-observed-distinction"

    unresolved_resolution = next(item for item in report.resolutions if item.case_id == "anaphora-ambiguous" and item.resolver_id == EXPLICIT_RESOLVER)
    assert unresolved_resolution.interpretations[0].unresolved_references == ("X1",)
    ambiguity_resolution = next(item for item in report.resolutions if item.case_id == "anaphora-ambiguous" and item.resolver_id == AMBIGUITY_RESOLVER)
    assert len(ambiguity_resolution.interpretations) == 2

    output = tmp_path / "v0.4.json"
    assert main(["--output", str(output), "--edcm-commit", "test-v4-edcm", "--ucns-source-root", str(Path(source_root))]) == 0
    payload = json.loads(output.read_text())
    assert payload["schema"] == "edcm.ucns-edcm-experiment-report/0.4.0"
    assert payload["canon_selection"] is None
    assert payload["report_digest"]
