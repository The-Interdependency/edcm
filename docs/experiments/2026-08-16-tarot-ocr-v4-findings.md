# Tarot PDF OCR microscope v4 — findings

Status: `FALSIFIED` after one complete 407-page run. Replay was not run because
accuracy failure is terminal under the frozen protocol.

## Usage guidance

Use this result to reject only the exact v4 OCR instrument, not the acquired
sources. The raw run remains under `artifacts/tarot/ocr-v4/run-a`; verify it
against the committed receipt's manifest and validation digests. Do not tune
Tesseract, swap models, preprocess images, loosen thresholds, or reinterpret
the output as a trustworthy transcription under this protocol.

## Exact instrument result

The run completed all 407 pages under the pinned MuPDF 1.23.10 renderer,
Tesseract 5.3.4 engine, and French `tessdata_fast` 4.1.0 model. It retained
every 300-DPI grayscale PNG, raw TXT, raw TSV, word confidence, page identity,
and typed absence of character alternatives.

Frozen validation result:

- aggregate CER: `0.7150127226463104` (maximum `0.08`);
- aggregate WER: `0.7846441947565543` (maximum `0.20`);
- book CER/WER: `1.0` / `1.0`;
- tableau CER/WER: `0.07628865979381444` / `0.21768707482993196`;
- every one of the eight preregistered eighteenth-century book samples yielded
  zero raw TXT and zero TSV word tokens, hence page CER/WER `1.0`;
- tableau pages `0004` and `0005` correctly remained exact-empty;
- tableau pages `0002`, `0003`, and `0006` independently failed page-level
  controls even though the modern Wellcome cover page `0001` matched exactly.

The complete-corpus audit makes the mechanism explicit: 397 of 401 book TXT
files are empty. Only 603 words were detected across the entire book, while
the selected historical body pages were completely undetected. The failure is
therefore not a crop-coordinate reconstruction defect. This exact automatic
segmentation/French-fast-model instrument does not recover the book's
eighteenth-century typography.

## Evidence boundary

- OCR v4: `FALSIFIED`;
- deterministic replay: not run, because it cannot repair accuracy;
- sealed trustworthy transcription corpus: not produced;
- source rejection: false;
- embedded-text result remains separately `FALSIFIED`;
- Tarot ontology, card equivalence, semantic normalization, UCNS geometry,
  EDCM interpretation, Platonic-card construction, historical truth, and canon
  remain absent.

hmmm: a new instrument would require a new preregistration with independently
justified preprocessing, segmentation, and/or historical-type model. V4 gives
no authority to feature-search among them.
