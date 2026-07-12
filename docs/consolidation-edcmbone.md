# Consolidation record — edcmbone → edcm

Date consolidated: 2026-07-06  
Authority transition recorded: 2026-07-12

## Current source of truth

```text
repo:   The-Interdependency/edcm
path:   edcm/measurement/
policy: canonical-maintained-edcm-v1
```

`edcm/measurement/` is the maintained structural-measurement implementation and frozen canon-data authority. Runtime package availability does not change this selection. An installed `edcmbone` package cannot silently override it.

Machine-readable authority is exported as:

```python
from edcm.measurement import MEASUREMENT_AUTHORITY
```

## Consolidation provenance

The implementation was originally mirrored from:

```text
repo:   The-Interdependency/edcmbone
path:   backend_old/src/edcmbone/
commit: 05eee6d15c7ad0a7dcf62220a3a0a8618f481a81
role:   provenance and compatibility source
```

This record preserves where the code came from; it does not make that historical source a competing live authority.

## What was consolidated

| historical edcmbone source | maintained EDCM surface |
|---|---|
| `backend_old/src/edcmbone/canon/` and `data/*_v1.json` | `edcm/measurement/canon/` |
| `backend_old/src/edcmbone/parser/turns_rounds.py` | `edcm/measurement/parser/turns_rounds.py` |
| `backend_old/src/edcmbone/metrics/` | `edcm/measurement/metrics/` |
| `backend_old/src/edcmbone/metrics/orthogonality.py` | not duplicated; re-exported from `edcm.ucns_objects` |
| `backend_old/src/edcmbone/ucns/` | `edcm/measurement/ucns/` |
| `backend_old/src/edcmbone/compress.py` | `edcm/measurement/compress.py` |

Ported tests cover closed-token encoding, canon polarity/affix regressions, deterministic transcript measurement, compression roundtrip, layer wiring, and the no-fork orthogonality guarantee.

## Original mechanical deltas

- Absolute `edcmbone.*` imports became package-relative imports.
- edcmbone-local ratio bookend stamps were not carried into EDCM.
- `metrics/orthogonality.py` was not duplicated; the surface is re-exported from `edcm.ucns_objects`.
- Historical `MODULE_BUILD` ids inside consolidated files remain provenance markers until the metadata reconciliation pass explicitly migrates them.

No metric formulas, sign maps, frozen canon JSON, thresholds, or parser behavior were changed during the original consolidation.

## Current wiring

- `edcm.layers.ConsolidatedMeasurementLayer` always selects the maintained `edcm.measurement` implementation.
- `build_default_layers()` does not import or prefer `edcmbone.MeasurementLayer`.
- `MEASUREMENT_AUTHORITY["runtime_override_by_edcmbone"]` is `False`.
- Public entry points are re-exported from `edcm`.
- Base-package operation remains stdlib-only.

## Compatibility policy

```text
id: edcmbone-provenance-only-v1
```

`edcmbone` may be used to:

- inspect historical provenance;
- compare or migrate external callers;
- recover material not yet consolidated;
- support an explicit, versioned compatibility adapter in the future.

It may not silently replace EDCM measurement because it happens to be importable.

## Frozen canon policy

Files under `edcm/measurement/canon/data/*_v1.json` are frozen. Changes require:

1. a new versioned data surface;
2. a migration record;
3. deterministic integrity fixtures;
4. explicit epoch/provenance consequences.

## Proof and empirical firewall

UCNS theorem/domain evidence is separate from EDCM measurement validity. Neither this consolidation nor an attached UCNS object promotes deterministic transcript metrics into diagnosis, intent, consciousness, external truth, or a concrete negative-factorization certificate.

## Usage

```python
from edcm import CanonLoader, compute_transcript, parse_transcript
from edcm.measurement import MEASUREMENT_AUTHORITY

assert MEASUREMENT_AUTHORITY["canonical"] is True
assert MEASUREMENT_AUTHORITY["runtime_override_by_edcmbone"] is False

canon = CanonLoader()
parsed = parse_transcript("A: We need to decide.", canon=canon)
metrics = compute_transcript(parsed, canon=canon)
```

## hmmm

The historical L0/L1/L2/L3 split, `A_MATRIX` wiring, P-metric layer assignment, bidirectional alerts, Bridge home, and any explicit compatibility adapter remain unresolved. They no longer create source-of-truth ambiguity: unfinished migration questions live under EDCM authority unless a later versioned governance decision says otherwise.
