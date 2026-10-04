"""Source-owned semantic specifications for EDCM metric origin construction.

The words here define the intended semantic origin of an instrument. They are
not observations and cannot by themselves make a metric fire. Stack language
construction may consume these specs; EDCM remains measurement authority.
"""

# === MODULE_BUILD ===
# id: edcm_metric_origin_specs_v0
#   module_name: metric_origin_spec
#   module_kind: schema
#   summary: exposes provenance-bearing semantic source text for EDCM metric-origin construction
#   owner: Erin Spencer
#   public_surface: MetricOriginSpec, METRIC_ORIGIN_SPECS, metric_origin_spec
#   internal_surface: immutable source registry
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_metric_origin_spec.py
#   rollout: candidate semantic instrument specification
#   rollback: remove module and dependent Stack origin constructions
#   requires: edcmbone_metrics_compute, edcmbone_canon_loader
#   since: 2026-10-03
#   unresolved: O and L labels conflict between maintained compute code and marker canon
# === END MODULE_BUILD ===

from __future__ import annotations
from dataclasses import dataclass

SCHEMA = "edcm.metric-origin-spec"
VERSION = "0.1.0"

@dataclass(frozen=True, slots=True)
class MetricOriginSpec:
    metric_id: str
    surface_terms: tuple[str, ...]
    defining_statement: str
    formula_or_rule: str
    source_refs: tuple[str, ...]
    standing: str
    unresolved: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "surface_terms", tuple(self.surface_terms))
        object.__setattr__(self, "source_refs", tuple(self.source_refs))
        object.__setattr__(self, "unresolved", tuple(self.unresolved))
        for label, value in (
            ("metric_id", self.metric_id),
            ("defining_statement", self.defining_statement),
            ("formula_or_rule", self.formula_or_rule),
            ("standing", self.standing),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{label} must be non-empty")
        if not self.surface_terms or any(not x.strip() for x in self.surface_terms):
            raise ValueError("surface_terms must be non-empty strings")
        if not self.source_refs or any(not x.strip() for x in self.source_refs):
            raise ValueError("source_refs must be non-empty strings")
        if self.standing not in {"resolved", "hmmm"}:
            raise ValueError("standing must be resolved or hmmm")
        if self.standing == "hmmm" and not self.unresolved:
            raise ValueError("hmmm standing requires an unresolved reason")

METRIC_ORIGIN_SPECS = {
    "C": MetricOriginSpec("C", ("Constraint Strain",),
        "constraint strain is pressure produced by contradiction within the measured window",
        "weighted contradiction density",
        ("edcm/measurement/canon/data/markers_v1.json#C", "edcm/measurement/metrics/compute.py#RoundMetrics.C"),
        "resolved"),
    "R": MetricOriginSpec("R", ("Refusal Density",),
        "refusal density is the concentration of refusal relative to active constraint statements",
        "count(refusal markers) / constraint statements",
        ("edcm/measurement/canon/data/markers_v1.json#R", "edcm/measurement/metrics/compute.py#RoundMetrics.R"),
        "resolved"),
    "F": MetricOriginSpec("F", ("Fixation",),
        "fixation is persistence of substantially the same constraint-bearing pattern across successive states",
        "semantic or structural persistence across consecutive constraint expressions",
        ("edcm/measurement/canon/data/markers_v1.json#F", "edcm/measurement/metrics/compute.py#RoundMetrics.F"),
        "resolved"),
    "E": MetricOriginSpec("E", ("Escalation",),
        "escalation is positive change in commitment or constraint intensity across sequence",
        "positive derivative of commitment intensity",
        ("edcm/measurement/canon/data/markers_v1.json#E", "edcm/measurement/metrics/compute.py#RoundMetrics.E"),
        "resolved"),
    "D": MetricOriginSpec("D", ("Deflection",),
        "deflection is movement away from the active constraint-bearing subject or relation",
        "one minus constraint-relevant share or a declared comparison proxy",
        ("edcm/measurement/canon/data/markers_v1.json#D", "edcm/measurement/metrics/compute.py#RoundMetrics.D"),
        "resolved"),
    "N": MetricOriginSpec("N", ("Noise",),
        "noise is activity that consumes representational space without proportionate constraint resolution",
        "one minus resolution relative to constraint load, with declared structural proxies",
        ("edcm/measurement/canon/data/markers_v1.json#N", "edcm/measurement/metrics/compute.py#RoundMetrics.N"),
        "resolved"),
    "I": MetricOriginSpec("I", ("Integration Failure",),
        "integration failure is failure of a correction or newly supplied constraint to alter subsequent behavior accordingly",
        "one minus correction integration similarity or a declared proxy",
        ("edcm/measurement/canon/data/markers_v1.json#I", "edcm/measurement/metrics/compute.py#RoundMetrics.I"),
        "resolved"),
    "O": MetricOriginSpec("O", ("Overextension", "Overconfidence"),
        "O has conflicting maintained semantic names and therefore has no closed semantic origin yet",
        "hmmm",
        ("edcm/measurement/canon/data/markers_v1.json#O", "edcm/measurement/metrics/compute.py#RoundMetrics.O"),
        "hmmm", ("marker canon says Overextension; compute.py says Overconfidence",)),
    "L": MetricOriginSpec("L", ("Load", "Coherence Loss"),
        "L has conflicting maintained semantic names and therefore has no closed semantic origin yet",
        "hmmm",
        ("edcm/measurement/canon/data/markers_v1.json#L", "edcm/measurement/metrics/compute.py#RoundMetrics.L"),
        "hmmm", ("marker canon says Load; compute.py says Coherence loss",)),
    "P": MetricOriginSpec("P", ("Progress",),
        "progress is newly integrated information or state change that advances resolution relative to the prior state",
        "novelty plus entropy-gain proxy in the maintained implementation",
        ("edcm/measurement/metrics/compute.py#RoundMetrics.P",),
        "resolved"),
    "kappa": MetricOriginSpec("kappa", ("Stored Tension",),
        "stored tension is unresolved dissonance carried forward as circuit state",
        "persistent circuit state updated by energy_step",
        ("edcm/measurement/metrics/compute.py#RoundMetrics.kappa",),
        "resolved"),
}

def metric_origin_spec(metric_id: str) -> MetricOriginSpec:
    try:
        return METRIC_ORIGIN_SPECS[metric_id]
    except KeyError as exc:
        raise KeyError(f"unknown EDCM metric origin {metric_id!r}") from exc

__all__ = ["SCHEMA", "VERSION", "MetricOriginSpec", "METRIC_ORIGIN_SPECS", "metric_origin_spec"]
