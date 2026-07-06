# === MODULE_BUILD ===
# id: edcm_layers
#   module_name: layers
#   module_kind: engine
#   summary: EDCM four-layer stack: Protocol interfaces, default implementations, and the build_default_layers bootstrap (optionally bridging ucns/edcmbone)
#   owner: Erin Spencer
#   public_surface: MeasurementLayer, SemanticsLayer, CompositionLayer, DeliveryLayer, DefaultMeasurementLayer, DefaultSemanticsLayer, DefaultCompositionLayer, DefaultDeliveryLayer, ConsolidatedMeasurementLayer, EDCMLayers, build_default_layers
#   internal_surface: _maybe_from_ucns, _maybe_from_edcmbone
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: hmmm
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: none
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class MeasurementLayer(Protocol):
    """Structural/measurement behavior (edcmbone-aligned)."""

    def measure(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...


class SemanticsLayer(Protocol):
    """Concept/ontology behavior (ucns-aligned)."""

    def normalize(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...


class CompositionLayer(Protocol):
    """Cross-layer composition behavior."""

    def compose(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...


class DeliveryLayer(Protocol):
    """App/service delivery behavior."""

    def deliver(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...


class DefaultMeasurementLayer:
    def measure(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"measurement": "default", **payload}


class ConsolidatedMeasurementLayer:
    """Measurement layer backed by the consolidated edcmbone mirror.

    Uses :mod:`edcm.measurement` (parse → compute → project). When the payload
    carries a ``transcript`` string, the full pipeline runs and the result is
    annotated with per-round metric vectors, agent projections, and the
    structural-density F readout; otherwise the payload passes through with
    only the measurement tag, matching the default-layer contract.
    """

    def measure(self, payload: dict[str, Any]) -> dict[str, Any]:
        transcript = payload.get("transcript")
        if not isinstance(transcript, str) or not transcript.strip():
            return {"measurement": "edcm.measurement", **payload}

        from . import measurement as m
        from .measurement import compress as codec

        canon = m.CanonLoader()
        parsed = m.parse_transcript(transcript, canon=canon)
        metrics = m.compute_transcript(parsed, canon=canon)
        projections = m.project_transcript(parsed, metrics)
        stats = codec.compression_stats(transcript, codec.to_bytes(parsed, metrics), parsed)
        return {
            "measurement": "edcm.measurement",
            "rounds": [rm.as_dict() for rm in metrics],
            "agent_metrics": [am.as_dict() for am in projections],
            "alerts": [m.fire_alerts(am) for am in projections],
            "structural_density": stats["structural_density"],
            **payload,
        }


class DefaultSemanticsLayer:
    def normalize(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"semantics": "default", **payload}


class DefaultCompositionLayer:
    def compose(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"composition": "default", **payload}


class DefaultDeliveryLayer:
    def deliver(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"delivery": "default", **payload}


@dataclass(slots=True)
class EDCMLayers:
    """The four executable layers of EDCM.

    1. semantics (UCNS concept handling)
    2. measurement (edcmbone structure/measurement)
    3. composition (integration/orchestration)
    4. delivery (application output)
    """

    semantics: SemanticsLayer
    measurement: MeasurementLayer
    composition: CompositionLayer
    delivery: DeliveryLayer

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self.semantics.normalize(payload)
        state = self.measurement.measure(state)
        state = self.composition.compose(state)
        return self.delivery.deliver(state)


def _maybe_from_ucns() -> SemanticsLayer | None:
    try:
        import ucns  # type: ignore

        if hasattr(ucns, "SemanticsLayer"):
            return ucns.SemanticsLayer()  # type: ignore[no-any-return]
    except Exception:
        return None
    return None


def _maybe_from_edcmbone() -> MeasurementLayer | None:
    try:
        import edcmbone  # type: ignore

        if hasattr(edcmbone, "MeasurementLayer"):
            return edcmbone.MeasurementLayer()  # type: ignore[no-any-return]
    except Exception:
        return None
    return None


def build_default_layers() -> EDCMLayers:
    """Import from ucns/edcmbone when present, otherwise create defaults.

    Measurement resolution order: an installed upstream ``edcmbone`` exposing
    ``MeasurementLayer`` wins (edcmbone remains canonical L0); otherwise the
    consolidated mirror in :mod:`edcm.measurement` provides the real pipeline.
    """

    semantics = _maybe_from_ucns() or DefaultSemanticsLayer()
    measurement = _maybe_from_edcmbone() or ConsolidatedMeasurementLayer()
    return EDCMLayers(
        semantics=semantics,
        measurement=measurement,
        composition=DefaultCompositionLayer(),
        delivery=DefaultDeliveryLayer(),
    )
