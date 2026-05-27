# edcm

This repository is the consolidation of:

- [`The-Interdependency/edcmbone`](https://github.com/The-Interdependency/edcmbone)
- [`erinepshovel-code/EDCM`](https://github.com/erinepshovel-code/EDCM)

It is intended to bring the structural measurement work from **edcmbone**
together with the application work from **EDCM** in one place.

## Four-layer bootstrap

A minimal executable four-layer bootstrap now exists in `edcm/layers.py`.

- **Semantics layer**: tries to import from `ucns` and falls back to a local default.
- **Measurement layer**: tries to import from `edcmbone` and falls back to a local default.
- **Composition layer**: local orchestration default.
- **Delivery layer**: local output default.

### Usage

```python
from edcm import build_default_layers

layers = build_default_layers()
result = layers.run({"input": "example"})
print(result)
```

This allows the repository to run today even before upstream package wiring is fully settled.

## UCNS metric construction objects

`edcm/ucns_objects.py` is a self-contained, dependency-free mirror of edcmbone's
UCNS construction layer for the v0.2 metric-orthogonality spec
(`The-Interdependency/edcmbone:docs/specs/edcm-ucns-metric-orthogonality-v0.2.md`).
Primary doctrine: **UCNS exists to construct EDCM metrics.**

- `AxisState` — signed ternary axis state where `NA != 0`.
- `ConstraintField` — state object; presence / contact / resolution readouts
  (R, D, I, L_resistance). An empty field yields `NA`, not `0`.
- `FieldMotion` — tangent object; F / E / O_scope motion readouts that share a
  parent transition hash but keep distinct axis ids.
- `canonical_axes()` — the §9 axis + §10 projection registry.

```python
from edcm import ConstraintField, FieldMotion

cf = ConstraintField(grain="round", raised_field_count=3, contact="against", resolution="open")
cf.contact_state()          # AxisState(enabled=True, s=-1, ...)
cf.behavioral_readouts()    # R/D/I/L_resistance MetricReadouts
```

> No UCNS-A theorem/proof status is transferred to EDCM, edcmbone, or UCNS-G by
> this code.
