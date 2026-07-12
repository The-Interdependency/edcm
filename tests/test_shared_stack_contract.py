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
        lambda: MetapatAdapterSelection(
            adapter=None,
            status=missing_metapat_status(),
        ),
    )
    monkeypatch.setattr(
        layers_module,
        "select_ucns_adapter",
        lambda: UCNSAdapterSelection(
            adapter=None,
            status=missing_ucns_status(),
        ),
    )


def test_base_mode_is_explicit_and_na_is_not_zero(monkeypatch):
    _force_base_mode(monkeypatch)
    result = layers_module.build_default_layers().run({"input": "no transcript"})
    contract = result["edcm_result"]

    assert contract["source_evidence"]["state"] == "NA"
    assert contract["readouts"]["state"] == "NA"
    assert contract["readouts"]["structural_density"] is None
    assert contract["readouts"]["structural_density"] != 0
    assert contract["metapat_semantic_constraints"]["state"] == "NA"
    assert contract["ucns_geometry_identity"]["state"] == "NA"
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
    baseline = PolicyManifest()
    rotated = PolicyManifest(polarity_dictionary_version="v032")

    first = layers_module.build_default_layers(baseline).run({"transcript": TRANSCRIPT})
    second = layers_module.build_default_layers(rotated).run({"transcript": TRANSCRIPT})

    assert first["rounds"] == second["rounds"]
    assert first["edcm_result"]["source_evidence"] == second["edcm_result"]["source_evidence"]
    assert first["edcm_result"]["epoch_identity"] != second["edcm_result"]["epoch_identity"]
    assert (
        first["edcm_result"]["edcm_policy_manifest"]["manifest_hash"]
        != second["edcm_result"]["edcm_policy_manifest"]["manifest_hash"]
    )


def test_layer_provenance_has_distinct_semantic_geometry_and_measurement_records(monkeypatch):
    _force_base_mode(monkeypatch)
    result = layers_module.build_default_layers().run({"transcript": TRANSCRIPT})
    provenance = result["layer_provenance"]

    assert set(provenance) == {
        "semantic_authority",
        "geometry",
        "semantics",
        "measurement",
        "composition",
        "delivery",
    }
    assert provenance["measurement"]["canonical"] is True
    assert provenance["composition"]["canonical"] is True
    assert provenance["delivery"]["canonical"] is True
    assert provenance["semantic_authority"]["selection"] == "unavailable"
    assert provenance["geometry"]["selection"] == "local_fallback"


def test_full_stack_fixture_preserves_all_identity_boundaries():
    metapat = pytest.importorskip("metapat")
    ucns = pytest.importorskip("ucns")

    envelope = metapat.root_spine_module_envelope()
    adaptation = metapat.adapt_envelope_to_ucns(envelope)
    obj = adaptation.ucns_object
    result = layers_module.build_default_layers().run(
        {
            "transcript": TRANSCRIPT,
            "source_ref": "fixture://shared-stack/root-spine",
            "metapat_envelope": envelope,
            "ucns_object": obj,
        }
    )
    contract = result["edcm_result"]

    assert contract["schema_id"] == "edcm.shared-stack-result"
    assert contract["metapat_semantic_constraints"]["canon_digest"] == envelope.canon_digest
    assert (
        contract["metapat_semantic_constraints"]["provenance_digest"]
        == envelope.provenance_digest
    )
    assert contract["metapat_semantic_constraints"]["source_statements"] == envelope.source_statements
    assert contract["ucns_geometry_identity"]["stable_hash"] == ucns.stable_hash(obj)
    assert result["ucns_geometry"]["stable_hash"] == adaptation.record.ucns_object_hash
    assert contract["edcm_policy_manifest"]["manifest_hash"] == PolicyManifest().manifest_hash()
    assert contract["readouts"]["state"] == "measured"
    assert contract["status_evidence"]["proof_status_transfers_to_measurement_validity"] is False
    assert contract["status_evidence"]["semantic_labels_are_measurement_values"] is False
    assert contract["status_evidence"]["ucns_theorem_status_attached"] is False
    assert contract["status_evidence"]["metapat_theorem_status_attached"] is False


def test_ucns_equality_and_stable_hash_survive_integration_path():
    metapat = pytest.importorskip("metapat")
    ucns = pytest.importorskip("ucns")

    adaptation = metapat.root_spine_adaptation()
    obj = adaptation.ucns_object
    result = layers_module.build_default_layers().run({"ucns_object": obj})

    assert result["ucns_geometry"]["stable_hash"] == ucns.stable_hash(obj)
    assert result["edcm_result"]["ucns_geometry_identity"]["stable_hash"] == ucns.stable_hash(obj)
    assert obj == obj


def test_importable_siblings_without_evidence_do_not_claim_attachment():
    pytest.importorskip("metapat")
    pytest.importorskip("ucns")

    result = layers_module.build_default_layers().run({"transcript": TRANSCRIPT})
    assert result["metapat_integration"]["metapat_package_available"] is True
    assert result["metapat_integration"]["metapat_adapter_active"] is True
    assert result["metapat_integration"]["metapat_envelope_attached"] is False
    assert result["ucns_integration"]["ucns_package_available"] is True
    assert result["ucns_integration"]["ucns_adapter_active"] is True
    assert result["ucns_integration"]["ucns_object_attached"] is False
    assert result["edcm_result"]["metapat_semantic_constraints"]["state"] == "NA"
    assert result["edcm_result"]["ucns_geometry_identity"]["state"] == "NA"


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
    assert (
        first["edcm_result"]["metapat_semantic_constraints"]["canon_digest"]
        != second["edcm_result"]["metapat_semantic_constraints"]["canon_digest"]
    )


def test_malformed_serialized_metapat_envelope_fails_closed():
    metapat = pytest.importorskip("metapat")
    pytest.importorskip("ucns")
    envelope = metapat.root_spine_module_envelope().to_dict()
    envelope["unknown_field"] = "must fail"

    with pytest.raises(ValueError, match="unknown envelope fields"):
        layers_module.build_default_layers().run(
            {"metapat_envelope_dict": envelope, "transcript": TRANSCRIPT}
        )
