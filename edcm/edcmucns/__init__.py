# === MODULE_BUILD ===
# id: edcmucns_package
#   module_name: edcmucns
#   module_kind: engine
#   summary: edcmucns v0.3.1 — EDCM on UCNS mathematics, provenance as the recurring theme; architecture-only implementation surface (identity layer), empirical claims remain frontier gates
#   owner: Erin Spencer
#   public_surface: PolicyManifest, ProvenanceWitness, Anchor, Payload, Window, Present, AbsentOperatorGeometry, OperatorTurn, BridgeDiagnostic, BoneEvent, encode_turn, make_cadence_anchor, with_cadence, REGISTRY, resolve_scope, ReadoutScope, UnknownReadoutScopeError, ucns_carrier_equivalent, edcm_measurement_equivalent, witness_geometry_consistent, validate_window, gauge_audit, seq_append, interaction_product, flat_reduction, kappa_balance, kappa_audit, EpochBreakError, EpochChain, compare_across_epochs, operator_presence_readout
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: transcript-shaped inputs (turn ids, speakers, surface forms, payload content)
#   admin_only: false
#   tests: tests.test_edcmucns_identity_v031, tests.test_edcmucns_encoder_v031, tests.test_edcmucns_scopes_v031, tests.test_edcmucns_epochs_v031
#   rollout: default_enabled
#   rollback: remove package and its references
#   requires: edcm.ucns_objects
#   since: 2026-07-06
#   unresolved: frontier gates (contact convergence, DA_geom, cadence admission from text, corpus parallel run, operating-state validity) are NotImplemented surfaces with named falsifiers; no empirical claim is made
# === END MODULE_BUILD ===

"""edcmucns — The Energy-Dissonance Circuit Model on UCNS Mathematics.

Design canon v0.3.1 — provenance as the recurring theme.
STATUS: RATIFIED AS ARCHITECTURE (frozen design canon);
FRONTIER AS EMPIRICAL MEASUREMENT.

Primary doctrine: UCNS exists to construct EDCM metrics.

Firewall: UCNS-A proof status applies to carrier geometry. EDCM validity
applies to the measurement function over geometry + provenance. No EDCM
measurement claim inherits proof status from its substrate.

Canon sentences held by this package::

    EDCM windows are ordered UCNS sequence objects composed by
    chronological append. UCNS multiplication is reserved for interaction,
    transport, and irreducibility analysis.

    UCNS equivalence proves same geometry.
    EDCM equivalence requires same geometry plus same readout-bearing witness.

    M_EDCM = readout(G_ucns, Π_provenance, payloads, field_state, policy_manifest)

    Geometry needs testimony. Measurement needs a manifest.
    Flesh needs cadence. Living weights need lineage.

Provenance is measurement material, not decorative metadata.
"""

from __future__ import annotations

from .composer import (
    EpochBreakError,
    InteractionSignature,
    flat_reduction,
    interaction_product,
    kappa_audit,
    kappa_balance,
    seq_append,
)
from .encoder import (
    BoneEvent,
    admit_cadence_from_text,
    encode_turn,
    make_cadence_anchor,
    make_origin_anchor,
    with_cadence,
)
from .epochs import (
    V031_ADOPTION_NOTE,
    EpochBoundary,
    EpochChain,
    EpochSegment,
    compare_across_epochs,
    window_identity_hash,
)
from .equivalence import (
    contact_convergence,
    edcm_measurement_equivalent,
    ucns_carrier_equivalent,
)
from .field_reader import (
    FieldReading,
    attach_field_chain,
    field_chain_hashes,
    field_readouts,
    read_field_chain,
)
from .geometry import (
    L_geo,
    L_op,
    active_families,
    bone_theta,
    cadence_theta,
    da_geom_correlation,
    lambda_field,
    n_cadence,
    n_family,
    n_host_total,
    n_payload,
    non_origin_residue,
    operator_shares,
)
from .manifest import DEFAULT_FAMILY_PRIME_GAUGE, RESIDUE_RULE_VERSION, PolicyManifest
from .provenance import (
    READOUT_BEARING_FIELDS,
    ProvenanceWitness,
    bundle_hash,
    canonicalize,
    witness_hash,
)
from .scopes import REGISTRY, ReadoutScope, UnknownReadoutScopeError, resolve_scope
from .types import (
    ANCHOR_ROLES,
    AbsentOperatorGeometry,
    Anchor,
    BridgeDiagnostic,
    ContentLensEvent,
    OperatorTurn,
    Payload,
    Present,
    Window,
    operator_presence_readout,
)
from .validation import gauge_audit, validate_window, witness_geometry_consistent

__all__ = [
    # manifest
    "PolicyManifest", "DEFAULT_FAMILY_PRIME_GAUGE", "RESIDUE_RULE_VERSION",
    # provenance
    "ProvenanceWitness", "READOUT_BEARING_FIELDS", "canonicalize",
    "witness_hash", "bundle_hash",
    # types
    "ANCHOR_ROLES", "Anchor", "Payload", "ContentLensEvent", "Window",
    "Present", "AbsentOperatorGeometry", "OperatorTurn", "BridgeDiagnostic",
    "operator_presence_readout",
    # geometry
    "non_origin_residue", "bone_theta", "cadence_theta", "L_geo", "L_op",
    "n_host_total", "n_family", "n_cadence", "n_payload", "active_families",
    "operator_shares", "lambda_field", "da_geom_correlation",
    # encoder
    "BoneEvent", "encode_turn", "make_origin_anchor", "make_cadence_anchor",
    "with_cadence", "admit_cadence_from_text",
    # scopes
    "ReadoutScope", "REGISTRY", "resolve_scope", "UnknownReadoutScopeError",
    # equivalence
    "ucns_carrier_equivalent", "edcm_measurement_equivalent",
    "contact_convergence",
    # validation
    "witness_geometry_consistent", "validate_window", "gauge_audit",
    # field reader
    "FieldReading", "read_field_chain", "field_chain_hashes",
    "attach_field_chain", "field_readouts",
    # composer
    "seq_append", "InteractionSignature", "interaction_product",
    "flat_reduction", "kappa_balance", "kappa_audit", "EpochBreakError",
    # epochs
    "EpochBoundary", "EpochSegment", "EpochChain", "window_identity_hash",
    "compare_across_epochs", "V031_ADOPTION_NOTE",
]
