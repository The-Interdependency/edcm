# EDCM integrity gates

## Run the gate

From a source checkout or installed wheel:

```bash
python -m edcm.integrity
```

The command prints a JSON report and exits non-zero when any check fails.

Programmatic use:

```python
import edcm

report = edcm.run_integrity_gate()
assert report.passed
```

## Frozen canon byte manifest

The four version-1 canon files are pinned by exact Git blob identity:

```text
bones_affixes_v1.json  68811fc62ffe61022c9db2d325c80b900d501282
bones_punct_v1.json    5cc294c70ebbd7325f07ad67982a9353d0017754
bones_words_v1.json    422cd3d0aa31ab0b2aac6dcbb982bbe4853e6a19
markers_v1.json        f937fab506c2201159ec90024ea18c898a331066
```

The gate checks both:

1. the complete set of `*_v1.json` files—no silent additions or removals;
2. the exact packaged bytes of every file.

A legitimate canon change requires a new versioned file and migration record. Updating the expected identity merely to make CI green would defeat the gate.

## Measurement-authority policy

The full machine-readable authority record is pinned, including:

```text
canonical = true
source_of_truth = The-Interdependency/edcm:edcm/measurement
compatibility_policy = edcmbone-provenance-only-v1
runtime_override_by_edcmbone = false
ucns_theorem_status_transfer = false
```

The original `edcmbone` repository, path, and source commit remain provenance. They are not runtime authority.

## Orthogonality no-fork check

The gate verifies that `edcm.measurement.metrics` re-exports these exact EDCM classes rather than maintaining another implementation:

```text
AxisState
ConstraintField
FieldMotion
```

Identity is checked with Python object identity (`is`), not matching names or similar source text.

## CI coverage

CI runs the integrity gate:

- from the editable source installation;
- through adversarial tests that mutate bytes, file sets, and authority fields;
- from a clean environment after installing the built wheel.

This prevents a false green where source tests pass while packaged resources or exports drift.

## Skill-lib and msdmd

EDCM vendors a bounded build/evidence subset from
`The-Interdependency/skill-lib@2b24be24947223b86440f59f1bd9766130f9cc11`.
The skill-compliance workflow checks those files byte-for-byte, generates the
canonical `edcm_msdmd.ts` collection, compares it with the tracked collection,
and runs the EDCM-native metadata validator.

Local validation:

```bash
python /path/to/skill-lib/tools/check_consumer_drift.py . \
  --canon-root /path/to/skill-lib \
  --sha 2b24be24947223b86440f59f1bd9766130f9cc11 \
  --strict-sha --require-vendored

PYTHONPATH=/path/to/skill-lib python /path/to/skill-lib/msdmd/collect.py \
  --root . --repo The-Interdependency/edcm --out /tmp/edcm_msdmd.ts
diff -u edcm_msdmd.ts /tmp/edcm_msdmd.ts
python tools/check_metadata_contracts.py
```

## hmmm

The repository-wide CONTRACTS/CHECKS graph is collected but is not yet
mutation-verified. A passing graph audit is evidence of linkage and resolution,
not proof that every witness detects every possible behavioral break.
