# === MODULE_BUILD ===
# id: edcm_language_relational_bridge
#   module_name: relational_bridge
#   module_kind: adapter
#   summary: independently constructs direct-atomic and molecular OEWN relation inputs for the UCNS metadata-free relational carrier and freezes external identity bindings before comparison
#   owner: Erin Spencer
#   public_surface: UCNS_RELATIONAL_COMMIT, UCNSProducerVerification, DirectAtomicFreeze, MolecularFreeze, verify_ucns_producer, build_direct_atomic, build_molecular, freeze_branch, validate_frozen_branch, compare_frozen_branches, canonical_json_bytes
#   internal_surface: _ucns_api, _digest, _relation_codes, _git
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
# id: lexical_relation_multiplicity_is_preserved
#   given: direct semantic evidence or molecular alternatives contain repeated relation occurrences
#   then: every occurrence remains in supplied order in the UCNS relational input without deduplication
#   class: correctness
#   since: 2026-08-16
#
# id: lexical_pre_replay_status_is_unresolved
#   given: one branch freeze or within-run branch comparison completes
#   then: its status is UNRESOLVED until a separately recorded clean independent replay agrees byte-for-byte
#   class: doctrine
#   since: 2026-08-16
#
# id: lexical_ucns_producer_is_exactly_verified
#   given: EDCM opens the UCNS relational construction API
#   then: the checkout HEAD equals the merged producer commit and the imported producer module is the exact source-root file whose bytes match the verification receipt
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
import subprocess
from typing import Any, Iterable, Mapping

from .affixes import AffixRecord
from .morphology import MorphologyGraph
from .rendering import normalize_lemma
from .source import WordnetSnapshot

UCNS_RELATIONAL_COMMIT = "d7c6f51304ed6c32d48badf63132bea6de8af497"
UCNS_RELATIONAL_MODULE_SHA256 = "b839d29c79b43d29faf6f5d9a39b7a1485f39a0f071b525fd1848cf18f061cdd"
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


def _git(repo: Path, *arguments: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo), *arguments],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise LexicalBridgeError("UCNS producer checkout verification failed") from exc


@dataclass(frozen=True, slots=True)
class UCNSProducerVerification:
    source_root: str
    commit: str
    module_sha256: str


def verify_ucns_producer(source_root: str | Path) -> UCNSProducerVerification:
    """Bind the imported API to the exact merged UCNS checkout bytes."""

    root = Path(source_root).resolve()
    if _git(root, "rev-parse", "HEAD") != UCNS_RELATIONAL_COMMIT:
        raise LexicalBridgeError("UCNS producer checkout commit mismatch")
    module_path = (root / "src" / "ucns" / "relational_carrier.py").resolve()
    if not module_path.is_file():
        raise LexicalBridgeError("UCNS relational carrier module is missing")
    working_bytes = module_path.read_bytes()
    try:
        committed_bytes = subprocess.check_output(
            ["git", "-C", str(root), "show", "HEAD:src/ucns/relational_carrier.py"],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        raise LexicalBridgeError("UCNS producer module commit verification failed") from exc
    if working_bytes != committed_bytes:
        raise LexicalBridgeError("UCNS relational carrier has uncommitted changes")
    module_digest = _digest(committed_bytes)
    if module_digest != UCNS_RELATIONAL_MODULE_SHA256:
        raise LexicalBridgeError("UCNS relational carrier committed digest mismatch")
    try:
        import ucns.relational_carrier as module
    except ImportError as exc:
        raise LexicalBridgeError("exact UCNS relational producer is not importable") from exc
    imported_path = Path(module.__file__ or "").resolve()
    if imported_path != module_path:
        raise LexicalBridgeError("imported UCNS producer does not come from the verified checkout")
    return UCNSProducerVerification(
        source_root=str(root),
        commit=UCNS_RELATIONAL_COMMIT,
        module_sha256=module_digest,
    )


def _ucns_api(verification: UCNSProducerVerification):
    if not isinstance(verification, UCNSProducerVerification):
        raise LexicalBridgeError("an exact UCNS producer verification is required")
    if verification.commit != UCNS_RELATIONAL_COMMIT:
        raise LexicalBridgeError("UCNS producer verification commit mismatch")
    try:
        import ucns.relational_carrier as module
    except ImportError as exc:
        raise LexicalBridgeError(
            "install the exact EDCM lexical-floor UCNS profile before construction"
        ) from exc
    expected_path = (
        Path(verification.source_root) / "src" / "ucns" / "relational_carrier.py"
    ).resolve()
    imported_path = Path(module.__file__ or "").resolve()
    if imported_path != expected_path or _digest(imported_path.read_bytes()) != verification.module_sha256:
        raise LexicalBridgeError("UCNS producer bytes changed after verification")
    return module.build_relational_carrier, module.relational_carrier_bytes


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
    for lexeme in snapshot.lexemes:
        for sense in lexeme.senses:
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


def freeze_branch(
    path: str | Path,
    branch: str,
    value: DirectAtomicFreeze | MolecularFreeze,
    verification: UCNSProducerVerification,
) -> dict[str, object]:
    """Freeze intrinsic bytes and external bindings as separate sibling files."""

    branch_types = {
        "direct-atomic": DirectAtomicFreeze,
        "molecular": MolecularFreeze,
    }
    if branch not in branch_types:
        raise LexicalBridgeError("unknown lexical branch")
    if not isinstance(value, branch_types[branch]):
        raise LexicalBridgeError(f"{branch} branch value type mismatch")
    build_carrier, carrier_bytes = _ucns_api(verification)
    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    intrinsic = carrier_bytes(build_carrier(len(value.node_binding), value.edges))
    binding = canonical_json_bytes({
        "schema": BRANCH_SCHEMA,
        "version": BRANCH_VERSION,
        "branch": branch,
        "ucns_commit": UCNS_RELATIONAL_COMMIT,
        "ucns_module_sha256": verification.module_sha256,
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
        "ucns_module_sha256": verification.module_sha256,
        "node_count": len(value.node_binding),
        "edge_count": len(value.edges),
        "intrinsic_sha256": _digest(intrinsic),
        "binding_sha256": _digest(binding),
        "geometry_attached": False,
        "measurement_attached": False,
        "status": "UNRESOLVED",
    }
    (target / f"{branch}.receipt.json").write_bytes(canonical_json_bytes(receipt))
    return receipt


def validate_frozen_branch(
    path: str | Path,
    branch: str,
    verification: UCNSProducerVerification,
) -> dict[str, object]:
    """Validate a resumable branch freeze completely or fail closed."""

    _ucns_api(verification)
    root = Path(path)
    receipt_bytes = (root / f"{branch}.receipt.json").read_bytes()
    receipt = json.loads(receipt_bytes)
    if canonical_json_bytes(receipt) != receipt_bytes:
        raise LexicalBridgeError(f"{branch} receipt is not canonical")
    if receipt.get("branch") != branch or receipt.get("ucns_commit") != UCNS_RELATIONAL_COMMIT:
        raise LexicalBridgeError(f"{branch} receipt identity mismatch")
    if receipt.get("ucns_module_sha256") != verification.module_sha256:
        raise LexicalBridgeError(f"{branch} producer module mismatch")
    if receipt.get("status") != "UNRESOLVED":
        raise LexicalBridgeError(f"{branch} pre-replay status mismatch")
    intrinsic = (root / f"{branch}.ucns.json").read_bytes()
    binding_bytes = (root / f"{branch}.binding.json").read_bytes()
    if _digest(intrinsic) != receipt.get("intrinsic_sha256") or _digest(binding_bytes) != receipt.get("binding_sha256"):
        raise LexicalBridgeError(f"{branch} freeze digest mismatch")
    binding = json.loads(binding_bytes)
    if canonical_json_bytes(binding) != binding_bytes:
        raise LexicalBridgeError(f"{branch} binding is not canonical")
    if binding.get("branch") != branch or binding.get("ucns_commit") != UCNS_RELATIONAL_COMMIT:
        raise LexicalBridgeError(f"{branch} binding identity mismatch")
    if binding.get("ucns_module_sha256") != verification.module_sha256:
        raise LexicalBridgeError(f"{branch} binding producer mismatch")
    if len(binding.get("node_binding", ())) != receipt.get("node_count"):
        raise LexicalBridgeError(f"{branch} node count mismatch")
    return receipt


def compare_frozen_branches(
    path: str | Path,
    verification: UCNSProducerVerification,
) -> dict[str, object]:
    """Compare only already-frozen and digest-validated branch artifacts."""

    root = Path(path)
    receipts: dict[str, Mapping[str, Any]] = {}
    bindings: dict[str, Mapping[str, Any]] = {}
    for branch in ("direct-atomic", "molecular"):
        receipt = validate_frozen_branch(root, branch, verification)
        binding_bytes = (root / f"{branch}.binding.json").read_bytes()
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
        "status": "UNRESOLVED",
    }
    (root / "comparison.json").write_bytes(canonical_json_bytes(result))
    return result


__all__ = [
    "DirectAtomicFreeze", "LexicalBridgeError", "MolecularFreeze",
    "UCNSProducerVerification",
    "UCNS_RELATIONAL_COMMIT", "UCNS_RELATIONAL_MODULE_SHA256",
    "build_direct_atomic", "build_molecular",
    "canonical_json_bytes", "compare_frozen_branches", "freeze_branch",
    "validate_frozen_branch", "verify_ucns_producer",
]
