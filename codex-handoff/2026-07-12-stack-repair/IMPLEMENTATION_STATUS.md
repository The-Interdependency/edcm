# EDCM stack repair — implementation status

Updated: 2026-07-12

This ledger tracks evidence against `REQUIRED_CHANGES.md` and `COMPLETED_LOOKS_LIKE.md`. A checked item means implemented on a merged or active repair branch with named tests or CI evidence; it does not mean the entire repair is complete.

## Completed or active

- [x] Authoritative package metadata, version, build system, typed marker, frozen canon package data, and development dependencies — merged in PR #15.
- [x] Python 3.11–3.13 base tests, source/wheel build, `twine check`, clean-wheel install, and installed public-API smoke gate — merged in PR #15.
- [x] EDCM-owned UCNS adapter protocol and actual public-surface implementation — active repair branch.
- [x] Direct missing UCNS distinguished from adapter construction/import/schema failure — active repair branch.
- [x] Actual `ucns.UCNSObject` stable hash, canonical schema, structure, and domain prerequisite metadata survive the EDCM path — active repair branch.
- [x] UCNS package availability, adapter activation, object attachment, scope metadata, negative certification, and theorem status are reported independently — active repair branch.
- [x] Transcript-only semantics is explicit and provenance-bearing rather than silently called `default` — active repair branch.
- [x] Installed `edcmbone` no longer silently overrides maintained `edcm.measurement` — active repair branch.
- [x] EDCM is declared the maintained measurement authority in code, README, agent instructions, and the consolidation record — active repair branch.
- [x] Consolidation source commit and compatibility policy are machine-readable through `edcm.measurement.MEASUREMENT_AUTHORITY` — active repair branch.
- [x] Actual UCNS integration CI is pinned to a specific UCNS commit and separated from base-package CI — active repair branch.

## Not yet complete

- [ ] Add source-of-truth drift and frozen-canon integrity checks.
- [ ] Add the versioned immutable METAPAT semantic-envelope adapter.
- [ ] Add METAPAT-only and full UCNS/METAPAT/EDCM shared-stack CI jobs.
- [ ] Create the final result envelope separating source evidence, METAPAT constraints, UCNS geometry, EDCM policy identity, implementation/fallback provenance, readouts, `NA`, and unresolved fields.
- [ ] Add official serialized UCNS bridge-record ingestion beyond live `UCNSObject` / `object_record` attachment.
- [ ] Attach negative-certification and theorem-status evidence only through validated evidence-bearing envelopes.
- [ ] Reconcile remaining MODULE_BUILD, DOCS, CAPABILITIES, BOUNDARIES, CONTRACTS, DEPENDENCIES, OWNERS, and skill-lib declarations.
- [ ] Add repo-local skill-lib drift and msdmd gates.

## Preserved frontier

Contact convergence, DA geometry correlation, cadence admission from text, and semantic-label-to-operating-state inference remain non-operational. No placeholder values or language-model judgments have been added.

## hmmm

The serialized UCNS bridge-record schema and the immutable METAPAT semantic envelope must be consumed from their actual canonical repositories rather than invented inside EDCM.
