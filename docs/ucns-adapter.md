# EDCM–UCNS integration boundary

## Current runtime profile

EDCM optionally consumes the exact EDCM-only observation profile at:

```text
The-Interdependency/ucns@eb264fba18bd051c46b4853c81c8fb91ec6d5811
profile: ucns.profile.edcm-word-gonol/0.1.0
```

Install it with:

```text
python -m pip install -e .[dev,ucns-profile]
```

Package presence alone does not activate a lookalike. The consumer checks the
profile identity, all twelve option values, the exact 157-token public gonol
invariants and digest, and the required producer types. A mismatch produces
typed suspension.

## Input contract

Pass the complete corpus as an ordered sequence of exact speaker turns:

```python
result = edcm.build_default_layers().run({
    "source_ref": "corpus://example",
    "transcript": "A: word  gonol\nB: é",
    "ucns_turns": (
        ("A", "word  gonol"),
        ("B", "é"),
    ),
})
```

`transcript` remains EDCM measurement input. `ucns_turns` is independently
authoritative for UCNS profile observation. The adapter does not reconstruct
speaker boundaries from flattened text, because doing so would invent support
units.

The adapter observes every supplied turn. It does not sample, truncate, case
fold, normalize Unicode, fold whitespace, or discard punctuation or
out-of-alphabet code points.

## Fixed option configuration

```text
carrier_requirement: mobius-origin-hidden-zero
corpus_execution: full-corpus
gonol_initiation: mobius-twist
nesting_boundary: superpositioned-space
normalization: none-preserve-source
occurrence_operation: ordered-concatenation
out_of_alphabet: retain-and-report
profile_scope: edcm-only
smallest_gonol: word
support: one-unit-per-speaker-turn
token_alphabet: public-gonol-157
token_identity: unicode-code-point
```

Maximal ordered non-SPACE sequences are word gonols. Every exact SPACE remains
a token and an explicit superpositioned nesting boundary. Every new word gonol
records a Möbius-twist initiation event. That event is evidence of the selected
interpretation; it is not a supplied formal coordinate construction.

## Result and authority boundary

Exact output is attached at:

```text
edcm_result.ucns_profile_observation
```

It includes the profile and source identities, full options, observation
digest, all turns in order, exact raw text, segments, token/code-point
positions, word and boundary counts, unit support, and retained
out-of-alphabet evidence.

The following remain typed `NA` or false:

```text
ucns_geometry_identity
ucns_factorization_evidence
ucns_bridge_record_attached
ucns_theorem_status_attached
proof_status_transfers_to_measurement_validity
```

The retired ordered-occurrence bridge, live `UCNSObject`, and factorization
input forms fail closed. Profile observations do not become geometry merely
because both surfaces use UCNS identifiers.

## Historical experiment epoch

The v0.1–v0.4 joint experiments remain reproducible at:

```text
The-Interdependency/ucns@5331ae9a4cf7eddfa1de72b8caed28e2358cc0ed
python -m pip install -e .[dev,ucns-experiments]
```

Those reports are historical evidence. They are not rewritten to the current
runtime profile, and their support, product-character, breadth, and structural
view candidates remain scoped to their recorded epoch.

## hmmm

The executable profile establishes exact corpus observations and exposes where
the 157-token alphabet or current word boundary interpretation is incomplete.
Formal Möbius coordinates, higher-gonol composition, and any projection from
observations into geometry or scalar claims remain open and must be learned
from full real-system corpus runs rather than collapsed early.
