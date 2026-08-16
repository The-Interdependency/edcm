# Tarot corpus acquisition — evidence before ontology

Status: first executable acquisition surface. It creates an auditable Tarot evidence snapshot; it does **not** define Tarot, perform EDCM embedding, construct UCNS objects, or claim a Platonic Tarot card.

## Work graph

- archival, museum, library, rules, primary-text, and scholarship sources own their own source content and claims;
- EDCM owns this manifest, acquisition policy, evidence indexing, and later distinction/relation discovery;
- UCNS owns downstream recursive relation representation once EDCM has surfaced distinctions;
- `skill-lib` owns build/evidence discipline.

No relation transfers semantic authority, historical truth, copyright authority, measurement validity, mathematical proof status, or canon standing.

## Construction boundary

The Tarot corpus begins as evidence envelopes:

```text
source identity
provenance
source date
media type
rights state
retrieval policy
raw bytes when lawfully and exactly retrievable
byte digest
```

There is no predeclared card schema. In particular, acquisition does not globally equate cards across decks and does not require 78 cards, 22 trumps, four suits, one numbering, one court structure, reversals, astrology, Kabbalah, or divinatory meanings. Those may occur in source evidence and are preserved as source-relative material for later EDCM discovery.

## Frozen v1 seed

`corpus/tarot/sources.v1.json` seeds the corpus across early deck/material witnesses, historical collections, occult/divinatory primary texts, a living game-rules surface, modern institutional interpretation, scholarship, and one near-neighbor negative control.

Only two entries currently authorize automatic bytes: Wellcome Collection's public-domain Etteilla materials. Other entries remain metadata or manual-review locators until exact downloadable identity and reuse authority are pinned. This is deliberate fail-closed behavior, not an assertion that the other sources are less important.

## Usage

Validate the manifest without network or writes:

```bash
python tools/acquire_tarot_corpus.py --dry-run
```

Acquire authorized bytes and seal the snapshot:

```bash
python tools/acquire_tarot_corpus.py \
  --manifest corpus/tarot/sources.v1.json \
  --output artifacts/tarot/acquisition-v1
```

Resume an interrupted run or verify/reuse a completed run:

```bash
python tools/acquire_tarot_corpus.py \
  --manifest corpus/tarot/sources.v1.json \
  --output artifacts/tarot/acquisition-v1 \
  --resume
```

The runner streams downloads with a per-source byte ceiling, checkpoints completed sources, and fails closed on stale manifest identity, changed source entries, altered bytes, missing files, or injected files.

Validate the implementation:

```bash
python -m pytest tests/test_tarot_corpus_acquisition.py
python tools/check_metadata_contracts.py
```

## Next stage

The acquisition output is an input boundary for EDCM, not an embedding itself.
The first bounded discovery stage is now executable:

```bash
python tools/discover_tarot_relations.py \
  --manifest corpus/tarot/sources.v1.json \
  --acquisition artifacts/tarot/acquisition-v1 \
  --output artifacts/tarot/relations-v1.json
```

This stage validates the complete sealed acquisition, preserves manifest order
and exact field values, records typed absence, binds fetched artifacts, and
reports only same-field byte-exact agreement. It does not inspect PDF content,
tokenize or normalize language, infer card identity, select an ontology, build
UCNS objects, or run EDCM measurement. A single result remains `UNRESOLVED`;
repeat-run byte identity is determinism evidence only.

The wider path remains:

```text
Tarot evidence snapshot
    -> EDCM source-envelope distinction/relation discovery [implemented]
    -> embedded-text extraction [FALSIFIED for both acquired PDFs]
    -> OCR v1 [BLOCKED: renderer warning]
    -> OCR v2 [BLOCKED: tableau validation sample lacks 100 decidable characters]
    -> source-faithful multimodal transcription design [hmmm]
    -> semantic discovery [not run]
    -> provenance-bearing recovered relations
    -> UCNS recursive objects
    -> reconstruction/adversarial tests
    -> hmmm: emergent Platonic Tarot card
```

EDCM should be allowed to discover that two sources agree, disagree, split, merge, omit, reinterpret, or fail to map. Acquisition must not erase those possibilities by preprocessing them into one Tarot taxonomy.

## hmmm

- comprehensive source coverage is impossible to claim from v1;
- item-level IIIF and reuse identities remain unresolved for several major collections;
- modern commercial decks and guidebooks need source-specific lawful acquisition;
- OCR is preregistered and twice blocked before execution; no OCR output exists;
- a source-faithful control must not force the predominantly visual tableau into a text-only validity criterion;
- image segmentation, multimodal transcription, language normalization, and semantic discovery remain separate undefined transformations;
- the Platonic Tarot card remains a target of discovery, not an input schema.
