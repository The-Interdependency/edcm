"""edcmucns v0.3.1 — regression tests for the PR #11 review findings.

Each test pins one correctness fix: face-to-anchor pairing in carrier
equivalence, unit-origin anchors, payload tension in the payload hash, the
canonical prime-gauge enforcement, witness role-mismatch diagnostics, and the
validate_window manifest-boundary check.
"""

from __future__ import annotations

import dataclasses
from fractions import Fraction

import pytest

from edcm.edcmucns import (
    Anchor,
    BoneEvent,
    Payload,
    PolicyManifest,
    edcm_measurement_equivalent,
    encode_turn,
    gauge_audit,
    ucns_carrier_equivalent,
    validate_window,
)
from edcm.edcmucns.manifest import DEFAULT_FAMILY_PRIME_GAUGE

MANIFEST = PolicyManifest()


def _window(events, turn_id="t1", speaker="A", manifest=MANIFEST, **kw):
    return encode_turn(turn_id, speaker, events, manifest, **kw).window


# --- P1: face-to-anchor pairing in carrier equivalence ----------------------

def test_carrier_equivalence_pairs_face_with_angle():
    # Same angle set, same face multiset {+1, -1}, but faces attached to
    # different angles: P+ K- versus P- K+.
    a = _window([BoneEvent("P", "x", face=1), BoneEvent("K", "y", face=-1)])
    b = _window([BoneEvent("P", "x", face=-1), BoneEvent("K", "y", face=1)])
    assert not ucns_carrier_equivalent(a, b)
    # And operator-scope equivalence (witness carries no face) must not paper
    # over it either.
    assert not edcm_measurement_equivalent(a, b, "operator_scope")
    # gauge_audit already treated this pairing as a divergence/mismatch.
    assert gauge_audit(a, b)
    # Identical windows stay equivalent.
    assert ucns_carrier_equivalent(a, _window(
        [BoneEvent("P", "x", face=1), BoneEvent("K", "y", face=-1)]))


# --- P2: origin anchors are unit datum anchors ------------------------------

def test_non_unit_origin_anchor_is_rejected():
    with pytest.raises(ValueError):
        Anchor(role="origin", family=None, lattice_n=3, ordinal=None,
               residue=None, theta=Fraction(0), face=0)


def test_origin_anchor_rejects_family_metadata():
    for bad in (
        dict(family="P"),
        dict(ordinal=1),
        dict(residue=2),
    ):
        kw = dict(role="origin", family=None, lattice_n=1, ordinal=None,
                  residue=None, theta=Fraction(0), face=0)
        kw.update(bad)
        with pytest.raises(ValueError):
            Anchor(**kw)


# --- P2: payload tension participates in identity ---------------------------

def test_payload_tension_changes_hash_and_payload_scope():
    low = Payload("pl1", status="open", tension=1)
    high = Payload("pl1", status="open", tension=5)
    assert low.content_hash != high.content_hash
    a = _window([BoneEvent("P", "x")], payloads=(low,))
    b = _window([BoneEvent("P", "x")], payloads=(high,))
    assert ucns_carrier_equivalent(a, b)
    assert not edcm_measurement_equivalent(a, b, "payload_scope")


# --- P2: canonical prime gauge is enforced ----------------------------------

def test_manifest_rejects_composite_gauge():
    bad = (("P", 4), ("K", 5), ("Q", 7), ("T", 13), ("S", 29))
    with pytest.raises(ValueError):
        PolicyManifest(family_prime_gauge=bad)


def test_manifest_rejects_missing_family():
    incomplete = (("P", 3), ("K", 5), ("Q", 7), ("T", 13))
    with pytest.raises(ValueError):
        PolicyManifest(family_prime_gauge=incomplete)


def test_manifest_accepts_canonical_gauge():
    canonical = tuple(sorted(DEFAULT_FAMILY_PRIME_GAUGE.items()))
    assert PolicyManifest(family_prime_gauge=canonical).gauge == DEFAULT_FAMILY_PRIME_GAUGE


# --- P2: witness role-mismatch diagnostic -----------------------------------

def test_witness_role_mismatch_emits_diagnostic():
    w = _window([BoneEvent("P", "x")])
    assert validate_window(w, MANIFEST) == []  # clean baseline
    bad_witness = dataclasses.replace(w.witnesses[0], role="cadence")
    tampered = dataclasses.replace(w, witnesses=(bad_witness,))
    diags = validate_window(tampered, MANIFEST)
    assert any(d.kind == "witness_role_mismatch" for d in diags)


# --- P2: validate_window checks the supplied manifest -----------------------

def test_validate_window_flags_manifest_boundary():
    w = _window([BoneEvent("P", "x")])
    other = PolicyManifest(polarity_dictionary_version="v032-draft")
    # Same family gauge, different policy version -> different manifest hash.
    diags = validate_window(w, other)
    assert any(d.kind == "manifest_epoch_mismatch" for d in diags)
    # Validated against its own manifest, no boundary diagnostic.
    assert all(d.kind != "manifest_epoch_mismatch" for d in validate_window(w, MANIFEST))
