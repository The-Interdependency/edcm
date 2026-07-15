"""Fail-closed METAPAT authorization lint for actual UCNS payload forks.

METAPAT authorizes constitutive meaning. UCNS owns recursive payload geometry.
This EDCM integration surface binds ordered semantic child ids to exact payload
cell indices and child stable hashes, then rejects any missing, extra, stale, or
tampered authorization.

The linter never infers meaning from a payload. With no matching authorization,
a payload fork is invalid for semantic integration.
"""

# === MODULE_BUILD ===
# id: edcm_ucns_fork_lint
#   module_name: ucns_fork_lint
#   module_kind: adapter
#   summary: binds METAPAT constitutive-fork authorizations to exact UCNS payload paths, indices, and stable hashes and fails closed over the complete recursive object
#   owner: Erin Spencer
#   public_surface: UCNSForkTopologyBinding, AuthorizedUCNSFork, UCNSForkLintReport, ForkLintDependencyError, ForkTopologyError, build_fork_topology_binding, lint_fork_topology, lint_all_payload_forks, enumerate_payload_fork_paths
#   internal_surface: _load_stack, _canonical_json, _text, _strings, _indices, _binding_payload, _binding_digest, _resolve_path, _payload_cells
#   auth_boundary: none
#   storage_boundary: serialization-only
#   network_boundary: optional package import only; no network performed by runtime code
#   user_data_boundary: semantic module ids and unresolved constraints remain producer provenance; transcript content and measurement values are not accepted
#   admin_only: false
#   tests: tests.test_ucns_fork_lint
#   rollout: optional_full_stack_integration
#   rollback: remove exports and consumer call sites; METAPAT authorization and UCNS geometry remain separate upstream authorities
#   requires: edcm_metapat_adapter, edcm_ucns_adapter
#   since: 2026-07-15
#   unresolved: no accepted production fixture exists until a caller supplies complete authorizations for every actual payload fork
# === END MODULE_BUILD ===

# === DOCS ===
# id: edcm_ucns_fork_lint_docs
#   summary: documents exact topology binding, complete recursive coverage, negative fixtures, and authority boundaries
#   audience: developer
#   source: docs/ucns-fork-lint.md
#   covers: UCNSForkTopologyBinding, build_fork_topology_binding, lint_fork_topology, lint_all_payload_forks
#   status: current
# === END DOCS ===

# === CAPABILITIES ===
# id: edcm_fail_closed_ucns_fork_lint
#   summary: validates every actual recursive UCNS payload fork against one exact METAPAT authorization and topology binding
#   exposes: edcm.lint_all_payload_forks
#   inputs: actual UCNSObject root and AuthorizedUCNSFork declarations
#   outputs: UCNSForkLintReport or typed failure
#   boundaries: auth:none, storage:serialization-only, network:none, user_data:semantic provenance only
# === END CAPABILITIES ===

# === BOUNDARIES ===
# id: edcm_ucns_fork_lint_boundary
#   summary: EDCM verifies authority-to-geometry binding but does not invent METAPAT meaning, alter UCNS algebra, or transfer proof status into measurement validity
#   auth_boundary: none
#   storage_boundary: serialization-only
#   network_boundary: none
#   user_data_boundary: no transcript or measurement values
#   admin_only: false
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: edcm_fork_binding_exact_topology
#   given: a METAPAT authorization is bound to an actual UCNS fork
#   then: root hash, fork path/hash, payload indices, ordered child ids/hashes, canon, policy, and authorization digest are exact
#   class: integration_contract
#
# id: edcm_fork_lint_complete_coverage
#   given: a recursive UCNS object is linted
#   then: every object with at least two payload children has exactly one valid declaration
#   class: safety
#
# id: edcm_fork_lint_missing_extra_rejected
#   given: a declaration is missing, duplicated, or targets a non-fork path
#   then: lint fails closed
#   class: safety
#
# id: edcm_fork_lint_drift_rejected
#   given: payload order, cell indices, object hashes, canon, policy, or producer authorization changes
#   then: lint fails closed
#   class: safety
#
# id: edcm_fork_lint_no_inference
#   given: geometry has fewer than two payload children or no declaration
#   then: no constitutive meaning is inferred; only actual forks require explicit authority
#   class: boundary_contract
#
# id: edcm_fork_binding_roundtrip
#   given: a topology binding is serialized and reconstructed
#   then: every field survives exactly and malformed or tampered records fail closed
#   class: schema_contract
#
# id: edcm_fork_lint_no_status_transfer
#   given: a valid binding and lint report
#   then: theorem_status_transfer and measurement_validity_claim remain false
#   class: boundary_contract
#
# id: edcm_fork_lint_dependency_visible
#   given: UCNS or METAPAT is directly absent or transitively broken
#   then: direct absence is typed and transitive import failure remains visible
#   class: safety
# === END CONTRACTS ===

from __future__ import annotations

import hashlib
import importlib
import json
from dataclasses import dataclass
from types import ModuleType
from typing import Any, Iterable, Mapping, Sequence

BINDING_SCHEMA_ID = "edcm.ucns-fork-topology-binding"
BINDING_SCHEMA_VERSION = "1.0.0"
LINT_REPORT_SCHEMA_ID = "edcm.ucns-fork-lint-report"
LINT_REPORT_SCHEMA_VERSION = "1.0.0"
TOPOLOGY_KIND = "ucns-payload-fork"
CONSTITUTIVE_RELATION_KIND = "constitutive-simultaneous"


class ForkLintDependencyError(ModuleNotFoundError):
    """Raised when full-stack lint is requested without UCNS or METAPAT."""


class ForkTopologyError(ValueError):
    """Raised when an authorization or topology binding fails closed."""


def _load_stack() -> tuple[ModuleType, ModuleType]:
    modules = []
    for name in ("ucns", "metapat"):
        try:
            module = importlib.import_module(name)
        except ModuleNotFoundError as exc:
            if exc.name != name:
                raise
            raise ForkLintDependencyError(
                "UCNS fork lint requires EDCM's `full-stack` extra.", name=name
            ) from exc
        modules.append(module)
    ucns, metapat = modules
    ucns_required = ("UCNSObject", "stable_hash")
    metapat_required = (
        "MetapatModuleEnvelope",
        "UCNSForkAuthorization",
        "validate_fork_authorization",
        "PHI_POLICY_VERSION",
        "CONSTITUTIVE_RELATION_KIND",
    )
    missing = [f"ucns.{name}" for name in ucns_required if not hasattr(ucns, name)]
    missing += [
        f"metapat.{name}" for name in metapat_required if not hasattr(metapat, name)
    ]
    if missing:
        raise ForkTopologyError(
            "full-stack packages are missing required public surfaces: "
            + ", ".join(missing)
        )
    return ucns, metapat


def _canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ForkTopologyError(f"{name} must be a non-empty string")
    return value


def _strings(value: Any, name: str, *, minimum: int = 0) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        raise ForkTopologyError(f"{name} must be an array of strings")
    result = tuple(value)
    if len(result) < minimum:
        raise ForkTopologyError(f"{name} must contain at least {minimum} entries")
    if any(not isinstance(item, str) or not item.strip() for item in result):
        raise ForkTopologyError(f"{name} must contain only non-empty strings")
    return result


def _indices(value: Any, name: str, *, minimum: int = 0) -> tuple[int, ...]:
    if not isinstance(value, (list, tuple)):
        raise ForkTopologyError(f"{name} must be an array of non-negative integers")
    result = tuple(value)
    if len(result) < minimum:
        raise ForkTopologyError(f"{name} must contain at least {minimum} entries")
    if any(not isinstance(item, int) or isinstance(item, bool) or item < 0 for item in result):
        raise ForkTopologyError(f"{name} must contain non-negative integers")
    return result


def _binding_payload(
    *,
    root_object_hash: str,
    fork_object_hash: str,
    fork_path: tuple[int, ...],
    parent_module_id: str,
    child_module_ids: tuple[str, ...],
    payload_cell_indices: tuple[int, ...],
    child_object_hashes: tuple[str, ...],
    authorization_digest: str,
    canon_digest: str,
    encoding_policy_version: str,
    unresolved_constraints: tuple[str, ...],
) -> dict[str, Any]:
    return {
        "schema_id": BINDING_SCHEMA_ID,
        "schema_version": BINDING_SCHEMA_VERSION,
        "topology_kind": TOPOLOGY_KIND,
        "root_object_hash": root_object_hash,
        "fork_object_hash": fork_object_hash,
        "fork_path": list(fork_path),
        "parent_module_id": parent_module_id,
        "child_module_ids": list(child_module_ids),
        "payload_cell_indices": list(payload_cell_indices),
        "child_object_hashes": list(child_object_hashes),
        "authorization_digest": authorization_digest,
        "canon_digest": canon_digest,
        "encoding_policy_version": encoding_policy_version,
        "relation_kind": CONSTITUTIVE_RELATION_KIND,
        "unresolved_constraints": list(unresolved_constraints),
        "theorem_status_transfer": False,
        "measurement_validity_claim": False,
    }


def _binding_digest(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class UCNSForkTopologyBinding:
    schema_id: str
    schema_version: str
    topology_kind: str
    root_object_hash: str
    fork_object_hash: str
    fork_path: tuple[int, ...]
    parent_module_id: str
    child_module_ids: tuple[str, ...]
    payload_cell_indices: tuple[int, ...]
    child_object_hashes: tuple[str, ...]
    authorization_digest: str
    canon_digest: str
    encoding_policy_version: str
    relation_kind: str
    unresolved_constraints: tuple[str, ...]
    theorem_status_transfer: bool
    measurement_validity_claim: bool
    binding_digest: str

    def __post_init__(self) -> None:
        if self.schema_id != BINDING_SCHEMA_ID or self.schema_version != BINDING_SCHEMA_VERSION:
            raise ForkTopologyError("unsupported fork topology binding schema")
        if self.topology_kind != TOPOLOGY_KIND:
            raise ForkTopologyError(f"topology_kind must be {TOPOLOGY_KIND}")
        for name in (
            "root_object_hash", "fork_object_hash", "parent_module_id",
            "authorization_digest", "canon_digest", "encoding_policy_version",
        ):
            _text(getattr(self, name), name)
        path = _indices(self.fork_path, "fork_path")
        children = _strings(self.child_module_ids, "child_module_ids", minimum=2)
        cells = _indices(self.payload_cell_indices, "payload_cell_indices", minimum=2)
        hashes = _strings(self.child_object_hashes, "child_object_hashes", minimum=2)
        if len(children) != len(cells) or len(children) != len(hashes):
            raise ForkTopologyError("children, payload indices, and child hashes must have equal length")
        if tuple(sorted(cells)) != cells or len(set(cells)) != len(cells):
            raise ForkTopologyError("payload_cell_indices must be unique and increasing")
        if self.relation_kind != CONSTITUTIVE_RELATION_KIND:
            raise ForkTopologyError("relation_kind must be constitutive-simultaneous")
        _strings(self.unresolved_constraints, "unresolved_constraints")
        if self.theorem_status_transfer is not False or self.measurement_validity_claim is not False:
            raise ForkTopologyError("fork binding status-transfer fields must be false")
        if self.binding_digest != _binding_digest(self._payload()):
            raise ForkTopologyError("binding_digest mismatch")
        object.__setattr__(self, "fork_path", path)
        object.__setattr__(self, "child_module_ids", children)
        object.__setattr__(self, "payload_cell_indices", cells)
        object.__setattr__(self, "child_object_hashes", hashes)

    def _payload(self) -> dict[str, Any]:
        return _binding_payload(
            root_object_hash=self.root_object_hash,
            fork_object_hash=self.fork_object_hash,
            fork_path=self.fork_path,
            parent_module_id=self.parent_module_id,
            child_module_ids=self.child_module_ids,
            payload_cell_indices=self.payload_cell_indices,
            child_object_hashes=self.child_object_hashes,
            authorization_digest=self.authorization_digest,
            canon_digest=self.canon_digest,
            encoding_policy_version=self.encoding_policy_version,
            unresolved_constraints=self.unresolved_constraints,
        )

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "binding_digest": self.binding_digest}

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "UCNSForkTopologyBinding":
        if not isinstance(data, Mapping):
            raise ForkTopologyError("fork topology binding must be a mapping")
        expected = {
            "schema_id", "schema_version", "topology_kind", "root_object_hash",
            "fork_object_hash", "fork_path", "parent_module_id", "child_module_ids",
            "payload_cell_indices", "child_object_hashes", "authorization_digest",
            "canon_digest", "encoding_policy_version", "relation_kind",
            "unresolved_constraints", "theorem_status_transfer",
            "measurement_validity_claim", "binding_digest",
        }
        unknown, missing = set(data) - expected, expected - set(data)
        if unknown:
            raise ForkTopologyError(f"unknown fork binding fields: {sorted(unknown)!r}")
        if missing:
            raise ForkTopologyError(f"missing fork binding fields: {sorted(missing)!r}")
        if not isinstance(data["theorem_status_transfer"], bool) or not isinstance(data["measurement_validity_claim"], bool):
            raise ForkTopologyError("status-transfer fields must be boolean")
        return cls(
            schema_id=_text(data["schema_id"], "schema_id"),
            schema_version=_text(data["schema_version"], "schema_version"),
            topology_kind=_text(data["topology_kind"], "topology_kind"),
            root_object_hash=_text(data["root_object_hash"], "root_object_hash"),
            fork_object_hash=_text(data["fork_object_hash"], "fork_object_hash"),
            fork_path=_indices(data["fork_path"], "fork_path"),
            parent_module_id=_text(data["parent_module_id"], "parent_module_id"),
            child_module_ids=_strings(data["child_module_ids"], "child_module_ids", minimum=2),
            payload_cell_indices=_indices(data["payload_cell_indices"], "payload_cell_indices", minimum=2),
            child_object_hashes=_strings(data["child_object_hashes"], "child_object_hashes", minimum=2),
            authorization_digest=_text(data["authorization_digest"], "authorization_digest"),
            canon_digest=_text(data["canon_digest"], "canon_digest"),
            encoding_policy_version=_text(data["encoding_policy_version"], "encoding_policy_version"),
            relation_kind=_text(data["relation_kind"], "relation_kind"),
            unresolved_constraints=_strings(data["unresolved_constraints"], "unresolved_constraints"),
            theorem_status_transfer=data["theorem_status_transfer"],
            measurement_validity_claim=data["measurement_validity_claim"],
            binding_digest=_text(data["binding_digest"], "binding_digest"),
        )

    @classmethod
    def from_json(cls, value: str) -> "UCNSForkTopologyBinding":
        if not isinstance(value, str):
            raise ForkTopologyError("fork topology binding JSON must be a string")
        decoded = json.loads(value)
        if not isinstance(decoded, dict):
            raise ForkTopologyError("fork topology binding JSON must decode to an object")
        return cls.from_dict(decoded)


@dataclass(frozen=True, slots=True)
class AuthorizedUCNSFork:
    envelope: Any
    authorization: Any
    binding: UCNSForkTopologyBinding


@dataclass(frozen=True, slots=True)
class UCNSForkLintReport:
    root_object_hash: str
    fork_paths: tuple[tuple[int, ...], ...]
    authorization_digests: tuple[str, ...]
    schema_id: str = LINT_REPORT_SCHEMA_ID
    schema_version: str = LINT_REPORT_SCHEMA_VERSION
    valid: bool = True
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "root_object_hash": self.root_object_hash,
            "fork_paths": [list(path) for path in self.fork_paths],
            "authorization_digests": list(self.authorization_digests),
            "valid": self.valid,
            "theorem_status_transfer": self.theorem_status_transfer,
            "measurement_validity_claim": self.measurement_validity_claim,
        }


def _resolve_path(root: Any, path: Sequence[int], ucns: ModuleType) -> Any:
    if not isinstance(root, ucns.UCNSObject):
        raise TypeError("root must be an actual ucns.UCNSObject")
    current = root
    for depth, index in enumerate(_indices(tuple(path), "fork_path")):
        if index >= len(current.A_plus):
            raise ForkTopologyError(f"fork_path index out of range at depth {depth}")
        payload = current.A_plus[index][1]
        if payload is None:
            raise ForkTopologyError(f"fork_path enters a unit payload at depth {depth}")
        if not isinstance(payload, ucns.UCNSObject):
            raise ForkTopologyError("fork_path encountered a non-UCNS payload")
        current = payload
    return current


def _payload_cells(obj: Any, ucns: ModuleType) -> tuple[tuple[int, Any], ...]:
    cells = []
    for index, (_, payload) in enumerate(obj.A_plus):
        if payload is None:
            continue
        if not isinstance(payload, ucns.UCNSObject):
            raise ForkTopologyError("UCNS object contains a non-UCNS payload")
        cells.append((index, payload))
    return tuple(cells)


def enumerate_payload_fork_paths(root: Any) -> tuple[tuple[int, ...], ...]:
    """Return every recursive path whose object has at least two payload children."""

    ucns, _ = _load_stack()
    if not isinstance(root, ucns.UCNSObject):
        raise TypeError("root must be an actual ucns.UCNSObject")
    found: list[tuple[int, ...]] = []
    active: set[int] = set()

    def walk(obj: Any, path: tuple[int, ...]) -> None:
        identity = id(obj)
        if identity in active:
            raise ForkTopologyError("cyclic UCNS payload graph is not admissible")
        active.add(identity)
        cells = _payload_cells(obj, ucns)
        if len(cells) >= 2:
            found.append(path)
        for index, payload in cells:
            walk(payload, path + (index,))
        active.remove(identity)

    walk(root, ())
    return tuple(found)


def build_fork_topology_binding(
    root: Any,
    authorization: Any,
    *,
    fork_path: Sequence[int] = (),
) -> UCNSForkTopologyBinding:
    """Bind one producer authorization to exact actual UCNS payload identities."""

    ucns, metapat = _load_stack()
    if not isinstance(authorization, metapat.UCNSForkAuthorization):
        raise TypeError("authorization must be a metapat.UCNSForkAuthorization")
    fork = _resolve_path(root, fork_path, ucns)
    cells = _payload_cells(fork, ucns)
    if len(cells) < 2:
        raise ForkTopologyError("target path is not a payload fork")
    if len(cells) != len(authorization.child_module_ids):
        raise ForkTopologyError("authorization child count does not match payload count")
    payload = _binding_payload(
        root_object_hash=ucns.stable_hash(root),
        fork_object_hash=ucns.stable_hash(fork),
        fork_path=tuple(fork_path),
        parent_module_id=authorization.parent_module_id,
        child_module_ids=tuple(authorization.child_module_ids),
        payload_cell_indices=tuple(index for index, _ in cells),
        child_object_hashes=tuple(ucns.stable_hash(child) for _, child in cells),
        authorization_digest=authorization.authorization_digest,
        canon_digest=authorization.canon_digest,
        encoding_policy_version=authorization.encoding_policy_version,
        unresolved_constraints=tuple(authorization.unresolved_constraints),
    )
    return UCNSForkTopologyBinding(
        fork_path=tuple(fork_path),
        child_module_ids=tuple(authorization.child_module_ids),
        payload_cell_indices=tuple(index for index, _ in cells),
        child_object_hashes=tuple(ucns.stable_hash(child) for _, child in cells),
        unresolved_constraints=tuple(authorization.unresolved_constraints),
        binding_digest=_binding_digest(payload),
        **{key: payload[key] for key in (
            "schema_id", "schema_version", "topology_kind", "root_object_hash",
            "fork_object_hash", "parent_module_id", "authorization_digest",
            "canon_digest", "encoding_policy_version", "relation_kind",
            "theorem_status_transfer", "measurement_validity_claim",
        )},
    )


def lint_fork_topology(
    root: Any,
    *,
    envelope: Any,
    authorization: Any,
    binding: UCNSForkTopologyBinding,
) -> UCNSForkTopologyBinding:
    """Validate one exact producer authorization against one actual payload fork."""

    ucns, metapat = _load_stack()
    if not isinstance(envelope, metapat.MetapatModuleEnvelope):
        raise TypeError("envelope must be a metapat.MetapatModuleEnvelope")
    if not isinstance(authorization, metapat.UCNSForkAuthorization):
        raise TypeError("authorization must be a metapat.UCNSForkAuthorization")
    if not isinstance(binding, UCNSForkTopologyBinding):
        raise TypeError("binding must be a UCNSForkTopologyBinding")
    try:
        metapat.validate_fork_authorization(
            authorization,
            envelope=envelope,
            child_module_ids=binding.child_module_ids,
        )
    except Exception as exc:
        raise ForkTopologyError("METAPAT fork authorization validation failed") from exc
    fork = _resolve_path(root, binding.fork_path, ucns)
    cells = _payload_cells(fork, ucns)
    expected = {
        "root_object_hash": ucns.stable_hash(root),
        "fork_object_hash": ucns.stable_hash(fork),
        "parent_module_id": authorization.parent_module_id,
        "payload_cell_indices": tuple(index for index, _ in cells),
        "child_object_hashes": tuple(ucns.stable_hash(child) for _, child in cells),
        "authorization_digest": authorization.authorization_digest,
        "canon_digest": authorization.canon_digest,
        "encoding_policy_version": authorization.encoding_policy_version,
        "relation_kind": metapat.CONSTITUTIVE_RELATION_KIND,
    }
    for name, value in expected.items():
        if getattr(binding, name) != value:
            raise ForkTopologyError(f"fork topology {name} mismatch")
    if len(cells) < 2:
        raise ForkTopologyError("authorized path is no longer a payload fork")
    return binding


def lint_all_payload_forks(
    root: Any,
    declarations: Iterable[AuthorizedUCNSFork],
) -> UCNSForkLintReport:
    """Require exactly one valid declaration for every recursive payload fork."""

    ucns, _ = _load_stack()
    actual_paths = enumerate_payload_fork_paths(root)
    by_path: dict[tuple[int, ...], AuthorizedUCNSFork] = {}
    for declaration in declarations:
        if not isinstance(declaration, AuthorizedUCNSFork):
            raise TypeError("declarations must contain AuthorizedUCNSFork values")
        path = declaration.binding.fork_path
        if path in by_path:
            raise ForkTopologyError(f"duplicate fork declaration for path {path!r}")
        by_path[path] = declaration
    missing = tuple(path for path in actual_paths if path not in by_path)
    extra = tuple(path for path in by_path if path not in set(actual_paths))
    if missing:
        raise ForkTopologyError(f"missing fork authorization for paths {missing!r}")
    if extra:
        raise ForkTopologyError(f"authorization supplied for non-fork paths {extra!r}")
    digests = []
    for path in actual_paths:
        declaration = by_path[path]
        lint_fork_topology(
            root,
            envelope=declaration.envelope,
            authorization=declaration.authorization,
            binding=declaration.binding,
        )
        digests.append(declaration.authorization.authorization_digest)
    return UCNSForkLintReport(
        root_object_hash=ucns.stable_hash(root),
        fork_paths=actual_paths,
        authorization_digests=tuple(digests),
    )


__all__ = [
    "AuthorizedUCNSFork", "BINDING_SCHEMA_ID", "BINDING_SCHEMA_VERSION",
    "ForkLintDependencyError", "ForkTopologyError", "UCNSForkLintReport",
    "UCNSForkTopologyBinding", "build_fork_topology_binding",
    "enumerate_payload_fork_paths", "lint_all_payload_forks", "lint_fork_topology",
]
