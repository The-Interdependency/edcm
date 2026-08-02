# MultiWOZ 2.1 booking-outcome holdout v0.1.0

Date: 2026-08-02
Status: frozen EDCM-only externally labelled holdout design; no canon selection

## Question

> Before a source-annotated booking response is revealed, does the maintained
> EDCM terminal progress readout distinguish `Booking-Book` from
> `Booking-NoBook` on the sealed MultiWOZ 2.1 test partition after all
> calibration and operating-threshold choices are frozen on development and
> validation evidence?

This is an outcome-event experiment, not a universal dialogue-success test.
The positive source label is `Booking-Book`; the negative source label is
`Booking-NoBook`. Both labels come from the Cambridge-distributed
`dialogue_acts.json`, not from this experiment's implementer.

## Frozen identities

| Participant | Exact identity | Authority and relation |
|---|---|---|
| MultiWOZ 2.1 | archive SHA-256 `d377a176f5ec82dc9f6a97e4653d4eddc6cad917704c1aaaa5a8ee3e79f63a8e` | source text, dialogue acts, and development/validation/test membership |
| UCNS | `The-Interdependency/ucns@a98c9e6c69804a8a08d0786b1d8b450bb2c49a97` | exact word-gonol observation/provenance only |
| EDCM represented-evidence seal | report file SHA-256 `e228b9cb74c60ec4d6efb66f1d86c38069f613a875fa4c91f2973b46d20436f6`; receipt file SHA-256 `8d20f99f3f788e09e9edad40f7d28a2b97de9d634868652bd058e50d504fe9c9` | proves the admitted archive's 143,048 turns were reconciled through the pinned UCNS profile before this measurement experiment |
| EDCM | producer commit and `edcm/` Git tree recorded by the sealed run | owns the maintained baseline calculation, calibration, aggregate report, and completion receipt |
| skill-lib | `The-Interdependency/skill-lib@2b24be24947223b86440f59f1bd9766130f9cc11` | build, metadata, contract, and evidence discipline |

The runner emits a deterministic work-graph identity over these participants
and explicit no-transfer boundaries. A digest detects drift; it is not a
producer signature.

## Source event and leakage boundary

For dialogue-act turn id `k`, MultiWOZ maps the annotated system response to
zero-based `data.json` log index `2k - 1`. An admitted outcome event must meet
all of these conditions:

1. its dialogue-act mapping contains exactly one of `Booking-Book` and
   `Booking-NoBook`;
2. `k` is a positive decimal integer and `2k - 1` names an in-range system
   response;
3. every preceding log entry has a string `text` value and follows the
   admitted even-user/odd-system convention.

The predictor receives exact preceding turns `0..2k-2`. It never receives the
labelled system response at `2k-1`, any later turn, the dialogue-act payload,
goal, turn metadata, ontology, or databases. Exact source text stays outside
Git. The report retains only counts and SHA-256 chains over source locators and
exact UTF-8 turn identities.

The maintained parser requires one physical line per speaker-labelled turn.
For candidate measurement only, CR and LF inside a source turn are mapped to
SPACE and the text is wrapped as `USER: ...` or `SYSTEM: ...`. This declared
presentation transform does not alter the exact-source provenance chain or the
prior UCNS observation seal.

An event containing both outcome labels is excluded as
`ambiguous-source-outcome`; missing or malformed source structure fails the
run closed. Exclusion is source-structural, never based on a candidate score.

## Partitions and freeze order

The Cambridge membership lists define the partitions. The runner processes
them in this order:

1. `development` (source `train`): fit calibration only;
2. `validation`: select one operating threshold only;
3. `test`: evaluate once with the frozen calibration and threshold.

The expected admitted inventory before test evaluation is:

| Partition | `Booking-Book` | `Booking-NoBook` | unambiguous events |
|---|---:|---:|---:|
| development | 4,164 | 1,050 | 5,214 |
| validation | 543 | 113 | 656 |
| test | 530 | 131 | 661 |

Nineteen development annotations containing both labels are retained as an
aggregate exclusion count. No such ambiguity occurs in validation or test.
These counts are part of the frozen source contract and must reconcile before
a complete receipt can be emitted.

## Candidate and calibration

The only raw candidate score is the maintained baseline terminal progress
proxy from `edcm.measurement.metrics.compute`:

```text
s = P_terminal
P = clamp(0.6 * novelty(current_round, prior_round)
          + 0.4 * relative_entropy_gain)
```

The experiment does not add a new semantic axis. The source outcome labels
are targets only; they do not become EDCM input.

Development scores fit a two-parameter Platt map:

```text
z = (s - development_mean) / development_population_stddev
p(book | s) = sigmoid(intercept + slope * z)
```

The fit uses deterministic Newton updates, a declared slope ridge of `1e-6`,
at most 100 iterations, and a `1e-12` convergence tolerance. A zero score
standard deviation fails closed.

Validation selects a probability threshold from the finite set consisting of
`0`, `1`, every observed validation probability, and adjacent-probability
midpoints. The objective is maximum balanced accuracy. Ties resolve by:

1. smallest absolute distance from `0.5`;
2. lowest numeric threshold.

Calibration coefficients, development moments, the candidate threshold set,
selected threshold, validation confusion counts, and a calibration-policy
digest freeze before test rows are evaluated.

## Metrics and uncertainty

The sealed test report must include integer `true_positive`, `false_positive`,
`false_negative`, and `true_negative` counts plus:

```text
sensitivity = TP / (TP + FN)
specificity = TN / (TN + FP)
balanced_accuracy = (sensitivity + specificity) / 2
brier_score = mean((p - y)^2)
ECE_10 = sum_bin(n_bin / n * abs(mean_probability_bin - outcome_rate_bin))
```

Sensitivity and specificity carry two-sided 95% Wilson score intervals.
Balanced accuracy, Brier score, and `ECE_10` carry deterministic percentile
intervals from 2,000 dialogue-cluster bootstrap replicates using seed
`20260802`. Whole dialogue clusters, not individual outcome events, are
resampled so repeated booking attempts do not masquerade as independent
events.

## Frozen hypotheses

The report evaluates, but build success does not assume, these relations:

1. test sensitivity is at least `0.50`;
2. test specificity is at least `0.50`;
3. test balanced accuracy is strictly greater than `0.50`;
4. test `ECE_10` is at most `0.10`;
5. all expected partition, class, exclusion, and leakage-boundary counts
   reconcile;
6. a byte-identical repeat produces the same aggregate report.

Supported and falsified relations both remain evidence. A hypothesis failure
does not change the command's exit status; admission, identity, schema,
leakage, freeze-order, or reconciliation failures do.

## Output schema and privacy

The aggregate report schema is
`edcm.multiwoz21-booking-outcome-holdout/0.1.0`. The completion receipt binds
the report digest, archive and member identities, source-event chain,
candidate-input chain, frozen calibration digest, EDCM producer commit/tree,
UCNS represented-evidence seal, and work-graph digest.

Neither artifact may contain dialogue ids, raw turns, normalized turns,
dialogue-act slot values, per-event scores, or per-event labels. Raw corpus
bytes and any temporary checkpoints remain outside Git.

## Usage after implementation

Run from a clean producer commit so the emitted tree identity is recoverable:

```bash
python -m edcm.corpora.multiwoz21_booking_holdout \
  --archive /path/to/MULTIWOZ2.1.zip \
  --edcm-repository-root /path/to/edcm \
  --edcm-commit "$(git rev-parse HEAD)" \
  --output /tmp/multiwoz-booking-holdout.json \
  --receipt /tmp/multiwoz-booking-holdout-complete.json
```

Run the same command a second time to separate paths and compare exact bytes.

## Non-claims and state boundaries

- `canon_selection = null`;
- `candidate_measurement_status = candidate-measured-evidence`;
- formal UCNS geometry and higher-gonol composition are `NA`, not zero;
- UCNS supplies exact occurrence observation/provenance only and does not
  supply, validate, or select the EDCM score;
- EDCM and METAPAT production activation remain inactive;
- theorem, proof, certification, measurement-validity, semantic-authority,
  and empirical-status transfer are all false;
- `Booking-Book` and `Booking-NoBook` are bounded source action annotations,
  not universal task success, user satisfaction, truth, intention, diagnosis,
  morality, or consciousness;
- no retired pre-reset `UCNSObject`, `recursive_encode`, or `stable_hash` path
  participates.

## hmmm

The public MultiWOZ test membership is sealed by source identity and untouched
by the calibration code path, but it is not independently hidden or held by an
external custodian. Dialogue-act annotations are external to the EDCM
implementer but are not independent human adjudications of end-user success.
The maintained progress proxy is lexical/statistical and may be unable to
distinguish booking outcomes; that failure is a permitted result. Formal
word-to-turn-to-dialogue UCNS geometry, lawful higher-gonol composition,
independent replication, signed producer authentication, multilingual
replication, and a first joint canon authority packet remain unresolved.
