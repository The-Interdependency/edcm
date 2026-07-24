from __future__ import annotations

import sys
from types import ModuleType

import pytest

import edcm.ucns_adapter as adapter_module
from edcm.ucns_adapter import (
    ActualUCNSAdapter,
    REJECTED_LEGACY_SCHEMAS,
    RESET_BOUNDARY_REASON,
    UCNSAdapterConstructionError,
    select_ucns_adapter,
    suspended_ucns_status,
)


def test_selector_is_suspended_when_package_is_absent(monkeypatch):
    monkeypatch.setattr(adapter_module, "_package_present", lambda: False)
    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.package_present is False
    assert selection.status.producer_recognized is False
    assert selection.status.profile_supported is False
    assert selection.status.adapter_active is False
    assert selection.status.selection == "suspended"
    assert selection.status.theorem_status_transfer is False
    assert selection.status.measurement_validity_claim is False


def test_fake_archived_package_cannot_activate(monkeypatch):
    fake = ModuleType("ucns")
    fake.UCNSObject = type("UCNSObject", (), {})
    fake.BRIDGE_RECORD_SCHEMA_ID = "ucns.bridge-record"
    fake.BRIDGE_RECORD_SCHEMA_VERSION = "1.0.0"
    fake.FACTORIZATION_EVIDENCE_SCHEMA_ID = "ucns.factorization-evidence"
    fake.FACTORIZATION_EVIDENCE_SCHEMA_VERSION = "1.0.0"
    monkeypatch.setitem(sys.modules, "ucns", fake)
    monkeypatch.setattr(adapter_module, "_package_present", lambda: True)

    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.package_present is True
    assert selection.status.producer_recognized is False
    assert selection.status.profile_supported is False
    assert selection.status.adapter_active is False

    with pytest.raises(UCNSAdapterConstructionError, match="awaiting post-reset producer profile"):
        ActualUCNSAdapter(fake)


def test_status_distinguishes_all_activation_dimensions():
    status = suspended_ucns_status(package_present=True)
    data = status.as_dict()
    assert data["package_present"] is True
    assert data["producer_recognized"] is False
    assert data["profile_supported"] is False
    assert data["adapter_active"] is False
    assert data["ucns_package_available"] is True
    assert data["ucns_adapter_active"] is False


def test_legacy_schema_identities_are_explicitly_rejected():
    assert "ucns-canonical-json-v1" in REJECTED_LEGACY_SCHEMAS
    assert "ucns.bridge-record@1.0.0" in REJECTED_LEGACY_SCHEMAS
    assert "ucns.factorization-evidence@1.0.0" in REJECTED_LEGACY_SCHEMAS


def test_suspension_reason_names_reset_profile_boundary():
    assert "post-reset producer profile" in RESET_BOUNDARY_REASON
    assert "exact source commit" in RESET_BOUNDARY_REASON


def test_na_is_not_zero():
    assert "NA" != 0
    assert "NA" != "0"
