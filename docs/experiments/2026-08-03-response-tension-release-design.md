# EDCM response-tension-release experiment

## Frozen next-experiment packet v0.1.0

Date frozen: 2026-08-03  
Design status: **FROZEN**  
Execution status: **BLOCKED pending signed custody and human-label manifests**  
Schema: `edcm.response-tension-release-experiment/0.1.0`  
Candidate: `edcm.response-tension-release/0.1.0`  
Canon selection: `null`

This packet freezes one new experiment design. It does not authorize execution,
modify EDCM equations, reopen prior evidence, activate production, or select a
canonical measurement.

The packet itself is immutable. Named people, keys, encrypted-bundle digests,
and run-time identities must be supplied in separately signed execution and
completion manifests that bind this packet's file digest. Changing any rule in
this packet requires a new packet version and a fresh sealed test.

## 1. Controlling predecessor boundary

The predecessor is [EDCM PR #49](https://github.com/The-Interdependency/edcm/pull/49),
`experiment: seal externally labelled MultiWOZ booking holdout`.

| Identity | Frozen value |
|---|---|
| PR base | `main@28632bd7ca5dc9397793bd66b73f0970dc51e650` |
| PR head | `3dd95962f7b21d70e7a4394d13428c650dc3783f` |
| Actions synthetic merge | `404685aec5d24a2aefe6f913c498bd21f723a658` |
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
| [UCNS–EDCM joint experiments](https://github.com/The-Interdependency/edcm/actions/runs/30743739525) | Python 3.11/3.12 historical experiment tests and byte-identical v0.1–v0.4 reruns | Historical joint reports; not a raw-corpus rerun of the new holdout |
| [Skill and metadata compliance](https://github.com/The-Interdependency/edcm/actions/runs/30743739528) | Seven pinned skill-lib consumers clean; canonical metadata regeneration matched | Contract and drift evidence only |
| [CI](https://github.com/The-Interdependency/edcm/actions/runs/30743739530) | 234 tests passed with 20 producer-dependent skips on Python 3.11–3.13; integrity, authority boundaries, packaging, Twine, and clean-wheel smoke passed | Raw MultiWOZ bytes and event labels were absent; the sealed evaluation was not independently regenerated |

The checks establish that the synthetic merge is buildable and that committed
hashes, leakage guards, aggregate schemas, status boundaries, and deterministic
machinery are internally consistent. They do not establish hidden external
custody, implementer blindness, independent human outcome validity, raw-corpus
ground truth, useful discrimination, generalization, production readiness, or
measurement validity. Green checks therefore preserve rather than supersede
the falsified sensitivity result and chance-spanning interval.

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
the target system response. The only presentation transform maps CR and LF
inside a source turn to SPACE and adds declared `USER:` / `SYSTEM:` speaker
prefixes.

The following are candidate non-inputs:

- human outcome labels, rater notes, and rubric decisions;
- source dialogue-act labels and payloads;
- goals, turn metadata, ontology, and domain databases;
- the next user turn and every later turn;
- partition identity, test membership, and custody secrets.

Each parsed speaker turn is treated as one one-turn EDCM round. Existing
`compute_round` equations are used unchanged with `alpha = 0.85` and
`delta_max = 0.30`. This turnwise round policy belongs only to this candidate;
it does not alter the maintained cycle-grouped baseline.

Turns are processed chronologically with initial stored tension `kappa_0 = 0`
and initial previous entropy `0`. Each turn's one-turn round becomes the next
turn's `prev_round`; stored tension and previous entropy advance exactly once
per turn under the maintained implementation.

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
threshold from `{0, 1, each observed validation score, each adjacent-score
midpoint}` by maximum balanced accuracy. Ties resolve first by smallest
distance from `0.5`, then by the lower threshold. This is the only allowed
data-dependent choice.

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

Two raters who are independent of the candidate author and external custodian
label every event independently while blinded to candidate scores and
partition membership. A third independent adjudicator resolves disagreements.
Before adjudication, raw agreement must be at least `0.80` and Cohen's kappa at
least `0.70` overall. Failure stops the experiment; the manual may not be
repaired after viewing agreement or candidate results. The signed adjudicated
ledger is controlling. Candidate code has no authority to change it.

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

After human adjudication, the custodian allocates within outcome-by-booking-
domain strata using HMAC-SHA-256 over the event digest and a secret 256-bit
seed. Domain quotas use proportional largest remainder. The custodian commits
the allocation code, seed commitment, eligible inventory, exclusion inventory,
and ordered partition-manifest digests before any development data are
released.

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
2. Name and sign the human-label authority and external custodian manifests.
3. Freeze source, eligibility, exclusion, label-manual, and allocation-code
   identities.
4. Label and adjudicate without candidate scores or partition identities.
5. Commit encrypted bundle, ledger, access-log, seed, and partition-manifest
   digests.
6. Freeze candidate code, dependencies, container, synthetic conformance
   results, and implementation digest before development data are released.
7. Release development rows and labels; run only the frozen development gate.
8. Release validation rows and labels; select the single threshold and freeze
   its configuration and policy digest. Candidate code and container remain
   byte-identical.
9. Deliver that network-disabled immutable container plus the signed threshold
   configuration to the custodian.
10. Custodian evaluates the sealed test twice internally, confirms
    byte-identical aggregate bytes, and then releases one signed aggregate
    report and completion receipt.

There are no interim test looks, per-event disclosures, adaptive accrual,
sample extension, relabelling, threshold retry, feature addition, sign change,
or second candidate.

## 8. Preregistered hypotheses and decision rule

### Development gate

The score must be finite for every admitted row, have non-zero variance, and
have development area under the receiver-operating-characteristic curve at
least `0.55` in the declared direction. Failure is a preserved development
falsification and stops the experiment before validation.

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
dialogue bootstrap with seed `20260803`. Confusion counts, point estimates, all
intervals, validation results, and the threshold must be reported whether the
hypotheses pass or fail. Threshold-free area under the receiver-operating-
characteristic curve is secondary and cannot rescue a co-primary failure.

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
- exclusive control of the sealed test manifest, labels, per-event scores,
  secret allocation seed, and encrypted source bundle;
- an append-only access log whose digest is included in the receipt.

The candidate implementer receives development and validation material only.
The custodian receives the immutable container by digest, runs it without
network access, and releases no output until the two internal renders are
byte-identical. Only aggregate counts, metrics, intervals, identities,
digests, status boundaries, and an `hmmm` field may leave custody.

An operational retry is allowed only when the identical container and inputs
failed for a documented infrastructure reason before any metric was released.
The custodian must sign the incident and zero-disclosure statement. A changed
container, configuration, threshold, label, test manifest, or sample is a new
experiment version, not a retry.

## 10. Stopping and failure conditions

### Stop before test and emit an incomplete receipt

- custodian, label-authority, consent, licence, or source identity is missing;
- a role conflict or undisclosed test access exists;
- PR #49 test membership or any predecessor test event enters the frame;
- a dialogue or exact-input digest crosses partitions;
- the agreement thresholds fail;
- an inventory, digest, signature, schema, or provenance field fails to
  reconcile;
- raw source, per-event label, score, locator, or test membership leaks;
- candidate parsing is empty, non-finite, out of range, or non-deterministic;
- the development or validation gate fails;
- formula, direction, round policy, label manual, eligibility, partition size,
  threshold policy, metric, uncertainty method, dependency, or candidate code
  changes after its applicable freeze;
- test membership, labels, or aggregate results are disclosed before the
  authorized release.

### Test scientific failure

A completed custody run that fails any co-primary hypothesis is a valid
scientific falsification. It receives a complete receipt with
`candidate_measurement_status = candidate-measured-evidence` and
`experiment_supported = false`.

### Invalid test execution

Byte mismatch between the two internal runs, custody breach, digest drift,
partition collision, forbidden output, or unauthorized retry invalidates the
execution. It receives an incomplete receipt and no empirical verdict.

## 11. Required provenance fields

The signed execution and completion manifests must record at least:

| Compartment | Required fields |
|---|---|
| Packet | schema, version, design status, file SHA-256, freeze timestamp, predecessor identities |
| Candidate | candidate ID, exact formula, direction, turnwise policy, input transform, `alpha`, `delta_max`, code commit/tree/blob identities |
| Runtime | lockfile, interpreter, operating system, architecture, skill-lib, container, entrypoint, and dependency digests |
| Source | owner, DOI/source URL, licence, consent/privacy decision, archive and member digests, language, domain, collection period |
| Eligibility | rule version, old-test exclusion digest, eligible/excluded counts and reasons, event and input digest chains, duplicate audit |
| Labels | manual and training-example digests, rater role IDs, conflicts, blinding assertion, raw agreement, Cohen's kappa, adjudicator identity, pre- and post-adjudication ledger digests and signatures |
| Partitions | allocation-code digest, seed commitment, strata and quotas, ordered encrypted manifests, counts, collision audit |
| Custody | custodian legal identity, conflict disclosure, key fingerprint, acceptance signature, encrypted bundle digest, access-log digest |
| Validation | score inventory digest, threshold candidate count, selected threshold, confusion counts, gate verdict, freeze digest |
| Test | run nonce and timestamps, exact container/config digest, confusion counts, interval methods and seed, co-primary verdicts, byte-repeat verdict |
| Evidence | canonical report digest, report file SHA-256, receipt digest, receipt file SHA-256, custodian signature |
| Boundaries | canon selection, activation states, typed absences, every theorem/proof/certification/semantic/measurement/empirical transfer flag |

Raw source text, dialogue identifiers, event locators, per-event labels,
per-event scores, rater identities beyond role-safe provenance, secret seed,
and test membership must remain outside Git and outside the aggregate report.

## 12. Smallest implementation plan

No implementation occurs under this packet-drafting task. A later authorized
implementation is limited to:

1. one new runner module implementing the turnwise response-tension-release
   score and custody-safe aggregate schema while reusing existing archive,
   EDCM metric, Wilson interval, bootstrap, digest, and receipt primitives;
2. one contract-test file covering four synthetic tension transitions,
   response inclusion and label/future-turn exclusion, old-test exclusion,
   partition isolation, aggregate-only output, fail-closed behavior, and two-
   run determinism;
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
