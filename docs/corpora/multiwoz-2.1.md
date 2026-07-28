# MultiWOZ 2.1 full-corpus evidence run

**Status:** admitted; profile-0.2 sealed full-corpus rerun complete on
2026-07-28; profile-0.1 SPACE interpretation superseded.
**Evidence state:** current and historical represented evidence; no EDCM
candidate measurement or joint-canon selection.

## Preserved structure

The runner processes the University of Cambridge deposit identified by DOI
`10.17863/CAM.41572`. Admission is bound to the complete ZIP SHA-256 and the
byte count and SHA-256 of every logical archive member. The raw archive remains
outside Git.

`data.json` is streamed in its original top-level dialogue order. Within each
dialogue, every `log[*].text` value is passed without normalization to the exact
EDCM-only UCNS word-gonol consumer. The runner does not sample, sort,
deduplicate, case-fold, normalize Unicode, fold whitespace, or flatten speaker
turns. Under profile 0.2, the pinned Unicode SPACE manifestations share carrier
position zero while their exact source values and code points remain separate
witnesses. Report and checkpoint profile identity bind the Unicode-scalar
source domain, all 25 ordered SPACE code points, and their canonical digest.

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
  --ucns-source-root /path/to/ucns-at-c799b3547afc91a6039a5d3b15f997426eed138a \
  --output experiments/corpora/results/2026-07-28-multiwoz-2.1-space-origin-rerun.json \
  --receipt experiments/corpora/receipts/2026-07-28-multiwoz-2.1-space-origin-complete.json \
  --checkpoint /tmp/multiwoz-2.1-space-origin.checkpoint.json
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
dialogue/turn reconciliation, chained exact-text identities, word and
carrier-SPACE totals, true non-SPACE out-of-alphabet code-point totals,
structural edge cases, and counts of source-declared nonempty `fail_book` and
`fail_info` goal mappings. Leading, trailing, and repeated SPACE metrics are
computed from `alphabet_position == 0`, not from raw equality with `U+0020`.

Those source annotations are not EDCM inferences. No correction, retraction,
refusal, unresolved-reference, diagnosis, intention, morality, consciousness,
or external-truth classifier is introduced by this runner.

The historical sealed run processed `10,438` dialogues and `143,048` turns.
Source turns, adapter turns, and profile unit support reconciled exactly; train,
validation, and test counts reconciled at `8,438 / 1,000 / 1,000`. Its immutable
[report](../../experiments/corpora/results/2026-07-28-multiwoz-2.1-full.json)
and [completion receipt](../../experiments/corpora/receipts/2026-07-28-multiwoz-2.1-complete.json)
remain provenance-bearing records.

That run classified `4,094` occurrences of `U+0009`, `U+000A`, and `U+00A0`
as out-of-alphabet. They are SPACE manifestations under the corrected profile
and belong at carrier position zero. Consequently the historical
out-of-alphabet, word-gonol, boundary, and leading/trailing/repeated SPACE
aggregates must not be presented as current profile-0.2 totals. The
[supersession record](../../experiments/corpora/supersessions/2026-07-28-multiwoz-2.1-space-origin.json)
states the defect and links the complete sealed replacement
[report](../../experiments/corpora/results/2026-07-28-multiwoz-2.1-space-origin-rerun.json)
and [receipt](../../experiments/corpora/receipts/2026-07-28-multiwoz-2.1-space-origin-complete.json).

The replacement ran from clean pushed commits
`edcm@fbee2ee57f765b47c362a6877521493cc1afe20a` and
`ucns@c799b3547afc91a6039a5d3b15f997426eed138a`. It preserved the exact archive,
dialogue count, turn count, partition counts, source-dialogue digest chain, and
turn-evidence digest chain. The corrected classification is:

| Observation | Profile 0.1 | Profile 0.2 | Change |
|---|---:|---:|---:|
| Carrier-unassigned occurrences | 4,094 | 0 | -4,094 |
| SPACE boundaries | 1,779,585 | 1,783,679 | +4,094 |
| Word gonols | 1,882,845 | 1,885,785 | +2,940 |
| Leading-SPACE turns | 186 | 261 | +75 |
| Trailing-SPACE turns | 20,493 | 21,264 | +771 |
| Repeated-SPACE excess | 19,109 | 19,417 | +308 |

Thus all `4,094` disputed occurrences moved from carrier-unassigned evidence to
source-preserved SPACE boundaries; none disappeared or changed code-point
identity.

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
| `experiments/corpora/supersessions/2026-07-28-multiwoz-2.1-space-origin.json` | created | preserve the old evidence identity and bind the sealed replacement | replacement mismatch or historical rewrite | supersession identity, file digest, and source-chain reconciliation |
| `edcm_msdmd.ts` | regenerated | skill-lib metadata collection | stale contract graph | pinned skill-lib diff |

## hmmm

The corrected SPACE-origin totals are sealed represented evidence. They are not
formal Möbius geometry or an EDCM measurement-validity claim. Source-native
labels for correction, retraction, refusal, and unresolved reference are not
complete in MultiWOZ 2.1 and remain unresolved rather than being guessed from
text. Formal Möbius coordinates, higher-gonol composition, and lawful projection
from exact observations into EDCM scalar readouts also remain open.
