# Consolidation record — edcmbone → edcm

Date: 2026-07-06
Executes: `The-Interdependency/edcmbone:LAYER_MIGRATION_PLAN.md` (the
"future `edcm` package" contract) in mirror form.

## Source of truth

```text
repo:   The-Interdependency/edcmbone
path:   backend_old/src/edcmbone/          (the canonical, tested package)
commit: 05eee6d15c7ad0a7dcf62220a3a0a8618f481a81
```

## What was consolidated

The canonical edcmbone structural-measurement package was mirrored into
`edcm/measurement/`:

| edcmbone (upstream) | edcm (here) |
|---|---|
| `backend_old/src/edcmbone/canon/` (+ `data/*_v1.json`) | `edcm/measurement/canon/` |
| `backend_old/src/edcmbone/parser/turns_rounds.py` | `edcm/measurement/parser/turns_rounds.py` |
| `backend_old/src/edcmbone/metrics/` (stats, risk, compute, matrix, projection) | `edcm/measurement/metrics/` |
| `backend_old/src/edcmbone/metrics/orthogonality.py` | **not duplicated** — re-exported from the pre-existing mirror `edcm/ucns_objects.py` (module bodies verified identical at the source commit) |
| `backend_old/src/edcmbone/ucns/` (ucns_v04, closed_tokens) | `edcm/measurement/ucns/` |
| `backend_old/src/edcmbone/compress.py` | `edcm/measurement/compress.py` |

Ported tests: `tests/test_measurement_closed_tokens.py` (from
`tests/test_closed_tokens.py`, retargeted at the packaged encoder),
`tests/test_measurement_canon.py` (polarity balance + backend-parser affix
regressions), and new `tests/test_measurement.py` (pipeline end-to-end,
compress roundtrip, layers wiring, no-fork guarantee).

## Mirror deltas (mechanical only)

- Absolute `edcmbone.*` imports rewritten to package-relative imports.
- `# ratios:` bookend stamps removed (edcmbone-local CI tooling; not run here).
- `metrics/__init__.py` imports the orthogonality surface from
  `edcm.ucns_objects` instead of a local `orthogonality.py`.
- MODULE_BUILD block ids (`edcmbone_*`) kept as-is for provenance and cheap
  re-mirror diffs.

No metric formulas, sign maps, canon JSON data, thresholds, or parser
behavior were changed.

## Wiring

- `edcm.layers.ConsolidatedMeasurementLayer` runs the consolidated pipeline
  (parse → compute → project → compression stats) when a payload carries a
  `transcript` string.
- `build_default_layers()` resolution order for the measurement layer:
  installed upstream `edcmbone` exposing `MeasurementLayer` (upstream stays
  canonical L0) → `ConsolidatedMeasurementLayer` → `DefaultMeasurementLayer`.
- Key entry points re-exported from the package root: `CanonLoader`,
  `parse_transcript`, `compute_transcript`, `project_transcript`,
  `RoundMetrics`, `AgentMetrics`, `fire_alerts`, plus the `edcm.measurement`
  subpackage itself.

## Doctrine kept intact

- **Mirror, not move.** edcmbone remains the canonical L0 source; this repo
  stays runnable without edcmbone installed (same doctrine as
  `edcm/ucns_objects.py`). Nothing was deleted upstream.
- **No theorem/proof transfer.** No UCNS-A theorem/proof status transfers to
  EDCM, edcmbone, or UCNS-G via this mirror (edcmbone
  `docs/ucns-boundary.md`).
- **Dependency-free.** The mirrored package is stdlib-only; imports of
  external `ucns`/`edcmbone` stay optional.

## hmmm — open items carried from LAYER_MIGRATION_PLAN.md

- The L0/L1/L2/L3 layer split is **not** executed here: the mirror carries
  all layers together because the metric-to-layer table (which letters are
  L1 Arc Style vs L2 composites) is still unpinned — the plan's Phase 2 gate.
- `A_MATRIX` wiring (Findings 07/08), `P`-metric layer assignment
  (Finding 06), bidirectional alerts (Finding 30), and the Bridge home
  decision remain open upstream; this mirror does not resolve them.
- edcmbone root `engine.py` (the v1.0.0 orchestrator) and `core/` (refactor
  side: Bridge, core parsing/operator) were not consolidated; whether `edcm`
  unifies `compute.py`/`engine.py` under one entry point is unresolved.
- Re-mirroring: upstream changes to `backend_old/src/edcmbone/` need to be
  re-applied here manually, citing the new source commit in
  `edcm/measurement/__init__.py`.
