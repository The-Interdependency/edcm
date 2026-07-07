"""edcmucns v0.3.1 — field reader tests.

The field reader wires edcm.ucns_objects ConstraintField/FieldMotion into the
Window.field_chain that field_scope reads. Architecture only: geometry/state
readouts, NA-safe, no empirical operating-state claim.
"""

from __future__ import annotations

import pytest

from edcm.edcmucns import (
    BoneEvent,
    PolicyManifest,
    attach_field_chain,
    edcm_measurement_equivalent,
    encode_turn,
    field_chain_hashes,
    field_readouts,
    read_field_chain,
    ucns_carrier_equivalent,
    window_identity_hash,
)
from edcm.ucns_objects import ConstraintField

MANIFEST = PolicyManifest()


def _window():
    return encode_turn("t1", "A", [BoneEvent("P", "not")], MANIFEST).window


def _field(rfc, contact="against", resolution="open"):
    return ConstraintField(
        grain="round", raised_field_count=rfc, contact=contact, resolution=resolution
    )


def test_empty_and_single_field_chains():
    assert read_field_chain([]).chain == ()
    cf = _field(2)
    reading = read_field_chain([cf])
    # A single field yields just its field_hash, no motion.
    assert reading.chain == (cf.field_hash,)
    assert reading.motions == ()


def test_chain_interleaves_field_and_motion_hashes():
    a, b, c = _field(1), _field(2), _field(3)
    reading = read_field_chain([a, b, c])
    assert len(reading.motions) == 2
    # [field_a, motion_a->b, field_b, motion_b->c, field_c]
    assert reading.chain == (
        a.field_hash,
        reading.motions[0].parent_hash,
        b.field_hash,
        reading.motions[1].parent_hash,
        c.field_hash,
    )
    assert reading.motions[0].parent_hash == f"{a.field_hash}->{b.field_hash}"


def test_field_chain_hashes_convenience_matches_reader():
    fields = [_field(1), _field(2)]
    assert field_chain_hashes(fields) == read_field_chain(fields).chain


def test_attach_field_chain_populates_window_and_raised_count():
    w = _window()
    assert w.field_chain == () and w.raised_field_count == 0
    attached = attach_field_chain(w, [_field(2), _field(3)])
    assert attached.field_chain == field_chain_hashes([_field(2), _field(3)])
    assert attached.raised_field_count == 5  # 2 + 3
    # Geometry/testimony are untouched.
    assert attached.anchors == w.anchors and attached.witnesses == w.witnesses


def test_field_scope_distinguishes_by_field_chain():
    w = _window()
    a = attach_field_chain(w, [_field(2), _field(3)])
    b = attach_field_chain(w, [_field(2), _field(9)])
    # Same carrier geometry, different field state.
    assert ucns_carrier_equivalent(a, b)
    assert not edcm_measurement_equivalent(a, b, "field_scope")
    # Identical field chains are field-scope equivalent.
    c = attach_field_chain(w, [_field(2), _field(3)])
    assert edcm_measurement_equivalent(a, c, "field_scope")


def test_window_identity_hash_covers_field_chain():
    w = _window()
    a = attach_field_chain(w, [_field(2), _field(3)])
    b = attach_field_chain(w, [_field(2), _field(9)])
    # Field-readout changes cannot hide inside an epoch identity hash.
    assert window_identity_hash(a) != window_identity_hash(b)


def test_field_readouts_are_na_safe():
    # Empty fields -> state readouts NA; motion between two empty fields NA.
    empty = _field(0, contact=None, resolution=None)
    reading = read_field_chain([empty, empty])
    readouts = field_readouts(reading)
    assert readouts["state"], "expected R/D/I/L_resistance readouts"
    assert all(r.state.enabled is False for r in readouts["state"])  # NA, not 0
    assert all(r.state.enabled is False for r in readouts["motion"])


def test_motion_reads_length_must_match_transitions():
    with pytest.raises(ValueError):
        read_field_chain([_field(1), _field(2)], motion_reads=())  # needs 1 entry


def test_motion_reads_flow_into_readouts():
    a, b = _field(1), _field(2)
    reading = read_field_chain(
        [a, b], motion_reads=({"recurrence_reads": (1.0, 1.0)},)
    )
    motion = field_readouts(reading)["motion"]
    fixation = next(r for r in motion if r.metric_id.endswith("F.fixation"))
    # Positive recurrence reads -> enabled +1 fixation readout (present fields).
    assert fixation.state.enabled is True and fixation.state.s == 1
