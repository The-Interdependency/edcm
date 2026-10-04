import operator
import pytest

from edcm.metric_origin_spec import CANONICAL_SPLIT_IDS, LEGACY_CARRIER_TARGETS, METRIC_ORIGIN_SPECS, MetricOriginSpec, metric_origin_spec

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

def test_legacy_o_l_carriers_have_explicit_canonical_targets():
    assert metric_origin_spec("O").standing == "resolved"
    assert metric_origin_spec("L").standing == "resolved"
    assert metric_origin_spec("O").canonical_metric_id == "edcm.behavioral.O_confidence"
    assert metric_origin_spec("L").canonical_metric_id == "edcm.behavioral.L_loss"
    assert LEGACY_CARRIER_TARGETS == {
        "O": "edcm.behavioral.O_confidence",
        "L": "edcm.behavioral.L_loss",
    }

def test_o_l_split_identities_remain_distinct():
    assert CANONICAL_SPLIT_IDS == (
        "edcm.behavioral.O_scope",
        "edcm.behavioral.O_confidence",
        "edcm.behavioral.L_load",
        "edcm.behavioral.L_loss",
        "edcm.behavioral.L_resistance",
    )

def test_registry_is_read_only():
    with pytest.raises(TypeError):
        operator.setitem(METRIC_ORIGIN_SPECS,"C",metric_origin_spec("R"))

@pytest.mark.parametrize("reason", ["", " ", None])
def test_blank_hmmm_reason_is_rejected(reason):
    with pytest.raises(ValueError, match="non-empty"):
        MetricOriginSpec(
            metric_id="X", canonical_metric_id="edcm.behavioral.X", surface_terms=("x",), construction_terms=(),
            semantic_definition="definition", declared_rule="declared",
            implemented_rule="implemented", source_refs=("source",),
            standing="hmmm", measurement_alignment="hmmm", unresolved=(reason,),
        )

def test_refusal_proxy_does_not_claim_constraint_statement_denominator():
    spec=metric_origin_spec("R")
    assert "token count" in spec.implemented_rule
    assert any("denominator" in item for item in spec.unresolved)

def test_unknown_metric_fails_closed():
    with pytest.raises(KeyError):
        metric_origin_spec("X")
