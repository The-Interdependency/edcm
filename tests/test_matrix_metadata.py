"""Regression coverage for the matrix module's executable witness reference."""

from __future__ import annotations

import ast
from pathlib import Path

from tools.check_metadata_contracts import parse_module_build, verify_test_references


def test_scope_matrix_metadata_resolves_declared_witness():
    root = Path(__file__).resolve().parents[1]
    matrix_path = root / "edcm/measurement/metrics/matrix.py"
    _, fields, findings = parse_module_build(matrix_path)
    assert not findings

    reference = fields["tests"]
    assert not verify_test_references(matrix_path, reference, root)
    test_path, separator, test_name = reference.partition("::")
    assert separator, "matrix metadata must identify the exact scope witness"
    assert test_path == "tests/test_measurement.py"
    assert test_name == "test_scope_matrix_matches_canon_and_compute"
    tree = ast.parse((root / test_path).read_text(encoding="utf-8"))
    assert any(
        isinstance(node, ast.FunctionDef) and node.name == test_name
        for node in tree.body
    )
