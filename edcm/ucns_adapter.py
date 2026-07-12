"""Explicit EDCM consumer for canonical UCNS geometry and status evidence.

Usage guidance
--------------
Call :func:`select_ucns_adapter` during pipeline construction. Direct absence
of the optional ``ucns`` package returns a typed unavailable selection. An
importable but malformed or unsupported UCNS package fails visibly.

Supply exactly one geometry form:

- ``ucns_object`` — an actual ``ucns.UCNSObject``;
- ``ucns_bridge_record`` — an actual ``ucns.UCNSBridgeRecord``;
- ``ucns_bridge_record_json`` — canonical producer JSON; or
- ``ucns_bridge_record_dict`` — the producer's canonical mapping.

Optionally supply exactly one factorization-evidence form:

- ``ucns_factorization_evidence``;
- ``ucns_factorization_evidence_json``; or
- ``ucns_factorization_evidence_dict``.

Serialized forms are validated by UCNS's own ``from_json`` / ``from_dict``
constructors. Factorization evidence must bind to the same stable object hash
as the geometry record. UCNS statuses remain evidence only and never promote
EDCM empirical validity.
"""

# === MODULE_BUILD ===
# id: edcm_ucns_adapter
#   module_name: ucns_adapter
#   module_kind: adapter
#   summary: EDCM-owned consumer over actual UCNS objects, canonical bridge records, and authoritative factorization evidence with stable-hash binding and no proof-status transfer.
#   owner: Erin Spencer
#   public_surface: UCNSAdapter, ActualUCNSAdapter, UCNSAdapterSelection, UCNSIntegrationStatus, UCNSGeometryEvidence, UCNSFactorizationEvidenceRecord, UCNSAdapterConstructionError, UnsupportedUCNSSchemaError, select_ucns_adapter, inspect_ucns_adapter, missing_ucns_status
#   internal_surface: _module_version, _failed_status, _one_present, _geometry_from_record, _factorization_from_record
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: accepts caller-supplied UCNS objects or canonical producer records and returns deterministic evidence
#   admin_only: false
#   tests: tests.test_ucns_adapter, tests.test_ucns_dependency, tests.test_shared_stack_contract
#   rollout: default_enabled
#   rollback: restore live-object-only adapter and mark serialized evidence unavailable
#   requires: optional ucns package public surface including UCNSBridgeRecord and UCNSFactorizationEvidence
#   since: 2026-07-12
#   unresolved: evidence digests are content identities, not cryptographic producer signatures
# === END MODULE_BUILD ===

from __future__ import annotations

import importlib
import importlib.metadata
from dataclasses import asdict, dataclass, replace
from types import ModuleType
from typing import Any, Mapping, Protocol

UCNS_SOURCE_REPOSITORY = "https://github.com/The-Interdependency/ucns"
SUPPORTED_SERIALIZATION_VERSIONS = frozenset({"ucns-canonical-json-v1"})
SUPPORTED_BRIDGE_SCHEMAS = frozenset({("ucns.bridge-record", "1.0.0")})
SUPPORTED_FACTORIZATION_EVIDENCE_SCHEMAS = frozenset(
    {("ucns.factorization-evidence", "1.0.0")}
)
INSTALL_HINT = (
    "Install the canonical UCNS package with: "
    "python -m pip install 'ucns @ git+https://github.com/"
    "The-Interdependency/ucns.git@27c004b21b6d02bf3873c280ebd3158131ef87fe'"
)

_GEOMETRY_INPUT_KEYS = (
    "ucns_object",
    "ucns_bridge_record",
    "ucns_bridge_record_json",
    "ucns_bridge_record_dict",
)
_FACTORIZATION_INPUT_KEYS = (
    "ucns_factorization_evidence",
    "ucns_factorization_evidence_json",
    "ucns_factorization_evidence_dict",
)
_REQUIRED_PUBLIC_SURFACE = (
    "UCNSObject",
    "UCNSBridgeRecord",
    "UCNSFactorizationEvidence",
    "bridge_record",
    "BRIDGE_RECORD_SCHEMA_ID",
    "BRIDGE_RECORD_SCHEMA_VERSION",
    "FACTORIZATION_EVIDENCE_SCHEMA_ID",
    "FACTORIZATION_EVIDENCE_SCHEMA_VERSION",
    "CANONICAL_SERIALIZATION_VERSION",
)


class UCNSAdapterConstructionError(RuntimeError):
    """Raised when an importable UCNS package cannot satisfy the adapter contract."""


class UnsupportedUCNSSchemaError(UCNSAdapterConstructionError):
    """Raised when UCNS exposes an unsupported producer schema."""


@dataclass(frozen=True)
class UCNSIntegrationStatus:
    """Independent UCNS integration-state flags.

    Package availability never implies adapter activation, object attachment,
    bridge attachment, scope evidence, factorization evidence, negative
    certification, or theorem-status attachment.
    """

    ucns_package_available: bool
    ucns_adapter_active: bool
    ucns_object_attached: bool
    ucns_bridge_record_attached: bool
    ucns_scope_metadata_attached: bool
    ucns_factorization_evidence_attached: bool
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
    """EDCM-owned view of one validated canonical UCNS bridge record."""

    bridge_schema_id: str
    bridge_schema_version: str
    bridge_producer_id: str
    bridge_evidence_digest: str
    ucns_serialization_version: str
    stable_hash: str
    domain_label: str
    domain_statuses: tuple[str, ...]
    completeness_guaranteed: bool
    seq_prime_claim_scope: str
    depth: int
    n_min: int
    length: int
    is_unit: bool
    is_verified_domain: bool
    is_frontier: bool
    note: str
    canonical_json: str
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class UCNSFactorizationEvidenceRecord:
    """EDCM-owned view of authoritative UCNS factorization evidence."""

    schema_id: str
    schema_version: str
    producer_id: str
    evidence_digest: str
    product_hash: str
    product_domain_label: str
    product_domain_statuses: tuple[str, ...]
    completeness_guaranteed: bool
    result_kind: str
    factor_hashes: tuple[str, ...]
    negative_result_certified: bool
    seq_prime_is_absolute: bool
    claim_scope: str
    note: str
    certification_policy_version: str
    search_exhausted: bool
    truncation_occurred: bool
    catalogue_source: str
    supplied_catalogue_size: int
    supplied_catalogue_fingerprint: str
    effective_catalogue_size: int
    effective_catalogue_fingerprint: str
    catalogue_coverage_status: str
    catalogue_coverage_reason: str
    catalogue_coverage_rule_version: str
    required_catalogue_rule_version: str
    required_catalogue_fingerprint: str
    coverage_record_validated: bool
    coverage_bound_to_search_report: bool
    pruning_applied: bool
    pruning_rule: str
    pruning_rule_version: str
    pruning_preserves_coverage: bool
    uncertified_reasons: tuple[str, ...]
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class UCNSAdapter(Protocol):
    """The narrow geometry and evidence behavior EDCM requires from UCNS."""

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


def _one_present(state: Mapping[str, Any], keys: tuple[str, ...], label: str) -> str | None:
    present = [key for key in keys if key in state]
    if len(present) > 1:
        raise ValueError(
            f"supply exactly one {label} form; got " + ", ".join(present)
        )
    return present[0] if present else None


def missing_ucns_status() -> UCNSIntegrationStatus:
    return UCNSIntegrationStatus(
        ucns_package_available=False,
        ucns_adapter_active=False,
        ucns_object_attached=False,
        ucns_bridge_record_attached=False,
        ucns_scope_metadata_attached=False,
        ucns_factorization_evidence_attached=False,
        ucns_negative_certification_attached=False,
        ucns_theorem_status_attached=False,
        implementation_id="edcm.ucns_adapter.unavailable",
        implementation_version=None,
        source_repository=UCNS_SOURCE_REPOSITORY,
        selection="unavailable",
        unresolved_constraints=("canonical ucns package is not installed",),
        errors=(INSTALL_HINT,),
    )


def _failed_status(error: BaseException) -> UCNSIntegrationStatus:
    return UCNSIntegrationStatus(
        ucns_package_available=True,
        ucns_adapter_active=False,
        ucns_object_attached=False,
        ucns_bridge_record_attached=False,
        ucns_scope_metadata_attached=False,
        ucns_factorization_evidence_attached=False,
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
    """Adapter over UCNS's actual object and evidence-envelope surfaces."""

    def __init__(self, module: ModuleType) -> None:
        missing = tuple(
            name for name in _REQUIRED_PUBLIC_SURFACE if not hasattr(module, name)
        )
        if missing:
            raise UCNSAdapterConstructionError(
                "Importable ucns package is missing required public surfaces: "
                + ", ".join(missing)
            )

        serialization_version = str(module.CANONICAL_SERIALIZATION_VERSION)
        if serialization_version not in SUPPORTED_SERIALIZATION_VERSIONS:
            raise UnsupportedUCNSSchemaError(
                f"Unsupported UCNS serialization schema {serialization_version!r}; "
                f"supported={sorted(SUPPORTED_SERIALIZATION_VERSIONS)!r}"
            )
        bridge_schema = (
            str(module.BRIDGE_RECORD_SCHEMA_ID),
            str(module.BRIDGE_RECORD_SCHEMA_VERSION),
        )
        if bridge_schema not in SUPPORTED_BRIDGE_SCHEMAS:
            raise UnsupportedUCNSSchemaError(
                f"Unsupported UCNS bridge schema {bridge_schema!r}; "
                f"supported={sorted(SUPPORTED_BRIDGE_SCHEMAS)!r}"
            )
        factor_schema = (
            str(module.FACTORIZATION_EVIDENCE_SCHEMA_ID),
            str(module.FACTORIZATION_EVIDENCE_SCHEMA_VERSION),
        )
        if factor_schema not in SUPPORTED_FACTORIZATION_EVIDENCE_SCHEMAS:
            raise UnsupportedUCNSSchemaError(
                f"Unsupported UCNS factorization evidence schema {factor_schema!r}; "
                "supported="
                f"{sorted(SUPPORTED_FACTORIZATION_EVIDENCE_SCHEMAS)!r}"
            )
        for producer_type, label in (
            (module.UCNSBridgeRecord, "UCNSBridgeRecord"),
            (module.UCNSFactorizationEvidence, "UCNSFactorizationEvidence"),
        ):
            for constructor in ("from_dict", "from_json"):
                if not callable(getattr(producer_type, constructor, None)):
                    raise UCNSAdapterConstructionError(
                        f"{label}.{constructor} is required"
                    )

        self._module = module
        self._serialization_version = serialization_version
        self._version = _module_version(module)

    @property
    def status(self) -> UCNSIntegrationStatus:
        return UCNSIntegrationStatus(
            ucns_package_available=True,
            ucns_adapter_active=True,
            ucns_object_attached=False,
            ucns_bridge_record_attached=False,
            ucns_scope_metadata_attached=False,
            ucns_factorization_evidence_attached=False,
            ucns_negative_certification_attached=False,
            ucns_theorem_status_attached=False,
            implementation_id="edcm.ucns_adapter.actual",
            implementation_version=self._version,
            source_repository=UCNS_SOURCE_REPOSITORY,
            selection="canonical_adapter",
        )

    def _coerce_bridge_record(
        self,
        state: Mapping[str, Any],
        geometry_key: str,
    ) -> tuple[Any, bool]:
        value = state[geometry_key]
        if geometry_key == "ucns_object":
            if not isinstance(value, self._module.UCNSObject):
                raise TypeError(
                    "ucns_object must be an actual ucns.UCNSObject; "
                    f"got {type(value).__module__}.{type(value).__qualname__}"
                )
            return self._module.bridge_record(value), True
        if geometry_key == "ucns_bridge_record":
            if not isinstance(value, self._module.UCNSBridgeRecord):
                raise TypeError(
                    "ucns_bridge_record must be an actual ucns.UCNSBridgeRecord; "
                    f"got {type(value).__module__}.{type(value).__qualname__}"
                )
            record = value
        elif geometry_key == "ucns_bridge_record_json":
            if not isinstance(value, str):
                raise TypeError("ucns_bridge_record_json must be a string")
            record = self._module.UCNSBridgeRecord.from_json(value)
        else:
            if not isinstance(value, Mapping):
                raise TypeError("ucns_bridge_record_dict must be a mapping")
            record = self._module.UCNSBridgeRecord.from_dict(value)
        # Producer-owned round trip binds this consumer to the exact schema,
        # type rules, canonical JSON, object hash, and evidence digest.
        return self._module.UCNSBridgeRecord.from_dict(record.to_dict()), False

    def _coerce_factorization_evidence(
        self,
        state: Mapping[str, Any],
        factor_key: str,
    ) -> Any:
        value = state[factor_key]
        if factor_key == "ucns_factorization_evidence":
            if not isinstance(value, self._module.UCNSFactorizationEvidence):
                raise TypeError(
                    "ucns_factorization_evidence must be an actual "
                    "ucns.UCNSFactorizationEvidence; got "
                    f"{type(value).__module__}.{type(value).__qualname__}"
                )
            evidence = value
        elif factor_key == "ucns_factorization_evidence_json":
            if not isinstance(value, str):
                raise TypeError(
                    "ucns_factorization_evidence_json must be a string"
                )
            evidence = self._module.UCNSFactorizationEvidence.from_json(value)
        else:
            if not isinstance(value, Mapping):
                raise TypeError(
                    "ucns_factorization_evidence_dict must be a mapping"
                )
            evidence = self._module.UCNSFactorizationEvidence.from_dict(value)
        return self._module.UCNSFactorizationEvidence.from_dict(evidence.to_dict())

    @staticmethod
    def _geometry_from_record(record: Any) -> UCNSGeometryEvidence:
        return UCNSGeometryEvidence(
            bridge_schema_id=str(record.schema_id),
            bridge_schema_version=str(record.schema_version),
            bridge_producer_id=str(record.producer_id),
            bridge_evidence_digest=str(record.evidence_digest),
            ucns_serialization_version=str(record.ucns_serialization_version),
            stable_hash=str(record.object_hash),
            domain_label=str(record.domain_label),
            domain_statuses=tuple(record.domain_statuses),
            completeness_guaranteed=bool(record.completeness_guaranteed),
            seq_prime_claim_scope=str(record.seq_prime_claim_scope),
            depth=int(record.depth),
            n_min=int(record.n_min),
            length=int(record.length),
            is_unit=bool(record.is_unit),
            is_verified_domain=bool(record.is_verified_domain),
            is_frontier=bool(record.is_frontier),
            note=str(record.note),
            canonical_json=str(record.canonical_json),
        )

    @staticmethod
    def _factorization_from_record(record: Any) -> UCNSFactorizationEvidenceRecord:
        return UCNSFactorizationEvidenceRecord(
            schema_id=str(record.schema_id),
            schema_version=str(record.schema_version),
            producer_id=str(record.producer_id),
            evidence_digest=str(record.evidence_digest),
            product_hash=str(record.product_hash),
            product_domain_label=str(record.product_domain_label),
            product_domain_statuses=tuple(record.product_domain_statuses),
            completeness_guaranteed=bool(record.completeness_guaranteed),
            result_kind=str(record.result_kind),
            factor_hashes=tuple(record.factor_hashes),
            negative_result_certified=bool(record.negative_result_certified),
            seq_prime_is_absolute=bool(record.seq_prime_is_absolute),
            claim_scope=str(record.claim_scope),
            note=str(record.note),
            certification_policy_version=str(record.certification_policy_version),
            search_exhausted=bool(record.search_exhausted),
            truncation_occurred=bool(record.truncation_occurred),
            catalogue_source=str(record.catalogue_source),
            supplied_catalogue_size=int(record.supplied_catalogue_size),
            supplied_catalogue_fingerprint=str(record.supplied_catalogue_fingerprint),
            effective_catalogue_size=int(record.effective_catalogue_size),
            effective_catalogue_fingerprint=str(record.effective_catalogue_fingerprint),
            catalogue_coverage_status=str(record.catalogue_coverage_status),
            catalogue_coverage_reason=str(record.catalogue_coverage_reason),
            catalogue_coverage_rule_version=str(
                record.catalogue_coverage_rule_version
            ),
            required_catalogue_rule_version=str(
                record.required_catalogue_rule_version
            ),
            required_catalogue_fingerprint=str(
                record.required_catalogue_fingerprint
            ),
            coverage_record_validated=bool(record.coverage_record_validated),
            coverage_bound_to_search_report=bool(
                record.coverage_bound_to_search_report
            ),
            pruning_applied=bool(record.pruning_applied),
            pruning_rule=str(record.pruning_rule),
            pruning_rule_version=str(record.pruning_rule_version),
            pruning_preserves_coverage=bool(record.pruning_preserves_coverage),
            uncertified_reasons=tuple(record.uncertified_reasons),
        )

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        state["semantics"] = "ucns.geometry_adapter"
        geometry_key = _one_present(state, _GEOMETRY_INPUT_KEYS, "UCNS geometry")
        factor_key = _one_present(
            state,
            _FACTORIZATION_INPUT_KEYS,
            "UCNS factorization evidence",
        )

        if geometry_key is None:
            if factor_key is not None:
                raise ValueError(
                    "UCNS factorization evidence requires an attached geometry "
                    "record with the same stable object hash"
                )
            state["ucns_integration"] = self.status.as_dict()
            state.pop("ucns_geometry", None)
            state.pop("ucns_factorization_evidence", None)
            return state

        bridge_record, live_object = self._coerce_bridge_record(state, geometry_key)
        geometry = self._geometry_from_record(bridge_record)
        status = replace(
            self.status,
            ucns_object_attached=live_object,
            ucns_bridge_record_attached=True,
            ucns_scope_metadata_attached=True,
            ucns_theorem_status_attached=True,
        )
        state["ucns_geometry"] = geometry.as_dict()
        state.pop("ucns_factorization_evidence", None)

        if factor_key is not None:
            factor_record = self._coerce_factorization_evidence(state, factor_key)
            if str(factor_record.product_hash) != geometry.stable_hash:
                raise ValueError(
                    "UCNS factorization evidence product_hash does not match "
                    "attached geometry stable_hash"
                )
            factorization = self._factorization_from_record(factor_record)
            state["ucns_factorization_evidence"] = factorization.as_dict()
            status = replace(
                status,
                ucns_factorization_evidence_attached=True,
                ucns_negative_certification_attached=(
                    factorization.negative_result_certified
                ),
                ucns_theorem_status_attached=True,
            )

        state["ucns_integration"] = status.as_dict()
        return state


def select_ucns_adapter() -> UCNSAdapterSelection:
    """Select the actual adapter or a typed unavailable state.

    Only direct absence of the optional ``ucns`` package becomes unavailable.
    Transitive import failures, malformed public surfaces, unsupported schemas,
    and invalid producer evidence remain visible exceptions.
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
    """Return explicit adapter status without activating fallback silently."""

    try:
        return select_ucns_adapter().status
    except Exception as exc:
        return _failed_status(exc)


__all__ = [
    "ActualUCNSAdapter",
    "INSTALL_HINT",
    "SUPPORTED_BRIDGE_SCHEMAS",
    "SUPPORTED_FACTORIZATION_EVIDENCE_SCHEMAS",
    "SUPPORTED_SERIALIZATION_VERSIONS",
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
]
