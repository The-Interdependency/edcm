# EDCM–UCNS integration boundary

## Status

**Experimentally active; production adapter remains unselected.**

UCNS now publishes a definition-first structural and candidate-research surface at the exact commit pinned by the joint EDCM workflow:

```text
The-Interdependency/ucns@5331ae9a4cf7eddfa1de72b8caed28e2358cc0ed
```

That surface provides:

- directed 720-degree carrier foundations;
- Structural Null and fail-closed cells;
- retained structural layers;
- explicit structural and comparison policies;
- reproducible witness and experiment manifests;
- competing noncanonical equivalence, product-character, and faithful-breadth candidates.

It does **not** publish a complete canonical `UCNSObject`, canonical `M`, canonical `B`, factorization authority, or theorem status suitable for direct EDCM validity claims.

## Two separate integration paths

### Historical compatibility adapter

`edcm.ucns_adapter` preserves the former bridge/factorization consumer contract for archaeology, migration analysis, and compatibility fixtures.

It is not used by the new joint experiment runner and must not treat surface-name compatibility as current authority.

### Joint research interface

`edcm.ucns_edcm_experiments` consumes the current UCNS research surface directly from the pinned commit.

It uses UCNS only to:

- encode EDCM turns under explicit support policies;
- retain raw transcript and provenance layers;
- apply ordered, multiset, and set views;
- run named `M` and `B` candidates;
- compare structural equivalence predictions with EDCM readout changes;
- record supported, falsified, errored, and scope-failed results.

This path is research infrastructure, not a production adapter.

## Dependency policy

The base EDCM package has no UCNS dependency.

The opt-in extra is pinned:

```text
python -m pip install -e .[dev,ucns-experiments]
```

Equivalent source-controlled runs should check out the pinned commit and install it locally, as the dedicated workflow does.

Package availability alone attaches no evidence. Every report records the asserted UCNS commit, and the workflow supplies the exact checkout.

## Current structural encoding candidates

Each transcript turn becomes one candidate UCNS cell retaining:

- turn ordinal;
- raw text;
- speaker tag;
- transparent candidate signals;
- case and support-policy provenance;
- adjacency relation.

The initial support policies are:

```text
unit-turn:     mu = 1
token-turn:    mu = max(1, token count)
pressure-turn: mu = 1 + constraint + refusal + resolution + repetition
```

These are experiment candidates. None is canonical support assignment.

Raw transcript, ordered turns, and case identity remain retained layers. Their existence does not silently extend cell-only `W` or validate `M` or `B`.

## Structural-policy test

The joint program compares:

- ordered sequence;
- unordered multiset;
- set.

When a policy declares two cases equivalent while a named EDCM readout materially differs, the report marks the policy incompatible **for preserving that readout on that case pair**.

This is scoped falsification, not universal rejection of the policy.

## Typed absence and scope failure

`NA != 0` remains non-negotiable.

A UCNS candidate that cannot lawfully evaluate an EDCM envelope must fail scope or return an explicit error. EDCM must not reinterpret that absence as a zero-valued measurement.

## Proof and measurement firewall

The following remain false:

```text
ucns_proof_status_implies_edcm_validity = false
edcm_empirical_fit_implies_ucns_proof = false
candidate_registration_implies_canon = false
measurement_validity_claim = false
proof_status_transfers_to_measurement_validity = false
```

UCNS candidate behavior cannot establish external truth, diagnosis, intention, morality, or consciousness.

## Usage guidance

```text
python -m pip install -e .[dev,ucns-experiments]
python -m pytest -q tests/test_ucns_edcm_experiments.py
python -m edcm.ucns_edcm_experiments \
  --output artifacts/ucns-edcm-report.json
```

See [`../CANON.md`](../CANON.md) and
[`UCNS_EDCM_EXPERIMENT_PROGRAM.md`](UCNS_EDCM_EXPERIMENT_PROGRAM.md).

## hmmm

A production UCNS adapter requires experiment-supported selections for structural equivalence, support assignment, `M`, `B`, migration behavior, and authenticated producer identity. None has yet been selected.
