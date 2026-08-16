# Maintained terminal-progress outcome proxy deprecation

Date: 2026-08-16  
Candidate: `edcm.maintained-terminal-progress/0.1.0`  
Disposition: **DEPRECATED for outcome discrimination**

## Falsifier

The frozen MultiWOZ 2.1 booking-outcome holdout required test sensitivity of
at least `0.50`. The sealed result measured `0.469811320754717`. Its balanced
accuracy interval, `0.4656057510819316–0.5739376739379676`, includes chance.

Continuing to use this candidate for outcome discrimination, content
generation, balance decisions, or production activation is therefore
irrational under the frozen rule.

## Evidence preserved

- design: `docs/experiments/2026-08-02-multiwoz-booking-outcome-holdout-design.md`
- findings: `docs/experiments/2026-08-02-multiwoz-booking-outcome-holdout-findings.md`
- result SHA-256: `4c7254cc2a2244eaf0e30e182153f803c9e2706774e9a743f7c22899bdcd64a3`
- receipt SHA-256: `ea2db8bf06785b54ab67dfa01a236bbec2e1d8ec79a5f9808c949363cff4ffe5`

Those artifacts remain historical evidence. They are not edited, relabelled,
or reused as a replacement epoch.

## Replacement

None selected.

## hmmm

A successor needs a new candidate identity, frozen target, independent labels,
comparator, thresholds, and fresh evidence paths. Calibration cannot teach a
weak discriminator to distinguish.
