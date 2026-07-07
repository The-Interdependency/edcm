"""edcmucns v0.3.1 — provenance/geometry identity and polarity-gauge tests."""

from __future__ import annotations

import dataclasses

import pytest

from edcm.edcmucns import (
    BoneEvent,
    Payload,
    PolicyManifest,
    Window,
    contact_convergence,
    edcm_measurement_equivalent,
    encode_turn,
    gauge_audit,
    ucns_carrier_equivalent,
    validate_window,
)

MANIFEST = PolicyManifest()
EVENTS = [BoneEvent("P", "not"), BoneEvent("K", "all", face=-1), BoneEvent("Q", "why")]


def _window(turn_id="t1", speaker="A", events=None, manifest=MANIFEST, **kw) -> Window:
    return encode_turn(turn_id, speaker, events or EVENTS, manifest, **kw).window


def test_family_witness_must_match_manifest_prime_geometry():
    assert validate_window(_window(), MANIFEST) == []


def test_family_geometry_mismatch_emits_bridge_diagnostic():
    w = _window()
    # Tamper with one witness's residue: geometry and testimony now disagree.
    bad = dataclasses.replace(w.witnesses[0], residue_r_f=2)
    tampered = dataclasses.replace(w, witnesses=(bad,) + w.witnesses[1:])
    diags = validate_window(tampered, MANIFEST)
    assert any(d.kind == "residue_rule_mismatch" for d in diags)
    # The mismatch is a diagnostic, never a silent alternate reading.
    assert all(d.kind != "" for d in diags)


def test_ucns_carrier_equivalent_ignores_edcm_witness():
    a = _window(turn_id="t1")
    b = _window(turn_id="t2")  # same geometry, different testimony
    assert ucns_carrier_equivalent(a, b)
    assert not edcm_measurement_equivalent(a, b, "operator_scope")


def test_measurement_equivalence_requires_manifest_and_in_scope_witness():
    a = _window()
    b = _window()
    assert edcm_measurement_equivalent(a, b, "operator_scope")

    other_manifest = PolicyManifest(polarity_dictionary_version="v032-draft")
    c = _window(manifest=other_manifest)
    assert ucns_carrier_equivalent(a, c)
    assert not edcm_measurement_equivalent(a, c, "operator_scope")


def test_same_geometry_different_turn_id_changes_turn_sensitive_readout():
    a = _window(turn_id="t1")
    b = _window(turn_id="t9")
    assert ucns_carrier_equivalent(a, b)
    assert not edcm_measurement_equivalent(a, b, "operator_scope")


def test_same_geometry_different_speaker_changes_speaker_scoped_readout():
    a = _window(speaker="A")
    b = _window(speaker="B")
    assert ucns_carrier_equivalent(a, b)
    assert not edcm_measurement_equivalent(a, b, "operator_scope")


def test_same_geometry_different_payload_hash_changes_payload_readout():
    a = _window(payloads=(Payload("pl1", content="alpha"),))
    b = _window(payloads=(Payload("pl1", content="beta"),))
    assert ucns_carrier_equivalent(a, b)
    assert not edcm_measurement_equivalent(a, b, "payload_scope")
    # Operator scope excludes flesh payload content.
    assert edcm_measurement_equivalent(a, b, "operator_scope")


def test_same_geometry_different_policy_manifest_changes_measurement_identity():
    a = _window()
    b = _window(manifest=PolicyManifest(lens_readout_policy_version="v032-draft"))
    for scope in ("operator_scope", "payload_scope", "cadence_scope",
                  "field_scope", "bridge_scope"):
        assert not edcm_measurement_equivalent(a, b, scope), scope


def test_gauge_audit_scoped_to_bone_faces():
    # Identical bone faces: silent, regardless of datum anchors.
    assert gauge_audit(_window(), _window()) == []


def test_constant_xor_face_flip_reports_gauge_mismatch():
    flipped = [dataclasses.replace(e, face=-e.face) for e in EVENTS]
    diags = gauge_audit(_window(), _window(events=flipped))
    assert [d.kind for d in diags] == ["gauge_mismatch"]


def test_nonconstant_face_difference_reports_measurement_divergence():
    partly = [dataclasses.replace(EVENTS[0], face=-EVENTS[0].face)] + EVENTS[1:]
    diags = gauge_audit(_window(), _window(events=partly))
    assert [d.kind for d in diags] == ["measurement_divergence"]


def test_contact_convergence_is_a_typed_placeholder():
    with pytest.raises(NotImplementedError):
        contact_convergence(_window(), _window())
