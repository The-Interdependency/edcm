import operator
import pytest

from edcm.metric_origin_spec import METRIC_ORIGIN_SPECS, MetricOriginSpec, metric_origin_spec

def test_complete_round_metric_origin_inventory():
    assert tuple(METRIC_ORIGIN_SPECS) == ("C","R","F","E","D","N","I","O","L","P","kappa")

def test_words_define_instrument_not_observation():
    for key in ("C","R","F","E","D","N","I","P","kappa"):
        spec = metric_origin_spec(key)
        assert spec.standing == "resolved"
        assert spec.surface_terms
        assert spec.semantic_definition
        assert spec.implemented_rule
        assert spec.measurement_alignment in {"aligned","proxy"}

def test_existing_semantic_collisions_fail_closed():
    assert metric_origin_spec("O").standing == "hmmm"
    assert metric_origin_spec("L").standing == "hmmm"
    assert metric_origin_spec("O").measurement_alignment == "conflict"
    assert metric_origin_spec("L").measurement_alignment == "conflict"

def test_registry_is_read_only():
    with pytest.raises(TypeError):
        operator.setitem(METRIC_ORIGIN_SPECS,"C",metric_origin_spec("R"))

def test_blank_hmmm_reason_is_rejected():
    with pytest.raises(ValueError, match="non-empty"):
        MetricOriginSpec("X",("x",),"definition","declared","implemented",("source",),
                         "hmmm","hmmm",("",))

def test_refusal_proxy_does_not_claim_constraint_statement_denominator():
    spec=metric_origin_spec("R")
    assert "token count" in spec.implemented_rule
    assert any("denominator" in item for item in spec.unresolved)

def test_unknown_metric_fails_closed():
    with pytest.raises(KeyError):
        metric_origin_spec("X")
