# Tarot corpus

This directory is the provenance-first input surface for discovering Tarot distinctions and relations with EDCM.

It deliberately contains **no Tarot ontology**. It does not select a canonical deck, 78-card requirement, Major/Minor split, suit system, numbering, card identity mapping, divinatory meaning, occult correspondence, or historical interpretation. Sources may assert any of those things; the manifest preserves who asserted what and where the evidence lives.

`sources.v1.json` is intentionally open-ended: a corpus snapshot is maximal only relative to admitted evidence. I Ching is out of scope and will receive an independent corpus later.

## Usage

```bash
python tools/acquire_tarot_corpus.py --dry-run
python tools/acquire_tarot_corpus.py --output artifacts/tarot/acquisition-v1
python tools/acquire_tarot_corpus.py --output artifacts/tarot/acquisition-v1 --resume
```

Then discover only the exact source-envelope relations:

```bash
python tools/discover_tarot_relations.py \
  --manifest corpus/tarot/sources.v1.json \
  --acquisition artifacts/tarot/acquisition-v1 \
  --output artifacts/tarot/relations-v1.json
```

Only entries explicitly marked `fetch_bytes` with public-domain authority are downloaded. `metadata_only` and `manual_review` entries remain source locators until exact object identity and rights are resolved.

The first discovery runner consumes the evidence index but does not inspect raw
PDF content. It retains source order, exact values, typed absence, artifact
bindings, and byte-exact same-field agreement. UCNS construction comes after
the distinctions exist; neither this manifest nor either runner creates the
Platonic Tarot card.

hmmm: source coverage, image-level acquisition, modern deck rights, transcription/OCR, and downstream multimodal EDCM ingestion remain open.
