# Molweni full-corpus run

**Status:** admitted source-native adapter; full evidence is aggregate-only.

**Source:** [`HIT-SCIR/Molweni`](https://github.com/HIT-SCIR/Molweni) at
`2eb681d7e610ee3fda4ab3b4cc364554bd17ee67`.

**Paper:** [Li et al., COLING 2020](https://aclanthology.org/2020.coling-main.238/).

**License:** Apache-2.0 as declared by the pinned repository.

## Preserved structure

Molweni publishes two differently partitioned annotation views derived from the
same Ubuntu chat source:

- **DP:** 10,000 dialogues, 88,303 explicit speaker EDUs, and 78,245 directed
  labeled discourse relations;
- **MRC(withDiscourse):** 9,754 dialogue annotation records and 30,066
  questions, including 25,779 answerable and 4,287 unanswerable questions with
  plausible spans.

The DP view is the complete exact turn stream. Every DP `edus[].text` enters the
pinned EDCM UCNS word-gonol profile exactly once. Nonempty
`edus[].speaker` strings pass unchanged. The release also contains 176 empty
speaker fields; those remain malformed source evidence and receive a
collision-checked dialogue/turn ordinal sentinel only at the adapter boundary,
where the pinned profile requires a nonempty identifier. The directed relation
list is retained beside that stream, not flattened into text or used to invent
a metric.

The MRC view is fully validated as an annotation layer. Context strings,
duplicate EDUs, relation lists, questions, answerability flags, answers,
plausible answers, and exact context spans are digested and reconciled. Its EDU
text is not measured a second time. Complete ordered EDU identity is compared
with DP independently from relation-graph identity, so identical turns with a
different graph remain positive disagreement evidence.

One released MRC dev dialogue has 12 EDUs but includes two edges targeting
ordinals 12 and 13. The adapter retains those malformed edge objects in the
annotation digest and reports them as `2 edges / 1 dialogue`; it does not drop
or repair them. DP endpoint validation remains strict because its complete
relation layer has no invalid endpoints.

## Usage guidance

Clone the official source outside this repository and pin it exactly:

```bash
git clone https://github.com/HIT-SCIR/Molweni.git /tmp/molweni
git -C /tmp/molweni checkout 2eb681d7e610ee3fda4ab3b4cc364554bd17ee67
```

Keep the checkout clean, provide the exact pinned UCNS source tree, and run:

```bash
python -m edcm.corpora.molweni \
  --source-root /tmp/molweni \
  --ucns-source-root /path/to/ucns-at-eb264fba18bd051c46b4853c81c8fb91ec6d5811 \
  --output experiments/corpora/results/2026-07-28-molweni-full.json \
  --receipt experiments/corpora/receipts/2026-07-28-molweni-complete.json \
  --checkpoint /tmp/molweni.checkpoint.json
```

The command verifies the Git commit and every admitted file hash before
observing source text. Checkpoints resume the DP profile phase. If the MRC phase
is interrupted, it restarts from the beginning so annotation counts cannot be
skipped or doubled.

Run its focused checks with:

```bash
python -m pytest -q tests/test_molweni_corpus.py
python tools/check_metadata_contracts.py
```

## Interpretation boundary

The report is represented evidence. It does not select an EDCM or UCNS canon,
repair a source graph, infer psychological properties, or convert a discourse
label, an unanswerable question, or a plausible span into a measured value.

Molweni is a filtered and annotated derivative of Ubuntu chat. Upstream
collection effects and Molweni selection, utterance-length filtering,
speaker-count filtering, discourse annotation, and MRC annotation remain
inseparable provenance.

## File plan

| Path | Change | Purpose | Primary risk | Required checks |
|---|---|---|---|---|
| `edcm/corpora/molweni.py` | created | admission verification, exact DP profile execution, graph retention, MRC validation, reconciliation, checkpoint, and receipts | false completion, graph flattening, duplicate measurement, or raw-text leakage | `tests/test_molweni_corpus.py` |
| `edcm/corpora/data/molweni_admission.json` | created | immutable repository/file, license, privacy, expected-count, and execution contract | source-version or annotation-boundary ambiguity | source mutation and reconciliation checks |
| `edcm/corpora/__init__.py` | modified | lazy public Molweni execution aliases | import-time side effects or wrong runner routing | full test suite |
| `docs/corpora/molweni.md` | created | copy-pasteable execution and interpretation guidance | overstated evidence status | documentation and metadata review |
| `experiments/corpora/` | updated only after a sealed run | Git-safe aggregate report and completion receipt | accidental raw source inclusion | tracked-file inspection and digest reconciliation |

## hmmm

The released DP and MRC views contain two identical-EDU cases with different
relation graphs. The runner retains both identities and the disagreement, but
the source does not establish which graph, if either, should be preferred.
The upstream meaning or cause of 176 empty released speaker fields is likewise
unknown; the adapter does not infer a participant for them.
