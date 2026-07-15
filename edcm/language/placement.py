"""Independent UCNS placement laws for the two English embedding branches.

The molecular branch derives root and affix components from the public
157-vertex glyph floor plus component-specific evidence. The direct atomic
branch derives whole-word gonols from OEWN senses and relation topology and
never consumes a molecular result. Domain-separated hashes prevent accidental
algorithm identity while retaining deterministic reproducibility.
"""

# === MODULE_BUILD ===
# id: edcm_language_placement
#   module_name: placement
#   module_kind: engine
#   summary: assigns glyph-grounded affix/root gonols, independently assigns whole-word relation gonols, superposes molecular alternatives, and computes fork comparison invariants
#   owner: Erin Spencer
#   public_surface: gonol_sha256, assign_affix_gonol, assign_root_gonol, assign_direct_atomic_gonol, superpose_gonols, compare_gonols
#   internal_surface: _canonical_bytes, _feature_payload, _vertices, _glyph_vertex, _payload_depth, _theta_set
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_full_run
#   rollout: default_enabled
#   rollback: restore the prior placement version and regenerate all gonol artifacts
#   requires: edcm_language_affixes, edcm_language_glyph_floor, edcm_language_source, edcm_language_artifacts, edcmbone_ucns_v04
#   since: 2026-07-13
#   unresolved: empirical interpretation of observed direct/generated distances remains a measurement question rather than a placement assumption
# === END MODULE_BUILD ===

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256, shake_256
import json
from typing import Any, Iterable, Mapping, Sequence
from weakref import WeakKeyDictionary

from edcm.measurement.ucns.ucns_v04 import AnchorPayload, UCNSObject

from .affixes import AffixRecord
from .glyph_floor import PUBLIC_GLYPH_FLOOR_157
from .source import LexemeRecord, SynsetRecord

_NONZERO_VERTEX_COUNT = 156
_GLYPH_INDEX = {glyph: index for index, glyph in enumerate(PUBLIC_GLYPH_FLOOR_157)}
_GONOL_HASH_CACHE: WeakKeyDictionary[UCNSObject, str] = WeakKeyDictionary()


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _update_intrinsic_hash(digest: Any, gonol: UCNSObject) -> None:
    """Feed the exact canonical intrinsic JSON bytes without building a record tree.

    ``intrinsic_gonol_record`` contains only integer arrays, null payloads, and
    nested records. Its sorted-key canonical JSON order is therefore fixed. The
    streaming form keeps the historical digest exactly while avoiding a second
    in-memory tree for large recursively shared molecular objects.
    """

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
    for index, face in enumerate(gonol.faces_pos):
        if index:
            digest.update(b",")
        digest.update(str(face).encode("ascii"))
    digest.update(b'],"n_dec":')
    digest.update(str(gonol.n_dec).encode("ascii"))
    digest.update(b',"n_min":')
    digest.update(str(gonol.n_min).encode("ascii"))
    digest.update(b"}")


def gonol_sha256(gonol: UCNSObject) -> str:
    """Stable identity of intrinsic gonol data only.

    UCNS language gonols are construction-complete objects and are not mutated
    after placement. The weak identity cache therefore removes repeated deep
    traversals without extending object lifetime or changing canonical bytes.
    """

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


def _vertices(domain: str, evidence: Any, count: int) -> tuple[int, ...]:
    raw = shake_256(domain.encode("utf-8") + b"\0" + _canonical_bytes(evidence)).digest(count * 8)
    selected: list[int] = []
    occupied: set[int] = set()
    for offset in range(0, len(raw), 8):
        value = 1 + int.from_bytes(raw[offset : offset + 8], "big") % _NONZERO_VERTEX_COUNT
        while value in occupied:
            value = 1 + value % _NONZERO_VERTEX_COUNT
        occupied.add(value)
        selected.append(value)
    return tuple(selected)


def _glyph_vertex(surface: str) -> int:
    """Chirality-sensitive reduction of the public glyph path to one vertex."""

    accumulator = 0
    for position, glyph in enumerate(surface):
        index = _GLYPH_INDEX.get(glyph)
        if index is None:
            index = 1 + int.from_bytes(sha256(glyph.encode("utf-8")).digest()[:4], "big") % 156
        accumulator = (accumulator * 53 + (position + 1) * index) % _NONZERO_VERTEX_COUNT
    return accumulator + 1


def _feature_payload(domain: str, values: Sequence[int]) -> UCNSObject | None:
    if not values:
        return None
    vertices = _vertices(domain, list(values), min(3, max(1, len(values))))
    anchors = [AnchorPayload(Fraction(0), None)]
    faces = [0]
    for index, vertex in enumerate(vertices):
        anchors.append(AnchorPayload(Fraction(vertex, 157), None))
        faces.append(int(values[index % len(values)]) & 1)
    return UCNSObject(157, 1, tuple(anchors), tuple(faces))


def _component_gonol(surface: str, role: str, evidence: Any, feature_values: Sequence[int]) -> UCNSObject:
    glyph_vertex = _glyph_vertex(surface)
    evidence_vertex = _vertices(f"edcm:{role}:evidence:v1", evidence, 1)[0]
    if evidence_vertex == glyph_vertex:
        evidence_vertex = 1 + evidence_vertex % _NONZERO_VERTEX_COUNT
    payload = _feature_payload(f"edcm:{role}:payload:v1", feature_values)
    role_face = int.from_bytes(sha256(role.encode("utf-8")).digest()[:1], "big") & 1
    evidence_face = int.from_bytes(sha256(_canonical_bytes(evidence)).digest()[:1], "big") & 1
    return UCNSObject(
        n_dec=157,
        n_min=1,
        anchors_pos=(
            AnchorPayload(Fraction(0), None),
            AnchorPayload(Fraction(glyph_vertex, 157), payload),
            AnchorPayload(Fraction(evidence_vertex, 157), None),
        ),
        faces_pos=(0, role_face, evidence_face),
    )


def assign_affix_gonol(affix: AffixRecord) -> UCNSObject:
    evidence = {
        "id": affix.affix_id,
        "canonical": affix.canonical,
        "surface": affix.surface,
        "kind": affix.kind,
        "section": affix.section,
        "primary": affix.primary,
        "families": affix.families,
        "variant_of": affix.variant_of,
    }
    return _component_gonol(
        affix.surface,
        "affix-component",
        evidence,
        (len(affix.bare), len(affix.families), ord(affix.primary[:1] or "S")),
    )


def _lexeme_signature(lexemes: Sequence[LexemeRecord]) -> dict[str, Any]:
    return {
        "parts_of_speech": sorted(record.part_of_speech for record in lexemes),
        "forms": sorted({form for record in lexemes for form in record.forms}),
        "senses": [
            {
                "sense_id": sense.sense_id,
                "synset_id": sense.synset_id,
                "relations": sense.relations,
                "subcategories": sense.subcategories,
                "adjective_position": sense.adjective_position,
            }
            for record in sorted(lexemes, key=lambda item: item.part_of_speech)
            for sense in record.senses
        ],
    }


def assign_root_gonol(surface: str, lexemes: Sequence[LexemeRecord]) -> UCNSObject:
    """Molecular root placement, domain-separated from direct atomic placement."""

    signature = _lexeme_signature(lexemes)
    sense_count = sum(len(record.senses) for record in lexemes)
    form_count = len({form for record in lexemes for form in record.forms})
    relation_count = sum(
        len(targets)
        for record in lexemes
        for sense in record.senses
        for _, targets in sense.relations
    )
    return _component_gonol(
        surface,
        "root-component",
        signature,
        (sense_count, form_count, relation_count),
    )


def _whole_word_signature(
    surface: str,
    lexemes: Sequence[LexemeRecord],
    synset_map: Mapping[str, SynsetRecord],
) -> dict[str, Any]:
    senses: list[dict[str, Any]] = []
    for record in sorted(lexemes, key=lambda item: item.part_of_speech):
        for sense in record.senses:
            synset = synset_map.get(sense.synset_id)
            senses.append(
                {
                    "sense_id": sense.sense_id,
                    "entry_pos": record.part_of_speech,
                    "sense_relations": sense.relations,
                    "synset": None
                    if synset is None
                    else {
                        "id": synset.synset_id,
                        "pos": synset.part_of_speech,
                        "members": synset.members,
                        "definitions": synset.definitions,
                        "relations": synset.relations,
                    },
                }
            )
    return {
        "surface": surface,
        "forms": sorted({form for record in lexemes for form in record.forms}),
        "senses": senses,
    }


def assign_direct_atomic_gonol(
    surface: str,
    lexemes: Sequence[LexemeRecord],
    synset_map: Mapping[str, SynsetRecord],
) -> UCNSObject:
    """Assign a whole-word gonol without consulting any molecular object."""

    signature = _whole_word_signature(surface, lexemes, synset_map)
    sense_count = len(signature["senses"])
    synset_relation_count = sum(
        len(targets)
        for item in signature["senses"]
        if item["synset"] is not None
        for _, targets in item["synset"]["relations"]
    )
    sense_relation_count = sum(
        len(targets)
        for item in signature["senses"]
        for _, targets in item["sense_relations"]
    )
    vertices = _vertices("edcm:direct-atomic:v1", signature, 3)
    payload = _feature_payload(
        "edcm:direct-atomic:payload:v1",
        (sense_count, synset_relation_count, sense_relation_count),
    )
    faces_digest = sha256(b"edcm:direct-atomic:faces:v1\0" + _canonical_bytes(signature)).digest()
    return UCNSObject(
        n_dec=157,
        n_min=1,
        anchors_pos=(
            AnchorPayload(Fraction(0), None),
            AnchorPayload(Fraction(vertices[0], 157), payload),
            AnchorPayload(Fraction(vertices[1], 157), None),
            AnchorPayload(Fraction(vertices[2], 157), None),
        ),
        faces_pos=(0, faces_digest[0] & 1, faces_digest[1] & 1, faces_digest[2] & 1),
    )


def superpose_gonols(gonols: Iterable[UCNSObject]) -> UCNSObject:
    """Place all alternative molecular readings behind one atomic-scale twist."""

    values = tuple(gonols)
    if not values:
        raise ValueError("superposition requires at least one gonol")
    if len(values) == 1:
        return values[0]
    identified = sorted(((gonol_sha256(value), value) for value in values), key=lambda item: item[0])
    anchors: list[AnchorPayload] = [AnchorPayload(Fraction(0), None)]
    faces: list[int] = [0]
    occupied: set[int] = set()
    for digest, value in identified:
        vertex = 1 + int(digest[:16], 16) % _NONZERO_VERTEX_COUNT
        while vertex in occupied:
            vertex = 1 + vertex % _NONZERO_VERTEX_COUNT
        occupied.add(vertex)
        anchors.append(AnchorPayload(Fraction(vertex, 157), value))
        faces.append(int(digest[-1], 16) & 1)
    return UCNSObject(157, 1, tuple(anchors), tuple(faces))


def _payload_depth(gonol: UCNSObject) -> int:
    depths = [
        0 if anchor.payload is None else 1 + _payload_depth(anchor.payload)
        for anchor in gonol.anchors_pos
    ]
    return max(depths, default=0)


def _theta_set(gonol: UCNSObject) -> set[tuple[int, int]]:
    return {(anchor.theta.numerator, anchor.theta.denominator) for anchor in gonol.anchors_pos}


def compare_gonols(direct: UCNSObject, generated: UCNSObject) -> dict[str, Any]:
    """Return exact identity plus non-binary topology invariants."""

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
    "assign_affix_gonol",
    "assign_direct_atomic_gonol",
    "assign_root_gonol",
    "compare_gonols",
    "gonol_sha256",
    "superpose_gonols",
]
