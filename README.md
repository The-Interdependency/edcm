# EDCM

EDCM is the Energy–Dissonance Circuit Model research and measurement repository.

The repository has three deliberately separate surfaces:

1. **Frozen maintained baseline:** `edcm/measurement/`, preserved as candidate `edcm-measurement-v1` with byte-checked canon and provenance.
2. **Experiment-first joint program:** reproducible UCNS–EDCM experiments that determine which structural and measurement candidates deserve later canon review.
3. **Exact corpus-observation profile:** the optional EDCM-only UCNS word-gonol configuration used to expose incomplete assumptions against full real-system corpora.

The baseline is executable. It is not automatically the final UCNS–EDCM canon.

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
2. candidate-measured evidence;
3. experiment-supported evidence;
4. canonically measured evidence.

The repository currently supports the first three. The experiment report always contains:

```text
canon_selection = null
```

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

The exact word-gonol profile is also optional:

```bash
python -m pip install -e .[dev,ucns-profile]
```

`full-stack` installs both the exact METAPAT producer and the EDCM UCNS profile producer. Use `ucns-experiments` only for the historical v0.1–v0.4 experiment epoch. Package availability alone attaches no evidence: UCNS activation also requires checkout package bytes that match the exact Git tree, or a VCS installation whose package inventory and wheel-record hashes match and whose cached bytecode derives from those verified sources. Exact ordered `ucns_turns` are required before an observation is attached.

## First real-system corpus runner

MultiWOZ 2.1 is the first admitted real-system source. Its runner verifies the
exact University of Cambridge archive and every logical member, streams all
`10,438` dialogues in source order, observes every exact speaker turn through
the pinned EDCM UCNS word-gonol profile, and independently repeats the exact
turn stream through the UCNS v0.14.1 full-corpus completion gate from the
exact v0.19 producer commit. Completion requires both passes and their
source-native turn chains to reconcile. Only
aggregate evidence and completion or incompletion receipts are emitted. Raw
corpus bytes remain outside Git.
Carrier SPACE metrics are derived from profile assignment at alphabet position
zero; the exact source code point remains independently serialized.

```bash
python -m edcm.corpora.multiwoz21 \
  --archive /path/to/MULTIWOZ2.1.zip \
  --ucns-source-root /path/to/ucns-at-872f53571d5dc2f133ff1813b7bdffd3a9c309f8 \
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
unchanged; the report and receipt identities bind the new EDCM and UCNS commits.
Measurement remains `not-run`, canon selection is null, and EDCM/METAPAT stay
inactive.

## Integrity gate

`python -m edcm.integrity` checks the frozen baseline:

- complete and exact `*_v1.json` canon bytes;
- measurement authority and compatibility policy;
- orthogonality-class no-fork identity;
- source and wheel behavior.

A legitimate baseline-canon change requires a new versioned file and migration record. Do not update identities merely to silence continuous integration.

## Provenance-bearing pipeline

The shared-stack pipeline separates:

- source evidence;
- METAPAT semantic constraints;
- exact UCNS word-gonol observations;
- typed UCNS geometry and factorization absence;
- EDCM policy and implementation provenance;
- readouts;
- status evidence.

The retired ordered-occurrence bridge, `UCNSObject`, and factorization inputs fail closed on the current runtime path. Historical experiment reports keep their original UCNS commit and are not rewritten as current profile evidence.

The pre-reset `edcm.ucns_metrics` resolver and its top-level exports are removed. They depended on archived `UCNSObject`, `recursive_encode`, and `stable_hash` surfaces rather than the exact current profile. Use `ucns_profile_observation` for represented evidence; any future scalar projection must remain linked to its complete trajectory and declare information loss. See [`docs/ucns-metric-objects.md`](docs/ucns-metric-objects.md) for migration guidance.

## Typed absence

`NA != 0` remains non-negotiable.

Unavailable evidence is typed absence. A candidate may fail scope, return an explicit error, or remain unmeasured; it may not invent a neutral measurement.

## Proof and measurement firewall

No UCNS or METAPAT status validates EDCM readouts, external truth, diagnosis, intention, morality, or consciousness.

The joint experiment reports structural preservation and candidate behavior only.

## Repository provenance

Historical implementation, source packets, repair handoffs, and prior adapter contracts remain preserved in Git history and under `archive/` or `codex-handoff/` where already present. They remain evidence, not automatic current canon.

## hmmm

UCNS v0.19 supplies a nonselected trace-local source-coordinate candidate over
its fixed full producer demonstration. This EDCM observation path does not
attach or consume that candidate, and higher-gonol composition plus lawful projection
into EDCM readouts remain open. The corrected MultiWOZ 2.1 SPACE-origin
aggregate is sealed represented evidence, not measurement validity; true
non-SPACE carrier coverage remains a separate hmmm.
