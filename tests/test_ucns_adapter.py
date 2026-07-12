from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from types import ModuleType, SimpleNamespace

import pytest

import edcm.layers as layers_module
import edcm.ucns_adapter as adapter_module
from edcm.layers import ConsolidatedMeasurementLayer
from edcm.metapat_adapter import MetapatAdapterSelection, missing_metapat_status
from edcm.ucns_adapter import (
    ActualUCNSAdapter,
    UCNSAdapterConstructionError,
    UCNSAdapterSelection,
    UnsupportedUCNSSchemaError,
    missing_ucns_status,
    select_ucns_adapter,
)


def _fake_ucns(*, schema: str = "ucns-canonical-json-v1") -> tuple[ModuleType, type]:
    module = ModuleType("ucns")

    class UCNSObject:
        pass

    @dataclass(frozen=True)
    class DomainMetadata:
        statuses: tuple[object, ...] = (SimpleNamespace(value="DEFENDED"),)
        completeness_guaranteed: bool = True
        seq_prime_claim_scope: str = "defended-domain-relative"

    @dataclass(frozen=True)
    class Record:
        object_hash: str = "abc123"
        domain_label: str = "depth-1"
        domain_metadata: DomainMetadata = DomainMetadata()
        depth: int = 1
        n_min: int = 1
        length: int = 1
        canonical_json: str = '{"kind":"object","version":"ucns-canonical-json-v1"}'

    module.UCNSObject = UCNSObject
    module.CANONICAL_SERIALIZATION_VERSION = schema
    module.stable_hash = lambda obj: "abc123"
    module.object_record = lambda obj: Record()
    module.__version__ = "0.test"
    return module, UCNSObject


def _force_missing_metapat(monkeypatch):
    monkeypatch.setattr(
        layers_module,
        "select_metapat_adapter",
        lambda: MetapatAdapterSelection(
            adapter=None,
            status=missing_metapat_status(),
        ),
    )


def test_direct_ucns_absence_is_typed_unavailable(monkeypatch):
    def missing(name: str):
        raise ModuleNotFoundError("No module named 'ucns'", name="ucns")

    monkeypatch.setattr(adapter_module.importlib, "import_module", missing)
    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.ucns_package_available is False
    assert selection.status.ucns_adapter_active is False
    assert selection.status.selection == "unavailable"


def test_transitive_import_failure_is_not_silently_fallback(monkeypatch):
    def broken(name: str):
        raise ModuleNotFoundError("No module named 'ucns_helper'", name="ucns_helper")

    monkeypatch.setattr(adapter_module.importlib, "import_module", broken)
    with pytest.raises(ModuleNotFoundError, match="ucns_helper"):
        select_ucns_adapter()


def test_importable_malformed_ucns_fails_adapter_construction():
    module, _ = _fake_ucns()
    del module.object_record
    with pytest.raises(UCNSAdapterConstructionError, match="object_record"):
        ActualUCNSAdapter(module)


def test_unsupported_ucns_schema_fails_closed():
    module, _ = _fake_ucns(schema="ucns-canonical-json-v99")
    with pytest.raises(UnsupportedUCNSSchemaError, match="v99"):
        ActualUCNSAdapter(module)


def test_package_and_adapter_do_not_imply_object_or_scope_attachment():
    module, _ = _fake_ucns()
    result = ActualUCNSAdapter(module).normalize({"transcript": "A: hello"})
    status = result["ucns_integration"]
    assert status["ucns_package_available"] is True
    assert status["ucns_adapter_active"] is True
    assert status["ucns_object_attached"] is False
    assert status["ucns_scope_metadata_attached"] is False
    assert status["ucns_negative_certification_attached"] is False
    assert status["ucns_theorem_status_attached"] is False
    assert "ucns_geometry" not in result


def test_actual_ucns_object_attaches_stable_geometry_evidence_only():
    module, object_type = _fake_ucns()
    result = ActualUCNSAdapter(module).normalize({"ucns_object": object_type()})
    status = result["ucns_integration"]
    geometry = result["ucns_geometry"]

    assert status["ucns_object_attached"] is True
    assert status["ucns_scope_metadata_attached"] is True
    assert status["ucns_negative_certification_attached"] is False
    assert status["ucns_theorem_status_attached"] is False
    assert geometry["stable_hash"] == "abc123"
    assert geometry["ucns_serialization_version"] == "ucns-canonical-json-v1"
    assert geometry["domain_statuses"] == ("DEFENDED",)
    assert geometry["theorem_status_transfer"] is False
    assert geometry["measurement_validity_claim"] is False


def test_wrong_object_type_fails_closed():
    module, _ = _fake_ucns()
    with pytest.raises(TypeError, match="actual ucns.UCNSObject"):
        ActualUCNSAdapter(module).normalize({"ucns_object": object()})


def test_transcript_only_pipeline_is_explicit(monkeypatch):
    _force_missing_metapat(monkeypatch)
    status = missing_ucns_status()
    monkeypatch.setattr(
        layers_module,
        "select_ucns_adapter",
        lambda: UCNSAdapterSelection(adapter=None, status=status),
    )
    result = layers_module.build_default_layers().run({"input": "example"})

    assert result["semantics"] == {
        "semantic_authority": "unavailable",
        "geometry": "edcm.transcript_only",
    }
    assert result["ucns_integration"]["selection"] == "unavailable"
    assert result["measurement"] == "edcm.measurement"
    assert result["layer_provenance"]["geometry"]["selection"] == "local_fallback"
    assert result["layer_provenance"]["semantic_authority"]["selection"] == "unavailable"
    assert result["layer_provenance"]["measurement"]["canonical"] is True
    assert set(result["layer_provenance"]) == {
        "semantic_authority",
        "geometry",
        "semantics",
        "measurement",
        "composition",
        "delivery",
    }
    assert result["edcm_result"]["ucns_geometry_identity"]["state"] == "NA"


def test_installed_edcmbone_cannot_override_canonical_edcm_measurement(monkeypatch):
    _force_missing_metapat(monkeypatch)
    status = missing_ucns_status()
    monkeypatch.setattr(
        layers_module,
        "select_ucns_adapter",
        lambda: UCNSAdapterSelection(adapter=None, status=status),
    )
    monkeypatch.setitem(__import__("sys").modules, "edcmbone", ModuleType("edcmbone"))
    assert isinstance(layers_module.build_default_layers().measurement, ConsolidatedMeasurementLayer)


def test_live_ucns_package_roundtrip_when_integration_is_installed():
    ucns = pytest.importorskip("ucns")
    obj = ucns.UCNSObject(1, 1, [(Fraction(0), None)], [0])
    result = ActualUCNSAdapter(ucns).normalize({"ucns_object": obj})

    assert result["ucns_geometry"]["stable_hash"] == ucns.stable_hash(obj)
    assert result["ucns_geometry"]["ucns_serialization_version"] == (
        ucns.CANONICAL_SERIALIZATION_VERSION
    )
    assert result["ucns_integration"]["ucns_object_attached"] is True
    assert result["ucns_integration"]["ucns_theorem_status_attached"] is False
