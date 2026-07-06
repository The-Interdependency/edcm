from .compute import RoundMetrics, compute_round, compute_transcript, energy_step
from .stats import (
    tokenize, ngrams, ttr, repetition_ratio, shannon_entropy,
    novelty, cosine_sim, rep_ngram_density, pattern_density,
    jaccard, correction_fidelity, clamp, norm_per_100,
)
from .risk import fixation_risk, broken_return, escalation_risk, stagnation_risk, loop_risk
from .projection import (
    AgentMetrics, project, project_transcript, gini_tbf,
    fire_alerts, crosswalk_risk,
)
from ...ucns_objects import (
    AxisState, MetricAxis, MetricReadout, ConstraintField, FieldMotion,
    SIGNED_TERNARY, GRAINS, CONTACT_SIGN, RESOLUTION_SIGN,
    canonical_axes, field_motion_fixture, FIELD_MOTION_FIXTURE_MATRIX,
)
from .matrix import (
    A_MATRIX, PROJECTION_MAP, ALERT_THRESHOLDS, RISK_TO_ALERT,
    MATRIX_VERSION, freeze, diff,
)

__all__ = [
    # Layer 1 compute
    "RoundMetrics", "compute_round", "compute_transcript", "energy_step",
    # Layer 0 stats
    "tokenize", "ngrams", "ttr", "repetition_ratio", "shannon_entropy",
    "novelty", "cosine_sim", "rep_ngram_density", "pattern_density",
    "jaccard", "correction_fidelity", "clamp", "norm_per_100",
    # Layer 2 risk
    "fixation_risk", "broken_return", "escalation_risk", "stagnation_risk", "loop_risk",
    # Layer 3 projection
    "AgentMetrics", "project", "project_transcript", "gini_tbf",
    "fire_alerts", "crosswalk_risk",
    # Matrix / weights
    "A_MATRIX", "PROJECTION_MAP", "ALERT_THRESHOLDS", "RISK_TO_ALERT",
    "MATRIX_VERSION", "freeze", "diff",
    # v0.2 orthogonality primitives + UCNS construction objects
    "SIGNED_TERNARY", "GRAINS", "CONTACT_SIGN", "RESOLUTION_SIGN",
    "AxisState", "MetricAxis", "MetricReadout", "ConstraintField", "FieldMotion",
    "canonical_axes", "field_motion_fixture", "FIELD_MOTION_FIXTURE_MATRIX",
]
