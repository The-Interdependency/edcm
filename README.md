# EDCM

EDCM is the Energy–Dissonance Circuit Model research, text-gonol construction, and measurement repository.

The repository has four deliberately separate surfaces:

1. **Frozen maintained baseline:** `edcm/measurement/`, preserved as candidate `edcm-measurement-v1` with byte-checked canon and provenance.
2. **Text-domain gonol construction:** EDCM-owned character admission and linguistic/semantic construction using current METAPAT affixiation semantics and current UCNS geometry.
3. **Experiment-first joint program:** reproducible UCNS–EDCM experiments that determine which structural and measurement candidates deserve later canon review.
4. **Historical corpus-observation profiles:** pinned EDCM/UCNS producer epochs used to expose assumptions against full real-system corpora. They are observation/replay evidence, not the definition of current text construction.

The baseline is executable. Text construction does not activate measurement. Neither is automatically the final UCNS–EDCM canon.

## UCNS–EDCM canon

The joint canon is reciprocal rather than inherited:

```text
EDCM proposes observable distinctions and falsifiable readouts.
UCNS proposes structural policies and candidate instruments.
Experiments test both directions.
A separate evidence-bearing decision may later select canon.
```

Neither side transfers status automatically:

```text
UCNS proof status -> EDCM empirical validity: false
EDCM empirical fit -> UCNS proof status: false
candidate registration -> canon: false
passing development fixtures -> canon: false
NA -> 0: false
```

See [`CANON.md`](CANON.md) and
[`docs/UCNS_EDCM_EXPERIMENT_PROGRAM.md`](docs/UCNS_EDCM_EXPERIMENT_PROGRAM.md).

The complete compiled mathematics currently declared or implemented by EDCM
is indexed in [`docs/EDCM_MATHEMATICS.md`](docs/EDCM_MATHEMATICS.md). The
reference separates the frozen baseline candidate, signed-axis construction,
implemented v0.3.1 architecture layer, joint experiment candidates, controlled
goal-vector candidate, and unresolved formal boundaries. A textbook or website
may carry a source-pinned copy but is not the mathematical authority.

## Gonol language boundary

The active authority split is:

```text
METAPAT   -> affixiation semantics and relational-integration invariants
UCNS      -> gonol geometry, native Möbius/Public Gonol carrier,
             geometrically established operations
EDCM      -> text-domain admission and linguistic/semantic gonol construction
EDCM      -> separately frozen measurement projections and falsifiers
```

For active EDCM text construction:

```text
every admitted character is a gonol
```

EDCM owns the source/profile that determines what is admitted as a character. If a profile has not selected Unicode code point, grapheme, exact Public Gonol glyph inventory, or another explicit unit, that admission boundary remains `hmmm`; UCNS does not silently choose it merely because UCNS owns the geometry.

Current EDCM text construction uses declared scale option sets rather than a mandatory adjacent-scale ladder. `edcm.gonol` is the implemented candidate constructor for closing one gonol at an admissible scale. None of its scale options is selected canon, and construction does not activate measurement. UCNS coupling geometry remains `hmmm`.

Affixiation is defined by METAPAT. UCNS owns any exact geometric realization. EDCM applies affixiation to text-domain gonols. Once closed, a gonol is atomic at any scale. Closed gonols may participate directly at any admissible scale without reopening, while constituent identity and provenance remain recoverable.

Do not insert conventional NLP token IDs, subword pieces, opaque external embedding vectors, or whole-string hashes as substitutes for gonol identity. Source prose, dictionaries, corpora, labels, and annotations may remain evidence and provenance; they become gonol semantics only through explicit EDCM construction.

Public Gonol operations are usable only where current UCNS geometry establishes them. Unicode names, dictionary definitions, glyph shape, adjacency, and conventional punctuation grammar do not define a UCNS operation. Unresolved geometry remains `hmmm` rather than being filled with an invented carrier, scale rule, or semantic inference.

A reproducible gonol construction establishes only that construction. Any EDCM measurement projection is frozen and evaluated separately.

See [`docs/GONOL_LANGUAGE_BOUNDARY.md`](docs/GONOL_LANGUAGE_BOUNDARY.md).

## First joint experiment

The initial fixed corpus pressures four load-bearing distinctions:

- order;
- multiplicity;
- constraint pressure;
- resolution timing.

It compares:

- the maintained EDCM baseline;
- a transparent sequence-sensitive EDCM candidate;
- unit-, token-, and pressure-weighted UCNS cell encodings;
- UCNS ordered, multiset, and set structural views;
- noncanonical UCNS product-character and faithful-breadth candidate families.

Here `token` names a frozen support unit in that historical experiment. It must
not be read forward as a tokenizer layer in the current gonol language path.

The experiment records supported, falsified, and errored hypotheses. A falsified hypothesis is valid research evidence and does not fail the build merely because a preferred candidate lost.

### Run locally

The base package remains dependency-free. Joint experiments are opt-in and pin the exact reviewed UCNS commit.

```bash
python -m pip install -e .[dev,ucns-experiments]
python -m pytest -q tests/test_ucns_edcm_experiments.py
python -m edcm.ucns_edcm_experiments \
  --ucns-source-root /path/to/ucns-checkout \
  --output artifacts/ucns-edcm-report.json
```

The dedicated workflow checks out UCNS at:

```text
The-Interdependency/ucns@5331ae9a4cf7eddfa1de72b8caed28e2358cc0ed
```

It runs the experiment twice and requires byte-identical reports before uploading the evidence artifact.

## Evidence states

The following remain distinct:

1. represented evidence;
2. constructed representation;
3. candidate-measured evidence;
4. experiment-supported evidence;
5. canonically measured evidence.

The repository currently supports the first four. The experiment report always contains:

```text
canon_selection = null
```

## First controlled goal-vector measurement

The historical exact UCNS observation profile feeds one bounded EDCM
candidate-measurement experiment. Two dialogues contain the same four exact
utterance occurrences in different orders: one resolves an availability
contradiction and one leaves it active. Every source word, turn, declared
fixture relation, component state, contradiction, and scalar information-loss
record remains inspectable.

The sealed 2026-08-02 [report](experiments/results/2026-08-02-goal-vector-contradiction-v0.1.0.json)
supports all eight declared findings. The resolved order ends at candidate
projection `1/1`, motion variance `1/8`, and zero active contradictions; the
reordered case ends at projection `1/2`, motion variance `9/64`, and one active
contradiction. The cases share one occurrence-multiset identity but have
different ordered and UCNS-observation identities.

```bash
python -m edcm.goal_vector_experiment \
  --ucns-source-root /path/to/ucns-at-a98c9e6c69804a8a08d0786b1d8b450bb2c49a97 \
  --output /tmp/goal-vector.json
```

This is controlled candidate-measured evidence, not empirical validation.
METAPAT constraints, formal UCNS geometry, formal completion, closed
floor-definition-gonol construction, proof transfer, and canon selection were
not part of this sealed experiment and are not retroactively supplied by the
later language-boundary correction.

## First externally labelled booking-outcome holdout

The sealed MultiWOZ 2.1 booking-outcome experiment evaluates the maintained
terminal progress proxy before source-annotated `Booking-Book` and
`Booking-NoBook` responses. Development alone fits calibration, validation
alone selects the threshold, and the 661-event test partition is evaluated
after that freeze. The labelled response and all later turns remain outside
candidate input.

The test produced `TP=249`, `FP=56`, `FN=281`, and `TN=75`: sensitivity
`0.4698`, specificity `0.5725`, and balanced accuracy `0.5212`. The 95%
dialogue-cluster interval for balanced accuracy is `0.4656–0.5739`, so the
small above-chance point estimate is weak evidence. The declared sensitivity
hypothesis is falsified and remains in the report.

- [frozen design](docs/experiments/2026-08-02-multiwoz-booking-outcome-holdout-design.md)
- [findings](docs/experiments/2026-08-02-multiwoz-booking-outcome-holdout-findings.md)
- [aggregate report](experiments/corpora/results/2026-08-02-multiwoz-2.1-booking-outcome-holdout-v0.1.0.json)
- [completion receipt](experiments/corpora/receipts/2026-08-02-multiwoz-2.1-booking-outcome-holdout-v0.1.0-complete.json)

```bash
python -m edcm.corpora.multiwoz21_booking_holdout \
  --archive /path/to/MULTIWOZ2.1.zip \
  --edcm-repository-root /path/to/edcm \
  --edcm-commit "$(git -C /path/to/edcm rev-parse HEAD)" \
  --output /tmp/multiwoz-booking-holdout.json \
  --receipt /tmp/multiwoz-booking-holdout-complete.json
```

The historical MultiWOZ profile seals remain represented evidence. The new
derived report is bounded candidate-measured holdout evidence; it does not
retroactively turn the profile observation into formal geometry or empirical
validation. `canon_selection` remains null, and EDCM/METAPAT activation remains
inactive.

## Frozen maintained baseline

`edcm/measurement/` consolidates the reviewed structural-measurement lineage from:

- `The-Interdependency/edcmbone`; and
- the earlier `erinepshovel-code/EDCM` application lineage.

It contains:

- frozen measurement canon data;
- deterministic transcript parsing;
- the eleven-component round vector;
- circuit-state recurrence;
- projection and risk surfaces;
- provenance and integrity gates.

Its maintained identity is useful as a baseline candidate. Integrity means the implementation did not drift; it does not mean the readouts are empirically validated.

## Install and validate the baseline

EDCM requires Python 3.11 or newer.

```bash
python -m pip install -e .[dev]
python -m edcm.integrity
python -m pytest -q
python tools/check_metadata_contracts.py
python -m build
python -m twine check dist/*
```

METAPAT integration remains optional:

```bash
python -m pip install -e .[dev,metapat]
```

The exact historical/replay word-gonol profile is also optional:

```bash
python -m pip install -e .[dev,ucns-profile]
```

`full-stack` installs both the exact METAPAT producer and the historical EDCM UCNS profile producer. Use `ucns-experiments` only for the historical v0.1–v0.4 experiment epoch. Package availability alone attaches no evidence: UCNS activation also requires checkout package bytes that match the exact Git tree or a VCS installation whose package bytes match EDCM's pinned producer manifest and raw wheel `RECORD`; the verified module graph is freshly loaded, and every runtime-loadable cache must derive from those verified sources. Exact ordered `ucns_turns` are required before a historical observation is attached.

## First real-system corpus runner

MultiWOZ 2.1 is the first admitted historical real-system source. Its runner verifies the
exact University of Cambridge archive and every logical member, streams all
`10,438` dialogues in source order, observes every exact speaker turn through
the pinned EDCM UCNS word-gonol profile, and independently repeats the exact
turn stream through the UCNS v0.14.1 full-corpus completion gate from the
merged v0.19 producer commit with final integrity repairs. Completion requires both passes and their
source-native turn chains to reconcile. Only
aggregate evidence and completion or incompletion receipts are emitted. Raw
corpus bytes remain outside Git.
Carrier SPACE metrics are derived from profile assignment at alphabet position
zero; the exact source code point remains independently serialized.

```bash
python edcm/corpora/run_multiwoz21_seal.py \
  --archive /path/to/MULTIWOZ2.1.zip \
  --ucns-source-root /path/to/ucns-at-a98c9e6c69804a8a08d0786b1d8b450bb2c49a97 \
  --output /tmp/multiwoz-2.1-ucns-v019.json \
  --receipt /tmp/multiwoz-2.1-ucns-v019-receipt.json \
  --checkpoint /tmp/multiwoz-2.1-ucns-v019.checkpoint.json
```

See [`docs/corpora/multiwoz-2.1.md`](docs/corpora/multiwoz-2.1.md). This is
represented evidence, not an EDCM candidate measurement, formal UCNS geometry,
or a canon selection. The original profile-0.1 report remains immutable but is
explicitly superseded because tabs, newlines, and non-breaking spaces were
misclassified as out-of-alphabet instead of SPACE manifestations. The sealed
profile-0.2 replacement assigns all `4,094` occurrences to carrier position
zero, reports `1,783,679` SPACE boundaries and no carrier-unassigned source
code points, and preserves the original source and turn digest chains.
That historical receipt remains immutable; it is not a UCNS v0.14.1
completion receipt. The authenticated v0.14.1 rerun is now independently
sealed in its own aggregate
[report](experiments/corpora/results/2026-07-31-multiwoz-2.1-ucns-v0.14.1-full.json)
and [completion receipt](experiments/corpora/receipts/2026-07-31-multiwoz-2.1-ucns-v0.14.1-complete.json).
It consumed all `143,048` turns, reconciled the repeated source-native chain,
and left EDCM and METAPAT activation inactive.

The exact reviewed UCNS v0.19 producer was then repinned and rerun without
changing the consumed profile or gate schema. Its sealed
[report](experiments/corpora/results/2026-07-31-multiwoz-2.1-ucns-v0.19-full.json)
and [completion receipt](experiments/corpora/receipts/2026-07-31-multiwoz-2.1-ucns-v0.19-complete.json)
cover all `10,438` dialogues and `143,048` turns. A completed-checkpoint repeat
was byte-identical. The exact stream hash and UCNS v0.14.1 receipt id remain
unchanged; the report and receipt identities bind the EDCM package tree and
the UCNS producer commit.
Measurement remains `not-run`, canon selection is null, and EDCM/METAPAT stay
inactive.

Merged UCNS v0.19 commit
`a98c9e6c69804a8a08d0786b1d8b450bb2c49a97` was then freshly resealed in
new immutable [aggregate report](experiments/corpora/results/2026-08-01-multiwoz-2.1-ucns-v0.19-integrated-full.json)
and [completion receipt](experiments/corpora/receipts/2026-08-01-multiwoz-2.1-ucns-v0.19-integrated-complete.json).
The completed-checkpoint repeat was byte-identical, all execution counts and
source-native chains reconciled, and the exact stream hash plus UCNS receipt id
remained unchanged. Measurement remains `not-run`, canon selection is null,
and EDCM/METAPAT stay inactive.

## Integrity gate

`python -m edcm.integrity` checks the frozen baseline:

- complete and exact `*_v1.json` canon bytes;
- measurement authority and compatibility policy;
- orthogonality-class no-fork identity;
- source and wheel behavior.

A legitimate baseline-canon change requires a new versioned file and migration record. Do not update identities merely to silence continuous integration.

## Provenance-bearing pipeline

The active shared-stack boundary separates:

- source evidence and EDCM text-admission profile;
- METAPAT semantic/affixiation authority;
- EDCM text-gonol construction identity and receipts;
- UCNS carrier/geometry identity and unresolved geometry;
- exact pinned historical UCNS word-gonol observations where replay profiles are used;
- typed UCNS geometry and factorization absence in historical adapters;
- EDCM measurement policy and implementation provenance;
- readouts;
- status evidence.

The retired ordered-occurrence bridge, `UCNSObject`, and factorization inputs fail closed on the current runtime path. Historical experiment reports keep their original UCNS commit and are not rewritten as current profile evidence.

The pre-reset `edcm.ucns_metrics` resolver and its top-level exports are removed. They depended on archived `UCNSObject`, `recursive_encode`, and `stable_hash` surfaces rather than the exact historical profile. Use `ucns_profile_observation` when reproducing represented historical evidence; any future scalar projection must remain linked to its complete trajectory and declare information loss. See [`docs/ucns-metric-objects.md`](docs/ucns-metric-objects.md) for migration guidance.

## Typed absence

`NA != 0` remains non-negotiable.

Unavailable evidence is typed absence. A candidate may fail scope, return an explicit error, or remain unmeasured; it may not invent a neutral measurement.

## Proof and measurement firewall

No UCNS or METAPAT status validates EDCM readouts, external truth, diagnosis, intention, morality, or consciousness.

A completed EDCM text-gonol construction likewise does not establish measurement validity.

## Repository provenance

Historical implementation, source packets, repair handoffs, and prior adapter contracts remain preserved in Git history and under `archive/` or `codex-handoff/` where already present. They remain evidence, not automatic current canon.

## Usage guidance

For new text-gonol work, start in EDCM and follow [`docs/GONOL_LANGUAGE_BOUNDARY.md`](docs/GONOL_LANGUAGE_BOUNDARY.md): resolve the source/admission profile, import METAPAT affixiation semantics, consume UCNS geometry, build and replay the declared construction, and freeze any later measurement separately.

For historical experiment replay, use the exact historical producer commit and profile named by the artifact; do not repin or reinterpret sealed evidence as current authority.

## hmmm

The exact EDCM character-admission unit remains profile-specific where not selected. The source-supported complete English morphology law, exact UCNS native Möbius-carrier affixiation/coupling geometry, and direct distant-scale coupling remain unresolved. EDCM has not selected a lawful projection, information-loss account, metric, benchmark, or falsifier for evaluating completed recursive text-gonol constructions. Historical MultiWOZ seals remain represented evidence, not measurement validity; external replication and broader carrier coverage remain separate unresolveds.
