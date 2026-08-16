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

Only entries explicitly marked `fetch_bytes` with public-domain authority are downloaded. `metadata_only` and `manual_review` entries remain source locators until exact object identity and rights are resolved.

After acquisition, EDCM may consume the evidence index and raw bytes to discover distinctions and relations. UCNS construction comes after those distinctions exist; neither this manifest nor the acquisition runner creates the Platonic Tarot card.

hmmm: source coverage, image-level acquisition, modern deck rights, transcription/OCR, and downstream multimodal EDCM ingestion remain open.
