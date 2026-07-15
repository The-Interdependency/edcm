"""Contracts for fail-closed METAPAT-to-UCNS payload fork lint."""

from __future__ import annotations

# === CHECKS ===
# id: check_edcm_fork_binding_exact
#   proves: edcm_fork_binding_exact_topology
#   call: self::test_binding_captures_exact_payload_topology
#   mutates: none
#   cleanup: none
#
# id: check_edcm_fork_complete_coverage
#   proves: edcm_fork_lint_complete_coverage
#   call: self::test_complete_recursive_lint_accepts_every_declared_fork
#   mutates: none
#   cleanup: none
#
# id: check_edcm_fork_missing_extra
#   proves: edcm_fork_lint_missing_extra_rejected
#   call: self::test_missing_duplicate_and_extra_declarations_fail_closed
#   mutates: none
#   cleanup: none
#
# id: check_edcm_fork_drift
#   proves: edcm_fork_lint_drift_rejected
#   call: self::test_payload_order_or_object_drift_fails_closed
#   mutates: none
#   cleanup: none
#
# id: check_edcm_fork_no_inference
#   proves: edcm_fork_lint_no_inference
#   call: self::test_single_payload_is_not_silently_typed_as_a_fork
#   mutates: none
#   cleanup: none
#
# id: check_edcm_fork_roundtrip
#   proves: edcm_fork_binding_roundtrip
#   call: self::test_binding_roundtrip_is_strict_and_tamper_evident
#   mutates: none
#   cleanup: none
#
# id: check_edcm_fork_status_firewall
#   proves: edcm_fork_lint_no_status_transfer
#   call: self::test_valid_report_preserves_status_firewall
#   mutates: none
#   cleanup: none
#
# id: check_edcm_fork_dependency
#   proves: edcm_fork_lint_dependency_visible
#   call: self::test_direct_dependency_absence_is_typed
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import hashlib
import importlib
import json
import sys
import types
from dataclasses import dataclass, replace
from fractions import Fraction

import pytest

from edcm.ucns_fork_lint import (
    AuthorizedUCNSFork,
    ForkLintDependencyError,
    ForkTopologyError,
    UCNSForkTopologyBinding,
    build_fork_topology_binding,
    enumerate_payload_fork_paths,
    lint_all_payload_forks,
    lint_fork_topology,
)


class FakeUCNSObject:
    def __init__(self, cells):
        self.A_plus = list(cells)


def _fake_hash(obj):
    def encode(node):
        return [
            [str(angle), None if payload is None else encode(payload)]
            for angle, payload in node.A_plus
        ]

    return hashlib.sha256(
        json.dumps(encode(obj), separators=(",", ":")).encode("utf-8")
    ).hexdigest()


@dataclass(frozen=True)
class FakeEnvelope:
    module_id: str = "metapat.parent"
    canon_digest: str = "c" * 64
    source_statement_refs: tuple[str, ...] = ("AXIOMS.md#parent",)


@dataclass(frozen=True)
class FakeAuthorization:
    parent_module_id: str
    child_module_ids: tuple[str, ...]
    source_statement_refs: tuple[str, ...]
    canon_digest: str
    encoding_policy_version: str = "1.0.0"
    relation_kind: str = "constitutive-simultaneous"
    unresolved_constraints: tuple[str, ...] = ()
    theorem_status_transfer: bool = False
    metapat_validity_claim: bool = False
    authorization_digest: str = "a" * 64


def _fake_validate(authorization, *, envelope, child_module_ids):
    if authorization.parent_module_id != envelope.module_id:
        raise ValueError("parent mismatch")
    if authorization.child_module_ids != tuple(child_module_ids):
        raise ValueError("child mismatch")
    if authorization.canon_digest != envelope.canon_digest:
        raise ValueError("canon mismatch")
    if authorization.relation_kind != "constitutive-simultaneous":
        raise ValueError("relation mismatch")
    return authorization


@pytest.fixture(autouse=True)
def fake_stack(monkeypatch):
    ucns = types.ModuleType("ucns")
    ucns.UCNSObject = FakeUCNSObject
    ucns.stable_hash = _fake_hash
    metapat = types.ModuleType("metapat")
    metapat.MetapatModuleEnvelope = FakeEnvelope
    metapat.UCNSForkAuthorization = FakeAuthorization
    metapat.validate_fork_authorization = _fake_validate
    metapat.PHI_POLICY_VERSION = "1.0.0"
    metapat.CONSTITUTIVE_RELATION_KIND = "constitutive-simultaneous"
    monkeypatch.setitem(sys.modules, "ucns", ucns)
    monkeypatch.setitem(sys.modules, "metapat", metapat)
    return ucns, metapat


def _leaf(face: int) -> FakeUCNSObject:
    return FakeUCNSObject(((Fraction(face, 1), None),))


def _root_with_two_children() -> FakeUCNSObject:
    return FakeUCNSObject(
        (
            (Fraction(0, 1), None),
            (Fraction(1, 3), _leaf(0)),
            (Fraction(2, 3), _leaf(1)),
        )
    )


def _authorization(children=("metapat.child.alpha", "metapat.child.beta")):
    envelope = FakeEnvelope()
    authorization = FakeAuthorization(
        parent_module_id=envelope.module_id,
        child_module_ids=tuple(children),
        source_statement_refs=envelope.source_statement_refs,
        canon_digest=envelope.canon_digest,
    )
    return envelope, authorization


def _declaration(root, *, path=(), children=("metapat.child.alpha", "metapat.child.beta")):
    envelope, authorization = _authorization(children)
    binding = build_fork_topology_binding(root, authorization, fork_path=path)
    return AuthorizedUCNSFork(envelope, authorization, binding)


def test_binding_captures_exact_payload_topology() -> None:
    root = _root_with_two_children()
    declaration = _declaration(root)
    binding = declaration.binding
    assert binding.fork_path == ()
    assert binding.payload_cell_indices == (1, 2)
    assert binding.child_module_ids == declaration.authorization.child_module_ids
    assert binding.child_object_hashes == (
        _fake_hash(root.A_plus[1][1]),
        _fake_hash(root.A_plus[2][1]),
    )
    assert binding.root_object_hash == _fake_hash(root)
    assert lint_fork_topology(
        root,
        envelope=declaration.envelope,
        authorization=declaration.authorization,
        binding=binding,
    ) == binding


def test_complete_recursive_lint_accepts_every_declared_fork() -> None:
    nested = _root_with_two_children()
    root = FakeUCNSObject(
        (
            (Fraction(0, 1), nested),
            (Fraction(1, 1), _leaf(1)),
        )
    )
    assert enumerate_payload_fork_paths(root) == ((), (0,))
    outer = _declaration(root, children=("metapat.nested", "metapat.leaf"))
    inner = _declaration(root, path=(0,))
    report = lint_all_payload_forks(root, (outer, inner))
    assert report.valid is True
    assert report.fork_paths == ((), (0,))


def test_missing_duplicate_and_extra_declarations_fail_closed() -> None:
    nested = _root_with_two_children()
    root = FakeUCNSObject(((Fraction(0, 1), nested), (Fraction(1, 1), _leaf(1))))
    outer = _declaration(root, children=("metapat.nested", "metapat.leaf"))
    inner = _declaration(root, path=(0,))
    with pytest.raises(ForkTopologyError, match="missing"):
        lint_all_payload_forks(root, (outer,))
    with pytest.raises(ForkTopologyError, match="duplicate"):
        lint_all_payload_forks(root, (outer, inner, inner))

    leaf_root = _leaf(0)
    with pytest.raises(ForkTopologyError, match="non-fork"):
        lint_all_payload_forks(leaf_root, (outer,))


def test_payload_order_or_object_drift_fails_closed() -> None:
    root = _root_with_two_children()
    declaration = _declaration(root)
    reversed_root = FakeUCNSObject(
        (
            root.A_plus[0],
            root.A_plus[2],
            root.A_plus[1],
        )
    )
    with pytest.raises(ForkTopologyError, match="root_object_hash"):
        lint_fork_topology(
            reversed_root,
            envelope=declaration.envelope,
            authorization=declaration.authorization,
            binding=declaration.binding,
        )

    with pytest.raises(ForkTopologyError, match="binding_digest mismatch"):
        replace(
            declaration.binding,
            child_object_hashes=tuple(reversed(declaration.binding.child_object_hashes)),
        )


def test_single_payload_is_not_silently_typed_as_a_fork() -> None:
    root = FakeUCNSObject(((Fraction(0, 1), None), (Fraction(1, 1), _leaf(0))))
    assert enumerate_payload_fork_paths(root) == ()
    report = lint_all_payload_forks(root, ())
    assert report.valid is True
    with pytest.raises(ForkTopologyError, match="not a payload fork"):
        _, authorization = _authorization()
        build_fork_topology_binding(root, authorization)


def test_binding_roundtrip_is_strict_and_tamper_evident() -> None:
    binding = _declaration(_root_with_two_children()).binding
    reconstructed = UCNSForkTopologyBinding.from_json(binding.to_json())
    assert reconstructed == binding

    unknown = binding.to_dict()
    unknown["external_edge_id"] = "provenance://not-containment"
    with pytest.raises(ForkTopologyError, match="unknown"):
        UCNSForkTopologyBinding.from_dict(unknown)

    tampered = binding.to_dict()
    tampered["payload_cell_indices"] = [2, 1]
    with pytest.raises(ForkTopologyError):
        UCNSForkTopologyBinding.from_dict(tampered)


def test_valid_report_preserves_status_firewall() -> None:
    root = _root_with_two_children()
    declaration = _declaration(root)
    report = lint_all_payload_forks(root, (declaration,))
    assert declaration.binding.theorem_status_transfer is False
    assert declaration.binding.measurement_validity_claim is False
    assert report.theorem_status_transfer is False
    assert report.measurement_validity_claim is False


def test_direct_dependency_absence_is_typed(monkeypatch) -> None:
    monkeypatch.delitem(sys.modules, "ucns", raising=False)
    real_import = importlib.import_module

    def missing(name, package=None):
        if name == "ucns":
            raise ModuleNotFoundError("No module named 'ucns'", name="ucns")
        return real_import(name, package)

    monkeypatch.setattr("edcm.ucns_fork_lint.importlib.import_module", missing)
    with pytest.raises(ForkLintDependencyError):
        enumerate_payload_fork_paths(_leaf(0))


def test_actual_full_stack_fixture_when_dependencies_are_installed(monkeypatch) -> None:
    """Runs only in EDCM's pinned full-stack CI job."""

    monkeypatch.undo()
    ucns = pytest.importorskip("ucns")
    metapat = pytest.importorskip("metapat")
    if not hasattr(metapat, "authorize_constitutive_fork"):
        pytest.skip("requires METAPAT Phi authorization producer")

    child_a = ucns.UCNSObject(1, 1, [(Fraction(0, 1), None)], [0])
    child_b = ucns.UCNSObject(1, 1, [(Fraction(0, 1), None)], [1])
    root = ucns.UCNSObject(
        2,
        2,
        [(Fraction(0, 1), child_a), (Fraction(1, 1), child_b)],
        [0, 1],
    )
    envelope = metapat.root_spine_module_envelope()
    authorization = metapat.authorize_constitutive_fork(
        envelope,
        child_module_ids=("metapat.child.alpha", "metapat.child.beta"),
        source_statement_refs=(envelope.source_statement_refs[0],),
    )
    binding = build_fork_topology_binding(root, authorization)
    report = lint_all_payload_forks(
        root,
        (AuthorizedUCNSFork(envelope, authorization, binding),),
    )
    assert report.valid is True
    assert report.fork_paths == ((),)
