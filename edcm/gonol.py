"""Unified EDCM gonol construction candidate.

Usage guidance
--------------
This is an implemented candidate, not selected canon. It enforces the current
EDCM construction order:

``character -> word -> definition -> recursive``

    from edcm.gonol import construct_gonol, replay_gonol

    cut = construct_gonol(scale="word", source="cut", source_id="example:cut")
    divide = construct_gonol(
        scale="word",
        source="divide",
        source_id="example:divide",
    )
    definition = construct_gonol(
        scale="definition",
        source="to divide with a sharp edge",
        participants=(cut.gonol, divide.gonol),
        source_id="example:cut#1",
    )
    recursive = construct_gonol(
        scale="recursive",
        relation="example:relates",
        participants=(definition.gonol, cut.gonol),
        source_id="example:relation#1",
    )
    assert recursive.receipt_digest == replay_gonol(receipt=recursive).receipt_digest

Frozen choices for ``edcm.gonol/v2``:

- the only active stages are character, word, definition, and recursive;
- word construction closes exact ordered Unicode-scalar character gonols;
- definition construction requires exact source evidence and closed word gonols;
- recursive construction accepts only closed word, definition, or recursive gonols;
- each completed gonol closes before atomic participation at the next declared
  scale;
- closed gonols participate without reopening while their internal structure
  remains recoverable;
- source strings are exact Unicode scalar sequences: no normalization, case
  folding, trimming, deduplication, or token substitution;
- relation identity is exact caller-supplied text where the option set requires
  it;
- pronunciation is not part of construction;
- UCNS Public Gonol geometry is consumed only from an explicit supplied
  authority, and absence remains ``hmmm`` rather than a base-package failure;
- no UCNS function operation or Mobius coupling law is invented.
"""

# === MODULE_BUILD ===
# id: edcm_gonol
#   module_name: gonol
#   module_kind: engine
#   summary: unified EDCM candidate constructor that enforces character-to-word-to-definition-to-recursive construction while preserving closed-gonol atomicity, deterministic replay, and UCNS geometry boundaries
#   owner: Erin Spencer
#   public_surface: CONSTRUCTOR_ID, CONSTRUCTOR_VERSION, PINNED_PUBLIC_GONOL_SHA256, ScaleOptionSet, ClosedGonol, GonolReceipt, GonolConstructionError, SCALE_OPTION_SETS, construct_gonol, replay_gonol, canonical_receipt_bytes
#   internal_surface: _option_set, _require_text, _source_units, _closed_participants, _validate_closed_gonol, _validate_stage_inputs, _relation_value, _geometry_observation, _source_character_gonols, _participant_payload, _atomic_payload, _receipt_payload, _digest
#   auth_boundary: EDCM owns text-domain closure; UCNS Public Gonol geometry is optional observation only when supplied as an explicit matching authority
#   storage_boundary: none; receipts remain caller-owned in-memory objects
#   network_boundary: none
#   user_data_boundary: caller-supplied source, relation, participants, and source_id remain in memory and are not transmitted
#   admin_only: false
#   tests: tests.test_gonol_constructor
#   rollout: explicit v2 candidate constructor; no canon selection, measurement activation, UCNS function operation, or Mobius coupling promotion
#   rollback: remove this module; historical lexical-floor and UCNS observation adapters remain unchanged
#   requires: none
#   since: 2026-08-22
#   unresolved: exact UCNS geometric operation of Public Gonol function positions; Mobius-carrier coupling law; which definition sources and recursive relations are later selected; any future construction that explicitly adds phonology or another stage
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: single_constructor_enforces_required_order
#   given: a caller constructs a character, word, definition, or recursive gonol
#   then: edcm.gonol permits only the current four stages and rejects construction that bypasses their declared input boundary
#   class: construction
#   since: 2026-09-10
#
# id: closed_gonol_atomic_at_next_stage
#   given: a closed gonol participates in another construction
#   then: the participant is consumed atomically at a legal next stage while recoverable provenance and nested structure remain available
#   class: construction
#   since: 2026-08-22
#
# id: word_closes_ordered_character_gonols
#   given: exact one-word source evidence is admitted
#   then: every Unicode scalar closes as an ordered character gonol before the word closes
#   class: construction
#   since: 2026-09-10
#
# id: definition_requires_words_and_exact_evidence
#   given: a definition gonol is requested
#   then: exact definition source and one or more already-closed word gonols are required
#   class: construction
#   since: 2026-09-10
#
# id: recursive_rejects_character_bypass
#   given: a recursive gonol is requested
#   then: ordered closed word, definition, or recursive gonols are accepted and raw character gonols are rejected
#   class: construction
#   since: 2026-09-10
#
# id: construction_survives_absent_ucns_geometry
#   given: UCNS Public Gonol geometry authority is not explicitly supplied
#   then: construction records geometry as hmmm, does not probe ambient imports, and does not fail base-package CI
#   class: safety
#   since: 2026-08-22
#
# id: geometry_mismatch_fails_closed
#   given: supplied UCNS Public Gonol geometry has a digest different from the pinned identity
#   then: construction raises rather than consuming or copying mismatched geometry
#   class: safety
#   since: 2026-08-22
#
# id: unified_candidate_does_not_select_canon
#   given: a receipt is minted
#   then: standing is implemented-candidate, selection_effect is none, and measurement, UCNS operation, and phonology remain nonclaims
#   class: doctrine
#   since: 2026-08-22
# === END CONTRACTS ===

from __future__ import annotations

from collections.abc import Mapping as RuntimeMapping
from dataclasses import dataclass, replace
from hashlib import sha256
import json
from types import MappingProxyType
from typing import Any, Mapping, Sequence


CONSTRUCTOR_ID = "edcm.gonol"
CONSTRUCTOR_VERSION = "v2"
PINNED_PUBLIC_GONOL_SHA256 = (
    "55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5"
)
STANDING = "implemented-candidate"
SELECTION_EFFECT = "none"

NONCLAIMS: tuple[str, ...] = (
    "not selected canon",
    "not EDCM measurement validity",
    "not complete English morphology law",
    "not a pronunciation or phonology model",
    "not a UCNS geometric function operation",
    "not a UCNS Mobius coupling law",
)

HMMM: tuple[str, ...] = (
    "exact UCNS geometric operation of each Public Gonol function position",
    "UCNS Mobius-carrier coupling law",
    "which definition sources and recursive relations, if any, are later selected",
    "any future construction that explicitly adds phonology or another stage",
)


class GonolConstructionError(RuntimeError):
    """Fail-closed constructor error."""


@dataclass(frozen=True, slots=True)
class ScaleOptionSet:
    """Frozen options for one required EDCM construction stage."""

    scale: str
    option_set_id: str
    source_policy: str
    participant_policy: str
    relation_policy: str
    default_relation: str | None
    closure_policy: str
    arity_policy: str
    geometry_policy: str


_SCALE_OPTION_SETS: dict[str, ScaleOptionSet] = {
    "character": ScaleOptionSet(
        scale="character",
        option_set_id="edcm.gonol.scale.character/v2",
        source_policy="exactly-one-unicode-scalar",
        participant_policy="none",
        relation_policy="declared-default",
        default_relation="admitted-character",
        closure_policy="close-one-source-unit",
        arity_policy="no-closed-participants",
        geometry_policy="observe-explicit-public-gonol-position-if-supplied",
    ),
    "word": ScaleOptionSet(
        scale="word",
        option_set_id="edcm.gonol.scale.word/v2",
        source_policy="exact-one-word-source-string",
        participant_policy="auto-close-ordered-source-characters",
        relation_policy="declared-default",
        default_relation="word-closure",
        closure_policy="close-word-from-ordered-character-gonols",
        arity_policy="source-required-no-explicit-participants",
        geometry_policy="observe-explicit-public-gonol-positions-if-supplied",
    ),
    "definition": ScaleOptionSet(
        scale="definition",
        option_set_id="edcm.gonol.scale.definition/v2",
        source_policy="exact-definition-source-required",
        participant_policy="closed-word-gonols-without-reopening",
        relation_policy="declared-default",
        default_relation="definition-of",
        closure_policy="close-definition-from-word-gonols-and-source-evidence",
        arity_policy="minimum-one-closed-word-and-source",
        geometry_policy="observe-explicit-public-gonol-positions-if-supplied",
    ),
    "recursive": ScaleOptionSet(
        scale="recursive",
        option_set_id="edcm.gonol.scale.recursive/v2",
        source_policy="optional-exact-source-evidence",
        participant_policy="closed-word-definition-or-recursive-gonols-without-reopening",
        relation_policy="caller-supplied-required",
        default_relation=None,
        closure_policy="close-relation-over-atomic-participants",
        arity_policy="minimum-two-closed-participants",
        geometry_policy="observe-explicit-public-gonol-positions-if-supplied",
    ),
}
SCALE_OPTION_SETS: Mapping[str, ScaleOptionSet] = MappingProxyType(_SCALE_OPTION_SETS)


@dataclass(frozen=True, slots=True)
class ClosedGonol:
    """Closed gonol value. Atomic identity participates; internals remain recoverable."""

    occurrence: int
    scale: str
    option_set_id: str
    relation: str
    source_id: str
    source_units: tuple[str, ...]
    source_characters: tuple["ClosedGonol", ...]
    participants: tuple["ClosedGonol", ...]
    atomic_id: str
    receipt_digest: str
    geometry_digest: str
    provenance: tuple[tuple[str, str], ...]

    @property
    def kind_id(self) -> tuple[str, str]:
        return (self.scale, self.atomic_id)


@dataclass(frozen=True, slots=True)
class GonolReceipt:
    """Deterministic construction receipt. Digest is replay identity."""

    constructor_id: str
    constructor_version: str
    standing: str
    selection_effect: str
    source_id: str
    option_set: ScaleOptionSet
    gonol: ClosedGonol
    geometry: Mapping[str, Any]
    nonclaims: tuple[str, ...]
    hmmm: tuple[str, ...]
    receipt_digest: str


def _option_set(scale: str) -> ScaleOptionSet:
    if not isinstance(scale, str) or not scale:
        raise GonolConstructionError("scale must be a non-empty string")
    try:
        return SCALE_OPTION_SETS[scale]
    except KeyError as exc:
        allowed = ", ".join(sorted(SCALE_OPTION_SETS))
        raise GonolConstructionError(f"scale must be one of: {allowed}") from exc


def _require_text(value: str, *, field: str, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise GonolConstructionError(f"{field} must be an exact Unicode string")
    if not allow_empty and not value:
        raise GonolConstructionError(f"{field} must be a non-empty string")
    for character in value:
        codepoint = ord(character)
        if 0xD800 <= codepoint <= 0xDFFF:
            raise GonolConstructionError(f"{field} contains a surrogate code point")
    return value


def _source_units(source: str | None, *, options: ScaleOptionSet) -> tuple[str, ...]:
    if source is None:
        return ()
    text = _require_text(source, field="source", allow_empty=False)
    units = tuple(text)
    if options.scale == "character" and len(units) != 1:
        raise GonolConstructionError("character scale closes exactly one Unicode scalar")
    if options.scale == "word" and any(unit.isspace() for unit in units):
        raise GonolConstructionError(
            "word scale source must be one closed source unit, not whitespace-delimited text"
        )
    return units


def _closed_participants(participants: Sequence[ClosedGonol] | None) -> tuple[ClosedGonol, ...]:
    if participants is None:
        return ()
    if not isinstance(participants, Sequence) or isinstance(participants, (str, bytes)):
        raise GonolConstructionError("participants must be an ordered sequence of closed gonols")
    closed = tuple(participants)
    for item in closed:
        if not isinstance(item, ClosedGonol):
            raise GonolConstructionError("participants must already be closed gonols")
        _validate_closed_gonol(item)
    return closed


def _relation_value(relation: str | None, *, options: ScaleOptionSet) -> str:
    if options.relation_policy == "declared-default":
        if options.default_relation is None:
            raise GonolConstructionError("declared-default relation policy requires a default relation")
        if relation is None:
            return options.default_relation
        relation_text = _require_text(relation, field="relation")
        if relation_text != options.default_relation:
            raise GonolConstructionError(
                f"{options.scale} scale relation must be declared default {options.default_relation!r}"
            )
        return relation_text
    if options.relation_policy == "caller-supplied-required":
        if options.default_relation is None:
            if relation is None:
                raise GonolConstructionError("relation must be exact caller-supplied text for this scale")
        elif relation is None:
            return options.default_relation
        relation_text = _require_text(relation, field="relation")
        if relation_text.isspace():
            raise GonolConstructionError("relation must be exact non-empty caller-supplied text")
        return relation_text
    raise GonolConstructionError(f"unknown relation policy: {options.relation_policy}")


def _validate_stage_inputs(
    *,
    options: ScaleOptionSet,
    units: tuple[str, ...],
    closed: tuple[ClosedGonol, ...],
) -> None:
    if options.scale == "character":
        if len(units) != 1:
            raise GonolConstructionError("character scale closes exactly one Unicode scalar")
        if closed:
            raise GonolConstructionError("character scale does not accept closed participants")
        return

    if options.scale == "word":
        if not units:
            raise GonolConstructionError("word scale requires exact source evidence")
        if closed:
            raise GonolConstructionError(
                "word scale closes ordered source characters and does not accept explicit participants"
            )
        return

    if options.scale == "definition":
        if not units:
            raise GonolConstructionError("definition scale requires exact source evidence")
        if not closed:
            raise GonolConstructionError(
                "definition scale requires at least one already-closed word gonol"
            )
        if any(item.scale != "word" for item in closed):
            raise GonolConstructionError(
                "definition scale accepts only already-closed word gonols"
            )
        return

    if options.scale == "recursive":
        if len(closed) < 2:
            raise GonolConstructionError(
                "recursive scale requires at least two closed participants: "
                "word, definition, or recursive gonols"
            )
        if any(item.scale not in {"word", "definition", "recursive"} for item in closed):
            raise GonolConstructionError(
                "recursive scale accepts only closed word, definition, or recursive gonols; "
                "close characters into words first"
            )
        return

    raise GonolConstructionError(f"unsupported construction stage: {options.scale}")


def _json_payload(value: Any) -> Any:
    if isinstance(value, RuntimeMapping):
        return {str(key): _json_payload(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_json_payload(item) for item in value]
    if isinstance(value, list):
        return [_json_payload(item) for item in value]
    return value


def _freeze_json(value: Any) -> Any:
    if isinstance(value, RuntimeMapping):
        return MappingProxyType({str(key): _freeze_json(item) for key, item in value.items()})
    if isinstance(value, tuple):
        return tuple(_freeze_json(item) for item in value)
    if isinstance(value, list):
        return tuple(_freeze_json(item) for item in value)
    return value


def _authority_value(authority: Any, name: str) -> Any:
    if isinstance(authority, RuntimeMapping):
        return authority.get(name)
    return getattr(authority, name, None)


def _authority_name(authority: Any) -> str:
    if isinstance(authority, RuntimeMapping):
        name = authority.get("authority_name") or authority.get("__name__")
        return str(name or "mapping")
    return str(getattr(authority, "__name__", authority.__class__.__name__))


def _public_gonol_sha256(carrier: tuple[str, ...]) -> str:
    payload = json.dumps(tuple(carrier), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return sha256(payload).hexdigest()


def _geometry_observation(
    source_units: tuple[str, ...],
    *,
    geometry_authority: Any | None,
) -> Mapping[str, Any]:
    if geometry_authority is None:
        return _freeze_json(
            {
                "state": "hmmm",
                "authority": "ucns.public_gonol",
                "authority_binding": "not-supplied",
                "reason": "UCNS Public Gonol authority not supplied",
                "positions": (),
            }
        )

    carrier_value = _authority_value(geometry_authority, "PUBLIC_GONOL_157")
    if not isinstance(carrier_value, Sequence) or isinstance(carrier_value, (str, bytes)):
        raise GonolConstructionError("UCNS Public Gonol authority is missing PUBLIC_GONOL_157")
    carrier = tuple(carrier_value)
    if len(carrier) != 157:
        raise GonolConstructionError("UCNS Public Gonol carrier must contain exactly 157 positions")
    for index, glyph in enumerate(carrier):
        if not isinstance(glyph, str) or not glyph:
            raise GonolConstructionError("UCNS Public Gonol carrier entries must be non-empty strings")
        _require_text(glyph, field=f"UCNS Public Gonol carrier entry {index}")
    if len(set(carrier)) != len(carrier):
        raise GonolConstructionError("UCNS Public Gonol carrier entries must be unique")

    computed_digest = _public_gonol_sha256(carrier)
    declared_digest = str(_authority_value(geometry_authority, "PUBLIC_GONOL_SHA256") or "")
    if not declared_digest:
        digest_function = _authority_value(geometry_authority, "public_gonol_sha256")
        if callable(digest_function):
            declared_digest = str(digest_function())
    if declared_digest != computed_digest or computed_digest != PINNED_PUBLIC_GONOL_SHA256:
        raise GonolConstructionError(
            "UCNS Public Gonol digest mismatch: "
            f"constructor pins {PINNED_PUBLIC_GONOL_SHA256}, "
            f"declared {declared_digest or 'missing'}, computed {computed_digest}"
        )

    index_by_glyph = {glyph: index for index, glyph in enumerate(carrier)}
    supplied_position = _authority_value(geometry_authority, "public_gonol_position")
    if callable(supplied_position):
        for glyph, index in index_by_glyph.items():
            if supplied_position(glyph) != index:
                raise GonolConstructionError("UCNS public_gonol_position disagrees with PUBLIC_GONOL_157")
        positions = tuple(supplied_position(unit) for unit in source_units)
    else:
        positions = tuple(index_by_glyph.get(unit) for unit in source_units)

    return _freeze_json(
        {
            "state": "observed",
            "authority": "ucns.public_gonol",
            "authority_binding": "explicit",
            "authority_name": _authority_name(geometry_authority),
            "carrier_digest": computed_digest,
            "positions": positions,
        }
    )


def _kind_payload(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_kind_payload(item) for item in value]
    if isinstance(value, list):
        return [_kind_payload(item) for item in value]
    return value


def _option_payload(options: ScaleOptionSet) -> dict[str, str | None]:
    return {
        "scale": options.scale,
        "option_set_id": options.option_set_id,
        "source_policy": options.source_policy,
        "participant_policy": options.participant_policy,
        "relation_policy": options.relation_policy,
        "default_relation": options.default_relation,
        "closure_policy": options.closure_policy,
        "arity_policy": options.arity_policy,
        "geometry_policy": options.geometry_policy,
    }


def _participant_payload(item: ClosedGonol) -> dict[str, Any]:
    return {
        "scale": item.scale,
        "occurrence": item.occurrence,
        "relation": item.relation,
        "source_id": item.source_id,
        "source_units": list(item.source_units),
        "source_characters": [_participant_payload(character) for character in item.source_characters],
        "kind_id": _kind_payload(item.kind_id),
        "atomic_id": item.atomic_id,
        "receipt_digest": item.receipt_digest,
        "geometry_digest": item.geometry_digest,
        "option_set_id": item.option_set_id,
        "provenance": [list(pair) for pair in item.provenance],
    }


def _atomic_payload(
    *,
    occurrence: int,
    source_id: str,
    options: ScaleOptionSet,
    relation: str,
    source_units: tuple[str, ...],
    source_characters: tuple[ClosedGonol, ...],
    participants: tuple[ClosedGonol, ...],
) -> dict[str, Any]:
    return {
        "constructor_id": CONSTRUCTOR_ID,
        "constructor_version": CONSTRUCTOR_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "occurrence": occurrence,
        "source_id": source_id,
        "option_set": _option_payload(options),
        "relation": relation,
        "source_units": list(source_units),
        "source_characters": [_participant_payload(character) for character in source_characters],
        "participants": [_participant_payload(item) for item in participants],
        "construction_order": ["character", "word", "definition", "recursive"],
        "closure_invariant": (
            "each gonol closes before atomic participation at a legal next stage without reopening"
        ),
    }


def _receipt_payload(
    *,
    source_id: str,
    options: ScaleOptionSet,
    gonol: ClosedGonol,
    geometry: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "constructor_id": CONSTRUCTOR_ID,
        "constructor_version": CONSTRUCTOR_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "source_id": source_id,
        "option_set": _option_payload(options),
        "gonol": _atomic_payload(
            occurrence=gonol.occurrence,
            source_id=gonol.source_id,
            options=options,
            relation=gonol.relation,
            source_units=gonol.source_units,
            source_characters=gonol.source_characters,
            participants=gonol.participants,
        ),
        "atomic_id": gonol.atomic_id,
        "geometry": _json_payload(geometry),
        "geometry_digest": gonol.geometry_digest,
        "nonclaims": list(NONCLAIMS),
        "hmmm": list(HMMM),
    }


def canonical_receipt_bytes(payload: Mapping[str, Any]) -> bytes:
    """Return stable JSON bytes for construction receipts."""

    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def _digest(payload: Mapping[str, Any]) -> str:
    return sha256(canonical_receipt_bytes(payload)).hexdigest()


def _geometry_digest(geometry: Mapping[str, Any]) -> str:
    return _digest({"geometry": _json_payload(geometry)})


def _is_sha256_digest(value: str) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _validate_source_character_links(item: ClosedGonol) -> None:
    if item.scale == "character":
        if item.source_characters:
            raise GonolConstructionError("character gonols cannot carry nested source characters")
        return
    if len(item.source_characters) != len(item.source_units):
        raise GonolConstructionError("source character gonol count does not match source units")
    for index, (unit, character) in enumerate(zip(item.source_units, item.source_characters, strict=True)):
        if character.scale != "character":
            raise GonolConstructionError("source characters must be closed character gonols")
        if character.source_units != (unit,):
            raise GonolConstructionError("source character gonol does not match source unit")
        if character.occurrence != index:
            raise GonolConstructionError("source character occurrence does not preserve source order")
        if character.participants or character.source_characters:
            raise GonolConstructionError("source character gonols must remain atomic leaves")


def _validate_closed_gonol(item: ClosedGonol, *, _seen: set[int] | None = None) -> None:
    if not isinstance(item, ClosedGonol):
        raise GonolConstructionError("participants must already be closed gonols")
    if _seen is None:
        _seen = set()
    identity = id(item)
    if identity in _seen:
        raise GonolConstructionError("closed gonol graph must be acyclic")
    _seen.add(identity)
    options = _option_set(item.scale)
    if item.option_set_id != options.option_set_id:
        raise GonolConstructionError("closed gonol option set identity mismatch")
    _require_text(item.source_id, field="closed gonol source_id")
    _require_text(item.relation, field="closed gonol relation")
    for unit in item.source_units:
        _require_text(unit, field="closed gonol source unit")
    for key, value in item.provenance:
        _require_text(key, field="closed gonol provenance key")
        _require_text(value, field="closed gonol provenance value")
    if not _is_sha256_digest(item.atomic_id):
        raise GonolConstructionError("closed gonol atomic identity must be a sha256 digest")
    if not _is_sha256_digest(item.receipt_digest):
        raise GonolConstructionError("closed gonol receipt identity must be a sha256 digest")
    if not _is_sha256_digest(item.geometry_digest):
        raise GonolConstructionError("closed gonol geometry identity must be a sha256 digest")
    for character in item.source_characters:
        _validate_closed_gonol(character, _seen=_seen)
    for participant in item.participants:
        _validate_closed_gonol(participant, _seen=_seen)
    _validate_source_character_links(item)
    _validate_stage_inputs(options=options, units=item.source_units, closed=item.participants)
    _relation_value(item.relation, options=options)
    expected_atomic_id = _digest(
        _atomic_payload(
            occurrence=item.occurrence,
            source_id=item.source_id,
            options=options,
            relation=item.relation,
            source_units=item.source_units,
            source_characters=item.source_characters,
            participants=item.participants,
        )
    )
    if item.atomic_id != expected_atomic_id:
        raise GonolConstructionError("closed gonol atomic identity does not match its fields")
    _seen.remove(identity)


def _close_validated_gonol(
    *,
    options: ScaleOptionSet,
    source_id: str,
    units: tuple[str, ...],
    source_characters: tuple[ClosedGonol, ...],
    closed: tuple[ClosedGonol, ...],
    relation_value: str,
    occurrence: int,
    geometry_authority: Any | None,
) -> GonolReceipt:
    geometry = _geometry_observation(units, geometry_authority=geometry_authority)
    geometry_digest = _geometry_digest(geometry)
    atomic_payload = _atomic_payload(
        occurrence=occurrence,
        source_id=source_id,
        options=options,
        relation=relation_value,
        source_units=units,
        source_characters=source_characters,
        participants=closed,
    )
    atomic_id = _digest(atomic_payload)
    provenance = (
        ("constructor", f"{CONSTRUCTOR_ID}/{CONSTRUCTOR_VERSION}"),
        ("source_id", source_id),
        ("option_set", options.option_set_id),
        ("geometry_digest", geometry_digest),
    )
    gonol = ClosedGonol(
        occurrence=occurrence,
        scale=options.scale,
        option_set_id=options.option_set_id,
        relation=relation_value,
        source_id=source_id,
        source_units=units,
        source_characters=source_characters,
        participants=closed,
        atomic_id=atomic_id,
        receipt_digest="0" * 64,
        geometry_digest=geometry_digest,
        provenance=provenance,
    )
    payload = _receipt_payload(
        source_id=source_id,
        options=options,
        gonol=gonol,
        geometry=geometry,
    )
    receipt_digest = _digest(payload)
    gonol = replace(gonol, receipt_digest=receipt_digest)
    return GonolReceipt(
        constructor_id=CONSTRUCTOR_ID,
        constructor_version=CONSTRUCTOR_VERSION,
        standing=STANDING,
        selection_effect=SELECTION_EFFECT,
        source_id=source_id,
        option_set=options,
        gonol=gonol,
        geometry=geometry,
        nonclaims=NONCLAIMS,
        hmmm=HMMM,
        receipt_digest=receipt_digest,
    )


def _source_character_gonols(
    *,
    source_id: str,
    units: tuple[str, ...],
    geometry_authority: Any | None,
) -> tuple[ClosedGonol, ...]:
    if not units:
        return ()
    options = _option_set("character")
    relation_value = _relation_value(None, options=options)
    characters: list[ClosedGonol] = []
    for index, unit in enumerate(units):
        receipt = _close_validated_gonol(
            options=options,
            source_id=f"{source_id}#source-character:{index}",
            units=(unit,),
            source_characters=(),
            closed=(),
            relation_value=relation_value,
            occurrence=index,
            geometry_authority=geometry_authority,
        )
        characters.append(receipt.gonol)
    return tuple(characters)


def _verify_receipt(receipt: GonolReceipt) -> GonolReceipt:
    if not isinstance(receipt, GonolReceipt):
        raise GonolConstructionError("receipt must be a GonolReceipt")
    if receipt.constructor_id != CONSTRUCTOR_ID or receipt.constructor_version != CONSTRUCTOR_VERSION:
        raise GonolConstructionError("receipt constructor identity mismatch")
    if receipt.standing != STANDING or receipt.selection_effect != SELECTION_EFFECT:
        raise GonolConstructionError("receipt candidate status mismatch")
    if receipt.nonclaims != NONCLAIMS or receipt.hmmm != HMMM:
        raise GonolConstructionError("receipt nonclaim or hmmm boundary mismatch")
    options = _option_set(receipt.gonol.scale)
    if receipt.option_set != options:
        raise GonolConstructionError("receipt option set is not the frozen constructor option set")
    if receipt.source_id != receipt.gonol.source_id:
        raise GonolConstructionError("receipt source identity does not match its gonol")
    geometry = _freeze_json(receipt.geometry)
    geometry_digest = _geometry_digest(geometry)
    if receipt.gonol.geometry_digest != geometry_digest:
        raise GonolConstructionError("receipt geometry digest does not match visible geometry")
    _validate_closed_gonol(receipt.gonol)
    payload = _receipt_payload(
        source_id=receipt.source_id,
        options=options,
        gonol=receipt.gonol,
        geometry=geometry,
    )
    expected_digest = _digest(payload)
    if receipt.receipt_digest != expected_digest or receipt.gonol.receipt_digest != expected_digest:
        raise GonolConstructionError("receipt digest does not match visible receipt fields")
    return GonolReceipt(
        constructor_id=receipt.constructor_id,
        constructor_version=receipt.constructor_version,
        standing=receipt.standing,
        selection_effect=receipt.selection_effect,
        source_id=receipt.source_id,
        option_set=options,
        gonol=receipt.gonol,
        geometry=geometry,
        nonclaims=receipt.nonclaims,
        hmmm=receipt.hmmm,
        receipt_digest=receipt.receipt_digest,
    )


def construct_gonol(
    *,
    scale: str,
    source_id: str,
    source: str | None = None,
    participants: Sequence[ClosedGonol] | None = None,
    relation: str | None = None,
    geometry_authority: Any | None = None,
    occurrence: int = 0,
) -> GonolReceipt:
    """Close one gonol at the requested stage of the required construction order."""

    options = _option_set(scale)
    source_id = _require_text(source_id, field="source_id")
    if isinstance(occurrence, bool) or not isinstance(occurrence, int) or occurrence < 0:
        raise GonolConstructionError("occurrence must be a non-negative integer")
    units = _source_units(source, options=options)
    closed = _closed_participants(participants)
    _validate_stage_inputs(options=options, units=units, closed=closed)
    relation_value = _relation_value(relation, options=options)
    source_characters = (
        ()
        if options.scale == "character"
        else _source_character_gonols(
            source_id=source_id,
            units=units,
            geometry_authority=geometry_authority,
        )
    )
    return _close_validated_gonol(
        options=options,
        source_id=source_id,
        units=units,
        source_characters=source_characters,
        closed=closed,
        relation_value=relation_value,
        occurrence=occurrence,
        geometry_authority=geometry_authority,
    )


def replay_gonol(*, receipt: GonolReceipt) -> GonolReceipt:
    """Verify a completed receipt from its frozen visible fields."""

    return _verify_receipt(receipt)


__all__ = [
    "CONSTRUCTOR_ID",
    "CONSTRUCTOR_VERSION",
    "PINNED_PUBLIC_GONOL_SHA256",
    "SCALE_OPTION_SETS",
    "ScaleOptionSet",
    "ClosedGonol",
    "GonolConstructionError",
    "GonolReceipt",
    "canonical_receipt_bytes",
    "construct_gonol",
    "replay_gonol",
]
