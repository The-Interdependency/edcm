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

`full-stack` installs both the exact METAPAT producer and the EDCM UCNS profile producer. Use `ucns-experiments` only for the historical v0.1–v0.4 experiment epoch. Package availability alone attaches no evidence; exact ordered `ucns_turns` are required.

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

## Typed absence

`NA != 0` remains non-negotiable.

Unavailable evidence is typed absence. A candidate may fail scope, return an explicit error, or remain unmeasured; it may not invent a neutral measurement.

## Proof and measurement firewall

No UCNS or METAPAT status validates EDCM readouts, external truth, diagnosis, intention, morality, or consciousness.

The joint experiment reports structural preservation and candidate behavior only.

## Repository provenance

Historical implementation, source packets, repair handoffs, and prior adapter contracts remain preserved in Git history and under `archive/` or `codex-handoff/` where already present. They remain evidence, not automatic current canon.

## hmmm

Formal Möbius coordinates, higher-gonol composition, and lawful projection from exact observations into a higher-dimensional lattice remain open. Full real-system corpus runs should pressure the current word, SPACE-boundary, support, and 157-token assumptions before any further canon selection.
