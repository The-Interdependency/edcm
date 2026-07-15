"""One scale-neutral UCNS composer for affixes, roots, words, and larger units."""

# === MODULE_BUILD ===
# id: edcm_language_composition
#   module_name: composition
#   module_kind: engine
#   summary: materializes explicit language composition trees through one UCNS product and compares independent direct atomic gonols with molecularly generated atomic views
#   owner: Erin Spencer
#   public_surface: GonolRegistry, compose_gonols, materialize, compare_atomic_fork, MissingGonolError
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_embeddings
#   rollout: default_enabled
#   rollback: remove language embedding package before any published artifact depends on this composer
#   requires: edcm_language_model, edcmbone_ucns_v04
#   since: 2026-07-13
#   unresolved: the maintained local UCNS engine is associative while explicit language grouping remains preserved as independent provenance for comparison
# === END MODULE_BUILD ===

from __future__ import annotations

from collections.abc import Iterable, Mapping

from edcm.measurement.ucns.ucns_v04 import UCNSObject, multiply, unit_obj

from .model import AtomicForkRelation, AtomicForkResult, CompositionNode


class MissingGonolError(KeyError):
    """Raised when a composition leaf has no assigned gonol."""


class GonolRegistry:
    """Metadata-side identity map; labels never enter intrinsic gonol data."""

    def __init__(self, assignments: Mapping[str, UCNSObject] | None = None) -> None:
        self._assignments: dict[str, UCNSObject] = dict(assignments or {})

    def assign(self, gonol_id: str, gonol: UCNSObject) -> None:
        if not gonol_id:
            raise ValueError("gonol_id must be non-empty")
        if not isinstance(gonol, UCNSObject):
            raise TypeError("gonol must be a UCNSObject")
        self._assignments[gonol_id] = gonol

    def resolve(self, gonol_id: str) -> UCNSObject:
        try:
            return self._assignments[gonol_id]
        except KeyError as exc:
            raise MissingGonolError(gonol_id) from exc

    def snapshot(self) -> dict[str, UCNSObject]:
        return dict(self._assignments)


def compose_gonols(parts: Iterable[UCNSObject]) -> UCNSObject:
    """Compose an ordered sequence without an avoidable unit multiplication.

    The universal unit remains the exact empty-sequence result. A non-empty
    sequence starts from its first validated part because ``unit × part`` is
    canonically equivalent to that part but allocates a redundant recursive
    copy for every molecular alternative.
    """

    iterator = iter(parts)
    try:
        result = next(iterator)
    except StopIteration:
        return unit_obj()
    if not isinstance(result, UCNSObject):
        raise TypeError("every composition part must be a UCNSObject")
    for part in iterator:
        if not isinstance(part, UCNSObject):
            raise TypeError("every composition part must be a UCNSObject")
        result = multiply(result, part)
    return result


def materialize(node: CompositionNode, registry: GonolRegistry) -> UCNSObject:
    """Materialize a molecular tree while preserving its grouping in metadata."""

    if node.leaf_id is not None:
        return registry.resolve(node.leaf_id)
    return compose_gonols(materialize(child, registry) for child in node.children)


def compare_atomic_fork(
    surface: str,
    molecular_tree: CompositionNode,
    molecular_registry: GonolRegistry,
    direct_atomic_registry: GonolRegistry,
) -> AtomicForkResult:
    """Compare an independent whole-word gonol with its generated atomic view."""

    generated = materialize(molecular_tree, molecular_registry)
    try:
        direct = direct_atomic_registry.resolve(surface)
    except MissingGonolError:
        return AtomicForkResult(
            surface,
            AtomicForkRelation.DIRECT_MISSING,
            molecular_tree,
        )
    relation = (
        AtomicForkRelation.EQUIVALENT
        if direct.equivalent(generated)
        else AtomicForkRelation.DIVERGENT
    )
    return AtomicForkResult(surface, relation, molecular_tree)


__all__ = [
    "GonolRegistry",
    "MissingGonolError",
    "compare_atomic_fork",
    "compose_gonols",
    "materialize",
]
