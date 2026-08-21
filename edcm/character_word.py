"""EDCM character-to-word gonol candidate constructor.

Usage guidance
--------------
This is an implemented candidate, not selected canon. It owns EDCM text-domain
admission and word closure only. Import current UCNS Public Gonol geometry;
do not copy the carrier into EDCM.

    from edcm.character_word import construct_character_word_gonols, replay_character_word_gonols

    first = construct_character_word_gonols("don't cut.", source_id="example")
    second = replay_character_word_gonols("don't cut.", source_id="example")
    assert first.receipt_digest == second.receipt_digest

Frozen choices for ``edcm.character_word_gonol/v1``:

- admission unit: one Unicode scalar (code point), not a grapheme cluster;
- word closure: Python ``str.isspace()`` (Unicode White_Space) is the declared
  EDCM delimiter relation, not a UCNS function inferred from SPACE;
- Public Gonol position is attached when the scalar is on the current carrier;
  otherwise geometry remains unresolved;
- pronunciation is ignored;
- no case folding, NFC, trimming, or deduplication.

UCNS geometry is consumed through ``ucns.public_gonol``. Set
``UCNS_SOURCE_ROOT`` to a current UCNS checkout if the package is not
importable. The constructor fails closed on a Public Gonol digest mismatch.
"""

# === MODULE_BUILD ===
# id: edcm_character_word_gonol
#   module_name: character_word
#   module_kind: engine
#   summary: named EDCM candidate that admits Unicode-scalar character gonols and closes non-whitespace runs into word gonols while consuming current UCNS Public Gonol geometry without selecting canon or activating measurement
#   owner: Erin Spencer
#   public_surface: CONSTRUCTOR_ID, CONSTRUCTOR_VERSION, PINNED_PUBLIC_GONOL_SHA256, CharacterGonol, WordGonol, CharacterWordReceipt, CharacterWordError, construct_character_word_gonols, replay_character_word_gonols, canonical_receipt_bytes
#   internal_surface: _load_public_gonol, _character_record, _close_words, _receipt_payload, _digest
#   auth_boundary: current UCNS Public Gonol digest must match the pinned geometry identity
#   storage_boundary: none; receipts remain caller-owned in-memory objects
#   network_boundary: none
#   user_data_boundary: caller-supplied source text remains in memory and is not transmitted
#   admin_only: false
#   tests: tests.test_character_word_gonol
#   rollout: explicit candidate constructor; no measurement, definition, or recursive-relation activation
#   rollback: remove this module; historical lexical-floor and word-gonol observation adapters remain unchanged
#   requires: ucns.public_gonol
#   since: 2026-08-21
#   unresolved: UCNS geometric operation of each Public Gonol function position; Möbius-carrier affixiation/coupling law; recursive gonol constructor; complete English morphology law
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: character_admission_is_unicode_scalar
#   given: a source string is admitted
#   then: every Unicode scalar is one character gonol with occurrence index, exact scalar, and optional Public Gonol position
#   class: construction
#   since: 2026-08-21
#
# id: word_closure_uses_declared_whitespace
#   given: admitted character gonols include Unicode White_Space
#   then: maximal non-whitespace runs close into word gonols and whitespace remains separately addressable boundary gonols
#   class: construction
#   since: 2026-08-21
#
# id: closed_words_preserve_constituents
#   given: a word gonol is closed
#   then: constituent character identities, order, multiplicity, and source offsets remain recoverable and the word is atomic for later participation
#   class: construction
#   since: 2026-08-21
#
# id: geometry_mismatch_fails_closed
#   given: imported Public Gonol digest differs from the pinned identity
#   then: construction raises rather than copying or inventing a carrier
#   class: safety
#   since: 2026-08-21
#
# id: candidate_does_not_select_canon
#   given: a receipt is minted
#   then: standing is implemented-candidate, selection_effect is none, and measurement/definition/recursive claims remain nonclaims
#   class: doctrine
#   since: 2026-08-21
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import importlib
import json
import os
from pathlib import Path
import sys
from types import ModuleType
from typing import Any, Callable, Mapping


CONSTRUCTOR_ID = "edcm.character_word_gonol"
CONSTRUCTOR_VERSION = "v1"
PINNED_PUBLIC_GONOL_SHA256 = (
    "55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5"
)
STANDING = "implemented-candidate"
SELECTION_EFFECT = "none"

FROZEN_CHOICES: tuple[tuple[str, str], ...] = (
    ("admission_unit", "unicode-scalar"),
    ("word_delimiter", "python-str-isspace-unicode-white-space"),
    ("carrier", "ucns.public_gonol"),
    ("pronunciation", "ignored"),
    ("normalization", "none"),
)

NONCLAIMS: tuple[str, ...] = (
    "not selected canon",
    "not EDCM measurement validity",
    "not a definition gonol constructor",
    "not a recursive-relation constructor",
    "not complete English morphology law",
    "not a UCNS geometric function operation",
    "not METAPAT canon promotion",
)

HMMM: tuple[str, ...] = (
    "exact UCNS geometric operation of each Public Gonol function position",
    "UCNS Möbius-carrier affixiation/coupling law",
    "definition gonol constructor",
    "recursive gonol-relation constructor",
    "source-supported complete English morphology law",
)


class CharacterWordError(RuntimeError):
    """Fail-closed constructor error."""


@dataclass(frozen=True, slots=True)
class CharacterGonol:
    """One admitted Unicode-scalar character gonol."""

    occurrence: int
    scalar: str
    codepoint: int
    carrier_index: int | None
    role: str

    @property
    def kind_id(self) -> str:
        return self.scalar


@dataclass(frozen=True, slots=True)
class WordGonol:
    """Ordered non-whitespace character gonols closed as one word."""

    occurrence: int
    source_start: int
    source_end: int
    characters: tuple[CharacterGonol, ...]

    @property
    def kind_id(self) -> tuple[str, ...]:
        return tuple(character.scalar for character in self.characters)


@dataclass(frozen=True, slots=True)
class CharacterWordReceipt:
    """Deterministic construction receipt. Digest is replay identity, not gonol identity."""

    constructor_id: str
    constructor_version: str
    standing: str
    selection_effect: str
    source_id: str
    source_length: int
    carrier_digest: str
    frozen_choices: tuple[tuple[str, str], ...]
    characters: tuple[CharacterGonol, ...]
    words: tuple[WordGonol, ...]
    boundaries: tuple[CharacterGonol, ...]
    nonclaims: tuple[str, ...]
    hmmm: tuple[str, ...]
    receipt_digest: str


def _candidate_ucns_roots() -> tuple[Path, ...]:
    roots: list[Path] = []
    configured = os.environ.get("UCNS_SOURCE_ROOT")
    if configured:
        roots.append(Path(configured) / "src")
    sibling = Path(__file__).resolve().parents[2] / "ucns" / "src"
    if sibling.is_dir():
        roots.append(sibling)
    return tuple(roots)


def _load_public_gonol() -> ModuleType:
    try:
        module = importlib.import_module("ucns.public_gonol")
    except ImportError:
        module = None
        last_error: Exception | None = None
        for root in _candidate_ucns_roots():
            if str(root) not in sys.path:
                sys.path.insert(0, str(root))
            try:
                module = importlib.import_module("ucns.public_gonol")
                break
            except ImportError as exc:
                last_error = exc
        if module is None:
            raise CharacterWordError(
                "current UCNS public_gonol geometry is required; "
                "install ucns or set UCNS_SOURCE_ROOT"
            ) from last_error
    digest = str(getattr(module, "PUBLIC_GONOL_SHA256", ""))
    if digest != PINNED_PUBLIC_GONOL_SHA256:
        raise CharacterWordError(
            "UCNS Public Gonol digest mismatch: "
            f"constructor pins {PINNED_PUBLIC_GONOL_SHA256}, "
            f"imported {digest or 'missing'}"
        )
    return module


def _character_record(
    occurrence: int,
    scalar: str,
    position_of: Callable[[str], int | None],
    role: str,
) -> CharacterGonol:
    if not isinstance(scalar, str) or len(scalar) != 1:
        raise CharacterWordError("admission unit is exactly one Unicode scalar")
    codepoint = ord(scalar)
    if 0xD800 <= codepoint <= 0xDFFF:
        raise CharacterWordError("surrogate code points are not Unicode scalars")
    return CharacterGonol(
        occurrence=occurrence,
        scalar=scalar,
        codepoint=codepoint,
        carrier_index=position_of(scalar),
        role=role,
    )


def _close_words(
    characters: tuple[CharacterGonol, ...],
) -> tuple[tuple[WordGonol, ...], tuple[CharacterGonol, ...]]:
    words: list[WordGonol] = []
    boundaries: list[CharacterGonol] = []
    current: list[CharacterGonol] = []
    for character in characters:
        if character.scalar.isspace():
            if current:
                start = current[0].occurrence
                end = current[-1].occurrence + 1
                words.append(
                    WordGonol(
                        occurrence=len(words),
                        source_start=start,
                        source_end=end,
                        characters=tuple(current),
                    )
                )
                current = []
            boundaries.append(
                CharacterGonol(
                    occurrence=character.occurrence,
                    scalar=character.scalar,
                    codepoint=character.codepoint,
                    carrier_index=character.carrier_index,
                    role="boundary",
                )
            )
            continue
        current.append(
            CharacterGonol(
                occurrence=character.occurrence,
                scalar=character.scalar,
                codepoint=character.codepoint,
                carrier_index=character.carrier_index,
                role="word-member",
            )
        )
    if current:
        words.append(
            WordGonol(
                occurrence=len(words),
                source_start=current[0].occurrence,
                source_end=current[-1].occurrence + 1,
                characters=tuple(current),
            )
        )
    return tuple(words), tuple(boundaries)


def _character_payload(character: CharacterGonol) -> dict[str, Any]:
    return {
        "occurrence": character.occurrence,
        "scalar": character.scalar,
        "codepoint": character.codepoint,
        "carrier_index": character.carrier_index,
        "role": character.role,
        "kind_id": character.kind_id,
    }


def _receipt_payload(
    *,
    source_id: str,
    source_length: int,
    carrier_digest: str,
    characters: tuple[CharacterGonol, ...],
    words: tuple[WordGonol, ...],
    boundaries: tuple[CharacterGonol, ...],
) -> dict[str, Any]:
    return {
        "constructor_id": CONSTRUCTOR_ID,
        "constructor_version": CONSTRUCTOR_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "source_id": source_id,
        "source_length": source_length,
        "carrier_digest": carrier_digest,
        "frozen_choices": [list(item) for item in FROZEN_CHOICES],
        "characters": [_character_payload(item) for item in characters],
        "words": [
            {
                "occurrence": word.occurrence,
                "source_start": word.source_start,
                "source_end": word.source_end,
                "kind_id": list(word.kind_id),
                "characters": [_character_payload(item) for item in word.characters],
            }
            for word in words
        ],
        "boundaries": [_character_payload(item) for item in boundaries],
        "nonclaims": list(NONCLAIMS),
        "hmmm": list(HMMM),
    }


def canonical_receipt_bytes(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def _digest(payload: Mapping[str, Any]) -> str:
    return sha256(canonical_receipt_bytes(payload)).hexdigest()


def construct_character_word_gonols(source: str, *, source_id: str) -> CharacterWordReceipt:
    """Admit every Unicode scalar and close whitespace-delimited word gonols."""

    if not isinstance(source, str):
        raise CharacterWordError("source must be a Unicode string")
    if not isinstance(source_id, str) or not source_id:
        raise CharacterWordError("source_id must be a non-empty string")

    geometry = _load_public_gonol()
    position_of = geometry.public_gonol_position
    admitted: list[CharacterGonol] = []
    for occurrence, scalar in enumerate(source):
        admitted.append(_character_record(occurrence, scalar, position_of, "admitted"))
    characters = tuple(admitted)
    words, boundaries = _close_words(characters)
    payload = _receipt_payload(
        source_id=source_id,
        source_length=len(source),
        carrier_digest=str(geometry.PUBLIC_GONOL_SHA256),
        characters=characters,
        words=words,
        boundaries=boundaries,
    )
    return CharacterWordReceipt(
        constructor_id=CONSTRUCTOR_ID,
        constructor_version=CONSTRUCTOR_VERSION,
        standing=STANDING,
        selection_effect=SELECTION_EFFECT,
        source_id=source_id,
        source_length=len(source),
        carrier_digest=str(geometry.PUBLIC_GONOL_SHA256),
        frozen_choices=FROZEN_CHOICES,
        characters=characters,
        words=words,
        boundaries=boundaries,
        nonclaims=NONCLAIMS,
        hmmm=HMMM,
        receipt_digest=_digest(payload),
    )


def replay_character_word_gonols(source: str, *, source_id: str) -> CharacterWordReceipt:
    """Independently reconstruct the same declared source."""

    return construct_character_word_gonols(source, source_id=source_id)


__all__ = [
    "CONSTRUCTOR_ID",
    "CONSTRUCTOR_VERSION",
    "PINNED_PUBLIC_GONOL_SHA256",
    "CharacterGonol",
    "CharacterWordError",
    "CharacterWordReceipt",
    "WordGonol",
    "canonical_receipt_bytes",
    "construct_character_word_gonols",
    "replay_character_word_gonols",
]
