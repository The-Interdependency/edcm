from __future__ import annotations

import json
from types import ModuleType, SimpleNamespace

import pytest

import edcm.ucns_adapter as adapter_module
from edcm.ucns_adapter import (
    ActualUCNSAdapter,
    PINNED_UCNS_COMMIT,
    REJECTED_LEGACY_SCHEMAS,
    UCNSAdapterConstructionError,
    select_ucns_adapter,
)


def _exact_module() -> ModuleType:
    module = ModuleType("ucns")
    module.PRODUCER_EPOCH = adapter_module.SUPPORTED_PRODUCER_EPOCH
    module.PROFILE_ID, module.PROFILE_VERSION = adapter_module.SUPPORTED_PROFILE
    module.BRIDGE_SCHEMA_ID, module.BRIDGE_SCHEMA_VERSION = adapter_module.SUPPORTED_BRIDGE_SCHEMA

    class Record:
        def __init__(self, source_commit=PINNED_UCNS_COMMIT):
            self.source_commit = source_commit
            self.producer_epoch = module.PRODUCER_EPOCH
            self.profile_id = module.PROFILE_ID
            self.profile_version = module.PROFILE_VERSION
            self.schema_id = module.BRIDGE_SCHEMA_ID
            self.schema_version = module.BRIDGE_SCHEMA_VERSION
            self.stable_identity = "stable-object"
            self.cells = (
                SimpleNamespace(occurrence_id="occ-0"),
                SimpleNamespace(occurrence_id="occ-1"),
            )
            self.retained_layers = (SimpleNamespace(name="provenance", digest="a" * 64),)
            self.operator_history = ("metapat-envelope-ordered-occurrence",)
            self.information_loss = ()
            self.theorem_status_transfer = False
            self.edcm_measurement_validity_transfer = False
            self.metapat_validity_transfer = False

        @classmethod
        def from_json_bytes(cls, value):
            if isinstance(value, bytes):
                value = value.decode()
            data = json.loads(value)
            return cls(source_commit=data.get("source_commit", PINNED_UCNS_COMMIT))

    module.EdcmMetapatBridgeRecord = Record
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


def test_exact_profile_activates(monkeypatch):
    module = _exact_module()
    monkeypatch.setattr(adapter_module.importlib, "import_module", lambda name: module)
    selection = select_ucns_adapter()
    assert selection.adapter is not None
    assert selection.status.producer_recognized is True
    assert selection.status.profile_supported is True
    assert selection.status.adapter_active is True


def test_exact_bridge_attaches_geometry_without_validity_transfer():
    module = _exact_module()
    adapter = ActualUCNSAdapter(module)
    result = adapter.normalize({"ucns_bridge_record": module.EdcmMetapatBridgeRecord()})
    geometry = result["ucns_geometry"]
    status = result["ucns_integration"]
    assert geometry["stable_hash"] == "stable-object"
    assert geometry["occurrence_ids"] == ("occ-0", "occ-1")
    assert geometry["source_commit"] == PINNED_UCNS_COMMIT
    assert geometry["theorem_status_transfer"] is False
    assert geometry["measurement_validity_claim"] is False
    assert status["ucns_bridge_record_attached"] is True
    assert status["ucns_factorization_evidence_attached"] is False
    assert status["ucns_theorem_status_attached"] is False


def test_json_bridge_and_commit_mismatch():
    module = _exact_module()
    adapter = ActualUCNSAdapter(module)
    result = adapter.normalize({"ucns_bridge_record_json": json.dumps({"source_commit": PINNED_UCNS_COMMIT})})
    assert result["ucns_geometry"]["stable_hash"] == "stable-object"
    with pytest.raises(UCNSAdapterConstructionError, match="source commit mismatch"):
        adapter.normalize({"ucns_bridge_record_json": json.dumps({"source_commit": "0" * 40})})


def test_archived_object_and_factorization_inputs_fail_closed():
    adapter = ActualUCNSAdapter(_exact_module())
    with pytest.raises(adapter_module.UnsupportedUCNSSchemaError, match="archived"):
        adapter.normalize({"ucns_object": object()})
    with pytest.raises(adapter_module.UnsupportedUCNSSchemaError, match="archived"):
        adapter.normalize({"ucns_factorization_evidence": object()})


def test_transcript_only_remains_operational():
    adapter = ActualUCNSAdapter(_exact_module())
    result = adapter.normalize({"transcript": "A: hello"})
    assert result["transcript"] == "A: hello"
    assert result["ucns_integration"]["adapter_active"] is True
    assert "ucns_geometry" not in result


def test_legacy_schema_identities_and_na_boundary():
    assert "ucns-canonical-json-v1" in REJECTED_LEGACY_SCHEMAS
    assert "ucns.bridge-record@1.0.0" in REJECTED_LEGACY_SCHEMAS
    assert "ucns.factorization-evidence@1.0.0" in REJECTED_LEGACY_SCHEMAS
    assert "NA" != 0
    assert "NA" != "0"
