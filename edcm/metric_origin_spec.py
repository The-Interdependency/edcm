"""Source-owned semantic specifications for EDCM metric-origin construction.

Semantic words define what an instrument is about. Declared and implemented
measurement rules are recorded separately so implementation drift cannot alter
the semantic origin silently. None of these words are observation evidence.
"""

# === MODULE_BUILD ===
# id: edcm_metric_origin_specs_v0
#   module_name: metric_origin_spec
#   module_kind: schema
#   summary: exposes provenance-bearing semantic source text and rule-alignment state for EDCM metric-origin construction
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
#   unresolved: O and L semantic labels conflict between maintained compute code and marker canon
# === END MODULE_BUILD ===

from __future__ import annotations
from dataclasses import dataclass
from types import MappingProxyType

SCHEMA = "edcm.metric-origin-spec"
VERSION = "0.3.0"

@dataclass(frozen=True, slots=True)
class MetricOriginSpec:
    metric_id: str
    surface_terms: tuple[str, ...]
    construction_terms: tuple[str, ...]
    semantic_definition: str
    declared_rule: str
    implemented_rule: str
    source_refs: tuple[str, ...]
    standing: str
    measurement_alignment: str
    unresolved: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "surface_terms", tuple(self.surface_terms))
        object.__setattr__(self, "construction_terms", tuple(self.construction_terms))
        object.__setattr__(self, "source_refs", tuple(self.source_refs))
        object.__setattr__(self, "unresolved", tuple(self.unresolved))
        for label, value in (
            ("metric_id", self.metric_id), ("semantic_definition", self.semantic_definition),
            ("declared_rule", self.declared_rule), ("implemented_rule", self.implemented_rule),
            ("standing", self.standing), ("measurement_alignment", self.measurement_alignment),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{label} must be non-empty")
        for label, values in (
            ("surface_terms", self.surface_terms), ("construction_terms", self.construction_terms), ("source_refs", self.source_refs),
            ("unresolved", self.unresolved),
        ):
            if any(not isinstance(x, str) or not x.strip() for x in values):
                raise ValueError(f"{label} must contain only non-empty strings")
        if not self.surface_terms or not self.source_refs:
            raise ValueError("surface_terms and source_refs must be non-empty")
        if self.standing == "resolved" and not self.construction_terms:
            raise ValueError("resolved metric origins require construction_terms")
        if self.standing not in {"resolved", "hmmm"}:
            raise ValueError("standing must be resolved or hmmm")
        if self.measurement_alignment not in {"aligned", "proxy", "conflict", "hmmm"}:
            raise ValueError("unsupported measurement_alignment")
        if self.standing == "hmmm" and not self.unresolved:
            raise ValueError("hmmm standing requires a non-empty unresolved reason")

_SPECS = {
    "C": MetricOriginSpec("C", ("Constraint Strain",), ("constraint","strain","contradiction","pressure"),
        "constraint strain is pressure produced by contradiction within the measured window",
        "weighted contradiction density",
        "explicit-contradiction marker hits divided by max one or token count over ten",
        ("edcm/measurement/canon/data/markers_v1.json#C","edcm/measurement/metrics/compute.py#_compute_C"),
        "resolved","proxy",("implicit contradiction semantics are not measured by the maintained proxy",)),
    "R": MetricOriginSpec("R", ("Refusal Density",), ("refusal","density","refusal","constraint"),
        "refusal density is the concentration of refusal relative to active constraint statements",
        "count refusal markers divided by constraint statements",
        "refusal marker hits divided by max one or token count over ten",
        ("edcm/measurement/canon/data/markers_v1.json#R","edcm/measurement/metrics/compute.py#_compute_R"),
        "resolved","proxy",("implemented denominator is token-count scale, not counted constraint statements",)),
    "F": MetricOriginSpec("F", ("Fixation",), ("fixation","persistence","repetition"),
        "fixation is persistence of substantially the same constraint-bearing pattern across successive states",
        "semantic similarity between consecutive constraint expressions",
        "weighted repetition, repeated trigram density, and inverse token novelty",
        ("edcm/measurement/canon/data/markers_v1.json#F","edcm/measurement/metrics/risk.py#fixation_risk"),
        "resolved","proxy",("maintained implementation is a lexical structural proxy, not embedding similarity",)),
    "E": MetricOriginSpec("E", ("Escalation",), ("escalation","increase","commitment","intensity"),
        "escalation is positive change in commitment or constraint intensity across sequence",
        "positive derivative of commitment intensity",
        "zero point six refusal proxy plus zero point four loop-risk proxy",
        ("edcm/measurement/canon/data/markers_v1.json#E","edcm/measurement/metrics/compute.py#_compute_E"),
        "resolved","proxy",("maintained implementation does not directly compute commitment-intensity derivative",)),
    "D": MetricOriginSpec("D", ("Deflection",), ("deflection","movement","away","constraint"),
        "deflection is movement away from the active constraint-bearing subject or relation",
        "one minus constraint-relevant token share",
        "one minus bag-of-words cosine similarity with the prior round",
        ("edcm/measurement/canon/data/markers_v1.json#D","edcm/measurement/metrics/compute.py#_compute_D"),
        "resolved","proxy",("prior-round lexical overlap substitutes for active-constraint topic tracking",)),
    "N": MetricOriginSpec("N", ("Noise",), ("noise","repetition","without","resolution"),
        "noise is activity that consumes representational space without proportionate constraint resolution",
        "one minus resolution tokens divided by constraint tokens",
        "zero point six repetition plus zero point four inverse normalized token entropy",
        ("edcm/measurement/canon/data/markers_v1.json#N","edcm/measurement/metrics/compute.py#_compute_N"),
        "resolved","proxy",("maintained implementation measures repetition and entropy rather than resolution ratio",)),
    "I": MetricOriginSpec("I", ("Integration Failure",), ("integration","failure","correction","change"),
        "integration failure is failure of a correction or newly supplied constraint to alter subsequent behavior accordingly",
        "one minus similarity between correction response and expected response",
        "correction-offered marker hits divided by max one or token count over ten",
        ("edcm/measurement/canon/data/markers_v1.json#I","edcm/measurement/metrics/compute.py#_compute_I"),
        "resolved","proxy",("maintained implementation does not observe subsequent integration behavior",)),
    "O": MetricOriginSpec("O", ("Overextension","Overconfidence"), (),
        "O has conflicting maintained semantic names and therefore has no closed semantic origin yet",
        "expansion beyond original scope per window",
        "first marker category versus second marker category mapped onto minus one to plus one and documented as overconfidence",
        ("edcm/measurement/canon/data/markers_v1.json#O","edcm/measurement/metrics/compute.py#_compute_O"),
        "hmmm","conflict",("marker canon says Overextension; compute.py says Overconfidence",)),
    "L": MetricOriginSpec("L", ("Load","Coherence Loss"), (),
        "L has conflicting maintained semantic names and therefore has no closed semantic origin yet",
        "total constraint tokens per window",
        "half repetition plus half inverse novelty relative to the prior round",
        ("edcm/measurement/canon/data/markers_v1.json#L","edcm/measurement/metrics/compute.py#_compute_L"),
        "hmmm","conflict",("marker canon says Load; compute.py says Coherence Loss",)),
    "P": MetricOriginSpec("P", ("Progress",), ("progress","novelty","change","resolution"),
        "progress is newly integrated information or state change that advances resolution relative to the prior state",
        "hmmm: no markers-v1 rule",
        "zero point six token novelty plus zero point four positive entropy-gain proxy",
        ("edcm/measurement/metrics/compute.py#_compute_P",),
        "resolved","proxy",("progress is explicitly implemented as a proxy",)),
    "kappa": MetricOriginSpec("kappa", ("Stored Tension",), ("stored","tension","unresolved","conflict"),
        "stored tension is unresolved dissonance carried forward as circuit state",
        "persistent circuit state",
        "clamped alpha times prior kappa plus dissonance minus bounded resolution",
        ("edcm/measurement/metrics/compute.py#energy_step",),
        "resolved","proxy",("resolution function is currently approximated from dissonance",)),
}
METRIC_ORIGIN_SPECS = MappingProxyType(_SPECS)

def metric_origin_spec(metric_id: str) -> MetricOriginSpec:
    try:
        return METRIC_ORIGIN_SPECS[metric_id]
    except KeyError as exc:
        raise KeyError(f"unknown EDCM metric origin {metric_id!r}") from exc

__all__ = ["SCHEMA","VERSION","MetricOriginSpec","METRIC_ORIGIN_SPECS","metric_origin_spec"]
