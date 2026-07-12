# EDCM UCNS adapter

## Purpose

EDCM owns the consumer contract it needs. UCNS owns the algebra, canonical serialization, bridge-record schema, factorization policy, and certification evidence.

EDCM consumes these actual public UCNS surfaces:

```text
ucns.UCNSObject
ucns.UCNSBridgeRecord
ucns.UCNSFactorizationEvidence
ucns.bridge_record
ucns.CANONICAL_SERIALIZATION_VERSION
ucns.BRIDGE_RECORD_SCHEMA_ID / VERSION
ucns.FACTORIZATION_EVIDENCE_SCHEMA_ID / VERSION
```

EDCM does not expect UCNS to expose an EDCM-specific `SemanticsLayer` and does not duplicate producer schemas.

## Install

```bash
python -m pip install -e ".[dev,ucns]"
```

The `ucns` extra is pinned to the verified producer commit that introduced canonical evidence envelopes.

## Geometry input

Supply exactly one geometry form:

```text
ucns_object
ucns_bridge_record
ucns_bridge_record_json
ucns_bridge_record_dict
```

### Live object

```python
import edcm
import ucns

obj = ucns.S2
result = edcm.build_default_layers().run({"ucns_object": obj})

assert result["ucns_geometry"]["stable_hash"] == ucns.stable_hash(obj)
assert result["ucns_integration"]["ucns_object_attached"] is True
assert result["ucns_integration"]["ucns_bridge_record_attached"] is True
```

The live object is immediately converted through `ucns.bridge_record()`. EDCM does not maintain an alternate object inspector.

### Serialized bridge record

```python
bridge = ucns.bridge_record(ucns.S2)
result = edcm.build_default_layers().run({
    "ucns_bridge_record_json": bridge.to_json(),
})

assert result["ucns_geometry"]["bridge_evidence_digest"] == bridge.evidence_digest
assert result["ucns_integration"]["ucns_object_attached"] is False
assert result["ucns_integration"]["ucns_bridge_record_attached"] is True
```

JSON and mapping forms are validated through UCNS's own `from_json()` and `from_dict()` constructors. The producer verifies canonical JSON, stable hash, exact fields, strict types, schema identity, producer identity, and evidence digest.

## Factorization evidence input

After attaching geometry, optionally supply exactly one:

```text
ucns_factorization_evidence
ucns_factorization_evidence_json
ucns_factorization_evidence_dict
```

```python
bridge = ucns.bridge_record(ucns.S2)
evidence = ucns.factorization_evidence(ucns.S2)

result = edcm.build_default_layers().run({
    "transcript": "A: Preserve the evidence boundary.",
    "ucns_bridge_record": bridge,
    "ucns_factorization_evidence": evidence,
})

assert result["ucns_integration"]["ucns_factorization_evidence_attached"] is True
assert result["ucns_integration"]["ucns_negative_certification_attached"] is True
assert result["ucns_factorization_evidence"]["evidence_digest"] == evidence.evidence_digest
```

The factorization record must have the same `product_hash` as the attached geometry `stable_hash`. A mismatch fails closed.

## Independent status fields

Every integration report distinguishes:

```text
ucns_package_available
ucns_adapter_active
ucns_object_attached
ucns_bridge_record_attached
ucns_scope_metadata_attached
ucns_factorization_evidence_attached
ucns_negative_certification_attached
ucns_theorem_status_attached
```

Package import alone sets only package availability and adapter activation. No object, bridge, scope, theorem, factorization, or negative-certification attachment is inferred.

A bridge record attaches typed UCNS domain-status evidence. Negative certification attaches only when a matching authoritative factorization record states `negative_result_certified = true` after producer validation.

An uncertified result remains attached evidence while the certification flag stays false:

```python
evidence = ucns.factorization_evidence(ucns.S2, catalogue=[])
assert not evidence.negative_result_certified
```

## Result contract

Result schema `edcm.shared-stack-result/1.1.0` includes separate compartments:

```text
ucns_geometry_identity
ucns_factorization_evidence
status_evidence
readouts
```

Factorization evidence changes `result_identity`, not measurement `epoch_identity`, because it is attached status evidence rather than a readout-governing geometry or policy change.

## Failure behavior

The adapter fails closed for:

- multiple geometry forms;
- multiple factorization-evidence forms;
- factorization evidence without geometry;
- factorization `product_hash` different from geometry `stable_hash`;
- wrong live object or record types;
- unknown, missing, coerced, tampered, or unsupported producer fields;
- unsupported UCNS serialization, bridge, or factorization-evidence schemas;
- transitive UCNS import failures.

Only direct absence of the optional `ucns` package becomes typed transcript-only geometry mode.

## Proof and measurement firewall

Geometry and factorization records deliberately preserve:

```text
theorem_status_transfer = false
measurement_validity_claim = false
```

UCNS domain status and certified negative search evidence do not validate EDCM readouts, METAPAT ontology, external truth, diagnosis, intent, or consciousness.

## Trust boundary

UCNS evidence digests are verified content identities. Version 1 records do not carry cryptographic producer signatures or transport authentication.

## hmmm

Signed producer attestations remain unresolved. Their absence does not reopen the canonical schema, stable-hash binding, certification policy, or proof-transfer firewall.
