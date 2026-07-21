# edcm

EDCM is the maintained, provenance-bearing Energy–Dissonance Circuit Model
package.

It consolidates:

- [`The-Interdependency/edcmbone`](https://github.com/The-Interdependency/edcmbone), the provenance source for structural measurement work; and
- [`erinepshovel-code/EDCM`](https://github.com/erinepshovel-code/EDCM), the earlier application lineage.

`edcm/measurement/` is the canonical maintained measurement implementation.
The pinned edcmbone source commit remains machine-readable provenance; an
installed `edcmbone` package does not silently replace EDCM.

## Current UCNS boundary

`The-Interdependency/ucns` reset its public root on 2026-07-19 after finding that
the former object type omitted the intrinsic Möbius twist/seam, hidden zero, and
720-degree return required by UCNS canon.

UCNS currently publishes no root implementation and no current producer schema.
EDCM therefore has no managed UCNS dependency and must represent UCNS geometry,
factorization, certification, and theorem evidence as typed `NA`.

Do not install or pin an archived pre-reset UCNS commit as current authority.
Surface-name compatibility is not object-definition compatibility.

See [`docs/ucns-adapter.md`](docs/ucns-adapter.md).

## Install, verify, test, and build

EDCM requires Python 3.11 or newer. The base package has no third-party runtime
dependencies.

```bash
python -m pip install -e .[dev]
python -m edcm.integrity
python -m pytest -q
python -m build
python -m twine check dist/*
```

METAPAT integration is optional and pinned to its reviewed producer commit:

```bash
python -m pip install -e ".[dev,metapat]"
```

The `full-stack` extra currently installs METAPAT only. UCNS must not return to
that extra until a new twist-bearing producer contract and migration are
published.

```bash
python -m pip install -e ".[dev,full-stack]"
```

Base installation does not imply that METAPAT or UCNS ran. Frozen measurement
canon JSON and `py.typed` are included in the wheel.

## Integrity gate

`python -m edcm.integrity` fails when any of these drift:

- the complete set or exact bytes of frozen `*_v1.json` canon files;
- the machine-readable measurement source-of-truth and compatibility policy;
- the no-fork identity between `edcm.measurement.metrics` and canonical EDCM
  orthogonality classes.

The gate runs from both the editable source install and a clean installed wheel.
See [`docs/integrity-gates.md`](docs/integrity-gates.md).

```python
import edcm

assert edcm.run_integrity_gate().passed
```

A legitimate canon change requires a new versioned file and migration record.
Do not update pinned identities merely to silence continuous integration.

## Maintained measurement authority

```text
repo:   The-Interdependency/edcm
path:   edcm/measurement/
policy: canonical-maintained-edcm-v1
```

Machine-readable authority is available as:

```python
from edcm.measurement import MEASUREMENT_AUTHORITY

assert MEASUREMENT_AUTHORITY["canonical"] is True
assert MEASUREMENT_AUTHORITY["runtime_override_by_edcmbone"] is False
assert MEASUREMENT_AUTHORITY["ucns_theorem_status_transfer"] is False
```

`edcm.measurement` contains frozen canon data, transcript parsing, deterministic
metric computation, projection surfaces, closed-token lineage, and the lossless
structural-density codec.

Consolidation provenance and compatibility policy are documented in
[`docs/consolidation-edcmbone.md`](docs/consolidation-edcmbone.md).

## Provenance-bearing pipeline

`build_default_layers()` assembles:

1. **Semantics:** independent METAPAT semantic authority when available, plus
   explicit UCNS geometry absence during the reset;
2. **Measurement:** canonical `edcm.measurement`;
3. **Composition:** canonical shared-stack composition; and
4. **Delivery:** deterministic `edcm.shared-stack-result` contract.

Every result carries independent integration and provenance records:

```text
metapat_integration
ucns_integration
layer_provenance
edcm_result
```

No unavailable integration is represented only by an unexplained `default`
label.

```python
from edcm import build_default_layers

result = build_default_layers().run({
    "transcript": "A: We must decide.\nB: Only after we define the constraint."
})

print(result["layer_provenance"])
print(result["edcm_result"]["result_identity"])
```

## Typed absence

Without optional semantic authority, measurement still runs while unavailable
inputs remain typed absence:

```python
result = build_default_layers().run({"transcript": "A: We must decide."})

assert result["edcm_result"]["ucns_geometry_identity"]["state"] == "NA"
assert result["edcm_result"]["ucns_factorization_evidence"]["state"] == "NA"
```

`NA != 0`: absence is never reported as an enabled neutral measurement.

During the UCNS reset, environments must not install a pre-reset `ucns` package
beside EDCM. The dependency pin and public installation path have been removed;
a code-level automatic rejection guard remains an explicit unfinished repair.

## METAPAT semantic authority

EDCM may consume the public producer schema from
`The-Interdependency/metapat`:

```text
metapat.MetapatModuleEnvelope
canonical to_json() / to_dict() serialization
producer-owned from_json() / from_dict() validation
MODULE_ENVELOPE_SCHEMA_ID
MODULE_ENVELOPE_SCHEMA_VERSION
```

Semantic labels are authority constraints and provenance, not calculated EDCM
values. METAPAT theorem or ontology status does not validate EDCM measurement.

See the package adapter documentation and tests for the exact accepted forms.

## Final result contract

Result schema `edcm.shared-stack-result/1.1.0` separates reviewable
compartments:

1. `source_evidence`;
2. `metapat_semantic_constraints`;
3. `ucns_geometry_identity`;
4. `ucns_factorization_evidence`;
5. `edcm_policy_manifest`;
6. `implementation_provenance`;
7. `readouts`; and
8. `status_evidence`.

`epoch_identity` binds the governing canon and implementation selections.
`result_identity` additionally binds source evidence, readouts, and attachment
states.

See [`docs/shared-stack-result.md`](docs/shared-stack-result.md).

## Proof and measurement firewall

The result contract preserves:

```text
theorem_status_transfer = false
measurement_validity_claim = false
proof_status_transfers_to_measurement_validity = false
```

No UCNS or METAPAT status validates EDCM readouts, external truth, diagnosis,
intention, morality, or consciousness.

## edcmucns architecture

`edcm/edcmucns/` implements policy-manifest hashing, provenance witnesses,
non-origin residue, carrier helpers, closed readout scopes,
geometry/measurement equivalence separation, witness validation, `SeqAppend`,
field-chain reading, and manifest-rotation epochs.

Guardrails:

- no-bone turns are typed absence and produce `NA`, never measured zero;
- ordered windows use `SeqAppend`, never averaging;
- geometry equivalence does not imply measurement equivalence;
- contact convergence, DA geometry correlation, cadence admission from text,
  and semantic-label-to-operating-state inference remain explicit
  non-implementations.

## Recovered source packet

The reviewed 2026-07-20 source packet is recorded under
[`archive/source-packets/2026-07-20-interdependency-project-files/`](archive/source-packets/2026-07-20-interdependency-project-files/).

It preserves provenance for alternate historical metric systems, threshold
proposals, parser doctrine, and pre-reset closed-token geometry without making
any of them a competing active authority.

## Repair status

The ordered stack-repair contract remains under
`codex-handoff/2026-07-12-stack-repair/`. Current evidence is tracked in
`IMPLEMENTATION_STATUS.md`.

## hmmm

Automatic runtime rejection of separately installed pre-reset UCNS packages and
renaming of the embedded legacy `measurement/ucns/` encoder remain unfinished.
The dependency path and documentation now fail closed in principle; the code
must be brought into exact agreement before UCNS-related integration can be
called safe.