from __future__ import annotations

import pytest

from edcm.ucns_adapter import ActualUCNSAdapter

ucns = pytest.importorskip("ucns")


def test_live_object_and_serialized_bridge_resolve_same_geometry_identity():
    obj = ucns.S2
    bridge = ucns.bridge_record(obj)
    adapter = ActualUCNSAdapter(ucns)

    live = adapter.normalize({"ucns_object": obj})
    serialized = adapter.normalize({"ucns_bridge_record_json": bridge.to_json()})

    assert live["ucns_geometry"] == serialized["ucns_geometry"]
    assert live["ucns_geometry"]["stable_hash"] == ucns.stable_hash(obj)
    assert live["ucns_geometry"]["bridge_evidence_digest"] == bridge.evidence_digest
    assert live["ucns_integration"]["ucns_object_attached"] is True
    assert serialized["ucns_integration"]["ucns_object_attached"] is False
    assert serialized["ucns_integration"]["ucns_bridge_record_attached"] is True


def test_producer_bridge_deserializer_rejects_unknown_and_tampered_fields():
    bridge = ucns.bridge_record(ucns.S2)
    unknown = bridge.to_dict()
    unknown["invented"] = True
    with pytest.raises(ValueError, match="unknown bridge record fields"):
        ActualUCNSAdapter(ucns).normalize({"ucns_bridge_record_dict": unknown})

    tampered = bridge.to_dict()
    tampered["canonical_json"] = tampered["canonical_json"] + " "
    with pytest.raises(ValueError):
        ActualUCNSAdapter(ucns).normalize({"ucns_bridge_record_dict": tampered})


def test_certified_negative_evidence_attaches_exact_search_and_coverage_record():
    obj = ucns.S2
    bridge = ucns.bridge_record(obj)
    evidence = ucns.factorization_evidence(obj)
    result = ActualUCNSAdapter(ucns).normalize(
        {
            "ucns_bridge_record": bridge,
            "ucns_factorization_evidence": evidence,
        }
    )

    status = result["ucns_integration"]
    attached = result["ucns_factorization_evidence"]
    assert status["ucns_factorization_evidence_attached"] is True
    assert status["ucns_negative_certification_attached"] is True
    assert status["ucns_theorem_status_attached"] is True
    assert attached["evidence_digest"] == evidence.evidence_digest
    assert attached["product_hash"] == bridge.object_hash
    assert attached["negative_result_certified"] is True
    assert attached["search_exhausted"] is True
    assert attached["truncation_occurred"] is False
    assert attached["coverage_record_validated"] is True
    assert attached["coverage_bound_to_search_report"] is True
    assert attached["pruning_preserves_coverage"] is True
    assert attached["uncertified_reasons"] == ()
    assert attached["theorem_status_transfer"] is False
    assert attached["measurement_validity_claim"] is False


def test_uncertified_evidence_is_attached_without_negative_certification():
    bridge = ucns.bridge_record(ucns.S2)
    evidence = ucns.factorization_evidence(ucns.S2, catalogue=[])
    result = ActualUCNSAdapter(ucns).normalize(
        {
            "ucns_bridge_record_json": bridge.to_json(),
            "ucns_factorization_evidence_json": evidence.to_json(),
        }
    )

    assert result["ucns_integration"]["ucns_factorization_evidence_attached"] is True
    assert result["ucns_integration"]["ucns_negative_certification_attached"] is False
    assert result["ucns_factorization_evidence"]["negative_result_certified"] is False
    assert result["ucns_factorization_evidence"]["uncertified_reasons"]


def test_unit_domain_evidence_never_becomes_prime_certification():
    bridge = ucns.bridge_record(ucns.UNIT)
    evidence = ucns.factorization_evidence(ucns.UNIT)
    result = ActualUCNSAdapter(ucns).normalize(
        {
            "ucns_bridge_record": bridge,
            "ucns_factorization_evidence": evidence,
        }
    )

    assert result["ucns_geometry"]["is_unit"] is True
    assert result["ucns_factorization_evidence"]["claim_scope"] == (
        "not-prime-unit-domain"
    )
    assert result["ucns_factorization_evidence"]["negative_result_certified"] is False
    assert result["ucns_integration"]["ucns_negative_certification_attached"] is False


def test_factorization_evidence_for_different_object_fails_binding():
    bridge = ucns.bridge_record(ucns.S2)
    other = ucns.factorization_evidence(ucns.UNIT)
    with pytest.raises(ValueError, match="product_hash does not match"):
        ActualUCNSAdapter(ucns).normalize(
            {
                "ucns_bridge_record": bridge,
                "ucns_factorization_evidence": other,
            }
        )


def test_package_availability_without_records_does_not_attach_status():
    result = ActualUCNSAdapter(ucns).normalize({"transcript": "A: evidence absent"})
    status = result["ucns_integration"]
    assert status["ucns_package_available"] is True
    assert status["ucns_adapter_active"] is True
    assert status["ucns_bridge_record_attached"] is False
    assert status["ucns_scope_metadata_attached"] is False
    assert status["ucns_factorization_evidence_attached"] is False
    assert status["ucns_negative_certification_attached"] is False
    assert status["ucns_theorem_status_attached"] is False
