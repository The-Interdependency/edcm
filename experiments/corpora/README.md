# Real-system corpus evidence

This tree stores Git-safe aggregate reports and completion or incompletion
receipts. Raw corpus archives, extracted text, and resumable checkpoints do not
belong here.

## Usage guidance

Run a corpus only through its admitted source-native adapter. Store:

- aggregate reports under `results/`;
- completion or incompletion receipts under `receipts/`; and
- raw archives and checkpoints outside Git.

Every complete receipt must reconcile the full admitted source. A sample,
partition-only run, source mismatch, adapter failure, or interrupted execution
is `incomplete` and must retain its exact stopping point and reason.

Current queue:

1. MultiWOZ 2.1
2. Molweni
3. PRISM
4. ICSI
5. AMI
6. WildChat-1M
7. LMSYS-Chat-1M

## Historical runs and supersession

| Corpus | Dialogues | Turns | Status | Report | Receipt |
|---|---:|---:|---|---|---|
| MultiWOZ 2.1 | 10,438 | 143,048 | execution complete; profile interpretation superseded | [`2026-07-28-multiwoz-2.1-full.json`](results/2026-07-28-multiwoz-2.1-full.json) | [`2026-07-28-multiwoz-2.1-complete.json`](receipts/2026-07-28-multiwoz-2.1-complete.json) |

The MultiWOZ report was produced by
`edcm@6279d2236256f11866250011d15bf7080e4d9025` with
`ucns@eb264fba18bd051c46b4853c81c8fb91ec6d5811`. Its report digest is
`0bf4eb5c9ddf67fd6f48c766ce874435f63be10a32335882a0170be95eb98b21`.
An immediate completed-checkpoint rerun produced byte-identical report and
receipt files.

The old files remain immutable because they prove what profile 0.1 executed.
They are not current profile evidence: `4,094` tab, newline, and non-breaking
space occurrences were reported as out-of-alphabet even though they are SPACE
manifestations assigned to carrier position zero. The machine-readable
[supersession record](supersessions/2026-07-28-multiwoz-2.1-space-origin.json)
preserves the exact old identities and keeps replacement report/receipt paths
null until a clean profile-0.2 full-corpus rerun is sealed. Do not infer or
publish corrected aggregates from the historical report alone.

## hmmm

The corrected MultiWOZ 2.1 aggregates remain hmmm until the sealed profile-0.2
rerun completes. Only MultiWOZ 2.1 has an admitted executable adapter in this
tree. The remaining six sources require their own license/privacy review,
immutable source identity, source-native adapter, and full-run reconciliation
before admission.
