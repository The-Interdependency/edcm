# CLAUDE.md — EDCM repository instructions

This repository is the maintained Python package for the Energy–Dissonance Circuit Model.

## Read first

Before changing code, read:

1. `codex-handoff/2026-07-12-stack-repair/REQUIRED_CHANGES.md`
2. `codex-handoff/2026-07-12-stack-repair/COMPLETED_LOOKS_LIKE.md`
3. `codex-handoff/2026-07-12-stack-repair/IMPLEMENTATION_STATUS.md`
4. `README.md`
5. `docs/ucns-adapter.md`
6. `docs/consolidation-edcmbone.md`
7. `docs/codex_edcmucns_v031_handoff.md`
8. repo-local `.agents/skills/` material, especially `the-interdependency`, `msdmd`, `meta-module-build`, and relevant metadata skills.

Unknown or unresolved facts are written `hmmm`, not guessed.

## Package facts

| Property | Value |
|---|---|
| Python | 3.11+; CI covers 3.11, 3.12, 3.13 |
| Runtime dependencies | none for the base package |
| Build metadata | `pyproject.toml` |
| Package version | `edcm.__version__` |
| License | MPL-2.0 |
| Tests | `pytest` |
| CI | `.github/workflows/ci.yml` |

Run the release gate from the repository root:

```bash
python -m pip install -e .[dev]
python -m pytest -q
python -m build
python -m twine check dist/*
```

CI also installs the built wheel into a clean environment and runs installed-package smoke tests.

## Source-of-truth decisions

### Measurement

`edcm/measurement/` is the canonical maintained measurement implementation and frozen canon-data authority.

- `The-Interdependency/edcmbone` is historical consolidation provenance and a possible explicit compatibility source.
- An installed `edcmbone` package must never silently override EDCM.
- Authority and provenance are machine-readable through `edcm.measurement.MEASUREMENT_AUTHORITY`.
- Frozen JSON under `edcm/measurement/canon/data/*_v1.json` changes only through a new version and migration record.

### UCNS

EDCM owns the adapter contract it needs. Do not look for or recreate `ucns.SemanticsLayer`.

The live adapter consumes actual UCNS public surfaces:

- `ucns.UCNSObject`
- `ucns.object_record`
- `ucns.stable_hash`
- `ucns.CANONICAL_SERIALIZATION_VERSION`
- typed domain prerequisite metadata

Direct absence of the optional `ucns` package selects explicit transcript-only mode. These conditions must remain visible failures rather than fallback triggers:

- transitive import errors;
- missing required public surfaces;
- unsupported canonical schemas;
- malformed geometry;
- non-`UCNSObject` values supplied as `ucns_object`.

Every result distinguishes:

```text
ucns_package_available
ucns_adapter_active
ucns_object_attached
ucns_scope_metadata_attached
ucns_negative_certification_attached
ucns_theorem_status_attached
```

Import success alone does not attach evidence.

### METAPAT

The METAPAT semantic-envelope adapter is not yet implemented. Do not invent its schema or convert root ontology statements directly into EDCM metric values. Preserve this as `hmmm` until the canonical versioned envelope is identified from METAPAT.

## Layer behavior

`build_default_layers()` assembles four provenance-bearing layers:

1. actual UCNS geometry adapter or explicit transcript-only semantics;
2. canonical `edcm.measurement`;
3. explicit local composition fallback;
4. explicit local delivery fallback.

Every layer reports implementation id, implementation version, source repository, role, selection state, canonical/fallback status, unresolved constraints, and loading errors where applicable.

Do not use unexplained labels such as `semantics: default` or `measurement: default`.

## Object boundary

`ConstraintField`, `FieldMotion`, metric axes, readouts, windows, and operator turns are EDCM objects constructed using UCNS geometry. They are not implementations or substitutes for `ucns.UCNSObject`.

Keep these identities separate in result and equivalence logic:

- source evidence;
- METAPAT canon/constraints;
- UCNS stable geometry identity;
- EDCM policy-manifest identity;
- EDCM measurement identity and readouts.

UCNS equality does not imply EDCM measurement equivalence.

## Non-negotiable guardrails

- `NA != 0`.
- No-bone, empty-field, absent-adapter, and missing-context cases remain typed absence or `NA`.
- Ordered windows compose with `SeqAppend`; never average testimony-bearing order.
- UCNS theorem/domain status is attached evidence only and never promotes EDCM empirical validity.
- METAPAT semantic labels never become measured values merely by being named.
- Deterministic transcript metrics do not establish diagnosis, intent, consciousness, external truth, or root ontology.

The following frontier gates remain non-operational until their named falsifiers and tests exist:

- contact convergence;
- DA geometry correlation;
- cadence admission from text;
- semantic-label-to-operating-state inference.

Do not replace `NotImplementedError` with constants, heuristics, language-model judgments, or decorative numbers.

## Repository layout

```text
edcm/
├── pyproject.toml
├── README.md
├── CLAUDE.md
├── .github/workflows/ci.yml
├── codex-handoff/2026-07-12-stack-repair/
├── docs/
├── edcm/
│   ├── __init__.py
│   ├── layers.py
│   ├── ucns_adapter.py
│   ├── ucns_dependency.py
│   ├── ucns_objects.py
│   ├── energy_claims.py
│   ├── falsifiability_bridge.py
│   ├── edcmucns/
│   └── measurement/
└── tests/
```

## msdmd and skill-lib

- New EDCM-native modules begin with an accurate `MODULE_BUILD` block.
- Changed native modules must cite real tests and actual dependencies.
- Tests do not carry `MODULE_BUILD` blocks.
- Consolidated historical measurement modules retain their current metadata until the explicit metadata-reconciliation pass; do not casually restamp them and erase provenance.
- Run repo-local skill-lib drift and msdmd checks when available. Their absence or failure remains explicit.
- Every code or documentation change includes runnable usage guidance, integration notes, limitations, and `hmmm` boundaries.

## Testing expectations

Base tests must pass without UCNS or METAPAT installed.

The UCNS integration job installs a pinned actual UCNS commit and proves:

- actual object acceptance;
- stable hash preservation;
- schema preservation;
- package availability distinct from evidence attachment;
- no theorem-status transfer;
- canonical EDCM measurement selection.

Add adversarial tests for malformed and absent metadata. Optional integration skips must be explicit; a fake sibling implementation must never count as integration success.

## Public API

When adding a supported public symbol, export it through `edcm/__init__.py` and include it in `__all__`. Keep built-wheel smoke tests aligned with the documented public surface.

## hmmm

Still unresolved:

- immutable METAPAT semantic-envelope ingestion;
- official serialized UCNS bridge-record ingestion beyond live `UCNSObject` / `object_record`;
- validated negative-certification and theorem-status evidence envelopes;
- full UCNS/METAPAT/EDCM result envelope and shared-stack fixtures;
- frozen-canon integrity manifest and repo-local skill-lib drift gate;
- historical L0/L1/L2/L3 split, P assignment, matrix wiring, bidirectional alerts, and Bridge home.

These unresolveds do not reopen measurement source-of-truth ambiguity: EDCM remains the maintained authority unless a later explicit, versioned governance decision changes it.
