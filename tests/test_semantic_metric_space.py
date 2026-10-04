from hashlib import sha256
from types import SimpleNamespace

from edcm.metric_origin_spec import metric_origin_spec
import pytest

from edcm.semantic_metric_space import VECTOR_ORDER, build_semantic_metric_space, bind_round_metrics

def _origins():
    out={}
    for metric in VECTOR_ORDER:
        spec=metric_origin_spec(metric)
        out[metric]={
            "schema":"english-gonol.edcm-metric-origin-set",
            "version":"0.2.0","metric_id":spec.canonical_metric_id,
            "origin_id":f"O_M({spec.canonical_metric_id})",
            "receipt_sha256":sha256(spec.canonical_metric_id.encode()).hexdigest(),
            "closed":True,
            "unresolved":list(spec.unresolved),
        }
    return out

def test_space_preserves_vector_order_and_canonical_targets():
    space=build_semantic_metric_space(_origins())
    assert tuple(x.metric_id for x in space.bindings)==VECTOR_ORDER
    assert space.complete is True
    assert space.unresolved_metrics==()
    assert next(x for x in space.bindings if x.metric_id=="O").canonical_metric_id=="edcm.behavioral.O_scope"
    assert next(x for x in space.bindings if x.metric_id=="L").canonical_metric_id=="edcm.behavioral.L_loss"

def test_scalar_readout_is_bound_but_semantic_projection_stays_hmmm():
    values={name:0.1 for name in VECTOR_ORDER}
    metrics=SimpleNamespace(**values)
    space=build_semantic_metric_space(_origins())
    rows=bind_round_metrics(metrics,space,evidence_receipt="evidence:1")
    assert len(rows)==11
    assert all(row.semantic_projection=="hmmm" for row in rows)
    assert all(row.evidence_receipt=="evidence:1" for row in rows)
    assert rows[0].value==0.1
    assert rows[0].origin_id=="O_M(edcm.behavioral.C.constraint_strain)"

def test_origin_identity_mismatch_fails_closed():
    origins=_origins()
    origins["C"]["metric_id"]="edcm.behavioral.R.refusal_density"
    with pytest.raises(ValueError,match="identity mismatch"):
        build_semantic_metric_space(origins)

def test_vector_order_is_not_silently_reordered():
    origins=_origins()
    reversed_origins=dict(reversed(list(origins.items())))
    with pytest.raises(ValueError,match="exact EDCM vector order"):
        build_semantic_metric_space(reversed_origins)


def test_edcm_conflicts_and_proxy_limits_survive_stack_omission():
    space = build_semantic_metric_space(_origins())
    for binding in space.bindings:
        assert set(metric_origin_spec(binding.metric_id).unresolved) <= set(binding.unresolved)


@pytest.mark.parametrize("identity", [None, "", " ", "O_M(R)", 123])
def test_invalid_origin_identity_fails_closed(identity):
    origins = _origins()
    origins["C"]["origin_id"] = identity
    with pytest.raises(ValueError, match="origin identity mismatch"):
        build_semantic_metric_space(origins)


@pytest.mark.parametrize("digest", ["z" * 64, "a" * 63, "a" * 65, " " * 64, None])
def test_malformed_receipt_fails_closed(digest):
    origins = _origins()
    origins["C"]["receipt_sha256"] = digest
    with pytest.raises(ValueError, match="invalid origin receipt"):
        build_semantic_metric_space(origins)


@pytest.mark.parametrize("reasons", [[], [""], [" "], [None], "reason"])
def test_unclosed_origins_need_nonblank_reasons(reasons):
    origins = _origins()
    origins["C"].update(closed=False, unresolved=reasons)
    with pytest.raises(ValueError, match="unresolved"):
        build_semantic_metric_space(origins)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), 10**400])
def test_nonfinite_readouts_fail_before_binding(value):
    metrics = SimpleNamespace(**{name: 0.1 for name in VECTOR_ORDER})
    metrics.C = value
    with pytest.raises(ValueError, match="finite scalar"):
        bind_round_metrics(metrics, build_semantic_metric_space(_origins()), evidence_receipt="evidence:1")


def test_documented_example_executes_with_maintained_metrics():
    from pathlib import Path
    document = (Path(__file__).parents[1] / "docs/semantic-metric-space.md").read_text()
    code = document.split("```python\n", 1)[1].split("```", 1)[0]
    exec(compile(code, "docs/semantic-metric-space.md", "exec"), {})


@pytest.mark.parametrize("field,value", [
    ("origin_id", "evil"), ("origin_receipt_sha256", "z"),
    ("closed", "yes"), ("unresolved", ()), ("unresolved", []),
])
def test_direct_bindings_cannot_bypass_admission(field, value):
    from dataclasses import replace
    space = build_semantic_metric_space(_origins())
    malformed = replace(space.bindings[0], **{field: value})
    space = replace(space, bindings=(malformed, *space.bindings[1:]))
    metrics = SimpleNamespace(**{name: 0.1 for name in VECTOR_ORDER})
    with pytest.raises(ValueError):
        bind_round_metrics(metrics, space, evidence_receipt="evidence:1")


@pytest.mark.parametrize("mutation", ["empty", "partial", "duplicate", "reversed", "complete", "unresolved", "canonical_O"])
def test_direct_space_cannot_bypass_vector_and_closure_rules(mutation):
    from dataclasses import replace
    space = build_semantic_metric_space(_origins())
    if mutation == "empty":
        space = replace(space, bindings=())
    elif mutation == "partial":
        space = replace(space, bindings=space.bindings[:1])
    elif mutation == "duplicate":
        space = replace(space, bindings=(space.bindings[1], *space.bindings[1:]))
    elif mutation == "reversed":
        space = replace(space, bindings=tuple(reversed(space.bindings)))
    elif mutation == "complete":
        space = replace(space, complete=False)
    elif mutation == "unresolved":
        space = replace(space, unresolved_metrics=("O",))
    else:
        space = replace(space, bindings=tuple(replace(b, canonical_metric_id="edcm.behavioral.O_confidence") if b.metric_id == "O" else b for b in space.bindings))
    with pytest.raises(ValueError):
        bind_round_metrics(SimpleNamespace(**{name: 0.1 for name in VECTOR_ORDER}), space, evidence_receipt="evidence:1")


@pytest.mark.parametrize("metric", VECTOR_ORDER)
@pytest.mark.parametrize("side", ["below", "above"])
def test_metric_domains_are_enforced(metric, side):
    metrics = SimpleNamespace(**{name: 0.1 for name in VECTOR_ORDER})
    setattr(metrics, metric, (-1.01 if metric == "O" else -0.01) if side == "below" else 1.01)
    with pytest.raises(ValueError, match="outside"):
        bind_round_metrics(metrics, build_semantic_metric_space(_origins()), evidence_receipt="evidence:1")


@pytest.mark.parametrize("edge", ["lower", "upper"])
def test_metric_domain_endpoints_are_preserved(edge):
    values = {name: (1.0 if edge == "upper" else (-1.0 if name == "O" else 0.0)) for name in VECTOR_ORDER}
    rows = bind_round_metrics(SimpleNamespace(**values), build_semantic_metric_space(_origins()), evidence_receipt="evidence:1")
    assert [row.value for row in rows] == list(values.values())
