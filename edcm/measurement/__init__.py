"""edcm.measurement — consolidated edcmbone structural-measurement package.

Dependency-free mirror of the canonical edcmbone package, consolidated into
`edcm` per `The-Interdependency/edcmbone:LAYER_MIGRATION_PLAN.md`.

Source of truth for L0 (bones-only operator layer) remains upstream:
    repo:   The-Interdependency/edcmbone
    path:   backend_old/src/edcmbone/
    commit: 05eee6d15c7ad0a7dcf62220a3a0a8618f481a81

Mirror deltas from upstream (mechanical only):
- absolute ``edcmbone.*`` imports rewritten to package-relative imports;
- ``metrics/orthogonality.py`` is not duplicated — its names are re-exported
  from :mod:`edcm.ucns_objects`, the pre-existing mirror of the same module;
- edcmbone-local ``# ratios:`` CI bookend stamps removed (that check runs
  only in the edcmbone repo).

No UCNS-A theorem/proof status transfers to EDCM, edcmbone, or UCNS-G via
this mirror (see edcmbone ``docs/ucns-boundary.md``).

hmmm: layer split (L0 stays upstream; L1/L2/L3 become edcm-owned) is not yet
executed — this mirror carries all layers together until the metric-to-layer
table is pinned (LAYER_MIGRATION_PLAN.md Phase 2 gate).
"""

# Version of the mirrored upstream package (backend_old/pyproject.toml).
__version__ = "0.1.0"

from .canon import CanonLoader
from .parser import parse_transcript, ParsedTranscript, Turn, Round, BoneToken, FleshToken
from .metrics import (
    RoundMetrics, compute_round, compute_transcript, energy_step,
    tokenize, ngrams, ttr, repetition_ratio, shannon_entropy,
    novelty, cosine_sim, rep_ngram_density, pattern_density,
    jaccard, correction_fidelity, clamp, norm_per_100,
    fixation_risk, broken_return, escalation_risk, stagnation_risk, loop_risk,
    AgentMetrics, project, project_transcript, gini_tbf,
    fire_alerts, crosswalk_risk,
    A_MATRIX, PROJECTION_MAP, ALERT_THRESHOLDS, RISK_TO_ALERT,
    MATRIX_VERSION, freeze, diff,
)

__all__ = [
    "__version__",
    # Canon
    "CanonLoader",
    # Parser
    "parse_transcript", "ParsedTranscript", "Turn", "Round", "BoneToken", "FleshToken",
    # Metrics — compute
    "RoundMetrics", "compute_round", "compute_transcript", "energy_step",
    # Metrics — stats
    "tokenize", "ngrams", "ttr", "repetition_ratio", "shannon_entropy",
    "novelty", "cosine_sim", "rep_ngram_density", "pattern_density",
    "jaccard", "correction_fidelity", "clamp", "norm_per_100",
    # Metrics — risk
    "fixation_risk", "broken_return", "escalation_risk", "stagnation_risk", "loop_risk",
    # Metrics — projection
    "AgentMetrics", "project", "project_transcript", "gini_tbf",
    "fire_alerts", "crosswalk_risk",
    # Metrics — matrix
    "A_MATRIX", "PROJECTION_MAP", "ALERT_THRESHOLDS", "RISK_TO_ALERT",
    "MATRIX_VERSION", "freeze", "diff",
]
