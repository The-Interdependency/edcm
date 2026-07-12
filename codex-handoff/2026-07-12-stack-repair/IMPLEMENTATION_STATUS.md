# EDCM stack repair — implementation status

Updated: 2026-07-12

This ledger tracks evidence against `REQUIRED_CHANGES.md` and `COMPLETED_LOOKS_LIKE.md`. A checked item means implemented on a merged or active repair branch with named tests or CI evidence; it does not mean the entire repair is complete.

## Completed or active

- [x] Authoritative package metadata, version, build system, typed marker, frozen canon package data, and development dependencies — merged in PR #15.
- [x] Python 3.11–3.13 base tests, source/wheel build, `twine check`, clean-wheel install, and installed public-API smoke gate — merged in PR #15.
- [x] EDCM-owned UCNS adapter over actual public surfaces, typed absence, fail-closed schema/object handling, and stable-hash preservation — merged in PR #17.
- [x] UCNS package availability, adapter activation, object attachment, scope metadata, negative certification, and theorem status reported independently — merged in PR #17.
- [x] Installed `edcmbone` cannot override canonical `edcm.measurement`; authority and consolidation provenance are machine-readable — merged in PR #17.
- [x] Canonical METAPAT producer schema and actual-UCNS adapter established in `The-Interdependency/metapat` — merged in METAPAT PR #3.
- [x] EDCM-owned METAPAT consumer validates actual envelope objects, canonical JSON, and canonical mappings through producer constructors — active PR #18.
- [x] METAPAT canon identity, exact source statements/references, constraints, permitted interpretations, unresolved `hmmm`, and provenance digest survive the EDCM path — active PR #18.
- [x] Final `edcm.shared-stack-result` separates source evidence, METAPAT constraints, UCNS geometry, EDCM policy identity, implementation provenance, readouts/`NA`, status evidence, and unresolved constraints — active PR #18.
- [x] Canon or EDCM manifest rotation produces a new epoch identity; transcript measurement remains deterministic — active PR #18.
- [x] Base, UCNS-only, METAPAT-only, full UCNS/METAPAT/EDCM, build, metadata, and clean-wheel CI gates pass — active PR #18.

## Not yet complete

- [ ] Add source-of-truth drift and frozen-canon integrity checks.
- [ ] Add official serialized UCNS bridge-record ingestion beyond live `UCNSObject` / `object_record` attachment.
- [ ] Attach negative-certification and theorem-status evidence only through validated evidence-bearing envelopes.
- [ ] Reconcile remaining MODULE_BUILD, DOCS, CAPABILITIES, BOUNDARIES, CONTRACTS, DEPENDENCIES, OWNERS, and skill-lib declarations.
- [ ] Add repo-local skill-lib drift and msdmd gates.

## Preserved frontier

Contact convergence, DA geometry correlation, cadence admission from text, and semantic-label-to-operating-state inference remain non-operational. No placeholder values or language-model judgments have been added.

## hmmm

The official serialized UCNS bridge-record schema and validated negative-certification/theorem-status evidence envelopes must come from canonical UCNS surfaces rather than being invented inside EDCM.
