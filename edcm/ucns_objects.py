"""edcm.ucns_objects — UCNS metric construction objects (v0.2 orthogonality spec).

Self-contained, dependency-free mirror of edcmbone's UCNS construction layer
(The-Interdependency/edcmbone: backend/src/edcmbone/metrics/orthogonality.py).
Kept dependency-free so this consolidation repo runs today without edcmbone
installed, consistent with the four-layer bootstrap in edcm/layers.py.

    AxisState        signed ternary axis state (NA is not 0)
    MetricAxis       canonical metric-axis identity record
    MetricReadout    a signed-ternary readout tied to its parent UCNS object
    ConstraintField  UCNS state object — presence / contact / resolution readouts
    FieldMotion      UCNS tangent object — F / E / O_scope motion readouts

Primary doctrine: UCNS exists to construct EDCM metrics.

No UCNS-A theorem/proof status is transferred to EDCM, edcmbone, or UCNS-G by
this module.
"""

# === MODULE_BUILD ===
# id: edcm_ucns_objects
#   module_name: ucns_objects
#   module_kind: engine
#   summary: dependency-free mirror of edcmbone's UCNS metric construction layer (v0.2 signed-axis orthogonality)
#   owner: Erin Spencer
#   public_surface: AxisState, MetricAxis, MetricReadout, ConstraintField, FieldMotion, field_motion_fixture, canonical_axes
#   internal_surface: _clamp_unit, _sign
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_ucns_objects
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: none
#   since: 2026-06-02
#   unresolved: mirror of edcmbone backend/src/edcmbone/metrics/orthogonality.py; keep in sync
# === END MODULE_BUILD ===


from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

SIGNED_TERNARY = (-1, 0, 1)

GRAINS = ("token", "turn", "round", "session", "archive")

# v0.1 adapter contact vocabulary -> signed ternary contact direction (spec §4.2).
#   away    -> 0  (neutral contact, carries a deflection signal)
#   toward  -> +1
#   against -> -1
CONTACT_SIGN = {"toward": 1, "against": -1, "away": 0}

# Adapter resolution vocabulary -> signed ternary resolution state (spec §4.3).
#   closed (payload None/unit) -> +1  integration / closure / accepted
#   open   (payload non-unit)  -> -1  dis-integration / opened constraint
#   unresolved                 ->  0  no testable resolution movement
RESOLUTION_SIGN = {"closed": 1, "open": -1, "unresolved": 0}


def _clamp_unit(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _sign(x: float) -> int:
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


@dataclass(frozen=True)
class AxisState:
    """Signed ternary axis state.

    NA is represented by ``enabled=False`` with ``s`` and ``m`` left as ``None``.
    When enabled, ``s`` must be in {-1,0,+1} and ``m`` in [0,1].

    Pin (spec §1): NA != 0. ``0`` is a neutral/uncommitted axis state that
    requires field/context presence; NA is a disabled readout because the
    required field/context is absent.
    """

    enabled: bool
    s: Optional[int] = None
    m: Optional[float] = None

    def __post_init__(self) -> None:
        if not self.enabled:
            if self.s is not None or self.m is not None:
                raise ValueError("disabled (NA) axis state must not carry s or m")
            return
        if self.s not in SIGNED_TERNARY:
            raise ValueError("s must be one of -1, 0, +1")
        if self.m is None or not (0.0 <= float(self.m) <= 1.0):
            raise ValueError("m must be in [0,1]")

    @classmethod
    def na(cls) -> "AxisState":
        return cls(enabled=False)


@dataclass(frozen=True)
class MetricAxis:
    metric_id: str
    axis_name: str
    parent_object: str
    primitive: bool = True


@dataclass(frozen=True)
class MetricReadout:
    """A signed-ternary metric readout tied to the UCNS object that produced it.

    ``parent_hash`` is the hash of the parent UCNS object (a ConstraintField
    field_hash, or a FieldMotion transition hash). F/E/O_scope readouts for the
    same transition share a parent_hash but keep distinct ``metric_id`` values
    (spec §14 obligations 9-10).
    """

    metric_id: str
    parent_hash: str
    state: AxisState


@dataclass(frozen=True)
class ConstraintField:
    """UCNS ConstraintField_t — EDCM state object.

    schema_id:   edcm/constraint_field_ucns_v1
    object_kind: constraint_field

    Constructs signed-ternary EDCM state readouts from:
      - ``raised_field_count``: intrinsic carrier / raised-field geometry, the
        presence substrate (spec §4.1). It is *not* L; it supports L readouts.
      - ``contact``: adapter direction (away/toward/against) -> contact_state.
      - ``resolution``: adapter payload state (closed/open/unresolved) -> I.

    Empty-field rule (spec §4.1): when ``raised_field_count == 0`` the contact,
    L, D, R and I readouts are NA, not 0.
    """

    grain: str
    raised_field_count: int
    contact: Optional[str] = None
    contact_magnitude: float = 0.0
    resolution: Optional[str] = None
    resolution_magnitude: float = 0.0
    witness: Optional[str] = None

    SCHEMA_ID = "edcm/constraint_field_ucns_v1"
    OBJECT_KIND = "constraint_field"

    def __post_init__(self) -> None:
        if self.grain not in GRAINS:
            raise ValueError(f"unknown grain: {self.grain!r}")
        if self.raised_field_count < 0:
            raise ValueError("raised_field_count must be >= 0")
        if self.contact is not None and self.contact not in CONTACT_SIGN:
            raise ValueError(f"unknown contact direction: {self.contact!r}")
        if self.resolution is not None and self.resolution not in RESOLUTION_SIGN:
            raise ValueError(f"unknown resolution state: {self.resolution!r}")

    @property
    def present(self) -> bool:
        return self.raised_field_count > 0

    @property
    def presence_substrate(self) -> int:
        """Intrinsic carrier / raised-field geometry (spec §4.1).

        This supports L readouts; it is not itself L.
        """
        return self.raised_field_count

    @property
    def field_hash(self) -> str:
        key = "|".join(
            str(p)
            for p in (
                self.SCHEMA_ID,
                self.grain,
                self.raised_field_count,
                self.contact,
                self.contact_magnitude,
                self.resolution,
                self.resolution_magnitude,
                self.witness,
            )
        )
        return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]

    def contact_state(self) -> AxisState:
        """Signed ternary contact (spec §4.2). NA on empty field."""
        if not self.present:
            return AxisState.na()
        s = CONTACT_SIGN[self.contact] if self.contact is not None else 0
        return AxisState(enabled=True, s=s, m=_clamp_unit(self.contact_magnitude))

    def resolution_state(self) -> AxisState:
        """Signed ternary resolution / integration (spec §4.3). NA on empty field."""
        if not self.present:
            return AxisState.na()
        s = RESOLUTION_SIGN[self.resolution] if self.resolution is not None else 0
        return AxisState(enabled=True, s=s, m=_clamp_unit(self.resolution_magnitude))

    def behavioral_readouts(self) -> Dict[str, MetricReadout]:
        """Construct the ConstraintField state readouts (R, D, I, L_resistance).

        Empty-field rule (spec §4.1): all are NA when the field is empty.
        """
        h = self.field_hash
        ids = (
            "edcm.behavioral.R.refusal_density",
            "edcm.behavioral.D.deflection",
            "edcm.behavioral.I.integration",
            "edcm.behavioral.L_resistance",
        )
        if not self.present:
            na = AxisState.na()
            return {mid: MetricReadout(mid, h, na) for mid in ids}

        c = self.contact
        m = _clamp_unit(self.contact_magnitude)
        # R — refusal / resistance contact: against hardens (+1), toward softens (-1).
        r_sign = {"against": 1, "toward": -1, "away": 0, None: 0}[c]
        # D — deflection / return: away deflects (+1), toward returns (-1).
        d_sign = {"away": 1, "toward": -1, "against": 0, None: 0}[c]
        # L_resistance — resistance hardening / softening, parent Contact.
        lr_sign = {"against": 1, "toward": -1, "away": 0, None: 0}[c]
        return {
            "edcm.behavioral.R.refusal_density": MetricReadout(
                "edcm.behavioral.R.refusal_density", h, AxisState(True, r_sign, m)
            ),
            "edcm.behavioral.D.deflection": MetricReadout(
                "edcm.behavioral.D.deflection", h, AxisState(True, d_sign, m)
            ),
            "edcm.behavioral.I.integration": MetricReadout(
                "edcm.behavioral.I.integration", h, self.resolution_state()
            ),
            "edcm.behavioral.L_resistance": MetricReadout(
                "edcm.behavioral.L_resistance", h, AxisState(True, lr_sign, m)
            ),
        }


@dataclass(frozen=True)
class FieldMotion:
    """UCNS FieldMotion_{t-1->t} — tangent / differential object.

    schema_id:   edcm/field_motion_ucns_v1
    object_kind: field_motion

    F, E and O_scope are signed-ternary right-angle readouts of the motion
    between two ConstraintFields (spec §5-§6). Each read tuple holds signed
    change signals for that axis; the readout sign is the sign of their mean and
    the magnitude is the clamped absolute mean.

    Presence: when neither field is present the readouts are NA. When present
    but an axis has no reads, the readout is a stable ``0`` (not NA).
    """

    previous_field_hash: str
    current_field_hash: str
    present: bool = True
    recurrence_reads: Tuple[float, ...] = ()
    intensity_reads: Tuple[float, ...] = ()
    scope_reads: Tuple[float, ...] = ()

    SCHEMA_ID = "edcm/field_motion_ucns_v1"
    OBJECT_KIND = "field_motion"

    @property
    def parent_hash(self) -> str:
        return f"{self.previous_field_hash}->{self.current_field_hash}"

    def _readout_state(self, reads: Tuple[float, ...]) -> AxisState:
        if not self.present:
            return AxisState.na()
        if not reads:
            return AxisState(enabled=True, s=0, m=0.0)
        mean = sum(float(x) for x in reads) / len(reads)
        return AxisState(enabled=True, s=_sign(mean), m=min(1.0, abs(mean)))

    def fixation(self) -> MetricReadout:
        """F — recurrence / release (spec §6.1)."""
        return MetricReadout(
            "edcm.behavioral.F.fixation",
            self.parent_hash,
            self._readout_state(self.recurrence_reads),
        )

    def escalation(self) -> MetricReadout:
        """E — escalation / de-escalation (spec §6.2)."""
        return MetricReadout(
            "edcm.behavioral.E.escalation",
            self.parent_hash,
            self._readout_state(self.intensity_reads),
        )

    def scope(self) -> MetricReadout:
        """O_scope — expansion / contraction (spec §6.3)."""
        return MetricReadout(
            "edcm.behavioral.O_scope",
            self.parent_hash,
            self._readout_state(self.scope_reads),
        )

    def readouts(self) -> Dict[str, MetricReadout]:
        return {r.metric_id: r for r in (self.fixation(), self.escalation(), self.scope())}

    @classmethod
    def from_fields(
        cls,
        previous: ConstraintField,
        current: ConstraintField,
        *,
        recurrence_reads: Tuple[float, ...] = (),
        intensity_reads: Tuple[float, ...] = (),
        scope_reads: Tuple[float, ...] = (),
    ) -> "FieldMotion":
        return cls(
            previous_field_hash=previous.field_hash,
            current_field_hash=current.field_hash,
            present=(previous.present or current.present),
            recurrence_reads=tuple(recurrence_reads),
            intensity_reads=tuple(intensity_reads),
            scope_reads=tuple(scope_reads),
        )


# Canonical F / E / O_scope fixture matrix (spec §13). Sign-only reference.
FIELD_MOTION_FIXTURE_MATRIX: Dict[str, Tuple[int, int, int]] = {
    "stable_resolution": (-1, -1, 0),
    "stuck_loop": (1, 0, 0),
    "sharp_spike": (0, 1, 0),
    "scope_contraction": (0, 0, -1),
    "scope_creep": (0, 0, 1),
    "escalating_loop": (1, 1, 0),
    "sprawling_loop": (1, 0, 1),
    "pressure_sprawl": (0, 1, 1),
    "runaway_spiral": (1, 1, 1),
    "decompressing_loop": (-1, -1, -1),
}


def field_motion_fixture(name: str) -> FieldMotion:
    """Build the canonical FieldMotion fixture from the spec §13 matrix."""
    f, e, o = FIELD_MOTION_FIXTURE_MATRIX[name]
    return FieldMotion(
        previous_field_hash=f"prev::{name}",
        current_field_hash=f"cur::{name}",
        present=True,
        recurrence_reads=(float(f),),
        intensity_reads=(float(e),),
        scope_reads=(float(o),),
    )


def canonical_axes() -> Dict[str, MetricAxis]:
    """Return canonical metric axis + projection registry (spec §9, §10)."""
    axes = {
        # §9 primitive axes
        "edcm.behavioral.C.constraint_strain": MetricAxis("edcm.behavioral.C.constraint_strain", "constraint strain", "ConstraintField / evidence"),
        "edcm.behavioral.R.refusal_density": MetricAxis("edcm.behavioral.R.refusal_density", "refusal / resistance contact", "ConstraintField / Contact"),
        "edcm.behavioral.D.deflection": MetricAxis("edcm.behavioral.D.deflection", "deflection / return", "ConstraintField / Contact"),
        "edcm.behavioral.I.integration": MetricAxis("edcm.behavioral.I.integration", "integration / dis-integration", "ConstraintField / Resolution"),
        "edcm.behavioral.F.fixation": MetricAxis("edcm.behavioral.F.fixation", "recurrence / release", "FieldMotion"),
        "edcm.behavioral.E.escalation": MetricAxis("edcm.behavioral.E.escalation", "escalation / de-escalation", "FieldMotion"),
        "edcm.behavioral.O_scope": MetricAxis("edcm.behavioral.O_scope", "expansion / contraction", "FieldMotion"),
        "edcm.behavioral.O_confidence": MetricAxis("edcm.behavioral.O_confidence", "confidence polarity", "confidence evidence"),
        "edcm.behavioral.L_load": MetricAxis("edcm.behavioral.L_load", "load increase / decrease", "ConstraintField"),
        "edcm.behavioral.L_loss": MetricAxis("edcm.behavioral.L_loss", "coherence loss / recovery", "continuity evidence"),
        "edcm.behavioral.L_resistance": MetricAxis("edcm.behavioral.L_resistance", "resistance hardening / softening", "ConstraintField / Contact"),
        "edcm.behavioral.N.noise": MetricAxis("edcm.behavioral.N.noise", "signal efficiency / inefficiency", "system evidence"),
        "edcm.round.P_progress": MetricAxis("edcm.round.P_progress", "progress / regression", "sequence state"),
        "edcm.state.kappa": MetricAxis("edcm.state.kappa", "stored tension / release", "state composite"),
        # §10 projections (not primitive)
        "edcm.projection.CM": MetricAxis("edcm.projection.CM", "projection over C and I", "projection", primitive=False),
        "edcm.projection.DA": MetricAxis("edcm.projection.DA", "projection over kappa, E, R", "projection", primitive=False),
        "edcm.projection.DRIFT": MetricAxis("edcm.projection.DRIFT", "projection over L and P", "projection", primitive=False),
        "edcm.projection.DVG": MetricAxis("edcm.projection.DVG", "projection over D and N", "projection", primitive=False),
        "edcm.projection.INT": MetricAxis("edcm.projection.INT", "projection over E and F", "projection", primitive=False),
        "edcm.projection.TBF": MetricAxis("edcm.projection.TBF", "speaker-share fairness projection", "projection", primitive=False),
    }
    return axes
