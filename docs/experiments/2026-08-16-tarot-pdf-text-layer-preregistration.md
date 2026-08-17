# Tarot PDF embedded-text gate — preregistration

Status: frozen before text extraction. This gate asks only whether the two
acquired Wellcome PDFs contain an adequate embedded text layer for later
source-relative discovery. It does not test OCR and does not inspect meaning.

## Frozen inputs and backend

- `wellcome_etteilla_1783_1785.pdf`: 401 pages, SHA-256
  `d44fc8bf81e5356fa1f05d11a9e92723ee36efe94b3af2def5c1c97e80ff5c0f`.
- `wellcome_etteilla_tableau_1780s.pdf`: 6 pages, SHA-256
  `d3a2e8e82c79e9a109e662e53ff034dcabc7f2902c52dcde10fec9d3529f5381`.
- backend: MuPDF `mutool 1.23.10`, executable SHA-256
  `9203440040cc38ee412aeedbfe57f452d6b85709c5b1600ca6ab2aa05478ab73`.
- command: `mutool draw -q -F txt -o page-%04d.txt INPUT.pdf`.

MuPDF reports OCR formats as disabled in this build. No alternate extractor,
OCR engine, language model, page sampling, normalization, or manual reading is
allowed in this experiment.

## Frozen measurements

For every page, over exact UTF-8 extractor output:

- non-whitespace code-point count;
- Unicode alphanumeric code-point count;
- U+FFFD replacement-character count;
- SHA-256 of the exact page output.

No case folding, accent removal, tokenization, header removal, or semantic
filter is applied.

## Frozen decision rule

The 401-page text passes only if all hold:

- at least 361 pages contain at least 100 non-whitespace code points;
- total non-whitespace code points are at least 100,000;
- alphanumeric code points are at least 50% of non-whitespace code points;
- replacement characters are at most 1% of non-whitespace code points.

The 6-page tableau passes only if all hold:

- at least 5 pages contain at least 100 non-whitespace code points;
- total non-whitespace code points are at least 500;
- the same 50% alphanumeric and 1% replacement limits hold.

Both inputs must pass for `SURVIVED`. Any failed input makes the embedded-text
route `FALSIFIED`. Backend/input drift, timeout, missing pages, decoding error,
or execution error is `BLOCKED`, never a pass. One report is `UNRESOLVED` until
an independent byte-identical replay agrees.

Passing establishes extractor adequacy only, not transcription correctness,
linguistic validity, card identity, ontology, UCNS geometry, EDCM measurement,
or canon. Failure authorizes only a separately preregistered OCR/image route.

hmmm: if this gate is falsified, select and pin an OCR backend, language model,
page-image rendering law, resolution, segmentation, accuracy controls, and
failure thresholds before examining OCR output.
