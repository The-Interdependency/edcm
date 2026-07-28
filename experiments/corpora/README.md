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

## hmmm

Only MultiWOZ 2.1 has an admitted executable adapter in this tree. The remaining
six sources require their own license/privacy review, immutable source identity,
source-native adapter, and full-run reconciliation before admission.
