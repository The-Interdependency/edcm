# Recovered dissonance controlled contrast v0.1.0 findings

Date: 2026-08-16
Status: controlled candidate evidence; no external evaluation or canon selection

## Result

The absolute recovered-dissonance candidate is **FALSIFIED**. It ordered each
matched pair correctly, but did not admit one strict pressure-independent
threshold: the low-pressure resolved score was `1`, below the high-pressure
unresolved score `2`.

The preregistered sole escalation was therefore admitted. Normalized recovered
dissonance is:

```text
accumulated_positive_pressure = sum(max(kappa_t - kappa_(t-1), 0))
normalized_recovery = (max(kappa_t) - kappa_final)
                      / accumulated_positive_pressure
```

It **SURVIVED** the controlled gate. Both resolved controls scored `1`; the
unresolved controls scored `0` and `1/5`. The frozen strict gap exists, and its
control-only threshold is `3/5`.

## Receipt

```text
preregistration commit       0bc34fa
execution implementation    4702dd9
preregistration SHA-256      120417a45a4515d0ab0d56e3a4b4c7cf66edde53c445e56db1152ff39d2e05cd
aggregate report SHA-256     5003427062a29941bafb288dc82f4b633e3884d8a1db2748b37c137e0faaed32
repeat comparison            byte-identical
sealed labels inspected      false
external evaluation          not run
```

The historical MultiWOZ sensitivity-at-least-`0.50` hypothesis remains
**FALSIFIED**, bound to report digest
`a726434a533395e7e3bd7d72ba3e9ce68f58c5b62f3b6b10d2b0556b09e85e61`.

## Stopping boundary

The controlled experiment stops here. No feature search, alternative
normalizer, threshold tuning, or sealed-label inspection is rational or
admitted under the preregistration.

The normalized candidate may now be packaged as a committed evaluator for the
UCNS PR #196 external evaluation harness. A transport pass would establish only
bounded execution and reconciliation. This controlled survival does not
establish measurement validity, empirical validity, canon, or activation;
`canon_selection` remains `null`.

## hmmm

Normalization is necessary for this cheapest scale adversary, but the controls
do not establish that accumulated positive κ increments are the correct
real-world pressure semantics. Temporal sampling comparability, external label
authority and custody, independent replay, and construct validity remain open.
