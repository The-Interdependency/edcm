"""EDCM-owned consumer adapter for canonical METAPAT semantic envelopes.

Usage guidance
--------------
Pass one canonical producer form in the EDCM payload:

- ``metapat_envelope``: an actual ``metapat.MetapatModuleEnvelope``;
- ``metapat_envelope_json``: canonical JSON emitted by that envelope; or
- ``metapat_envelope_dict``: the envelope's canonical mapping.

EDCM validates serialized forms by calling METAPAT's own ``from_json`` or
``from_dict`` constructors. This module deliberately does not duplicate the
producer schema or convert semantic labels into measured values.
"""

# === MODULE_BUILD ===
# id: edcm_metapat_adapter
#   module_name: metapat_adapter
#   module_kind: adapter
#   summary: EDCM-owned consumer for actual versioned immutable METAPAT semantic-authority envelopes; preserves canon identity, exact source references, constraints, permitted interpretations, hmmm, and provenance without creating metric values.
#   owner: Erin Spencer
#   public_surface: MetapatAdapter, ActualMetapatAdapter, MetapatAdapterSelection, MetapatIntegrationStatus, MetapatSemanticEvidence, MetapatAdapterConstructionError, UnsupportedMetapatSchemaError, select_metapat_adapter, inspect_metapat_adapter, missing_metapat_status
#   internal_surface: _module_version, _failed_status, _coerce_envelope
#   auth_boundary: none
#   storage_boundary: no persistence; canonical envelope data is copied into the result record
#   network_boundary: none
#   user_data_boundary: preserves caller-supplied METAPAT source statements and references exactly
#   admin_only: false
#   tests: tests.test_metapat_adapter, tests.test_shared_stack_contract
#   rollout: default_enabled
#   rollback: remove module and restore METAPAT-unavailable status in layer assembly
#   requires: optional metapat package
#   since: 2026-07-12
#   unresolved: official serialized UCNS bridge-record ingestion remains separate; METAPAT statement-to-UCNS payload/tag semantics remain hmmm
# === END MODULE_BUILD ===

from __future__ import annotations

import importlib
from dataclasses import asdict, dataclass, replace
from types import ModuleType
from typing import Any, Mapping, Protocol

METAPAT_SOURCE_REPOSITORY = "https://github.com/The-Interdependency/metapat"
METAPAT_INSTALL_HINT = (
    "Install the canonical METAPAT package with: "
    "python -m pip install 'metapat @ git+https://github.com/"
    "The-Interdependency/metapat.git@3a096f1789432fdb931d4f1659eebf7ef321fbaa'"
)
SUPPORTED_ENVELOPE_SCHEMAS = frozenset({("metapat.module-envelope", "1.0.0")})
_ENVELOPE_INPUT_KEYS = (
    "metapat_envelope",
    "metapat_envelope_json",
    "metapat_envelope_dict",
)


class MetapatAdapterConstructionError(RuntimeError):
    """Raised when an importable METAPAT package lacks the required surface."""


class UnsupportedMetapatSchemaError(ValueError):
    """Raised when the producer envelope schema is not supported by EDCM."""


@dataclass(frozen=True, slots=True)
class MetapatIntegrationStatus:
    metapat_package_available: bool
    metapat_adapter_active: bool
    metapat_envelope_attached: bool
    metapat_canon_identity_attached: bool
    metapat_semantic_constraints_attached: bool
    metapat_theorem_status_attached: bool
    metapat_measurement_values_attached: bool
    implementation_id: str
    implementation_version: str | None
    source_repository: str
    selection: str
    unresolved_constraints: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class MetapatSemanticEvidence:
    schema_id: str
    schema_version: str
    module_id: str
    module_kind: str
    canon_version: str
    canon_digest: str
    source_statement_refs: tuple[str, ...]
    source_statements: tuple[str, ...]
    constraints: tuple[str, ...]
    permitted_interpretations: tuple[str, ...]
    unresolved_constraints: tuple[str, ...]
    provenance_digest: str
    semantic_labels_are_measurements: bool = False
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class MetapatAdapterSelection:
    adapter: "ActualMetapatAdapter | None"
    status: MetapatIntegrationStatus


class MetapatAdapter(Protocol):
    @property
    def status(self) -> MetapatIntegrationStatus:
        ...

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        ...


def _module_version(module: ModuleType) -> str | None:
    value = getattr(module, "__version__", None)
    return str(value) if value is not None else None


def missing_metapat_status() -> MetapatIntegrationStatus:
    return MetapatIntegrationStatus(
        metapat_package_available=False,
        metapat_adapter_active=False,
        metapat_envelope_attached=False,
        metapat_canon_identity_attached=False,
        metapat_semantic_constraints_attached=False,
        metapat_theorem_status_attached=False,
        metapat_measurement_values_attached=False,
        implementation_id="edcm.metapat_adapter.unavailable",
        implementation_version=None,
        source_repository=METAPAT_SOURCE_REPOSITORY,
        selection="unavailable",
        unresolved_constraints=(
            "canonical METAPAT package is not installed",
            "no METAPAT semantic-authority envelope was consumed",
        ),
        errors=(METAPAT_INSTALL_HINT,),
    )


def _failed_status(exc: Exception) -> MetapatIntegrationStatus:
    return MetapatIntegrationStatus(
        metapat_package_available=True,
        metapat_adapter_active=False,
        metapat_envelope_attached=False,
        metapat_canon_identity_attached=False,
        metapat_semantic_constraints_attached=False,
        metapat_theorem_status_attached=False,
        metapat_measurement_values_attached=False,
        implementation_id="edcm.metapat_adapter.failed",
        implementation_version=None,
        source_repository=METAPAT_SOURCE_REPOSITORY,
        selection="failed",
        unresolved_constraints=("METAPAT adapter construction failed",),
        errors=(f"{type(exc).__name__}: {exc}",),
    )


class ActualMetapatAdapter:
    """Consumer adapter over METAPAT's actual public envelope constructors."""

    _required_public = (
        "MetapatModuleEnvelope",
        "MODULE_ENVELOPE_SCHEMA_ID",
        "MODULE_ENVELOPE_SCHEMA_VERSION",
    )

    def __init__(self, module: ModuleType) -> None:
        missing = [name for name in self._required_public if not hasattr(module, name)]
        if missing:
            raise MetapatAdapterConstructionError(
                "METAPAT package is importable but missing required public surfaces: "
                + ", ".join(missing)
            )

        schema = (
            str(module.MODULE_ENVELOPE_SCHEMA_ID),
            str(module.MODULE_ENVELOPE_SCHEMA_VERSION),
        )
        if schema not in SUPPORTED_ENVELOPE_SCHEMAS:
            raise UnsupportedMetapatSchemaError(
                f"Unsupported METAPAT envelope schema {schema!r}; "
                f"supported={sorted(SUPPORTED_ENVELOPE_SCHEMAS)!r}"
            )

        envelope_type = module.MetapatModuleEnvelope
        for constructor in ("from_dict", "from_json"):
            if not callable(getattr(envelope_type, constructor, None)):
                raise MetapatAdapterConstructionError(
                    f"MetapatModuleEnvelope.{constructor} is required"
                )

        self._module = module
        self._envelope_type = envelope_type
        self._schema = schema
        self._version = _module_version(module)

    @property
    def status(self) -> MetapatIntegrationStatus:
        return MetapatIntegrationStatus(
            metapat_package_available=True,
            metapat_adapter_active=True,
            metapat_envelope_attached=False,
            metapat_canon_identity_attached=False,
            metapat_semantic_constraints_attached=False,
            metapat_theorem_status_attached=False,
            metapat_measurement_values_attached=False,
            implementation_id="edcm.metapat_adapter.actual",
            implementation_version=self._version,
            source_repository=METAPAT_SOURCE_REPOSITORY,
            selection="canonical_adapter",
            unresolved_constraints=(
                "no semantic envelope is attached until supplied by the caller",
            ),
        )

    def _coerce_envelope(self, state: Mapping[str, Any]) -> Any | None:
        present = [key for key in _ENVELOPE_INPUT_KEYS if key in state]
        if len(present) > 1:
            raise ValueError(
                "supply exactly one METAPAT envelope form; got " + ", ".join(present)
            )
        if not present:
            return None

        key = present[0]
        value = state[key]
        if key == "metapat_envelope":
            if not isinstance(value, self._envelope_type):
                raise TypeError(
                    "metapat_envelope must be an actual "
                    "metapat.MetapatModuleEnvelope; got "
                    f"{type(value).__module__}.{type(value).__qualname__}"
                )
            envelope = value
        elif key == "metapat_envelope_json":
            if not isinstance(value, str):
                raise TypeError("metapat_envelope_json must be a string")
            envelope = self._envelope_type.from_json(value)
        else:
            if not isinstance(value, Mapping):
                raise TypeError("metapat_envelope_dict must be a mapping")
            envelope = self._envelope_type.from_dict(value)

        # Producer-owned round-trip validation binds this consumer to the exact
        # canonical schema and provenance calculation without duplicating either.
        return self._envelope_type.from_dict(envelope.to_dict())

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        envelope = self._coerce_envelope(state)
        state["semantic_authority"] = "metapat.module-envelope"

        if envelope is None:
            state["metapat_integration"] = self.status.as_dict()
            state.pop("metapat_semantics", None)
            return state

        evidence = MetapatSemanticEvidence(
            schema_id=str(envelope.schema_id),
            schema_version=str(envelope.schema_version),
            module_id=str(envelope.module_id),
            module_kind=str(envelope.module_kind),
            canon_version=str(envelope.canon_version),
            canon_digest=str(envelope.canon_digest),
            source_statement_refs=tuple(envelope.source_statement_refs),
            source_statements=tuple(envelope.source_statements),
            constraints=tuple(envelope.constraints),
            permitted_interpretations=tuple(envelope.permitted_interpretations),
            unresolved_constraints=tuple(envelope.unresolved_constraints),
            provenance_digest=str(envelope.provenance_digest),
        )
        attached = replace(
            self.status,
            metapat_envelope_attached=True,
            metapat_canon_identity_attached=True,
            metapat_semantic_constraints_attached=True,
            unresolved_constraints=evidence.unresolved_constraints,
        )
        state["metapat_semantics"] = evidence.as_dict()
        state["metapat_integration"] = attached.as_dict()
        return state


def select_metapat_adapter() -> MetapatAdapterSelection:
    """Select the canonical adapter or a typed unavailable state.

    Only direct absence of ``metapat`` becomes unavailable. Transitive import
    errors, missing public surfaces, invalid schemas, and malformed envelopes
    remain visible failures.
    """

    try:
        module = importlib.import_module("metapat")
    except ModuleNotFoundError as exc:
        if exc.name != "metapat":
            raise
        status = missing_metapat_status()
        return MetapatAdapterSelection(adapter=None, status=status)

    adapter = ActualMetapatAdapter(module)
    return MetapatAdapterSelection(adapter=adapter, status=adapter.status)


def inspect_metapat_adapter() -> MetapatIntegrationStatus:
    """Return adapter status while preserving construction failures explicitly."""

    try:
        return select_metapat_adapter().status
    except Exception as exc:
        return _failed_status(exc)


__all__ = [
    "ActualMetapatAdapter",
    "METAPAT_INSTALL_HINT",
    "MetapatAdapter",
    "MetapatAdapterConstructionError",
    "MetapatAdapterSelection",
    "MetapatIntegrationStatus",
    "MetapatSemanticEvidence",
    "SUPPORTED_ENVELOPE_SCHEMAS",
    "UnsupportedMetapatSchemaError",
    "inspect_metapat_adapter",
    "missing_metapat_status",
    "select_metapat_adapter",
]
