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
(`.github/workflows`), or lint config in this repository. Do not invent or reference any.
The repo is used as a source tree imported directly (see `tests/conftest.py`).

---

## Repository layout

```
edcm/
├── README.md                  # Project intent, usage examples
├── docs/                      # Handoffs + consolidation records
│   ├── codex_edcmucns_v031_handoff.md
│   └── consolidation-edcmbone.md   # edcmbone → edcm consolidation record (source SHA, deltas, hmmm)
├── edcm/                      # The package
│   ├── __init__.py            # Public API surface (re-exports from submodules)
│   ├── layers.py              # Four-layer EDCM bootstrap (+ ConsolidatedMeasurementLayer)
│   ├── ucns_objects.py        # UCNS metric construction objects (v0.2 spec mirror)
│   ├── energy_claims.py       # Energy-audit claim extraction/auditing
│   ├── falsifiability_bridge.py    # edcmbone-style F-loss preservation audit
│   ├── ucns_dependency.py     # Optional ucns availability helpers
│   ├── edcmucns/              # edcmucns v0.3.1 architecture (identity layer; frontier gated)
│   │   ├── manifest.py types.py provenance.py geometry.py encoder.py
│   │   ├── scopes.py equivalence.py validation.py composer.py epochs.py
│   │   └── __init__.py        # public surface + canon doctrine docstring
│   └── measurement/           # Consolidated edcmbone mirror (stdlib-only)
│       ├── canon/             # CanonLoader + frozen data/*_v1.json (do not edit data)
│       ├── parser/            # turns_rounds transcript parser
│       ├── metrics/           # stats, risk, compute, matrix, projection
│       │                      #   (orthogonality re-exported from edcm.ucns_objects — no fork)
│       ├── ucns/              # closed-token UCNS encoder (ucns_v04, closed_tokens)
│       └── compress.py        # lossless codec + compression stats (F)
└── tests/
    ├── conftest.py            # Inserts repo root onto sys.path so `import edcm` works
    ├── test_ucns_objects.py   # ucns_objects tests
    ├── test_energy_claims.py / test_falsifiability_bridge.py / test_ucns_dependency.py
    ├── test_measurement.py    # pipeline end-to-end, layers wiring, no-fork guarantee
    ├── test_measurement_canon.py          # polarity balance + affix regressions (ported)
    └── test_measurement_closed_tokens.py  # closed-token encoder suite (ported)
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

The package has three main pieces (plus the `edcmucns/` architecture package
and the smaller energy-audit modules).

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

### 3. Consolidated measurement package (`edcm/measurement/`)

A dependency-free mirror of the canonical edcmbone structural-measurement
package (`The-Interdependency/edcmbone: backend_old/src/edcmbone/`; source
commit pinned in `edcm/measurement/__init__.py`). Ships canon data +
`CanonLoader`, the turns/rounds parser, the metric stack (stats/risk/compute/
matrix/projection), the closed-token UCNS encoder, and the lossless codec with
`structural_density` (F). Pipeline: `parse_transcript → compute_transcript →
project_transcript` (+ `compress` for F stats).

- `layers.ConsolidatedMeasurementLayer` runs this pipeline when a payload has
  a `transcript` string; `build_default_layers()` uses it whenever an
  installed upstream `edcmbone` doesn't provide a `MeasurementLayer`.
- `measurement/metrics/orthogonality` is **not** a second copy — the
  orthogonality surface is re-exported from `edcm.ucns_objects`
  (`tests/test_measurement.py::test_orthogonality_surface_is_not_forked`).
- Mirror doctrine: edcmbone stays canonical L0; re-mirror upstream changes
  manually and bump the source commit. See `docs/consolidation-edcmbone.md`
  for full provenance, mirror deltas, and open `hmmm` items.
- Canon JSON under `edcm/measurement/canon/data/` is frozen (`_v1`) — do not
  edit by hand.

### 4. edcmucns v0.3.1 architecture (`edcm/edcmucns/`)

Implements the **edcmucns design canon v0.3.1** (`docs/codex_edcmucns_v031_handoff.md`):
EDCM on UCNS mathematics, provenance as the recurring theme. **Architecture
only** — ratified/frozen as architecture, frontier as empirical measurement.
Primary doctrine: *UCNS exists to construct EDCM metrics.* Firewall: no EDCM
measurement claim inherits proof status from its UCNS-A substrate.

Modules: `manifest` (hashable `PolicyManifest`; hash change = epoch break),
`provenance` (`ProvenanceWitness`; only readout-bearing fields hashed),
`types` (`Anchor` origin/bone/cadence, `Payload`, `Window`, `OperatorTurn` =
`Present | AbsentOperatorGeometry`), `geometry` (non-origin residue rule,
`L_geo`/`L_op` mass, `n_host_total`/`n_family`/`n_cadence`/`n_payload`
carriers, `lambda_field`), `encoder` (`encode_turn`; no-bone turns →
`AbsentOperatorGeometry`), `scopes` (closed `REGISTRY` of five readout
scopes), `equivalence` (`ucns_carrier_equivalent` vs scoped
`edcm_measurement_equivalent`), `validation` (`witness_geometry_consistent`,
`gauge_audit` → `BridgeDiagnostic`s), `composer` (`seq_append` ⊞ for windows;
`interaction_product` ⊠ reserved; kappa placeholders), `epochs` (`EpochChain`
manifest rotation).

Guardrails (enforced by tests, from the handoff):
- **Non-origin residue rule**: `r_f(m) = 1 + ((m−1) mod (p−1))`,
  `θ = r_f/p`. θ=0 is reserved for explicit datum (origin) roles; a bone
  never lands on the origin. Do **not** reintroduce the old `m mod p` rule.
- **NA, never 0**: empty fields and no-bone turns emit NA; absent field load
  is `None`, not `0`.
- **Never average windows**; compose with `seq_append` (lengths add, F
  concatenates, carrier = lcm). `A⊞B ≠ B⊞A` — order is testimony.
- **Manifest identity is always in scope** for `edcm_measurement_equivalent`;
  same geometry does **not** imply same reading.
- **Frontier gates** (`contact_convergence`, `da_geom_correlation`,
  `admit_cadence_from_text`) are `NotImplementedError` surfaces with named
  falsifiers — do not make them return values or claim they work.

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

- `edcm/measurement/` is the consolidated, dependency-free mirror of edcmbone's canonical
  package (see `docs/consolidation-edcmbone.md` for provenance and mirror deltas).
- `layers.py` optionally imports `edcmbone.MeasurementLayer` at runtime (upstream override
  wins — edcmbone stays canonical L0), then falls back to `ConsolidatedMeasurementLayer`
  backed by `edcm.measurement`, then to the inert default.
- `ucns_objects.py` is a hand-maintained, dependency-free mirror of edcmbone's
  orthogonality module — not an import. Changes upstream may need to be re-mirrored here.
  `edcm.measurement.metrics` re-exports it rather than carrying a second copy.
- Not consolidated (still upstream-only): root `engine.py`, `core/` (Bridge, refactor-side
  parsing/operator), `canon_eng/`, UCNS-G, and the new `edcmbone_backend` 0.2.0 package.
