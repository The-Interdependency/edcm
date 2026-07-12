"""Canonical maintained EDCM structural-measurement package.

This package was consolidated from ``The-Interdependency/edcmbone`` and keeps
that source commit as provenance. As of the 2026-07-12 stack repair,
``edcm/measurement`` is the maintained source of truth. Installed ``edcmbone``
packages are compatibility/provenance inputs only and never silently override
this implementation.

Consolidation provenance:
    source_repo:   The-Interdependency/edcmbone
    source_path:   backend_old/src/edcmbone/
    source_commit: 05eee6d15c7ad0a7dcf62220a3a0a8618f481a81

No UCNS theorem or proof status transfers into EDCM measurement validity.
Frozen canon data under ``canon/data/*_v1.json`` may change only through a new
version and migration record.

Usage guidance
--------------
Import maintained measurement entry points from ``edcm`` or
``edcm.measurement``. Use :data:`MEASUREMENT_AUTHORITY` in diagnostics and
drift tooling instead of inferring authority from package availability.
"""

# Version of the maintained EDCM measurement surface.
__version__ = "0.1.0"

CONSOLIDATION_SOURCE_REPOSITORY = "https://github.com/The-Interdependency/edcmbone"
CONSOLIDATION_SOURCE_PATH = "backend_old/src/edcmbone/"
CONSOLIDATION_SOURCE_COMMIT = "05eee6d15c7ad0a7dcf62220a3a0a8618f481a81"
MEASUREMENT_SOURCE_OF_TRUTH = "The-Interdependency/edcm:edcm/measurement"
MEASUREMENT_COMPATIBILITY_POLICY = "edcmbone-provenance-only-v1"
MEASUREMENT_AUTHORITY = {
    "canonical": True,
    "source_of_truth": MEASUREMENT_SOURCE_OF_TRUTH,
    "implementation_version": __version__,
    "compatibility_policy": MEASUREMENT_COMPATIBILITY_POLICY,
    "consolidation_source_repository": CONSOLIDATION_SOURCE_REPOSITORY,
    "consolidation_source_path": CONSOLIDATION_SOURCE_PATH,
    "consolidation_source_commit": CONSOLIDATION_SOURCE_COMMIT,
    "runtime_override_by_edcmbone": False,
    "ucns_theorem_status_transfer": False,
}

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
    "CONSOLIDATION_SOURCE_REPOSITORY",
    "CONSOLIDATION_SOURCE_PATH",
    "CONSOLIDATION_SOURCE_COMMIT",
    "MEASUREMENT_SOURCE_OF_TRUTH",
    "MEASUREMENT_COMPATIBILITY_POLICY",
    "MEASUREMENT_AUTHORITY",
    "CanonLoader",
    "parse_transcript", "ParsedTranscript", "Turn", "Round", "BoneToken", "FleshToken",
    "RoundMetrics", "compute_round", "compute_transcript", "energy_step",
    "tokenize", "ngrams", "ttr", "repetition_ratio", "shannon_entropy",
    "novelty", "cosine_sim", "rep_ngram_density", "pattern_density",
    "jaccard", "correction_fidelity", "clamp", "norm_per_100",
    "fixation_risk", "broken_return", "escalation_risk", "stagnation_risk", "loop_risk",
    "AgentMetrics", "project", "project_transcript", "gini_tbf",
    "fire_alerts", "crosswalk_risk",
    "A_MATRIX", "PROJECTION_MAP", "ALERT_THRESHOLDS", "RISK_TO_ALERT",
    "MATRIX_VERSION", "freeze", "diff",
]
