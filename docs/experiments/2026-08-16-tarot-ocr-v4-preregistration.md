# Tarot PDF OCR microscope v4 — empty-page rule preregistration

Status: frozen before reference sealing or OCR.

## Usage guidance

Read v1's complete protocol and the v2/v3 deltas first. V4 inherits every
identity, command, validation source/page, transcription rule, nonempty-page
threshold, serialization, resource bound, stopping rule, provenance boundary,
and nonclaim. Apply only the zero-reference rule below.

## Frozen predecessor

V3 protocol commit `b010bb903d5320f76c6de0630f8859ae91098170`
exhaustively admits all six tableau pages. V3 was `BLOCKED` at commit
`4b56f2c262b51ec597d19882cf6f943224898868` because pages `0004` and
`0005` have empty textual references and division by zero left their page CER
undefined. Tesseract has not run.

## Sole frozen change

After inherited comparison normalization:

- empty reference and empty candidate: page `exact_empty = true`; pass the
  page; omit it from CER/WER aggregate numerators and denominators;
- empty reference and nonempty candidate: page `exact_empty = false`; classify
  the complete instrument `FALSIFIED` regardless of other scores;
- nonempty reference: apply inherited CER/WER rules and thresholds unchanged.

The reference is empty only when exhaustive manual transcription found no
decidable textual characters on the complete page. Pictorial content is not
described, interpreted, or converted to text.

## Frozen escalation rule

Seal the independent book and exhaustive tableau references before OCR. Then
run the exact 407-page protocol twice. Any nonempty OCR on an empty-reference
page, accuracy failure, or replay mismatch is `FALSIFIED`; producer/identity,
reference, parse, or resource failure is `BLOCKED`; one passing run is
`UNRESOLVED`; two byte-identical passing runs are `SURVIVED`.

hmmm: whether the exact instrument passes the now-total validation rule.
