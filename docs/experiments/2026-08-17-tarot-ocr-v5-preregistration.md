# Tarot PDF OCR microscope v5 — adaptive-threshold preregistration

Status: frozen before v5 OCR execution.

## Usage guidance

Read the v1 protocol and v4 findings first. V5 inherits every source,
renderer, page order, language model, segmentation/orientation rule, validation
reference, normalization, threshold, serialization rule, resource limit,
failure rule, provenance boundary, and nonclaim from v4. Execute v5 only with
the exact single OCR change below. Any further preprocessing, segmentation,
model, threshold, or parameter change requires a new preregistration.

## Predecessor evidence and rationale

V4 is sealed `FALSIFIED` at EDCM commit
`d5f8180581c1c808e4e609fe6ba92c85117eeb75` and merged by
`6ccde9c2c156ff692df2ac33fcc2350006a087b5`. Its complete 407-page run
produced empty text on 397 of 401 book pages and zero tokens on every frozen
book validation page. The failure is therefore text detection, not the
comparison crop.

Before selecting v5, discovery was restricted to producer inventory and
non-semantic grayscale statistics from the already frozen v4 PNGs. The eight
book validation pages span median grayscale values `122` through `150` and
fractions below gray `128` from `0.1051` through `0.6515`. This page-to-page
and within-page background variation supplies an independent technical reason
to replace global thresholding with one adaptive method. No v5 OCR candidate
was run, no output label was inspected, and no parameter search occurred.

## Sole frozen instrument change

Use Tesseract's built-in Sauvola thresholding with its installed defaults:

```text
OMP_THREAD_LIMIT=1 tesseract PAGE.png OUT -l fra --oem 1 --psm 3 \
  -c thresholding_method=2 txt tsv
```

The frozen producer reports:

```text
thresholding_method=2  Sauvola
thresholding_window_size=0.33
thresholding_kfactor=0.34
```

Do not tune the window or k-factor. Do not externally binarize, invert,
deskew, denoise, sharpen, crop, rescale, rotate, or change page segmentation.
The exact Tesseract executable, `tessdata_fast` French model, MuPDF renderer,
300-DPI grayscale inputs, and raw TXT/TSV retention remain unchanged.

## Frozen decision and stopping rule

Apply the complete v4 validation reference and exact-empty rule unchanged.
Any accuracy failure is `FALSIFIED`; any producer, identity, reference,
serialization, parse, or resource failure is `BLOCKED`; one passing complete
run is `UNRESOLVED`; two byte-identical passing complete runs are `SURVIVED`.
Stop after a terminal accuracy failure because replay cannot repair validity.

Passing would establish only that this exact adaptive-threshold instrument
survived this exact corpus gate. It would not prove the transcription or
establish Tarot ontology, card equivalence, semantic normalization, historical
truth, UCNS geometry, EDCM interpretation, Platonic-card construction, or
canon.

hmmm: whether fixed-default Sauvola thresholding is sufficient to expose the
eighteenth-century type to the otherwise unchanged OCR instrument.
