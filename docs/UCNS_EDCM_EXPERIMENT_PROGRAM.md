# UCNS–EDCM initial experiment program

**Status:** executable research specification; no canon selection.  
**UCNS experiment authority:** exact commit pinned by the workflow and report.  
**EDCM baseline:** `edcm.measurement` retained as candidate `edcm-measurement-v1`.

## Purpose

This program asks a narrow question:

> Which structural choices preserve distinctions that materially change EDCM readouts, and which EDCM candidate readouts remain stable under declared structural perturbations?

The first run does not attempt to validate the entire Energy–Dissonance Circuit Model. It creates a falsifiable joint surface and records where candidates agree, disagree, fail scope, or lose information.

## Experiment objects

### Case

An experiment case contains:

- stable case identifier;
- exact transcript bytes;
- development or holdout partition;
- declared manipulation;
- provenance;
- tags that describe experiment construction, not inferred participant psychology.

### Expected relation

An expected relation compares one named readout across two cases:

```text
left < right
left > right
left == right
left != right
```

Every relation includes a rationale and acts as a falsifier. A failed relation remains in the report.

### Candidate families

The initial runner contains:

1. **EDCM maintained baseline** — summaries of the existing round metrics and circuit state.
2. **EDCM contrastive candidate** — a small transparent lexical/sequence model used to test experiment mechanics independently of the frozen marker canon.
3. **UCNS support encodings** — unit-turn, token-weighted, and EDCM-pressure-weighted cells.
4. **UCNS product-character candidates** — geometric mean, maximum support, and minimum support.
5. **UCNS breadth candidates** — cell log-support, cell detail, and retained presence.
6. **UCNS structural views** — ordered sequence, unordered multiset, and set views over retained turns.

No family has a default winner.

## Corpus v0

### Order contrast

The same four turns occur in a different order.

- `order-resolution-last`: constraint → refusal → clarification → agreement.
- `order-refusal-last`: clarification → agreement → constraint → refusal.

Hypotheses:

- final stored tension is lower when resolution occurs last;
- ordered structural views differ;
- multiset and set views agree;
- any equivalence policy that declares the cases equal is incompatible with preserving a readout that differs materially.

### Multiplicity contrast

- `single-refusal`: one constraint and one refusal.
- `repeated-refusal`: the same constraint and refusal, with the refusal repeated exactly.

Hypotheses:

- refusal and loop-sensitive readouts increase under repetition;
- set views agree because unique turns are unchanged;
- multiset and ordered views differ;
- set equivalence is falsified for any readout that changes.

### Constraint-pressure holdout

- `low-constraint`: a choice with an ordinary request and direct answer.
- `high-constraint`: forced immediacy, eliminated alternatives, and refusal.

Hypotheses:

- transparent constraint pressure increases;
- the maintained baseline constraint axis should increase if its marker canon covers the phrasing;
- pressure-weighted UCNS breadth should increase;
- unit-turn breadth may remain equal when turn count is equal, documenting its blindness rather than treating it as failure outside its declared scope.

### Resolution holdout

- `unresolved-pressure`: constraint followed by refusal and no repair.
- `resolved-pressure`: the same initial pressure followed by clarification and agreement.

Hypotheses:

- transparent final tension is lower in the resolved case;
- maintained baseline final kappa is tested rather than assumed;
- structural policies that erase the added resolution event should be marked lossy for EDCM use.

## EDCM contrastive candidate v0

The transparent candidate exposes:

- `constraint_pressure` — declared phrase-hit density;
- `refusal_pressure` — refusal phrase-hit density;
- `resolution_signal` — resolution phrase-hit density;
- `repetition_pressure` — repeated normalized turn density;
- `final_tension` — ordered recurrence over turn-local pressure and resolution;
- `turn_count` and `token_count`.

The phrase lists and recurrence are versioned candidate code, not canon. Their purpose is to make experiment behavior inspectable while the maintained baseline is tested alongside them.

## Event-to-UCNS encodings

Each parsed turn becomes one UCNS cell retaining:

- ordinal coordinate;
- raw text payload;
- speaker/type tag;
- candidate signal state;
- case provenance;
- adjacent-turn relation;
- positive support `mu` selected by one of the following policies.

### `unit-turn`

```text
mu = 1
```

Retains occurrence but ignores text length and pressure.

### `token-turn`

```text
mu = max(1, token_count)
```

Retains textual extent but not semantic pressure.

### `pressure-turn`

```text
mu = 1 + constraint + refusal + resolution + repetition
```

Retains all declared candidate signal magnitudes without assigning positive or negative moral value.

Raw transcript, ordered turns, case identity, and candidate provenance remain retained envelope layers and do not silently enter cell-only `W`.

## Structural-policy preservation test

For each selected case pair:

1. apply ordered, multiset, and set views to the retained turn layer;
2. compare the resulting signatures;
3. compare EDCM candidate readouts under an explicit numerical comparison policy;
4. mark a structural view **incompatible for that readout** when it declares equivalence while the readout materially differs;
5. retain the source evidence and information-loss record.

This is not universal rejection of a policy. It is a scoped falsification for preserving a named EDCM distinction.

## Report

The machine-readable report includes:

- schema and program version;
- exact repository identities;
- case identities and partitions;
- candidate identities;
- all readouts and errors;
- expected-relation verdicts;
- structural signatures and preservation findings;
- candidate disagreements;
- `canon_selection: null`.

## Build and run

```text
python -m pip install -e .[dev]
python -m pip install /path/to/pinned/ucns
python -m pytest -q tests/test_ucns_edcm_experiments.py
python -m edcm.ucns_edcm_experiments --ucns-source-root /path/to/ucns-checkout --output artifacts/ucns-edcm-report.json
```

The dedicated GitHub Actions workflow performs the exact UCNS checkout, runs the tests and experiment, and uploads the report artifact.

## Interpretation boundary

A successful hypothesis means only that one candidate behaved as declared on this corpus. A failed hypothesis means only that the candidate or hypothesis did not survive this test. Neither outcome establishes diagnosis, intention, morality, consciousness, or universal human behavior.

## hmmm

The 2026-08-02 MultiWOZ booking-outcome run now supplies one bounded holdout
with source labels not authored by the candidate implementer. Its public test
membership is identity-sealed but not independently hidden, its balanced
accuracy interval spans chance, and the source actions are not independent
human adjudications of universal task success. The first externally meaningful
canon decision still requires independent corpus review and replication,
externally held test custody, human outcome authority, and an explicit joint
decision packet.
