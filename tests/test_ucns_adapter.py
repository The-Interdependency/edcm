"""Contracts for the exact EDCM UCNS word-gonol profile consumer."""

from __future__ import annotations

# === CHECKS ===
# id: check_edcm_ucns_exact_profile_only
#   proves: edcm_ucns_exact_profile_only
#   call: self::test_exact_profile_activates_and_option_drift_suspends
#   mutates: none
#   cleanup: none
#
# id: check_edcm_ucns_full_turn_observation
#   proves: edcm_ucns_full_turn_observation
#   call: self::test_live_profile_preserves_full_turn_order_spaces_and_alphabet_failures
#   mutates: none
#   cleanup: none
#
# id: check_edcm_ucns_no_geometry_or_proof_transfer
#   proves: edcm_ucns_no_geometry_or_proof_transfer
#   call: self::test_live_profile_attaches_observation_without_geometry_or_proof_transfer
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import importlib.util
from types import ModuleType

import pytest

import edcm
import edcm.ucns_adapter as adapter_module
from edcm.ucns_adapter import (
    ActualUCNSAdapter,
    EXPECTED_PROFILE_OPTIONS,
    EXPECTED_PUBLIC_GONOL_SHA256,
    EXPECTED_SOURCE_DOMAIN,
    EXPECTED_SPACE_ASSIGNMENT_POLICY,
    EXPECTED_SPACE_CODE_POINT_LABELS,
    EXPECTED_SPACE_CODE_POINTS_SHA256,
    PINNED_UCNS_COMMIT,
    REJECTED_LEGACY_SCHEMAS,
    UCNSAdapterConstructionError,
    UnsupportedUCNSSchemaError,
    select_ucns_adapter,
)


def _exact_identity_module() -> ModuleType:
    module = ModuleType("ucns")
    module.EDCM_PROFILE_ID, module.EDCM_PROFILE_VERSION = (
        adapter_module.SUPPORTED_PROFILE
    )
    module.EDCM_PROFILE_SCOPE = adapter_module.SUPPORTED_PROFILE_SCOPE
    module.EDCM_PROFILE_OPTIONS = EXPECTED_PROFILE_OPTIONS
    module.EDCM_NORMALIZATION_POLICY = "none-preserve-source"
    module.EDCM_SUPPORT_POLICY = "one-unit-per-speaker-turn"
    module.EDCM_CORPUS_EXECUTION = "full-corpus"
    module.EDCM_SMALLEST_GONOL = "word"
    module.EDCM_GONOL_INITIATION = "mobius-twist"
    module.EDCM_SOURCE_DOMAIN = EXPECTED_SOURCE_DOMAIN
    module.EDCM_SPACE_ASSIGNMENT_POLICY = EXPECTED_SPACE_ASSIGNMENT_POLICY
    module.EDCM_SPACE_CODE_POINTS = tuple(
        chr(int(label[2:], 16)) for label in EXPECTED_SPACE_CODE_POINT_LABELS
    )
    module.PUBLIC_GONOL_157 = (" ", "0", *(chr(0x1000 + i) for i in range(155)))
    module.PUBLIC_GONOL_SHA256 = EXPECTED_PUBLIC_GONOL_SHA256
    module.public_gonol_sha256 = lambda: EXPECTED_PUBLIC_GONOL_SHA256

    class Profile:
        def observe_corpus(self, turns, *, source_id=None):
            raise AssertionError("identity-only fake must not observe a corpus")

    module.EdcmWordGonolProfile = Profile
    module.EdcmWordGonol = type("EdcmWordGonol", (), {})
    module.SuperpositionedSpaceBoundary = type(
        "SuperpositionedSpaceBoundary", (), {}
    )
    return module


def test_absent_package_is_typed_suspension(monkeypatch):
    real_import = adapter_module.importlib.import_module

    def missing(name):
        if name == "ucns":
            raise ModuleNotFoundError("No module named ucns", name="ucns")
        return real_import(name)

    monkeypatch.setattr(adapter_module.importlib, "import_module", missing)
    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.adapter_active is False
    assert selection.status.selection == "suspended"
    assert selection.status.ucns_profile_observation_attached is False


def test_pre_reset_metric_resolver_is_removed_from_public_surface():
    assert importlib.util.find_spec("edcm.ucns_metrics") is None
    for name in (
        "MetricDefinition",
        "ResolvedMetricUCNS",
        "UCNSMetricDependencyError",
        "UCNSMetricResolutionError",
        "METRIC_DEFINITIONS",
        "SYMBOL_TO_METRIC_ID",
        "resolve_metric_axis",
        "resolve_metric_value",
        "resolve_metric_vector",
        "resolve_round_metrics",
        "resolved_metric_objects_payload",
    ):
        assert not hasattr(edcm, name)


def test_archived_lookalike_cannot_activate(monkeypatch):
    fake = ModuleType("ucns")
    fake.UCNSObject = object
    monkeypatch.setattr(adapter_module.importlib, "import_module", lambda name: fake)
    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.package_present is True
    assert selection.status.producer_recognized is False
    with pytest.raises(UCNSAdapterConstructionError, match="surface missing"):
        ActualUCNSAdapter(fake)


def test_exact_profile_activates_and_option_drift_suspends(monkeypatch):
    module = _exact_identity_module()
    assert len(EXPECTED_PROFILE_OPTIONS) == 14
    assert ("source_domain", EXPECTED_SOURCE_DOMAIN) in EXPECTED_PROFILE_OPTIONS
    assert (
        "space_assignment",
        EXPECTED_SPACE_ASSIGNMENT_POLICY,
    ) in EXPECTED_PROFILE_OPTIONS
    monkeypatch.setattr(adapter_module.importlib, "import_module", lambda name: module)
    selection = select_ucns_adapter()
    assert selection.adapter is not None
    assert selection.status.producer_recognized is True
    assert selection.status.profile_supported is True
    assert selection.status.adapter_active is True

    module.EDCM_PROFILE_OPTIONS = (*EXPECTED_PROFILE_OPTIONS[:-1], ("z", "drift"))
    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.adapter_active is False
    assert "options mismatch" in selection.status.errors[0]

    module.EDCM_PROFILE_OPTIONS = EXPECTED_PROFILE_OPTIONS
    module.EDCM_SPACE_CODE_POINTS = (
        *module.EDCM_SPACE_CODE_POINTS[:-1],
        "\u3001",
    )
    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.adapter_active is False
    assert "code-point pin mismatch" in selection.status.errors[0]

    module.EDCM_SPACE_CODE_POINTS = tuple(
        chr(int(label[2:], 16)) for label in EXPECTED_SPACE_CODE_POINT_LABELS
    )
    module.EDCM_SOURCE_DOMAIN = "all-unicode-code-points"
    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.adapter_active is False
    assert "source domain mismatch" in selection.status.errors[0]


def test_retired_bridge_object_and_factorization_inputs_fail_closed():
    adapter = ActualUCNSAdapter(_exact_identity_module())
    for key in (
        "ucns_object",
        "ucns_bridge_record",
        "ucns_bridge_record_json",
        "ucns_bridge_record_dict",
        "ucns_factorization_evidence",
    ):
        with pytest.raises(UnsupportedUCNSSchemaError, match="retired"):
            adapter.normalize({key: object()})


def test_flat_transcript_does_not_invent_speaker_turn_boundaries():
    adapter = ActualUCNSAdapter(_exact_identity_module())
    result = adapter.normalize({"transcript": "A: hello\nB: there"})
    assert result["ucns_integration"]["adapter_active"] is True
    assert result["ucns_integration"]["ucns_profile_observation_attached"] is False
    assert "ucns_profile_observation" not in result


def test_live_profile_preserves_full_turn_order_spaces_and_alphabet_failures():
    ucns = pytest.importorskip("ucns")
    adapter = ActualUCNSAdapter(ucns)
    result = adapter.normalize(
        {
            "source_ref": "fixture://exact-turns",
            "ucns_turns": (
                ("A", "word\tgonol\n\u00a0"),
                ("B", "é"),
            ),
        }
    )
    evidence = result["ucns_profile_observation"]
    assert evidence["source_commit"] == PINNED_UCNS_COMMIT
    assert evidence["profile_id"] == "ucns.profile.edcm-word-gonol"
    assert evidence["token_alphabet_size"] == 157
    assert tuple(turn["speaker_id"] for turn in evidence["turns"]) == ("A", "B")
    first = evidence["turns"][0]
    assert first["raw_text"] == "word\tgonol\n\u00a0"
    assert first["unit_support"] == 1.0
    assert first["word_count"] == 2
    assert first["nesting_boundary_count"] == 3
    assert tuple(segment["kind"] for segment in first["segments"]) == (
        "word-gonol",
        "superpositioned-space-boundary",
        "word-gonol",
        "superpositioned-space-boundary",
        "superpositioned-space-boundary",
    )
    boundaries = tuple(
        segment["token"]
        for segment in first["segments"]
        if segment["kind"] == "superpositioned-space-boundary"
    )
    assert tuple(token["source_value"] for token in boundaries) == (
        "\t",
        "\n",
        "\u00a0",
    )
    assert all(token["carrier_token"] == " " for token in boundaries)
    assert all(token["carrier_position"] == 0 for token in boundaries)
    assert all(token["alphabet_position"] == 0 for token in boundaries)
    assert all(token["is_space_manifestation"] is True for token in boundaries)
    assert all(token["has_carrier_assignment"] is True for token in boundaries)
    assert all(token["in_alphabet"] is True for token in boundaries)
    assert all(
        token["is_public_gonol_token"] is False for token in boundaries
    )
    assert first["carrier_unassigned"] == ()
    assert first["out_of_alphabet"] == ()
    assert first["has_complete_carrier_assignment"] is True
    assert first["has_complete_alphabet_coverage"] is True
    assert evidence["source_domain"] == EXPECTED_SOURCE_DOMAIN
    assert evidence["space_assignment_policy"] == EXPECTED_SPACE_ASSIGNMENT_POLICY
    assert evidence["space_code_point_labels"] == EXPECTED_SPACE_CODE_POINT_LABELS
    assert (
        evidence["space_code_points_sha256"]
        == EXPECTED_SPACE_CODE_POINTS_SHA256
    )
    assert evidence["turns"][1]["carrier_unassigned"][0]["value"] == "é"
    assert evidence["turns"][1]["out_of_alphabet"][0]["value"] == "é"
    assert (
        evidence["turns"][1]["out_of_alphabet"][0]["source_value"]
        == "é"
    )
    assert (
        evidence["turns"][1]["out_of_alphabet"][0]["carrier_token"]
        is None
    )
    assert evidence["turns"][1]["has_complete_alphabet_coverage"] is False


def test_live_profile_attaches_observation_without_geometry_or_proof_transfer():
    ucns = pytest.importorskip("ucns")
    result = ActualUCNSAdapter(ucns).normalize(
        {"ucns_turns": (("A", "exact evidence"),)}
    )
    status = result["ucns_integration"]
    evidence = result["ucns_profile_observation"]
    assert status["ucns_profile_observation_attached"] is True
    assert status["ucns_bridge_record_attached"] is False
    assert status["ucns_factorization_evidence_attached"] is False
    assert status["ucns_theorem_status_attached"] is False
    assert evidence["evidence_mode"] == "exact-observation"
    assert evidence["projection_status"] == "not-projected"
    assert evidence["theorem_status_transfer"] is False
    assert evidence["measurement_validity_claim"] is False
    assert "ucns_geometry" not in result
    assert "ucns_factorization_evidence" not in result


def test_invalid_turn_container_fails_closed():
    ucns = pytest.importorskip("ucns")
    adapter = ActualUCNSAdapter(ucns)
    with pytest.raises(TypeError, match="ordered sequence"):
        adapter.normalize({"ucns_turns": iter((("A", "text"),))})
    with pytest.raises(TypeError, match="must be"):
        adapter.normalize({"ucns_turns": [["A", "text"]]})


def test_legacy_schema_identities_and_na_boundary():
    assert "ucns-canonical-json-v1" in REJECTED_LEGACY_SCHEMAS
    assert "ucns.bridge.edcm-metapat-ordered-occurrence" in REJECTED_LEGACY_SCHEMAS
    assert "NA" != 0
    assert "NA" != "0"
