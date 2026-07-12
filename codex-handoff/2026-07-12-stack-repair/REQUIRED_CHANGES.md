# EDCM stack repair — required changes

Date: 2026-07-12
Repository: `The-Interdependency/edcm`
Audience: coding specialist AI
Status: implementation handoff

## Governing objective

Make EDCM an installable, testable, provenance-bearing measurement package that consumes actual UCNS geometry and METAPAT semantic constraints without silently substituting defaults, preserving stale mirrors as competing authorities, or importing theorem status into empirical readouts.

Before editing, read `CLAUDE.md`, `README.md`, `docs/consolidation-edcmbone.md`, `docs/codex_edcmucns_v031_handoff.md`, `edcm/layers.py`, `edcm/ucns_dependency.py`, `edcm/ucns_objects.py`, `edcm/energy_claims.py`, `edcm/edcmucns/`, `edcm/measurement/`, all tests, and the repo-local `.agents/skills/` material if present. Follow `The-Interdependency/skill-lib` doctrine and preserve every empirical frontier gate and `hmmm` boundary unless the corresponding falsifier and implementation are actually supplied.

## Required patch order

### 1. Make EDCM a real Python package

Add an authoritative `pyproject.toml` with:

- build system;
- package name and version;
- Python support matching CI;
- MPL-2.0 license metadata;
- package discovery;
- public project URLs;
- dev/test/build dependencies;
- typed-package declaration if supported by the codebase;
- optional integration extras for actual UCNS and METAPAT adapters where installable.

Expose `edcm.__version__` from the same authoritative version source.

Add package build, wheel install, metadata, and import smoke tests. Remove documentation that says the repository has no package metadata once the package exists.

### 2. Add continuous integration and a release gate

Create GitHub Actions coverage for supported Python versions. The gate must include:

```bash
python -m pip install -e .[dev]
python -m pytest -q
python -m build
python -m twine check dist/*
```

Also install the produced wheel into a clean environment and run public API smoke tests there.

CI must distinguish:

- base package tests without sibling repositories;
- UCNS integration tests;
- METAPAT integration tests;
- full shared-stack contract tests.

Unavailable optional integrations may skip explicitly. They may not silently substitute a fake integration and report success.

### 3. Replace the fictional `ucns.SemanticsLayer` discovery

`build_default_layers()` currently looks for `ucns.SemanticsLayer`, a public surface UCNS does not provide, catches every exception, and silently returns `DefaultSemanticsLayer`.

Replace this with an EDCM-owned adapter protocol and an explicit actual-UCNS implementation.

Minimum behavior:

- EDCM defines the protocol it needs; UCNS is not required to expose an EDCM-specific class.
- the adapter uses actual public UCNS objects and the official UCNS bridge/status surfaces;
- missing optional dependency is distinct from adapter construction failure;
- catch only the expected missing-dependency exception;
- unexpected import, schema, or adapter errors propagate or produce an explicit failed integration status;
- the selected adapter and its version/provenance appear in the pipeline result;
- fallback mode is explicit in output and tests, never silent.

Delete or deprecate `_maybe_from_ucns()` once the real adapter is in place.

### 4. Resolve measurement source-of-truth ambiguity

The repository is described as the consolidation target, yet documentation still says `edcmbone` remains canonical L0 and EDCM carries dependency-free mirrors.

Make one explicit decision and encode it everywhere. Preferred decision:

- EDCM becomes the canonical maintained measurement implementation after consolidation;
- `edcmbone` becomes archived, compatibility-only, or a provenance source rather than a competing live authority.

If edcmbone must remain authoritative temporarily, replace manual mirroring with a deterministic sync and drift-check process that fails CI when the mirror diverges.

Required outcomes:

- one source of truth for `measurement` code and canon data;
- no runtime preference for an installed stale `edcmbone.MeasurementLayer` over newer consolidated EDCM code unless a versioned compatibility policy explicitly authorizes it;
- source commit, local deltas, and synchronization state remain machine-readable;
- duplicated orthogonality or UCNS geometry classes are eliminated or generated from one canonical source.

### 5. Use actual UCNS objects at the geometry boundary

`edcm.ucns_objects` and `edcm.edcmucns` may retain EDCM-specific state/readout types, but they must not masquerade as the UCNS algebra.

Implement a narrow geometry adapter that:

- accepts actual `ucns.UCNSObject` or the official UCNS bridge record;
- records UCNS object stable hash and bridge schema version;
- derives only the geometry needed by EDCM;
- keeps EDCM metric identity and provenance separate from UCNS equality;
- reports UCNS theorem/domain status only as attached evidence, never as measurement validity;
- fails closed on malformed geometry or unsupported schema versions.

Rename any local concepts that could reasonably be mistaken for canonical UCNS objects. `ConstraintField`, `FieldMotion`, metric axes, windows, and operator turns are EDCM objects constructed **using** UCNS geometry, not substitutes for `UCNSObject`.

### 6. Add the METAPAT semantic-authority adapter

Consume the versioned METAPAT semantic module envelope rather than importing METAPAT root statements as metric values.

The adapter must preserve:

- canon version/digest;
- source statement references;
- module kind;
- permitted interpretations and constraints;
- unresolved `hmmm` fields;
- provenance digest.

The measurement pipeline must keep separate fields for:

- source evidence;
- METAPAT semantic constraints;
- UCNS geometry identity;
- EDCM measurement policy/manifest;
- EDCM readouts.

Changing the METAPAT canon digest or the EDCM policy manifest must create an observable provenance/epoch change. It must not silently alter historical readouts in place.

### 7. Correct dependency and scope reporting

`audit_energy_text()` currently treats successful `import ucns` as if UCNS-dependent scope metadata were attached.

Change reporting so it distinguishes:

```text
ucns_package_available
ucns_adapter_active
ucns_object_attached
ucns_scope_metadata_attached
ucns_negative_certification_attached
ucns_theorem_status_attached
```

A package import alone may set only `ucns_package_available`.

Attach exact evidence records where available. Do not reduce these states to one `available/missing` string. Add adversarial tests showing that importable UCNS with absent or malformed metadata does not produce a false attachment claim.

### 8. Make fallback and absence first-class states

Every layer selection must produce an explicit provenance record.

For semantics, measurement, composition, and delivery, record:

- implementation id;
- implementation version;
- source repository/commit where applicable;
- whether it is canonical, compatibility, local fallback, or unavailable;
- unresolved constraints;
- errors encountered during optional adapter loading.

Do not annotate a payload with `semantics: default` or `measurement: default` without also making clear that no canonical integration ran.

No-bone, empty-field, absent-adapter, and missing-context cases must remain `NA` or typed absence, never measured zero.

### 9. Preserve empirical frontier gates

The following or equivalent named frontier surfaces must remain non-operational until implemented with their named falsifiers and tests:

- contact convergence;
- DA geometry correlation;
- cadence admission from text;
- any inference that converts semantic labels directly into operating-state claims.

Do not replace `NotImplementedError` with placeholder numbers, defaults, heuristics, or language-model judgments merely to make an integration test pass.

### 10. Add the shared UCNS/METAPAT/EDCM contract suite

Create deterministic integration fixtures proving:

1. a versioned METAPAT semantic module envelope is accepted;
2. an actual UCNS object or official bridge record is attached;
3. UCNS equality and stable hash survive the integration path;
4. EDCM policy manifest and METAPAT canon identity remain distinct provenance components;
5. a valid EDCM readout can be produced without importing UCNS proof status;
6. `NA != 0` throughout empty and absent cases;
7. malformed bridge/schema/provenance data fails closed;
8. manifest or canon rotation creates a new epoch identity;
9. raw transcript measurement remains reproducible;
10. no sibling package availability check is misreported as attached evidence.

### 11. Reconcile docs, metadata, and agent surfaces

Update all affected:

- README and CLAUDE instructions;
- consolidation records;
- package metadata;
- public API documentation;
- `MODULE_BUILD`, `DOCS`, `CAPABILITIES`, `BOUNDARIES`, `CONTRACTS`, `DEPENDENCIES`, and `OWNERS` blocks;
- tests named in metadata;
- skill-lib/msdmd declarations;
- source-of-truth statements;
- fallback descriptions;
- claim-status firewalls.

Remove statements made obsolete by packaging, CI, source-of-truth selection, or real adapter implementation.

## Required non-goals

Do not:

- make EDCM measurement claims inherit UCNS theorem status;
- make METAPAT semantic labels equal measured values;
- silently catch arbitrary integration exceptions;
- silently prefer an installed stale edcmbone implementation;
- keep two canonical measurement implementations;
- call absence zero;
- average ordered windows where `SeqAppend` is required;
- implement empirical frontier gates with fabricated heuristics;
- claim that deterministic transcript metrics establish external truth, diagnosis, intent, or consciousness;
- change frozen measurement canon data without a version and migration record.

## Verification gate

From a clean checkout, run:

```bash
python -m pip install -e .[dev]
python -m pytest -q
python -m build
python -m twine check dist/*
```

Then run:

- clean-wheel installation and public API smoke tests;
- base-package tests without UCNS/METAPAT;
- actual UCNS adapter tests;
- actual METAPAT envelope tests;
- full shared-stack fixtures;
- source-of-truth drift check;
- frozen-canon integrity check;
- manifest/canon epoch-rotation tests;
- repo-local skill-lib drift and msdmd checks.

## hmmm

The remaining architectural choice is whether EDCM should require UCNS for every geometry-bearing workflow or support a base transcript-only mode. Either is viable. Completion requires that the selected mode be explicit, typed, provenance-bearing, and never confused with the full UCNS-backed measurement path.