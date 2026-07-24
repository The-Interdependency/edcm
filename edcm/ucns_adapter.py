"""Exact-profile EDCM consumer for the post-reset UCNS ordered-occurrence bridge.

UCNS is a stable identifier without a canonical expansion. Package presence alone
never establishes authority, and archived object/factorization surfaces are rejected.
"""
from __future__ import annotations

import importlib
import importlib.util
from dataclasses import asdict, dataclass, replace
from types import ModuleType
from typing import Any, Mapping, Protocol

UCNS_SOURCE_REPOSITORY = "https://github.com/The-Interdependency/ucns"
SUPPORTED_PRODUCER_EPOCH = "ucns.post-reset.v1"
SUPPORTED_PROFILE = ("ucns.profile.edcm-metapat-ordered-occurrence", "1.0.0")
SUPPORTED_BRIDGE_SCHEMA = ("ucns.bridge.edcm-metapat-ordered-occurrence", "1.0.0")
PINNED_UCNS_COMMIT = "19f1afddb993f7d933ac8727627e7d5e1c3b88fc"
RESET_BOUNDARY_REASON = "exact post-reset UCNS producer profile is unavailable or mismatched"
INSTALL_HINT = None
SUPPORTED_SERIALIZATION_VERSIONS = frozenset()
SUPPORTED_BRIDGE_SCHEMAS = frozenset({SUPPORTED_BRIDGE_SCHEMA})
SUPPORTED_FACTORIZATION_EVIDENCE_SCHEMAS = frozenset()
REJECTED_LEGACY_SCHEMAS = frozenset({
    "ucns-canonical-json-v1",
    "ucns.bridge-record@1.0.0",
    "ucns.factorization-evidence@1.0.0",
})


class UCNSAdapterConstructionError(RuntimeError):
    """Raised when UCNS fails the exact post-reset consumer contract."""


class UnsupportedUCNSSchemaError(UCNSAdapterConstructionError):
    """Raised for pre-reset or otherwise unsupported producer identities."""


@dataclass(frozen=True)
class UCNSIntegrationStatus:
    package_present: bool
    producer_recognized: bool
    profile_supported: bool
    adapter_active: bool
    ucns_object_attached: bool = False
    ucns_bridge_record_attached: bool = False
    ucns_scope_metadata_attached: bool = False
    ucns_factorization_evidence_attached: bool = False
    ucns_negative_certification_attached: bool = False
    ucns_theorem_status_attached: bool = False
    implementation_id: str = "edcm.ucns_adapter.post_reset"
    implementation_version: str | None = "1.0.0"
    source_repository: str = UCNS_SOURCE_REPOSITORY
    selection: str = "suspended"
    unresolved_constraints: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False
    metapat_validity_claim: bool = False

    @property
    def ucns_package_available(self) -> bool:
        return self.package_present

    @property
    def ucns_adapter_active(self) -> bool:
        return self.adapter_active

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["ucns_package_available"] = self.package_present
        data["ucns_adapter_active"] = self.adapter_active
        return data


@dataclass(frozen=True)
class UCNSGeometryEvidence:
    stable_hash: str
    producer_epoch: str
    profile_id: str
    profile_version: str
    bridge_schema_id: str
    bridge_schema_version: str
    source_commit: str
    occurrence_ids: tuple[str, ...]
    retained_layers: tuple[tuple[str, str], ...]
    operator_history: tuple[str, ...]
    information_loss: tuple[tuple[str, tuple[str, ...]], ...]
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False
    metapat_validity_claim: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class UCNSFactorizationEvidenceRecord:
    product_hash: str
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False


class UCNSAdapter(Protocol):
    @property
    def status(self) -> UCNSIntegrationStatus: ...
    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]: ...


class SuspendedUCNSAdapter:
    def __init__(self, *, package_present: bool) -> None:
        self._status = suspended_ucns_status(package_present=package_present)

    @property
    def status(self) -> UCNSIntegrationStatus:
        return self._status

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        state["ucns_integration"] = self.status.as_dict()
        state.pop("ucns_geometry", None)
        state.pop("ucns_factorization_evidence", None)
        return state


class ActualUCNSAdapter:
    """Consumer of only the exact post-reset bridge record surface."""

    def __init__(self, module: ModuleType) -> None:
        required = (
            "PRODUCER_EPOCH", "PROFILE_ID", "PROFILE_VERSION",
            "BRIDGE_SCHEMA_ID", "BRIDGE_SCHEMA_VERSION", "EdcmMetapatBridgeRecord",
        )
        missing = [name for name in required if not hasattr(module, name)]
        if missing:
            raise UCNSAdapterConstructionError("UCNS exact-profile surface missing: " + ", ".join(missing))
        if str(module.PRODUCER_EPOCH) != SUPPORTED_PRODUCER_EPOCH:
            raise UnsupportedUCNSSchemaError("UCNS producer epoch mismatch")
        if (str(module.PROFILE_ID), str(module.PROFILE_VERSION)) != SUPPORTED_PROFILE:
            raise UnsupportedUCNSSchemaError("UCNS profile identity mismatch")
        if (str(module.BRIDGE_SCHEMA_ID), str(module.BRIDGE_SCHEMA_VERSION)) != SUPPORTED_BRIDGE_SCHEMA:
            raise UnsupportedUCNSSchemaError("UCNS bridge schema mismatch")
        self._module = module

    @property
    def status(self) -> UCNSIntegrationStatus:
        return UCNSIntegrationStatus(
            package_present=True,
            producer_recognized=True,
            profile_supported=True,
            adapter_active=True,
            selection="exact_profile_adapter",
        )

    def _coerce_bridge(self, state: Mapping[str, Any]) -> Any | None:
        keys = [key for key in ("ucns_bridge_record", "ucns_bridge_record_json", "ucns_bridge_record_dict") if key in state]
        if len(keys) > 1:
            raise ValueError("supply exactly one UCNS bridge form")
        if not keys:
            if any(key in state for key in ("ucns_object", "ucns_factorization_evidence", "ucns_factorization_evidence_json", "ucns_factorization_evidence_dict")):
                raise UnsupportedUCNSSchemaError("archived UCNS object and factorization surfaces are rejected")
            return None
        key = keys[0]
        value = state[key]
        record_type = self._module.EdcmMetapatBridgeRecord
        if key == "ucns_bridge_record":
            if not isinstance(value, record_type):
                raise TypeError("ucns_bridge_record must be an exact post-reset producer record")
            record = value
        elif key == "ucns_bridge_record_json":
            if not isinstance(value, (str, bytes)):
                raise TypeError("ucns_bridge_record_json must be string or bytes")
            record = record_type.from_json_bytes(value)
        else:
            if not isinstance(value, Mapping):
                raise TypeError("ucns_bridge_record_dict must be a mapping")
            raw = __import__("json").dumps(dict(value), sort_keys=True, separators=(",", ":"))
            record = record_type.from_json_bytes(raw)
        if record.source_commit != PINNED_UCNS_COMMIT:
            raise UCNSAdapterConstructionError("UCNS bridge source commit mismatch")
        if record.theorem_status_transfer or record.edcm_measurement_validity_transfer or record.metapat_validity_transfer:
            raise UCNSAdapterConstructionError("UCNS bridge validity transfer is forbidden")
        return record

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        record = self._coerce_bridge(state)
        if record is None:
            state["ucns_integration"] = self.status.as_dict()
            state.pop("ucns_geometry", None)
            state.pop("ucns_factorization_evidence", None)
            return state
        geometry = UCNSGeometryEvidence(
            stable_hash=record.stable_identity,
            producer_epoch=record.producer_epoch,
            profile_id=record.profile_id,
            profile_version=record.profile_version,
            bridge_schema_id=record.schema_id,
            bridge_schema_version=record.schema_version,
            source_commit=record.source_commit,
            occurrence_ids=tuple(cell.occurrence_id for cell in record.cells),
            retained_layers=tuple((layer.name, layer.digest) for layer in record.retained_layers),
            operator_history=tuple(record.operator_history),
            information_loss=tuple((item.operation, tuple(item.lost)) for item in record.information_loss),
        )
        status = replace(
            self.status,
            ucns_bridge_record_attached=True,
            ucns_scope_metadata_attached=True,
        )
        state["ucns_geometry"] = geometry.as_dict()
        state["ucns_integration"] = status.as_dict()
        state.pop("ucns_factorization_evidence", None)
        return state


@dataclass(frozen=True)
class UCNSAdapterSelection:
    adapter: UCNSAdapter | None
    status: UCNSIntegrationStatus


def _package_present() -> bool:
    try:
        return importlib.util.find_spec("ucns") is not None
    except (ImportError, AttributeError, ValueError):
        return "ucns" in __import__("sys").modules


def suspended_ucns_status(*, package_present: bool | None = None, error: str | None = None) -> UCNSIntegrationStatus:
    present = _package_present() if package_present is None else package_present
    return UCNSIntegrationStatus(
        package_present=present,
        producer_recognized=False,
        profile_supported=False,
        adapter_active=False,
        selection="suspended",
        unresolved_constraints=(RESET_BOUNDARY_REASON,),
        errors=((error or RESET_BOUNDARY_REASON),),
    )


def missing_ucns_status() -> UCNSIntegrationStatus:
    return suspended_ucns_status(package_present=False)


def select_ucns_adapter() -> UCNSAdapterSelection:
    try:
        module = importlib.import_module("ucns")
    except ModuleNotFoundError as exc:
        if exc.name != "ucns":
            raise
        status = suspended_ucns_status(package_present=False)
        return UCNSAdapterSelection(adapter=None, status=status)
    try:
        adapter = ActualUCNSAdapter(module)
    except UCNSAdapterConstructionError as exc:
        status = suspended_ucns_status(package_present=True, error=str(exc))
        return UCNSAdapterSelection(adapter=None, status=status)
    return UCNSAdapterSelection(adapter=adapter, status=adapter.status)


def inspect_ucns_adapter() -> UCNSIntegrationStatus:
    return select_ucns_adapter().status


__all__ = [
    "ActualUCNSAdapter", "INSTALL_HINT", "PINNED_UCNS_COMMIT",
    "REJECTED_LEGACY_SCHEMAS", "RESET_BOUNDARY_REASON", "SUPPORTED_BRIDGE_SCHEMA",
    "SUPPORTED_BRIDGE_SCHEMAS", "SUPPORTED_FACTORIZATION_EVIDENCE_SCHEMAS",
    "SUPPORTED_PRODUCER_EPOCH", "SUPPORTED_PROFILE", "SUPPORTED_SERIALIZATION_VERSIONS",
    "SuspendedUCNSAdapter", "UCNSAdapter", "UCNSAdapterConstructionError",
    "UCNSAdapterSelection", "UCNSFactorizationEvidenceRecord", "UCNSGeometryEvidence",
    "UCNSIntegrationStatus", "UnsupportedUCNSSchemaError", "inspect_ucns_adapter",
    "missing_ucns_status", "select_ucns_adapter", "suspended_ucns_status",
]
