# EDCM–UCNS integration boundary

## Current runtime profile

EDCM optionally consumes the exact EDCM-only observation profile at:

```text
The-Interdependency/ucns@872f53571d5dc2f133ff1813b7bdffd3a9c309f8
profile: ucns.profile.edcm-word-gonol/0.2.0
full-corpus gate: ucns.edcm.full-corpus-execution/0.14.1
```

Install it with:

```text
python -m pip install -e .[dev,ucns-profile]
```

Package presence alone does not activate a lookalike. Before accepting the
profile, the consumer requires the pinned UCNS commit from producer-owned
identity or PEP 610 installed-distribution metadata. A local editable install
must resolve to a clean checkout of the declared UCNS repository at that exact
commit. The consumer then checks the profile identity, all fourteen option
values, the exact 157-token public gonol invariants and digest, the source domain, the pinned
`unicode-white-space-origin-v1` assignment policy, all 25 exact SPACE source
code points, and the required producer types. A mismatch produces typed
suspension.

The admitted MultiWOZ runner additionally requires the exact v0.14.1
full-corpus producer surface. It repeats the authenticated source-native turn
stream, requires iterator exhaustion and the declared turn count, and binds the
execution-generated receipt to the source archive, admission decision, adapter,
privacy treatment, and redaction policy. That receipt opens only
failure-seeking analysis; it does not activate EDCM or METAPAT.
The first admitted seal is recorded by the 2026-07-31 MultiWOZ 2.1
[aggregate report](../experiments/corpora/results/2026-07-31-multiwoz-2.1-ucns-v0.14.1-full.json)
and [completion receipt](../experiments/corpora/receipts/2026-07-31-multiwoz-2.1-ucns-v0.14.1-complete.json).

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
fold, normalize Unicode, rewrite whitespace, or discard punctuation or
out-of-alphabet code points. SPACE equivalence changes only the carrier
assignment: every exact source value and code point remains present as its own
witness.

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
source_domain: unicode-scalar-values
space_assignment: unicode-white-space-origin-v1
support: one-unit-per-speaker-turn
token_alphabet: public-gonol-157
token_identity: unicode-code-point
```

The adapter authenticates the ordered SPACE-source pin and its canonical
identity:

```text
U+0009..U+000D, U+0020, U+0085, U+00A0, U+1680,
U+2000..U+200A, U+2028, U+2029, U+202F, U+205F, U+3000
sha256: a5dc5ec34775d511a02b17911aa385c5d92908ee58749ea16d721cd53d19b944
```

The declared source domain is Unicode scalar values. Surrogate code points
`U+D800`–`U+DFFF` are outside this profile rather than silently counted as
ordinary characters.

Maximal ordered sequences not assigned to carrier position zero are word
gonols. Each code point in the pinned Unicode White_Space set is assigned to
the existing public SPACE carrier at position zero and becomes an explicit
superpositioned nesting boundary. This is carrier equivalence, not Unicode
normalization: a tab remains `U+0009`, a newline remains `U+000A`, and a
non-breaking space remains `U+00A0` in source evidence. Every new word gonol
records a Möbius-twist initiation event. That event is evidence of the selected
interpretation; it is not a supplied formal coordinate construction.

## Result and authority boundary

Exact output is attached at:

```text
edcm_result.ucns_profile_observation
```

It includes the profile and source identities, full options, SPACE-assignment
policy, observation digest, all turns in order, exact raw text, segments, word
and boundary counts, unit support, and retained non-SPACE out-of-alphabet
evidence. Every token record separates:

```text
source_value / source_code_point
carrier_token / carrier_position
```

Canonical token fields include `has_carrier_assignment` and
`is_public_gonol_token`; canonical turn/word unassigned evidence is
`carrier_unassigned`, and a turn records
`has_complete_carrier_assignment`. The legacy `value`, `code_point`,
`alphabet_position`, `in_alphabet`, `out_of_alphabet`, and
`has_complete_alphabet_coverage` keys remain present. `value` and `code_point`
are exact source witnesses, `alphabet_position` is the carrier assignment, and
the other legacy names are compatibility aliases for the canonical carrier
fields.

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

The executable profile establishes exact corpus observations and now resolves
the admitted SPACE manifestations to the Möbius origin. Coverage of true
non-SPACE code points outside the 157-token carrier alphabet remains open.
UCNS v0.19 supplies a nonselected trace-local source-coordinate candidate over
its fixed full producer demonstration, but this adapter does not attach or
consume that evidence. Higher-gonol composition and any projection from observations
into geometry or scalar claims remain open and must be learned from full
real-system corpus runs rather than collapsed early.
