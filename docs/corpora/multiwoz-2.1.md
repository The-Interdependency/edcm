# MultiWOZ 2.1 full-corpus evidence run

**Status:** admitted source and executable full-corpus adapter.
**Evidence state:** represented evidence; no EDCM candidate measurement or
joint-canon selection.

## Preserved structure

The runner processes the University of Cambridge deposit identified by DOI
`10.17863/CAM.41572`. Admission is bound to the complete ZIP SHA-256 and the
byte count and SHA-256 of every logical archive member. The raw archive remains
outside Git.

`data.json` is streamed in its original top-level dialogue order. Within each
dialogue, every `log[*].text` value is passed without normalization to the exact
EDCM-only UCNS word-gonol consumer. The runner does not sample, sort,
deduplicate, case-fold, normalize Unicode, fold whitespace, or flatten speaker
turns.

MultiWOZ does not carry an explicit speaker field in each log entry. The
adapter therefore declares its own convention:

```text
zero-based even log ordinal -> user
zero-based odd log ordinal  -> system
```

This convention is adapter provenance, not source truth. Goal objects, turn
metadata, dialogue acts, ontology, databases, and partition lists remain
source-native evidence and do not silently enter the word-gonol observation.

## Usage guidance

Keep the archive outside the repository and use a clean checkout of the exact
UCNS profile commit:

```bash
python -m edcm.corpora.multiwoz21 \
  --archive /path/to/MULTIWOZ2.1.zip \
  --ucns-source-root /path/to/ucns-at-eb264fba18bd051c46b4853c81c8fb91ec6d5811 \
  --output experiments/corpora/results/2026-07-28-multiwoz-2.1-full.json \
  --receipt experiments/corpora/receipts/2026-07-28-multiwoz-2.1-complete.json \
  --checkpoint /tmp/multiwoz-2.1.checkpoint.json
```

The runner refuses a dirty EDCM or UCNS tracked tree for a sealed run. A
checkpoint is written atomically at the selected interval and can resume only
when archive, admission, EDCM commit, UCNS commit, and already-processed source
prefix all match.

Successful completion requires:

- all `10,438` dialogues;
- all source turns observed exactly once by the adapter;
- unit support equal to adapted turn count;
- exact `8,438 / 1,000 / 1,000` train/validation/test reconciliation;
- every validation and test identifier present; and
- valid source JSON through EOF.

Any failure produces an incomplete receipt containing the last completed
dialogue and the active dialogue/turn position when available. Reports,
receipts, and checkpoints contain no raw turn text.

## Output interpretation

Committed aggregate evidence includes source/archive identities, full
dialogue/turn reconciliation, chained exact-text identities, word and SPACE
totals, out-of-alphabet code-point totals, structural edge cases, and counts of
source-declared nonempty `fail_book` and `fail_info` goal mappings.

Those source annotations are not EDCM inferences. No correction, retraction,
refusal, unresolved-reference, diagnosis, intention, morality, consciousness,
or external-truth classifier is introduced by this runner.

```text
exact profile observation != formal UCNS geometry
represented evidence != candidate-measured evidence
candidate-measured evidence != canonically measured evidence
NA != 0
```

## File plan

| Path | Change | Purpose | Risk | Required test |
|---|---|---|---|---|
| `edcm/corpora/multiwoz21.py` | created | admission, streaming, exact adaptation, checkpoint, reconciliation, receipts | source-text leakage or false completion | `tests/test_multiwoz21_corpus.py` |
| `edcm/corpora/data/multiwoz_2_1_admission.json` | created | immutable source, license, privacy, and execution contract | source/version ambiguity | archive mutation and identity checks |
| `tests/test_multiwoz21_corpus.py` | created | source-owned contract witnesses | fixture/real-profile drift | full suite plus optional pinned UCNS test |
| `experiments/corpora/` | created after sealed run | aggregate report and receipt only | accidental raw inclusion | tracked-file inspection and digest reconciliation |
| `edcm_msdmd.ts` | regenerated | skill-lib metadata collection | stale contract graph | pinned skill-lib diff |

## hmmm

Source-native labels for correction, retraction, refusal, and unresolved
reference are not complete in MultiWOZ 2.1. They remain unresolved rather than
being guessed from text. Formal Möbius coordinates, higher-gonol composition,
and lawful projection from exact observations into EDCM scalar readouts also
remain open.
