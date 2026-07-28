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

## Completed runs

| Corpus | Dialogues | Turns | Status | Report | Receipt |
|---|---:|---:|---|---|---|
| MultiWOZ 2.1 | 10,438 | 143,048 | complete | [`2026-07-28-multiwoz-2.1-full.json`](results/2026-07-28-multiwoz-2.1-full.json) | [`2026-07-28-multiwoz-2.1-complete.json`](receipts/2026-07-28-multiwoz-2.1-complete.json) |
| Molweni | 10,000 | 88,303 | complete | [`2026-07-28-molweni-full.json`](results/2026-07-28-molweni-full.json) | [`2026-07-28-molweni-complete.json`](receipts/2026-07-28-molweni-complete.json) |

The MultiWOZ report was produced by
`edcm@6279d2236256f11866250011d15bf7080e4d9025` with
`ucns@eb264fba18bd051c46b4853c81c8fb91ec6d5811`. Its report digest is
`0bf4eb5c9ddf67fd6f48c766ce874435f63be10a32335882a0170be95eb98b21`.
An immediate completed-checkpoint rerun produced byte-identical report and
receipt files.

The Molweni report was produced by
`edcm@750e2155d5e63fe38e308b1f6964b3dc8d1a6235` with
`ucns@eb264fba18bd051c46b4853c81c8fb91ec6d5811`. Its report digest is
`a9af423d62629df6cf4a8c413372b9559120316099c0b0f4b235c44202c2cd7a`.
The DP stream reconciles 78,245 directed relations; the complete MRC layer
reconciles 30,066 questions without measuring its duplicate EDU text again.
An immediate completed-checkpoint rerun produced byte-identical report and
receipt files.

## hmmm

MultiWOZ 2.1 and Molweni are complete. The remaining five sources require their
own license/privacy review, immutable source identity, source-native adapter,
and full-run reconciliation before admission. PRISM is next in the queue.
