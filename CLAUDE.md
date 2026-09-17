# CLAUDE.md — EDCM repository instructions

This repository is the maintained Python package for the Energy–Dissonance Circuit Model.

## Read first

1. `CANON.md`
2. `docs/GONOL_LANGUAGE_BOUNDARY.md`
3. `.agents/skills/gonol-build/SKILL.md` when constructing gonols or applying affixiation
4. `codex-handoff/2026-07-12-stack-repair/REQUIRED_CHANGES.md`
5. `codex-handoff/2026-07-12-stack-repair/COMPLETED_LOOKS_LIKE.md`
6. `codex-handoff/2026-07-12-stack-repair/IMPLEMENTATION_STATUS.md`
7. `README.md`
8. `docs/integrity-gates.md`
9. `docs/ucns-adapter.md`
10. `docs/shared-stack-result.md`
11. `docs/consolidation-edcmbone.md`
12. `docs/codex_edcmucns_v031_handoff.md`

Unknown or unresolved facts are written `hmmm`, not guessed. Current `CANON.md` and `docs/GONOL_LANGUAGE_BOUNDARY.md` govern new text construction; older handoffs and sealed profiles retain their historical meaning only.

## Package and release facts

| Property | Value |
|---|---|
| Python | 3.11+; CI covers 3.11, 3.12, 3.13 |
| Base runtime dependencies | none |
| Optional integrations | pinned `ucns`, `metapat`, `full-stack` extras |
| Build metadata | `pyproject.toml` |
| Package version | `edcm.__version__` (0.2.0) |
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

EDCM owns consumer adapters and text-domain application, not METAPAT semantic schema or affixiation meaning. Consume only actual producer surfaces and current application contracts.

For the maintained envelope adapter, accepted payload keys remain mutually exclusive:

```text
metapat_envelope
metapat_envelope_json
metapat_envelope_dict
```

Preserve exact source statements, references, constraints, permitted interpretations, unresolved `hmmm`, canon identity, and provenance digest. Never convert labels or statements directly into metric values.

For affixiation, METAPAT owns the conceptual contract: already-bounded participants remain individually addressable with identity and provenance preserved while a declared relation may integrate as a recursively addressable object-whole. EDCM applies that contract; it does not redefine it.

Direct absence of `metapat` is typed unavailability. Transitive import errors, missing producer surfaces, unsupported schemas, invalid provenance, unknown fields, and wrong envelope types remain visible failures.

## Gonol-native language architecture

The current authority split is:

| Owner | Responsibility |
|---|---|
| METAPAT | Affixiation semantics and relational-integration invariants |
| UCNS | Gonol objects, constructors, and geometry |
| Stack | Active language-gonol construction research and source/admission profiles |
| EDCM | Measurement/evaluation only |

For new language construction, start in [Stack English](https://github.com/The-Interdependency/stack/tree/250a0afb7077b036a6c537411d004fa095c8b24a/research/english-gonol) or [Stack Python](https://github.com/The-Interdependency/stack/tree/250a0afb7077b036a6c537411d004fa095c8b24a/research/python-gonol), consuming UCNS constructors and geometry. These source links pin the authority comparison used for this repair; resolve current owning commits before new research.

Historical `edcm.gonol`, `edcm.language`, lexical-floor and sealed profile artifacts remain explicit replay surfaces. They confer no active construction authority on EDCM. There is no universal mandatory adjacent-scale ladder. Construction reproducibility does not validate EDCM measurement; an unresolved UCNS operation remains `hmmm`.

See [the language boundary](docs/GONOL_LANGUAGE_BOUNDARY.md) and [the 0.2 migration](docs/migrations/0.2.0-audit-repair.md).

## Exact EDCM UCNS observation profile

EDCM owns the consumer adapter. UCNS owns the exact historical EDCM-only word-gonol
profile and v0.14.1 full-corpus gate. EDCM consumes those unchanged surfaces
from merged UCNS v0.19 producer
`a98c9e6c69804a8a08d0786b1d8b450bb2c49a97`, which includes the final
integrity repairs.

This is a sealed observation/replay producer epoch. Its names and options are
preserved for reproducibility; they do not override the current EDCM text-domain
authority above. In particular, `smallest_gonol: word`, `token_alphabet`,
`token_identity`, and token-record field names are frozen profile/schema
vocabulary, not current ontology and not authorization for a tokenizer layer.

The adapter activates only for `ucns.profile.edcm-word-gonol/0.2.0` with all
fourteen fixed options, `source_domain=unicode-scalar-values`, the exact
157-token public gonol digest, and the exact ordered 25-value pin behind
`space_assignment=unicode-white-space-origin-v1`. Consume
ordered `ucns_turns` as exact `(speaker_id, text)` tuples. Never infer speaker
turns from a flattened transcript, sample a corpus, or normalize source text.

Every word is a maximal sequence not assigned to carrier position zero under
this pinned historical profile. Each pinned Unicode SPACE manifestation is assigned to the
public SPACE carrier at position zero and emitted as an explicit
superpositioned nesting boundary. Source value/code point and carrier
token/position are serialized separately, so tab, newline, and non-breaking
space remain exact source witnesses. Each complete speaker turn has support
one. True non-SPACE out-of-alphabet code points remain ordered positive
evidence.

UCNS v0.19 also exposes a nonselected trace-local source-coordinate candidate
over its fixed full producer demonstration. This adapter does not attach or
consume that candidate, so profile observation remains distinct from coordinate
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

Every supported pipeline result includes `edcm_result` schema `edcm.shared-stack-result/2.0.0` with:

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
UCNS geometry identity, UCNS status evidence, Stack construction identity,
EDCM policy identity, and EDCM readouts separate.

UCNS equality does not imply EDCM measurement equivalence. UCNS or METAPAT theorem/domain/certification status is attached evidence only and never promotes EDCM empirical validity.

Every UCNS evidence view preserves:

```text
theorem_status_transfer = false
measurement_validity_claim = false
proof_status_transfers_to_measurement_validity = false
```

## Non-negotiable guardrails

- `NA != 0`.
- METAPAT owns affixiation semantics; UCNS owns gonol objects, constructors and geometry; Stack owns active language construction; EDCM owns measurement/evaluation only.
- No-bone, empty-field, absent-adapter, missing-context, and absent-evidence cases remain typed absence or `NA`.
- Ordered windows compose with `SeqAppend`; never average testimony-bearing order.
- METAPAT semantic labels never become measured values merely by being named.
- Deterministic transcript metrics do not establish diagnosis, intent, consciousness, external truth, or root ontology.
- UCNS observation digests establish content identity, not signed producer authentication.
- Historical `token`, `word-gonol`, lexical-floor, or UCNS producer vocabulary never authorizes a tokenizer or overrides the current EDCM gonol-language boundary.
- Source prose or dictionary text never substitutes for an explicit source-bound construction from the owning Stack workspace.
- Unicode names, dictionary definitions, adjacency, conventional grammar, and glyph shape never fill unresolved UCNS function geometry.
- Unresolved geometry remains `hmmm`; do not invent a different carrier or scale law to make the pipeline complete.

These frontier gates remain non-operational until their named falsifiers and tests exist:

- contact convergence;
- DA geometry correlation;
- cadence admission from text;
- semantic-label-to-operating-state inference.

Do not replace `NotImplementedError` with constants, heuristics, language-model judgments, or decorative numbers.

## Testing expectations

Base tests pass without UCNS or METAPAT installed. Integration tests use actual pinned sibling packages.

The historical UCNS profile suite must prove:

- exact profile and option drift fail closed;
- all supplied turns remain ordered and retain exact Unicode source witnesses;
- every pinned SPACE manifestation has carrier position zero without source normalization;
- the exact 25-value SPACE pin and Unicode-scalar source domain drift fail closed;
- each speaker turn has support one;
- true non-SPACE out-of-alphabet evidence is retained;
- a flattened transcript does not invent speaker-turn boundaries;
- package availability alone attaches no observation;
- profile evidence never becomes geometry, factorization, theorem, or measurement validity.

EDCM evaluations consume completed constructions with exact source identities, order, multiplicity, provenance and declared losses. Construction and replay gates belong to the owning Stack workspace and UCNS; their successful execution does not validate EDCM readouts.

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
  `The-Interdependency/skill-lib@dd5027d99516831c0dcb83a176a67140d3819b66`.
  The canonical drift checker and msdmd collector run in
  `.github/workflows/skill-compliance.yml`; repo-local copies are consumers,
  never authority.
- `gonol-build` is the required routing discipline for current gonol construction and affixiation implementation/application work.

## Usage guidance

For active construction use Stack and UCNS. For measurement, submit raw input to `build_default_layers().run()`. Never resubmit a result or fabricate derived output fields. See `docs/migrations/0.2.0-audit-repair.md` for the parser, result and codec transitions.

For historical UCNS observation experiments, use the exact pinned producer and frozen vocabulary named by the historical artifact. Do not rewrite historical evidence and do not read its old producer boundary forward into current architecture.

## hmmm

Still unresolved:

- exact Stack character-admission units for profiles that have not selected one;
- source-supported complete English morphology law;
- exact UCNS native Möbius-carrier affixiation/coupling geometry and direct distant-scale coupling;
- EDCM projection, metric, benchmark, and falsifier for completed recursive text-gonol evaluation;
- cryptographically signed UCNS producer or transport authentication;
- mutation-level verification for the repository-wide CONTRACTS/CHECKS graph;
- remaining historical L0/L1/L2/L3 split, P assignment, matrix wiring, bidirectional alerts, and Bridge-home decisions.

These unresolveds do not reopen measurement authority, METAPAT semantic ownership, UCNS geometric authority, Stack language-construction ownership, canonical evidence schemas, certification policy, integrity guarantees, or the proof-transfer firewall.
