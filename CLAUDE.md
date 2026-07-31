# CLAUDE.md — EDCM repository instructions

This repository is the maintained Python package for the Energy–Dissonance Circuit Model.

## Read first

1. `codex-handoff/2026-07-12-stack-repair/REQUIRED_CHANGES.md`
2. `codex-handoff/2026-07-12-stack-repair/COMPLETED_LOOKS_LIKE.md`
3. `codex-handoff/2026-07-12-stack-repair/IMPLEMENTATION_STATUS.md`
4. `README.md`
5. `docs/integrity-gates.md`
6. `docs/ucns-adapter.md`
7. `docs/shared-stack-result.md`
8. `docs/consolidation-edcmbone.md`
9. `docs/codex_edcmucns_v031_handoff.md`

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
python -m edcm.integrity
python -m pytest -q
python -m build
python -m twine check dist/*
```

CI separately verifies base, integrity, UCNS evidence, METAPAT-only, full shared-stack, and clean-wheel modes. The integrity gate must also pass from the installed wheel.

## Integrity and source of truth

`edcm/measurement/` is the canonical maintained measurement implementation and frozen canon-data authority.

- `The-Interdependency/edcmbone` is historical consolidation provenance and explicit compatibility input only.
- An installed `edcmbone` package never silently overrides EDCM.
- Authority and provenance are machine-readable through `edcm.measurement.MEASUREMENT_AUTHORITY`.
- Frozen JSON under `edcm/measurement/canon/data/*_v1.json` changes only through a new version and migration record.

`python -m edcm.integrity` verifies:

1. the exact set and Git blob identities of all frozen `*_v1.json` files;
2. the complete measurement-authority and compatibility-policy record;
3. that measurement orthogonality re-exports the canonical EDCM classes rather than a drifting copy.

Never update pinned canon identities merely to make CI pass. A legitimate change creates a new canon version and migration record.

## METAPAT semantic authority

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

## Exact EDCM UCNS observation profile

EDCM owns the consumer adapter. UCNS owns the exact EDCM-only word-gonol
profile and v0.14.1 full-corpus gate. EDCM consumes those unchanged surfaces
from exact UCNS v0.19 producer
`872f53571d5dc2f133ff1813b7bdffd3a9c309f8`.

The adapter activates only for `ucns.profile.edcm-word-gonol/0.2.0` with all
fourteen fixed options, `source_domain=unicode-scalar-values`, the exact
157-token public gonol digest, and the exact ordered 25-value pin behind
`space_assignment=unicode-white-space-origin-v1`. Consume
ordered `ucns_turns` as exact `(speaker_id, text)` tuples. Never infer speaker
turns from a flattened transcript, sample a corpus, or normalize source text.

Every word is a maximal sequence not assigned to carrier position zero. Each
pinned Unicode SPACE manifestation is assigned to the public SPACE carrier at
position zero and emitted as an explicit superpositioned nesting boundary.
Source value/code point and carrier token/position are serialized separately,
so tab, newline, and non-breaking space remain exact source witnesses. Each
complete speaker turn has support one. True non-SPACE out-of-alphabet code
points remain ordered positive evidence.

UCNS v0.19 also exposes a nonselected trace-local source-coordinate candidate
for exact initiated outcome evidence. This adapter does not attach or consume
that candidate, so profile observation remains distinct from coordinate
assignment, formal higher geometry, and EDCM measurement validity.

Prefer `has_carrier_assignment`, `is_public_gonol_token`,
`carrier_unassigned`, and `has_complete_carrier_assignment`. The older
`in_alphabet`, `out_of_alphabet`, and `has_complete_alphabet_coverage` names
remain compatibility aliases only.

The retired inputs fail closed:

```text
ucns_object
ucns_bridge_record
ucns_bridge_record_json
ucns_bridge_record_dict
ucns_factorization_evidence
ucns_factorization_evidence_json
ucns_factorization_evidence_dict
```

The live package must not expose `edcm.ucns_metrics` or its former scalar-to-object resolver names. That path required archived `UCNSObject`, `recursive_encode`, and `stable_hash` surfaces and was removed after the reset. Current callers use exact `ucns_profile_observation`; a scalar projection requires a separately versioned, trajectory-linked, declared-loss contract.

Independent status fields are:

```text
ucns_package_available
ucns_adapter_active
ucns_profile_observation_attached
ucns_object_attached
ucns_bridge_record_attached
ucns_scope_metadata_attached
ucns_factorization_evidence_attached
ucns_negative_certification_attached
ucns_theorem_status_attached
```

Package availability alone attaches nothing. Exact ordered turns attach only
`ucns_profile_observation`. Geometry, factorization, certification, theorem
status, and measurement-validity transfer remain absent. Direct absence of
`ucns` is typed profile absence; transitive failures and profile drift remain
visible.

## Layer and result behavior

`build_default_layers(policy_manifest=None)` assembles:

1. composite semantics: independent METAPAT authority and UCNS observation-profile sublayers;
2. canonical `edcm.measurement`;
3. canonical shared-stack composition;
4. canonical final result-contract delivery.

Layer provenance records remain separate:

```text
semantic_authority
ucns_profile
semantics
measurement
composition
delivery
```

Every supported pipeline result includes `edcm_result` schema `edcm.shared-stack-result/1.2.0` with:

```text
source_evidence
metapat_semantic_constraints
ucns_profile_observation
ucns_geometry_identity
ucns_factorization_evidence
edcm_policy_manifest
implementation_provenance
readouts
status_evidence
unresolved_constraints
```

`epoch_identity` binds METAPAT canon/provenance, the exact UCNS profile
configuration and source commit, the EDCM manifest, and implementation
selection. `result_identity` additionally binds source evidence, full profile
observations, readouts, independently attached evidence, and attachment states.

## Object and proof boundaries

`ConstraintField`, `FieldMotion`, metric axes, readouts, windows, and operator
turns are EDCM objects. They are not substitutes for formal UCNS geometry.

Keep source evidence, METAPAT semantic authority, UCNS profile observations,
UCNS geometry identity, UCNS status evidence, EDCM policy identity, and EDCM
readouts separate.

UCNS equality does not imply EDCM measurement equivalence. UCNS or METAPAT theorem/domain/certification status is attached evidence only and never promotes EDCM empirical validity.

Every UCNS evidence view preserves:

```text
theorem_status_transfer = false
measurement_validity_claim = false
proof_status_transfers_to_measurement_validity = false
```

## Non-negotiable guardrails

- `NA != 0`.
- No-bone, empty-field, absent-adapter, missing-context, and absent-evidence cases remain typed absence or `NA`.
- Ordered windows compose with `SeqAppend`; never average testimony-bearing order.
- METAPAT semantic labels never become measured values merely by being named.
- Deterministic transcript metrics do not establish diagnosis, intent, consciousness, external truth, or root ontology.
- UCNS observation digests establish content identity, not signed producer authentication.

These frontier gates remain non-operational until their named falsifiers and tests exist:

- contact convergence;
- DA geometry correlation;
- cadence admission from text;
- semantic-label-to-operating-state inference.

Do not replace `NotImplementedError` with constants, heuristics, language-model judgments, or decorative numbers.

## Testing expectations

Base tests pass without UCNS or METAPAT installed. Integration tests use actual pinned sibling packages.

The UCNS profile suite must prove:

- exact profile and option drift fail closed;
- all supplied turns remain ordered and retain exact Unicode source witnesses;
- every pinned SPACE manifestation has carrier position zero without source normalization;
- the exact 25-value SPACE pin and Unicode-scalar source domain drift fail closed;
- each speaker turn has support one;
- true non-SPACE out-of-alphabet evidence is retained;
- a flattened transcript does not invent speaker-turn boundaries;
- package availability alone attaches no observation;
- profile evidence never becomes geometry, factorization, theorem, or measurement validity.

The full-stack fixture proves identity separation, deterministic measurement, `NA != 0`, fail-closed producer validation, canon/manifest epoch rotation, and no proof-status transfer.

The integrity suite must include adversarial byte mutation, added/missing canon files, authority reversal, and no-fork identity checks.

Optional skips are explicit. Fake sibling implementations may test adversarial construction but never count as integration success.

## msdmd and skill-lib

- New EDCM-native modules begin with accurate `MODULE_BUILD` blocks.
- Changed native modules cite real tests and actual dependencies.
- Tests carry no `MODULE_BUILD` block.
- Historical measurement modules retain provenance until the explicit metadata-reconciliation pass.
- Code and documentation include runnable usage guidance, integration notes, limitations, and `hmmm` boundaries.
- EDCM vendors the bounded build/evidence subset from
  `The-Interdependency/skill-lib@2b24be24947223b86440f59f1bd9766130f9cc11`.
  The canonical drift checker and msdmd collector run in
  `.github/workflows/skill-compliance.yml`; repo-local copies are consumers,
  never authority.

## hmmm

Still unresolved:

- cryptographically signed UCNS producer or transport authentication;
- mutation-level verification for the repository-wide CONTRACTS/CHECKS graph;
- remaining historical L0/L1/L2/L3 split, P assignment, matrix wiring, bidirectional alerts, and Bridge-home decisions.

These unresolveds do not reopen measurement authority, semantic-authority ownership, canonical evidence schemas, certification policy, integrity guarantees, or the proof-transfer firewall.
