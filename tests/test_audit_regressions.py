"""Regression witnesses for the 2026-09-17 audit.

Usage: python -m pytest -q tests/test_audit_regressions.py
Base-mode cases always run; installed producer cases require the full-stack extra.
"""

import hashlib
import json

import pytest

import edcm.layers as layers_module
from edcm import compute_transcript, parse_transcript
from edcm.edcmucns import PolicyManifest
from edcm.measurement import compress
from edcm.metapat_adapter import MetapatAdapterSelection, missing_metapat_status
from edcm.shared_stack import build_result_contract
from edcm.ucns_adapter import REJECTED_LEGACY_INPUTS, UCNSAdapterSelection, missing_ucns_status


@pytest.fixture(params=["base", "full-stack"])
def pipeline(request, monkeypatch):
    if request.param == "base":
        monkeypatch.setattr(layers_module, "select_metapat_adapter", lambda: MetapatAdapterSelection(None, missing_metapat_status()))
        monkeypatch.setattr(layers_module, "select_ucns_adapter", lambda: UCNSAdapterSelection(None, missing_ucns_status()))
    else:
        pytest.importorskip("metapat")
        pytest.importorskip("ucns")
    return layers_module.build_default_layers()


def test_multiline_refusal_is_retained_and_measured():
    plain = "A: Here is the plan.\nB: Accepted."
    source = "A: Here is the plan.\nI cannot do this.\nB: Accepted."
    parsed = parse_transcript(source)
    assert "I cannot do this." in parsed.turns[0].text
    assert parsed.source_text == source
    assert compute_transcript(parsed)[0].token_count > compute_transcript(parse_transcript(plain))[0].token_count
    assert compute_transcript(parsed)[0].vector() != compute_transcript(parse_transcript(plain))[0].vector()


def test_mixed_speaker_formats_and_preamble_keep_every_turn():
    source = "Context before labels.\r\n**A**: first\r\nB: second\r\n[A]: third\r\nB (assistant): fourth"
    parsed = parse_transcript(source)
    assert [t.speaker for t in parsed.turns] == ["SPEAKER", "A", "B", "A", "B"]
    assert [t.text.strip() for t in parsed.turns] == ["Context before labels.", "first", "second", "third", "fourth"]
    assert parsed.source_text == source


def test_empty_speaker_line_does_not_consume_next_speaker():
    parsed = parse_transcript("A:\nB: hello\ncontinued")
    assert [t.speaker for t in parsed.turns] == ["A", "B"]
    assert "continued" in parsed.turns[1].text


@pytest.mark.parametrize("field", ["rounds", "agent_metrics", "alerts", "structural_density", "measurement_computed", "layer_provenance", "edcm_result", "ucns_geometry"])
def test_public_pipeline_rejects_output_fields(pipeline, field):
    with pytest.raises(ValueError, match="output-only"):
        pipeline.run({field: []})


@pytest.mark.parametrize("field", sorted(REJECTED_LEGACY_INPUTS))
def test_retired_inputs_fail_in_all_modes(pipeline, field):
    with pytest.raises(ValueError, match="retired"):
        pipeline.run({field: {"made_up": True}})


def test_direct_measurement_clears_stale_outputs():
    state = layers_module.ConsolidatedMeasurementLayer().measure({"rounds": [{"P": 1}], "measurement_computed": True})
    assert "rounds" not in state
    contract = build_result_contract(state, PolicyManifest())
    assert contract.readouts["state"] == "NA"


def test_result_builder_does_not_infer_execution_from_rounds():
    contract = build_result_contract({"rounds": [{"P": 1}]}, PolicyManifest())
    assert contract.readouts["state"] == "NA"


@pytest.mark.parametrize("field", ["ucns_geometry", "ucns_factorization_evidence"])
def test_result_builder_rejects_unsupported_evidence(field):
    with pytest.raises(ValueError, match="unsupported"):
        build_result_contract({field: {"claim": "arbitrary"}}, PolicyManifest())


def test_result_identity_binds_every_emitted_compartment(pipeline):
    contract = pipeline.run({"transcript": "A: Here is the plan.\nB: Accepted."})["edcm_result"]
    identity = contract.pop("result_identity")
    def digest(value):
        return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()
    assert identity == digest(contract)
    for field in contract:
        changed = {**contract, field: {"changed": True}}
        assert digest(changed) != identity, field


@pytest.mark.parametrize("damage", ["missing_projection", "nan", "wrong_index", "source_absent"])
def test_result_builder_rejects_incomplete_measurements(pipeline, damage):
    state = pipeline.run({"transcript": "A: Here is the plan.\nB: Accepted."})
    if damage == "missing_projection":
        state["agent_metrics"] = []
    elif damage == "nan":
        state["rounds"][0]["P"] = float("nan")
    elif damage == "wrong_index":
        state["rounds"][0]["round_index"] = 9
    else:
        state.pop("transcript")
    with pytest.raises(ValueError, match="measurement"):
        build_result_contract(state, PolicyManifest())


def test_codec_preserves_source_and_every_token_field():
    source = " **A**: here’s  a plan\r\nA: here is the plan.\r\nB: Accepted.\n"
    parsed = parse_transcript(source)
    metrics = compute_transcript(parsed)
    restored, restored_metrics = compress.from_bytes(compress.to_bytes(parsed, metrics))
    assert restored.source_text == source
    assert [(t.speaker, t.text) for t in restored.turns] == [(t.speaker, t.text) for t in parsed.turns]
    for before, after in zip(parsed.turns, restored.turns, strict=True):
        for original, decoded in zip(before.tokens, after.tokens, strict=True):
            assert type(decoded) is type(original)
            for field in original.__slots__:
                assert getattr(decoded, field) == getattr(original, field)
    assert [m.as_dict() for m in restored_metrics] == [m.as_dict() for m in metrics]


def test_codec_refuses_unversioned_or_historical_lossy_payloads():
    for version in (None, 1, 99):
        with pytest.raises(ValueError, match="version"):
            compress.decode({"v": version, "rounds": []})


def test_codec_refuses_partial_metric_lists():
    parsed = parse_transcript("A: first\nB: second\nA: third")
    with pytest.raises(ValueError, match="metrics"):
        compress.encode(parsed, compute_transcript(parsed)[:1])


@pytest.mark.parametrize("ending", ["\n", "\r\n", "\r"])
def test_turn_delimiters_do_not_create_order_signals(ending):
    left = parse_transcript(f"A: first{ending}B: second")
    right = parse_transcript(f"B: second{ending}A: first{ending}")
    assert sorted((t.speaker, t.text) for t in left.turns) == sorted((t.speaker, t.text) for t in right.turns)
    source = f"A: first{ending}continued{ending}{ending}B: second{ending}"
    parsed = parse_transcript(source)
    assert [t.text for t in parsed.turns] == [f"first{ending}continued{ending}", "second"]
    assert parsed.source_text == source
