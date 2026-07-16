# EDCM public-gonol canon correction

## Decision

EDCM does not own the public gonol.

The exact public gonol implemented in
`The-Interdependency/a0-betatest@7af8debf6ef3905f01baff02b43d8c3bee16ccbc`
is canon for all UCNS and is being promoted into the UCNS public package.
EDCM is a downstream consumer.

The earlier EDCM language experiment is retired because it:

- rebuilt the 157-position arrangement locally as an EDCM `canon` module;
- reduced glyph sequences and dictionary evidence to hash-selected positions;
- constructed local objects with `Fraction(vertex, 157)` values;
- assigned additional positions and faces from hashes;
- described those outputs as public-gonol/UCNS language embeddings without a
  canon-approved bridge.

Those operations are not the A0 public gonol canon. No new artifacts may be
constructed through them.

## Canon preserved upstream

The UCNS public surface preserves:

```text
arity 157
SPACE/ZERO at fixed position 0
Möbius twist point / seam / system origin
exact public arrangement
faces, chirality, adjacency, and origin-fixed mirror
private transforms that never move position 0
lossless lifted text traversal
full 157-step repeated-character revolution
spaces as emitted seam events
digit "0" as an ordinary nonzero glyph
```

No `k/157`, `2k/157`, arbitrary-origin, or removable-gauge interpretation is
introduced as public-gonol canon.

## Current EDCM behavior

`edcm.language.glyph_floor` is now a lazy compatibility view over the pinned
UCNS public surface. It contains no arrangement construction law.

If the optional canonical UCNS package is absent, accessing the public gonol
raises `UCNSPublicGonolDependencyError`. If the source commit, origin, required
surface, or digest drifts, it raises `UCNSPublicGonolContractError`.

All previous EDCM language-placement entry points now raise
`NonCanonicalLanguagePlacementError`:

```text
assign_affix_gonol
assign_root_gonol
assign_direct_atomic_gonol
superpose_gonols
```

The OEWN corpus workflows and artifact finalizer are removed. The retained
builder command fails before reading OEWN or writing artifacts.

Read-only inspection of already-existing local compatibility objects remains
available so historical data can be identified and migrated deliberately.

## Reopening conditions

Language-gonol construction may reopen only after Erin ratifies an explicit
bridge from the UCNS-owned public gonol into the intended EDCM language object.
That bridge must state exactly what is preserved and must not silently:

- move or normalize away the twist origin;
- substitute hash-derived positions;
- invent angle units or conversion formulas;
- erase lifted-path order or seam crossings;
- convert dictionary semantics into carrier coordinates without an authorized
  mapping;
- transfer UCNS proof status into EDCM measurement validity.

## Migration order

1. Review and merge the UCNS public-gonol promotion.
2. Replace A0's local authority with UCNS imports or strict parity wrappers.
3. Repin EDCM to the merged UCNS commit.
4. Specify the consumer bridge separately.
5. Build simple word-list or OEWN adapters only after the bridge is accepted.

## hmmm

This correction protects the canon by stopping construction. It does not guess
the missing bridge.
