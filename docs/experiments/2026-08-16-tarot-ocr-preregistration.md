# Tarot PDF OCR microscope — preregistration

Status: frozen before page rendering, validation transcription, or OCR. This
experiment asks only whether one exact OCR instrument is accurate and
deterministic enough to produce a source-faithful transcription corpus from
the two acquired Wellcome PDFs whose embedded-text route was falsified.

## Usage guidance

Run only from a checkout containing this frozen protocol and the exact
acquisition under `artifacts/tarot/acquisition-v1`. First materialize the
validation crops without invoking Tesseract, transcribe them literally, and
seal that independent reference. Only then may the complete OCR command run.
Do not read OCR output before the reference seal exists.

The execution tool and exact commands are added after this preregistration
commit. They must implement these constants without changing them. Any needed
change first records this protocol `FALSIFIED`, `UNRESOLVED`, or `BLOCKED` and
starts a new version; it does not repair version 1 in place.

## Frozen inputs and authority

- EDCM parent commit: `9db7912eb439738d76479467daae671df46efc0d`.
- `wellcome_etteilla_1783_1785.pdf`: 401 pages, 77,852,106 bytes,
  SHA-256 `d44fc8bf81e5356fa1f05d11a9e92723ee36efe94b3af2def5c1c97e80ff5c0f`.
- `wellcome_etteilla_tableau_1780s.pdf`: 6 pages, 869,817 bytes,
  SHA-256 `d3a2e8e82c79e9a109e662e53ff034dcabc7f2902c52dcde10fec9d3529f5381`.
- Wellcome Collection owns source/item provenance and declares both downloads
  with a Public Domain Mark. EDCM owns only the acquisition, transformation,
  validation, and evidence records.
- `The-Interdependency/skill-lib@b4234ca29529f56526541df8deb58c2c19570792`
  supplies build/evidence discipline; it supplies no OCR validity.

## Frozen renderer

- Debian package `mupdf-tools 1.23.10+ds1-1build3`.
- command identity `mutool version 1.23.10`.
- `/usr/bin/mutool`: 44,735,344 bytes; SHA-256
  `9203440040cc38ee412aeedbfe57f452d6b85709c5b1600ca6ab2aa05478ab73`.
- license boundary: Debian records MuPDF core as AGPL-3+ with separately
  identified bundled-component licenses. The executable is an external tool;
  it is not redistributed by EDCM.
- render command, once per source in manifest order:

  ```text
  mutool draw -q -r 300 -c gray -F png -o page-%04d.png INPUT.pdf 1-N
  ```

- resolution: 300 DPI; color: 8-bit grayscale PNG; no alpha request,
  binarization, deskew, crop, rescale, denoise, sharpening, rotation, or page
  deletion.
- page order: PDF source order, one-based and zero-padded to four digits.
- every PNG is retained by page identity and SHA-256. A page count mismatch,
  renderer warning/error, or repeat-render digest mismatch is `BLOCKED`.

## Frozen OCR engine and model

- Debian `tesseract-ocr 5.3.4-1build5`, `libtesseract5 5.3.4-1build5`,
  `liblept5 1.82.0-3build4`.
- `/usr/bin/tesseract`: 39,320 bytes; SHA-256
  `9f831cab7525c3dab04af41bda35182af7ea1df9dceeaaa2f3bf207ac45c06a5`.
- engine version begins exactly `tesseract 5.3.4` and `leptonica-1.82.0`.
- model: Debian `tesseract-ocr-fra 1:4.1.0-2`, upstream `tessdata_fast`;
  `/usr/share/tesseract-ocr/5/tessdata/fra.traineddata`: 1,130,365 bytes;
  SHA-256 `ced037562e8c80c13122dece28dd477d399af80911a28791a66a63ac1e3445ca`.
- Tesseract and the French model are Apache-2.0. They are external producers
  and are not redistributed by EDCM.
- no English or orientation model is admitted. No network lookup, dictionary
  augmentation, training, correction, or post-OCR language model is admitted.
- exact OCR calls for every rendered page:

  ```text
  OMP_THREAD_LIMIT=1 tesseract PAGE.png OUT -l fra --oem 1 --psm 3 txt tsv
  ```

- segmentation: Tesseract page segmentation mode 3 (automatic page
  segmentation without orientation/script detection). Orientation is the
  renderer's source orientation. No rotation is inferred or applied.
- raw UTF-8 `.txt` and raw tab-separated `.tsv` are retained. TSV supplies the
  engine's word-level confidence and geometry. Character alternatives are
  unavailable from this interface and are recorded as typed `NA`, not
  reconstructed.

## Frozen independent validation sample

The reference transcription is produced before any Tesseract invocation.
Selection is independent of image or text content:

- book pages: `0025`, `0075`, `0125`, `0175`, `0225`, `0275`, `0325`, `0375`;
- tableau pages: `0002`, `0005`;
- sample crop on each 300-DPI page: integer pixel box
  `(floor(0.10*w), floor(0.30*h), ceil(0.90*w), ceil(0.55*h))`, with right and
  bottom exclusive;
- crop bytes are lossless grayscale PNG and are pinned by digest before
  transcription;
- the independent reference records exact visible reading order and literal
  characters, including accents, punctuation, capitalization, long-s/modern-s
  distinction where visually decidable, line breaks, uncertain glyphs, and
  illegible regions. Uncertain glyphs use U+FFFD; an illegible contiguous
  region uses one U+FFFD. Whitespace outside line breaks is transcribed as one
  ASCII space.

The reference file and crop manifest must be committed in a dedicated
pre-OCR seal. The transcriber must not run or inspect Tesseract output first.
The execution receipt records the reference commit. If either source has fewer
than 100 decidable reference characters across its crops, the experiment is
`BLOCKED`; no sample is replaced after inspection.

## Frozen comparison and thresholds

For validation only, crop each page's raw OCR TSV tokens to words whose box
centres fall inside the frozen crop, order by TSV `(page, block, paragraph,
line, word)`, and join words with one ASCII space per line and `\n` between
lines. Apply the same comparison normalization to reference and candidate:

1. Unicode NFC;
2. CRLF/CR to LF;
3. trim outer whitespace on each line;
4. collapse internal Unicode whitespace to one ASCII space;
5. drop empty lines;
6. join remaining lines with LF.

No case folding, accent removal, spelling modernization, hyphen repair,
punctuation deletion, `ſ`/`s` equivalence, or semantic correction is allowed.
Character error rate (CER) and word error rate (WER) use standard Levenshtein
distance divided by reference character and whitespace-token counts.

`SURVIVED` requires all of:

- aggregate CER across all samples at most `0.08`;
- aggregate WER across all samples at most `0.20`;
- each source's aggregate CER at most `0.10`;
- no individual crop CER above `0.20`;
- no U+FFFD in OCR output;
- two complete runs produce byte-identical canonical manifests and identical
  raw text/TSV digests for every page.

Any accuracy or determinism threshold failure is `FALSIFIED`. Missing or
drifting inputs, executables, models, reference seal, pages, output files,
parse failures, or resource exhaustion is `BLOCKED`. A completed first run is
`UNRESOLVED` until the independent complete replay agrees.

## Frozen serialization, resources, and stopping rules

- canonical JSON: UTF-8, keys sorted, separators `(',', ':')`, ensure-ASCII
  false, one trailing LF;
- page records are source order then page number and contain source/page
  identity, renderer digest, TXT digest, TSV digest, byte counts, and TSV word
  confidence values without rounding;
- raw files remain outside Git under the existing `artifacts/tarot/` pipeline;
  Git seals manifests, receipts, validation reference, findings, and exact
  artifact digests;
- maximum 407 pages, 2 GiB rendered bytes, 1 GiB OCR bytes, 20 seconds render
  per page, 60 seconds OCR per page, and 8 hours per complete run;
- process pages sequentially with one OCR thread; checkpoint after every page;
  resume accepts only exact verified prior outputs and never skips an
  unverified page;
- stop immediately as `BLOCKED` on identity drift, unexpected files, limit
  breach, nonzero producer exit, missing confidence fields, or checkpoint
  inconsistency;
- do not alter the microscope after seeing results. A failure remains sealed.

Passing means only that this exact instrument survived this exact source and
validation gate. It does not prove a transcription, establish linguistic or
historical truth, select a Tarot ontology or card equivalence, normalize
semantics, construct a Platonic card, attach UCNS geometry, activate EDCM
measurement, or select canon.

hmmm: whether the frozen French fast model and unrotated automatic segmentation
recover eighteenth-century typography within these source-faithful thresholds.
