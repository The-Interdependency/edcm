# CLAUDE.md — edcm: EDCM (consolidation repository)

This file gives AI assistants context needed to work effectively in this repository.

---

## Overview

`edcm` is a Python package that consolidates two upstream projects into one place:

- [`The-Interdependency/edcmbone`](https://github.com/The-Interdependency/edcmbone) — the structural / measurement work.
- [`erinepshovel-code/EDCM`](https://github.com/erinepshovel-code/EDCM) — the application work.

The goal is to bring the structural measurement work from **edcmbone** together with the
application work from **EDCM** in a single repository. The repo is intentionally
dependency-free so it runs today, before upstream package wiring (`ucns`, `edcmbone`)
is fully settled.

| Property        | Value                                                              |
| --------------- | ------------------------------------------------------------------ |
| Language        | Python (developed and tested on 3.11)                              |
| Runtime deps    | None — standard library only                                       |
| Test framework  | `pytest`                                                           |
| Package version | Not declared (no `pyproject.toml`/`setup.py`)                      |
| License         | MPL-2.0 (root `LICENSE`; relicensed from MIT — weak copyleft)      |

There is **no** `pyproject.toml`, `setup.py`, `requirements.txt`, `Makefile`, CI workflow
(`.github/workflows`), `docs/` directory, or lint config in this repository. Do not invent
or reference any. The repo is used as a source tree imported directly (see `tests/conftest.py`).

---

## Repository layout

```
edcm/
├── README.md                  # Project intent, usage examples
├── edcm/                      # The package
│   ├── __init__.py            # Public API surface (re-exports from submodules)
│   ├── layers.py              # Four-layer EDCM bootstrap
│   └── ucns_objects.py        # UCNS metric construction objects (v0.2 spec mirror)
└── tests/
    ├── conftest.py            # Inserts repo root onto sys.path so `import edcm` works
    └── test_ucns_objects.py   # Tests for ucns_objects (9 tests)
```

Everything the package exposes is re-exported from `edcm/__init__.py`; prefer importing
from `edcm` directly (e.g. `from edcm import ConstraintField`).

---

## Build / test / lint / run

There is no build system. The package runs in place. `tests/conftest.py` prepends the
repository root to `sys.path`, so tests resolve `import edcm` without installation.

| Task           | Command                                  | Notes                                  |
| -------------- | ---------------------------------------- | -------------------------------------- |
| Run tests      | `python3 -m pytest -q`                   | From repo root. All 9 tests pass.      |
| Run one test   | `python3 -m pytest tests/test_ucns_objects.py::test_field_motion_fixture_matrix` | |
| Try the bootstrap | `python3 -c "from edcm import build_default_layers; print(build_default_layers().run({'input': 'example'}))"` | |

There is no configured linter or formatter. The existing code uses `from __future__ import
annotations`, `@dataclass` (with `slots=True`/`frozen=True`), and PEP 604 / typing-style
annotations; match that style.

---

## Architecture & key concepts

The package has two independent pieces.

### 1. Four-layer bootstrap (`edcm/layers.py`)

A minimal, executable pipeline of four layers. Each layer is a `Protocol`, paired with a
`Default*Layer` implementation, and assembled into the `EDCMLayers` dataclass.

| Layer         | Protocol method | Role                                   | External source |
| ------------- | --------------- | -------------------------------------- | --------------- |
| Semantics     | `normalize`     | concept / ontology handling            | `ucns`          |
| Measurement   | `measure`       | structure / measurement                | `edcmbone`      |
| Composition   | `compose`       | cross-layer orchestration              | local default   |
| Delivery      | `deliver`       | application output                     | local default   |

`EDCMLayers.run(payload)` threads the payload through `normalize → measure → compose →
deliver`. `build_default_layers()` tries to import a `SemanticsLayer` from `ucns` and a
`MeasurementLayer` from `edcmbone`; if those packages are absent (the import is wrapped in
`try/except`), it silently falls back to the local default layers. This is what lets the
repo run before upstream wiring exists.

### 2. UCNS metric construction objects (`edcm/ucns_objects.py`)

A self-contained, dependency-free mirror of edcmbone's UCNS construction layer for the
**v0.2 metric-orthogonality spec** (`The-Interdependency/edcmbone:
docs/specs/edcm-ucns-metric-orthogonality-v0.2.md`; upstream source mirrored from
`backend/src/edcmbone/metrics/orthogonality.py`).

Primary doctrine: **UCNS exists to construct EDCM metrics.**

Core types:

- `AxisState` — signed ternary axis state. **Key invariant (spec §1): `NA != 0`.** `NA`
  is `enabled=False` (a disabled readout, required field/context absent); `0` is a real,
  enabled, neutral state. Enabled states require `s ∈ {-1, 0, +1}` and `m ∈ [0, 1]`.
- `MetricAxis` — canonical metric-axis identity record (`metric_id`, `axis_name`,
  `parent_object`, `primitive`).
- `MetricReadout` — a signed-ternary readout tied to its parent UCNS object via
  `parent_hash`.
- `ConstraintField` — UCNS **state object** (`schema_id` `edcm/constraint_field_ucns_v1`).
  Produces presence / contact / resolution readouts (R, D, I, L_resistance). **Empty-field
  rule (spec §4.1): when `raised_field_count == 0` the readouts are `NA`, not `0`.**
- `FieldMotion` — UCNS **tangent object** (`schema_id` `edcm/field_motion_ucns_v1`).
  Produces F / E / O_scope motion readouts between two `ConstraintField`s. The three
  readouts share one `parent_hash` but keep distinct `metric_id`s.

Vocabulary maps (signed ternary): `CONTACT_SIGN` (`toward=+1`, `against=-1`, `away=0`),
`RESOLUTION_SIGN` (`closed=+1`, `open=-1`, `unresolved=0`). `GRAINS` enumerates valid
`grain` values.

Reference data: `FIELD_MOTION_FIXTURE_MATRIX` and `field_motion_fixture(name)` provide the
spec §13 sign-only F/E/O_scope fixtures; `canonical_axes()` returns the spec §9 primitive
axes plus §10 projections (projections have `primitive=False`).

---

## Conventions & gotchas

- **`NA != 0`.** Never collapse a disabled (`enabled=False`) `AxisState` into a `0` state.
  Empty `ConstraintField`s and absent `FieldMotion` presence yield `NA`; present-but-empty
  reads yield a stable `0`. Tests assert this distinction explicitly.
- **No theorem/proof transfer.** Per the module/README docstrings: no UCNS-A theorem/proof
  status is transferred to EDCM, edcmbone, or UCNS-G by this code. Keep that scoping intact.
- **Spec-anchored.** `ucns_objects.py` mirrors a specific upstream spec version (v0.2).
  When changing readout logic, sign maps, axis ids, or the fixture matrix, keep them
  consistent with that spec and update `tests/test_ucns_objects.py` to match.
- **Dependency-free.** Do not add third-party runtime dependencies to the package; the
  whole point is that it runs without `ucns`/`edcmbone` installed. Imports of those
  packages must stay optional (guarded by `try/except`).
- **Public API.** When adding a public symbol, export it from `edcm/__init__.py` `__all__`.
- **After edits, run `python3 -m pytest -q`** from the repo root and keep all tests green.

---

## Relationship to `edcmbone`

`edcmbone` is one of the two upstream repos being consolidated here and the source of the
measurement layer and the UCNS construction objects. In this repo:

- `layers.py` optionally imports `edcmbone.MeasurementLayer` at runtime, falling back to a
  local default when unavailable.
- `ucns_objects.py` is a hand-maintained, dependency-free mirror of edcmbone's
  orthogonality module — not an import. Changes upstream may need to be re-mirrored here.
