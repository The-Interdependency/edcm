"""EDCM package bootstrap.

Provides a single place to assemble all four EDCM layers while
optionally integrating with external `ucns` and `edcmbone` packages, plus the
UCNS metric construction objects (v0.2 orthogonality spec) and the
consolidated edcmbone structural-measurement mirror (`edcm.measurement`).
"""

# === MODULE_BUILD ===
# id: edcm_package
#   module_name: edcm
#   module_kind: engine
#   summary: EDCM package root — assembles the four-layer bootstrap and re-exports the public API (energy audit, UCNS construction objects, edcmucns v0.3.1, consolidated measurement surface)
#   owner: Erin Spencer
#   public_surface: build_default_layers, EDCMLayers, ConsolidatedMeasurementLayer, audit_energy_text, audit_energy_claim, extract_energy_claim_candidates, audit_falsifiability_preservation, EnergyAuditReport, AuditFlag, EnergyClaim, EDCMBONE_FAILURE_TAXONOMY, BOUNDARY_NOTE, AxisState, MetricAxis, MetricReadout, ConstraintField, FieldMotion, canonical_axes, field_motion_fixture, FIELD_MOTION_FIXTURE_MATRIX, SIGNED_TERNARY, GRAINS, CONTACT_SIGN, RESOLUTION_SIGN, measurement, edcmucns, CanonLoader, parse_transcript, ParsedTranscript, compute_transcript, RoundMetrics, project_transcript, AgentMetrics, fire_alerts
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_measurement, tests.test_ucns_objects, tests.test_energy_claims
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: edcm_layers, edcm_energy_claims, edcm_falsifiability_bridge, edcm_ucns_objects, edcmucns_package
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===

from . import edcmucns
from . import measurement
from .layers import ConsolidatedMeasurementLayer, EDCMLayers, build_default_layers
from .measurement import (
    AgentMetrics,
    CanonLoader,
    ParsedTranscript,
    RoundMetrics,
    compute_transcript,
    fire_alerts,
    parse_transcript,
    project_transcript,
)

from .falsifiability_bridge import (
    BOUNDARY_NOTE,
    EDCMBONE_FAILURE_TAXONOMY,
    audit_falsifiability_preservation,
)

from .energy_claims import (
    AuditFlag,
    EnergyAuditReport,
    EnergyClaim,
    audit_energy_claim,
    audit_energy_text,
    extract_energy_claim_candidates,
)

from .ucns_objects import (
    AxisState,
    MetricAxis,
    MetricReadout,
    ConstraintField,
    FieldMotion,
    canonical_axes,
    field_motion_fixture,
    FIELD_MOTION_FIXTURE_MATRIX,
    SIGNED_TERNARY,
    GRAINS,
    CONTACT_SIGN,
    RESOLUTION_SIGN,
)

__all__ = [
    "audit_energy_text",
    "audit_energy_claim",
    "extract_energy_claim_candidates",
    "audit_falsifiability_preservation",
    "EDCMBONE_FAILURE_TAXONOMY",
    "BOUNDARY_NOTE",
    "EnergyAuditReport",
    "AuditFlag",
    "EnergyClaim",
    "EDCMLayers",
    "build_default_layers",
    "ConsolidatedMeasurementLayer",
    "measurement",
    "edcmucns",
    "CanonLoader",
    "parse_transcript",
    "ParsedTranscript",
    "compute_transcript",
    "RoundMetrics",
    "project_transcript",
    "AgentMetrics",
    "fire_alerts",
    "AxisState",
    "MetricAxis",
    "MetricReadout",
    "ConstraintField",
    "FieldMotion",
    "canonical_axes",
    "field_motion_fixture",
    "FIELD_MOTION_FIXTURE_MATRIX",
    "SIGNED_TERNARY",
    "GRAINS",
    "CONTACT_SIGN",
    "RESOLUTION_SIGN",
]
