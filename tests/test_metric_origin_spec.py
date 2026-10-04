from edcm.metric_origin_spec import METRIC_ORIGIN_SPECS, metric_origin_spec

def test_complete_round_metric_origin_inventory():
    assert tuple(METRIC_ORIGIN_SPECS) == ("C","R","F","E","D","N","I","O","L","P","kappa")

def test_words_define_instrument_not_observation():
    for key in ("C","R","F","E","D","N","I","P","kappa"):
        spec = metric_origin_spec(key)
        assert spec.standing == "resolved"
        assert spec.surface_terms
        assert spec.defining_statement
        assert spec.formula_or_rule

def test_existing_semantic_collisions_fail_closed():
    assert metric_origin_spec("O").standing == "hmmm"
    assert metric_origin_spec("L").standing == "hmmm"
    assert "Overextension" in metric_origin_spec("O").surface_terms
    assert "Overconfidence" in metric_origin_spec("O").surface_terms
    assert "Load" in metric_origin_spec("L").surface_terms
    assert "Coherence Loss" in metric_origin_spec("L").surface_terms

def test_unknown_metric_fails_closed():
    try:
        metric_origin_spec("X")
    except KeyError:
        pass
    else:
        raise AssertionError("unknown metric origin must fail closed")
