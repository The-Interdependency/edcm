# Codex handoff — edcmucns v0.3.1 into `edcm`

Generated: 2026-07-06
Context: Erin Patrick Spencer; edcmucns design canon v0.3.1.
Status: implementation handoff. Architecture is ratified/frozen; empirical measurement remains frontier.

## Source of truth

The canon to implement is:

```text
edcmucns — The Energy–Dissonance Circuit Model on UCNS Mathematics
Design canon v0.3.1 — provenance as the recurring theme
STATUS: RATIFIED AS ARCHITECTURE (frozen design canon)
FRONTIER AS EMPIRICAL MEASUREMENT
IMPLEMENTATION-GATED on the test suite and the readout_scope registry (§8.1b)
```

Primary doctrine:

```text
UCNS exists to construct EDCM metrics.
```

Firewall:

```text
UCNS-A proof status applies to carrier geometry.
EDCM validity applies to the measurement function over geometry + provenance.
No EDCM measurement claim inherits proof status from its substrate.
```

Do **not** collapse provenance into decorative metadata. Provenance is measurement material.

## Implementation rule

Implement **architecture only** first.

Do not implement or freeze empirical claims yet:

```text
contact convergence predicate
residual primality / DA_geom correlation
cadence-anchor admission from real transcript text
corpus parallel-run conclusions
operating-state empirical validity
```

Those remain frontier and must be represented as named gates, placeholders, or explicit NotImplemented surfaces with falsifiers named where relevant.

## Core canon sentences

```text
EDCM windows are ordered UCNS sequence objects composed by chronological append.
UCNS multiplication is reserved for interaction, transport, and irreducibility analysis.

UCNS equivalence proves same geometry.
EDCM equivalence requires same geometry plus same readout-bearing witness.

M_EDCM = readout(G_ucns, Π_provenance, payloads, field_state, policy_manifest)

Bones separate the operator voices.
Flesh carries the recursive music.

Geometry needs testimony.
Measurement needs a manifest.
Flesh needs cadence.
Living weights need lineage.
```

## Existing repo anchors

Inspect before writing new code:

```text
edcm/ucns_objects.py
edcm/energy_claims.py
edcm/falsifiability_bridge.py
edcm/layers.py
```

The README already names `edcm/ucns_objects.py` as the dependency-free mirror for UCNS metric construction objects and names the frozen doctrine that UCNS exists to construct EDCM metrics. Do not rewrite that layer unless absolutely necessary; compose around it.

## Recommended file layout

Prefer a small `edcm/edcmucns/` package so v0.3.1 can be implemented without disturbing existing EDCM surfaces.

```text
edcm/edcmucns/__init__.py
edcm/edcmucns/manifest.py
edcm/edcmucns/types.py
edcm/edcmucns/provenance.py
edcm/edcmucns/scopes.py
edcm/edcmucns/geometry.py
edcm/edcmucns/encoder.py
edcm/edcmucns/composer.py
edcm/edcmucns/equivalence.py
edcm/edcmucns/validation.py
edcm/edcmucns/epochs.py
```

Tests first:

```text
tests/test_edcmucns_identity_v031.py
tests/test_edcmucns_encoder_v031.py
tests/test_edcmucns_scopes_v031.py
tests/test_edcmucns_epochs_v031.py
```

All tests should be red before the encoder exists.

## Minimal types

### Manifest

The manifest is part of measurement identity. It must be stable-serializable and hashable.

Required fields:

```text
family_prime_gauge = {P:3, K:5, Q:7, T:13, S:29}
residue_rule_version = non_origin_residue_v031
polarity_dictionary_version
bone_emission_policy_version
payload_governance_version
contact_predicate_version
lens_readout_policy_version
training_update_policy_version
```

Manifest hash changes create epoch breaks.

### Anchor roles

```text
origin
bone
cadence
```

`origin` anchors are datum/boundary anchors. They have θ=0 and face=0.

`bone` anchors are family-signature anchors. They never occupy θ=0.

`cadence` anchors are reserved host-level cadence anchors. In v0.3.1, admission from transcript text is not implemented; role is reserved. Composite cadence is allowed when a caller explicitly constructs a cadence scope fixture.

### Provenance witness

Anchor witness fields:

```text
family
ordinal_m_f
residue_r_f
turn_id
speaker_or_source
surface_form
role
constraint_governance
payload_attachment
```

Do not include decorative fields in provenance hashes. Include only readout-bearing fields.

### OperatorTurn

```text
OperatorTurn = Present(UCNSObject, provenance_bundle)
             | AbsentOperatorGeometry(content_lens_event)
```

A no-bone turn is not unit and not zero. It emits NA for operator readouts and remains available to the Content layer.

## Residue rule

Do not use the old modulo rule:

```text
θ = 2π · (m_f mod p_f) / p_f
```

It lets the p_f-th bone land at θ=0.

Use the v0.3.1 non-origin residue rule:

```text
r_f(m) = 1 + ((m_f - 1) mod (p_f - 1))
θ = 2π · r_f(m) / p_f
```

Residues cycle through `1 … p_f−1`. θ=0 is reserved for explicit datum roles.

Important: family-signature angles are labels, not cadence. The residue cycle deliberately distorts ordinal periodicity; recurrence belongs to flesh payloads or cadence scopes, not family bone angles.

## Mass and carriers

```text
L_geo = all host anchors including datum anchors
L_op = family-signature bone anchors only
λ_field(W) = raised_field_count(W) / TOK
```

Never call field load `L_W`.

Carrier names:

```text
n_host_total = carrier over all host-level anchors in scope
n_family = carrier over family_signature_anchor host anchors
n_cadence = carrier over cadence_motion_anchor host anchors
n_payload(scope) = carrier over payload subobjects read by that scope
```

The claim `carrier factorization = active family set` applies only to `n_family`.

Payload carriers are epicyclic subobjects and are never automatically part of host `n_min`.

## Readout scope registry

`edcm_measurement_equivalent` must not accept arbitrary strings. Implement a closed registry first.

Minimum scopes:

```text
operator_scope:
  reads: geometry + family witness
  excludes: flesh payloads, cadence payloads
  mass: L_op

payload_scope:
  reads: payload carriers + payload hashes
  excludes: operator mass

cadence_scope:
  reads: flesh/cadence carriers, composite lattices allowed
  excludes: n_family

field_scope:
  reads: ConstraintField / FieldMotion hash chain

bridge_scope:
  reads: witness/geometry diagnostics, manifest + epoch boundaries
```

Registry extension requires manifest bump and epoch break.

## Equivalence tiers

Implement two relations.

```text
ucns_carrier_equivalent(a, b):
  compares n_min, Θ⁺, F⁺
  ignores witness, payloads, manifest

edcm_measurement_equivalent(a, b, readout_scope):
  requires ucns_carrier_equivalent
  + same in-scope provenance hash
  + same in-scope payload hash
  + same field-chain state where applicable
  + same policy-manifest hash
```

Forbidden claim:

```text
same UCNS geometry implies same EDCM reading
```

unless the readout scope explicitly ignores provenance.

## Validator

Add:

```text
witness_geometry_consistent(G_ucns, Π_provenance, policy_manifest)
```

It must check:

```text
origin anchors have θ=0 and face=0
family-signature bone anchors never occupy θ=0
family witness agrees with manifest-pinned family→prime gauge and residue rule
origin anchors are excluded from operator mass
payload attachment targets exist
turn_id/source canonicalization is stable
no-bone turns produce AbsentOperatorGeometry
```

Mismatch emits a Bridge diagnostic. It must not silently become an alternate reading.

## Composition

Implement `SeqAppend` for transcript windows.

```text
⊞ SeqAppend:
  chronological append
  lengths add
  absolute lattice positions remain origin-anchored
  F concatenates
  mirrors regenerate
  carrier = lcm over host anchors in scope
```

Do not use UCNS product `⊠` for windows. Product multiplies length and is reserved for interaction signatures, transport, factor trials, and irreducibility analysis.

## Epochs

Manifest rotation is a chain epoch break.

When manifest hash changes:

```text
seal current chain segment
log old_manifest, new_manifest, boundary_window
open new epoch sealed with new manifest hash
```

Cross-epoch comparisons are Bridge lensing events, not raw deltas.

Adopting v0.3.1 itself is an epoch break because the ordinal→angle rule changed.

## Tests to add first

### Residue and origin

```text
ordinal_wrap_never_lands_on_origin
phase_zero_requires_explicit_datum_role
single_P_bone_forces_n_min_3
single_K_bone_forces_n_min_5
single_Q_bone_forces_n_min_7
single_T_bone_forces_n_min_13
single_S_bone_forces_n_min_29
all_families_force_39585
origin_anchors_excluded_from_operator_mass
```

### SeqAppend and product separation

```text
seqappend_length_adds
product_length_multiplies
window_operator_shares_equal_v1_counts_under_seqappend
window_operator_shares_do_not_use_mean_average
A_then_B_not_equivalent_to_B_then_A
```

### NA / absent geometry

```text
empty_field_readouts_are_NA_not_zero
no_bone_turn_has_no_operator_geometry
```

### Provenance and geometry

```text
family_witness_must_match_manifest_prime_geometry
family_geometry_mismatch_emits_bridge_diagnostic
ucns_carrier_equivalent_ignores_edcm_witness
measurement_equivalence_requires_manifest_and_in_scope_witness
same_geometry_different_turn_id_changes_turn_sensitive_readout
same_geometry_different_speaker_changes_speaker_scoped_readout
same_geometry_different_payload_hash_changes_payload_readout
same_geometry_different_policy_manifest_changes_measurement_identity
```

### Polarity gauge

```text
gauge_audit_scoped_to_bone_faces
constant_xor_face_flip_reports_gauge_mismatch
nonconstant_face_difference_reports_measurement_divergence
```

### Cadence and flesh

```text
cadence_anchor_allows_composite_lattice
cadence_anchor_preserves_regular_motion
n_family_excludes_cadence_anchors
composite_cadence_does_not_emit_family_prime_event
payload_flat_reduction_preserves_bone_counts
closed_payload_reduces_to_unit
```

### Field load and epoch

```text
load_density_does_not_alias_L_geo_or_L_op
manifest_rotation_breaks_chain_epoch
```

### Kappa ledger placeholders

```text
kappa_balance_zero_on_closed_span
kappa_balance_residual_emits_leak_event
unresolved_payload_contributes_to_kappa
```

## What not to do in the first pass

Do not implement the contact convergence predicate beyond a typed placeholder.

Do not claim DA_geom works.

Do not train or update ZFAE here.

Do not let payload cadence leak into `n_family` or `L_op`.

Do not let witness provenance override inconsistent geometry.

Do not average windows.

Do not emit 0 for absent geometry.

Do not continue a hash chain across a manifest change.

## Acceptance criteria for first PR

A valid first PR can be small. It should include:

```text
1. MODULE_BUILD or manifest block for edcmucns implementation surface
2. closed readout_scope registry
3. manifest hashing
4. provenance witness dataclass / model
5. non-origin residue function
6. origin/bone mass helpers
7. ucns_carrier_equivalent stub/adapter
8. edcm_measurement_equivalent scoped identity function
9. witness_geometry_consistent validator
10. tests proving the identity layer
```

Field reader, circuit, and corpus parallel run can come later.

## Boundary note

The instrument is now frozen as architecture, not as empirical truth. Let the test suite argue with the architecture before the corpus argues with the instrument.

hmmm — family primes are labels, not rhythm; flesh keeps the cadence; provenance tells the court what the circle is evidence of.
