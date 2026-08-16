# Recovered dissonance controlled contrast v0.1.0

Date: 2026-08-16
Status: frozen preregistration; controlled outcomes and external outcome labels not inspected

## Decision

Determine whether absolute recovery of the maintained EDCM dissonance state is
sufficient to distinguish resolution from non-resolution, or whether recovery
must be normalized by pressure accumulated along the trajectory.

This is a minimal falsification experiment. It does not revise the maintained
EDCM baseline, establish measurement validity, select canon, or authorize
production use.

## Frozen identities and provenance

| Participant | Exact identity | Authority and relation |
|---|---|---|
| EDCM | parent commit `29cc5997c2c8cf7b7a145a9d4d59659054ffba41` | owns the candidate, controlled contrasts, and result |
| UCNS external evaluation harness | `The-Interdependency/ucns@1234950` (PR #196) | transport and reconciliation contract only; used only after a candidate survives the controlled gate |
| skill-lib | `The-Interdependency/skill-lib@6ef2e4c123225f9db20e5230e5894c9c86b42ee6` | action-sizing and evidence doctrine inspected before freeze; no dependency update is implied |
| Prior MultiWOZ result | EDCM report schema `edcm.multiwoz21-booking-outcome-holdout/0.1.0`, report digest `a726434a533395e7e3bd7d72ba3e9ce68f58c5b62f3b6b10d2b0556b09e85e61` | preserved historical evidence: sensitivity-at-least-0.50 is **FALSIFIED** |

The contrast trajectories below are hand-authored controls. Their construction
labels are not external outcome labels. No sealed outcome row, per-event score,
or outcome payload may be inspected while implementing or running this gate.

## Candidate A: absolute recovered dissonance

For an ordered finite trajectory `kappa = (kappa_0, ..., kappa_T)`, with
`T >= 2` and every value finite and nonnegative:

```text
A(kappa) = max(kappa_t) - kappa_T
```

Higher is predicted to indicate more recovery. No coefficient is fitted.

## Controlled contrast corpus

The cases are deliberately minimal and noiseless:

| Pair | Construction label | κ trajectory | Frozen role |
|---|---|---|---|
| low-pressure | resolved | `[0, 1, 0]` | complete recovery |
| low-pressure | unresolved | `[0, 1, 1]` | no recovery |
| high-pressure | resolved | `[0, 10, 0]` | complete recovery |
| high-pressure | unresolved | `[0, 10, 8]` | small recovery relative to injected pressure |

Within each pair, the initial state, prefix, peak, length, and sampling are
identical; only the final recovery differs. Pressure magnitude differs only
between pairs. This is the cheapest scale-confound test: a score can order both
matched pairs correctly yet still fail to supply one pressure-independent
separation rule.

## Frozen calibration and threshold rule

There is no statistical fit and no label-driven threshold search. Candidate A
separates the controls exactly when both conditions hold:

1. every resolved member scores strictly above its matched unresolved member;
2. `min(score_resolved) > max(score_unresolved)`.

If they hold, the frozen control threshold is the exact midpoint between those
two extrema. Equality is failure, not a tie to tune around. The controlled
corpus is exhaustive for this gate, so no sampling uncertainty or significance
test is claimed.

## Frozen minimum escalation

Candidate B may be evaluated only if Candidate A is `FALSIFIED` solely because
the global strict-gap condition fails after both matched directions pass.
Candidate B adds exactly one temporal quantity:

```text
I(kappa) = sum(t=1..T, max(kappa_t - kappa_(t-1), 0))
N(kappa) = A(kappa) / I(kappa)
```

`I` is accumulated positive dissonance pressure. `N` is dimensionless recovery
per accumulated positive pressure. It uses the same direction, controls,
strict-gap rule, and midpoint rule as Candidate A. If `I == 0`, Candidate B is
`UNRESOLVED`; no zero substitution, epsilon, smoothing, alternative integral,
or feature is permitted. No further candidate may be introduced in this
experiment.

## Frozen falsifiers

- reject non-sequences, fewer than three states, booleans, non-finite values,
  or negative κ values;
- the score must be deterministic and invariant under finite positive scaling
  of the entire κ trajectory;
- zero recovery must score zero;
- each resolved case must strictly exceed its matched unresolved control;
- one strict global threshold must separate all resolved from all unresolved
  controls;
- Candidate B must remain in `[0, 1]` for every admitted control;
- a byte-identical repeat must be obtained before a result is committed;
- the prior MultiWOZ sensitivity result must remain recorded as `FALSIFIED`;
- `canon_selection` must remain `null`, and transport success must not be
  reported as measurement validity.

Candidate A is not required to be scale invariant in raw magnitude; failure of
the global separation under the frozen scale contrast is its intended decisive
falsifier. Candidate B is required to be scale invariant.

## Outcome and stopping rules

- **SURVIVED:** all admission and falsifier checks pass and the candidate has a
  strict global control gap. Stop controlled development. Freeze its formula
  and threshold for external evaluation through PR #196's harness.
- **FALSIFIED:** an admitted candidate violates a frozen direction, separation,
  range, invariance, or repeat rule. If and only if Candidate A fails under the
  escalation condition above, evaluate Candidate B; otherwise stop.
- **UNRESOLVED:** arithmetic is undefined under the frozen formula or evidence
  is insufficient to assign survived/falsified without changing the design.
  Stop without repair or substitution.
- **BLOCKED:** identity, provenance, clean execution, or required harness
  prerequisites cannot be established. Stop without inspecting sealed labels.

After Candidate B, every outcome stops this experiment. Feature search,
alternative normalizers, threshold tuning, and sealed-label inspection are out
of scope. External evaluation is a separate execution and may begin only from
a committed frozen candidate that is `SURVIVED` here.

## External evaluation boundary

PR #196's harness is the only admitted next transport surface. It must consume
a committed evaluator executable and execution-generated full-corpus receipt
under its own disclosure, custody, digest, resource, and reconciliation rules.
Passing that harness proves bounded transport and reconciliation only. It does
not establish construct validity, empirical validity, theorem status, UCNS or
EDCM canon, or activation.

## hmmm

The controlled gate can decide whether absolute recovery is scale-sufficient
for these adversarial trajectories. It cannot decide whether accumulated
positive κ increments are the correct real-world pressure semantics. External
outcome-label authority, independent custody, temporal sampling comparability,
and measurement validity remain unresolved.
