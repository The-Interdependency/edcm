# === MODULE_BUILD ===
# id: edcm_language_relational_bridge
#   module_name: relational_bridge
#   module_kind: adapter
#   summary: independently constructs direct-atomic and molecular OEWN relation inputs for the UCNS metadata-free relational carrier and freezes external identity bindings before comparison
#   owner: Erin Spencer
#   public_surface: UCNS_RELATIONAL_COMMIT, DirectAtomicFreeze, MolecularFreeze, build_direct_atomic, build_molecular, freeze_branch, compare_frozen_branches, canonical_json_bytes
#   internal_surface: _ucns_api, _digest, _relation_codes
#   auth_boundary: exact UCNS producer commit is pinned by package profile and work-graph artifact
#   storage_boundary: writes caller-selected frozen artifacts only
#   network_boundary: none
#   user_data_boundary: OEWN evidence remains in external bindings and never enters intrinsic UCNS bytes
#   admin_only: false
#   tests: tests.test_language_relational_bridge
#   rollout: explicit lexical-floor builder; no geometry, measurement, canon, or higher-language activation
#   rollback: remove adapter and generated lexical artifacts while preserving source evidence modules
#   requires: ucns_relational_carrier, edcm_language_oewn_source, edcm_language_affixes, edcm_language_morphology
#   since: 2026-08-16
#   unresolved: geometric placement, canonical English morphology, closed compounds, pronunciation, phrase and higher semantics
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: lexical_branches_are_independently_constructed
#   given: direct-atomic and molecular branch builders run
#   then: the direct builder consumes only OEWN lexical and semantic evidence while the molecular builder independently consumes surfaces, declared affixes, and reversible decompositions
#   class: correctness
#   since: 2026-08-16
#
# id: english_metadata_is_external_to_ucns_carrier
#   given: either branch is frozen
#   then: English labels and provenance appear only in the external binding while intrinsic bytes are produced by the pinned UCNS carrier API
#   class: safety
#   since: 2026-08-16
#
# id: comparison_requires_two_prior_freezes
#   given: a branch comparison is requested
#   then: both immutable branch files and their recorded digests are validated before any comparison is emitted
#   class: evidence
#   since: 2026-08-16
# === END CONTRACTS ===

"""EDCM-owned English evidence adapter for UCNS relational representation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .affixes import AffixRecord
from .morphology import MorphologyGraph
from .rendering import normalize_lemma
from .source import WordnetSnapshot

UCNS_RELATIONAL_COMMIT = "d74b8d8139bd1f41a60afc454809edeae641d1e1"
BRANCH_SCHEMA = "edcm.english-lexical-relational-branch"
BRANCH_VERSION = "1.0.0"


class LexicalBridgeError(ValueError):
    pass


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8") + b"\n"


def _digest(payload: bytes) -> str:
    return sha256(payload).hexdigest()


def _ucns_api():
    try:
        from ucns.relational_carrier import (
            build_relational_carrier,
            relational_carrier_bytes,
        )
    except ImportError as exc:
        raise LexicalBridgeError(
            "install the exact EDCM lexical-floor UCNS profile before construction"
        ) from exc
    return build_relational_carrier, relational_carrier_bytes


def _relation_codes(labels: Iterable[str]) -> tuple[dict[str, int], list[dict[str, object]]]:
    ordered = tuple(sorted(set(labels)))
    mapping = {label: index for index, label in enumerate(ordered)}
    return mapping, [{"code": mapping[label], "label": label} for label in ordered]


@dataclass(frozen=True, slots=True)
class DirectAtomicFreeze:
    node_binding: tuple[dict[str, object], ...]
    relation_binding: tuple[dict[str, object], ...]
    edges: tuple[tuple[int, int, int], ...]


@dataclass(frozen=True, slots=True)
class MolecularFreeze:
    node_binding: tuple[dict[str, object], ...]
    relation_binding: tuple[dict[str, object], ...]
    edges: tuple[tuple[int, int, int], ...]


def build_direct_atomic(snapshot: WordnetSnapshot) -> DirectAtomicFreeze:
    """Construct the whole-word branch without reading molecular evidence."""

    surface_records: dict[str, list[Any]] = {}
    for lexeme in snapshot.lexemes:
        surfaces = {normalize_lemma(lexeme.lemma)}
        surfaces.update(normalize_lemma(form) for form in lexeme.forms)
        for surface in surfaces:
            if surface:
                surface_records.setdefault(surface, []).append(lexeme)
    surfaces = tuple(sorted(surface_records))
    senses = tuple(sorted({sense.sense_id for row in snapshot.lexemes for sense in row.senses}))
    synsets = tuple(sorted(item.synset_id for item in snapshot.synsets))
    binding: list[dict[str, object]] = []
    address: dict[tuple[str, str], int] = {}
    for kind, values in (("surface", surfaces), ("sense", senses), ("synset", synsets)):
        for value in values:
            address[(kind, value)] = len(binding)
            binding.append({"address": len(binding), "kind": kind, "identity": value})

    raw_edges: list[tuple[int, str, int]] = []
    for surface in surfaces:
        for lexeme in sorted(surface_records[surface], key=lambda item: (item.lemma, item.part_of_speech)):
            for sense in lexeme.senses:
                raw_edges.append((address[("surface", surface)], "has-sense", address[("sense", sense.sense_id)]))
                raw_edges.append((address[("sense", sense.sense_id)], "in-synset", address[("synset", sense.synset_id)]))
                for relation, targets in sense.relations:
                    for target in targets:
                        target_key = ("sense", target)
                        if target_key in address:
                            raw_edges.append((address[("sense", sense.sense_id)], f"sense:{relation}", address[target_key]))
    for synset in snapshot.synsets:
        for relation, targets in synset.relations:
            for target in targets:
                target_key = ("synset", target)
                if target_key in address:
                    raw_edges.append((address[("synset", synset.synset_id)], f"synset:{relation}", address[target_key]))
    codes, relation_binding = _relation_codes(label for _, label, _ in raw_edges)
    return DirectAtomicFreeze(
        tuple(binding), tuple(relation_binding),
        tuple((source, codes[label], target) for source, label, target in raw_edges),
    )


def build_molecular(
    graph: MorphologyGraph,
    affixes: Iterable[AffixRecord],
) -> MolecularFreeze:
    """Construct the decomposition branch without reading direct branch output."""

    affix_values = tuple(affixes)
    binding: list[dict[str, object]] = []
    address: dict[tuple[str, str], int] = {}
    for kind, values in (
        ("surface", graph.surfaces),
        ("root", graph.roots),
        ("affix", tuple(item.affix_id for item in affix_values)),
    ):
        for value in values:
            address[(kind, value)] = len(binding)
            binding.append({"address": len(binding), "kind": kind, "identity": value})
    raw_edges: list[tuple[int, str, int]] = []
    for root in graph.roots:
        raw_edges.append((address[("surface", root)], "root-evidence", address[("root", root)]))
    for surface in graph.surfaces:
        for alternative_index, alternative in enumerate(graph.immediate(surface)):
            for part_index, part in enumerate(alternative.parts):
                if part.startswith("affix:"):
                    target = address[("affix", part.removeprefix("affix:"))]
                else:
                    target = address[("surface", part.removeprefix("surface:"))]
                label = f"decomposition:{alternative.rule}:{alternative_index}:{part_index}"
                raw_edges.append((address[("surface", surface)], label, target))
    codes, relation_binding = _relation_codes(label for _, label, _ in raw_edges)
    return MolecularFreeze(
        tuple(binding), tuple(relation_binding),
        tuple((source, codes[label], target) for source, label, target in raw_edges),
    )


def freeze_branch(path: str | Path, branch: str, value: DirectAtomicFreeze | MolecularFreeze) -> dict[str, object]:
    """Freeze intrinsic bytes and external bindings as separate sibling files."""

    if branch not in {"direct-atomic", "molecular"}:
        raise LexicalBridgeError("unknown lexical branch")
    build_carrier, carrier_bytes = _ucns_api()
    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    intrinsic = carrier_bytes(build_carrier(len(value.node_binding), value.edges))
    binding = canonical_json_bytes({
        "schema": BRANCH_SCHEMA,
        "version": BRANCH_VERSION,
        "branch": branch,
        "ucns_commit": UCNS_RELATIONAL_COMMIT,
        "node_binding": list(value.node_binding),
        "relation_binding": list(value.relation_binding),
    })
    intrinsic_path = target / f"{branch}.ucns.json"
    binding_path = target / f"{branch}.binding.json"
    intrinsic_path.write_bytes(intrinsic)
    binding_path.write_bytes(binding)
    receipt = {
        "schema": "edcm.english-lexical-branch-freeze",
        "version": "1.0.0",
        "branch": branch,
        "ucns_commit": UCNS_RELATIONAL_COMMIT,
        "node_count": len(value.node_binding),
        "edge_count": len(value.edges),
        "intrinsic_sha256": _digest(intrinsic),
        "binding_sha256": _digest(binding),
        "geometry_attached": False,
        "measurement_attached": False,
        "status": "SURVIVED",
    }
    (target / f"{branch}.receipt.json").write_bytes(canonical_json_bytes(receipt))
    return receipt


def compare_frozen_branches(path: str | Path) -> dict[str, object]:
    """Compare only already-frozen and digest-validated branch artifacts."""

    root = Path(path)
    receipts: dict[str, Mapping[str, Any]] = {}
    bindings: dict[str, Mapping[str, Any]] = {}
    for branch in ("direct-atomic", "molecular"):
        receipt = json.loads((root / f"{branch}.receipt.json").read_bytes())
        intrinsic = (root / f"{branch}.ucns.json").read_bytes()
        binding_bytes = (root / f"{branch}.binding.json").read_bytes()
        if _digest(intrinsic) != receipt["intrinsic_sha256"] or _digest(binding_bytes) != receipt["binding_sha256"]:
            raise LexicalBridgeError(f"{branch} freeze digest mismatch")
        receipts[branch] = receipt
        bindings[branch] = json.loads(binding_bytes)
    direct_surfaces = {
        row["identity"] for row in bindings["direct-atomic"]["node_binding"]
        if row["kind"] == "surface"
    }
    molecular_surfaces = {
        row["identity"] for row in bindings["molecular"]["node_binding"]
        if row["kind"] == "surface"
    }
    result = {
        "schema": "edcm.english-lexical-frozen-comparison",
        "version": "1.0.0",
        "direct_receipt_sha256": _digest(canonical_json_bytes(receipts["direct-atomic"])),
        "molecular_receipt_sha256": _digest(canonical_json_bytes(receipts["molecular"])),
        "shared_surface_count": len(direct_surfaces & molecular_surfaces),
        "direct_only_surface_count": len(direct_surfaces - molecular_surfaces),
        "molecular_only_surface_count": len(molecular_surfaces - direct_surfaces),
        "intrinsic_equal": receipts["direct-atomic"]["intrinsic_sha256"] == receipts["molecular"]["intrinsic_sha256"],
        "interpretation": "preserved-disagreement; no structural equivalence or measurement claim",
        "status": "SURVIVED",
    }
    (root / "comparison.json").write_bytes(canonical_json_bytes(result))
    return result


__all__ = [
    "DirectAtomicFreeze", "LexicalBridgeError", "MolecularFreeze",
    "UCNS_RELATIONAL_COMMIT", "build_direct_atomic", "build_molecular",
    "canonical_json_bytes", "compare_frozen_branches", "freeze_branch",
]
