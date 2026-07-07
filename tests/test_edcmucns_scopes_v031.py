"""edcmucns v0.3.1 — scope registry, SeqAppend/product separation, cadence/flesh."""

from __future__ import annotations

from fractions import Fraction

import pytest

from edcm.edcmucns import (
    BoneEvent,
    Payload,
    PolicyManifest,
    REGISTRY,
    ReadoutScope,
    UnknownReadoutScopeError,
    active_families,
    edcm_measurement_equivalent,
    encode_turn,
    flat_reduction,
    interaction_product,
    lambda_field,
    make_cadence_anchor,
    n_family,
    n_payload,
    operator_shares,
    resolve_scope,
    seq_append,
    with_cadence,
    L_geo,
    L_op,
)
from edcm.edcmucns import geometry as geometry_module

MANIFEST = PolicyManifest()


def _window(turn_id, events, **kw):
    return encode_turn(turn_id, "A", events, MANIFEST, **kw).window


# --- closed registry ---------------------------------------------------------

def test_registry_is_closed_to_arbitrary_strings():
    a = _window("t1", [BoneEvent("P", "not")])
    with pytest.raises(UnknownReadoutScopeError):
        edcm_measurement_equivalent(a, a, "arbitrary_scope")
    with pytest.raises(UnknownReadoutScopeError):
        resolve_scope("operator")  # near-miss names are not admitted
    forged = ReadoutScope(name="operator_scope", reads=(), excludes=(), mass=None)
    with pytest.raises(UnknownReadoutScopeError):
        resolve_scope(forged)


def test_registry_holds_the_five_v031_scopes():
    assert set(REGISTRY) == {
        "operator_scope", "payload_scope", "cadence_scope",
        "field_scope", "bridge_scope",
    }
    assert REGISTRY["operator_scope"].mass == "L_op"
    assert "n_family" in REGISTRY["cadence_scope"].excludes


# --- SeqAppend and product separation ---------------------------------------

def test_seqappend_length_adds():
    a = _window("t1", [BoneEvent("P", "not"), BoneEvent("P", "never")])
    b = _window("t2", [BoneEvent("K", "all")])
    assert seq_append(a, b).length == a.length + b.length


def test_product_length_multiplies():
    a = _window("t1", [BoneEvent("P", "not"), BoneEvent("P", "never")])
    b = _window("t2", [BoneEvent("K", "all")])
    sig = a.length * b.length
    product = interaction_product(a, b)
    assert product.length == sig
    assert product.kind == "interaction_product"


def test_window_operator_shares_equal_v1_counts_under_seqappend():
    a = _window("t1", [BoneEvent("P", "not"), BoneEvent("P", "never"),
                       BoneEvent("K", "all")])
    b = _window("t2", [BoneEvent("K", "each")])
    combined = seq_append(a, b)
    # Shares come from summed v1 counts: P=2, K=2 of 4 bones.
    assert operator_shares(combined) == {"P": Fraction(1, 2), "K": Fraction(1, 2)}


def test_window_operator_shares_do_not_use_mean_average():
    a = _window("t1", [BoneEvent("P", "not"), BoneEvent("P", "never"),
                       BoneEvent("K", "all")])
    b = _window("t2", [BoneEvent("K", "each")])
    combined = seq_append(a, b)
    mean_p = (operator_shares(a).get("P", Fraction(0))
              + operator_shares(b).get("P", Fraction(0))) / 2
    assert operator_shares(combined)["P"] != mean_p


def test_A_then_B_not_equivalent_to_B_then_A():
    a = _window("t1", [BoneEvent("P", "not")])
    b = _window("t2", [BoneEvent("K", "all")])
    ab = seq_append(a, b)
    ba = seq_append(b, a)
    # Chronological order is readout-bearing testimony.
    assert not edcm_measurement_equivalent(ab, ba, "operator_scope")


# --- cadence and flesh -------------------------------------------------------

def test_cadence_anchor_allows_composite_lattice():
    anchor = make_cadence_anchor(ordinal=1, lattice_n=6)  # 6 is composite
    assert anchor.role == "cadence"
    assert anchor.lattice_n == 6


def test_cadence_anchor_preserves_regular_motion():
    thetas = [make_cadence_anchor(m, 6).theta for m in range(1, 6)]
    steps = {b - a for a, b in zip(thetas, thetas[1:])}
    assert steps == {Fraction(1, 6)}  # rhythm: even 1/n steps, no distortion


def test_n_family_excludes_cadence_anchors():
    w = _window("t1", [BoneEvent("P", "not")])
    with_rhythm = with_cadence(w, make_cadence_anchor(1, 6))
    assert n_family(with_rhythm) == n_family(w) == 3


def test_composite_cadence_does_not_emit_family_prime_event():
    w = _window("t1", [BoneEvent("P", "not")])
    with_rhythm = with_cadence(w, make_cadence_anchor(1, 6))
    assert active_families(with_rhythm) == ("P",)  # no new family event
    assert all(a.family is None for a in with_rhythm.anchors if a.role == "cadence")


def test_payload_flat_reduction_preserves_bone_counts():
    w = _window("t1", [BoneEvent("P", "not"), BoneEvent("K", "all")],
                payloads=(Payload("pl1", carrier_n=4, content="flesh"),))
    reduced = flat_reduction(w)
    assert L_op(reduced) == L_op(w) == 2
    assert reduced.payloads == ()


def test_closed_payload_reduces_to_unit():
    open_payload = Payload("pl1", carrier_n=4, status="open")
    closed_payload = Payload("pl1", carrier_n=4, status="closed")
    assert open_payload.reduced_carrier == 4
    assert closed_payload.reduced_carrier == 1
    w = _window("t1", [BoneEvent("P", "not")], payloads=(closed_payload,))
    assert n_payload(w) == 1


# --- field load --------------------------------------------------------------

def test_load_density_does_not_alias_L_geo_or_L_op():
    w = _window("t1", [BoneEvent("P", "not"), BoneEvent("K", "all")],
                tok_count=8, raised_field_count=2)
    density = lambda_field(w)
    assert density == Fraction(1, 4)
    assert density != L_geo(w) and density != L_op(w)
    # The name L_W must not exist anywhere in the geometry surface.
    assert not hasattr(geometry_module, "L_W")


def test_load_density_absent_substrate_is_not_zero():
    w = _window("t1", [BoneEvent("P", "not")])  # tok_count == 0
    assert lambda_field(w) is None  # NA, not 0
