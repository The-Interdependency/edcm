# EDCM upgrade avenues

Decision basis: the 2026-09-17 audit and the versioned 0.2.0 repair. These are
proposed work packets, not delivered capabilities or validated claims.

Start with explainable source attribution. Then test one narrowly defined
measurement candidate against independent labels before expanding integration.

| Priority | Avenue | Concrete next deliverable | Advancement gate |
|---|---|---|---|
| 1 | Evidence spans and parser accounting | For each readout expose contributing source spans, rule IDs, denominator, round membership and retained-but-unmatched text. Bind offsets to exact source identity. | Every attributed span slices the original source correctly across Unicode, CRLF, mixed labels and continuations; coverage gaps stay visible. No silent source loss. |
| 2 | Independent validity study | Freeze one operational target, annotation/adjudication protocol, trivial and task-specific baselines, dialogue-level partitions, metric, uncertainty interval and falsifier before inspecting new outcomes. | Beat preregistered baselines on independently held-out evidence with the declared effect margin; report subgroup failures and uncertainty. Do not tune on the sealed booking test set. |
| 3 | Scope and order candidate | Build a separate versioned readout that tests negation, quotation, speaker attribution, repetition and order against minimal pairs. Declare what source information the projection loses. | Correct directional separation on frozen, unseen counterexamples; failure of a pair blocks the associated scope claim. Preserve v1/v2 evidence under their original IDs. |
| 4 | Recovery dynamics stress test | Extend normalized recovered-dissonance experiments with stalled, oscillating, regressing, adversarial and differently sized trajectories. Freeze sampling and aggregation first. | Separate improvement from length, repetition and reset artifacts; survive unseen trajectories with specified falsifiers. Four controlled successes do not establish real-dialogue validity. |
| 5 | Exact construction receipt consumer | In EDCM, consume one existing pinned Stack construction receipt using UCNS objects/constructors/geometry and a declared evaluation projection. Keep producer absence typed. | Reconcile source, object identity, order, multiplicity, closure and hashes against the producer. No reconstructed geometry or proof-to-measurement transfer. Construction belongs upstream. |

Priority 1 is bounded engineering. Priorities 2–4 require research design and new
evidence; their cost depends on label authority and custody. Priority 5 depends
on a concrete producer contract, not merely repository availability. It should
follow a useful evaluation question rather than precede one.

## Evidence limiting promotion

The sealed [booking-outcome findings](experiments/2026-08-02-multiwoz-booking-outcome-holdout-findings.md)
report 661 test events, balanced accuracy 0.521165 with 95% interval
[0.465606, 0.573938], and sensitivity 0.4698, below the declared 0.50 floor.
That bounded candidate's sensitivity hypothesis is falsified. This is neither
validation of the maintained axes nor a universal disproof of every EDCM model.
The repair creates a new measurement candidate, not a new validity result.

The audited multiline refusal is now retained, but “I cannot do this.” still
has no hit on the frozen refusal axis. The historical scope experiment also
exposes zero constraint signals on its tested distinctions. These motivate
explicit span explanations and a new scope candidate, not an undocumented
change to frozen markers.

Normalized recovered dissonance survived four controlled trajectories in its
recorded scope. Replicate the sealed evidence from its own pinned source before
extending it; controlled success alone cannot establish generalization.

## External methodological support

Using a predictor that ignores input features gives a transparent trivial
baseline; this is the explicit purpose of scikit-learn's
[DummyClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html).
If a future readout claims probability, fit and assess its calibration on data
separate from estimator training, following the independence boundary described
in the [calibration documentation](https://scikit-learn.org/stable/modules/calibration.html).
These recommendations do not require adding scikit-learn to EDCM's runtime.

Define the target construct and its operationalization before interpreting a
score as the construct itself. [Jacobs and Wallach, Measurement and Fairness](https://arxiv.org/abs/1912.05511)
provides measurement-model context for that distinction. Applying it here is a
research recommendation, not evidence that an EDCM axis is valid.

## hmmm

Which single outcome matters most to the intended consumer; who owns independent
labels and sealed-test custody; the minimum worthwhile effect; the relevant
language/domain coverage; and the exact next receipt producer remain open.
