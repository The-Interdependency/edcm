"""EDCM package bootstrap.

Provides a single place to assemble all four EDCM layers while
optionally integrating with external `ucns` and `edcmbone` packages, plus the
UCNS metric construction objects (v0.2 orthogonality spec).
"""

from .layers import EDCMLayers, build_default_layers

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
