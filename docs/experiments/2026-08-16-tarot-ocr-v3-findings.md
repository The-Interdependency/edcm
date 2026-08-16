# Tarot PDF OCR microscope v3 — findings

Status: `BLOCKED` before reference sealing or OCR.

## Usage guidance

Use this as the exhaustive-tableau prerequisite receipt. Do not infer OCR
accuracy or reject the source. A later protocol must define how an empty
reference page is scored before Tesseract runs.

## Result

All six complete tableau pages rendered under the frozen v2 producer with zero
stdout, zero stderr, and zero exit status. Inspection occurred only after the
v3 commit and found:

- page `0001`: more than 100 decidable textual characters;
- pages `0002` and `0003`: visual arrangements with limited printed text;
- pages `0004` and `0005`: no decidable textual characters;
- page `0006`: a predominantly blank/frame view with a small printed identifier.

The source therefore clears v3's aggregate 100-character prerequisite. But v3
inherits standard CER as Levenshtein distance divided by reference-character
count and does not define the zero-reference case for pages `0004` and `0005`.
That makes the page-level decision rule uninterpretable. The protocol is
`BLOCKED` before reference sealing and before any Tesseract invocation.

hmmm: preregister an exact empty-page rule—empty OCR output passes an empty
reference, any nonempty OCR output fails—without changing any other control.
