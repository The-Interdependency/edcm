"""Dictionary-bounded molecular analysis for the OEWN 2025 run.

The graph is complete relative to the declared affix inventory and written
rendering rules. Every matching affix decomposition is retained; no preferred
English convention deletes another valid molecular reading. Explicit spaced or
hyphenated compounds are recursively composed by the same operation.
"""

# === MODULE_BUILD ===
# id: edcm_language_morphology
#   module_name: morphology
#   module_kind: engine
#   summary: derives the run root set and the complete affix/compound decomposition DAG for every OEWN surface while preserving all valid alternatives
#   owner: Erin Spencer
#   public_surface: Decomposition, MorphologyGraph, build_morphology_graph
#   internal_surface: _compound_parts, _alternative_key
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_full_run
#   rollout: builder_only
#   rollback: restore the prior graph builder and regenerate all molecular artifacts
#   requires: edcm_language_affixes, edcm_language_rendering, edcm_language_model
#   since: 2026-07-13
#   unresolved: closed compounds without explicit dictionary separators remain whole roots unless an affix analysis reaches them
# === END MODULE_BUILD ===

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Iterable, Iterator, Mapping

from .affixes import AffixRecord
from .model import CompositionNode
from .rendering import inverse_affix_candidates, normalize_lemma


@dataclass(frozen=True, slots=True)
class Decomposition:
    """One immediate molecular reading of a surface expression."""

    rule: str
    parts: tuple[str, ...]
    affix_id: str | None = None
    rendering: str | None = None

    def __post_init__(self) -> None:
        if len(self.parts) < 2:
            raise ValueError("a decomposition must contain at least two parts")


@dataclass(frozen=True, slots=True)
class MorphologyGraph:
    """Complete finite decomposition DAG over the materialized dictionary set."""

    surfaces: tuple[str, ...]
    roots: tuple[str, ...]
    alternatives: Mapping[str, tuple[Decomposition, ...]]

    def is_root(self, surface: str) -> bool:
        return normalize_lemma(surface) in frozenset(self.roots)

    def immediate(self, surface: str) -> tuple[Decomposition, ...]:
        return self.alternatives.get(normalize_lemma(surface), ())

    def primary_tree(self, surface: str) -> CompositionNode:
        """Return one deterministic tree without deleting alternative metadata."""

        normalized = normalize_lemma(surface)
        memo: dict[str, CompositionNode] = {}

        def build(value: str) -> CompositionNode:
            if value in memo:
                return memo[value]
            alternatives = self.alternatives.get(value, ())
            if not alternatives:
                node = CompositionNode.leaf(f"root:{value}")
            else:
                selected = min(alternatives, key=_alternative_key)
                children: list[CompositionNode] = []
                for part in selected.parts:
                    if part.startswith("affix:"):
                        children.append(CompositionNode.leaf(part))
                    else:
                        children.append(build(part.removeprefix("surface:")))
                node = CompositionNode.compose(*children)
            memo[value] = node
            return node

        if normalized not in set(self.surfaces):
            raise KeyError(normalized)
        return build(normalized)

    def metadata_record(self) -> dict[str, object]:
        return {
            "schema": "edcm.english-morphology-graph",
            "version": "1.0.0",
            "surface_count": len(self.surfaces),
            "root_count": len(self.roots),
            "alternative_count": sum(len(values) for values in self.alternatives.values()),
            "roots": list(self.roots),
            "alternatives": {
                surface: [asdict(item) for item in values]
                for surface, values in sorted(self.alternatives.items())
            },
        }


def _compound_parts(surface: str, surface_set: frozenset[str]) -> Iterator[tuple[str, ...]]:
    """Yield only explicitly marked compounds; closed compounds remain whole."""

    for separator in (" ", "-"):
        if separator not in surface:
            continue
        parts = tuple(part for part in surface.split(separator) if part)
        if len(parts) >= 2 and all(part in surface_set for part in parts):
            yield parts


def _alternative_key(item: Decomposition) -> tuple[int, int, str, tuple[str, ...]]:
    # Prefer longest affix evidence, then fewer immediate parts, then stable text.
    affix_length = 0 if item.rendering is None else len(item.rendering.replace("-", ""))
    return (-affix_length, len(item.parts), item.rule, item.parts)


def build_morphology_graph(
    surfaces: Iterable[str],
    affixes: Iterable[AffixRecord],
) -> MorphologyGraph:
    """Build the complete finite run graph.

    Every affix is tested against every surface through reversible rendering.
    A decomposition becomes dictionary-sound for this run when its base is also
    present in the selected materialized surface set. Universal validity exists
    beyond this finite graph and is represented by the renderer itself.
    """

    ordered_surfaces = tuple(sorted({normalize_lemma(value) for value in surfaces if value.strip()}))
    surface_set = frozenset(ordered_surfaces)
    affix_values = tuple(affixes)
    alternatives: dict[str, tuple[Decomposition, ...]] = {}

    for surface in ordered_surfaces:
        found: set[Decomposition] = set()
        for affix in affix_values:
            for base in inverse_affix_candidates(surface, affix):
                if base not in surface_set or len(base) >= len(surface):
                    continue
                affix_leaf = f"affix:{affix.affix_id}"
                surface_leaf = f"surface:{base}"
                if affix.kind == "prefix":
                    parts = (affix_leaf, surface_leaf)
                else:
                    parts = (surface_leaf, affix_leaf)
                found.add(
                    Decomposition(
                        rule=f"affix-{affix.kind}",
                        parts=parts,
                        affix_id=affix.affix_id,
                        rendering=affix.surface,
                    )
                )
        for parts in _compound_parts(surface, surface_set):
            found.add(
                Decomposition(
                    rule="explicit-compound",
                    parts=tuple(f"surface:{part}" for part in parts),
                    rendering=("space" if " " in surface else "hyphen"),
                )
            )
        if found:
            alternatives[surface] = tuple(sorted(found, key=_alternative_key))

    roots = tuple(surface for surface in ordered_surfaces if surface not in alternatives)
    return MorphologyGraph(
        surfaces=ordered_surfaces,
        roots=roots,
        alternatives=alternatives,
    )


__all__ = ["Decomposition", "MorphologyGraph", "build_morphology_graph"]
