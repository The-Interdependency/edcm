# Tarot PDF OCR microscope v7 — renderer-flag repair preregistration

Status: frozen before v7 OCR execution.

## Usage guidance

V7 inherits v6 in full and changes only how Tesseract's TXT and TSV renderers
are enabled. Run it with the exact historic model and existing sealed
reference. Do not change the model, thresholding, segmentation, page handling,
validation, or thresholds.

## Frozen predecessor

V6 is `BLOCKED` at commit
`843e8af0e2f0fe98e84ed7fba34fe6a16d8ff8e1` with zero admitted pages. Its
custom model-only `--tessdata-dir` lacks the named `txt` and `tsv` config
files. The installed Debian configs contain only the relevant declarations:

```text
tessedit_create_txt 1
tessedit_create_tsv 1
```

Their SHA-256 identities are respectively
`9bcbdbe285fd3a024be563cb237751ceb3435d86610e231f08894023321af5d7`
and `59d079bb75d8b3d7c839a3564580cb559e362c93a9d70f234e421c0c3e767e04`.
The engine's frozen parameter inventory independently exposes both boolean
parameters with default zero. No v6 accuracy output exists.

## Sole frozen repair

Replace terminal config filenames `txt tsv` with their exact engine
parameters:

```text
OMP_THREAD_LIMIT=1 tesseract PAGE.png OUT \
  --tessdata-dir artifacts/tarot/ocr-models \
  -l frak2021-0.905 --oem 1 --psm 3 \
  -c thresholding_method=2 \
  -c tessedit_create_txt=1 \
  -c tessedit_create_tsv=1
```

This does not admit the Debian renderer config files as mutable runtime inputs;
their content only establishes equivalence before freeze. The v7 command uses
engine parameters directly and requires both output files before admitting a
page.

## Frozen decision and stopping rule

All v6/v5 accuracy, replay, identity, resource, provenance, and nonclaim rules
remain unchanged. Accuracy failure is `FALSIFIED`; producer or evidence failure
is `BLOCKED`; one passing run is `UNRESOLVED`; two byte-identical passing runs
are `SURVIVED`. Stop after terminal accuracy failure.

hmmm: whether the now-executable historic-print instrument meets the frozen
source-wide validation gate.
