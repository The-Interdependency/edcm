# Tarot PDF OCR microscope v6 — historic-print model preregistration

Status: frozen before v6 OCR execution.

## Usage guidance

Read v1, v5's protocol, and v5's findings first. V6 inherits v5's exact
sources, renderer, 300-DPI grayscale pages, fixed-default Sauvola thresholding,
OEM, PSM, orientation, sealed reference, scoring, thresholds, serialization,
resources, failure rules, provenance boundaries, and nonclaims. It replaces
only the recognition model. Do not run v6 until this protocol is committed.

## Predecessor evidence and independent rationale

V5 is sealed `FALSIFIED` at commit
`ffb85e7ce0f796d763165f6224b0bd9ffe9ae05a`. It recovered text on 392 of 401
book pages, so another threshold or segmentation change is not justified.
Seven of eight book validation crops reached CER `0.0701`–`0.1261`, while
book WER remained `0.4625`. This separates remaining historical-character and
word recognition from v4's broad detection failure.

The v6 model was chosen by declared training domain before running it:
Zenodo record `10125246` describes `frak2021-0.905.traineddata` as a generic
Tesseract best model for historic Latin-script prints, trained mainly on
German and Latin ground truth and explicitly usable for French and other
Western European texts. It is the smallest available change that targets the
remaining historical-print recognition layer while retaining the exact v5
engine and image path. No v6 OCR was run and no candidate score was observed.

## Frozen model and provenance

- source: Zenodo record `10125246`, DOI `10.5281/zenodo.10125246`;
- title: *Tesseract OCR models for historic prints based on Latin script*;
- creator: Stefan Weil, ORCID `0000-0002-0524-9898`;
- immutable API content URL:
  `https://zenodo.org/api/records/10125246/files/frak2021-0.905.traineddata/content`;
- filename: `frak2021-0.905.traineddata`;
- bytes: `3421140`;
- Zenodo checksum: `md5:234e8bb819042f615576bd01aa2419fd`;
- independently computed SHA-256:
  `1da2384254fa8462c776faf3b43307fe19ce51be0931c623b2fdd560f96e299a`;
- license: CC0-1.0; external model, cached outside Git and not redistributed
  by the EDCM package.

The model cache path is
`artifacts/tarot/ocr-models/frak2021-0.905.traineddata`. A fresh checkout must
acquire the exact content URL and verify byte count, MD5, and SHA-256 before
execution. Missing or drifting model bytes are `BLOCKED`.

## Sole frozen instrument change

```text
OMP_THREAD_LIMIT=1 tesseract PAGE.png OUT \
  --tessdata-dir artifacts/tarot/ocr-models \
  -l frak2021-0.905 --oem 1 --psm 3 \
  -c thresholding_method=2 txt tsv
```

Do not combine the historic model with French `tessdata_fast`, add a lexicon,
normalize long-s, tune Sauvola, change segmentation, or post-correct output.
Raw model characters are compared under the unchanged source-faithful rule.

## Frozen decision and stopping rule

Any inherited accuracy failure is `FALSIFIED`; any producer, model, identity,
reference, parse, serialization, or resource failure is `BLOCKED`; one passing
complete run is `UNRESOLVED`; two byte-identical passing complete runs are
`SURVIVED`. Stop after terminal accuracy failure. If v6 fails, further
single-model Tesseract escalation is irrational without an independently
justified French diachronic model and a separate treatment of visual pages.

Passing establishes only bounded OCR survival. It does not prove a
transcription or establish ontology, card equivalence, semantic normalization,
historical truth, UCNS geometry, EDCM interpretation, Platonic cards, or canon.

hmmm: whether a generic historic Latin-print model transfers sufficiently to
the eighteenth-century French book without increasing tableau false text.
