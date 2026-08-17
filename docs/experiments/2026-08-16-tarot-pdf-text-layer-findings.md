# Tarot PDF embedded-text gate — findings

Result: **FALSIFIED**.

The preregistered MuPDF 1.23.10 embedded-text route failed on both exact
Wellcome PDFs. The 401-page Etteilla text contained only 820 non-whitespace
characters and one populated page; it required at least 100,000 characters and
361 populated pages. The 6-page tableau contained 685 non-whitespace characters
and one populated page; it required five populated pages. Both reports were
byte-identical across independent execution.

An initial pre-extraction attempt was `BLOCKED` because the harness read the
backend version from stdout while MuPDF writes it to stderr. No text extraction
occurred in that attempt. Commit `85c9985` corrected only diagnostic-stream
capture; the preregistered backend, inputs, command, measurements, thresholds,
and decision rule remained unchanged.

This falsifies only embedded-text ingestion for these acquired PDFs. It says
nothing about their image content, historical claims, card structure, or the
quality attainable through OCR. No extracted text was semantically inspected
or committed.

## Next boundary

OCR is required, but this MuPDF build reports OCR output as disabled and no
pinned OCR producer exists in the current work graph. Before OCR, freeze:

- exact OCR engine, version, executable/model digests, and license;
- deterministic page rendering backend, resolution, color law, and page order;
- language/script models for eighteenth-century French typography;
- segmentation and orientation rules;
- an independently transcribed validation subset and accuracy thresholds;
- failure, disagreement, resource, and stopping rules;
- preservation of page images, raw OCR alternatives, confidence, order, and
  provenance without conventionalizing Tarot terminology.

hmmm: choosing that OCR microscope and obtaining an independent transcription
control is the next load-bearing authority/evidence boundary.
