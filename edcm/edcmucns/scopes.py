# === MODULE_BUILD ===
# id: edcmucns_scopes
#   module_name: scopes
#   module_kind: schema
#   summary: Closed readout_scope registry for edcmucns v0.3.1 — edcm_measurement_equivalent must not accept arbitrary strings
#   owner: Erin Spencer
#   public_surface: ReadoutScope, REGISTRY, resolve_scope, UnknownReadoutScopeError
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_edcmucns_scopes_v031
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: none
#   since: 2026-07-06
#   unresolved: bridge_scope read set (witness/geometry diagnostics + manifest + epoch boundaries) is named but its diagnostic vocabulary is still growing with the validator
# === END MODULE_BUILD ===

"""Closed readout-scope registry (edcmucns v0.3.1).

Measurement needs a manifest — and a scope. ``edcm_measurement_equivalent``
resolves scopes only through this registry. Registry extension requires a
manifest bump and an epoch break; there is deliberately no runtime
``register()`` surface.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


class UnknownReadoutScopeError(ValueError):
    """Raised when a scope name is not in the closed registry."""


@dataclass(frozen=True, slots=True)
class ReadoutScope:
    """A named readout scope: what it reads, what it excludes, which mass."""

    name: str
    reads: tuple[str, ...]
    excludes: tuple[str, ...]
    mass: str | None


REGISTRY: MappingProxyType[str, ReadoutScope] = MappingProxyType(
    {
        "operator_scope": ReadoutScope(
            name="operator_scope",
            reads=("geometry", "family_witness"),
            excludes=("flesh_payloads", "cadence_payloads"),
            mass="L_op",
        ),
        "payload_scope": ReadoutScope(
            name="payload_scope",
            reads=("payload_carriers", "payload_hashes"),
            excludes=("operator_mass",),
            mass=None,
        ),
        "cadence_scope": ReadoutScope(
            name="cadence_scope",
            reads=("flesh_cadence_carriers", "composite_lattices"),
            excludes=("n_family",),
            mass=None,
        ),
        "field_scope": ReadoutScope(
            name="field_scope",
            reads=("field_hash_chain",),
            excludes=(),
            mass=None,
        ),
        "bridge_scope": ReadoutScope(
            name="bridge_scope",
            reads=("witness_geometry_diagnostics", "manifest", "epoch_boundaries"),
            excludes=(),
            mass=None,
        ),
    }
)


def resolve_scope(scope: str | ReadoutScope) -> ReadoutScope:
    """Resolve a scope strictly through the closed registry.

    Arbitrary strings and forged ReadoutScope instances are rejected.
    """

    if isinstance(scope, ReadoutScope):
        registered = REGISTRY.get(scope.name)
        if registered != scope:
            raise UnknownReadoutScopeError(
                f"readout scope {scope.name!r} is not the registered scope object"
            )
        return registered
    if scope not in REGISTRY:
        raise UnknownReadoutScopeError(
            f"unknown readout scope {scope!r}; registry extension requires a "
            "manifest bump and an epoch break"
        )
    return REGISTRY[scope]
