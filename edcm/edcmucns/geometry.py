# === MODULE_BUILD ===
# id: edcmucns_geometry
#   module_name: geometry
#   module_kind: engine
#   summary: v0.3.1 non-origin residue rule, anchor angles, mass helpers (L_geo/L_op), carriers (n_host_total/n_family/n_cadence/n_payload), operator shares, lambda_field
#   owner: Erin Spencer
#   public_surface: non_origin_residue, bone_theta, cadence_theta, L_geo, L_op, bone_anchors, cadence_anchors, origin_anchors, n_host_total, n_family, n_cadence, n_payload, active_families, operator_shares, lambda_field, da_geom_correlation
#   internal_surface: _lcm_over
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_edcmucns_encoder_v031, tests.test_edcmucns_scopes_v031
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: edcmucns_types
#   since: 2026-07-06
#   unresolved: DA_geom correlation is frontier — placeholder raises NotImplementedError; cadence theta wrap at ordinal % n == 0 collides with the datum reservation and is left to the validator (hmmm)
# === END MODULE_BUILD ===

"""Geometry helpers for edcmucns v0.3.1.

Residue rule (v0.3.1, non-origin)::

    r_f(m) = 1 + ((m_f - 1) mod (p_f - 1))
    theta  = r_f(m) / p_f          (turn fraction)

Residues cycle through 1 .. p_f-1; theta = 0 is reserved for explicit datum
roles. Family-signature angles are labels, not cadence: the residue cycle
deliberately distorts ordinal periodicity; recurrence belongs to flesh
payloads or cadence scopes.

Mass and carriers::

    L_geo = all host anchors including datum anchors
    L_op  = family-signature bone anchors only
    lambda_field(W) = raised_field_count(W) / TOK      (never "L_W")

The claim "carrier factorization = active family set" applies only to
``n_family``. Payload carriers are epicyclic subobjects and are never
automatically part of host n_min.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Iterable

from .types import Anchor, Window


def non_origin_residue(ordinal: int, prime: int) -> int:
    """The v0.3.1 non-origin residue r_f(m). Never 0: theta never lands on origin."""

    if ordinal < 1:
        raise ValueError("ordinals are 1-based")
    if prime < 2:
        raise ValueError("family gauge must be >= 2")
    return 1 + ((ordinal - 1) % (prime - 1))


def bone_theta(ordinal: int, prime: int) -> Fraction:
    return Fraction(non_origin_residue(ordinal, prime), prime)


def cadence_theta(ordinal: int, lattice_n: int) -> Fraction:
    """Regular cadence motion: even 1/n steps, no residue distortion."""

    if lattice_n < 1:
        raise ValueError("cadence lattice_n must be >= 1")
    return Fraction(ordinal % lattice_n, lattice_n)


def origin_anchors(window: Window) -> tuple[Anchor, ...]:
    return tuple(a for a in window.anchors if a.role == "origin")


def bone_anchors(window: Window) -> tuple[Anchor, ...]:
    return tuple(a for a in window.anchors if a.role == "bone")


def cadence_anchors(window: Window) -> tuple[Anchor, ...]:
    return tuple(a for a in window.anchors if a.role == "cadence")


def L_geo(window: Window) -> int:
    """Geometric mass: all host anchors, datum anchors included."""

    return len(window.anchors)


def L_op(window: Window) -> int:
    """Operator mass: family-signature bone anchors only (origin excluded)."""

    return len(bone_anchors(window))


def _lcm_over(values: Iterable[int]) -> int:
    result = 1
    for v in values:
        result = math.lcm(result, v)
    return result


def n_host_total(window: Window) -> int:
    """Carrier over all host-level anchors in scope (window n_min)."""

    return _lcm_over(a.lattice_n for a in window.anchors)


def n_family(window: Window) -> int:
    """Carrier over family_signature_anchor host anchors only.

    Carrier factorization = active family set holds here and only here.
    Cadence anchors are excluded by construction.
    """

    return _lcm_over(a.lattice_n for a in bone_anchors(window))


def n_cadence(window: Window) -> int:
    """Carrier over cadence_motion_anchor host anchors (composite allowed)."""

    return _lcm_over(a.lattice_n for a in cadence_anchors(window))


def n_payload(window: Window) -> int:
    """Carrier over payload subobjects (epicyclic; closed payloads reduce to unit)."""

    return _lcm_over(p.reduced_carrier for p in window.payloads)


def active_families(window: Window) -> tuple[str, ...]:
    seen: list[str] = []
    for a in bone_anchors(window):
        if a.family is not None and a.family not in seen:
            seen.append(a.family)
    return tuple(seen)


def operator_shares(window: Window) -> dict[str, Fraction]:
    """Per-family operator shares from v1 counts.

    Shares are count ratios over the window's bone anchors. Under SeqAppend
    the appended window's shares equal the shares of the summed counts —
    never the mean average of the two windows' shares.
    """

    bones = bone_anchors(window)
    total = len(bones)
    shares: dict[str, Fraction] = {}
    if total == 0:
        return shares
    for a in bones:
        assert a.family is not None
        shares[a.family] = shares.get(a.family, Fraction(0)) + Fraction(1, total)
    return shares


def lambda_field(window: Window) -> Fraction | None:
    """Field load density lambda_field(W) = raised_field_count / TOK.

    Distinct from L_geo and L_op; never call this L_W. Returns None (NA)
    when the window carries no token count — absent substrate is not 0.
    """

    if window.tok_count <= 0:
        return None
    return Fraction(window.raised_field_count, window.tok_count)


def da_geom_correlation(*_args: object, **_kwargs: object) -> None:
    """FRONTIER — residual primality / DA_geom correlation is not implemented.

    Named falsifier: a corpus parallel run in which DA_geom fails to track
    the DA projection within the pre-registered tolerance refutes the
    correlation claim. Until that run exists, no code path may claim DA_geom
    works.
    """

    raise NotImplementedError(
        "frontier (v0.3.1): DA_geom correlation is an empirical claim, "
        "not architecture; see docs/codex_edcmucns_v031_handoff.md"
    )
