# === MODULE_BUILD ===
# id: edcmucns_equivalence
#   module_name: equivalence
#   module_kind: engine
#   summary: v0.3.1 equivalence tiers — ucns_carrier_equivalent (geometry only) and edcm_measurement_equivalent (geometry + in-scope witness + manifest); contact convergence is a frontier gate
#   owner: Erin Spencer
#   public_surface: ucns_carrier_equivalent, edcm_measurement_equivalent, contact_convergence
#   internal_surface: _operator_bundle_hash, _payload_signature, _cadence_signature
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_edcmucns_identity_v031
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: edcmucns_types,edcmucns_scopes,edcmucns_provenance,edcmucns_geometry
#   since: 2026-07-06
#   unresolved: Theta+/F+ are compared as sorted multisets over host anchors (hmmm — ordering sensitivity lives in the witness bundle, which hashes chronologically); bridge_scope equivalence compares manifest identity only until the diagnostic vocabulary is frozen
# === END MODULE_BUILD ===

"""Equivalence tiers for edcmucns v0.3.1.

UCNS equivalence proves same geometry. EDCM equivalence requires same
geometry plus same readout-bearing witness::

    ucns_carrier_equivalent(a, b):
        compares n_min, Theta+, F+
        ignores witness, payloads, manifest

    edcm_measurement_equivalent(a, b, readout_scope):
        requires ucns_carrier_equivalent
        + same in-scope provenance hash
        + same in-scope payload hash
        + same field-chain state where applicable
        + same policy-manifest hash

Forbidden claim: "same UCNS geometry implies same EDCM reading" — no scope
in the closed registry ignores provenance and manifest together.
"""

from __future__ import annotations

from .geometry import cadence_anchors, n_cadence, n_host_total
from .provenance import bundle_hash
from .scopes import ReadoutScope, resolve_scope
from .types import Window


def ucns_carrier_equivalent(a: Window, b: Window) -> bool:
    """Same carrier geometry: n_min, Theta+ and F+ over host anchors.

    Witness, payloads, and manifest are deliberately ignored.
    """

    if n_host_total(a) != n_host_total(b):
        return False
    # Compare (theta, face) as a single per-anchor pairing, not two
    # independent sorted bags: two windows with the same angles and the same
    # face multiset but the negative face attached to a different angle are
    # NOT the same geometry (gauge_audit reports that case as measurement
    # divergence, and ProvenanceWitness carries no face to catch it downstream).
    pairs_a = sorted((anchor.theta, anchor.face) for anchor in a.anchors)
    pairs_b = sorted((anchor.theta, anchor.face) for anchor in b.anchors)
    return pairs_a == pairs_b


def _operator_bundle_hash(window: Window) -> str:
    # Operator scope reads geometry + family witness; flesh/cadence payload
    # content is out of scope (the attachment reference is witness structure
    # and stays readout-bearing).
    return bundle_hash(window.witnesses)


def _payload_signature(window: Window) -> tuple[tuple[str, int], ...]:
    return tuple(sorted((p.content_hash, p.reduced_carrier) for p in window.payloads))


def _cadence_signature(window: Window) -> tuple[object, ...]:
    return (
        n_cadence(window),
        tuple((a.lattice_n, a.ordinal, a.theta) for a in cadence_anchors(window)),
    )


def edcm_measurement_equivalent(
    a: Window, b: Window, readout_scope: str | ReadoutScope
) -> bool:
    """Scoped EDCM measurement identity (v0.3.1 §equivalence tiers)."""

    scope = resolve_scope(readout_scope)

    if not ucns_carrier_equivalent(a, b):
        return False
    # Measurement identity always includes the policy manifest.
    if a.manifest_hash != b.manifest_hash:
        return False

    if scope.name == "operator_scope":
        return _operator_bundle_hash(a) == _operator_bundle_hash(b)
    if scope.name == "payload_scope":
        return _payload_signature(a) == _payload_signature(b)
    if scope.name == "cadence_scope":
        return _cadence_signature(a) == _cadence_signature(b)
    if scope.name == "field_scope":
        return a.field_chain == b.field_chain
    if scope.name == "bridge_scope":
        # Bridge is observational: manifest + carrier identity suffice here;
        # diagnostics are emitted by the validator, not compared as identity.
        return True
    raise AssertionError(f"registered scope without an identity rule: {scope.name}")


def contact_convergence(*_args: object, **_kwargs: object) -> None:
    """FRONTIER — the contact convergence predicate is a typed placeholder.

    Named falsifier: a transcript pair judged convergent by the predicate
    whose ConstraintField contact readouts diverge under the frozen v0.2
    orthogonality spec refutes the predicate.
    """

    raise NotImplementedError(
        "frontier (v0.3.1): contact convergence predicate is not implemented; "
        "see docs/codex_edcmucns_v031_handoff.md"
    )
