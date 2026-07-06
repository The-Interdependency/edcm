"""
ucns_v04 — UCNS Engine (turn-fraction angle convention)
========================================================
Angles are stored as Fraction objects representing fractions of a full turn:
  0 = 0 deg, 1/4 = 90 deg, 1/2 = 180 deg, 2 = 720 deg = 0 on doubled cover.

The algebra operates on the doubled cover of the unit circle, so the
fundamental period is 2 (two full turns = identity). Normalization shifts
the first anchor to theta=0 and reduces all thetas mod 2.

n_min is the LCM of denominators of all non-zero anchor thetas, computed
directly from the Fraction denominators (no pi-unit conversion).

Public API
----------
AnchorPayload(theta, payload)
UCNSObject(n_dec, n_min, anchors_pos, faces_pos)
    .anchors_pos    : tuple[AnchorPayload, ...]
    .faces_pos      : tuple[int, ...]
    .n_dec          : int
    .n_min          : int
    .normalize()    : UCNSObject  (returns self; normalization done in __init__)
    .equivalent(other) : bool
unit_obj()          : UCNSObject  (multiplicative unit)
is_unit_payload(obj): bool
multiply(A, B)      : UCNSObject  (A ⊠ B)
"""

# === MODULE_BUILD ===
# id: edcmbone_ucns_v04
#   module_name: ucns_v04
#   module_kind: engine
#   summary: local UCNS engine using the turn-fraction angle convention on the doubled cover of the unit circle
#   owner: Erin Spencer
#   public_surface: AnchorPayload, UCNSObject, unit_obj, is_unit_payload, multiply
#   internal_surface: _lcm, _reduce_lcm
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_ucns_objects
#   rollout: default_enabled
#   rollback: remove module; closed_tokens loses its UCNS object algebra
#   requires: none
#   since: 2026-06-02
#   unresolved: this is edcmbone's local UCNS-A layer; per docs/ucns-boundary.md no UCNS-A theorem status transfers to EDCM/UCNS-G
# === END MODULE_BUILD ===


from __future__ import annotations

from fractions import Fraction
from math import gcd
from functools import reduce
from typing import Optional, Tuple

__all__ = [
    "AnchorPayload",
    "UCNSObject",
    "unit_obj",
    "is_unit_payload",
    "multiply",
]


def _lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def _reduce_lcm(denoms):
    return reduce(_lcm, denoms, 1)


class AnchorPayload:
    """Named container for a (theta, payload) anchor entry."""
    __slots__ = ("theta", "payload")

    def __init__(self, theta, payload):
        self.theta = Fraction(theta)
        self.payload = payload  # UCNSObject or None

    def __repr__(self) -> str:
        return f"AnchorPayload(theta={self.theta}, payload={self.payload!r})"


class UCNSObject:
    """
    A UCNS algebraic object on the doubled unit circle.

    anchors_pos : tuple of AnchorPayload (theta in turn-fractions, payload)
    faces_pos   : tuple of int (face label per anchor, 0 or 1)
    n_dec       : declared carrier size (context hint; upper bound on n_min)
    n_min       : minimal carrier = LCM of denominators of non-zero thetas
    """

    def __init__(
        self,
        n_dec: int,
        n_min: int,
        anchors_pos,
        faces_pos,
    ):
        self.n_dec = int(n_dec)
        self._anchors_raw = tuple(anchors_pos)
        self._faces_raw = tuple(faces_pos)
        # Normalization populates .anchors_pos, .faces_pos, .n_min.
        self.anchors_pos: Tuple[AnchorPayload, ...] = self._anchors_raw
        self.faces_pos: Tuple[int, ...] = self._faces_raw
        self.n_min = int(n_min)
        self._do_normalize()

    def _do_normalize(self):
        """Shift so first anchor is at 0; recompute n_min from thetas."""
        if not self._anchors_raw:
            self.anchors_pos = ()
            self.faces_pos = ()
            self.n_min = 1
            return

        theta0 = self._anchors_raw[0].theta
        normalized = []
        for ap in self._anchors_raw:
            new_theta = (ap.theta - theta0) % 2
            normalized.append(AnchorPayload(new_theta, ap.payload))

        self.anchors_pos = tuple(normalized)
        self.faces_pos = self._faces_raw

        non_zero_denoms = [
            ap.theta.denominator
            for ap in self.anchors_pos
            if ap.theta != 0
        ]
        self.n_min = _reduce_lcm(non_zero_denoms) if non_zero_denoms else 1

    def normalize(self) -> "UCNSObject":
        """Return self (normalization happens at construction time)."""
        return self

    def equivalent(self, other: "UCNSObject") -> bool:
        """Deep structural equivalence."""
        if not isinstance(other, UCNSObject):
            return False
        a = self
        b = other
        if len(a.anchors_pos) != len(b.anchors_pos):
            return False
        if a.faces_pos != b.faces_pos:
            return False
        for ap, bp in zip(a.anchors_pos, b.anchors_pos):
            if ap.theta != bp.theta:
                return False
            if ap.payload is None and bp.payload is None:
                continue
            if ap.payload is None or bp.payload is None:
                return False
            if not ap.payload.equivalent(bp.payload):
                return False
        return True

    def __repr__(self) -> str:
        thetas = [str(ap.theta) for ap in self.anchors_pos]
        return f"UCNSObject(n_dec={self.n_dec}, n_min={self.n_min}, thetas={thetas})"


def unit_obj() -> UCNSObject:
    """Return the multiplicative unit: single anchor at theta=0, no payload."""
    return UCNSObject(
        n_dec=1,
        n_min=1,
        anchors_pos=(AnchorPayload(Fraction(0), None),),
        faces_pos=(0,),
    )


def is_unit_payload(obj: Optional[UCNSObject]) -> bool:
    """True if obj is None (no payload) or structurally equivalent to the unit."""
    if obj is None:
        return True
    return obj.equivalent(unit_obj())


def multiply(A: UCNSObject, B: UCNSObject) -> UCNSObject:
    """
    UCNS product A ⊠ B.

    Each anchor a_k of A is combined with each anchor b_j of B to yield
    a result anchor with:
      theta   = (a_k.theta + b_j.theta) % 2
      payload = multiply(a_k.payload, b_j.payload)  [recursive; None is unit]
      face    = a_k.face XOR b_j.face

    The result has len(A.anchors_pos) * len(B.anchors_pos) anchors, ordered
    A-major (outer loop over A, inner loop over B).

    The single-anchor unit_obj() is a two-sided identity under this product.
    The product is associative.
    """
    new_anchors = []
    new_faces = []

    for ai, ak in enumerate(A.anchors_pos):
        for bi, bj in enumerate(B.anchors_pos):
            theta = (ak.theta + bj.theta) % 2

            pa = ak.payload
            pb = bj.payload
            if pa is None and pb is None:
                payload = None
            elif pa is None:
                payload = pb
            elif pb is None:
                payload = pa
            else:
                payload = multiply(pa, pb)

            face = A.faces_pos[ai] ^ B.faces_pos[bi]
            new_anchors.append(AnchorPayload(theta, payload))
            new_faces.append(face)

    n_dec = _lcm(A.n_dec, B.n_dec)
    return UCNSObject(
        n_dec=n_dec,
        n_min=1,
        anchors_pos=tuple(new_anchors),
        faces_pos=tuple(new_faces),
    )
