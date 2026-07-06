"""
edcmbone.metrics.projection
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Layer 1 → Layer 3 projection: 11 Arc-Style metrics → 6 agent-facing metrics.

Agent-facing 6 (spec.md §3.6):
    CM    Constraint Mismatch
    DA    Dissonance Accumulation
    DRIFT Drift
    DVG   Divergence
    INT   Intensity
    TBF   Turn-Balance Fairness   (Gini on speaker token shares — independent)

All values in [0, 1].

Public API
----------
    AgentMetrics                   — result container
    project(round_metrics, turns)  — Layer 1 + turn list -> AgentMetrics
    gini_tbf(turns)                — Gini coefficient of speaker token shares
    fire_alerts(agent_metrics)     — list of alert name strings that fired
    crosswalk_risk(risk_name)      — alert names for a Layer 2 risk proxy
"""

# === MODULE_BUILD ===
# id: edcmbone_metrics_projection
#   module_name: projection
#   module_kind: engine
#   summary: projects the 11 Layer-1 Arc-Style metrics to the 6 agent-facing metrics (CM, DA, DRIFT, DVG, INT, TBF)
#   owner: Erin Spencer
#   public_surface: AgentMetrics, project, project_transcript, gini_tbf, fire_alerts, crosswalk_risk
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: hmmm
#   rollout: default_enabled
#   rollback: remove module; agent-facing 6-metric view unavailable
#   requires: edcmbone_metrics_matrix
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===


from __future__ import annotations

from .matrix import ALERT_THRESHOLDS, PROJECTION_MAP, RISK_TO_ALERT
from .stats import clamp


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------

class AgentMetrics:
    """Layer 3 agent-facing metric vector.

    All values [0, 1].  TBF is computed from turn token shares (Gini);
    the others are linear projections from Layer 1.
    """

    __slots__ = ("CM", "DA", "DRIFT", "DVG", "INT", "TBF", "round_index")

    def __init__(self, CM, DA, DRIFT, DVG, INT, TBF, round_index=None):
        self.CM = CM
        self.DA = DA
        self.DRIFT = DRIFT
        self.DVG = DVG
        self.INT = INT
        self.TBF = TBF
        self.round_index = round_index

    def as_dict(self):
        return {s: getattr(self, s) for s in self.__slots__}

    def vector(self):
        """[CM, DA, DRIFT, DVG, INT, TBF]"""
        return [self.CM, self.DA, self.DRIFT, self.DVG, self.INT, self.TBF]

    def __repr__(self):
        fields = ", ".join(
            "{}={:.3f}".format(k, getattr(self, k))
            for k in ("CM", "DA", "DRIFT", "DVG", "INT", "TBF")
        )
        return "AgentMetrics({})".format(fields)


# ---------------------------------------------------------------------------
# Gini coefficient for TBF
# ---------------------------------------------------------------------------

def gini_tbf(turns):
    """Gini coefficient of speaker token-share distribution.

    Higher = more imbalanced = less fair.  Returns 0 for 0 or 1 speaker.
    Normalised to [0, 1] (not [0, 1-1/n]).
    """
    from collections import Counter
    # Count tokens per speaker
    speaker_counts = Counter()
    for turn in turns:
        speaker_counts[turn.speaker] += turn.token_count

    values = sorted(speaker_counts.values())
    n = len(values)
    if n <= 1:
        return 0.0
    total = sum(values)
    if total == 0:
        return 0.0

    # Gini = (2 * Σ i*x_i) / (n * Σ x_i) - (n+1)/n  (sorted ascending, 1-indexed)
    weighted_sum = sum((i + 1) * v for i, v in enumerate(values))
    gini = (2 * weighted_sum) / (n * total) - (n + 1) / n
    # Normalise from [0, (n-1)/n] to [0, 1]
    max_gini = (n - 1) / n
    if max_gini == 0:
        return 0.0
    return clamp(gini / max_gini)


# ---------------------------------------------------------------------------
# Projection — Layer 1 → Layer 3
# ---------------------------------------------------------------------------

def project(round_metrics, turns):
    """Map a RoundMetrics (Layer 1) + turn list → AgentMetrics (Layer 3).

    Parameters
    ----------
    round_metrics : RoundMetrics
    turns         : list[Turn] for the same round (needed for TBF)

    Returns
    -------
    AgentMetrics
    """
    w = PROJECTION_MAP["metrics"]

    m = round_metrics
    neg_P = 1.0 - m.P

    CM    = clamp(w["CM"]["C"]    * m.C    + w["CM"]["I"]    * m.I)
    DA    = clamp(w["DA"]["kappa"]* m.kappa+ w["DA"]["E"]    * m.E  + w["DA"]["R"] * m.R)
    DRIFT = clamp(w["DRIFT"]["L"] * m.L    + w["DRIFT"]["neg_P"] * neg_P)
    DVG   = clamp(w["DVG"]["D"]   * m.D    + w["DVG"]["N"]   * m.N)
    INT   = clamp(w["INT"]["E"]   * m.E    + w["INT"]["F"]   * m.F)
    TBF   = gini_tbf(turns)

    return AgentMetrics(
        CM=CM, DA=DA, DRIFT=DRIFT, DVG=DVG, INT=INT, TBF=TBF,
        round_index=round_metrics.round_index,
    )


# ---------------------------------------------------------------------------
# Alert firing — Layer 3 → named alerts
# ---------------------------------------------------------------------------

def fire_alerts(agent_metrics):
    """Return list of alert name strings that exceed their thresholds.

    Uses ALERT_THRESHOLDS from matrix.py.
    """
    fired = []
    for name, spec in ALERT_THRESHOLDS["alerts"].items():
        val = getattr(agent_metrics, spec["metric"])
        if spec["direction"] == "above" and val > spec["threshold"]:
            fired.append(name)
        elif spec["direction"] == "below" and val < spec["threshold"]:
            fired.append(name)
        elif spec["direction"] not in ("above", "below"):
            raise ValueError(
                "Unknown alert direction {!r} for alert {!r}".format(
                    spec["direction"], name
                )
            )
    return fired


def crosswalk_risk(risk_name):
    """Return alert names associated with a Layer 2 risk proxy name.

    Parameters
    ----------
    risk_name : str  e.g. "R_fix", "R_esc", "R_stag", "R_loop"

    Returns
    -------
    list[str]  alert names, empty list if unknown
    """
    return list(RISK_TO_ALERT.get(risk_name, []))


# ---------------------------------------------------------------------------
# Transcript-level projection
# ---------------------------------------------------------------------------

def project_transcript(parsed_transcript, layer1_metrics):
    """Project all rounds of a ParsedTranscript to AgentMetrics.

    Parameters
    ----------
    parsed_transcript : ParsedTranscript
    layer1_metrics    : list[RoundMetrics]  (same length as parsed_transcript.rounds)

    Returns
    -------
    list[AgentMetrics]
    """
    results = []
    for rnd, m in zip(parsed_transcript.rounds, layer1_metrics):
        results.append(project(m, rnd.turns))
    return results
