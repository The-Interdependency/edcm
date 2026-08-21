# EDCM–UCNS integration boundary

## Historical runtime observation profile

EDCM optionally consumes the exact EDCM-only observation profile at:

```text
The-Interdependency/ucns@a98c9e6c69804a8a08d0786b1d8b450bb2c49a97
profile: ucns.profile.edcm-word-gonol/0.2.0
full-corpus gate: ucns.edcm.full-corpus-execution/0.14.1
```

This profile remains the runtime **observation/replay contract** for its sealed corpus path. Its option names, including `smallest_gonol: word`, `token_alphabet`, and `token_identity`, are producer-epoch fields and must remain exact for reproduction. They do **not** define current text-gonol architecture.

The current boundary is instead:

```text
METAPAT   -> affixiation semantics and relational-integration invariants
UCNS      -> gonol geometry, native Möbius/Public Gonol carrier,
             geometrically established operations
EDCM      -> text-domain admission and linguistic/semantic gonol construction
```

For active EDCM text construction, every admitted character is a gonol. See [`GONOL_LANGUAGE_BOUNDARY.md`](GONOL_LANGUAGE_BOUNDARY.md).

Current authority does not retroactively mutate this adapter or its sealed receipts. Historical names and options stay fixed for replay.

Install the historical runtime profile with:

```text
python -m pip install -e .[dev,ucns-profile]
```

Package presence alone does not activate a lookalike. Before accepting the
profile, the consumer requires the pinned UCNS commit from PEP 610
installed-distribution metadata. A non-editable installation must also match
the EDCM-pinned package-file manifest independently of its mutable wheel
`RECORD`. A local editable install must resolve to a clean checkout of the
declared UCNS repository at that exact commit. A
producer-owned commit identity, when exported, is cross-checked against that
installed identity and cannot bypass checkout verification. An explicit UCNS
source checkout supplied to the corpus runner is accepted only when the
imported module is the checkout's exact package path and the same repository,
clean-tree, and commit checks pass. After byte authentication, the consumer
freshly loads the UCNS module graph and rechecks the identity so stale in-memory
code cannot inherit the verified label. It verifies caches only for the active
Python ABI and exact runtime optimization level, including levels above two,
because other cache files cannot execute in that runtime. The
consumer then checks the profile identity, all fourteen option values, the exact
157-token public gonol invariants and digest, the source domain, the pinned
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
authoritative for this historical UCNS profile observation. The adapter does not reconstruct
speaker boundaries from flattened text, because doing so would invent support
units.

The adapter observes every supplied turn. It does not sample, truncate, case
fold, normalize Unicode, rewrite whitespace, or discard punctuation or
out-of-alphabet code points. SPACE equivalence changes only the carrier
assignment: every exact source value and code point remains present as its own
witness.

## Fixed option configuration

The following block is frozen producer-epoch configuration, not current stack
ontology:

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
`U+D800`–`U+DFFF` are outside this historical profile rather than silently counted as
ordinary characters.

Maximal ordered sequences not assigned to carrier position zero are word
gonols under this pinned profile. Each code point in the pinned Unicode
White_Space set is assigned to the existing public SPACE carrier at position
zero and becomes an explicit superpositioned nesting boundary. This is carrier
equivalence, not Unicode normalization: a tab remains `U+0009`, a newline
remains `U+000A`, and a non-breaking space remains `U+00A0` in source evidence.
Every new word gonol records a Möbius-twist initiation event. That event is
evidence of the selected historical profile interpretation; it is not a supplied
formal coordinate construction and does not override the current EDCM rule that every
admitted character is a gonol.

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

`token` here is a frozen schema field, not a current tokenizer abstraction.
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

## Current text-gonol construction boundary

This historical adapter is not the current gonol constructor.

New text-gonol work starts in EDCM and follows the active contract:

- EDCM declares the exact source and character-admission profile;
- every admitted character is a gonol;
- METAPAT supplies affixiation semantics without being redefined downstream;
- UCNS supplies the current gonol/Möbius/Public Gonol geometry;
- unresolved UCNS operations remain `hmmm` rather than being inferred from Unicode names, dictionary definitions, adjacency, glyph shape, or conventional grammar;
- EDCM constructs words, then definitions, then recursive gonol relations while preserving identity, occurrence, order, multiplicity, relation identity, scale, source, and provenance; `edcm.character_word` and `edcm.definition_gonol` are the implemented candidates for those stages;
- completion claims require a deterministic receipt and independent complete replay; and
- EDCM measurement remains a separate projection with explicit information loss and falsifiers.

Do not create a parallel “consumer” that waits for UCNS to own language construction. UCNS is the geometry authority; EDCM is the current text-construction authority.

## Historical experiment epoch

The v0.1–v0.4 joint experiments remain reproducible at:

```text
The-Interdependency/ucns@5331ae9a4cf7eddfa1de72b8caed28e2358cc0ed
python -m pip install -e .[dev,ucns-experiments]
```

Those reports are historical evidence. They are not rewritten to the current
runtime profile or current gonol-language boundary, and their support,
product-character, breadth, and structural view candidates remain scoped to
their recorded epoch.

## Usage guidance

Use this adapter only for artifacts that name its exact pinned historical profile. Do not
repin it to current UCNS merely to make terminology look current.

For new text construction, do not extend this historical adapter. Work in EDCM under [`GONOL_LANGUAGE_BOUNDARY.md`](GONOL_LANGUAGE_BOUNDARY.md), consume current UCNS geometry and METAPAT affixiation semantics, and keep the later EDCM measurement boundary separate.

## hmmm

The executable historical profile establishes exact corpus observations and resolves its
admitted SPACE manifestations to its pinned Möbius-origin interpretation.
Coverage of true non-SPACE code points outside the 157-token carrier alphabet
remains open for that historical profile. UCNS v0.19 supplies a nonselected trace-local
source-coordinate candidate over its fixed demonstration, but this adapter does
not attach or consume that evidence. For current work, the exact EDCM character-admission unit remains profile-specific where not selected, the exact UCNS native Möbius-carrier affixiation/coupling geometry remains unresolved, and EDCM's recursive text-gonol measurement projection, metric, benchmark, and falsifier remain unselected.
