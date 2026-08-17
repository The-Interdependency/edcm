"""Metadata-bearing records for atomic and molecular English gonols."""

# === MODULE_BUILD ===
# id: edcm_language_model
#   module_name: model
#   module_kind: schema
#   summary: defines explicit composition trees, evidence states, and direct/generated atomic comparison records without placing linguistic metadata inside gonols
#   owner: Erin Spencer
#   public_surface: CompositionNode, Attestation, Soundness, LexicalEvidence, AtomicForkRelation, AtomicForkResult
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_relational_bridge
#   rollout: default_enabled
#   rollback: remove language embedding package before any published artifact depends on these schemas
#   requires: none
#   since: 2026-07-13
#   unresolved: whether soundness will ultimately be indexed by context, technology, community, or all three
# === END MODULE_BUILD ===

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterator


class Attestation(str, Enum):
    """Evidence that a surface expression appears in the selected dictionary."""

    ATTESTED = "attested"
    UNATTESTED = "unattested"


class Soundness(str, Enum):
    """Grounding status inside the evidence boundary of this run."""

    SOUND = "sound"
    UNSOUND = "unsound"
    UNRESOLVED = "unresolved"


class AtomicForkRelation(str, Enum):
    """Observed relation between direct and molecularly generated atomic gonols."""

    EQUIVALENT = "equivalent"
    DIVERGENT = "divergent"
    DIRECT_MISSING = "direct-missing"


@dataclass(frozen=True)
class CompositionNode:
    """A scale-neutral, explicitly grouped composition of gonol identities.

    Affix-to-root, word-to-phrase, phrase-to-sentence, and every other scale use
    this same tree. A leaf names a gonol in an external registry; a branch groups
    ordered child gonols. The labels are metadata and never enter intrinsic
    gonol serialization.
    """

    leaf_id: str | None = None
    children: tuple["CompositionNode", ...] = ()

    def __post_init__(self) -> None:
        has_leaf = self.leaf_id is not None
        has_children = bool(self.children)
        if has_leaf == has_children:
            raise ValueError("a composition node must be exactly one leaf or one non-empty branch")

    @classmethod
    def leaf(cls, gonol_id: str) -> "CompositionNode":
        if not gonol_id:
            raise ValueError("gonol_id must be non-empty")
        return cls(leaf_id=gonol_id)

    @classmethod
    def compose(cls, *children: "CompositionNode") -> "CompositionNode":
        if not children:
            raise ValueError("composition requires at least one child")
        return cls(children=tuple(children))

    @property
    def is_leaf(self) -> bool:
        return self.leaf_id is not None

    def leaves(self) -> Iterator[str]:
        if self.leaf_id is not None:
            yield self.leaf_id
            return
        for child in self.children:
            yield from child.leaves()


@dataclass(frozen=True)
class LexicalEvidence:
    """Dictionary-bounded evidence for one rendered surface expression."""

    surface: str
    attestation: Attestation
    soundness: Soundness
    source_dictionary: str

    @property
    def valid(self) -> bool:
        """All universally composed expressions are structurally valid."""

        return True


@dataclass(frozen=True)
class AtomicForkResult:
    """Metadata-only comparison result for the direct/generated fork."""

    surface: str
    relation: AtomicForkRelation
    molecular_tree: CompositionNode


__all__ = [
    "AtomicForkRelation",
    "AtomicForkResult",
    "Attestation",
    "CompositionNode",
    "LexicalEvidence",
    "Soundness",
]
