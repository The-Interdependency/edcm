# Tarot PDF OCR microscope v3 — exhaustive tableau validation preregistration

Status: frozen before inspecting any additional tableau page or running OCR.

## Usage guidance

Read the complete v1 protocol, v1/v2 findings, and v2 delta first. V3 inherits
the exact v2 renderer, OCR engine/model, book validation crops, transcription
rules, comparison normalization, thresholds, serialization, resources,
stopping rules, provenance, and nonclaims. Apply only the tableau validation
replacement below. No v2 OCR exists to reuse or inspect.

## Frozen predecessors

- v1 complete protocol commit:
  `d46f4ad849694b738b5211f9bcc3dadb49c2c9c1`;
- v2 protocol commit: `45025ca4e8ad3ac36bf103ca2596509cb661256c`;
- merged EDCM parent: `ae25f7b48e6272ef385f933278494c6a18469dc1`;
- current skill-lib identity:
  `b4234ca29529f56526541df8deb58c2c19570792`.

V2 was `BLOCKED` because its two frozen tableau crops contained fewer than 100
decidable reference characters. Those samples may not be replaced with chosen
text-bearing regions. V3 removes region selection by admitting every complete
tableau page to the independent reference.

## Sole frozen validation change

The book control remains the exact eight v2 crops on pages `0025`, `0075`,
`0125`, `0175`, `0225`, `0275`, `0325`, and `0375`.

Replace the tableau pages/crops with all six complete rendered pages `0001`
through `0006`, in source order. The independent pre-OCR transcription records
every decidable textual character on each page in top-to-bottom, left-to-right
order. It includes letters, digits, accents, punctuation, and printed symbols
that have a Unicode character. It excludes pictorial content rather than
describing or interpreting it. Illegible text uses the inherited U+FFFD rule.

The exhaustive reference is sealed before Tesseract runs. If the complete
six-page source still has fewer than 100 decidable textual characters, v3 is
`BLOCKED` and OCR does not run. No page or region may then be substituted.

All inherited accuracy thresholds remain unchanged. For tableau validation,
OCR TSV tokens across each full page are compared with that page's full literal
reference; no crop filtering applies. `SURVIVED` still requires two complete
byte-identical 407-page runs after both sources pass their independent controls.

## Frozen escalation rule

- at least 100 exhaustive tableau reference characters → seal both references,
  execute the exact complete OCR protocol twice, and apply the inherited gate;
- fewer than 100 → `BLOCKED`; stop because this source cannot support the
  frozen text-accuracy inference without introducing a different modality;
- OCR accuracy/determinism threshold failure → `FALSIFIED`;
- every threshold and replay passes → `SURVIVED` and seal the transcription
  corpus for relational discovery.

Passing remains instrument adequacy for this tested scope only. It establishes
no Tarot ontology, card equivalence, semantic normalization, UCNS geometry,
EDCM interpretation, Platonic-card construction, historical truth, or canon.

hmmm: whether exhaustive, selection-free tableau transcription supplies enough
text to validate an OCR instrument at all.
