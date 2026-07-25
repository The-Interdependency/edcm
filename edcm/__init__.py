"""Public EDCM package surface.

EDCM owns the maintained measurement implementation and the consumer adapter
protocols used for canonical METAPAT semantic authority and actual UCNS
word-gonol observations and status evidence. Optional package absence remains explicit typed
absence; no sibling package silently replaces EDCM measurement or supplies
invented semantics or certification.
"""

# === MODULE_BUILD ===
# id: edcm_package
#   module_name: edcm
#   module_kind: engine
#   summary: EDCM package root — declares package identity and re-exports provenance-bearing shared-stack layers, canonical METAPAT consumer surfaces, the exact EDCM UCNS word-gonol observation profile consumer, historical metric-object and fork-topology research surfaces, result contracts, integrity gates, energy audit, EDCM objects, edcmucns architecture, and canonical maintained measurement.
#   owner: Erin Spencer
#   public_surface: __version__, build_default_layers, EDCMLayers, LayerProvenance, ConsolidatedMeasurementLayer, CompositeSemanticsLayer, MissingMetapatSemanticAuthorityLayer, MetapatSemanticAuthorityLayer, MissingUCNSProfileLayer, UCNSProfileLayer, SharedStackCompositionLayer, SharedStackDeliveryLayer, ActualMetapatAdapter, MetapatIntegrationStatus, MetapatSemanticEvidence, select_metapat_adapter, inspect_metapat_adapter, ActualUCNSAdapter, UCNSIntegrationStatus, UCNSProfileObservationEvidence, select_ucns_adapter, inspect_ucns_adapter, AuthorizedUCNSFork, UCNSForkTopologyBinding, UCNSForkLintReport, ForkLintDependencyError, ForkTopologyError, build_fork_topology_binding, enumerate_payload_fork_paths, lint_fork_topology, lint_all_payload_forks, EDCMResultContract, build_result_contract, RESULT_SCHEMA_ID, RESULT_SCHEMA_VERSION, IntegrityFinding, IntegrityReport, run_integrity_gate, verify_frozen_canon, verify_measurement_authority, verify_orthogonality_alias, audit_energy_text, audit_energy_claim, extract_energy_claim_candidates, audit_falsifiability_preservation, EnergyAuditReport, AuditFlag, EnergyClaim, EDCMBONE_FAILURE_TAXONOMY, BOUNDARY_NOTE, AxisState, MetricAxis, MetricReadout, ConstraintField, FieldMotion, canonical_axes, field_motion_fixture, FIELD_MOTION_FIXTURE_MATRIX, SIGNED_TERNARY, GRAINS, CONTACT_SIGN, RESOLUTION_SIGN, MetricDefinition, ResolvedMetricUCNS, UCNSMetricDependencyError, UCNSMetricResolutionError, METRIC_DEFINITIONS, SYMBOL_TO_METRIC_ID, resolve_metric_axis, resolve_metric_value, resolve_metric_vector, resolve_round_metrics, resolved_metric_objects_payload, measurement, language, edcmucns, CanonLoader, parse_transcript, ParsedTranscript, compute_transcript, RoundMetrics, project_transcript, AgentMetrics, fire_alerts
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_measurement, tests.test_ucns_adapter, tests.test_ucns_dependency, tests.test_metapat_adapter, tests.test_shared_stack_contract, tests.test_integrity, tests.test_ucns_objects, tests.test_ucns_fork_lint, tests.test_ucns_metrics, tests.test_energy_claims, tests.test_packaging
#   rollout: default_enabled
#   rollback: remove new exports and restore prior package root only with a result-schema migration
#   requires: edcm_layers, edcm_metapat_adapter, edcm_ucns_adapter, edcm_ucns_fork_lint, edcm_shared_stack, edcm_integrity, edcm_energy_claims, edcm_falsifiability_bridge, edcm_ucns_objects, edcm_ucns_metrics, edcmucns_package, edcm_language_package
#   since: 2026-06-02
#   unresolved: UCNS observation digests, historical fork topology bindings, and metric-object hashes provide content identity but not cryptographic producer authentication; formal Mobius coordinates and higher-gonol composition remain open
# === END MODULE_BUILD ===

__version__ = "0.1.0"

from . import edcmucns
from . import measurement
from . import language
from .layers import (
    CompositeSemanticsLayer,
    ConsolidatedMeasurementLayer,
    EDCMLayers,
    LayerProvenance,
    MetapatSemanticAuthorityLayer,
    MissingMetapatSemanticAuthorityLayer,
    MissingUCNSProfileLayer,
    SharedStackCompositionLayer,
    SharedStackDeliveryLayer,
    UCNSProfileLayer,
    build_default_layers,
)
from .metapat_adapter import (
    ActualMetapatAdapter,
    MetapatAdapterConstructionError,
    MetapatIntegrationStatus,
    MetapatSemanticEvidence,
    UnsupportedMetapatSchemaError,
    inspect_metapat_adapter,
    select_metapat_adapter,
)
from .ucns_adapter import (
    ActualUCNSAdapter,
    UCNSAdapterConstructionError,
    UCNSIntegrationStatus,
    UCNSProfileObservationEvidence,
    UnsupportedUCNSSchemaError,
    inspect_ucns_adapter,
    select_ucns_adapter,
)
from .ucns_fork_lint import (
    AuthorizedUCNSFork,
    ForkLintDependencyError,
    ForkTopologyError,
    UCNSForkLintReport,
    UCNSForkTopologyBinding,
    build_fork_topology_binding,
    enumerate_payload_fork_paths,
    lint_all_payload_forks,
    lint_fork_topology,
)
from .shared_stack import (
    EDCMResultContract,
    RESULT_SCHEMA_ID,
    RESULT_SCHEMA_VERSION,
    build_result_contract,
)
from .integrity import (
    IntegrityFinding,
    IntegrityReport,
    run_integrity_gate,
    verify_frozen_canon,
    verify_measurement_authority,
    verify_orthogonality_alias,
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
from .ucns_metrics import (
    METRIC_DEFINITIONS,
    SYMBOL_TO_METRIC_ID,
    MetricDefinition,
    ResolvedMetricUCNS,
    UCNSMetricDependencyError,
    UCNSMetricResolutionError,
    resolve_metric_axis,
    resolve_metric_value,
    resolve_metric_vector,
    resolve_round_metrics,
    resolved_metric_objects_payload,
)

__all__ = [
    "__version__",
    "ActualMetapatAdapter",
    "MetapatAdapterConstructionError",
    "MetapatIntegrationStatus",
    "MetapatSemanticEvidence",
    "UnsupportedMetapatSchemaError",
    "inspect_metapat_adapter",
    "select_metapat_adapter",
    "ActualUCNSAdapter",
    "UCNSAdapterConstructionError",
    "UCNSIntegrationStatus",
    "UCNSProfileObservationEvidence",
    "UnsupportedUCNSSchemaError",
    "inspect_ucns_adapter",
    "select_ucns_adapter",
    "AuthorizedUCNSFork",
    "ForkLintDependencyError",
    "ForkTopologyError",
    "UCNSForkLintReport",
    "UCNSForkTopologyBinding",
    "build_fork_topology_binding",
    "enumerate_payload_fork_paths",
    "lint_all_payload_forks",
    "lint_fork_topology",
    "EDCMResultContract",
    "RESULT_SCHEMA_ID",
    "RESULT_SCHEMA_VERSION",
    "build_result_contract",
    "IntegrityFinding",
    "IntegrityReport",
    "run_integrity_gate",
    "verify_frozen_canon",
    "verify_measurement_authority",
    "verify_orthogonality_alias",
    "LayerProvenance",
    "CompositeSemanticsLayer",
    "MissingMetapatSemanticAuthorityLayer",
    "MetapatSemanticAuthorityLayer",
    "MissingUCNSProfileLayer",
    "UCNSProfileLayer",
    "SharedStackCompositionLayer",
    "SharedStackDeliveryLayer",
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
    "language",
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
    "MetricDefinition",
    "ResolvedMetricUCNS",
    "UCNSMetricDependencyError",
    "UCNSMetricResolutionError",
    "METRIC_DEFINITIONS",
    "SYMBOL_TO_METRIC_ID",
    "resolve_metric_axis",
    "resolve_metric_value",
    "resolve_metric_vector",
    "resolve_round_metrics",
    "resolved_metric_objects_payload",
]
