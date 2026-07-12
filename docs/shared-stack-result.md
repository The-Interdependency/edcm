# Shared UCNS / METAPAT / EDCM result contract

## Purpose

`edcm.shared_stack` emits one deterministic review record without collapsing the identities of the systems that contributed to it.

```python
result = edcm.build_default_layers().run(payload)
contract = result["edcm_result"]
```

Schema:

```text
schema_id: edcm.shared-stack-result
schema_version: 1.1.0
```

Version 1.1.0 adds an explicit canonical UCNS factorization-evidence compartment and binds that evidence into result identity.

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

Contains one validated canonical UCNS bridge record projected into EDCM's read-only evidence view:

```text
bridge schema and producer identity
bridge evidence digest
canonical UCNS serialization version
stable object hash
canonical JSON
typed domain statuses and completeness prerequisite
SEQ-PRIME claim scope
structural facts and unit/frontier flags
```

A live `UCNSObject` is converted through `ucns.bridge_record()`. Serialized records are validated through the producer's own constructors.

### `ucns_factorization_evidence`

Contains one optional authoritative `ucns.UCNSFactorizationEvidence` view:

```text
factorization evidence schema and producer identity
evidence digest and product hash
result kind and factor stable hashes
negative-certification state and claim scope
certification policy version
search exhaustion and truncation
catalogue source, sizes, and fingerprints
coverage validation and search-report binding
pruning rule/version and coverage preservation
explicit uncertified reasons
```

The producer record must bind to the same object hash as `ucns_geometry_identity`. Absence is typed `NA`. An attached but uncertified record remains evidence while `ucns_negative_certification_attached` stays false.

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

Keeps attachment states independent:

```text
ucns_bridge_record_attached
ucns_factorization_evidence_attached
ucns_theorem_status_attached
ucns_negative_certification_attached
metapat_theorem_status_attached
proof_status_transfers_to_measurement_validity = false
semantic_labels_are_measurement_values = false
```

Content digests are verified. Version 1 records do not claim cryptographic producer signatures.

## Identity rules

`epoch_identity` changes when readout-governing context changes:

- METAPAT canon or provenance digest;
- UCNS stable hash, canonical schema, or bridge evidence digest;
- EDCM policy-manifest hash;
- selected semantic, geometry, or measurement implementation.

`result_identity` additionally binds:

- source evidence;
- measured readouts;
- attached UCNS factorization evidence;
- status-evidence attachment states.

Factorization evidence changes result identity but not measurement epoch identity because it is status evidence rather than readout-governing geometry or policy.

Changing a METAPAT canon digest or EDCM manifest creates a new identity epoch. Historical results are not rewritten in place.

## Full-stack usage

```python
import edcm
import metapat
import ucns

envelope = metapat.root_spine_module_envelope()
adaptation = metapat.adapt_envelope_to_ucns(envelope)

result = edcm.build_default_layers().run({
    "transcript": "A: Preserve the boundary.",
    "source_ref": "example://root-spine",
    "metapat_envelope": envelope,
    "ucns_object": adaptation.ucns_object,
})

contract = result["edcm_result"]
assert contract["ucns_geometry_identity"]["stable_hash"] == ucns.stable_hash(
    adaptation.ucns_object
)
assert contract["ucns_factorization_evidence"]["state"] == "NA"
```

## Certified-evidence usage

```python
bridge = ucns.bridge_record(ucns.S2)
evidence = ucns.factorization_evidence(ucns.S2)

result = edcm.build_default_layers().run({
    "transcript": "A: Preserve authoritative status evidence.",
    "ucns_bridge_record_json": bridge.to_json(),
    "ucns_factorization_evidence_json": evidence.to_json(),
})

contract = result["edcm_result"]
assert contract["ucns_factorization_evidence"]["negative_result_certified"] is True
assert contract["status_evidence"]["ucns_negative_certification_attached"] is True
assert contract["status_evidence"]["proof_status_transfers_to_measurement_validity"] is False
```

## Failure behavior

The pipeline fails closed for:

- multiple METAPAT envelope forms;
- malformed or unknown serialized METAPAT fields;
- invalid METAPAT provenance digest;
- multiple UCNS geometry forms;
- multiple UCNS factorization-evidence forms;
- factorization evidence without geometry;
- factorization product hash different from geometry stable hash;
- unknown, missing, coerced, tampered, or unsupported UCNS producer fields;
- non-METAPAT, non-UCNS, or wrong record object types;
- unsupported METAPAT or UCNS schema versions;
- transitive import failures inside optional sibling packages.

Only direct absence of an optional sibling becomes typed unavailability.

## hmmm

UCNS evidence digests are content identities, not signed producer attestations. Signed transport or producer authentication remains unresolved without weakening canonical record validation or the proof-transfer firewall.
