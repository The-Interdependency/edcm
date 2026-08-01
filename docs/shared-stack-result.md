# Shared UCNS / METAPAT / EDCM result contract

`edcm.shared_stack` emits one deterministic review record without collapsing
the identities or authority of its contributors.

```text
schema_id: edcm.shared-stack-result
schema_version: 1.2.0
```

Version 1.2 adds the exact EDCM UCNS profile-observation compartment and keeps
geometry and factorization independently typed.

## Compartments

- `source_evidence` identifies the flattened transcript measured by EDCM.
- `metapat_semantic_constraints` contains only validated METAPAT authority and
  provenance; semantic labels are not metric values.
- `ucns_profile_observation` contains exact full-corpus word-gonol evidence
  when ordered `ucns_turns` were supplied. Source code-point witnesses remain
  separate from carrier assignment; pinned Unicode SPACE manifestations share
  carrier position zero without normalization.
- `ucns_geometry_identity` remains typed `NA`; the current profile does not
  supply formal UCNS geometry.
- `ucns_factorization_evidence` remains typed `NA`; no factorization producer
  is authorized by this profile.
- `edcm_policy_manifest` binds the selected EDCM measurement policy.
- `implementation_provenance` records independent semantic-authority,
  UCNS-profile, measurement, composition, and delivery selections.
- `readouts` contains EDCM measurements or typed absence; `NA != 0`.
- `status_evidence` keeps profile, bridge, factorization, theorem, and
  certification attachment flags independent.

## Identity rules

`epoch_identity` binds:

- METAPAT canon and provenance;
- UCNS profile id, version, scope, exact options, and pinned source commit;
- the Unicode-scalar source domain and exact ordered 25-value SPACE pin,
  including its canonical digest, through the observation record;
- EDCM policy-manifest identity;
- selected semantic-authority, UCNS-profile, and measurement implementations.

`result_identity` additionally binds source evidence, exact profile
observations, EDCM readouts, independently attached evidence, and status flags.
Changing corpus evidence changes result identity without pretending that the
profile configuration changed.

## Full-stack usage

```python
import edcm
import metapat

envelope = metapat.root_spine_module_envelope()
result = edcm.build_default_layers().run({
    "transcript": "A: Preserve the boundary.\nB: Keep spaces  exact.",
    "source_ref": "example://root-spine",
    "metapat_envelope": envelope,
    "ucns_turns": (
        ("A", "Preserve the boundary."),
        ("B", "Keep spaces  exact."),
    ),
})

contract = result["edcm_result"]
assert contract["ucns_profile_observation"]["state"] == "attached"
assert contract["ucns_geometry_identity"]["state"] == "NA"
assert contract["ucns_factorization_evidence"]["state"] == "NA"
assert contract["status_evidence"]["ucns_profile_observation_attached"] is True
assert contract["status_evidence"]["proof_status_transfers_to_measurement_validity"] is False
```

## Failure behavior

The current path fails closed for profile identity or option drift, producer
checkout drift, installed-file hash or executable-bytecode drift, malformed
producer metadata, public alphabet drift, malformed turn containers, retired
bridge/object/factorization inputs, malformed METAPAT evidence, and transitive
import failures. Only direct optional-package absence becomes typed
unavailability.

## hmmm

Observation digests establish deterministic content identity, not signed
producer authentication. More importantly, exact word-gonol evidence is not
yet a formal higher-dimensional lattice or a lawful projection into one; that
boundary remains visible in the contract.
