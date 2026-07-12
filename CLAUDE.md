# CLAUDE.md — EDCM repository instructions

This repository is the maintained Python package for the Energy–Dissonance Circuit Model.

## Read first

1. `codex-handoff/2026-07-12-stack-repair/REQUIRED_CHANGES.md`
2. `codex-handoff/2026-07-12-stack-repair/COMPLETED_LOOKS_LIKE.md`
3. `codex-handoff/2026-07-12-stack-repair/IMPLEMENTATION_STATUS.md`
4. `README.md`
5. `docs/ucns-adapter.md`
6. `docs/shared-stack-result.md`
7. `docs/consolidation-edcmbone.md`
8. `docs/codex_edcmucns_v031_handoff.md`
9. repo-local `.agents/skills/`, especially `the-interdependency`, `msdmd`, `meta-module-build`, and applicable metadata skills.

Unknown or unresolved facts are written `hmmm`, not guessed.

## Package and release facts

| Property | Value |
|---|---|
| Python | 3.11+; CI covers 3.11, 3.12, 3.13 |
| Base runtime dependencies | none |
| Optional integrations | pinned `ucns`, `metapat`, `full-stack` extras |
| Build metadata | `pyproject.toml` |
| Package version | `edcm.__version__` |
| License | MPL-2.0 |
| Tests | `pytest` |
| CI | `.github/workflows/ci.yml` |

Release gate:

```bash
python -m pip install -e .[dev]
python -m pytest -q
python -m build
python -m twine check dist/*
```

CI separately verifies base, UCNS-only, METAPAT-only, full shared-stack, and clean-wheel modes.

## Source-of-truth decisions

### Measurement

`edcm/measurement/` is the canonical maintained measurement implementation and frozen canon-data authority.

- `The-Interdependency/edcmbone` is historical consolidation provenance and an explicit compatibility source only.
- An installed `edcmbone` package never silently overrides EDCM.
- Authority and provenance are machine-readable through `edcm.measurement.MEASUREMENT_AUTHORITY`.
- Frozen JSON under `edcm/measurement/canon/data/*_v1.json` changes only through a new version and migration record.

### METAPAT semantic authority

EDCM owns the consumer adapter, not the semantic schema. Consume only the actual producer surfaces:

```text
metapat.MetapatModuleEnvelope
metapat.MODULE_ENVELOPE_SCHEMA_ID
metapat.MODULE_ENVELOPE_SCHEMA_VERSION
MetapatModuleEnvelope.from_json
MetapatModuleEnvelope.from_dict
```

Accepted payload keys are mutually exclusive:

```text
metapat_envelope
metapat_envelope_json
metapat_envelope_dict
```

Preserve exact source statements, references, constraints, permitted interpretations, unresolved `hmmm`, canon identity, and provenance digest. Never convert labels or statements directly into metric values.

Direct absence of `metapat` is typed unavailability. Transitive import errors, missing producer surfaces, unsupported schemas, invalid provenance, unknown fields, and wrong envelope types remain visible failures.

### UCNS geometry

Do not look for or recreate `ucns.SemanticsLayer`. Consume actual:

```text
ucns.UCNSObject
ucns.object_record
ucns.stable_hash
ucns.CANONICAL_SERIALIZATION_VERSION
typed domain prerequisite metadata
```

Direct absence of `ucns` is typed geometry absence. Transitive import errors, missing public surfaces, unsupported schemas, malformed geometry, and non-`UCNSObject` values remain visible failures.

Package availability alone never implies object, scope, negative-certification, or theorem evidence attachment.

## Layer behavior

`build_default_layers(policy_manifest=None)` assembles four provenance-bearing stages:

1. composite semantics: independent METAPAT authority and UCNS geometry sublayers;
2. canonical `edcm.measurement`;
3. canonical shared-stack composition;
4. canonical final result-contract delivery.

Layer provenance records are separate:

```text
semantic_authority
geometry
semantics
measurement
composition
delivery
```

Every record includes implementation id/version, source repository, role, selection state, canonical/fallback status, unresolved constraints, and loading errors where applicable.

## Final result contract

Every supported pipeline result includes `edcm_result` with distinct compartments:

```text
source_evidence
metapat_semantic_constraints
ucns_geometry_identity
edcm_policy_manifest
implementation_provenance
readouts
status_evidence
unresolved_constraints
```

`epoch_identity` binds METAPAT canon/provenance, UCNS geometry, EDCM manifest, and implementation selection. `result_identity` additionally binds source evidence and readouts.

Changing a METAPAT canon digest or EDCM policy manifest must change epoch identity. It must not silently mutate historical identity.

## Object and proof boundaries

`ConstraintField`, `FieldMotion`, metric axes, readouts, windows, and operator turns are EDCM objects constructed using UCNS geometry. They are not substitutes for `ucns.UCNSObject`.

Keep separate:

- source evidence;
- METAPAT semantic authority;
- UCNS stable geometry identity;
- EDCM policy-manifest identity;
- EDCM measurement identity and readouts.

UCNS equality does not imply EDCM measurement equivalence. UCNS or METAPAT theorem/domain status is attached evidence only and never promotes EDCM empirical validity.

## Non-negotiable guardrails

- `NA != 0`.
- No-bone, empty-field, absent-adapter, and missing-context cases remain typed absence or `NA`.
- Ordered windows compose with `SeqAppend`; never average testimony-bearing order.
- METAPAT semantic labels never become measured values merely by being named.
- Deterministic transcript metrics do not establish diagnosis, intent, consciousness, external truth, or root ontology.

These frontier gates remain non-operational until their named falsifiers and tests exist:

- contact convergence;
- DA geometry correlation;
- cadence admission from text;
- semantic-label-to-operating-state inference.

Do not replace `NotImplementedError` with constants, heuristics, language-model judgments, or decorative numbers.

## Testing expectations

Base tests pass without UCNS or METAPAT installed. Integration tests use actual pinned sibling packages.

The full-stack fixture proves:

- a canonical METAPAT envelope is accepted;
- an actual UCNS object is attached;
- UCNS stable hash survives;
- METAPAT canon identity and EDCM manifest identity remain distinct;
- readouts are produced without proof-status transfer;
- `NA != 0`;
- malformed producer data fails closed;
- canon or manifest rotation changes epoch identity;
- transcript measurement is deterministic;
- package availability is not misreported as attached evidence.

Optional skips are explicit. Fake sibling implementations may test adversarial construction but never count as integration success.

## msdmd and skill-lib

- New EDCM-native modules begin with accurate `MODULE_BUILD` blocks.
- Changed native modules cite real tests and actual dependencies.
- Tests carry no `MODULE_BUILD` block.
- Historical measurement modules retain provenance until the explicit metadata-reconciliation pass.
- Run repo-local skill-lib drift and msdmd checks when available; absence or failure remains explicit.
- Code and documentation include runnable usage guidance, integration notes, limitations, and `hmmm` boundaries.

## hmmm

Still unresolved:

- official serialized UCNS bridge-record ingestion beyond live `UCNSObject` / `object_record`;
- validated negative-certification and theorem-status evidence envelopes;
- frozen-canon integrity and source-of-truth drift automation;
- repo-local skill-lib drift and msdmd CI gates;
- remaining historical L0/L1/L2/L3 split, P assignment, matrix wiring, bidirectional alerts, and Bridge-home decisions.

These unresolveds do not reopen measurement authority, semantic-authority ownership, or the proof-transfer firewall.
