# Tarot PDF OCR microscope v7 — findings

Status: `FALSIFIED` after one complete 407-page run. Replay was not run because
the frozen accuracy failure is terminal.

## Usage guidance

Use this result to reject the exact v7 source-wide text-OCR instrument and to
bound the next architecture. The raw run remains at
`artifacts/tarot/ocr-v7/run-a`; verify its hashes against the committed receipt.
Do not tune, combine models, reinterpret false text, or call the output a
trustworthy corpus.

## Exact result

The historic Latin-print model improved recognition relative to v5:

- book CER: `0.07681692732290708`, below the frozen source maximum `0.10`;
- book WER: `0.27906976744186046`, above the frozen aggregate maximum `0.20`;
- five of eight book samples have CER below `0.07`;
- the previous near-total miss on book page `0375` improved from CER `0.9969`
  to `0.1807`.

The complete source-wide gate nevertheless fails decisively:

- aggregate CER/WER: `0.15585241730279897` / `0.4250936329588015`;
- tableau CER/WER: `0.33298969072164947` / `0.8095238095238095`;
- tableau page `0005` produces nonempty OCR against an exact-empty reference;
- tableau pages `0002` and `0003` generate large false-positive token sets;
- tableau page `0006` misses its small textual reference entirely;
- book WER remains above the required transcription threshold.

## Decisive boundary

V4 established that global-threshold modern-French OCR could not detect the
book. V5 established that adaptive thresholding mostly repairs detection. V7
establishes that a generic historic-print model materially repairs book
character recognition but does not meet word accuracy and cannot turn a
predominantly visual tableau into a source-faithful text transcription.

Further single-model Tesseract substitution is irrational under the frozen
stopping rule. The remaining work is not one more text-recognition parameter:
it requires an independently preregistered architecture that distinguishes
text-bearing regions from visual evidence, preserves nontext rather than
hallucinating it as language, and validates each modality under its own lawful
criterion. That is a new multimodal/region-classification experiment, not a
repair to this OCR microscope.

## Evidence boundary

- OCR v7: `FALSIFIED`;
- deterministic replay: not run because it cannot repair accuracy;
- trustworthy transcription corpus: not produced;
- source rejection: false;
- surviving local result: historic-model + Sauvola book CER survived its
  source-level character threshold, while book WER did not;
- ontology, equivalence, semantic normalization, historical truth, UCNS
  geometry, EDCM interpretation, Platonic-card construction, and canon remain
  absent.

hmmm: the next lawful microscope is a preregistered multimodal region gate with
separate text-recognition and nontext-preservation validation, not another
whole-page OCR model.
