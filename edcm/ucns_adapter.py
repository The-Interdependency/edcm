"""Explicit adapter from EDCM to the public UCNS package surface.

Usage guidance
--------------
Call :func:`select_ucns_adapter` during pipeline construction. A missing
optional ``ucns`` package returns a typed unavailable selection. If ``ucns``
is importable but its required public surface is malformed, construction
fails visibly; EDCM must not silently fall back.

When an actual ``ucns.UCNSObject`` is supplied under ``ucns_object``,
:class:`ActualUCNSAdapter` attaches an EDCM-owned geometry evidence record
containing the UCNS stable hash, canonical serialization version, structural
facts, and domain prerequisite metadata. None of that evidence promotes an
EDCM measurement claim or certifies a concrete negative factorization result.
"""

# === MODULE_BUILD ===
# id: edcm_ucns_adapter
#   module_name: ucns_adapter
#   module_kind: adapter
#   summary: Explicit EDCM-owned adapter over actual UCNS public objects, stable identity, and typed domain prerequisite metadata.
#   owner: Erin Spencer
#   public_surface: UCNSAdapter, ActualUCNSAdapter, UCNSAdapterSelection, UCNSIntegrationStatus, UCNSGeometryEvidence, UCNSAdapterConstructionError, UnsupportedUCNSSchemaError, select_ucns_adapter, inspect_ucns_adapter, missing_ucns_status
#   internal_surface: _module_version, _failed_status
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: accepts caller-supplied UCNS objects and returns deterministic structural evidence
#   admin_only: false
#   tests: tests.test_ucns_adapter, tests.test_ucns_dependency, tests.test_measurement
#   rollout: default_enabled
#   rollback: remove module, restore transcript-only semantics selection, and remove its public exports
#   requires: optional ucns package public surface
#   since: 2026-07-12
#   unresolved: official serialized bridge-record ingestion beyond live UCNSObject/object_record
# === END MODULE_BUILD ===

from __future__ import annotations

import importlib
import importlib.metadata
from dataclasses import asdict, dataclass, replace
from types import ModuleType
from typing import Any, Mapping, Protocol

UCNS_SOURCE_REPOSITORY = "https://github.com/The-Interdependency/ucns"
UCNS_BRIDGE_SCHEMA_VERSION = "edcm-ucns-object-record-v1"
SUPPORTED_SERIALIZATION_VERSIONS = frozenset({"ucns-canonical-json-v1"})
INSTALL_HINT = "Install the sibling ucns package with: python -m pip install -e ../ucns"

_REQUIRED_PUBLIC_SURFACE = (
    "UCNSObject",
    "object_record",
    "stable_hash",
    "CANONICAL_SERIALIZATION_VERSION",
)


class UCNSAdapterConstructionError(RuntimeError):
    """Raised when an importable UCNS package cannot satisfy the adapter contract."""


class UnsupportedUCNSSchemaError(UCNSAdapterConstructionError):
    """Raised when UCNS exposes an unsupported canonical serialization schema."""


@dataclass(frozen=True)
class UCNSIntegrationStatus:
    """Independent UCNS integration-state flags.

    Package availability never implies adapter activation, object attachment,
    scope evidence, negative certification, or theorem-status attachment.
    """

    ucns_package_available: bool
    ucns_adapter_active: bool
    ucns_object_attached: bool
    ucns_scope_metadata_attached: bool
    ucns_negative_certification_attached: bool
    ucns_theorem_status_attached: bool
    implementation_id: str
    implementation_version: str | None
    source_repository: str
    selection: str
    unresolved_constraints: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class UCNSGeometryEvidence:
    """EDCM-owned evidence record derived from an actual UCNS object."""

    bridge_schema_version: str
    ucns_serialization_version: str
    stable_hash: str
    domain_label: str
    domain_statuses: tuple[str, ...]
    completeness_guaranteed: bool
    seq_prime_claim_scope: str
    depth: int
    n_min: int
    length: int
    canonical_json: str
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class UCNSAdapter(Protocol):
    """The narrow geometry/identity behavior EDCM requires from UCNS."""

    @property
    def status(self) -> UCNSIntegrationStatus:
        ...

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        ...


@dataclass(frozen=True)
class UCNSAdapterSelection:
    adapter: UCNSAdapter | None
    status: UCNSIntegrationStatus


def _module_version(module: ModuleType) -> str | None:
    try:
        return importlib.metadata.version("ucns")
    except importlib.metadata.PackageNotFoundError:
        value = getattr(module, "__version__", None)
        return str(value) if value is not None else None


def missing_ucns_status() -> UCNSIntegrationStatus:
    return UCNSIntegrationStatus(
        ucns_package_available=False,
        ucns_adapter_active=False,
        ucns_object_attached=False,
        ucns_scope_metadata_attached=False,
        ucns_negative_certification_attached=False,
        ucns_theorem_status_attached=False,
        implementation_id="edcm.ucns_adapter.unavailable",
        implementation_version=None,
        source_repository=UCNS_SOURCE_REPOSITORY,
        selection="unavailable",
        unresolved_constraints=("ucns package is not installed",),
    )


def _failed_status(error: BaseException) -> UCNSIntegrationStatus:
    return UCNSIntegrationStatus(
        ucns_package_available=True,
        ucns_adapter_active=False,
        ucns_object_attached=False,
        ucns_scope_metadata_attached=False,
        ucns_negative_certification_attached=False,
        ucns_theorem_status_attached=False,
        implementation_id="edcm.ucns_adapter.failed",
        implementation_version=None,
        source_repository=UCNS_SOURCE_REPOSITORY,
        selection="failed",
        unresolved_constraints=("UCNS adapter construction failed",),
        errors=(f"{type(error).__name__}: {error}",),
    )


class ActualUCNSAdapter:
    """Adapter over UCNS's actual public object and inspection surfaces."""

    def __init__(self, module: ModuleType) -> None:
        missing = tuple(name for name in _REQUIRED_PUBLIC_SURFACE if not hasattr(module, name))
        if missing:
            raise UCNSAdapterConstructionError(
                "Importable ucns package is missing required public surfaces: "
                + ", ".join(missing)
            )

        schema_version = str(module.CANONICAL_SERIALIZATION_VERSION)
        if schema_version not in SUPPORTED_SERIALIZATION_VERSIONS:
            raise UnsupportedUCNSSchemaError(
                f"Unsupported UCNS serialization schema {schema_version!r}; "
                f"supported={sorted(SUPPORTED_SERIALIZATION_VERSIONS)!r}"
            )

        self._module = module
        self._schema_version = schema_version
        self._version = _module_version(module)

    @property
    def status(self) -> UCNSIntegrationStatus:
        return UCNSIntegrationStatus(
            ucns_package_available=True,
            ucns_adapter_active=True,
            ucns_object_attached=False,
            ucns_scope_metadata_attached=False,
            ucns_negative_certification_attached=False,
            ucns_theorem_status_attached=False,
            implementation_id="edcm.ucns_adapter.actual",
            implementation_version=self._version,
            source_repository=UCNS_SOURCE_REPOSITORY,
            selection="canonical_adapter",
        )

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        state["semantics"] = "ucns.geometry_adapter"

        if "ucns_object" not in state:
            state["ucns_integration"] = self.status.as_dict()
            state.pop("ucns_geometry", None)
            return state

        obj = state["ucns_object"]
        if not isinstance(obj, self._module.UCNSObject):
            raise TypeError(
                "ucns_object must be an actual ucns.UCNSObject; "
                f"got {type(obj).__module__}.{type(obj).__qualname__}"
            )

        record = self._module.object_record(obj)
        metadata = record.domain_metadata
        statuses = tuple(
            status.value if hasattr(status, "value") else str(status)
            for status in metadata.statuses
        )
        evidence = UCNSGeometryEvidence(
            bridge_schema_version=UCNS_BRIDGE_SCHEMA_VERSION,
            ucns_serialization_version=self._schema_version,
            stable_hash=str(record.object_hash),
            domain_label=str(record.domain_label),
            domain_statuses=statuses,
            completeness_guaranteed=bool(metadata.completeness_guaranteed),
            seq_prime_claim_scope=str(metadata.seq_prime_claim_scope),
            depth=int(record.depth),
            n_min=int(record.n_min),
            length=int(record.length),
            canonical_json=str(record.canonical_json),
        )
        attached = replace(
            self.status,
            ucns_object_attached=True,
            ucns_scope_metadata_attached=True,
        )
        state["ucns_geometry"] = evidence.as_dict()
        state["ucns_integration"] = attached.as_dict()
        return state


def select_ucns_adapter() -> UCNSAdapterSelection:
    """Select the actual adapter or a typed unavailable state.

    Only direct absence of the optional ``ucns`` package becomes an unavailable
    selection. Transitive import failures, malformed public surfaces, and
    unsupported schemas remain visible exceptions.
    """

    try:
        module = importlib.import_module("ucns")
    except ModuleNotFoundError as exc:
        if exc.name != "ucns":
            raise
        status = missing_ucns_status()
        return UCNSAdapterSelection(adapter=None, status=status)

    adapter = ActualUCNSAdapter(module)
    return UCNSAdapterSelection(adapter=adapter, status=adapter.status)


def inspect_ucns_adapter() -> UCNSIntegrationStatus:
    """Return an explicit status report without silently activating fallback."""

    try:
        return select_ucns_adapter().status
    except Exception as exc:
        return _failed_status(exc)


__all__ = [
    "ActualUCNSAdapter",
    "INSTALL_HINT",
    "SUPPORTED_SERIALIZATION_VERSIONS",
    "UCNSAdapter",
    "UCNSAdapterConstructionError",
    "UCNSAdapterSelection",
    "UCNSGeometryEvidence",
    "UCNSIntegrationStatus",
    "UnsupportedUCNSSchemaError",
    "inspect_ucns_adapter",
    "missing_ucns_status",
    "select_ucns_adapter",
]
