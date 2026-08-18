# === MODULE_BUILD ===
# id: edcm_language_deep_recursion
#   module_name: deep_recursion
#   module_kind: engine
#   summary: constructs the complete first closed OEWN definition and semantic-relation layer over an already frozen lexical floor
#   owner: Erin Spencer
#   public_surface: DEEP_RECURSION_LAYER, DefinitionAtom, DeepRecursionLayer, definition_atoms, load_floor_surface_binding, build_deep_recursion_layer
#   internal_surface: _is_atom_character
#   auth_boundary: OEWN owns lexical evidence; UCNS owns only the metadata-free relational carrier
#   storage_boundary: none; callers freeze returned evidence separately
#   network_boundary: none
#   user_data_boundary: no user data
#   admin_only: false
#   tests: tests.test_language_deep_recursion
#   rollout: explicit corpus builder after lexical-floor freeze validation
#   rollback: remove this candidate layer without changing the sealed lexical floor
#   requires: edcm_language_oewn_source, edcm_language_relational_bridge
#   since: 2026-08-18
#   unresolved: dictionary coverage beyond OEWN, lexical ambiguity resolution, UCNS geometry, EDCM measurement validity, phrase and discourse semantics
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: deep_recursion_is_closed_over_frozen_floor
#   given: a definition or semantic relation is admitted to the first deep-recursion layer
#   then: every lexical endpoint is an exact normalized surface in the supplied frozen floor and every definition endpoint is constructed solely from such floor surfaces
#   class: correctness
#   since: 2026-08-18
#
# id: deep_recursion_processes_complete_oewn_inventory
#   given: the first deep-recursion layer is constructed
#   then: every OEWN definition, synset membership pair, synset relation occurrence, and sense relation occurrence is either materialized with full multiplicity or named in the coverage exclusions
#   class: evidence
#   since: 2026-08-18
#
# id: definition_order_and_multiplicity_are_preserved
#   given: a closed definition contains repeated or ordered lexical atoms
#   then: its definition-token edges and external evidence retain every occurrence in source order
#   class: correctness
#   since: 2026-08-18
#
# id: deep_recursion_does_not_claim_semantic_canon
#   given: the complete closed layer is frozen and replayed
#   then: the result remains OEWN-bounded represented evidence without geometry, measurement validity, canonical sense selection, or higher-language activation
#   class: doctrine
#   since: 2026-08-18
# === END CONTRACTS ===

"""Complete, dictionary-bounded first recursion over frozen floor word gonols.

The construction is deliberately exhaustive rather than selective.  It expands
all source semantic occurrences whose endpoints close over the supplied floor.
Definitions are admitted only when every atom produced by the frozen Unicode
atomizer has an existing floor surface; rejected definitions remain inspectable
in the coverage ledger.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import unicodedata
from typing import Mapping

from .relational_bridge import canonical_json_bytes
from .rendering import normalize_lemma
from .source import WordnetSnapshot

DEEP_RECURSION_LAYER = "semantic-definition-depth-1"


class DeepRecursionError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class DefinitionAtom:
    text: str
    normalized: str
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class DeepRecursionLayer:
    node_binding: tuple[dict[str, object], ...]
    relation_binding: tuple[dict[str, object], ...]
    edge_binding: tuple[dict[str, object], ...]
    edges: tuple[tuple[int, int, int], ...]
    coverage: dict[str, object]


def _is_atom_character(character: str) -> bool:
    return unicodedata.category(character)[0] in {"L", "M", "N"}


def definition_atoms(text: str) -> tuple[DefinitionAtom, ...]:
    """Return maximal Unicode lexical atoms with internal apostrophes/hyphens."""

    atoms: list[DefinitionAtom] = []
    start: int | None = None
    for index, character in enumerate(text):
        lexical = _is_atom_character(character)
        internal_joiner = (
            character in {"'", "’", "-", "‐", "‑"}
            and index > 0
            and index + 1 < len(text)
            and _is_atom_character(text[index - 1])
            and _is_atom_character(text[index + 1])
        )
        if lexical or internal_joiner:
            if start is None:
                start = index
        elif start is not None:
            raw = text[start:index]
            atoms.append(DefinitionAtom(raw, normalize_lemma(raw), start, index))
            start = None
    if start is not None:
        raw = text[start:]
        atoms.append(DefinitionAtom(raw, normalize_lemma(raw), start, len(text)))
    return tuple(atom for atom in atoms if atom.normalized)


def load_floor_surface_binding(path: str | Path) -> tuple[dict[str, object], ...]:
    """Load and fully validate the surface identity subset of a frozen floor binding."""

    payload = Path(path).read_bytes()
    value = json.loads(payload)
    if canonical_json_bytes(value) != payload:
        raise DeepRecursionError("lexical floor binding is not canonical")
    if value.get("schema") != "edcm.english-lexical-relational-branch":
        raise DeepRecursionError("lexical floor binding schema mismatch")
    if value.get("branch") != "direct-atomic":
        raise DeepRecursionError("deep recursion requires the direct-atomic floor")
    rows = value.get("node_binding")
    if not isinstance(rows, list):
        raise DeepRecursionError("lexical floor node binding is missing")
    if [row.get("address") for row in rows] != list(range(len(rows))):
        raise DeepRecursionError("lexical floor node addresses are not dense")
    surfaces = tuple(dict(row) for row in rows if row.get("kind") == "surface")
    identities = [row.get("identity") for row in surfaces]
    if not identities or any(not isinstance(item, str) or not item for item in identities):
        raise DeepRecursionError("lexical floor surface identity is invalid")
    if len(set(identities)) != len(identities) or identities != sorted(identities):
        raise DeepRecursionError("lexical floor surfaces are not unique and ordered")
    return surfaces


def build_deep_recursion_layer(
    snapshot: WordnetSnapshot,
    floor_surface_binding: tuple[Mapping[str, object], ...],
) -> DeepRecursionLayer:
    """Process the full OEWN semantic and definition inventory into one closed layer."""

    floor: dict[str, Mapping[str, object]] = {}
    for row in floor_surface_binding:
        identity = row.get("identity")
        if not isinstance(identity, str) or not identity:
            raise DeepRecursionError("floor surface identity is invalid")
        if identity in floor:
            raise DeepRecursionError("floor surface identity is duplicated")
        floor[identity] = row
    if not floor:
        raise DeepRecursionError("floor surface binding is empty")

    nodes: list[dict[str, object]] = []
    address: dict[tuple[str, str], int] = {}
    for surface in sorted(floor):
        address[("surface", surface)] = len(nodes)
        nodes.append({
            "address": len(nodes),
            "kind": "surface",
            "identity": surface,
            "floor_address": floor[surface]["address"],
        })

    synset_surfaces: dict[str, tuple[str, ...]] = {}
    for synset in snapshot.synsets:
        values = tuple(
            surface for surface in (normalize_lemma(member) for member in synset.members)
            if surface in floor
        )
        synset_surfaces[synset.synset_id] = values

    sense_surfaces: dict[str, tuple[str, ...]] = {}
    for lexeme in snapshot.lexemes:
        values = tuple(sorted({
            surface for surface in (
                normalize_lemma(value) for value in (lexeme.lemma, *lexeme.forms)
            ) if surface in floor
        }))
        for sense in lexeme.senses:
            if sense.sense_id in sense_surfaces:
                raise DeepRecursionError("OEWN sense identity is duplicated")
            sense_surfaces[sense.sense_id] = values

    accepted_definitions: list[tuple[object, int, str, tuple[DefinitionAtom, ...]]] = []
    rejected_definitions: list[dict[str, object]] = []
    empty_definitions: list[dict[str, object]] = []
    unknown_occurrences: dict[str, int] = {}
    total_definition_atoms = 0
    for synset in snapshot.synsets:
        for definition_index, definition in enumerate(synset.definitions):
            atoms = definition_atoms(definition)
            total_definition_atoms += len(atoms)
            identity = f"definition:{synset.synset_id}:{definition_index}"
            if not atoms:
                empty_definitions.append({
                    "identity": identity, "synset_id": synset.synset_id,
                    "definition_index": definition_index, "text": definition,
                })
                continue
            unknown = tuple(atom.normalized for atom in atoms if atom.normalized not in floor)
            if unknown:
                for item in unknown:
                    unknown_occurrences[item] = unknown_occurrences.get(item, 0) + 1
                rejected_definitions.append({
                    "identity": identity, "synset_id": synset.synset_id,
                    "definition_index": definition_index, "text": definition,
                    "unknown_atoms": list(unknown),
                })
                continue
            accepted_definitions.append((synset, definition_index, definition, atoms))
            address[("definition", identity)] = len(nodes)
            nodes.append({
                "address": len(nodes), "kind": "definition", "identity": identity,
                "synset_id": synset.synset_id, "definition_index": definition_index,
                "text": definition,
            })

    raw_edges: list[tuple[int, str, int, dict[str, object]]] = []

    def add(source: int, label: str, target: int, evidence: dict[str, object]) -> None:
        raw_edges.append((source, label, target, evidence))

    membership_total = membership_materialized = 0
    excluded_memberships: list[dict[str, object]] = []
    for synset in snapshot.synsets:
        raw_members = tuple(normalize_lemma(member) for member in synset.members)
        for source_index, source in enumerate(raw_members):
            for target_index, target in enumerate(raw_members):
                if source_index == target_index:
                    continue
                membership_total += 1
                if source not in floor or target not in floor:
                    excluded_memberships.append({
                        "synset_id": synset.synset_id,
                        "source_member_index": source_index,
                        "target_member_index": target_index,
                        "source_surface": source,
                        "target_surface": target,
                        "source_in_floor": source in floor,
                        "target_in_floor": target in floor,
                    })
                    continue
                membership_materialized += 1
                add(address[("surface", source)], "synset-co-member", address[("surface", target)], {
                    "kind": "synset-membership", "synset_id": synset.synset_id,
                    "source_member_index": source_index, "target_member_index": target_index,
                    "source_surface": source, "target_surface": target,
                })

    synset_relation_total = synset_relation_materialized = 0
    missing_synset_relations: list[dict[str, object]] = []
    for synset in snapshot.synsets:
        source_values = synset_surfaces[synset.synset_id]
        for relation, targets in synset.relations:
            for target_index, target_id in enumerate(targets):
                synset_relation_total += 1
                target_values = synset_surfaces.get(target_id, ())
                if not source_values or not target_values:
                    missing_synset_relations.append({
                        "source_synset_id": synset.synset_id, "relation": relation,
                        "target_index": target_index, "target_synset_id": target_id,
                        "source_surface_count": len(source_values),
                        "target_surface_count": len(target_values),
                    })
                    continue
                for source in source_values:
                    for target in target_values:
                        synset_relation_materialized += 1
                        add(address[("surface", source)], f"synset:{relation}", address[("surface", target)], {
                            "kind": "synset-relation", "source_synset_id": synset.synset_id,
                            "relation": relation, "target_index": target_index,
                            "target_synset_id": target_id, "source_surface": source,
                            "target_surface": target,
                        })

    sense_relation_total = sense_relation_materialized = 0
    missing_sense_relations: list[dict[str, object]] = []
    for lexeme in snapshot.lexemes:
        for sense in lexeme.senses:
            source_values = sense_surfaces[sense.sense_id]
            for relation, targets in sense.relations:
                for target_index, target_id in enumerate(targets):
                    sense_relation_total += 1
                    target_values = sense_surfaces.get(target_id, ())
                    if not source_values or not target_values:
                        missing_sense_relations.append({
                            "source_sense_id": sense.sense_id, "relation": relation,
                            "target_index": target_index, "target_sense_id": target_id,
                            "source_surface_count": len(source_values),
                            "target_surface_count": len(target_values),
                        })
                        continue
                    for source in source_values:
                        for target in target_values:
                            sense_relation_materialized += 1
                            add(address[("surface", source)], f"sense:{relation}", address[("surface", target)], {
                                "kind": "sense-relation", "source_sense_id": sense.sense_id,
                                "relation": relation, "target_index": target_index,
                                "target_sense_id": target_id, "source_surface": source,
                                "target_surface": target,
                            })

    definition_token_edges = definition_member_edges = 0
    definitions_without_floor_members: list[str] = []
    for synset, definition_index, definition, atoms in accepted_definitions:
        identity = f"definition:{synset.synset_id}:{definition_index}"
        definition_address = address[("definition", identity)]
        members = synset_surfaces[synset.synset_id]
        if not members:
            definitions_without_floor_members.append(identity)
        for member_index, member in enumerate(members):
            definition_member_edges += 2
            common = {
                "kind": "definition-membership", "definition_identity": identity,
                "synset_id": synset.synset_id, "definition_index": definition_index,
                "member_index": member_index, "member_surface": member,
            }
            add(address[("surface", member)], "has-definition", definition_address, {**common, "direction": "word-to-definition"})
            add(definition_address, "defines-word", address[("surface", member)], {**common, "direction": "definition-to-word"})
        for token_index, atom in enumerate(atoms):
            definition_token_edges += 1
            add(definition_address, "definition-token", address[("surface", atom.normalized)], {
                "kind": "definition-token", "definition_identity": identity,
                "synset_id": synset.synset_id, "definition_index": definition_index,
                "definition_text": definition, "token_index": token_index,
                "raw": atom.text, "surface": atom.normalized,
                "start": atom.start, "end": atom.end,
            })

    labels = tuple(sorted({label for _, label, _, _ in raw_edges}))
    relation_codes = {label: index for index, label in enumerate(labels)}
    relation_binding = tuple({"code": relation_codes[label], "label": label} for label in labels)
    edges: list[tuple[int, int, int]] = []
    edge_binding: list[dict[str, object]] = []
    for edge_index, (source, label, target, evidence) in enumerate(raw_edges):
        edges.append((source, relation_codes[label], target))
        edge_binding.append({"edge_index": edge_index, **evidence})

    coverage: dict[str, object] = {
        "schema": "edcm.english-lexical-deep-recursion-coverage",
        "version": "1.0.0",
        "layer": DEEP_RECURSION_LAYER,
        "floor_surface_count": len(floor),
        "definition_count": sum(len(item.definitions) for item in snapshot.synsets),
        "definition_atom_count": total_definition_atoms,
        "closed_definition_count": len(accepted_definitions),
        "rejected_definition_count": len(rejected_definitions),
        "empty_definition_count": len(empty_definitions),
        "definition_token_edge_count": definition_token_edges,
        "definition_member_edge_count": definition_member_edges,
        "definitions_without_floor_members": definitions_without_floor_members,
        "unknown_definition_atom_occurrences": sum(unknown_occurrences.values()),
        "unknown_definition_atom_types": [
            {"surface": surface, "occurrences": unknown_occurrences[surface]}
            for surface in sorted(unknown_occurrences)
        ],
        "rejected_definitions": rejected_definitions,
        "empty_definitions": empty_definitions,
        "synset_membership_pair_count": membership_total,
        "synset_membership_edge_count": membership_materialized,
        "excluded_synset_membership_pair_count": membership_total - membership_materialized,
        "excluded_synset_memberships": excluded_memberships,
        "synset_relation_occurrence_count": synset_relation_total,
        "synset_relation_edge_count": synset_relation_materialized,
        "excluded_synset_relations": missing_synset_relations,
        "sense_relation_occurrence_count": sense_relation_total,
        "sense_relation_edge_count": sense_relation_materialized,
        "excluded_sense_relations": missing_sense_relations,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "status": "UNRESOLVED",
        "nonclaims": [
            "canonical lexical sense", "dictionary completeness", "UCNS geometry",
            "EDCM measurement validity", "phrase or discourse semantics",
        ],
    }
    return DeepRecursionLayer(
        tuple(nodes), relation_binding, tuple(edge_binding), tuple(edges), coverage
    )


__all__ = [
    "DEEP_RECURSION_LAYER", "DeepRecursionError", "DeepRecursionLayer",
    "DefinitionAtom", "build_deep_recursion_layer", "definition_atoms",
    "load_floor_surface_binding",
]
