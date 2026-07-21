# Reviewed EDCM source packet — 2026-07-20

## Scope

This record reviews the EDCM-relevant portion of the uploaded
`interdependency_project_files.zip` packet. The full packet contained 69 files;
12 were classified as EDCM history or candidate doctrine.

This directory does not create a second measurement authority. Current
maintained authority remains:

```text
The-Interdependency/edcm:edcm/measurement/
policy: canonical-maintained-edcm-v1
```

Frozen `*_v1.json` canon data, parser behavior, metric formulas, and integrity
identities are unchanged by this source-packet placement.

## Recovered files reviewed

The EDCM-classified material comprised:

- two broad EDCM engine/metric narratives;
- three canon-aggregator copies, two of which are byte-identical;
- one threshold/state document;
- two edcmbone architecture/specification drafts;
- one closed-token encoder and its test script;
- one pipeline scaffold;
- and one empty lexicon placeholder.

The filename-level hash inventory is in [`MANIFEST.md`](MANIFEST.md).

## Findings

### Strong carry-forward doctrine

The packet repeatedly supports these boundaries, which are compatible with the
maintained measurement direction:

1. Dissonance is unresolved constraint mismatch, not a feeling label.
2. EDCM measures observable behavior under constraint; it does not infer belief,
   intention, morality, consciousness, diagnosis, or hidden internal state.
3. Transcript handling should be lossless and deterministic, with unknown
   speakers kept explicit rather than merged.
4. System and tool messages remain ordered evidence but are excluded from human
   interaction rounds by default.
5. Operator features are computed per turn; round aggregation sums counts before
   renormalization rather than averaging normalized turn vectors.
6. Behavioral metrics are round-native by default.
7. A bridge between measurement layers is observational and read-only; it does
   not rewrite either source layer.
8. `hmmm` is a fail-closed record for unresolved constraints and evidentiary
   incompletion, not decorative prose.

These are reviewed doctrine candidates. They do not override implemented or
frozen measurement behavior merely because an older file called them canon.

### Conflicting metric systems

The packet contains at least three incompatible measurement surfaces:

- a broad approximately 30-metric interaction engine with energy, repair,
  mutuality, pressure, and safety flags;
- a five-metric DA/RPI/CE/GL/RM system with named qualitative states; and
- the operator/behavioral/bridge system consolidated into edcmbone lineage.

They differ in primitives, aggregation, thresholds, and intended claims. They
must not be merged by name or averaged into one schema. Any migration requires a
versioned proposal, formula-level crosswalk, fixtures, and an explicit statement
of which old surface is superseded.

### Thresholds are not validated canon

`core_thresholds_Version3.md` names useful failure patterns, but its state
transitions and thresholds are not tied to the maintained implementation's
frozen formulas, calibration corpus, confidence intervals, or external
validation. It is preserved as design history only.

Terms such as “diagnostic state” must not be read as medical diagnosis or hidden
state inference.

### Closed-token encoder is pre-reset UCNS history

The packet's `closed_tokens.py` maps English closed classes to a 16-gon using the
pre-reset UCNS object model. Its tests pass against that model, but the encoder:

- has no intrinsic hidden Möbius seam;
- treats the host as an ordinary one-circle lattice;
- uses optional/absent payloads rather than complete twist-bearing recursive
  objects; and
- therefore cannot be called current UCNS.

The same lineage remains inside `edcm/measurement/ucns/` as consolidation
provenance. It may support deterministic legacy encoding, but it must be named
and governed as a legacy EDCM structural encoding until a lawful projection from
new UCNS exists.

### UCNS producer discontinuity

Current UCNS root states that there is no current implementation and that old
machinery is archive evidence only. EDCM's existing documentation and optional
dependency still referenced an archived pre-reset producer commit as canonical.
That is a cross-repository authority error.

This review therefore accompanies:

- removal of the managed legacy UCNS dependency pin from `pyproject.toml`; and
- replacement of `docs/ucns-adapter.md` with the current suspension boundary.

The code-level selector still needs a dedicated fail-closed change so that a
separately installed archived `ucns` package cannot activate as current
geometry authority. That work is deliberately not disguised as completed here.

## Material not placed in EDCM

The following packet content was excluded:

- private LLC filings, addresses, receipts, payment fragments, and government
  correspondence;
- The Interdependent Way text, whose sole canon source is `wayseer00`;
- A0 bootstrap material;
- UCNS implementation/specification history, reviewed in the UCNS repository;
- a speculative consciousness-primes paper requiring separate scientific
  review; and
- a public-advocacy handoff containing personal contact and campaign details.

The mixed `canon_pack_frozen_plus_open.md` was not copied because it bundles
several projects and asserts a source hierarchy that would improperly duplicate
The Interdependent Way canon outside `wayseer00`.

## Placement rule

Recovered doctrine enters active EDCM only through a versioned change that:

1. identifies the current source-of-truth surface affected;
2. distinguishes definition, formula, threshold, interpretation, and claim;
3. supplies deterministic fixtures and migration consequences;
4. preserves `NA != 0` and the proof/measurement firewall; and
5. records unresolved questions in `hmmm`.

## hmmm

The source packet clarifies several durable measurement boundaries, but it does
not resolve which historical metric system should become the next EDCM version.
The archived UCNS adapter must remain unavailable until UCNS publishes a new
intrinsically twist-bearing producer contract.