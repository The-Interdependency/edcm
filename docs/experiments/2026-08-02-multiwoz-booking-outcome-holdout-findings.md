# MultiWOZ 2.1 booking-outcome holdout v0.1.0 findings

Date: 2026-08-02
Status: sealed externally labelled candidate-measurement evidence; no canon selection

## Outcome

The maintained EDCM terminal progress proxy did not meet the frozen
sensitivity hypothesis. It produced a small above-chance point estimate for
balanced accuracy, but the dialogue-cluster uncertainty interval spans chance.
This is weak discrimination evidence, not empirical validation.

The complete admitted event inventory was:

| Partition | `Booking-Book` | `Booking-NoBook` | Excluded ambiguous | Included events |
|---|---:|---:|---:|---:|
| development | 4,164 | 1,050 | 19 | 5,214 |
| validation | 543 | 113 | 0 | 656 |
| test | 530 | 131 | 0 | 661 |

All development, validation, test, label, and exclusion counts reconciled to
the frozen design. The labelled response and later turns were withheld from
the candidate input.

## Frozen calibration

Development-only Platt calibration converged in four Newton updates:

```text
development score mean       0.4070603393895371
development population sd    0.10207709388134982
intercept                     1.37779426310035
slope                         0.019040813646053385
ridge                         0.000001
```

Validation selected threshold `0.799077245397563` from 415 declared
candidates. Its validation confusion counts were `TP=258`, `FP=49`, `FN=285`,
and `TN=64`. Calibration identity is
`881cf6f629384958e1bae593cbc5323e5c34d437f7d9c787cc489fd99ab59d72`.

The fitted slope is positive but very small. The maintained progress score
therefore contributes little probability movement beyond the development
class prevalence.

## Sealed test result

Test confusion counts:

| Count | Value |
|---|---:|
| true positive | 249 |
| false positive | 56 |
| false negative | 281 |
| true negative | 75 |

Metrics and 95% uncertainty intervals:

| Metric | Estimate | 95% interval | Method |
|---|---:|---:|---|
| sensitivity | 0.4698 | 0.4277–0.5124 | Wilson score, 530 positive events |
| specificity | 0.5725 | 0.4869–0.6540 | Wilson score, 131 negative events |
| balanced accuracy | 0.5212 | 0.4656–0.5739 | 2,000-replicate dialogue-cluster bootstrap |
| Brier score | 0.1588 | 0.1367–0.1814 | 2,000-replicate dialogue-cluster bootstrap |
| ECE, 10 bins | 0.0047 | 0.0034–0.0480 | 2,000-replicate dialogue-cluster bootstrap |

The point-estimate hypotheses for specificity, balanced accuracy, and ECE are
supported. The sensitivity-at-least-0.50 hypothesis is falsified. The balanced
accuracy interval includes 0.50, so its supported point relation must not be
read as a statistically settled separation. The low ECE reflects probabilities
concentrated near the source class base rate; calibration quality does not
repair weak discrimination.

## Evidence identities

```text
schema                 edcm.multiwoz21-booking-outcome-holdout/0.1.0
EDCM producer          c292430771b4dc76734522b580caa2be18ca04f9
EDCM tree              04beb8d9c6f01f2ec00bb06e55f77bea21e9b14a
UCNS producer          a98c9e6c69804a8a08d0786b1d8b450bb2c49a97
archive SHA-256        d377a176f5ec82dc9f6a97e4653d4eddc6cad917704c1aaaa5a8ee3e79f63a8e
report digest          a726434a533395e7e3bd7d72ba3e9ce68f58c5b62f3b6b10d2b0556b09e85e61
report file SHA-256    4c7254cc2a2244eaf0e30e182153f803c9e2706774e9a743f7c22899bdcd64a3
receipt file SHA-256   ea2db8bf06785b54ab67dfa01a236bbec2e1d8ec79a5f9808c949363cff4ffe5
```

A second complete command run produced byte-identical report and receipt
files.

## Interpretation boundary

This is the first EDCM-only holdout here with source outcome labels not
authored by the candidate implementer. It advances the admitted events from
represented evidence to bounded candidate-measured evidence and evaluates the
declared holdout relations. It does not validate universal dialogue success or
select a canonical measurement.

`Booking-Book` and `Booking-NoBook` are source-native system-action
annotations. They are not independent human judgments of user satisfaction,
truth, intent, diagnosis, morality, or consciousness. UCNS supplies the exact
word-gonol represented-evidence seal and occurrence provenance only; it does
not supply or validate the EDCM score.

## Status boundaries

- `canon_selection = null`;
- formal UCNS geometry and higher-gonol composition remain `NA`;
- EDCM and METAPAT production activation remain inactive;
- theorem, proof, certification, semantic-authority, measurement-validity,
  and empirical-status transfer remain false;
- the retired pre-reset object/hash path remains absent.

## hmmm

The public test partition is identity-sealed but not independently hidden by
an external custodian. The source dialogue acts are externally authored but
not independently re-adjudicated here. The weak score slope and chance-spanning
balanced-accuracy interval call for a separately specified candidate rather
than post-hoc feature or threshold changes on this test partition. Independent
replication, multilingual outcome evidence, formal higher-gonol composition,
signed producer authentication, and the first joint canon authority packet
remain unresolved.
