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
    """Import from ucns/edcmbone when present, otherwise create defaults."""

    semantics = _maybe_from_ucns() or DefaultSemanticsLayer()
    measurement = _maybe_from_edcmbone() or DefaultMeasurementLayer()
    return EDCMLayers(
        semantics=semantics,
        measurement=measurement,
        composition=DefaultCompositionLayer(),
        delivery=DefaultDeliveryLayer(),
    )
