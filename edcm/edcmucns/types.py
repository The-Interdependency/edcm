# === MODULE_BUILD ===
# id: edcmucns_types
#   module_name: types
#   module_kind: schema
#   summary: Core edcmucns v0.3.1 value objects — Anchor (origin/bone/cadence), Payload, Window, OperatorTurn (Present | AbsentOperatorGeometry), BridgeDiagnostic
#   owner: Erin Spencer
#   public_surface: ANCHOR_ROLES, Anchor, Payload, ContentLensEvent, Window, Present, AbsentOperatorGeometry, OperatorTurn, BridgeDiagnostic, operator_presence_readout
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: transcripts may carry user speech in payload content / lens events
#   admin_only: false
#   tests: tests.test_edcmucns_encoder_v031, tests.test_edcmucns_identity_v031
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: edcmucns_provenance
#   since: 2026-07-06
#   unresolved: cadence anchors are reserved in v0.3.1 (no admission from transcript text); composite cadence exists only for explicit caller-built fixtures
# === END MODULE_BUILD ===

"""Core value objects for edcmucns v0.3.1.

EDCM windows are ordered UCNS sequence objects composed by chronological
append. A no-bone turn is not unit and not zero: it is
:class:`AbsentOperatorGeometry` — NA for operator readouts, still available
to the Content layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib

from ..ucns_objects import AxisState
from .provenance import ProvenanceWitness

# Anchor roles (v0.3.1). origin = datum/boundary anchor (theta=0, face=0);
# bone = family-signature anchor (never theta=0); cadence = reserved
# host-level cadence anchor (composite lattice allowed for explicit fixtures).
ANCHOR_ROLES: tuple[str, ...] = ("origin", "bone", "cadence")


@dataclass(frozen=True, slots=True)
class Anchor:
    """A host-level anchor on the unit circle.

    ``theta`` is an exact turn fraction in [0, 1). ``lattice_n`` is the
    anchor's carrier contribution: 1 for origin datum anchors, the family
    prime for bones, any n >= 1 (composite allowed) for cadence anchors.
    """

    role: str
    family: str | None
    lattice_n: int
    ordinal: int | None
    residue: int | None
    theta: Fraction
    face: int

    def __post_init__(self) -> None:
        if self.role not in ANCHOR_ROLES:
            raise ValueError(f"unknown anchor role: {self.role!r}")
        if self.lattice_n < 1:
            raise ValueError("lattice_n must be >= 1")
        if not (0 <= self.theta < 1):
            raise ValueError("theta must be a turn fraction in [0, 1)")
        if self.role == "origin":
            if self.theta != 0 or self.face != 0:
                raise ValueError("origin anchors must have theta=0 and face=0")
            return
        # theta=0 is reserved for explicit datum roles (v0.3.1).
        if self.theta == 0:
            raise ValueError(
                "phase zero requires an explicit datum role; "
                f"{self.role} anchors never occupy theta=0"
            )
        if self.role == "bone":
            if self.face not in (-1, 1):
                raise ValueError("bone anchors carry polarity face in {-1, +1}")
        elif self.face != 0:
            raise ValueError("cadence anchors carry face=0 (rhythm, not polarity)")


@dataclass(frozen=True, slots=True)
class Payload:
    """Flesh payload subobject — epicyclic; never automatically part of host n_min."""

    payload_id: str
    carrier_n: int = 1
    status: str = "open"  # "open" | "closed"
    content: str = ""
    tension: int = 1

    def __post_init__(self) -> None:
        if self.carrier_n < 1:
            raise ValueError("payload carrier_n must be >= 1")
        if self.status not in ("open", "closed"):
            raise ValueError(f"unknown payload status: {self.status!r}")

    @property
    def reduced_carrier(self) -> int:
        """A closed payload reduces to unit."""

        return 1 if self.status == "closed" else self.carrier_n

    @property
    def content_hash(self) -> str:
        blob = f"{self.payload_id}|{self.carrier_n}|{self.status}|{self.content}"
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class ContentLensEvent:
    """Content-layer event emitted when a turn has no operator geometry."""

    turn_id: str
    speaker_or_source: str
    text_surface: str = ""
    reason: str = "no_bone_geometry"


@dataclass(frozen=True, slots=True)
class BridgeDiagnostic:
    """Observational Bridge event. A mismatch is a diagnostic, never a
    silent alternate reading."""

    kind: str
    detail: str
    expected: str = ""
    observed: str = ""


@dataclass(frozen=True, slots=True)
class Window:
    """An EDCM window: ordered anchors + their testimony + payloads.

    ``anchors`` is chronological; absolute lattice positions stay
    origin-anchored. ``witnesses`` pairs 1:1 with the bone anchors in order.
    ``field_chain`` carries ConstraintField / FieldMotion hash-chain state for
    field-scope readouts.
    """

    anchors: tuple[Anchor, ...]
    witnesses: tuple[ProvenanceWitness, ...]
    manifest_hash: str
    payloads: tuple[Payload, ...] = ()
    tok_count: int = 0
    raised_field_count: int = 0
    field_chain: tuple[str, ...] = ()

    @property
    def length(self) -> int:
        """Sequence length (SeqAppend adds it; product multiplies it)."""

        return len(self.anchors)

    @property
    def faces(self) -> tuple[int, ...]:
        """F — the chronological face sequence (concatenates under SeqAppend)."""

        return tuple(a.face for a in self.anchors)


@dataclass(frozen=True, slots=True)
class Present:
    """OperatorTurn with operator geometry: Present(UCNSObject, provenance)."""

    window: Window


@dataclass(frozen=True, slots=True)
class AbsentOperatorGeometry:
    """OperatorTurn without operator geometry — not unit, not zero."""

    event: ContentLensEvent


OperatorTurn = Present | AbsentOperatorGeometry


def operator_presence_readout(turn: OperatorTurn) -> AxisState:
    """Operator-presence readout. Absent geometry emits NA — never 0."""

    if isinstance(turn, AbsentOperatorGeometry):
        return AxisState.na()
    return AxisState(enabled=True, s=1, m=1.0)
