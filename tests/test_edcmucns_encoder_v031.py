"""edcmucns v0.3.1 — residue/origin and NA/absent-geometry tests (handoff list)."""

from __future__ import annotations

from fractions import Fraction

import pytest

from edcm.edcmucns import (
    AbsentOperatorGeometry,
    Anchor,
    BoneEvent,
    PolicyManifest,
    Present,
    admit_cadence_from_text,
    bone_theta,
    encode_turn,
    n_host_total,
    non_origin_residue,
    L_geo,
    L_op,
    operator_presence_readout,
)
from edcm.ucns_objects import ConstraintField

MANIFEST = PolicyManifest()
GAUGE = MANIFEST.gauge


def _single_bone_window(family):
    turn = encode_turn("t1", "A", [BoneEvent(family, "x")], MANIFEST)
    assert isinstance(turn, Present)
    return turn.window


def test_ordinal_wrap_never_lands_on_origin():
    for family, p in GAUGE.items():
        for m in range(1, 3 * p + 1):
            r = non_origin_residue(m, p)
            assert 1 <= r <= p - 1, (family, m, r)
            assert bone_theta(m, p) != 0


def test_phase_zero_requires_explicit_datum_role():
    # Non-datum roles cannot occupy theta=0 — Anchor construction refuses a
    # bone at the origin, and the origin role is pinned to theta=0/face=0.
    with pytest.raises(ValueError):
        Anchor(role="bone", family="P", lattice_n=3, ordinal=None,
               residue=None, theta=Fraction(0), face=1)
    with pytest.raises(ValueError):
        Anchor(role="origin", family=None, lattice_n=1, ordinal=None,
               residue=None, theta=Fraction(1, 3), face=0)


@pytest.mark.parametrize(
    "family,expected",
    [("P", 3), ("K", 5), ("Q", 7), ("T", 13), ("S", 29)],
    ids=["single_P_bone_forces_n_min_3", "single_K_bone_forces_n_min_5",
         "single_Q_bone_forces_n_min_7", "single_T_bone_forces_n_min_13",
         "single_S_bone_forces_n_min_29"],
)
def test_single_family_bone_forces_n_min(family, expected):
    assert n_host_total(_single_bone_window(family)) == expected


def test_all_families_force_39585():
    events = [BoneEvent(f, f.lower()) for f in ("P", "K", "Q", "T", "S")]
    turn = encode_turn("t1", "A", events, MANIFEST)
    assert n_host_total(turn.window) == 39585  # 3*5*7*13*29


def test_origin_anchors_excluded_from_operator_mass():
    w = _single_bone_window("P")
    assert L_geo(w) == 2  # origin datum + one bone
    assert L_op(w) == 1  # bone only


def test_empty_field_readouts_are_NA_not_zero():
    cf = ConstraintField(grain="round", raised_field_count=0)
    for readout in cf.behavioral_readouts().values():
        assert readout.state.enabled is False  # NA, not an enabled 0
    assert cf.contact_state().enabled is False


def test_no_bone_turn_has_no_operator_geometry():
    turn = encode_turn("t2", "B", [], MANIFEST, text_surface="mm-hmm")
    assert isinstance(turn, AbsentOperatorGeometry)
    # Not unit, not zero: the operator readout is NA and the content lens
    # event stays available.
    state = operator_presence_readout(turn)
    assert state.enabled is False
    assert turn.event.reason == "no_bone_geometry"
    assert turn.event.text_surface == "mm-hmm"


def test_cadence_admission_from_text_is_reserved():
    with pytest.raises(NotImplementedError):
        admit_cadence_from_text("some transcript text")
