# Goal-vector contradiction experiment

Date: 2026-08-02  
Status: controlled candidate-measurement design; no canon selection

## Question

> Given a declared goal and two dialogues containing exactly the same
> utterance occurrences in different orders, can the current UCNS–EDCM path
> deterministically distinguish a contradiction that is resolved from one
> that remains active, report the resulting goal-vector variance, and cite
> every exact source occurrence without treating `NA` as zero?

## Controlled fixture

The declared goal is explicit mutual agreement that Tuesday at 15:00 works.
It has four required components:

1. participant A is available;
2. participant B is available;
3. participant A explicitly agrees;
4. participant B explicitly agrees.

The fixture uses four immutable utterance occurrences:

| occurrence | speaker | exact text | declared fixture effect |
|---|---|---|---|
| `a-available` | A | Tuesday at three works for me. | A availability toward the goal |
| `b-unavailable` | B | Tuesday at three does not work for me. | B availability away from the goal |
| `b-revision` | B | My schedule changed; Tuesday at three now works for me, and I agree. | B availability and agreement toward the goal; revision when an earlier opposing B-availability claim exists |
| `a-agreement` | A | Agreed. | A agreement toward the goal |

The resolved case orders them as:

```text
a-available -> b-unavailable -> b-revision -> a-agreement
```

The active-contradiction case orders the same occurrences as:

```text
b-revision -> a-agreement -> a-available -> b-unavailable
```

The semantic effects above are controlled experiment declarations. They are
not inferred participant psychology, external truth, or METAPAT canon.

## State and variance contract

Every goal component is one of:

```text
toward
away
NA
```

`NA` is serialized explicitly with no numeric value. A turn that makes no
claim about a component is `no-claim`, also without a numeric value. Neither
state is encoded as zero.

For inspection only, the candidate emits a lossy scalar projection:

```text
projection = (toward_count - away_count) / total_goal_components
```

The same record retains `toward_count`, `away_count`, and `NA_count`, so a
zero projection caused by all-`NA` state cannot be confused with a measured
neutral state. Each turn's motion is the exact difference between consecutive
projections. Goal-motion variance is the population variance of those ordered
turn motions. The complete component state and contradiction ledger remain
the authority-bearing evidence; the scalar is only a declared-loss candidate
readout.

## UCNS boundary

The experiment requires the exact current EDCM word-gonol producer:

```text
The-Interdependency/ucns@a98c9e6c69804a8a08d0786b1d8b450bb2c49a97
ucns.profile.edcm-word-gonol/0.2.0
```

Each case is observed through that profile in exact turn order. The report
retains the complete UCNS observation, its digest, exact source text, speaker,
turn ordinal, word gonols, SPACE boundaries, and carrier-unassigned evidence.
The profile observation is represented evidence, not formal geometry.

## Expected findings

The experiment tests rather than assumes that:

- both cases have the same occurrence multiset;
- their ordered occurrence identities and UCNS observation digests differ;
- the resolved case ends with zero active contradictions;
- the reordered case ends with one active contradiction;
- the resolved case has the greater terminal goal projection;
- the ordered goal-motion variances differ;
- repeat runs produce byte-identical reports;
- every unavailable component remains `NA`, not zero.

A failed finding remains in the report as falsified evidence.

## Usage

Install EDCM and the exact pinned UCNS checkout, then run twice:

```bash
python -m edcm.goal_vector_experiment \
  --ucns-source-root /path/to/ucns \
  --output /tmp/goal-vector.json
python -m edcm.goal_vector_experiment \
  --ucns-source-root /path/to/ucns \
  --output /tmp/goal-vector-repeat.json
diff -u /tmp/goal-vector.json /tmp/goal-vector-repeat.json
```

## Non-claims

- `canon_selection = null`;
- formal UCNS geometry and formal completion remain `NA`;
- the experiment does not establish higher-gonol composition;
- the synthetic annotations do not establish METAPAT semantic authority;
- candidate measurement does not imply empirical validity;
- contradiction does not imply dishonesty, intention, diagnosis, morality,
  consciousness, or external truth.

## hmmm

Independent semantic annotation, real-dialogue goal authority, lawful
word-to-turn-to-dialogue UCNS geometry, calibration, holdout replication, and
human outcome validation remain unresolved. The controlled fixture asks only
whether the current stack can preserve order and show its candidate work.
