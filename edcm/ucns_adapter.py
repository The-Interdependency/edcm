"""Fail-closed EDCM boundary for post-reset UCNS profile consumption.

UCNS is a stable identifier without a canonical expansion.  Import-name presence,
matching class names, and archived schema fields never establish producer authority.
"""
from __future__ import annotations

import importlib.util
from dataclasses import asdict, dataclass
from typing import Any, Mapping, Protocol

UCNS_SOURCE_REPOSITORY = "https://github.com/The-Interdependency/ucns"
RESET_BOUNDARY_REASON = (
    "UCNS integration is suspended: awaiting post-reset producer profile, reviewed "
    "handoff, and exact source commit"
)
INSTALL_HINT = None
SUPPORTED_PRODUCER_EPOCH: str | None = None
SUPPORTED_PROFILE: tuple[str, str] | None = None
SUPPORTED_BRIDGE_SCHEMA: tuple[str, str] | None = None
PINNED_UCNS_COMMIT: str | None = None
SUPPORTED_SERIALIZATION_VERSIONS = frozenset()
SUPPORTED_BRIDGE_SCHEMAS = frozenset()
SUPPORTED_FACTORIZATION_EVIDENCE_SCHEMAS = frozenset()
REJECTED_LEGACY_SCHEMAS = frozenset(
    {
        "ucns-canonical-json-v1",
        "ucns.bridge-record@1.0.0",
        "ucns.factorization-evidence@1.0.0",
    }
)


class UCNSAdapterConstructionError(RuntimeError):
    """Raised when UCNS consumption is attempted across the reset boundary."""


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
    implementation_id: str = "edcm.ucns_adapter.suspended"
    implementation_version: str | None = None
    source_repository: str = UCNS_SOURCE_REPOSITORY
    selection: str = "suspended"
    unresolved_constraints: tuple[str, ...] = (RESET_BOUNDARY_REASON,)
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
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False


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
    """Typed inactive adapter used only to report the reset/profile boundary."""

    def __init__(self, *, package_present: bool) -> None:
        self._status = suspended_ucns_status(package_present=package_present)

    @property
    def status(self) -> UCNSIntegrationStatus:
        return self._status

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        raise UCNSAdapterConstructionError(RESET_BOUNDARY_REASON)


class ActualUCNSAdapter(SuspendedUCNSAdapter):
    """Compatibility name; archived activation is deliberately impossible."""

    def __init__(self, module: object | None = None) -> None:
        del module
        raise UCNSAdapterConstructionError(RESET_BOUNDARY_REASON)


@dataclass(frozen=True)
class UCNSAdapterSelection:
    adapter: UCNSAdapter | None
    status: UCNSIntegrationStatus


def _package_present() -> bool:
    try:
        return importlib.util.find_spec("ucns") is not None
    except (ImportError, AttributeError, ValueError):
        return "ucns" in __import__("sys").modules


def suspended_ucns_status(*, package_present: bool | None = None) -> UCNSIntegrationStatus:
    present = _package_present() if package_present is None else package_present
    return UCNSIntegrationStatus(
        package_present=present,
        producer_recognized=False,
        profile_supported=False,
        adapter_active=False,
        errors=(
            "An installed package named 'ucns' is classified only as package presence; "
            "it is not recognized producer authority."
            if present
            else "No package named 'ucns' is present; activation would remain suspended even if one were installed."
        ,),
    )


def missing_ucns_status() -> UCNSIntegrationStatus:
    """Compatibility name returning the typed suspended state."""
    return suspended_ucns_status()


def select_ucns_adapter() -> UCNSAdapterSelection:
    """Always return typed suspension until exact post-reset identities are pinned."""
    status = suspended_ucns_status()
    return UCNSAdapterSelection(adapter=None, status=status)


def inspect_ucns_adapter() -> UCNSIntegrationStatus:
    return select_ucns_adapter().status


__all__ = [
    "ActualUCNSAdapter",
    "INSTALL_HINT",
    "PINNED_UCNS_COMMIT",
    "REJECTED_LEGACY_SCHEMAS",
    "RESET_BOUNDARY_REASON",
    "SUPPORTED_BRIDGE_SCHEMA",
    "SUPPORTED_BRIDGE_SCHEMAS",
    "SUPPORTED_FACTORIZATION_EVIDENCE_SCHEMAS",
    "SUPPORTED_PRODUCER_EPOCH",
    "SUPPORTED_PROFILE",
    "SUPPORTED_SERIALIZATION_VERSIONS",
    "SuspendedUCNSAdapter",
    "UCNSAdapter",
    "UCNSAdapterConstructionError",
    "UCNSAdapterSelection",
    "UCNSFactorizationEvidenceRecord",
    "UCNSGeometryEvidence",
    "UCNSIntegrationStatus",
    "UnsupportedUCNSSchemaError",
    "inspect_ucns_adapter",
    "missing_ucns_status",
    "select_ucns_adapter",
    "suspended_ucns_status",
]
