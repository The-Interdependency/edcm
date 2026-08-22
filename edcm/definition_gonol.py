"""EDCM definition-gonol candidate constructor.

Usage guidance
--------------
This is an implemented candidate, not selected canon. It constructs one
definition gonol from already-closed word gonols plus exact caller-supplied
definition evidence. It does not load a dictionary, invent a gloss, or reopen
closed words.

    from edcm.definition_gonol import (
        construct_definition_gonol,
        replay_definition_gonol,
    )

    first = construct_definition_gonol(
        headword="cut",
        definition="to divide with a sharp edge",
        source_id="example:cut#1",
    )
    second = replay_definition_gonol(
        headword="cut",
        definition="to divide with a sharp edge",
        source_id="example:cut#1",
    )
    assert first.receipt_digest == second.receipt_digest

Frozen choices for ``edcm.definition_gonol/v1``:

- definition evidence is the exact ``headword`` and ``definition`` strings plus
  ``source_id`` supplied by the caller;
- both strings are constructed through ``edcm.character_word``;
- closed word gonols participate atomically and are not reopened;
- the intrinsic relation is ``definition-of``: ordered headword words plus
  ordered definition-body words;
- pronunciation is ignored and must not be passed as a substitute gloss;
- no lemma, stem, morphology, or sense-inventory is inferred;
- each call constructs one definition gonol; multiple senses remain multiple
  gonols.

Historical OEWN and lexical-floor artifacts are not this constructor. Pass
their exact sense text as ``definition`` only when reproducing that source
identity.
"""

# === MODULE_BUILD ===
# id: edcm_definition_gonol
#   module_name: definition_gonol
#   module_kind: engine
#   summary: named EDCM candidate that affixiates already-closed word gonols with exact caller-supplied definition evidence into one definition gonol without selecting canon, inventing glosses, or activating measurement
#   owner: Erin Spencer
#   public_surface: CONSTRUCTOR_ID, CONSTRUCTOR_VERSION, RELATION, DefinitionGonol, DefinitionGonolError, DefinitionGonolReceipt, construct_definition_gonol, replay_definition_gonol
#   internal_surface: _require_words, _word_payload, _receipt_payload, _digest
#   auth_boundary: consumes edcm.character_word and therefore the pinned UCNS Public Gonol digest
#   storage_boundary: none; receipts remain caller-owned in-memory objects
#   network_boundary: none
#   user_data_boundary: caller-supplied headword and definition text remain in memory and are not transmitted
#   admin_only: false
#   tests: tests.test_definition_gonol
#   rollout: explicit candidate constructor; no measurement or recursive-relation activation
#   rollback: remove this module; character_word and historical lexical-floor evidence remain unchanged
#   requires: edcm_character_word_gonol
#   since: 2026-08-21
#   unresolved: UCNS geometric operation of each Public Gonol function position; Möbius-carrier affixiation/coupling law; which recursive relations are later selected; complete English morphology law; selection among competing definition sources
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: definition_uses_closed_word_gonols
#   given: headword and definition strings are admitted
#   then: both are constructed through character_word and the definition gonol participants are those closed word gonols without reopening their characters as a free stream
#   class: construction
#   since: 2026-08-21
#
# id: definition_requires_exact_source_evidence
#   given: definition evidence is missing, empty of words, or not a string
#   then: construction fails closed rather than inventing a gloss or loading a dictionary
#   class: safety
#   since: 2026-08-21
#
# id: definition_relation_is_intrinsic
#   given: a definition gonol is closed
#   then: the relation definition-of enters the construction as ordered headword words plus ordered body words with recoverable nested receipts
#   class: construction
#   since: 2026-08-21
#
# id: definition_candidate_does_not_select_canon
#   given: a receipt is minted
#   then: standing is implemented-candidate, selection_effect is none, and measurement, recursion, morphology, and dictionary-authority remain nonclaims
#   class: doctrine
#   since: 2026-08-21
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

from .character_word import CharacterWordReceipt, WordGonol, construct_character_word_gonols


CONSTRUCTOR_ID = "edcm.definition_gonol"
CONSTRUCTOR_VERSION = "v1"
RELATION = "definition-of"
STANDING = "implemented-candidate"
SELECTION_EFFECT = "none"

FROZEN_CHOICES: tuple[tuple[str, str], ...] = (
    ("word_constructor", "edcm.character_word_gonol/v1"),
    ("definition_evidence", "caller-supplied-exact-strings"),
    ("relation", RELATION),
    ("pronunciation", "ignored"),
    ("morphology", "not-a-stage"),
    ("sense_inventory", "one-definition-per-call"),
)

NONCLAIMS: tuple[str, ...] = (
    "not selected canon",
    "not EDCM measurement validity",
    "not a recursive-relation constructor",
    "not complete English morphology law",
    "not a dictionary or sense inventory",
    "not a UCNS geometric function operation",
    "not METAPAT canon promotion",
    "not OEWN or lexical-floor revival",
)

HMMM: tuple[str, ...] = (
    "exact UCNS geometric operation of each Public Gonol function position",
    "UCNS Möbius-carrier affixiation/coupling law",
    "which recursive relations, if any, are later selected",
    "source-supported complete English morphology law",
    "which definition source, if any, is later selected",
)


class DefinitionGonolError(RuntimeError):
    """Fail-closed definition constructor error."""


@dataclass(frozen=True, slots=True)
class DefinitionGonol:
    """Closed definition gonol whose participants are already-closed words."""

    occurrence: int
    relation: str
    headword_words: tuple[WordGonol, ...]
    body_words: tuple[WordGonol, ...]

    @property
    def kind_id(self) -> tuple[tuple[tuple[str, ...], ...], tuple[tuple[str, ...], ...]]:
        return (
            tuple(word.kind_id for word in self.headword_words),
            tuple(word.kind_id for word in self.body_words),
        )


@dataclass(frozen=True, slots=True)
class DefinitionGonolReceipt:
    """Deterministic definition receipt. Digest is replay identity, not gonol identity."""

    constructor_id: str
    constructor_version: str
    standing: str
    selection_effect: str
    source_id: str
    frozen_choices: tuple[tuple[str, str], ...]
    headword_receipt: CharacterWordReceipt
    definition_receipt: CharacterWordReceipt
    definition: DefinitionGonol
    nonclaims: tuple[str, ...]
    hmmm: tuple[str, ...]
    receipt_digest: str


def _require_words(receipt: CharacterWordReceipt, *, field: str) -> tuple[WordGonol, ...]:
    if not receipt.words:
        raise DefinitionGonolError(
            f"{field} produced no closed word gonols; exact source evidence is required"
        )
    return receipt.words


def _word_payload(word: WordGonol) -> dict[str, Any]:
    return {
        "occurrence": word.occurrence,
        "source_start": word.source_start,
        "source_end": word.source_end,
        "kind_id": list(word.kind_id),
        "character_occurrences": [item.occurrence for item in word.characters],
    }


def _receipt_payload(
    *,
    source_id: str,
    headword_receipt: CharacterWordReceipt,
    definition_receipt: CharacterWordReceipt,
    definition: DefinitionGonol,
) -> dict[str, Any]:
    return {
        "constructor_id": CONSTRUCTOR_ID,
        "constructor_version": CONSTRUCTOR_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "source_id": source_id,
        "frozen_choices": [list(item) for item in FROZEN_CHOICES],
        "relation": RELATION,
        "headword_receipt_digest": headword_receipt.receipt_digest,
        "definition_receipt_digest": definition_receipt.receipt_digest,
        "headword_words": [_word_payload(word) for word in definition.headword_words],
        "body_words": [_word_payload(word) for word in definition.body_words],
        "kind_id": [
            [list(word_kind) for word_kind in definition.kind_id[0]],
            [list(word_kind) for word_kind in definition.kind_id[1]],
        ],
        "nonclaims": list(NONCLAIMS),
        "hmmm": list(HMMM),
    }


def _digest(payload: Mapping[str, Any]) -> str:
    return sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def construct_definition_gonol(
    *,
    headword: str,
    definition: str,
    source_id: str,
) -> DefinitionGonolReceipt:
    """Close one definition gonol from exact headword and definition source text."""

    if not isinstance(headword, str):
        raise DefinitionGonolError("headword must be an exact Unicode string")
    if not isinstance(definition, str):
        raise DefinitionGonolError("definition must be an exact Unicode string")
    if not isinstance(source_id, str) or not source_id:
        raise DefinitionGonolError("source_id must be a non-empty string")

    headword_receipt = construct_character_word_gonols(
        headword,
        source_id=f"{source_id}#headword",
    )
    definition_receipt = construct_character_word_gonols(
        definition,
        source_id=f"{source_id}#definition",
    )
    definition_gonol = DefinitionGonol(
        occurrence=0,
        relation=RELATION,
        headword_words=_require_words(headword_receipt, field="headword"),
        body_words=_require_words(definition_receipt, field="definition"),
    )
    payload = _receipt_payload(
        source_id=source_id,
        headword_receipt=headword_receipt,
        definition_receipt=definition_receipt,
        definition=definition_gonol,
    )
    return DefinitionGonolReceipt(
        constructor_id=CONSTRUCTOR_ID,
        constructor_version=CONSTRUCTOR_VERSION,
        standing=STANDING,
        selection_effect=SELECTION_EFFECT,
        source_id=source_id,
        frozen_choices=FROZEN_CHOICES,
        headword_receipt=headword_receipt,
        definition_receipt=definition_receipt,
        definition=definition_gonol,
        nonclaims=NONCLAIMS,
        hmmm=HMMM,
        receipt_digest=_digest(payload),
    )


def replay_definition_gonol(
    *,
    headword: str,
    definition: str,
    source_id: str,
) -> DefinitionGonolReceipt:
    """Independently reconstruct the same declared definition source."""

    return construct_definition_gonol(
        headword=headword,
        definition=definition,
        source_id=source_id,
    )


__all__ = [
    "CONSTRUCTOR_ID",
    "CONSTRUCTOR_VERSION",
    "RELATION",
    "DefinitionGonol",
    "DefinitionGonolError",
    "DefinitionGonolReceipt",
    "construct_definition_gonol",
    "replay_definition_gonol",
]
