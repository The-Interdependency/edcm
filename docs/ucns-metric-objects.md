# UCNS-resolved EDCM metric objects

## Purpose

`edcm.ucns_metrics` gives every supported EDCM metric axis and scalar observation a canonical UCNS audit identity. Existing EDCM formulas and scalar outputs remain unchanged.

No UCNS-A theorem/proof status is transferred to EDCM, edcmbone, or UCNS-G by this change.

The resolver produces two object kinds:

- `metric_axis`: stable identity for a namespaced EDCM metric definition;
- `metric_value`: one rationalized observation at a declared grain, source, context, and formula version.

## Install

The base EDCM package remains dependency-free. Install the optional UCNS integration before resolving objects:

```bash
python -m pip install -e ".[ucns]"
```

Direct absence of `ucns` raises `UCNSMetricDependencyError`. Transitive import failures and incomplete UCNS public surfaces remain visible errors rather than being treated as optional absence.

## Resolve one value

```python
from edcm.ucns_metrics import resolve_metric_value

resolved = resolve_metric_value(
    "behavioral:O",
    -0.25,
    grain="round",
    source="RoundMetrics",
    context_id="round:12",
    formula_version="edcm.measurement.metrics.compute/1",
)

assert resolved.sign == -1
assert (resolved.magnitude_num, resolved.magnitude_den) == (1, 4)
print(resolved.ucns_hash)
print(resolved.record_list())
```

Floats are converted through their decimal string and limited to a rational denominator of at most 1,000,000. Binary floating-point artifacts therefore do not become part of the UCNS identity.

## Resolve a complete `RoundMetrics` vector

```python
from edcm.ucns_metrics import (
    resolve_round_metrics,
    resolved_metric_objects_payload,
)

resolved = resolve_round_metrics(round_metrics)
audit_payload = resolved_metric_objects_payload(resolved)

output = {
    "metrics": round_metrics.as_dict(),
    "resolved_metric_objects": audit_payload,
}
```

`resolved_metric_objects` is adjacent, non-scoring audit data. The resolver does not mutate `round_metrics`, replace `RoundMetrics.as_dict()`, or feed UCNS hashes back into metric formulas.

## Namespace discipline

Canonical ids are:

```text
behavioral:C
behavioral:R
behavioral:F
behavioral:E
behavioral:D
behavioral:N
behavioral:I
behavioral:O
behavioral:L
round:P_progress
state:kappa
```

`round:P_progress` is not UCNS-G Operator `P`. `state:kappa` also has no UCNS-G primitive assignment. Both records therefore carry an empty `ucns_g_axis` field.

## Canonical record

A value object is encoded as an ordered list of pairs using `ucns.recursive_encode`, then addressed with `ucns.stable_hash`. Its record includes:

```text
schema and object kind
metric id, symbol, and name
source, grain, context id, and formula version
rational value numerator and denominator
sign and rational magnitude
range and optional UCNS-G axis
EXPERIMENTAL status
ucns_theorem_transfer = false
```

The live `UCNSObject` remains available on `ResolvedMetricUCNS.ucns_object`; JSON-facing output should use `to_payload()` or `resolved_metric_objects_payload()`, which emit the stable hash and canonical record without trying to serialize the live object.

## Limits

- The resolver does not establish metric correctness or empirical validity.
- It does not construct the formal UCNS-A ↔ UCNS-G theorem bridge.
- It does not assign a prime to Progress or κ.
- UCNS hashes provide canonical content identity, not cryptographic producer signatures or transport authentication.

## hmmm

The correct attachment point for automatically emitted resolved objects across every delivery surface remains a versioned result-contract decision. Until that schema migration is made, callers attach the payload explicitly beside scalar metrics.
