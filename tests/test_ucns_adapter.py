from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from types import ModuleType

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

HASH_A = "a" * 64
HASH_B = "b" * 64


def _fake_ucns(
    *,
    serialization: str = "ucns-canonical-json-v1",
    bridge_version: str = "1.0.0",
    factor_version: str = "1.0.0",
) -> tuple[ModuleType, type, type, type]:
    module = ModuleType("ucns")

    class UCNSObject:
        pass

    @dataclass(frozen=True)
    class UCNSBridgeRecord:
        schema_id: str = "ucns.bridge-record"
        schema_version: str = bridge_version
        producer_id: str = "ucns.object_record"
        evidence_digest: str = "c" * 64
        ucns_serialization_version: str = serialization
        object_hash: str = HASH_A
        domain_label: str = "depth-1"
        domain_statuses: tuple[str, ...] = ("DEFENDED", "TEST_BACKED")
        completeness_guaranteed: bool = True
        seq_prime_claim_scope: str = "defended-domain-relative"
        depth: int = 1
        n_min: int = 1
        length: int = 1
        is_unit: bool = False
        is_verified_domain: bool = True
        is_frontier: bool = False
        note: str = "typed domain prerequisite evidence"
        canonical_json: str = '{"kind":"object","version":"ucns-canonical-json-v1"}'

        def to_dict(self):
            return {
                name: getattr(self, name)
                for name in self.__dataclass_fields__
            }

        @classmethod
        def from_dict(cls, data):
            return cls(**dict(data))

        @classmethod
        def from_json(cls, value):
            return cls.from_dict(json.loads(value))

    @dataclass(frozen=True)
    class UCNSFactorizationEvidence:
        schema_id: str = "ucns.factorization-evidence"
        schema_version: str = factor_version
        producer_id: str = "ucns.factorization_result"
        evidence_digest: str = "d" * 64
        product_hash: str = HASH_A
        product_domain_label: str = "depth-1"
        product_domain_statuses: tuple[str, ...] = ("DEFENDED", "TEST_BACKED")
        completeness_guaranteed: bool = True
        result_kind: str = "SEQ_PRIME"
        factor_hashes: tuple[str, ...] = ()
        negative_result_certified: bool = True
        seq_prime_is_absolute: bool = True
        claim_scope: str = "absolute-certified-negative"
        note: str = "authoritative negative evidence"
        certification_policy_version: str = "ucns-negative-certification-v2"
        search_exhausted: bool = True
        truncation_occurred: bool = False
        catalogue_source: str = "canonical-generated"
        supplied_catalogue_size: int = 2
        supplied_catalogue_fingerprint: str = "e" * 64
        effective_catalogue_size: int = 2
        effective_catalogue_fingerprint: str = "e" * 64
        catalogue_coverage_status: str = "canonical-exact"
        catalogue_coverage_reason: str = "validated"
        catalogue_coverage_rule_version: str = "coverage-v1"
        required_catalogue_rule_version: str = "catalogue-v1"
        required_catalogue_fingerprint: str = "f" * 64
        coverage_record_validated: bool = True
        coverage_bound_to_search_report: bool = True
        pruning_applied: bool = True
        pruning_rule: str = "carrier-support"
        pruning_rule_version: str = "pruning-v1"
        pruning_preserves_coverage: bool = True
        uncertified_reasons: tuple[str, ...] = ()

        def to_dict(self):
            return {
                name: getattr(self, name)
                for name in self.__dataclass_fields__
            }

        @classmethod
        def from_dict(cls, data):
            return cls(**dict(data))

        @classmethod
        def from_json(cls, value):
            return cls.from_dict(json.loads(value))

    module.UCNSObject = UCNSObject
    module.UCNSBridgeRecord = UCNSBridgeRecord
    module.UCNSFactorizationEvidence = UCNSFactorizationEvidence
    module.CANONICAL_SERIALIZATION_VERSION = serialization
    module.BRIDGE_RECORD_SCHEMA_ID = "ucns.bridge-record"
    module.BRIDGE_RECORD_SCHEMA_VERSION = bridge_version
    module.FACTORIZATION_EVIDENCE_SCHEMA_ID = "ucns.factorization-evidence"
    module.FACTORIZATION_EVIDENCE_SCHEMA_VERSION = factor_version
    module.bridge_record = lambda obj: UCNSBridgeRecord()
    module.__version__ = "0.test"
    return module, UCNSObject, UCNSBridgeRecord, UCNSFactorizationEvidence


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
    assert selection.status.ucns_bridge_record_attached is False
    assert selection.status.ucns_factorization_evidence_attached is False
    assert selection.status.selection == "unavailable"


def test_transitive_import_failure_is_not_silently_fallback(monkeypatch):
    def broken(name: str):
        raise ModuleNotFoundError("No module named 'ucns_helper'", name="ucns_helper")

    monkeypatch.setattr(adapter_module.importlib, "import_module", broken)
    with pytest.raises(ModuleNotFoundError, match="ucns_helper"):
        select_ucns_adapter()


def test_importable_malformed_ucns_fails_adapter_construction():
    module, _, _, _ = _fake_ucns()
    del module.UCNSBridgeRecord
    with pytest.raises(UCNSAdapterConstructionError, match="UCNSBridgeRecord"):
        ActualUCNSAdapter(module)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"serialization": "ucns-canonical-json-v99"}, "v99"),
        ({"bridge_version": "99.0.0"}, "bridge schema"),
        ({"factor_version": "99.0.0"}, "factorization evidence schema"),
    ],
)
def test_unsupported_ucns_schemas_fail_closed(kwargs, message):
    module, _, _, _ = _fake_ucns(**kwargs)
    with pytest.raises(UnsupportedUCNSSchemaError, match=message):
        ActualUCNSAdapter(module)


def test_package_and_adapter_do_not_imply_any_attachment():
    module, _, _, _ = _fake_ucns()
    result = ActualUCNSAdapter(module).normalize({"transcript": "A: hello"})
    status = result["ucns_integration"]
    assert status["ucns_package_available"] is True
    assert status["ucns_adapter_active"] is True
    assert status["ucns_object_attached"] is False
    assert status["ucns_bridge_record_attached"] is False
    assert status["ucns_scope_metadata_attached"] is False
    assert status["ucns_factorization_evidence_attached"] is False
    assert status["ucns_negative_certification_attached"] is False
    assert status["ucns_theorem_status_attached"] is False
    assert "ucns_geometry" not in result
    assert "ucns_factorization_evidence" not in result


def test_live_ucns_object_is_converted_through_canonical_bridge_record():
    module, object_type, _, _ = _fake_ucns()
    result = ActualUCNSAdapter(module).normalize({"ucns_object": object_type()})
    status = result["ucns_integration"]
    geometry = result["ucns_geometry"]

    assert status["ucns_object_attached"] is True
    assert status["ucns_bridge_record_attached"] is True
    assert status["ucns_scope_metadata_attached"] is True
    assert status["ucns_theorem_status_attached"] is True
    assert status["ucns_negative_certification_attached"] is False
    assert geometry["stable_hash"] == HASH_A
    assert geometry["bridge_schema_id"] == "ucns.bridge-record"
    assert geometry["bridge_evidence_digest"] == "c" * 64
    assert geometry["domain_statuses"] == ("DEFENDED", "TEST_BACKED")
    assert geometry["theorem_status_transfer"] is False
    assert geometry["measurement_validity_claim"] is False


@pytest.mark.parametrize(
    "key",
    [
        "ucns_bridge_record",
        "ucns_bridge_record_json",
        "ucns_bridge_record_dict",
    ],
)
def test_bridge_record_object_json_and_mapping_are_accepted(key):
    module, _, record_type, _ = _fake_ucns()
    record = record_type()
    if key.endswith("_json"):
        value = json.dumps(record.to_dict())
    elif key.endswith("_dict"):
        value = record.to_dict()
    else:
        value = record
    result = ActualUCNSAdapter(module).normalize({key: value})

    assert result["ucns_geometry"]["stable_hash"] == HASH_A
    assert result["ucns_integration"]["ucns_object_attached"] is False
    assert result["ucns_integration"]["ucns_bridge_record_attached"] is True
    assert result["ucns_integration"]["ucns_theorem_status_attached"] is True


def test_multiple_geometry_forms_fail_closed():
    module, object_type, record_type, _ = _fake_ucns()
    with pytest.raises(ValueError, match="exactly one UCNS geometry"):
        ActualUCNSAdapter(module).normalize(
            {
                "ucns_object": object_type(),
                "ucns_bridge_record": record_type(),
            }
        )


def test_wrong_geometry_types_fail_closed():
    module, _, _, _ = _fake_ucns()
    with pytest.raises(TypeError, match="actual ucns.UCNSObject"):
        ActualUCNSAdapter(module).normalize({"ucns_object": object()})
    with pytest.raises(TypeError, match="actual ucns.UCNSBridgeRecord"):
        ActualUCNSAdapter(module).normalize({"ucns_bridge_record": object()})


def test_factorization_evidence_requires_matching_geometry():
    module, _, record_type, factor_type = _fake_ucns()
    adapter = ActualUCNSAdapter(module)

    with pytest.raises(ValueError, match="requires an attached geometry"):
        adapter.normalize({"ucns_factorization_evidence": factor_type()})

    mismatch = factor_type(product_hash=HASH_B)
    with pytest.raises(ValueError, match="product_hash does not match"):
        adapter.normalize(
            {
                "ucns_bridge_record": record_type(),
                "ucns_factorization_evidence": mismatch,
            }
        )


@pytest.mark.parametrize(
    "key",
    [
        "ucns_factorization_evidence",
        "ucns_factorization_evidence_json",
        "ucns_factorization_evidence_dict",
    ],
)
def test_certified_factorization_evidence_forms_attach_exact_record(key):
    module, _, record_type, factor_type = _fake_ucns()
    factor = factor_type()
    if key.endswith("_json"):
        value = json.dumps(factor.to_dict())
    elif key.endswith("_dict"):
        value = factor.to_dict()
    else:
        value = factor
    result = ActualUCNSAdapter(module).normalize(
        {"ucns_bridge_record": record_type(), key: value}
    )

    status = result["ucns_integration"]
    evidence = result["ucns_factorization_evidence"]
    assert status["ucns_factorization_evidence_attached"] is True
    assert status["ucns_negative_certification_attached"] is True
    assert status["ucns_theorem_status_attached"] is True
    assert evidence["product_hash"] == HASH_A
    assert evidence["negative_result_certified"] is True
    assert evidence["search_exhausted"] is True
    assert evidence["coverage_record_validated"] is True
    assert evidence["theorem_status_transfer"] is False
    assert evidence["measurement_validity_claim"] is False


def test_uncertified_factorization_evidence_attaches_without_certification_claim():
    module, _, record_type, factor_type = _fake_ucns()
    factor = factor_type(
        negative_result_certified=False,
        seq_prime_is_absolute=False,
        claim_scope="domain-relative-uncertified",
        uncertified_reasons=("catalogue-coverage-uncertified",),
    )
    result = ActualUCNSAdapter(module).normalize(
        {
            "ucns_bridge_record": record_type(),
            "ucns_factorization_evidence": factor,
        }
    )

    status = result["ucns_integration"]
    assert status["ucns_factorization_evidence_attached"] is True
    assert status["ucns_negative_certification_attached"] is False
    assert result["ucns_factorization_evidence"]["uncertified_reasons"] == (
        "catalogue-coverage-uncertified",
    )


def test_multiple_factorization_forms_fail_closed():
    module, _, record_type, factor_type = _fake_ucns()
    factor = factor_type()
    with pytest.raises(ValueError, match="exactly one UCNS factorization evidence"):
        ActualUCNSAdapter(module).normalize(
            {
                "ucns_bridge_record": record_type(),
                "ucns_factorization_evidence": factor,
                "ucns_factorization_evidence_dict": factor.to_dict(),
            }
        )


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
    assert result["edcm_result"]["ucns_geometry_identity"]["state"] == "NA"
    assert result["edcm_result"]["ucns_factorization_evidence"]["state"] == "NA"


def test_installed_edcmbone_cannot_override_canonical_edcm_measurement(monkeypatch):
    _force_missing_metapat(monkeypatch)
    status = missing_ucns_status()
    monkeypatch.setattr(
        layers_module,
        "select_ucns_adapter",
        lambda: UCNSAdapterSelection(adapter=None, status=status),
    )
    monkeypatch.setitem(__import__("sys").modules, "edcmbone", ModuleType("edcmbone"))
    assert isinstance(
        layers_module.build_default_layers().measurement,
        ConsolidatedMeasurementLayer,
    )


def test_live_ucns_package_bridge_and_certification_roundtrip():
    ucns = pytest.importorskip("ucns")
    obj = ucns.S2
    bridge = ucns.bridge_record(obj)
    factorization = ucns.factorization_evidence(obj)
    result = ActualUCNSAdapter(ucns).normalize(
        {
            "ucns_bridge_record_json": bridge.to_json(),
            "ucns_factorization_evidence_json": factorization.to_json(),
        }
    )

    assert result["ucns_geometry"]["stable_hash"] == ucns.stable_hash(obj)
    assert result["ucns_geometry"]["bridge_evidence_digest"] == bridge.evidence_digest
    assert result["ucns_integration"]["ucns_object_attached"] is False
    assert result["ucns_integration"]["ucns_bridge_record_attached"] is True
    assert result["ucns_integration"]["ucns_factorization_evidence_attached"] is True
    assert result["ucns_integration"]["ucns_negative_certification_attached"] is True
    assert result["ucns_integration"]["ucns_theorem_status_attached"] is True
    assert result["ucns_factorization_evidence"]["evidence_digest"] == (
        factorization.evidence_digest
    )
