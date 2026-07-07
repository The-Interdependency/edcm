"""edcmucns v0.3.1 — epoch breaks and kappa ledger placeholder tests."""

from __future__ import annotations

import pytest

from edcm.edcmucns import (
    BoneEvent,
    BridgeDiagnostic,
    EpochBreakError,
    EpochChain,
    Payload,
    PolicyManifest,
    V031_ADOPTION_NOTE,
    compare_across_epochs,
    encode_turn,
    kappa_audit,
    kappa_balance,
    seq_append,
)

MANIFEST = PolicyManifest()
ROTATED = PolicyManifest(polarity_dictionary_version="v032-draft")


def _window(manifest=MANIFEST, **kw):
    return encode_turn("t1", "A", [BoneEvent("P", "not")], manifest, **kw).window


def test_manifest_rotation_breaks_chain_epoch():
    chain = EpochChain(MANIFEST)
    w = _window()
    chain.record(w)

    boundary = chain.rotate(ROTATED, boundary_window=w)
    old, new = chain.segments
    assert old.sealed and old.boundary is boundary
    assert boundary.old_manifest_hash == MANIFEST.manifest_hash()
    assert boundary.new_manifest_hash == ROTATED.manifest_hash()
    assert boundary.boundary_window_hash is not None
    assert new.manifest_hash == ROTATED.manifest_hash() and not new.sealed

    # The chain refuses to continue across the manifest change.
    with pytest.raises(EpochBreakError):
        chain.record(w)
    chain.record(_window(manifest=ROTATED))


def test_seqappend_refuses_cross_manifest_hash_chains():
    with pytest.raises(EpochBreakError):
        seq_append(_window(), _window(manifest=ROTATED))


def test_cross_epoch_comparison_is_a_bridge_lensing_event():
    diag = compare_across_epochs(_window(), _window(manifest=ROTATED))
    assert isinstance(diag, BridgeDiagnostic)
    assert diag.kind == "cross_epoch_lens"
    # Same-epoch windows are not a lensing case.
    with pytest.raises(ValueError):
        compare_across_epochs(_window(), _window())


def test_adopting_v031_is_itself_an_epoch_break():
    assert "epoch break" in V031_ADOPTION_NOTE
    assert "non_origin_residue_v031" in V031_ADOPTION_NOTE


# --- kappa ledger placeholders ----------------------------------------------

def test_kappa_balance_zero_on_closed_span():
    w = _window(payloads=(
        Payload("pl1", carrier_n=4, status="closed", tension=2),
        Payload("pl2", status="closed"),
    ))
    balance, diags = kappa_audit(w)
    assert balance == 0
    assert diags == []


def test_kappa_balance_residual_emits_leak_event():
    w = _window(payloads=(Payload("pl1", status="open", tension=2),))
    balance, diags = kappa_audit(w)
    assert balance == 2
    assert [d.kind for d in diags] == ["kappa_leak"]


def test_unresolved_payload_contributes_to_kappa():
    resolved = _window(payloads=(Payload("pl1", status="closed", tension=3),))
    unresolved = _window(payloads=(Payload("pl1", status="open", tension=3),))
    assert kappa_balance(resolved) == 0
    assert kappa_balance(unresolved) == 3
