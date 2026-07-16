"""Fail-closed boundary for the retired EDCM language-gonol placement laws.

The previous implementation copied the public gonol into EDCM, derived carrier
positions from hashes and dictionary evidence, and converted those positions
into local fractional angles. That model is not the A0/UCNS public gonol canon
and must not generate new artifacts.

EDCM may still inspect and hash already-existing local compatibility objects.
Constructing new affix, root, whole-word, or superposed language gonols is
blocked until an Erin-ratified bridge from the UCNS-owned public gonol exists.
"""

# === MODULE_BUILD ===
# id: edcm_language_placement
#   module_name: placement
#   module_kind: adapter
#   summary: retires noncanonical hash/evidence-derived language placement while retaining read-only compatibility inspection of existing objects
#   owner: Erin Spencer
#   public_surface: NonCanonicalLanguagePlacementError, require_canonical_language_placement, assign_affix_gonol, assign_root_gonol, assign_direct_atomic_gonol, superpose_gonols, compare_gonols, gonol_sha256
#   internal_surface: _update_intrinsic_hash, _payload_depth, _theta_set
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_embeddings, tests.test_language_full_run
#   rollout: fail_closed
#   rollback: restore placement only after an Erin-ratified UCNS public-gonol bridge and migration plan exist
#   requires: edcm_language_manifest
#   since: 2026-07-16
#   unresolved: public-gonol to EDCM language-object bridge remains hmmm
# === END MODULE_BUILD ===

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from typing import Any, Iterable, Mapping, Sequence
from weakref import WeakKeyDictionary

from edcm.measurement.ucns.ucns_v04 import UCNSObject

_RETIREMENT_MESSAGE = (
    "EDCM language-gonol placement is retired: the prior hash/evidence-derived "
    "Fraction(vertex, 157) construction is not the canonical public gonol. "
    "UCNS now owns the exact A0 public gonol, and no bridge into EDCM's local "
    "UCNSObject representation has been ratified."
)


class NonCanonicalLanguagePlacementError(RuntimeError):
    """Raised whenever retired placement would construct a new language gonol."""


def require_canonical_language_placement() -> None:
    """Fail closed until a canonical UCNS-to-EDCM language bridge is ratified."""

    raise NonCanonicalLanguagePlacementError(_RETIREMENT_MESSAGE)


_GONOL_HASH_CACHE: WeakKeyDictionary[UCNSObject, str] = WeakKeyDictionary()


def _update_intrinsic_hash(digest: Any, gonol: UCNSObject) -> None:
    """Hash an already-existing local compatibility object without re-placement."""

    digest.update(b'{"anchors":[')
    for index, anchor in enumerate(gonol.anchors_pos):
        if index:
            digest.update(b",")
        digest.update(b'{"payload":')
        if anchor.payload is None:
            digest.update(b"null")
        else:
            _update_intrinsic_hash(digest, anchor.payload)
        digest.update(b',"theta":[')
        digest.update(str(anchor.theta.numerator).encode("ascii"))
        digest.update(b",")
        digest.update(str(anchor.theta.denominator).encode("ascii"))
        digest.update(b"]}")
    digest.update(b'],"faces":[')
    for index, face_value in enumerate(gonol.faces_pos):
        if index:
            digest.update(b",")
        digest.update(str(face_value).encode("ascii"))
    digest.update(b'],"n_dec":')
    digest.update(str(gonol.n_dec).encode("ascii"))
    digest.update(b',"n_min":')
    digest.update(str(gonol.n_min).encode("ascii"))
    digest.update(b"}")


def gonol_sha256(gonol: UCNSObject) -> str:
    """Stable identity for an already-existing local compatibility object."""

    if not isinstance(gonol, UCNSObject):
        raise TypeError("gonol must be a UCNSObject")
    cached = _GONOL_HASH_CACHE.get(gonol)
    if cached is not None:
        return cached
    digest = sha256()
    _update_intrinsic_hash(digest, gonol)
    value = digest.hexdigest()
    _GONOL_HASH_CACHE[gonol] = value
    return value


def assign_affix_gonol(affix: Any) -> UCNSObject:
    require_canonical_language_placement()
    raise AssertionError("unreachable")


def assign_root_gonol(surface: str, lexemes: Sequence[Any]) -> UCNSObject:
    require_canonical_language_placement()
    raise AssertionError("unreachable")


def assign_direct_atomic_gonol(
    surface: str,
    lexemes: Sequence[Any],
    synset_map: Mapping[str, Any],
) -> UCNSObject:
    require_canonical_language_placement()
    raise AssertionError("unreachable")


def superpose_gonols(gonols: Iterable[UCNSObject]) -> UCNSObject:
    require_canonical_language_placement()
    raise AssertionError("unreachable")


def _payload_depth(gonol: UCNSObject) -> int:
    depths = [
        0 if anchor.payload is None else 1 + _payload_depth(anchor.payload)
        for anchor in gonol.anchors_pos
    ]
    return max(depths, default=0)


def _theta_set(gonol: UCNSObject) -> set[tuple[int, int]]:
    return {
        (anchor.theta.numerator, anchor.theta.denominator)
        for anchor in gonol.anchors_pos
    }


def compare_gonols(direct: UCNSObject, generated: UCNSObject) -> dict[str, Any]:
    """Inspect two already-existing local compatibility objects."""

    if not isinstance(direct, UCNSObject) or not isinstance(generated, UCNSObject):
        raise TypeError("compare_gonols requires existing UCNSObject values")
    direct_theta = _theta_set(direct)
    generated_theta = _theta_set(generated)
    union = direct_theta | generated_theta
    intersection = direct_theta & generated_theta
    direct_faces = Counter(direct.faces_pos)
    generated_faces = Counter(generated.faces_pos)
    return {
        "direct_sha256": gonol_sha256(direct),
        "generated_sha256": gonol_sha256(generated),
        "equivalent": direct.equivalent(generated),
        "carrier_equal": direct.n_min == generated.n_min,
        "direct_n_min": direct.n_min,
        "generated_n_min": generated.n_min,
        "direct_anchor_count": len(direct.anchors_pos),
        "generated_anchor_count": len(generated.anchors_pos),
        "theta_jaccard": 1.0 if not union else len(intersection) / len(union),
        "face_histogram_equal": direct_faces == generated_faces,
        "direct_face_histogram": dict(sorted(direct_faces.items())),
        "generated_face_histogram": dict(sorted(generated_faces.items())),
        "direct_payload_depth": _payload_depth(direct),
        "generated_payload_depth": _payload_depth(generated),
    }


__all__ = [
    "NonCanonicalLanguagePlacementError",
    "require_canonical_language_placement",
    "assign_affix_gonol",
    "assign_direct_atomic_gonol",
    "assign_root_gonol",
    "compare_gonols",
    "gonol_sha256",
    "superpose_gonols",
]
