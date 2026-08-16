# Tarot PDF OCR microscope v2 — findings

Status: `BLOCKED` before reference transcription or OCR.

## Usage guidance

Use this result with the v1 and v2 protocol records. It establishes that the
ICC-disabled renderer cleared its producer gate, but the frozen validation
sample cannot support the required per-source accuracy control. Do not replace
the samples, infer OCR accuracy, reject either source, or run Tesseract under
this protocol.

## Result

The exact v2 renderer commands completed with zero stdout, zero stderr, and
zero exit status. The ten selected 300-DPI grayscale pages and their frozen
crops were materialized. The canonical crop-manifest SHA-256 is
`f78554ea2452fdf1e626cf1d15c3366486d8d1606425372e18f0715922fed6ad`.

Independent inspection of only those preregistered crops found:

- the eight book crops contain decidable printed French text;
- tableau page `0002` is a visual arrangement with symbols and images but no
  100-character textual reference in the crop;
- tableau page `0005` is blank in the crop;
- the tableau source therefore has fewer than the frozen minimum of 100
  decidable reference characters across its two samples.

Protocol v1, inherited unchanged by v2, says this condition is `BLOCKED` and
forbids replacing a sample after inspection. Tesseract was not invoked. No CER,
WER, raw OCR, confidence, alternative, or complete-corpus output exists.

## Evidence status

- embedded-text extraction: `FALSIFIED`;
- OCR v1: `BLOCKED` at the renderer gate;
- OCR v2: `BLOCKED` at the independent-reference gate;
- source rejection: false;
- ontology, card equivalence, semantic normalization, UCNS geometry, EDCM
  interpretation, Platonic-card construction, and canon: not run/absent.

The result is also modality evidence: the tableau PDF is not lawfully reduced
to a text-only success criterion by this experiment. It does not by itself
define the next multimodal representation or authorize a new sample.

hmmm: a next experiment requires an independently authorized validation design
that distinguishes text-bearing book pages from a predominantly visual
tableau without selecting text regions after seeing this failed sample.
