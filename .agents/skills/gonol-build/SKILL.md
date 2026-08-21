---
name: gonol-build
description: Construction, closure, and replay contract for gonols across UCNS and EDCM. Load this when building or reviewing UCNS geometry used by gonols, or building EDCM character, word, definition, or recursive-relation gonols. UCNS owns geometry; EDCM owns text construction. The required EDCM order is characters -> words -> definitions -> recursive gonol relations. Pronunciation is not required unless an explicitly declared later experiment makes it part of the construction. Do not load for unrelated geometry, ordinary prose editing, or measurement over already-closed gonols.
---

# gonol-build

Use this skill to keep gonol construction on the declared architecture and nothing else.

## Authority

```text
UCNS      = geometry
EDCM      = text-domain gonol construction
skill-lib = construction/replay discipline
```

Resolve the current UCNS and EDCM authorities before building. Do not move text semantics into UCNS or invent geometry in EDCM.

## EDCM construction contract

```text
characters -> words -> definitions -> recursive gonol relations
```

This order is load-bearing.

- Every admitted character is a gonol.
- Ordered character gonols close into a word gonol.
- A closed word gonol is atomic at the consuming scale while its constituent identities, order, multiplicity, source positions, and provenance remain recoverable.
- Definition gonols are constructed from the applicable closed word gonols and exact source definition evidence.
- Recursive relations are constructed from already-closed gonols without reopening or erasing their internal structure.

Do not insert another required stage into this sequence unless the governing contract is explicitly changed.

## Pronunciation boundary

Pronunciation is not required for this construction. Pronunciation, phonetic spelling, IPA, audio, or other sound representations must not alter gonol identity, closure, ordering, or relations unless a later explicitly declared experiment makes phonology part of its construction.

Source pronunciation data may remain source metadata. It is not a dependency of the current build.

## Construction invariant

At every scale:

```text
ordered eligible gonols
-> authorized UCNS geometric relation/application
-> closure
-> deterministic identity + provenance receipt
-> atomic participation at the next declared scale
```

Preserve exact source identity, occurrence order, multiplicity, and provenance. Do not normalize, deduplicate, infer relations, or substitute tokens, embeddings, hashes, or another representation for gonol identity unless the active contract explicitly authorizes it.

If required UCNS geometry is unresolved, preserve that boundary as `hmmm`; do not fill it with an invented rule.

## Candidate boundary

An unresolved constructor is permission to construct a named, bounded candidate; it does not block declared experimentation. It blocks promotion beyond the evidence, not construction or testing.

## Completion and replay

Before a full run, preflight the resources required to finish it. Once a healthy admitted run begins, let it reach its natural terminal condition unless a genuine safety/resource boundary or preregistered load-bearing stop condition fires. Do not add arbitrary wall-clock limits.

A completion claim requires:

1. exact UCNS, EDCM, source/profile, and constructor identities;
2. the complete declared source scope;
3. deterministic construction receipts; and
4. independent complete replay where replay is required by the governing protocol.

Replay establishes reproducibility of that construction only. It does not by itself establish semantic quality, measurement validity, cognition claims, or canon outside the declared scope.

## Usage guidance

For text construction, start in EDCM and consume current UCNS geometry.

```text
UCNS: geometry
EDCM: characters -> words -> definitions -> recursive gonol relations
```

When a word closes, use that word gonol atomically at the next scale. Ignore pronunciation unless a future explicit construction says otherwise.

## hmmm

- exact UCNS geometric operations that remain unresolved in current implementation;
- any future construction that explicitly adds phonology or another stage;
- any recursive relation whose governing source or geometry is not yet established.
