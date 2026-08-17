# Tarot generated artifacts

The Tarot acquisition runner writes a snapshot such as:

```text
artifacts/tarot/acquisition-v1/
  raw/                     # only explicitly authorized downloaded bytes
  evidence-index.json      # every admitted source, including metadata-only locators
  run-receipt.json         # deterministic manifest and file identities
```

Interrupted runs use a temporary `.checkpoint.json`; a completed run removes it. `--resume` validates manifest identity, byte digests, and the exact file set before reuse.

Do not commit generated corpus bytes here.

hmmm: EDCM embedding outputs will receive their own versioned artifact contract after the acquisition boundary survives.
