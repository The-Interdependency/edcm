"""Bind EDCM scalar readouts to independently constructed semantic origins.

This adapter does not compute semantic distance. It preserves the measurement
value, evidence identity, and Stack origin-set receipt together so a later
lawful projection can compare observed structure to the metric origin.

Usage guidance: see ``docs/semantic-metric-space.md`` for a runnable maintained
RoundMetrics example and the Stack JSON integration path. Input receipts are
externally verified construction records, not authentication or observations.
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
import math
import re
from typing import Mapping

from .metric_origin_spec import metric_origin_spec

VECTOR_ORDER = ("C","R","F","E","D","N","I","O","L","P","kappa")
STACK_ORIGIN_SCHEMA = "english-gonol.edcm-metric-origin-set"
STACK_ORIGIN_VERSION = "0.2.0"

@dataclass(frozen=True, slots=True)
class MetricOriginBinding:
    metric_id: str
    origin_id: str
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
    origin_id: str
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
    origin_id = record.get("origin_id")
    if origin_id != f"O_M({metric_id})":
        raise ValueError(f"{metric_id}: origin identity mismatch")
    receipt = record.get("receipt_sha256")
    if not isinstance(receipt, str) or re.fullmatch(r"[0-9a-fA-F]{64}", receipt) is None:
        raise ValueError(f"{metric_id}: invalid origin receipt")
    closed = record.get("closed")
    if type(closed) is not bool:
        raise ValueError(f"{metric_id}: closed must be bool")
    unresolved_raw = record.get("unresolved", [])
    if not isinstance(unresolved_raw, list) or any(not isinstance(x,str) or not x.strip() for x in unresolved_raw):
        raise ValueError(f"{metric_id}: unresolved must be a string list")
    if not closed and not unresolved_raw:
        raise ValueError(f"{metric_id}: unclosed origin requires an unresolved reason")
    spec = metric_origin_spec(metric_id)
    if closed and spec.standing != "resolved":
        raise ValueError(f"{metric_id}: EDCM semantic origin remains hmmm")
    # Preserve producer-owned conflicts and proxy limitations even if Stack
    # omits them. Construction closure cannot confer measurement validity.
    unresolved = tuple(dict.fromkeys((*unresolved_raw, *spec.unresolved)))
    return MetricOriginBinding(metric_id, origin_id, receipt, closed, unresolved)

def build_semantic_metric_space(
    origins: Mapping[str, Mapping[str, object]],
) -> SemanticMetricSpace:
    if tuple(origins.keys()) != VECTOR_ORDER:
        raise ValueError("origin mapping must follow the exact EDCM vector order")
    bindings = tuple(_origin_binding(metric_id, origins[metric_id]) for metric_id in VECTOR_ORDER)
    unresolved = tuple(binding.metric_id for binding in bindings if not binding.closed)
    return SemanticMetricSpace(bindings, not unresolved, unresolved)

def bind_round_metrics(metrics: object, space: SemanticMetricSpace, *, evidence_receipt: str) -> tuple[SemanticMetricReadout, ...]:
    # These public dataclasses can be constructed without the builder. Rebuild
    # their input contract at the readout boundary before attaching provenance.
    if not isinstance(space, SemanticMetricSpace) or not isinstance(space.bindings, tuple):
        raise ValueError("validated SemanticMetricSpace required")
    if any(not isinstance(binding, MetricOriginBinding) or not isinstance(binding.unresolved, tuple)
           for binding in space.bindings):
        raise ValueError("immutable MetricOriginBinding records required")
    if tuple(binding.metric_id for binding in space.bindings) != VECTOR_ORDER:
        raise ValueError("semantic space must follow the exact EDCM vector order")
    validated = build_semantic_metric_space({
        binding.metric_id: {
            "schema": STACK_ORIGIN_SCHEMA, "version": STACK_ORIGIN_VERSION,
            "metric_id": binding.metric_id, "origin_id": binding.origin_id,
            "receipt_sha256": binding.origin_receipt_sha256,
            "closed": binding.closed, "unresolved": list(binding.unresolved),
        }
        for binding in space.bindings
    })
    if type(space.complete) is not bool or validated != space:
        raise ValueError("semantic space disagrees with validated bindings or completion state")
    if not isinstance(evidence_receipt, str) or not evidence_receipt.strip():
        raise ValueError("evidence_receipt must be non-empty")
    out = []
    for binding in space.bindings:
        raw = getattr(metrics, binding.metric_id, None)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            raise ValueError(f"{binding.metric_id}: scalar metric value required")
        try:
            value = float(raw)
        except OverflowError as exc:
            raise ValueError(f"{binding.metric_id}: finite scalar metric value required") from exc
        if not math.isfinite(value):
            raise ValueError(f"{binding.metric_id}: finite scalar metric value required")
        lower = -1.0 if binding.metric_id == "O" else 0.0
        if not lower <= value <= 1.0:
            raise ValueError(f"{binding.metric_id}: scalar metric value outside [{lower}, 1.0]")
        out.append(SemanticMetricReadout(
            metric_id=binding.metric_id,
            origin_id=binding.origin_id,
            value=value,
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
