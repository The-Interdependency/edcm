"""Provenance-bearing EDCM layer assembly.

Usage guidance
--------------
Use :func:`build_default_layers` for the supported package bootstrap. The
semantics stage is composite: canonical METAPAT semantic authority and the
EDCM-only UCNS word-gonol observation profile are selected independently, with
typed absence when either optional package is unavailable. The profile does
not supply UCNS geometry. The maintained ``edcm.measurement`` surface always
supplies measurement. Composition and delivery emit the deterministic result.

Every result includes independent ``metapat_integration``, ``ucns_integration``,
``layer_provenance``, and ``edcm_result`` records. Missing integrations are
never represented only by a bare ``default`` label.
"""

# === MODULE_BUILD ===
# id: edcm_layers
#   module_name: layers
#   module_kind: engine
#   summary: Provenance-bearing EDCM stack with independently selected METAPAT semantic authority, exact UCNS word-gonol observation profile or typed absence, canonical local measurement, shared-stack composition, and final result-contract delivery.
#   owner: Erin Spencer
#   public_surface: LayerProvenance, MeasurementLayer, SemanticsLayer, CompositionLayer, DeliveryLayer, DefaultMeasurementLayer, DefaultCompositionLayer, DefaultDeliveryLayer, MissingMetapatSemanticAuthorityLayer, MetapatSemanticAuthorityLayer, MissingUCNSProfileLayer, UCNSProfileLayer, CompositeSemanticsLayer, ConsolidatedMeasurementLayer, SharedStackCompositionLayer, SharedStackDeliveryLayer, EDCMLayers, build_default_layers
#   internal_surface: _record_layer, _local_provenance
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: threads caller payloads through deterministic package-local layers; transcript content is hashed in final result identity
#   admin_only: false
#   tests: tests.test_measurement, tests.test_ucns_adapter, tests.test_metapat_adapter, tests.test_shared_stack_contract
#   rollout: default_enabled
#   rollback: restore prior layer assembly and remove shared-stack result delivery
#   requires: edcm_metapat_adapter, edcm_ucns_adapter, edcm_measurement, edcm_shared_stack
#   since: 2026-06-02
#   unresolved: formal Mobius coordinates and higher-gonol composition remain unattached; profile observations do not supply geometry, factorization, or theorem status
# === END MODULE_BUILD ===

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Protocol

from . import __version__ as EDCM_VERSION
from .edcmucns.manifest import PolicyManifest
from .metapat_adapter import (
    ActualMetapatAdapter,
    METAPAT_INSTALL_HINT,
    MetapatIntegrationStatus,
    missing_metapat_status,
    select_metapat_adapter,
)
from .shared_stack import build_result_contract
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


class MissingMetapatSemanticAuthorityLayer:
    """Typed semantic-authority absence when METAPAT is not installed."""

    def __init__(self, status: MetapatIntegrationStatus | None = None) -> None:
        self._status = status or missing_metapat_status()
        self.provenance = _local_provenance(
            "edcm.semantic_authority.metapat_unavailable",
            "semantic_authority",
            "unavailable",
            canonical=False,
            unresolved_constraints=self._status.unresolved_constraints,
        )

    def normalize(self, payload: dict[str, Any]) -> dict[str, Any]:
        if any(
            key in payload
            for key in (
                "metapat_envelope",
                "metapat_envelope_json",
                "metapat_envelope_dict",
            )
        ):
            raise ImportError(METAPAT_INSTALL_HINT)
        state = dict(payload)
        state["semantic_authority"] = "unavailable"
        state["metapat_integration"] = self._status.as_dict()
        state.pop("metapat_semantics", None)
        return _record_layer(state, "semantic_authority", self.provenance)


class MetapatSemanticAuthorityLayer:
    """Semantic-authority wrapper around :class:`ActualMetapatAdapter`."""

    def __init__(self, adapter: ActualMetapatAdapter) -> None:
        self._adapter = adapter
        status = adapter.status
        self.provenance = LayerProvenance(
            implementation_id=status.implementation_id,
            implementation_version=status.implementation_version,
            source_repository=status.source_repository,
            role="semantic_authority",
            selection=status.selection,
            canonical=True,
            unresolved_constraints=status.unresolved_constraints,
            errors=status.errors,
        )

    def normalize(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self._adapter.normalize(payload)
        return _record_layer(state, "semantic_authority", self.provenance)


class MissingUCNSProfileLayer:
    """Typed profile absence when the optional exact UCNS profile is unavailable."""

    def __init__(self, status: UCNSIntegrationStatus | None = None) -> None:
        self._status = status or missing_ucns_status()
        self.provenance = _local_provenance(
            "edcm.ucns_profile.unavailable",
            "ucns_profile",
            "unavailable",
            canonical=False,
            unresolved_constraints=(
                "no exact UCNS word-gonol profile ran",
                *self._status.unresolved_constraints,
            ),
        )

    def normalize(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        state["ucns_profile"] = "unavailable"
        state["ucns_integration"] = self._status.as_dict()
        state.pop("ucns_profile_observation", None)
        return _record_layer(state, "ucns_profile", self.provenance)


class UCNSProfileLayer:
    """Observation-profile wrapper around :class:`ActualUCNSAdapter`."""

    def __init__(self, adapter: ActualUCNSAdapter) -> None:
        self._adapter = adapter
        status = adapter.status
        self.provenance = LayerProvenance(
            implementation_id=status.implementation_id,
            implementation_version=status.implementation_version,
            source_repository=status.source_repository,
            role="ucns_profile",
            selection=status.selection,
            canonical=False,
            unresolved_constraints=status.unresolved_constraints,
            errors=status.errors,
        )

    def normalize(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self._adapter.normalize(payload)
        state["ucns_profile"] = "ucns.edcm_word_gonol_profile"
        return _record_layer(state, "ucns_profile", self.provenance)


class CompositeSemanticsLayer:
    """Run semantic authority and the UCNS observation profile independently."""

    def __init__(self, authority: SemanticsLayer, profile: SemanticsLayer) -> None:
        self._authority = authority
        self._profile = profile
        unresolved = tuple(
            dict.fromkeys(
                (
                    *authority.provenance.unresolved_constraints,
                    *profile.provenance.unresolved_constraints,
                )
            )
        )
        self.provenance = _local_provenance(
            "edcm.semantics.composite",
            "semantics",
            "canonical",
            canonical=True,
            unresolved_constraints=unresolved,
        )

    def normalize(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self._authority.normalize(payload)
        state = self._profile.normalize(state)
        state["semantics"] = {
            "semantic_authority": state.get("semantic_authority"),
            "ucns_profile": state.get("ucns_profile"),
        }
        return _record_layer(state, "semantics", self.provenance)


class SharedStackCompositionLayer:
    """Canonical composition boundary before final result delivery."""

    provenance = _local_provenance(
        "edcm.composition.shared_stack",
        "composition",
        "canonical",
        canonical=True,
    )

    def compose(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        state["composition"] = "edcm.shared_stack"
        return _record_layer(state, "composition", self.provenance)


class DefaultCompositionLayer(SharedStackCompositionLayer):
    """Backward-compatible name for canonical shared-stack composition."""


class SharedStackDeliveryLayer:
    """Emit the final separated, deterministic EDCM result contract."""

    def __init__(self, manifest: PolicyManifest) -> None:
        self._manifest = manifest
        self.provenance = _local_provenance(
            "edcm.delivery.result_contract",
            "delivery",
            "canonical",
            canonical=True,
        )

    def deliver(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        state["delivery"] = "edcm.result_contract"
        state = _record_layer(state, "delivery", self.provenance)
        state["edcm_result"] = build_result_contract(state, self._manifest).as_dict()
        return state


class DefaultDeliveryLayer(SharedStackDeliveryLayer):
    """Backward-compatible name for canonical result-contract delivery."""

    def __init__(self, manifest: PolicyManifest | None = None) -> None:
        super().__init__(manifest or PolicyManifest())


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


def build_default_layers(
    policy_manifest: PolicyManifest | None = None,
) -> EDCMLayers:
    """Build the supported stack without silent sibling-package substitution.

    EDCM's maintained measurement implementation always runs locally. METAPAT
    and UCNS are selected independently through EDCM-owned adapters. Direct
    package absence yields typed absence; malformed imports and schemas remain
    visible failures. A supplied policy manifest changes result epoch identity.
    """

    metapat_selection = select_metapat_adapter()
    if metapat_selection.adapter is None:
        authority: SemanticsLayer = MissingMetapatSemanticAuthorityLayer(
            metapat_selection.status
        )
    else:
        if not isinstance(metapat_selection.adapter, ActualMetapatAdapter):
            raise TypeError(
                "select_metapat_adapter returned an unsupported adapter implementation"
            )
        authority = MetapatSemanticAuthorityLayer(metapat_selection.adapter)

    ucns_selection = select_ucns_adapter()
    if ucns_selection.adapter is None:
        profile: SemanticsLayer = MissingUCNSProfileLayer(ucns_selection.status)
    else:
        if not isinstance(ucns_selection.adapter, ActualUCNSAdapter):
            raise TypeError(
                "select_ucns_adapter returned an unsupported adapter implementation"
            )
        profile = UCNSProfileLayer(ucns_selection.adapter)

    manifest = policy_manifest or PolicyManifest()
    return EDCMLayers(
        semantics=CompositeSemanticsLayer(authority, profile),
        measurement=ConsolidatedMeasurementLayer(),
        composition=SharedStackCompositionLayer(),
        delivery=SharedStackDeliveryLayer(manifest),
    )
