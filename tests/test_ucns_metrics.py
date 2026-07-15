"""Tests for canonical UCNS audit objects built from EDCM metric values."""

from __future__ import annotations

import hashlib
import json
import sys
import types

import pytest

from edcm.ucns_metrics import (
    METRIC_DEFINITIONS,
    RESOLVED_METRICS_SCHEMA_ID,
    ROUND_METRIC_FIELDS,
    UCNSMetricDependencyError,
    resolve_metric_axis,
    resolve_metric_value,
    resolve_metric_vector,
    resolve_round_metrics,
    resolved_metric_objects_payload,
)


class _FakeUCNSObject:
    def __init__(self, value):
        self.value = value


@pytest.fixture
def fake_ucns(monkeypatch):
    module = types.ModuleType("ucns")
    module.UCNSObject = _FakeUCNSObject
    module.recursive_encode = lambda value: _FakeUCNSObject(value)
    module.stable_hash = lambda obj: hashlib.sha256(
        json.dumps(obj.value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    monkeypatch.setitem(sys.modules, "ucns", module)
    return module


def _record_dict(resolved):
    return dict(resolved.record)


def test_progress_and_kappa_are_not_ucns_g_primitives():
    assert METRIC_DEFINITIONS["round:P_progress"].ucns_g_axis is None
    assert METRIC_DEFINITIONS["state:kappa"].ucns_g_axis is None


def test_dependency_absence_is_typed(monkeypatch):
    monkeypatch.delitem(sys.modules, "ucns", raising=False)

    real_import = __import__("importlib").import_module

    def missing(name, package=None):
        if name == "ucns":
            raise ModuleNotFoundError("No module named 'ucns'", name="ucns")
        return real_import(name, package)

    monkeypatch.setattr("edcm.ucns_metrics.importlib.import_module", missing)
    with pytest.raises(UCNSMetricDependencyError):
        resolve_metric_axis("behavioral:C")


def test_axis_identity_has_no_scalar_observation(fake_ucns):
    axis = resolve_metric_axis("behavioral:C")
    record = _record_dict(axis)
    assert axis.object_kind == "metric_axis"
    assert axis.value_num is None
    assert axis.value_den is None
    assert "value_num" not in record
    assert record["ucns_theorem_transfer"] is False


def test_same_observation_is_deterministic(fake_ucns):
    kwargs = {
        "grain": "round",
        "source": "RoundMetrics",
        "context_id": "round:7",
        "formula_version": "compute/1",
    }
    left = resolve_metric_value("behavioral:C", 0.3, **kwargs)
    right = resolve_metric_value("C", "0.300000", **kwargs)
    assert left.ucns_hash == right.ucns_hash
    assert (left.value_num, left.value_den) == (3, 10)


def test_changed_value_changes_hash(fake_ucns):
    kwargs = {"grain": "round", "source": "RoundMetrics"}
    left = resolve_metric_value("behavioral:C", 0.3, **kwargs)
    right = resolve_metric_value("behavioral:C", 0.4, **kwargs)
    assert left.ucns_hash != right.ucns_hash


def test_signed_o_preserves_sign_and_magnitude(fake_ucns):
    kwargs = {"grain": "round", "source": "RoundMetrics"}
    negative = resolve_metric_value("behavioral:O", -0.25, **kwargs)
    zero = resolve_metric_value("behavioral:O", 0, **kwargs)
    positive = resolve_metric_value("behavioral:O", 0.25, **kwargs)
    assert (negative.sign, negative.magnitude_num, negative.magnitude_den) == (-1, 1, 4)
    assert zero.sign == 0
    assert positive.sign == 1


def test_kappa_record_has_no_ucns_g_axis(fake_ucns):
    resolved = resolve_metric_value(
        "state:kappa", 0.4, grain="round", source="RoundMetrics"
    )
    assert _record_dict(resolved)["ucns_g_axis"] == ""


def test_vector_resolution_does_not_mutate_scalars(fake_ucns):
    scalars = {
        "C": 0.2,
        "R": 0.1,
        "F": 0.3,
        "E": 0.4,
        "D": 0.5,
        "N": 0.6,
        "I": 0.7,
        "O": -0.2,
        "L": 0.8,
        "P": 0.9,
        "kappa": 0.25,
    }
    before = dict(scalars)
    resolved = resolve_metric_vector(scalars, grain="round", source="RoundMetrics")
    assert scalars == before
    assert set(resolved) == {
        "behavioral:C",
        "behavioral:R",
        "behavioral:F",
        "behavioral:E",
        "behavioral:D",
        "behavioral:N",
        "behavioral:I",
        "behavioral:O",
        "behavioral:L",
        "round:P_progress",
        "state:kappa",
    }


def test_round_metrics_selects_only_metric_vector(fake_ucns):
    values = {name: 0.1 for name in ROUND_METRIC_FIELDS}
    values.update({"round_index": 12, "dissonance_energy": 0.9, "token_count": 100})
    resolved = resolve_round_metrics(values)
    assert len(resolved) == 11
    assert _record_dict(resolved["behavioral:C"])["context_id"] == "round:12"


def test_payload_is_adjacent_non_scoring_audit_data(fake_ucns):
    resolved = {
        "behavioral:C": resolve_metric_value(
            "behavioral:C", 0.2, grain="round", source="RoundMetrics"
        )
    }
    payload = resolved_metric_objects_payload(resolved)
    assert payload["schema_id"] == RESOLVED_METRICS_SCHEMA_ID
    assert payload["ucns_theorem_transfer"] is False
    assert payload["objects"]["behavioral:C"]["hash"] == resolved["behavioral:C"].ucns_hash
    assert "ucns_object" not in payload["objects"]["behavioral:C"]
