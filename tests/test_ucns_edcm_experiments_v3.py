# === CHECKS ===
# id: check_ucns_edcm_v3_program
#   proves: edcm_ucns_edcm_experiments_v3
#   call: self::test_v3_program_structure
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_scope_assertion_candidate
#   proves: edcm_ucns_edcm_experiments_v3
#   call: self::test_scope_assertion_candidate_invariants
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_ucns_edcm_v3_joint_report
#   proves: edcm_ucns_edcm_experiments_v3
#   call: self::test_v3_joint_report_preserves_scope_and_no_canon
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import json
import os
from pathlib import Path

import pytest

from edcm.ucns_edcm_experiments import EXPECTED_UCNS_COMMIT
from edcm.ucns_edcm_experiments_v3 import (
    PRIOR_V1_REPORT_DIGEST,
    PRIOR_V2_REPORT_DIGEST,
    ExperimentPartition,
    build_v3_program,
    main,
    run_v3_experiments,
    _extract_scope_events,
    scope_assertion_readout,
)


def _case(case_id):
    cases, _, _ = build_v3_program()
    return next(case for case in cases if case.case_id == case_id)


def test_v3_program_structure() -> None:
    cases, relations, pair_specs = build_v3_program()
    assert len(cases) == 14
    assert len({case.case_id for case in cases}) == len(cases)
    assert {case.partition for case in cases} == {
        ExperimentPartition.DEVELOPMENT,
        ExperimentPartition.HOLDOUT,
    }
    assert len(relations) == 23
    assert len(pair_specs) == 7
    assert all(case.digest == case.digest for case in cases)
    assert all(relation.rationale for relation in relations)


def test_scope_assertion_candidate_invariants() -> None:
    asserted = scope_assertion_readout(_case("penalty-asserted"))
    negated = scope_assertion_readout(_case("penalty-negated"))
    assert asserted["lexical_constraint_mentions"] == negated["lexical_constraint_mentions"] == 1.0
    assert asserted["asserted_constraint_events"] == 1.0
    assert negated["asserted_constraint_events"] == 0.0
    assert negated["negated_mentions"] == 1.0

    direct = scope_assertion_readout(_case("must-direct"))
    quoted = scope_assertion_readout(_case("must-quoted-rescinded"))
    assert direct["asserted_constraint_events"] > quoted["asserted_constraint_events"]
    assert quoted["quoted_mentions"] == 2.0
    assert quoted["retracted_mentions"] == 2.0

    operative = scope_assertion_readout(_case("revocation-operative"))
    hypothetical = scope_assertion_readout(_case("revocation-hypothetical"))
    assert operative["asserted_constraint_events"] > hypothetical["asserted_constraint_events"]
    assert hypothetical["hypothetical_mentions"] >= 1.0

    owned = scope_assertion_readout(_case("refusal-owned"))
    attributed = scope_assertion_readout(_case("refusal-attributed"))
    assert owned["owned_refusal_events"] == 1.0
    assert attributed["owned_refusal_events"] == 0.0
    assert attributed["attributed_refusal_mentions"] == 1.0

    repaired = scope_assertion_readout(_case("pressure-repaired"))
    renewed = scope_assertion_readout(_case("pressure-renewed"))
    assert repaired["final_active_pressure"] == 0.0
    assert renewed["final_active_pressure"] > 0.0

    active = scope_assertion_readout(_case("mandatory-active"))
    withdrawn = scope_assertion_readout(_case("mandatory-withdrawn"))
    assert active["asserted_constraint_events"] > withdrawn["asserted_constraint_events"]
    assert withdrawn["retracted_mentions"] >= 1.0

    positive = scope_assertion_readout(_case("refusal-positive"))
    refusal_negated = scope_assertion_readout(_case("refusal-negated"))
    assert positive["lexical_refusal_mentions"] == refusal_negated["lexical_refusal_mentions"] == 1.0
    assert positive["owned_refusal_events"] == 1.0
    assert refusal_negated["owned_refusal_events"] == 0.0
    assert refusal_negated["negated_mentions"] == 1.0


def test_scope_event_provenance_preserves_speaker_and_source_order() -> None:
    single = _extract_scope_events(_case("refusal-owned"))
    assert len(single) == 1
    assert single[0].speaker == "B"
    assert single[0].event_index == 1
    assert ":e1:" in single[0].event_id

    conditional = _extract_scope_events(_case("revocation-operative"))
    assert tuple(event.phrase for event in conditional) == (
        "refuse",
        "access will be revoked",
    )
    assert tuple(event.event_index for event in conditional) == (1, 2)
    assert tuple(":e1:" in conditional[0].event_id for _ in (0,)) == (True,)
    assert ":e2:" in conditional[1].event_id


def test_v3_joint_report_preserves_scope_and_no_canon(tmp_path) -> None:
    pytest.importorskip("ucns")
    source_root = os.environ.get("UCNS_SOURCE_ROOT")
    if source_root is None:
        pytest.skip("verified UCNS source checkout is not available")

    report = run_v3_experiments(
        edcm_commit="test-edcm-v3",
        ucns_commit=EXPECTED_UCNS_COMMIT,
        ucns_source_root=source_root,
    )
    assert report.canon_selection is None
    assert report.prior_v1_report_digest == PRIOR_V1_REPORT_DIGEST
    assert report.prior_v2_report_digest == PRIOR_V2_REPORT_DIGEST
    assert report.ucns_identity_verified
    assert report.edcm_commit == "test-edcm-v3"
    assert len(report.structural_signatures) == 14 * 3 * 5
    assert report.scope_events
    assert report.readouts
    assert report.relation_verdicts
    assert report.pair_findings
    assert all(
        verdict.status in {"supported", "falsified", "error"}
        for verdict in report.relation_verdicts
    )

    verdicts = {verdict.relation_id: verdict.status for verdict in report.relation_verdicts}
    for relation_id in (
        "negation-scope-active",
        "quote-scope-active",
        "hypothetical-scope-active",
        "ownership-scope-owned",
        "repair-order-scope",
        "retraction-scope-active",
        "refusal-negation-scope",
    ):
        assert verdicts[relation_id] == "supported"

    negation_lexical = next(
        finding
        for finding in report.pair_findings
        if finding.pair_id == "negation"
        and finding.view_name == "lexical-set"
        and finding.readout == "edcm.scope.asserted_constraint_events"
    )
    assert negation_lexical.structures_equivalent
    assert negation_lexical.status == "incompatible-for-readout"
    assert "scope" in negation_lexical.information_loss

    repair_multiset = next(
        finding
        for finding in report.pair_findings
        if finding.pair_id == "repair-order"
        and finding.view_name == "full-multiset"
        and finding.readout == "edcm.scope.final_active_pressure"
    )
    assert repair_multiset.structures_equivalent
    assert repair_multiset.status == "incompatible-for-readout"
    assert "order" in repair_multiset.information_loss

    output = tmp_path / "v0.3.json"
    assert main(
        [
            "--output",
            str(output),
            "--edcm-commit",
            "test-edcm-v3",
            "--ucns-source-root",
            source_root,
        ]
    ) == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["schema"].endswith("/0.3.0")
    assert payload["prior_v2_report_digest"] == PRIOR_V2_REPORT_DIGEST
    assert payload["canon_selection"] is None
    assert payload["report_digest"]


def test_v3_rejects_wrong_ucns_identity() -> None:
    pytest.importorskip("ucns")
    with pytest.raises(ValueError):
        run_v3_experiments(ucns_commit="wrong", ucns_source_root=Path("."))
