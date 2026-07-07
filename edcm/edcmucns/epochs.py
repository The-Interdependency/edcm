# === MODULE_BUILD ===
# id: edcmucns_epochs
#   module_name: epochs
#   module_kind: engine
#   summary: Epoch chain for edcmucns v0.3.1 — manifest rotation seals the segment and opens a new epoch; cross-epoch comparisons are Bridge lensing events, not raw deltas
#   owner: Erin Spencer
#   public_surface: EpochBoundary, EpochSegment, EpochChain, window_identity_hash, compare_across_epochs, V031_ADOPTION_NOTE
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_edcmucns_epochs_v031
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: edcmucns_manifest,edcmucns_types,edcmucns_provenance,edcmucns_composer
#   since: 2026-07-06
#   unresolved: none
# === END MODULE_BUILD ===

"""Epoch chain for edcmucns v0.3.1.

Living weights need lineage. Manifest rotation is a chain epoch break: seal
the current segment, log old_manifest / new_manifest / boundary_window, open
a new epoch sealed with the new manifest hash. Hash chains never continue
across a manifest change, and cross-epoch comparisons are Bridge lensing
events rather than raw deltas.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from .composer import EpochBreakError
from .manifest import PolicyManifest
from .provenance import bundle_hash
from .types import BridgeDiagnostic, Window

# Adopting v0.3.1 is itself an epoch break: the ordinal->angle rule changed
# from the old modulo rule to the non-origin residue rule.
V031_ADOPTION_NOTE = (
    "adopting edcmucns v0.3.1 is an epoch break (ordinal->angle rule changed "
    "to non_origin_residue_v031); do not continue pre-v0.3.1 hash chains"
)


def window_identity_hash(window: Window) -> str:
    """Stable identity hash of a window (geometry + testimony + manifest)."""

    geometry = ";".join(
        f"{a.role}:{a.family}:{a.lattice_n}:{a.ordinal}:{a.theta}:{a.face}"
        for a in window.anchors
    )
    blob = "|".join((
        geometry,
        bundle_hash(window.witnesses),
        ",".join(sorted(p.content_hash for p in window.payloads)),
        window.manifest_hash,
    ))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class EpochBoundary:
    """The logged rotation record: old manifest, new manifest, boundary window."""

    old_manifest_hash: str
    new_manifest_hash: str
    boundary_window_hash: str | None


@dataclass(slots=True)
class EpochSegment:
    """One chain segment, sealed with a single manifest hash."""

    manifest_hash: str
    entries: list[str] = field(default_factory=list)
    sealed: bool = False
    boundary: EpochBoundary | None = None


class EpochChain:
    """A measurement hash chain segmented by manifest epochs."""

    def __init__(self, manifest: PolicyManifest) -> None:
        self._segments: list[EpochSegment] = [EpochSegment(manifest.manifest_hash())]

    @property
    def segments(self) -> tuple[EpochSegment, ...]:
        return tuple(self._segments)

    @property
    def current(self) -> EpochSegment:
        return self._segments[-1]

    def record(self, window: Window) -> str:
        """Append a window to the current epoch; refuses cross-manifest records."""

        if window.manifest_hash != self.current.manifest_hash:
            raise EpochBreakError(
                "window manifest differs from the current epoch; rotate the "
                "chain before recording"
            )
        h = window_identity_hash(window)
        self.current.entries.append(h)
        return h

    def rotate(self, new_manifest: PolicyManifest,
               boundary_window: Window | None = None) -> EpochBoundary:
        """Manifest rotation: seal the segment, log the break, open a new epoch."""

        old = self.current
        boundary = EpochBoundary(
            old_manifest_hash=old.manifest_hash,
            new_manifest_hash=new_manifest.manifest_hash(),
            boundary_window_hash=(
                window_identity_hash(boundary_window)
                if boundary_window is not None else None
            ),
        )
        old.sealed = True
        old.boundary = boundary
        self._segments.append(EpochSegment(new_manifest.manifest_hash()))
        return boundary


def compare_across_epochs(a: Window, b: Window) -> BridgeDiagnostic:
    """Cross-epoch comparison is a Bridge lensing event, not a raw delta."""

    if a.manifest_hash == b.manifest_hash:
        raise ValueError(
            "windows share a manifest epoch; use edcm_measurement_equivalent"
        )
    return BridgeDiagnostic(
        kind="cross_epoch_lens",
        detail="windows belong to different manifest epochs; readings are "
               "lensed, not directly comparable",
        expected=a.manifest_hash,
        observed=b.manifest_hash,
    )
