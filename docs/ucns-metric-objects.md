# Retired pre-reset UCNS metric-object resolver

**Status:** removed from the live EDCM package.  
**Current integration:** [exact EDCM UCNS observation profile](ucns-adapter.md).

## Why this surface was removed

The former `edcm.ucns_metrics` module converted completed scalar EDCM values
into content-addressed objects by requiring these archived UCNS surfaces:

```text
UCNSObject
recursive_encode
stable_hash
```

Those names belong to the pre-reset producer lineage. They do not implement or
validate the exact EDCM-only word-gonol profile, Möbius initiation, completion
motion, higher-gonol composition, or a lawful projection from retained
trajectory evidence into scalar readouts. Keeping the resolver importable
allowed an unrelated package named `ucns` to reactivate the retired path.

The module, its top-level `edcm` exports, and its fake-producer tests have
therefore been removed. Git history preserves the implementation as historical
evidence; it is not a compatibility surface.

## Current usage guidance

Install the exact profile producer and pass every exact speaker turn separately:

```bash
python -m pip install -e .[dev,ucns-profile]
```

```python
import edcm

result = edcm.build_default_layers().run({
    "transcript": "A: Preserve the boundary.\nB: Keep spaces  exact.",
    "ucns_turns": (
        ("A", "Preserve the boundary."),
        ("B", "Keep spaces  exact."),
    ),
})

observation = result["edcm_result"]["ucns_profile_observation"]
assert observation["state"] == "attached"
assert result["edcm_result"]["ucns_geometry_identity"]["state"] == "NA"
```

Use `ucns_profile_observation` as exact represented evidence. Do not reconstruct
speaker units from `transcript`, treat an observation digest as formal geometry,
or turn an existing scalar into a UCNS object merely to give it an identity.

A future scalar projection must be versioned, name its assignment and transition
law, link to the complete completion-motion trajectory, and declare every lost
distinction. Until then, absence of such a projection is `NA`, not zero.

## Compatibility effect

Importing `edcm.ucns_metrics` or importing its former resolver names from
`edcm` is intentionally unsupported. Consumers must migrate to the exact
profile observation contract above. No alias or silent fallback is provided.

## hmmm

Formal Möbius coordinates, the exact assignment and transition law,
higher-gonol composition, and lawful readout-specific scalar projections remain
open. Removing an invalid resolver preserves that incompletion instead of
encoding a convenient answer into the wrong object model.
