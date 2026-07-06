"""Consolidation tests for edcm.measurement (the edcmbone mirror).

Covers the full deterministic pipeline (parse -> compute -> project ->
compress), the layers-bootstrap wiring, and the no-fork guarantee that the
mirror's orthogonality surface is edcm.ucns_objects itself.
"""

from __future__ import annotations

import edcm
from edcm import build_default_layers
from edcm.layers import ConsolidatedMeasurementLayer
from edcm.measurement import (
    AgentMetrics,
    CanonLoader,
    RoundMetrics,
    compute_transcript,
    fire_alerts,
    parse_transcript,
    project_transcript,
)
from edcm.measurement import compress as codec

TRANSCRIPT = """A: We need to decide this now. Do you agree?
B: I can't. Not like that. Why are we rushing?
A: Because if we don't, it will fail.
B: Okay. But only if we define the scope.
A: Agreed. Let's define scope and thresholds.
B: Also: I won't accept semantic inference in Operator.
A: Understood. Bones-only stays bones-only."""


def _pipeline():
    canon = CanonLoader()
    parsed = parse_transcript(TRANSCRIPT, canon=canon)
    metrics = compute_transcript(parsed, canon=canon)
    return canon, parsed, metrics


def test_pipeline_end_to_end():
    _, parsed, metrics = _pipeline()
    assert len(parsed.rounds) > 0
    assert len(metrics) == len(parsed.rounds)
    assert all(isinstance(m, RoundMetrics) for m in metrics)

    projections = project_transcript(parsed, metrics)
    assert len(projections) == len(metrics)
    assert all(isinstance(p, AgentMetrics) for p in projections)
    for p in projections:
        for name in ("CM", "DA", "DRIFT", "DVG", "INT", "TBF"):
            v = getattr(p, name)
            assert 0.0 <= v <= 1.0, f"{name} out of [0, 1]: {v}"
        assert isinstance(fire_alerts(p), list)


def test_compress_roundtrip_and_structural_density():
    _, parsed, metrics = _pipeline()
    blob = codec.to_bytes(parsed, metrics)
    parsed2, metrics2 = codec.from_bytes(blob)
    assert len(parsed2.rounds) == len(parsed.rounds)
    assert len(metrics2) == len(metrics)

    stats = codec.compression_stats(TRANSCRIPT, blob, parsed)
    # F (structural density) is a ratio readout.
    assert 0.0 <= stats["structural_density"] <= 1.0


def test_canon_loader_lookups():
    canon = CanonLoader()
    assert canon.lookup_word("not") is not None
    assert canon.lookup_punct("?") is not None
    assert set("CRDN").issubset(set(canon.metric_names()))


def test_orthogonality_surface_is_not_forked():
    # The mirror must re-export edcm.ucns_objects, not carry a second copy.
    from edcm.measurement.metrics import AxisState, ConstraintField, FieldMotion

    assert AxisState is edcm.ucns_objects.AxisState
    assert ConstraintField is edcm.ucns_objects.ConstraintField
    assert FieldMotion is edcm.ucns_objects.FieldMotion


def test_build_default_layers_uses_consolidated_measurement():
    layers = build_default_layers()
    # Without an installed upstream edcmbone exposing MeasurementLayer, the
    # consolidated mirror provides the measurement layer.
    assert isinstance(layers.measurement, ConsolidatedMeasurementLayer)

    result = layers.run({"transcript": TRANSCRIPT})
    assert result["measurement"] == "edcm.measurement"
    assert len(result["rounds"]) == len(result["agent_metrics"]) > 0
    assert len(result["alerts"]) == len(result["agent_metrics"])
    assert 0.0 <= result["structural_density"] <= 1.0


def test_layers_passthrough_without_transcript():
    result = build_default_layers().run({"input": "example"})
    assert result["measurement"] == "edcm.measurement"
    assert "rounds" not in result


def test_public_api_reexports():
    for name in (
        "measurement", "ConsolidatedMeasurementLayer", "CanonLoader",
        "parse_transcript", "ParsedTranscript", "compute_transcript",
        "RoundMetrics", "project_transcript", "AgentMetrics", "fire_alerts",
    ):
        assert name in edcm.__all__, f"{name} missing from edcm.__all__"
        assert hasattr(edcm, name)
