# EDCM public-gonol canon correction

Status: retirement completed; lawful non-geometric replacement active.

The replacement is the exact UCNS-owned metadata-free relational carrier pinned
in [`ENGLISH_LEXICAL_FLOOR.md`](ENGLISH_LEXICAL_FLOOR.md). It is representation,
not placement: no fractional angle, hash coordinate, evidence-derived geometry,
or local `UCNSObject` was restored. The retired active modules were removed once
the replacement branch tests passed.

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

The retired EDCM language-placement modules and their entry points were deleted:

```text
assign_affix_gonol
assign_root_gonol
assign_direct_atomic_gonol
superpose_gonols
```

Importing those old modules or names is therefore unavailable; there is no
compatibility stub that can accidentally look like an active placement API.

The active `tools/build_oewn2025_embeddings.py` workflow is a separate,
metadata-free relational construction. It requires exact clean OEWN and UCNS
source checkouts, keeps English identities in external binding files, and emits
no position, face, angle, geometry, measurement, or canon selection. Completed
output can resume only after the exact source manifest, exact artifact file set,
intrinsic carriers, bindings, receipts, and producer identities are revalidated.

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

## Completed migration

1. The UCNS public-gonol promotion was merged and EDCM retained only a strict,
   lazy compatibility view.
2. The old local placement authority and constructors were removed.
3. The bounded lexical consumer bridge was specified separately and pinned to
   an exact UCNS relational producer commit.
4. OEWN construction reopened only through that relational bridge, with the
   source, representation, and claim boundaries recorded independently.

## hmmm

This correction protects the canon by keeping compatibility access and lexical
relational construction on distinct surfaces. The lexical bridge does not
manufacture the unresolved geometric or measurement bridge.
