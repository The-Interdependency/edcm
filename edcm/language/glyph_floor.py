"""Compatibility access to the UCNS-owned public gonol.

EDCM does not construct or own the public 157-gonal. The canonical source is
the UCNS public package, promoted from ``a0-betatest@7af8deb``. This module is a
lazy compatibility adapter so importing the base EDCM package does not imply
that the optional UCNS integration is installed or active.
"""

# === MODULE_BUILD ===
# id: edcm_language_glyph_floor
#   module_name: glyph_floor
#   module_kind: adapter
#   summary: lazily consumes the UCNS-owned public gonol without retaining a competing EDCM arrangement authority
#   owner: Erin Spencer
#   public_surface: PUBLIC_GLYPH_FLOOR_157, build_public_glyph_floor_157, validate_public_glyph_floor, glyph_floor_sha256, UCNSPublicGonolDependencyError, UCNSPublicGonolContractError
#   internal_surface: _load_ucns_public_gonol, _PublicGonolProxy
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: package_import_only
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_relational_bridge
#   rollout: compatibility_only
#   rollback: restore only after reverting canonical ownership to the exact pinned UCNS source
#   requires: edcm_language_manifest
#   since: 2026-07-16
#   unresolved: canonical public-gonol to EDCM language-object bridge remains hmmm
# === END MODULE_BUILD ===

from __future__ import annotations

import hashlib
import importlib
from collections.abc import Iterator, Sequence
from types import ModuleType

from .manifest import PUBLIC_GLYPH_FLOOR_SHA256

_EXPECTED_A0_SOURCE_COMMIT = "7af8debf6ef3905f01baff02b43d8c3bee16ccbc"


class UCNSPublicGonolDependencyError(ModuleNotFoundError):
    """Raised when the optional canonical UCNS public gonol is unavailable."""


class UCNSPublicGonolContractError(RuntimeError):
    """Raised when an installed UCNS package lacks or drifts from the canon."""


def _load_ucns_public_gonol() -> ModuleType:
    try:
        module = importlib.import_module("ucns")
    except ModuleNotFoundError as exc:
        if exc.name != "ucns":
            raise
        raise UCNSPublicGonolDependencyError(
            "EDCM no longer owns a public-gonol copy; install the pinned UCNS integration",
            name="ucns",
        ) from exc

    required = (
        "PUBLIC_GONOL_157",
        "PUBLIC_GONOL_SHA256",
        "public_gonol_sha256",
    )
    missing = tuple(name for name in required if not hasattr(module, name))
    if missing:
        raise UCNSPublicGonolContractError(
            "installed ucns is missing canonical public-gonol surfaces: "
            + ", ".join(missing)
        )
    try:
        source_module = importlib.import_module("ucns.edcm")
    except ModuleNotFoundError as exc:
        raise UCNSPublicGonolContractError(
            "installed ucns is missing the EDCM public-gonol source surface"
        ) from exc
    if (
        getattr(source_module, "PUBLIC_GONOL_SOURCE_COMMIT", None)
        != _EXPECTED_A0_SOURCE_COMMIT
    ):
        raise UCNSPublicGonolContractError("UCNS public-gonol source commit mismatch")
    glyphs = tuple(module.PUBLIC_GONOL_157)
    if len(glyphs) != 157 or glyphs[0] != " ":
        raise UCNSPublicGonolContractError("UCNS public gonol lost its fixed SPACE/ZERO origin")
    producer_digest = module.public_gonol_sha256(glyphs)
    compatibility_digest = hashlib.sha256(
        ("\n".join(glyphs) + "\n").encode("utf-8")
    ).hexdigest()
    if (
        producer_digest != module.PUBLIC_GONOL_SHA256
        or compatibility_digest != PUBLIC_GLYPH_FLOOR_SHA256
    ):
        raise UCNSPublicGonolContractError("UCNS public-gonol arrangement digest mismatch")
    return module


class _PublicGonolProxy(Sequence[str]):
    """Read-only lazy sequence backed exclusively by the UCNS public canon."""

    def _glyphs(self) -> tuple[str, ...]:
        return tuple(_load_ucns_public_gonol().PUBLIC_GONOL_157)

    def __getitem__(self, index):
        return self._glyphs()[index]

    def __len__(self) -> int:
        return len(self._glyphs())

    def __iter__(self) -> Iterator[str]:
        return iter(self._glyphs())

    def __repr__(self) -> str:
        return "<UCNS-owned public gonol; lazy EDCM compatibility view>"


def build_public_glyph_floor_157() -> tuple[str, ...]:
    """Return a caller-owned immutable view of the UCNS public gonol."""

    return tuple(_load_ucns_public_gonol().PUBLIC_GONOL_157)


def glyph_floor_sha256(glyphs: Sequence[str]) -> str:
    """Hash the one-glyph-per-line arrangement without defining its authority."""

    return hashlib.sha256(("\n".join(glyphs) + "\n").encode("utf-8")).hexdigest()


def validate_public_glyph_floor(glyphs: Sequence[str]) -> None:
    """Require exact equality with the UCNS-owned canon."""

    canonical = build_public_glyph_floor_157()
    candidate = tuple(glyphs)
    if candidate != canonical:
        raise UCNSPublicGonolContractError("EDCM glyph input differs from UCNS public gonol")


PUBLIC_GLYPH_FLOOR_157: Sequence[str] = _PublicGonolProxy()


__all__ = [
    "PUBLIC_GLYPH_FLOOR_157",
    "UCNSPublicGonolDependencyError",
    "UCNSPublicGonolContractError",
    "build_public_glyph_floor_157",
    "glyph_floor_sha256",
    "validate_public_glyph_floor",
]
