"""
edcmbone.metrics.matrix
~~~~~~~~~~~~~~~~~~~~~~~
Explicit, freezable A matrix for the EDCM four-layer stack.

Architecture
------------
Layer 0  Primitives          φ(y_t, y_{t-1}) — text-computable features
Layer 1  Arc-Style 11        M_t = A · φ     — metric vector (this file)
Layer 2  Risk Composites     R_fix, R_esc, R_stag, R_loop
Layer 3  Agent-Facing 6      CM, DA, DRIFT, DVG, INT, TBF

The A matrix maps primitive features to Layer 1 metrics.  The
PROJECTION_MAP maps Layer 1 to Layer 3.  Both are versioned dicts
so they can be frozen, diff-ed, and stamped into encoded artefacts.

Notes on invariants
-------------------
- All Layer 1 metrics except O are [0, 1].
- O is [-1, 1]: positive = overconfident, negative = under-confident.
  It is the only signed metric.  Callers that need [0, 1] should use
  abs(O) or (O + 1) / 2 as appropriate; the signed range is preserved
  here for full fidelity.
- κ (kappa) ∈ [0, 1].  It is a state variable (RC-circuit stored
  tension) clamped to [0, 1] by energy_step().  PROJECTION_MAP["DA"]
  also requires κ ∈ [0, 1].
- P (Progress) is the only health metric; it is *subtracted* in
  composite risk (−β₆P in the logistic formulation).

Freezing
--------
Call freeze(matrix) to produce an immutable, version-stamped copy
suitable for embedding in compressed artefacts.

Note on A_MATRIX vs compute.py
------------------------------
A_MATRIX is currently documentation-shaped: it records the intended
weights and primitive inputs for each Layer 1 metric, but the actual
computation weights are hardcoded in compute.py (functions _compute_*).
A_MATRIX should eventually become the single source of truth so that
changing a weight here automatically changes the computation.  Until
that refactor is complete, keep both in sync manually.
"""

# === MODULE_BUILD ===
# id: edcmbone_metrics_matrix
#   module_name: matrix
#   module_kind: schema
#   summary: explicit freezable A matrix (Layer0->Layer1) and PROJECTION_MAP (Layer1->Layer3) as versioned, diffable dicts
#   owner: Erin Spencer
#   public_surface: freeze, diff
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: hmmm
#   rollout: default_enabled
#   rollback: remove module; metric projection loses its frozen coefficient source
#   requires: none
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===


from __future__ import annotations

import copy
import hashlib
import json

# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------

MATRIX_VERSION = "1.0"

# ---------------------------------------------------------------------------
# A matrix — Layer 0 → Layer 1 weights
#
# Each entry: metric_name -> {primitive_name: weight}
# Weights within each row should sum to 1.0 (or be explicitly non-normalised
# where marker density normalisation happens externally).
#
# Primitives key:
#   rep_b         RepetitionRatio(tokens_b)
#   rep_ngram     RepNgramDensity(tokens_b, n=3)
#   non_novelty   1 - Novelty(tokens_b | tokens_a)
#   entropy_b     ShannonEntropy(tokens_b)          (normalised /10 for N)
#   cosine_ab     CosineSim(tokens_a, tokens_b)
#   rho_refusal   PatternDensity(refusal phrases)   (÷5 before use)
#   rho_hedge     PatternDensity(hedge phrases)      (÷5 before use)
#   marker_C      MarkerHits(C, contradiction)       (÷token_count before use)
#   marker_R      MarkerHits(R, refusal)             (÷token_count before use)
#   marker_I      MarkerHits(I, integration-fail)    (÷token_count before use)
#   marker_O_over MarkerHits(O, overconfidence)      (signed, see O row)
#   marker_O_under MarkerHits(O, under-confidence)   (signed, see O row)
#   loop_risk     composite (rep_b, rep_ngram, cosine_ab) — see risk.py
#   entropy_gain  ΔH between rounds                  (for P)
# ---------------------------------------------------------------------------

A_MATRIX: dict = {
    "version": MATRIX_VERSION,
    "metrics": {
        # C: constraint strain — pure marker signal
        "C": {
            "marker_C": 1.0,
        },
        # R: refusal density — pure marker signal
        "R": {
            "marker_R": 1.0,
        },
        # F: fixation — repetition + n-gram repetition + low novelty
        "F": {
            "rep_b":       0.30,
            "rep_ngram":   0.30,
            "non_novelty": 0.40,
        },
        # E: escalation — refusal signal + loop risk
        # NOTE: E depends on Layer 1 metric R — Layer mixing; see issue #38
        "E": {
            "R":         0.60,   # R is itself a Layer 1 metric here
            "loop_risk": 0.40,
        },
        # D: deflection — low cosine overlap with prior round
        "D": {
            "non_cosine_ab": 1.0,   # 1 - cosine_ab
        },
        # N: noise — repetition + low entropy
        "N": {
            "rep_b":         0.60,
            "non_entropy_b": 0.40,  # 1 - (entropy_b / 10)
        },
        # I: integration failure — pure marker signal
        "I": {
            "marker_I": 1.0,
        },
        # O: overconfidence — signed [-1, 1]
        #    O = (over - under) / (over + under); weights are directional
        "O": {
            "marker_O_over":  +1.0,
            "marker_O_under": -1.0,
        },
        # L: coherence loss — repetition + low novelty
        "L": {
            "rep_b":       0.50,
            "non_novelty": 0.50,
        },
        # P: progress (health) — novelty + entropy gain
        "P": {
            "novelty":      0.60,
            "entropy_gain": 0.40,
        },
        # kappa: stored tension (state variable, not a metric per se)
        "kappa": {
            "_circuit": "RC",  # computed by energy_step(), not A·φ
            "alpha":    0.85,
            "delta_max": 0.30,
        },
    },
}

# ---------------------------------------------------------------------------
# Projection map — Layer 1 → Layer 3 weights
#
# Each row: agent_metric -> {layer1_metric: weight}
# All rows produce values in [0, 1] after clamp.
# DRIFT uses neg_P = (1 - P) so that high progress = low drift.
# TBF is independent (Gini on turn token shares, not a projection).
# ---------------------------------------------------------------------------

PROJECTION_MAP: dict = {
    "version": MATRIX_VERSION,
    "metrics": {
        # CM: Constraint Mismatch — strain + integration failure
        "CM": {
            "C": 0.50,
            "I": 0.50,
        },
        # DA: Dissonance Accumulation — stored tension + escalation + refusal
        "DA": {
            "kappa": 0.40,
            "E":     0.40,
            "R":     0.20,
        },
        # DRIFT: coherence loss + lack of progress
        "DRIFT": {
            "L":     0.50,
            "neg_P": 0.50,   # neg_P = 1 - P
        },
        # DVG: Divergence — deflection + noise
        "DVG": {
            "D": 0.50,
            "N": 0.50,
        },
        # INT: Intensity — escalation + fixation
        "INT": {
            "E": 0.50,
            "F": 0.50,
        },
        # TBF: Turn-Balance Fairness — Gini coefficient, independent
        "TBF": {
            "_method": "gini",
        },
    },
}

# ---------------------------------------------------------------------------
# Alert thresholds — Layer 3 → named alerts
# ---------------------------------------------------------------------------

ALERT_THRESHOLDS: dict = {
    "version": MATRIX_VERSION,
    "alerts": {
        "ALERT_CM_HIGH":   {"metric": "CM",   "threshold": 0.70, "direction": "above"},
        "ALERT_DA_RISING": {"metric": "DA",   "threshold": 0.60, "direction": "above"},
        "ALERT_DRIFT":     {"metric": "DRIFT","threshold": 0.50, "direction": "above"},
        "ALERT_DVG_HIGH":  {"metric": "DVG",  "threshold": 0.60, "direction": "above"},
        "ALERT_INT_HIGH":  {"metric": "INT",  "threshold": 0.70, "direction": "above"},
        "ALERT_TBF_SKEW":  {"metric": "TBF",  "threshold": 0.40, "direction": "above"},
    },
}

# ---------------------------------------------------------------------------
# Risk → Alert crosswalk (Layer 2 → Layer 3 names)
# ---------------------------------------------------------------------------

RISK_TO_ALERT: dict = {
    "R_fix":  ["ALERT_INT_HIGH", "ALERT_DRIFT"],
    "R_esc":  ["ALERT_DA_RISING", "ALERT_CM_HIGH"],
    "R_stag": ["ALERT_DRIFT", "ALERT_DA_RISING"],
    "R_loop": ["ALERT_INT_HIGH"],
}

# ---------------------------------------------------------------------------
# Freeze / diff utilities
# ---------------------------------------------------------------------------

def freeze(matrix: dict) -> dict:
    """Return an immutable-stamped copy of a matrix dict.

    Adds a ``_sha256`` field over the canonical JSON representation so
    callers can detect weight drift between versions.
    """
    copy_ = copy.deepcopy(matrix)
    canonical = json.dumps(copy_, sort_keys=True, separators=(",", ":"))
    copy_["_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()[:16]
    return copy_


def diff(matrix_a: dict, matrix_b: dict) -> dict:
    """Return {metric: (weight_a, weight_b)} for weights that changed."""
    changes = {}
    rows_a = matrix_a.get("metrics", {})
    rows_b = matrix_b.get("metrics", {})
    all_metrics = set(rows_a) | set(rows_b)
    for metric in all_metrics:
        row_a = rows_a.get(metric, {})
        row_b = rows_b.get(metric, {})
        all_prims = set(row_a) | set(row_b)
        for prim in all_prims:
            wa = row_a.get(prim)
            wb = row_b.get(prim)
            if wa != wb:
                changes[(metric, prim)] = (wa, wb)
    return changes
