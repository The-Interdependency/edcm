# === MODULE_BUILD ===
# id: edcmucns_composer
#   module_name: composer
#   module_kind: engine
#   summary: SeqAppend window composition (chronological append; lengths add; F concatenates; carrier = lcm), reserved interaction product, payload flat reduction, kappa ledger placeholders
#   owner: Erin Spencer
#   public_surface: seq_append, InteractionSignature, interaction_product, flat_reduction, kappa_balance, kappa_audit, EpochBreakError
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_edcmucns_scopes_v031, tests.test_edcmucns_epochs_v031
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: edcmucns_types
#   since: 2026-07-06
#   unresolved: kappa ledger is an architecture placeholder — open-payload tension only; the full stored-tension circuit remains upstream/frontier
# === END MODULE_BUILD ===

"""Window composition for edcmucns v0.3.1.

EDCM windows compose by chronological append (⊞ SeqAppend): lengths add,
absolute lattice positions remain origin-anchored, F concatenates, mirrors
regenerate, carrier = lcm over host anchors in scope. UCNS product (⊠) is
reserved for interaction signatures, transport, factor trials, and
irreducibility analysis — product multiplies length and must not be used for
windows. Windows are never averaged.
"""

from __future__ import annotations

from dataclasses import dataclass

from .types import BridgeDiagnostic, Window


class EpochBreakError(ValueError):
    """Raised when composition would continue a hash chain across a manifest change."""


def seq_append(a: Window, b: Window) -> Window:
    """⊞ SeqAppend — chronological append of two windows.

    Lengths add; F (the face sequence) concatenates; payloads, witnesses and
    field chains concatenate; the carrier is recomputed as the lcm over host
    anchors by the geometry helpers. Appending across different manifest
    hashes is an epoch break, not a composition.
    """

    if a.manifest_hash != b.manifest_hash:
        raise EpochBreakError(
            "do not continue a hash chain across a manifest change; rotate "
            "the epoch chain instead"
        )
    return Window(
        anchors=a.anchors + b.anchors,
        witnesses=a.witnesses + b.witnesses,
        manifest_hash=a.manifest_hash,
        payloads=a.payloads + b.payloads,
        tok_count=a.tok_count + b.tok_count,
        raised_field_count=a.raised_field_count + b.raised_field_count,
        field_chain=a.field_chain + b.field_chain,
    )


@dataclass(frozen=True, slots=True)
class InteractionSignature:
    """Result shape of the reserved ⊠ product: not a window."""

    length: int
    left_length: int
    right_length: int
    kind: str = "interaction_product"


def interaction_product(a: Window, b: Window) -> InteractionSignature:
    """⊠ — reserved for interaction, transport, and irreducibility analysis.

    Product multiplies length. It deliberately does not return a Window:
    transcript windows compose with :func:`seq_append` only.
    """

    return InteractionSignature(
        length=a.length * b.length,
        left_length=a.length,
        right_length=b.length,
    )


def flat_reduction(window: Window) -> Window:
    """Reduce flesh payloads away, preserving all bone geometry and testimony."""

    return Window(
        anchors=window.anchors,
        witnesses=window.witnesses,
        manifest_hash=window.manifest_hash,
        payloads=(),
        tok_count=window.tok_count,
        raised_field_count=window.raised_field_count,
        field_chain=window.field_chain,
    )


def kappa_balance(window: Window) -> int:
    """Kappa ledger placeholder: unresolved payload tension over the span.

    A closed span (every payload closed) balances to zero. Architecture
    only — no empirical stored-tension claim.
    """

    return sum(p.tension for p in window.payloads if p.status != "closed")


def kappa_audit(window: Window) -> tuple[int, list[BridgeDiagnostic]]:
    """Return (balance, diagnostics); a nonzero balance emits a leak event."""

    balance = kappa_balance(window)
    if balance == 0:
        return 0, []
    return balance, [BridgeDiagnostic(
        kind="kappa_leak",
        detail="kappa balance residual on span (unresolved payload tension)",
        expected="0",
        observed=str(balance),
    )]
