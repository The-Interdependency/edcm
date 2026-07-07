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

## Consolidated measurement package (`edcm.measurement`)

The canonical edcmbone structural-measurement package is now consolidated here
as a dependency-free mirror (`edcm/measurement/`): canon data + `CanonLoader`,
the turns/rounds transcript parser, the metric stack (stats, risk, compute,
matrix, projection), the closed-token UCNS encoder, and the lossless codec
with `structural_density` (F) stats. Source of truth for L0 remains
`The-Interdependency/edcmbone`; provenance (path + commit SHA) is recorded in
`edcm/measurement/__init__.py` and `docs/consolidation-edcmbone.md`.

The measurement layer of the bootstrap now runs this pipeline for real:

```python
from edcm import build_default_layers

result = build_default_layers().run({"transcript": "A: We must decide now.\nB: No. Why rush?"})
result["rounds"]              # per-round metric vectors (C, R, F, E, D, N, I, O, L, P, kappa)
result["agent_metrics"]       # per-round CM/DA/DRIFT/DVG/INT/TBF projections
result["structural_density"]  # F readout from the lossless codec
```

Direct use of the consolidated surface:

```python
from edcm import CanonLoader, parse_transcript, compute_transcript, project_transcript

canon = CanonLoader()
parsed = parse_transcript(transcript, canon=canon)
metrics = compute_transcript(parsed, canon=canon)
agents = project_transcript(parsed, metrics)
```


## edcmucns (v0.3.1 architecture)

`edcm/edcmucns/` implements the **edcmucns design canon v0.3.1** — the
Energy–Dissonance Circuit Model on UCNS mathematics, with provenance as the
recurring theme (`docs/codex_edcmucns_v031_handoff.md`). Status: ratified as
architecture; frontier as empirical measurement. The identity layer ships:
policy-manifest hashing, provenance witnesses, the non-origin residue rule,
origin/bone mass and carrier helpers, a closed readout-scope registry, the
two equivalence tiers, the witness/geometry validator, SeqAppend
composition, and manifest-rotation epoch chains.

```python
from edcm.edcmucns import (
    BoneEvent, PolicyManifest, encode_turn,
    ucns_carrier_equivalent, edcm_measurement_equivalent,
)

manifest = PolicyManifest()          # P:3 K:5 Q:7 T:13 S:29, non_origin_residue_v031
turn = encode_turn("t1", "A", [BoneEvent("P", "not")], manifest)
edcm_measurement_equivalent(turn.window, turn.window, "operator_scope")  # True
```

- UCNS equivalence proves same geometry; EDCM equivalence additionally
  requires the in-scope provenance/payload hashes and the policy-manifest
  hash.
- No-bone turns are `AbsentOperatorGeometry` — NA for operator readouts,
  never 0.
- Frontier gates (contact convergence, DA_geom correlation, cadence
  admission from text) are explicit `NotImplementedError` surfaces with
  named falsifiers — no empirical claim is made.

## Energy falsifiability bridge

`edcm.falsifiability_bridge` consolidates the useful preservation idea from
**edcmbone** into the new energy-audit layer without making edcmbone a hard
runtime dependency. It compares whether falsifiability-bearing claims from an
input survive in an output and reports edcmbone-style F-loss labels such as
F1 deletion and F6 decorative preservation.

```python
from edcm import audit_falsifiability_preservation

result = audit_falsifiability_preservation(
    "The theory predicts a CMB power-spectrum excess at multipole l ≈ 10^4.",
    "The theory is elegant and coherent.",
)
print(result["possible_falsifiability_loss"])  # True
```

The bridge remains an audit of claim structure only: it does not validate
external physics, import UCNS-A proof status, or decide empirical truth.

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
