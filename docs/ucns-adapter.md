# EDCM UCNS adapter

## Purpose

EDCM owns the adapter contract it needs. UCNS does not need to expose an EDCM-specific `SemanticsLayer`.

The adapter consumes the actual public UCNS package surface:

- `ucns.UCNSObject`;
- `ucns.object_record`;
- `ucns.stable_hash`;
- `ucns.CANONICAL_SERIALIZATION_VERSION`;
- typed domain prerequisite metadata carried by the object record.

## Usage

With UCNS installed:

```python
from fractions import Fraction

import edcm
import ucns

obj = ucns.UCNSObject(1, 1, [(Fraction(0), None)], [0])
result = edcm.build_default_layers().run({"ucns_object": obj})

assert result["ucns_geometry"]["stable_hash"] == ucns.stable_hash(obj)
assert result["ucns_integration"]["ucns_object_attached"] is True
```

Without UCNS installed:

```python
import edcm

result = edcm.build_default_layers().run({"transcript": "A: We need to decide."})
assert result["semantics"] == "edcm.transcript_only"
assert result["ucns_integration"]["ucns_package_available"] is False
```

## Independent status fields

Every integration report distinguishes:

```text
ucns_package_available
ucns_adapter_active
ucns_object_attached
ucns_scope_metadata_attached
ucns_negative_certification_attached
ucns_theorem_status_attached
```

Package import alone sets only package availability and, after successful adapter construction, adapter activation. It does not claim that an object or evidence record was attached.

## Failure behavior

- Direct absence of the optional `ucns` package selects explicit transcript-only mode.
- A transitive import failure is raised.
- Missing public surfaces fail adapter construction.
- Unsupported canonical serialization versions fail closed.
- A value under `ucns_object` that is not an actual `ucns.UCNSObject` raises `TypeError`.

## Proof and measurement firewall

The geometry evidence record preserves the UCNS stable hash and domain prerequisite metadata. It deliberately sets:

```text
theorem_status_transfer = false
measurement_validity_claim = false
```

Domain metadata is attached evidence, not validation of an EDCM empirical readout and not certification of a concrete negative factorization result.

## hmmm

Live `UCNSObject` / `object_record` ingestion is implemented. Official serialized bridge-record ingestion remains unresolved until its canonical schema is identified and pinned from UCNS rather than invented locally.
