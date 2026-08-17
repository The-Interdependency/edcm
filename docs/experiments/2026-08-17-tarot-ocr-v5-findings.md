# Tarot PDF OCR microscope v5 — findings

Status: `FALSIFIED` after one complete 407-page run. Replay was not run because
accuracy failure is terminal under the frozen protocol.

## Usage guidance

Use this result to reject only the exact fixed-default Sauvola v5 instrument.
The raw run is retained at `artifacts/tarot/ocr-v5/run-a`; verify its files
against the committed receipt. Do not treat improved detection as trustworthy
transcription, tune Sauvola parameters, or select a new model from these labels.

## Exact result

The sole v4-to-v5 change recovered text on 392 of 401 book pages, compared
with four nonempty book pages under v4. Across the complete book it detected
65,031 word tokens. This establishes that adaptive thresholding addressed most
of v4's detection failure, but it did not satisfy source-faithful accuracy.

Frozen validation result:

- aggregate CER: `0.2627226463104326` (maximum `0.08`);
- aggregate WER: `0.5543071161048689` (maximum `0.20`);
- book CER/WER: `0.22585096596136153` / `0.4625322997416021`;
- tableau CER/WER: `0.34536082474226804` / `0.7959183673469388`;
- seven of eight book samples produced CER from `0.07011070110701106` to
  `0.12601626016260162`, but page `0375` remained almost entirely undetected
  at CER `0.9968847352024922`;
- tableau page `0005` produced 15 characters against an exact-empty reference,
  which independently falsifies the instrument;
- several tableau pages produced large false-positive token sets, while page
  `0006` remained undetected.

The result distinguishes two failure layers. Fixed adaptive thresholding is a
large detection improvement for most book pages. It is not a sufficient
source-wide transcription instrument: recognition errors remain above the
frozen word threshold, one book page remains a detection failure, and the
predominantly visual tableau receives both false-positive and false-negative
text.

## Evidence boundary

- OCR v5: `FALSIFIED`;
- deterministic replay: not run because it cannot repair accuracy;
- trustworthy transcription corpus: not produced;
- source rejection: false;
- v4 remains separately `FALSIFIED` rather than overwritten;
- ontology, card equivalence, semantic normalization, UCNS geometry, EDCM
  interpretation, Platonic-card construction, historical truth, and canon
  remain absent.

hmmm: a further source-wide instrument would need independently justified
historical recognition and a lawful treatment of predominantly visual pages.
V5 supplies no authority to tune adaptive-threshold parameters or choose among
models by validation score.
