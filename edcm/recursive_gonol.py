"""EDCM recursive-gonol candidate constructor.

Usage guidance
--------------
This is an implemented candidate, not selected canon. It closes one recursive
gonol from already-closed word, definition, or recursive gonols plus an exact
caller-supplied relation identity. It does not infer the relation from
adjacency, reopen participants, or invent UCNS coupling geometry.

    from edcm.character_word import construct_character_word_gonols
    from edcm.recursive_gonol import construct_recursive_gonol, replay_recursive_gonol

    words = construct_character_word_gonols("cut divide", source_id="example")
    first = construct_recursive_gonol(
        relation="example:ordered-pair",
        participants=words.words,
        source_id="example:pair#1",
    )
    second = replay_recursive_gonol(
        relation="example:ordered-pair",
        participants=words.words,
        source_id="example:pair#1",
    )
    assert first.receipt_digest == second.receipt_digest

Frozen choices for ``edcm.recursive_gonol/v1``:

- participants are already-closed ``WordGonol``, ``DefinitionGonol``, or
  ``RecursiveGonol`` values;
- at least two participants are required;
- the relation identity is the exact caller-supplied string;
- participants remain atomic and recoverable;
- the closed recursive gonol may itself participate in a later relation;
- UCNS geometric coupling remains unresolved and is not filled;
- pronunciation, morphology, and adjacency grammar are not used.

Do not pass character gonols. Close words first. Do not treat a WordNet edge
table or other sidecar graph as this constructor.
"""

# === MODULE_BUILD ===
# id: edcm_recursive_gonol
#   module_name: recursive_gonol
#   module_kind: engine
#   summary: named EDCM candidate that closes recursive gonols from already-closed word, definition, or recursive gonols and an exact caller-supplied relation without inventing UCNS geometry or selecting canon
#   owner: Erin Spencer
#   public_surface: CONSTRUCTOR_ID, CONSTRUCTOR_VERSION, RecursiveGonol, RecursiveGonolError, RecursiveGonolReceipt, construct_recursive_gonol, replay_recursive_gonol
#   internal_surface: _scale_of, _kind_payload, _participant_payload, _receipt_payload, _digest
#   auth_boundary: consumes closed EDCM gonols; does not invent UCNS coupling geometry
#   storage_boundary: none; receipts remain caller-owned in-memory objects
#   network_boundary: none
#   user_data_boundary: caller-supplied relation identity and participant gonols remain in memory and are not transmitted
#   admin_only: false
#   tests: tests.test_recursive_gonol
#   rollout: explicit candidate constructor; no measurement activation and no UCNS coupling law
#   rollback: remove this module; character_word and definition_gonol remain unchanged
#   requires: edcm_character_word_gonol, edcm_definition_gonol
#   since: 2026-08-21
#   unresolved: UCNS geometric operation of each Public Gonol function position; Möbius-carrier affixiation/coupling law; which recursive relations are later selected; complete English morphology law
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: recursive_uses_closed_gonols
#   given: ordered already-closed word, definition, or recursive gonols and an exact relation identity
#   then: the recursive gonol participants are those gonols without reopening their internal character streams
#   class: construction
#   since: 2026-08-21
#
# id: recursive_relation_is_caller_supplied
#   given: the relation identity is missing, empty, or inferred from adjacency
#   then: construction fails closed rather than inventing a linguistic or geometric relation
#   class: safety
#   since: 2026-08-21
#
# id: recursive_result_may_participate
#   given: a recursive gonol is closed
#   then: that gonol may be supplied as a participant in a later recursive construction while remaining atomic
#   class: construction
#   since: 2026-08-21
#
# id: recursive_candidate_does_not_select_canon
#   given: a receipt is minted
#   then: standing is implemented-candidate, selection_effect is none, and measurement, UCNS coupling, and relation-inventory claims remain nonclaims
#   class: doctrine
#   since: 2026-08-21
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping, Sequence, Union

from .character_word import CharacterGonol, WordGonol
from .definition_gonol import DefinitionGonol


CONSTRUCTOR_ID = "edcm.recursive_gonol"
CONSTRUCTOR_VERSION = "v1"
STANDING = "implemented-candidate"
SELECTION_EFFECT = "none"

FROZEN_CHOICES: tuple[tuple[str, str], ...] = (
    ("participants", "closed-word-definition-or-recursive-gonols"),
    ("minimum_participants", "2"),
    ("relation", "caller-supplied-exact-identity"),
    ("ucns_coupling", "hmmm"),
    ("pronunciation", "ignored"),
    ("morphology", "not-a-stage"),
)

NONCLAIMS: tuple[str, ...] = (
    "not selected canon",
    "not EDCM measurement validity",
    "not a UCNS geometric coupling law",
    "not a dictionary, WordNet, or sense-inventory graph",
    "not complete English morphology law",
    "not adjacency or punctuation grammar",
    "not METAPAT canon promotion",
)

HMMM: tuple[str, ...] = (
    "exact UCNS geometric operation of each Public Gonol function position",
    "UCNS Möbius-carrier affixiation/coupling law",
    "which recursive relations, if any, are later selected",
    "source-supported complete English morphology law",
)

ClosedGonol = Union[WordGonol, DefinitionGonol, "RecursiveGonol"]


class RecursiveGonolError(RuntimeError):
    """Fail-closed recursive constructor error."""


@dataclass(frozen=True, slots=True)
class RecursiveGonol:
    """Closed recursive gonol whose participants are already-closed gonols."""

    occurrence: int
    relation: str
    participants: tuple[ClosedGonol, ...]

    @property
    def kind_id(self) -> tuple[str, tuple[tuple[str, Any], ...]]:
        return (
            self.relation,
            tuple((_scale_of(item), item.kind_id) for item in self.participants),
        )


@dataclass(frozen=True, slots=True)
class RecursiveGonolReceipt:
    """Deterministic recursive receipt. Digest is replay identity, not gonol identity."""

    constructor_id: str
    constructor_version: str
    standing: str
    selection_effect: str
    source_id: str
    frozen_choices: tuple[tuple[str, str], ...]
    recursive: RecursiveGonol
    nonclaims: tuple[str, ...]
    hmmm: tuple[str, ...]
    receipt_digest: str


def _scale_of(item: ClosedGonol) -> str:
    if isinstance(item, WordGonol):
        return "word"
    if isinstance(item, DefinitionGonol):
        return "definition"
    if isinstance(item, RecursiveGonol):
        return "recursive"
    raise RecursiveGonolError("participants must be closed word, definition, or recursive gonols")


def _kind_payload(kind_id: Any) -> Any:
    if isinstance(kind_id, tuple):
        return [_kind_payload(item) for item in kind_id]
    if isinstance(kind_id, list):
        return [_kind_payload(item) for item in kind_id]
    return kind_id


def _participant_payload(item: ClosedGonol) -> dict[str, Any]:
    return {
        "scale": _scale_of(item),
        "occurrence": item.occurrence,
        "kind_id": _kind_payload(item.kind_id),
    }


def _receipt_payload(*, source_id: str, recursive: RecursiveGonol) -> dict[str, Any]:
    return {
        "constructor_id": CONSTRUCTOR_ID,
        "constructor_version": CONSTRUCTOR_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "source_id": source_id,
        "frozen_choices": [list(item) for item in FROZEN_CHOICES],
        "relation": recursive.relation,
        "participants": [_participant_payload(item) for item in recursive.participants],
        "kind_id": _kind_payload(recursive.kind_id),
        "nonclaims": list(NONCLAIMS),
        "hmmm": list(HMMM),
    }


def _digest(payload: Mapping[str, Any]) -> str:
    return sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def construct_recursive_gonol(
    *,
    relation: str,
    participants: Sequence[ClosedGonol],
    source_id: str,
) -> RecursiveGonolReceipt:
    """Close one recursive gonol from already-closed gonols and an exact relation."""

    if not isinstance(relation, str) or not relation or relation.isspace():
        raise RecursiveGonolError("relation must be an exact non-empty caller-supplied identity")
    if not isinstance(source_id, str) or not source_id:
        raise RecursiveGonolError("source_id must be a non-empty string")
    if not isinstance(participants, Sequence) or isinstance(participants, (str, bytes)):
        raise RecursiveGonolError("participants must be an ordered sequence of closed gonols")
    closed = tuple(participants)
    if len(closed) < 2:
        raise RecursiveGonolError("recursive construction requires at least two closed gonols")
    for item in closed:
        if isinstance(item, CharacterGonol):
            raise RecursiveGonolError("character gonols are not recursive participants; close words first")
        _scale_of(item)

    recursive = RecursiveGonol(occurrence=0, relation=relation, participants=closed)
    payload = _receipt_payload(source_id=source_id, recursive=recursive)
    return RecursiveGonolReceipt(
        constructor_id=CONSTRUCTOR_ID,
        constructor_version=CONSTRUCTOR_VERSION,
        standing=STANDING,
        selection_effect=SELECTION_EFFECT,
        source_id=source_id,
        frozen_choices=FROZEN_CHOICES,
        recursive=recursive,
        nonclaims=NONCLAIMS,
        hmmm=HMMM,
        receipt_digest=_digest(payload),
    )


def replay_recursive_gonol(
    *,
    relation: str,
    participants: Sequence[ClosedGonol],
    source_id: str,
) -> RecursiveGonolReceipt:
    """Independently reconstruct the same declared recursive relation."""

    return construct_recursive_gonol(
        relation=relation,
        participants=participants,
        source_id=source_id,
    )


__all__ = [
    "CONSTRUCTOR_ID",
    "CONSTRUCTOR_VERSION",
    "RecursiveGonol",
    "RecursiveGonolError",
    "RecursiveGonolReceipt",
    "construct_recursive_gonol",
    "replay_recursive_gonol",
]
