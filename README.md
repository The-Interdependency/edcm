# edcm

EDCM is the maintained consolidation of:

- [`The-Interdependency/edcmbone`](https://github.com/The-Interdependency/edcmbone), the provenance source for structural measurement work;
- [`erinepshovel-code/EDCM`](https://github.com/erinepshovel-code/EDCM), the earlier application work.

`edcm/measurement/` is now the canonical maintained measurement implementation. The pinned `edcmbone` source commit remains machine-readable provenance; an installed `edcmbone` package does not silently override EDCM.

## Install, test, and build

EDCM requires Python 3.11 or newer. The base package has no third-party runtime dependencies.

```bash
python -m pip install -e .[dev]
python -m pytest -q
python -m build
python -m twine check dist/*
```

Check the built wheel independently:

```bash
python -m venv .wheel-venv
.wheel-venv/bin/python -m pip install dist/*.whl
.wheel-venv/bin/python -c "import edcm; print(edcm.__version__)"
```

`edcm.__version__` supplies the built distribution version. Frozen measurement canon JSON and `py.typed` are included in the wheel. Base installation does not imply that UCNS or METAPAT integration ran.

## Provenance-bearing four-layer pipeline

`build_default_layers()` assembles:

- **Semantics/geometry:** the EDCM-owned actual-UCNS adapter when `ucns` is installed; otherwise explicit transcript-only mode.
- **Measurement:** canonical `edcm.measurement`.
- **Composition:** an explicit local fallback pending the shared-stack composition policy.
- **Delivery:** an explicit local fallback pending application-specific delivery selection.

Every result carries `layer_provenance` and `ucns_integration`. No layer is represented only by an unexplained `default` label.

```python
from edcm import build_default_layers

result = build_default_layers().run({"input": "example"})
print(result["layer_provenance"])
print(result["ucns_integration"])
```

### Transcript-only mode

When UCNS is unavailable:

```python
result = build_default_layers().run({"transcript": "A: We must decide."})
assert result["semantics"] == "edcm.transcript_only"
assert result["ucns_integration"]["ucns_package_available"] is False
```

This mode is supported, but it cannot be mistaken for the full UCNS-backed path.

## Actual UCNS adapter

EDCM does not expect UCNS to expose an EDCM-specific `SemanticsLayer`. The adapter consumes actual UCNS public surfaces:

- `ucns.UCNSObject`;
- `ucns.object_record`;
- `ucns.stable_hash`;
- `ucns.CANONICAL_SERIALIZATION_VERSION`;
- typed domain prerequisite metadata.

```python
from fractions import Fraction

import edcm
import ucns

obj = ucns.UCNSObject(1, 1, [(Fraction(0), None)], [0])
result = edcm.build_default_layers().run({"ucns_object": obj})

assert result["ucns_geometry"]["stable_hash"] == ucns.stable_hash(obj)
assert result["ucns_integration"]["ucns_object_attached"] is True
assert result["ucns_integration"]["ucns_theorem_status_attached"] is False
```

The status record distinguishes:

```text
ucns_package_available
ucns_adapter_active
ucns_object_attached
ucns_scope_metadata_attached
ucns_negative_certification_attached
ucns_theorem_status_attached
```

Package import alone does not imply evidence attachment. Domain prerequisite metadata is attached evidence, not EDCM measurement validity and not certification of a concrete negative factorization result. See `docs/ucns-adapter.md`.

## Canonical measurement package

`edcm.measurement` contains:

- frozen canon data and `CanonLoader`;
- turns/rounds transcript parsing;
- deterministic metric computation;
- matrix and projection surfaces;
- closed-token encoding;
- the lossless codec and structural-density readout.

```python
from edcm import CanonLoader, compute_transcript, parse_transcript, project_transcript

transcript = "A: We must decide now.\nB: No. Why rush?"
canon = CanonLoader()
parsed = parse_transcript(transcript, canon=canon)
metrics = compute_transcript(parsed, canon=canon)
agents = project_transcript(parsed, metrics)
```

The four-layer pipeline runs the same maintained implementation:

```python
result = build_default_layers().run({"transcript": transcript})
result["rounds"]
result["agent_metrics"]
result["structural_density"]
assert result["layer_provenance"]["measurement"]["canonical"] is True
```

Machine-readable authority and consolidation provenance live in `edcm.measurement.MEASUREMENT_AUTHORITY` and `docs/consolidation-edcmbone.md`.

## edcmucns v0.3.1 architecture

`edcm/edcmucns/` implements the ratified architecture described in `docs/codex_edcmucns_v031_handoff.md`: policy-manifest hashing, provenance witnesses, non-origin residue, carrier helpers, closed readout scopes, geometry/measurement equivalence separation, witness validation, `SeqAppend`, field-chain reading, and manifest-rotation epochs.

```python
from edcm.edcmucns import (
    BoneEvent,
    PolicyManifest,
    edcm_measurement_equivalent,
    encode_turn,
)

manifest = PolicyManifest()
turn = encode_turn("t1", "A", [BoneEvent("P", "not")], manifest)
assert edcm_measurement_equivalent(turn.window, turn.window, "operator_scope")
```

Guardrails:

- no-bone turns are typed absence and produce `NA`, never measured zero;
- ordered windows use `SeqAppend`, never averaging;
- UCNS geometry equivalence does not imply EDCM measurement equivalence;
- contact convergence, DA geometry correlation, and cadence admission from text remain explicit `NotImplementedError` frontier gates.

## EDCM construction objects

`ConstraintField`, `FieldMotion`, axes, windows, turns, and readouts are EDCM objects constructed using UCNS geometry. They are not replacement implementations of `ucns.UCNSObject`.

```python
from edcm import ConstraintField

field = ConstraintField(
    grain="round",
    raised_field_count=3,
    contact="against",
    resolution="open",
)
field.contact_state()
field.behavioral_readouts()
```

`NA != 0`: an absent required context is disabled/typed absence; zero is an enabled neutral measurement.

## Energy falsifiability audit

```python
from edcm import audit_energy_text

report = audit_energy_text("The theory predicts a CMB excess.")
print(report.flags)
print(report.ucns_dependency)
```

The audit examines claim structure and falsifiability readiness. It does not validate external physics, import UCNS-A proof status, decide empirical truth, or treat package availability as attached UCNS scope evidence.

## Repair status

The ordered repair contract lives in `codex-handoff/2026-07-12-stack-repair/`. Current evidence is tracked in `IMPLEMENTATION_STATUS.md`.

## hmmm

The METAPAT semantic-envelope adapter, full shared-stack result envelope, serialized UCNS bridge-record ingestion, validated negative/theorem evidence envelopes, and repo-local skill-lib drift gates remain unfinished. Their absence must remain visible rather than replaced by fabricated defaults.
