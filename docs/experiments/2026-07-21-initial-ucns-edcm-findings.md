# Initial UCNS–EDCM findings — 2026-07-21

**Program:** `edcm.ucns-edcm-experiment-report/0.1.0`  
**EDCM branch evidence commit:** `5d15592d509a760ff9fbcdd346a2e749537bb2ba`  
**UCNS commit:** `5331ae9a4cf7eddfa1de72b8caed28e2358cc0ed`  
**Workflow run:** `UCNS-EDCM joint experiments #1` / run `29848564274`  
**Report digest:** `d7da6a26fa0391c9d9dad40c3e78d5b19f40986cebf91537096e595b21185942`  
**Reproducibility:** byte-identical repeat reports on Python 3.11 and 3.12.  
**Canon selection:** none.

## Result count

```text
supported hypotheses: 8
falsified hypotheses: 2
errored hypotheses:   0
```

Hypothesis failure was retained as evidence and did not fail the workflow.

## Supported findings

### 1. Turn order is EDCM-load-bearing

The same four turns were presented in two orders.

```text
transparent final tension
resolution last: 0.0000
refusal last:    0.6020

baseline final kappa
resolution last: 0.0000
refusal last:    0.1570997173
```

Both EDCM candidates changed materially when only turn order changed.

UCNS policy consequences on this pair:

- ordered sequence distinguished the structures and preserved both readout differences;
- unordered multiset declared the structures equivalent and was incompatible with both readouts;
- set declared the structures equivalent and was incompatible with both readouts.

**Evidence-supported boundary:** a sequence-blind equivalence cannot preserve these EDCM circuit readouts on the tested pair.

This does not yet prove that every EDCM object must always be globally sequence-equivalent only by exact order. It establishes that order cannot be discarded before the readout scope is chosen.

### 2. Multiplicity is load-bearing for the transparent refusal candidate

```text
transparent refusal pressure
single refusal:   0.5000
repeated refusal: 0.6666666667
```

The repeated case contained the same unique turns plus one exact repeated refusal.

- ordered sequence preserved the distinction;
- unordered multiset preserved the distinction while explicitly discarding order;
- set erased multiplicity and was incompatible with the transparent refusal readout.

**Evidence-supported boundary:** set semantics cannot be the only retained structural view for an occurrence-sensitive EDCM measurement.

### 3. Resolution timing reduced stored tension

```text
transparent final tension
resolved:   0.0000
unresolved: 0.6020

baseline final kappa
resolved:   0.0000
unresolved: 0.1299285714
```

Both candidates preserved the distinction between unresolved pressure and an otherwise similar exchange containing clarification and agreement.

### 4. Transparent constraint pressure survived the holdout contrast

```text
high constraint: 0.5000
low constraint:  0.0000
```

The transparent candidate detected forced immediacy and removed alternatives in the holdout phrasing.

### 5. Pressure-weighted UCNS breadth preserved constraint intensity

For `pressure-turn` support and the UCNS `cell-detail` breadth candidate:

```text
high constraint: 4.1972245773
low constraint:  3.3862943611
```

The unit-turn encoding remained equal for the two equal-turn-count cases, documenting its declared blindness to pressure rather than an implementation error.

**Evidence-supported boundary:** event occurrence alone and candidate pressure-weighted support are meaningfully different encodings. Neither may silently replace the other.

### 6. Unit-turn cell detail preserved occurrence multiplicity

```text
repeated refusal: 5.0794415417
single refusal:   3.3862943611
```

The cell-detail candidate increased because the repeated case retained an additional cell occurrence.

## Falsified findings

### 1. Maintained baseline refusal density did not distinguish repetition

Expected:

```text
R_mean(repeated refusal) > R_mean(single refusal)
```

Observed:

```text
R_mean(repeated refusal) = 1.0
R_mean(single refusal)   = 1.0
```

The baseline candidate saturated on both cases.

**Consequence:** baseline `R` cannot presently serve as the sole occurrence-sensitive refusal measure. The parser retained the extra turn, but the readout collapsed the distinction at the tested intensity.

This falsifies the specific sensitivity hypothesis, not the entire baseline measurement system.

### 2. Maintained baseline constraint axis missed the holdout phrasing

Expected:

```text
C_mean(high constraint) > C_mean(low constraint)
```

Observed:

```text
C_mean(high constraint) = 0.0
C_mean(low constraint)  = 0.0
```

The frozen marker canon did not recognize the tested high-constraint wording.

**Consequence:** baseline `C` is not sufficiently phrase-robust for joint canon without broader corpus testing or a different candidate construction.

This is a marker-coverage falsifier, not evidence that constraint pressure was absent.

## Product-character observations

No product-character candidate is selected.

The first report shows that candidate outputs depend strongly on support assignment:

- unit-turn gives `M = 1` for all tested cells and therefore preserves occurrence through `W`/breadth but not through these `M` candidates;
- pressure-turn changed `M` across low/high constraint and single/repeated refusal;
- token-turn reflected textual extent and produced another distinct ordering of cases.

These differences are candidate disagreements requiring targeted falsifiers. They are not a vote.

## Breadth observations

The tested breadth candidates were insensitive to turn order when cell content and support distributions were otherwise identical. That is compatible with breadth as quantity of retained distinction, but it means breadth alone cannot recover EDCM sequence state.

**Required joint design consequence:** order must remain in retained structure even when a scalar breadth evaluator is order-invariant.

## Initial pre-canon constraints

The experiment supports carrying these constraints into the next program:

1. preserve exact order until a readout-specific policy explicitly discards it;
2. preserve multiplicity even when a set view is also available;
3. do not rely on baseline `R` alone for refusal occurrence;
4. do not rely on the current baseline `C` marker list for phrase-robust constraint measurement;
5. keep support assignment explicit because unit, token, and pressure encodings produce materially different UCNS readings;
6. keep sequence state separate from scalar `W`, `M`, and `B` outputs;
7. retain both successful and falsified candidates for subsequent corpus expansion.

These are experiment-supported restrictions, not final canon declarations.

## Next experiment obligations

- add paraphrase families for constraint and refusal coverage;
- add equal-total-pressure cases distributed differently across rounds to pressure `M` candidates;
- add speaker-swap and sidedness cases;
- add false-positive controls containing words such as “must” in non-coercive contexts;
- separate development authorship from sealed holdout authorship;
- solicit an independently authored expected-relation set;
- test whether baseline saturation can be repaired without losing deterministic auditability.

## hmmm

The first report shows that UCNS structural policy can falsify an EDCM-preservation claim, while EDCM readout behavior can falsify a UCNS equivalence choice. That reciprocal falsification is the intended mechanism for determining `ucns-edcm` canon.
