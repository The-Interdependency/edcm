# MultiWOZ 2.1 full-corpus evidence run

**Status:** admitted; profile-0.2 sealed full-corpus rerun complete on
2026-07-28; profile-0.1 SPACE interpretation superseded; UCNS v0.14.1
completion-receipt rerun and exact v0.19-producer rerun sealed on 2026-07-31.
**Evidence state:** current and historical represented evidence; no EDCM
candidate measurement or joint-canon selection.

## Preserved structure

The runner processes the University of Cambridge deposit identified by DOI
`10.17863/CAM.41572`. Admission is bound to the complete ZIP SHA-256 and the
byte count and SHA-256 of every logical archive member. The raw archive remains
outside Git.

`data.json` is streamed in its original top-level dialogue order. Within each
dialogue, every `log[*].text` value is passed without normalization to the exact
EDCM-only UCNS word-gonol consumer. After source-native reconciliation, the
runner independently repeats the authenticated turn stream through the UCNS
v0.14.1 full-corpus gate and requires its execution-generated receipt plus a
matching source-native turn chain. The runner does not sample, sort,
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
UCNS v0.19 producer commit. The consumed profile remains version 0.2.0 and the
full-corpus completion schema remains version 0.14.1:

```bash
python -m edcm.corpora.multiwoz21 \
  --archive /path/to/MULTIWOZ2.1.zip \
  --ucns-source-root /path/to/ucns-at-872f53571d5dc2f133ff1813b7bdffd3a9c309f8 \
  --output /tmp/multiwoz-2.1-ucns-v019.json \
  --receipt /tmp/multiwoz-2.1-ucns-v019-receipt.json \
  --checkpoint /tmp/multiwoz-2.1-ucns-v019.checkpoint.json
```

The runner refuses a dirty EDCM or UCNS tracked tree for a sealed run. It also
compares every EDCM package file directly with replacement-disabled `HEAD` and
verifies active-runtime EDCM caches, so index flags cannot hide executed-code
drift. Its public entry point dispatches the seal to an isolated fresh Python
interpreter from a cache-free, replacement-disabled Git archive of the sealed
EDCM producer checkout. The bootstrap resolves one exact commit and `edcm/`
tree, archives that exact commit, and passes the same tree identity into the
worker, so a concurrent `HEAD` change cannot relabel the executing snapshot.
That authenticated runner verifies the original worktree and its active caches,
then verifies the UCNS package tree and active caches before its first import.
Already-loaded or pre-verification module code therefore cannot survive into
sealed execution. Bootstrap identity, archive, or extraction failure writes an
incomplete receipt before exit. The child preserves the caller's working
directory, so relative command-line paths keep their documented meaning. A
checkpoint is written atomically at the selected interval and can resume only
when archive, admission, EDCM package tree, UCNS commit, and already-processed source
prefix all match.

Successful completion requires:

- all `10,438` dialogues;
- all source turns observed exactly once by the adapter;
- all `143,048` source turns consumed by the UCNS v0.14.1 gate;
- UCNS source and reconstructed-observation stream digests equal;
- the repeated UCNS-pass source-native turn chain equals the first pass;
- unit support equal to adapted turn count;
- exact `8,438 / 1,000 / 1,000` train/validation/test reconciliation;
- every validation and test identifier present; and
- valid source JSON through EOF.

Any failure produces an incomplete receipt containing the last completed
dialogue and the active dialogue/turn position when available. Reports,
receipts, and checkpoints contain no raw turn text.

The v1.0.0 admission manifest remains committed under its versioned filename so
the 2026-07-28 report and receipt digests stay reconstructable. The live v1.1.0
manifest adds the already observed `143,048`-turn expectation and the explicit
v0.14.1 adapter, privacy, redaction, and admission-decision bindings. It does
not rewrite the historical evidence.

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

The historical replacement predates the UCNS v0.14.1 execution gate. Its
completion receipt remains valid for the EDCM v1.1 runner contract but cannot
be promoted into a v0.14.1 receipt. |∆|Only a fresh execution over the admitted
archive could create that receipt; the independently sealed execution below is
that new evidence.|∆|

## UCNS v0.14.1 sealed execution

The fresh run used clean EDCM merge commit
`2e667f648bfcfa9f067997eb7e56d2346a4ba30c` and exact UCNS commit
`868d80878c9ecd93ff30e91ca289122ded805a49`. It authenticated the admitted
archive and all 13 members, completed the EDCM pass, then independently replayed
all turns through the UCNS full-corpus executor. A checkpoint repeat produced
byte-identical artifacts.

- [aggregate report](../../experiments/corpora/results/2026-07-31-multiwoz-2.1-ucns-v0.14.1-full.json)
- [completion receipt](../../experiments/corpora/receipts/2026-07-31-multiwoz-2.1-ucns-v0.14.1-complete.json)
- dialogues: `10,438`
- source, adapter, UCNS-gate, and unit-support turns: `143,048`
- exact UCNS source/observation stream SHA-256: `e94ba2e5e1e9d52b23fd5b9c33303be009dae32f4c3bc6a1d5186a353acb40b5`
- UCNS receipt id: `921ceacad026de1d884eec3e049b090246014706c937c062bd32f40bbff01f0c`
- EDCM report digest: `ff4718ba80d40028cc18fc222eae53295d8ab9efebe4a5da6b0e7c47e6088b77`
- EDCM receipt digest: `4ebbb9a69be3690c01271e6a041de227e91615c073ad9e8601bdb9096fe41783`

The repeated UCNS-pass turn-evidence chain equals the source-native EDCM pass,
and the current failure-seeking aggregates equal the corrected 2026-07-28
profile-0.2 evidence. `canon_selection` remains null; EDCM and METAPAT
activation remain inactive.

```text
exact profile observation != formal UCNS geometry
represented evidence != candidate-measured evidence
candidate-measured evidence != canonically measured evidence
NA != 0
```

## UCNS v0.19 producer seal

After the v0.19 source-coordinate boundary reached clean review, EDCM repinned
the unchanged profile `0.2.0` and full-corpus gate `0.14.1` to exact UCNS commit
`872f53571d5dc2f133ff1813b7bdffd3a9c309f8`. Clean EDCM producer commit
`69f7470439ad5e3a578bf16eab8c6165b6ea07d6`, whose `edcm/` subtree is
`006441f18e665097e66d10af9486ad6512122757`, reran the admitted archive. A
completed-checkpoint repeat produced byte-identical artifacts.

Schema `1.3.0` seals the content-addressed Git tree for the executing `edcm/`
package rather than treating the intermediate producer commit as the durable
code identity. The same subtree is embedded unchanged in the evidence commit
and remains reachable after a squash merge; the producer commit is retained as
an audit coordinate but is not required to recover the executed package bytes.

- [aggregate report](../../experiments/corpora/results/2026-07-31-multiwoz-2.1-ucns-v0.19-full.json)
- [completion receipt](../../experiments/corpora/receipts/2026-07-31-multiwoz-2.1-ucns-v0.19-complete.json)
- dialogues: `10,438`
- source, adapter, UCNS-gate, and unit-support turns: `143,048`
- exact UCNS source/observation stream SHA-256: `e94ba2e5e1e9d52b23fd5b9c33303be009dae32f4c3bc6a1d5186a353acb40b5`
- UCNS receipt id: `921ceacad026de1d884eec3e049b090246014706c937c062bd32f40bbff01f0c`
- EDCM report digest: `161d0a981d7f62e1e33b38cadd1a05a41c3a92593b94fa4ee220f4e5d2fac97e`
- EDCM receipt digest: `7f23a5535e5d90da28ba08bc57ce2df0bdcf53b8a67d99dfe25afc7207ed0249`

The source dialogue chain, turn-evidence chain, execution counts, failure-seeking
aggregates, exact stream hash, and v0.14.1 gate receipt remain identical to the
prior sealed rerun. The EDCM report and receipt identities change because they
correctly bind the EDCM package tree and UCNS producer commit. UCNS v0.19's coordinate
candidate is evidenced only over its fixed full producer demonstration; this
corpus runner neither attaches nor consumes it. `canon_selection` remains null,
candidate measurement remains `not-run`, and EDCM/METAPAT remain inactive.

## File plan

| Path | Change | Purpose | Risk | Required test |
|---|---|---|---|---|
| `edcm/corpora/multiwoz21.py` | modified | admission, streaming, exact adaptation, checkpoint, dual reconciliation, and receipts | source-text leakage or false completion | `tests/test_multiwoz21_corpus.py` |
| `edcm/corpora/data/multiwoz_2_1_admission.json` | versioned | live source, license, privacy, and v0.14.1 execution contract | source/version ambiguity | archive mutation, historical-manifest identity, and receipt checks |
| `edcm/corpora/data/multiwoz_2_1_admission_v1_0_0.json` | preserved | reconstruct historical report admission identity | accidental historical rewrite | canonical manifest digest |
| `tests/test_multiwoz21_corpus.py` | modified | source-owned dual-gate contract witnesses | fixture/real-profile drift | full suite plus pinned UCNS test |
| `experiments/corpora/` | sealed evidence added | aggregate report and receipt only | accidental raw inclusion | tracked-file inspection, digest reconciliation, and byte-identical checkpoint repeat |
| `experiments/corpora/supersessions/2026-07-28-multiwoz-2.1-space-origin.json` | created | preserve the old evidence identity and bind the sealed replacement | replacement mismatch or historical rewrite | supersession identity, file digest, and source-chain reconciliation |
| `edcm_msdmd.ts` | regenerated | skill-lib metadata collection | stale contract graph | pinned skill-lib diff |

## hmmm

The corrected SPACE-origin totals and UCNS v0.14.1 execution receipt are sealed
represented evidence. The new receipt was earned by fresh execution rather than
inferred from the prior report. They are not formal Möbius geometry or an EDCM
measurement-validity claim. Source-native
labels for correction, retraction, refusal, and unresolved reference are not
complete in MultiWOZ 2.1 and remain unresolved rather than being guessed from
text. UCNS v0.19 supplies a nonselected trace-local source-coordinate candidate
over its fixed full producer demonstration, but this corpus runner does not
attach or consume it. Higher-gonol composition and lawful projection from exact
observations into EDCM scalar readouts remain open.
