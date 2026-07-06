"""
edcmbone.metrics.risk
~~~~~~~~~~~~~~~~~~~~~
The four risk proxies defined in the EDCM specification (§5).

All return values are clamped to [0, 1].

Functions
---------
fixation_risk(tokens_b, tokens_a)                          -> float
broken_return(tokens_a, tokens_b, tokens_c)                -> float
escalation_risk(tokens_a, tokens_b, tokens_c,
                refusal_density, hedge_density)             -> float
stagnation_risk(refusal_density, tokens_b, tokens_a,
                gain)                                       -> float
loop_risk(tokens_a, tokens_b)                              -> float
"""

# === MODULE_BUILD ===
# id: edcmbone_metrics_risk
#   module_name: risk
#   module_kind: engine
#   summary: the EDCM risk proxies (fixation, broken-return, escalation, stagnation, loop), all clamped to [0,1]
#   owner: Erin Spencer
#   public_surface: fixation_risk, broken_return, escalation_risk, stagnation_risk, loop_risk
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: hmmm
#   rollout: default_enabled
#   rollback: remove module; risk composites unavailable
#   requires: none
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===


from __future__ import annotations

from .stats import (
    clamp,
    cosine_sim,
    jaccard,
    novelty,
    rep_ngram_density,
    repetition_ratio,
)


def fixation_risk(tokens_b, tokens_a):
    """Fixation risk.

    R_fix = clamp(0.3 * RepB + 0.3 * RepNgram(B) + 0.4 * (1 - Novelty(B|A)))

    tokens_b : current response tokens
    tokens_a : previous response tokens
    """
    rep_b = repetition_ratio(tokens_b)
    rep_ngram = rep_ngram_density(tokens_b, n=3)
    nov = novelty(tokens_b, tokens_a)
    return clamp(0.3 * rep_b + 0.3 * rep_ngram + 0.4 * (1.0 - nov))


def broken_return(tokens_a, tokens_b, tokens_c):
    """Broken-return sub-component.

    R_broken = clamp(0.55 * cos(c_A, c_B) + 0.45 * (1 - J(T_C, T_B)))

    tokens_a : original response A
    tokens_b : new response B
    tokens_c : correction/target C
    """
    cos = cosine_sim(tokens_a, tokens_b)
    j = jaccard(set(tokens_c), set(tokens_b))
    return clamp(0.55 * cos + 0.45 * (1.0 - j))


def escalation_risk(tokens_a, tokens_b, tokens_c, refusal_density, hedge_density):
    """Escalation / shutdown risk.

    R_esc = clamp(0.45 * R_broken + 0.35 * rho_refusal/5 + 0.2 * rho_hedge/5)

    tokens_a        : original response tokens
    tokens_b        : new response tokens
    tokens_c        : correction tokens
    refusal_density : rho_refusal (pattern density, per 1000 chars)
    hedge_density   : rho_hedge   (pattern density, per 1000 chars)
    """
    r_broken = broken_return(tokens_a, tokens_b, tokens_c)
    return clamp(
        0.45 * r_broken
        + 0.35 * (refusal_density / 5.0)
        + 0.20 * (hedge_density / 5.0)
    )


def stagnation_risk(refusal_density, tokens_b, tokens_a, gain):
    """Stagnation proxy.

    R_stag = clamp(0.45 * rho_refusal/5 + 0.35 * (1 - Novelty) + 0.2 * (1 - Gain))

    refusal_density : rho_refusal (per 1000 chars)
    tokens_b        : current response tokens
    tokens_a        : previous response tokens
    gain            : unique-gain score in [0, 1]
    """
    nov = novelty(tokens_b, tokens_a)
    return clamp(
        0.45 * (refusal_density / 5.0)
        + 0.35 * (1.0 - nov)
        + 0.20 * (1.0 - gain)
    )


def loop_risk(tokens_a, tokens_b):
    """Repetition loop risk (v0.4).

    R_loop = clamp(0.5 * RepB + 0.3 * RepNgram(B) + 0.2 * cos(c_A, c_B))

    tokens_a : previous response tokens
    tokens_b : current response tokens
    """
    rep_b = repetition_ratio(tokens_b)
    rep_ngram = rep_ngram_density(tokens_b, n=3)
    cos = cosine_sim(tokens_a, tokens_b)
    return clamp(0.5 * rep_b + 0.3 * rep_ngram + 0.2 * cos)
