"""
edcmbone.metrics.compute
~~~~~~~~~~~~~~~~~~~~~~~~
Computes the EDCM metric vector M_t and dissonance energy for a round.

Layer designation
-----------------
Decision: A — behavioral/orchestration layer, not Operator L0.

This module is retained temporarily inside edcmbone for compatibility, but
canonically belongs upstream in the future `edcm` package. It consumes parsed
round text, token statistics, marker phrases, and prior-round comparisons. It
may carry `bone_count` through its result container for audit continuity, but it
does not compute the L0 Operator vector and must not be treated as the
bones-only Operator substrate.

The L0 Operator entry point remains separate: `core/operator/operator_extractor.py`.

The metric vector M_t ∈ ℝ^11 covers:
  C  Constraint strain     [0,1]
  R  Refusal density       [0,1]
  F  Fixation              [0,1]
  E  Escalation            [0,1]
  D  Deflection            [0,1]
  N  Noise                 [0,1]
  I  Integration failure   [0,1]
  O  Overconfidence        [-1,1]
  L  Coherence loss        [0,1]
  P  Progress              [0,1]
  k  Stored tension        κ ∈ [0, 1]

Most metrics are partially computable from markers (phrase-level signals).
Some require embeddings / cross-turn semantic comparison (marked below).

Public API
----------
RoundMetrics          — data class holding all computed values
compute_round(round_, prev_round, canon, alpha, delta_max[, prev_kappa, prev_entropy]) -> RoundMetrics
energy_step(prev_kappa, dissonance, alpha, delta_max)      -> (E_t, s_t)
energy_step(prev_energy, prev_kappa, dissonance, ...)      -> (E_t, s_t)  # legacy
"""

# === MODULE_BUILD ===
# id: edcmbone_metrics_compute
#   module_name: compute
#   module_kind: engine
#   summary: computes the EDCM metric vector M_t and dissonance energy for a parsed round/transcript
#   owner: Erin Spencer
#   public_surface: RoundMetrics,compute_round,compute_transcript,energy_step
#   internal_surface: _compute_R,_compute_F,_compute_L,_compute_N,_compute_P,_compute_O,_compute_I,_compute_C,_compute_D,_compute_E,_build_phrase_patterns,_count_marker_hits
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_metrics_layer_designation
#   rollout: default_enabled
#   rollback: remove module; no behavioral metric vector produced
#   requires: edcmbone_metrics_stats,edcmbone_metrics_risk,edcmbone_canon_loader
#   since: 2026-06-02
#   unresolved: per its own docstring this layer-A module canonically belongs upstream in the future edcm package
# === END MODULE_BUILD ===


from __future__ import annotations

import re

from ..canon import CanonLoader
from ..parser.turns_rounds import Round

from .stats import (
    clamp,
    tokenize,
    ttr,
    repetition_ratio,
    shannon_entropy,
    novelty,
    cosine_sim,
    rep_ngram_density,
    pattern_density,
)
from .risk import fixation_risk, loop_risk


# ---------------------------------------------------------------------------
# Layer contract
# ---------------------------------------------------------------------------

LAYER_DECISION = "A_BEHAVIORAL_ORCHESTRATION"
LAYER_DESIGNATION = "L1_L2_L3_ORCHESTRATOR_PENDING_EDCM_MIGRATION"
LAYER_INPUT_SUBSTRATE = "round_text_tokens_marker_stats_prior_round_context"
OPERATOR_LAYER_SUBSTRATE = "bones_only"
OPERATES_ON_OPERATOR_BONES = False
CONSUMES_BONE_COUNT_FOR_AUDIT = True
MIGRATION_TARGET = "edcm"
OPERATOR_ENTRYPOINT = "core.operator.operator_extractor"


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------

class RoundMetrics:
    """Metric vector M_t for one round.

    Attributes
    ----------
    C : Constraint strain       — partial (markers)
    R : Refusal density         — yes (markers)
    F : Fixation                — yes (stats)
    E : Escalation              — partial (stats + markers)
    D : Deflection              — partial (requires embeddings for full)
    N : Noise                   — yes (stats)
    I : Integration failure     — partial (markers)
    O : Overconfidence          — partial (markers)
    L : Coherence loss          — yes (stats)
    P : Progress                — proxy (novelty + entropy gain)
    kappa : Stored tension      — circuit state (from energy_step)

    dissonance_energy : E_t for this round
    """

    __slots__ = (
        "C", "R", "F", "E", "D", "N", "I", "O", "L", "P",
        "kappa", "dissonance_energy",
        "round_index", "token_count", "bone_count",
    )

    def __init__(self, **kwargs):
        for k in self.__slots__:
            default = 0 if k in ("round_index", "token_count", "bone_count") else 0.0
            setattr(self, k, kwargs.get(k, default))

    def as_dict(self):
        return {k: getattr(self, k) for k in self.__slots__}

    def vector(self):
        """Return the 11-component metric vector as a list [C,R,F,E,D,N,I,O,L,P,kappa]."""
        return [self.C, self.R, self.F, self.E, self.D,
                self.N, self.I, self.O, self.L, self.P, self.kappa]

    def __repr__(self):
        fields = ", ".join(
            "{}={:.3f}".format(k, getattr(self, k))
            for k in ("C", "R", "F", "E", "D", "N", "I", "O", "L", "P", "kappa")
        )
        return "RoundMetrics({})".format(fields)


# ---------------------------------------------------------------------------
# Marker phrase matching helpers
# ---------------------------------------------------------------------------

def _build_phrase_patterns(canon, metric, category):
    """Return a compiled regex that matches any phrase in a marker category."""
    try:
        phrases = canon.marker_phrases(metric, category)
    except KeyError:
        return None
    escaped = [re.escape(p.lower()) for p in phrases if isinstance(p, str)]
    if not escaped:
        return None
    return re.compile(r"(?:" + "|".join(escaped) + r")", re.IGNORECASE)


def _count_marker_hits(text, pattern):
    if pattern is None or not text:
        return 0
    return len(pattern.findall(text))


# ---------------------------------------------------------------------------
# Circuit dynamics
# ---------------------------------------------------------------------------

def energy_step(*args, dissonance=None, alpha=0.85, delta_max=0.3):
    """Compute one step of the RC-circuit energy model.

    s_{t+1} = alpha * s_t + E_t - delta_t
    delta_t  = min(delta_max, g(y_t, y_{t-1}))

    Here g is approximated as delta_max * (1 - dissonance), i.e. the
    system resolves more when dissonance is lower.

    Supports both current and legacy call signatures:
      - energy_step(prev_kappa, dissonance, alpha=..., delta_max=...)
      - energy_step(prev_energy, prev_kappa, dissonance=..., alpha=..., delta_max=...)

    `prev_energy` is accepted for backward compatibility and ignored.
    Returns (E_t, s_{t+1}).
    """
    if len(args) == 2:
        # Current signature: (prev_kappa, dissonance)
        prev_kappa, resolved_dissonance = args
    elif len(args) == 3:
        # Legacy positional form: (prev_energy, prev_kappa, dissonance)
        _, prev_kappa, resolved_dissonance = args
    elif len(args) == 4:
        # Current 4-positional form: (prev_kappa, dissonance, alpha, delta_max)
        prev_kappa, resolved_dissonance, alpha, delta_max = args
    elif len(args) == 0:
        prev_kappa = None
        resolved_dissonance = dissonance
    else:
        raise TypeError("energy_step accepts 2, 3, or 4 positional arguments")

    if dissonance is not None:
        resolved_dissonance = dissonance

    if prev_kappa is None or resolved_dissonance is None:
        raise TypeError("energy_step requires prev_kappa and dissonance")

    g = delta_max * max(0.0, 1.0 - resolved_dissonance)
    delta = min(delta_max, g)
    new_kappa = clamp(alpha * prev_kappa + resolved_dissonance - delta)
    return resolved_dissonance, new_kappa


# ---------------------------------------------------------------------------
# Per-metric computation
# ---------------------------------------------------------------------------

def _compute_R(round_text, canon):
    """Refusal density — fully computable from markers."""
    info = canon.metric_info("R")
    cats = list(info["markers"].keys())
    refusal_pat = _build_phrase_patterns(canon, "R", cats[0]) if cats else None
    n_refusals = _count_marker_hits(round_text, refusal_pat)
    # Normalise by rough token count
    tokens = tokenize(round_text)
    if not tokens:
        return 0.0
    return clamp(n_refusals / max(1, len(tokens) / 10))


def _compute_F(tokens_b, tokens_a):
    """Fixation — stat-based."""
    return fixation_risk(tokens_b, tokens_a)


def _compute_L(tokens_b, tokens_a):
    """Coherence loss — repetition + loss of novelty."""
    rep = repetition_ratio(tokens_b)
    nov = novelty(tokens_b, tokens_a) if tokens_a else 0.5
    return clamp(0.5 * rep + 0.5 * (1.0 - nov))


def _compute_N(tokens_b):
    """Noise — high repetition + low entropy."""
    if not tokens_b:
        return 0.0
    rep = repetition_ratio(tokens_b)
    h = shannon_entropy(tokens_b)
    # Normalise entropy: English text ~ 10 bits max for short texts
    h_norm = clamp(h / 10.0)
    return clamp(0.6 * rep + 0.4 * (1.0 - h_norm))


def _compute_P(tokens_b, tokens_a, h_prev):
    """Progress proxy — novelty + entropy gain over previous round."""
    nov = novelty(tokens_b, tokens_a) if tokens_a else 0.5
    h_curr = shannon_entropy(tokens_b)
    h_gain = clamp((h_curr - h_prev) / max(h_prev, 1e-9)) if h_prev > 0 else 0.5
    return clamp(0.6 * nov + 0.4 * h_gain)


def _compute_O(round_text, canon):
    """Overconfidence — marker-based, range [-1, 1].

    Positive = overconfident; negative = under-confident.
    """
    info = canon.metric_info("O")
    cats = list(info["markers"].keys())
    tokens = tokenize(round_text)
    if not tokens:
        return 0.0
    over_pat = _build_phrase_patterns(canon, "O", cats[0]) if len(cats) > 0 else None
    under_pat = _build_phrase_patterns(canon, "O", cats[1]) if len(cats) > 1 else None
    n_over = _count_marker_hits(round_text, over_pat)
    n_under = _count_marker_hits(round_text, under_pat)
    total = n_over + n_under
    if total == 0:
        return 0.0
    return clamp(n_over / total) * 2.0 - 1.0  # map [0,1] -> [-1,1]


def _compute_I(round_text, canon):
    """Integration failure — marker-based."""
    info = canon.metric_info("I")
    cats = list(info["markers"].keys())
    pat = _build_phrase_patterns(canon, "I", cats[0]) if cats else None
    tokens = tokenize(round_text)
    if not tokens:
        return 0.0
    hits = _count_marker_hits(round_text, pat)
    return clamp(hits / max(1, len(tokens) / 10))


def _compute_C(round_text, canon):
    """Constraint strain — partial marker approximation."""
    info = canon.metric_info("C")
    cats = list(info["markers"].keys())
    pat = _build_phrase_patterns(canon, "C", cats[0]) if cats else None
    tokens = tokenize(round_text)
    if not tokens:
        return 0.0
    hits = _count_marker_hits(round_text, pat)
    return clamp(hits / max(1, len(tokens) / 10))


def _compute_D(tokens_b, tokens_a, round_text, canon):
    """Deflection — partial; 1 - cosine similarity with prior round as proxy.

    Low cosine overlap with the prior round is treated as deflection:
    high similarity = on-topic = low deflection.
    """
    if not tokens_a:
        return 0.0
    cos = cosine_sim(tokens_b, tokens_a)
    # High similarity to prior = on-topic = low deflection
    return clamp(1.0 - cos)


def _compute_E(round_text, tokens_b, tokens_a, canon):
    """Escalation — refusal density + loop risk."""
    r = _compute_R(round_text, canon)
    lp = loop_risk(tokens_a, tokens_b) if tokens_a else 0.0
    return clamp(0.6 * r + 0.4 * lp)


# ---------------------------------------------------------------------------
# Public compute function
# ---------------------------------------------------------------------------

def compute_round(round_, prev_round=None,
                  canon=None,
                  alpha=0.85, delta_max=0.3,
                  prev_kappa=0.0, prev_entropy=0.0):
    """Compute the metric vector for a Round.

    Parameters
    ----------
    round_      : Round object from the parser
    prev_round  : Round object for the previous round (or None for first round)
    canon       : CanonLoader (created fresh if None)
    alpha       : persistence coefficient for the RC circuit [0, 1]
    delta_max   : max resolution rate per step [0, 1]
    prev_kappa  : stored tension from previous step (κ_{t-1})
    prev_entropy: Shannon entropy of previous round (for progress computation)

    Returns
    -------
    RoundMetrics
    """
    if canon is None:
        canon = CanonLoader()

    # Collect text and tokens for this round
    round_text = " ".join(t.text for t in round_.turns)
    tokens_b = tokenize(round_text)

    tokens_a = []
    if prev_round is not None:
        prev_text = " ".join(t.text for t in prev_round.turns)
        tokens_a = tokenize(prev_text)

    # Compute each metric
    C = _compute_C(round_text, canon)
    R = _compute_R(round_text, canon)
    F = _compute_F(tokens_b, tokens_a)
    E = _compute_E(round_text, tokens_b, tokens_a, canon)
    D = _compute_D(tokens_b, tokens_a, round_text, canon)
    N = _compute_N(tokens_b)
    I = _compute_I(round_text, canon)
    O = _compute_O(round_text, canon)
    L = _compute_L(tokens_b, tokens_a)
    P = _compute_P(tokens_b, tokens_a, prev_entropy)

    # Dissonance energy: weighted sum of violations
    # Proxy: mean of constraint-carrying metrics
    dissonance = clamp((C + R + F + E + N + I + L) / 7.0)

    # Circuit dynamics
    _, new_kappa = energy_step(prev_kappa, dissonance, alpha, delta_max)

    return RoundMetrics(
        C=C, R=R, F=F, E=E, D=D, N=N, I=I, O=O, L=L, P=P,
        kappa=new_kappa,
        dissonance_energy=dissonance,
        round_index=round_.index,
        token_count=len(tokens_b),
        bone_count=round_.bone_count,
    )


def compute_transcript(parsed_transcript, canon=None, alpha=0.85, delta_max=0.3):
    """Compute metrics for every round in a ParsedTranscript.

    Returns a list of RoundMetrics in round order.
    """
    if canon is None:
        canon = CanonLoader()

    results = []
    prev_round = None
    prev_kappa = 0.0
    prev_entropy = 0.0

    for rnd in parsed_transcript.rounds:
        m = compute_round(
            rnd,
            prev_round=prev_round,
            canon=canon,
            alpha=alpha,
            delta_max=delta_max,
            prev_kappa=prev_kappa,
            prev_entropy=prev_entropy,
        )
        results.append(m)

        prev_round = rnd
        prev_kappa = m.kappa
        prev_entropy = shannon_entropy(tokenize(" ".join(t.text for t in rnd.turns)))

    return results
