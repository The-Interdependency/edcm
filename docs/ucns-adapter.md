# EDCM–UCNS integration boundary

## Status

**Suspended.**

On 2026-07-19, `The-Interdependency/ucns` reset its public root after finding
that the previous `UCNSObject` omitted the load-bearing object invariant:

- every UCNS object is an intrinsically Möbius-twisted recursive carrier;
- its unique hidden twist/seam is zero;
- one visible circuit reverses orientation;
- two circuits complete the return; and
- normalization cannot choose, move, expose, or erase the seam.

The UCNS root currently publishes no implementation and no system-wide theorem
claim. Its former Python package, bridge records, factorization evidence, and
schemas are preserved under the UCNS archive as historical evidence.

They are not a current producer contract.

## Immediate EDCM rule

EDCM must treat UCNS geometry, factorization, certification, and theorem status
as typed absence until UCNS publishes a new twist-bearing producer surface.

Expected result state:

```text
ucns_geometry_identity.state = NA
ucns_factorization_evidence.state = NA
ucns_package_available = false or non-authoritative
ucns_adapter_active = false
ucns_object_attached = false
ucns_bridge_record_attached = false
ucns_scope_metadata_attached = false
ucns_factorization_evidence_attached = false
ucns_negative_certification_attached = false
ucns_theorem_status_attached = false
```

`NA != 0`: the absence of lawful UCNS geometry is not neutral geometry and must
not be converted into a zero-valued measurement.

EDCM measurement continues independently through the maintained
`edcm/measurement/` package. UCNS absence does not disable transcript
measurement, and archived UCNS proof status never validates EDCM readouts.

## Dependency policy

The managed optional dependency on an archived pre-reset UCNS commit has been
removed from `pyproject.toml`.

Do not restore an old commit, PyPI release, local checkout, or compatibility
package as the canonical producer merely because it still exposes:

```text
UCNSObject
UCNSBridgeRecord
UCNSFactorizationEvidence
bridge_record
stable_hash
```

Surface-name compatibility does not establish object-definition compatibility.

## Historical adapter code

`edcm.ucns_adapter` still records the former consumer contract and can be useful
for schema archaeology, migration analysis, and test fixtures. It does not make
the former producer current.

A code-level fail-closed change is still required so a separately installed
archived `ucns` package cannot activate through automatic import. Until that
change lands, environments running EDCM must not install a pre-reset UCNS
package beside it.

This incompletion is explicit rather than hidden behind a successful import.

## Embedded closed-token lineage

`edcm/measurement/ucns/` contains historical edcmbone encoding machinery built
on the pre-reset object model. Its deterministic token mappings may remain
useful as an EDCM-owned legacy structural encoding, but they are not current
UCNS geometry.

Any continued use must distinguish:

```text
legacy EDCM structural encoding
```

from:

```text
current UCNS object or theorem evidence
```

A rename or versioned migration should remove the false authority implied by
the package name.

## Requirements for reactivation

EDCM may reactivate a UCNS adapter only after UCNS publishes a versioned producer
contract that provides all of the following:

1. an object type that makes a twistless carrier unrepresentable;
2. an intrinsic seam/zero that coordinates cannot select or move;
3. explicit orientation state across 360-degree traversal and 720-degree return;
4. recursive payloads that are complete twist-bearing UCNS objects;
5. serialization and stable identity that preserve the seam invariant;
6. bridge records whose schema states the new object epoch;
7. status evidence that does not inherit claims from the archived system;
8. migration rules for any recoverable pre-reset projections; and
9. EDCM fixtures proving typed absence, schema rejection, and no proof transfer.

A new schema version is required. Reusing the former version identifiers would
make incompatible objects appear identical.

## Proof and measurement firewall

Even after reactivation:

```text
theorem_status_transfer = false
measurement_validity_claim = false
proof_status_transfers_to_measurement_validity = false
```

UCNS geometry or factorization evidence cannot validate EDCM readouts, METAPAT
ontology, external truth, diagnosis, intention, morality, or consciousness.

## hmmm

The dependency pin and documentation authority error are removed here. Automatic
runtime rejection of separately installed pre-reset UCNS packages, and renaming
of the embedded legacy closed-token geometry, remain unfinished code changes.