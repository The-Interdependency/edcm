# Tarot PDF OCR microscope v1 — findings

Status: `BLOCKED` before validation transcription or OCR.

## Usage guidance

Use this result as a fail-closed receipt for protocol v1. Do not treat it as an
OCR accuracy result and do not reject either source. Any later attempt must
preregister a new protocol version rather than changing v1.

## Result

The exact frozen renderer command emitted:

```text
warning: ICC support is not available
```

Protocol v1 states that any renderer warning is `BLOCKED`. The warning occurred
while rendering the preregistered validation pages, before any crop was viewed
or transcribed and before any Tesseract invocation. Therefore no accuracy or
determinism threshold was evaluated.

The generated validation-page and crop bytes are non-evidence scratch outputs.
Their existence does not advance the protocol because the renderer producer
failed its frozen acceptance rule.

## Preserved boundaries

- embedded-text extraction remains `FALSIFIED` from PR #58;
- OCR v1 is `BLOCKED`, not `FALSIFIED` and not `SURVIVED`;
- source semantic content was not inspected;
- Tarot ontology, card equivalence, semantic normalization, UCNS geometry,
  EDCM interpretation, Platonic-card construction, and canon remain absent;
- neither acquired Wellcome source is rejected.

hmmm: a new preregistration may explicitly disable MuPDF ICC handling with
the documented `-N` renderer option, because v1 cannot silently add it.
