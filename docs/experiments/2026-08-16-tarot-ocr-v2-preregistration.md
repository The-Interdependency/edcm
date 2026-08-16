# Tarot PDF OCR microscope v2 — preregistration

Status: frozen before v2 rendering, validation transcription, or OCR.

## Usage guidance

Read v1's complete frozen protocol first, then apply only the renderer-command
replacement below. All other v1 identities, controls, validation pages and
crops, transcription rules, accuracy thresholds, serialization, resource
bounds, stopping rules, provenance boundaries, and nonclaims remain exact and
unchanged. Run no v1 scratch output as v2 evidence.

## Frozen predecessor

- complete protocol: `edcm.tarot-ocr-protocol/1.0.0`, commit
  `d46f4ad849694b738b5211f9bcc3dadb49c2c9c1`, protocol-file SHA-256
  `e45712fe7140338e2b37135453b5f0cc6edbbe82d206018d26c131e7a29e0678`;
- v1 result: `BLOCKED` at commit
  `f4922fcabcd5797fc68201b6e777ddccdbb8edef` because MuPDF emitted
  `warning: ICC support is not available` and v1 blocked on any warning.

No semantic content was inspected and Tesseract was not run before this v2
freeze.

## Sole frozen change

Replace v1's renderer command with:

```text
mutool draw -q -N -r 300 -c gray -F png -o page-%04d.png INPUT.pdf 1-N
```

MuPDF 1.23.10 documents `-N` as disabling ICC workflow. This makes the
rendering color-management boundary explicit for 8-bit grayscale output and
removes the unsupported ICC path that blocked v1. The renderer executable,
version, digest, resolution, grayscale format, page order, timeout, and all
other rules are unchanged. Any stdout/stderr output or nonzero exit still
makes v2 `BLOCKED`.

hmmm: whether this sole change clears the producer gate and the otherwise
unchanged instrument recovers the eighteenth-century typography within the
frozen accuracy thresholds.
