from types import SimpleNamespace
import pytest

from edcm.semantic_metric_space import VECTOR_ORDER, build_semantic_metric_space, bind_round_metrics

def _origins():
    out={}
    for metric in VECTOR_ORDER:
        closed=metric not in {"O","L"}
        out[metric]={
            "schema":"english-gonol.edcm-metric-origin-set",
            "version":"0.1.0","metric_id":metric,
            "receipt_sha256":(metric[0].lower() if metric!="kappa" else "k")*64,
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
