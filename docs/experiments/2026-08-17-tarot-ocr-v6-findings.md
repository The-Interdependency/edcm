# Tarot PDF OCR microscope v6 — findings

Status: `BLOCKED` before any page was admitted.

## Usage guidance

Use this result only to reject the exact v6 producer interface. Do not infer
anything about historic-model accuracy from it. The page-1 render and TXT are
unadmitted partial files and must not enter a corpus or validation result.

## Exact blocker

The historic model is stored in its own frozen `--tessdata-dir`. Tesseract
therefore also searched that directory for the terminal `txt` and `tsv`
renderer config files. They are absent from the model-only cache. Tesseract
returned zero, emitted `Can't open txt` and `Can't open tsv` diagnostics, wrote
only its default TXT output, and omitted the required TSV output. The v6 runner
failed closed at book page `0001` before checkpointing it.

This is a command/configuration boundary, not an OCR observation. No v6
candidate was scored and no semantic content was inspected. The exact Debian
renderer configs independently show that `txt` sets
`tessedit_create_txt=1` and `tsv` sets `tessedit_create_tsv=1`; an explicit
parameter form can repair the interface without changing the model or OCR
method, but it requires a new preregistration.

## Evidence boundary

- OCR v6: `BLOCKED`;
- admitted pages: `0`;
- accuracy and determinism: not evaluated;
- trustworthy transcription corpus: not produced;
- v5 remains separately `FALSIFIED`;
- source rejection and all semantic, ontological, UCNS, EDCM, Platonic-card,
  historical-truth, and canon claims remain absent.

hmmm: whether the unchanged v6 model survives after the renderer-output flags
are made independent of the custom tessdata directory.
