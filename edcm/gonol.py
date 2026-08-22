"""Unified EDCM gonol candidate constructor.

Usage guidance
--------------
This is an implemented candidate, not selected canon. It closes one gonol at a
declared scale using the scale's option set. It does not encode a mandatory
``character -> word -> definition -> recursive`` ladder.

    from edcm.gonol import construct_gonol, replay_gonol

    word = construct_gonol(scale="word", source="try", source_id="example:try")
    ing = construct_gonol(
        scale="suffix",
        source="ing",
        source_id="example:ing",
        carried_options=(("suffix-coupling.final-y-after-consonant", "preserve-y"),),
    )
    rel = construct_gonol(
        scale="suffix-coupling",
        participants=(word.gonol, ing.gonol),
        source_id="example:trying#1",
    )
    assert rel.receipt_digest == replay_gonol(receipt=rel).receipt_digest

Frozen choices for ``edcm.gonol/v1``:

- construction is one constructor selected by a scale option set;
- once closed, a gonol is atomic at any scale;
- closed gonols may participate directly at any admissible scale without
  reopening;
- source strings are exact Unicode scalar sequences: no normalization, case
  folding, trimming, deduplication, or token substitution;
- relation identity is exact caller-supplied text where the option set requires
  it;
- suffix-coupling exceptions are carried by the closed suffix gonol, not by a
  global morphology law or by reopening the suffix during coupling;
- UCNS Public Gonol geometry is consumed only from an explicit supplied
  authority, and absence remains ``hmmm`` rather than a base-package failure;
- no UCNS function operation or Mobius coupling law is invented.
"""

# === MODULE_BUILD ===
# id: edcm_gonol
#   module_name: gonol
#   module_kind: engine
#   summary: unified EDCM candidate constructor that closes gonols through declared scale option sets while preserving closed-gonol atomicity, carried suffix options, deterministic replay, and UCNS/METAPAT authority boundaries
#   owner: Erin Spencer
#   public_surface: CONSTRUCTOR_ID, CONSTRUCTOR_VERSION, PINNED_PUBLIC_GONOL_SHA256, ScaleOptionSet, ClosedGonol, GonolReceipt, GonolConstructionError, SCALE_OPTION_SETS, construct_gonol, replay_gonol, canonical_receipt_bytes
#   internal_surface: _option_set, _require_text, _source_units, _closed_participants, _validate_closed_gonol, _carried_option_pairs, _has_suffix_coupling_options, _relation_value, _geometry_observation, _source_character_gonols, _participant_payload, _atomic_payload, _receipt_payload, _digest
#   auth_boundary: EDCM owns text-domain closure; UCNS Public Gonol geometry is optional observation only when supplied as an explicit matching authority; METAPAT affixiation semantics are consumed, not redefined
#   storage_boundary: none; receipts remain caller-owned in-memory objects
#   network_boundary: none
#   user_data_boundary: caller-supplied source, relation, participants, and source_id remain in memory and are not transmitted
#   admin_only: false
#   tests: tests.test_gonol_constructor
#   rollout: explicit candidate constructor; no canon selection, measurement activation, UCNS function operation, or Mobius coupling promotion
#   rollback: remove this module; historical lexical-floor and UCNS observation adapters remain unchanged
#   requires: none
#   since: 2026-08-22
#   unresolved: exact UCNS geometric operation of Public Gonol function positions; Mobius-carrier affixiation/coupling law; which scales and relations are later selected; complete English morphology law
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: single_constructor_uses_scale_option_sets
#   given: a caller closes source evidence or closed gonol participants
#   then: edcm.gonol uses the declared scale option set rather than dispatching through specialized ladder constructors
#   class: construction
#   since: 2026-08-22
#
# id: closed_gonol_atomic_at_any_scale
#   given: a closed gonol participates in another construction
#   then: the participant is consumed by atomic identity while recoverable provenance and nested structure remain available
#   class: construction
#   since: 2026-08-22
#
# id: suffix_exception_carried_by_suffix_gonol
#   given: suffix coupling has a final-y exception such as ing preserving y after a consonant
#   then: the exception is stored on the closed suffix gonol participant and replayed through participant provenance rather than global morphology law
#   class: construction
#   since: 2026-08-22
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
#   then: standing is implemented-candidate, selection_effect is none, and measurement, UCNS operation, and METAPAT promotion remain nonclaims
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
CONSTRUCTOR_VERSION = "v1"
PINNED_PUBLIC_GONOL_SHA256 = (
    "55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5"
)
STANDING = "implemented-candidate"
SELECTION_EFFECT = "none"

NONCLAIMS: tuple[str, ...] = (
    "not selected canon",
    "not EDCM measurement validity",
    "not a mandatory character-word-definition-recursive ladder",
    "not complete English morphology law",
    "not a UCNS geometric function operation",
    "not a UCNS Mobius coupling law",
    "not METAPAT canon promotion",
)

HMMM: tuple[str, ...] = (
    "exact UCNS geometric operation of each Public Gonol function position",
    "UCNS Mobius-carrier affixiation/coupling law",
    "which scales and relations, if any, are later selected",
    "source-supported complete English morphology law",
)


class GonolConstructionError(RuntimeError):
    """Fail-closed constructor error."""


@dataclass(frozen=True, slots=True)
class ScaleOptionSet:
    """Frozen options for one admissible gonol scale."""

    scale: str
    option_set_id: str
    source_policy: str
    participant_policy: str
    relation_policy: str
    default_relation: str | None
    closure_policy: str
    arity_policy: str
    geometry_policy: str
    carried_option_policy: str


_SCALE_OPTION_SETS: dict[str, ScaleOptionSet] = {
    "character": ScaleOptionSet(
        scale="character",
        option_set_id="edcm.gonol.scale.character/v1",
        source_policy="exactly-one-unicode-scalar",
        participant_policy="none",
        relation_policy="declared-default",
        default_relation="admitted-character",
        closure_policy="close-one-source-unit",
        arity_policy="no-closed-participants",
        geometry_policy="observe-explicit-public-gonol-position-if-supplied",
        carried_option_policy="none",
    ),
    "word": ScaleOptionSet(
        scale="word",
        option_set_id="edcm.gonol.scale.word/v1",
        source_policy="exact-source-string-or-closed-participants",
        participant_policy="any-closed-gonols-without-reopening",
        relation_policy="caller-supplied-or-declared-default",
        default_relation="word-closure",
        closure_policy="close-declared-word-scale-object",
        arity_policy="any-closed-participants-or-source",
        geometry_policy="observe-explicit-public-gonol-positions-if-supplied",
        carried_option_policy="declared-on-closed-gonol",
    ),
    "suffix": ScaleOptionSet(
        scale="suffix",
        option_set_id="edcm.gonol.scale.suffix/v1",
        source_policy="exact-source-string",
        participant_policy="none",
        relation_policy="declared-default",
        default_relation="suffix-form",
        closure_policy="close-declared-suffix-scale-object",
        arity_policy="no-closed-participants",
        geometry_policy="observe-explicit-public-gonol-positions-if-supplied",
        carried_option_policy="declared-on-closed-suffix-gonol",
    ),
    "suffix-coupling": ScaleOptionSet(
        scale="suffix-coupling",
        option_set_id="edcm.gonol.scale.suffix-coupling/v1",
        source_policy="optional-exact-source-evidence",
        participant_policy="closed-base-and-closed-suffix-without-reopening",
        relation_policy="caller-supplied-or-declared-default",
        default_relation="suffix-coupling",
        closure_policy="close-relation-over-atomic-base-and-suffix",
        arity_policy="exactly-two-ordered-base-and-suffix",
        geometry_policy="observe-explicit-public-gonol-positions-if-supplied",
        carried_option_policy="consume-carried-options-from-suffix-participant",
    ),
    "definition": ScaleOptionSet(
        scale="definition",
        option_set_id="edcm.gonol.scale.definition/v1",
        source_policy="exact-source-string-or-closed-participants",
        participant_policy="any-closed-gonols-without-reopening",
        relation_policy="caller-supplied-or-declared-default",
        default_relation="definition-evidence",
        closure_policy="close-declared-definition-scale-object",
        arity_policy="any-closed-participants-or-source",
        geometry_policy="observe-explicit-public-gonol-positions-if-supplied",
        carried_option_policy="declared-on-closed-gonol",
    ),
    "recursive": ScaleOptionSet(
        scale="recursive",
        option_set_id="edcm.gonol.scale.recursive/v1",
        source_policy="optional-exact-source-evidence",
        participant_policy="any-closed-gonols-without-reopening",
        relation_policy="caller-supplied-required",
        default_relation=None,
        closure_policy="close-relation-over-atomic-participants",
        arity_policy="minimum-two-closed-participants",
        geometry_policy="observe-explicit-public-gonol-positions-if-supplied",
        carried_option_policy="declared-on-closed-gonol",
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
    carried_options: tuple[tuple[str, str], ...]
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
    if options.scale in {"word", "suffix"} and any(unit.isspace() for unit in units):
        raise GonolConstructionError(
            f"{options.scale} scale source must be one closed source unit, not whitespace-delimited text"
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


def _carried_option_pairs(
    carried_options: Sequence[Sequence[str]] | None,
) -> tuple[tuple[str, str], ...]:
    if carried_options is None:
        return ()
    if not isinstance(carried_options, Sequence) or isinstance(carried_options, (str, bytes)):
        raise GonolConstructionError("carried_options must be an ordered sequence of exact text pairs")
    pairs: list[tuple[str, str]] = []
    for pair in carried_options:
        if not isinstance(pair, Sequence) or isinstance(pair, (str, bytes)) or len(pair) != 2:
            raise GonolConstructionError("each carried option must be an exact text pair")
        key, value = pair
        key = _require_text(key, field="carried option key")
        value = _require_text(value, field="carried option value")
        if key.isspace():
            raise GonolConstructionError("carried option key must be exact non-empty text")
        if value.isspace():
            raise GonolConstructionError("carried option value must be exact non-empty text")
        pairs.append((key, value))
    return tuple(pairs)


def _has_suffix_coupling_options(carried_options: tuple[tuple[str, str], ...]) -> bool:
    return any(key.startswith("suffix-coupling.") for key, _value in carried_options)


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
    if options.relation_policy == "caller-supplied-or-declared-default":
        if relation is None:
            if options.default_relation is None:
                raise GonolConstructionError("relation must be exact caller-supplied text for this scale")
            return options.default_relation
        relation_text = _require_text(relation, field="relation")
        if relation_text.isspace():
            raise GonolConstructionError("relation must be exact non-empty caller-supplied text")
        return relation_text
    raise GonolConstructionError(f"unknown relation policy: {options.relation_policy}")


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
        "carried_option_policy": options.carried_option_policy,
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
        "carried_options": [list(pair) for pair in item.carried_options],
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
    carried_options: tuple[tuple[str, str], ...],
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
        "carried_options": [list(pair) for pair in carried_options],
        "closure_invariant": "once closed, a gonol is atomic at any scale",
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
            carried_options=gonol.carried_options,
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
    _carried_option_pairs(item.carried_options)
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
    expected_atomic_id = _digest(
        _atomic_payload(
            occurrence=item.occurrence,
            source_id=item.source_id,
            options=options,
            relation=item.relation,
            source_units=item.source_units,
            source_characters=item.source_characters,
            participants=item.participants,
            carried_options=item.carried_options,
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
    carried: tuple[tuple[str, str], ...],
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
        carried_options=carried,
    )
    atomic_id = _digest(atomic_payload)
    provenance = (
        ("constructor", f"{CONSTRUCTOR_ID}/{CONSTRUCTOR_VERSION}"),
        ("source_id", source_id),
        ("option_set", options.option_set_id),
        ("geometry_digest", geometry_digest),
    ) + tuple(("carried_option", f"{key}={value}") for key, value in carried)
    gonol = ClosedGonol(
        occurrence=occurrence,
        scale=options.scale,
        option_set_id=options.option_set_id,
        relation=relation_value,
        source_id=source_id,
        source_units=units,
        source_characters=source_characters,
        participants=closed,
        carried_options=carried,
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
            carried=(),
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
    carried_options: Sequence[Sequence[str]] | None = None,
    geometry_authority: Any | None = None,
    occurrence: int = 0,
) -> GonolReceipt:
    """Close one gonol at a declared scale using its option set."""

    options = _option_set(scale)
    source_id = _require_text(source_id, field="source_id")
    if isinstance(occurrence, bool) or not isinstance(occurrence, int) or occurrence < 0:
        raise GonolConstructionError("occurrence must be a non-negative integer")
    units = _source_units(source, options=options)
    closed = _closed_participants(participants)
    carried = _carried_option_pairs(carried_options)
    if options.scale == "character" and closed:
        raise GonolConstructionError("character scale does not accept closed participants")
    if options.scale == "character" and carried:
        raise GonolConstructionError("character scale does not carry declared options")
    if options.scale != "suffix" and _has_suffix_coupling_options(carried):
        raise GonolConstructionError("suffix-coupling options must be carried by a closed suffix gonol")
    if options.scale == "suffix" and closed:
        raise GonolConstructionError("suffix scale does not accept closed participants")
    if options.scale == "suffix-coupling":
        if len(closed) != 2 or closed[1].scale != "suffix":
            raise GonolConstructionError(
                "suffix-coupling scale requires ordered closed base and closed suffix participants"
            )
        if carried:
            raise GonolConstructionError(
                "suffix-coupling options must be carried by the closed suffix participant"
            )
    if not units and not closed:
        raise GonolConstructionError("construction requires source evidence or closed participants")
    if options.scale == "recursive" and len(closed) < 2:
        raise GonolConstructionError("recursive scale requires at least two closed participants")
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
        carried=carried,
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
