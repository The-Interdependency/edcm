# edcm

EDCM is the maintained consolidation of:

- [`The-Interdependency/edcmbone`](https://github.com/The-Interdependency/edcmbone), the provenance source for structural measurement work;
- [`erinepshovel-code/EDCM`](https://github.com/erinepshovel-code/EDCM), the earlier application work.

`edcm/measurement/` is the canonical maintained measurement implementation. The pinned `edcmbone` source commit remains machine-readable provenance; an installed `edcmbone` package does not silently override EDCM.

## Install, verify, test, and build

EDCM requires Python 3.11 or newer. The base package has no third-party runtime dependencies.

```bash
python -m pip install -e .[dev]
python -m edcm.integrity
python -m pytest -q
python -m build
python -m twine check dist/*
```

Integration extras install the exact verified sibling packages:

```bash
python -m pip install -e ".[dev,ucns]"
python -m pip install -e ".[dev,metapat]"
python -m pip install -e ".[dev,full-stack]"
```

Base installation does not imply that UCNS or METAPAT ran. Frozen measurement canon JSON and `py.typed` are included in the wheel.

## Integrity gate

`python -m edcm.integrity` fails when any of these drift:

- the complete set or exact bytes of frozen `*_v1.json` canon files;
- the machine-readable measurement source-of-truth and compatibility policy;
- the no-fork identity between `edcm.measurement.metrics` and canonical EDCM orthogonality classes.

The gate runs from both the editable source install and a clean installed wheel. See [`docs/integrity-gates.md`](docs/integrity-gates.md).

```python
import edcm

assert edcm.run_integrity_gate().passed
```

A legitimate canon change requires a new versioned file and migration record. Do not update pinned identities merely to silence CI.

## Provenance-bearing four-layer pipeline

`build_default_layers()` assembles:

1. **Semantics:** independent METAPAT semantic-authority and UCNS geometry/status-evidence sublayers;
2. **Measurement:** canonical `edcm.measurement`;
3. **Composition:** canonical shared-stack composition;
4. **Delivery:** deterministic `edcm.shared-stack-result` contract.

Every result carries:

```text
metapat_integration
ucns_integration
layer_provenance
edcm_result
```

No unavailable integration is represented only by an unexplained `default` label.

```python
from edcm import build_default_layers

result = build_default_layers().run({"transcript": "A: We must decide."})
print(result["layer_provenance"])
print(result["edcm_result"]["result_identity"])
```

### Base transcript mode

Without optional siblings, measurement still runs while semantic authority, geometry, and factorization evidence remain typed absence:

```python
result = build_default_layers().run({"transcript": "A: We must decide."})

assert result["metapat_integration"]["metapat_package_available"] is False
assert result["ucns_integration"]["ucns_package_available"] is False
assert result["edcm_result"]["metapat_semantic_constraints"]["state"] == "NA"
assert result["edcm_result"]["ucns_geometry_identity"]["state"] == "NA"
assert result["edcm_result"]["ucns_factorization_evidence"]["state"] == "NA"
```

`NA != 0`: absence is never reported as an enabled neutral measurement.

## Canonical METAPAT semantic authority

EDCM consumes the actual public producer schema from `The-Interdependency/metapat`:

- `metapat.MetapatModuleEnvelope`;
- canonical `to_json()` / `to_dict()` serialization;
- producer-owned `from_json()` / `from_dict()` validation;
- `MODULE_ENVELOPE_SCHEMA_ID` and `MODULE_ENVELOPE_SCHEMA_VERSION`.

EDCM accepts exactly one of:

```text
metapat_envelope
metapat_envelope_json
metapat_envelope_dict
```

```python
import edcm
import metapat

envelope = metapat.root_spine_module_envelope()
result = edcm.build_default_layers().run({
    "transcript": "A: Preserve exact semantic authority.",
    "metapat_envelope": envelope,
})

assert result["metapat_semantics"]["canon_digest"] == envelope.canon_digest
assert result["metapat_semantics"]["provenance_digest"] == envelope.provenance_digest
assert result["metapat_integration"]["metapat_envelope_attached"] is True
assert result["metapat_integration"]["metapat_theorem_status_attached"] is False
```

The consumer preserves schema identity, module identity, canon identity, exact source references and statements, constraints, permitted interpretations, unresolved `hmmm`, and provenance digest. Semantic labels are authority constraints and provenance—not calculated EDCM values.

## Canonical UCNS geometry and status evidence

EDCM consumes the actual public producer surfaces from `The-Interdependency/ucns`:

```text
ucns.UCNSObject
ucns.UCNSBridgeRecord
ucns.UCNSFactorizationEvidence
ucns.bridge_record
canonical producer from_json / from_dict constructors
```

Supply exactly one geometry form:

```text
ucns_object
ucns_bridge_record
ucns_bridge_record_json
ucns_bridge_record_dict
```

A live object is converted through `ucns.bridge_record()` so live and serialized paths share one canonical identity record.

```python
import edcm
import ucns

obj = ucns.S2
result = edcm.build_default_layers().run({"ucns_object": obj})

assert result["ucns_geometry"]["stable_hash"] == ucns.stable_hash(obj)
assert result["ucns_integration"]["ucns_object_attached"] is True
assert result["ucns_integration"]["ucns_bridge_record_attached"] is True
assert result["ucns_integration"]["ucns_theorem_status_attached"] is True
assert result["ucns_integration"]["ucns_negative_certification_attached"] is False
```

Package import alone does not imply object, bridge, scope, factorization, negative-certification, or theorem evidence attachment.

### Authoritative factorization evidence

After geometry, optionally supply exactly one:

```text
ucns_factorization_evidence
ucns_factorization_evidence_json
ucns_factorization_evidence_dict
```

```python
bridge = ucns.bridge_record(ucns.S2)
evidence = ucns.factorization_evidence(ucns.S2)

result = edcm.build_default_layers().run({
    "transcript": "A: Preserve authoritative evidence.",
    "ucns_bridge_record_json": bridge.to_json(),
    "ucns_factorization_evidence_json": evidence.to_json(),
})

assert result["ucns_factorization_evidence"]["evidence_digest"] == evidence.evidence_digest
assert result["ucns_integration"]["ucns_factorization_evidence_attached"] is True
assert result["ucns_integration"]["ucns_negative_certification_attached"] is True
```

The factorization record must bind to the same stable object hash as the geometry. An attached but uncertified record remains evidence while the certification flag stays false.

See [`docs/ucns-adapter.md`](docs/ucns-adapter.md).

## Full UCNS / METAPAT / EDCM path

METAPAT can adapt its semantic envelope into actual UCNS geometry while keeping exact semantic text outside UCNS payload meaning:

```python
import edcm
import metapat
import ucns

envelope = metapat.root_spine_module_envelope()
adaptation = metapat.adapt_envelope_to_ucns(envelope)

result = edcm.build_default_layers().run({
    "transcript": "A: Preserve the complete boundary.",
    "source_ref": "example://root-spine",
    "metapat_envelope": envelope,
    "ucns_object": adaptation.ucns_object,
})

contract = result["edcm_result"]
assert contract["metapat_semantic_constraints"]["canon_digest"] == envelope.canon_digest
assert contract["ucns_geometry_identity"]["stable_hash"] == ucns.stable_hash(adaptation.ucns_object)
assert contract["ucns_factorization_evidence"]["state"] == "NA"
assert contract["status_evidence"]["proof_status_transfers_to_measurement_validity"] is False
```

## Final result contract

Result schema `edcm.shared-stack-result/1.1.0` separates eight reviewable compartments:

1. `source_evidence` — source reference, content digest, and size;
2. `metapat_semantic_constraints` — canon identity, exact statements, constraints, and unresolved fields;
3. `ucns_geometry_identity` — canonical bridge identity, stable hash, schema, structural facts, and typed status evidence;
4. `ucns_factorization_evidence` — authoritative search, coverage, pruning, factor, scope, certification, and uncertified-reason evidence or typed `NA`;
5. `edcm_policy_manifest` — manifest fields and hash;
6. `implementation_provenance` — selected semantic, geometry, measurement, composition, and delivery implementations;
7. `readouts` — measured values or typed `NA`;
8. `status_evidence` — independent attachment flags and proof-transfer firewall.

`epoch_identity` binds METAPAT canon/provenance, UCNS bridge geometry, EDCM manifest, and implementation selection. `result_identity` additionally binds source evidence, readouts, UCNS factorization evidence, and attachment states. Factorization evidence changes result identity, not measurement epoch identity.

```python
from edcm import build_default_layers
from edcm.edcmucns import PolicyManifest

manifest = PolicyManifest(polarity_dictionary_version="v032")
result = build_default_layers(manifest).run({"transcript": "A: example"})
```

See [`docs/shared-stack-result.md`](docs/shared-stack-result.md).

## Proof and measurement firewall

UCNS geometry and factorization evidence preserve:

```text
theorem_status_transfer = false
measurement_validity_claim = false
proof_status_transfers_to_measurement_validity = false
```

UCNS status evidence does not validate EDCM readouts, METAPAT ontology, external truth, diagnosis, intent, or consciousness.

## Canonical measurement package

`edcm.measurement` contains frozen canon data, transcript parsing, deterministic metric computation, projection surfaces, closed-token encoding, and the lossless structural-density codec.

Machine-readable authority and consolidation provenance live in `edcm.measurement.MEASUREMENT_AUTHORITY` and `docs/consolidation-edcmbone.md`.

## edcmucns v0.3.1 architecture

`edcm/edcmucns/` implements policy-manifest hashing, provenance witnesses, non-origin residue, carrier helpers, closed readout scopes, geometry/measurement equivalence separation, witness validation, `SeqAppend`, field-chain reading, and manifest-rotation epochs.

Guardrails:

- no-bone turns are typed absence and produce `NA`, never measured zero;
- ordered windows use `SeqAppend`, never averaging;
- UCNS geometry equivalence does not imply EDCM measurement equivalence;
- contact convergence, DA geometry correlation, cadence admission from text, and semantic-label-to-operating-state inference remain explicit non-implementations.

## Repair status

The ordered repair contract lives in `codex-handoff/2026-07-12-stack-repair/`. Current evidence is tracked in `IMPLEMENTATION_STATUS.md`.

## hmmm

Version 1 UCNS evidence digests establish canonical content identity, not cryptographic producer signatures. Signed producer or transport authentication and repo-local skill-lib drift/msdmd gates remain unfinished. EDCM currently has no `.agents/skills/` installation, so no local skill drift result is claimed.
