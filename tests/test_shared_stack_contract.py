from __future__ import annotations

from dataclasses import replace

import pytest

import edcm.layers as layers_module
from edcm.edcmucns import PolicyManifest
from edcm.metapat_adapter import MetapatAdapterSelection, missing_metapat_status
from edcm.ucns_adapter import UCNSAdapterSelection, missing_ucns_status

TRANSCRIPT = "A: We must preserve exact source evidence.\nB: Agreed. Define the boundary."


def _force_base_mode(monkeypatch):
    monkeypatch.setattr(
        layers_module,
        "select_metapat_adapter",
        lambda: MetapatAdapterSelection(adapter=None, status=missing_metapat_status()),
    )
    monkeypatch.setattr(
        layers_module,
        "select_ucns_adapter",
        lambda: UCNSAdapterSelection(adapter=None, status=missing_ucns_status()),
    )


def test_base_mode_is_explicit_and_na_is_not_zero(monkeypatch):
    _force_base_mode(monkeypatch)
    result = layers_module.build_default_layers().run({"input": "no transcript"})
    contract = result["edcm_result"]
    assert contract["schema_version"] == "1.2.0"
    assert contract["source_evidence"]["state"] == "NA"
    assert contract["readouts"]["state"] == "NA"
    assert contract["readouts"]["structural_density"] is None
    assert contract["readouts"]["structural_density"] != 0
    assert contract["metapat_semantic_constraints"]["state"] == "NA"
    assert contract["ucns_profile_observation"]["state"] == "NA"
    assert contract["ucns_geometry_identity"]["state"] == "NA"
    assert contract["ucns_factorization_evidence"]["state"] == "NA"
    assert result["metapat_integration"]["metapat_package_available"] is False
    assert result["ucns_integration"]["ucns_package_available"] is False


def test_raw_transcript_measurement_is_deterministic(monkeypatch):
    _force_base_mode(monkeypatch)
    first = layers_module.build_default_layers().run({"transcript": TRANSCRIPT})
    second = layers_module.build_default_layers().run({"transcript": TRANSCRIPT})
    assert first["rounds"] == second["rounds"]
    assert first["agent_metrics"] == second["agent_metrics"]
    assert first["structural_density"] == second["structural_density"]
    assert first["edcm_result"]["result_identity"] == second["edcm_result"]["result_identity"]


def test_policy_manifest_rotation_changes_epoch_not_source_measurement(monkeypatch):
    _force_base_mode(monkeypatch)
    first = layers_module.build_default_layers(PolicyManifest()).run({"transcript": TRANSCRIPT})
    second = layers_module.build_default_layers(
        PolicyManifest(polarity_dictionary_version="v032")
    ).run({"transcript": TRANSCRIPT})
    assert first["rounds"] == second["rounds"]
    assert first["edcm_result"]["source_evidence"] == second["edcm_result"]["source_evidence"]
    assert first["edcm_result"]["epoch_identity"] != second["edcm_result"]["epoch_identity"]


def test_layer_provenance_has_distinct_semantic_profile_and_measurement_records(monkeypatch):
    _force_base_mode(monkeypatch)
    result = layers_module.build_default_layers().run({"transcript": TRANSCRIPT})
    provenance = result["layer_provenance"]
    assert set(provenance) == {
        "semantic_authority", "ucns_profile", "semantics", "measurement", "composition", "delivery"
    }
    assert provenance["measurement"]["canonical"] is True
    assert provenance["semantic_authority"]["selection"] == "unavailable"
    assert provenance["ucns_profile"]["selection"] == "unavailable"


def test_full_stack_fixture_uses_exact_profile_and_preserves_boundaries():
    metapat = pytest.importorskip("metapat")
    pytest.importorskip("ucns")
    envelope = metapat.root_spine_module_envelope()
    result = layers_module.build_default_layers().run(
        {
            "transcript": TRANSCRIPT,
            "source_ref": "fixture://shared-stack/root-spine",
            "metapat_envelope": envelope,
            "ucns_turns": (
                ("A", "We must preserve exact source evidence."),
                ("B", "Agreed. Define the boundary."),
            ),
        }
    )
    contract = result["edcm_result"]
    assert contract["schema_id"] == "edcm.shared-stack-result"
    assert contract["metapat_semantic_constraints"]["canon_digest"] == envelope.canon_digest
    assert contract["metapat_semantic_constraints"]["source_statements"] == envelope.source_statements
    observation = contract["ucns_profile_observation"]
    assert observation["profile_id"] == "ucns.profile.edcm-word-gonol"
    assert observation["source_commit"] == "eb264fba18bd051c46b4853c81c8fb91ec6d5811"
    assert observation["token_alphabet_size"] == 157
    assert tuple(turn["speaker_id"] for turn in observation["turns"]) == ("A", "B")
    assert result["layer_provenance"]["ucns_profile"]["canonical"] is False
    assert contract["ucns_geometry_identity"]["state"] == "NA"
    assert contract["ucns_factorization_evidence"]["state"] == "NA"
    assert contract["readouts"]["state"] == "measured"
    status = contract["status_evidence"]
    assert status["ucns_profile_observation_attached"] is True
    assert status["ucns_bridge_record_attached"] is False
    assert status["ucns_factorization_evidence_attached"] is False
    assert status["ucns_theorem_status_attached"] is False
    assert status["proof_status_transfers_to_measurement_validity"] is False


def test_profile_observation_identity_is_deterministic_through_integration_path():
    pytest.importorskip("ucns")
    payload = {"ucns_turns": (("A", "word  gonol"), ("B", "é"))}
    first = layers_module.build_default_layers().run(
        payload
    )
    second = layers_module.build_default_layers().run(
        payload
    )
    assert first["ucns_profile_observation"] == second["ucns_profile_observation"]
    assert first["edcm_result"]["epoch_identity"] == second["edcm_result"]["epoch_identity"]
    assert first["edcm_result"]["result_identity"] == second["edcm_result"]["result_identity"]


def test_archived_object_and_factorization_inputs_are_rejected():
    pytest.importorskip("ucns")
    with pytest.raises(Exception, match="retired"):
        layers_module.build_default_layers().run({"ucns_object": object()})
    with pytest.raises(Exception, match="retired"):
        layers_module.build_default_layers().run({"ucns_factorization_evidence": object()})


def test_importable_siblings_without_evidence_do_not_claim_attachment():
    pytest.importorskip("metapat")
    pytest.importorskip("ucns")
    result = layers_module.build_default_layers().run({"transcript": TRANSCRIPT})
    assert result["metapat_integration"]["metapat_package_available"] is True
    assert result["metapat_integration"]["metapat_adapter_active"] is True
    assert result["metapat_integration"]["metapat_envelope_attached"] is False
    assert result["ucns_integration"]["ucns_package_available"] is True
    assert result["ucns_integration"]["ucns_adapter_active"] is True
    assert result["ucns_integration"]["ucns_profile_observation_attached"] is False
    assert result["ucns_integration"]["ucns_bridge_record_attached"] is False
    assert result["ucns_integration"]["ucns_factorization_evidence_attached"] is False
    assert result["ucns_integration"]["ucns_theorem_status_attached"] is False
    assert result["edcm_result"]["ucns_geometry_identity"]["state"] == "NA"
    assert result["edcm_result"]["ucns_profile_observation"]["state"] == "NA"


def test_canon_rotation_creates_new_epoch_identity():
    metapat = pytest.importorskip("metapat")
    pytest.importorskip("ucns")
    envelope = metapat.root_spine_module_envelope()
    rotated = replace(envelope, canon_digest="c" * 64, provenance_digest="")
    first = layers_module.build_default_layers().run(
        {"metapat_envelope": envelope, "transcript": TRANSCRIPT}
    )
    second = layers_module.build_default_layers().run(
        {"metapat_envelope": rotated, "transcript": TRANSCRIPT}
    )
    assert first["rounds"] == second["rounds"]
    assert first["edcm_result"]["epoch_identity"] != second["edcm_result"]["epoch_identity"]


def test_malformed_serialized_metapat_envelope_fails_closed():
    metapat = pytest.importorskip("metapat")
    envelope = metapat.root_spine_module_envelope().to_dict()
    envelope["unknown_field"] = "must fail"
    with pytest.raises(ValueError, match="unknown envelope fields"):
        layers_module.build_default_layers().run(
            {"metapat_envelope_dict": envelope, "transcript": TRANSCRIPT}
        )
