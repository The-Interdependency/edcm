"""Provenance-bearing EDCM layer assembly.

Usage guidance
--------------
Use :func:`build_default_layers` for the supported package bootstrap. The
measurement implementation is always the maintained ``edcm.measurement``
surface. UCNS is optional: when unavailable the semantics stage is explicitly
``transcript_only``; when available, the EDCM-owned adapter consumes actual
``ucns.UCNSObject`` values supplied as ``ucns_object``.

Every result includes ``layer_provenance`` and ``ucns_integration`` records.
Fallback, compatibility, and unavailable states are never represented only by
a bare ``default`` label.
"""

# === MODULE_BUILD ===
# id: edcm_layers
#   module_name: layers
#   module_kind: engine
#   summary: Provenance-bearing EDCM four-layer stack with canonical local measurement and explicit actual-UCNS or transcript-only semantics selection.
#   owner: Erin Spencer
#   public_surface: LayerProvenance, MeasurementLayer, SemanticsLayer, CompositionLayer, DeliveryLayer, DefaultMeasurementLayer, DefaultSemanticsLayer, DefaultCompositionLayer, DefaultDeliveryLayer, TranscriptOnlySemanticsLayer, UCNSSemanticsLayer, ConsolidatedMeasurementLayer, EDCMLayers, build_default_layers
#   internal_surface: _record_layer, _local_provenance
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: threads caller payloads through deterministic package-local layers
#   admin_only: false
#   tests: tests.test_measurement, tests.test_ucns_adapter
#   rollout: default_enabled
#   rollback: restore prior layer assembly and remove provenance records
#   requires: edcm_ucns_adapter, edcm_measurement
#   since: 2026-06-02
#   unresolved: METAPAT semantic-authority adapter and full shared-stack result envelope
# === END MODULE_BUILD ===

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Protocol

from . import __version__ as EDCM_VERSION
from .ucns_adapter import (
    ActualUCNSAdapter,
    UCNSIntegrationStatus,
    missing_ucns_status,
    select_ucns_adapter,
)


@dataclass(frozen=True)
class LayerProvenance:
    implementation_id: str
    implementation_version: str | None
    source_repository: str
    role: str
    selection: str
    canonical: bool
    unresolved_constraints: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _local_provenance(
    implementation_id: str,
    role: str,
    selection: str,
    *,
    canonical: bool,
    unresolved_constraints: tuple[str, ...] = (),
) -> LayerProvenance:
    return LayerProvenance(
        implementation_id=implementation_id,
        implementation_version=EDCM_VERSION,
        source_repository="https://github.com/The-Interdependency/edcm",
        role=role,
        selection=selection,
        canonical=canonical,
        unresolved_constraints=unresolved_constraints,
    )


def _record_layer(
    payload: Mapping[str, Any],
    layer_name: str,
    provenance: LayerProvenance,
) -> dict[str, Any]:
    state = dict(payload)
    records = dict(state.get("layer_provenance", {}))
    records[layer_name] = provenance.as_dict()
    state["layer_provenance"] = records
    return state


class MeasurementLayer(Protocol):
    provenance: LayerProvenance

    def measure(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...


class SemanticsLayer(Protocol):
    provenance: LayerProvenance

    def normalize(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...


class CompositionLayer(Protocol):
    provenance: LayerProvenance

    def compose(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...


class DeliveryLayer(Protocol):
    provenance: LayerProvenance

    def deliver(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...


class DefaultMeasurementLayer:
    """Explicit unavailable measurement layer retained for manual construction."""

    provenance = _local_provenance(
        "edcm.measurement.unavailable",
        "measurement",
        "unavailable",
        canonical=False,
        unresolved_constraints=("no measurement implementation selected",),
    )

    def measure(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        state["measurement"] = "unavailable"
        return _record_layer(state, "measurement", self.provenance)


class ConsolidatedMeasurementLayer:
    """Canonical maintained measurement layer backed by ``edcm.measurement``."""

    provenance = _local_provenance(
        "edcm.measurement",
        "measurement",
        "canonical",
        canonical=True,
    )

    def measure(self, payload: dict[str, Any]) -> dict[str, Any]:
        transcript = payload.get("transcript")
        state = dict(payload)
        state["measurement"] = "edcm.measurement"

        if not isinstance(transcript, str) or not transcript.strip():
            return _record_layer(state, "measurement", self.provenance)

        from . import measurement as m
        from .measurement import compress as codec

        canon = m.CanonLoader()
        parsed = m.parse_transcript(transcript, canon=canon)
        metrics = m.compute_transcript(parsed, canon=canon)
        projections = m.project_transcript(parsed, metrics)
        stats = codec.compression_stats(transcript, codec.to_bytes(parsed, metrics), parsed)
        state.update(
            rounds=[rm.as_dict() for rm in metrics],
            agent_metrics=[am.as_dict() for am in projections],
            alerts=[m.fire_alerts(am) for am in projections],
            structural_density=stats["structural_density"],
        )
        return _record_layer(state, "measurement", self.provenance)


class TranscriptOnlySemanticsLayer:
    """Explicit local mode used only when the optional UCNS package is absent."""

    def __init__(self, status: UCNSIntegrationStatus | None = None) -> None:
        self._status = status or missing_ucns_status()
        self.provenance = _local_provenance(
            "edcm.semantics.transcript_only",
            "semantics",
            "local_fallback",
            canonical=False,
            unresolved_constraints=(
                "no actual UCNS geometry adapter ran",
                *self._status.unresolved_constraints,
            ),
        )

    def normalize(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        state["semantics"] = "edcm.transcript_only"
        state["ucns_integration"] = self._status.as_dict()
        state.pop("ucns_geometry", None)
        return _record_layer(state, "semantics", self.provenance)


class DefaultSemanticsLayer(TranscriptOnlySemanticsLayer):
    """Backward-compatible name for the explicit transcript-only fallback."""


class UCNSSemanticsLayer:
    """Semantics-stage wrapper around :class:`ActualUCNSAdapter`."""

    def __init__(self, adapter: ActualUCNSAdapter) -> None:
        self._adapter = adapter
        status = adapter.status
        self.provenance = LayerProvenance(
            implementation_id=status.implementation_id,
            implementation_version=status.implementation_version,
            source_repository=status.source_repository,
            role="semantics_geometry_adapter",
            selection=status.selection,
            canonical=True,
            unresolved_constraints=status.unresolved_constraints,
            errors=status.errors,
        )

    def normalize(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self._adapter.normalize(payload)
        return _record_layer(state, "semantics", self.provenance)


class DefaultCompositionLayer:
    provenance = _local_provenance(
        "edcm.composition.local",
        "composition",
        "local_fallback",
        canonical=False,
        unresolved_constraints=("shared-stack composition policy is not yet integrated",),
    )

    def compose(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        state["composition"] = "edcm.local"
        return _record_layer(state, "composition", self.provenance)


class DefaultDeliveryLayer:
    provenance = _local_provenance(
        "edcm.delivery.local",
        "delivery",
        "local_fallback",
        canonical=False,
        unresolved_constraints=("application-specific delivery adapter is not selected",),
    )

    def deliver(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        state["delivery"] = "edcm.local"
        return _record_layer(state, "delivery", self.provenance)


@dataclass(slots=True)
class EDCMLayers:
    """The four executable, provenance-bearing EDCM layers."""

    semantics: SemanticsLayer
    measurement: MeasurementLayer
    composition: CompositionLayer
    delivery: DeliveryLayer

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self.semantics.normalize(payload)
        state = self.measurement.measure(state)
        state = self.composition.compose(state)
        return self.delivery.deliver(state)


def build_default_layers() -> EDCMLayers:
    """Build the supported stack without silent sibling-package substitution.

    EDCM's maintained measurement implementation always runs locally. UCNS is
    selected only through the EDCM-owned adapter. Direct package absence yields
    transcript-only mode; malformed or broken UCNS imports remain visible.
    """

    selection = select_ucns_adapter()
    semantics: SemanticsLayer
    if selection.adapter is None:
        semantics = TranscriptOnlySemanticsLayer(selection.status)
    else:
        if not isinstance(selection.adapter, ActualUCNSAdapter):
            raise TypeError("select_ucns_adapter returned an unsupported adapter implementation")
        semantics = UCNSSemanticsLayer(selection.adapter)

    return EDCMLayers(
        semantics=semantics,
        measurement=ConsolidatedMeasurementLayer(),
        composition=DefaultCompositionLayer(),
        delivery=DefaultDeliveryLayer(),
    )
