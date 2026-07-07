# === MODULE_BUILD ===
# id: edcmucns_encoder
#   module_name: encoder
#   module_kind: engine
#   summary: v0.3.1 turn encoder — bone events to origin-anchored windows with provenance witnesses; no-bone turns emit AbsentOperatorGeometry; cadence admission from text is a reserved frontier gate
#   owner: Erin Spencer
#   public_surface: BoneEvent, encode_turn, make_origin_anchor, make_cadence_anchor, with_cadence, admit_cadence_from_text
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: transcript-shaped inputs (turn ids, speakers, surface forms)
#   admin_only: false
#   tests: tests.test_edcmucns_encoder_v031
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: edcmucns_manifest,edcmucns_types,edcmucns_provenance,edcmucns_geometry
#   since: 2026-07-06
#   unresolved: bone emission from raw text is out of scope here — callers supply BoneEvents; the bone_emission_policy_version pins which upstream emitter produced them
# === END MODULE_BUILD ===

"""Turn encoder for edcmucns v0.3.1.

Bones separate the operator voices; flesh carries the recursive music. The
encoder consumes explicit bone events (family + surface form + polarity
face), assigns per-family 1-based ordinals in chronological order, applies
the non-origin residue rule, and returns an origin-anchored window wrapped
as an OperatorTurn. A turn with no bone events is AbsentOperatorGeometry —
NA for operator readouts, available to the Content layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .geometry import bone_theta, cadence_theta, non_origin_residue
from .manifest import PolicyManifest
from .provenance import ProvenanceWitness, canonicalize
from .types import (
    AbsentOperatorGeometry,
    Anchor,
    ContentLensEvent,
    OperatorTurn,
    Payload,
    Present,
    Window,
)


@dataclass(frozen=True, slots=True)
class BoneEvent:
    """One emitted bone: family signature + surface testimony + polarity face."""

    family: str
    surface_form: str
    face: int = 1
    constraint_governance: str = "none"
    payload_attachment: str | None = None


def make_origin_anchor() -> Anchor:
    """The datum/boundary anchor: theta=0, face=0, unit lattice."""

    return Anchor(
        role="origin", family=None, lattice_n=1,
        ordinal=None, residue=None, theta=Fraction(0), face=0,
    )


def encode_turn(
    turn_id: str,
    speaker_or_source: str,
    events: tuple[BoneEvent, ...] | list[BoneEvent],
    manifest: PolicyManifest,
    *,
    tok_count: int = 0,
    raised_field_count: int = 0,
    payloads: tuple[Payload, ...] = (),
    field_chain: tuple[str, ...] = (),
    text_surface: str = "",
) -> OperatorTurn:
    """Encode one transcript turn into an OperatorTurn."""

    turn_id = canonicalize(turn_id)
    speaker_or_source = canonicalize(speaker_or_source)

    if not events:
        return AbsentOperatorGeometry(
            ContentLensEvent(
                turn_id=turn_id,
                speaker_or_source=speaker_or_source,
                text_surface=text_surface,
            )
        )

    anchors: list[Anchor] = [make_origin_anchor()]
    witnesses: list[ProvenanceWitness] = []
    ordinals: dict[str, int] = {}

    for event in events:
        prime = manifest.prime_for(event.family)
        if event.face not in (-1, 1):
            raise ValueError("bone polarity face must be -1 or +1")
        ordinal = ordinals.get(event.family, 0) + 1
        ordinals[event.family] = ordinal
        residue = non_origin_residue(ordinal, prime)
        anchors.append(
            Anchor(
                role="bone",
                family=event.family,
                lattice_n=prime,
                ordinal=ordinal,
                residue=residue,
                theta=bone_theta(ordinal, prime),
                face=event.face,
            )
        )
        witnesses.append(
            ProvenanceWitness(
                family=event.family,
                ordinal_m_f=ordinal,
                residue_r_f=residue,
                turn_id=turn_id,
                speaker_or_source=speaker_or_source,
                surface_form=event.surface_form,
                role="bone",
                constraint_governance=event.constraint_governance,
                payload_attachment=event.payload_attachment,
            )
        )

    return Present(
        Window(
            anchors=tuple(anchors),
            witnesses=tuple(witnesses),
            manifest_hash=manifest.manifest_hash(),
            payloads=tuple(payloads),
            tok_count=tok_count,
            raised_field_count=raised_field_count,
            field_chain=tuple(field_chain),
        )
    )


def make_cadence_anchor(ordinal: int, lattice_n: int) -> Anchor:
    """Explicit cadence-scope fixture constructor (composite lattice allowed).

    Cadence anchors are RESERVED in v0.3.1: admission from transcript text is
    not implemented. This constructor exists so a caller can explicitly build
    a cadence scope fixture. Cadence keeps regular 1/n motion — rhythm, not a
    family-prime label — and never emits a family prime event.
    """

    return Anchor(
        role="cadence",
        family=None,
        lattice_n=lattice_n,
        ordinal=ordinal,
        residue=None,
        theta=cadence_theta(ordinal, lattice_n),
        face=0,
    )


def with_cadence(window: Window, *cadence: Anchor) -> Window:
    """Return a window with explicit cadence fixture anchors appended."""

    for a in cadence:
        if a.role != "cadence":
            raise ValueError("with_cadence accepts cadence anchors only")
    return Window(
        anchors=window.anchors + tuple(cadence),
        witnesses=window.witnesses,
        manifest_hash=window.manifest_hash,
        payloads=window.payloads,
        tok_count=window.tok_count,
        raised_field_count=window.raised_field_count,
        field_chain=window.field_chain,
    )


def admit_cadence_from_text(*_args: object, **_kwargs: object) -> None:
    """FRONTIER — cadence-anchor admission from real transcript text.

    Reserved in v0.3.1. Named falsifier: an admission rule whose admitted
    cadence anchors fail to preserve regular 1/n motion on held-out
    transcripts refutes that rule.
    """

    raise NotImplementedError(
        "frontier (v0.3.1): cadence-anchor admission from transcript text is "
        "reserved; construct explicit cadence fixtures via make_cadence_anchor"
    )
