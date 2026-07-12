# Shared UCNS / METAPAT / EDCM result contract

## Purpose

`edcm.shared_stack` emits one deterministic review record without collapsing the identities of the systems that contributed to it.

The contract is available at:

```python
result = edcm.build_default_layers().run(payload)
contract = result["edcm_result"]
```

Schema:

```text
schema_id: edcm.shared-stack-result
schema_version: 1.0.0
```

## Compartments

### `source_evidence`

Identifies what was measured through source reference, SHA-256 digest, UTF-8 size, and character count. Empty input is typed `NA`; raw text remains in the caller payload rather than being duplicated inside the contract.

### `metapat_semantic_constraints`

Contains only validated METAPAT semantic authority and provenance:

```text
schema id/version
module id/kind
canon version/digest
source statement references
source statements
constraints
permitted interpretations
unresolved constraints
provenance digest
```

No field is interpreted as an EDCM metric value.

### `ucns_geometry_identity`

Contains actual UCNS geometry evidence derived through `ucns.object_record`, including stable hash, serialization schema, structural facts, and typed domain prerequisite metadata.

It does not certify a concrete negative factorization result and does not promote EDCM measurement validity.

### `edcm_policy_manifest`

Contains the canonical JSON, parsed policy fields, and manifest hash for the `PolicyManifest` supplied to `build_default_layers()`.

### `implementation_provenance`

Records the selected implementations for:

```text
semantic_authority
geometry
semantics
measurement
composition
delivery
```

Each record identifies version, source, role, selection state, canonical/fallback state, unresolved constraints, and loading errors.

### `readouts`

Contains deterministic transcript readouts when a non-empty transcript was measured. Otherwise every absent readout is represented by typed `NA` and `None`, never numeric zero.

### `status_evidence`

Keeps attachment states independent and pins the firewalls:

```text
proof_status_transfers_to_measurement_validity = false
semantic_labels_are_measurement_values = false
```

## Identity rules

`epoch_identity` changes when any readout-governing context changes:

- METAPAT canon digest;
- METAPAT provenance digest;
- UCNS stable hash or serialization schema;
- EDCM policy-manifest hash;
- selected semantic, geometry, or measurement implementation.

`result_identity` additionally binds source evidence and measured readouts.

Changing a METAPAT canon digest or EDCM manifest creates a new identity epoch. Historical results are not rewritten in place.

## Full-stack usage

```python
import edcm
import metapat

envelope = metapat.root_spine_module_envelope()
adaptation = metapat.adapt_envelope_to_ucns(envelope)

result = edcm.build_default_layers().run({
    "transcript": "A: Preserve the boundary.",
    "source_ref": "example://root-spine",
    "metapat_envelope": envelope,
    "ucns_object": adaptation.ucns_object,
})

contract = result["edcm_result"]
```

## Failure behavior

The pipeline fails closed for:

- multiple METAPAT envelope forms in one payload;
- non-METAPAT objects supplied as `metapat_envelope`;
- malformed or unknown serialized METAPAT fields;
- invalid METAPAT provenance digest;
- unsupported METAPAT or UCNS schema versions;
- non-UCNS objects supplied as `ucns_object`;
- transitive import failures inside optional sibling packages.

Only direct absence of an optional sibling becomes typed unavailability.

## hmmm

Official serialized UCNS bridge-record ingestion and validated negative-certification/theorem-status evidence envelopes remain unresolved. Until canonical schemas exist, their attachment flags remain false.
