"""Public EDCM package surface.

EDCM owns the maintained measurement implementation and the adapter protocol
used to consume actual UCNS geometry. Optional UCNS absence remains an explicit
transcript-only mode; no sibling package silently replaces EDCM measurement.
"""

# === MODULE_BUILD ===
# id: edcm_package
#   module_name: edcm
#   module_kind: engine
#   summary: EDCM package root — declares package identity and re-exports provenance-bearing layers, actual-UCNS adapter surfaces, energy audit, EDCM objects, edcmucns architecture, and canonical maintained measurement.
#   owner: Erin Spencer
#   public_surface: __version__, build_default_layers, EDCMLayers, LayerProvenance, ConsolidatedMeasurementLayer, TranscriptOnlySemanticsLayer, UCNSSemanticsLayer, ActualUCNSAdapter, UCNSIntegrationStatus, UCNSGeometryEvidence, select_ucns_adapter, inspect_ucns_adapter, audit_energy_text, audit_energy_claim, extract_energy_claim_candidates, audit_falsifiability_preservation, EnergyAuditReport, AuditFlag, EnergyClaim, EDCMBONE_FAILURE_TAXONOMY, BOUNDARY_NOTE, AxisState, MetricAxis, MetricReadout, ConstraintField, FieldMotion, canonical_axes, field_motion_fixture, FIELD_MOTION_FIXTURE_MATRIX, SIGNED_TERNARY, GRAINS, CONTACT_SIGN, RESOLUTION_SIGN, measurement, edcmucns, CanonLoader, parse_transcript, ParsedTranscript, compute_transcript, RoundMetrics, project_transcript, AgentMetrics, fire_alerts
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_measurement, tests.test_ucns_adapter, tests.test_ucns_objects, tests.test_energy_claims, tests.test_packaging
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: edcm_layers, edcm_ucns_adapter, edcm_energy_claims, edcm_falsifiability_bridge, edcm_ucns_objects, edcmucns_package
#   since: 2026-06-02
#   unresolved: METAPAT adapter and full shared-stack result envelope
# === END MODULE_BUILD ===

__version__ = "0.1.0"

from . import edcmucns
from . import measurement
from .layers import (
    ConsolidatedMeasurementLayer,
    EDCMLayers,
    LayerProvenance,
    TranscriptOnlySemanticsLayer,
    UCNSSemanticsLayer,
    build_default_layers,
)
from .ucns_adapter import (
    ActualUCNSAdapter,
    UCNSAdapterConstructionError,
    UCNSGeometryEvidence,
    UCNSIntegrationStatus,
    UnsupportedUCNSSchemaError,
    inspect_ucns_adapter,
    select_ucns_adapter,
)
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
    "__version__",
    "ActualUCNSAdapter",
    "UCNSAdapterConstructionError",
    "UCNSGeometryEvidence",
    "UCNSIntegrationStatus",
    "UnsupportedUCNSSchemaError",
    "inspect_ucns_adapter",
    "select_ucns_adapter",
    "LayerProvenance",
    "TranscriptOnlySemanticsLayer",
    "UCNSSemanticsLayer",
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
