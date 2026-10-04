"""Bind EDCM scalar readouts to independently constructed semantic origins.

This adapter does not compute semantic distance. It preserves the measurement
value, evidence identity, and Stack origin-set receipt together so a later
lawful projection can compare observed structure to the metric origin.
"""

# === MODULE_BUILD ===
# id: edcm_semantic_metric_space_v0
#   module_name: semantic_metric_space
#   module_kind: adapter
#   summary: binds the 11-component EDCM vector to provenance-bearing Stack semantic metric origins without inventing a semantic distance law
#   owner: Erin Spencer
#   public_surface: MetricOriginBinding, SemanticMetricReadout, SemanticMetricSpace, build_semantic_metric_space, bind_round_metrics
#   internal_surface: strict Stack-origin receipt validation
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_semantic_metric_space.py
#   rollout: candidate adapter; existing scalar computation unchanged
#   rollback: remove adapter; existing RoundMetrics remain authoritative measurement output
#   requires: edcm_metric_origin_specs_v0, external Stack metric-origin-set receipts
#   since: 2026-10-03
#   unresolved: lawful semantic projection/distance from observed construct to origin set
# === END MODULE_BUILD ===

from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping

VECTOR_ORDER = ("C","R","F","E","D","N","I","O","L","P","kappa")
STACK_ORIGIN_SCHEMA = "english-gonol.edcm-metric-origin-set"
STACK_ORIGIN_VERSION = "0.2.0"

@dataclass(frozen=True, slots=True)
class MetricOriginBinding:
    metric_id: str
    origin_receipt_sha256: str
    closed: bool
    unresolved: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class SemanticMetricSpace:
    bindings: tuple[MetricOriginBinding, ...]
    complete: bool
    unresolved_metrics: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class SemanticMetricReadout:
    metric_id: str
    value: float
    origin_receipt_sha256: str
    evidence_receipt: str
    semantic_projection: str
    origin_closed: bool
    unresolved: tuple[str, ...]

def _origin_binding(metric_id: str, record: Mapping[str, object]) -> MetricOriginBinding:
    if record.get("schema") != STACK_ORIGIN_SCHEMA or record.get("version") != STACK_ORIGIN_VERSION:
        raise ValueError(f"{metric_id}: unsupported Stack metric-origin schema")
    if record.get("metric_id") != metric_id:
        raise ValueError(f"{metric_id}: origin metric identity mismatch")
    receipt = record.get("receipt_sha256")
    if not isinstance(receipt, str) or len(receipt) != 64:
        raise ValueError(f"{metric_id}: invalid origin receipt")
    closed = record.get("closed")
    if type(closed) is not bool:
        raise ValueError(f"{metric_id}: closed must be bool")
    unresolved_raw = record.get("unresolved", [])
    if not isinstance(unresolved_raw, list) or any(not isinstance(x,str) or not x for x in unresolved_raw):
        raise ValueError(f"{metric_id}: unresolved must be a string list")
    return MetricOriginBinding(metric_id, receipt, closed, tuple(unresolved_raw))

def build_semantic_metric_space(
    origins: Mapping[str, Mapping[str, object]],
) -> SemanticMetricSpace:
    if tuple(origins.keys()) != VECTOR_ORDER:
        raise ValueError("origin mapping must follow the exact EDCM vector order")
    bindings = tuple(_origin_binding(metric_id, origins[metric_id]) for metric_id in VECTOR_ORDER)
    unresolved = tuple(binding.metric_id for binding in bindings if not binding.closed)
    return SemanticMetricSpace(bindings, not unresolved, unresolved)

def bind_round_metrics(metrics: object, space: SemanticMetricSpace, *, evidence_receipt: str) -> tuple[SemanticMetricReadout, ...]:
    if not isinstance(evidence_receipt, str) or not evidence_receipt:
        raise ValueError("evidence_receipt must be non-empty")
    out = []
    for binding in space.bindings:
        raw = getattr(metrics, binding.metric_id)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            raise ValueError(f"{binding.metric_id}: scalar metric value required")
        out.append(SemanticMetricReadout(
            metric_id=binding.metric_id,
            value=float(raw),
            origin_receipt_sha256=binding.origin_receipt_sha256,
            evidence_receipt=evidence_receipt,
            semantic_projection="hmmm",
            origin_closed=binding.closed,
            unresolved=binding.unresolved + (
                "lawful observed-construct -> semantic-origin projection not yet established",
            ),
        ))
    return tuple(out)

__all__ = ["VECTOR_ORDER","MetricOriginBinding","SemanticMetricReadout","SemanticMetricSpace",
           "build_semantic_metric_space","bind_round_metrics"]
