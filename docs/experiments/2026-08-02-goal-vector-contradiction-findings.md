# Goal-vector contradiction findings

Date: 2026-08-02
Status: controlled candidate-measured evidence; no canon selection

## Result

The experiment answered its narrow question positively on the fixed synthetic
fixture. The current exact UCNS profile preserved the changed turn order, and
the EDCM candidate distinguished a contradiction resolved by a later declared
revision from a contradiction left active by reordering the same occurrences.

```text
EDCM producer: 14c87440eedd213c1533b0cf9633c0286f09cb09
EDCM tree:     e2efdd48d43a7771f0f2f9c3f98ffbbc5dec6f26
UCNS producer: a98c9e6c69804a8a08d0786b1d8b450bb2c49a97
report digest: 8a1e3d4548b6b6ee4b3df4f55769b8707a42264450223cdcc88e64f9119c0e30
file sha256:   03b35230c22724b908d3d8733376da035b9b748ef54513dab1e8f2466a3519ee
supported:     8
falsified:     0
```

## Case comparison

| Result | Contradiction resolved | Contradiction active |
|---|---:|---:|
| Terminal candidate projection | `1/1` | `1/2` |
| Goal-motion variance | `1/8` | `9/64` |
| Goal-trajectory variance | `5/32` | `11/256` |
| Active contradictions at terminal state | 0 | 1 |
| Candidate completion state | `candidate-complete` | `unresolved` |

The resolved motion sequence was:

```text
+1/4, -1/4, +3/4, +1/4
```

The active-contradiction motion sequence was:

```text
+1/2, +1/4, +1/4, -1/2
```

The cases had the same occurrence-multiset digest. Their ordered occurrence
digests and exact UCNS observation digests differed. This is the required
evidence that order survived rather than collapsing into a word or turn bag.

## What the report can show

- exact source text, speaker, occurrence identity, and turn ordinal;
- every UCNS word gonol and SPACE boundary emitted for each source turn;
- the declared fixture claim affecting each goal component;
- all component states after every turn, including explicit `NA`;
- the exact contradiction endpoints and whether the conflict is active or
  resolved by a later declared revision;
- the lossy scalar projection, its ordered motion, and exact rational
  variances;
- the difference between candidate goal completion and formal completion.

## Interpretation boundary

This run establishes implementation behavior on one controlled fixture. It
does not establish a general contradiction detector, semantic correctness,
empirical calibration, diagnosis, dishonesty, intention, morality,
consciousness, or external truth. The scalar projection is subordinate to the
complete component-state and contradiction evidence.

`NA != 0` remains intact. METAPAT semantic constraints, formal UCNS geometry,
formal completion, and higher-gonol composition remain `NA`; empirical
validity and proof transfer remain false; `canon_selection` remains null.

## Reproduce

```bash
python -m edcm.goal_vector_experiment \
  --edcm-commit 14c87440eedd213c1533b0cf9633c0286f09cb09 \
  --ucns-source-root /path/to/ucns-at-a98c9e6c69804a8a08d0786b1d8b450bb2c49a97 \
  --output /tmp/goal-vector.json
sha256sum /tmp/goal-vector.json
```

Expected file SHA-256:

```text
03b35230c22724b908d3d8733376da035b9b748ef54513dab1e8f2466a3519ee
```

## hmmm

The next honest pressure is independently declared semantic relations and a
small held-out dialogue set. Real corpus execution should begin only after a
separate goal-authority contract prevents the candidate from silently
inventing what completion means.
