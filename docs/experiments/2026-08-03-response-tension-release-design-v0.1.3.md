# EDCM response-tension-release experiment

## Frozen next-experiment packet v0.1.3

| Field | Frozen value |
|---|---|
| Date frozen | `2026-08-03` |
| Design status | **FROZEN** |
| Execution status | **BLOCKED pending signed custody and human-label manifests** |
| Schema | `edcm.response-tension-release-experiment/0.1.3` |
| Candidate | `edcm.response-tension-release/0.1.0` |
| Canon selection | `null` |
| Supersedes | Immutable v0.1.2 packet SHA-256 `78fc589eb8729aaccd553fded35c599606f651bf76b75961dd40cb28bf7e9ed1` |
| Current-packet index | `docs/experiments/README.md` |

This complete v0.1.3 packet freezes the same single new experiment design and
supersedes v0.1.2 only to bind label-manual independence, binary-label
reliability, exact parser framing, and a current-packet index. It does not modify
any immutable earlier packet, authorize execution, alter EDCM equations, reopen
prior evidence, activate production, or select a canonical measurement. No
earlier packet was executed; no candidate input, human label, partition
membership, per-event score, or sealed outcome was viewed between packet
versions.

This v0.1.3 packet is immutable. Named people, keys, encrypted-bundle digests,
and run-time identities must be supplied in separately signed execution and
completion manifests that bind this packet's file digest. Changing any rule in
this packet requires a new packet version and a fresh sealed test.

## 1. Controlling predecessor boundary

The predecessor is [EDCM PR #49](https://github.com/The-Interdependency/edcm/pull/49),
`experiment: seal externally labelled MultiWOZ booking holdout`.

| Identity | Frozen value |
|---|---|
| PR base | `main@28632bd7ca5dc9397793bd66b73f0970dc51e650` |
| PR head after evidence-binding review repair | `969775ee2cbc2b286fbde55ba436f27986f72e7b` |
| PR head tree | `2f71a472fa3aa9dfd960542973da29ffdb1a3e36` |
| Actions synthetic merge | `a2ff97607a80f8783ae61a81586d48ea207274d4` |
| Sealed EDCM producer | `c292430771b4dc76734522b580caa2be18ca04f9` |
| Sealed EDCM tree | `04beb8d9c6f01f2ec00bb06e55f77bea21e9b14a` |
| UCNS producer | `a98c9e6c69804a8a08d0786b1d8b450bb2c49a97` |
| MultiWOZ 2.1 archive SHA-256 | `d377a176f5ec82dc9f6a97e4653d4eddc6cad917704c1aaaa5a8ee3e79f63a8e` |
| Sealed report digest | `a726434a533395e7e3bd7d72ba3e9ce68f58c5b62f3b6b10d2b0556b09e85e61` |
| Report file SHA-256 | `4c7254cc2a2244eaf0e30e182153f803c9e2706774e9a743f7c22899bdcd64a3` |
| Receipt file SHA-256 | `ea2db8bf06785b54ab67dfa01a236bbec2e1d8ec79a5f9808c949363cff4ffe5` |

The predecessor's controlling empirical result is:

- sensitivity `0.469811320754717`, 95% Wilson interval
  `[0.42769111208421506, 0.51236599762268]`; the preregistered sensitivity
  hypothesis was falsified;
- balanced accuracy `0.5211652023620913`, 95% dialogue-cluster interval
  `[0.4656057510819316, 0.5739376739379676]`; the interval spans chance;
- Platt slope `0.019040813646053385`; the old terminal-progress score added
  little movement beyond class prevalence;
- low ten-bin expected calibration error did not repair weak discrimination.

The old candidate, `edcm.maintained-terminal-progress/0.1.0`, used only terminal
progress before the labelled response. Its 661 test events, membership,
per-event labels, per-event scores, errors, and fitted choices are forbidden
inputs to this experiment. The old aggregate result above is a boundary, not
training data.

## 2. Successful-check audit

All three GitHub Actions workflows associated with the PR head completed
successfully, comprising twelve successful jobs:

| Workflow | Verified surface | Material limit |
|---|---|---|
| [UCNS–EDCM joint experiments](https://github.com/The-Interdependency/edcm/actions/runs/30788628801) | Python 3.11/3.12 historical experiment tests and byte-identical v0.1–v0.4 reruns | Historical joint reports; not a raw-corpus rerun of the new holdout |
| [Skill and metadata compliance](https://github.com/The-Interdependency/edcm/actions/runs/30788628787) | Seven pinned skill-lib consumers clean; canonical metadata regeneration matched | Contract and drift evidence only |
| [CI](https://github.com/The-Interdependency/edcm/actions/runs/30788628782) | 240 tests passed with 20 producer-dependent skips on Python 3.11–3.13; integrity, authority boundaries, packaging, Twine, and clean-wheel smoke passed | Raw MultiWOZ bytes and event labels were absent; the sealed evaluation was not independently regenerated |

The checks establish that the synthetic merge is buildable and that committed
hashes, leakage guards, aggregate schemas, status boundaries, and deterministic
machinery are internally consistent. They do not establish hidden external
custody, implementer blindness, independent human outcome validity, raw-corpus
ground truth, useful discrimination, generalization, production readiness, or
measurement validity. Green checks therefore preserve rather than supersede
the falsified sensitivity result and chance-spanning interval.

The final repaired PR head fails closed when the loaded EDCM runtime does not
match the recorded checkout, loads one authenticated in-memory canon for all
events, and re-verifies the runtime after canon load and after scoring. It
leaves a single-run byte-repeat finding `not-evaluated`; rejects colliding
report, receipt, and atomic-temporary paths; and rejects any such artifact path
that aliases the admitted source archive. Those repairs govern future
predecessor schema v0.1.1 output. They do not change the sealed v0.1.0 report or
receipt bytes, their metrics, or the controlling negative interpretation.

The historical v0.1.0 producer serialized its repeat finding as `supported`
before a second complete output existed; that producer status was premature.
Two complete commands were later compared externally and their report and
receipt files were byte-identical. This distinction and both historical file
hashes remain visible rather than being rewritten.

## 3. New question

> When the target system response itself is measured, does its one-turn effect
> on maintained EDCM stored tension distinguish independently human-adjudicated
> resolution from non-resolution of one explicit booking request on a fresh,
> externally held test partition?

This is a bounded response-measurement experiment. It is not a forecast of an
unseen response and not a claim about universal dialogue success, satisfaction,
truth, intention, diagnosis, morality, consciousness, or competence.

## 4. Exactly one new candidate

### 4.1 Candidate identity

`edcm.response-tension-release/0.1.0`

The candidate is genuinely distinct from the predecessor:

- the predecessor scored terminal novelty and relative entropy gain before the
  response;
- this candidate includes the target response and measures its immediate
  directional effect on stored tension;
- it adds no learned feature weights, sign search, ensemble, ablation family,
  or alternative candidate;
- it is never executed on the predecessor's test events.

### 4.2 Input and structural policy

Candidate input contains exact speaker turns from the dialogue start through
the target system response. For each source turn, replace every CR and every LF
character with one ASCII SPACE. Prefix alternating turns with exactly `USER: `
and `SYSTEM: `, starting with `USER: `, join them with one LF, and add no
trailing LF.

Call maintained `parse_transcript` exactly once on that complete framed string
with `round_strategy="cycle"` and the frozen run's one authenticated
`CanonLoader`. The parser must return exactly the source turn count, alternating
`USER` / `SYSTEM` speakers, and normalized `Turn.text` values equal to the
source turns after the CR/LF transform; otherwise fail closed. Speaker prefixes
are framing and must not remain in `Turn.text` or its tokens. Ignore the
parser's cycle-grouped `rounds` for this candidate.

The following are candidate non-inputs:

- human outcome labels, rater notes, and rubric decisions;
- source dialogue-act labels and payloads;
- goals, turn metadata, ontology, and domain databases;
- the next user turn and every later turn;
- partition identity, test membership, and custody secrets.

For each parsed turn at zero-based position `i`, construct exactly
`Round(index=i, turns=[parsed.turns[i]])`. Apply the existing `compute_round`
equations unchanged to those one-turn rounds with `alpha = 0.85` and
`delta_max = 0.30`. This turnwise policy belongs only to this candidate; it does
not alter the maintained cycle-grouped baseline.

Process the constructed rounds chronologically with initial stored tension
`kappa_0 = 0` and initial previous entropy `0`. Each one-turn round becomes the
next call's `prev_round`; stored tension and previous entropy advance exactly
once per turn. Parsing turns separately, passing a one-line prefixed transcript
to the parser, using parser-produced cycle rounds, retaining prefixes as tokens,
or calling a different round strategy is forbidden.

### 4.3 Frozen score

Let `kappa_pre` be stored tension immediately after the user turn directly
preceding the target response. Let `kappa_post` be stored tension after one
additional circuit step on the target system response.

```text
release = kappa_pre - kappa_post
score   = (1 + release) / 2
```

Because both tension states must lie in `[0,1]`, `release` must lie in
`[-1,1]` and `score` in `[0,1]`. Higher score means greater response-induced
tension release. Missing turns, empty parsing, non-finite values, state values
outside their declared ranges, or a score outside `[0,1]` fail closed. No
post-hoc sign inversion is permitted.

There is no fitted development model. Validation selects one operating
threshold from `{0, 1, each distinct observed validation score, each midpoint
between adjacent distinct observed scores}` by maximum balanced accuracy. A
row predicts `resolved = 1` if and only if
`score >= selected_threshold`; otherwise it predicts `resolved = 0`.
This comparator governs every candidate threshold, the selected validation
confusion matrix, and the sealed test, including scores exactly equal to the
threshold. Ties resolve first by smallest distance from `0.5`, then by the
lower threshold. This is the only allowed data-dependent choice.

### 4.4 Score-inventory commitment

Every development, validation, and test score inventory uses one frozen digest
rule. Sort admitted rows by their lowercase 64-hex event digest; duplicate
event digests fail closed. For each row, encode
`event_digest + TAB + float.hex(score) + LF` as ASCII, where `score` is the
final finite IEEE-754 binary64 candidate score. Concatenate the rows without a
header and record the SHA-256. The digest may leave custody; the sealed test
rows, event digests, and scores may not.

## 5. Human outcome-label authority

The source dialogue action locates a candidate event but has no outcome-label
authority. Authority belongs to an independent human panel operating under a
signed, frozen manual.

For one active explicit booking request:

- `resolved = 1` when the target response correctly completes and confirms the
  requested action, or correctly establishes that it cannot be completed and
  supplies the minimum usable next choice required to continue;
- `resolved = 0` when the response falsely claims completion, omits an active
  constraint, refuses or offloads without a valid necessity, contradicts the
  authoritative record, or otherwise leaves the request unresolved;
- `not-adjudicable` when there are multiple inseparable active requests,
  insufficient authoritative evidence, malformed source structure, or
  irreducible ambiguity. These events are excluded and counted before
  allocation.

Raters may inspect the full context through the response, the source goal,
relevant turn metadata and database state, and the immediately following user
turn when available. These label-only materials never enter the candidate.

The label-manual author, training-example author, label authority, both raters,
and the adjudicator must be independent of the candidate author, every
candidate designer or implementer, and the external custodian. Before the
manual or examples are created, a signed role manifest freezes those exclusions
and permanently bars those people from candidate design or implementation for
this experiment. They must not compute, inspect, receive, or order any source
row by a candidate score. Training examples must be digest-excluded from the
source frame before eligibility is frozen.

Two raters label every event independently while blinded to candidate scores
and partition membership. If either rater assigns `not-adjudicable`, the event
is excluded and counted; the adjudicator may not promote it into the experiment.
The third adjudicator resolves only disagreements where both original ratings
are binary.

Before adjudication, two separate reliability gates must both pass. On the
complete paired three-category ledger, raw agreement must be at least `0.80`
and unweighted Cohen's kappa at least `0.70`. On the complete subset where both
raters assigned `resolved` or `unresolved`, binary raw agreement must also be at
least `0.80` and binary unweighted Cohen's kappa at least `0.70`. The binary
subset, its counts, and both statistics freeze before any binary disagreement
is adjudicated; an empty subset or undefined kappa fails. These calculations
occur before exclusion or allocation. Failure stops the experiment; the manual
may not be repaired after viewing agreement or candidate results. The signed
adjudicated ledger is controlling. Candidate code has no authority to change
it.

## 6. Source frame and partitions

The initial source frame is the exact MultiWOZ 2.1 archive identified above.
Every dialogue in the Cambridge `testListFile.json` used by PR #49 is excluded
entirely. The exclusion-list member SHA-256 is
`56fff5bf8c7b0a64fba8672241a7bdd947c3a58986bf06f46d37f33288f73ce0`.

Within the remaining source-train and source-validation dialogues, the
eligibility rule selects the earliest structurally valid system response whose
source act contains exactly one of `Booking-Book` and `Booking-NoBook`. That act
is a locator only. There is at most one event per dialogue. Exact candidate
input duplicates are deduplicated before allocation. No dialogue or candidate
input digest may cross partitions.

Before any outcome label is created, the custodian generates exactly one
secret 256-bit allocation seed and publishes a signed SHA-256 commitment over a
domain separator, this packet's digest, the frozen allocation-code digest, and
the seed. The same pre-label release binds the eligible and exclusion
inventories. The seed remains exclusively in custody.

After human adjudication, the custodian allocates within outcome-by-booking-
domain strata using HMAC-SHA-256 over each event digest and that exact committed
seed. Domain quotas use proportional largest remainder. The custodian then
commits the ordered outcome-stratified partition-manifest digests before any
development data are released. Trying, replacing, or selecting among seeds
after any label exists invalidates the experiment.

| Partition | Positive | Negative | Total | Permitted use |
|---|---:|---:|---:|---|
| Development | 150 | 150 | 300 | Extractor conformance and frozen go/no-go only; no formula or direction change |
| Validation | 100 | 100 | 200 | Select the single threshold and freeze its digest |
| External sealed test | 200 | 200 | 400 | Exactly one aggregate evaluation after all freezes |

If the exact inventories cannot be filled without changing eligibility or
reusing a dialogue, execution stops incomplete. Because allocation is
class-balanced, this experiment makes no prevalence, probability-calibration,
Brier-score, or expected-calibration-error claim.

## 7. Freeze and execution order

1. Freeze and digest this packet.
2. Name and sign the manual author, training-example author, label authority,
   raters, adjudicator, candidate-author and implementer, and external-custodian
   role manifests with the exclusions and score-blinding rules above.
3. Author and freeze the manual and digest-excluded training examples while
   score-blind; freeze source, eligibility, exclusion, and allocation-code
   identities; generate the one allocation seed and publish its signed
   commitment before any label is created.
4. Label, apply both pre-adjudication reliability gates, exclude every row with
   either `not-adjudicable` rating, and adjudicate remaining binary
   disagreements without candidate scores or partition identities.
5. Commit encrypted bundle, ledger, access-log, and ordered partition-manifest
   digests, all bound to the pre-label seed commitment.
6. Freeze candidate code, dependencies, container, synthetic conformance
   results, and implementation digest before development data are released.
7. Release development rows and labels; run only the frozen development gate.
8. Release validation rows and labels; select the single threshold and freeze
   its configuration and policy digest. Candidate code and container remain
   byte-identical.
9. Deliver that network-disabled immutable container plus the signed threshold
   configuration to the custodian.
10. Custodian evaluates the sealed test twice internally, confirms both the
    byte-identical aggregate bytes and ordered test score-inventory digest, and
    then releases one signed aggregate report and completion receipt. The
    underlying per-event scores remain sealed.

There are no interim test looks, per-event disclosures, adaptive accrual,
sample extension, relabelling, threshold retry, feature addition, sign change,
or second candidate.

## 8. Preregistered hypotheses and decision rule

### Development gate

The score must be finite for every admitted row, have non-zero variance, and
have development area under the receiver-operating-characteristic curve at
least `0.55` in the declared direction. Development AUC is the exact
Mann–Whitney probability over every positive-negative pair: a strictly greater
positive score contributes `1`, an equal score contributes `0.5`, and a lower
score contributes `0`, divided by the number of pairs. Failure is a preserved
development falsification and stops the experiment before validation.

Every signed completion, `stopped-before-test`, or incomplete manifest must
contain a development compartment. Once development runs, it records the
ordered score-inventory
digest, admitted-row count, finite-count audit, variance, AUC method, AUC
value, declared direction, gate thresholds, and gate verdict even when that
verdict stops the experiment. If execution stops before development, the same
fields are present with typed `not-run` values and the prior stop reason.

### Validation gate

At the selected threshold, validation balanced accuracy must be at least
`0.55`, sensitivity at least `0.50`, and specificity at least `0.50`. Failure
is a preserved validation falsification and stops the experiment before test.

### Sealed-test hypotheses

All three empirical hypotheses are co-primary and must pass:

1. **Discrimination:** the lower bound of the two-sided 95% balanced-accuracy
   interval is strictly greater than `0.50`.
2. **Sensitivity repair:** the lower bound of the two-sided 95% Wilson
   sensitivity interval is strictly greater than `0.50`.
3. **Specificity guardrail:** the lower bound of the two-sided 95% Wilson
   specificity interval is strictly greater than `0.50`.

Balanced accuracy uses a deterministic 10,000-replicate, outcome-stratified
dialogue bootstrap with seed `20260803`. Because eligibility admits at most one
event per dialogue, each test event is its dialogue cluster. Within each
outcome, the 200 clusters are ordered by event digest. One
`random.Random(20260803)` instance runs exactly 10,000 replicates; in each
replicate it draws 200 positive indices and then 200 negative indices with
replacement using `randrange(200)`. Balanced accuracy is computed on those 400
draws. The two-sided interval sorts all 10,000 estimates and applies linear
percentiles at `q = 0.025` and `q = 0.975`: `h = (n - 1) * q`, interpolating
between the values at `floor(h)` and `ceil(h)`. No alternative seed, draw order,
stratification, percentile rule, or invalid-replicate filtering is permitted.
Confusion counts, point estimates, all intervals, validation results, and the
threshold must be reported whether the hypotheses pass or fail. Threshold-free
area under the receiver-operating-characteristic curve is secondary and cannot
rescue a co-primary failure.

If the balanced-accuracy interval touches or spans chance, sensitivity fails,
or specificity fails, the candidate is not experiment-supported. The result
is preserved as falsified or weak evidence. Scientific failure must serialize
successfully and must not be converted into a build failure.

## 9. External test custody

The custodian must be a named person or organization with:

- no write role in the EDCM repository;
- no role in candidate design, implementation, human labelling, or
  adjudication;
- a recorded legal identity, conflict disclosure, public-key fingerprint, and
  signed acceptance of this packet;
- exclusive control, after the adjudicated-ledger handoff and allocation, of
  the sealed test manifest, test labels, per-event scores, secret allocation
  seed, and encrypted source bundle;
- an append-only access log whose digest is included in the receipt.

The human panel creates the full blinded ledger but never receives the
allocation seed or any partition manifest. After the signed ledger handoff,
the custodian alone maps rows into partitions. The candidate implementer
receives development and validation material only. The custodian receives the
immutable container by digest, runs it without
network access, and releases no output until the two internal renders are
byte-identical. Only aggregate counts, metrics, intervals, identities,
digests, status boundaries, and an `hmmm` field may leave custody. The signed
ordered test score-inventory digest leaves custody as provenance; its
underlying ordered scores do not.

An operational retry is allowed only when the identical container and inputs
failed for a documented infrastructure reason before any metric was released.
The custodian must sign the incident and zero-disclosure statement. A changed
container, configuration, threshold, label, test manifest, or sample is a new
experiment version, not a retry.

## 10. Stopping and failure conditions

### Administrative or integrity stop before test — incomplete

- custodian, label-authority, consent, licence, or source identity is missing;
- a role conflict, manual-author score exposure, or undisclosed test access
  exists;
- PR #49 test membership or any predecessor test event enters the frame;
- a dialogue or exact-input digest crosses partitions;
- the agreement thresholds fail;
- an inventory, digest, signature, schema, or provenance field fails to
  reconcile;
- the pre-label seed commitment is absent, late, replaced, or inconsistent;
- raw source, per-event label, score, locator, or test membership leaks;
- frozen candidate identity or synthetic conformance fails before development
  release;
- formula, direction, round policy, label manual, eligibility, partition size,
  threshold policy, metric, uncertainty method, dependency, or candidate code
  changes after its applicable freeze;
- test membership, labels, or aggregate results are disclosed before the
  authorized release.

### Preregistered gate stop — stopped-before-test

A completed development or validation gate that fails its frozen criterion is
a scientifically valid negative stop, not an invalid execution. It emits a
signed `stopped-before-test` receipt containing the controlling gate provenance
and falsification reason; no sealed-test verdict exists. Missing, non-finite,
or out-of-range development scores, zero variance, and sub-threshold
development AUC are development-gate failures under this rule.

### Test scientific failure

A completed custody run that fails any co-primary hypothesis is a valid
scientific falsification. It receives a complete receipt with
`candidate_measurement_status = candidate-measured-evidence` and
`experiment_supported = false`.

### Invalid test execution

Byte mismatch between the two internal runs or their ordered test
score-inventory digests, custody breach, digest drift, partition collision,
missing, non-finite, or out-of-range sealed-test scores, forbidden output, or
an unauthorized retry invalidates the execution. It receives an incomplete
receipt and no empirical verdict.

## 11. Required provenance fields

The signed execution and completion manifests must record at least:

| Compartment | Required fields |
|---|---|
| Packet | schema, version, design status, file SHA-256, freeze timestamp, superseded-packet SHA-256, no-data-between-versions attestation, predecessor identities |
| Candidate | candidate ID, exact framing bytes, single parser call and arguments, one-turn construction, formula, direction, `alpha`, `delta_max`, code commit/tree/blob identities |
| Runtime | lockfile, interpreter, operating system, architecture, skill-lib, container, entrypoint, and dependency digests |
| Source | owner, DOI/source URL, licence, consent/privacy decision, archive and member digests, language, domain, collection period |
| Eligibility | rule version, old-test exclusion digest, eligible/excluded counts and reasons, event and input digest chains, duplicate audit |
| Labels | manual/training-example author and authority role IDs, manual and digest-excluded training-example identities, candidate-score-blinding assertions, conflicts, complete three-category and both-binary agreement populations/counts/statistics, exclusion counts, adjudicator identity, pre- and post-adjudication ledger digests and signatures |
| Partitions | allocation-code digest, signed pre-label seed commitment and timestamp, strata and quotas, ordered encrypted manifests, counts, collision audit |
| Custody | custodian legal identity, conflict disclosure, key fingerprint, acceptance signature, signed ledger-handoff identity, encrypted bundle digest, access-log digest |
| Development | ordered score-inventory digest, admitted and finite counts, variance, exact Mann–Whitney AUC value/direction, gate thresholds and verdict, or typed `not-run` fields and prior stop reason; required in every completion, `stopped-before-test`, or incomplete manifest |
| Validation | score inventory digest, threshold candidate count, `score >= selected_threshold` comparator, selected threshold, confusion counts, gate verdict, freeze digest |
| Test | run nonce and timestamps, exact container/config digest, ordered test score-inventory digest, confusion counts, interval methods and seed, co-primary verdicts, aggregate-byte and score-inventory-repeat verdicts |
| Evidence | canonical report digest, report file SHA-256, receipt payload digest, receipt file SHA-256, custodian signature |
| Boundaries | canon selection, activation states, typed absences, every theorem/proof/certification/semantic/measurement/empirical transfer flag |

The deterministic aggregate report excludes run nonce, timestamps, access-log
content, signatures, and other render-varying custody fields; those belong only
in the signed receipt and completion manifest. The receipt binds the aggregate
report's digest and file SHA-256. Because a file cannot contain its own digest,
the receipt file SHA-256 is recorded in a separately signed completion envelope
or append-only custody registry after the receipt bytes freeze.

Every status serializes every compartment. A compartment that was not reached
contains typed `not-run` values and the controlling prior stop reason rather
than disappearing from the evidence chain.

Raw source text, dialogue identifiers, event locators, per-event labels,
per-event scores, rater identities beyond role-safe provenance, secret seed,
and test membership must remain outside Git and outside the aggregate report.

## 12. Smallest implementation plan

No implementation occurs under this packet-drafting task. A later authorized
implementation is limited to:

1. one new runner module implementing the turnwise response-tension-release
   score and custody-safe aggregate schema while reusing existing archive,
   EDCM metric, Wilson interval, linear-percentile, digest, and receipt
   primitives and adding only the frozen outcome-stratified sampler above;
2. one contract-test file covering four synthetic tension transitions, exact
   full-transcript framing and one-turn construction, response inclusion and
   label/future-turn exclusion, old-test exclusion, partition isolation,
   equality at the `>=` threshold, manual-author role/score blindness, both
   reliability gates, pre-label seed binding, complete development-gate
   provenance, sealed ordered score-inventory digests, aggregate-only output,
   fail-closed behavior, and two-run determinism;
3. one network-disabled container entrypoint for custodian execution;
4. after a valid run only, one immutable aggregate report and receipt plus the
   minimum documentation and generated metadata updates required by the
   repository gates.

The maintained metric equations, PR #49 report and receipt, historical
experiments, source archive, and old test partition are unchanged. A regression
must prove the predecessor report and receipt remain byte-identical.

## 13. Non-transfer boundary

Regardless of outcome:

```text
canon_selection = null
formal_ucns_geometry = NA
formal_higher_gonol_composition = NA
edcm_production_activation = inactive
metapat_production_activation = inactive
theorem_status_transfer = false
proof_status_transfer = false
certification_status_transfer = false
semantic_authority_transfer = false
measurement_validity_claim = false
measurement_status_transfer = false
empirical_status_transfer = false
```

Even complete support establishes only one bounded candidate measurement on
one English booking corpus under one human manual and one custody event.

## hmmm

No external custodian, signing key, human panel, conflict disclosures, or
signed execution manifest is presently instantiated. Execution is therefore
blocked without weakening the frozen design. MultiWOZ source bytes are public;
external custody can hide test membership, human labels, and per-event outputs,
not make the public corpus itself secret. Participant independence is not
recoverable from the released corpus, so one-event-per-dialogue is the strongest
available clustering boundary. Cross-domain, multilingual, prospective, and
real-world action validity remain unresolved. A green machine can preserve a
negative result perfectly; it cannot promote it by good manners.
