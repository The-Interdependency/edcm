from hashlib import sha256
from types import SimpleNamespace

from edcm.metric_origin_spec import metric_origin_spec
import pytest

from edcm.semantic_metric_space import VECTOR_ORDER, build_semantic_metric_space, bind_round_metrics

def _origins():
    out={}
    for metric in VECTOR_ORDER:
        closed=metric not in {"O","L"}
        out[metric]={
            "schema":"english-gonol.edcm-metric-origin-set",
            "version":"0.2.0","metric_id":metric,"origin_id":f"O_M({metric})",
            "receipt_sha256":sha256(metric.encode()).hexdigest(),
            "closed":closed,
            "unresolved":[] if closed else ["source semantic collision"],
        }
    return out

def test_space_preserves_vector_order_and_hmmm():
    space=build_semantic_metric_space(_origins())
    assert tuple(x.metric_id for x in space.bindings)==VECTOR_ORDER
    assert space.complete is False
    assert space.unresolved_metrics==("O","L")

def test_scalar_readout_is_bound_but_semantic_projection_stays_hmmm():
    values={name:0.1 for name in VECTOR_ORDER}
    metrics=SimpleNamespace(**values)
    space=build_semantic_metric_space(_origins())
    rows=bind_round_metrics(metrics,space,evidence_receipt="evidence:1")
    assert len(rows)==11
    assert all(row.semantic_projection=="hmmm" for row in rows)
    assert all(row.evidence_receipt=="evidence:1" for row in rows)
    assert rows[0].value==0.1
    assert rows[0].origin_id=="O_M(C)"

def test_origin_identity_mismatch_fails_closed():
    origins=_origins()
    origins["C"]["metric_id"]="R"
    with pytest.raises(ValueError,match="identity mismatch"):
        build_semantic_metric_space(origins)

def test_vector_order_is_not_silently_reordered():
    origins=_origins()
    reversed_origins=dict(reversed(list(origins.items())))
    with pytest.raises(ValueError,match="exact EDCM vector order"):
        build_semantic_metric_space(reversed_origins)


@pytest.mark.parametrize("metric", ["O", "L"])
def test_stack_closure_cannot_resolve_edcm_semantics(metric):
    origins = _origins()
    origins[metric].update(closed=True, unresolved=[])
    with pytest.raises(ValueError, match="EDCM semantic origin remains hmmm"):
        build_semantic_metric_space(origins)


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
