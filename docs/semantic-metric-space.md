# Semantic metric space — usage guidance

Install from this EDCM checkout with `python -m pip install -e '.[dev]'`.
The adapter binds maintained scalar measurements to externally constructed
metric origins. EDCM owns metric meanings; Stack owns the English construction.
O and L remain `hmmm`, including when a caller supplies a closed Stack record.

## Runnable adapter example

Run this Python block from the checkout. Its origin records are explicitly
synthetic adapter fixtures, **not verified Stack construction evidence**.
The transcript measurements use maintained `RoundMetrics`.

```python
from dataclasses import asdict
from hashlib import sha256
import json

from edcm.measurement import RoundMetrics, compute_transcript, parse_transcript
from edcm.metric_origin_spec import metric_origin_spec
from edcm.semantic_metric_space import (
    VECTOR_ORDER, build_semantic_metric_space, bind_round_metrics,
)

origins = {}
for metric_id in VECTOR_ORDER:
    spec = metric_origin_spec(metric_id)
    origins[metric_id] = {
        "schema": "english-gonol.edcm-metric-origin-set",
        "version": "0.2.0",
        "metric_id": metric_id,
        "origin_id": f"O_M({metric_id})",
        "receipt_sha256": sha256(f"synthetic-example:{metric_id}".encode()).hexdigest(),
        "closed": spec.standing == "resolved",
        "unresolved": list(spec.unresolved),
    }

text = "A: State the constraint.\nB: The constraint is recorded."
metrics = compute_transcript(parse_transcript(text))[0]
assert isinstance(metrics, RoundMetrics)
space = build_semantic_metric_space(origins)
rows = bind_round_metrics(
    metrics, space, evidence_receipt="sha256:" + sha256(text.encode()).hexdigest(),
)
assert space.unresolved_metrics == ("O", "L")
assert [row.value for row in rows] == metrics.vector()
assert all(row.semantic_projection == "hmmm" for row in rows)
print(json.dumps([asdict(row) for row in rows], allow_nan=False, indent=2))
```

## Stack integration

Use the dependent Stack metric-origin implementation at the exact commit
registered by its work graph. After replaying its full English construct,
export `build_metric_origin_set(state_dir, metric_id).to_dict()` for every
metric in `VECTOR_ORDER` into one ordered JSON object keyed by metric ID.
Supply that object to `build_semantic_metric_space` instead of the synthetic
`origins` above. Do not sort its keys: the declared EDCM vector order is required.

Each record must have the schema/version shown above, matching `metric_id`
and `origin_id`, a 64-character hexadecimal SHA-256 receipt, a boolean `closed`,
and an `unresolved` list of nonblank strings. An unclosed record requires at
least one reason. EDCM also carries its own conflicts and proxy limitations
forward even when the external record omits them. A record claiming closure
for an EDCM `hmmm` origin is rejected.

The adapter checks identity shape and EDCM authority boundaries. It does not
replay the Stack database, authenticate the producer, or verify the complete
Stack payload digest; those checks belong to the Stack construction/export
path. The evidence receipt identifies the independently measured transcript
or measurement artifact; origin words must never substitute for that evidence.
Non-finite values, booleans, and nonnumeric scalar values are rejected.
Values must also remain in the maintained metric domain: O in `[-1, 1]`,
all other components in `[0, 1]`. Binding revalidates the entire space,
including order, origin identities, receipts, EDCM constraints and completion
state; manually constructing the public dataclasses cannot bypass admission.

## hmmm

The lawful projection or distance from an observed construct to a semantic
origin remains unestablished. Bound scalars retain their maintained proxy
meaning; no semantic distance, empirical validity, diagnosis, or canon
selection follows from this adapter.

Verify the executable example and boundary regressions with:

```bash
python -m pytest -q tests/test_semantic_metric_space.py tests/test_metric_origin_spec.py
```
